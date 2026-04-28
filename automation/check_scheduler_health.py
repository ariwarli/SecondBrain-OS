#!/usr/bin/env python3

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
LOG_DIR = Path(os.environ.get("TELEGRAM_RUNNER_LOG_DIR", SCRIPT_DIR / "logs"))
CONFIG_PATH = Path(os.environ.get("TELEGRAM_RUNNER_CONFIG", SCRIPT_DIR / "telegram-config.json"))
RUNNER_PATH = Path(SCRIPT_DIR / "telegram_runner.py")

END_RE = re.compile(r"^\[(?P<ts>[^\]]+)\] END job_id=(?P<job>\S+) status=(?P<status>\d+)$")
TS_FORMAT = "%Y-%m-%d %H:%M:%S"


@dataclass
class JobExpectation:
    job_id: str
    max_age_hours: int


EXPECTATIONS = [
    JobExpectation("end_of_day_summary", 24),
    JobExpectation("heartbeat_4", 24),
    JobExpectation("overnight_research", 12),
    JobExpectation("overnight_leads", 12),
    JobExpectation("overnight_builder", 12),
]


def parse_last_end(log_file: Path):
    if not log_file.exists():
        return None
    lines = log_file.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in reversed(lines):
        match = END_RE.match(line.strip())
        if not match:
            continue
        raw_ts = match.group("ts")
        ts_without_zone = raw_ts.rsplit(" ", 1)[0]
        ts = datetime.strptime(ts_without_zone, TS_FORMAT)
        status = int(match.group("status"))
        return ts, status
    return None


def build_report(now: datetime):
    failures = []
    stale = []
    missing = []

    for item in EXPECTATIONS:
        log_file = LOG_DIR / f"{item.job_id}.log"
        parsed = parse_last_end(log_file)
        if not parsed:
            missing.append(item.job_id)
            continue
        ts, status = parsed
        age = now - ts
        if status != 0:
            failures.append(f"{item.job_id} status={status} at {ts.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        if age > timedelta(hours=item.max_age_hours):
            stale.append(f"{item.job_id} age={int(age.total_seconds() // 3600)}h")

    return failures, stale, missing


def send_alert(text: str):
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    token_env = config.get("token_env", "SCHEDULER_BOT_TOKEN")
    env = os.environ.copy()
    if token_env not in env:
        raise SystemExit(f"Missing environment variable: {token_env}")

    proc = subprocess.run(
        [
            sys.executable,
            str(RUNNER_PATH),
            "--job-id",
            "scheduler_health_alert",
            "--thread-key",
            "ops",
            "--config",
            str(CONFIG_PATH),
            "--label",
            "scheduler_health_alert",
            "--message",
            f"Peringatan kesehatan scheduler\n\n{text}",
        ],
        capture_output=True,
        env=env,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout or "Failed to send scheduler health alert")


def main() -> int:
    now = datetime.now().astimezone().replace(tzinfo=None)
    failures, stale, missing = build_report(now)

    if not failures and not stale and not missing:
        print("OK: Pengecekan kesehatan scheduler lulus")
        return 0

    sections = ["Smoke check found issues:"]
    if failures:
        sections.append("Failed jobs:")
        sections.extend(f"- {item}" for item in failures)
    if stale:
        sections.append("Stale jobs:")
        sections.extend(f"- {item}" for item in stale)
    if missing:
        sections.append("Missing logs:")
        sections.extend(f"- {item}" for item in missing)

    alert = "\n".join(sections)
    print(alert)
    send_alert(alert)
    return 1


if __name__ == "__main__":
    sys.exit(main())
