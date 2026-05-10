#!/usr/bin/env python3
"""
inbox_writer.py — REED Inbox Item Creator

Dipanggil oleh REED ketika user kirim pesan ke topic inbox (thread_id: 11).
Nulis pesan ke inbox/pending/ supaya reed-archivist bisa proses saat heartbeat.

Usage:
    python3 inbox_writer.py "pesan dari user" [--source voice|text|manual]
"""

import sys
import os
import argparse
from datetime import datetime

WORKSPACE = "/home/openclaw/banirisset"
PENDING_DIR = os.path.join(WORKSPACE, "inbox", "pending")
PROCESSED_DIR = os.path.join(WORKSPACE, "inbox", "processed")
UNSORTED_DIR = os.path.join(WORKSPACE, "inbox", "unsorted")

def setup_dirs():
    for d in [PENDING_DIR, PROCESSED_DIR, UNSORTED_DIR]:
        os.makedirs(d, exist_ok=True)

def write_inbox_item(message: str, source: str = "telegram") -> str:
    setup_dirs()

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    date_str = now.strftime("%Y-%m-%d %H:%M")

    # Sanitize message for filename
    slug = message[:40].strip().replace(" ", "-").replace("/", "-")
    slug = "".join(c for c in slug if c.isalnum() or c in "-_")

    filename = f"{timestamp}_{slug}.md"
    filepath = os.path.join(PENDING_DIR, filename)

    content = f"""# INBOX: {message[:60]}

**Timestamp:** {date_str}
**Source:** {source}
**Original:** {message}

## Notes
[Context tambahan kalau ada]
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath

def main():
    parser = argparse.ArgumentParser(description="Write inbox item for reed-archivist to process")
    parser.add_argument("message", help="Message content from user")
    parser.add_argument("--source", default="telegram", choices=["telegram", "voice", "manual"],
                       help="Source of the message")

    args = parser.parse_args()

    filepath = write_inbox_item(args.message, args.source)
    print(f"✅ Inbox item created: {os.path.basename(filepath)}")
    print(f"   Path: {filepath}")
    print(f"   reed-archivist akan proses saat heartbeat berikutnya.")

if __name__ == "__main__":
    main()
