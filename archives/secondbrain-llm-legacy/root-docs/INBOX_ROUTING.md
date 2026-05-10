# Inbox Routing Rules

File ini adalah **aturan utama** bagaimana REED + REED DULL memproses, mengklasifikasi, dan mengarsipkan semua yang masuk ke Inbox.

## Prinsip

> **User cuma kirim ke Inbox. REED yang mikir mau ditaruh di mana.**

User nggak perlu:
- Buka folder manual
- Ingat nama folder project
- Ketik `/route` atau command khusus
- Mikirin struktur arsip

Cukup: **kirim → lupa → REED yang handle.**

---

## Klasifikasi: 5 Bucket Utama

Setiap item yang masuk Inbox dikategorikan ke salah satu dari 5 bucket:

### 1. 🗂️ Project (Client atau Internal)
Item yang berkaitan dengan project aktif.

**Keywords pemicu:**
- Nama client (NIRVA, SentraChat, STOP TB, APPS, APPSSYNC, PT SIN)
- "project", "client", "brief", "deliverable", "deadline"
- "TOR", "proposal", "scope", "milestone"
- Nama internal project (Brand OS, Content OS, Ghostwriter, Tool Lab, PARA)

**Routing:**
- Client → `clients/<slug>/inbox/<YYYY-MM-DD>_<type>.md`
- Internal → `projects/<slug>/inbox/<YYYY-MM-DD>_<type>.md`

**Action:** Buat file baru atau append ke yang existing. Update `projects/PROJECTS.md` status.

---

### 2. 📝 Content (Konten untuk dipublish)
Item yang perlu jadi konten: Threads, LinkedIn, Instagram, blog, newsletter.

**Keywords pemicu:**
- "post", "thread", "linkedin", "instagram", "konten", "hook", "caption"
- "voice note", "voice memo", "rekam"
- "draft", "publish", "jadwal posting"
- Nama platform: "Threads", "LinkedIn", "IG"

**Routing:**
- Draft/post → `Brand OS - Bani Risset/content/drafts/<YYYY-MM-DD>_<platform>.md`
- Voice note transcription → `Brand OS - Bani Risset/content/inbox/<YYYY-MM-DD>_voice.md`
- Ide konten → `openclaw/secondbrain/content-ideas.md` (append)

**Action:** Kalau konten sudah siap → REED DULL auto-schedule ke content topic Telegram untuk nagger.

---

### 3. 👥 CRM (Orang/Relasi/Follow-up)
Item tentang orang: kontak baru, follow-up, meeting notes, deal tracking.

**Keywords pemicu:**
- Nama orang (DEDE, dll.)
- "meeting", "follow-up", "kontak", "deal", "client baru"
- "nanya", "nawarin", "proposal", "negosiasi"
- "overdue", "belum jawab", "ghosting"

**Routing:**
- Kontak baru → `crm.md` (tambah ke Key Relationships)
- Follow-up → `crm.md` (update Follow-Up Queue)
- Meeting notes → `clients/<slug>/notes.md` (kalau terkait client) atau `research/meetings/<YYYY-MM-DD>_<topic>.md`

**Action:** Kalau ada follow-up yang overdue → REED DULL kirim reminder di topic `personal-crm`.

---

### 4. 📋 Task (Aksi yang perlu dikerjakan)
Item yang butuh action >5 menit.

**Keywords pemicu:**
- "bikin", "buat", "kerjain", "selesaiin", "fix"
- "urgent", "deadline", "harus"
- "tolong", "bantu" + action verb
- "check", "audit", "review"

**Routing:**
- Task harian → `daily.md` (bagian Delegated To OpenClaw)
- Task project → `clients/<slug>/tasks.md` atau `projects/<slug>/tasks.md`
- Task technical/ops → `openclaw/ops/tasks.md`

**Action:** Kalau task >10 menit → REED delegate ke subagent atau queue ke overnight.

---

### 5. 📚 Knowledge vs 🔍 Research — BEDAKAN INI

**Knowledge-base (PASIF)** — referensi yang disimpan, tidak butuh action sekarang.

Keywords:
- URL/link (otomatis detect)
- "simpan", "bookmark", "referensi", "nanti dibaca"
- "tools", "resource", "template", "contoh"
- "tutorial", "guide", "doc", "dokumentasi"

Routing:
- Link/URL → `research/bookmarks/<YYYY-MM-DD>_<topic>.md` + forward ke Telegram topic `Knowledge-base` (topic 16)
- Dokumen penting → `research/docs/<slug>.md`
- Tool baru → `research/tools/<tool-name>.md`

Action: Kalau link → REED fetch summary singkat via `web_fetch`, simpan bersama link.

---

**Research (AKTIF)** — ada pertanyaan yang perlu dijawab, ada output yang diharapkan.

Keywords:
- "riset", "cari tau", "analisis", "compare", "audit"
- "gimana cara X", "apa bedanya X dan Y", "cari contoh X"
- "market research", "competitor", "benchmark"
- Task yang melibatkan reed-researcher

