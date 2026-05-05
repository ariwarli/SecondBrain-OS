from __future__ import annotations

import os
from pathlib import Path

from .paths import STATE_DIR, WORKSPACE_ROOT

RUNTIME_ENV_PATH = STATE_DIR / ".env"
FALLBACK_ENV_PATH = WORKSPACE_ROOT / ".env"


def _parse_env_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or "=" not in stripped:
        return None
    key, value = stripped.split("=", 1)
    key = key.strip()
    value = value.strip().strip('"').strip("'")
    if not key:
        return None
    return key, value


def _load_file(path: Path, overwrite: bool) -> bool:
    if not path.exists():
        return False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        parsed = _parse_env_line(raw_line)
        if not parsed:
            continue
        key, value = parsed
        if overwrite or key not in os.environ:
            os.environ[key] = value
    return True


def load_runtime_env(overwrite: bool = False) -> str | None:
    if _load_file(RUNTIME_ENV_PATH, overwrite=overwrite):
        return str(RUNTIME_ENV_PATH)
    if _load_file(FALLBACK_ENV_PATH, overwrite=overwrite):
        return str(FALLBACK_ENV_PATH)
    return None
