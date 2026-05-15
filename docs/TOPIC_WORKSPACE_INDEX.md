<!--
Tujuan: index README untuk semua topic Telegram workspace Hermes / Second Brain
Caller: user, main, dan subagent operasional
Dependensi: docs/INBOX_ROUTING.md, hermes.md, docs/REED_COMMAND_RUNTIME_SOT.md
Main Functions: memberi peta topic, fungsi, dan prompt use-case singkat
Side Effects: jadi referensi cepat sebelum routing atau brainstorming
-->

# Telegram Topic Workspace Index

Index cepat semua topic Telegram aktif di workspace Hermes / Second Brain.

## Cara Pakai

- kirim bahan mentah ke topic yang sesuai
- pakai `Inbox` hanya untuk capture awal
- pakai `Command Center` untuk lintas topic atau keputusan besar
- pindah ke lane tujuan setelah classify selesai

## Topic Index

### `Command Center` (`thread_id: 1`)
**Fungsi:** hub diskusi utama, brainstorming lintas topik, review multi-lane.

**Pakai untuk:**
- keputusan besar
- evaluasi strategi workspace
- brainstorming yang menyentuh banyak lane
- review lintas `tasks`, `content`, `crm`, `knowledge-base`

**Prompt contoh:**
- `Tolong bandingkan 2 opsi dan pilih yang terbaik.`
- `Review impact kalau semua workspace digabung.`
- `Bikin keputusan final dari beberapa opsi ini.`

### `INBOX` (`thread_id: 11`)
**Fungsi:** capture awal.

**Pakai untuk:**
- pesan mentah
- intake yang belum jelas
- routing awal ke lane tujuan

**Prompt contoh:**
- `Tolong route pesan ini.`
- `Simpan dulu lalu arahkan ke topik yang tepat.`

### `tasks` (`thread_id: 10`)
**Fungsi:** kerja aktif, project, action item.

**Pakai untuk:**
- task kerja
- revisi
- audit
- implementasi
- follow-up operasional

**Prompt contoh:**
- `Buat daftar task dari ini.`
- `Kerjakan follow-up dari catatan ini.`
- `Audit ini lalu beri action list.`

### `content` (`thread_id: 3`)
**Fungsi:** drafting lane untuk output publik.

**Pakai untuk:**
- post
- carousel
- thread
- caption
- script
- hook

**Prompt contoh:**
- `Buat 5 hook dari framework ini.`
- `Ubah ini jadi LinkedIn post.`
- `Bikin carousel 7 slide dari konsep ini.`

### `personal-crm` (`thread_id: 9`)
**Fungsi:** relasi, follow-up, kontak, deal.

**Pakai untuk:**
- orang tertentu
- reminder follow-up
- meeting
- deal pipeline

**Prompt contoh:**
- `Simpan ini sebagai follow-up orang ini.`
- `Ringkas konteks relasi ini.`
- `Buat next action untuk kontak ini.`

### `knowledge-base` (`thread_id: 16`)
**Fungsi:** bahan bacaan, source, synthesize knowledge.

**Pakai untuk:**
- URL
- PDF
- tutorial
- referensi
- insight mentah
- source summary

**Prompt contoh:**
- `Simpan ini sebagai source dan ringkas poin utamanya.`
- `Klasifikasikan ini jadi concept, source, atau entity.`
- `Ambil framework inti dari materi ini.`

### `Hormozi`
**Fungsi:** lane khusus offer, pricing, funnel, sales copy, value equation.

**Pakai untuk:**
- offer design
- pricing logic
- acquisition
- lead magnet
- source-to-concept synthesis
- angle konten berbasis Hormozi

**Prompt contoh:**
- `Analisis ini pakai lens Hormozi untuk offer.`
- `Bikin value equation dari produk ini.`
- `Turunkan source ini jadi framework bisnis yang jelas.`

### `ops`
**Fungsi:** runtime, incident, infra, workflow, automation.

**Pakai untuk:**
- debug sistem
- audit config
- troubleshooting
- scheduling
- service health

**Prompt contoh:**
- `Cek kenapa workflow ini gagal.`
- `Diagnosa masalah routing ini.`
- `Rancang alur automation yang aman.`

### `updates`
**Fungsi:** brief, summary, laporan, alert.

**Pakai untuk:**
- progress report
- status singkat
- incident summary
- daily update

**Prompt contoh:**
- `Buat ringkasan progress hari ini.`
- `Lapor status kerjaan yang sudah selesai.`

## Routing Ringkas

- mentah → `INBOX`
- belajar / simpan → `knowledge-base`
- output publik → `content`
- action → `tasks`
- orang → `personal-crm`
- sistem → `ops`
- strategi lintas lane → `Command Center`
- domain offer/pricing/funnel → `Hormozi`

## Referensi Terkait

- `docs/INBOX_ROUTING.md`
- `docs/HORMOZI_WORKSPACE_GUIDE.md`
- `docs/REED_COMMAND_RUNTIME_SOT.md`
- `hermes.md`
