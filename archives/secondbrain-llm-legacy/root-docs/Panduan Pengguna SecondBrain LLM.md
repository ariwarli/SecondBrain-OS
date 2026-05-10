# Panduan Pengguna Second Brain LLM

Dokumen ini ditulis untuk pengguna biasa.

Tujuannya:

- menjelaskan cara memakai sistem
- menjelaskan peran Telegram, Obsidian, dan LLM
- menjelaskan arti folder-folder utama
- menjelaskan alur kerja harian

Kalau ingin versi paling singkat:

- **Telegram** untuk menangkap ide, file, voice note, dan pertanyaan
- **LLM** untuk merapikan dan menyusun pengetahuan
- **Obsidian** untuk menyimpan knowledge final

## 1. Cara Memahami Sistem Ini

Bayangkan sistem ini seperti dapur:

- Telegram adalah meja masuk bahan mentah
- LLM adalah koki yang mengolah bahan
- Obsidian adalah lemari penyimpanan hasil jadi

Artinya:

- Telegram bukan tempat knowledge final
- Obsidian bukan tempat membuang semua hal mentah
- masing-masing punya fungsi berbeda

## 2. Yang Anda Lakukan Sebagai User

Sebagai user, Anda biasanya hanya perlu melakukan empat hal:

1. kirim bahan mentah
2. ajukan pertanyaan
3. cek hasil yang sudah dirapikan
4. koreksi jika ada yang kurang tepat

Contoh bahan mentah:

- ide singkat
- voice note
- link artikel
- catatan meeting
- file PDF
- pertanyaan seperti "apa insight utama dari semua ini?"

## 3. Tiga Mode Penggunaan

### Mode 1: Capture cepat lewat Telegram

Gunakan saat Anda:

- sedang mobile
- habis meeting
- punya ide mendadak
- ingin menyimpan voice note
- ingin forward artikel atau link

Contoh:

- "Simpan ini sebagai ide konten"
- "Ringkas voice note ini"
- "Masukkan artikel ini ke topik pricing"
- "Apa 3 poin penting dari diskusi minggu lalu?"

### Mode 2: Membaca hasil di Obsidian

Gunakan saat Anda:

- ingin membaca knowledge yang sudah rapi
- ingin melihat hubungan antar topik
- ingin membuka note final, bukan chat mentah
- ingin menelusuri keputusan, proyek, atau riset

### Mode 3: Bertanya ke LLM

Gunakan saat Anda ingin:

- mencari ulang sesuatu
- membandingkan dua topik
- meminta rangkuman
- meminta draft
- meminta daftar keputusan, insight, atau action items

## 4. Flow Sederhana yang Perlu Anda Ingat

```text
Anda kirim sesuatu ke Telegram
    ->
LLM memproses isinya
    ->
Knowledge yang sudah rapi masuk ke Obsidian
    ->
Sistem mengindeks knowledge itu
    ->
Saat Anda bertanya, LLM mencari dari knowledge yang sudah rapi
```

Kalau mau disingkat:

- Telegram = pintu masuk
- Obsidian = pusat pengetahuan
- LLM = mesin perapian dan pencarian

## 5. Kenapa Telegram Dipakai

Telegram dipakai karena paling nyaman untuk input cepat.

Keunggulannya:

- bisa dipakai dari HP
- cocok untuk text, voice note, file, dan link
- terasa natural seperti chat biasa
- cepat untuk menangkap ide sebelum hilang

Kalau Anda harus selalu buka dashboard atau vault dulu, banyak ide tidak akan pernah masuk.

Karena itu Telegram dipakai untuk capture.

## 6. Kenapa Obsidian Dipakai

Obsidian dipakai karena knowledge final harus hidup di tempat yang:

- rapi
- tahan lama
- mudah dibaca manusia
- mudah di-link
- mudah dicari
- tidak terkunci ke satu vendor

Kalau Telegram adalah meja kerja, Obsidian adalah perpustakaan pribadi Anda.

## 7. Struktur Folder yang Perlu Anda Pahami

Contoh struktur folder:

```text
knowledge-base/
  inbox/
  raw/
  notes/
  projects/
  people/
  decisions/
  meetings/
  references/
  index.md
  log.md
```

Anda tidak perlu menghafal semuanya. Yang penting, paham fungsi tiap bagian.

### `inbox/`

Tempat draft dan bahan yang belum rapi.

Anggap ini sebagai meja kerja sementara.

### `raw/`

Tempat bahan mentah:

- transcript asli
- dokumen asli
- capture mentah

Anggap ini sebagai arsip bahan baku.

### `notes/`

Tempat note umum yang sudah rapi.

Ini salah satu tempat utama untuk membaca hasil knowledge.

### `projects/`

Tempat konteks per proyek:

- ringkasan
- status
- insight
- keputusan terkait proyek

### `people/`

Tempat note tentang orang, stakeholder, partner, atau kontak penting.

