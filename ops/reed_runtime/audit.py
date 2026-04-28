from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from .paths import AUDIT_LOG_PATH, ensure_state_dirs


def log_event(action: str, payload: dict[str, Any]) -> None:
    ensure_state_dirs()
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "payload": payload,
    }
    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def tail_events(limit: int = 20) -> list[dict[str, Any]]:
    if not AUDIT_LOG_PATH.exists():
        return []
    lines = AUDIT_LOG_PATH.read_text(encoding="utf-8").splitlines()
    events: list[dict[str, Any]] = []
    for line in lines[-limit:]:
        if not line.strip():
            continue
        events.append(json.loads(line))
    return events
