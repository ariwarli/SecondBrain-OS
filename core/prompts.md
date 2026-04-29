# Hermes Prompt Pack

Prompt pack ini disusun dari pola yang ditekankan di NotebookLM legacy `OpenClaw` (`05667e4d-493c-4236-83a4-ae74dadb178e`).

## Morning Brief Setup

```text
Set up a daily morning brief at 7 AM.
Include calendar, priority emails, overdue follow-ups, overnight results, and only truly urgent items.
Keep it concise.
```

## End Of Day Summary

```text
Set up an end-of-day summary at 6 PM.
Include completed tasks, pending tasks, blockers, and what should be queued for tomorrow.
```

## CRM Review

```text
Run a daily CRM review.
Tell me who needs follow-up, why they matter, and draft the next message.
Prioritize revenue and leverage.
```

## Content Nagger

```text
Act as a content accountability system.
Nudge me to publish one worthwhile piece of content per day.
Escalate if I keep deferring.
```

## Delegate Heavy Work

```text
If this task will take more than 10 seconds, spawn a subagent.
Keep the main thread responsive.
Return with a concise summary, artifact location, and next decision needed.
```

## Feedback Loop

```text
When I give specific correction and say "update the skill", generalize the fix so the same mistake does not repeat.
```

## Minimal Context Reminder

```text
Load only SOUL.md, USER.md, IDENTITY.md, hermes.md, and daily.md.
Pull more context only when needed.
```
