# Notion Database Schema

4 database yang dibutuhkan untuk sistem Prompt Refinery.
Buat di Notion, lalu paste Database IDs ke `CLAUDE.md`.

---

## Cara Dapat Database ID

1. Buka database di Notion
2. Klik `...` → `Copy link`
3. URL format: `notion.so/[workspace]/[DATABASE_ID]?v=...`
4. Ambil bagian `[DATABASE_ID]` (32 karakter tanpa tanda hubung)

---

## 1. Prompt Intake

**Fungsi:** Tempat dump prompt mentah yang belum diproses.

| Field | Tipe | Keterangan |
|-------|------|------------|
| Name | Title | Judul singkat prompt |
| Status | Select | `New` / `In Progress` / `Done` |
| Raw Prompt | Text | Isi prompt mentah |
| Source | Select | `Manual` / `Client` / `Internal` / `Template` |
| Submitted By | Text | Nama submitter |
| Date Submitted | Date | Auto-fill saat buat |
| Priority | Select | `High` / `Medium` / `Low` |
| Notes | Text | Catatan tambahan |

**Filter default saat query:** `Status = New`

---

## 2. Refinement Queue

**Fungsi:** Tracking progress proses refine.

| Field | Tipe | Keterangan |
|-------|------|------------|
| Name | Title | ID + judul (contoh: MKT-001 Email Onboarding) |
| Status | Select | `Queued` / `Refining` / `QA Review` / `Done` |
| Prompt ID | Text | Format: MKT-001, SAL-003, dll |
| Kategori | Select | Marketing / Sales / Product / Support / Ops / Research / General |
| Intake Ref | Relation | Link ke Prompt Intake DB |
| Assigned To | Text | Siapa yang mengerjakan |
| Started Date | Date | Kapan mulai diproses |
| Completed Date | Date | Kapan selesai |
| Layer Issues | Multi-select | Layer mana yang bermasalah: ROLE / CONTEXT / TASK / FORMAT / CONSTRAINT |

---

## 3. QA Staging

**Fungsi:** Review dan scoring sebelum masuk Library.

| Field | Tipe | Keterangan |
|-------|------|------------|
| Name | Title | ID + judul prompt |
| Status | Select | `Pending Review` / `Approved` / `Rejected` / `Revision` |
| Prompt ID | Text | Format: MKT-001 |
| Queue Ref | Relation | Link ke Refinement Queue |
| Refined Prompt | Text | Full prompt yang sudah direfine (5 layer) |
| Score Clarity | Number | 0–10 |
| Score Output Quality | Number | 0–10 |
| Score Reusability | Number | 0–10 |
| Score Specificity | Number | 0–10 |
| Score Business Value | Number | 0–10 |
| Total Score | Formula | `Score Clarity + Score Output Quality + Score Reusability + Score Specificity + Score Business Value` |
| QA Notes | Text | Catatan reviewer |
| Reviewed By | Text | Nama reviewer |
| Review Date | Date | Tanggal review |

**Auto-routing:**
- Total ≥ 40 → Status = Approved → pindah ke Library
- Total < 40 → Status = Revision → kembali ke Queue

---

## 4. Prompt Library

**Fungsi:** Koleksi final prompt yang sudah approved.

| Field | Tipe | Keterangan |
|-------|------|------------|
| Name | Title | ID + judul deskriptif |
| Prompt ID | Text | Format: MKT-001 |
| Kategori | Select | Marketing / Sales / Product / Support / Ops / Research / General |
| Status | Select | `Active` / `Deprecated` / `Archived` |
| Full Prompt | Text | Prompt lengkap 5 layer, siap pakai |
| QA Score | Number | Score akhir (40–50) |
| Use Cases | Text | Deskripsi kapan/bagaimana menggunakan prompt ini |
| Variables | Text | List `[variable]` yang bisa diganti |
| Tags | Multi-select | Tag bebas untuk search |
| Versi | Text | Format: v1.0, v1.1, dst. |
| Model Tested | Multi-select | GPT-4 / Claude / Gemini / dll |
| Times Used | Number | Counter berapa kali dipakai |
| Last Used | Date | Kapan terakhir dipakai |
| Published Date | Date | Kapan masuk Library |
| QA Ref | Relation | Link ke QA Staging |
| Last Tested Date | Date | Kapan terakhir diuji ulang di model aktif |

---

## Aturan Re-Testing (Prompt Drift)

Prompt yang bagus hari ini bisa degradasi setelah model target di-update. Ini disebut **Prompt Drift**.

**Kapan wajib re-test:**
- Model target rilis major update (misal: GPT-4 → GPT-4o, Claude 3 → Claude 4)
- Prompt tidak dipakai > 3 bulan
- Ada laporan output yang tidak sesuai ekspektasi

**Prosedur re-test:**
1. Jalankan ulang 3-Run Test (`qa-scorecard.md`)
2. Bandingkan output dengan versi sebelumnya
3. Jika score turun di bawah 40 → pindah ke status `Needs Update`
4. Update field `Last Tested Date` dan `Model Tested` setelah re-test
5. Jika perlu revisi → buat versi baru (v1.1, v1.2) — jangan overwrite versi lama

---

## Views yang Disarankan

### Prompt Intake
- `New Intake` — filter: Status = New, sort: Date Submitted (newest)
- `By Priority` — group by Priority

### Refinement Queue
- `Active Work` — filter: Status = Refining, sort: Started Date
- `Board View` — group by Status (Kanban)

### QA Staging
- `Pending Review` — filter: Status = Pending Review
- `Score Dashboard` — gallery view dengan Total Score visible

### Prompt Library
- `All Active` — filter: Status = Active, sort: Published Date (newest)
- `By Category` — group by Kategori
- `Top Scored` — sort by QA Score (highest first)
- `Recently Used` — sort by Last Used (newest)

---

## Setup Checklist

- [ ] Buat database Prompt Intake
- [ ] Buat database Refinement Queue
- [ ] Buat database QA Staging
- [ ] Buat database Prompt Library
- [ ] Setup formula Total Score di QA Staging
- [ ] Buat relations antar database
- [ ] Paste semua Database IDs ke `CLAUDE.md`
- [ ] Test: buat 1 prompt dummy, jalankan alur lengkap
