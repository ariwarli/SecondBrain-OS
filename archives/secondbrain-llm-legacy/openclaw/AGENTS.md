# OpenClaw Subtree Guide

Scope file ini khusus untuk pekerjaan di `openclaw/`.

## Source of Truth (urut pakai)
- `openclaw/openclaw.md` untuk state runtime aktif, model, boundary, dan incident terbaru.
- Runtime VPS menang atas dokumen: cek langsung jika ada konflik (`/home/openclaw/.openclaw/openclaw.json`, `/home/openclaw/.openclaw/openclaw-gateway.env`).
- `openclaw/openclaw-rules.md` hanya untuk aturan operasional yang relatif stabil.
- `openclaw/openclaw.json.remote` adalah template referensi, bukan config live.

## Startup Minimum
- Baca berurutan: `openclaw/SOUL.md` -> `openclaw/USER.md` -> `openclaw/openclaw.md`.
- `openclaw/openclaw-rules.md` hanya load jika task butuh aturan detail eksekusi.
- Jangan load semua docs di `openclaw/docs/` kecuali dibutuhkan untuk task spesifik.

## Startup Decision Gate
- Kalau dokumen berbeda dengan kondisi sistem, verifikasi dulu runtime VPS sebelum eksekusi.
- Gunakan bukti minimum ini sebelum klaim status: `openclaw config validate`, status service relevan, dan log terbaru.
- Jangan bilang "sudah beres" tanpa output command yang fresh di sesi yang sama.
- Jangan menulis key custom ke `~/.openclaw/openclaw.json`; config live harus tetap strict-schema. Alias model, cache resolver, dan metadata eksperimen simpan di `state/` atau dokumen ops, bukan config runtime.

## VPS Reality (jangan salah asumsi)
- Workspace produksi: `/home/openclaw/banirisset`.
- Deploy flow: bare repo `/home/openclaw/banirisset.git` dengan `hooks/post-receive` yang checkout ke working dir.
- Jangan asumsikan working dir VPS adalah git repo biasa (`.git` tidak ada di `/home/openclaw/banirisset`).

## Inbox Router Facts
- Router aktif: `openclaw/scripts/inbox_monitor_v2.py`.
- Mekanisme: baca session JSONL (`reed-archivist`) dan kirim `sendMessage/copyMessage`; bukan `getUpdates` untuk routing utama.
- Service unit ada di `openclaw/scripts/inbox-monitor.service` (daemon polling default 20 detik).
- Ubah keyword/path routing hanya di `RULES` dalam `openclaw/scripts/inbox_monitor_v2.py`.
- Router hanya membuat marker di `inbox/processed/`; jangan jadikan processed marker sebagai final knowledge.

## Knowledge-Base Promotion Pipeline
- Final knowledge dipromosikan dari `inbox/processed/*.md` memakai `openclaw/scripts/kb_ingest_promote.py`.
- Promoter menulis ke `knowledge-base/wiki/{notes,projects,decisions,references,research,meetings,templates}/`, membuat raw copy, update index/log, dan mencatat state idempotent.
- `Task` dan `Unsorted` tidak dipromosikan otomatis kecuali diarahkan eksplisit ke knowledge-base.
- Reusable template seperti response, SOP snippet, dan format balasan masuk `knowledge-base/wiki/templates/`.
- Data wellbeing/personal/restricted harus diskip kecuali ada approval eksplisit user.
- Gunakan `openclaw/scripts/kb_lint.py` untuk cek final note sebelum klaim KB sehat.
- Jangan masukkan RAG/vector DB/n8n sebagai dependency aktif kecuali sudah ada implementasi runtime yang terverifikasi.

## Commands Yang Sering Benar
- Cek monitor: `systemctl --user status inbox-monitor.service --no-pager`
- Restart monitor: `systemctl --user restart inbox-monitor.service`
- Log monitor: `tail -f /home/openclaw/banirisset/inbox/monitor_v2.log`
- Cek validitas config OpenClaw: `openclaw config validate`
- Dry-run KB promotion: `python3 openclaw/scripts/kb_ingest_promote.py --kb-root /home/openclaw/banirisset/knowledge-base --pending-dir /home/openclaw/banirisset/inbox/processed --pending --dry-run`
- Lint KB final notes: `python3 openclaw/scripts/kb_lint.py --kb-root /home/openclaw/banirisset/knowledge-base`

