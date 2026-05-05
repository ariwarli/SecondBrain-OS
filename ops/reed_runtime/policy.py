from __future__ import annotations

import re
from pathlib import Path

from .paths import WORKSPACE_ROOT

POLICY_FILES = [
    WORKSPACE_ROOT / "hermes.md",
    WORKSPACE_ROOT / "docs" / "INBOX_ROUTING.md",
]

# String markers retained for strict backward compatibility checks.
LEGACY_MARKERS = (
    "default ke alias `speedup-brand`",
    "default global `qwen3-coder:480b`",
    "Provider aktif:** `ollama-cloud`",
)

# Broader patterns to prevent false negatives when wording changes.
LEGACY_PATTERNS = (
    re.compile(r"speedup-brand", re.IGNORECASE),
    re.compile(r"qwen3-coder:480b", re.IGNORECASE),
    re.compile(r"ollama-cloud", re.IGNORECASE),
)

NEGATION_HINTS = (
    "jangan pakai",
    "legacy",
    "mis.",
    "contoh",
)


def _line_is_actionable(line: str) -> bool:
    lowered = line.lower()
    return not any(hint in lowered for hint in NEGATION_HINTS)


def find_legacy_markers(content: str) -> list[str]:
    findings: list[str] = []
    lines = content.splitlines()
    for raw_line in lines:
        line = raw_line.strip()
        if not line or not _line_is_actionable(line):
            continue
        for marker in LEGACY_MARKERS:
            if marker in line:
                findings.append(f"literal:{marker}")
        for pattern in LEGACY_PATTERNS:
            if pattern.search(line):
                findings.append(f"pattern:{pattern.pattern}")
    # Keep deterministic order while removing duplicates.
    deduped = sorted(set(findings))
    return deduped


def policy_legacy_findings() -> dict[Path, list[str]]:
    findings: dict[Path, list[str]] = {}
    for policy_file in POLICY_FILES:
        content = policy_file.read_text(encoding="utf-8") if policy_file.exists() else ""
        hits = find_legacy_markers(content)
        findings[policy_file] = hits
    return findings
