# Panduan Ngobrol dengan REED
**Untuk siapa:** Bani Risset
**Last updated:** 2026-04-11

> TL;DR: Kirim ke topic yang tepat → REED langsung tahu konteksnya → tidak perlu jelasin ulang dari nol.

---

## Peta Topic Telegram

### 🏥 Wellbeing (topic 19)
**Untuk apa:**
- Jawab morning check-in (angka 1–10)
- Curhat soal kondisi — stres, capek, overwhelm, burnout
- Hal yang masih berputar di kepala sebelum tidur (evening capture)
- Cerita personal yang bukan kerja murni — kekhawatiran, hubungan, decision besar hidup

**Jangan taruh di sini:**
- Task kerja
- Pertanyaan teknis

**Kenapa topic ini ada:**
REED di sini bermode *companion* — tidak langsung problem-solving, lebih hadir dulu. Kalau lo kirim sesuatu ke sini, REED tahu ini bukan tentang produktivitas, ini tentang lo sebagai manusia.

---

### 📥 Inbox (topic 11)
**Untuk apa:**
- Semua yang masuk tapi belum tahu mau diapakan
- Voice note (GROQ Whisper langsung transcribe)
- Ide yang muncul tiba-tiba
- Link artikel, tools, resource
- Info dari klien atau orang lain yang perlu diproses

**Cara pakainya:**
Kirim → lupa → REED yang urus. Dia classify, route ke folder yang tepat, laporkan hasilnya.

**Contoh yang cocok:**
- *"Link ini bagus buat referensi konten LinkedIn"* → masuk Knowledge
- *"Dede minta revisi brief STOP TB besok"* → masuk CRM + Tasks
- Voice note 30 detik tentang ide konten → masuk Content

---

### 📋 Tasks (topic 10)
**Untuk apa:**
- Task kerja yang sudah jelas mau diapakan
- Follow-up kerja dengan klien
- Deliverable yang punya deadline
- Hal teknis yang butuh REED kerjakan sekarang

**Cara pakainya:**
Langsung instruksi. Tidak perlu konteks panjang kalau sudah obvious.

**Contoh:**
- *"Bikin outline proposal untuk NIRVA, deadline Jumat"*
- *"Draft email follow-up ke PT SIN tentang meeting minggu lalu"*

---

### 👥 Personal CRM (topic 9)
**Untuk apa:**
- Update tentang orang — kontak baru, perubahan relasi
- Cerita tentang meeting atau percakapan penting dengan seseorang
- Follow-up yang perlu ditrack
- "Gosip" yang punya implikasi bisnis atau relasi

**Contoh:**
- *"Tadi ketemu Mas Dede, dia mau scale tim tahun ini — kemungkinan buka peluang kolaborasi"*
- *"Si X belum bales proposal sejak 2 minggu lalu"*

REED catat ke crm.md dan set reminder kalau perlu.

---

### 📝 Content (topic 3)
**Untuk apa:**
- Draft konten Threads, LinkedIn, Instagram
- Ide konten yang mau dikembangkan
- Minta REED bikin hook, outline, atau full utas
- Review atau feedback konten yang sudah ada

---

### ⚙️ Ops (topic 27)
**Untuk apa:**
- Hal teknis soal REED sendiri — debug, config, restart
- Shell commands yang mau dijalankan di VPS
- Setup baru, integrasi baru

---

### 📚 Knowledge Base (topic 16)
**Untuk apa:**
- Minta REED riset sesuatu secara dalam
- Simpan pengetahuan yang mau bisa di-recall nanti
- Q&A yang butuh web search

---

### 📊 Updates (topic 13)
**Baca saja.** Ini output otomatis dari automation layer REED:
- Morning brief
- Heartbeat status
- Notifikasi sistem

---

## Cara Bikin REED Makin Pinter tentang Lo

REED baca beberapa file setiap awal sesi. File-file ini adalah "otaknya" tentang lo. Makin lengkap isinya, makin kontekstual responsnya.

### File yang perlu lo *feed* secara aktif

| File | Isi | Cara update |
|------|-----|-------------|
| `health.md` | Kapasitas harian, pattern burnout | Jawab morning check-in (otomatis) |
| `daily.md` | Konteks hari ini — task, priority, update | REED update otomatis; lo bisa tambah manual via Inbox |
| `crm.md` | Siapa aja orang penting, status relasi | Cerita di topic Personal CRM |
| `USER.md` | Siapa lo, cara kerja lo, yang bikin lo annoy | Kasih tau REED kalau ada yang berubah |

### Cara "feed" REED yang paling efektif

**1. Cerita langsung ke Inbox atau topic yang relevan**
REED menyorot info penting otomatis. Lo tidak perlu format apapun — ngomong natural saja.

*Contoh:*
> "Gw baru nyadar gw paling produktif kalau mulai kerja sebelum jam 9. Setelah itu distraksi tinggi."

REED akan simpan ini ke `health.md` sebagai pattern.

**2. Koreksi REED kalau dia salah asumsi**
> "Eh, gw bukan tipe yang suka morning routine panjang — keep it under 5 menit."

REED update `USER.md` berdasarkan koreksi ini.

**3. Kasih tau konteks yang REED mungkin tidak tahu**
> "FYI, klien NIRVA itu punya masalah komunikasi internal — jadi response mereka sering lama bukan karena tidak interested."

REED catat ke `crm.md` dan pakai konteks ini saat lo nanya soal NIRVA berikutnya.

**4. Kasih label kalau mau sesuatu diingat**
> "Ingat ini: gw prefer proposal yang dimulai dari masalah dulu, bukan dari solusi."

REED simpan ke `USER.md` atau `daily.md` tergantung relevansinya.

---

## Cheat Sheet: Kirim ke Mana?

| Situasi | Topic |
|---------|-------|
| Capek, stres, overwhelm | Wellbeing |
| Jawab morning check-in | Wellbeing |
| Ada yang muter di kepala | Wellbeing |
| Ide muncul tiba-tiba | Inbox |
| Voice note apapun | Inbox |
| Link menarik | Inbox |
| Info dari klien | Inbox |
| Task yang sudah jelas | Tasks |
| Cerita soal seseorang | Personal CRM |
| Minta draft konten | Content |
| Debug atau config REED | Ops |
| Minta riset mendalam | Knowledge Base |

---

## Yang Tidak Perlu Lo Lakukan

- ❌ Jelasin ulang siapa lo atau siapa kliennya — REED sudah tahu dari USER.md dan crm.md
- ❌ Format pesan dengan markdown — ngomong natural saja
- ❌ Kirim ke topic yang "paling dekat" kalau tidak yakin — kirim ke Inbox, REED yang route
- ❌ Khawatir REED lupa — dia baca file-file di atas setiap awal sesi
