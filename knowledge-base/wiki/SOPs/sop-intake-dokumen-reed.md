<!--
Tujuan: canon SOP intake dokumen ke REED/Hermes
Caller: REED, archivist, operator workspace, dan sesi intake dokumen
Dependensi: docs/workspace-structure.md, projects/PROJECTS.md, knowledge-base/wiki/index.md, docs/INBOX_ROUTING.md
Main Functions: mengatur channel intake, representasi minimum, routing, dan promosi canon untuk dokumen
Side Effects: memperbarui lane operasional, memory, context klien, dan knowledge-base sesuai jenis dokumen
-->

# SOP Intake Dokumen ke REED (Master + Examples) — v1.3

## 1. Tujuan & Prinsip

Tujuan SOP ini adalah memastikan setiap dokumen yang masuk tidak ngambang, tetapi berakhir di tempat yang tepat dengan ringkasan yang berguna untuk keputusan ke depan.

Prinsip utama:
- Default channel intake adalah **Telegram-first** (Inbox REED).
- Default output REED adalah **Summary + Route + (optional) Next action**, bukan full analysis.
- Dokumen `sensitif` tidak dipaksa lewat Telegram; diproses lokal dulu di Mac.
- SOP ini mengajarkan **pola pikir operasional Bani**, bukan hanya checklist mekanis.
- Hanya alur/insight yang **durable dan reusable** yang boleh naik ke canon, mengikuti taxonomy wiki aktif: `Research`, `Frameworks`, `SOPs`, `Decisions`, `Incidents`.
- **SOP ini tidak menciptakan struktur folder atau bucket baru.** Semua path dan taxonomy tunduk ke `workspace-structure.md`, `PROJECTS.md`, dan `knowledge-base/wiki/index.md`. Jika ada konflik, dokumen-dokumen itu yang menang; SOP ini yang harus di-update.

## 2. Tiga Keputusan Awal (Root Decision Tree)

1. **Jenis dokumen apa ini?**
   - `client` -> materi milik klien atau terkait project klien.
   - `personal` -> dokumen pribadi (life admin, keuangan, refleksi, dsb).
   - `personal-brand` -> terkait brand Bani (strategy, konten, produk personal brand).
   - `reference` -> referensi umum (artikel, whitepaper, buku, deck orang lain, dsb).

2. **Sensitivitasnya bagaimana?**
   - `normal` -> aman dikirim ke Telegram tanpa risiko berarti jika bocor.
   - `sensitif` -> mengandung data keuangan, legal, identitas pihak ketiga, NDA, credential, atau hal yang akan problem jika bocor.

3. **Tujuan kerja apa?**
   - `store` -> hanya disimpan rapi.
   - `summarize` -> ingin ringkasan dan pemahaman konten.
   - `insight` -> ingin REED ambil insight, pola, keputusan penting, risiko, opportunity.
   - `execute` -> ingin REED bantu generate output lanjutan (task, plan, konten, dsb).

## 3. Decision Tree: Telegram vs Lokal

**Telegram-first** jika:
- Dokumen `normal`.
- Ukuran wajar untuk dikirim.
- Tujuan: `store`, `summarize`, `insight`, atau `execute` tanpa manipulasi file asli.

**Lokal Mac-first** jika:
- Dokumen `sensitif`.
- File sangat besar atau butuh kerja file-level (edit langsung di Keynote/Excel/PDF).

Jika lokal dulu, REED tetap harus menerima **payload minimum** via Telegram, berisi:
- Label dokumen (nama file atau deskripsi aman).
- Owner (klien / institusi / Bani sendiri).
- Jenis dokumen.
- Tag `sensitif`.
- Keputusan utama yang diambil.
- Ringkasan aman 3–5 kalimat (tanpa detail raw sensitif).

REED menyimpan payload ini di lane yang tepat sesuai `workspace-structure.md`, sehingga continuity dan ingestion tetap terjaga.

## 4. Jalur Default per Kategori Dokumen

Catatan: Path di bawah mengacu ke struktur yang sudah didefinisikan di `workspace-structure.md` dan `PROJECTS.md`. REED dilarang membuat folder atau file baru di luar struktur yang sudah ada.

### 4.1. Dokumen Klien (`client`)

Default: **Telegram-first** (kecuali `sensitif`/NDA berat -> lokal dulu + payload ke REED).

Kontrak representasi:
- **Default**: REED selalu update `clients/<slug>/context.md` sebagai satu-satunya home intake klien.
- **Jika ada konflik antara `clients/README.md` dan `PROJECTS.md`**: home intake mengikuti `PROJECTS.md` (`context.md`), kecuali user secara eksplisit meminta raw disimpan ke `inbox/`.
- **`inbox/` hanya dipakai jika**: user secara eksplisit meminta "simpan raw ke inbox/" dalam instruksi. Tanpa instruksi itu, REED tidak menyentuh `inbox/`.
- REED tidak membuat subfolder atau file baru di dalam `clients/<slug>/` tanpa instruksi eksplisit.

