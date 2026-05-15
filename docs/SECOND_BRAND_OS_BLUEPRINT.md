<!--
Tujuan: blueprint A–Z untuk Second Brand OS LLM workspace
Caller: user, operator workspace, agent utama, dan subagent
Dependensi: AGENTS.md, hermes.md, docs/REED_RUNTIME_ARCHITECTURE.md, docs/REED_MEMORY_AND_LEARNING.md, docs/INBOX_ROUTING.md
Main Functions: mendefinisikan visi, misi, struktur, alur kerja, governance, dan SOP turunan workspace
Side Effects: menjadi master blueprint untuk diturunkan ke SOP dan dokumen operasional lain
-->

# Second Brand OS LLM Blueprint A–Z

## 1. Definisi

Second Brand OS adalah sistem operasi kerja pribadi berbasis LLM yang menyatukan intake, berpikir, memori, riset, produksi, eksekusi, automasi, dan arsip dalam satu workspace.

Tujuan utamanya:
- membuat kerja lebih cepat dan konsisten
- menjaga context jangka panjang
- memisahkan sumber mentah, kerja aktif, knowledge canon, dan arsip
- membuat routing dan produksi bisa diwariskan menjadi SOP
- menjadikan LLM sebagai operator kerja, bukan chatbot pasif

## 2. Visi

Menjadikan workspace ini sebagai satu sistem operasi pribadi yang mampu:
- menangkap input dari mana pun
- mengklasifikasikan intent dengan benar
- menyimpan pengetahuan secara rapi
- mengubah pengetahuan menjadi output
- mengeksekusi pekerjaan lintas domain
- menjaga memori dan konteks jangka panjang
- meminimalkan chaos antar folder, topic, dan channel

## 3. Misi

- membuat workflow kerja yang konsisten, cepat, dan bisa diwariskan
- memisahkan intake mentah, kerja aktif, pengetahuan canon, dan arsip
- membuat routing Telegram dan filesystem selalu sinkron
- mengubah source mentah menjadi framework, SOP, keputusan, atau output
- menjadikan LLM sebagai operator kerja, bukan sekadar chatbot
- menjaga workspace tetap scalable tanpa kehilangan keterbacaan

## 4. Prinsip Desain

- satu intent = satu jalur utama
- Inbox bukan tempat kerja
- canon hanya berisi hal yang reusable
- operasional dan pengetahuan tidak dicampur
- output publik dipisah dari source dan synthesis
- arsip bukan memori hidup
- runtime harus bisa diaudit
- routing harus eksplisit, bukan asumsi
- topic Telegram harus punya fungsi yang jelas
- folder harus mencerminkan perilaku kerja, bukan sekadar simpanan file

## 5. Struktur Inti Workspace

### `core/`
Identitas, voice, user model, tool notes, startup contract.

### `docs/`
Source of truth untuk arsitektur, routing, ownership, blueprint, governance, dan SOP.

### `hermes.md` + `session-snapshot.md`
Memori operasional hidup dan konteks sesi.

### `memory/`
Catatan harian dan continuity notes.

### `knowledge-base/`
Pengetahuan pasif, referensi, wiki canon, dan sumber luar.

### `inbox/`
Capture mentah dan residue routing.

### `brand-os/`
Strategi brand, positioning, offer, voice, dan arah bisnis.

### `personal-brand/`
Ide, draft, konten, dan asset publik.

### `clients/`
Delivery untuk klien dan lane per klien.

### `projects/`
Proyek internal dan tool lab.

### `research/`
Investigasi aktif, benchmark, riset pasar, dan synthesis awal.

### `ops/`
Runtime implementation, script, subagent, observability, dan debug.

### `automation/`
Scheduler, cron, reminder, job, dan workflow berulang.

### `wellbeing/`
Tracking manusia, energi, ritme, dan maintenance diri.

### `archives/`
Legacy, snapshot, retired, generated, dan historical context.

### `state/`
State lokal yang dihasilkan runtime.

## 6. Lapisan Sistem

