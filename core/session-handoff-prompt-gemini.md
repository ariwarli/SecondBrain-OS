# Session Handoff Prompt — Continue in Gemini

## Context Summary
You are continuing a session focused on stabilizing Bani Risset's Telegram-first operating system across REED, Hermes, INBOX routing, and knowledge boundaries.

The newest priority is no longer just topic health. The session also established a clear boundary model:
- `INBOX` = intake layer only
- `Hermes` = working / operational memory
- `Wiki` = canonical knowledge layer

Do not collapse those into one bucket.

## Latest Verified Runtime Facts

1. **Hermes Runtime Source Of Truth**
   - Hermes live config is under `/home/hermes/.hermes`
   - Main files:
     - `/home/hermes/.hermes/.env`
     - `/home/hermes/.hermes/config.yaml`
   - Do not assume legacy OpenClaw config controls Hermes Telegram behavior

2. **Active Service**
   - Hermes Telegram runtime is `hermes-gateway.service`
   - Service is active and running

3. **Bot Identity**
   - Hermes token points to bot id `8648903806`
   - Active bot is `@survivorset_bot`

4. **Telegram Surface Status**
   - DM is working
   - Legacy `SecondBrain OS` `INBOX` topic was restored into Hermes channel directory
   - `INBOX` is alive again as a valid intake surface

## What Was Decided In This Session

1. **INBOX Is Keep, Not Kill**
   - INBOX exists because Bani is idea-heavy and forgetful
   - INBOX is the fast capture surface
   - INBOX must remain the single low-friction intake layer
   - INBOX is not a final destination or canon bucket

2. **Boundary Model**
   - `INBOX` = intake
   - `tasks/content/personal-crm/ops/knowledge-base/updates` = operational destinations
   - `Hermes` = memory for action continuity
   - `Wiki` = durable, audit-friendly knowledge canon

3. **Routing Rule For Mixed Messages**
   - One message may split into multiple routed objects
   - Example:
     - idea for ebook -> `content`
     - reminder at 15:00 -> `tasks`
   - Reminder should surface in `tasks`, not in `content` or `INBOX`

4. **Canon Taxonomy Direction**
   - `task` and `daily recap` should not become canon wiki buckets
   - candidate durable buckets currently are:
     - `Research`
     - `Frameworks`
     - `SOPs`
     - `Decisions`
     - `Incidents`
   - `Sources` is still an open design question

## Open Questions

1. Final official canon bucket set
2. Whether `Sources` should be a standalone canon bucket
3. Whether boundary wording should later be promoted into `AGENTS.md` or wiki canon docs

## Local Workspace Facts

- Main local workspace: `/Users/banirisset/2_Areas/banirisset`
- Existing continuity files:
  - `/Users/banirisset/2_Areas/banirisset/AGENTS.md`
  - `/Users/banirisset/2_Areas/banirisset/openclaw.md`
  - `/Users/banirisset/2_Areas/banirisset/daily.md`
  - `/Users/banirisset/2_Areas/banirisset/crm.md`
  - `/Users/banirisset/2_Areas/banirisset/memory/2026-04-28.md`

## What To Read First

1. `AGENTS.md`
2. `SOUL.md`
3. `USER.md`
4. `openclaw.md`
5. `daily.md`
6. `memory/2026-04-28.md`

If the task touches live Telegram or Hermes runtime, validate runtime directly before assuming local docs are current.

## SSH Access

- Use key: `/Users/banirisset/.ssh/openclaw_sync_ed25519`
- Host: `167.253.158.103`

## Success Criteria For Continuation

- Do not re-diagnose already-solved bot/token mismatch unless new evidence appears
- Preserve `INBOX` as intake-only
- Preserve `Hermes vs Wiki` boundary
- Treat routing and taxonomy as separate layers
- Advance only the remaining open questions or new runtime issues
