# Wiki Log

> Catatan kronologis semua aksi wiki. Append-only.

## [2026-05-05] setup | Wiki initialized
- Domain: AI tools, open-source projects, digital marketing
- Structure: raw/, entities/, concepts/, comparisons/, queries/
- All files created: SCHEMA.md, index.md, log.md

## [2026-05-06] add | Command Code AI pricing + entity
- **Source:** Scraped https://commandcode.ai/pricing (241KB HTML) → `raw/articles/command-code-pricing.md`
- **Entity:** `entities/command-code.md` — AI coding agent CLI, taste-1, plans $1-$200/bulan, BYOK
- **Index:** Updated with new entry under Tools & Projects (total pages: 1)

## [2026-05-06] add | Open Design raw source + entity
- **Source:** README.md from https://github.com/nexu-io/open-design → `raw/articles/open-design.md` (SHA256: 440e901e)
- **Entity:** `entities/open-design.md` — Open-source Claude Design alternative, Apache 2.0, 26.8k stars, 15 CLI adapters, 31 skills, 72 design systems
- **Index:** Updated with new entry under Tools & Projects (total pages: 2)

## [2026-05-05] add | Pixelle-Video raw source + entity
- **Source:** GitHub README from https://github.com/AIDC-AI/Pixelle-Video → `raw/articles/pixelle-video.md`
- **Entity:** `entities/pixelle-video.md` — AI short video engine, Apache 2.0, 11.5k stars
- **Index:** Updated with new entry under Tools & Projects (total pages: 3)

## [2026-05-06] ingest | Elementor + AI Landing Page Workflow
- **Source:** YouTube video → `raw/articles/elementor-ai-landing-page.md`
- **Entity:** `entities/elementor-ai-workflow.md` — Workflow landing page 5 menit tanpa coding pakai Elementor + Claude AI
- **Index:** Updated with new entry under Tools & Projects (total pages: 5)

## [2026-05-08] add | AIMurah API Platform
- **Source:** https://aimurah.my.id/ → `raw/aimurah-my-id.md` (SHA256: 8f3c2e1a)
- **Entity:** `entities/aimurah.md` — Platform AI API 27+ model (Claude Sonnet 4.5, GPT-5, Gemini 3.1), 1B token gratis, OpenAI-compatible, pricing IDR Rp 29k–199k/bulan
- **Index:** Updated with new entry under Tools & Projects (total pages: 6)

## [2026-05-11] maintenance | Wiki structural improvements (Devin)
- **WIKI_PATH:** Set env var in `~/.hermes/.env`, created symlink `~/wiki` -> `~/SecondBrain/wiki`
- **Concepts (3 new):**
  - `concepts/ai-coding-agents.md` — AI coding agent category overview, differentiation approaches, pricing models
  - `concepts/byok-model.md` — BYOK pricing pattern, pros/cons, tools that use it
  - `concepts/ai-content-automation.md` — Content automation pipeline, automation spectrum
- **Comparisons (2 new):**
  - `comparisons/ai-coding-agents-comparison.md` — Feature matrix + pricing across 5 coding agents
  - `comparisons/ai-content-tools-comparison.md` — Pixelle-Video vs Elementor+AI vs Open Design
- **Wikilink fixes:** Fixed broken links in aimurah.md, open-design.md, command-code.md, elementor-ai-workflow.md
- **Index:** Updated with all new pages (total pages: 6 -> 11)
- **Lint:** Ran health-check, identified and resolved orphan pages and missing cross-references
