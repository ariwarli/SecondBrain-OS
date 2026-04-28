MASTER BLUEPRINT — Secondbrain OS (Bani Risset)
- Tujuan utama: REED gak overload, knowledge jadi compounding asset, dan operasi harian lo rapi + terukur.
- Prinsip: single source of truth, deterministic routing, Obsidian-first, audit trail wajib.
A. Blueprint Arsitektur Inti (yang wajib jadi dulu)
1) Control Plane Multi-Agent
- Scope: main, reed-archivist, reed-builder, reed-researcher, reed-wellbeing
- Deliverable:
  - BOT-MATRIX.md (sudah)
  - SOP-main.md s/d SOP-reed-wellbeing.md (sudah)
  - HANDOFF-PROTOCOL.md (sudah)
- DoD:
  - 1 topik = 1 owner bot
  - escalation lintas domain selalu lewat main
  - publish gate final di main
2) Topic Routing Deterministik
- Scope: Inbox -> klasifikasi -> target topic/folder
- Deliverable:
  - INBOX_ROUTING.md final v1 (terkunci keyword + fallback unsorted)
  - Routing matrix Telegram topic -> bot -> folder output
- DoD:
  - salah route < 10%
  - unsorted punya SLA triage (mis. <24 jam)
3) Memory Plane Obsidian-Only
- Scope: hapus ketergantungan Notion, semua memory markdown
- Deliverable:
  - Struktur knowledge-base/raw, knowledge-base/wiki, wiki/index.md, wiki/log.md
  - Policy memory di AGENTS.md (sudah: auto checkpoint tiap 20 chat)
- DoD:
  - tidak ada alur aktif ke Notion
  - semua knowledge penting masuk wiki markdown
---
B. Blueprint Sinkronisasi VPS <-> Obsidian (aman-teraudit)
4) Git-Sync Audited (bukan realtime liar)
- Scope: sync dua arah berbasis Git
- Opsi remote:
  1. VPS bare repo (recommended cepat)
  2. GitHub private (opsional mirror offsite)
- Aturan:
  - sebelum nulis: pull --rebase
  - sesudah nulis: add/commit/push
  - conflict: no force push, wajib log ke wiki/log.md
- Deliverable:
  - KB-SYNC-RULES.md
  - KB-CONFLICT-RUNBOOK.md
- DoD:
  - 3 skenario lolos: VPS->Mac, Mac->VPS, concurrent conflict handled
5) Checkpoint Worker Hardening (hemat resource)
- Scope: auto save tiap 20 chat/session (sudah hidup), optimasi resource
- Upgrade plan:
  - timer 2 menit -> 5 menit
  - skip session yang mtime tidak berubah
  - max file scan window per run
- Deliverable:
  - tuning policy di SOP ops
  - metrik run (success/fail/duration)
- DoD:
  - CPU/IO stabil
  - checkpoint tetap konsisten
---
C. Blueprint Knowledge Compounding (model Karpathy/LLM Wiki)
6) Ingest Workflow Standar
- Scope: raw -> diskusi/sintesis -> wiki pages -> index/log
- Deliverable:
  - template halaman wiki
  - template ingest checklist
  - citation rule (source: filename)
- DoD:
  - setiap source update index.md + log.md
  - tidak ada klaim tanpa source
7) Wiki Quality Loop
- Scope: lint wiki rutin
- Audit item:
  - orphan pages
  - broken links
  - contradiksi
  - outdated claims
- Deliverable:
  - checklist lint mingguan
- DoD:
  - orphans turun bertahap
  - page format konsisten
---
D. Blueprint Security & Privacy
8) Data Boundary Policy
- Scope: personal/wellbeing vs workspace umum
- Rule:
  - wellbeing/personal default exclude dari repo umum
  - share hanya explicit approval
  - no secret/token di repo
- Deliverable:
  - KB-DATA-CLASSIFICATION.md (Public/Internal/Sensitive/Restricted)
- DoD:
  - tidak ada leakage lane wellbeing ke lane umum
9) Credential Hygiene
- Scope: env/token debt cleanup berkelanjutan
- Deliverable:
  - rotasi key playbook
  - scan berkala string sensitif
- DoD:
  - tidak ada secret hardcoded baru
---
E. Blueprint Operasional Harian
10) Daily Command Center
- Scope: satu dashboard harian lintas ruang
- Deliverable:
  - state/control-tower.md (Top 3, blocker, owner, due)
- DoD:
  - lo bisa lihat status sistem dalam <2 menit
11) Weekly Review Engine
- Scope: review output + bottleneck + keputusan minggu depan
- Deliverable:
  - state/weekly-review.md template
- DoD:
  - keputusan minggu berikutnya selalu tertulis
---
F. Blueprint Implementasi Bertahap (Roadmap)
Phase 1 (Minggu 1) — Stabilkan Fondasi
- lock role matrix + routing v1
- lock Obsidian-only policy
- tuning checkpoint worker (hemat resource)
- hasil: operasi gak chaos
Phase 2 (Minggu 2) — Nyalakan Git Sync Audited
- bootstrap repo knowledge
- atur SSH key + remote private
- uji 3 skenario sync
- hasil: memory durable + sinkron dua arah
Phase 3 (Minggu 3–4) — Compounding Knowledge
- aktifkan ingest+lint cycle
- rapikan index/log/wiki format
- hasil: knowledge mulai reusable dan makin cepat dipakai
Phase 4 (Bulan 2–3) — Scale & Governance
- KPI dashboard
- privacy/security hardening
- offsite mirror opsional
- hasil: siap scale tanpa rewrite
---
G. KPI yang dipakai (biar objektif)
- Routing accuracy (% pesan masuk owner benar)
- Time-to-output (inbox -> output pertama)
- Task aging (task >7 hari)
- Knowledge reuse rate (berapa kali page dipakai ulang)
- Checkpoint health (run success rate)
- Conflict resolution time (git sync conflict)
- Sensitive data incidents (target: 0)
---
H. Risiko yang harus dihindari
- tambah bot terlalu cepat tanpa boundary
- full auto sync semua lane (noise + leak)
- two-way sync tanpa policy conflict
- jadikan chat mentah sebagai memory final
- ubah banyak sistem sekaligus tanpa phase gate
