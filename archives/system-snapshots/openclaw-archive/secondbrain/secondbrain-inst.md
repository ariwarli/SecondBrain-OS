# SecondBrain OS Instruction Manual

Panduan ini menjelaskan cara pakai group Telegram `SecondBrain OS` sebagai operating system harian untuk OpenClaw.

Panduan ini mengikuti arah dari NotebookLM `OpenClaw`:
- Telegram sebagai interface utama
- topic routing biar context tidak campur
- REED sebagai chief of staff utama
- REED DULL sebagai scheduler/automation layer

Dokumen pendamping:
- `secondbrain-sop.md` untuk SOP harian pagi/siang/sore
- `secondbrain-cheatsheet.md` untuk versi 1 halaman
- `secondbrain-prompts.md` untuk prompt siap pakai
- `secondbrain-ops-playbook.md` untuk incident handling

## Identitas Bot

- `@survivorset_bot` = **REED**
  - bot utama
  - dipakai untuk brainstorming, planning, drafting, delegasi, dan eksekusi

- `@survivorsched_bot` = **REED DULL**
  - bot scheduler
  - dipakai untuk cron, alert, heartbeat, dan job terjadwal
  - bukan bot utama untuk kerja harian

## Aturan Inti

- kerja utama dilakukan di group `SecondBrain OS`
- gunakan topic yang tepat, jangan campur semua hal ke satu thread
- default: tulis biasa tanpa mention
- kalau REED tidak merespons atau kamu ingin memastikan dia kepanggil, mention `@survivorset_bot`
- jangan pakai `@survivorsched_bot` untuk brainstorming atau kerja harian
- `@survivorsched_bot` hanya untuk scheduler test / alert / automation

## Kapan Harus Mention

### Tidak perlu mention

Kalau REED respons normal, cukup kirim pesan biasa di topic yang benar.

Contoh:
```text
Riset 5 competitor agency AI lokal dan ringkas positioning mereka.
```

### Mention REED

Kalau:
- REED tidak respons
- kamu ingin memastikan bot utama yang menangani
- prompt penting dan kamu ingin eksplisit

Contoh:
```text
@survivorset_bot Bantu brainstorm 10 angle offer baru buat agency AI gw.
```

### Mention REED DULL

Hanya untuk:
- test scheduler
- test topic ID
- alert path

Contoh:
```text
@survivorsched_bot ops ping
```

## Struktur Topic

### `updates`

Fungsi:
- morning brief
- end-of-day summary
- hasil overnight
- heartbeat ringkas

Jangan pakai untuk:
- brainstorming panjang
- task dump

Contoh:
- baca morning brief
- minta ringkasan status

### `inbox`

Fungsi:
- ide mentah
- voice note
- catatan cepat
- random brain dump

Pakai saat:
- kamu belum tahu ide itu harus jadi task, content, atau CRM

Contoh:
```text
Gw kepikiran bikin offer AI audit untuk UKM, tapi belum jelas packaging-nya.
```

### `tasks`

Fungsi:
- kerja konkret
- delegasi
- task yang perlu output nyata

Pakai saat:
- kamu mau REED benar-benar ngerjain sesuatu

Contoh:
```text
@survivorset_bot Audit 5 competitor AI agency di Indonesia. Ringkas pricing, positioning, dan peluang diferensiasi.
```

### `personal-crm`

Fungsi:
- follow-up
- relasi
- outreach
- stale contacts

Contoh:
```text
@survivorset_bot Siapa yang overdue follow-up minggu ini? Draft pesan singkatnya.
```

### `content`

Fungsi:
- ide konten
- hook
- outline
- repurpose
- content nagger

Contoh:
```text
@survivorset_bot Ubah ide ini jadi 3 hook LinkedIn dan 1 outline carousel.
```

### `ops`

Fungsi:
- error
- audit
- logs
- smoke-check alert
- hal teknis

Contoh:
```text
@survivorset_bot Cek kenapa morning brief hari ini tidak masuk.
```

### `knowledge-base`

Fungsi:
- bahan masuk
- referensi
- URL
- PDF
- materi yang nanti dipakai untuk kerja

Contoh:
```text
Simpan referensi ini. Ambil insight yang paling relevan buat positioning gw.
```

## Use Case Nyata

### 1. Pagi hari

Masuk ke `updates`.

Lakukan:
1. baca morning brief
2. pilih 3 prioritas
3. kalau ada kerja berat, kirim ke `tasks`

