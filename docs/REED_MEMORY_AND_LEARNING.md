<!--
Tujuan: kontrak memory, recall, learning loop, dan canon promotion REED
Caller: agent utama, memory worker, archivist, operator runtime
Dependensi: knowledge-base/wiki, AGENTS.md, docs/REED_RUNTIME_ARCHITECTURE.md
Main Functions: mendefinisikan tier memory dan kapan sesuatu masuk memory vs wiki vs session store
Side Effects: mencegah memory drift, canon bloat, dan hilangnya pembelajaran agent
-->

# REED Memory And Learning

REED memakai model memory tiga lapis.

## Tier 1 — Operational Memory

Ini adalah memory gaya Hermes yang kecil, padat, dan selalu relevan untuk sesi baru.

Isi yang boleh masuk:
- preferensi user
- fakta environment yang sulit dilupakan
- konvensi workflow
- koreksi penting
- pelajaran operasional yang berulang
- status sistem yang berdampak ke perilaku REED

Isi yang tidak boleh masuk:
- transcript panjang
- jurnal penuh
- referensi pustaka
- dump riset
- log kasar

Target bentuk:
- curated
- bounded
- dioptimalkan untuk injection cepat saat session start

## Tier 2 — Session Recall

Semua percakapan, keputusan, reminder, dan hasil kerja harus bisa dicari kembali.

Fungsi:
- mencari “kita pernah bahas apa”
- mengingat detail lama tanpa membebani prompt harian
- menjadi bahan ekstraksi memory dan skill

Tier ini adalah sumber recall, bukan canon.

## Tier 3 — Canon Library

Ini tetap hidup di markdown / Obsidian-style wiki.

Gunakan untuk:
- pustaka jangka panjang
- SOP
- framework
- decisions
- incidents
- journal / catatan hidup yang memang perlu diingat jangka sangat panjang

Lokasi canonical saat ini:
- `knowledge-base/wiki/`
- folder knowledge lain yang memang ditetapkan sebagai library durable

## Promotion Rules

### Session -> Operational Memory
Promosikan jika:
- akan mengubah perilaku REED di sesi masa depan
- penting untuk gaya kerja user
- fakta environment tidak boleh sering dilupakan
- pelajaran operasional sudah terbukti berguna berulang

### Session -> Canon Library
Promosikan jika:
- reusable
- durable
- bibliographic / pustaka
- bagian dari journal jangka panjang
- keputusan atau framework yang akan dipakai lagi

### Session -> Skill Candidate
Promosikan jika:
- workflow berulang
- langkah-langkahnya cukup stabil
- hasil lebih baik bila dibakukan

## Learning Loop

REED harus punya loop pembelajaran tertutup:

1. Observe
- lihat pola kerja, koreksi user, hasil gagal, hasil sukses

2. Extract
- tentukan apakah itu memory, canon, atau skill candidate

3. Consolidate
- gabungkan memory yang mirip
- ringkas pola yang berulang
- buang yang obsolete

4. Reuse
- memory dipakai saat boot
- session recall dipakai saat butuh detail
- skill dipakai untuk workflow berulang

5. Improve
- kalau skill lama tidak lagi cukup, revisi skill atau buat skill baru

## Memory Ownership

- `Operational memory` dimiliki runtime REED
- `Session recall` dimiliki persistence/session store
- `Canon library` dimiliki wiki/knowledge-base

Jangan campur ownership ini.

## Default Policy

- memory first untuk perilaku agent
- wiki first untuk pustaka dan journal hidup
- session recall untuk histori percakapan

Kalau ragu:
- “apakah ini perlu selalu ada di kepala REED saat boot?”
  - ya -> operational memory
- “apakah ini perlu tetap hidup sebagai pustaka/journal?”
  - ya -> canon library
- “apakah ini hanya detail histori yang mungkin dicari nanti?”
  - ya -> session recall
