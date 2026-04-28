#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from ops.reed_runtime.audit import tail_events
from ops.reed_runtime.approvals import classify_action
from ops.reed_runtime.cron_engine import initialize_state, list_state_jobs, run_job, set_paused, tick
from ops.reed_runtime.cron import list_cron_jobs
from ops.reed_runtime.doctor import doctor_summary
from ops.reed_runtime.memory import get_memory_store
from ops.reed_runtime.paths import ensure_state_dirs
from ops.reed_runtime.recall import add_event, search_events
from ops.reed_runtime.status import format_status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="REED runtime foundation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Print REED runtime status")

    memory_parser = subparsers.add_parser("memory", help="Manage operational/user memory")
    memory_sub = memory_parser.add_subparsers(dest="action", required=True)
    for action in ("list",):
        action_parser = memory_sub.add_parser(action)
        action_parser.add_argument("--target", default="operational")
    add_parser = memory_sub.add_parser("add")
    add_parser.add_argument("--target", default="operational")
    add_parser.add_argument("--content", required=True)
    replace_parser = memory_sub.add_parser("replace")
    replace_parser.add_argument("--target", default="operational")
    replace_parser.add_argument("--old-text", required=True)
    replace_parser.add_argument("--content", required=True)
    remove_parser = memory_sub.add_parser("remove")
    remove_parser.add_argument("--target", default="operational")
    remove_parser.add_argument("--old-text", required=True)

    recall_parser = subparsers.add_parser("recall", help="Manage session recall")
    recall_sub = recall_parser.add_subparsers(dest="action", required=True)
    recall_add = recall_sub.add_parser("add")
    recall_add.add_argument("--session-key", required=True)
    recall_add.add_argument("--lane", required=True)
    recall_add.add_argument("--role", required=True)
    recall_add.add_argument("--content", required=True)
    recall_add.add_argument("--metadata", default="{}")
    recall_search = recall_sub.add_parser("search")
    recall_search.add_argument("--query", required=True)
    recall_search.add_argument("--limit", type=int, default=10)

    cron_parser = subparsers.add_parser("cron", help="Inspect cron registry")
    cron_sub = cron_parser.add_subparsers(dest="action", required=True)
    cron_sub.add_parser("list")
    cron_sub.add_parser("init")
    cron_sub.add_parser("tick")
    cron_run = cron_sub.add_parser("run")
    cron_run.add_argument("--job-id", required=True)
    cron_pause = cron_sub.add_parser("pause")
    cron_pause.add_argument("--job-id", required=True)
    cron_resume = cron_sub.add_parser("resume")
    cron_resume.add_argument("--job-id", required=True)
    cron_sub.add_parser("state")

    audit_parser = subparsers.add_parser("audit", help="Inspect audit trail")
    audit_sub = audit_parser.add_subparsers(dest="action", required=True)
    audit_tail = audit_sub.add_parser("tail")
    audit_tail.add_argument("--limit", type=int, default=20)

    approvals_parser = subparsers.add_parser("approvals", help="Check approval policy for an action")
    approvals_sub = approvals_parser.add_subparsers(dest="action", required=True)
    approvals_check = approvals_sub.add_parser("check")
    approvals_check.add_argument("--action-name", required=True)

    doctor_parser = subparsers.add_parser("doctor", help="Run REED runtime health checks")
    doctor_sub = doctor_parser.add_subparsers(dest="action", required=True)
    doctor_sub.add_parser("run")

    return parser


def handle_memory(args: argparse.Namespace) -> int:
    store = get_memory_store(args.target)
    if args.action == "list":
        payload = {
            "target": store.target,
            "usage": {"chars": store.usage()[0], "limit": store.usage()[1]},
            "entries": store.list_entries(),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    if args.action == "add":
        store.add(args.content)
        return 0
    if args.action == "replace":
        store.replace(args.old_text, args.content)
        return 0
    if args.action == "remove":
        store.remove(args.old_text)
        return 0
    raise SystemExit(f"unknown memory action: {args.action}")


def handle_recall(args: argparse.Namespace) -> int:
    if args.action == "add":
        try:
            metadata = json.loads(args.metadata)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid --metadata JSON: {exc}") from exc
        add_event(args.session_key, args.lane, args.role, args.content, metadata)
        return 0
    if args.action == "search":
        results = [
            {
                "created_at": result.created_at,
                "session_key": result.session_key,
                "lane": result.lane,
                "role": result.role,
                "content": result.content,
                "metadata": result.metadata,
            }
            for result in search_events(args.query, args.limit)
        ]
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0
    raise SystemExit(f"unknown recall action: {args.action}")


def handle_cron(args: argparse.Namespace) -> int:
    if args.action == "list":
        payload = [
            {
                "job_id": job.job_id,
                "channel": job.channel,
                "goal": job.goal,
                "type": job.kind,
                "prompt_file": job.prompt_file,
                "phase_1_status": job.phase_1_status,
            }
            for job in list_cron_jobs()
        ]
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    if args.action == "init":
        print(json.dumps(initialize_state(force=True), indent=2, ensure_ascii=False))
        return 0
    if args.action == "tick":
        print(json.dumps(tick(), indent=2, ensure_ascii=False))
        return 0
    if args.action == "run":
        print(json.dumps(run_job(args.job_id, manual=True), indent=2, ensure_ascii=False))
        return 0
    if args.action == "pause":
        print(json.dumps(set_paused(args.job_id, True), indent=2, ensure_ascii=False))
        return 0
    if args.action == "resume":
        print(json.dumps(set_paused(args.job_id, False), indent=2, ensure_ascii=False))
        return 0
    if args.action == "state":
        print(json.dumps(list_state_jobs(), indent=2, ensure_ascii=False))
        return 0
    raise SystemExit(f"unknown cron action: {args.action}")


def handle_audit(args: argparse.Namespace) -> int:
    if args.action == "tail":
        print(json.dumps(tail_events(args.limit), indent=2, ensure_ascii=False))
        return 0
    raise SystemExit(f"unknown audit action: {args.action}")


def handle_approvals(args: argparse.Namespace) -> int:
    if args.action == "check":
        decision = classify_action(args.action_name)
        print(json.dumps(decision.__dict__, indent=2, ensure_ascii=False))
        return 0
    raise SystemExit(f"unknown approvals action: {args.action}")


def handle_doctor(args: argparse.Namespace) -> int:
    if args.action == "run":
        summary = doctor_summary()
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0 if summary["ok"] else 1
    raise SystemExit(f"unknown doctor action: {args.action}")


def main() -> int:
    ensure_state_dirs()
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "status":
        print(format_status())
        return 0
    if args.command == "memory":
        return handle_memory(args)
    if args.command == "recall":
        return handle_recall(args)
    if args.command == "cron":
        return handle_cron(args)
    if args.command == "audit":
        return handle_audit(args)
    if args.command == "approvals":
        return handle_approvals(args)
    if args.command == "doctor":
        return handle_doctor(args)
    raise SystemExit(f"unknown command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
