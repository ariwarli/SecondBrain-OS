#!/usr/bin/env python3

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = SCRIPT_DIR / "telegram-config.json"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Config not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def load_prompt(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        raise SystemExit(f"Prompt file not found: {path}")


def chunk_text(text: str, limit: int = 3500) -> list[str]:
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    current = ""
    for paragraph in text.split("\n\n"):
        candidate = paragraph if not current else f"{current}\n\n{paragraph}"
        if len(candidate) <= limit:
            current = candidate
            continue
        if current:
            chunks.append(current)
        if len(paragraph) <= limit:
            current = paragraph
            continue
        start = 0
        while start < len(paragraph):
            chunks.append(paragraph[start : start + limit])
            start += limit
        current = ""
    if current:
        chunks.append(current)
    return chunks


def build_message(
    *,
    job_id: str,
    prompt: str,
    target_bot_username: str | None,
    job_label: str | None,
) -> str:
    parts = []
    if target_bot_username:
        handle = target_bot_username.lstrip("@")
        parts.append(f"@{handle}")
    label = job_label or job_id
    parts.append(f"[JADWAL TUGAS: {label}]")
    parts.append(prompt)
    return "\n\n".join(parts).strip()


def send_message(
    *,
    token: str,
    chat_id: str,
    text: str,
    thread_id: int | None,
    disable_notification: bool,
) -> dict:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload: dict[str, object] = {
        "chat_id": chat_id,
        "text": text,
        "disable_notification": disable_notification,
    }
    if thread_id is not None:
        payload["message_thread_id"] = thread_id

    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    context = None
    if os.environ.get("TELEGRAM_INSECURE_SSL") == "1":
        context = ssl._create_unverified_context()

    try:
        with urllib.request.urlopen(req, timeout=30, context=context) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Telegram API HTTP error {exc.code}: {detail}")
    except urllib.error.URLError as exc:
        raise SystemExit(f"Telegram API connection error: {exc}")

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        raise SystemExit(f"Non-JSON response from Telegram API: {body}")

    if not parsed.get("ok"):
        raise SystemExit(f"Telegram API rejected request: {parsed}")

    return parsed


def resolve_thread_id(config: dict, thread_key: str | None) -> int | None:
    if not thread_key:
        return None
    threads = config.get("threads", {})
    if thread_key not in threads:
        valid = ", ".join(sorted(threads.keys()))
        raise SystemExit(f"Unknown thread key '{thread_key}'. Valid keys: {valid}")
    return int(threads[thread_key])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a scheduled OpenClaw prompt into a Telegram topic.")
    parser.add_argument("--job-id", required=True, help="Logical job id, e.g. morning_brief")
    parser.add_argument("--prompt-file", help="Path to the job prompt markdown file")
    parser.add_argument("--message", help="Raw message body to send instead of reading a prompt file")
    parser.add_argument("--thread-key", help="Thread/topic alias from telegram-config.json")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to telegram-config.json")
    parser.add_argument("--label", help="Optional label shown in the message header")
    parser.add_argument("--dry-run", action="store_true", help="Print the message instead of sending it")
    args = parser.parse_args()
    if not args.prompt_file and not args.message:
        parser.error("one of --prompt-file or --message is required")
    return args


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).expanduser()
    config = load_json(config_path)
    if args.message is not None:
        prompt = args.message.strip()
    else:
        prompt_path = Path(args.prompt_file).expanduser()
        prompt = load_prompt(prompt_path)

    chat_id = str(config.get("chat_id", "")).strip()
    if not chat_id:
        raise SystemExit("telegram-config.json is missing 'chat_id'")

    target_bot_username = config.get("target_bot_username")
    thread_id = resolve_thread_id(config, args.thread_key)
    disable_notification = bool(config.get("disable_notification", False))

    message = build_message(
        job_id=args.job_id,
        prompt=prompt,
        target_bot_username=target_bot_username,
        job_label=args.label,
    )

    if args.dry_run:
        print(message)
        return 0

    token_env = config.get("token_env", "SCHEDULER_BOT_TOKEN")
    token = os.environ.get(token_env)
    if not token:
        raise SystemExit(f"Missing environment variable: {token_env}")

    for chunk in chunk_text(message):
        send_message(
            token=token,
            chat_id=chat_id,
            text=chunk,
            thread_id=thread_id,
            disable_notification=disable_notification,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
