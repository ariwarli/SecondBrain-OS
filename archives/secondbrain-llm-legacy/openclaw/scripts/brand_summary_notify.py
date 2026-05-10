#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import urllib.parse
import urllib.request
from typing import List, Tuple

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = "-1003344368011"
TOPIC_ID = "11"
REPO_DIR = "/home/openclaw/banirisset"
STATE_FILE = "/home/openclaw/.openclaw/workspace/.brand-summary-last-commit"
TRACKED_PATHS = [
    "Brand OS - Bani Risset/claude-project/docs",
    "Brand OS - Bani Risset/claude-project/memory.md",
]


def run_git(args: List[str]) -> str:
    result = subprocess.run(
        ["git", "-C", REPO_DIR, *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_head_commit() -> str:
    try:
        return run_git(["rev-parse", "HEAD"])
    except subprocess.CalledProcessError:
        return ""


def get_last_notified_commit() -> str:
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def set_last_notified_commit(commit_hash: str) -> None:
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(commit_hash + "\n")


def get_commit_meta(commit_hash: str) -> Tuple[str, str, str]:
    raw = run_git(
        [
            "show",
            "-s",
            "--format=%H%n%cd%n%s",
            "--date=format:%Y-%m-%d %H:%M WIB",
            commit_hash,
        ]
    )
    lines = raw.splitlines()
    return lines[0], lines[1], lines[2]


def get_changed_files(commit_hash: str) -> List[str]:
    raw = run_git(
        [
            "show",
            "--name-only",
            "--format=",
            commit_hash,
            "--",
            *TRACKED_PATHS,
        ]
    )
    files = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if not line.endswith(".md"):
            continue
        files.append(line)
    return files


def get_diff(commit_hash: str, max_chars: int = 12000) -> str:
    diff = run_git(
        [
            "show",
            "--unified=1",
            "--format=",
            commit_hash,
            "--",
            *TRACKED_PATHS,
        ]
    )
    return diff[:max_chars]


def fallback_summary(files: List[str]) -> str:
    if not files:
        return "- Tidak ada file brand markdown yang berubah."
    bullets = []
    for path in files[:5]:
        bullets.append(f"- Update pada `{os.path.basename(path)}`")
    return "\n".join(bullets)


def summarize_changes(commit_time: str, commit_subject: str, files: List[str], diff: str) -> str:
    file_list = "\n".join(f"- {os.path.basename(path)}" for path in files) or "- Tidak ada file markdown terdeteksi"
    if not diff.strip():
        return fallback_summary(files)
    if not DEEPSEEK_KEY:
        return fallback_summary(files)

    prompt = (
        "Brand knowledge baru diupdate. Jangan ringkas ulang seluruh brand profile. "
        "Fokus hanya pada perubahan TERBARU dari diff ini.\n\n"
        f"Waktu update: {commit_time}\n"
        f"Commit: {commit_subject}\n"
        f"File berubah:\n{file_list}\n\n"
        "Tulis output Bahasa Indonesia singkat, no BS, format bullet.\n"
        "Isi maksimal 4 bullet dan fokus pada:\n"
        "1. informasi apa yang baru ditambah/diubah,\n"
        "2. bagian mana yang direvisi,\n"
        "3. implikasi praktis jika ada.\n\n"
        f"Diff:\n{diff}"
    )
    payload = {
        "model": "deepseek-chat",
        "max_tokens": 350,
        "messages": [
            {"role": "system", "content": "Asisten ringkas. Fokus ke delta/perubahan terbaru saja. Bahasa Indonesia. No basa-basi."},
            {"role": "user", "content": prompt},
        ],
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_KEY}",
        },
    )
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
        return resp["choices"][0]["message"]["content"].strip()
    except Exception:
        return fallback_summary(files)


def build_message(commit_time: str, commit_subject: str, files: List[str], summary: str) -> str:
    file_line = ", ".join(os.path.basename(path) for path in files[:4]) if files else "-"
    if len(files) > 4:
        file_line += f" +{len(files) - 4} file lain"
    return (
        "🧠 Brand knowledge updated\n\n"
        f"Update terakhir: {commit_time}\n"
        f"Sumber: {commit_subject}\n"
        f"File: {file_line}\n\n"
        "Perubahan info:\n"
        f"{summary}"
    )


def send_telegram(text: str) -> None:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    body = urllib.parse.urlencode(
        {
            "chat_id": CHAT_ID,
            "message_thread_id": TOPIC_ID,
            "text": text,
        }
    ).encode()
    urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=10)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    head_commit = get_head_commit()
    if not head_commit:
        print("no HEAD commit found")
        return 0

    files = get_changed_files(head_commit)
    if not files:
        print("no brand-doc change in latest push")
        return 0

    if head_commit == get_last_notified_commit():
        print("latest brand-doc commit already notified")
        return 0

    _, commit_time, commit_subject = get_commit_meta(head_commit)
    diff = get_diff(head_commit)
    summary = summarize_changes(commit_time, commit_subject, files, diff)
    message = build_message(commit_time, commit_subject, files, summary)

    if args.dry_run:
        print(message)
        return 0

    if not BOT_TOKEN:
        print("telegram bot token not set; notification skipped")
        return 0

    send_telegram(message)
    set_last_notified_commit(head_commit)
    print("notif sent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
