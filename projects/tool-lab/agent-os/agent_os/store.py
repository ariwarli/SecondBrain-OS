from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path

from .schema import SCHEMA_SQL


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class TaskRecord:
    id: int
    goal_id: int
    description: str
    task_type: str
    payload: dict
    verification_spec: dict
    depends_on: list[int]
    priority: int
    risk_level: str
    trust_domain: str
    budget_limit: int
    budget_used: int
    approval_status: str
    status: str
    attempts: int
    evidence_path: str | None


class Store:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.db_path = self.root / "state.sqlite3"
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def init(self) -> None:
        self.conn.executescript(SCHEMA_SQL)
        self._migrate_schema()
        self.conn.commit()

    def _migrate_schema(self) -> None:
        task_columns = {row["name"] for row in self.conn.execute("PRAGMA table_info(tasks)").fetchall()}
        task_migrations = {
            "trust_domain": "ALTER TABLE tasks ADD COLUMN trust_domain TEXT NOT NULL DEFAULT 'general'",
            "budget_limit": "ALTER TABLE tasks ADD COLUMN budget_limit INTEGER NOT NULL DEFAULT 0",
            "budget_used": "ALTER TABLE tasks ADD COLUMN budget_used INTEGER NOT NULL DEFAULT 0",
            "approval_status": "ALTER TABLE tasks ADD COLUMN approval_status TEXT NOT NULL DEFAULT 'not_required'",
        }
        for column, sql in task_migrations.items():
            if column not in task_columns:
                try:
                    self.conn.execute(sql)
                except sqlite3.OperationalError as exc:
                    if "duplicate column name" not in str(exc):
                        raise
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
                status TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create_goal(self, title: str, project_id: str) -> int:
        cur = self.conn.execute(
            "INSERT INTO goals (title, project_id, status, created_at) VALUES (?, ?, ?, ?)",
            (title, project_id, "pending", utc_now()),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def delete_goal(self, goal_id: int) -> None:
        self.conn.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
        self.conn.commit()

    def create_task(
        self,
        goal_id: int,
        description: str,
        task_type: str,
        payload: dict,
        verification_spec: dict,
        depends_on: list[int] | None = None,
        priority: int = 50,
        risk_level: str = "low",
        trust_domain: str = "general",
        budget_limit: int = 0,
        approval_status: str = "not_required",
    ) -> int:
        now = utc_now()
        cur = self.conn.execute(
            """
            INSERT INTO tasks (
                goal_id, description, task_type, payload_json, verification_json,
                depends_on_json, priority, risk_level, trust_domain, budget_limit, budget_used,
                approval_status, status, attempts, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                goal_id,
                description,
                task_type,
                json.dumps(payload),
                json.dumps(verification_spec),
                json.dumps(depends_on or []),
                priority,
                risk_level,
                trust_domain,
                budget_limit,
                0,
                approval_status,
                "pending",
                0,
                now,
                now,
            ),
        )
        self.conn.commit()
        if approval_status == "pending":
            self.conn.execute(
                "INSERT INTO approvals (task_id, status, reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (int(cur.lastrowid), "pending", "policy gate before dispatch", now, now),
            )
            self.conn.commit()
        return int(cur.lastrowid)

    def log_event(self, event_type: str, goal_id: int | None, task_id: int | None, details: dict) -> None:
        self.conn.execute(
            "INSERT INTO events (goal_id, task_id, event_type, details_json, created_at) VALUES (?, ?, ?, ?, ?)",
            (goal_id, task_id, event_type, json.dumps(details), utc_now()),
        )
        self.conn.commit()

    def add_session(self, goal_id: int | None, task_id: int | None, phase: str, status: str, summary: str) -> None:
        self.conn.execute(
            "INSERT INTO sessions (goal_id, task_id, phase, status, summary, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (goal_id, task_id, phase, status, summary, utc_now()),
        )
        self.conn.commit()

    def add_learning(self, run_id: str, category: str, summary: str) -> None:
        self.conn.execute(
            "INSERT INTO learnings (run_id, category, summary, created_at) VALUES (?, ?, ?, ?)",
            (run_id, category, summary, utc_now()),
        )
        self.conn.commit()

    def list_tasks(self) -> list[TaskRecord]:
        rows = self.conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
        return [self._row_to_task(row) for row in rows]

    def claim_ready_task(self) -> TaskRecord | None:
        rows = self.conn.execute(
            "SELECT * FROM tasks WHERE status = 'pending' ORDER BY priority ASC, id ASC"
        ).fetchall()
        for row in rows:
            task = self._row_to_task(row)
            if task.approval_status not in {"not_required", "approved"}:
                continue
            if task.budget_limit and task.budget_used >= task.budget_limit:
                continue
            if self._dependencies_ready(task.depends_on):
                self.conn.execute(
                    "UPDATE tasks SET status = ?, attempts = attempts + 1, updated_at = ? WHERE id = ?",
                    ("running", utc_now(), task.id),
                )
                self.conn.commit()
                return self.get_task(task.id)
        return None

    def _dependencies_ready(self, depends_on: list[int]) -> bool:
        if not depends_on:
            return True
        placeholders = ",".join("?" for _ in depends_on)
        rows = self.conn.execute(
            f"SELECT status FROM tasks WHERE id IN ({placeholders})",
            depends_on,
        ).fetchall()
        statuses = {row["status"] for row in rows}
        return statuses == {"verified"}

    def get_task(self, task_id: int) -> TaskRecord:
        row = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            raise KeyError(task_id)
        return self._row_to_task(row)

    def update_task_status(self, task_id: int, status: str, evidence_path: str | None = None) -> None:
        self.conn.execute(
            "UPDATE tasks SET status = ?, evidence_path = ?, updated_at = ? WHERE id = ?",
            (status, evidence_path, utc_now(), task_id),
        )
        self.conn.commit()

    def update_task_budget_used(self, task_id: int, budget_used: int) -> None:
        self.conn.execute(
            "UPDATE tasks SET budget_used = ?, updated_at = ? WHERE id = ?",
            (budget_used, utc_now(), task_id),
        )
        self.conn.commit()

    def set_approval_status(self, task_id: int, status: str, reason: str) -> None:
        now = utc_now()
        self.conn.execute(
            "UPDATE tasks SET approval_status = ?, updated_at = ? WHERE id = ?",
            (status, now, task_id),
        )
        row = self.conn.execute("SELECT id FROM approvals WHERE task_id = ?", (task_id,)).fetchone()
        if row is None:
            self.conn.execute(
                "INSERT INTO approvals (task_id, status, reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (task_id, status, reason, now, now),
            )
        else:
            self.conn.execute(
                "UPDATE approvals SET status = ?, reason = ?, updated_at = ? WHERE task_id = ?",
                (status, reason, now, task_id),
            )
        self.conn.commit()

    def list_pending_approvals(self) -> list[sqlite3.Row]:
        return self.conn.execute(
            """
            SELECT a.task_id, a.status, a.reason, t.description, t.task_type, t.risk_level
            FROM approvals a
            JOIN tasks t ON t.id = a.task_id
            WHERE a.status = 'pending'
            ORDER BY a.task_id
            """
        ).fetchall()

    def update_goal_status(self, goal_id: int) -> None:
        rows = self.conn.execute("SELECT status FROM tasks WHERE goal_id = ?", (goal_id,)).fetchall()
        statuses = {row["status"] for row in rows}
        if not statuses:
            goal_status = "pending"
        elif statuses == {"verified"}:
            goal_status = "verified"
        elif "failed" in statuses:
            goal_status = "failed"
        elif "running" in statuses:
            goal_status = "running"
        else:
            goal_status = "pending"
        self.conn.execute("UPDATE goals SET status = ? WHERE id = ?", (goal_status, goal_id))
        self.conn.commit()

    def goal_summary(self) -> list[sqlite3.Row]:
        return self.conn.execute(
            """
            SELECT g.id, g.title, g.status,
                   COUNT(t.id) AS task_count,
                   SUM(CASE WHEN t.status = 'verified' THEN 1 ELSE 0 END) AS verified_count
            FROM goals g
            LEFT JOIN tasks t ON t.goal_id = g.id
            GROUP BY g.id
            ORDER BY g.id
            """
        ).fetchall()

    def prune_empty_pending_goals(self) -> int:
        cur = self.conn.execute(
            """
            DELETE FROM goals
            WHERE status = 'pending'
              AND id NOT IN (SELECT DISTINCT goal_id FROM tasks)
            """
        )
        self.conn.commit()
        return int(cur.rowcount)

    def latest_events(self, limit: int = 20) -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM events ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()

    def metrics(self) -> dict[str, int]:
        task_total = self.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        verified_total = self.conn.execute("SELECT COUNT(*) FROM tasks WHERE status = 'verified'").fetchone()[0]
        goals_total = self.conn.execute("SELECT COUNT(*) FROM goals").fetchone()[0]
        learning_total = self.conn.execute("SELECT COUNT(*) FROM learnings").fetchone()[0]
        return {
            "goals_total": int(goals_total),
            "tasks_total": int(task_total),
            "tasks_verified": int(verified_total),
            "learning_total": int(learning_total),
        }

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> TaskRecord:
        return TaskRecord(
            id=int(row["id"]),
            goal_id=int(row["goal_id"]),
            description=str(row["description"]),
            task_type=str(row["task_type"]),
            payload=json.loads(row["payload_json"]),
            verification_spec=json.loads(row["verification_json"]),
            depends_on=json.loads(row["depends_on_json"]),
            priority=int(row["priority"]),
            risk_level=str(row["risk_level"]),
            trust_domain=str(row["trust_domain"]),
            budget_limit=int(row["budget_limit"]),
            budget_used=int(row["budget_used"]),
            approval_status=str(row["approval_status"]),
            status=str(row["status"]),
            attempts=int(row["attempts"]),
            evidence_path=row["evidence_path"],
        )