Promosi ke canon: hanya jika pola kerja dari project ini reusable di >=3 klien berbeda -> masuk bucket `SOPs` atau `Frameworks` di wiki.

### 4.2. Dokumen Pribadi (`personal`)

Default: **Telegram-first** untuk `normal`. **Lokal-first + payload minimum** untuk `sensitif`.

Aturan home lane personal (decision-complete):

| Isi dokumen | Lane + file konkret |
|---|---|
| Kesehatan, energi, habit, wellbeing | `wellbeing/` (sesuai struktur yang ada) |
| Refleksi, keputusan personal, insight dari dokumen | Append ke `memory/YYYY-MM-DD.md` (file daily memory tanggal intake) |
| Panduan/framework yang sudah jadi pengetahuan reusable | `knowledge-base/` sesuai `workspace-structure.md` |

- Untuk keputusan personal dan insight dari dokumen sensitif: REED menambahkan entry baru di `memory/YYYY-MM-DD.md` hari itu, mengikuti kontrak daily continuity notes yang sudah ada di repo.
- Tidak ada lane `personal/` baru. Tidak ada `knowledge-base/personal/...` sebagai catch-all.

Promosi ke canon: hampir tidak pernah; pengecualian hanya untuk `Decisions` atau `Incidents` personal yang dampaknya mempengaruhi cara kerja/bisnis.

### 4.3. Dokumen Personal Brand (`personal-brand`)

Default: **Telegram-first**.

REED membedakan:
- `brand-os/` -> strategy, positioning, offer, audience, arsitektur brand.
- `personal-brand/` -> execution asset (draft konten, ide, script, bahan workshop).

Promosi ke canon:
- Strategy/positioning yang terbukti efektif -> masuk bucket `Frameworks` atau `Decisions` di wiki.
- Execution asset tidak langsung naik ke canon; hanya jika menghasilkan pola reusable.

### 4.4. Dokumen Referensi Umum (`reference`)

Default: **Telegram-first**.

Kontrak representasi:
- REED selalu append entry baru ke **`knowledge-base/references.md`** sebagai landing file resmi untuk semua referensi eksternal.
- Format entry di `references.md`:

```text
## [Judul Dokumen / Nama File]
- Tanggal intake: YYYY-MM-DD
- Sumber: [nama pengirim / URL / external]
- Topik: [tag topik singkat]
- Summary: [3–5 kalimat ringkasan]
- Kandidat canon: [ya – bucket X / tidak]
```

- Tidak ada subfolder baru di dalam `knowledge-base/`.
- Hanya naik ke wiki jika sudah ada **synthesis atau framework yang dibuat dari referensi ini**, dengan bucket yang jelas: `Research` atau `Frameworks`.

## 5. Format Instruksi Saat Menyerahkan Dokumen ke REED

Minimal sertakan tiga hal: jenis dokumen, owner, tujuan.

Format prompt minimum:

> "Ini dokumen `[jenis]` milik `[siapa]`, tujuan saya `[tujuan]`. Tolong jalankan SOP intake dokumen."

Contoh prompt per kategori:
- **Client**:
  - "Ini dokumen `client` milik `[slug-klien]`, tujuan saya `summarize + insight` untuk next step. Tolong jalankan SOP intake dokumen."
- **Personal**:
  - "Ini dokumen `personal`, tujuan saya `store + summarize`. Tolong jalankan SOP intake dokumen dan mapping ke lane yang sesuai (wellbeing/memory/knowledge-base)."
- **Personal brand**:
  - "Ini dokumen `personal-brand`, fokusnya strategy/offer. Tujuan saya `insight + execute`. Tolong jalankan SOP intake dokumen."
- **Reference**:
  - "Ini `reference` umum (judul: [judul]), tujuan saya `store + summarize`. Kalau ada framework/insight penting, tandai sebagai kandidat `Research` atau `Frameworks` di wiki."

Untuk dokumen `sensitif` lokal:

> "Aku baru review dokumen sensitif lokal: `[label]` milik `[owner]`, jenis `[jenis]`. Sensitivitas: `sensitif`. Keputusan utama: `[keputusan]`. Ringkasan aman: `[3–5 kalimat]`. Tolong simpan payload ini dan route sesuai SOP intake dokumen sensitif."

## 6. Output Standar REED untuk Intake Dokumen

Setiap kali menerima dokumen, REED **selalu** membalas dengan format:

