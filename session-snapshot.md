# Session Snapshot — Konteks Terkini

File ini berisi konteks temporal yang berubah per sesi.
Aturan permanen ada di `startup-template.md` — file ini tidak menduplikasi aturan dari sana.

## Who You Are Helping

- User: Bani Risset
- Main local workspace: `/Users/banirisset/2_Areas/banirisset`
- Primary operating interface: Telegram

## Memory Files

Tanggal memory file yang valid saat ini:

- `memory/2026-04-30.md`
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
- 2026-04-30: Repo hermes-agent di-fork ke ariwarli/hermes-agent karena push ke NousResearch gagal 403
- 2026-04-30: Merge upstream NousResearch/main → fork local (update besar, 387 file, 33900+ baris)
- 2026-04-30: VPS sync ke fork + restart gateway, checkout `3dde707c`
- 2026-04-30: Telegram slash menu showing all commands instead of /menu only — menu fix not complete, needs live investigation
- 2026-04-30: Menu cache fix skipped — user memilih skip clear client cache; next step: modifikasi code `set_my_commands` pakai `scope` supaya lebih reliable
- 2026-04-30: Bot sudah responsif dengan model `deepseek-v4-flash` — screenshot confirm bot reply panjang tentang auto-reminder
- 2026-04-30: Sesi ini tersimpan ditengah proses karena user meminta "save session" saat menu masih belum fixed
- 2026-04-30: python-pptx installed dan configured di VPS — Hermes sekarang bisa generate dan auto-deliver PPTX via `MEDIA:` tag tanpa manual user steps
- 2026-04-30: SSH locked down ke Tailscale only (`100.113.246.119:22`) — user non-root `banirisset` dibuat, public SSH refused
- 2026-04-30: Autonomy prompt fix — update `system_prompt` + `supplementary_prompt` di `config.yaml` supaya Hermes tahu dia running di VPS DeepThree dan wajib execute langsung tanpa kasih instruksi manual ke user

## Open Questions

- Final canon bucket set is not locked yet
- `Sources` may or may not become an official canon bucket
- Boundary wording may later be promoted into canon docs
- `/menu` “Menu closed” karena state launcher tidak persisten antara tombol “Close” dan command — user perlu ketik `/menu` lagi setelah close untuk membuka ulang
- ~~Model default sudah ada (`model.default`), tapi model besar (480b) membuat bot lambat — fix: ganti ke model lebih cepat (`deepseek-v4-flash`)~~ → **RESOLVED**
- **Telegram client cache**: Apakah perlu modifikasi `set_my_commands` pakai `scope=BotCommandScope*` supaya client selalu update?

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

### 2026-04-30 (Menu not fixed live)

- Telegram slash menu still shows all commands (/branch, /compress, etc), /menu sends closed message, code fix verified but not reflected in live bot
- Server-side fix (`delete_my_commands` + `set_my_commands`) deployed tapi client Telegram masih cache — user skip clear cache
- Decision: next step modifikasi code pakai `scope=BotCommandScopeAllPrivateChats()` agar lebih reliable

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

## Mid-Task Save

Trigger: user explicitly requests save during an in-progress task.

Agent wajib lakukan:

1. **Record task interruption**
   - Note the task that was in progress when save was requested
   - Include brief description of what was being done

2. **Plan resume**
   - Outline the next steps needed to resume the task after save
   - Note any dependencies or pending actions
   - Include this in the save confirmation message

Format catatan mid-task save:

```
- YYYY-MM-DD HH:MM: Task interrupted — [TASK NAME]
  - Status: [In progress / Pending / Blocked]
  - Next steps: [What needs to happen next]
  - Resume after save: [Yes / Pending user input]
```