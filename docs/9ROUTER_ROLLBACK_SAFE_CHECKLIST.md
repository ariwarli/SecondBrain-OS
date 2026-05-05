# 9router Rollback-Safe Checklist

Tujuan checklist ini adalah memastikan migrasi provider wajib `9router` bisa diverifikasi, dijalankan, dan di-rollback dengan aman jika terjadi insiden.

## 1) Preflight Sebelum Deploy

- Pastikan env service terpasang:
  - `NINE_ROUTER_BASE_URL`
  - `NINE_ROUTER_API_KEY`
- Jalankan:
  - `python3 ops/scripts/model_routing_guardrail.py`
- Ekspektasi:
  - `"ok": true`
  - tidak ada `issues`

## 2) Smoke Test Jalur Live

- Jalankan:
  - `python3 ops/scripts/model_routing_smoke.py`
- Ekspektasi:
  - `"ok": true`
  - `status_code: 200`
  - `response_preview` terisi (contoh `OK`)

## 3) Verifikasi Runtime Spec dan Policy

- Cek status runtime:
  - `python3 ops/scripts/reed_runtime.py status`
- Ekspektasi:
  - `model_routing.mandatory_provider == "9router"`
- Pastikan policy tidak memuat marker legacy:
  - `speedup-brand`
  - `qwen3-coder:480b`
  - `ollama-cloud/`

## 4) Monitoring Pasca Deploy

- Pantau log untuk marker routing:
  - `Model routing marker: provider=... model=... base_url=...`
- Jika provider bukan `9router`, anggap incident dan hentikan rollout.

## 5) Rollback Aman (Jika Gagal)

- Kembalikan env service ke nilai terakhir yang diketahui sehat.
- Jalankan ulang guardrail + smoke sampai hijau.
- Restart service secara terkontrol sesuai SOP operasi.
- Simpan incident note berisi:
  - waktu kejadian
  - error utama
  - langkah rollback
  - status akhir verifikasi
