<!--
Tujuan: setup satu file env runtime untuk REED health checks
Caller: operator runtime, maintainer REED
Dependensi: ops/reed_runtime/env.py, ops/scripts/reed_runtime.py, ops/scripts/model_routing_guardrail.py, ops/scripts/model_routing_smoke.py
Main Functions: menentukan lokasi .env runtime dan cara pemakaian tanpa inject manual
Side Effects: menyederhanakan eksekusi doctor/guardrail/smoke/status
-->

# Runtime Env Setup

REED runtime sekarang membaca env otomatis dari:

- primary: `state/reed-runtime/.env`
- fallback: `.env` di root workspace

## Minimal variables

```env
NINE_ROUTER_BASE_URL=http://100.113.246.119:20128/v1
NINE_ROUTER_API_KEY=...
TELEGRAM_BOT_TOKEN=...
```

## Perintah (tanpa inject manual)

- `python3 ops/scripts/reed_runtime.py status`
- `python3 ops/scripts/reed_runtime.py doctor run`
- `python3 ops/scripts/model_routing_guardrail.py`
- `python3 ops/scripts/model_routing_smoke.py`
- `python3 ops/scripts/reed_runtime_health_evidence.py`
- `python3 ops/scripts/sync_reed_dm_menu.py` (force DM menu launcher-only `/menu`)
