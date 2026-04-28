#!/usr/bin/env python3
"""
REED DULL — Proactive Engine

Modes:
- daily_brief: kirim morning brief jam 08:00 WIB ke topic Updates
- stale_scan: deteksi task stagnan >3 hari dan nudge ke topic Tasks
- crm_scan: deteksi follow-up CRM >48 jam dan nudge ke topic Personal CRM
- weekly_gap: kirim weekly knowledge gap report (Jumat 17:00 WIB) ke topic Knowledge Base
- pulse: jalankan stale_scan + crm_scan
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import requests
except ImportError:
    os.system("pip3 install requests -q")
    import requests


SEND_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
GROUP_CHAT_ID = -1003344368011
TOPIC_UPDATES = 13
TOPIC_TASKS = 10
TOPIC_PERSONAL_CRM = 9
TOPIC_KNOWLEDGE = 16

WORKSPACE = Path("/home/openclaw/banirisset")
STATE_FILE = WORKSPACE / "state" / "proactive_engine_state.json"
LOG_DIR = WORKSPACE / "scheduler" / "logs"
INBOX_UNSORTED_DIR = WORKSPACE / "inbox" / "unsorted"

TASK_STALE_DAYS = 3
CRM_OVERDUE_HOURS = 48
UNSORTED_OVERDUE_HOURS = 24


LOG_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "proactive_engine.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("proactive_engine")


@dataclass
class StaleTask:
    source: str
    title: str
    age_days: float


@dataclass
class CRMOverdue:
    name: str
    company: str
    status: str
    due_raw: str
    age_hours: float
    context: str


def tg_send(method: str, **params):
    url = f"https://api.telegram.org/bot{SEND_TOKEN}/{method}"
    for attempt in range(3):
        try:
            resp = requests.post(url, json=params, timeout=30)
            data = resp.json()
            if data.get("ok"):
                return data
            if data.get("error_code") == 429:
                retry_after = data.get("parameters", {}).get("retry_after", 5)
                time.sleep(retry_after + 1)
            else:
                log.error("Telegram API error: %s", data)
                return data
        except Exception as exc:
            log.error("Telegram request failed (attempt %s): %s", attempt + 1, exc)
            if attempt < 2:
                time.sleep(3)
    return None


def send_topic(thread_id: int, text: str) -> bool:
    if not SEND_TOKEN:
        log.error("TELEGRAM_BOT_TOKEN not set")
        return False
    result = tg_send(
        "sendMessage",
        chat_id=GROUP_CHAT_ID,
        message_thread_id=thread_id,
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return bool(result and result.get("ok"))


def now_local() -> datetime:
    return datetime.now()


def stable_key(prefix: str, value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}:{digest}"


def load_state() -> Dict:
    if not STATE_FILE.exists():
        return {"sent": {}, "last_daily_brief": "", "last_weekly_report": ""}
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("invalid state")
        data.setdefault("sent", {})
        data.setdefault("last_daily_brief", "")
        data.setdefault("last_weekly_report", "")
        return data
    except Exception:
        return {"sent": {}, "last_daily_brief": "", "last_weekly_report": ""}


def prune_old_sent(sent: Dict[str, str], keep_days: int = 14) -> Dict[str, str]:
    keep = {}
    cutoff = now_local() - timedelta(days=keep_days)
    for key, iso_ts in sent.items():
        try:
            ts = datetime.fromisoformat(iso_ts)
        except Exception:
            continue
        if ts >= cutoff:
            keep[key] = iso_ts
    return keep


def save_state(state: Dict) -> None:
    state["sent"] = prune_old_sent(state.get("sent", {}), keep_days=14)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def can_send(state: Dict, key: str, cooldown_hours: int) -> bool:
    sent = state.get("sent", {})
    last = sent.get(key)
    if not last:
        return True
    try:
        last_ts = datetime.fromisoformat(last)
    except Exception:
        return True
    return now_local() - last_ts >= timedelta(hours=cooldown_hours)


def mark_sent(state: Dict, key: str) -> None:
    state.setdefault("sent", {})[key] = now_local().isoformat(timespec="seconds")


def parse_date(value: str) -> Optional[datetime]:
    raw = (value or "").strip()
    if not raw or raw in {"-", "[TBD]", "TBD", "Active", "active"}:
        return None

    raw = re.sub(r"\s*WIB$", "", raw, flags=re.IGNORECASE)

    fmts = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d %b %Y",
        "%d %B %Y",
        "%b %d %Y",
        "%B %d %Y",
        "%b %d",
        "%B %d",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(raw, fmt)
            if "%Y" not in fmt:
                dt = dt.replace(year=now_local().year)
            return dt
        except ValueError:
            continue
    return None


def parse_md_tables(text: str) -> List[Tuple[List[str], List[List[str]]]]:
    lines = text.splitlines()
    tables: List[Tuple[List[str], List[List[str]]]] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("|"):
            i += 1
            continue
        if i + 1 >= len(lines):
            break
        sep = lines[i + 1].strip()
        if not (sep.startswith("|") and "---" in sep):
            i += 1
            continue
        headers = [c.strip() for c in line.strip("|").split("|")]
        rows: List[List[str]] = []
        i += 2
        while i < len(lines):
            row_line = lines[i].strip()
            if not row_line.startswith("|"):
                break
            row = [c.strip() for c in row_line.strip("|").split("|")]
            if len(row) == len(headers):
                rows.append(row)
            i += 1
        tables.append((headers, rows))
    return tables


def detect_unsorted_overdue() -> List[Path]:
    overdue = []
    now = now_local()
    if not INBOX_UNSORTED_DIR.exists():
        return overdue
    for path in sorted(INBOX_UNSORTED_DIR.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "**Status:** pending-triage" not in text:
            continue
        ts_match = re.search(r"\*\*Timestamp:\*\*\s*(.+)", text)
        item_ts = parse_date(ts_match.group(1).strip()) if ts_match else None
        if not item_ts:
            item_ts = datetime.fromtimestamp(path.stat().st_mtime)
        if now - item_ts > timedelta(hours=UNSORTED_OVERDUE_HOURS):
            overdue.append(path)
    return overdue


def detect_stale_tasks() -> List[StaleTask]:
    stale: List[StaleTask] = []
    now = now_local()

    daily_path = WORKSPACE / "daily.md"
    if daily_path.exists():
        text = daily_path.read_text(encoding="utf-8", errors="ignore")
        age_days = (now - datetime.fromtimestamp(daily_path.stat().st_mtime)).total_seconds() / 86400.0
        blocks = re.findall(r"###\s+Task:\s*(.+?)\n(.*?)(?=\n###\s+Task:|\Z)", text, flags=re.DOTALL)
        for title, body in blocks:
            status_match = re.search(r"\*\*Status:\*\*\s*(.+)", body)
            status = (status_match.group(1).strip().lower() if status_match else "pending")
            if any(k in status for k in ["done", "selesai", "completed", "resolved"]):
                continue
            if age_days > TASK_STALE_DAYS:
                stale.append(StaleTask(source="daily.md", title=title.strip(), age_days=age_days))

    clients_dir = WORKSPACE / "clients"
    if clients_dir.exists():
        for task_file in clients_dir.glob("*/tasks.md"):
            try:
                text = task_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            age_days = (now - datetime.fromtimestamp(task_file.stat().st_mtime)).total_seconds() / 86400.0
            if age_days <= TASK_STALE_DAYS:
                continue
            for match in re.finditer(r"^-\s*\[\s\]\s+(.+)$", text, flags=re.MULTILINE):
                stale.append(
                    StaleTask(
                        source=str(task_file.relative_to(WORKSPACE)),
                        title=match.group(1).strip(),
                        age_days=age_days,
                    )
                )

    uniq = {(item.source, item.title): item for item in stale}
    return sorted(uniq.values(), key=lambda item: item.age_days, reverse=True)


def detect_crm_overdue() -> List[CRMOverdue]:
    out: List[CRMOverdue] = []
    crm_path = WORKSPACE / "crm.md"
    if not crm_path.exists():
        return out

    text = crm_path.read_text(encoding="utf-8", errors="ignore")
    tables = parse_md_tables(text)
    now = now_local()

    for headers, rows in tables:
        low_headers = [h.lower() for h in headers]
        if "nama" not in low_headers or "status" not in low_headers:
            continue

        idx_name = low_headers.index("nama")
        idx_company = low_headers.index("company") if "company" in low_headers else -1
        idx_status = low_headers.index("status")
        idx_due = low_headers.index("due") if "due" in low_headers else -1
        idx_next = low_headers.index("next action") if "next action" in low_headers else -1

        for row in rows:
            name = row[idx_name].strip()
            status = row[idx_status].strip()
            company = row[idx_company].strip() if idx_company >= 0 else "-"
            due_raw = row[idx_due].strip() if idx_due >= 0 else ""
            next_action = row[idx_next].strip() if idx_next >= 0 else ""

            if not name or name in {"[TBD]", "-"}:
                continue

            status_low = status.lower()
            next_low = next_action.lower()
            if "follow" not in status_low and "follow" not in next_low and "proposal" not in status_low:
                continue

            due_dt = parse_date(due_raw)
            if not due_dt:
                continue
            age_hours = (now - due_dt).total_seconds() / 3600.0
            if age_hours <= CRM_OVERDUE_HOURS:
                continue

            out.append(
                CRMOverdue(
                    name=name,
                    company=company,
                    status=status,
                    due_raw=due_raw,
                    age_hours=age_hours,
                    context=next_action or status or "follow-up overdue",
                )
            )

    uniq = {(item.name, item.company, item.due_raw): item for item in out}
    return sorted(uniq.values(), key=lambda item: item.age_hours, reverse=True)


def choose_next_action(stale_tasks: List[StaleTask], crm_overdue: List[CRMOverdue], unsorted_overdue: List[Path]) -> str:
    if crm_overdue:
        item = crm_overdue[0]
        return f"Follow-up {item.name} ({item.company}) hari ini: {item.context}."
    if stale_tasks:
        item = stale_tasks[0]
        return f"Mulai task paling mandek: {item.title[:80]}"
    if unsorted_overdue:
        return f"Triage {len(unsorted_overdue)} item unsorted biar routing bersih."
    return "Eksekusi 1 task prioritas revenue tertinggi sebelum jam 10."


def send_daily_brief(state: Dict) -> bool:
    today_key = now_local().strftime("%Y-%m-%d")
    if state.get("last_daily_brief") == today_key:
        log.info("Daily brief already sent today")
        return False

    stale = detect_stale_tasks()
    crm = detect_crm_overdue()
    unsorted = detect_unsorted_overdue()
    next_action = choose_next_action(stale, crm, unsorted)

    text = (
        f"🌅 Morning brief: stale task {len(stale)} | CRM >48h {len(crm)} | unsorted >24h {len(unsorted)}\n"
        f"🎯 Next action: {next_action[:120]}\n"
        "Reply: GAS untuk gw breakdown langkah pertama sekarang."
    )

    ok = send_topic(TOPIC_UPDATES, text)
    if ok:
        state["last_daily_brief"] = today_key
        log.info("Morning brief sent")
    return ok


def send_stale_task_nudge(state: Dict) -> int:
    stale = detect_stale_tasks()
    sent = 0
    for item in stale[:3]:
        key = stable_key("stale_task", f"{item.source}|{item.title}")
        if not can_send(state, key, cooldown_hours=24):
            continue
        text = (
            f"⏳ Ini masih nyangkut: {item.title[:90]}\n"
            "Masih relevan?\n"
            "Kalau iya gw bantu mulai sekarang."
        )
        if send_topic(TOPIC_TASKS, text):
            mark_sent(state, key)
            sent += 1
    return sent


def send_crm_nudges(state: Dict) -> int:
    overdue = detect_crm_overdue()
    sent = 0
    for item in overdue[:3]:
        key = stable_key("crm_followup", f"{item.name}|{item.company}|{item.due_raw}")
        if not can_send(state, key, cooldown_hours=24):
            continue
        text = (
            f"📞 Follow-up overdue: {item.name} ({item.company})\n"
            f"Penting: {item.context[:90]}\n"
            "Aksi: kirim follow-up hari ini biar deal gak dingin."
        )
        if send_topic(TOPIC_PERSONAL_CRM, text):
            mark_sent(state, key)
            sent += 1
    return sent


def detect_knowledge_gaps() -> Tuple[List[str], str]:
    areas = [
        "knowledge-base/wiki/index.md",
        "knowledge-base/wiki/log.md",
        "knowledge-base/wiki/sessions",
    ]
    candidates = []
    for area in areas:
        path = WORKSPACE / area
        if path.is_dir():
            files = list(path.glob("*.md"))
            recent = [f for f in files if now_local() - datetime.fromtimestamp(f.stat().st_mtime) <= timedelta(days=7)]
            if len(recent) < max(1, len(files) // 4):
                candidates.append(f"{path.name} (sedikit sintesis)")
        elif path.exists():
            lines = path.read_text(encoding="utf-8", errors="ignore").count("\n") + 1
            age_days = (now_local() - datetime.fromtimestamp(path.stat().st_mtime)).days
            if lines < 80 or age_days > 7:
                candidates.append(f"{path.name} (tipis/kurang update)")
        else:
            candidates.append(f"{Path(area).name} (belum ada)")

    if not candidates:
        candidates = ["wiki synthesis lintas project"]

    question = "Apa decision rule paling konsisten untuk bedain Task vs Content vs Project dari pesan ambigu minggu ini?"
    return candidates[:2], question


def send_weekly_gap_report(state: Dict) -> bool:
    week_key = now_local().strftime("%G-W%V")
    if state.get("last_weekly_report") == week_key:
        log.info("Weekly report already sent this week")
        return False

    gaps, question = detect_knowledge_gaps()
    text = (
        f"📚 Weekly gap: {', '.join(gaps)[:120]}\n"
        "Aktivitas mingguan tinggi, tapi bagian ini belum jadi knowledge reusable.\n"
        f"❓Riset prioritas: {question[:110]}"
    )

    ok = send_topic(TOPIC_KNOWLEDGE, text)
    if ok:
        state["last_weekly_report"] = week_key
        log.info("Weekly knowledge gap report sent")
    return ok


def run_mode(mode: str) -> int:
    state = load_state()
    sent_count = 0

    if mode == "daily_brief":
        sent_count += 1 if send_daily_brief(state) else 0
    elif mode == "stale_scan":
        sent_count += send_stale_task_nudge(state)
    elif mode == "crm_scan":
        sent_count += send_crm_nudges(state)
    elif mode == "weekly_gap":
        sent_count += 1 if send_weekly_gap_report(state) else 0
    elif mode == "pulse":
        sent_count += send_stale_task_nudge(state)
        sent_count += send_crm_nudges(state)
    elif mode == "run_all":
        sent_count += send_stale_task_nudge(state)
        sent_count += send_crm_nudges(state)
        sent_count += 1 if send_daily_brief(state) else 0
        sent_count += 1 if send_weekly_gap_report(state) else 0
    else:
        raise ValueError(f"Unknown mode: {mode}")

    save_state(state)
    return sent_count


def main() -> None:
    parser = argparse.ArgumentParser(description="REED proactive engine")
    parser.add_argument(
        "--mode",
        default="pulse",
        choices=["daily_brief", "stale_scan", "crm_scan", "weekly_gap", "pulse", "run_all"],
    )
    args = parser.parse_args()

    if not SEND_TOKEN:
        log.error("TELEGRAM_BOT_TOKEN not set")
        raise SystemExit(1)

    sent = run_mode(args.mode)
    log.info("Mode=%s done. notifications_sent=%s", args.mode, sent)


if __name__ == "__main__":
    main()
