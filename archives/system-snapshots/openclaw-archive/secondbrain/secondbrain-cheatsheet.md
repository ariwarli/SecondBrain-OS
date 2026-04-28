# SecondBrain OS One-Page Cheat Sheet

## Bot

- `@survivorset_bot` = REED = asisten utama
- `@survivorsched_bot` = REED DULL = bot scheduler/alert

## Default Rule

- kerja harian: di group `SecondBrain OS`
- default: kirim biasa tanpa mention
- kalau perlu paksa asisten utama: mention `@survivorset_bot`
- jangan pakai `@survivorsched_bot` untuk kerja harian

## Topic Map

- `updates`
  - morning brief
  - end-of-day summary
  - overnight results

- `inbox`
  - ide mentah
  - voice note
  - brain dump

- `tasks`
  - kerja konkret
  - delegasi
  - riset
  - audit

- `personal-crm`
  - follow-up
  - relasi
  - outreach

- `content`
  - ide konten
  - hooks
  - drafts

- `ops`
  - error
  - logs
  - scheduler alert

- `knowledge-base`
  - URL
  - PDF
  - bahan referensi

## Kapan Pakai Apa

- ide mentah: `inbox`
- minta kerja: `tasks`
- lihat hasil: `updates`
- follow-up orang: `personal-crm`
- bikin konten: `content`
- ada error: `ops`
- lempar bahan: `knowledge-base`

## Daily Flow

### Pagi
- buka `updates`
- pilih 3 prioritas
- lempar kerja ke `tasks`

### Siang
- ide ke `inbox`
- kerja ke `tasks`
- follow-up ke `personal-crm`
- konten ke `content`

### Sore
- baca `updates`
- putuskan carry-over
- queue overnight kalau perlu

## Mention Rule

- tidak perlu mention kalau REED respons normal
- mention `@survivorset_bot` kalau mau eksplisit
- mention `@survivorsched_bot` hanya untuk test scheduler

## Fast Health Check

Kalau mau cek cepat apakah sistem inti masih aman:

- test REED di `ops`:
  - `@survivorset_bot Tes cepat. Balas singkat kalau kamu online.`
- test scheduler path:
  - `@survivorsched_bot ops ping`
- kalau REED diam:
  - cek `ops playbook`
  - jangan pakai `General` sebagai patokan
- kalau scheduler mati:
  - cek jalur REED DULL, bukan REED

## 5 Prompt Cepat

```text
@survivorset_bot Audit 5 competitor lokal dan ringkas positioning mereka.
```

```text
@survivorset_bot Ubah ide ini jadi 3 hook LinkedIn.
```

```text
@survivorset_bot Siapa yang overdue follow-up minggu ini?
```

```text
@survivorset_bot Ringkas progres hari ini jadi selesai, pending, dan carry-over.
```

```text
@survivorset_bot Dari konteks yang ada dulu, kasih hipotesis dan research plan. Jangan ngarang data internet.
```
