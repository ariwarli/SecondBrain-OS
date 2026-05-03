# Session Snapshot — Konteks Terkini

File ini berisi konteks temporal yang berubah per sesi.
Aturan permanen ada di `startup-template.md` — file ini tidak menduplikasi aturan dari sana.

## Who You Are Helping

- User: Bani Risset
- Main local workspace: `/Users/banirisset/2_Areas/banirisset`
- Primary operating interface: Telegram

## Memory Files

Tanggal memory file yang valid saat ini:

- `memory/2026-05-03.md` (Hari ini)
- `memory/2026-05-02.md`
- `memory/2026-05-01.md`

## Live Runtime Facts

- Main bot: `@survivorset_bot`
- Hermes Telegram runtime service: `hermes-gateway.service`
- Hermes live config path: `/home/hermes/.hermes`
- Hermes Telegram DM works
- Legacy `SecondBrain OS` `INBOX` topic is mapped to Hermes channel directory.

## Current Decisions

- 2026-05-03: `startup-template.md` di-refactor menjadi source of truth tunggal untuk cold boot. Aturan Read Order dan boundary dipertegas di satu file.
- 2026-05-03: `hermes.md` di-clean up menjadi lebih padat, menghindari tumpang tindih instruksi startup dengan `startup-template.md`.
- 2026-04-30: Repo hermes-agent berjalan di fork `ariwarli/hermes-agent`.
- 2026-04-30: python-pptx installed di VPS. Hermes bisa auto-deliver PPTX via `MEDIA:` tag.
- 2026-04-30: SSH locked down ke Tailscale only (`100.113.246.119:22`), user `banirisset`.

## Open Questions

- **Telegram client cache / Menu:** Apakah modifikasi `set_my_commands` dengan `scope=BotCommandScopeAllPrivateChats()` sudah fully resolving isu slash menu di client?
- Finalisasi bucket canon: Apakah `Sources` resmi masuk canon bucket atau tetap staging?

## Recent Incidents

### 2026-04-30 (Menu not fixed live)
- Telegram slash menu shows all commands. `delete_my_commands` + `set_my_commands` deployed but Telegram client cached.
- Decision: Use `scope=BotCommandScopeAllPrivateChats()` for reliable command setting.

### 2026-04-29 (Proton Pass CLI Setup)
- Proton Pass CLI terinstall via brew. Helper script: `ops/scripts/proton_pass_helper.py`. Menunggu interactive login `pass-cli login`.

## Save Session Protocol

Trigger: user bilang "Reed save session ini" atau variasi yang jelas.

Agent wajib lakukan:

1. **Refresh memory dates**: Update `Memory Files` dengan tanggal terbaru (today + yesterday). Update `memory/YYYY-MM-DD.md`.
2. **Sync incidents**: Baca `hermes.md` blok `GENERATED:INCIDENTS`. Append yang baru.
3. **Capture decisions**: Append keputusan operasional/penting ke blok `Current Decisions`.
4. **Update open questions**: Tambah/hapus open loops.
5. **Konfirmasi**: Balas "✅ Saved — [N] decisions, [N] incidents, [N] open questions"

## Mid-Task Save

Trigger: user minta save di tengah kerjaan.

Agent wajib lakukan:
1. Catat "Task interrupted" (Nama task, Status, Next steps).
2. Konfirmasi rencana resume ke user.
