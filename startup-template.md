# Startup Template

File ini berisi aturan permanen untuk memulai sesi baru dengan agent kosong.
Untuk konteks sesi terkini, baca `session-snapshot.md` setelah file ini.

## Working Directory

Set `cwd` / home agent ke:

`/Users/banirisset/2_Areas/banirisset`

## Read Order

Baca file berikut secara berurutan:

1. `AGENTS.md`
2. `SOUL.md`
3. `USER.md`
4. `hermes.md`
5. `daily.md`
6. `memory/YYYY-MM-DD.md` untuk hari ini dan kemarin
7. `knowledge-base/wiki/index.md`
8. `knowledge-base/wiki/log.md`
9. `knowledge-base/wiki/sessions/*-active.md` jika ada dan relevan

Lalu baca `session-snapshot.md` untuk konteks sesi terkini.

## Optional Stronger Handoff

Kalau butuh konteks sesi yang lebih kuat, baca juga:

- `core/session-handoff-prompt-gemini.md`
- `crm.md`

## Core Boundary Model

Jangan campur tiga lapis ini:

- `INBOX` = intake layer only
- `Hermes` = working / operational memory
- `Wiki` = canonical knowledge layer

Rules:
- Jangan jadikan `INBOX` sebagai final bucket
- Jangan biarkan `Hermes` menjadi wiki
- Jangan biarkan `Wiki` menjadi agent RAM

## Routing Rules

Incoming Telegram capture masuk melalui `INBOX`, lalu route ke lane tujuan.

`INBOX` adalah ack-only:
- maksimum 2 baris singkat
- tidak ada status recap
- tidak ada to-do list lengkap
- tidak ada prioritisasi
- tidak ada dialog kerja lanjutan
- tidak ada pertanyaan seperti `mau mulai dari mana?`

Lane tujuan operasional:
- `tasks`
- `content`
- `personal-crm`
- `ops`
- `knowledge-base`
- `updates`

Jika satu pesan mengandung beberapa fungsi, split ke lane yang tepat.

Contoh:
- ide untuk ebook → `content`
- reminder jam 15:00 → `tasks`

Jika user minta:
- to-do list hari ini
- status kerja / pending items
- reminders
- mulai dari mana

Anggap sebagai `tasks`. Di `INBOX` hanya ack routing singkat, lalu lanjut di `tasks`.

## Workspace Conventions

- Workspace ini adalah home operasional Hermes/REED.
- `memory/` = log kontinuitas harian.
- `knowledge-base/wiki/` = canon durable.
- Canon bucket resmi: `Research`, `Frameworks`, `SOPs`, `Decisions`, `Incidents`.
- `Sources` bukan bucket canon utama.