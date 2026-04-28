# Decisions

## 2026-04-15

- Use Python stdlib only for v1 to avoid bootstrap friction.
- Use SQLite + markdown instead of a web control plane first.
- Keep milestone 1 deterministic; no LLM dependency required to prove the loop.
- Treat file-pack as canonical state and SQLite as operational index.
- Keep generated Python cache out of version control.
- Gate `shell_command` tasks behind explicit approval by default.
- Execute shell tasks with `shell=False` and a prefix allowlist.
