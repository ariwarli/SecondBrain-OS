#!/usr/bin/env python3
"""
REED DULL — Model Health Checker
Dijalankan oleh cron setiap 5 menit.
Monitor model yang sedang dipakai REED via sessions.json.
Alert ke Updates topic kalau:
1. Model mati / error (tidak ada session aktif)
2. Model switch (primary model berubah dari baseline)
Usage:
    python3 model_health_checker.py
"""
import os
import sys
import json
import time
import logging
import subprocess
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
WORKSPACE = SCRIPT_DIR.parent
SESSIONS_JSON = Path("/home/openclaw/.openclaw/agents/reed-archivist/sessions/sessions.json")
OPENCLAW_CONFIG = Path("/home/openclaw/.openclaw/openclaw.json")
STATE_FILE = WORKSPACE / "scheduler" / "tracking" / "model_state.json"
LOG_DIR = WORKSPACE / "scheduler" / "logs"

# Baseline model — yang seharusnya dipakai
BASELINE_MODEL = "openrouter/elephant-alpha"

# === LOGGING ===
for d in [STATE_FILE.parent, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "model_health.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("model_health")

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

def load_previous_state():
    """Load previously known model state."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"last_model": None, "last_check": None, "last_alert_type": None}

def save_state(model, alert_type):
    """Save current model state."""
    state = {
        "last_model": model,
        "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_alert_type": alert_type,
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def get_current_model():
    """
    Determine current active model from sessions.json.
    Returns (model_name, active_session_count, error_count).
    """
    if not SESSIONS_JSON.exists():
        return None, 0, 0

    try:
        with open(SESSIONS_JSON) as f:
            sessions = json.load(f)
    except Exception as e:
        log.error(f"Failed to load sessions.json: {e}")
        return None, 0, 0

    active_count = 0
    error_count = 0
    models = {}

    for key, sess in sessions.items():
        if not isinstance(sess, dict):
            continue

        # Count active sessions (not archived/closed)
        status = sess.get("status", "")
        if status in ("active", "waiting", "idle"):
            active_count += 1

        # Track models used
        model_raw = sess.get("model")
        model = ""
        if isinstance(model_raw, dict):
            model = model_raw.get("name") or model_raw.get("id", "")
        elif isinstance(model_raw, str):
            model = model_raw

        if not model:
            model = sess.get("modelOverride", "")

        if model:
            models[model] = models.get(model, 0) + 1

        # Check for error indicators
        if sess.get("error") or sess.get("status") == "error":
            error_count += 1

    # Most frequently used model = current primary
    current_model = max(models, key=models.get) if models else None

    return current_model, active_count, error_count

def get_model_from_config():
    """Get configured primary model from openclaw.json."""
    if not OPENCLAW_CONFIG.exists():
        return None

    try:
        with open(OPENCLAW_CONFIG) as f:
            config = json.load(f)
        model = config.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
        return model
    except:
        return None

def check_gateway_health():
    """Check if gateway service is running (user service first, then process fallback)."""
    uid = os.getuid()
    env = os.environ.copy()
    env.setdefault("XDG_RUNTIME_DIR", f"/run/user/{uid}")

    try:
        proc = subprocess.run(
            ["systemctl", "--user", "is-active", "openclaw-gateway.service"],
            capture_output=True,
            text=True,
            env=env,
            timeout=5,
            check=False,
        )
        if proc.stdout.strip() == "active":
            return True
    except Exception:
        pass

    try:
        proc = subprocess.run(
            ["pgrep", "-f", "openclaw-gateway"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return proc.returncode == 0 and bool(proc.stdout.strip())
    except Exception:
        return False

def send_model_alert(alert_type, current_model, active_count, error_count, prev_model):
    """Send model health alert to Updates topic."""
    now = datetime.now().strftime("%H:%M WIB")

    if alert_type == "model_switch":
        text = (
            f"🔄 <b>MODEL SWITCH DETECTED</b>\n"
            f"🕐 {now}\n\n"
            f"<b>Dari:</b> <code>{prev_model or 'Unknown'}</code>\n"
            f"<b>Ke:</b> <code>{current_model or 'Unknown'}</code>\n\n"
            f"Active sessions: {active_count}\n"
            f"Errors: {error_count}\n\n"
            f"⚠️ Cek apakah ini disengaja atau auto-fallback."
        )
    elif alert_type == "model_down":
        text = (
            f"🔴 <b>MODEL ERROR / DOWN</b>\n"
            f"🕐 {now}\n\n"
            f"Aktif session: {active_count}\n"
            f"Error count: {error_count}\n\n"
            f"Model terakhir: <code>{current_model or 'Unknown'}</code>\n\n"
            f"⚠️ Gateway mungkin bermasalah. Cek VPS."
        )
    elif alert_type == "gateway_down":
        text = (
            f"🔴 <b>GATEWAY DOWN</b>\n"
            f"🕐 {now}\n\n"
            f"openclaw-gateway.service tidak aktif.\n\n"
            f"🛠️ Fix: <code>systemctl --user restart openclaw-gateway</code>"
        )
    elif alert_type == "model_restored":
        text = (
            f"✅ <b>MODEL RESTORED</b>\n"
            f"🕐 {now}\n\n"
            f"Kembali ke: <code>{current_model}</code>\n"
            f"Active sessions: {active_count}\n\n"
            f"Semua normal."
        )
    else:
        return None

    result = tg_send(
        "sendMessage",
        chat_id=GROUP_CHAT_ID,
        message_thread_id=UPDATES_TOPIC_ID,
        text=text,
        parse_mode="HTML",
    )

    return result

def main():
    if not SEND_TOKEN:
        log.error("TELEGRAM_BOT_TOKEN not set!")
        sys.exit(1)

    prev_state = load_previous_state()
    current_model, active_count, error_count = get_current_model()
    configured_model = get_model_from_config()
    gateway_ok = check_gateway_health()

    log.info(f"Check: model={current_model}, active={active_count}, errors={error_count}, gateway={gateway_ok}")

    # Save state
    save_state(current_model, prev_state.get("last_alert_type"))

    # Check for gateway down
    if not gateway_ok:
        if prev_state.get("last_alert_type") != "gateway_down":
            log.warning("Gateway is down, sending alert")
            send_model_alert("gateway_down", current_model, active_count, error_count, prev_state.get("last_model"))
            save_state(current_model, "gateway_down")
        return

    # No model info — could be first run or sessions.json empty
    if not current_model:
        log.info("No current model detected (may be first run)")
        return

    # Detect model switch
    prev_model = prev_state.get("last_model")
    if prev_model and current_model != prev_model:
        log.warning(f"Model switched: {prev_model} → {current_model}")
        send_model_alert("model_switch", current_model, active_count, error_count, prev_model)
        save_state(current_model, "model_switch")
        return

    # Detect model restored to baseline
    if prev_state.get("last_alert_type") in ("model_switch", "model_down") and current_model == BASELINE_MODEL:
        log.info("Model restored to baseline")
        send_model_alert("model_restored", current_model, active_count, error_count, prev_model)
        save_state(current_model, None)
        return

    # Detect model errors
    if error_count > 3:
        if prev_state.get("last_alert_type") != "model_down":
            log.warning(f"High error count: {error_count}")
            send_model_alert("model_down", current_model, active_count, error_count, prev_model)
            save_state(current_model, "model_down")
        return

if __name__ == "__main__":
    main()