## No-Assumption Runtime
- Jangan asumsi `openclaw-gateway.service` atau service lain pasti aktif; cek status dulu sebelum restart atau diagnosis.
- Untuk operasi gateway, mulai dari validasi config + status runtime, lalu ambil aksi paling kecil yang perlu.
- Jika bot terlihat diam tapi service lain sehat, prioritaskan diagnosis gateway schema/config lebih dulu sebelum utak-atik router atau Telegram lane.

## ClawHub Approval Gate
- Install dari ClawHub harus lewat approval gate: `openclaw/scripts/clawhub_approval.py`.
- Format approval wajib exact (case-sensitive):
  - `APPROVE SKILL <slug> <version>`
  - `APPROVE PLUGIN <slug> <version>`
- Token approval bersifat single-use, ada TTL, dan terikat ke kombinasi `kind+slug+version`.
- Hard-stop rule: kalau approval tidak ada / expired / sudah dipakai, instalasi wajib batal.

## ClawHub Autonomous Installer
- Gunakan `openclaw/scripts/clawhub_installer.py` untuk mengelola siklus hidup instalasi:
  1. **Propose:** Jalankan `python3 clawhub_installer.py propose --slug <slug>` untuk mendapatkan metadata, analisis risiko, dan perintah persetujuan.
  2. **Safety Check:** Installer secara otomatis memverifikasi:
     - **Source Allowlist:** Hanya `https://clawhub.ai` yang diperbolehkan.
     - **Version Pinning:** Versi wajib mengikuti format SemVer (misal: `1.2.3`).
  3. **Human Approval:** Laporkan hasil `propose` (termasuk `risk_level`) ke user dan tunggu perintah `APPROVE ...` yang sesuai.
  4. **Install:** Setelah mendapatkan token, jalankan `python3 clawhub_installer.py install --slug <slug> --token <token>`.
     - **High-Risk Escalation:** Jika `risk_level` adalah **HIGH**, kamu WAJIB menambahkan flag `--confirm-high-risk` saat menjalankan perintah `install`.
  5. **Promotion:** Setelah `install` berhasil ke staging, jalankan `python3 clawhub_installer.py promote --staging-path <path>` untuk memindahkan artifact ke lokasi produksi operasional.
  6. **Verification:** Installer akan otomatis melakukan *smoke test* di area `staging/` sebelum instalasi dinyatakan selesai.

## Capabilities & Integrations
- **ClawHub Autonomous Installer:** REED can discover, analyze (risk level), and install skills/plugins with human approval.
- **Ollama Cloud Integration:** Runtime aktif memakai provider `ollama-cloud` via `https://ollama.com/v1` dengan API `openai-completions`.
  - Jangan asumsi ID model pendek di config lama valid di runtime; verifikasi ke endpoint live atau log gateway.
- **DM Model Control (REED Control Center):**
  - `/model` dan `/models` untuk kontrol model sekarang aktif **hanya dari DM REED** (owner `163335047`).
  - Perintah ini **tidak boleh** menulis `agents.defaults.model` di `openclaw.json`.
  - Perubahan model disimpan di session target (`sessions.json`) via `modelOverride` + `modelControl`.
  - Target v1: `wellbeing` -> session key `agent:reed-wellbeing:telegram:group:-1003344368011:topic:19`.
  - Pool wellbeing v1:
    - `ollama-cloud/minimax-m2.1`
    - `ollama-cloud/kimi-k2:1t`
    - `ollama-cloud/kimi-k2-thinking`
- **Auto-Rotate:**
  - Mode `auto` rotasi antar model pool saat kegagalan provider/model berlanjut > 60 detik.
  - State rotasi disimpan di session target (bukan config global).
  - Manual override via DM tetap bisa (`/model wellbeing <provider/model>`), reset ke auto via `/model wellbeing auto`.

## Session Log (April 16, 2026)
- Implementasi live dilakukan dengan patch file dist OpenClaw di VPS (bukan repo lokal source):
  - `/home/openclaw/.npm-global/lib/node_modules/openclaw/dist/commands-models-DgtNKT2D.js`
  - `/home/openclaw/.npm-global/lib/node_modules/openclaw/dist/commands-handlers.runtime-CrpNMDpp.js`
  - `/home/openclaw/.npm-global/lib/node_modules/openclaw/dist/agent-command-BUw17dbz.js`
