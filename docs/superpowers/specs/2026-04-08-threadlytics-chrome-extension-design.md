# Threadlytics — Chrome Extension for Threads Analytics
**Date:** 2026-04-08
**Status:** Design Approved
**Author:** Bani Risset

---

## Overview

Chrome extension yang menganalisa pertumbuhan follower, post engagement, views, likes, dan comments di Threads (threads.net). Distribusi publik via Chrome Web Store. Monetisasi freemium dengan trial 3 hari penuh, kemudian free tier terbatas atau upgrade ke Pro.

---

## 1. Arsitektur & Komponen

### Komponen Utama

| Komponen | Teknologi | Fungsi |
|---|---|---|
| Content Script | Vanilla JS | Scrape DOM threads.net secara pasif |
| Background Service Worker | Service Worker (MV3) | Data pipeline, deduplication, storage |
| Side Panel UI | Preact + Tailwind CSS | Tampilan analytics |
| Local Storage | IndexedDB via Dexie.js | Simpan data 30 hari rolling |
| Backend | Supabase (PostgreSQL + Edge Functions) | Trial enforcement, license validation |
| Payment & License | Sejoi + Xendit | Checkout, generate license key |

### Diagram Arsitektur

```
[threads.net]
     │
     ▼
[Content Script] ← passive DOM scraping via MutationObserver
     │
     ▼
[Background Service Worker]
  - deduplicate by post_id
  - simpan ke IndexedDB (30 hari rolling)
  - snapshot follower 1x/hari
  - cek trial/license ke Supabase (1x/jam)
     │
     ▼
[Side Panel UI — Preact]
  - query IndexedDB
  - kalkulasi growth & engagement rate di client
  - render chart (uPlot)
     │
     ▼ (hanya device_id, install_date, license_key)
[Supabase Edge Functions]
  - /register-install
  - /validate
  - /activate-license (validasi ke Sejoi API)
```

---

## 2. Data yang Dikumpulkan

### Data Points

| Metrik | Raw | Growth/Trend |
|---|---|---|
| Follower | Count harian | +/- vs kemarin, 7 hari, 30 hari |
| View per post | Count per post | Avg view (minggu ini vs lalu) |
| Like per post | Count per post | Avg like (minggu ini vs lalu) |
| Comment per post | Count per post | Avg comment (minggu ini vs lalu) |
| Engagement rate | (like+comment)/view | Trend per periode |

### Kalkulasi Growth

```
Follower growth:
  - +127 hari ini
  - +843 minggu ini (+12.3%)
  - +2,341 bulan ini (+38.1%)

Avg engagement per post (7 hari terakhir):
  - View: 4,231 avg (+9% vs 7 hari sebelumnya)
  - Like: 284 avg (+18% vs 7 hari sebelumnya)
  - Comment: 43 avg (+5% vs 7 hari sebelumnya)
  - Engagement rate: 2.1% (+0.3%)
```

### Struktur IndexedDB

```
followers_history: [{ date, count }]
posts: [{ post_id, date, views, likes, comments, text_preview }]
```

### Scraping Strategy

- Aktif hanya di `threads.net` (permission minimal)
- Passive scraping — tidak ada request tambahan, hanya observasi DOM
- `MutationObserver` untuk deteksi konten baru saat scroll
- Deduplication by `post_id` sebelum simpan ke IndexedDB
- Follower snapshot 1x per hari (bukan per page load)
- Multiple fallback selector untuk mitigasi UI update Threads

### Fitur Top Posts (Viral Tracker)

Tampilkan post paling viral berdasarkan views, dengan sort options:
- Views (default)
- Likes
- Comments
- Engagement Rate

---

## 3. Freemium Gate & Trial System

### Tier

| Fase | Durasi | Akses |
|---|---|---|
| Trial | 3 hari pertama setelah install | Semua fitur Pro |
| Free (post-trial) | Setelah 3 hari | Fitur terbatas |
| Pro | Setelah aktivasi license | Semua fitur Pro |

### Fitur per Tier

