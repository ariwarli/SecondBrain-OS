# Business Productivity Blueprint - Executive One Pager

## Tujuan

Membangun workspace kedua sebagai **Business Productivity Layer** untuk mempercepat eksekusi bisnis Bani Risset: brutal funnel, konten harian lintas channel, proposal/deliverable, dan pipeline revenue, tanpa mengganggu sistem SecondBrain yang sudah berjalan.

## Positioning Sistem

- **SecondBrain (tetap):** capture, canonical knowledge, indexing, retrieval + citation.
- **Business Workspace (baru):** planning, drafting, distribution, revenue tracking, orchestration.
- **Rule keras:** tidak ada pipeline LLM baru; semua drafting wajib lewat Retrieval API existing.

## Scope Utama

1. Client & project tracking
2. Content & campaign execution
3. Proposal & deliverable generation
4. Revenue & invoice pipeline tracking
5. Personal brand execution

## Arsitektur Singkat

- Shared resource: satu VPS, satu vault, satu PostgreSQL, satu vector DB, satu Telegram bot.
- Jalur model resmi: `BusinessExecutionAPI -> Retrieval API existing -> Ollama Cloud API` (tanpa pipeline LLM baru).
- Vault shared adalah Obsidian lokal; sinkronisasi Obsidian lokal <-> VPS wajib terjadwal dan diaudit.
- Tambahan: BusinessExecutionAPI + engine modular (funnel, content, deliverable, revenue, governance).
- Output wajib: markdown di `knowledge-base/content`, `knowledge-base/deliverables`, `knowledge-base/pipeline`.

## Routing Platform (OpenClaw vs Hermes)

- **OpenClaw:** canonical knowledge, retrieval grounding, proposal-grade output, command governance.
- **Hermes:** eksekusi harian multi-channel, batch content, distribution, tracking throughput.
- **Orchestrator:** routing task, lifecycle control, review gate, incident escalation.

## Daily Operating Rhythm

- 06:00 `funnel_gap`
- 06:30 `daily_batch`
- 07:30 review high-risk content
- 09:00 lock publish queue
- 11:00-17:00 distribusi
- 20:00 signal review + pipeline sync
- 21:00 queue shaping untuk hari berikutnya

Minimum output harian:
- Awareness: 2
- Consideration: 1
- Conversion: 1
- Expansion: 1

## Command Set Inti

- `/daily_batch`
- `/funnel_gap`
- `/content_draft`
- `/publish_queue`
- `/proposal_gen`
- `/deal_add`, `/deal_stage`
- `/invoice_update`
- `/pipeline_report`
- `/sla_status`

## Governance Minimum

- Lifecycle task: `Inbox -> Assigned -> In Progress -> Review -> Done|Failed`
- Handoff wajib 5 field: done, artifact path, verifikasi, risiko, next action
- Prompt policy: retrieval-first, citation-required, no-hallucination
- Reconciliation harian: DB vs vault
- Rollback level: workflow, command, schema, operational freeze
- Reliability policy: timeout/retry/circuit-breaker + degrade mode `context_not_sufficient`
- Capacity guardrail: concurrency limit + queue backpressure di shared VPS
- Cost guardrail: budget threshold 70/85/100% + throttle non-critical workflows

## Fallback Operasional (Command Kritis)

- Jika `/daily_batch` gagal: jalankan manual queue shaping untuk asset conversion dulu.
- Jika `/publish_queue` gagal: lock queue via fallback checklist dan publish manual bertahap.
- Jika `/proposal_gen` gagal: fallback ke template proposal baseline + retrieval manual evidence.
- Semua fallback wajib tercatat di audit log dan dipulihkan ke jalur normal di war room terdekat.

## KPI Utama

- Routing accuracy
- SLA harian terpenuhi
- Funnel stage coverage
- Review compliance
- Content-to-revenue linkage
- Pipeline velocity
- Reconciliation success
- MTTD/MTTR incident

## Deliverable Dokumen Master

- Blueprint lengkap: `docs/BUSINESS-PRODUCTIVITY-BLUEPRINT-MASTER.md`
- Bab governance detail: `docs/BUSINESS-PRODUCTIVITY-BLUEPRINT-BAB-15.md`

## Definition of Success (90 Hari)

- Eksekusi konten harian stabil lintas funnel
- Proposal/deliverable turnaround lebih cepat
- Pipeline terhubung langsung dengan output konten
- Shared system tetap stabil tanpa konflik resource
- Outage utama (model API, command routing, vault sync) tertangani via fallback + rollback teruji
