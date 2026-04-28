#!/usr/bin/env python3
"""
Auto checkpoint every 20 user messages per session.

Design goals:
- Runs safely out-of-process (does not touch OpenClaw runtime config/process).
- Reads session JSONL logs from /home/openclaw/.openclaw/agents/*/sessions.
- Writes Obsidian-compatible markdown checkpoints to knowledge-base/wiki/sessions.
- Maintains a compact "active" summary per session (drops stale context).
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from model_router import get_wiki_model
except ImportError:
    get_wiki_model = None


WORKSPACE = Path("/home/openclaw/banirisset")
AGENTS_ROOT = Path("/home/openclaw/.openclaw/agents")
KB_ROOT = WORKSPACE / "knowledge-base" / "wiki"
SESSIONS_OUT = KB_ROOT / "sessions"
LOG_PATH = KB_ROOT / "log.md"
INDEX_PATH = KB_ROOT / "index.md"
STATE_PATH = WORKSPACE / "state" / "session-checkpoint-state.json"
STATE_META_PATH = WORKSPACE / "state" / "session-checkpoint-meta.json"
WORKER_LOG_PATH = WORKSPACE / "state" / "session-checkpoint.log"

CHECKPOINT_EVERY = 20

DECISION_KW = (
    "setuju",
    "final",
    "gunakan",
    "pakai",
    "lanjut",
    "delete",
    "hapus",
    "implement",
    "sync",
    "ok",
    "oke",
)

BLOCKER_KW = (
    "error",
    "gagal",
    "rusak",
    "konflik",
    "conflict",
    "timeout",
    "failed",
    "broken",
)

ACTION_KW = (
    "lanjut",
    "buat",
    "generate",
    "update",
    "sync",
    "cek",
    "review",
    "deploy",
    "push",
)

HF_PREFIX = "huggingface/"
HF_PROVIDER = "huggingface"


@dataclass
class SessionMeta:
    agent_id: str
    session_key: str
    session_id: str
    jsonl_path: Path


def ensure_dirs() -> None:
    (WORKSPACE / "state").mkdir(parents=True, exist_ok=True)
    KB_ROOT.mkdir(parents=True, exist_ok=True)
    SESSIONS_OUT.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        LOG_PATH.write_text("# Wiki Log\n\n", encoding="utf-8")
    if not INDEX_PATH.exists():
        INDEX_PATH.write_text(
            "# Wiki Index\n\n"
            "## Session Checkpoints\n"
            "- `sessions/` otomatis diisi checkpoint tiap 20 chat per session.\n",
            encoding="utf-8",
        )
    if not WORKER_LOG_PATH.exists():
        WORKER_LOG_PATH.write_text("", encoding="utf-8")


def log_worker(message: str) -> None:
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    with WORKER_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")


def get_wiki_model_summary() -> Optional[str]:
    if get_wiki_model is None:
        return None
    try:
        primary, fallback = get_wiki_model()
    except Exception:
        return None
    summary = f"{primary.provider}/{primary.model_id}"
    if fallback is not None:
        summary += f" fallback={fallback.provider}/{fallback.model_id}"
    return summary


def load_state() -> Dict[str, int]:
    if not STATE_PATH.exists():
        return {}
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            out: Dict[str, int] = {}
            for k, v in data.items():
                if isinstance(k, str) and isinstance(v, int):
                    out[k] = v
            return out
    except Exception:
        pass
    return {}


def save_state(state: Dict[str, int]) -> None:
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_meta_state() -> Dict[str, float]:
    if not STATE_META_PATH.exists():
        return {}
    try:
        data = json.loads(STATE_META_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            out: Dict[str, float] = {}
            for k, v in data.items():
                if isinstance(k, str) and isinstance(v, (int, float)):
                    out[k] = float(v)
            return out
    except Exception:
        pass
    return {}


def save_meta_state(meta: Dict[str, float]) -> None:
    STATE_META_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def discover_sessions() -> List[SessionMeta]:
    out: List[SessionMeta] = []
    for store_path in AGENTS_ROOT.glob("*/sessions/sessions.json"):
        agent_id = store_path.parents[1].name
        try:
            store = json.loads(store_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(store, dict):
            continue

        sessions_dir = store_path.parent
        for session_key, entry in store.items():
            if not isinstance(entry, dict):
                continue
            session_id = entry.get("sessionId")
            if not isinstance(session_id, str) or not session_id:
                continue

            direct = sessions_dir / f"{session_id}.jsonl"
            topic_matches = list(sessions_dir.glob(f"{session_id}-topic-*.jsonl"))
            jsonl_path = direct if direct.exists() else (topic_matches[0] if topic_matches else None)
            if not jsonl_path or not jsonl_path.exists():
                continue

            out.append(
                SessionMeta(
                    agent_id=agent_id,
                    session_key=session_key,
                    session_id=session_id,
                    jsonl_path=jsonl_path,
                )
            )
    return out


def prune_huggingface_overrides() -> int:
    """Remove stale HuggingFace overrides from session stores.

    This keeps runtime clean when no HuggingFace API key is configured.
    """
    changes = 0
    for store_path in AGENTS_ROOT.glob("*/sessions/sessions.json"):
        try:
            store = json.loads(store_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(store, dict):
            continue

        changed_here = 0
        for _, entry in store.items():
            if not isinstance(entry, dict):
                continue

            provider_override = entry.get("providerOverride")
            if isinstance(provider_override, str) and provider_override == HF_PROVIDER:
                entry.pop("providerOverride", None)
                changed_here += 1

            model_override = entry.get("modelOverride")
            if isinstance(model_override, str) and model_override.startswith(HF_PREFIX):
                entry.pop("modelOverride", None)
                changed_here += 1

            fallback_model = entry.get("fallbackNoticeSelectedModel")
            if isinstance(fallback_model, str) and fallback_model.startswith(HF_PREFIX):
                entry.pop("fallbackNoticeSelectedModel", None)
                changed_here += 1

            model_control = entry.get("modelControl")
            if isinstance(model_control, dict):
                to_delete = [
                    key
                    for key, value in model_control.items()
                    if isinstance(value, str) and HF_PROVIDER in value
                ]
                for key in to_delete:
                    model_control.pop(key, None)
                    changed_here += 1
                if not model_control:
                    entry.pop("modelControl", None)

        if changed_here > 0:
            store_path.write_text(json.dumps(store, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changes += changed_here

    return changes


def clean_text(text: str) -> str:
    text = re.sub(r"Conversation info \(untrusted metadata\):\s*```json.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"Sender \(untrusted metadata\):\s*```json.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_heartbeat_noise(text: str) -> bool:
    normalized = clean_text(text).lower()
    if not normalized:
        return True

    heartbeat_markers = (
        "read heartbeat.md if it exists",
        "follow it strictly",
        "reply heartbeat_ok",
        "heartbeat_ok",
        "do not read docs/heartbeat.md",
        "workspace file /home/openclaw/.openclaw/workspaces/",
    )
    return any(marker in normalized for marker in heartbeat_markers)


def extract_text(message_obj: dict) -> str:
    content = message_obj.get("content")
    if not isinstance(content, list):
        return ""
    parts: List[str] = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            val = item.get("text")
            if isinstance(val, str) and val.strip():
                parts.append(val)
    return clean_text("\n".join(parts))


def read_user_messages(jsonl_path: Path) -> List[Tuple[str, str]]:
    msgs: List[Tuple[str, str]] = []
    for line in jsonl_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if obj.get("type") != "message":
            continue
        message = obj.get("message")
        if not isinstance(message, dict):
            continue
        if message.get("role") != "user":
            continue
        text = extract_text(message)
        if not text:
            continue
        ts = obj.get("timestamp")
        if not isinstance(ts, str):
            ts = ""
        msgs.append((ts, text))
    return msgs


def pick_lines(messages: List[str], keywords: Tuple[str, ...], limit: int = 4) -> List[str]:
    out: List[str] = []
    for msg in messages:
        lower = msg.lower()
        if any(k in lower for k in keywords):
            out.append(msg)
        if len(out) >= limit:
            break
    return out


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "session"


def session_slug(meta: SessionMeta) -> str:
    return slugify(f"{meta.agent_id}-{meta.session_key}")


def ts_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def write_checkpoint(meta: SessionMeta, batch_no: int, chunk: List[Tuple[str, str]]) -> Path:
    slug = session_slug(meta)
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    out_path = SESSIONS_OUT / f"{stamp}-{slug}-cp-{batch_no}.md"

    texts = [m for _, m in chunk]
    context_texts = [msg for msg in texts if not is_heartbeat_noise(msg)]
    decisions = pick_lines(context_texts, DECISION_KW)
    blockers = pick_lines(context_texts, BLOCKER_KW)
    actions = pick_lines(context_texts[-8:], ACTION_KW)

    facts = []
    seen = set()
    for msg in context_texts:
        compact = msg.strip()
        if not compact or compact in seen:
            continue
        seen.add(compact)
        facts.append(compact)
        if len(facts) >= 8:
            break

    body = [
        f"# Session Checkpoint: {slug} (batch {batch_no})",
        "",
        f"**Saved at:** {ts_now()}",
        f"**Agent:** {meta.agent_id}",
        f"**Session key:** `{meta.session_key}`",
        f"**Session file:** `{meta.jsonl_path}`",
        f"**Range:** user message {(batch_no - 1) * CHECKPOINT_EVERY + 1} s/d {batch_no * CHECKPOINT_EVERY}",
        "",
        "## Keputusan",
    ]
    if decisions:
        body.extend([f"- {x}" for x in decisions])
    else:
        body.append("- Tidak ada keputusan eksplisit pada batch ini.")

    body.extend(["", "## Fakta Baru"])
    if facts:
        body.extend([f"- {x}" for x in facts])
    else:
        body.append("- Tidak ada fakta baru yang signifikan.")

    body.extend(["", "## Blocker"])
    if blockers:
        body.extend([f"- {x}" for x in blockers])
    else:
        body.append("- Tidak ada blocker yang terdeteksi.")

    body.extend(["", "## Next Action"])
    if actions:
        body.extend([f"- {x}" for x in actions])
    elif context_texts:
        body.append(f"- Follow-up dari pesan terbaru: {context_texts[-1]}")
    else:
        body.append("- Tidak ada next action terdeteksi.")

    body.append("")
    out_path.write_text("\n".join(body), encoding="utf-8")

    # Active summary = overwrite with latest relevant context (drops stale entries)
    active_path = SESSIONS_OUT / f"{slug}-active.md"
    active_lines = [
        f"# Active Context: {slug}",
        "",
        f"**Last checkpoint:** `{out_path.name}`",
        f"**Updated at:** {ts_now()}",
        "",
        "## Current Decisions",
    ]
    active_lines.extend([f"- {x}" for x in (decisions[:5] or ["Belum ada keputusan kuat."])])
    active_lines.extend(["", "## Current Blockers"])
    active_lines.extend([f"- {x}" for x in (blockers[:5] or ["Tidak ada blocker aktif."])])
    active_lines.extend(["", "## Current Next Actions"])
    active_lines.extend(
        [f"- {x}" for x in (actions[:5] or ([context_texts[-1]] if context_texts else ["Tidak ada aksi baru."]))]
    )
    active_lines.append("")
    active_path.write_text("\n".join(active_lines), encoding="utf-8")

    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(
            f"- {ts_now()} | session-checkpoint | {meta.agent_id} | "
            f"{meta.session_key} | batch={batch_no} | file=`sessions/{out_path.name}`\n"
        )

    return out_path


def run_once(verbose: bool = False) -> int:
    ensure_dirs()
    pruned = prune_huggingface_overrides()
    if pruned > 0:
        log_worker(f"hygiene removed_huggingface_overrides={pruned}")
    state = load_state()
    meta_state = load_meta_state()
    changes = 0

    for meta in discover_sessions():
        try:
            mtime = float(meta.jsonl_path.stat().st_mtime)
            last_seen_mtime = meta_state.get(meta.session_id)
            if last_seen_mtime is not None and mtime <= last_seen_mtime:
                continue

            user_msgs = read_user_messages(meta.jsonl_path)
            total = len(user_msgs)
            if total < CHECKPOINT_EVERY:
                meta_state[meta.session_id] = mtime
                continue

            max_batch = total // CHECKPOINT_EVERY
            last_batch = state.get(meta.session_id, 0)
            if max_batch <= last_batch:
                meta_state[meta.session_id] = mtime
                continue

            for batch in range(last_batch + 1, max_batch + 1):
                start = (batch - 1) * CHECKPOINT_EVERY
                end = batch * CHECKPOINT_EVERY
                out = write_checkpoint(meta, batch, user_msgs[start:end])
                changes += 1
                if verbose:
                    print(f"checkpoint: {meta.session_key} batch={batch} -> {out}")

            state[meta.session_id] = max_batch
            meta_state[meta.session_id] = mtime
        except Exception as exc:
            log_worker(
                "error session="
                f"{meta.session_key} agent={meta.agent_id} file={meta.jsonl_path} err={exc}"
            )
            continue

    save_state(state)
    save_meta_state(meta_state)
    if verbose:
        print(f"done. checkpoints_written={changes}")
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto checkpoint every 20 chats per session")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--verbose", action="store_true", help="Print checkpoint actions")
    args = parser.parse_args()

    # current implementation is oneshot only
    _ = args.once
    try:
        wiki_model = get_wiki_model_summary()
        if wiki_model:
            log_worker(f"wiki_model={wiki_model}")
        written = run_once(verbose=args.verbose)
        log_worker(f"ok checkpoints_written={written}")
    except Exception as exc:
        log_worker(f"fatal err={exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
