from __future__ import annotations

import json
import subprocess
import sys
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from .audit import log_event
from .paths import AUTOMATION_DIR, LOG_DIR, SCHEDULER_DIR, STATE_DIR, ensure_state_dirs
from .spec import load_legacy_schedule


CRON_STATE_PATH = STATE_DIR / "cron_state.json"
JAKARTA = ZoneInfo("Asia/Jakarta")


@dataclass
class RuntimeJob:
    job_id: str
    channel: str
    goal: str
    kind: str
    prompt_file: str | None = None
    phase_1_status: str | None = None
    cron_expr: str | None = None
    label: str | None = None
    script_path: str | None = None
    enabled: bool = True


def _parse_field(field: str, minimum: int, maximum: int) -> set[int]:
    values: set[int] = set()
    for part in field.split(","):
        part = part.strip()
        if part == "*":
            values.update(range(minimum, maximum + 1))
            continue
        if part.startswith("*/"):
            step = int(part[2:])
            values.update(range(minimum, maximum + 1, step))
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            values.update(range(int(start), int(end) + 1))
            continue
        values.add(int(part))
    return {value for value in values if minimum <= value <= maximum}


def _cron_matches(dt: datetime, expr: str) -> bool:
    minute_s, hour_s, dom_s, month_s, dow_s = expr.split()
    minutes = _parse_field(minute_s, 0, 59)
    hours = _parse_field(hour_s, 0, 23)
    dom = _parse_field(dom_s, 1, 31)
    months = _parse_field(month_s, 1, 12)
    dow = _parse_field(dow_s, 0, 6)
    python_dow = (dt.weekday() + 1) % 7
    return (
        dt.minute in minutes
        and dt.hour in hours
        and dt.day in dom
        and dt.month in months
        and python_dow in dow
    )


def _next_run_after(base: datetime, expr: str, tz: ZoneInfo = JAKARTA) -> datetime:
    probe = base.astimezone(tz).replace(second=0, microsecond=0) + timedelta(minutes=1)
    limit = probe + timedelta(days=14)
    while probe <= limit:
        if _cron_matches(probe, expr):
            return probe
        probe += timedelta(minutes=1)
    raise ValueError(f"unable to find next run for cron expr: {expr}")


def load_runtime_jobs() -> list[RuntimeJob]:
    raw = load_legacy_schedule()
    jobs: list[RuntimeJob] = []
    for item in raw.get("jobs", []):
        jobs.append(
            RuntimeJob(
                job_id=str(item.get("id", "")),
                channel=str(item.get("channel", "")),
                goal=str(item.get("goal", "")),
                kind=str(item.get("type", "")),
                prompt_file=item.get("prompt_file"),
                phase_1_status=item.get("phase_1_status"),
                cron_expr=item.get("cron_wib"),
                label=item.get("label"),
            )
        )

    jobs.append(
        RuntimeJob(
            job_id="reminder_processing",
            channel="updates",
            goal="Process due reminders and archive delivered entries",
            kind="recurring",
            cron_expr="*/30 * * * *",
            script_path=str(SCHEDULER_DIR / "scripts" / "reminder_checker.py"),
        )
    )
    return jobs


def _state_payload(job: RuntimeJob, now: datetime) -> dict[str, Any]:
    next_run = _next_run_after(now, job.cron_expr, JAKARTA) if job.cron_expr else None
    return {
        "job_id": job.job_id,
        "channel": job.channel,
        "goal": job.goal,
        "kind": job.kind,
        "prompt_file": job.prompt_file,
        "phase_1_status": job.phase_1_status,
        "cron_expr": job.cron_expr,
        "label": job.label,
        "script_path": job.script_path,
        "enabled": job.enabled,
        "paused": False,
        "next_run_at": next_run.isoformat() if next_run else None,
        "last_run_at": None,
        "last_status": None,
    }


