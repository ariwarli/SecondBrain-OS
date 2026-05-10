# KB Conflict Runbook

## Tujuan
Panduan cepat saat terjadi conflict sinkronisasi knowledge-base.

## Gejala Umum
- `git pull --rebase` gagal karena conflict
- push ditolak karena branch tertinggal

## Langkah Penanganan
1. Jalankan `git status` untuk lihat file conflict.
2. Buka file conflict dan merge manual.
3. Pastikan hasil final tetap mengikuti struktur wiki.
4. Jalankan `git add <file>` untuk semua file yang resolved.
5. Lanjutkan rebase: `git rebase --continue`.
6. Verifikasi: `git status` harus clean.
7. Commit jika perlu dan `git push`.

## Larangan
- Jangan gunakan `git push --force`.
- Jangan menghapus file sumber mentah (`raw/`) untuk “mempermudah” resolve.

## Logging
- Setelah conflict selesai, append ke `wiki/log.md`:
  - timestamp
  - file yang conflict
  - ringkas keputusan merge

Format contoh:
- `2026-04-16T12:40+07:00 | conflict-resolved | wiki/topic-x.md | kept latest facts, merged citations`
