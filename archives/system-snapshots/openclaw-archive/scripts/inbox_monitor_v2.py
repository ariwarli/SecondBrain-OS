#!/usr/bin/env python3
"""
inbox_monitor_v2.py — File-based Inbox Router for REED
Reads from OpenClaw session JSONL files (NO getUpdates = NO conflict with REED).
Uses bot token only for sendMessage/copyMessage (safe to run alongside REED).

Usage:
    python3 inbox_monitor_v2.py              # Run once
    python3 inbox_monitor_v2.py --daemon     # Run continuously
"""

import os
import sys
import json
import time
import re
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    os.system("pip3 install requests -q")
    import requests

from inbox_writer import write_unsorted_item

# === CONFIG ===
SEND_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
GROUP_CHAT_ID = -1003344368011
BANI_USER_ID = "163335047"
OPENCLAW_CONFIG = os.environ.get("OPENCLAW_CONFIG_PATH", "/home/openclaw/.openclaw/openclaw.json")
MANDATORY_PROVIDER = os.environ.get("INBOX_ROUTER_PROVIDER", "9router")

# Model selection via model_router or env override
def get_classifier_config():
    """Get classifier model config from router or env override."""
    env_override = os.environ.get("INBOX_ROUTER_CLASSIFIER_MODEL")
    if env_override:
        return env_override, 180, 0
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from model_router import get_classifier_model
        primary, _ = get_classifier_model()
        return f"{primary.provider}/{primary.model_id}", primary.max_tokens, primary.temperature
    except Exception:
        return f"{MANDATORY_PROVIDER}/reed-classifier", 180, 0

CLASSIFIER_MODEL, CLASSIFIER_MAX_TOKENS, CLASSIFIER_TEMPERATURE = get_classifier_config()
CLASSIFIER_THRESHOLD = int(os.environ.get("INBOX_ROUTER_CLASSIFIER_THRESHOLD", "70"))
CLASSIFIER_TIMEOUT = int(os.environ.get("INBOX_ROUTER_CLASSIFIER_TIMEOUT", "20"))

TOPICS = {
    "inbox": 11,
    "tasks": 10,
    "personal-crm": 9,
    "content": 3,
    "ops": 27,
    "knowledge-base": 16,
    "research": 16,
    "updates": 13,
    "archives": 12,
    "scheduler": 99,
    "wellbeing": 19,
}

WORKSPACE = "/home/openclaw/banirisset"
SESSIONS_JSON = "/home/openclaw/.openclaw/agents/reed-archivist/sessions/sessions.json"
STATE_FILE = os.path.join(WORKSPACE, "inbox", ".monitor_v2_state.json")
PROCESSED_DIR = os.path.join(WORKSPACE, "inbox", "processed")
TRIAGE_TTL_HOURS = 24
MANUAL_TRIAGE_CHOICES = {
    "project": "Project",
    "content": "Content",
    "crm": "CRM",
    "task": "Task",
    "knowledge": "Knowledge",
    "research": "Research",
    "ops": "Ops",
    "archive": "Archives",
}

