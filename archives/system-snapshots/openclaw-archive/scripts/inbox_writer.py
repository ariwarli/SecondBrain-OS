#!/usr/bin/env python3
"""
inbox_writer.py — REED Inbox Item Creator

Dipanggil oleh REED ketika user kirim pesan ke topic inbox (thread_id: 11).
Nulis pesan ke inbox/pending/ supaya reed-archivist bisa proses saat heartbeat.

Usage:
    python3 inbox_writer.py "pesan dari user" [--source voice|text|manual]
"""

import os
import argparse
from datetime import datetime
from typing import Optional

WORKSPACE = "/home/openclaw/banirisset"
PENDING_DIR = os.path.join(WORKSPACE, "inbox", "pending")
PROCESSED_DIR = os.path.join(WORKSPACE, "inbox", "processed")
UNSORTED_DIR = os.path.join(WORKSPACE, "inbox", "unsorted")

def setup_dirs():
    for directory in [PENDING_DIR, PROCESSED_DIR, UNSORTED_DIR]:
        os.makedirs(directory, exist_ok=True)


def sanitize_slug(value: str, fallback: str = "item") -> str:
    slug = value[:40].strip().replace(" ", "-").replace("/", "-")
    slug = "".join(char for char in slug if char.isalnum() or char in "-_")
    return slug or fallback


def parse_timestamp(timestamp: Optional[str] = None) -> datetime:
    if not timestamp:
        return datetime.now()
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M")


def write_markdown_file(directory: str, filename: str, content: str) -> str:
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as file_obj:
        file_obj.write(content)
    return filepath


def build_pending_content(message: str, source: str, timestamp: datetime, title: Optional[str] = None) -> str:
    heading = title or message[:60]
    return f"""# INBOX: {heading}

**Timestamp:** {timestamp.strftime("%Y-%m-%d %H:%M")}
**Source:** {source}
**Original:** {message}

## Notes
[Context tambahan kalau ada]
"""


def build_unsorted_content(
    message: str,
    tg_msg_id: str,
    timestamp: datetime,
    title: Optional[str] = None,
) -> str:
    heading = title or message[:60]
    return f"""# [Unsorted] — {heading}

**Timestamp:** {timestamp.strftime("%Y-%m-%d %H:%M")}
**Source message id:** {tg_msg_id}
**Status:** pending-triage
**SLA:** triage < 24 jam
**Original:** {message}
"""


def write_pending_item(
    message: str,
    source: str = "telegram",
    timestamp: Optional[str] = None,
    filename: Optional[str] = None,
    title: Optional[str] = None,
) -> str:
    setup_dirs()

    now = parse_timestamp(timestamp)
    file_name = filename or f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{sanitize_slug(message)}.md"
    content = build_pending_content(message, source, now, title=title)
    return write_markdown_file(PENDING_DIR, file_name, content)


def write_unsorted_item(
    message: str,
    tg_msg_id: str,
    timestamp: Optional[str] = None,
    filename: Optional[str] = None,
    title: Optional[str] = None,
) -> str:
    setup_dirs()

    now = parse_timestamp(timestamp)
    safe_id = sanitize_slug(str(tg_msg_id), fallback="unknown")
    file_name = filename or f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{safe_id}.md"
    content = build_unsorted_content(message, safe_id, now, title=title)
    return write_markdown_file(UNSORTED_DIR, file_name, content)


def write_inbox_item(message: str, source: str = "telegram") -> str:
    return write_pending_item(message, source=source)


def main():
    parser = argparse.ArgumentParser(description="Write inbox item for reed-archivist to process")
    parser.add_argument("message", help="Message content from user")
    parser.add_argument(
        "--source",
        default="telegram",
        choices=["telegram", "voice", "manual"],
        help="Source of the message",
    )
    parser.add_argument(
        "--kind",
        default="pending",
        choices=["pending", "unsorted"],
        help="Target inbox bucket",
    )
    parser.add_argument("--message-id", default="unknown", help="Telegram message id for unsorted item")
    parser.add_argument("--timestamp", help="Explicit timestamp in format YYYY-MM-DD HH:MM")
    parser.add_argument("--filename", help="Override output filename")
    parser.add_argument("--title", help="Override markdown title/heading")

    args = parser.parse_args()

    if args.kind == "unsorted":
        filepath = write_unsorted_item(
            args.message,
            tg_msg_id=args.message_id,
            timestamp=args.timestamp,
            filename=args.filename,
            title=args.title,
        )
    else:
        filepath = write_pending_item(
            args.message,
            source=args.source,
            timestamp=args.timestamp,
            filename=args.filename,
            title=args.title,
        )

    print(f"✅ Inbox item created: {os.path.basename(filepath)}")
    print(f"   Path: {filepath}")
    print(f"   reed-archivist akan proses saat heartbeat berikutnya.")

if __name__ == "__main__":
    main()
