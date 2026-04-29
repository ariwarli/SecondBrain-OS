# Session Handoff Prompt — Empty Agent

You are a fresh agent continuing work for Bani Risset.

Do not assume prior chat context. Build context from files first.

## Who You Are Helping

- User: Bani Risset
- Main local workspace: `/Users/banirisset/2_Areas/banirisset`
- Primary operating interface: Telegram

## Read These First

Read in this order:

1. `/Users/banirisset/2_Areas/banirisset/AGENTS.md`
2. `/Users/banirisset/2_Areas/banirisset/SOUL.md`
3. `/Users/banirisset/2_Areas/banirisset/USER.md`
4. `/Users/banirisset/2_Areas/banirisset/hermes.md`
5. `/Users/banirisset/2_Areas/banirisset/daily.md`
6. `/Users/banirisset/2_Areas/banirisset/memory/2026-04-28.md`

If available and needed later, also read:
- `/Users/banirisset/2_Areas/banirisset/crm.md`
- `/Users/banirisset/2_Areas/banirisset/session-handoff-prompt-gemini.md`

## Core Boundary Model

Do not confuse these layers:

- `INBOX` = intake layer only
- `Hermes` = working / operational memory
- `Wiki` = canonical knowledge layer

Rules:
- Do not use `INBOX` as a final bucket
- Do not let `Hermes` become a wiki
- Do not let `Wiki` become agent RAM

## Routing Rules

Incoming Telegram capture should enter through `INBOX`, then route onward.

Operational destination topics:
- `tasks`
- `content`
- `personal-crm`
- `ops`
- `knowledge-base`
- `updates`

If one message contains multiple functions, split it.

Example:
- idea for ebook -> `content`
- reminder at 15:00 -> `tasks`

The reminder should surface in `tasks`, not in `content` and not stay in `INBOX`.

## Live Runtime Facts

- Main bot: `@survivorset_bot`
- Hermes Telegram runtime service: `hermes-gateway.service`
- Hermes live config path: `/home/hermes/.hermes`
- Hermes Telegram DM works
- Legacy `SecondBrain OS` `INBOX` topic has been restored into Hermes channel directory

If the task touches Telegram, Hermes, or bot routing:
- validate live runtime before trusting stale local assumptions

## Current Decisions Already Made

- `INBOX` is kept and is intentional
- `INBOX` exists as a fast capture surface because the user is idea-heavy and forgetful
- `task` and `daily recap` should not be canon wiki buckets
- candidate canon buckets are currently:
  - `Research`
  - `Frameworks`
  - `SOPs`
  - `Decisions`
  - `Incidents`

## Open Questions

- Final canon bucket set is not locked yet
- `Sources` may or may not become an official canon bucket
- Boundary wording may later be promoted into canon docs

## First Step

1. Read the required files in order
2. Summarize current state to yourself
3. If the request touches Telegram/Hermes, validate runtime
4. Continue work without treating `INBOX` as a permanent category
