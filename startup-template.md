<!--
Tujuan: file canonical startup untuk REED / Hermes workspace
Owner: startup-doc-maintainer
Main Functions: instruksi cold boot untuk sesi baru agent utama
Side Effects: set base state untuk routing, memory, dan identity
-->

# Startup Template

File ini adalah aturan permanen (canonical) untuk memulai sesi baru. Jangan buat duplikat file startup.
Konteks sesi berjalan ada di `session-snapshot.md`.

## Working Directory

Set `cwd` / home agent ke:
`/Users/banirisset/2_Areas/banirisset`

## Initialization Sequence (Read Order)

Baca secara berurutan saat fresh boot:

### 1. Core Identity & Voice
- `AGENTS.md` (Base Rules)
- `core/SOUL.md` (Voice & Inbox Rules)
- `core/USER.md` (Target User)

### 2. Live Operating State
- `hermes.md` (Runtime brain & transition state)
- `daily.md` (Scoreboard hari ini)
- `docs/REED_RUNTIME_ARCHITECTURE.md` (Target architecture & boundaries)

### 3. Memory & Continuity
- `memory/YYYY-MM-DD.md` (Hari ini dan kemarin)
- `session-snapshot.md` (Konteks live sesi)

### 4. Canon & Library (Bila relevan)
- `knowledge-base/wiki/index.md`
- `knowledge-base/wiki/log.md`
- `knowledge-base/wiki/sessions/*-active.md`

### Optional Stronger Handoff
Bila butuh deep context:
- `core/session-handoff-prompt-gemini.md`
- `crm.md`
- `docs/AGENT_OWNERSHIP_SOP.md` (Jika ada isu delegasi/ownership)

## Memory Tier Boundaries

Patuhi 3 lapis memori (`docs/REED_MEMORY_AND_LEARNING.md`):
1. **Operational Memory (Hermes)**: Padat, curated, penentu perilaku di sesi baru.
2. **Session Recall**: Log percakapan dan detail lama. Bukan canon.
3. **Canon Library (Wiki)**: `knowledge-base/wiki/`. Durable, reusable. Bucket resmi: `Research`, `Frameworks`, `SOPs`, `Decisions`, `Incidents`.

**Strict Rules**:
- Jangan jadikan `INBOX` sebagai final bucket.
- Jangan biarkan `Hermes` (operational memory) menjadi wiki.
- Jangan biarkan `Wiki` menjadi agent RAM.

## Inbox & Routing Rules

Semua pesan Telegram di `INBOX` (thread 11) WAJIB masuk proses routing (`docs/INBOX_ROUTING.md`).

**Inbox adalah ack-only:**
- Maksimum 2 baris singkat.
- Tidak ada status recap, to-do list lengkap, prioritisasi, atau pertanyaan di Inbox.
- Tidak ada percakapan kerja lanjutan di Inbox.
- Balas format: `✅ [ROUTED → bucket] path/file` \n `Next: lanjut di [lane tujuan]`

**Lane Operasional Tujuan:**
- `tasks` (Project, task, to-do list)
- `content` (Draft post, ide)
- `personal-crm` (Relasi, follow-up, kontak)
- `ops` (Infrastruktur, runtime Hermes)
- `knowledge-base` (Bahan bacaan, URL, PDF)
- `updates` (Laporan harian, alert)

**Mixed Message Rule:**
Jika pesan memuat multi-fungsi (contoh: minta reminder + draft konten), split dan route ke lane masing-masing.

## Delegation & Ownership

- `main` = Orchestrator, memory continuity, user-facing routing.
- `reed-archivist` = CRM, knowledge base ingestion, wiki canon promotion.
- `reed-researcher` = Research & synthesis.
- `reed-builder` = Implementasi kode & tooling.
- Roster lengkap baca: `docs/AGENT_OWNERSHIP_SOP.md`.
