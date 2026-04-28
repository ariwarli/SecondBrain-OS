from __future__ import annotations

import shlex


SAFE_SHELL_PREFIXES = {
    "pwd",
    "date",
    "echo",
    "ls",
}

BANNED_TOKENS = {"&&", "||", ";", "|", ">", ">>", "<", "$(", "`"}


def infer_approval_status(task_type: str, risk_level: str) -> str:
    if risk_level in {"high", "critical"}:
        return "pending"
    if task_type == "shell_command":
        return "pending"
    return "not_required"


def validate_shell_command(command: str) -> list[str]:
    tokens = shlex.split(command)
    if not tokens:
        raise ValueError("empty shell command")
    for banned in BANNED_TOKENS:
        if banned in command:
            raise ValueError(f"disallowed shell token: {banned}")
    if tokens[0] not in SAFE_SHELL_PREFIXES:
        raise ValueError(f"disallowed command prefix: {tokens[0]}")
    return tokens
