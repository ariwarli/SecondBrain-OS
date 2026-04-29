<!--
Tujuan: source of truth routing Inbox Telegram ke topic dan bucket kerja Hermes
Caller: agent utama REED, subagent archivist, dan operator workspace
Dependensi: AGENTS.md, SOUL.md, hermes.md, daily.md, crm.md
Main Functions: classify inbox, route ke topic, konfirmasi balik, tentukan kapan item naik ke wiki
Side Effects: update topic kerja, daily.md, crm.md, dan knowledge-base/wiki bila item layak jadi canon
-->

# INBOX_ROUTING

Inbox adalah surface capture tercepat. Inbox bukan tempat final.

## Boundary

- `INBOX` = capture
- `tasks/content/personal-crm/ops/knowledge-base/updates` = operational destinations
- `Wiki` = canon durable

## Routing Flow

1. Classify isi pesan
2. Route ke topic kerja yang tepat
3. Reply confirmation singkat di Inbox
4. Execute task bila memang perlu aksi lanjutan
5. Naikkan ke wiki hanya jika item punya nilai reuse jangka panjang

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
Next: [action selanjutnya]
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

Jangan paksa semua isi pesan tinggal di satu topic bila fungsinya beda.

## Canon Escalation Rule

Item dari `knowledge-base` atau lane lain baru naik ke wiki jika memenuhi salah satu ini:

- `Research` = ada synthesis atau temuan reusable
- `Frameworks` = ada model pikir atau rubric
- `SOPs` = ada langkah kerja yang harus diulang konsisten
- `Decisions` = ada keputusan final yang perlu diingat
- `Incidents` = ada failure, root cause, fix, atau preventive lesson

Link mentah, PDF mentah, dan notes mentah tidak otomatis jadi canon.
