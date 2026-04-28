# 5-Layer Refinement Method

Metode standar refine semua prompt di sistem ini.
Setiap layer WAJIB diisi — tidak boleh ada yang kosong.

---

## Overview

```
PROMPT MENTAH
    ↓
[RISC Analysis]      → Analisis awal sebelum refine
    ↓
Layer 1: ROLE        → Siapa AI ini?
Layer 2: CONTEXT     → Situasi & tujuan
Layer 3: TASK        → Langkah eksekusi
Layer 4: FORMAT      → Bentuk output
Layer 5: CONSTRAINT  → Larangan
    ↓
PROMPT REFINED
```

---

## Pre-Refinement: RISC Analysis

Sebelum mulai refine, evaluasi prompt mentah dengan framework ini:

| Dimensi | Pertanyaan Kunci |
|---------|-----------------|
| **R**elevance | Apakah prompt relevan untuk use case bisnis nyata? |
| **I**ntent | Apa tujuan sebenarnya dari prompt ini? |
| **S**tructure | Apakah struktur instruksinya logis dan urut? |
| **C**larity | Apakah instruksinya bebas dari ambiguitas? |

Kalau Relevance = tidak → tolak, jangan diproses.
Kalau Intent tidak jelas → tanya ke submitter sebelum lanjut.

---

---

## Layer 1 — ROLE

**Pertanyaan:** Siapa persona AI yang akan menjalankan prompt ini?

Bukan sekadar "kamu adalah seorang penulis" — harus spesifik dan kontekstual.

**Formula:**
```
Kamu adalah [jabatan spesifik] dengan [X tahun/level pengalaman]
di bidang [domain], yang ahli dalam [keahlian spesifik].
Kamu bekerja untuk [konteks perusahaan/klien].
```

**Contoh buruk:**
> Kamu adalah seorang copywriter.

**Contoh baik:**
> Kamu adalah Senior Copywriter dengan 8 tahun pengalaman di industri SaaS B2B,
> yang mengkhususkan diri dalam email onboarding dan conversion copy.
> Kamu bekerja untuk startup dengan target audiens founder dan product manager.

---

## Layer 2 — CONTEXT

**Pertanyaan:** Apa situasinya? Untuk siapa? Tujuan bisnis apa?

Isi minimal 3 dari 5 elemen ini:
- **Situasi** — kondisi saat ini
- **Audiens** — siapa yang akan membaca/menerima output
- **Tujuan bisnis** — apa yang ingin dicapai
- **Batasan** — resource, waktu, anggaran
- **Background** — informasi pendukung yang relevan

**Contoh:**
```
Konteks: Startup SaaS baru launch fitur baru (dashboard analytics).
Audiens: User aktif yang sudah pakai produk > 30 hari, segmen SMB.
Tujuan: Meningkatkan feature adoption rate dari 12% ke 30% dalam 60 hari.
Batasan: Email harus < 200 kata. Tidak ada budget untuk A/B test skala besar.
```

---

## Layer 3 — TASK

**Pertanyaan:** Apa yang harus dilakukan, step by step?

Aturan:
- 1 kalimat = 1 instruksi
- Gunakan numbered list
- Urutan logis: riset → analisis → eksekusi → output
- Tidak boleh ambigu — setiap langkah harus actionable

**Contoh buruk:**
> Tulis email yang bagus tentang fitur baru.

**Contoh baik:**
```
1. Identifikasi 1 pain point utama yang diselesaikan fitur dashboard ini.
2. Buat subject line dengan format: [angka/data] + [benefit] (max 50 karakter).
3. Tulis opening paragraph yang langsung menyebut pain point tersebut (2–3 kalimat).
4. Jelaskan fitur dalam 3 bullet point — format: [apa] → [artinya bagi user].
5. Tambahkan 1 social proof atau data usage (bisa placeholder jika belum ada).
6. Tutup dengan 1 CTA yang spesifik dan mendesak.
```

---

## Layer 4 — FORMAT

**Pertanyaan:** Output seperti apa yang diharapkan?

Isi semua elemen ini:
- **Tipe output** — email / artikel / script / tabel / bullet points / dll
- **Panjang** — jumlah kata / paragraf / slide
- **Bahasa** — Indonesia / Inggris / bilingual
- **Tone** — formal / kasual / persuasif / edukatif
- **Struktur** — heading, numbering, dll

**Contoh:**
```
Output: 1 email dalam Bahasa Indonesia
Panjang: 150–200 kata (body), subject line max 50 karakter
Tone: Kasual tapi profesional — seperti teman yang rekomendasikan sesuatu
Struktur:
  - Subject line
  - Opening (2–3 kalimat)
  - Body dengan 3 bullet points
  - CTA (1 kalimat + tombol label)
Bahasa: Indonesia, hindari kata teknis tanpa penjelasan
```

---

## Layer 5 — CONSTRAINT

**Pertanyaan:** Apa yang TIDAK boleh ada di output?

Selalu isi setidaknya 5 constraint spesifik. Jangan generik.

**Contoh buruk:**
> Jangan membuat output yang buruk.

**Contoh baik:**
```
- Jangan gunakan kata-kata hype seperti "revolusioner", "game-changer", "terdepan"
- Jangan sebut kompetitor secara langsung
- Jangan buat klaim tanpa data ("99% user puas") kecuali ada sumber valid
- Jangan gunakan kalimat pasif lebih dari 2x dalam seluruh email
- Jangan tutup dengan "Salam hangat" atau salam generik — gunakan sesuatu yang on-brand
- Jangan jelaskan cara kerja teknis fitur — fokus pada benefit
```

---

## Teknik Refinement Lanjutan

