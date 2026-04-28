#!/usr/bin/env python3
"""
recover_inbox_failed_writes.py

Deteksi tool call `write` yang gagal untuk `inbox/pending/*.md` di session topic Inbox,
lalu pulihkan file yang hilang bila diminta.
"""

import argparse
import json
import os
from dataclasses import dataclass
from typing import Dict, Iterable, List


WORKSPACE = "/home/openclaw/banirisset"
DEFAULT_SESSION_JSONL = (
    "/home/openclaw/.openclaw/agents/reed-archivist/sessions/"
    "7c157168-445d-406b-b3ad-f717fe0be4ad-topic-11.jsonl"
)
PENDING_DIR = os.path.join(WORKSPACE, "inbox", "pending")
WRITE_ERROR = "sandbox pinned mutation helper requires python3 or python"


@dataclass
class FailedWrite:
    tool_call_id: str
    relative_path: str
    absolute_path: str
    content: str
    timestamp: str


def iter_jsonl(path: str) -> Iterable[dict]:
    with open(path, encoding="utf-8") as file_obj:
        for line in file_obj:
            line = line.strip()
            if line:
                yield json.loads(line)


def collect_failed_pending_writes(session_jsonl: str) -> List[FailedWrite]:
    pending_calls: Dict[str, FailedWrite] = {}
    failed: Dict[str, FailedWrite] = {}

    for entry in iter_jsonl(session_jsonl):
        if entry.get("type") != "message":
            continue

        message = entry.get("message", {})
        role = message.get("role")
        content = message.get("content", [])

        if role == "assistant":
            for block in content:
                if block.get("type") != "toolCall" or block.get("name") != "write":
                    continue
                arguments = block.get("arguments", {})
                rel_path = arguments.get("path", "")
                if not rel_path.startswith("inbox/pending/"):
                    continue
                pending_calls[block["id"]] = FailedWrite(
                    tool_call_id=block["id"],
                    relative_path=rel_path,
                    absolute_path=os.path.join(WORKSPACE, rel_path),
                    content=arguments.get("content", ""),
                    timestamp=entry.get("timestamp", ""),
                )

        elif role == "toolResult":
            tool_call_id = message.get("toolCallId")
            failed_write = pending_calls.get(tool_call_id)
            if not failed_write:
                continue
            details = message.get("details", {})
            error_text = details.get("error", "")
            if WRITE_ERROR in error_text:
                failed[tool_call_id] = failed_write

    deduped: Dict[str, FailedWrite] = {}
    for item in failed.values():
        if os.path.exists(item.absolute_path):
            continue
        deduped[item.relative_path] = item
    return list(deduped.values())


def apply_recovery(item: FailedWrite) -> None:
    os.makedirs(os.path.dirname(item.absolute_path), exist_ok=True)
    with open(item.absolute_path, "w", encoding="utf-8") as file_obj:
        file_obj.write(item.content)


def main():
    parser = argparse.ArgumentParser(description="Recover failed inbox pending writes from session logs")
    parser.add_argument("--session-jsonl", default=DEFAULT_SESSION_JSONL, help="Path to Inbox topic session JSONL")
    parser.add_argument("--apply", action="store_true", help="Actually recreate missing files")
    args = parser.parse_args()

    items = collect_failed_pending_writes(args.session_jsonl)
    print(json.dumps(
        [
            {
                "relative_path": item.relative_path,
                "absolute_path": item.absolute_path,
                "timestamp": item.timestamp,
                "status": "recovered" if args.apply else "missing",
            }
            for item in items
        ],
        indent=2,
        ensure_ascii=False,
    ))

    if args.apply:
        for item in items:
            apply_recovery(item)


if __name__ == "__main__":
    main()
