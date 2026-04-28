# Agent OS V1

## Mission

Build a local-first, durable, observable agentic operating system that can take a goal, decompose it into explicit tasks, execute them through a worker loop, verify the result, update memory, and leave a human-readable artifact trail.

## Owner

- Human: Bani Risset
- Builder: Codex

## Runtime Profile

- Mode: harness-wrapper friendly, native local-first baseline
- Host: macOS local machine
- Execution: Python 3.13 standard library only for v1
- State: markdown file-pack + SQLite

## First Milestone

Prove the full closed loop:

1. intake a goal
2. persist goal and task graph
3. claim and execute a task
4. verify artifact outcome
5. record event timeline
6. write memory update
7. run an eval replay
8. show status to a human

## Non-Goals for V1

- Browser automation
- Desktop automation
- Multi-machine workers
- External side effects
- Autonomous approval rules
- LLM-powered decomposition

## Constraints

- Network not required
- No extra packages assumed
- Must survive fresh session from files alone

## Success Evidence

- `python3 -m agent_os.cli demo`
- `python3 -m unittest discover -s tests -v`
- updated `status.md`, `tasks.md`, `memory/`, `artifacts/`, `runs/`
