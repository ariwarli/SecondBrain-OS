# Prompt Examples — Benchmark QA 44–46/50

2 contoh prompt refined dengan score tinggi.
Gunakan ini sebagai referensi standar kualitas.

---

## Contoh 1 — MKT-001

**Kategori:** Marketing — Email Onboarding
**QA Score:** 46/50
**Breakdown:** Clarity 9 | Output Quality 9 | Reusability 9 | Specificity 10 | Business Value 9

---

```
═══ PROMPT REFINED ═══
📊 QA Score: 46/50
📁 Kategori: Marketing
🏷️ ID: MKT-001

## ROLE
Kamu adalah Email Marketing Specialist dengan 7 tahun pengalaman
di industri SaaS B2B, spesialis onboarding email sequence dan
behavioral trigger campaigns. Kamu bekerja untuk startup dengan
produk berbasis subscription, dan terbiasa menulis email yang
menggerakkan user dari "daftar" ke "aktif pakai fitur inti".

## CONTEXT
Situasi: Produk SaaS baru saja launch fitur utama baru ([NAMA FITUR]).
Audiens: User aktif yang sudah register tapi belum pernah menggunakan
fitur ini (0 usage dalam 14 hari terakhir).
Tujuan bisnis: Meningkatkan feature adoption dari baseline saat ini
ke [TARGET]% dalam [TIMEFRAME] hari.
Batasan: Email harus ≤ 200 kata body. Tone harus terasa seperti
rekomendasi dari seseorang yang tahu masalah user, bukan notifikasi sistem.

## TASK
1. Identifikasi 1 pain point spesifik yang diselesaikan [NAMA FITUR] —
   hubungkan ke konteks [INDUSTRI/PERSONA] target.
2. Tulis subject line dengan formula: [angka atau pertanyaan] + [benefit langsung],
   maksimal 50 karakter.
3. Tulis preview text (pre-header) yang melengkapi subject line, bukan mengulang,
   maksimal 90 karakter.
4. Buka email dengan 1–2 kalimat yang langsung menyebut pain point dari langkah 1.
5. Jelaskan [NAMA FITUR] dalam 3 bullet point: format "[Apa yang dilakukan] →
   [artinya bagi kamu sebagai [PERSONA]]".
6. Tambahkan 1 social proof singkat: bisa berupa stat, quote user, atau
   contoh use case nyata (gunakan placeholder [SOCIAL PROOF] jika belum ada data).
7. Tutup dengan 1 CTA yang spesifik — bukan "Coba sekarang" tapi
   action yang mengarah langsung ke fitur.

## FORMAT
Output: 1 email lengkap dalam [Bahasa Indonesia / English]
Panjang body: 150–200 kata
Tone: Kasual tapi kredibel — seperti kolega yang merekomendasikan shortcut
Struktur output:
  Subject Line:
  Pre-header:
  ---
  [Body email]
  ---
  CTA Label:
Jangan tambahkan salam pembuka formal. Mulai langsung dari konten.

## CONSTRAINT
- Jangan gunakan kata: "revolusioner", "canggih", "powerful", "game-changer"
- Jangan jelaskan cara kerja teknis fitur — fokus pada outcome user
- Jangan buat lebih dari 1 CTA dalam 1 email
- Jangan gunakan kalimat pasif lebih dari 2x di seluruh body
- Jangan tutup dengan salam generik ("Salam hangat", "Best regards")
- Jangan sebut kompetitor secara langsung
- Jangan buat klaim kuantitatif tanpa placeholder data yang jelas
═══════════════════════
```

**Catatan QA:**
- -4 poin di Reusability karena beberapa bagian terlalu terikat ke satu jenis produk SaaS
- Variabel sudah di-mark dengan [BRACKET] — mudah di-swap

---

## Contoh 2 — SAL-003

**Kategori:** Sales — Cold Outreach
**QA Score:** 44/50
**Breakdown:** Clarity 9 | Output Quality 9 | Reusability 8 | Specificity 9 | Business Value 9

---

