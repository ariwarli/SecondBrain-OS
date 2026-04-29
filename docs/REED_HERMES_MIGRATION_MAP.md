<!--
Tujuan: peta konsolidasi artefak runtime lama ke runtime REED/Hermes
Caller: builder, operator, dan auditor migrasi
Dependensi: hermes.md, automation/, archives/legacy-runtime/scheduler/, ops/subagents/, docs/REED_RUNTIME_ARCHITECTURE.md
Main Functions: menentukan apa yang di-keep, di-merge, di-rewrite, dan di-retire
Side Effects: mengurangi drift dan mencegah fragmentasi runtime
-->

# REED Hermes Migration Map

Dokumen ini menjawab: artefak runtime lama yang ada sekarang harus diapakan saat REED dikonsolidasikan ke model Hermes-style.

## Keep As Transitional Source

Tetap dipakai sebagai input migrasi:
- `hermes.md`
- `automation/README.md`
- `automation/schedule.yaml`
- `automation/jobs/*.md`
- `archives/legacy-runtime/scheduler/scripts/*.py`
- `ops/subagents/README.md`
- `docs/INBOX_ROUTING.md`

Alasan:
- artefak ini sudah memuat ritme kerja, cadence, topic map, reminder flow, dan roster worker

## Rewrite Into Canonical REED Runtime

Harus diubah menjadi bentuk runtime REED yang baru:

### Scheduler / Cron
- `automation/schedule.yaml`
  - dari blueprint lama menjadi source-of-truth cron spec REED
- `archives/legacy-runtime/scheduler/queue`, `archives/legacy-runtime/scheduler/archive`, `archives/legacy-runtime/scheduler/tracking`
  - dari direktori helper menjadi bagian dari unified scheduler subsystem

### Subagents
- `ops/subagents/README.md`
  - dari roster lama menjadi REED worker contract

### Runtime Brain
- `hermes.md`
  - dari startup brain utama menjadi compat/transitional state file
  - state arsitektur target pindah ke `docs/REED_RUNTIME_ARCHITECTURE.md`

## Merge Rules

- `REED DULL` concept -> merge into internal scheduler subsystem
- `content nag`, `heartbeat`, `crm review`, `end-of-day summary` -> merge into unified cron service
- reminder checker + accountability + model health -> merge under observability/scheduler health
- Notebook-derived SOP fragments -> convert into skills or runtime docs, bukan dibiarkan sebagai blueprint lepas

## Retire Rules

Harus dianggap retired pada target state:
- model mental “scheduler bot = sistem terpisah”
- cron examples sebagai final implementation
- state penting yang hanya hidup di satu dokumen naratif tanpa spec

## Mapping Table

| Current artifact | Future REED home | Action |
| --- | --- | --- |
| `hermes.md` | compat state + migration note | Keep, narrow scope |
| `automation/schedule.yaml` | `automation/reed-runtime-spec.yaml` | Merge/replace |
| `automation/jobs/*.md` | skills or cron prompts | Reclassify |
| `archives/legacy-runtime/scheduler/scripts/*.py` | scheduler subsystem | Port or rewrite |
| `ops/subagents/README.md` | worker contract | Rewrite |
| `docs/INBOX_ROUTING.md` | keep | Preserve and extend |
| `knowledge-base/wiki/` | canon library | Keep |

## Migration Sequence

1. Establish REED runtime docs and spec
2. Re-anchor memory ownership and canon promotion
3. Unify cron/scheduler contracts
4. Convert reusable procedures into skills
5. Collapse sidecar concepts into one runtime model
6. Only then update or replace implementation scripts/services
