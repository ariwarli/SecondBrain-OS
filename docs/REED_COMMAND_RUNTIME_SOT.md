<!--
Tujuan: menetapkan source of truth command runtime REED untuk audit /menu, /model, dan /route-*
Caller: operator runtime, maintainer REED, auditor incident
Dependensi: automation/reed-command-compliance.yaml, docs/INBOX_ROUTING.md
Main Functions: lock canonical command handler, matrix command per topic, status compliance
Side Effects: jadi acuan audit dan hardening runtime command
-->

# REED Command Runtime Source of Truth

Dokumen ini mengunci lokasi sumber runtime command dan matrix command minimum lintas topic.

## Canonical Source

- Canonical DM command handler: `gateway/platforms/telegram.py`
- Kontrak compliance: `automation/reed-command-compliance.yaml`
- Validator:
  - `ops/scripts/reed_command_compliance.py`
  - `ops/scripts/reed_runtime.py doctor run` (termasuk check command compliance)

Jika canonical handler belum ada di workspace, status compliance harus dianggap gagal sampai handler tersedia/terhubung.

## Mandatory Command Contract

Kontrak command wajib dikelola di `automation/reed-command-compliance.yaml`:

- `/menu` harus singleton global.
- Semua topic wajib memiliki `/model`.
- Topic `inbox` wajib punya minimal satu pola `/route-*`.

## Ack Contract Alignment

Format ack inbox yang resmi tetap mengacu ke `docs/INBOX_ROUTING.md` bagian Confirmation Format.
Implementasi snapshot di `archives/system-snapshots/openclaw-archive/` dianggap referensi historis, bukan canonical runtime.
