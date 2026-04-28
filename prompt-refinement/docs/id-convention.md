# ID Convention

Format standar ID untuk semua prompt di library.

---

## Format

```
[KATEGORI]-[NOMOR 3 DIGIT]
```

Contoh: `MKT-001`, `SAL-042`, `PRD-007`

---

## Kategori

| Kode | Kategori | Deskripsi |
|------|----------|-----------|
| `MKT` | Marketing | Konten, copywriting, ads, email marketing, social media |
| `SAL` | Sales | Cold outreach, follow-up, proposal, objection handling |
| `PRD` | Product | Feature spec, user story, PRD, roadmap, changelog |
| `SUP` | Support | Customer service, FAQ, troubleshooting, onboarding |
| `OPS` | Operations | SOP, process doc, runbook, reporting |
| `RES` | Research | Analisis kompetitor, riset pasar, user research synthesis |
| `GEN` | General | Tidak masuk kategori lain, serba guna |

---

## Aturan Penomoran

- Nomor dimulai dari `001` per kategori
- Nomor tidak di-reset — terus increment meski ada yang dihapus
- Nomor yang sudah dipakai tidak boleh dipakai ulang (bahkan setelah prompt dihapus)
- Tracking nomor terakhir per kategori disimpan di Notion (Prompt Library → field "Last ID")

---

## Naming File

Simpan file prompt di folder sesuai status dengan format:

```
[ID]-[slug-judul].md
```

Contoh:
```
prompts/library/MKT-001-email-onboarding-fitur-baru.md
prompts/refined/SAL-003-cold-outreach-founder-saas.md
prompts/in-progress/PRD-002-user-story-dashboard.md
```

Aturan slug:
- Lowercase semua
- Spasi → tanda hubung (`-`)
- Maks 5 kata
- Deskriptif tapi singkat

---

## Sub-kategori (Opsional)

Untuk library yang sudah besar, bisa tambah sub-kategori:

```
MKT-EMAIL-001    → Marketing > Email
MKT-SOCIAL-001   → Marketing > Social Media
SAL-COLD-001     → Sales > Cold Outreach
SAL-CLOSE-001    → Sales > Closing
```

Gunakan sub-kategori hanya kalau satu kategori sudah punya > 20 prompt.

---

## Aturan Penggunaan [variable]

Semua placeholder di prompt menggunakan format `[nama_variable]`.

**Kapan pakai `[variable]`:**
- Input yang berubah tiap penggunaan (nama klien, industri, angka target)
- Data yang harus diisi user sebelum menjalankan prompt
- Konteks yang tidak bisa di-hardcode

**Kapan hardcode (jangan pakai variable):**
- Tone, bahasa, dan format yang memang standar untuk prompt ini
- Constraint yang berlaku universal untuk semua use case prompt ini
- Role yang sudah sangat spesifik dan tidak akan diubah

**Contoh benar:**
```
Kamu adalah copywriter untuk [nama_brand] di industri [industri].
Target audiens: [target_audiens].
Tulis [jumlah] variasi headline untuk campaign [nama_campaign].
Tone: conversational. Bahasa: Indonesia. Max 10 kata per headline.
```

**Naming convention variable:**
- Lowercase, gunakan underscore untuk spasi: `[income_bulanan]`
- Deskriptif tapi singkat: `[target_audiens]` bukan `[ta]`
- Konsisten dalam 1 prompt — jangan pakai `[brand]` dan `[nama_brand]` untuk hal yang sama

---

## Quick Reference

| Mau buat prompt baru? | Langkah |
|----------------------|---------|
| 1. Tentukan kategori | Lihat tabel di atas |
| 2. Cek nomor terakhir | Cek Notion Library atau folder `prompts/library/` |
| 3. Increment +1 | MKT-007 → MKT-008 |
| 4. Buat file | `prompts/in-progress/MKT-008-[slug].md` |
| 5. Update tracking | Update field "Last ID" di Notion setelah approved |
