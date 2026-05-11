# Wiki Schema

## Domain
AI tools, open-source projects, digital marketing tools, automation, coding/dev tools — curated links, pricing, and notes for Bani's consulting work.

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `pixelle-video.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 1 outbound link per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- Default language: Bahasa Indonesia (boleh campur English untuk istilah teknis)

## Frontmatter
```yaml
---
title: Nama Halaman
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: tool | concept | comparison | query | person | project
tags: [dari taxonomy di bawah]
sources: [raw/articles/nama-sumber.md]
url: https://...
status: active | archived
---
```

### raw/ Frontmatter
```yaml
---
source_url: https://...
ingested: YYYY-MM-DD
sha256: <hex digest>
---
```

## Tag Taxonomy
- **Tools:** ai-tool, video, image, audio, code, automation, analytics, design
- **AI:** llm, tts, stt, comfyui, diffusion, agent
- **Business:** pricing, startup, opensource, saas, api
- **Content:** marketing, social-media, seo, writing
- **Platform:** github, web-app, self-hosted, mobile
- **Meta:** comparison, reference, inspiration, tutorial

## Page Thresholds
- **Create a page** when a tool/project appears in 2+ sources OR is worth tracking (interesting enough for Bani to save)
- **Add to existing page** when finding new info about a known tool
- **DON'T create a page** for passing mentions
- **Archive** when content fully superseded → move to `_archive/`

## Entity Pages
One page per tool/project/company. Include:
- Overview / what it does
- Key features
- Pricing (if known)
- Why relevant for Bani
- Related tools ([[wikilinks]])

## Update Policy
- New sources supersede old ones
- If contradictory, note both positions
- Mark contradictions in frontmatter
