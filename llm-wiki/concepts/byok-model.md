---
title: BYOK (Bring Your Own Key)
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [pricing, api, llm, saas]
status: active
---

# BYOK (Bring Your Own Key)

Model bisnis di mana tool AI menyediakan interface/agent tapi user membawa API key sendiri dari provider (OpenAI, Anthropic, dll). Tool tidak meng-charge untuk inference — hanya untuk fitur tambahan atau gratis sepenuhnya.

## Keuntungan

- **Kontrol biaya** — user bayar langsung ke provider, tanpa markup
- **Privasi** — data tidak lewat server pihak ketiga (selain provider)
- **Fleksibilitas** — switch provider kapan saja
- **No vendor lock-in** — tool bisa diganti tanpa kehilangan akses model

## Kerugian

- User perlu manage API keys sendiri
- Tidak ada "simple pricing" — biaya bervariasi per penggunaan
- Onboarding lebih rumit untuk non-technical users

## Tools yang Pakai BYOK

| Tool | BYOK Support | Notes |
|------|-------------|-------|
| [[entities/command-code.md\|Command Code]] | Ya | BYOK + subscription plans |
| [[entities/open-design.md\|Open Design]] | Ya (full) | 100% BYOK, Apache 2.0 |
| [[entities/pixelle-video.md\|Pixelle-Video]] | Ya | OpenAI-compatible API |
| Cursor | Ya | BYOK atau subscription |
| Cline | Ya (full) | Open-source, BYOK only |

## Alternatif: API Aggregator

Daripada manage banyak API keys, bisa pakai aggregator seperti [[entities/aimurah.md\|AIMurah]] — satu API key untuk 27+ model. Trade-off: convenience vs direct control.

## Related

- [[concepts/ai-coding-agents.md\|AI Coding Agents]] — banyak agent pakai BYOK
- [[entities/aimurah.md\|AIMurah]] — aggregator API sebagai alternatif BYOK
