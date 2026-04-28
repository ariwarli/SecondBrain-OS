from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path

from .memory import append_memory
from .policy import validate_shell_command
from .store import Store
from .verifier import verify


def run_once(root: Path) -> dict:
    store = Store(root)
    store.init()
    task = store.claim_ready_task()
    if task is None:
        return {"status": "idle"}

    store.log_event("task_claimed", task.goal_id, task.id, {"task_type": task.task_type})
    run_id = datetime.now().strftime("%Y%m%dT%H%M%S")
    run_dir = root / "runs"
    run_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = run_dir / f"{run_id}-task-{task.id}.json"

    result = {"task_id": task.id, "goal_id": task.goal_id, "run_id": run_id, "task_type": task.task_type}
    try:
        if task.task_type == "write_file":
            target = root / task.payload["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(task.payload["content"], encoding="utf-8")
            result["execution"] = {"written_file": str(target.relative_to(root))}
            store.update_task_budget_used(task.id, 1)
        elif task.task_type == "shell_command":
            command = task.payload["command"]
            argv = validate_shell_command(command)
            completed = subprocess.run(
                argv,
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            result["execution"] = {
                "command": argv,
                "exit_code": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
            store.update_task_budget_used(task.id, len(argv))
            if task.verification_spec.get("type") == "stdout_contains":
                task.verification_spec["stdout"] = completed.stdout
        else:
            raise ValueError(f"unsupported task_type: {task.task_type}")

        ok, message = verify(root, task.verification_spec)
        result["verification"] = {"ok": ok, "message": message}
        if not ok:
            store.update_task_status(task.id, "failed", str(evidence_path.relative_to(root)))
            store.log_event("task_verification_failed", task.goal_id, task.id, {"message": message})
            store.add_session(task.goal_id, task.id, "verify", "failed", message)
            store.add_learning(run_id, "verification_gap", message)
            append_memory(root, f"Verification failed for task {task.id}: {message}")
        else:
            store.update_task_status(task.id, "verified", str(evidence_path.relative_to(root)))
            store.log_event("task_verified", task.goal_id, task.id, {"message": message})
            store.add_session(task.goal_id, task.id, "verify", "ok", message)
            store.add_learning(run_id, "milestone_progress", "Closed-loop task verified successfully")
            append_memory(root, f"Verified task {task.id} for goal {task.goal_id}: {message}")
        store.update_goal_status(task.goal_id)
    except Exception as exc:
        result["error"] = str(exc)
        store.update_task_status(task.id, "failed", str(evidence_path.relative_to(root)))
        store.log_event("task_failed", task.goal_id, task.id, {"error": str(exc)})
        store.add_session(task.goal_id, task.id, "execute", "failed", str(exc))
        store.add_learning(run_id, "execution_failure", str(exc))
        append_memory(root, f"Execution failed for task {task.id}: {exc}")
        store.update_goal_status(task.goal_id)

    evidence_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result
