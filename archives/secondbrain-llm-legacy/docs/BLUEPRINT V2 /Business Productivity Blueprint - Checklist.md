# Business Productivity Blueprint - Infrastructure Alignment Checklist
## Tujuan
Checklist untuk memastikan dokumen blueprint sudah **eksplisit** dan **konsisten** dengan infrastruktur aktual:
1. VPS
2. Telegram
3. Ollama Cloud (model API)
4. Obsidian lokal (knowledge)
---
## A. Cross-Document Consistency (Semua Dokumen)
- [ ] Semua dokumen menyebut arsitektur inti yang sama (tanpa kontradiksi).
- [ ] Istilah konsisten: `Retrieval API existing`, `BusinessExecutionAPI`, `vault shared`, `Telegram bot shared`.
- [ ] Tidak ada istilah yang ambigu/berpotensi ditafsir beda antar dokumen.
- [ ] Rule “no new LLM pipeline” tetap konsisten di semua dokumen.
- [ ] Setiap komponen baru punya dependency yang jelas ke infrastruktur existing.
---
## B. VPS Alignment
- [ ] Disebut eksplisit: sistem berjalan di **satu VPS shared**.
- [ ] Boundary resource disebut: CPU/RAM/storage/network dibagi dengan SecondBrain.
- [ ] Ada guardrail beban (batch throttling / concurrency limit).
- [ ] Ada strategi observability minimum (log, audit, error tracking).
- [ ] Ada strategi rollback saat incident (workflow/command/schema/freeze).
---
## C. Telegram Alignment
- [ ] Disebut eksplisit: menggunakan **Telegram bot existing** (shared).
- [ ] Command baru menggunakan extension, bukan bot terpisah.
- [ ] Ada anti-collision command map/versioning.
- [ ] Ada fallback saat command gagal (manual flow atau retry policy).
- [ ] Audit log mencatat command name, owner platform, status, timestamp.
---
## D. Ollama Cloud (Model API) Alignment
- [ ] Disebut eksplisit: backend model untuk retrieval/drafting adalah **Ollama Cloud API**.
- [ ] Relasi jelas: BusinessExecutionAPI -> RetrievalAPIExisting -> Ollama Cloud.
- [ ] Policy timeout/retry/circuit-breaker API tercantum.
- [ ] Ada fallback saat model/API unavailable (`context_not_sufficient` atau degrade mode).
- [ ] Ada kontrol biaya/rate limit/token usage.
- [ ] Tidak ada pipeline LLM duplikat di luar jalur resmi.
---
## E. Obsidian Lokal (Knowledge) Alignment
- [ ] Disebut eksplisit: `vault shared` = **Obsidian lokal**.
- [ ] Path/folder output markdown jelas dan konsisten.
- [ ] Arah data jelas (read retrieval + write artifacts).
- [ ] Mekanisme sinkronisasi lokal <-> VPS dijelaskan ringkas.
- [ ] Ada kebijakan backup/restore untuk vault.
- [ ] Reconciliation DB vs vault dijadwalkan harian.
---
## F. Security & Governance Minimum
- [ ] Access control untuk komponen shared dijelaskan (siapa boleh read/write).
- [ ] Prompt compliance contract aktif (retrieval-first, citation-required, no hallucination).
- [ ] Incident severity A/B/C + SLA respons sudah terdokumentasi.
- [ ] Definition of Done menyebut verifikasi infrastruktur 4 komponen.
- [ ] Bukti audit bisa ditelusuri end-to-end per task/command.
---
## G. Checklist Per Dokumen
## 1) BUSINESS-PRODUCTIVITY-BLUEPRINT-EXECUTIVE-ONE-PAGER.md
- [ ] Tambahkan kalimat eksplisit: model API menggunakan **Ollama Cloud**.
- [ ] Tambahkan kalimat eksplisit: knowledge vault menggunakan **Obsidian lokal**.
- [ ] Pastikan ringkasan “satu VPS, satu bot” tetap ada.
- [ ] Pastikan tidak ada bahasa yang mengesankan stack baru terpisah.
## 2) BUSINESS-PRODUCTIVITY-BLUEPRINT-MASTER.md
- [ ] Pada diagram/komponen, tambah label **Ollama Cloud** di jalur model API.
- [ ] Pada bagian vault, jelaskan bahwa vault shared adalah **Obsidian lokal**.
- [ ] Tambahkan section singkat reliability (timeout/retry/fallback untuk model API).
- [ ] Tambahkan catatan sinkronisasi/akses vault dari VPS.
## 3) BUSINESS-PRODUCTIVITY-BLUEPRINT-BAB-15.md
- [ ] Tambahkan kontrol incident khusus gangguan Ollama Cloud API.
- [ ] Tambahkan kontrol incident khusus desync Obsidian lokal vs DB/vault view.
- [ ] Tambahkan KPI/indikator availability model API (opsional).
- [ ] Pastikan rollback level men-cover command/routing saat provider model bermasalah.
## 4) BUSINESS-PRODUCTIVITY-BLUEPRINT-PITCH-DECK-OUTLINE-10-SLIDES.md
- [ ] Slide arsitektur menyebut eksplisit 4 infrastruktur: VPS, Telegram, Ollama Cloud, Obsidian lokal.
- [ ] Slide governance menambahkan risk item untuk API model outage + vault sync risk.
- [ ] Slide roadmap menambahkan milestone validasi integrasi Ollama + Obsidian.
- [ ] Slide constraint compliance tetap menegaskan “tanpa pipeline LLM baru”.
---
## H. Final Go/No-Go
- [ ] GO hanya jika 4 komponen infrastruktur disebut eksplisit di dokumen strategis.
- [ ] GO hanya jika dependency chain end-to-end tidak ambigu.
- [ ] GO hanya jika fallback + rollback untuk outage utama sudah tertulis.
- [ ] GO hanya jika audit/reconciliation berjalan harian.
- [ ] Jika satu item kritikal gagal, status = **NO-GO** sampai diperbaiki.