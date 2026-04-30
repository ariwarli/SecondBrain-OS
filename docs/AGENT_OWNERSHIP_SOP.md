<!--
Tujuan: source of truth tunggal untuk ownership agent, memory, canon, dan domain kerja SECONDBRAIN OS
Caller: agent utama, subagent, operator workspace, dan sesi startup baru
Dependensi: AGENTS.md, hermes.md, docs/REED_MEMORY_AND_LEARNING.md, ops/subagents/README.md
Main Functions: memetakan owner per domain, writable assets, dan escalation path
Side Effects: mencegah overlap ownership, proliferasi file, dan ambiguity "siapa pegang apa"
-->

# Agent Ownership SOP

Dokumen ini adalah source of truth tunggal untuk ownership agent di SECONDBRAIN OS / Hermes.

## Core Rule

- satu domain = satu owner utama
- agent non-owner boleh membuat candidate, draft, atau output antara
- final write ke canonical source dilakukan oleh owner domain
- jangan buat file baru jika domain itu sudah punya canonical file
- kalau ragu, escalate ke owner domain, bukan membuat dokumen baru

## Active Roster

### `main`

Peran:
- operator utama REED
- interface Telegram / user-facing command layer
- orchestrator delegasi dan keputusan lintas lane

Default domain:
- routing keputusan
- routing dari `Inbox`
- perilaku balasan user-facing di `Inbox`
- pemecahan mixed message ke lane tujuan
- continuity operasional Hermes
- runtime state dan live-operating docs

### `reed-archivist`

Peran:
- ingestion worker
- CRM/knowledge processor
- canon promotion owner

Default domain:
- `inbox/pending`, `inbox/processed`, `inbox/unsorted`
- CRM structured memory
- knowledge-base ingestion lane
- promosi ke wiki canon

### `reed-researcher`

Peran:
- research worker
- source synthesis
- benchmark / competitor / market analysis

Default domain:
- research artifacts
- synthesis yang belum jadi canon

### `reed-builder`

Peran:
- implementation worker
- internal tools / automation prototype builder

Default domain:
- build artifacts
- changed files
- technical implementation output

### `startup-doc-maintainer`

Peran:
- owner governance untuk startup/handoff docs
- anti-proliferation guard untuk file bootstrap/handoff

Catatan:
- ini role resmi untuk ownership dokumen
- role ini tidak harus selalu menjadi runtime bot terpisah
- saat belum ada runtime agent khusus, role ini dipanggil sebagai maintenance contract

Default domain:
- startup/handoff docs
- redirect/stub compat docs
- aturan anti-duplikasi file startup

## Ownership Matrix

| Domain | Owner Utama | Non-owner Yang Boleh Draft | Canonical Output |
| --- | --- | --- | --- |
| Hermes operational memory | `main` | `reed-archivist` | runtime REED/Hermes operational memory + continuity files |
| Session recall / persistence | runtime REED session store | `main` | session store / persistence layer |
| Obsidian Wiki LLM / `knowledge-base/wiki` | `reed-archivist` | `main`, `reed-researcher`, `reed-builder` | wiki canon buckets: `Research`, `Frameworks`, `SOPs`, `Decisions`, `Incidents` |
| `knowledge-base/` ingestion lane | `reed-archivist` | `main`, `reed-researcher` | staged knowledge summaries, references, promotion candidates |
| Inbox routing policy | `main` | `reed-archivist` | routing rules + lane decision |
| Inbox user-facing reply behavior | `main` | none | short ack-only response in `Inbox` |
| Inbox staging folders (`pending` / `processed` / `unsorted`) | `reed-archivist` | `main` | orderly staging state and ingestion hygiene |
| CRM structured memory | `reed-archivist` | `main` | `crm.md` and CRM follow-up structure |
| Research lane | `reed-researcher` | `main` | research reports and source synthesis |
| Build / tooling lane | `reed-builder` | `main` | implementation artifacts, tests, changed files |
| Startup / handoff docs | `startup-doc-maintainer` | `main` | canonical startup prompt + compat stub |
| Runtime architecture / live operating docs | `main` | `reed-builder` | runtime docs, live compat notes, operating state |

## Memory Ownership

### Siapa in charge untuk memorinya Hermes?

`main`

Ruang lingkup:
- operational continuity
- active context
- what REED needs in its head at boot
- current working state