def initialize_state(force: bool = False, now: datetime | None = None) -> dict[str, Any]:
    ensure_state_dirs()
    current_now = now or datetime.now(JAKARTA)
    if CRON_STATE_PATH.exists() and not force:
        return json.loads(CRON_STATE_PATH.read_text(encoding="utf-8"))
    payload = {
        "initialized_at": current_now.isoformat(),
        "timezone": "Asia/Jakarta",
        "jobs": [_state_payload(job, current_now) for job in load_runtime_jobs()],
    }
    CRON_STATE_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log_event("cron.init", {"job_count": len(payload["jobs"]), "force": force})
    return payload


def load_state() -> dict[str, Any]:
    return initialize_state(force=False)


def save_state(state: dict[str, Any]) -> None:
    ensure_state_dirs()
    CRON_STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _find_job(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    for item in state["jobs"]:
        if item["job_id"] == job_id:
            return item
    raise KeyError(f"unknown cron job: {job_id}")


def _job_should_auto_run(job: dict[str, Any]) -> bool:
    return job.get("phase_1_status") not in {"manual_trigger_only", "planned_not_automatic"}


def _run_prompt_job(job: dict[str, Any]) -> int:
    runner_path = AUTOMATION_DIR / "telegram_runner.py"
    config_path = AUTOMATION_DIR / "telegram-config.json"
    prompt_path = AUTOMATION_DIR / str(job["prompt_file"])
    command = [
        sys.executable,
        str(runner_path),
        "--job-id",
        job["job_id"],
        "--prompt-file",
        str(prompt_path),
        "--thread-key",
        job["channel"],
        "--config",
        str(config_path),
    ]
    label = job.get("label")
    if label:
        command.extend(["--label", label])
    if os.environ.get("TELEGRAM_RUNNER_DRY_RUN"):
        command.append("--dry-run")
    result = subprocess.run(command, capture_output=True, text=True)
    log_path = LOG_DIR / f"{job['job_id']}.log"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(result.stdout)
        if result.stderr:
            handle.write(result.stderr)
    return result.returncode


def _run_script_job(job: dict[str, Any]) -> int:
    script_path = Path(str(job["script_path"]))
    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    log_path = LOG_DIR / f"{job['job_id']}.log"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(result.stdout)
        if result.stderr:
            handle.write(result.stderr)
    return result.returncode


def run_job(job_id: str, manual: bool = False, now: datetime | None = None) -> dict[str, Any]:
    state = load_state()
    job = _find_job(state, job_id)
    if job.get("paused") and not manual:
        return {"job_id": job_id, "status": "paused"}
    if not manual and not _job_should_auto_run(job):
        return {"job_id": job_id, "status": "manual_only"}

    current_now = now or datetime.now(JAKARTA)
    if job.get("script_path"):
        status = _run_script_job(job)
    else:
        status = _run_prompt_job(job)

    job["last_run_at"] = current_now.isoformat()
    job["last_status"] = status
    job["next_run_at"] = (
        _next_run_after(current_now, str(job["cron_expr"]), JAKARTA).isoformat() if job.get("cron_expr") else None
    )
    save_state(state)
    log_event(
        "cron.run",
        {"job_id": job_id, "manual": manual, "status": status, "next_run_at": job["next_run_at"]},
    )
    return {"job_id": job_id, "status": status, "next_run_at": job["next_run_at"]}


def tick(now: datetime | None = None) -> list[dict[str, Any]]:
    state = load_state()
    current_now = now or datetime.now(JAKARTA)
    due_results: list[dict[str, Any]] = []
    for job in state["jobs"]:
        if job.get("paused") or not job.get("enabled", True):
            continue
        next_run_at = job.get("next_run_at")
        if not next_run_at:
            continue
        due_at = datetime.fromisoformat(next_run_at)
        if due_at <= current_now and _job_should_auto_run(job):
            due_results.append(run_job(job["job_id"], manual=False, now=current_now))
    return due_results


def set_paused(job_id: str, paused: bool) -> dict[str, Any]:
    state = load_state()
    job = _find_job(state, job_id)
    job["paused"] = paused
    save_state(state)
    log_event("cron.pause" if paused else "cron.resume", {"job_id": job_id})
    return {"job_id": job_id, "paused": paused}


def list_state_jobs() -> list[dict[str, Any]]:
    return list(load_state()["jobs"])
