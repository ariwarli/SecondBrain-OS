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


def load_runtime_spec() -> RuntimeSpec:
    return RuntimeSpec(_load_yaml(SPEC_PATH))


def load_legacy_schedule() -> dict[str, Any]:
    return _load_yaml(LEGACY_SCHEDULE_PATH)