Gunakan teknik ini untuk meningkatkan kualitas di atas baseline 5-layer:

**Teknik 1 — Role Stacking**
Gabungkan dua perspektif dalam satu role untuk output yang lebih kaya:
> *"Kamu adalah seorang copywriter sekaligus psikolog perilaku konsumen..."*

**Teknik 2 — Constraint Inversion**
Daripada bilang "buat yang bagus", tentukan apa yang buruk dan larang:
> *"Hindari jargon teknis, hindari kalimat pasif, hindari pembukaan dengan 'Dalam era digital ini...'"*

**Teknik 3 — Output Scaffolding**
Berikan "tulang" output yang harus diisi AI:
> *"Gunakan struktur: [Hook] → [Problem] → [Solution] → [CTA]"*

**Teknik 4 — Chain Prompting**
Pecah prompt kompleks menjadi 2–3 prompt berantai. Output prompt 1 = input prompt 2.

Pastikan setiap chain punya arah yang jelas — jangan lompat topik:
```
Chain 1: "Buat outline untuk [topik]"
Chain 2: "Kembangkan poin [X] dari outline di atas"
Chain 3: "Revisi agar cocok untuk audiens [target_audiens]"
```

**Teknik 5 — Temperature Instruction**
Minta AI mengatur tingkat kreativitas eksplisit:
> *"Berikan 3 versi: 1 konservatif, 1 moderat, 1 bold/disruptif"*

**Teknik 6 — Fact-Check Chain**
Setelah AI menghasilkan output, challenge dengan prompt verifikasi:
```
Chain 1: "[Instruksi utama — hasilkan output]"
Chain 2: "Kamu adalah fact-checker kritis. Verifikasi output di atas.
          Tandai klaim mana yang tidak akurat atau perlu sumber.
          Jelaskan apa yang mungkin menyebabkan inakurasi tersebut."
```
Berguna untuk prompt kategori riset, data, atau klaim bisnis.

**Teknik 7 — Step-Back Prompting**
Sebelum menjawab task utama, minta AI mundur dulu untuk identifikasi prinsip dasarnya:
```
Sebelum menjawab, identifikasi dulu: prinsip atau framework apa yang
paling relevan untuk [task]? Baru setelah itu kerjakan task-nya.
```
Berguna untuk prompt yang butuh reasoning mendalam — strategi bisnis, analisis, diagnosis masalah.

**Teknik 8 — RaR (Rephrase and Respond)**
Minta AI rephrase instruksi sebelum eksekusi — untuk deteksi ambiguitas di prompt:
```
Sebelum mengerjakan, tulis ulang instruksi ini dengan kata-katamu sendiri
untuk konfirmasi pemahaman. Baru setelah itu eksekusi.
```
Berguna saat testing prompt baru. Kalau AI rephrase-nya meleset → prompt perlu diperjelas.

**Teknik 9 — Emotion Prompting**
Tambahkan stake atau urgensi emosional untuk output yang lebih engaged dan serius:
```
"Output ini akan dipakai langsung di depan 500 investor — pastikan
setiap kata akurat dan meyakinkan."

"Ini adalah email pertama ke klien paling penting tahun ini —
jangan ada kalimat yang terasa generik."
```
Berguna untuk prompt marketing, sales, dan copywriting. Jangan dipakai untuk prompt analitis/teknis.

**Teknik 10 — Penalty/Reward Language**
Tambahkan konsekuensi eksplisit untuk mendorong kepatuhan pada constraint:
```
"Kamu akan mendapat penalti jika output mengandung klaim tanpa data pendukung."
"Pastikan output ini layak dipresentasikan ke board level — tidak ada ruang untuk generik atau filler."
"Setiap instruksi yang diabaikan akan membuat output ini gagal QA."
```
Berbeda dari Emotion Prompting — ini bukan soal emosi, tapi accountability.
Efektif untuk prompt dengan constraint ketat yang sering dilanggar AI.

**Teknik 11 — Delimiter Structure**
Untuk prompt kompleks (> 200 kata), gunakan delimiter eksplisit antar section agar AI tidak salah baca batas layer:
```
###ROLE###
[isi role]

###CONTEXT###
[isi context]

###TASK###
[isi task]

###FORMAT###
[isi format]

###CONSTRAINT###
[isi constraint]
```
Pakai ini sebagai alternatif `## HEADING` kalau prompt akan dijalankan via API atau di model yang sensitif terhadap markdown.

---

## Balanced Prompting — Pre-Check Sebelum Mulai

Sebelum menulis 5 layer, tanyakan:
> *"Apa minimum detail yang masih menjamin output yang gw butuhkan?"*

| Kondisi | Pendekatan |
|---------|-----------|
| Task sederhana, 1 output jelas | 3 layer cukup: ROLE + TASK + FORMAT |
| Task kompleks, multi-step, ada audiens spesifik | 5 layer penuh wajib |
| Task berulang dengan variasi | 5 layer + variabel `[placeholder]` |

Jangan over-engineer prompt sederhana. Jangan under-specify prompt kompleks.

---

## Checklist Sebelum Submit QA

- [ ] Layer ROLE: jabatan + pengalaman + domain + konteks kerja
- [ ] Layer CONTEXT: situasi + audiens + tujuan bisnis
- [ ] Layer TASK: semua langkah numbered, 1 kalimat per instruksi
- [ ] Layer FORMAT: tipe + panjang + bahasa + tone + struktur
- [ ] Layer CONSTRAINT: minimal 5 larangan spesifik
- [ ] Tidak ada layer yang kosong atau terlalu pendek (< 2 baris)

---

*Referensi: `qa-scorecard.md` untuk scoring per layer*
