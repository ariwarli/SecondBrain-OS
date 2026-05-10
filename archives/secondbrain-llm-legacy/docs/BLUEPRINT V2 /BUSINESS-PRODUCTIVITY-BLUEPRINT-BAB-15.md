# 15. Governance & Audit Layer

Bab ini menutup blueprint agar production-grade: ada change control, quality gate, auditability, rollback, dan incident handling untuk resource yang shared (vault, PostgreSQL, Telegram bot, retrieval API).

## 15.1 Tujuan Governance

- Menjaga kualitas output tetap tinggi saat volume eksekusi naik.
- Mencegah drift antara knowledge layer (SecondBrain) dan execution layer (Business Workspace).
- Menjamin semua perubahan bisa diaudit, di-reconcile, dan di-rollback tanpa ganggu sistem existing.

## 15.2 Scope Governance

- Change control untuk schema, command bot, workflow, template.
- Audit trail untuk konten, deliverable, pipeline, dan notifikasi.
- Compliance prompt policy (retrieval-first, citation-first, no-hallucination).
- Rollback strategy untuk error operasional.
- Incident playbook untuk shared resource conflict.

## 15.3 Governance Principles (Wajib)

- Documents are source of truth.
- Retrieval mendahului generation.
- Tidak ada pipeline LLM duplikat.
- Semua output bisnis wajib markdown di vault shared.
- Semua entity bisnis di PostgreSQL wajib referensial ke `knowledge_note` atau `raw_capture` jika relevan.
- Failed state valid, tetapi harus ada reason, evidence, dan recovery step.

## 15.4 Change Control Policy

Perubahan diklasifikasikan:

- **Low risk**
  - perubahan template minor
  - perubahan copy non-client-facing
- **Medium risk**
  - perubahan workflow content lifecycle
  - perubahan query filter metadata
- **High risk**
  - perubahan schema `biz`
  - command Telegram baru atau perubahan routing command
  - perubahan policy retrieval/prompt contract

Aturan approval:

- Low: owner modul.
- Medium: owner modul + reviewer.
- High: orchestrator + reviewer + approval owner sistem.

## 15.5 Prompt Compliance Contract

Semua modul drafting wajib mematuhi:

- hanya gunakan context hasil retrieval yang diberikan,
- sertakan sumber note,
- jika context tidak cukup, return `context_not_sufficient`,
- dilarang menambah klaim tanpa evidence.

Prompt non-compliant dianggap incident kualitas.

## 15.5.1 Reliability Contract untuk Model API

- Jalur resmi model: `BusinessExecutionAPI -> Retrieval API existing -> Ollama Cloud API`.
- Timeout:
  - retrieval request: 10 detik
  - model call via retrieval: 30 detik
- Retry:
  - maksimal 2 retry, backoff 1 detik lalu 3 detik
  - hanya untuk kegagalan transient (timeout, network reset, 5xx)
- Circuit breaker:
  - open jika 5 failure beruntun dalam 60 detik
  - hold open 120 detik
  - half-open 1 probe request sebelum normalisasi
- Degrade mode wajib:
  - return `context_not_sufficient` jika retrieval/model tidak sehat
  - dilarang generate claim tanpa evidence

## 15.6 Audit Trail Requirements

Setiap task/command harus meninggalkan jejak:

- `task_id`
- `command_name`
- `owner_platform` (`openclaw` atau `hermes`)
- `input_ref` (note/capture id)
- `output_path` (vault markdown path)
- `status` (`done/failed/review_reject`)
- `reviewer`
- `timestamp`

Audit disimpan di:

- PostgreSQL: tabel log operasional `biz.execution_audit_log`
- Vault: ringkasan mingguan di `knowledge-base/pipeline/audit/`

## 15.7 Data Reconciliation Policy

Rekonsiliasi harian wajib:

- bandingkan status di `biz.daily_content_queue` vs file aktual `knowledge-base/content/`
- bandingkan `biz.deliverable_item` vs file `knowledge-base/deliverables/`
- tandai mismatch sebagai `reconcile_failed`

Hasil rekonsiliasi masuk laporan:

- `knowledge-base/pipeline/audit/reconciliation-YYYY-MM-DD.md`

Tambahan khusus vault:

- `vault shared` didefinisikan sebagai Obsidian lokal.
- Sinkronisasi Obsidian lokal <-> VPS wajib diverifikasi harian:
  - file count delta,
  - checksum sampling,
  - mismatch critical path (`content`, `deliverables`, `pipeline`).
- Jika desync melewati threshold:
  - tandai incident minimal kelas B,
  - freeze write non-critical hingga sync pulih.

## 15.8 Rollback Strategy

Rollback level:

- **Level 1 (Workflow rollback)**  
  Kembalikan state task ke `Assigned` dari `In Progress/Review`.
- **Level 2 (Command rollback)**  
  Nonaktifkan command baru dan kembali ke command map versi sebelumnya.