### `decisions/`

Tempat keputusan penting dan alasannya.

Kalau Anda ingin tahu "kenapa kita memutuskan ini?", biasanya mulai dari sini.

### `meetings/`

Tempat ringkasan rapat dan action items.

Idealnya bukan transcript mentah, tetapi versi yang sudah padat dan bisa dipakai ulang.

### `references/`

Tempat sumber dari luar:

- artikel
- paper
- bacaan
- dokumen referensi

### `index.md`

Ini adalah peta isi knowledge base.

Kalau bingung harus mulai dari mana, mulai dari file ini.

### `log.md`

Ini adalah catatan perubahan:

- apa yang baru masuk
- note apa yang diperbarui
- kapan ada perubahan penting

Kalau ingin tahu "apa yang berubah akhir-akhir ini?", lihat file ini.

## 8. Cara Memakai Sistem dengan Benar

### Saat Anda punya ide cepat

Kirim ke Telegram.

Jangan tunggu rapi dulu.

### Saat Anda punya bahan mentah penting

Kirim ke Telegram atau jalur ingest.

Contohnya:

- voice note
- link artikel
- PDF
- hasil meeting

### Saat Anda ingin membaca hasil final

Buka Obsidian.

Jangan cari di chat lama kalau yang Anda butuhkan adalah knowledge yang sudah rapi.

### Saat Anda ingin insight atau jawaban

Tanya ke LLM.

Contoh:

- "Apa keputusan utama tentang pricing bulan ini?"
- "Rangkum semua meeting soal produk X"
- "Apa pola yang berulang dari semua note research ini?"

## 9. Apa yang Terjadi Setelah Anda Kirim Data

Saat Anda mengirim sesuatu, sistem idealnya melakukan ini:

1. menyimpan bahan mentah
2. mengenali jenis input
3. mentranskrip atau merangkum bila perlu
4. menaruh hasil yang lebih rapi ke knowledge base
5. menambahkan metadata
6. mengindeks hasilnya agar bisa dicari ulang

Jadi sistem ini bukan hanya menyimpan chat.

Ia mengubah input mentah menjadi pengetahuan yang bisa dipakai ulang.

## 10. Kesalahan Cara Pakai yang Paling Umum

### Salah 1: Menganggap Telegram adalah knowledge base

Bukan.

Telegram adalah pintu masuk dan tempat percakapan cepat.

### Salah 2: Menganggap semua yang masuk otomatis bagus

Tidak.

Beberapa hal tetap perlu dirapikan atau ditinjau.

### Salah 3: Mencari di folder mentah saat butuh jawaban final

Kalau Anda butuh hasil yang rapi, lihat note final atau tanya sistem berdasarkan knowledge yang sudah diproses.

### Salah 4: Tidak pernah cek hasil ringkasan

LLM sangat membantu, tetapi tetap perlu arahan dan koreksi dari Anda.

## 11. Kenapa Sistem Ini Lebih Unggul dari Sekadar Chat dengan File

Pada sistem biasa:

- dokumen diunggah
- saat ada pertanyaan, sistem mencari potongan yang mirip
- model menjawab
- selesai

Di sistem seperti itu, pengetahuan tidak terlalu menumpuk. Setiap pertanyaan terasa seperti mulai lagi dari nol.

Pada Second Brain LLM:

- bahan mentah masuk
- knowledge dirapikan dan disimpan
- hubungan antar topik dibangun
- note lama bisa diperbarui
- hasil pertanyaan yang penting bisa disimpan kembali

Artinya sistem ini:

- makin bagus seiring waktu
- makin kaya konteks
- makin enak dipakai untuk berpikir

Itulah keunggulan utamanya.

Bukan hanya menjawab.

Tetapi mengompilasi pengetahuan Anda menjadi sistem yang terus tumbuh.

## 12. Rutinitas Mingguan yang Disarankan

Rutinitas sederhana yang sehat:

1. kirim ide dan bahan mentah secara rutin
2. cek note yang paling penting
3. koreksi ringkasan yang keliru
4. buka `index.md` untuk melihat area yang sudah padat atau masih kosong
5. buka `log.md` untuk melihat perubahan terbaru
6. minta sistem merangkum apa yang sudah dipelajari minggu ini

## 13. Aturan Singkat Kalau Anda Bingung

Kalau bingung sesuatu harus masuk ke mana:

- kalau masih mentah: Telegram atau `raw/`
- kalau masih perlu dibersihkan: `inbox/`
- kalau sudah jadi knowledge: folder note final
- kalau ingin lihat peta isi: `index.md`
- kalau ingin lihat riwayat perubahan: `log.md`

## 14. Ringkasan Paling Pendek

Kalau ingin mengingat sistem ini dengan satu model mental:

- Telegram untuk menangkap
- LLM untuk merapikan
- Obsidian untuk menyimpan
- index untuk mencari
- Anda untuk mengarahkan
