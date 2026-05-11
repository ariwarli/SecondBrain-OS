---
source_url: https://github.com/nexu-io/open-design
ingested: 2026-05-06
sha256: 440e901ecd7a525138386c788dad5392f4ad591e7ce9adf1b446011ba466d7a5
---

# Open Design

> **The open-source alternative to [Claude Design][cd].** Local-first, web-deployable, BYOK at every layer — **15 coding-agent CLIs** auto-detected on your `PATH` (Claude Code, Codex, Devin for Terminal, Cursor Agent, Gemini CLI, OpenCode, Qwen, GitHub Copilot CLI, Hermes, Kimi, Pi, Kiro, Kilo, Mistral Vibe, DeepSeek TUI) become the design engine, driven by **31 composable Skills** and **72 brand-grade Design Systems**. No CLI? An OpenAI-compatible BYOK proxy is the same loop minus the spawn.

## Why this exists

Anthropic's [Claude Design][cd] (released 2026-04-17, Opus 4.7) showed what happens when an LLM stops writing prose and starts shipping design artifacts. It went viral — and stayed closed-source, paid-only, cloud-only, locked to Anthropic's model and Anthropic's skills. There is no checkout, no self-host, no Vercel deploy, no swap-in-your-own-agent.

**Open Design (OD) is the open-source alternative.** Same loop, same artifact-first mental model, none of the lock-in. We don't ship an agent — the strongest coding agents already live on your laptop. We wire them into a skill-driven design workflow that runs locally with `pnpm tools-dev`, can deploy the web layer to Vercel, and stays BYOK at every layer.

OD stands on four open-source shoulders:

- [**`alchaincyf/huashu-design`**](https://github.com/alchaincyf/huashu-design) — the design-philosophy compass.
- [**`op7418/guizang-ppt-skill`**](https://github.com/op7418/guizang-ppt-skill) — the deck mode.
- [**`OpenCoworkAI/open-codesign`**](https://github.com/OpenCoworkAI/open-codesign) — the UX north star and closest peer.
- [**`multica-ai/multica`**](https://github.com/multica-ai/multica) — the daemon-and-runtime architecture.

## At a glance

- **Coding-agent CLIs (15):** Claude Code, Codex CLI, Devin for Terminal, Cursor Agent, Gemini CLI, OpenCode, Qwen Code, GitHub Copilot CLI, Hermes (ACP), Kimi CLI (ACP), Pi (RPC), Kiro CLI (ACP), Kilo (ACP), Mistral Vibe CLI (ACP), DeepSeek TUI
- **BYOK fallback:** Protocol-specific API proxy at `/api/proxy/{anthropic,openai,azure,google}/stream`
- **Design systems built-in:** 129 — 2 hand-authored starters + 70 product systems + 57 design skills
- **Skills built-in:** 31 — 27 prototype mode + 4 deck mode
- **Media generation:** gpt-image-2, Seedance 2.0, HyperFrames; 93 ready-to-replicate prompts gallery
- **Visual directions:** 5 curated schools (Editorial Monocle, Modern Minimal, Warm Soft, Tech Utility, Brutalist Experimental)
- **Device frames:** iPhone 15 Pro, Pixel, iPad Pro, MacBook, Browser Chrome
- **Persistence:** SQLite at `.od/app.sqlite`
- **Export:** HTML, PDF, PPTX, ZIP, Markdown
- **License:** Apache-2.0
- **Stars:** 26.8k

## Architecture

Frontend: Next.js 16 App Router + React 18 + TypeScript, Vercel-deployable
Daemon: Node 24 + Express + SSE streaming + better-sqlite3
Agent transport: child_process.spawn with typed-event parsers per CLI
Storage: Plain files in `.od/projects/<id>/` + SQLite at `.od/app.sqlite`

## Six load-bearing ideas

1. We don't ship an agent — yours is good enough.
2. Skills are files, not plugins.
3. Design Systems are portable Markdown, not theme JSON.
4. The interactive question form prevents 80% of redirects.
5. The daemon makes the agent feel like it's on your laptop.
6. The prompt stack is the product.

## Quickstart

```bash
git clone https://github.com/nexu-io/open-design.git
cd open-design
corepack enable
pnpm install
pnpm tools-dev run web
```

Or download prebuilt desktop app from [open-design.ai](https://open-design.ai/).

[cd]: https://x.com/claudeai/status/2045156267690213649
