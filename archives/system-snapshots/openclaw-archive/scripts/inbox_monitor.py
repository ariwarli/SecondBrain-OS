#!/usr/bin/env python3
"""
inbox_monitor.py — Programmatic Inbox Router for REED

Monitors SecondBrain OS inbox topic via Telegram Bot API.
Classifies messages and forwards to correct topic.
Runs as a persistent service alongside REED.

Usage:
    python3 inbox_monitor.py              # Run once (cron mode)
    python3 inbox_monitor.py --daemon     # Run continuously (service mode)
"""

import os
import sys
import json
import time
import re
import logging
import argparse
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip3 install requests -q")
    import requests

# === CONFIG ===

# REED DULL token for READING messages (no conflict with REED main)
# REED main token for SENDING replies/forwards
POLL_TOKEN = os.environ.get("SCHEDULER_BOT_TOKEN", "")
SEND_TOKEN = os.environ.get("SCHEDULER_BOT_TOKEN", "")
GROUP_CHAT_ID = -1003344368011
BANI_USER_ID = 163335047

# Topic thread IDs
TOPICS = {
    "inbox": 11,
    "tasks": 10,
    "personal-crm": 9,
    "content": 3,
    "ops": 27,
    "knowledge-base": 16,
    "updates": 13,
}

WORKSPACE = "/home/openclaw/banirisset"
STATE_FILE = os.path.join(WORKSPACE, "inbox", ".monitor_state.json")
PENDING_DIR = os.path.join(WORKSPACE, "inbox", "pending")
PROCESSED_DIR = os.path.join(WORKSPACE, "inbox", "processed")

# === CLASSIFICATION RULES ===

RULES = [
    {
        "bucket": "Project",
        "topic": "tasks",
        "keywords": [
            r"\bnirva\b", r"\bsentrachat\b", r"\bstop\s*tb\b", r"\bstoptb\b",
            r"\bapps\b", r"\bappssync\b", r"\bpt\s*sin\b",
            r"\bproject\b", r"\bclient\b", r"\bbrief\b", r"\bdeliverable\b",
            r"\bdeadline\b", r"\btor\b", r"\bproposal\b", r"\bscope\b",
            r"\bmilestone\b", r"\bbrand\s*os\b", r"\bcontent\s*os\b",
            r"\btool\s*lab\b", r"\bpara\b",
        ],
        "path_map": {
            "nirva": "clients/nirva/",
            "sentrachat": "clients/sentrachat/",
            "stop.?tb|stoptb": "clients/stop-tb/",
            "apps(?!sync)": "clients/apps/",
            "appssync": "clients/appssync/",
            "pt.?sin": "clients/pt-sin/",
            "brand.?os": "Brand OS - Bani Risset/",
            "tool.?lab": "projects/tool-lab/",
            "para": "projects/para/",
        },
    },
    {
        "bucket": "CRM",
        "topic": "personal-crm",
        "keywords": [
            r"\bfollow[\s-]?up\b", r"\bmeeting\b", r"\bkontak\b",
            r"\bdeal\b", r"\bclient\s*baru\b", r"\bnanya\b", r"\bnawarin\b",
            r"\bnegosiasi\b", r"\boverdue\b", r"\bghosting\b",
            r"\bdede\b", r"\bbelum\s*jawab\b",
        ],
        "path": "crm.md",
    },
    {
        "bucket": "Content",
        "topic": "content",
        "keywords": [
            r"\bthread\b", r"\bpost\b", r"\blinkedin\b", r"\binstagram\b",
            r"\bkonten\b", r"\bhook\b", r"\bcaption\b", r"\bdraft\b",
            r"\bpublish\b", r"\bjadwal\s*posting\b", r"\bcarousel\b",
            r"\butas\b", r"\bblog\b", r"\bnewsletter\b",
        ],
        "path": "Brand OS - Bani Risset/content/drafts/",
    },
    {
        "bucket": "Task",
        "topic": "tasks",
        "keywords": [
            r"\bbikin\b", r"\bbuat\b", r"\bkerjain\b", r"\bselesaiin\b",
            r"\bfix\b", r"\burgent\b", r"\bharus\b", r"\btolong\b",
            r"\bbantu\b", r"\bcheck\b", r"\baudit\b", r"\breview\b",
        ],
        "path": "daily.md",
    },
    {
        "bucket": "Knowledge",
        "topic": "knowledge-base",
        "keywords": [
            r"https?://", r"\bsimpan\b", r"\bbookmark\b", r"\breferensi\b",
            r"\bnanti\s*dibaca\b", r"\btools?\b", r"\bresource\b",
            r"\btemplate\b", r"\btutorial\b", r"\bguide\b", r"\bdoc\b",
        ],
        "path": "research/bookmarks/",
    },
]


# === LOGGING ===

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(WORKSPACE, "inbox", "monitor.log")),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("inbox_monitor")


# === TELEGRAM API ===

def tg_api(method, token=None, **params):
    t = token or SEND_TOKEN
    url = f"https://api.telegram.org/bot{t}/{method}"
    resp = requests.post(url, json=params, timeout=30)
    data = resp.json()
    if not data.get("ok"):
        log.error(f"Telegram API error: {data}")
    return data


def send_message(text, thread_id=None):
    params = {"chat_id": GROUP_CHAT_ID, "text": text, "parse_mode": "HTML"}
    if thread_id:
        params["message_thread_id"] = thread_id
    return tg_api("sendMessage", **params)


