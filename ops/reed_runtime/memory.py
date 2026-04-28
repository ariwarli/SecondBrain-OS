from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .audit import log_event
from .paths import OP_MEMORY_PATH, USER_MEMORY_PATH, ensure_state_dirs


DEFAULT_LIMITS = {
    "operational": 2200,
    "user": 1375,
}


@dataclass
class MemoryStore:
    target: str
    path: Path
    char_limit: int

    def _default(self) -> dict:
        return {"target": self.target, "char_limit": self.char_limit, "entries": []}

    def load(self) -> dict:
        ensure_state_dirs()
        if not self.path.exists():
            data = self._default()
            self.save(data)
            return data
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data: dict) -> None:
        ensure_state_dirs()
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def usage(self) -> tuple[int, int]:
        data = self.load()
        total = sum(len(entry) for entry in data["entries"])
        return total, int(data["char_limit"])

    def list_entries(self) -> list[str]:
        return list(self.load()["entries"])

    def add(self, content: str) -> None:
        content = content.strip()
        if not content:
            raise ValueError("content is empty")
        data = self.load()
        entries = data["entries"]
        if content in entries:
            return
        projected = sum(len(entry) for entry in entries) + len(content)
        if projected > int(data["char_limit"]):
            raise ValueError(f"memory full: {projected}/{data['char_limit']}")
        entries.append(content)
        self.save(data)
        log_event("memory.add", {"target": self.target, "content": content})

    def _match_index(self, old_text: str) -> int:
        matches = [idx for idx, entry in enumerate(self.list_entries()) if old_text in entry]
        if not matches:
            raise ValueError(f"no memory entry matches substring: {old_text!r}")
        if len(matches) > 1:
            raise ValueError(f"substring matched multiple entries: {old_text!r}")
        return matches[0]

    def replace(self, old_text: str, content: str) -> None:
        content = content.strip()
        if not content:
            raise ValueError("content is empty")
        data = self.load()
        idx = self._match_index(old_text)
        data["entries"][idx] = content
        projected = sum(len(entry) for entry in data["entries"])
        if projected > int(data["char_limit"]):
            raise ValueError(f"memory full after replace: {projected}/{data['char_limit']}")
        self.save(data)
        log_event("memory.replace", {"target": self.target, "old_text": old_text, "content": content})

    def remove(self, old_text: str) -> None:
        data = self.load()
        idx = self._match_index(old_text)
        removed = data["entries"].pop(idx)
        self.save(data)
        log_event("memory.remove", {"target": self.target, "old_text": old_text, "removed": removed})


def get_memory_store(target: str) -> MemoryStore:
    normalized = target.lower()
    if normalized in {"operational", "memory"}:
        return MemoryStore("operational", OP_MEMORY_PATH, DEFAULT_LIMITS["operational"])
    if normalized in {"user", "profile"}:
        return MemoryStore("user", USER_MEMORY_PATH, DEFAULT_LIMITS["user"])
    raise ValueError(f"unknown memory target: {target}")
