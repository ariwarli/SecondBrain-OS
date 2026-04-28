#!/usr/bin/env python3
"""
REED DULL — Reminder Checker

Dijalankan oleh cron setiap 30 menit.
Scan scheduler/queue/ untuk reminder yang waktunya sudah tiba.
Kirim notifikasi ke topic Updates via Telegram API.
Arsipkan reminder yang sudah terkirim.

Usage:
    python3 reminder_checker.py
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    os.system("pip3 install requests -q")
    import requests

# === CONFIG ===
SEND_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
GROUP_CHAT_ID = -1003344368011
UPDATES_TOPIC_ID = 13

SCRIPT_DIR = Path(__file__).resolve().parent.parent
WORKSPACE = SCRIPT_DIR.parent  # /home/openclaw/banirisset
QUEUE_DIR = WORKSPACE / "scheduler" / "queue"
ARCHIVE_DIR = WORKSPACE / "scheduler" / "archive"
LOG_DIR = WORKSPACE / "scheduler" / "logs"

# === LOGGING ===
for d in [QUEUE_DIR, ARCHIVE_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "reminder_checker.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("reminder_checker")


def tg_send(method, **params):
    """Send Telegram API request with retry logic."""
    url = f"https://api.telegram.org/bot{SEND_TOKEN}/{method}"
    for attempt in range(3):
        try:
            resp = requests.post(url, json=params, timeout=30)
            data = resp.json()
            if data.get("ok"):
                return data
            if data.get("error_code") == 429:
                retry_after = data.get("parameters", {}).get("retry_after", 5)
                log.warning(f"Rate limited, waiting {retry_after}s...")
                time.sleep(retry_after + 1)
            else:
                log.error(f"Telegram API error: {data}")
                return data
        except Exception as e:
            log.error(f"Request failed (attempt {attempt + 1}): {e}")
            if attempt < 2:
                time.sleep(5)
    return None


def send_reminder_alert(reminder_data):
    """Send reminder notification to Updates topic."""
    target_time = reminder_data.get("target_at", "Unknown")
    description = reminder_data.get("description", "")
    original = reminder_data.get("original_text", "")

    # Build message
    # If description is same as original, just show one
    if description.strip().lower() == original.strip().lower():
        content = description[:120]
    else:
        content = description[:120]

    # Time formatting
    try:
        dt = datetime.strptime(target_time, "%Y-%m-%d %H:%M")
        day_name = dt.strftime("%A")
        time_str = dt.strftime("%H:%M")
        date_str = dt.strftime("%d %b %Y")
    except:
        day_name = ""
        time_str = target_time
        date_str = ""

    if date_str == datetime.now().strftime("%d %b %Y"):
        time_header = f"🕐 {time_str} WIB"
    else:
        time_header = f"🕐 {time_str} WIB ({day_name}, {date_str})"

    text = (
        f"⏰ <b>REMINDER</b>\n"
        f"{time_header}\n\n"
        f"<i>{content}</i>\n\n"
        f"📥 Request dari: Inbox\n"
        f" REED DULL — Scheduler"
    )

    result = tg_send(
        "sendMessage",
        chat_id=GROUP_CHAT_ID,
        message_thread_id=UPDATES_TOPIC_ID,
        text=text,
        parse_mode="HTML",
    )

    return result


def process_reminder(filepath):
    """Process a single reminder file. Return True if delivered."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        log.error(f"Failed to read {filepath}: {e}")
        return False

    if data.get("delivered"):
        log.info(f"Already delivered: {filepath.name}")
        return False

    target_ts = data.get("target_timestamp", 0)
    now_ts = int(time.time())

    if now_ts < target_ts:
        # Not time yet
        return False

    # Time to deliver!
    log.info(f"Delivering reminder: {filepath.name} → {data.get('description', '')[:60]}")

    result = send_reminder_alert(data)

    if result and result.get("ok"):
        # Mark as delivered
        data["delivered"] = True
        data["delivered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Move to archive
        archive_path = ARCHIVE_DIR / filepath.name
        try:
            filepath.rename(archive_path)
            log.info(f"Archived: {filepath.name} → archive/")
        except Exception as e:
            log.warning(f"Failed to archive {filepath.name}: {e}")

        return True
    else:
        log.error(f"Failed to send reminder: {filepath.name}")
        return False


def main():
    if not SEND_TOKEN:
        log.error("TELEGRAM_BOT_TOKEN not set!")
        sys.exit(1)

    QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    # Get all queue files, sorted by filename (which encodes target time)
    queue_files = sorted(QUEUE_DIR.glob("*.json"))

    if not queue_files:
        log.info("No pending reminders")
        return

    delivered = 0
    for filepath in queue_files:
        if process_reminder(filepath):
            delivered += 1

    log.info(f"Processed {len(queue_files)} reminders, {delivered} delivered")


if __name__ == "__main__":
    main()
