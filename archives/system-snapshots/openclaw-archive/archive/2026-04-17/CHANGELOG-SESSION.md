# Changelog Session

**Tanggal:** 2026-04-17

Dokumen ini merangkum perubahan utama yang dibangun selama sesi ini.

## 1. Proactive Engine Live

Proactive Engine sudah dibangun dan diverifikasi di VPS untuk workflow nudge proaktif REED.

Komponen yang aktif:

- morning brief harian jam `08:00 WIB`
- weekly gap report tiap `Jumat 17:00 WIB`
- pulse scan berkala untuk stale task + CRM overdue

Service/timer yang dipasang:

- `reed-dull-morning-brief.service`
- `reed-dull-morning-brief.timer`
- `reed-dull-proactive-pulse.service`
- `reed-dull-proactive-pulse.timer`
- `reed-dull-weekly-gap.service`
- `reed-dull-weekly-gap.timer`

Outcome:

- scheduler hidup
- detector hidup
- dispatcher hidup
- dedupe/rate-limit state tersimpan di runtime VPS

## 2. Detector and Dispatcher Rules

Deteksi yang dikunci:

- stale task `> 3 hari`
- CRM follow-up `> 48 jam`
- unsorted inbox `> 24 jam`

Format dispatch:

- nudge maksimum 3 baris
- satu pesan per item dalam cooldown window
- state anti-annoying disimpan di `proactive_engine_state.json`

## 3. Classifier Tuning

Routing `Task` vs `Content/Project` dirapikan supaya false positive turun.

Perubahan utama:

- keyword content ditambah untuk sinyal seperti `ide konten`
- ambiguitas `Task` dengan sinyal non-task sekarang dipaksa turun confidence
- pesan borderline diarahkan ke jalur LLM/fallback, bukan langsung dianggap `Task`

File yang terdampak:

- `scripts/inbox_monitor_v2.py`
- `scripts/tests/test_secondbrain_runtime.py`

Hasil verifikasi:

- runtime tests di VPS `PASS`
- sample ambigu seperti `tolong cek ide konten ini...` tidak lagi jatuh ke `Task`

## 4. Model Per Use Case

Sistem model routing per use case ditambahkan dan diaktifkan.

File utama:

- `scripts/model_router.py`
- `scripts/tests/test_model_router.py`

Use case yang di-handle:

- `classifier`
- `wiki_ingest`
- `reed_dm`
- `wellbeing`

Perubahan integrasi:

- `inbox_monitor_v2.py` membaca classifier model dari router
- `session_checkpoint_worker.py` menulis log model wiki yang dipakai saat runtime

## 5. Auto Resolver Model

Resolver model otomatis ditambahkan supaya sistem bisa pakai exact target model bila endpoint sudah support, dan fallback ke tag yang terbukti hidup bila exact tag gagal.

Perilaku final:

- probe live ke endpoint cloud sebelum memilih model
- exact tag diprioritaskan
- fallback dipilih dari kandidat lain yang juga lolos probe
- cache stale tidak lagi mengunci hasil lama secara default

Verifikasi runtime terakhir:

- `classifier` resolve ke `ollama-cloud/qwen3.5`
- `wiki_ingest` resolve ke `ollama-cloud/qwen3.5`
- `reed_dm` default diarahkan ke `ollama-cloud/minimax-m2.7`
- `wellbeing` default diarahkan ke `ollama-cloud/minimax-m2.7`

Catatan penting:

- beberapa tag yang muncul di katalog cloud tidak diterima sebagai exact ID oleh endpoint saat dites
- resolver sekarang menangani mismatch katalog vs exact runtime tag secara otomatis

## 6. Runtime Verification

Verifikasi operasional yang dilakukan di VPS:

- compile script Python: `PASS`
- unit tests `test_model_router` + `test_secondbrain_runtime`: `PASS`
- `openclaw-gateway.service`: aktif
- `inbox-monitor.service`: aktif
- `session-checkpoint.service`: aktif saat dipanggil
- log checkpoint menulis model wiki aktif terbaru

## 7. Operational Outcome

Sistem sekarang punya:

- proactive reminder engine yang jalan live
- classifier yang lebih bersih untuk inbox routing
- model routing per use case
- auto resolver yang tahan mismatch tag model
- audit trail session yang tersimpan di archive harian