def forward_message(message_id, to_thread_id):
    """Copy a message to another topic in the same group."""
    return tg_api(
        "copyMessage",
        chat_id=GROUP_CHAT_ID,
        from_chat_id=GROUP_CHAT_ID,
        message_id=message_id,
        message_thread_id=to_thread_id,
    )


# === CLASSIFICATION ===

def classify(text):
    text_lower = text.lower()
    scores = {}

    for rule in RULES:
        bucket = rule["bucket"]
        score = 0
        for kw in rule["keywords"]:
            if re.search(kw, text_lower):
                score += 1
        if score > 0:
            scores[bucket] = score

    if not scores:
        return None, 0

    best = max(scores, key=scores.get)
    confidence = scores[best] / max(len(scores), 1)

    return best, confidence


def get_rule(bucket):
    for r in RULES:
        if r["bucket"] == bucket:
            return r
    return None


def get_project_path(text, rule):
    if "path_map" not in rule:
        return rule.get("path", "inbox/unsorted/")

    text_lower = text.lower()
    for pattern, path in rule["path_map"].items():
        if re.search(pattern, text_lower):
            return path

    return "inbox/unsorted/"


# === STATE ===

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_update_id": 0}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


# === INBOX FILE WRITER ===

def write_inbox_file(text, bucket, path, source="telegram"):
    now = datetime.now()
    ts = now.strftime("%Y-%m-%d_%H-%M-%S")
    date_str = now.strftime("%Y-%m-%d %H:%M")
    slug = re.sub(r"[^a-zA-Z0-9_-]", "", text[:30].replace(" ", "-"))

    filepath = os.path.join(PROCESSED_DIR, f"{ts}_{slug}.md")
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    content = f"""# [{bucket}] — {text[:60]}

**Timestamp:** {date_str}
**Source:** {source}
**Bucket:** {bucket}
**Routed to:** {path}
**Original:** {text}

## Status
- Processed: ✅
- Routed to: {path}
"""
    with open(filepath, "w") as f:
        f.write(content)

    return filepath


# === MAIN LOOP ===

def process_updates():
    state = load_state()
    offset = state["last_update_id"] + 1

    data = tg_api("getUpdates", token=POLL_TOKEN, offset=offset, timeout=5)
    updates = data.get("result", [])

    if not updates:
        return 0

    processed = 0

    for update in updates:
        state["last_update_id"] = update["update_id"]
        msg = update.get("message")

        if not msg:
            continue

        # Only process messages from SecondBrain OS inbox topic
        chat_id = msg.get("chat", {}).get("id")
        thread_id = msg.get("message_thread_id")
        from_id = msg.get("from", {}).get("id")

        if chat_id != GROUP_CHAT_ID:
            continue
        if thread_id != TOPICS["inbox"]:
            continue
        if from_id != BANI_USER_ID:
            continue

        # Skip bot messages
        if msg.get("from", {}).get("is_bot"):
            continue

        text = msg.get("text", "")
        if not text:
            # Could be voice note transcript — check caption
            text = msg.get("caption", "")
        if not text:
            continue

        log.info(f"Inbox message: {text[:80]}")

        # Classify
        bucket, confidence = classify(text)
        message_id = msg["message_id"]

        if bucket and confidence > 0:
            rule = get_rule(bucket)
            target_topic = TOPICS.get(rule["topic"], TOPICS["inbox"])
            path = get_project_path(text, rule)

            # Forward to correct topic
            forward_message(message_id, target_topic)

            # Write file
            filepath = write_inbox_file(text, bucket, path)

            # Reply confirmation in inbox
            conf_text = (
                f"✅ <b>[ROUTED → {bucket}]</b>\n"
                f"📂 <code>{path}</code>\n"
                f"💬 Forwarded ke topic <b>{rule['topic']}</b>"
            )
            send_message(conf_text, thread_id=TOPICS["inbox"])

            log.info(f"Routed: {bucket} → {path}")
            processed += 1

        else:
            # Low confidence — ask user
            unsorted_path = write_inbox_file(text, "Unsorted", "inbox/unsorted/")
            ask_text = (
                f"❓ Gw kurang yakin ini masuk ke mana.\n"
                f"<i>\"{text[:100]}\"</i>\n\n"
                f"Pilih: /route_project /route_content /route_crm /route_task /route_knowledge"
            )
            send_message(ask_text, thread_id=TOPICS["inbox"])
            log.info(f"Unsorted: {text[:50]}")
            processed += 1

    save_state(state)
    return processed


def run_once():
    """Single run mode — for cron."""
    if not POLL_TOKEN:
        log.error("SCHEDULER_BOT_TOKEN not set!")
        sys.exit(1)

    count = process_updates()
    log.info(f"Processed {count} inbox items")


def run_daemon(interval=30):
    """Continuous mode — polls every N seconds."""
    if not POLL_TOKEN:
        log.error("SCHEDULER_BOT_TOKEN not set!")
        sys.exit(1)

    log.info(f"Inbox monitor daemon started (poll every {interval}s)")

    while True:
        try:
            process_updates()
        except KeyboardInterrupt:
            log.info("Stopped by user")
            break
        except Exception as e:
            log.error(f"Error: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="REED Inbox Monitor")
    parser.add_argument("--daemon", action="store_true", help="Run continuously")
    parser.add_argument("--interval", type=int, default=30, help="Poll interval in seconds")
    args = parser.parse_args()

    if args.daemon:
        run_daemon(args.interval)
    else:
        run_once()
