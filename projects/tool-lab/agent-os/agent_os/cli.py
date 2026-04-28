from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

from .engine import intake_goal
from .store import Store
from .worker import run_once


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def mirror_status(root: Path) -> None:
    store = Store(root)
    store.init()
    metrics = store.metrics()
    goals = store.goal_summary()
    approvals = store.list_pending_approvals()
    lines = [
        "# Status",
        "",
        f"- Phase: milestone 2 policy/budget baseline",
        f"- Goals total: {metrics['goals_total']}",
        f"- Tasks total: {metrics['tasks_total']}",
        f"- Tasks verified: {metrics['tasks_verified']}",
        f"- Learnings written: {metrics['learning_total']}",
        "",
        "## Goals",
        "",
    ]
    for goal in goals:
        lines.append(
            f"- Goal {goal['id']}: {goal['title']} | status={goal['status']} | verified={goal['verified_count']}/{goal['task_count']}"
        )
    lines.extend(["", "## Pending Approvals", ""])
    if approvals:
        for approval in approvals:
            lines.append(
                f"- Task {approval['task_id']}: {approval['description']} | type={approval['task_type']} | risk={approval['risk_level']} | reason={approval['reason']}"
            )
    else:
        lines.append("- none")
    (root / "status.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_init(_: argparse.Namespace) -> int:
    root = project_root()
    store = Store(root)
    store.init()
    store.prune_empty_pending_goals()
    mirror_status(root)
    return 0


def cmd_intake(args: argparse.Namespace) -> int:
    root = project_root()
    fixture = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    intake_goal(root, fixture["goal_title"], fixture["task"])
    mirror_status(root)
    return 0


def cmd_run_once(_: argparse.Namespace) -> int:
    root = project_root()
    run_once(root)
    mirror_status(root)
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    root = project_root()
    store = Store(root)
    store.init()
    store.set_approval_status(args.task_id, "approved", args.reason)
    store.log_event("task_approved", None, args.task_id, {"reason": args.reason})
    mirror_status(root)
    return 0


def cmd_list_approvals(_: argparse.Namespace) -> int:
    root = project_root()
    store = Store(root)
    store.init()
    for approval in store.list_pending_approvals():
        print(
            f"task={approval['task_id']} type={approval['task_type']} risk={approval['risk_level']} reason={approval['reason']} desc={approval['description']}"
        )
    return 0


def cmd_demo(_: argparse.Namespace) -> int:
    root = project_root()
    store = Store(root)
    store.init()
    fixture_path = root / "evals" / "fixtures" / "closed_loop_demo.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    intake_goal(root, fixture["goal_title"], fixture["task"])
    run_once(root)
    mirror_status(root)
    return 0


def cmd_run_eval(args: argparse.Namespace) -> int:
    root = project_root()
    fixture = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    temp_root = Path(tempfile.mkdtemp(prefix="agent-os-eval-"))
    try:
        for dirname in ("artifacts", "memory", "runs"):
            (temp_root / dirname).mkdir(parents=True, exist_ok=True)
        store = Store(temp_root)
        store.init()
        intake_goal(temp_root, fixture["goal_title"], fixture["task"])
        result = run_once(temp_root)
        ok = bool(result.get("verification", {}).get("ok"))
        eval_summary = {
            "fixture": str(Path(args.fixture).name),
            "ok": ok,
            "result": result,
        }
        out_path = root / "evals" / f"{Path(args.fixture).stem}-last.json"
        out_path.write_text(json.dumps(eval_summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(eval_summary, indent=2))
        return 0 if ok else 1
    finally:
        shutil.rmtree(temp_root)


def cmd_status(_: argparse.Namespace) -> int:
    root = project_root()
    store = Store(root)
    store.init()
    store.prune_empty_pending_goals()
    mirror_status(root)
    print((root / "status.md").read_text(encoding="utf-8"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agent OS v1 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init")
    init_parser.set_defaults(func=cmd_init)

    intake_parser = sub.add_parser("intake")
    intake_parser.add_argument("fixture", help="Path to JSON fixture")
    intake_parser.set_defaults(func=cmd_intake)

    run_parser = sub.add_parser("run-once")
    run_parser.set_defaults(func=cmd_run_once)

    approve_parser = sub.add_parser("approve")
    approve_parser.add_argument("task_id", type=int)
    approve_parser.add_argument("--reason", default="manual approval")
    approve_parser.set_defaults(func=cmd_approve)

    approvals_parser = sub.add_parser("list-approvals")
    approvals_parser.set_defaults(func=cmd_list_approvals)

    demo_parser = sub.add_parser("demo")
    demo_parser.set_defaults(func=cmd_demo)

    eval_parser = sub.add_parser("run-eval")
    eval_parser.add_argument("fixture", help="Path to eval JSON fixture")
    eval_parser.set_defaults(func=cmd_run_eval)

    status_parser = sub.add_parser("status")
    status_parser.set_defaults(func=cmd_status)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
