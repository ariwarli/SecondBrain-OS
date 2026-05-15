from __future__ import annotations

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

    menu_contract = contract.get("telegram_menu", {})
    if not isinstance(menu_contract, dict):
        menu_contract = {}
    exposed_commands = menu_contract.get("exposed_commands", [])
    if not isinstance(exposed_commands, list):
        exposed_commands = []
    hidden_commands = menu_contract.get("hidden_commands", [])
    if not isinstance(hidden_commands, list):
        hidden_commands = []
    exposed_menu_count = sum(
        1 for item in exposed_commands if isinstance(item, str) and item.strip() == "/menu"
    )
    checks.append(
        CommandCheckResult(
            "launcher_only_menu_surface",
            exposed_menu_count == 1 and len(exposed_commands) == 1,
            f"telegram_menu.exposed_commands={exposed_commands}",
        )
    )
    menu_hidden = any(isinstance(item, str) and item.strip() == "/menu" for item in hidden_commands)
    checks.append(
        CommandCheckResult(
            "launcher_not_hidden",
            not menu_hidden,
            "Launcher command /menu is not listed in hidden_commands"
            if not menu_hidden
            else "hidden_commands must not include /menu",
        )
    )

    topic_commands = contract.get("topic_commands", {})
    if not isinstance(topic_commands, dict):
        topic_commands = {}
    topics_missing_launcher: list[str] = []
    for topic, config in topic_commands.items():
        if not isinstance(config, dict):
            topics_missing_launcher.append(str(topic))
            continue
        launcher = str(config.get("launcher", "")).strip()
        if launcher != "/menu":
            topics_missing_launcher.append(str(topic))
    checks.append(
        CommandCheckResult(
            "topic_launcher_binding",
            not topics_missing_launcher,
            "All topics are bound to /menu launcher"
            if not topics_missing_launcher
            else f"Topics missing /menu launcher binding: {', '.join(sorted(topics_missing_launcher))}",
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
