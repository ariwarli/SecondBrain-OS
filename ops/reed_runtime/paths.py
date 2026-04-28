from __future__ import annotations

from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
AUTOMATION_DIR = WORKSPACE_ROOT / "automation"
SCHEDULER_DIR = WORKSPACE_ROOT / "scheduler"
STATE_DIR = WORKSPACE_ROOT / "state" / "reed-runtime"
MEMORY_DIR = STATE_DIR / "memory"
LOG_DIR = STATE_DIR / "logs"
DB_PATH = STATE_DIR / "session_recall.db"
AUDIT_LOG_PATH = LOG_DIR / "audit.jsonl"
OP_MEMORY_PATH = MEMORY_DIR / "operational_memory.json"
USER_MEMORY_PATH = MEMORY_DIR / "user_profile.json"
SPEC_PATH = AUTOMATION_DIR / "reed-runtime-spec.yaml"
LEGACY_SCHEDULE_PATH = AUTOMATION_DIR / "schedule.yaml"


def ensure_state_dirs() -> None:
    for path in (STATE_DIR, MEMORY_DIR, LOG_DIR):
        path.mkdir(parents=True, exist_ok=True)
