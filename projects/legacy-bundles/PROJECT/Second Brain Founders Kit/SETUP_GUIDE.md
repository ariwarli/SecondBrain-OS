# Setup Guide: AI Second Brain for Founders (SBF)

Selamat datang di sistem infrastruktur intelijen pribadi Anda. Panduan ini akan membantu Anda membangun "Otak Kedua" yang mampu menangkap ide secepat kilat dan memberikan jawaban strategis berbasis AI.

## Arsitektur Sistem
Sistem ini menggunakan 3 lapisan utama:
1. **Capture (Telegram):** Pintu masuk data (Teks, Audio).
2. **Storage (Obsidian):** Rumah bagi pengetahuan Anda (Markdown).
3. **Intelligence (LLM):** Mesin yang memproses dan menjawab (GPT-4 / Claude).

---

## Langkah 1: Setup Obsidian (The Storage)
Obsidian adalah "Source of Truth" Anda. Semua data tersimpan di komputer Anda sendiri dalam format Markdown (.md).

1. Download dan Install [Obsidian](https://obsidian.md).
2. Buat Vault Baru dengan nama `Second Brain`.
3. Gunakan struktur folder **PARA + Authority** (Lihat `OBSIDIAN_STRUCTURE.md` untuk detail):
   - `00 Inbox/`: Tempat penampungan capture mentah.
   - `10 Projects/`: Pekerjaan aktif dengan deadline.
   - `20 Areas/`: Tanggung jawab jangka panjang.
   - `30 Resources/`: Minat dan topik pengetahuan.
   - `40 Archives/`: Hal-hal yang sudah selesai.
   - `50 Authority/`: Draft konten untuk personal branding/otoritas.

---

## Langkah 2: Setup Telegram Bot (The Capture)
Kita ingin menangkap ide tanpa harus buka aplikasi berat.

1. Buka Telegram dan cari `@BotFather`.
2. Ketik `/newbot`, beri nama (Contoh: `Bani's Brain Bot`).
3. Simpan **API Token** yang Anda dapatkan.
4. Gunakan blueprint di `TELEGRAM_BOT_BLUEPRINT.md` untuk menghubungkan Bot ini ke folder `00 Inbox` Anda menggunakan Make.com atau Script sederhana.

---

## Langkah 3: Intelligence Layer (The Prompts)
AI butuh instruksi spesifik untuk tidak sekadar meringkas, tapi memberikan wawasan.

1. Buka file `PROMPT_LIBRARY.md`.
2. Gunakan **Classification Prompt** untuk memilah catatan masuk secara otomatis.
3. Gunakan **Synthesis Prompt** saat Anda ingin membuat draft konten otoritas dari kumpulan riset di folder `30 Resources`.

---

## Cara Pakai Harian (Workflow)

### 1. Capture (Frictionless)
Muncul ide di jalan? Buka Bot Telegram Anda, kirim Voice Note atau Teks singkat. AI akan otomatis mengubahnya menjadi file `.md` di Obsidian Anda.

### 2. Organize (Low-Maintenance)
Seminggu sekali, buka folder `00 Inbox`. Pindahkan catatan ke folder yang relevan (Projects/Resources) sesuai petunjuk di file `OBSIDIAN_STRUCTURE.md`.

### 3. Retrieve (Ask Your Brain)
Gunakan perintah `/ask` di Bot Telegram Anda. AI akan mencari di vault Obsidian Anda dan menjawab: *"Berdasarkan catatan meeting Anda bulan lalu, klien ini lebih suka pendekatan X..."*

---

**Next Action:** Mulai dengan Setup Obsidian Anda sekarang.
