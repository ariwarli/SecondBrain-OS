# Personal Brand — Bani Risset
# Project instructions untuk Claude Code

## File Penting di Project Ini

- `context-profile.md` — SIAPA Bani & target audiens (baca ini sebelum generate konten apapun)
- `content-calendar.csv` — 181 topik siap dipakai, status Pending/Done
- `threads/drafts/` — Output utas harian disimpan di sini

## Default Behavior di Project Ini

- Selalu baca `context-profile.md` sebelum generate konten
- Gunakan skill `utas-generator` untuk semua pembuatan utas
- Simpan output ke `threads/drafts/YYYY-MM-DD-[topik].md`
- Update status di `content-calendar.csv` dari Pending → Done setelah topik dipakai

## Workflow Harian

1. Ambil topik dari `content-calendar.csv` (status: Pending)
2. Generate utas dengan skill `utas-generator`
3. Simpan ke `threads/drafts/`
4. Update status CSV

## Pilihan Topik

Prioritaskan berurutan:
1. Tier 1 (Informasi Asimetris) — AI UNTUK BISNIS, DIGITAL GROWTH
2. Tier 2 (Konsekuensi Tersembunyi) — SEO & GEO
3. Tier 4 (Lifehack Praktis) — LIFEHACK SOSIAL, Mac ecosystem
4. Tier 5 (Affiliate) — MARKETPLACE HUNTER, Aksesoris MacBook
