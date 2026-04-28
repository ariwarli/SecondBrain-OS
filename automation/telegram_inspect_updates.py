#!/usr/bin/env python3

import json
import os
import ssl
import sys
import urllib.error
import urllib.request


def fetch_updates(token: str) -> dict:
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    context = None
    if os.environ.get("TELEGRAM_INSECURE_SSL") == "1":
        context = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(url, timeout=30, context=context) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Telegram API HTTP error {exc.code}: {detail}")
    except urllib.error.URLError as exc:
        raise SystemExit(f"Telegram API connection error: {exc}")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        raise SystemExit(f"Non-JSON response from Telegram API: {body}")

    if not data.get("ok"):
        raise SystemExit(f"Telegram API rejected request: {data}")

    return data


def main() -> int:
    token = os.environ.get("SCHEDULER_BOT_TOKEN")
    if not token:
        raise SystemExit("Missing environment variable: SCHEDULER_BOT_TOKEN")

    data = fetch_updates(token)
    results = data.get("result", [])

    if not results:
        print("No updates yet. Send a few test messages into each Telegram topic first.")
        return 0

    seen = set()
    for item in results:
        message = item.get("message") or item.get("edited_message") or {}
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        title = chat.get("title") or chat.get("username") or chat.get("first_name") or "unknown"
        thread_id = message.get("message_thread_id")
        text = message.get("text", "")
        key = (chat_id, thread_id)
        if key in seen:
            continue
        seen.add(key)
        print(json.dumps({
            "chat_id": chat_id,
            "chat_title": title,
            "thread_id": thread_id,
            "sample_text": text[:120]
        }, ensure_ascii=True))

    return 0


if __name__ == "__main__":
    sys.exit(main())
