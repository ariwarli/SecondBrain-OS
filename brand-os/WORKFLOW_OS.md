---
[WORKFLOW_OS | FOR: semua project — cara kerja, tools, SOP, bottleneck]
Environment: Claude Desktop + MCP (primary). Chat-first, bukan terminal-first.
Default output: copy-paste ready, zero editing needed.
Pola kerja: Pomodoro, deep work terbatas, speed > perfection.
---

# WORKFLOW_OS — BANI RISSET
> Dokumen referensi cara kerja dan sistem. Update setiap 2 minggu.
> Last updated: April 2026

---

## TOOLS STACK

### AI & Thinking
- **Claude Pro** (primary — Desktop + MCP) — strategy, copy, content, funnel
- **ChatGPT** — content generation, ideation
- **Perplexity Pro** — research & fact-checking
- **Gemini AI** — certified, untuk Google ecosystem tasks

### Automation
- **n8n** (VPS) — full-stack automation, semua 8 platform — IN PROGRESS
- **Integrately Premium** (lifetime) — bridge automasi sementara n8n belum live
- **Radaar.io Pro** — cross-platform daily scheduler (current, sementara)
- **CloudChat.id** — WhatsApp automation agency platform (unlimited multi-tenant)

### Content & Design
- **Canva** — carousel, visual content, ebook, PDF (preferred over programmatic)
- **Canva MCP** — Claude generate → Canva eksekusi visual

### MCP Integrations (aktif di Claude Desktop)
- Notion, Gmail, Google Calendar, Canva, Supabase, Gamma, Miro

### Digital Product Sales
- **Lynk.id** (primary) — digital product storefront
- **Gumroad** (secondary, untuk prompt packs)

### Analytics & SEO
- **Google Search Console** — weekly review (wajib daftar)
- **RankMath SEO** — schema + meta management

### Web & Cloud
- **WordPress** — banirisset.com + terasdigital.co.id
- **VPS** — n8n deployment, active
- **AWS, GCP** — cloud infrastructure

---

## SKILLS ARSENAL (Claude Skills yang tersedia)

### User Skills (Custom — Bani Risset)
| Skill | Trigger | Fungsi |
|-------|---------|--------|
| `utas-generator` | "buatkan utas", "bikin thread" | Threads content, multi-post |
| `seo-geo-aeo` | "audit situs", "cek SEO" | Full SEO/GEO/AEO audit |
| `social-media-carousel` | "carousel", "instagram slides" | Multi-slide carousel design |
| `stop-slop` | "stop slop", "de-AI ini" | Remove AI writing patterns |
| `10x-thinking` | "think 10x", "think bigger" | Breakthrough strategy |
| `landing-page-copy` | "buat sales page", "landing page" | Full sales page 9 section |
| `email-sequence` | "email sequence", "nurture email" | 4 template sequence |
| `product-launch-pack` | "launch produk", "launch pack" | Full 6-asset launch kit |

### Public Skills (tersedia)
- `docx`, `pdf`, `pptx`, `xlsx` — file creation
- `frontend-design` — web UI/component
- `file-reading`, `pdf-reading` — file processing

---

## SOP BERULANG

### SOP 1: Produksi Konten Threads
1. Buka `utas-generator` skill
2. Input: topik + angle + target audience
3. Output: hook + isi per post + CTA
4. Review dengan `stop-slop` jika perlu
5. Schedule via Radaar.io Pro

### SOP 2: Launch Digital Product
1. Buka `product-launch-pack` skill
2. Input: nama produk + harga + benefit utama + target
3. Output: pricing table + Threads thread + 3 IG caption + 2 WA broadcast + timeline
4. Design visual di Canva
5. Upload ke Lynk.id
6. Blast ke email database (1,500 contacts)

### SOP 3: Sales Page / Landing Page
1. Buka `landing-page-copy` skill
2. Input: offer + harga + target persona + proof points
3. Output: 9 section lengkap (Hero → CTA akhir)
4. Flag bagian yang butuh konfirmasi Bani sebelum publish

### SOP 4: Email Campaign
1. Buka `email-sequence` skill
2. Input: tujuan sequence + offer + tone (formal/casual)
3. Default: formal (saya/Anda) karena database mix
4. Output: subject line (3 opsi) + preview text + body + P.S. + timeline

