# SOP Harian - reed-archivist (6 langkah)

1. `git pull --rebase` di repo `knowledge-base/` sebelum menulis.
2. Proses input baru -> normalisasi transient object dulu, lalu ringkas ke format wiki (bukan transcript mentah).
3. Simpan ke `wiki/` dan update `wiki/index.md` jika ada page baru.
4. Append catatan perubahan ke `wiki/log.md` (timestamp + ringkas perubahan).
5. `git add` -> `git commit` dengan format `kb: [ingest|update|link|lint] <topic>`.
6. `git push`; jika conflict, resolve manual lalu logkan hasil merge ke `wiki/log.md`.
