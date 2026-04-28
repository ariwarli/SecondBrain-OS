from __future__ import annotations

import json
from pathlib import Path

from .policy import infer_approval_status
from .store import Store


def ensure_store(root: Path) -> Store:
    store = Store(root)
    store.init()
    return store


def intake_goal(root: Path, goal_title: str, task: dict, project_id: str = "agent-os-v1") -> tuple[int, int]:
    store = ensure_store(root)
    goal_id = store.create_goal(goal_title, project_id)
    try:
        task_id = store.create_task(
            goal_id=goal_id,
            description=task["description"],
            task_type=task["task_type"],
            payload=task["payload"],
            verification_spec=task["verification_spec"],
            risk_level=task.get("risk_level", "low"),
            trust_domain=task.get("trust_domain", "general"),
            budget_limit=task.get("budget_limit", 0),
            approval_status=task.get(
                "approval_status",
                infer_approval_status(task["task_type"], task.get("risk_level", "low")),
            ),
        )
    except Exception:
        store.delete_goal(goal_id)
        raise
    store.log_event("goal_intake", goal_id, None, {"goal_title": goal_title})
    store.log_event("task_created", goal_id, task_id, {"task": task["description"]})
    store.add_session(goal_id, task_id, "intake", "ok", "Goal and initial task created")
    return goal_id, task_id


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
