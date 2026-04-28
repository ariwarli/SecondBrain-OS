# REED Ops Scripts

Script di folder ini adalah entrypoint operasional untuk runtime REED.

## `reed_runtime.py`

CLI fondasi runtime REED untuk:
- cek status runtime
- lihat registry cron
- inisialisasi / tick scheduler
- run / pause / resume job
- cek approval policy
- jalankan doctor / health checks
- kelola operational memory
- kelola session recall
- baca audit trail

Contoh:

```bash
python3 ops/scripts/reed_runtime.py status
python3 ops/scripts/reed_runtime.py cron state
python3 ops/scripts/reed_runtime.py cron tick
python3 ops/scripts/reed_runtime.py approvals check --action-name public_posting
python3 ops/scripts/reed_runtime.py doctor run
python3 ops/scripts/reed_runtime.py memory list --target operational
python3 ops/scripts/reed_runtime.py recall search --query reminder
python3 ops/scripts/reed_runtime.py audit tail --limit 20
```

Dry-run scheduler job:

```bash
TELEGRAM_RUNNER_DRY_RUN=1 python3 ops/scripts/reed_runtime.py cron run --job-id morning_brief
```

## Script Legacy

- `set_reminder.sh`
  - helper lama untuk one-shot reminder via Telegram scheduler
- `sync-brand-docs.sh`
  - helper sync dokumen brand lama
- `setup-workspace.sh`
  - bootstrap folder legacy

Script legacy tetap ada untuk kompatibilitas, tapi arah runtime baru harus masuk lewat `reed_runtime.py` dan package `ops/reed_runtime/`.

## Systemd Templates

Template install awal untuk VPS ada di:
- `ops/templates/reed-runtime-tick.service`
- `ops/templates/reed-runtime-tick.timer`

Fungsinya menjalankan `cron tick` setiap menit sampai gateway scheduler REED benar-benar menyatu penuh.