`reed-archivist` boleh membantu ekstraksi, cleanup, atau promotion, tetapi bukan owner utama.

### Siapa in charge untuk Obsidian Wiki LLM?

`reed-archivist`

Ruang lingkup:
- `knowledge-base/wiki/`
- bucket canon resmi:
  - `Research`
  - `Frameworks`
  - `SOPs`
  - `Decisions`
  - `Incidents`

`main`, `reed-researcher`, dan `reed-builder` boleh menghasilkan material kandidat, tetapi promosi canon final dimiliki `reed-archivist`.

## Domain Rules

### Operational Memory

Masuk domain `main` jika informasinya:
- perlu selalu relevan saat boot
- mengubah perilaku REED
- merupakan continuity operasional, bukan pustaka durable

Jangan pindahkan ke wiki hanya karena “terasa penting”.

### Inbox Ownership

`main` adalah owner tunggal untuk:
- routing dari `Inbox`
- perilaku balasan di `Inbox`
- split mixed message ke lane tujuan
- keputusan lane akhir bila satu pesan menyentuh banyak fungsi

`reed-archivist` bukan owner percakapan user-facing di `Inbox`.

`reed-archivist` hanya pegang:
- `inbox/pending`
- `inbox/processed`
- `inbox/unsorted`
- CRM/knowledge processing
- canon promotion prep

Akuntabilitas:
- jika `Inbox` penuh karena chatter, recap, atau dialog kerja yang salah tempat: owner `main`
- jika staging `pending/unsorted/processed` berantakan: owner `reed-archivist`
- jika kontrak dokumen startup/runtime/routing perlu dirapikan: owner `startup-doc-maintainer`

### Wiki Canon

Masuk domain `reed-archivist` jika informasinya:
- durable
- reusable
- lintas waktu
- lebih cocok jadi pustaka daripada context boot

Jangan biarkan wiki menjadi RAM agent.

### Research

`reed-researcher` owner untuk:
- mencari
- menyusun
- membandingkan
- mensintesis sumber

Kalau output research sudah durable, handoff ke `reed-archivist` untuk promosi ke canon.

### Build

`reed-builder` owner untuk:
- implementasi
- prototipe
- script/tool baru
- technical edits

Kalau build menghasilkan pelajaran durable:
- insiden -> handoff ke `reed-archivist` untuk `Incidents`
- prosedur stabil -> handoff ke `reed-archivist` untuk `SOPs`

### Startup/Handoff Docs

`startup-doc-maintainer` owner untuk:
- file startup canonical
- file compat/stub
- aturan anti-file-baru untuk startup/handoff

Default policy:
- satu file canonical
- file lama cukup redirect/stub
- perubahan normal harus masuk file canonical, bukan membuat variasi baru

## Handoff Rules

- `main` memutuskan kapan delegasi dibutuhkan
- `reed-researcher` handoff ke `main` atau `reed-archivist` tergantung outputnya
- `reed-builder` handoff ke `main` dengan changed files, tests, dan next decision
- `reed-archivist` handoff ke `main` dengan canon/log update atau CRM update
- `startup-doc-maintainer` aktif hanya saat boundary startup/runtime/read-order/source-of-truth berubah

## Escalation Rules

- Kalau satu task menyentuh banyak domain:
  - `main` tetap owner keputusan akhir
  - worker domain mengerjakan bagian sempitnya
- Kalau ada konflik ownership:
  - ikuti dokumen ini
  - kalau masih ambigu, `main` jadi tie-breaker
- Kalau canonical file domain belum jelas:
  - jangan buat file baru dulu
  - tentukan owner domain, lalu update canonical source yang paling dekat

## Anti-Proliferation Rules

- dilarang membuat file baru bertema startup/handoff/bootstrap di root tanpa kebutuhan compat eksplisit
- dilarang menduplikasi tabel ownership ini ke banyak dokumen
- dokumen lain harus menunjuk ke SOP ini, bukan mendefinisikan ulang roster ownership penuh
- kalau butuh contoh cepat, cukup beri pointer ke section yang relevan di SOP ini

## Quick Answers

- owner memorinya Hermes: `main`
- owner Obsidian Wiki LLM: `reed-archivist`
- owner startup/handoff docs: `startup-doc-maintainer`
- owner research artifacts: `reed-researcher`
- owner build/tooling artifacts: `reed-builder`
- owner keputusan akhir lintas domain: `main`
