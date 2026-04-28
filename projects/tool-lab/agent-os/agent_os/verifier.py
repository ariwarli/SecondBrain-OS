from __future__ import annotations

from pathlib import Path


def verify(root: Path, spec: dict) -> tuple[bool, str]:
    spec_type = spec["type"]
    if spec_type == "file_contains":
        target = root / spec["path"]
        if not target.exists():
            return False, f"missing file: {target}"
        content = target.read_text(encoding="utf-8")
        needle = spec["contains"]
        if needle not in content:
            return False, f"content mismatch: expected substring {needle!r}"
        return True, f"verified file contains substring: {needle!r}"
    if spec_type == "stdout_contains":
        stdout = spec.get("stdout", "")
        needle = spec["contains"]
        if needle not in stdout:
            return False, f"stdout mismatch: expected substring {needle!r}"
        return True, f"verified stdout contains substring: {needle!r}"
    return False, f"unsupported verification type: {spec_type}"