- Backup dibuat sebelum patch (`*.bak-20260416-0842`) dan service direstart sehat.
- Verifikasi penting yang sudah terbukti:
  - Command DM model-control berjalan (`/model wellbeing ...`, `/models wellbeing`).
  - Perubahan tersimpan di `/home/openclaw/.openclaw/agents/reed-wellbeing/sessions/sessions.json`.
  - `openclaw.json` tetap tidak berubah byte-for-byte.
- Catatan operasional:
  - Karena patch di `dist`, update npm package OpenClaw bisa overwrite perubahan ini.
  - Setelah upgrade OpenClaw, fitur DM model-control harus diverifikasi ulang.
- Update blueprint-hardening yang sudah diverifikasi live:
  - Routing Inbox dikunci ulang:
    - `Research` tidak pakai topic terpisah; sementara share owner lane `Knowledge-base` (topic 16).
    - Route normal tidak perlu kirim konfirmasi ulang di Inbox.
    - `unsorted` wajib punya SLA triage `<24 jam`.
  - Router runtime `openclaw/scripts/inbox_monitor_v2.py` sudah diupdate:
    - tambah bucket `Research`
    - tambah file `inbox/unsorted/*.md` dengan status `pending-triage`
    - hapus reply konfirmasi routing normal di Inbox
  - Artefak knowledge-base yang sekarang wajib ada:
    - `knowledge-base/state/control-tower.md`
    - `knowledge-base/state/weekly-review.md`
    - `knowledge-base/wiki/page-template.md`
    - `knowledge-base/wiki/ingest-checklist.md`
    - `knowledge-base/wiki/wiki-lint-weekly-checklist.md`
  - Hygiene live yang sudah dibenahi:
    - `openclaw.json.remote` di live root + workspace `reed-archivist` kembali pakai env placeholder untuk token runtime, bukan literal hardcoded.
    - `/home/openclaw/.openclaw/workspaces/reed-archivist/openclaw/ops/openclaw-providers.env` tidak lagi jadi source secret aktif dan Notion dimatikan dari file aktif.
  - Verifikasi yang sudah terbukti di sesi ini:
    - `python3 -m unittest openclaw/scripts/tests/test_secondbrain_runtime.py` -> 3 test pass
    - `python3 -m py_compile openclaw/scripts/inbox_monitor_v2.py` lokal + live -> pass
    - `inbox-monitor.service` aktif setelah restart
    - `session-checkpoint.timer` aktif
  - Residual risk yang belum ditutup:
    - repo `knowledge-base/` di VPS masih dirty, jadi audited git sync belum selesai end-to-end
    - backup/archive lama masih bisa memuat secret lama; jangan anggap target incident = 0 sebelum artefak lama dibersihkan

## Memory Policy (Obsidian-Only)
- Notion dinonaktifkan dari workspace aktif. Memory resmi hanya lewat markdown yang kompatibel Obsidian.
- Source of truth memory: `knowledge-base/` (struktur wiki markdown).
- Urutan recall saat **mulai sesi baru** atau saat lane aktif dibuka lagi:
  1. baca `knowledge-base/wiki/sessions/*-active.md` untuk lane tersebut sebagai memory aktif utama
  2. baca `knowledge-base/wiki/index.md` untuk peta layer sistem / governance
  3. baca `knowledge-base/wiki/log.md` jika perlu tahu perubahan terbaru atau audit trail
  4. buka file checkpoint spesifik di `knowledge-base/wiki/sessions/*.md` hanya jika active context tidak cukup atau butuh detail histori
- Kontrak file memory:
  - `*-active.md` = current working memory
  - `wiki/index.md` = map / directory
  - `wiki/log.md` = timeline / recent changes
  - `sessions/*.md` = history snapshots
  - `wiki/{notes,projects,decisions,references,research,meetings,templates}/` = final knowledge hasil promosi, bukan raw transcript
- Jangan auto-load transcript lama, dump chat panjang, atau semua checkpoint historis saat start-of-session. Naik ke histori hanya jika benar-benar perlu.
- Checkpoint **otomatis** wajib jalan tiap 20 chat per session lane (contoh: DM REED, topic tertentu) tanpa perintah manual user.
  - Trigger berbasis counter session internal, bukan command manual.
  - User tidak perlu mengetik "save"/"checkpoint".
  - Saat counter mencapai 20, REED langsung simpan ringkasan dan reset counter untuk batch berikutnya.
