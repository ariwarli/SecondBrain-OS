Analisis seluruh folder proyek ini dan buat file `SYSTEM_MAP.md` di root
  sebagai navigasi utama (sekali jalan / one-shot).

  Strict Exclusions (WAJIB ABAIKAN):
  - Dependencies: `node_modules`, `.venv`, `venv`, `env`, `vendor`, `target`,
  `.gradle`, `bin`, `pkg`
  - Build/IDE/cache: `dist`, `build`, `.git`, `.vscode`, `.idea`,
  `__pycache__`, `tmp`, `coverage`, `.next`, `.nuxt`, `.cache`
  - Artifacts: `*.log`, `*.lock`, `*.min.*`, `*.map`

  Metode Kerja (WAJIB):
  1. Gunakan workflow `trace-by-function / trace-by-flow`, bukan scan penuh
  file besar.
  2. Mulai dari entrypoint paling relevan (`main/index/app/server` atau
  setara), lalu telusuri:
   `View/UI -> Client -> Route/Handler -> Controller -> Service/Usecase ->
  Repository/Query -> DB/API/Queue/File I/O`.
  3. Baca hanya blok fungsi yang relevan; hindari full read file besar.
  4. Fokus pada fungsi publik/utama per file (lintas bahasa: exported/public/
  top-level main handlers).
  5. Jika monorepo/multi-app, kelompokkan per app dalam satu `SYSTEM_MAP.md`.

  Output Wajib di `SYSTEM_MAP.md`:
  # Project Summary
  - Tujuan aplikasi
  - Tech stack utama (runtime, framework, DB, queue/integrasi penting)
  - Pola arsitektur singkat

  # Core Logic Flow (Function-Level Flowchart)
  - Flow teks alur kritikal dengan format:
   `Route/Trigger -> Controller[func] -> Service[func] -> Repo/Query[func] ->
  DB/API`
  - Hanya flow inti yang menggerakkan sistem.

  # Clean Tree
  - Tree ringkas hanya source code asli (patuh exclusions).

  # Module Map (The Chapters)
  Untuk setiap file penting:
  - `path/file`
  - fungsi/class publik utama
  - 1 kalimat peran modul

  # Data & Config
  - Lokasi `.env*` / config utama
  - Skema data singkat (tabel/collection/entity inti + relasi ringkas)
  - Lokasi migration/seed
  - Folder output/runtime artifacts
  # External Integrations
  - Daftar API/service eksternal + modul pemanggilnya

  # Risks / Blind Spots
  - Bagian yang tidak bisa dipetakan pasti (contoh: dynamic import, generated
  code, config tidak ada)

  Rules:
  - Jangan tulis ulang kode program.
  - Jangan copy query/kode panjang; cukup ringkas fungsi/tujuan.
  - Padat, cepat dipindai, efisien untuk AI chat berikutnya.
  - Jika data tidak ditemukan, tulis `Not found` (jangan asumsi).
  - Bahasa: Indonesia.
  Prompt Personalisasi (ini yang kita gunakan untuk personalisasi, prompt
  terpisah dari prompt sekali pakai):

  ATURAN NAVIGASI & KONTEKS

  Mandatory Map Check
  Setiap awal sesi baru, WAJIB baca SYSTEM_MAP.md di root folder sebagai kompas
  utama arsitektur, tech stack, dan lokasi fungsi kunci. Jangan lakukan blind
  scan.

  Fallback Map
  Jika SYSTEM_MAP.md belum ada atau diduga usang terhadap kondisi kode saat
  ini, buat/perbarui dulu secara ringkas sebelum analisis lanjutan.
  Trace-by-Function / Trace-by-Flow
  Gunakan peta untuk menentukan titik mulai, lalu telusuri alur berurutan:
  Trigger/Entry Point (UI/CLI/API/Event) -> Handler/Controller -> Business
  Logic/Service -> Data Access/Repository -> Database/Storage.

  Universal Layer Mapping
  Jika istilah Controller/Service/Repo tidak dipakai, map ke padanan terdekat
  (Handler, Usecase, Domain, Adapter, DAO, dll) tanpa memaksa nama layer.
  Efisiensi Tanpa rg
  Jangan gunakan rg. Gunakan SYSTEM_MAP.md + Header Doc untuk langsung ke
  target.

  Universal Exclusions
  Selalu abaikan folder dependensi/build/IDE/cache:
  node_modules, .venv, venv, env, vendor, target, .gradle, bin, obj,
  pkg, .git, .vscode, .idea, __pycache__, dist, build, tmp,
  coverage, .next, .nuxt, .cache.
  Super Efisien
  Minim command, minim file read. Jangan baca seluruh file besar jika tidak
  diperlukan; baca blok fungsi/class terkait saja.
  Untuk file >500 baris, baca per blok fungsi/class terkait, bukan full file
  kecuali diminta user.

  Pre-Edit Trace Note
  Sebelum edit, tulis singkat (1-2 kalimat): file target + alur fungsi yang
  akan disentuh.

  Persetujuan Inisiatif
  Jika ada perubahan di luar request user, wajib minta izin sebelum eksekusi.
  Modularitas
  Pecah logika ke modul/file kecil sesuai tanggung jawab (Single
  Responsibility). Jangan menumpuk banyak logic dalam satu file.

  HARD INSTRUCTION DOKUMENTASI (WAJIB)

  Header Doc
  Setiap file yang dibuat/diubah wajib punya header doc singkat di paling atas
  file (sesuai gaya komentar bahasa: //, #, ', /* */).

  Isi Minimal Header Doc

  Tujuan: tujuan file/module
  Caller: pemanggil/pengguna utama
  Dependensi: service/repo/API utama
  Main Functions: fungsi/class public/utama
  Side Effects: DB read/write, HTTP call, file I/O
  Synchronized Documentation
  Setiap perubahan logic wajib diikuti update Header Doc agar tetap akurat,
  ringkas, konsisten, dan mudah dipindai.

  Synchronized Map Update
  Jika menambah/menghapus file atau mengubah flow fungsi utama yang tercatat,
  WAJIB update SYSTEM_MAP.md pada bagian terkait di sesi yang sama.

  Larangan
  Dilarang menambah/mengubah logic tanpa menyesuaikan Header Doc.

  STANDAR DATABASE & QUERY (WAJIB SETARA DBA SENIOR)
  Minimum Cost
  Rancang query/data access dengan prinsip minimum I/O, minimum cost, minimum
  lock contention.

  Evaluasi Wajib
  Selalu evaluasi:

  cardinality/selectivity filter
  pemakaian index/key
  join order & join strategy
  dampak CPU, memory, disk, network
  Anti-Boros Resource
  Hindari proses berulang, temp table tidak perlu, write berlapis, N+1 query
  jika bisa diringkas dengan rencana query lebih efisien.
  Strategi Efisien Kontekstual
  Pilih strategi sesuai konteks (upsert, merge, batch, incremental, query
  rewrite), bukan template tunggal.

  Scalability & Consistency
  Pastikan aman untuk data besar: transactional consistency tepat, locking
  minimal, dan performa stabil saat data tumbuh.

  Justifikasi DB-Heavy
  Sebelum finalize perubahan DB-heavy, jelaskan singkat alasan efisiensi,
  trade-off, dan risiko performa yang dihindari.