### SOP 5: Brand Review (2 Mingguan)
1. Buka project-review.md
2. Copy prompt review
3. New chat → paste → run
4. Hasilkan diff → update BRAND_DNA.md + WORKFLOW_OS.md

---

## FORMAT OUTPUT FAVORIT

- **Konten sosmed:** Hook + value + CTA. Kalimat pendek. Tanpa preamble.
- **Email:** Formal tone, angka konkret, 1 CTA jelas per email
- **Landing page:** Problem → Agitate → Solution → Proof → CTA
- **Proposal:** Situasi klien → gap → solusi → timeline → harga → next step
- **Report/analisis:** Bullet point per bagian, angka di depan, rekomendasi di akhir

---

## REVENUE ARCHITECTURE

**Target:** IDR 100 juta/bulan

**Scenario realistis:**
```
3 Retainer Clients @ IDR 15 juta     = IDR 45 juta
2 One-time Projects @ IDR 20 juta    = IDR 40 juta
1 Workshop/Training @ IDR 15 juta    = IDR 15 juta
──────────────────────────────────────────────────
TOTAL                                = IDR 100 juta
```

**Pricing floor (minimum — jangan di bawah ini):**
- Website fix: IDR 7.5 juta
- Digital marketing strategy: IDR 15 juta
- Private AI training (1 hari): IDR 10 juta
- AI Implementation (30 hari): IDR 15 juta
- Retainer: IDR 20 juta/bulan

---

## DIGITAL PRODUCT ROADMAP

| Prioritas | Produk | Harga | Status |
|-----------|--------|-------|--------|
| P0 — Sekarang | AI Prompt Pack 100 | Rp97–197K | Belum dibuat |
| P0 — Sekarang | Mini Course 5 Hari (email-based) | Rp297K | Belum dibuat |
| P0 — Siap launch | AI Quick Win Sprint — 14 Hari | IDR 5.000.000 | Copy siap |
| P1 — Bulan 2 | Workshop Live 3 Jam | Rp497K | Konsep ada |
| P1 — Bulan 2 | WA Automation Starter Kit | Rp497K | Konsep ada |
| P1 — Bulan 2 | Ebook Case Study SG | Rp397K | Konsep ada |
| P2 — Bulan 3+ | Self-paced Course 30 Hari | Rp1.5–2.5 juta | Ide |
| P2 — Bulan 3+ | Personal Brand in a Box | Rp2.5 juta | Ide |
| P2 — Bulan 3+ | Annual Digital Health Check | Rp997K | Ide |

**Aturan eksekusi:** 1 produk launch → ukur → baru berikutnya. Jangan parallel launch.

---

## BOTTLENECK YANG TERIDENTIFIKASI

1. **n8n belum live** — otomasi masih manual via Radaar + Integrately
2. **AI Quick Win Sprint belum di-launch** — copy sudah jadi, eksekusi pending
3. **Testimonial database tidak ada** — menghambat case study content
4. **Pricing page Corporate AI Training** — nomor WA placeholder belum diganti
5. **Tidak ada retainer client** — semua masih project-based, zero recurring
6. **Landing page / opt-in page** — belum ada, email growth mengandalkan manual

---

## KAPASITAS SOLO OPERATION

- ~3 jam per klien aktif
- Max ~10 klien simultaneous
- Deep work: beberapa sesi Pomodoro per hari
- Pomodoro level: Goals 1–2 (Cirillo framework)
- Context switching = bottleneck utama produktivitas

---

## ASET DIGITAL AKTIF

| Aset | Angka | Catatan |
|------|-------|---------|
| Instagram @banirisset | 22.9K followers | 534 posts |
| Threads @banirisset | 2.2K followers | Aktif, tumbuh |
| LinkedIn | 5K+ followers + 500 connections | Perlu content activation |
| Email database | 1,500+ contacts | Mix: alumni, referral, network |
| WhatsApp broadcast | Aktif | — |
| banirisset.com | Live | SEO score 72/100 |
| terasdigital.co.id | Live | — |
| Lynk.id/banirisset | Live | Belum ada produk aktif |
