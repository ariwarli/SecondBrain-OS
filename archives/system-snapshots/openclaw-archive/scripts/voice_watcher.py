#!/usr/bin/env python3
import os
import time
import json
import logging
import threading
import urllib.request
import subprocess

CONFIG_FILE = "/home/openclaw/banirisset/automation/telegram-config.json"
OPENCLAW_BIN = "/home/openclaw/.npm-global/bin/openclaw"
GATEWAY_ENV_FILE = "/home/openclaw/.openclaw/openclaw-gateway.env"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
LOGGER = logging.getLogger("voice-watcher")
try:
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
except Exception:
    exit(1)

TOKEN = os.environ.get("SCHEDULER_BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY not set — voice transcription requires GROQ Whisper. Set the key and restart.")
TARGET_CHAT = str(config.get("chat_id", ""))

INBOX_THREAD = int(config.get("threads", {}).get("inbox", 11))
WELLBEING_THREAD = int(config.get("threads", {}).get("wellbeing", 19))

MONITORED_THREADS = {INBOX_THREAD, WELLBEING_THREAD}


def load_env_file(path):
    env = {}
    try:
        with open(path, "r") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                env[key] = value.strip().strip('"').strip("'")
    except FileNotFoundError:
        LOGGER.warning("Env file not found: %s", path)
    return env


OPENCLAW_ENV = os.environ.copy()
OPENCLAW_ENV.setdefault("HOME", "/home/openclaw")
OPENCLAW_ENV["PATH"] = f"/home/openclaw/.npm-global/bin:{OPENCLAW_ENV.get('PATH', '/usr/local/bin:/usr/bin:/bin')}"
OPENCLAW_ENV.update(load_env_file(GATEWAY_ENV_FILE))


def send_message(text, thread_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TARGET_CHAT,
        "message_thread_id": thread_id,
        "text": text,
        "parse_mode": "Markdown"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
    except Exception:
        pass


def get_updates(offset):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?timeout=30&offset={offset}&allowed_updates=[\"message\"]"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=40) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception:
        return None


def transcribe(file_id):
    try:
        req = urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}")
        data = json.loads(req.read().decode("utf-8"))
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{data['result']['file_path']}"
        os.system(f"curl -s -o /tmp/voice.ogg '{file_url}'")

        cmd = [
            "curl", "-s", "-X", "POST", "https://api.groq.com/openai/v1/audio/transcriptions",
            "-H", f"Authorization: bearer {GROQ_KEY}",
            "-F", "file=@/tmp/voice.ogg",
            "-F", "model=whisper-large-v3",
            "-F", "language=id",
            "-F", "response_format=json"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(res.stdout).get("text", "").strip()
    except Exception:
        return ""


def _shorten(text, limit=400):
    if not text:
        return ""
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def run_openclaw_agent(args, thread_id):
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            env=OPENCLAW_ENV,
        )
    except Exception:
        LOGGER.exception("Failed to launch OpenClaw agent")
        send_message("⚠️ Transkrip masuk, tapi jalur respon REED gagal dieksekusi.", thread_id)
        return

    if result.returncode != 0:
        LOGGER.error(
            "OpenClaw agent failed (rc=%s) stdout=%s stderr=%s",
            result.returncode,
            _shorten(result.stdout),
            _shorten(result.stderr),
        )
        send_message("⚠️ Transkrip masuk, tapi REED gagal memproses voice note.", thread_id)
        return

    LOGGER.info("OpenClaw agent completed for thread %s", thread_id)


def dispatch_openclaw(prompt, thread_id):
    session_target = f"{TARGET_CHAT}:topic:{thread_id}"
    args = [
        OPENCLAW_BIN,
        "agent",
        "--agent",
        "reed-archivist",
        "--channel",
        "telegram",
        "--message",
        prompt,
        "--to",
        session_target,
        "--deliver",
    ]
    LOGGER.info("Dispatching OpenClaw agent for thread %s via %s", thread_id, session_target)
    threading.Thread(
        target=run_openclaw_agent,
        args=(args, thread_id),
        daemon=True,
    ).start()


def call_openclaw_inbox(text):
    prompt = (
        f"Bani Risset mengirim voice note ke topic Inbox: '{text}'. "
        f"Lakukan 3 hal: 1. Jika ini ide, catat ke file markdown di folder research/. "
        f"2. Jika ini task, tambah ke daily.md. "
        f"3. Jika ada instruksi waktu, set reminder. "
        f"Balas ke topic inbox (thread_id={INBOX_THREAD}) dalam bahasa Indonesia yang singkat dan no BS."
    )
    dispatch_openclaw(prompt, INBOX_THREAD)


def call_openclaw_wellbeing(text):
    prompt = (
        f"Bani Risset mengirim voice note ke topic Wellbeing: '{text}'. "
        f"Ini bukan task atau inbox item — ini konteks personal atau kondisi dirinya. "
        f"Respons dengan mode companion: hadir dulu, validasi kalau perlu, jangan langsung problem-solving kecuali dia minta. "
        f"Kalau ada angka 1-10 → simpan ke health.md sebagai capacity hari ini dan kirim daily guidance. "
        f"Kalau ada hal yang perlu diingat → simpan ke health.md bagian Active Flags atau memory hari ini. "
        f"Balas singkat, hangat, no fluff. Kirim ke topic wellbeing (thread_id={WELLBEING_THREAD})."
    )
    dispatch_openclaw(prompt, WELLBEING_THREAD)


def main():
    offset = 0
    while True:
        updates = get_updates(offset)
        if updates and updates.get("ok"):
            for u in updates["result"]:
                offset = u["update_id"] + 1
                msg = u.get("message", {})
                chat_id = str(msg.get("chat", {}).get("id", ""))
                thread_id = msg.get("message_thread_id")

                if "voice" not in msg:
                    continue
                if chat_id != TARGET_CHAT:
                    continue
                if thread_id not in MONITORED_THREADS:
                    continue

                send_message("⏳ *Sedang men-transkrip...*", thread_id)
                text = transcribe(msg["voice"]["file_id"])

                if not text:
                    send_message("⚠️ Gagal transkrip. Coba ketik pesannya.", thread_id)
                    continue

                if thread_id == INBOX_THREAD:
                    send_message(f"🎙️ *[Transkrip]*\n\"{text}\"\n\n⚙️ *Eksekusi via REED...*", thread_id)
                    call_openclaw_inbox(text)

                elif thread_id == WELLBEING_THREAD:
                    send_message(f"🎙️ *[Transkrip]*\n\"{text}\"", thread_id)
                    call_openclaw_wellbeing(text)

        time.sleep(2)


if __name__ == "__main__":
    main()
