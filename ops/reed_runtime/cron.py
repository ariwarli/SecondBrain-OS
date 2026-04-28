from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .cron_engine import list_state_jobs
from .spec import load_legacy_schedule, load_runtime_spec


@dataclass(frozen=True)
class CronJob:
    job_id: str
    channel: str
    goal: str
    kind: str
    prompt_file: str | None
    phase_1_status: str | None


def list_cron_jobs() -> list[CronJob]:
    schedule = load_legacy_schedule()
    jobs_raw: list[dict[str, Any]] = list(schedule.get("jobs", []))
    jobs: list[CronJob] = []
    for item in jobs_raw:
        jobs.append(
            CronJob(
                job_id=str(item.get("id", "")),
                channel=str(item.get("channel", "")),
                goal=str(item.get("goal", "")),
                kind=str(item.get("type", "")),
                prompt_file=item.get("prompt_file"),
                phase_1_status=item.get("phase_1_status"),
            )
        )
    return jobs


def cron_summary() -> dict[str, Any]:
    jobs = list_cron_jobs()
    spec = load_runtime_spec()
    state_jobs = list_state_jobs()
    return {
        "runtime_declared_jobs": spec.cron_jobs,
        "legacy_schedule_jobs": [job.job_id for job in jobs],
        "state_jobs": [job["job_id"] for job in state_jobs],
        "job_count": len(jobs),
        "channels": sorted({job.channel for job in jobs if job.channel}),
    }
