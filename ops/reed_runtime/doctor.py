from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from pathlib import Path

from .commands import run_command_compliance_checks
from .env import load_runtime_env
from .paths import DB_PATH, OP_MEMORY_PATH, SPEC_PATH, STATE_DIR, USER_MEMORY_PATH
from .policy import policy_legacy_findings
from .spec import load_runtime_spec


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def run_checks() -> list[CheckResult]:
    load_runtime_env()
    checks: list[CheckResult] = []
    spec = load_runtime_spec()
    checks.append(CheckResult("runtime_spec", SPEC_PATH.exists(), str(SPEC_PATH)))
    checks.append(CheckResult("state_dir", STATE_DIR.exists(), str(STATE_DIR)))
    checks.append(CheckResult("operational_memory", OP_MEMORY_PATH.exists(), str(OP_MEMORY_PATH)))
    checks.append(CheckResult("user_memory", USER_MEMORY_PATH.exists(), str(USER_MEMORY_PATH)))
    checks.append(CheckResult("session_recall_db", DB_PATH.exists(), str(DB_PATH)))

    # SCHEDULER_BOT_TOKEN was used by legacy REED DULL flow and is no longer mandatory.
    checks.append(
        CheckResult(
            "scheduler_bot_token_env",
            True,
            "SCHEDULER_BOT_TOKEN is optional (legacy REED DULL token, not required)",
        )
    )

    python_ok = Path("/usr/bin/python3").exists() or Path("/opt/homebrew/bin/python3").exists()
    checks.append(CheckResult("python3", python_ok, "python3 executable expected on host"))

    mandatory_provider = spec.mandatory_provider
    provider_ok = mandatory_provider == "9router"
    checks.append(
        CheckResult(
            "mandatory_provider",
            provider_ok,
            f"runtime.model_routing.mandatory_provider={mandatory_provider or '<missing>'}",
        )
    )

    required_env = spec.required_model_env
    missing_required_env = [name for name in required_env if not os.environ.get(name)]
    checks.append(
        CheckResult(
            "model_routing_env",
            not missing_required_env,
            (
                "All required model routing env vars are present"
                if not missing_required_env
                else f"Missing env vars: {', '.join(missing_required_env)}"
            ),
        )
    )

    required_aliases = spec.required_aliases
    lane_alias_map = {"content_lane": "content", "default_lane": "default"}
    missing_required_aliases = [
        alias
        for alias in required_aliases
        if alias not in spec.model_routing
        and not (
            alias in lane_alias_map and lane_alias_map[alias] in spec.lane_defaults
        )
    ]
    checks.append(
        CheckResult(
            "model_routing_aliases",
            not missing_required_aliases,
            (
                "All required model routing aliases are defined in spec"
                if not missing_required_aliases
                else f"Missing required aliases: {', '.join(missing_required_aliases)}"
            ),
        )
    )

    lane_defaults = spec.lane_defaults
    missing_lanes = [lane for lane in ("content", "default") if lane not in lane_defaults]
    invalid_lane_provider = [
        lane for lane, alias in lane_defaults.items() if not alias.startswith("9router/")
    ]
    lane_detail_parts: list[str] = []
    if missing_lanes:
        lane_detail_parts.append(f"Missing lane defaults: {', '.join(missing_lanes)}")
    if invalid_lane_provider:
        lane_detail_parts.append(
            f"Lane defaults must use 9router/* aliases: {', '.join(invalid_lane_provider)}"
        )
    checks.append(
        CheckResult(
            "lane_defaults",
            not missing_lanes and not invalid_lane_provider,
            "Lane defaults are present and pinned to 9router aliases"
            if not missing_lanes and not invalid_lane_provider
            else "; ".join(lane_detail_parts),
        )
    )

    # Fail fast when legacy aliases are still pinned in policy docs.
    for policy_file, found in policy_legacy_findings().items():
        checks.append(
            CheckResult(
                f"policy_guard_{policy_file.name}",
                not found,
                "No legacy model markers found" if not found else f"Legacy markers detected: {', '.join(found)}",
            )
        )

    for compliance_check in run_command_compliance_checks():
        checks.append(
            CheckResult(
                f"command_{compliance_check.name}",
                compliance_check.ok,
                compliance_check.detail,
            )
        )
    return checks


def doctor_summary() -> dict:
    checks = run_checks()
    return {
        "ok": all(item.ok for item in checks),
        "checks": [asdict(item) for item in checks],
    }
