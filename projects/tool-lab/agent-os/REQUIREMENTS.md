# Requirements

## Functional

1. Accept a goal from CLI.
2. Persist goals, tasks, sessions, events, and learnings in SQLite.
3. Support explicit task dependencies.
4. Execute at least one deterministic task kind end to end.
5. Verify task output with a separate verifier.
6. Mirror current state into markdown files.
7. Record a memory entry from each run.
8. Run at least one replayable eval.

## Non-Functional

1. No external dependencies beyond Python stdlib.
2. All meaningful state continuable from folder alone.
3. Human-readable status must exist outside the database.
4. Failures must write evidence into `FAILURE.md` or `runs/`.
