#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

import requests

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from ops.reed_runtime.env import load_runtime_env


def _telegram_api(base: str, token: str, method: str, payload: dict) -> dict:
    url = f"{base}/bot{token}/{method}"
    response = requests.post(url, json=payload, timeout=20)
    data = response.json()
    if response.status_code != 200 or not data.get("ok"):
        raise RuntimeError(f"{method} failed: status={response.status_code} body={data}")
    return data


def _sync_scope(base: str, token: str, scope: dict, dry_run: bool) -> dict:
    commands = [{"command": "menu", "description": "Open launcher menu"}]
    if dry_run:
        return {
            "scope": scope,
            "deleted": True,
            "set_commands": commands,
            "dry_run": True,
        }
    _telegram_api(base, token, "deleteMyCommands", {"scope": scope})
    _telegram_api(base, token, "setMyCommands", {"scope": scope, "commands": commands})
    return {
        "scope": scope,
        "deleted": True,
        "set_commands": commands,
        "dry_run": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Force REED DM menu to /menu only")
    parser.add_argument("--dry-run", action="store_true", help="Print payloads without calling Telegram API")
    args = parser.parse_args()

    load_runtime_env()
    token = (
        os.environ.get("TELEGRAM_BOT_TOKEN")
        or os.environ.get("REED_BOT_TOKEN")
        or os.environ.get("SCHEDULER_BOT_TOKEN")
        or ""
    ).strip()
    if not token:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "missing bot token (TELEGRAM_BOT_TOKEN/REED_BOT_TOKEN/SCHEDULER_BOT_TOKEN)",
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 1

    api_base = os.environ.get("TELEGRAM_API_BASE", "https://api.telegram.org").rstrip("/")
    scopes = [
        {"type": "default"},
        {"type": "all_private_chats"},
    ]
    try:
        results = [_sync_scope(api_base, token, scope, args.dry_run) for scope in scopes]
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2, ensure_ascii=False))
        return 1

    print(json.dumps({"ok": True, "api_base": api_base, "results": results}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
