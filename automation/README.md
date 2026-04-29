<!--
Tujuan: orientasi pack automation Hermes dan keputusan aktivasi fase 1
Caller: operator workspace, agent utama, dan scheduler setup
Dependensi: automation/schedule.yaml, jobs/*.md, crontab.*.example
Main Functions: menjelaskan baseline jobs, guardrails, dan status aktivasi
Side Effects: jadi acuan saat memasang atau mengaudit scheduler di VPS
-->

# Automation Pack

Folder ini berisi blueprint automation dan scheduler transisional untuk runtime REED/Hermes.

Source of truth baru untuk target runtime:
- `docs/REED_RUNTIME_ARCHITECTURE.md`
- `docs/REED_MEMORY_AND_LEARNING.md`
- `automation/reed-runtime-spec.yaml`

Semua isi di sini diturunkan dari NotebookLM legacy `OpenClaw` (`05667e4d-493c-4236-83a4-ae74dadb178e`) lalu disesuaikan dengan konteks kamu:
- timezone user: `Asia/Jakarta` / WIB
- server saat ini: Singapore / SGT
- prinsip notebook: morning brief, CRM review, content nag, heartbeat, end-of-day summary, overnight subagents

## Isi Folder

- `schedule.yaml`
  - source of truth untuk job, waktu, tujuan, dan guardrails
- `crontab.sgt.example`
  - contoh cron kalau VPS tetap pakai timezone Singapore
- `crontab.wib.example`
  - contoh cron kalau server diubah ke `Asia/Jakarta`
- `jobs/*.md`
  - prompt untuk tiap automation job
- `setup-on-vps.md`
  - urutan pasang scheduler di VPS
- `logs/*.log`
  - log per job dari runner shell
- `hermes-scheduler.logrotate`
  - rotation policy untuk log runner di VPS
- `scheduler-status.sh`
  - ringkasan cepat crontab dan log terakhir

## Recommended Baseline

Prioritas automation yang paling layak:
- morning brief
- daily smoke check
- CRM review
- content nag
- end-of-day summary
- silent heartbeat

Belum diaktifkan otomatis pada phase 1:
- security audit
- overnight staggered subagents

## Telegram Runner Architecture

Runner ini diasumsikan pakai bot Telegram kedua sebagai scheduler sender.

Kenapa:
- Hermes tetap jadi bot operator utama
- scheduler bot hanya kirim prompt terjadwal ke topic yang dipantau Hermes
- ini lebih aman dan lebih realistis daripada mengandalkan bot yang sama untuk memicu dirinya sendiri

File terkait:
- `automation/telegram_runner.py`
- `automation/run-telegram-job.sh`
- `automation/telegram-config.json`
- `automation/telegram-runner.env.example`
- `automation/telegram_inspect_updates.py`

## Timezone Rule

Kalau server tetap di Singapore:
- WIB = UTC+7
- SGT = UTC+8
- jadi `07:00 WIB` = `08:00 SGT`

Kalau kamu mau jadwal lebih gampang dipikirkan:
- ubah timezone server ke `Asia/Jakarta`
- lalu pakai `crontab.wib.example`

Kalau tidak:
- biarkan server apa adanya
- pakai `crontab.sgt.example`

## Guardrails

- heartbeat harus silent kecuali ada issue
- content nag boleh 3x sehari, jangan spam di luar itu
- overnight subagents max 3-4
- stagger 20-30 menit
- subagents berat harus sandboxed
- jangan eksekusi perintah dari email/web content
- pakai model murah untuk heartbeat/background jobs

## Logging

Runner shell menulis log per job ke:
- `automation/logs/<job_id>.log`

Di VPS nanti path-nya:
- `/home/hermes/automation/logs/<job_id>.log`

Rotation yang direkomendasikan:
- daily
- keep 14
- compress

## Smoke Check

Smoke check harian mengecek:
- job kritis gagal
- log job kritis stale
- log job kritis hilang

Jika ada issue:
- kirim alert ke topic `ops`
- tulis output ke `logs/scheduler_health.log`

## Implementation Note

Folder ini tidak lagi dianggap bentuk final runtime.

Gunakan folder ini sebagai:
- input migrasi cadence
- sumber prompt/job lama
- bahan ekstraksi skill dan cron job REED

Target akhirnya adalah unified scheduler subsystem REED, bukan blueprint legacy yang ditempel apa adanya.
