<!--
Tujuan: SOP operasional per lane untuk Second Brand OS
Caller: user, main, dan operator workspace
Dependensi: docs/SECOND_BRAND_OS_BLUEPRINT.md, docs/INBOX_ROUTING.md, docs/REED_MEMORY_AND_LEARNING.md, docs/REED_COMMAND_RUNTIME_SOT.md
Main Functions: mendefinisikan cara kerja per lane agar bisa langsung diturunkan ke workflow harian
Side Effects: menjadi master SOP yang bisa dipecah lagi menjadi SOP lebih spesifik per lane bila diperlukan
-->

# SOP Second Brand OS per Lane

## 1. Tujuan SOP

SOP ini menetapkan cara kerja standar tiap lane workspace agar Second Brand OS berjalan konsisten, cepat, dan bisa diwariskan.

## 2. Aturan Umum Semua Lane

- satu intent = satu lane utama
- `Inbox` hanya untuk capture dan routing
- pekerjaan aktif tidak boleh tinggal di `Inbox`
- knowledge mentah tidak otomatis jadi canon
- output final harus ditaruh di lane tujuan
- jika ada konflik, ikuti source of truth di `docs/`
- semua hal reusable harus dipertimbangkan untuk promosi ke canon

## 2.1. Progress Merge dari SOP Lama

Sudah diadopsi dari SOP legacy:
- `Inbox` ack-only
- routing ke `tasks`, `content`, `personal-crm`, `knowledge-base`, `ops`
- rhythm kerja pagi / siang / sore
- `Command Center` untuk brainstorming lintas lane
- anti-pattern: jangan kerja utama di personal chat, jangan dump semua ke updates
- reminder yang selesai harus ditutup
- task aging dan carry-over harus terlihat jelas
- research/reference mentah tidak langsung jadi canon

## 3. SOP `INBOX`

### Tujuan
Menangkap pesan mentah dan mengarahkan ke lane yang benar.

### Input
- pesan acak
- request campuran
- link mentah
- reminder
- pertanyaan belum terklasifikasi

### Proses
1. Baca intent utama.
2. Pecah mixed message bila perlu.
3. Tentukan lane tujuan.
4. Balas ack singkat.
5. Lanjutkan kerja di lane tujuan.

### Output
- ack 2 baris
- lane tujuan jelas

### Larangan
- recap panjang
- to-do list
- diskusi lanjutan
- jawaban final kerja di Inbox

## 4. SOP `Command Center`

### Tujuan
Menangani keputusan lintas lane dan brainstorming besar.

### Input
- strategi workspace
- perbandingan opsi
- keputusan besar
- review lintas `tasks`, `content`, `crm`, `knowledge-base`, `brand-os`

### Proses
1. Gabungkan konteks multi-lane yang relevan.
2. Susun opsi dan tradeoff.
3. Pilih rekomendasi.
4. Handoff ke lane operasional.

### Output
- keputusan
- alasan singkat
- handoff ke lane tujuan

## 5. SOP `tasks`

### Tujuan
Menangani kerja aktif, revisi, audit, dan implementasi.

### Input
- task kerja
- revisi
- audit
- follow-up aksi
- implementasi

### Proses
1. Definisikan task.
2. Pecah ke langkah kecil.
3. Kerjakan atau jadwalkan.
4. Update status.
5. Tutup task bila selesai.

### Output
- daftar aksi
- status
- next step

### Rutinitas Harian
- pagi: pilih prioritas utama
- siang: eksekusi dan update blocker
- sore: review carry-over dan closure

## 6. SOP `content`

### Tujuan
Mengubah knowledge dan ide menjadi output publik.

### Input
- source summary
- framework
- angle
- brief konten

### Proses
1. Tentukan format output.
2. Tentukan audience dan tujuan.
3. Susun hook, body, CTA.
4. Revisi tone dan struktur.
5. Finalkan draft.

### Output
- post
- carousel
- thread
- script
- caption

## 7. SOP `personal-crm`

### Tujuan
Mengelola relasi, follow-up, dan komunikasi penting.

### Input
- nama orang
- konteks relasi
- follow-up
- meeting
- deal

### Proses
1. Identifikasi siapa dan kenapa penting.
2. Catat konteks relasi.
3. Tentukan next action.
4. Jadwalkan follow-up bila perlu.
5. Simpan update ke CRM lane.

### Output
- summary relasi
- next action
- reminder/follow-up

## 8. SOP `knowledge-base`

### Tujuan
Menangkap sumber, menyusun knowledge, dan menjaga canon tetap bersih.

### Input
- URL
- PDF
- artikel
- catatan riset
- insight mentah

### Proses
1. Klasifikasikan sebagai source, concept, atau entity.
2. Ringkas poin inti.
3. Tandai relevansi.
4. Sintesis bila perlu.
5. Promosikan ke canon jika reusable.

### Output
- source summary
- concept note
- candidate framework
- canon promotion candidate

## 9. SOP `ops`

### Tujuan
Menjaga runtime, automation, routing, dan observability tetap sehat.

### Input
- issue runtime
- error workflow
- routing problem
- debug request
- service health

### Proses
1. Identifikasi komponen yang gagal.
2. Cek log/trace/config.
3. Tentukan root cause sementara.
4. Terapkan fix atau eskalasi.
5. Catat incident bila ada.

