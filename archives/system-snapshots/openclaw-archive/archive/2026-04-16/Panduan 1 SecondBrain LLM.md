# Panduan Lengkap Menyelaraskan OpenClaw / SecondBrain dengan Blueprint

  ## Ringkasan

  Panduan ini menjabarkan urutan kerja lengkap untuk membuat kondisi runtime OpenClaw selaras dengan knowledge-base/wiki/
  secondbrain-master-blueprint.md, berdasarkan temuan tanggal 2026-04-16.

  Kondisi saat ini:

  - Routing topic sudah dikunci.
  - Wiki memory sudah aktif dan dipakai sebagai acuan.
  - Checkpoint dan healthcheck sudah hidup.
  - Blocker utama masih ada pada agent:main:main karena session store stale dan file JSONL utama hilang.
  - Hygiene secret/config live masih belum rapi.

  Target akhir:

  - main bisa memulihkan konteks secara normal.
  - Semua agent memakai memory yang sama dan konsisten.
  - Dokumen governance sesuai runtime.
  - Flow sync knowledge repo auditable.
  - Secret/config drift tertutup.
  - Verifikasi akhir membuktikan blueprint benar-benar dijalankan, bukan hanya didokumentasikan.

  ## Hasil Akhir Yang Harus Ada

  Pada akhir pekerjaan, sistem harus memenuhi kondisi ini:

  - agent:main:main tidak stale.
  - Session recovery main tidak lagi bergantung pada status darurat seeded-from-session-log.
  - Semua referensi operasional memory mengarah ke knowledge-base/wiki/.
  - Deliverable phase 1, 2, dan 3 di blueprint sudah ada atau sudah diperbarui.
  - wiki/log.md menjadi audit trail perubahan yang cukup.
  - Tidak ada secret sensitif yang ikut terbawa ke repo umum.
  - Healthcheck topic valid tetap lulus.
  - Tidak ada error baru message thread not found.
  - SOP harian dan mekanisme sync benar-benar sejalan dengan perilaku runtime.

  ## Tahap 1: Pulihkan Session main

  ### Tujuan

  Menutup blocker paling penting: agent:main:main stale dan file JSONL utama hilang.

  ### Masalah Yang Diselesaikan

  Dari temuan:

  - main-agent-main-main-active.md menyebut session store agent:main:main stale.
  - File JSONL utama hilang.
  - Recall main tidak terbangun otomatis.

  ### Langkah Kerja

  1. Inventarisasi sumber kebenaran untuk main

  - Cek entry agent:main:main di session store live.
  - Catat field penting:
      - sessionId
      - sessionFile
      - startedAt
      - updatedAt
      - endedAt
      - status
  - Verifikasi apakah sessionFile yang dirujuk benar-benar ada di filesystem.
  - Jika tidak ada, catat ini sebagai insiden resmi di log kerja.

  2. Audit jalur pembentukan active context

  - Temukan proses mana yang biasanya membangun main-agent-main-main-active.md.
  - Tentukan apakah sumber utamanya:
      - session JSONL live
      - checkpoint worker
      - seeded reconstruction dari wiki/log.md
  - Pastikan hanya ada satu jalur resmi untuk recovery normal, dan fallback hanya dipakai saat incident.

  3. Tentukan strategi recovery
     Gunakan prioritas berikut:

  - Prioritas A:
      - jika JSONL hilang tapi bisa direcover dari log, restore file atau regenerate session artifact yang ekuivalen.
  - Prioritas B:
      - jika tidak bisa direcover, buat prosedur rebuild main dari wiki memory resmi:
          - knowledge-base/wiki/log.md
          - knowledge-base/wiki/index.md
          - knowledge-base/wiki/sessions/*-active.md

  4. Terapkan recovery contract

  - Setelah recovery, main harus bisa:
      - membaca context aktif
      - mengetahui decision yang dikunci
      - mengetahui blocker
      - mengetahui next actions
  - Active context main harus mencerminkan keadaan runtime normal, bukan sekadar hasil recovery manual yang tidak terdokumentasi.

  5. Dokumentasikan insiden

  - Tambah entri ke wiki/log.md yang menjelaskan:
      - session store stale
      - session file hilang
      - recovery path yang dipilih
      - hasil verifikasi setelah recovery

  ### Output Tahap 1

  - Session main pulih.
  - Jalur recovery terdokumentasi.
  - Active context main valid.
  - Ada catatan audit di wiki/log.md.

  ### Kriteria Selesai

  - agent:main:main tidak stale lagi.
  - Session metadata valid.
  - Active context main bisa dibentuk ulang tanpa intervensi ad hoc.

  ## Tahap 2: Kunci Source of Truth Memory

  ### Tujuan

  Memastikan blueprint phase 2 benar-benar dijalankan: memory utama hanya dari markdown knowledge.

  ### Masalah Yang Diselesaikan

  Saat ini keputusan sudah ada:

  - Recall memory diarahkan ke knowledge-base/wiki/...
  - Referensi legacy knowledge/ harus dialihkan

  Tetapi ini masih perlu diamankan secara menyeluruh.

  ### Langkah Kerja

  1. Petakan semua referensi memory operasional

  - Cari semua referensi ke:
      - knowledge/
      - knowledge-base/
      - Notion
      - session checkpoint lama
  - Fokuskan pada file yang mempengaruhi runtime:
      - heartbeat
      - worker
      - checkpoint script
      - routing / handoff docs
      - system prompt / active context seed

  2. Klasifikasikan referensi
     Untuk setiap referensi, tandai:

  - valid dan dipertahankan
  - legacy dan harus diganti
  - fallback-only
  - dead path dan harus dihapus

  3. Terapkan aturan memory tunggal
     Kontrak operasional resmi harus menjadi:

  - session active state:
      - knowledge-base/wiki/sessions/*-active.md
  - audit log:
      - knowledge-base/wiki/log.md
  - knowledge entrypoint:
      - knowledge-base/wiki/index.md

  4. Audit heartbeat reed-archivist
     Karena sudah ada keputusan bahwa archivist harus restore dari wiki memory:

  - pastikan heartbeat tidak lagi menarik konteks utama dari inbox/knowledge lama
  - pastikan ia memakai file memory resmi yang sudah dikunci

  5. Audit checkpoint flow

  - Pastikan checkpoint baru disimpan ke folder wiki sessions yang benar.
  - Pastikan checkpoint baru bisa dipakai untuk rebuild context.

  ### Output Tahap 2

  - Tidak ada lagi ambiguitas source of truth memory.
  - Semua runtime path kritikal mengarah ke knowledge-base/wiki/.

  ### Kriteria Selesai

  - Referensi legacy knowledge/ untuk jalur runtime kritikal menjadi nol.
  - Notion tidak lagi menjadi sumber memory aktif.
  - Semua jalur recovery menggunakan memory wiki.

  ## Tahap 3: Lengkapi Deliverable Blueprint Phase 1

  ### Tujuan

  Menyelaraskan runtime dengan artefak governance yang diwajibkan blueprint.

  ### Masalah Yang Diselesaikan

  Blueprint phase 1 meminta:

  - docs/BOT-MATRIX.md
  - docs/SOP-*.md
  - docs/HANDOFF-PROTOCOL.md

  Sementara keputusan runtime saat ini sudah ada, tetapi belum tentu seluruhnya tercermin di dokumen formal.

  ### Langkah Kerja

  1. Bentuk BOT Matrix
     Dokumen ini harus memuat:

  - daftar agent:
      - main
      - reed-archivist
      - reed-builder
      - reed-researcher
      - reed-wellbeing
  - owner per lane
  - fungsi tiap agent
  - input utama
  - output utama
  - boundary data
  - lane/topic resmi milik tiap agent

  2. Bentuk dokumen handoff protocol
     Dokumen harus mengunci format handoff:

  - Context
  - Task
  - Deadline
  - Done Criteria

  Dokumen juga harus menjelaskan:

  - siapa boleh handoff ke siapa
  - kapan handoff diperlukan
  - kapan tidak perlu handoff
  - aturan anti-noise
  - aturan anti-duplikasi task

  3. Dokumentasikan topic ownership
     Masukkan keputusan runtime yang sudah locked:

  - topic valid runtime REED: 11,10,9,3,27,16,13,12,19
  - 1 topic = 1 owner
  - research dan knowledge share owner topic 16 sampai ada lane baru resmi
  - wellbeing tetap lane restricted
  - inbox tidak perlu kirim route confirmation untuk route normal

  4. Sinkronkan dengan control-tower.md
     Semua dokumen phase 1 harus konsisten dengan:

  - owner aktif
  - status lane
  - blockers
  - next step
  - watchlist

  ### Output Tahap 3

  - Governance tidak lagi tersebar hanya di active context.
  - Dokumen phase 1 benar-benar usable bagi agent baru.

  ### Kriteria Selesai

  - Fresh agent bisa memahami struktur lane, owner, dan protokol tanpa membaca chat lama.
  - Tidak ada konflik antara control-tower.md, AGENTS.md, dan dokumen governance baru.

  ## Tahap 4: Sempurnakan Flow Sync dan Auditability

  ### Tujuan

  Menuntaskan blueprint phase 3: git sync audited.

  ### Masalah Yang Diselesaikan

  Sudah ada:

  - conflict runbook
  - SOP harian archivist
  - log perubahan

  Tetapi perlu dipastikan bahwa praktik live sama dengan aturan dokumen.

  ### Langkah Kerja

  1. Cocokkan SOP dengan perilaku nyata
     Bandingkan flow aktual dengan SOP:
  2. git pull --rebase
  3. write
  4. update wiki/log.md
  5. git add
  6. git commit
  7. git push
  8. Audit conflict handling

  - Pastikan tidak ada praktik force push untuk repo knowledge.
  - Pastikan conflict diselesaikan manual.
  - Pastikan hasil merge dicatat di wiki/log.md.

  3. Validasi audit trail

  - Setiap write penting ke wiki harus punya log.
  - Setiap conflict resolution harus punya log.
  - Setiap checkpoint penting harus punya pointer file.

  4. Uji skenario conflict terkontrol
     Simulasikan konflik kecil di page wiki non-kritis:

  - local change
  - vps/remote change
  - pull/rebase
  - resolve manual
  - append hasil ke wiki/log.md

  5. Ratakan istilah
     Samakan istilah di semua dokumen:

  - knowledge-base/wiki/
  - checkpoint
  - active context
  - conflict-resolved
  - kb-governance

  ### Output Tahap 4

  - Sync knowledge repo benar-benar bisa diaudit.
  - SOP bukan hanya teks, tapi terbukti di lapangan.

  ### Kriteria Selesai

  - Satu skenario conflict teruji end-to-end.
  - Semua aturan sync konsisten antara SOP, runbook, dan log aktual.

  ## Tahap 5: Tutup Hygiene Secret / Config Drift

  ### Tujuan

  Menyelesaikan blocker yang masih tercatat di control-tower.md.

  ### Masalah Yang Diselesaikan

  Blocker aktif:

  - secret/config drift masih ada di file live yang tidak boleh dibawa ke repo umum

  ### Langkah Kerja

  1. Inventarisasi semua lokasi sensitif
     Cari file yang mungkin menyimpan:

  - token
  - API key
  - credential
  - URL internal
  - file config lokal
  - konfigurasi workspace live yang seharusnya tidak dipublikasikan

  2. Klasifikasikan setiap item
     Setiap item harus masuk ke satu kategori:

  - live-only
  - pindah ke env
  - aman untuk private repo
  - tidak boleh masuk repo umum
  - obsolete dan harus dihapus

  3. Lock boundary data
     Dokumentasikan aturan:

  - wellbeing/personal default exclude
  - config sensitif tidak ikut sync umum
  - secret tidak disimpan di dokumen governance
  - contoh file yang boleh dan tidak boleh di-commit

  4. Sesuaikan dokumen governance
     Tambahkan atau perbarui:

  - aturan data classification
  - rule repo umum vs repo private
  - rule lane restricted untuk wellbeing

  5. Verifikasi pasca-audit

  - pastikan file sensitif tidak muncul di jalur sync umum
  - pastikan tidak ada pointer yang salah dari dokumen umum ke path sensitif

  ### Output Tahap 5

  - Secret/config drift terpetakan dan tertangani.
  - Guardrail blueprint aktif, bukan asumsi.

  ### Kriteria Selesai

  - Tidak ada secret aktif di dokumen/artefak yang bisa ikut ke repo umum.
  - Wellbeing lane tetap terisolasi.

  ## Tahap 6: Verifikasi Blueprint End-to-End

  ### Tujuan

  Membuktikan bahwa blueprint sudah dijalankan secara operasional.

  ### Langkah Kerja

  1. Verifikasi control plane

  - topic routing sesuai daftar valid
  - owner topic konsisten
  - tidak ada route confirmation yang tidak perlu
  - tidak ada message thread not found

  2. Verifikasi memory plane

  - active context main terbentuk normal
  - checkpoint baru tercatat
  - wiki/log.md menerima log baru
  - wiki/index.md tetap menjadi entrypoint knowledge

  3. Verifikasi sync plane

  - satu write normal berjalan sesuai SOP
  - satu conflict terkontrol bisa diselesaikan
  - audit trail lengkap

  4. Verifikasi security plane

  - secret/config drift tertutup
  - wellbeing lane tidak bocor ke jalur umum

  5. Verifikasi operasional harian

  - inbox-monitor.service sehat
  - session-checkpoint.timer aktif/waiting
  - healthcheck ke topic valid lulus

  ### Output Tahap 6

  - Bukti tertulis bahwa blueprint sudah hidup di sistem.
  - Daftar gap sisa, jika masih ada.

  ### Kriteria Selesai

  Semua poin berikut bernilai benar:

  - main recovery sehat
  - memory source tunggal
  - governance sinkron
  - sync auditable
  - security guardrail aktif
  - healthcheck lulus

  ## Urutan Eksekusi Yang Benar

  Urutan wajib:

  1. Tahap 1
  2. Tahap 2
  3. Tahap 3
  4. Tahap 4
  5. Tahap 5
  6. Tahap 6

  Paralel yang diizinkan:

  - Tahap 3 dan Tahap 5 boleh berjalan paralel setelah Tahap 2 stabil
  - Tahap 4 boleh mulai saat artefak governance utama dari Tahap 3 sudah cukup jelas
  - Tahap 6 selalu terakhir

  Urutan ini penting karena:

  - main stale adalah blocker paling mendasar
  - memory source harus jelas sebelum governance difinalkan
  - governance harus jelas sebelum sync dan audit dianggap final
  - security harus diverifikasi sebelum status “selesai” boleh diklaim

  ## Artefak Yang Harus Dicek Atau Diperbarui

  Artefak yang sudah ada dan wajib dijadikan acuan:

  - knowledge-base/wiki/secondbrain-master-blueprint.md
  - knowledge-base/state/control-tower.md
  - knowledge-base/wiki/log.md
  - knowledge-base/wiki/sessions/main-agent-main-main-active.md
  - knowledge-base/wiki/sop-reed-archivist-daily.md
  - knowledge-base/wiki/wiki-lint-weekly-checklist.md
  - knowledge-base/wiki/ingest-checklist.md

  Artefak yang blueprint minta dan harus dipastikan ada:

  - docs/BOT-MATRIX.md
  - docs/HANDOFF-PROTOCOL.md
  - docs/SOP-*.md
  - docs/KB-CONFLICT-RUNBOOK.md

  ## Acceptance Criteria

  Pekerjaan hanya dianggap selesai jika:

  - agent:main:main tidak stale
  - file atau fallback recovery main jelas dan terdokumentasi
  - active context main tidak lagi bersifat darurat
  - semua referensi memory utama sudah mengarah ke knowledge-base/wiki/
  - deliverable phase 1, 2, dan 3 blueprint tercermin di dokumen dan runtime
  - flow sync sesuai SOP dan terbukti
  - wiki/log.md cukup untuk audit perubahan
  - tidak ada secret/config sensitif di jalur repo umum
  - healthcheck topic valid tetap lulus

  ## Asumsi

  - Blueprint yang menjadi acuan utama adalah knowledge-base/wiki/secondbrain-master-blueprint.md.
  - Tanggal acuan operasional adalah 2026-04-16.
  - Fokus pekerjaan adalah alignment operasional, bukan redesign arsitektur baru.
  - Jika ada gap antara runtime dan dokumen, runtime saat ini tidak otomatis dianggap benar; gap harus diselesaikan secara
    eksplisit dan dilogkan.