### 2. Lagi jalan / kepikiran ide

Masuk ke `inbox`.

Kirim:
- voice note
- ide mentah
- pertanyaan singkat

Lalu nanti minta REED ubah jadi:
- task
- konten
- note

### 3. Mau brainstorming

Gunakan:
- `inbox` kalau masih mentah
- `tasks` kalau brainstorming-nya sudah diarahkan ke output kerja
- `content` kalau brainstorming konten

Contoh:
```text
@survivorset_bot Bantu brainstorm 10 angle positioning untuk offer AI ops gw. Jangan ngarang data internet.
```

### 4. Mau riset atau eksekusi

Masuk ke `tasks`.

Contoh:
```text
@survivorset_bot Bikin plan eksekusi 5 langkah untuk meluncurkan offer ini minggu depan.
```

### 5. Mau follow-up orang

Masuk ke `personal-crm`.

Contoh:
```text
@survivorset_bot Dari semua kontak aktif, siapa yang paling dekat ke revenue dalam 30 hari?
```

### 6. Mau bikin konten

Masuk ke `content`.

Contoh:
```text
@survivorset_bot Ubah insight ini jadi 1 post LinkedIn, 1 thread, dan 3 hook pendek.
```

### 7. Ada error / curiga scheduler mati

Masuk ke `ops`.

Contoh:
```text
@survivorset_bot Cek health scheduler dan kasih tahu kalau ada job yang gagal.
```

## Brainstorming Tanpa Web

Kalau REED tidak punya akses live web/search, tetap bisa dipakai untuk:
- ideation
- framing
- messaging
- breakdown plan
- hypothesis generation

Cara prompt yang benar:
```text
@survivorset_bot Brainstorm 10 angle offer baru berdasarkan konteks yang kamu sudah tahu. Tandai bagian yang masih asumsi.
```

Kalau topik butuh data terbaru:
```text
@survivorset_bot Gue butuh competitor research terbaru. Dari konteks yang ada dulu, bikin hipotesis dan research plan. Jangan pura-pura punya data live.
```

## Ritme Harian yang Disarankan

### Pagi
- buka `updates`
- pilih 3 prioritas
- lempar kerja utama ke `tasks`

### Siang
- semua ide masuk `inbox`
- semua kerja >10 menit masuk `tasks`
- follow-up orang di `personal-crm`

### Sore
- baca ringkasan di `updates`
- tentukan carry-over ke besok

### Malam
- overnight jobs jalan otomatis
- hasil kembali ke `updates` / topic terkait

## Scheduler dan Automasi

Scheduler berjalan 24/7 di VPS, bukan di Mac.

Fakta penting:
- host: `DeepThree`
- user: `openclaw`
- path: `/home/openclaw/automation`
- logs: `/home/openclaw/automation/logs`
- quick status: `/home/openclaw/automation/scheduler-status.sh`

Job penting yang aktif:
- morning brief
- CRM review
- content nag
- heartbeats
- end-of-day summary
- overnight jobs
- smoke-check harian

## Topic Mapping

- Group: `SecondBrain OS`
- chat_id: `-1003344368011`
- `updates`: `13`
- `inbox`: `11`
- `tasks`: `10`
- `personal-crm`: `9`
- `content`: `3`
- `ops`: `27`
- `knowledge-base`: `16`

## Quick Rules

- kerja utama = group
- REED = `@survivorset_bot`
- REED DULL = `@survivorsched_bot`
- default tanpa mention
- mention REED kalau perlu eksplisit
- jangan kerja harian lewat REED DULL
- `inbox` untuk ide mentah
- `tasks` untuk kerja konkret
- `updates` untuk baca hasil
- `ops` untuk error dan alert

## Contoh Prompt Siap Pakai

### Inbox
```text
Ubah dump ini jadi task, content idea, dan follow-up.
```

### Tasks
```text
@survivorset_bot Bikin plan eksekusi paling sederhana untuk goal ini. Maksimal 5 langkah.
```

### Personal CRM
```text
@survivorset_bot Draft follow-up singkat untuk kontak ini. Tone hangat dan langsung.
```

### Content
```text
@survivorset_bot Ubah ide ini jadi 3 hook, 1 outline, dan CTA yang kuat.
```

### Ops
```text
@survivorset_bot Cek log scheduler dan kasih root cause kalau ada job yang gagal.
```