Routing:
- Brief riset → `research/<YYYY-MM-DD>_<topik>.md`
- Output reed-researcher → forward ke Telegram topic `Knowledge-base` (topic 16) dengan owner `reed-researcher`
- Kalau butuh web search → spawn reed-researcher

Action: REED delegate ke reed-researcher, output dikirim ke topic `Knowledge-base` agar tetap satu lane owner untuk knowledge + research.

---

## Routing Table: Claude Desktop Project ↔ OpenClaw Path

Ini mapping antara project di Claude Desktop ke folder di OpenClaw:

| Claude Desktop Project | OpenClaw Path | Telegram Topic |
|---|---|---|
| Brand OS - Bani Risset | `Brand OS - Bani Risset/` | `content` |
| Client OS - NIRVA APPS | `clients/nirva/` | `clients` |
| Client OS - SentraChat | `clients/sentrachat/` | `clients` |
| Client OS - STOP TB | `clients/stop-tb/` | `clients` |
| Client OS - APPS SCREANING | `clients/apps/` | `clients` |
| Client OS - APPSSYNC | `clients/appssync/` | `clients` |
| Client OS - PT SIN | `clients/pt-sin/` | `clients` |
| Content OS | `Brand OS - Bani Risset/content/` | `content` |
| Tools OS - CLAW | `openclaw/` | `ops` |
| Tools OS - PARA | `projects/para/` | `tasks` |
| Ghostwriter | `Brand OS - Bani Risset/ghostwriter/` | `content` |
| Tool Lab - Chrome Extension | `projects/tool-lab/chrome-ext/` | `tasks` |
| Tool Lab - WordPress OS | `projects/tool-lab/wordpress-os/` | `tasks` |
| Ops OS | `openclaw/ops/` | `ops` |

**Aturan:** Kalau user mention nama project → REED langsung tau folder tujuannya. Kalau nggak jelas → masuk ke `inbox/unsorted/` untuk triage manual maksimal 24 jam.

---

## Flow Lengkap: Inbox → Route → Archive

```
User kirim ke Inbox (Telegram)
        │
        ▼
REED baca pesan
        │
        ▼
Klasifikasi (5 bucket)
        │
        ├── 🗂️ Project → clients/ atau projects/ + update PROJECTS.md
        ├── 📝 Content → Brand OS/content/ + queue ke Content Nag
        ├── 👥 CRM → crm.md + set follow-up reminder
        ├── 📋 Task → daily.md atau project tasks.md
        ├── 📚 Knowledge (pasif) → Knowledge-base topic (16) + research/bookmarks/
        └── 🔍 Research (aktif) → Knowledge-base topic (16) + reed-researcher
        │
        ▼
        │
        ▼
REED DULL (kalau perlu):
- Set reminder/follow-up
- Queue content nag
- Schedule overnight task
```

---

## Format File Inbox Item

Setiap item yang masuk dari Inbox disimpen dengan format ini:

```markdown
# [Type] - [Brief Title]

**Source:** Inbox Telegram (via REED)
**Date:** YYYY-MM-DD HH:MM
**Original:** [quote pesan asli]

## Context
[Ringkasan/context tambahan]

## Action Items
- [ ] ...

## Status
- Routed to: [path/file]
- Processed: ✅/⏳
- Next: [apa selanjutnya]
```

---

## Unsorted Handling

Kalau REED nggak yakin klasifikasinya (confidence <70%):

1. Simpan ke `inbox/unsorted/<YYYY-MM-DD>_<id>.md`
2. Kalau butuh klarifikasi, balas singkat dan natural di Inbox: `"Ini belum cukup jelas. Gw taruh dulu di unsorted. Balas aja: project / content / crm / task / knowledge / research."`
3. Kalau user jawab → REED route ulang + tandai item unsorted selesai
4. Kalau user tidak jawab, REED DULL wajib triage backlog `unsorted` maksimal dalam 24 jam

---

## Daily Cleanup

Setiap jam 07:00, REED DULL:
1. Cek `inbox/unsorted/` — ada yang pending?
2. Cek apakah semua inbox item hari sebelumnya udah di-route
3. Kalau ada backlog `unsorted` >24 jam, kirim alert singkat ke topic `updates`

---

## Rules Tambahan

- **Jangan hapus** item dari Inbox sebelum di-route. Pindah, jangan hapus.
- **Jangan merge** item dari Inbox ke file yang sama tanpa context. Tiap item tetap punya file sendiri (kecuali ide konten yang boleh di-append ke list).
- **Timestamp wajib.** Tiap file inbox item harus punya tanggal+jam original.
- **Original message preserved.** Selalu quote pesan asli user biar context nggak hilang.
- **Reply confirmation.** REED dilarang mengirim konfirmasi routing di Inbox untuk route normal. REED harus langsung memberikan respon atau eksekusi di topik tujuan.
- **Token hygiene.** Hemat token hanya untuk chatter routing yang redundant. Jangan hemat context kalau itu bikin memory, handoff, atau workspace jadi bolong.
