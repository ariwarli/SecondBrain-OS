# Handoff Protocol - REED Multi-Agent

## Tujuan
Mencegah handoff ambigu dan bolak-balik antar bot.

## Format Wajib

Gunakan format ini setiap handoff:

```text
Context:
Task:
Deadline:
Done Criteria:
```

## Contoh

```text
Context: Topik content minta thread AI untuk UMKM.
Task: Buat draft 7 post thread sesuai voice Bani.
Deadline: Hari ini 18:00 WIB.
Done Criteria: Draft markdown siap publish + CTA final + status content queue terupdate.
```

## Rule Handoff
- Satu task punya satu owner bot.
- Handoff lintas domain wajib diketahui `main`.
- Kalau `Done Criteria` tidak jelas, task dikembalikan sebelum dieksekusi.

## Rule Completion
- Saat selesai, owner wajib kirim:
  - hasil ringkas 3-5 baris
  - path file output
  - blocker sisa (jika ada)