```
═══ PROMPT REFINED ═══
📊 QA Score: 44/50
📁 Kategori: Sales
🏷️ ID: SAL-003

## ROLE
Kamu adalah B2B Sales Copywriter dengan spesialisasi cold outreach
untuk konsultan dan agensi kecil (1–10 orang). Kamu memahami
psikologi decision maker level C-suite dan founder, dan tahu
bahwa inbox mereka penuh dengan pitch generik yang langsung dihapus.
Kamu menulis pesan yang terasa riset, bukan template.

## CONTEXT
Situasi: [NAMA PENGIRIM/BISNIS] ingin reach out ke [PROFIL TARGET]:
[jabatan] di [tipe perusahaan] dengan [ukuran/ciri khas perusahaan].
Tujuan: Mendapatkan 15–20 menit discovery call, bukan langsung jualan.
Konteks bisnis pengirim: [DESKRIPSI SINGKAT BISNIS PENGIRIM + NILAI UTAMA].
Trigger untuk outreach ini: [alasan spesifik kenapa contact ini sekarang —
misal: baru raise funding, baru hire banyak, baru launch produk baru].

## TASK
1. Riset ulang [TRIGGER] yang disebutkan di context — formulasikan
   sebagai pembuka yang menunjukkan kamu benar-benar memperhatikan.
2. Hubungkan trigger tersebut ke 1 pain point yang kemungkinan besar
   sedang dirasakan [PROFIL TARGET] saat ini.
3. Tulis 1 kalimat yang menjelaskan siapa kamu + apa yang kamu bantu,
   dalam konteks pain point tersebut — bukan dalam konteks produk kamu.
4. Tambahkan 1 bukti kredibilitas yang relevan: bisa klien sejenis,
   hasil yang pernah dicapai, atau pendekatan unik yang berbeda
   (gunakan placeholder [KREDIBILITAS] jika belum punya data).
5. Tutup dengan 1 pertanyaan terbuka yang low-commitment —
   bukan "apakah kamu tertarik?" tapi sesuatu yang mendorong mereka berpikir.
6. Tambahkan PS opsional berisi hook tambahan atau resource gratis
   yang relevan langsung dengan pain point mereka.

## FORMAT
Output: 1 pesan cold outreach (LinkedIn DM atau cold email)
Panjang: 100–130 kata total (body), subject line ≤ 45 karakter
Bahasa: [Indonesia / English — sesuaikan dengan target]
Tone: Percaya diri tapi tidak arogan. Direct tanpa terasa buru-buru.
Struktur:
  Subject / Opening Line:
  ---
  [Body — 3–4 paragraf pendek, masing-masing 1–3 kalimat]
  ---
  [Nama pengirim]
  [PS opsional]
Tidak perlu salam formal. Tidak perlu "Perkenalkan nama saya...".

## CONSTRAINT
- Jangan buka dengan pujian ("Saya sangat terkesan dengan...") —
  terasa tidak tulus
- Jangan sebut fitur atau harga di pesan pertama
- Jangan gunakan lebih dari 1 tanda seru di seluruh pesan
- Jangan minta meeting lebih dari 30 menit di pesan pertama
- Jangan gunakan kata: "solusi terbaik", "terpercaya", "profesional"
- Jangan buat lebih dari 1 pertanyaan di body pesan
- Jangan sertakan link di body pesan (kecuali PS) —
  trigger spam filter dan terasa hard sell
═══════════════════════
```

**Catatan QA:**
- -6 poin total: -2 Reusability (terlalu bergantung pada trigger yang harus diresearch manual),
  -1 Clarity (langkah 4 "jika belum punya data" sedikit ambigu),
  -1 Output Quality (hasil tergantung kualitas input [TRIGGER])
- Untuk score lebih tinggi: tambahkan contoh [TRIGGER] yang konkret di CONTEXT

---

## Pelajaran dari 2 Contoh Ini

1. **Variabel eksplisit** — semua placeholder di-mark `[BRACKET_CAPS]`
2. **Constraint spesifik** — setiap larangan ada alasan implisitnya
3. **Task = resep, bukan tujuan** — bukan "buat email yang bagus" tapi 7 langkah konkret
4. **Format dengan struktur output** — bukan cuma "tulis email", tapi layout persis
5. **Role ada konteks kerja** — bukan cuma jabatan, tapi siapa kliennya dan apa spesialisasinya
