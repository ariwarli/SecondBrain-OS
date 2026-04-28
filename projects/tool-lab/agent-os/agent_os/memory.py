from __future__ import annotations

from datetime import datetime
from pathlib import Path


def append_memory(root: Path, line: str) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d")
    path = root / "memory" / f"{stamp}.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else f"# {stamp}\n\n"
    if not existing.endswith("\n"):
        existing += "\n"
    existing += f"- {line}\n"
    path.write_text(existing, encoding="utf-8")
    return path
