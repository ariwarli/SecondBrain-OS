# Session Snapshot — Konteks Terkini

File ini berisi konteks temporal yang berubah per sesi.
Aturan permanen ada di `startup-template.md` — file ini tidak menduplikasi aturan dari sana.

## Who You Are Helping

- User: Bani Risset
- Main local workspace: `/Users/banirisset/2_Areas/banirisset`
- Primary operating interface: Telegram

## Memory Files

Tanggal memory file yang valid saat ini:

- `memory/2026-04-29.md`
- `memory/2026-04-28.md`

## Live Runtime Facts

- Main bot: `@survivorset_bot`
- Hermes Telegram runtime service: `hermes-gateway.service`
- Hermes live config path: `/home/hermes/.hermes`
- Hermes Telegram DM works
- Legacy `SecondBrain OS` `INBOX` topic has been restored into Hermes channel directory

Jika task menyentuh Telegram, Hermes, atau bot routing:
- validasi runtime live sebelum mempercayai asumsi lokal yang basi

## Current Decisions

- 2026-04-28: INBOX kept and intentional — fast capture surface for idea-heavy, forgetful user
- 2026-04-28: Task and daily recap are not canon wiki buckets
- 2026-04-28: Candidate canon buckets — Research, Frameworks, SOPs, Decisions, Incidents
- 2026-04-29: SPLIT — startup-template.md untuk aturan permanen, session-snapshot.md untuk konteks temporal
- 2026-04-29: Save session dipicu oleh user, format "Reed save session ini"
- 2026-04-29: Auto-update saat save — tanggal memory + incidents sync otomatis; decisions/open questions manual capture
- 2026-04-29: Incidents sync hanya saat ada incident baru yang belum ada di snapshot

## Open Questions

- Final canon bucket set is not locked yet
- `Sources` may or may not become an official canon bucket
- Boundary wording may later be promoted into canon docs

## Recent Incidents

### 2026-04-28 (Runtime Verification)

- runtime live terverifikasi adalah `hermes-gateway.service`, bukan `openclaw-gateway.service`
- config live terverifikasi ada di `/home/hermes/.hermes/.env` dan `/home/hermes/.hermes/config.yaml`
- bot aktif terverifikasi tetap `@survivorset_bot`
- legacy `INBOX` topic di `SecondBrain OS` terdaftar lagi di Hermes channel directory

### 2026-04-29 (Cleanup Rule)

- state `voice transcription disabled` dinyatakan stale; voice workflow aktif dan dipertahankan
- model mental `REED DULL` sebagai sistem kedua dinyatakan retired
- referensi `docs/openclaw-rules.md` dinyatakan stale; pakai path arsip bila perlu

### 2026-04-29 (Content Topic Runtime Fix)

- topic `content` di `SecondBrain OS` sekarang punya policy model `speedup-brand` pada fresh turn
- `/models` sekarang alias resmi dari `/model`

### 2026-04-29 (Proton Pass CLI Setup)

- Proton Pass CLI terinstall via `brew install protonpass/tap/pass-cli`
- GUI Proton Pass juga terinstall via `brew install --cask proton-pass`
- Helper script: `ops/scripts/proton_pass_helper.py`
- Status: CLI ready, menunggu user login interaktif (`pass-cli login`)

## Save Session Protocol

Trigger: user bilang "Reed save session ini" atau variasi yang jelas.

Agent wajib lakukan:

1. **Refresh memory dates**
   - Cek `memory/` untuk file terbaru (today + yesterday)
   - Update date references di bagian `Memory Files` atas
   - Update `memory/YYYY-MM-DD.md` kalau belum ada entry hari ini

2. **Sync incidents**
   - Baca blok `GENERATED:INCIDENTS` di `hermes.md`
   - Bandingkan dengan incidents yang sudah ada di snapshot ini
   - Append hanya yang baru, jangan replace semua

3. **Capture decisions**
   - Identifikasi keputusan penting dari conversation
   - Append ke `Current Decisions` dengan format: `- YYYY-MM-DD: SHORT_DESCRIPTION`
   - Jangan capture hal rutin atau trivial

4. **Update open questions**
   - Tambah pertanyaan baru kalau ada
   - Mark resolved: hapus dari list, tambah catatan kecil di decisions

5. **Opsional: update `startup-template.md`**
   - Hanya kalau aturan fundamental berubah (boundary, routing, read order)
   - Jarang terjadi

6. **Konfirmasi ke user**
   - Balas singkat: "✅ Saved — [N] decisions, [N] incidents, [N] open questions"