#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = WORKSPACE_ROOT / "automation" / "reed-runtime-spec.yaml"
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from ops.reed_runtime.env import load_runtime_env
from ops.reed_runtime.policy import policy_legacy_findings


def read_spec_model_routing() -> dict[str, object]:
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(f"PyYAML is required: {exc}") from exc

    if not SPEC_PATH.exists():
        raise FileNotFoundError(f"Spec not found: {SPEC_PATH}")
    data = yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8")) or {}
    routing = data.get("runtime", {}).get("model_routing", {})
    return routing if isinstance(routing, dict) else {}


def main() -> int:
    load_runtime_env()
    issues: list[str] = []
    routing = read_spec_model_routing()
    mandatory_provider = str(routing.get("mandatory_provider", "")).strip()
    if mandatory_provider != "9router":
        issues.append(f"mandatory_provider must be '9router', got '{mandatory_provider or '<missing>'}'")

    required_aliases_raw = routing.get("required_aliases", [])
    required_aliases = [str(item) for item in required_aliases_raw if isinstance(item, str) and item]
    lane_defaults_raw = routing.get("lane_defaults", {})
    lane_defaults = lane_defaults_raw if isinstance(lane_defaults_raw, dict) else {}
    lane_alias_map = {"content_lane": "content", "default_lane": "default"}
    missing_aliases = [
        alias
        for alias in required_aliases
        if alias not in routing
        and not (alias in lane_alias_map and lane_alias_map[alias] in lane_defaults)
    ]
    if missing_aliases:
        issues.append(f"missing required aliases in spec: {', '.join(missing_aliases)}")

    for lane in ("content", "default"):
        if lane not in lane_defaults:
            issues.append(f"missing required lane default: {lane}")
    non_9router_lanes = [
        lane
        for lane, alias in lane_defaults.items()
        if isinstance(alias, str) and not alias.startswith("9router/")
    ]
    if non_9router_lanes:
        issues.append(f"lane defaults must use 9router/* aliases: {', '.join(non_9router_lanes)}")

    for env_name in ("NINE_ROUTER_BASE_URL", "NINE_ROUTER_API_KEY"):
        if not os.environ.get(env_name):
            issues.append(f"missing required environment variable: {env_name}")

    for policy_path, found in policy_legacy_findings().items():
        if found:
            issues.append(f"{policy_path}: legacy markers found: {', '.join(found)}")

    payload = {
        "ok": not issues,
        "mandatory_provider": mandatory_provider,
        "issues": issues,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
