# Secondbrain Master Blueprint

## Objective
Membangun Secondbrain OS yang tidak overload, terukur, dan compounding via markdown knowledge.

## Phase 1 - Stabilize Control Plane
- Lock role per agent: `main`, `reed-archivist`, `reed-builder`, `reed-researcher`, `reed-wellbeing`.
- Lock routing topic -> owner bot (1 topic = 1 owner).
- Lock handoff protocol (`Context/Task/Deadline/Done Criteria`).
- Deliverables:
  - `docs/BOT-MATRIX.md`
  - `docs/SOP-*.md`
  - `docs/HANDOFF-PROTOCOL.md`

## Phase 2 - Obsidian-Only Memory
- Notion dinonaktifkan dari workspace aktif.
- Source of truth memory: `knowledge-base/` markdown.
- Auto checkpoint tiap 10 chat atau 15 menit per session aktif via worker + timer.
- Deliverables:
  - `knowledge-base/wiki/sessions/*.md`
  - `docs/KB-SYNC-RULES.md`

## Phase 3 - Git Sync Audited
- Setup remote private untuk knowledge repo (VPS bare repo atau GitHub private).
- Terapkan flow `pull --rebase` -> write -> `commit` -> `push`.
- Terapkan conflict runbook tanpa force push.
- Deliverables:
  - `docs/KB-CONFLICT-RUNBOOK.md`
  - SOP sync aktif dan teruji.

## Phase 4 - Knowledge Compounding
- Terapkan ingest workflow: raw source -> wiki pages -> index/log.
- Lakukan lint berkala untuk orphan/kontradiksi/outdated claims.
- Deliverables:
  - `wiki/index.md`
  - `wiki/log.md`
  - laporan lint berkala.

## Security & Privacy Guardrails
- Jangan commit secrets.
- `raw/` append-only.
- Wellbeing/personal default exclude dari repo umum kecuali approval eksplisit.

## Success Metrics
- Routing accuracy.
- Time-to-output dari inbox.
- Task aging turun.
- Checkpoint worker success rate.
- Knowledge reuse rate naik.