```text
Classification:
  - Jenis: [client / personal / personal-brand / reference]
  - Sensitivitas: [normal / sensitif]
  - Tujuan: [store / summarize / insight / execute]
  - Priority: [P1 / P2 / P3]

Route:
  ✅ ROUTED → [path nyata sesuai workspace-structure / PROJECTS.md]
  (mis: clients/rumahsakit-sehat/context.md)

Summary:
  [ringkasan singkat isi dokumen]

Next:
  [satu next action konkret, atau "No immediate action - archived for reference"]
```

### Aturan P1/P2/P3

Priority adalah **label tampilan informatif**, tidak otomatis memicu behavior downstream:
- `P1` -> butuh perhatian Bani dalam 24–48 jam.
- `P2` -> penting tapi tidak urgent.
- `P3` -> arsip/referensi saja.

P1/P2/P3 **tidak** mengubah routing path, tidak otomatis muncul di `daily.md`, dan tidak otomatis membuat task. Penggunaan downstream (scheduler, daily review, reminder) hanya aktif jika ada aturan eksplisit yang dibuat terpisah di luar SOP ini.

REED **tidak pernah**:
- Memaksa upload dokumen `sensitif` ke Telegram.
- Membuat folder, file baru, atau bucket wiki baru tanpa instruksi eksplisit.
- Mengusulkan promosi ke canon pada intake pertama tanpa bukti reuse (kecuali bucket `Decisions`/`Incidents`).

## 7. Kriteria Promosi ke Canon

Canon mengikuti taxonomy wiki aktif: `Research`, `Frameworks`, `SOPs`, `Decisions`, `Incidents`.

| Bucket | Kapan masuk canon |
|---|---|
| `SOPs` | Alur operasional yang sudah dipakai >=3 kali di konteks berbeda, hasil konsisten |
| `Frameworks` | Model atau pola kerja yang dipakai sebagai acuan pengambilan keputusan |
| `Research` | Temuan/riset yang sudah disintesis (bukan sekadar referensi mentah) |
| `Decisions` | Keputusan berdampak jangka panjang, one-way door, atau mengubah cara kerja |
| `Incidents` | Kejadian dengan pelajaran penting yang perlu mencegah pengulangan |

Golden rule:

> "Canon berisi pengetahuan yang **durable**: SOPs/Frameworks butuh bukti reuse; Decisions/Incidents boleh masuk walau sekali jika penting dan berdampak jangka panjang. Semua entri harus jelas bucket-nya dan tidak bertentangan dengan Bani-OS yang ada."

## 8. Example Pack (4 Kasus Nyata)

### Example 1 – PPT Klien dari Email

**Input**
- File: `Marketing-Plan-Q3.pptx`
- Owner: `rumahsakit-sehat`
- Jenis: `client`, `normal`
- Tujuan: `summarize + insight` untuk next step

**Prompt ke REED**

> "Ini dokumen `client` milik `rumahsakit-sehat`, tujuan saya `summarize + insight` untuk next step. Tolong jalankan SOP intake dokumen."

**Output REED yang benar**

```text
Classification:
  - Jenis: client
  - Sensitivitas: normal
  - Tujuan: summarize + insight
  - Priority: P1

Route:
  ✅ ROUTED → clients/rumahsakit-sehat/context.md
  (update context.md dengan summary intake ini;
  inbox/ tidak disentuh karena tidak ada instruksi eksplisit)

Summary:
  Deck rencana kampanye WhatsApp Q3. Target: 1.500 lead baru/bulan
  dari pasien baru. Budget: 60 juta/bulan (Meta Ads + agency). KPI:
  CTR 1,5–2%, conversion to appointment 8–10%, CAC maks 150k.

Next:
  Review asumsi KPI dan susun counter-proposal dengan 2–3 skenario
  budget sebelum membalas klien.
```

**Status canon**: tidak naik sekarang. Naik ke `SOPs` jika pola kerja ini dipakai di >=3 klien berbeda.

### Example 2 – Dokumen Pribadi Sensitif (Keuangan)

**Input**
- File lokal: `2026-personal-finance-projection.xlsx`
- Owner: `Bani`
- Jenis: `personal`, `sensitif`
- Tujuan: `insight` (putuskan apakah bisa ambil project besar baru)

**Langkah lokal di Mac**
- Review file di Numbers/Excel, catat keputusan utama secara manual.

**Payload ke REED**