- Format checkpoint tetap ringkas:
  - ringkas hanya: keputusan, fakta baru, blocker, next action.
  - hindari menyalin percakapan mentah panjang.
- Saat checkpoint, buang konteks yang sudah tidak relevan dari ringkasan aktif:
  - hapus item yang selesai/obsolete/duplikat.
  - pertahankan hanya konteks yang masih berdampak ke eksekusi saat ini.
- Update `*-active.md` hanya jika ada perubahan pada keputusan, blocker, atau next action yang masih aktif sekarang.
- Jika informasi baru hanya menambah histori tanpa mengubah current state, cukup simpan ke checkpoint / log tanpa memperpanjang active context.
- Jika butuh histori penuh, simpan di arsip terpisah; jangan campur dengan ringkasan konteks aktif.
- Autosave policy:
  - update `openclaw.md` hanya untuk snapshot state aktif yang memang berubah sekarang
  - update `AGENTS.md` hanya untuk rule/policy yang stabil dan lintas sesi
  - jangan auto-write transcript, command log, atau progress mentah ke dua file ini
  - bila perubahan penting terlalu panjang, ringkas ke `archive/YYYY-MM-DD/CHANGELOG-SESSION.md` dan prune section lama dulu
- Anti-bloat rule:
  - generated sections harus overwrite, bukan append bebas
  - incident/session log lama wajib dipindah ke archive kalau sudah tidak relevan untuk startup
  - `openclaw.md` dan `AGENTS.md` harus tetap layak dibaca saat boot tanpa scrolling berlebihan

## Autosave Decision Tree
- Pertanyaan 1: "Apakah ini benar sekarang dan perlu diketahui saat boot?"
  - Jika ya, update `openclaw.md`.
- Pertanyaan 2: "Apakah ini aturan umum yang harus berlaku lintas sesi?"
  - Jika ya, update `AGENTS.md`.
- Pertanyaan 3: "Apakah ini hanya hasil kerja, diagnosis, atau progress sesi ini?"
  - Jika ya, update `CHANGELOG-SESSION.md`.
- Kalau sebuah update tidak jelas masuk mana, default jatuh ke changelog, bukan ke core docs.

## Core Doc Write Rules
- `openclaw.md` hanya boleh berisi current operating state:
  - service aktif
  - current runtime shape
  - current model strategy
  - current resolver/source-of-truth location
  - incident terbaru yang masih relevan ke startup
- `openclaw.md` dilarang berisi:
  - transcript
  - session progress
  - unresolved diagnosis
  - dump config mentah
  - historical notes yang tidak lagi mempengaruhi boot
- `AGENTS.md` hanya boleh berisi stable operating rules:
  - source-of-truth order
  - startup verification rules
  - schema/config safety rules
  - autosave boundary rules
  - runtime verification policy
- `AGENTS.md` dilarang berisi:
  - PID sementara
  - workaround harian
  - status service hari ini
  - session log rutin
  - state eksperimen temporer

## Deterministic Write Modes
- `openclaw.md` = overwrite generated state block atau prune incident window.
- `AGENTS.md` = surgical edit ke rule yang memang berubah.
- `CHANGELOG-SESSION.md` = append.
- Jangan append bebas ke `openclaw.md`.
- Jangan append "session update" ke `AGENTS.md`.

## Promotion Threshold
- Update hanya boleh naik ke `openclaw.md` jika sudah terjadi di runtime nyata dan sudah diverifikasi dengan command fresh.
- Update hanya boleh naik ke `AGENTS.md` jika bukan workaround sementara dan masih akan benar di sesi berikutnya.
- Kalau belum lolos syarat itu, simpan ke changelog saja.

## Canonical Examples
- "gateway sekarang aktif sebagai systemd user service" -> `openclaw.md`
- "metadata resolver tidak boleh masuk openclaw.json" -> `AGENTS.md`
- "tadi gateway crash karena modelAliases" -> detail ke `CHANGELOG-SESSION.md`, hanya mitigasi final ringkas ke core docs
- "sedang investigasi kenapa bot lambat" -> jangan masuk core docs

## Security & Hygiene
- Jangan commit atau tampilkan secret dari file env (contoh `openclaw/ops/openclaw-providers.env`).
- Anggap token/API key di script lama sebagai debt; jangan direplikasi ke file baru.
- Abaikan artefak non-source (`__pycache__/`, `.DS_Store`, file backup `.bak*`) kecuali task memang cleanup.
