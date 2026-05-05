from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import yaml

from .paths import WORKSPACE_ROOT

COMMAND_COMPLIANCE_PATH = WORKSPACE_ROOT / "automation" / "reed-command-compliance.yaml"


@dataclass(frozen=True)
class CommandCheckResult:
    name: str
    ok: bool
    detail: str


def _load_contract() -> dict[str, Any]:
    if not COMMAND_COMPLIANCE_PATH.exists():
        raise FileNotFoundError(f"Command compliance file not found: {COMMAND_COMPLIANCE_PATH}")
    data = yaml.safe_load(COMMAND_COMPLIANCE_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {COMMAND_COMPLIANCE_PATH}")
    return data


def run_command_compliance_checks() -> list[CommandCheckResult]:
    checks: list[CommandCheckResult] = []
    contract = _load_contract()

    global_menu = contract.get("global_command_menu", [])
    if not isinstance(global_menu, list):
        global_menu = []
    menu_count = sum(1 for item in global_menu if isinstance(item, str) and item.strip() == "/menu")
    checks.append(
        CommandCheckResult(
            "global_menu_singleton",
            menu_count == 1 and len(global_menu) == 1,
            f"global_command_menu={global_menu}",
        )
    )

    topic_commands = contract.get("topic_commands", {})
    if not isinstance(topic_commands, dict):
        topic_commands = {}

    missing_model_topics: list[str] = []
    missing_route_pattern_topics: list[str] = []
    for topic, config in topic_commands.items():
        if not isinstance(config, dict):
            continue
        required = config.get("required", [])
        if not isinstance(required, list):
            required = []
        if "/model" not in required:
            missing_model_topics.append(str(topic))

        if str(topic) == "inbox":
            required_patterns = config.get("required_patterns", [])
            if not isinstance(required_patterns, list):
                required_patterns = []
            has_route_pattern = any(
                isinstance(pattern, str) and re.search(r"route-", pattern)
                for pattern in required_patterns
            )
            if not has_route_pattern:
                missing_route_pattern_topics.append(str(topic))

    checks.append(
        CommandCheckResult(
            "model_command_all_topics",
            not missing_model_topics,
            "All topics include /model"
            if not missing_model_topics
            else f"Topics missing /model: {', '.join(sorted(missing_model_topics))}",
        )
    )
    checks.append(
        CommandCheckResult(
            "inbox_route_command_pattern",
            not missing_route_pattern_topics,
            "Inbox topic includes /route-* command pattern"
            if not missing_route_pattern_topics
            else "Inbox topic missing /route-* command pattern",
        )
    )

    runtime_sources = contract.get("runtime_sources", [])
    if not isinstance(runtime_sources, list):
        runtime_sources = []
    missing_required_sources: list[str] = []
    for entry in runtime_sources:
        if not isinstance(entry, dict):
            continue
        rel_path = str(entry.get("path", "")).strip()
        if not rel_path:
            continue
        required = bool(entry.get("required", True))
        target_path = WORKSPACE_ROOT / rel_path
        if required and not target_path.exists():
            missing_required_sources.append(rel_path)
    checks.append(
        CommandCheckResult(
            "runtime_source_presence",
            not missing_required_sources,
            "All required runtime source files exist"
            if not missing_required_sources
            else f"Missing required runtime source files: {', '.join(missing_required_sources)}",
        )
    )
    return checks


def command_compliance_summary() -> dict[str, Any]:
    checks = run_command_compliance_checks()
    return {
        "ok": all(item.ok for item in checks),
        "contract_path": str(COMMAND_COMPLIANCE_PATH),
        "checks": [asdict(item) for item in checks],
    }
