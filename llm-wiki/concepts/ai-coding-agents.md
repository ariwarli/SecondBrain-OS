---
title: AI Coding Agents
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [llm, code, agent, ai-tool]
status: active
---

# AI Coding Agents

Kategori tool AI yang membantu developer menulis, review, dan debug kode secara otonom melalui CLI atau IDE. Agent ini beroperasi sebagai "pair programmer" yang bisa memahami codebase, menjalankan perintah, dan membuat perubahan langsung.

## Karakteristik Utama

- **CLI-first atau IDE-integrated** — berjalan di terminal atau sebagai extension
- **Context window besar** — memahami codebase secara keseluruhan (100K–1M token)
- **Tool use** — bisa menjalankan shell commands, edit files, browse web
- **Model agnostic** — kebanyakan mendukung multiple LLM providers (BYOK)

## Pendekatan Diferensiasi

| Pendekatan | Contoh | Keunggulan |
|------------|--------|------------|
| Taste learning | [[entities/command-code.md\|Command Code]] | Belajar gaya coding user secara lokal |
| Agent framework | Claude Code, Cursor | Deep IDE integration |
| Open-source | Cline, Kilo Code | Transparansi, self-hosted |
| Design-focused | [[entities/open-design.md\|Open Design]] | Agent khusus untuk UI/design |

## Pricing Models

Umumnya ada 3 model:
1. **Subscription** — flat monthly fee (Command Code: –00/bulan)
2. **Token-based** — bayar per penggunaan (via [[entities/aimurah.md\|AIMurah]] atau provider langsung)
3. **BYOK** — bring your own API key, tool gratis

## Relevansi

AI coding agents adalah core toolchain untuk consulting work — evaluasi dan rekomendasi tool ke klien, serta meningkatkan produktivitas development sendiri.

## Related

- [[entities/command-code.md\|Command Code AI]] — taste-learning coding agent
- [[entities/open-design.md\|Open Design]] — design-focused agent
- [[concepts/byok-model.md\|BYOK Model]] — pricing pattern yang umum di agent tools
