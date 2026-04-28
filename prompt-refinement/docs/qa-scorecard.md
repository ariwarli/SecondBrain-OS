# QA Scorecard

Rubrik scoring standar untuk semua prompt yang masuk ke sistem ini.
Total: **50 poin**. Threshold ke Library: **≥ 40 poin**.

---

## Kriteria & Rubrik

### 1. Clarity — Kejelasan Instruksi (0–10)

| Skor | Deskripsi |
|------|-----------|
| 9–10 | Setiap instruksi satu makna. Tidak ada ruang untuk interpretasi berbeda. |
| 7–8  | Hampir semua jelas. Ada 1–2 frasa yang sedikit ambigu tapi tidak kritis. |
| 5–6  | Beberapa instruksi bisa diinterpretasikan berbeda. Butuh asumsi dari AI. |
| 3–4  | Instruksi generik. AI harus mengisi banyak kekosongan sendiri. |
| 0–2  | Tidak jelas. Hasilnya akan sangat bervariasi tiap run. |

**Test:** Minta 2 orang berbeda baca prompt ini. Apakah mereka akan menghasilkan output yang mirip?

---

### 2. Output Quality — Kualitas Output Expected (0–10)

| Skor | Deskripsi |
|------|-----------|
| 9–10 | Format output sangat spesifik. Hasilnya bisa langsung dipakai tanpa edit. |
| 7–8  | Output jelas dan berguna. Mungkin butuh minor editing. |
| 5–6  | Output cukup berguna tapi masih butuh reformatting atau tambahan. |
| 3–4  | Output yang dihasilkan masih kasar, butuh banyak penyesuaian. |
| 0–2  | Output tidak akan berguna dalam kondisi saat ini. |

**Test:** Jalankan prompt ini sekali. Apakah output bisa langsung dipakai?

---

### 3. Reusability — Bisa Dipakai Ulang (0–10)

| Skor | Deskripsi |
|------|-----------|
| 9–10 | Bisa dipakai 10x+ dengan konteks berbeda. Variable jelas dan mudah diganti. |
| 7–8  | Bisa dipakai beberapa kali dengan minor adjustment. |
| 5–6  | Bisa dipakai ulang tapi butuh refactor signifikan per use case. |
| 3–4  | Terlalu spesifik untuk satu kasus, sulit diadaptasi. |
| 0–2  | One-time use. Tidak bisa di-repurpose. |

**Test:** Bisakah prompt ini jadi template dengan `[variable]` placeholder yang mudah diganti?

---

### 4. Specificity — Seberapa Spesifik (0–10)

| Skor | Deskripsi |
|------|-----------|
| 9–10 | Role, context, task, format, constraint semuanya sangat spesifik dan kontekstual. |
| 7–8  | Mayoritas layer spesifik. 1 layer masih agak generik. |
| 5–6  | Beberapa layer cukup spesifik, beberapa masih terlalu broad. |
| 3–4  | Sebagian besar masih generik. Bisa berlaku untuk 10 topik berbeda. |
| 0–2  | Tidak spesifik. Template boilerplate tanpa konteks nyata. |

**Test:** Bisa kah prompt ini dipakai tanpa modifikasi untuk industri/use case yang sangat berbeda? Kalau iya, terlalu generik.

---

### 5. Business Value — Nilai Bisnis (0–10)

| Skor | Deskripsi |
|------|-----------|
| 9–10 | Langsung terhubung ke revenue, conversion, retention, atau efisiensi operasional. |
| 7–8  | Kontribusi bisnis jelas, meski indirect. |
| 5–6  | Ada nilai bisnis tapi tidak terukur atau tidak langsung. |
| 3–4  | Nilai bisnis tidak jelas atau terlalu jauh dari outcome nyata. |
| 0–2  | Tidak ada nilai bisnis yang bisa diidentifikasi. |

**Test:** Kalau prompt ini dijalankan 100x, apakah outputnya akan mempengaruhi metrik bisnis yang bisa diukur?

---

## Cara Ngitung Score

```
Total = Clarity + Output Quality + Reusability + Specificity + Business Value

≥ 40 → Approved, pindah ke Library
35–39 → Minor revision (1–2 layer)
25–34 → Major revision (3+ layer)
< 25  → Reject, buat ulang dari nol
```

---

## Sycophancy Warning

Jangan test prompt dengan bertanya ke AI yang sama: *"Apakah output ini sudah bagus?"*

AI cenderung menjawab "ya" karena sifat sycophancy — ia akan setuju dengan framing pertanyaanmu. Ini bukan QA yang valid.

**Test yang benar:**
- Blind test — jalankan prompt tanpa konteks tambahan, evaluasi output langsung
- Peer test — minta orang lain (atau AI session baru tanpa context) baca output dan tebak instruksinya
- Stress test — jalankan dengan input yang buruk, lihat apakah output tetap on-track

Jangan pernah jadikan persetujuan AI sebagai bukti prompt sudah bagus.

---

## Testing Protocol

Sebelum finalisasi score, jalankan **3-Run Test**:

1. **Run 1** — jalankan prompt persis seperti adanya
2. **Run 2** — jalankan dengan variasi konteks minor
3. **Run 3** — jalankan dengan konteks yang lebih ekstrem

Evaluasi:
- Konsistensi output antar 3 run (bobot Clarity & Specificity)
- Kualitas output terbaik yang bisa dihasilkan (bobot Output Quality)
- Berapa banyak edit yang dibutuhkan sebelum bisa dipakai (bobot Output Quality)

---

## Pass/Fail Checklist — Wajib Sebelum Finalisasi Score

```
✅ Output konsisten di 3 percobaan berturut-turut
✅ Tidak ada output yang menyimpang dari instruksi
✅ Format output 100% sesuai spesifikasi
✅ Tidak menghasilkan konten yang tidak relevan
✅ Waktu ke output berkualitas: maksimal 1 iterasi
✅ Satu prompt = satu tujuan (tidak ada 2 use case dalam 1 prompt)
```

Kalau ada 1 item yang gagal → wajib revisi dulu sebelum scoring.

---

## Score Sheet Template

```
Prompt ID: [ID]
Tanggal QA: [tanggal]
Reviewer: [nama]

Clarity:        __/10  | Catatan: ___________
Output Quality: __/10  | Catatan: ___________
Reusability:    __/10  | Catatan: ___________
Specificity:    __/10  | Catatan: ___________
Business Value: __/10  | Catatan: ___________

TOTAL: __/50

Keputusan: [ ] Approved  [ ] Minor Revision  [ ] Major Revision  [ ] Reject

Layer yang perlu diperbaiki:
[ ] ROLE      [ ] CONTEXT    [ ] TASK    [ ] FORMAT    [ ] CONSTRAINT

Catatan tambahan:
```

---

*Lihat contoh prompt dengan score tinggi → `prompt-examples.md`*