| Fitur | Free | Pro |
|---|---|---|
| Follower growth (7 hari) | ✅ | ✅ |
| Follower growth (30 hari) | ❌ | ✅ |
| Like, comment, view stats | ✅ | ✅ |
| Top 3 viral posts | ✅ | ✅ |
| Top 10 viral posts | ❌ | ✅ |
| Engagement rate trend | ❌ | ✅ |
| Export CSV | ❌ | ✅ |
| Data history penuh (30 hari) | ❌ | ✅ |

### Trial Enforcement

- Install timestamp disimpan di Supabase (bukan localStorage — mudah di-reset)
- Device fingerprint: kombinasi browser UA + timezone + screen resolution
- Reinstall extension tidak reset trial (timestamp di backend)
- Hari ke-4: fitur Pro dikunci, tampil banner upgrade

---

## 4. License System

### Rules

- 1 license key = 1 device + 1 email
- Tidak bisa dipakai bersamaan di browser/device lain
- Transfer license: request ke support → manual reset device_id di Supabase → aktivasi ulang

### Aktivasi Flow

```
User beli di Sejoi
  → Xendit proses pembayaran
  → Sejoi generate license key → kirim ke email user
  → User input [email] + [license key] di extension
  → Extension → Supabase /activate-license
      - Validasi key ke Sejoi API
      - Bind device_id + email
      - Unlock Pro
```

### Anti-sharing

- Setiap validasi license kirim device_id terbaru ke backend
- Device_id mismatch → license dinonaktifkan otomatis + notif ke email terdaftar

### Tabel licenses (Supabase)

```
licenses: {
  id, key, email, device_id,
  activated_at, is_active,
  transfer_requested_at
}
```

> **Catatan:** Perlu konfirmasi bahwa Sejoi expose API untuk validasi license key secara programmatic. Jika tidak tersedia, fallback ke webhook atau validasi manual.

---

## 5. Side Panel UI

### Layout

```
┌──────────────────────────┐
│ 🧵 Threads Analytics     │
│ @username      [Trial: 2h│
├──────────────────────────┤
│ FOLLOWERS                │
│ 12,847  +127 hari ini    │
│ +843 minggu (+12.3%)     │
│ [chart 7 hari]           │
├──────────────────────────┤
│ ENGAGEMENT (avg/post)    │
│ 👁 4,231  💬 43  ❤️ 284  │
│ ER: 2.1% ▲ +0.3%        │
├──────────────────────────┤
│ 🔥 TOP POSTS             │
│ 1. [post preview] 24.8k  │
│ 2. [post preview] 18.2k  │
│ 3. [post preview] 11.9k  │
│ [Lihat semua →] 🔒       │
├──────────────────────────┤
│ [Upgrade ke Pro] [Export]│
└──────────────────────────┘
```

---

## 6. Distribution & Pricing

### Chrome Web Store

- Nama: **Threadlytics**
- Permissions: `tabs`, `sidePanel`, `storage` — hanya aktif di `threads.net`
- Privacy policy wajib (karena collect device ID)

### Pricing

| Tier | Harga | Model |
|---|---|---|
| Free | Rp 0 | Selamanya, fitur terbatas |
| Pro Monthly | Rp 49.000/bln | Subscription via Sejoi + Xendit |
| Pro Yearly | Rp 399.000/thn | ~32% lebih hemat, 1 license key |

### Go-to-Market

1. Soft launch → share di Threads @banirisset (built-in audience)
2. Minta review dari early adopters (boost Chrome Web Store ranking)
3. Affiliate/referral program via Sejoi

### Timeline MVP

| Fase | Scope |
|---|---|
| Week 1–2 | Extension scaffold + scraping + IndexedDB |
| Week 3 | Side panel UI + charts |
| Week 4 | Backend Supabase + trial/license system |
| Week 5 | Polish + Chrome Web Store submission |

---

## 7. Privacy & Data

Data yang keluar dari device user hanya:
1. Device ID + install date (trial enforcement)
2. Email + license key (aktivasi Pro)

Semua data analytics (follower, post stats) tersimpan lokal di browser user — tidak pernah dikirim ke server.

---

## Open Questions

- [ ] Apakah Sejoi expose API untuk validasi license key programmatic?
- [ ] Nama final extension (Threadlytics atau nama lain?)
- [ ] Bahasa UI extension: Indonesia atau Inggris?
