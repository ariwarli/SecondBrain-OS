# KB Sync Rules (Obsidian-Only)

## Scope
Rules ini berlaku untuk sinkronisasi knowledge-base antara VPS dan Obsidian lokal Mac, dengan model Git audited.

## Source of Truth
- Root memory resmi: `knowledge-base/`
- Struktur wajib:
  - `raw/` (append-only, immutable)
  - `wiki/`
  - `wiki/index.md`
  - `wiki/log.md`

## Sync Model
- Gunakan Git (audit trail), bukan sync realtime tanpa histori.
- Obsidian membaca working copy Git lokal di Mac.

## Operational Flow (wajib)
1. Sebelum menulis: `git pull --rebase`
2. Tulis/update file markdown
3. Sesudah menulis: `git add` -> `git commit` -> `git push`

## Commit Convention
- Format: `kb: [ingest|update|link|lint] <topic>`
- Contoh: `kb: [ingest] model-routing-fallback`

## Conflict Policy
- Dilarang `push --force`
- Jika conflict:
  - resolve manual
  - commit hasil resolve
  - catat singkat di `wiki/log.md`

## Security Policy
- Jangan commit secrets/token/API key.
- `raw/` hanya tambah file atau append; tidak overwrite sumber mentah.
- Wellbeing/personal default tidak ikut repo umum kecuali approval eksplisit user.

## Bot Ownership
- `reed-archivist`: owner write ke `wiki/`
- `reed-researcher`: menyiapkan sintesis bahan
- `main`: approval policy/prioritas

## Checkpoint Integration
- Checkpoint per 10 chat atau 15 menit/session ditulis ke `wiki/sessions/`.
- Ringkasan aktif ada di file `*-active.md` (overwritten agar konteks usang terbuang).