# === CLASSIFICATION RULES ===
FAST_PATH_RULES = [
    {
        "bucket": "Archives",
        "topic": "archives",
        "keywords": [
            r"\barchive\s+(ini|saja)\b", r"\bpindah\s+ke\s+arsip\b",
            r"\bsudah\s+selesai\b", r"\bclosed\b", r"\bselesai,\s+simpan\b",
            r"\bcompleted\b", r"\bclose\s+(project|deal|ticket)\b",
        ],
        "path": "archives/general/",
    },
    {
        "bucket": "Ops",
        "topic": "ops",
        "keywords": [
            r"\bserver\b", r"\bVPS\b", r"\bgateway\b", r"\bdeploy\b",
            r"\bconfig\b", r"\bopenclaw\b", r"\bsystemctl\b",
            r"\bred\s*(bot|gateway|config)\b", r"\berror\s+di\b",
            r"\bgagal\b", r"\bcrash\b", r"\bpm2\b", r"\bcron\b",
            r"\brestart\b", r"\bhealth\s+check\b",
        ],
        "path": "openclaw/ops/tasks.md",
    },
    {
        "bucket": "Reminder",
        "topic": "scheduler",
        "keywords": [
            r"\bingatkan\b", r"\breminder\b", r"\bingat\b",
            r"\bingatkan\s+gw\b", r"\bingatkan\s+saya\b",
            r"\bcatat\s+reminder\b", r"\bjam\s+\d{1,2}",
            r"\bpukul\s+\d{1,2}", r"\bsetengah\s+\d{1,2}",
            r"\b\d{1,2}\.\d{2}\s*(am|pm|pagi|siang|sore|malam)\b",
            r"\bbesok\s+(pagi|siang|sore|malam)\b",
            r"\bnanti\s+(pagi|siang|sore|malam)\b",
            r"\bsetel\s+alarm\b", r"\bbuat\s+reminder\b",
        ],
        "path": "scheduler/queue/",
        "action": "write_reminder",
    },

    {
        "bucket": "Project",
        "topic": "tasks",
        "keywords": [
            r"\bnirva\b", r"\bsentrachat\b", r"\bstop\s*tb\b", r"\bstoptb\b",
            r"\bapps\b", r"\bappssync\b", r"\bpt\s*sin\b",
            r"\bproject\b", r"\bclient\b", r"\bbrief\b", r"\bdeliverable\b",
            r"\bdeadline\b", r"\btor\b", r"\bproposal\b", r"\bscope\b",
            r"\bmilestone\b", r"\bbrand\s*os\b", r"\bcontent\s*os\b",
            r"\btool\s*lab\b",
        ],
        "path_map": {
            "nirva": "clients/nirva/",
            "sentrachat": "clients/sentrachat/",
            r"stop.?tb|stoptb": "clients/stop-tb/",
            r"apps(?!sync)": "clients/apps/",
            "appssync": "clients/appssync/",
            r"pt.?sin": "clients/pt-sin/",
            r"brand.?os": "Brand OS - Bani Risset/",
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
            r"\bide\s+konten\b", r"\bkonten\s+ini\b",
            r"\bproduk\s*digital\b", r"\bjualan\b", r"\bjual\b",
            r"\bmateri\b", r"\bebook\b", r"\bkelas\b", r"\bmodul\b",
            r"\bkursus\b", r"\bpaid\b", r"\bberbayar\b",
            r"\brefine\b", r"\bremix\b", r"\bremake\b",
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
            r"\bcek\b", r"\brapihin\b", r"\bsusun\b", r"\bcompile\b",
        ],
        "path": "daily.md",
    },
    {
        "bucket": "Research",
        "topic": "research",
        "keywords": [
            r"\briset\b", r"\bcari\s*tau\b", r"\banalisis\b",
            r"\bcompare\b", r"\bbandingin\b", r"\bapa\s+bedanya\b",
            r"\bbenchmark\b", r"\bmarket\s*research\b",
            r"\bcompetitor\b", r"\bkompetitor\b", r"\bresearch\b",
        ],
        "path": "research/",
    },
    {
        "bucket": "Knowledge",
        "topic": "knowledge-base",
        "keywords": [
            r"https?://", r"\bsimpan\b", r"\bbookmark\b", r"\breferensi\b",
            r"\bnanti\s*dibaca\b", r"\btools?\b", r"\bresource\b",
            r"\btemplate\b", r"\btutorial\b", r"\bguide\b", r"\bdoc\b",
        ],
        "path": "knowledge-base/",
    },
]
BUCKET_DEFINITIONS = {
    "Archives": "Item yang sudah selesai, ditutup, dipindah ke arsip, atau tidak aktif lagi.",
    "Ops": "Task atau incident teknis: server, VPS, bot, gateway, deployment, config, restart, error infra.",
    "Reminder": "Permintaan pengingat dengan waktu atau jadwal yang jelas.",
    "Project": "Update, brief, deliverable, planning, atau pekerjaan terkait client/project aktif.",
    "CRM": "Kontak, follow-up orang, meeting, deal, relasi, atau status komunikasi personal/client.",
    "Content": "Ide konten, draft posting, thread, caption, blog, newsletter, atau asset publikasi.",
    "Task": "Todo/action item umum yang perlu dikerjakan, dicek, dirapikan, atau direview.",
    "Research": "Permintaan riset, analisis, benchmark, compare, cari tahu, atau eksplorasi aktif.",
    "Knowledge": "Referensi pasif untuk disimpan: link, bookmark, tutorial, doc, template, resource.",
}

# === LOGGING ===
log_dir = os.path.join(WORKSPACE, "inbox")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "monitor_v2.log")),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("inbox_monitor_v2")


