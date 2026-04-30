<!--
Tujuan: source of truth routing Inbox Telegram ke topic dan bucket kerja Hermes
Caller: agent utama REED, subagent archivist, dan operator workspace
Dependensi: AGENTS.md, SOUL.md, hermes.md, daily.md, crm.md
Main Functions: classify inbox, route ke topic, konfirmasi balik, tentukan kapan item naik ke wiki
Side Effects: update topic kerja, daily.md, crm.md, dan knowledge-base/wiki bila item layak jadi canon
-->

# INBOX_ROUTING

Inbox adalah surface capture tercepat. Inbox bukan tempat final, bukan tempat kerja aktif, dan bukan tempat recap status.

## Boundary

- `INBOX` = capture
- `tasks/content/personal-crm/ops/knowledge-base/updates` = operational destinations
- `Wiki` = canon durable
- owner routing + reply behavior di `Inbox` = `main`
- owner staging `inbox/pending`, `processed`, `unsorted` = `reed-archivist`

## Routing Flow

1. Classify isi pesan
2. Route ke topic kerja yang tepat
3. Reply confirmation singkat di Inbox
4. Lanjutkan execution dan dialog kerja hanya di topic tujuan
5. Naikkan ke wiki hanya jika item punya nilai reuse jangka panjang

Prinsip keras:
- `Inbox` hanya boleh berisi ack singkat hasil routing
- execution, clarification kerja, dan percakapan lanjutan harus pindah ke lane tujuan
- jangan gunakan `Inbox` untuk reminder management, active to-do management, atau recap progres

## Buckets

### Project

- Trigger: nama client, proyek, deliverable, revisi, brief kerja
- Route default: `tasks`
- Path default:
  - `clients/nirva/`
  - `clients/sentrachat/`
  - `clients/stop-tb/`
  - `clients/apps/`
  - `clients/appssync/`
  - `clients/pt-sin/`

### Content

- Trigger: ide post, hook, caption, thread, carousel, draft publish
- Route default: `content`
- Path default:
  - `brand-os/`
  - `personal-brand/`
- Runtime note:
  - topic Telegram `content` (`thread_id: 3`) adalah drafting lane
  - fresh turn di topic ini sekarang diarahkan ke alias runtime `speedup-brand`; jangan pakai latensi `qwen3-coder:480b` sebagai patokan lane content

### CRM

- Trigger: follow-up, relasi, meeting, kontak, deal, orang tertentu
- Route default: `personal-crm`
- File default:
  - `crm.md`

### Task

- Trigger: bikin, audit, review, fix, cek, implement, kirim
- Route default: `tasks`
- File default:
  - `daily.md`

### Knowledge

- Trigger: URL, PDF, tutorial, referensi, bookmark, bahan, insight luar
- Route default: `knowledge-base`
- Escalation:
  - tetap di operational lane bila masih mentah
  - naik ke wiki jika sudah ada synthesis, framework, keputusan, SOP, atau lesson

## Topic Map

- `inbox` = capture awal
- `tasks` = kerja aktif
- `content` = publish lane
- `personal-crm` = relasi dan follow-up
- `ops` = runtime, incident, infra
- `knowledge-base` = bahan dan knowledge work
- `updates` = brief, summary, alert

## Confirmation Format

```text
✅ [ROUTED → bucket] path/file
Next: lanjut di [lane tujuan]
```

Aturan format:
- maksimum 2 baris
- singkat saja, tanpa recap, prioritas, atau breakdown kerja
- `Next:` hanya boleh menunjuk lane tujuan, misalnya `Next: lanjut di tasks`

Contoh yang boleh:

```text
✅ [ROUTED → Task] daily.md
Next: lanjut di tasks
```

```text
✅ [ROUTED → CRM] crm.md
Next: lanjut di personal-crm
```

Tidak boleh di `Inbox`:
- recap status sekarang
- daftar to-do aktif lengkap
- penentuan prioritas awal
- pertanyaan seperti `mau mulai dari mana?`
- penjelasan panjang setelah routing
- jawaban seperti `gw cek to-do list lu hari ini`
- status seperti `belum ada yang dikerjain`
- rundown `setelah selesai nanti`

Kasus screenshot yang salah:
- jika user minta atau sistem tergoda memberi to-do list harian, status pending, atau urutan kerja, route ke `tasks`
- jika perlu diskusi `mulai dari nomor berapa`, lakukan di `tasks`
- `Inbox` tetap hanya ack singkat, misalnya:

```text
✅ [ROUTED → Task] daily.md
Next: lanjut di tasks
```

## Completion Signals

User bisa menutup loop task atau reminder dengan kata `done`.

Aturan default:
- jika user membalas reminder atau task dengan `done`, anggap item itu selesai
- jika konteks terakhir ada di `tasks`, tutup item aktif terakhir di lane `tasks`
- jika konteks terakhir ada di `personal-crm`, tutup follow-up aktif terakhir di lane `personal-crm`
- setelah `done`, jangan ulangi reminder yang sama kecuali user membuat next action baru

Fallback:
- jika ada lebih dari satu item aktif dan `done` ambigu, minta klarifikasi singkat
- jika `done` muncul di `inbox` tanpa open loop yang jelas, cari item aktif terakhir yang paling relevan
- jika tetap tidak jelas, tanya singkat sebelum menutup item

Contoh:

```text
🔔 Reminder: follow-up DEDE jam 15:00
User: done
Result: item follow-up dianggap selesai dan tidak di-remind ulang
```

```text
🔔 Reminder: revisi landing page NIRVA
User: done
Result: task aktif terakhir di `tasks` ditutup
```

## Mixed Message Rule

Satu pesan boleh dipecah menjadi lebih dari satu objek.

Contoh:
- ide ebook -> `content`
- reminder follow-up jam 15:00 -> `tasks`
- reminder meeting -> `tasks`
- to-do aktif -> `tasks`
- setup Google Calendar -> `tasks` atau `ops` sesuai intent

Jangan paksa semua isi pesan tinggal di satu topic bila fungsinya beda.

Jika satu pesan memuat banyak fungsi:
- split menjadi objek terpisah per fungsi
- route tiap objek ke lane yang tepat
- `Inbox` hanya ack hasil split/routing, bukan membahas semua objek itu satu per satu

Aturan untuk status/to-do request:
- request `cek to-do`, `status hari ini`, `apa yang pending`, `reminder meeting`, dan sejenisnya diperlakukan sebagai `Task`
- jawabannya harus muncul di `tasks`, bukan `Inbox`

## Canon Escalation Rule

Item dari `knowledge-base` atau lane lain baru naik ke wiki jika memenuhi salah satu ini:

- `Research` = ada synthesis atau temuan reusable
- `Frameworks` = ada model pikir atau rubric
- `SOPs` = ada langkah kerja yang harus diulang konsisten
- `Decisions` = ada keputusan final yang perlu diingat
- `Incidents` = ada failure, root cause, fix, atau preventive lesson

Link mentah, PDF mentah, dan notes mentah tidak otomatis jadi canon.
