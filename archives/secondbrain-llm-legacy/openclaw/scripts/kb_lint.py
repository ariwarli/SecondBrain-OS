#!/usr/bin/env python3
"""
Lightweight lint for final SecondBrain wiki notes.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import NamedTuple


DEFAULT_KB_ROOT = Path("/home/openclaw/banirisset/knowledge-base")
FINAL_DIRS = ("notes", "projects", "decisions", "references", "research", "meetings", "templates")
SECRET_PATTERNS = (
    re.compile(r"\b[A-Z0-9_]*(TOKEN|SECRET|API_KEY|PASSWORD)\s*=\s*\S+", re.IGNORECASE),
    re.compile(r"\b\d{8,}:[A-Za-z0-9_-]{25,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
)


class Finding(NamedTuple):
    path: Path
    message: str


def final_note_paths(kb_root: Path) -> list[Path]:
    wiki_root = kb_root / "wiki"
    paths: list[Path] = []
    for folder in FINAL_DIRS:
        folder_path = wiki_root / folder
        if not folder_path.exists():
            continue
        paths.extend(
            path
            for path in folder_path.rglob("*.md")
            if path.is_file() and path.name not in {"index.md", "_template.md"}
        )
    return sorted(paths)


def lint_note(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    if "## Source" not in text:
        findings.append(Finding(path, "missing Source section"))
    if "Data Classification:" not in text and "## Classification" not in text:
        findings.append(Finding(path, "missing Data Classification"))
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(Finding(path, "possible secret pattern"))
            break
    return findings


def lint_kb(kb_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in final_note_paths(kb_root):
        findings.extend(lint_note(path))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint final SecondBrain wiki notes")
    parser.add_argument("--kb-root", default=str(DEFAULT_KB_ROOT), help="Knowledge-base root")
    args = parser.parse_args()

    kb_root = Path(args.kb_root).resolve()
    findings = lint_kb(kb_root)
    for finding in findings:
        rel = finding.path.relative_to(kb_root).as_posix()
        print(f"{rel}: {finding.message}")
    if findings:
        return 1
    print("kb lint: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
