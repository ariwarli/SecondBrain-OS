# Template Siap Copas untuk Mulai Kerja dengan REED

Dokumen ini berisi template perintah siap copas untuk Bani saat:

- memulai pekerjaan
- memberi update
- meminta maintenance
- memaksa save sesi penting

Gunakan bahasa natural. Template ini hanya membantu supaya intent lebih cepat terbaca dan hasilnya lebih konsisten.

## 1. Start Kerja Harian

Pakai saat Anda baru mulai kerja dan ingin REED membuka konteks aktif lane yang relevan.

### Template umum

```text
Gw mulai kerja sekarang. Buka konteks aktif untuk lane ini, ringkas status sekarang, lalu kasih:
1. keputusan aktif
2. blocker
3. next action paling penting
4. apa yang berubah terakhir kalau ada
```

### Template untuk topic Inbox

```text
Gw mulai kerja. Tolong buka konteks aktif yang paling relevan dari Inbox routing, lalu ringkas:
- apa yang sedang aktif
- apa yang belum jelas
- 3 next action terdekat
```

### Template untuk topic Tasks

```text
Gw mulai kerja di task lane ini. Buka konteks aktif dulu, lalu kasih:
- prioritas utama
- blocker
- deliverable yang harus bergerak hari ini
```

### Template untuk topic Knowledge Base / Research

```text
Gw lanjut kerja di lane knowledge/research ini. Baca konteks aktif dulu, lalu kasih:
- ringkasan topik aktif
- pertanyaan yang masih terbuka
- next action paling bernilai
```

### Template untuk topic Content

```text
Gw lanjut kerja di lane content ini. Buka konteks aktif dulu, lalu kasih:
- ide atau draft yang paling aktif
- blocker
- next action untuk bikin output hari ini
```

### Template untuk topic Personal CRM

```text
Gw lanjut kerja di lane CRM ini. Buka konteks aktif dulu, lalu kasih:
- relasi yang paling perlu diperhatikan
- follow-up yang overdue
- next action paling penting
```

### Template untuk topic Wellbeing

```text
Gw mau check-in. Buka konteks aktif wellbeing dulu, lalu bantu gw lihat:
- kondisi aktif
- pola yang lagi berulang
- satu next step yang paling membantu hari ini
```

### Template untuk topic Ops

```text
Gw lanjut kerja di lane ops ini. Buka konteks aktif dulu, lalu kasih:
- issue aktif
- blocker teknis
- next action paling aman untuk dikerjakan sekarang
```

## 2. Update atau Menambah Konteks

Pakai saat Anda habis meeting, punya ide baru, atau ada keputusan baru.

### Template update umum

```text
Update konteks:
[tulis update di sini]

Kalau ini mengubah keputusan, blocker, atau next action aktif, update memory aktifnya juga.
Kalau tidak, cukup simpan sebagai histori yang relevan.
```

### Template habis meeting

```text
Habis meeting. Ini poin mentahnya:
[tempel poin atau kirim voice note]

Tolong ubah jadi:
- summary singkat
- keputusan
- blocker
- action items

Kalau relevan, update konteks aktif lane ini.
```

### Template keputusan penting

```text
Ingat keputusan ini:
[isi keputusan]

Tolong simpan sebagai keputusan yang bisa direcall nanti. Kalau ini mengubah state aktif, update konteks aktif juga.
```

## 3. Maintenance / Rapikan State

Pakai saat Anda merasa lane mulai bising, terlalu panjang, atau perlu dibersihkan.

### Template maintenance lane

```text
Rapikan lane ini.

Tolong:
- buang item yang sudah selesai atau usang dari konteks aktif
- pertahankan hanya keputusan, blocker, dan next action yang masih relevan
- bilang kalau ada gap knowledge yang perlu diisi
```

### Template weekly cleanup

```text
Jalankan review mingguan untuk lane ini.

Tolong cek:
- apakah konteks aktif masih relevan
- apakah ada keputusan usang
- apakah ada next action yang mandek
- apakah ada hal penting yang belum masuk knowledge
```

## 4. Save Session Penting

Pakai saat sesi ini penting dan Anda tidak mau menunggu auto-checkpoint 10 chat atau 15 menit.

### Template save manual

```text
Save upload session ini ke knowledge-base.

Ringkas hanya:
- keputusan
- fakta baru
- blocker
- next action

Kalau ini mengubah konteks aktif, update file aktifnya juga. Kalau tidak, cukup simpan sebagai histori sesi.
```

## 5. Saat Anda Bingung Harus Kirim ke Mana

Pakai kalau Anda tidak yakin topic yang paling benar.

### Template fallback

```text
Gw belum yakin ini harus masuk lane mana.

Tolong route yang benar, lalu kasih tau:
- ini masuk ke lane apa
- apa action berikutnya
- apakah perlu disimpan sebagai knowledge, task, decision, atau cuma histori
```

## 6. Prinsip Pakai yang Paling Penting

- Untuk mulai kerja, minta REED buka **konteks aktif** dulu.
- Untuk update biasa, cukup kirim natural.
- Untuk sesi penting, pakai template save manual.
- Anda tidak perlu menyebut checkpoint kecuali memang butuh histori lama.

## 7. Template Super Singkat per Topic

### Inbox

```text
Buka konteks aktif Inbox dan kasih 3 next action.
```

### Tasks

```text
Buka konteks aktif task lane ini dan kasih prioritas hari ini.
```

### Content

```text
Buka konteks aktif content lane ini dan kasih output yang paling dekat selesai.
```

### Personal CRM

```text
Buka konteks aktif CRM dan kasih follow-up terpenting.
```

### Knowledge Base

```text
Buka konteks aktif knowledge lane ini dan kasih pertanyaan terbuka + next action.
```

### Wellbeing

```text
Buka konteks aktif wellbeing dan bantu gw check-in singkat.
```

### Ops

```text
Buka konteks aktif ops dan kasih issue aktif + langkah berikutnya.
```
