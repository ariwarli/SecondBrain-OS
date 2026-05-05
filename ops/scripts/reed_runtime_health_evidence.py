#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_PATH = WORKSPACE_ROOT / "state" / "reed-runtime" / "logs" / "health-evidence.json"


def _run_command(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=WORKSPACE_ROOT, capture_output=True, text=True)
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    payload: Any
    try:
        payload = json.loads(stdout) if stdout else {}
    except json.JSONDecodeError:
        payload = {"raw_stdout": stdout}
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout": payload,
        "stderr": stderr,
    }


def main() -> int:
    EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    checks = {
        "status": _run_command(["python3", "ops/scripts/reed_runtime.py", "status"]),
        "doctor": _run_command(["python3", "ops/scripts/reed_runtime.py", "doctor", "run"]),
        "guardrail": _run_command(["python3", "ops/scripts/model_routing_guardrail.py"]),
        "smoke": _run_command(["python3", "ops/scripts/model_routing_smoke.py"]),
        "command_compliance": _run_command(["python3", "ops/scripts/reed_command_compliance.py"]),
    }
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
    }
    EVIDENCE_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": True, "evidence_path": str(EVIDENCE_PATH)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
