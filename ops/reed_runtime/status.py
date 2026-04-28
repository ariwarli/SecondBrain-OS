from __future__ import annotations

import json
from typing import Any

from .audit import tail_events
from .cron import cron_summary
from .memory import get_memory_store
from .paths import OP_MEMORY_PATH, SCHEDULER_DIR, USER_MEMORY_PATH
from .recall import count_events
from .spec import load_runtime_spec


def build_status() -> dict[str, Any]:
    spec = load_runtime_spec()
    op_usage = get_memory_store("operational").usage()
    user_usage = get_memory_store("user").usage()
    queue_count = len(list((SCHEDULER_DIR / "queue").glob("*.json")))
    archive_count = len(list((SCHEDULER_DIR / "archive").glob("*.json")))

    return {
        "mode": spec.raw.get("mode"),
        "deployment_phase": spec.deployment_phase,
        "channels": {
            "primary": spec.channel_primary,
            "planned": spec.channel_planned,
        },
        "execution": {
            "backends": spec.execution_backends,
            "future_backends": spec.future_backends,
            "tiers": spec.autonomy_tiers,
        },
        "memory": {
            "operational_path": str(OP_MEMORY_PATH),
            "user_path": str(USER_MEMORY_PATH),
            "operational_usage": {"chars": op_usage[0], "limit": op_usage[1]},
            "user_usage": {"chars": user_usage[0], "limit": user_usage[1]},
            "session_recall_events": count_events(),
        },
        "scheduler": {
            "queue_count": queue_count,
            "archive_count": archive_count,
            "summary": cron_summary(),
        },
        "recent_audit_events": tail_events(5),
    }


def format_status() -> str:
    return json.dumps(build_status(), indent=2, ensure_ascii=False)