- **Level 3 (Schema rollback)**  
  Nonaktifkan fitur yang bergantung pada kolom/tabel baru; gunakan migration down script terverifikasi.
- **Level 4 (Operational freeze)**  
  Hanya command read-only diizinkan sampai root cause ditutup.

Rule rollback:

- Tidak menghapus artifact markdown yang sudah terbit; gunakan status `superseded`.
- Tidak melakukan destructive reset pada DB shared tanpa approval eksplisit.

## 15.9 Incident Playbook

### Incident Kelas A (Kritis)

Contoh:
- command bot conflict yang mengganggu command lama,
- output client-facing salah konteks tanpa citation,
- mismatch masif DB-vault.

Tindakan:
1. freeze command terkait,
2. aktifkan fallback workflow manual,
3. jalankan rollback sesuai level,
4. publish incident note maksimal 60 menit.

### Incident Kelas B (Mayor)

Contoh:
- keterlambatan SLA harian >20%,
- banyak task gagal review karena quality drift.

Tindakan:
1. throttle batch harian,
2. naikkan mandatory review,
3. lakukan root-cause review pada war room berikutnya.

Kasus khusus kelas B:

- Ollama Cloud unavailable > 10 menit dengan dampak ke drafting throughput.
- Obsidian sync mismatch di folder output bisnis selama 2 siklus harian.

### Incident Kelas C (Minor)

Contoh:
- 1-2 task gagal karena context tipis.

Tindakan:
1. return `context_not_sufficient`,
2. minta context tambahan,
3. lanjutkan batch lainnya.

## 15.10 RACI Governance

| Aktivitas | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Change approval medium/high risk | Orchestrator | Owner sistem | Reviewer | Tim eksekusi |
| Prompt compliance audit | Reviewer | Orchestrator | OpenClaw owner | Hermes owner |
| Reconciliation harian | Hermes owner | Orchestrator | OpenClaw owner | Tim eksekusi |
| Incident handling | Orchestrator | Owner sistem | Reviewer | Semua owner modul |
| Rollback execution | Owner modul | Orchestrator | Reviewer | Tim terkait |

## 15.11 Governance KPI

- `% prompt compliance pass`
- `% task dengan audit log lengkap`
- `% reconciliation success`
- `% model api availability`
- `% degrade mode handled correctly`
- `% vault sync success`
- `MTTD` (mean time to detect incident)
- `MTTR` (mean time to recover)
- `% rollback success tanpa side effect`

## 15.11.1 Capacity & Cost Guardrail KPI

- `% hari tanpa breach concurrency limit`
- `p95 queue latency`
- `% hari di atas threshold budget 85%`
- `% non-critical job yang berhasil ditrottle saat budget breach`

## 15.12 Governance Cadence

- **Harian:** reconciliation + SLA compliance check.
- **Mingguan:** audit sampling output high-risk + review incident log.
- **Bulanan:** governance review (policy update, threshold tuning, risk register refresh).
- **Harian tambahan:** reliability check (timeout/retry/circuit breaker hit rate), sync check Obsidian, budget threshold check 70/85/100%.

## 15.13 Definition of Done Bab 15

Bab 15 dianggap aktif jika:

- change control berjalan dengan approval matrix.
- audit trail tersedia untuk semua command utama.
- reconciliation report harian rutin terbit.
- rollback level 1-3 sudah diuji.
- incident playbook berjalan dengan SLA respons terukur.
- reliability contract Ollama Cloud aktif dan terukur.
- sync contract Obsidian lokal <-> VPS aktif dan terukur.
- capacity/cost guardrail berjalan dengan bukti audit.

## 15.16 Command Critical Runbook (Minimum)

Runbook wajib terdokumentasi dan diuji untuk command berikut:

- `/daily_batch`
  - failure mode: timeout model/retrieval, queue overload
  - fallback: conversion-first manual queue
  - restore: replay job idempotent per `idempotency_key`
- `/publish_queue`
  - failure mode: route conflict atau write vault gagal
  - fallback: lock queue manual checklist + publish bertahap
  - restore: command map rollback + reconciliation post-publish
- `/proposal_gen`
  - failure mode: retrieval context tipis/model unavailable
  - fallback: baseline template + manual retrieval evidence
  - restore: rerun generation setelah circuit half-open sukses

## 15.14 Template Incident Report

```md
# Incident Report

## Metadata
- incident_id:
- severity:
- detected_at:
- detected_by:

## Impact
- affected_module:
- affected_commands:
- business_impact:

## Root Cause
- summary:
- evidence_refs:

## Mitigation
- immediate_actions:
- rollback_level:
- recovery_time:

## Preventive Action
- policy_update:
- owner:
- due_date:
```

## 15.15 Penutup Governance

Dengan bab ini, blueprint bukan hanya kuat untuk produksi konten dan scaling revenue, tapi juga aman untuk dijalankan di atas resource shared yang sama dengan SecondBrain tanpa mengganggu stabilitas sistem existing.