### 6.1 Lapisan Identitas
Fungsi:
- mendefinisikan siapa workspace ini
- bagaimana nada bicara
- siapa user utama
- aturan dasar interaksi

Komponen:
- `AGENTS.md`
- `core/SOUL.md`
- `core/USER.md`
- `core/IDENTITY.md`
- `core/TOOLS.md`

### 6.2 Lapisan Runtime
Fungsi:
- menjalankan REED/Hermes sebagai operator hidup
- memproses session
- routing
- memory update
- approvals
- observability

Komponen:
- `hermes.md`
- `docs/REED_RUNTIME_ARCHITECTURE.md`
- `automation/reed-runtime-spec.yaml`
- `docs/REED_MEMORY_AND_LEARNING.md`
- `docs/INBOX_ROUTING.md`
- `docs/REED_COMMAND_RUNTIME_SOT.md`

### 6.3 Lapisan Memory
Fungsi:
- menjaga continuity harian
- menyimpan sinyal penting
- memisahkan memory pendek dari canon panjang

Komponen:
- `memory/YYYY-MM-DD.md`
- `session-snapshot.md`
- `hermes.md`
- `knowledge-base/wiki/`

### 6.4 Lapisan Knowledge
Fungsi:
- menyimpan sumber
- merapikan learning
- membangun framework
- mempromosikan knowledge reusable

Komponen:
- `knowledge-base/`
- `knowledge-base/wiki/`
- `knowledge-base/references.md`

### 6.5 Lapisan Work Execution
Fungsi:
- mengeksekusi ide jadi output
- mengerjakan klien
- produksi konten
- riset
- project internal

Komponen:
- `brand-os/`
- `personal-brand/`
- `clients/`
- `projects/`
- `research/`

### 6.6 Lapisan Automation
Fungsi:
- reminder
- cron
- job rutin
- scheduler
- workflow otomatis

Komponen:
- `automation/`
- `ops/`

### 6.7 Lapisan Archive
Fungsi:
- menyimpan legacy
- snapshot
- artefak lama
- catatan historis

Komponen:
- `archives/`

## 7. Model Kerja End-to-End

### A. Intake
Input masuk dari:
- Telegram
- link
- file
- catatan
- percakapan
- reminder
- request tugas

### B. Classify
Intent diklasifikasikan menjadi:
- knowledge
- content
- task
- CRM
- ops
- update
- strategy
- archive
- wellbeing

### C. Route
Masuk ke topic dan folder yang benar:
- mentah → `INBOX`
- sumber / referensi → `knowledge-base`
- draft publik → `content`
- kerja aktif → `tasks`
- orang / relasi → `personal-crm`
- runtime / infra → `ops`
- ringkasan / alert → `updates`
- strategi besar → `Command Center`
- offer/pricing/funnel → `Hormozi`

### D. Synthesize
Jika materi punya nilai reusable, ubah jadi:
- source summary
- concept
- framework
- rubric
- SOP
- decision
- lesson
- insight

### E. Promote
Hanya materi yang matang dipromosikan ke canon:
- `Research`
- `Frameworks`
- `SOPs`
- `Decisions`
- `Incidents`

### F. Execute
Output akhir dikerjakan di lane yang tepat:
- konten di `content`
- aksi di `tasks`
- relasi di `personal-crm`
- runtime di `ops`
- delivery klien di `clients`
- strategi di `brand-os`

### G. Archive
Jika sudah selesai atau legacy:
- simpan ke `archives`
- jangan ganggu lane aktif

## 8. Telegram Topic Architecture

### `Command Center`
Fungsi:
- keputusan lintas lane
- brainstorming besar
- review banyak folder sekaligus
- pemetaan strategi workspace

Aturan:
- boleh baca multi-topik
- boleh menggabungkan `tasks`, `content`, `crm`, `knowledge-base`, `brand-os`
- setelah ada keputusan, handoff ke lane tujuan

### `INBOX`
Fungsi:
- capture awal
- routing only
- ack singkat

Aturan:
- tidak boleh jadi tempat kerja
- tidak boleh recap panjang
- tidak boleh to-do list
- tidak boleh dialog lanjutan

