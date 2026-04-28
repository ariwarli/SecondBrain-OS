# SecondBrain OS Daily SOP

SOP ini adalah versi operasional harian dari `secondbrain-inst.md`.

Tujuan:
- bikin pemakaian `SecondBrain OS` konsisten
- kurangi kebiasaan balik ke SSH untuk hal yang bisa dikerjakan via Telegram
- pakai REED sebagai operator utama dan REED DULL sebagai automation layer

## Rule Utama

- kerja harian utama dilakukan di group `SecondBrain OS`
- `@survivorset_bot` = REED = bot kerja utama
- `@survivorsched_bot` = REED DULL = scheduler/alert bot
- default: kirim pesan biasa tanpa mention
- mention `@survivorset_bot` kalau perlu memastikan REED yang menangani
- jangan pakai `@survivorsched_bot` untuk kerja harian

## Pagi: 5-10 Menit

### 1. Buka `updates`

Cek:
- morning brief
- overnight results
- heartbeat penting
- alert dari `ops` kalau ada

### 2. Tentukan 3 prioritas hari ini

Aturan:
- maksimal 3 prioritas utama
- sisanya parkir
- jangan buka semua thread sekaligus

Kalau perlu minta bantuan:
```text
@survivorset_bot Dari morning brief hari ini, bantu pilih 3 prioritas paling penting.
```

### 3. Dorong kerja berat ke `tasks`

Kalau ada kerja yang butuh:
- riset
- audit
- plan
- drafting
- build

lempar ke `tasks`.

Contoh:
```text
@survivorset_bot Audit 5 competitor AI agency lokal dan ringkas positioning mereka.
```

## Siang: Execution Loop

### 1. Semua ide mentah masuk `inbox`

Gunakan `inbox` untuk:
- voice note
- ide mendadak
- pertanyaan mentah
- brain dump

Contoh:
```text
Gw kepikiran angle baru buat offer AI audit UKM.
```

### 2. Semua kerja nyata masuk `tasks`

Gunakan `tasks` kalau:
- kamu minta hasil kerja
- task >10 menit
- task butuh beberapa langkah

Contoh:
```text
@survivorset_bot Ubah ide ini jadi plan eksekusi 5 langkah.
```

### 3. Semua follow-up orang masuk `personal-crm`

Contoh:
```text
@survivorset_bot Siapa yang overdue follow-up minggu ini? Draft pesan singkatnya.
```

### 4. Semua hal konten masuk `content`

Contoh:
```text
@survivorset_bot Ubah insight ini jadi 3 hook LinkedIn dan 1 outline post.
```

### 5. Semua error/technical masuk `ops`

Contoh:
```text
@survivorset_bot Cek kenapa scheduler tidak kirim heartbeat siang ini.
```

## Sore: 5-10 Menit

### 1. Balik ke `updates`

Cek:
- apa yang sudah selesai
- apa yang masih pending
- apakah ada blocker

### 2. Putuskan carry-over

Jangan biarkan semua task kebawa tanpa keputusan.

Pilihan:
- selesai
- lanjut besok
- delegate overnight
- drop

Contoh:
```text
@survivorset_bot Ringkas progres hari ini jadi selesai, pending, dan carry-over.
```

### 3. Queue kerja malam yang benar-benar bernilai

Masuk ke `tasks` kalau kamu ingin overnight execution.

Task overnight yang bagus:
- riset kompetitor
- audit
- drafting panjang
- pembersihan backlog

## Malam / Overnight

Yang jalan otomatis:
- overnight research
- overnight leads
- overnight builder

Yang kamu lakukan:
- tidak perlu mantengin
- hasilnya akan kembali ke topic yang relevan atau `updates`

## Kapan Pakai Topic Apa

- ide mentah: `inbox`
- kerja konkret: `tasks`
- status/hasil: `updates`
- orang/follow-up: `personal-crm`
- konten: `content`
- error/health: `ops`
- referensi/bahan: `knowledge-base`

## Kapan Harus Mention REED

### Tidak perlu mention

Kalau bot respons normal di topic yang tepat.

### Mention `@survivorset_bot`

Kalau:
- REED tidak merespons
- kamu ingin memastikan prompt penting terbaca
- kamu sedang memberi instruksi penting

### Jangan mention `@survivorsched_bot`

Kecuali:
- test scheduler
- test alert
- test topic mapping

## Brainstorming SOP

### Pakai `inbox`

Kalau ide masih mentah.

Contoh:
```text
@survivorset_bot Bantu brainstorm 10 angle offer baru untuk founder kecil.
```

### Pakai `tasks`

Kalau brainstorming-nya sudah diarahkan ke output.

Contoh:
```text
@survivorset_bot Brainstorm 5 strategi launch yang paling realistis untuk minggu depan, lalu pilih 1 yang paling ringan dieksekusi.
```

### Pakai `content`

Kalau brainstorming konten.

Contoh:
```text
@survivorset_bot Bantu brainstorm 15 ide konten dari tema AI ops buat founder Indonesia.
```

## Kalau Butuh Data Internet

Jangan biarkan REED pura-pura tahu data live.

Gunakan pola ini:
```text
@survivorset_bot Dari konteks yang ada dulu, kasih hipotesis dan bikin research plan. Jangan ngarang data internet.
```

## Check Cepat Kalau Ada Masalah

### Kalau morning brief tidak masuk
- cek `ops`
- minta REED cek scheduler

### Kalau mau cek status sistem cepat
Di VPS:
```bash
/home/openclaw/automation/scheduler-status.sh
```

## Anti-Pattern

- jangan kerja utama di personal chat
- jangan pakai REED DULL untuk brainstorming
- jangan dump semua ke `updates`
- jangan pakai `ops` untuk diskusi biasa
- jangan simpan semua context di kepala atau chat acak

## Flow Paling Sederhana

### Pagi
- buka `updates`
- pilih 3 prioritas
- lempar kerja ke `tasks`

### Siang
- ide masuk `inbox`
- kerja masuk `tasks`
- follow-up masuk `personal-crm`
- konten masuk `content`

### Sore
- baca `updates`
- putuskan carry-over
- queue overnight kalau perlu
