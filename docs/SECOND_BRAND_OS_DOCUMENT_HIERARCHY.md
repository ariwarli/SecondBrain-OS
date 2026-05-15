<!--
Tujuan: memetakan hierarchy dokumen final Second Brand OS
Caller: user, operator workspace, agent utama
Dependensi: docs/SECOND_BRAND_OS_BLUEPRINT.md, docs/AGENT_OWNERSHIP_SOP.md, docs/INBOX_ROUTING.md
Main Functions: menjelaskan dokumen mana yang jadi source of truth dan dokumen mana yang hanya turunan
Side Effects: mencegah konflik antar dokumen dan proliferasi source of truth
-->

# Second Brand OS Document Hierarchy

## Level 1 — Master Source of Truth

Dokumen di level ini menentukan arah sistem dan menang atas dokumen turunannya.

- `docs/SECOND_BRAND_OS_BLUEPRINT.md`
- `docs/AGENT_OWNERSHIP_SOP.md`
- `docs/INBOX_ROUTING.md`
- `docs/REED_RUNTIME_ARCHITECTURE.md`
- `docs/REED_MEMORY_AND_LEARNING.md`
- `docs/REED_HERMES_MIGRATION_MAP.md`
- `automation/reed-runtime-spec.yaml`

## Level 2 — Operating Contracts

Dokumen ini menerjemahkan blueprint ke aturan operasional dan penggunaan harian.

- `docs/SECOND_BRAND_OS_SOP_PER_LANE.md`
- `docs/SECOND_BRAND_OS_VISI_MISI.md`
- `docs/SECOND_BRAND_OS_ONBOARDING_MAP.md`
- `docs/TOPIC_WORKSPACE_INDEX.md`
- `docs/TOPIC_WORKSPACE_TABLE.md`
- `docs/HORMOZI_WORKSPACE_GUIDE.md`
- `docs/REED_COMMAND_RUNTIME_SOT.md`

## Level 3 — Live Operating State

Dokumen ini hidup, berubah, dan harus mengikuti aturan dari level 1–2.

- `hermes.md`
- `session-snapshot.md`
- `daily.md`
- `crm.md`
- `memory/YYYY-MM-DD.md`

## Level 4 — Domain & Work Lanes

Dokumen/folder kerja aktif.

- `brand-os/`
- `personal-brand/`
- `clients/`
- `projects/`
- `research/`
- `knowledge-base/`
- `ops/`
- `automation/`
- `wellbeing/`

## Level 5 — Historical / Legacy

Dokumen dan folder di level ini tidak boleh mengalahkan dokumen level atas.

- `archives/`
- snapshot lama
- legacy runtime docs
- generated artifacts yang sudah retired

## Legacy Merge Status

- dokumen lama dipakai sebagai referensi historis
- isi yang reusable sudah dipindah ke blueprint/SOP/index baru
- `docs/REED_HERMES_MIGRATION_MAP.md` tetap jadi jembatan transisi, bukan source of truth akhir
- archive hanya menyimpan konteks lama dan bukti evolusi

## Rule Konflik

Jika ada konflik:
1. Level 1 menang atas semua level di bawahnya.
2. Level 2 menerjemahkan Level 1, bukan menggantikannya.
3. Level 3 hanya menyimpan state hidup, bukan mengganti aturan.
4. Level 4 adalah tempat kerja, bukan penentu governance.
5. Level 5 hanya referensi historis.