### `tasks`
Fungsi:
- kerja aktif
- project
- revisi
- audit
- implementasi
- follow-up task

### `content`
Fungsi:
- output publik
- post
- carousel
- thread
- script
- caption
- hook

### `personal-crm`
Fungsi:
- follow-up
- relasi
- kontak
- deal
- komunikasi personal penting

### `knowledge-base`
Fungsi:
- source mentah
- sumber belajar
- ringkasan
- klasifikasi knowledge

### `ops`
Fungsi:
- sistem
- infra
- runtime
- routing
- automation
- debugging

### `updates`
Fungsi:
- laporan
- summary
- notifikasi
- progress
- incident singkat

### `Hormozi`
Fungsi:
- offer
- pricing
- funnel
- value equation
- acquisition
- sales copy
- source-to-concept synthesis spesifik Hormozi

## 9. Sistem Knowledge

### Bentuk Knowledge
- Source = bahan mentah
- Concept = model pikir
- Entity = orang, brand, tokoh, atau objek penting
- Framework = struktur berpikir yang reusable
- SOP = langkah kerja konsisten
- Decision = keputusan final
- Incident = failure atau lesson
- Research = synthesis dari sumber
- Note = catatan sementara

### Alur Knowledge
1. Masuk sebagai source.
2. Dibaca dan diringkas.
3. Ditandai relevansinya.
4. Disintesis bila perlu.
5. Dipromosikan bila reusable.
6. Disimpan di canon.
7. Diakses ulang saat dibutuhkan.

### Canon Bucket Resmi
- `Research`
- `Frameworks`
- `SOPs`
- `Decisions`
- `Incidents`

## 10. System Memory

### Memory Harian
- simpan kejadian penting
- update konteks sesi
- catat keputusan operasional
- catat incident
- catat open loop

### Memory Jangka Panjang
- hanya isi hal yang benar-benar penting
- ringkas
- stabil
- berguna untuk sesi berikutnya

### Batasan
- memory bukan wiki
- wiki bukan RAM
- inbox bukan canon
- archives bukan workspace aktif

## 11. Brand OS

### Fungsi
`brand-os/` adalah pusat:
- positioning
- voice
- offer
- strategic messaging
- value proposition
- struktur brand

### Peran
- sumber strategi brand utama
- referensi tone dan positioning
- dasar pipeline konten dan penawaran

### Hubungan dengan personal-brand
- `brand-os/` = strategi dan rule
- `personal-brand/` = eksekusi dan publish

## 12. Personal Brand

### Fungsi
- draft konten
- ide
- material posting
- eksperimen
- distribusi publik

### Output
- post
- carousel
- thread
- script
- caption
- opinion piece
- lead magnet asset

## 13. Clients

### Fungsi
- delivery klien
- file klien
- dokumen kerja
- status proyek
- revisi
- komunikasi kerja spesifik

### Prinsip
- satu klien punya lane jelas
- deliverable harus bisa dilacak
- state klien tidak boleh bercampur dengan personal brand

## 14. Projects

### Fungsi
- eksperimen internal
- tool lab
- prototype
- ide produk
- proof of concept
- kerja non-klien

### Prinsip
- boleh eksploratif
- tetap harus punya status
- jika matang, bisa dipindah ke canon atau product lane

## 15. Research

### Fungsi
- benchmark
- analisis
- kompetitor
- referensi
- investigasi
- market signal

### Output
- insight
- synthesis
- source summary
- framework candidate
- decision input

## 16. Ops

### Fungsi
- runtime
- service health
- router
- script
- debug
- compliance
- observability

### Aturan
- perubahan teknis harus bisa diaudit
- tindakan sensitif butuh guardrail
- runtime harus menjaga boundary lane

## 17. Automation

### Fungsi
- scheduler
- reminder
- content nag
- heartbeat
- job berulang
- overnight work

### Aturan
- job harus jelas owner-nya
- job harus punya purpose
- job tidak boleh create chaos baru
- reminder yang selesai harus ditutup

