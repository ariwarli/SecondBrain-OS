from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from pathlib import Path

from .paths import DB_PATH, OP_MEMORY_PATH, SPEC_PATH, STATE_DIR, USER_MEMORY_PATH


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def run_checks() -> list[CheckResult]:
    checks: list[CheckResult] = []
    checks.append(CheckResult("runtime_spec", SPEC_PATH.exists(), str(SPEC_PATH)))
    checks.append(CheckResult("state_dir", STATE_DIR.exists(), str(STATE_DIR)))
    checks.append(CheckResult("operational_memory", OP_MEMORY_PATH.exists(), str(OP_MEMORY_PATH)))
    checks.append(CheckResult("user_memory", USER_MEMORY_PATH.exists(), str(USER_MEMORY_PATH)))
    checks.append(CheckResult("session_recall_db", DB_PATH.exists(), str(DB_PATH)))

    scheduler_token_present = bool(os.environ.get("SCHEDULER_BOT_TOKEN"))
    checks.append(
        CheckResult(
            "scheduler_bot_token_env",
            scheduler_token_present,
            "SCHEDULER_BOT_TOKEN present in environment" if scheduler_token_present else "Missing SCHEDULER_BOT_TOKEN",
        )
    )

    python_ok = Path("/usr/bin/python3").exists() or Path("/opt/homebrew/bin/python3").exists()
    checks.append(CheckResult("python3", python_ok, "python3 executable expected on host"))
    return checks


def doctor_summary() -> dict:
    checks = run_checks()
    return {
        "ok": all(item.ok for item in checks),
        "checks": [asdict(item) for item in checks],
    }
