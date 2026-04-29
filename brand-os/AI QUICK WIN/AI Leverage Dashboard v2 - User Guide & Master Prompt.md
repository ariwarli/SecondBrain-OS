# AI Leverage Dashboard v2 - User Guide & Master Prompt

## Purpose

Dokumen ini berisi panduan penggunaan dashboard untuk client dan master prompt untuk membuat **AI Leverage Dashboard v2**.

Dashboard ini dipakai untuk service **AI Workflow Sprint 48H**.

Fungsi utama:

* sales demo asset
* client delivery asset
* decision engine
* workflow implementation map

---

# 1. Dashboard User Guide

## Untuk siapa

Panduan ini untuk owner, founder, executive, atau tim yang menerima **AI Leverage Dashboard v2** setelah AI Workflow Sprint 48H.

---

## Fungsi dashboard

Dashboard ini membantu Anda:

* memilih 1 workflow prioritas
* melihat bottleneck utama
* memahami peran AI dan manusia
* menjalankan prompt + SOP
* memantau eksekusi 7 hari
* melihat indikator dampak sederhana

Dashboard ini bukan sekadar laporan.

Dashboard ini adalah alat keputusan dan alat eksekusi.

---

## Cara pakai dalam 5 menit

### 1. Buka tab README

Baca aturan penggunaan singkat.

Fokus utama:

* workflow mana yang sedang diperbaiki
* siapa owner workflow
* output apa yang dianggap selesai

---

### 2. Buka Executive Summary

Lihat ringkasan:

* workflow terpilih
* bottleneck utama
* peran AI
* aturan review manusia
* keputusan berikutnya
* fokus 7 hari

Kalau hanya punya 5 menit, tab ini yang paling penting.

---

### 3. Cek Workflow Intelligence

Gunakan tab ini untuk melihat:

* step mana yang paling macet
* input apa yang dibutuhkan
* output apa yang harus dihasilkan
* siapa pemilik setiap step
* peluang AI di setiap bagian

Tujuannya bukan menganalisis semua proses bisnis.

Tujuannya memilih titik paling high-leverage dulu.

---

### 4. Ambil keputusan di Decision Board

Setiap workflow biasanya macet karena keputusan belum jelas.

Gunakan tab ini untuk menjawab:

* keputusan apa yang dibutuhkan?
* siapa yang memutuskan?
* opsi mana yang direkomendasikan?
* kapan harus selesai?
* apa blocker-nya?

Jika status masih **Blocked**, workflow belum siap dieksekusi penuh.

---

### 5. Jalankan Prompt + SOP Engine

Pilih use case yang sesuai.

Masukkan input yang diminta.

Gunakan output AI sebagai:

* draft follow-up
* summary lead
* reminder
* checklist review
* bahan keputusan owner

Jangan gunakan output AI untuk keputusan sensitif tanpa review manusia.

---

### 6. Update 7-Day Execution Board

Update status minimal 1x sehari selama 7 hari.

Status yang digunakan:

* **Not Started**: belum dimulai
* **In Progress**: sedang dijalankan
* **Blocked**: butuh input atau keputusan
* **Done**: selesai sesuai definition of done

---

### 7. Cek Impact Dashboard

Gunakan tab ini untuk melihat indikator sederhana:

* average response time
* follow-up consistency
* lead leakage
* owner dependency
* booking conversion proxy

Tidak perlu mencari angka sempurna.

Cukup lihat apakah workflow mulai lebih jelas, lebih cepat, dan lebih konsisten.

---

## Aturan penggunaan

* Jangan ubah struktur kolom utama.
* Update status task minimal 1x sehari selama 7 hari.
* Gunakan AI untuk draft, summary, dan rekomendasi awal.
* Keputusan penting tetap direview manusia.
* Jika prompt menghasilkan output generik, perbaiki input/context dulu.
* Jika workflow terasa terlalu luas, kecilkan scope menjadi 1 workflow spesifik.

---

## Kapan perlu eskalasi ke strategist

Hubungi strategist jika:

* workflow terlalu luas
* owner belum bisa memilih prioritas
* task tidak punya owner jelas
* prompt menghasilkan output terlalu generik
* tim bingung kapan sebuah task dianggap selesai
* ada keputusan penting yang masih tertahan di owner

---

# 2. Master Prompt Pembuatan Dashboard

Gunakan prompt ini di AI Studio, Gemini, ChatGPT, atau tool AI lain untuk membuat struktur awal **AI Leverage Dashboard v2**.

```text
Buat desain Google Sheet premium bernama "AI Leverage Dashboard v2" untuk service "AI Workflow Sprint 48H".

Tujuan dashboard:
Membantu business owner memilih 1 workflow prioritas, memahami bottleneck, melihat peran AI dan manusia, menjalankan prompt/SOP, dan mengeksekusi rencana 7 hari.

Gunakan skenario dummy:
- Bisnis: B2B consulting/service business
- Workflow utama: follow-up sales
- Problem: lead masuk dari DM/WhatsApp, tapi follow-up tidak konsisten, respons terlambat, dan owner masih menjadi pusat keputusan
- Goal: meningkatkan konsistensi follow-up, mengurangi lead leakage, dan memperjelas handoff ke owner/sales

Buat struktur Google Sheet dengan tab berikut:
1. README
2. Executive Summary
3. Workflow Intelligence
4. Decision Board
5. AI Workflow Blueprint
6. Prompt + SOP Engine
7. 7-Day Execution Board
8. Impact Dashboard

Untuk setiap tab, berikan:
- Tujuan tab
- Kolom yang dibutuhkan
- 5-10 baris dummy data yang realistis
- Formula sederhana bila relevan
- Instruksi formatting agar terlihat premium, rapi, dan mudah dipahami owner non-teknis

README harus berisi panduan penggunaan singkat:
- Apa fungsi dashboard ini
- Cara pakai dalam 5 menit
- Aturan penggunaan
- Cara membaca status
- Kapan perlu eskalasi ke strategist

Executive Summary harus menampilkan:
- Workflow terpilih
- Bottleneck utama
- AI role
- Human review rule
- Next decision
- 7-day focus
- Simple impact indicators

Workflow Intelligence harus memetakan:
- Workflow step
- Input
- Output
- Owner
- Current friction
- AI opportunity
- Risk
- Priority score

Decision Board harus memuat:
- Decision needed
- Why it matters
- Options
- Recommended choice
- Owner
- Status
- Deadline

AI Workflow Blueprint harus memuat:
- Workflow step
- AI task
- Human task
- Input needed
- Output expected
- Review rule
- Success indicator

Prompt + SOP Engine harus memuat:
- Use case
- Prompt title
- Prompt text
- Required input
- Expected output format
- SOP steps
- Review checklist

7-Day Execution Board harus memuat:
- Day
- Task
- Owner
- Status
- Blocker
- Definition of Done

Impact Dashboard harus memuat dummy metric:
- Average response time
- Follow-up consistency
- Lead leakage
- Owner dependency
- Booking conversion proxy
- Before value
- After target
- Current status

Tambahkan Apps Script opsional hanya jika berguna untuk:
- Generate executive summary dari tab lain
- Update timestamp saat status berubah
- Membuat menu custom sederhana

Jangan buat sistem terlalu kompleks. Dashboard harus bisa dipahami dalam kurang dari 5 menit dan dipakai oleh owner non-teknis.
```
