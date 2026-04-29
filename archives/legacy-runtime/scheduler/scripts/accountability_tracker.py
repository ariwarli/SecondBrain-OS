#!/usr/bin/env python3
"""
REED DULL — Accountability Tracker

Dijalankan oleh cron setiap hari jam 18:00 (sore).
Cek topic Content dan Tasks untuk hitung progress vs target harian.
Kirim laporan ke topic Updates.

Usage:
    python3 accountability_tracker.py
"""

import os
import sys
import json
import time
import re
import logging
from datetime import datetime, timedelta
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
CONTENT_TOPIC_ID = 3
TASKS_TOPIC_ID = 10

SCRIPT_DIR = Path(__file__).resolve().parent.parent
WORKSPACE = SCRIPT_DIR.parent
TRACKING_DIR = WORKSPACE / "scheduler" / "tracking"
LOG_DIR = WORKSPACE / "scheduler" / "logs"

# === LOGGING ===
for d in [TRACKING_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "accountability.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("accountability")


def tg_send(method, **params):
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


def count_today_content_posts():
    """
    Count how many content items were posted today by checking Content topic session files.
    Returns count and list of post descriptions.
    """
    sessions_dir = Path("/home/openclaw/.openclaw/agents/reed-archivist/sessions")
    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    posts = []

    # Look for topic:3 (content) session files modified today
    for session_file in sessions_dir.glob("*topic-3.jsonl"):
        if not session_file.stat().st_mtime > time.time() - 86400 * 2:
            continue
        try:
            with open(session_file) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except:
                        continue

                    if entry.get("type") != "message":
                        continue

                    timestamp = entry.get("timestamp", "")
                    if not timestamp.startswith(today):
                        continue

                    msg = entry.get("message", {})
                    if msg.get("role") != "assistant":
                        continue

                    content = msg.get("content", "")
                    if isinstance(content, list):
                        content = " ".join(c.get("text", "") for c in content if isinstance(c, dict))

                    # Look for content-related keywords
                    content_keywords = ["thread", "post", "linkedin", "carousel", "draft", "konten", "hook", "caption"]
                    if any(kw in content.lower() for kw in content_keywords):
                        count += 1
                        preview = content[:80].replace("\n", " ")
                        posts.append(preview)
        except Exception as e:
            log.warning(f"Error reading {session_file}: {e}")

    # Also check content drafts folder for files created today
    content_drafts = WORKSPACE / "Brand OS - Bani Risset" / "content" / "drafts"
    if content_drafts.exists():
        for f in content_drafts.iterdir():
            if f.is_file() and today in f.name:
                count += 1
                posts.append(f"Draft: {f.name}")

    return count, posts


def count_today_completed_tasks():
    """
    Count tasks marked as done today from daily.md and client task files.
    """
    daily_md = WORKSPACE / "daily.md"
    today = datetime.now().strftime("%Y-%m-%d")
    done_count = 0
    done_tasks = []

    if daily_md.exists():
        try:
            with open(daily_md) as f:
                content = f.read()
            # Look for completed checkboxes today
            done_matches = re.findall(r'- \[x\]\s+(.+)', content, re.IGNORECASE)
            done_count = len(done_matches)
            done_tasks = [t.strip()[:60] for t in done_matches]
        except Exception as e:
            log.warning(f"Error reading daily.md: {e}")

    # Check client task files
    clients_dir = WORKSPACE / "clients"
    if clients_dir.exists():
        for client_dir in clients_dir.iterdir():
            if client_dir.is_dir():
                tasks_file = client_dir / "tasks.md"
                if tasks_file.exists():
                    try:
                        with open(tasks_file) as f:
                            content = f.read()
                        done_matches = re.findall(r'- \[x\]\s+(.+)', content, re.IGNORECASE)
                        done_count += len(done_matches)
                        done_tasks.extend([f"[{client_dir.name}] {t.strip()[:50]}" for t in done_matches])
                    except:
                        pass

    return done_count, done_tasks


def load_daily_goals():
    """Load today's goals from tracking file."""
    today = datetime.now().strftime("%Y-%m-%d")
    goals_file = TRACKING_DIR / f"{today}.json"

    if goals_file.exists():
        try:
            with open(goals_file) as f:
                return json.load(f)
        except:
            pass

    return {"goals": {}, "date": today}


def generate_report(goals, content_count, content_posts, task_count, done_tasks):
    """Generate accountability report HTML."""
    lines = []
    lines.append("📊 <b>ACCOUNTABILITY CHECK</b>")
    lines.append(f"📅 {datetime.now().strftime('%A, %d %B %Y')}")
    lines.append("")

    # Goals section
    goal_items = goals.get("goals", {})
    if goal_items:
        lines.append("<b>Target Hari Ini:</b>")
        for key, val in goal_items.items():
            lines.append(f"• {key}: {val}")
        lines.append("")

    # Content results
    lines.append(f"<b>Konten:</b> {content_count} item")
    if content_posts:
        for p in content_posts[:3]:
            lines.append(f"  → {p}")
    if content_count == 0 and goal_items.get("konten"):
        lines.append("  ❌ <b>Belum ada konten hari ini.</b>")
    lines.append("")

    # Task results
    lines.append(f"<b>Tasks:</b> {task_count} selesai")
    if done_tasks:
        for t in done_tasks[:3]:
            lines.append(f"  → {t}")
    lines.append("")

    # Verdict
    total_goals = len(goal_items)
    if total_goals == 0:
        lines.append("<i>Tidak ada target yang dicatat hari ini.</i>")
        lines.append("")
        lines.append("💡 Kirim ke Inbox: <i>\"Target hari ini: 3 post LinkedIn\"</i>")
    elif content_count > 0 or task_count > 0:
        lines.append("✅ <b>Progress ada. Keep going!</b>")
    else:
        lines.append("🚩 <b>Hari ini masih kosong.</b>")
        lines.append("Mau gw draft sesuatu biar ada progress?")

    lines.append("")
    lines.append("REED DULL — Accountability Tracker")

    return "\n".join(lines)


def main():
    if not SEND_TOKEN:
        log.error("TELEGRAM_BOT_TOKEN not set!")
        sys.exit(1)

    log.info("Running accountability check...")

    goals = load_daily_goals()
    content_count, content_posts = count_today_content_posts()
    task_count, done_tasks = count_today_completed_tasks()

    report = generate_report(goals, content_count, content_posts, task_count, done_tasks)

    result = tg_send(
        "sendMessage",
        chat_id=GROUP_CHAT_ID,
        message_thread_id=UPDATES_TOPIC_ID,
        text=report,
        parse_mode="HTML",
    )

    if result and result.get("ok"):
        log.info("Accountability report sent to Updates")
    else:
        log.error("Failed to send accountability report")


if __name__ == "__main__":
    main()
