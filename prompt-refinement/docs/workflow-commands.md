# Workflow Commands

Template perintah siap copas ke Claude untuk setiap tahap kerja.
Ganti teks dalam [BRACKET] sebelum dipakai.

---

## Refine 1 Prompt

```
Refine prompt ini pakai 5-Layer Method.
Beri QA Score setelah selesai.

Prompt mentah:
[PASTE PROMPT DI SINI]

Kategori: [Marketing / Sales / Product / Support / Ops / Research / General]
```

---

## Batch Refine dari File

```
Buka file prompts/intake/[NAMA-FILE].md
Refine semua prompt di dalamnya pakai 5-Layer Method.
Proses maksimal 5 prompt, lalu stop dan minta konfirmasi.
Simpan hasil ke prompts/refined/[ID]-[slug].md per prompt.
```

---

## Batch Refine dari Notion

```
Ambil 5 prompt dengan Status=New dari Intake DB di Notion.
Refine satu per satu pakai 5-Layer Method.
Beri QA Score per prompt.
Update Status di Notion jadi "In Progress" saat mulai,
"Done" saat selesai.
```

---

## QA Score Saja (Tanpa Refine)

```
Beri QA Score untuk prompt ini tanpa refine.
Gunakan rubrik di qa-scorecard.md.
Breakdown per kriteria, lalu berikan rekomendasi
layer mana yang perlu diperbaiki.

Prompt:
[PASTE PROMPT DI SINI]
```

---

## Revisi Berdasarkan QA Feedback

```
Revisi prompt [ID] berdasarkan feedback QA ini:
Layer yang perlu diperbaiki: [ROLE / CONTEXT / TASK / FORMAT / CONSTRAINT]
Feedback: [PASTE CATATAN QA]

Prompt saat ini:
[PASTE PROMPT]
```

---

## Approve & Simpan ke Library

```
Prompt [ID] sudah approved (Score: [X]/50).
1. Pindahkan file dari prompts/refined/ ke prompts/library/
2. Update Notion: Status = "Active" di Library DB
3. Tambahkan field Use Cases dan Variables di Notion
```

---

## Cek Status Batch

```
Lihat semua file di prompts/in-progress/ dan prompts/refined/.
Buat summary: berapa yang sedang diproses, berapa yang menunggu QA,
dan prompt mana yang sudah siap dipindah ke library.
```

---

## Generate ID Baru

```
Cek file terakhir di prompts/library/ dan prompts/refined/
untuk kategori [KATEGORI].
Berikan ID berikutnya yang tersedia.
```

---

## Search Library

```
Cari di prompts/library/ semua prompt dengan kata kunci [KEYWORD].
Tampilkan: ID, judul, QA Score, dan ringkasan Use Cases.
```

---

## Deprecated Prompt

```
Tandai prompt [ID] sebagai deprecated.
Alasan: [ALASAN]
Update status di Notion jadi "Deprecated".
Jangan hapus file — rename jadi [ID]-DEPRECATED-[slug].md
```

---

## End of Session

```
Sesi selesai. Buat summary:
- Berapa prompt yang direfine hari ini
- ID yang diassign
- Prompt mana yang approved / masih perlu revisi
- Next action untuk sesi berikutnya

Simpan summary ke prompts/in-progress/session-log-[TANGGAL].md
```

---

## Tips Efisiensi

- Pakai `/clear` setelah selesai 5 prompt untuk reset context
- Kalau Claude mulai lambat, mulai sesi baru dan paste ulang CLAUDE.md
- Batch prompt sejenis dulu (semua MKT, baru SAL) — lebih konsisten
- Kalau ragu kategori, tanya dulu sebelum mulai refine