# === TELEGRAM API (send only — no getUpdates) ===
def tg_send(method, **params):
    url = f"https://api.telegram.org/bot{SEND_TOKEN}/{method}"
    for attempt in range(3):
        resp = requests.post(url, json=params, timeout=30)
        data = resp.json()
        if data.get("ok"):
            return data
        if data.get("error_code") == 429:
            retry_after = data.get("parameters", {}).get("retry_after", 5)
            log.warning(f"Rate limited, waiting {retry_after}s...")
            time.sleep(retry_after + 1)
        else:
            log.error(f"Telegram API error [{method}]: {data}")
            return data
    return data


def send_message(text, thread_id=None):
    params = {"chat_id": GROUP_CHAT_ID, "text": text, "parse_mode": "HTML"}
    if thread_id:
        params["message_thread_id"] = thread_id
    return tg_send("sendMessage", **params)


def copy_message(message_id, to_thread_id):
    return tg_send(
        "copyMessage",
        chat_id=GROUP_CHAT_ID,
        from_chat_id=GROUP_CHAT_ID,
        message_id=message_id,
        message_thread_id=to_thread_id,
    )


# === CLASSIFICATION ===
def strip_metadata_blocks(text):
    cleaned = re.sub(
        r"Conversation info \(untrusted metadata\):\s*```json.*?```",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    cleaned = re.sub(
        r"Sender \(untrusted metadata\):\s*```json.*?```",
        "",
        cleaned,
        flags=re.DOTALL | re.IGNORECASE,
    )
    cleaned = re.sub(
        r"Replied message \(untrusted, for context\):\s*```json.*?```",
        "",
        cleaned,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return cleaned.strip()


def extract_user_text(raw_text):
    transcript_match = re.search(r"Transcript:\s*(.+)$", raw_text, re.DOTALL | re.IGNORECASE)
    if transcript_match:
        return transcript_match.group(1).strip()

    user_text_match = re.search(r"User text:\s*(.+)$", raw_text, re.DOTALL | re.IGNORECASE)
    if user_text_match:
        candidate = user_text_match.group(1).strip()
        candidate = re.sub(r"\[Replying to .*?\].*?\[/Replying\]", "", candidate, flags=re.DOTALL)
        candidate = re.sub(r"\[Telegram .*?:\s*<media:[^>]+>\s*", "", candidate)
        candidate = re.sub(r"<media:[^>]+>", "", candidate)
        candidate = candidate.strip()
        if candidate:
            return candidate

    cleaned = strip_metadata_blocks(raw_text)
    cleaned = re.sub(r"```.*?```", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"\[Telegram .*?\]", "", cleaned)
    cleaned = re.sub(r"<media:[^>]+>", "", cleaned)
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    return "\n".join(lines).strip()


def normalize_text_for_routing(text):
    text = strip_metadata_blocks(text)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"<media:[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_openclaw_model_provider(provider_name):
    if not os.path.exists(OPENCLAW_CONFIG):
        return None
    try:
        with open(OPENCLAW_CONFIG, encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    return config.get("models", {}).get("providers", {}).get(provider_name)


def get_classifier_runtime():
    provider_name, model_id = CLASSIFIER_MODEL.split("/", 1) if "/" in CLASSIFIER_MODEL else (MANDATORY_PROVIDER, CLASSIFIER_MODEL)
    provider = load_openclaw_model_provider(provider_name) or {}
    base_url = os.environ.get("INBOX_ROUTER_CLASSIFIER_BASE_URL") or provider.get("baseUrl") or os.environ.get("NINE_ROUTER_BASE_URL", "http://100.113.246.119:20128/v1")
    api_key = (
        os.environ.get("INBOX_ROUTER_CLASSIFIER_API_KEY")
        or os.environ.get("NINE_ROUTER_API_KEY")
        or os.environ.get("OLLAMA_CLOUD_API_KEY")
        or provider.get("apiKey")
        or ""
    )
    return {
        "provider": provider_name,
        "model": model_id,
        "base_url": base_url.rstrip("/"),
        "api_key": api_key,
        "max_tokens": CLASSIFIER_MAX_TOKENS,
        "temperature": CLASSIFIER_TEMPERATURE,
    }


def log_classifier_runtime_marker():
    runtime = get_classifier_runtime()
    log.info(
        "Model routing marker: provider=%s model=%s base_url=%s",
        runtime["provider"],
        runtime["model"],
        runtime["base_url"],
    )


def is_conversational(text):
    """
    Detect if a message is a direct conversation/question to REED
    rather than an inbox item to be routed.
    Returns True if should be skipped by the router.
    """
    text_lower = text.lower().strip()

    # Very short messages are likely reactions/replies, not inbox items
    word_count = len(text_lower.split())
    if word_count <= 3:
        return True

    # Starts with greeting — conversational opener
    greetings = ["hai", "halo", "hey", "hi ", "reed", "oi ", "yo "]
    if any(text_lower.startswith(g) for g in greetings):
        # Only conversational if no strong actionable content follows
        strong_action_words = [
            "bikin", "buat", "kerjain", "selesaiin", "fix", "tolong",
            "simpan", "catat", "reminder", "jadwal", "post", "publish",
            "draft", "follow up", "meeting",
        ]
        if not any(w in text_lower for w in strong_action_words):
            return True

    # Direct questions about REED/system behavior
    question_patterns = [
        r"\bperlu\s+ngobrol\b",
        r"\bperlu\s+kirim\b",
        r"\bharus\s+(?:ke\s+)?inbox\b",
        r"\bcara\s+(?:pakai|pake|kerja)\b",
        r"\bgimana\s+(?:cara|kalau|kalo)\b",
        r"\bkamu\s+(?:bisa|tau|tahu)\b",
        r"\blu\s+(?:bisa|tau|tahu)\b",
        r"\blo\s+(?:bisa|tau|tahu)\b",
        r"\bapa\s+(?:itu|ini|bedanya)\b",
        r"\blah\s+masa\b",
        r"\bkok\s+(?:gitu|begitu)\b",
        r"\bwait\b",
        r"\bserius\b.*\?",
    ]
    if any(re.search(p, text_lower) for p in question_patterns):
        return True

    return False


def infer_bucket_from_phrasing(text_lower):
    product_terms = [
        "produk digital", "jualan", "jual", "materi", "ebook",
        "kelas", "kursus", "modul", "berbayar", "paid",
    ]
    transform_terms = ["refine", "remix", "remake", "repurpose", "olah", "susun"]
    action_terms = ["cek", "check", "audit", "review", "rapihin"]

    if any(term in text_lower for term in product_terms):
        if any(term in text_lower for term in transform_terms):
            return "Content", 3.5
        if any(term in text_lower for term in action_terms):
            return "Content", 2.5
    return None, 0


def fast_path_classify(text):
    normalized = normalize_text_for_routing(text)
    text_lower = normalized.lower()
    inferred_bucket, inferred_score = infer_bucket_from_phrasing(text_lower)
    scores = {}

    if inferred_bucket:
        scores[inferred_bucket] = inferred_score

    for rule in FAST_PATH_RULES:
        score = sum(1 for kw in rule["keywords"] if re.search(kw, text_lower))
        if score > 0:
            scores[rule["bucket"]] = scores.get(rule["bucket"], 0) + score

    if not scores:
        return {
            "bucket": None,
            "confidence": 0,
            "reasoning_short": "No fast-path keyword match.",
            "source": "fast_path_none",
            "scores": {},
        }

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best, best_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0
    delta = best_score - second_score
    confidence = min(100, max(0, int(55 + (best_score * 10) + (delta * 12))))
    reasoning = f"Keyword score={best_score}, delta={delta}."

    # Generic Task verbs (tolong/cek/bikin) often collide with richer intents
    # like Content/Project/Knowledge. Force LLM arbitration for these borderline cases.
    if best == "Task":
        competing_signal = max(
            scores.get("Project", 0),
            scores.get("Content", 0),
            scores.get("Knowledge", 0),
            scores.get("Research", 0),
        )
        if best_score <= 2:
            confidence = min(confidence, 78)
            reasoning = f"{reasoning} Weak task signal; prefer LLM check."
        if competing_signal >= 1 and delta <= 1:
            confidence = min(confidence, 72)
            reasoning = f"{reasoning} Ambiguous with competing non-task signal."

    if best == "Reminder" and best_score >= 2:
        confidence = max(confidence, 95)
    elif delta >= 2 and best_score >= 2:
        confidence = max(confidence, 85)
    return {
        "bucket": best,
        "confidence": confidence,
        "reasoning_short": reasoning,
        "source": "fast_path",
        "scores": scores,
    }


def build_classifier_prompt(text):
    bucket_lines = []
    for bucket_name, definition in BUCKET_DEFINITIONS.items():
        bucket_lines.append(f"- {bucket_name}: {definition}")
    buckets = "\n".join(bucket_lines)
    return (
        "Kamu adalah classifier routing untuk Telegram Inbox.\n"
        "Pilih tepat satu bucket paling cocok dari daftar.\n"
        "Confidence harus angka 0-100.\n"
        "Kalau pesan kurang jelas atau butuh tebakan tinggi, pilih bucket terbaik tapi turunkan confidence.\n"
        "Reasoning harus singkat, maksimum satu kalimat.\n"
        "Jawab JSON valid saja dengan format:\n"
        '{"bucket":"BucketName","confidence":0,"reasoning_short":"..."}\n\n'
        f"Daftar bucket:\n{buckets}\n\n"
        f"Pesan user:\n{text}"
    )


def parse_classifier_response(content):
    text = content.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    decoder = json.JSONDecoder()
    if "{" in text:
        start = text.index("{")
        try:
            parsed, _ = decoder.raw_decode(text[start:])
            return parsed
        except json.JSONDecodeError:
            pass

    bucket_match = re.search(r'"bucket"\s*:\s*"([^"]+)"', text)
    confidence_match = re.search(r'"confidence"\s*:\s*(\d{1,3})', text)
    reasoning_match = re.search(r'"reasoning_short"\s*:\s*"([^"]*)"', text)
    if bucket_match:
        return {
            "bucket": bucket_match.group(1),
            "confidence": int(confidence_match.group(1)) if confidence_match else 0,
            "reasoning_short": reasoning_match.group(1) if reasoning_match else "",
        }
    raise ValueError(f"Unable to parse classifier response: {content[:200]}")


def call_llm_classifier(text):
    runtime = get_classifier_runtime()
    if not runtime["api_key"]:
        raise RuntimeError("Classifier API key missing.")

    payload = {
        "model": runtime["model"],
        "temperature": runtime.get("temperature", 0),
        "max_tokens": runtime.get("max_tokens", 180),
        "messages": [
            {
                "role": "system",
                "content": "Return valid JSON only. No markdown. No extra text.",
            },
            {
                "role": "user",
                "content": build_classifier_prompt(text),
            },
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {runtime['api_key']}",
    }
    response = requests.post(
        f"{runtime['base_url']}/chat/completions",
        headers=headers,
        json=payload,
        timeout=CLASSIFIER_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"].strip()
    parsed = parse_classifier_response(content)
    bucket = parsed.get("bucket")
    confidence = int(parsed.get("confidence", 0))
    reasoning_short = str(parsed.get("reasoning_short", "")).strip()[:160]
    if bucket not in BUCKET_DEFINITIONS:
        raise ValueError(f"Invalid classifier bucket: {bucket}")
    return {
        "bucket": bucket,
        "confidence": max(0, min(100, confidence)),
        "reasoning_short": reasoning_short or "LLM classified without short reason.",
        "source": "llm",
    }


def classify(text):
    fast_result = fast_path_classify(text)
    if fast_result["bucket"] and fast_result["confidence"] >= 85:
        return fast_result

    try:
        llm_result = call_llm_classifier(normalize_text_for_routing(text))
        if fast_result["bucket"] and fast_result["bucket"] == llm_result["bucket"]:
            llm_result["confidence"] = max(llm_result["confidence"], min(100, fast_result["confidence"] + 5))
            llm_result["reasoning_short"] = f"{llm_result['reasoning_short']} Fast-path mendukung bucket yang sama."
        return llm_result
    except Exception as exc:
        if fast_result["bucket"]:
            fallback = dict(fast_result)
            fallback["source"] = "fast_path_fallback"
            fallback["reasoning_short"] = f"{fast_result['reasoning_short']} LLM fallback error: {exc}"
            return fallback
        return {
            "bucket": None,
            "confidence": 0,
            "reasoning_short": f"LLM fallback error: {exc}",
            "source": "llm_error",
            "scores": {},
        }


def get_rule(bucket):
    return next((r for r in FAST_PATH_RULES if r["bucket"] == bucket), None)


def get_project_path(text, rule):
    if "path_map" not in rule:
        return rule.get("path", "inbox/unsorted/")
    text_lower = text.lower()
    for pattern, path in rule["path_map"].items():
        if re.search(pattern, text_lower):
            return path
    return "inbox/unsorted/"


# === STATE ===
def default_state():
    return {"processed_message_ids": [], "pending_triage": []}


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)
        if "processed_message_ids" not in state:
            state["processed_message_ids"] = []
        if "pending_triage" not in state:
            state["pending_triage"] = []
        return state
    return default_state()


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def prune_pending_triage(entries, now=None):
    now = now or datetime.now()
    kept = []
    for entry in entries:
        created_at = entry.get("created_at")
        if not created_at:
            continue
        try:
            created_dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        if now - created_dt > timedelta(hours=TRIAGE_TTL_HOURS):
            continue
        if entry.get("status") != "pending":
            continue
        kept.append(entry)
    return kept


def parse_manual_triage_choice(text):
    normalized = normalize_text_for_routing(text).lower()
    normalized = re.sub(r"[^a-z-]+", " ", normalized).strip()
    tokens = normalized.split()
    if len(tokens) != 1:
        return None
    return MANUAL_TRIAGE_CHOICES.get(tokens[0])


def remember_pending_triage(state, tg_msg_id, text, unsorted_path):
    state["pending_triage"] = prune_pending_triage(state.get("pending_triage", []))
    state["pending_triage"].append({
        "source_message_id": str(tg_msg_id),
        "unsorted_path": unsorted_path,
        "original_text": text,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending",
        "awaiting_choice": True,
    })


def consume_pending_triage(state):
    entries = prune_pending_triage(state.get("pending_triage", []))
    if not entries:
        state["pending_triage"] = []
        return None
    selected = entries[-1]
    remaining = []
    for entry in entries:
        if entry is selected:
            continue
        remaining.append(entry)
    state["pending_triage"] = remaining
    return selected


def mark_unsorted_resolved(unsorted_path, bucket):
    if not unsorted_path or not os.path.exists(unsorted_path):
        return
    with open(unsorted_path, encoding="utf-8") as f:
        content = f.read()
    content = content.replace("**Status:** pending-triage", f"**Status:** resolved-{bucket.lower()}")
    if f"**Resolved to:** {bucket}" not in content:
        content = content.rstrip() + f"\n**Resolved to:** {bucket}\n"
    with open(unsorted_path, "w", encoding="utf-8") as f:
        f.write(content)


# === SESSION FILE READER ===
def get_inbox_session_file():
    """Find current reed-archivist session JSONL for topic:11."""
    if not os.path.exists(SESSIONS_JSON):
        return None

    with open(SESSIONS_JSON) as f:
        sessions = json.load(f)

    for key, sess in sessions.items():
        if "topic:11" in key and "reed-archivist" in key:
            session_file = sess.get("sessionFile")
            if session_file and os.path.exists(session_file):
                return session_file

    return None


def parse_session_messages(session_file):
    """
    Parse JSONL session file, return list of user messages from inbox topic.
    Each item: {"message_id": str, "text": str, "timestamp": str}
    """
    seen_ids = set()
    messages = []
    with open(session_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if entry.get("type") != "message":
                continue

            msg = entry.get("message", {})
            if msg.get("role") != "user":
                continue

            content = msg.get("content", "")
            if isinstance(content, list):
                content = " ".join(
                    c.get("text", "") for c in content if isinstance(c, dict)
                )

            # Extract Telegram message metadata from the injected JSON block
            meta_match = re.search(
                r'"message_id":\s*"(\d+)".*?"sender_id":\s*"(\d+)".*?"topic_id":\s*"11"',
                content, re.DOTALL
            )
            if not meta_match:
                continue

            tg_message_id = meta_match.group(1)
            sender_id = meta_match.group(2)

            if sender_id != BANI_USER_ID:
                continue

            # Deduplicate by message_id within the same session file
            if tg_message_id in seen_ids:
                continue
            seen_ids.add(tg_message_id)

            user_text = extract_user_text(content)
            if not user_text:
                continue

            messages.append({
                "message_id": tg_message_id,
                "text": user_text,
                "timestamp": entry.get("timestamp", ""),
            })

    return messages



# === REMINDER WRITER ===
def parse_reminder_time(text):
    """
    Parse reminder time from text. Returns (hour, minute, day_offset, description).
    Supports: "jam 3 sore", "besok pagi", "nanti jam 14.00", "ingatan jam 9 malam"
    """
    import re as re2
    text_lower = text.lower()

    # Time mappings
    time_words = {
        "pagi": (8, 0),
        "siang": (12, 0),
        "sore": (15, 0),
        "malam": (20, 0),
        "tengah malam": (0, 0),
        "subuh": (5, 0),
        "dzuhur": (12, 0),
        "ashar": (15, 0),
        "maghrib": (18, 0),
        "isya": (19, 0),
    }

    day_offset = 0
    hour = None
    minute = 0

    # Check for "besok" or "nanti"
    if "besok" in text_lower:
        day_offset = 1
    elif "lusa" in text_lower:
        day_offset = 2

    # Pattern: "jam X" or "pukul X" or "jam X.YY"
    jam_match = re2.search(r"(?:jam|pukul)\s+(\d{1,2})[.:,]?(\d{0,2})", text_lower)
    if jam_match:
        hour = int(jam_match.group(1))
        if jam_match.group(2):
            minute = int(jam_match.group(2))
    else:
        # Pattern: "jam X pagi/siang/sore/malam"
        for word, (h, m) in time_words.items():
            if word in text_lower:
                hour = h
                minute = m
                break

    # Fallback: if no time found, default to next hour
    if hour is None:
        from datetime import datetime
        hour = (datetime.now().hour + 1) % 24
        minute = 0

    # Extract reminder description (everything after the time phrase)
    desc_match = re2.search(r"(?:ingatkan|reminder|ingat|alarm|catat).*?(?:ke|untuk|buat|tentang)\s+(.+)$", text_lower)
    if not desc_match:
        # Take everything after time words
        desc_match = re2.search(r"(?:jam|pukul)\s+\d{1,2}[.:,]?\d{0,2}\s*(?:pagi|siang|sore|malam)?\s*[,\s]+(.+)$", text_lower)
    if desc_match:
        description = desc_match.group(1).strip()
    else:
        description = text

    return hour, minute, day_offset, description


def write_reminder_file(text, tg_msg_id):
    """
    Parse reminder request and write to scheduler/queue/.
    File name encodes target time for easy sorting.
    """
    from datetime import datetime, timedelta
    import json

    hour, minute, day_offset, description = parse_reminder_time(text)

    now = datetime.now()
    target_date = now + timedelta(days=day_offset)
    target = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # If target is in the past (for today), push to tomorrow
    if target < now:
        target = target + timedelta(days=1)

    # Filename: YYYYMMDD_HHMM_reminder.json
    filename = f"{target.strftime('%Y%m%d_%H%M')}_reminder.json"
    queue_dir = os.path.join(WORKSPACE, "scheduler", "queue")
    os.makedirs(queue_dir, exist_ok=True)
    filepath = os.path.join(queue_dir, filename)

    reminder_data = {
        "id": f"r_{tg_msg_id}_{int(now.timestamp())}",
        "source_message_id": tg_msg_id,
        "source_topic": "inbox",
        "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "target_at": target.strftime("%Y-%m-%d %H:%M"),
        "target_timestamp": int(target.timestamp()),
        "description": description,
        "original_text": text,
        "delivered": False,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(reminder_data, f, indent=2, ensure_ascii=False)

    return filepath, target


# === FILE WRITER ===
def write_processed_file(text, bucket, path):
    now = datetime.now()
    ts = now.strftime("%Y-%m-%d_%H-%M-%S")
    date_str = now.strftime("%Y-%m-%d %H:%M")
    slug = re.sub(r"[^a-zA-Z0-9_-]", "", text[:30].replace(" ", "-"))

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    filepath = os.path.join(PROCESSED_DIR, f"{ts}_{slug}.md")

    content = f"""# [{bucket}] — {text[:60]}

**Timestamp:** {date_str}
**Bucket:** {bucket}
**Routed to:** {path}
**Original:** {text}

## Status
- Processed: ✅
- Routed to: {path}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def write_unsorted_file(text, tg_msg_id):
    filepath = write_unsorted_item(
        text,
        tg_msg_id=str(tg_msg_id),
        title=text[:60],
    )
    return filepath


def route_bucket_message(text, tg_msg_id, bucket, rule):
    if rule.get("action") == "write_reminder":
        filepath, target = write_reminder_file(text, tg_msg_id)
        reply = (
            f"⏰ <b>[REMINDER SET]</b>\n"
            f"🕐 {target.strftime('%A, %d %b %H:%M')}\n"
            f"📝 {text[:80]}\n\n"
            f"REED DULL akan remind kamu di topic <b>Updates</b>."
        )
        send_message(reply, thread_id=TOPICS["inbox"])
        log.info(f"Reminder set: #{tg_msg_id} → {filepath}")
        return

    target_topic = TOPICS.get(rule["topic"], TOPICS["inbox"])
    path = get_project_path(text, rule)
    copy_message(tg_msg_id, target_topic)
    write_processed_file(text, bucket, path)
    log.info(f"Routed: #{tg_msg_id} → {bucket} → {path}")


# === MAIN PROCESSOR ===
def process_inbox():
    state = load_state()
    processed_ids = set(state.get("processed_message_ids", []))
    state["pending_triage"] = prune_pending_triage(state.get("pending_triage", []))

    session_file = get_inbox_session_file()
    if not session_file:
        log.debug("No inbox session file found — no activity yet")
        return 0

    messages = parse_session_messages(session_file)
    new_messages = [m for m in messages if m["message_id"] not in processed_ids]

    if not new_messages:
        return 0

    count = 0
    for msg in new_messages:
        text = msg["text"]
        tg_msg_id = int(msg["message_id"])
        manual_bucket = parse_manual_triage_choice(text)

        log.info(f"Processing inbox message #{tg_msg_id}: {text[:80]}")

        if manual_bucket:
            pending = consume_pending_triage(state)
            if pending:
                rule = get_rule(manual_bucket)
                source_message_id = int(pending["source_message_id"])
                route_bucket_message(pending["original_text"], source_message_id, manual_bucket, rule)
                mark_unsorted_resolved(pending.get("unsorted_path"), manual_bucket)
                write_processed_file(
                    f"{text} → {pending['original_text']}",
                    f"ManualTriage:{manual_bucket}",
                    get_project_path(pending["original_text"], rule),
                )
                log.info(
                    f"Manual triage resolved: choice=#{tg_msg_id} source=#{source_message_id} bucket={manual_bucket}"
                )
                processed_ids.add(msg["message_id"])
                count += 1
                continue

        # Skip conversational messages — let REED handle them directly
        if is_conversational(text):
            log.info(f"Skipped (conversational): #{tg_msg_id}")
            processed_ids.add(msg["message_id"])
            count += 1
            continue

        classification = classify(text)
        bucket = classification.get("bucket")
        confidence = classification.get("confidence", 0)
        reasoning_short = classification.get("reasoning_short", "")
        source = classification.get("source", "unknown")

        if bucket and confidence >= CLASSIFIER_THRESHOLD:
            log.info(
                f"Classifier {source}: #{tg_msg_id} bucket={bucket} confidence={confidence} reason={reasoning_short}"
            )
            rule = get_rule(bucket)
            route_bucket_message(text, tg_msg_id, bucket, rule)

        else:
            log.info(
                f"Classifier fallback-unsorted: #{tg_msg_id} bucket={bucket} confidence={confidence} reason={reasoning_short}"
            )
            unsorted_path = write_unsorted_file(text, tg_msg_id)
            remember_pending_triage(state, tg_msg_id, text, unsorted_path)
            write_processed_file(text, "Unsorted", "inbox/unsorted/")
            preview = normalize_text_for_routing(text)
            if len(preview) > 140:
                preview = preview[:137] + "..."
            ask = (
                f"❓ Ini belum cukup jelas, jadi gw taruh dulu di <b>unsorted</b>.\n"
                f"<i>{preview}</i>\n\n"
                f"Balas aja: project / content / crm / task / knowledge / research / ops / archive"
            )
            send_message(ask, thread_id=TOPICS["inbox"])
            log.info(f"Persistence success: message_id={tg_msg_id} path={unsorted_path}")
            log.info(f"Unsorted: #{tg_msg_id}")

        processed_ids.add(msg["message_id"])
        count += 1

    state["processed_message_ids"] = list(processed_ids)
    # Keep only last 1000 IDs to prevent unbounded growth
    if len(state["processed_message_ids"]) > 1000:
        state["processed_message_ids"] = state["processed_message_ids"][-1000:]
    save_state(state)
    return count


def run_once():
    if not SEND_TOKEN:
        log.error("TELEGRAM_BOT_TOKEN not set!")
        sys.exit(1)
    log_classifier_runtime_marker()
    count = process_inbox()
    log.info(f"Processed {count} inbox items")


def run_daemon(interval=20):
    if not SEND_TOKEN:
        log.error("TELEGRAM_BOT_TOKEN not set!")
        sys.exit(1)

    log.info(f"Inbox monitor v2 started (poll every {interval}s, file-based)")
    log_classifier_runtime_marker()
    while True:
        try:
            process_inbox()
        except KeyboardInterrupt:
            log.info("Stopped by user")
            break
        except Exception as e:
            log.error(f"Error: {e}")
        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="REED Inbox Monitor v2 (file-based)")
    parser.add_argument("--daemon", action="store_true")
    parser.add_argument("--interval", type=int, default=20)
    args = parser.parse_args()

    if args.daemon:
        run_daemon(args.interval)
    else:
        run_once()
