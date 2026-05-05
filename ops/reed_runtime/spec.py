from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .paths import LEGACY_SCHEDULE_PATH, SPEC_PATH


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"YAML not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


@dataclass(frozen=True)
class RuntimeSpec:
    raw: dict[str, Any]

    @property
    def deployment_phase(self) -> str:
        return str(self.raw.get("deployment_phase", "unknown"))

    @property
    def channel_primary(self) -> list[str]:
        return list(self.raw.get("channels", {}).get("primary", []))

    @property
    def channel_planned(self) -> list[str]:
        return list(self.raw.get("channels", {}).get("planned", []))

    @property
    def execution_backends(self) -> list[str]:
        return list(self.raw.get("execution", {}).get("backends", []))

    @property
    def future_backends(self) -> list[str]:
        return list(self.raw.get("execution", {}).get("future_backends", []))

    @property
    def cron_jobs(self) -> list[str]:
        return list(self.raw.get("cron", {}).get("jobs", []))

    @property
    def autonomy_tiers(self) -> dict[str, list[str]]:
        tiers = self.raw.get("execution", {}).get("autonomy_tiers", {})
        return {str(key): list(value) for key, value in tiers.items()}

    @property
    def model_routing(self) -> dict[str, Any]:
        routing = self.raw.get("runtime", {}).get("model_routing", {})
        return routing if isinstance(routing, dict) else {}

    @property
    def mandatory_provider(self) -> str:
        return str(self.model_routing.get("mandatory_provider", "")).strip()

    @property
    def required_model_env(self) -> list[str]:
        required = self.model_routing.get("required_env", [])
        return [str(item) for item in required if isinstance(item, str) and item]

    @property
    def required_aliases(self) -> list[str]:
        aliases = self.model_routing.get("required_aliases", [])
        return [str(item) for item in aliases if isinstance(item, str) and item]

    @property
    def lane_defaults(self) -> dict[str, str]:
        defaults = self.model_routing.get("lane_defaults", {})
        if not isinstance(defaults, dict):
            return {}
        normalized: dict[str, str] = {}
        for key, value in defaults.items():
            if not isinstance(key, str) or not key.strip():
                continue
            if not isinstance(value, str) or not value.strip():
                continue
            normalized[key.strip()] = value.strip()
        return normalized


def load_runtime_spec() -> RuntimeSpec:
    return RuntimeSpec(_load_yaml(SPEC_PATH))


def load_legacy_schedule() -> dict[str, Any]:
    return _load_yaml(LEGACY_SCHEDULE_PATH)
