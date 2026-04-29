# Scheduler Setup On VPS

Panduan ini menghubungkan blueprint scheduler ke VPS Hermes kamu.

Semua jadwal di file ini mengikuti rekomendasi NotebookLM legacy `OpenClaw` dan kondisi server kamu saat ini.

## 1. Tentukan Timezone Scheduler

Kamu punya dua opsi:

### Opsi A: Tetap pakai timezone server Singapore

Pakai file:
- `automation/crontab.sgt.example`

Kelebihan:
- tidak mengubah setting server

Kekurangan:
- semua jadwal kerja harus dipikir sebagai `WIB + 1 jam`

### Opsi B: Ubah server ke WIB

Pakai file:
- `automation/crontab.wib.example`

Kelebihan:
- jadwal cocok langsung dengan jam kerja kamu

Kekurangan:
- perlu ubah timezone server

## 2. Tentukan Runner

Runner Telegram sudah disiapkan:

- `automation/telegram_runner.py`
- `automation/run-telegram-job.sh`

Arsitektur yang dipakai:
- Hermes bot tetap bot utama
- bot kedua dipakai sebagai scheduler sender
- cron memakai bot kedua untuk post prompt ke topic yang benar

Ini lebih cocok dengan pola NotebookLM yang mendorong Telegram sebagai interface utama.

### Kenapa pakai bot kedua

Inferensi teknis:
- bot yang sama tidak sebaiknya dipakai untuk menjadwalkan pesan ke dirinya sendiri
- scheduler sender yang terpisah membuat trigger lebih jelas dan observability lebih rapi

### Yang perlu diisi

- `automation/telegram-config.json`
  - `chat_id`
  - semua `thread_id`
- `automation/telegram-runner.env`
  - `SCHEDULER_BOT_TOKEN`

Template env sudah ada di:
- `automation/telegram-runner.env.example`

### Cara ambil `chat_id` dan `thread_id`

1. Tambahkan scheduler bot ke group/topic yang sama dengan Hermes
2. Kirim pesan test manual ke tiap topic
3. Jalankan:

```bash
python3 /Users/banirisset/2_Areas/banirisset/automation/telegram_inspect_updates.py
```

4. Ambil nilai `chat_id` dan `thread_id` dari output
5. Isi ke `automation/telegram-config.json`

Kalau kena error SSL certificate verify:

Tambahkan ke `automation/telegram-runner.env`:

```bash
TELEGRAM_INSECURE_SSL=1
```

## 3. Install Crontab

Setelah runner siap:

```bash
crontab -e
```

Lalu paste salah satu:
- `automation/crontab.sgt.example`
- `automation/crontab.wib.example`

Sebelum itu:

```bash
chmod +x /Users/banirisset/2_Areas/banirisset/automation/run-telegram-job.sh
```

## 4. Verification Checklist

Checklist minimal:
- test dry run runner
- morning brief terkirim jam yang benar
- smoke check harian ada
- CRM review jalan
- content nag tidak spam
- security audit tetap jalan
- overnight subagents tidak overlap liar
- log cron ada
- log runner ada di `/home/hermes/automation/logs/`

Contoh dry run:

```bash
python3 /Users/banirisset/2_Areas/banirisset/automation/telegram_runner.py \
  --job-id morning_brief \
  --prompt-file /Users/banirisset/2_Areas/banirisset/automation/jobs/morning-brief.md \
  --thread-key updates \
  --config /Users/banirisset/2_Areas/banirisset/automation/telegram-config.json \
  --dry-run
```

## 5. Recommended Order

Urutan aktivasi yang paling aman:

1. morning brief
2. CRM review
3. end-of-day summary
4. content nag
5. heartbeat
6. overnight jobs

Jangan aktifkan overnight jobs dulu sebelum logika runner dan log-nya beres.

## 6. Non-Negotiables

- heartbeat harus silent kecuali ada issue
- overnight jobs max 3-4
- stagger 20-30 menit
- audit cost kalau job mulai membengkak
- jangan biarkan runner mengeksekusi input eksternal mentah

## 7. Log Rotation

Pasang policy ini di VPS:
- `automation/hermes-scheduler.logrotate`

Target path di VPS:
- `/etc/logrotate.d/hermes-scheduler`

Tujuan:
- rotate log harian
- simpan 14 arsip
- compress log lama

## 8. Quick Status

Untuk cek cepat di VPS:

```bash
/home/hermes/automation/scheduler-status.sh
```
