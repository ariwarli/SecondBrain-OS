# Local Operating Summary

- Default architecture: one supervisor CLI, one SQLite task store, one worker loop, one verifier layer, one file-pack as canonical memory.
- First milestone: prove goal -> task -> execution -> verification -> memory -> visibility -> eval on one local machine.
- Guardrails: transparent files over chat state, verification before completion, no external side effects, no hidden memory, no silent task completion.
- Runtime constraints: macOS local shell, Python 3.13 available, repo writable, network not required, `pytest` unavailable so tests use `unittest`.