> "Aku baru review dokumen sensitif lokal: `2026-personal-finance-projection.xlsx` milik `Bani`, jenis `personal`. Sensitivitas: `sensitif`. Keputusan utama: runway aman +-18 bulan; boleh ambil 1–2 project besar dengan margin sehat; hindari fixed cost baru sebelum Q4. Ringkasan aman: proyeksi keuangan macro 2026 menunjukkan ruang ekspansi terbatas dengan batas yang jelas. Tolong simpan payload ini dan route sesuai SOP intake dokumen sensitif."

**Output REED yang benar**

```text
Classification:
  - Jenis: personal
  - Sensitivitas: sensitif
  - Tujuan: insight
  - Priority: P2

Route:
  ✅ ROUTED → memory/2026-04-29.md
  (append entry keputusan personal ke daily memory file hari ini;
  format mengikuti kontrak continuity notes yang ada di repo)

Summary:
  Dokumen keuangan pribadi 2026 (sensitif, lokal). Kesimpulan:
  runway +-18 bulan dengan asumsi income sekarang. Boleh ambil
  1–2 project besar asalkan margin sehat, tanpa tambah fixed cost
  signifikan sebelum Q4.

Next:
  Jadikan constraint ini sebagai referensi saat menilai project
  baru. Tidak perlu action harian.
```

**Status canon**: tidak naik. Keputusan personal ini bersifat situasional, bukan reusable sebagai SOP.

### Example 3 – Deck Personal Brand (Strategy)

**Input**
- File: `BaniRisset-Brand-OS-v2.key`
- Owner: `Bani`
- Jenis: `personal-brand`, `normal`
- Tujuan: `insight + execute` (refine strategi dan turunkan ke plan)

**Prompt ke REED**

> "Ini deck `personal-brand` milik `Bani`, isinya strategy/offer untuk personal brand (Brand OS v2). Tujuan saya `insight + execute`. Tolong jalankan SOP intake dokumen."

**Output REED yang benar**

```text
Classification:
  - Jenis: personal-brand
  - Sub-tipe: strategy (bukan execution asset)
  - Sensitivitas: normal
  - Tujuan: insight + execute
  - Priority: P1

Route:
  ✅ ROUTED → brand-os/
  (ini strategy/positioning/offer -> home-nya brand-os/, bukan
  personal-brand/)

Summary:
  Brand OS v2: audience inti = founder/exec Indonesia yang ingin
  integrasi AI & automation. Positioning: Digital & AI Strategist,
  18 tahun + 1.000+ klien. Tiga offering utama 12 bulan:
  WhatsApp automation (healthcare/NGO), corporate AI training,
  personal brand monetization. Channel: Telegram (ops),
  X/LinkedIn (distribution), email list.

Next:
  1) Turunkan menjadi 3–5 key initiatives per kuartal.
  2) Buat mapping: offering ↔ ICP ↔ channel ↔ format konten.
  3) Jika strategi ini terbukti jalan setelah dipakai, promosikan
     ke wiki bucket Frameworks (bukan sekarang).
```

**Status canon**: kandidat `Frameworks` setelah terbukti efektif; belum naik di intake pertama.

### Example 4 – PDF Referensi Umum

**Input**
- File: `AI-Agent-Playbook-2026.pdf` (ebook publik)
- Owner: `external`
- Jenis: `reference`, `normal`
- Tujuan: `store + summarize`; kalau ada framework penting, tandai sebagai kandidat wiki

**Prompt ke REED**

> "Ini `reference` umum (judul: AI-Agent-Playbook-2026.pdf), tujuan saya `store + summarize`. Kalau ada framework/insight penting, tandai sebagai kandidat `Research` atau `Frameworks` di wiki."

**Output REED yang benar**

```text
Classification:
  - Jenis: reference
  - Owner: external (publik)
  - Sensitivitas: normal
  - Tujuan: store + summarize
  - Priority: P3

Route:
  ✅ ROUTED → knowledge-base/references.md
  (append entry baru dengan format kontrak references.md;
  topik: ai-agents; kandidat canon: ya - Frameworks, setelah versi
  lokal dibuat dan dipakai)

Summary:
  Ebook ini membahas implementasi AI agent di bisnis:
  tahapan ide -> prototipe -> pilot -> scale; mulai dari use case
  internal sebelum customer-facing; 2 framework visual relevan
  untuk Bani: decision tree pemilihan use case pertama, dan
  matriks value vs complexity untuk prioritisasi.

Next:
  No immediate action - archived for reference.
  Kandidat wiki: dua framework di atas bisa dipromosikan ke bucket
  Frameworks HANYA setelah Bani membuat versi lokal yang sudah
  disesuaikan dan dipakai dalam pengambilan keputusan nyata.
```

**Status canon**: belum naik. Masuk `Research` jika sudah ada sintesis dari ebook ini; masuk `Frameworks` jika versi lokalnya sudah dipakai sebagai alat keputusan.
