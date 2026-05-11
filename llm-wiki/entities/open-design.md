---
title: Open Design
created: 2026-05-06
updated: 2026-05-06
type: tool
tags: [ai-tool, design, opensource, code, github, agent]
sources: [raw/articles/open-design.md]
url: https://github.com/nexu-io/open-design
status: active
---

# Open Design

Open-source alternative to Anthropic's Claude Design — local-first, web-deployable, BYOK at every layer. Auto-detects 15 coding-agent CLIs on your `PATH` and wires them into a skill-driven design workflow.

## Key Features

- **15 Coding-Agent CLIs:** Claude Code, Codex, Devin, Cursor Agent, Gemini CLI, OpenCode, Qwen, GitHub Copilot CLI, Hermes, Kimi, Pi, Kiro, Kilo, Mistral Vibe, DeepSeek TUI — auto-detected, swap with one click
- **31 Composable Skills:** 27 prototype mode (web-prototype, saas-landing, dashboard, mobile-app, social-carousel, magazine-poster, etc.) + 4 deck mode (guizang-ppt, simple-deck, replit-deck, weekly-update)
- **72 Brand-Grade Design Systems:** Linear, Stripe, Vercel, Airbnb, Tesla, Notion, Apple, Cursor, Supabase, Figma, and more — each as a portable `DESIGN.md`
- **Media Generation:** gpt-image-2 (posters, avatars, infographics), Seedance 2.0 (cinematic text-to-video), HyperFrames (HTML-to-MP4 motion graphics)
- **Export Formats:** HTML, PDF, PPTX, ZIP, Markdown
- **BYOK Proxy:** OpenAI-compatible with SSRF guard — supports Anthropic, OpenAI, Azure OpenAI, Google Gemini
- **Claude Design ZIP Import:** Drop a Claude Design export to continue editing locally
- **SQLite Persistence:** Projects, conversations, messages, tabs, saved templates
- **Interactive Question Form:** Pre-design discovery to prevent redirects
- **5 Visual Directions:** Editorial Monocle, Modern Minimal, Warm Soft, Tech Utility, Brutalist Experimental

## Architecture

- **Frontend:** Next.js 16 App Router + React 18 + TypeScript, Vercel-deployable
- **Daemon:** Node 24 + Express + SSE streaming + better-sqlite3
- **Agent Transport:** child_process.spawn with per-CLI typed-event parsers
- **Preview:** Sandboxed iframe via srcdoc
- **Desktop (optional):** Electron shell with sidecar IPC

## Pricing

Free & open-source (Apache-2.0). BYOK — bring your own API keys for AI providers.

## Why Relevant for Bani

- Reference open-source design tool alternative to proprietary Claude Design
- Relevant for consulting work around AI tooling, agentic workflows, and design systems
- Showcases agent-as-teammate architecture — pattern that applies to many client projects
- Represents the open-source shift in AI design tooling

## Related Tools

- Claude Design — proprietary counterpart (halaman belum dibuat)
- [[entities/command-code.md|Command Code AI]] — coding agent CLI
- [[concepts/ai-coding-agents.md|AI Coding Agents]] — konsep terkait
