# Runtime Capability Matrix

Date: 2026-04-15

| Capability | Status | Notes |
|---|---|---|
| Repo read access | yes | Repo `/Users/banirisset/banirisset` readable |
| Repo write access | yes | Workspace-write available |
| Shell access | yes | `zsh` working |
| Filesystem search | yes | `rg`, `find`, `sed` available |
| File editing | yes | via patching |
| Git access | yes | repo detected |
| Network access | constrained | not needed for v1 |
| Package install | partial | not needed; avoid external deps |
| Local database | yes | SQLite via stdlib |
| Browser control | no | deferred |
| Screenshot / vision | no | deferred |
| Desktop input control | no | deferred |
| Tool-calling support | partial | host tools available, internal adapter deferred |
| Sub-agent support | yes | runtime supports it, not needed for v1 |
| Long-running background execution | partial | can add later, v1 stays foreground |
| Cron / schedule | partial | available elsewhere in workspace, deferred here |
| Webhook / triggers | no | deferred |
| Persistent storage | yes | files + SQLite |
| UI / dashboard rendering | partial | markdown status mirror in v1 |
| Secret management | partial | avoid secrets in v1 |
| Approval / interruption controls | partial | human-in-loop via file state for v1 |
| Multi-machine support | no | deferred |

## Scope Decisions

- Emulate control plane with markdown + SQLite.
- Defer browser, desktop, remote workers, and external integrations.
- Use deterministic task kinds first; LLM routing comes after closed-loop proof.
