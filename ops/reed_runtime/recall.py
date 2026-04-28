from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .audit import log_event
from .paths import DB_PATH, ensure_state_dirs


def connect() -> sqlite3.Connection:
    ensure_state_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS session_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            session_key TEXT NOT NULL,
            lane TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}'
        )
        """
    )
    conn.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS session_events_fts
        USING fts5(content, session_key, lane, role, content='session_events', content_rowid='id')
        """
    )
    conn.execute(
        """
        CREATE TRIGGER IF NOT EXISTS session_events_ai AFTER INSERT ON session_events BEGIN
          INSERT INTO session_events_fts(rowid, content, session_key, lane, role)
          VALUES (new.id, new.content, new.session_key, new.lane, new.role);
        END
        """
    )
    conn.execute(
        """
        CREATE TRIGGER IF NOT EXISTS session_events_ad AFTER DELETE ON session_events BEGIN
          INSERT INTO session_events_fts(session_events_fts, rowid, content, session_key, lane, role)
          VALUES('delete', old.id, old.content, old.session_key, old.lane, old.role);
        END
        """
    )
    conn.execute(
        """
        CREATE TRIGGER IF NOT EXISTS session_events_au AFTER UPDATE ON session_events BEGIN
          INSERT INTO session_events_fts(session_events_fts, rowid, content, session_key, lane, role)
          VALUES('delete', old.id, old.content, old.session_key, old.lane, old.role);
          INSERT INTO session_events_fts(rowid, content, session_key, lane, role)
          VALUES (new.id, new.content, new.session_key, new.lane, new.role);
        END
        """
    )
    return conn


@dataclass
class RecallResult:
    created_at: str
    session_key: str
    lane: str
    role: str
    content: str
    metadata: dict[str, Any]


def add_event(session_key: str, lane: str, role: str, content: str, metadata: dict[str, Any] | None = None) -> None:
    if not content.strip():
        raise ValueError("content is empty")
    payload = metadata or {}
    ts = datetime.now(timezone.utc).isoformat()
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO session_events(created_at, session_key, lane, role, content, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (ts, session_key, lane, role, content.strip(), json.dumps(payload, ensure_ascii=False)),
        )
        conn.commit()
    log_event(
        "recall.add",
        {
            "session_key": session_key,
            "lane": lane,
            "role": role,
            "content_preview": content.strip()[:120],
        },
    )


def search_events(query: str, limit: int = 10) -> list[RecallResult]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT e.created_at, e.session_key, e.lane, e.role, e.content, e.metadata_json
            FROM session_events_fts f
            JOIN session_events e ON e.id = f.rowid
            WHERE session_events_fts MATCH ?
            ORDER BY e.id DESC
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()
    return [
        RecallResult(
            created_at=row["created_at"],
            session_key=row["session_key"],
            lane=row["lane"],
            role=row["role"],
            content=row["content"],
            metadata=json.loads(row["metadata_json"]),
        )
        for row in rows
    ]


def count_events() -> int:
    with connect() as conn:
        row = conn.execute("SELECT COUNT(*) AS count FROM session_events").fetchone()
    return int(row["count"])
