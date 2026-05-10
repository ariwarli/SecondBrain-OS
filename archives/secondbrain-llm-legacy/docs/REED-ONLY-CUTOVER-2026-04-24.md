# REED-Only Cutover — 2026-04-24

## Keputusan

Mulai sesi ini, identitas bot operasional untuk `SecondBrain OS` disederhanakan menjadi satu:

- `REED` = satu-satunya identitas bot utama
- scheduler, reminder, heartbeat, updates, dan automation = automation layer milik `REED`
- `REED DULL` = dinonaktifkan sebagai identitas operasional

## Alasan

- Menghapus dualisme antara bot utama dan bot scheduler
- Menyatukan provenance operasional agar lebih konsisten dengan pipeline memory
- Mengurangi kebingungan user di Telegram topic
- Menjaga agar jalur menuju `knowledge-base/wiki` tetap punya owner sistem yang jelas

## Perubahan Docs Dan Workspace

- Referensi `REED DULL` dibersihkan dari docs dan script utama di repo
- Wording diganti menjadi `REED`, `REED Automation`, atau `automation layer REED`
- Boundary baru:
  - `REED` = interface utama, routing, orchestration, diagnosis
  - automation REED = scheduler, reminder, heartbeat, updates, dan job terjadwal

## Perubahan Live VPS

Cutover live yang diterapkan:

- automation sender pindah dari `SCHEDULER_BOT_TOKEN` ke `TELEGRAM_BOT_TOKEN`
- `/home/openclaw/automation/telegram-config.json`
  - `token_env` -> `TELEGRAM_BOT_TOKEN`
  - `policy.system_name` -> `REED Automation`
  - `lane_contracts[*].owner` -> `REED Automation`
- `/home/openclaw/automation/telegram_runner.py`
  - validator owner legacy `REED DULL` dihapus
  - header output `RED DULL:` diganti menjadi `REED:`
- bot lama `@survivorsched_bot` keluar dari group utama
  - status akhir Telegram: `left`

## Dampak Operasional

Topic yang sekarang menerima automation via identitas `REED`:

- `updates`
- `personal-crm`
- `content`
- `tasks`
- `wellbeing`
- `ops`

## Guardrail

- automation tetap `send-only`
- automation tidak boleh mengambil alih percakapan interaktif harian
- routing utama tetap lewat REED / OpenClaw gateway
- final knowledge tetap dipromosikan terpisah via `kb_ingest_promote.py`

## Implikasi Ke Knowledge Base

Cutover ini memperjelas provenance:

- `REED` / capture layer
- `inbox/processed`
- `kb_ingest_promote.py`
- `knowledge-base/wiki`

Dengan begitu, tidak ada lagi ambiguitas bahwa ada bot kedua yang seolah menjadi producer memory paralel.

## Status

- repo docs: dibersihkan dari istilah `REED DULL`
- VPS live: sender automation sudah memakai token REED utama
- bot lama: tidak lagi aktif di group utama