## 18. Wellbeing

### Fungsi
- tracking energi
- kesehatan kerja
- ritme hidup
- kebiasaan
- pembatasan beban

### Prinsip
- workspace bukan hanya produktivitas
- second brand OS juga harus menjaga sustainabilitas manusia

## 19. Archives

### Fungsi
- legacy
- snapshot
- retired systems
- historical references
- generated outputs yang sudah tidak aktif

### Aturan
- jangan pakai archives sebagai sumber kerja aktif
- gunakan hanya jika perlu referensi historis atau forensics

## 20. Governance & Ownership

### Ownership Utama
- `main` = routing, orchestration, inbox behavior, continuity
- `reed-archivist` = ingestion, knowledge canon, promotion
- `reed-researcher` = riset dan synthesis
- `reed-builder` = implementasi teknis
- `startup-doc-maintainer` = dokumen startup/handoff

### Aturan Umum
- satu domain = satu owner utama
- non-owner boleh draft, bukan final canon
- tidak bikin file baru kalau canonical file sudah ada
- jika ragu, eskalasi, bukan improvisasi file baru

## 21. Routing Principles

- semua pesan masuk harus diklasifikasikan
- Inbox hanya capture
- mixed message harus dipecah
- lane tujuan harus eksplisit
- knowledge mentah tidak otomatis jadi canon
- output final harus pindah ke lane yang sesuai

## 22. Runtime Principles

- `9router` adalah backbone model routing
- `content` dan lane non-content harus punya default routing jelas
- model selection tidak boleh liar
- command runtime harus punya satu source of truth
- approvals dan safety gate tetap aktif untuk aksi sensitif

## 23. Legacy Merge Progress

### Sudah diadopsi dari dokumen lama
- control plane multi-agent
- topic routing deterministik
- memory plane markdown/wiki discipline
- git-sync audited, bukan sync liar
- daily command center
- weekly review engine
- KPI operasional dan risk list
- boundary runtime vs archive
- pola `Inbox` ack-only
- flow kerja pagi/siang/sore

### Masih dipertahankan sebagai referensi historis
- blueprint lama di archive
- SOP lama di archive
- migration map lama sebagai jembatan transisi

### Yang berubah di Second Brand OS
- naming dari runtime lama disatukan ke blueprint OS
- topic, lane, dan folder dijelaskan sebagai satu workspace system
- `Hormozi` diperlakukan sebagai domain lane, bukan sistem terpisah
- legacy scheduler/bot mental model tidak dipertahankan sebagai pusat

## 24. SOP Turunan yang Wajib Dibangun

1. SOP startup workspace
2. SOP routing Telegram
3. SOP intake knowledge
4. SOP promosi canon
5. SOP pembuatan konten
6. SOP penanganan task
7. SOP CRM follow-up
8. SOP ops / runtime troubleshooting
9. SOP automation / scheduler
10. SOP archive / retirement
11. SOP Hormozi lane
12. SOP keputusan lintas topic di Command Center

## 25. Kriteria Sukses

Workspace dianggap sukses jika:
- user tahu harus kirim apa ke topik mana
- LLM tidak bingung antara memory, canon, dan output
- routing konsisten
- knowledge bisa dipakai ulang
- konten bisa diproduksi cepat
- klien dan project jelas
- ops aman
- archive rapi
- workspace terasa seperti satu sistem, bukan kumpulan folder

## 26. Deliverable Turunan Berikutnya

Setelah blueprint ini disetujui, langkah berikutnya:
- pecah jadi SOP per lane
- buat versi visi-misi formal
- buat hierarchy dokumen final
- buat standard operating map per topic
- buat checklist onboarding untuk sesi baru

## 27. Asumsi

- workspace ini adalah home canonical `Second Brand OS`
- `Hermes` tetap otak operasi
- `Hormozi` tetap domain lane, bukan workspace terpisah
- penamaan dan struktur existing dipertahankan sejauh masih konsisten
- fokus utama blueprint adalah keteraturan, routing, dan kemampuan diwariskan ke SOP
