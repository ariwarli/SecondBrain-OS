<!--
Tujuan: peta navigasi utama arsitektur dan flow inti repo SECONDBRAIN-LLM
Caller: user atau agent yang memulai sesi analisis / implementasi
Dependensi: README root, docs/README.md, knowledge-base/README.md, knowledge-base/tools/*.py
Main Functions: ringkasan proyek, flow inti, clean tree, module map, data/config, integrasi eksternal
Side Effects: none, dokumentasi only
-->

# Project Summary

- Tujuan aplikasi: pusat dokumen, governance, dan knowledge-base Obsidian/Git untuk workflow SecondBrain LLM dan REED.
- Tech stack utama: Markdown vault, Python CLI utilities, Git-backed knowledge base, Obsidian-compatible storage, SSH/systemd check ke VPS OpenClaw, optional premium ingestion vendors.
- Runtime/framework utama: Python 3 script-based tooling di `knowledge-base/tools/`; tidak ada web app/server utama di scope repo ini.
- DB/queue utama: Not found.
- Pola arsitektur singkat: docs-first + filesystem workflow. Root repo menyimpan panduan dan governance, sedangkan `knowledge-base/` menyimpan memory canonical dan tool lokal yang memproses file markdown.

# Core Logic Flow (Function-Level Flowchart)

- Processed markdown -> `kb_ingest.main` -> `ingest_file` -> `parse_processed_file` -> `build_ingest_plan` -> `write_index_entry` / `write_vault_index_entry` / `write_log_entry` / `record_ingest` -> filesystem (`raw/`, folder canonical, `index.md`, `wiki/log.md`, `state/kb-ingest-state.json`)
- Pending processed folder -> `kb_ingest.main --pending` -> `pending_files` -> `ingest_file` per file -> filesystem canonical
- Save-update CLI -> `session_handoff.main` -> `synthesize_context_fallbacks` -> `write_outputs` -> `build_checkpoint` / `build_handoff` / `update_active_text` / `append_log` -> filesystem (`wiki/sessions/`, `wiki/log.md`)
- Save-update with VPS snapshot -> `session_handoff.main --vps-snapshot` -> `vps_snapshot` -> `run_readonly` -> SSH + systemd status + premium readiness -> checkpoint markdown
- Wiki maintenance check -> `wiki_lint.main` -> `run_lint` -> `iter_markdown_files` / `backlinks_map` / `lint_file` -> lint findings stdout
- Premium readiness check -> `premium_stack_readiness.main` -> `build_report` -> `load_local_env` / `resolve_value` / `is_set` -> env status report

# Clean Tree

```text
SECONDBRAIN-LLM/
├── AGENTS.md
├── README.md
├── START-HERE.md
├── SOUL.md
├── USER.md
├── USER-ONE-PAGER.md
├── INBOX_ROUTING.md
├── DAILY-OPERATING-RHYTHM.md
├── Blueprint Implementasi SecondBrain LLM.md
├── docs/
│   ├── README.md
│   ├── REED-INTERACTION-GUIDE.md
│   ├── REED-STARTER-TEMPLATES.md
│   ├── INBOX-ROUTER-GUIDE.md
│   ├── BOT-MATRIX.md
│   ├── HANDOFF-PROTOCOL.md
│   ├── KB-SYNC-RULES.md
│   ├── KB-CONFLICT-RUNBOOK.md
│   ├── KB-DATA-CLASSIFICATION.md
│   ├── SOP-main.md
│   └── SOP-reed-archivist*.md
└── knowledge-base/
    ├── README.md
    ├── .env.premium.example
    ├── .env.premium.local
    ├── index.md
    ├── inbox/
    │   ├── index.md
    │   ├── _template.md
    │   └── processed/
    ├── raw/
    ├── notes/
    ├── projects/
    ├── people/
    ├── decisions/
    ├── meetings/
    ├── references/
    ├── research/
    ├── archive/
    ├── state/
    │   ├── control-tower.md
    │   └── weekly-review.md
    ├── wiki/
    │   ├── index.md
    │   ├── log.md
    │   ├── page-template.md
    │   ├── ingest-checklist.md
    │   ├── kb-sync-rules.md
    │   ├── kb-conflict-runbook.md
    │   ├── kb-data-classification.md
    │   ├── wiki-maintenance-policy.md
    │   ├── wiki-maintenance-runbook.md
    │   └── sessions/
    ├── tools/
    │   ├── kb_ingest.py
    │   ├── session_handoff.py
    │   ├── wiki_lint.py
    │   └── premium_stack_readiness.py
    └── tests/
        ├── test_kb_ingest.py
        ├── test_session_handoff.py
        ├── test_vault_structure.py
        └── test_wiki_lint.py
```

# Module Map (The Chapters)

- `README.md`
  - Fungsi/class publik utama: Not found
  - Peran modul: menjelaskan boundary repo sebagai control center dokumen dan memisahkan root docs dari `knowledge-base/`.

- `START-HERE.md`
  - Fungsi/class publik utama: Not found
  - Peran modul: entrypoint operasional tercepat untuk user saat memulai kerja dengan REED.

- `AGENTS.md`
  - Fungsi/class publik utama: Not found
  - Peran modul: aturan operasional subtree, source-of-truth order, dan boundary runtime OpenClaw/knowledge-base.

- `docs/README.md`
  - Fungsi/class publik utama: Not found
  - Peran modul: indeks dokumen harian, governance, knowledge repo rules, dan audit artifacts.

- `knowledge-base/README.md`
  - Fungsi/class publik utama: Not found
  - Peran modul: definisi struktur vault, daily flow, ingest pipeline, recall order, dan health-check knowledge-base.

- `knowledge-base/tools/kb_ingest.py`
  - Fungsi/class publik utama: `ProcessedItem`, `IngestPlan`, `IngestResult`, `parse_processed_file`, `build_ingest_plan`, `ingest_file`, `main`
  - Peran modul: mengubah file processed markdown menjadi raw capture + canonical note + index/log/state yang idempotent.

- `knowledge-base/tools/session_handoff.py`
  - Fungsi/class publik utama: `SaveUpdate`, `synthesize_context_fallbacks`, `build_checkpoint`, `build_handoff`, `write_outputs`, `main`
  - Peran modul: membuat checkpoint save-update, handoff agent berikutnya, update active session, dan append audit log.

- `knowledge-base/tools/wiki_lint.py`
  - Fungsi/class publik utama: `LintFinding`, `iter_markdown_files`, `backlinks_map`, `lint_file`, `run_lint`, `main`
  - Peran modul: memeriksa kualitas note canonical dan wiki secara read-only untuk mendeteksi page tipis, orphan, source hilang, dan review stale.

- `knowledge-base/tools/premium_stack_readiness.py`
  - Fungsi/class publik utama: `ProviderSpec`, `load_local_env`, `build_report`, `main`
  - Peran modul: mengecek kesiapan env premium stack tanpa melakukan panggilan API eksternal.

- `knowledge-base/tests/test_kb_ingest.py`
  - Fungsi/class publik utama: `KbIngestTests`
  - Peran modul: menguji parsing processed markdown, routing/classification, idempotency, metadata carry-over, dan mode `--pending`.

- `knowledge-base/tests/test_session_handoff.py`
  - Fungsi/class publik utama: `SessionHandoffTests`
  - Peran modul: menguji fallback penyusunan item `done` dan prioritas sumber konteks saat save-update.

- `knowledge-base/tests/test_vault_structure.py`
  - Fungsi/class publik utama: `VaultStructureTests`
  - Peran modul: memastikan direktori canonical, template, dokumen sistem, dan ignore runtime artifacts tetap konsisten.

- `knowledge-base/tests/test_wiki_lint.py`
  - Fungsi/class publik utama: `WikiLintTests`
  - Peran modul: menguji aturan lint untuk note yang baik versus note bermasalah.

# Data & Config

- Lokasi `.env*` / config utama:
  - `knowledge-base/.env.premium.example`
  - `knowledge-base/.env.premium.local`
  - `knowledge-base/.gitignore`
  - `AGENTS.md`
  - `knowledge-base/README.md`

- Skema data singkat:
  - `ProcessedItem`: representasi file processed mentah yang sudah punya `Timestamp`, `Bucket`, `Routed to`, `Original`, dan metadata sumber.
  - `IngestPlan`: rencana output deterministic untuk satu processed item, termasuk path raw/final, folder target, classification, dan metadata sumber.
  - `IngestResult`: status hasil ingest (`created`, `dry_run`, `skipped`, `invalid`, `skipped_restricted`).
  - `SaveUpdate`: paket data save-update untuk checkpoint/handoff, berisi session, done, evidence, blocker, next action, dan opsi VPS snapshot.
  - `LintFinding`: satu temuan lint berisi code, path, dan detail.

- Entity/folder inti + relasi ringkas:
  - `inbox/processed/*.md` -> sumber input ingest.
  - `raw/YYYY-MM-DD/*.md` -> salinan mentah append-only dari processed item.
  - `notes/`, `projects/`, `people/`, `decisions/`, `meetings/`, `references/`, `research/`, `archive/` -> note canonical hasil ingest atau kurasi manual.
  - `index.md` root vault + `*/index.md` -> navigasi ringkas ke note canonical.
  - `wiki/log.md` -> audit trail ingest dan save-update.
  - `wiki/sessions/*-active.md` + checkpoint `cp-*.md` + handoff -> memory aktif dan histori session.
  - `state/kb-ingest-state.json` -> state idempotency ingest.

- DB/collection/entity formal:
  - Database schema: Not found
  - Collection schema: Not found
  - Queue broker formal: Not found

- Lokasi migration/seed:
  - Migration: Not found
  - Seed: Not found

- Folder output/runtime artifacts:
  - `knowledge-base/raw/`
  - `knowledge-base/inbox/processed/`
  - `knowledge-base/wiki/log.md`
  - `knowledge-base/wiki/sessions/`
  - `knowledge-base/state/`

# External Integrations

- SSH ke VPS OpenClaw
  - Modul pemanggil: `knowledge-base/tools/session_handoff.py`
  - Peran: ambil snapshot status service non-secret saat `--vps-snapshot` dipakai.

- systemd service checks (`openclaw-gateway.service`, `inbox-monitor.service`, `session-checkpoint.timer`)
  - Modul pemanggil: `knowledge-base/tools/session_handoff.py`
  - Peran: validasi singkat runtime VPS dalam checkpoint.

- Firecrawl
  - Modul pemanggil: `knowledge-base/tools/premium_stack_readiness.py`
  - Peran: lane ingestion web/doc/PDF via env readiness check.

- AssemblyAI
  - Modul pemanggil: `knowledge-base/tools/premium_stack_readiness.py`
  - Peran: lane ingestion audio/video/YouTube via env readiness check.

- You.com Research
  - Modul pemanggil: `knowledge-base/tools/premium_stack_readiness.py`
  - Peran: lane research bersitasi via env readiness check.

- Git / Obsidian
  - Modul pemanggil: `knowledge-base/README.md` workflow, seluruh vault structure
  - Peran: storage dan navigasi canonical knowledge-base.

# Risks / Blind Spots

- Runtime OpenClaw live tidak berada di source repo ini; aturan dan referensi ada di dokumen, tetapi implementasi live service berada di VPS / subtree lain.
- Repo ini tidak memiliki entrypoint web/server/API utama; flow sistem yang bisa dipetakan pasti hanya CLI/tooling lokal dan workflow markdown.
- Banyak behavior level produk berada di dokumen governance, bukan di kode executable lokal.
- `knowledge-base/.env.premium.local` ada sebagai lokasi config, tetapi nilainya tidak boleh dipetakan; hanya keberadaan dan tujuan env yang bisa dijelaskan.
- Beberapa state penting bersifat runtime/file-generated, misalnya `state/kb-ingest-state.json`, checkpoint session, dan isi `wiki/log.md`; struktur diketahui, isi aktual bisa berubah setiap saat.
- Dynamic import / generated code: Not found.
- DB schema formal / migration chain / seed pipeline: Not found.