### Output
- diagnosis
- fix
- incident note
- preventive lesson

## 10. SOP `updates`

### Tujuan
Menyampaikan status, ringkasan, dan alert.

### Input
- progress
- summary
- incident singkat
- laporan harian

### Proses
1. Pilih informasi paling penting.
2. Ringkas tanpa noise.
3. Sertakan status dan dampak.
4. Tambahkan next action jika perlu.

### Output
- update singkat
- alert
- summary

### Aturan Praktis
- tidak dipakai untuk dump semua context
- cukup ringkas status, blocker, dan next action
- kalau ada keputusan besar, pindah ke `Command Center`

## 11. SOP `Hormozi`

### Tujuan
Menangani offer, pricing, funnel, sales copy, dan synthesis berbasis Hormozi.

### Input
- produk atau jasa
- source bisnis
- offer draft
- pricing question
- funnel question

### Proses
1. Identifikasi core offer.
2. Analisis value equation.
3. Susun positioning dan angle.
4. Turunkan ke output konten atau task.
5. Simpan insight reusable ke knowledge-base.

### Output
- offer draft
- pricing logic
- funnel angle
- sales copy angle

## 12. SOP `brand-os`

### Tujuan
Menjadi pusat strategi brand, positioning, dan offer.

### Input
- arah brand
- positioning
- USP
- voice
- penawaran

### Proses
1. Tetapkan tujuan brand.
2. Pilih positioning.
3. Tentukan voice dan message.
4. Susun offer atau content direction.
5. Simpan rule yang reusable.

### Output
- strategic notes
- offer direction
- content direction
- brand rule

## 13. SOP `personal-brand`

### Tujuan
Mengubah strategi menjadi output publik.

### Input
- draft
- ide konten
- angle
- asset

### Proses
1. Ambil strategi dari `brand-os`.
2. Pilih format publik.
3. Tulis draft.
4. Revisi tone dan CTA.
5. Finalkan untuk publish.

### Output
- konten publik
- asset publish
- draft final

## 14. SOP `clients`

### Tujuan
Melayani delivery klien dengan state yang jelas.

### Input
- brief klien
- revisi
- dokumen kerja
- status delivery

### Proses
1. Mapping klien dan deliverable.
2. Simpan konteks kerja.
3. Kerjakan per milestone.
4. Update status dan risiko.
5. Tutup setelah delivery selesai.

### Output
- deliverable
- status update
- revisi

## 15. SOP `projects`

### Tujuan
Menangani proyek internal dan eksperimen.

### Input
- ide produk
- prototype
- eksperimen
- proof of concept

### Proses
1. Definisikan tujuan proyek.
2. Tentukan status dan owner.
3. Jalankan eksperimen kecil.
4. Catat hasil.
5. Promote jika layak.

### Output
- eksperimen
- prototype
- keputusan lanjut/stop

## 16. SOP `research`

### Tujuan
Mengubah investigasi menjadi insight yang bisa dipakai.

### Input
- benchmark
- referensi
- analisis kompetitor
- source luar

### Proses
1. Kumpulkan sumber.
2. Bandingkan pola.
3. Tarik insight.
4. Simpan synthesis.
5. Promosikan bila reusable.

### Output
- riset ringkas
- insight
- framework candidate

## 17. SOP `automation`

### Tujuan
Menjalankan pekerjaan berulang secara andal.

### Input
- reminder
- cron job
- workflow berulang
- content nag

### Proses
1. Tentukan trigger.
2. Tentukan output.
3. Pastikan owner jelas.
4. Test sebelum aktif.
5. Monitor dan rapikan bila gagal.

### Output
- job aktif
- reminder
- summary otomatis

## 18. SOP `wellbeing`

### Tujuan
Menjaga sustainabilitas manusia yang menjalankan workspace.

### Input
- energi
- ritme kerja
- kebiasaan
- sinyal burnout

### Proses
1. Catat kondisi aktual.
2. Deteksi overload.
3. Sesuaikan intensitas kerja.
4. Simpan refleksi penting.
5. Buat guardrail bila perlu.

### Output
- wellbeing note
- adjustment
- reminder sehat

## 19. SOP `archives`

### Tujuan
Menjaga arsip agar tidak mengganggu sistem aktif.

### Input
- legacy
- snapshot
- output lama
- sistem lama

### Proses
1. Identifikasi status legacy.
2. Pindahkan dari lane aktif.
3. Beri label jelas.
4. Simpan sebagai referensi historis.

### Output
- arsip rapi
- legacy traceable

## 20. SOP `state`

### Tujuan
Menyimpan state runtime lokal yang dihasilkan sistem.

### Proses
1. Simpan hanya state yang memang perlu.
2. Pisahkan dari canon dan memory harian.
3. Gunakan sebagai cache operasional.
4. Jangan jadikan sumber pengetahuan utama.

## 21. Aturan Penutup

- SOP ini adalah master working rule, bukan narasi motivasi.
- Jika ada conflict dengan `docs/` lain, source of truth yang lebih spesifik menang.
- SOP turunan boleh dibuat per lane jika dibutuhkan detail implementasi lebih lanjut.
