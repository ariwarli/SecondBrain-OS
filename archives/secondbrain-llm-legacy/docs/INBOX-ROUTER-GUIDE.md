# REED Inbox Router — Panduan Lengkap
**Last updated:** 2026-04-10

---

> Posisi dokumen ini: panduan khusus **mekanisme Inbox router**.
>
> Untuk panduan utama cara ngobrol dengan REED per topic, baca:
> - [REED-INTERACTION-GUIDE.md](/Users/banirisset/banirisset/openclaw/docs/REED-INTERACTION-GUIDE.md)
> - [REED-STARTER-TEMPLATES.md](/Users/banirisset/banirisset/openclaw/docs/REED-STARTER-TEMPLATES.md)
> - [TELEGRAM-TOPIC-CHEAT-SHEET.md](/Users/banirisset/banirisset/openclaw/docs/TELEGRAM-TOPIC-CHEAT-SHEET.md)

## Cara Pakai (Daily Workflow)

**Cukup kirim pesan ke topic `Inbox` di SecondBrain OS.**

Dalam ~20 detik, muncul konfirmasi:
```
✅ [ROUTED → Project]
📂 clients/stop-tb/
💬 Forwarded ke topic tasks
```

Selesai. Tidak perlu pilih folder, tidak perlu ingat nama topic.

---

## Bagaimana Cara Kerjanya

```
Kamu kirim pesan ke Inbox (topic 11)
          ↓
reed-archivist merespons (OpenClaw sub-agent)
          ↓
inbox_monitor_v2.py polling tiap 20 detik
  - Baca dari session file (BUKAN getUpdates — no conflict)
          ↓
Classify → 5 bucket
          ↓
copyMessage ke topic tujuan + reply konfirmasi
```

---

## 5 Bucket Klasifikasi

| Bucket | Topic Tujuan | Contoh Keyword |
|--------|-------------|----------------|
| **Project** | tasks (10) | nirva, sentrachat, stop tb, apps, appssync, pt sin, brand os, deadline, brief, TOR |
| **CRM** | personal-crm (9) | follow-up, meeting, dede, deal, negosiasi, ghosting |
| **Content** | content (3) | thread, post, linkedin, draft, hook, caption, utas, carousel |
| **Task** | tasks (10) | bikin, buat, kerjain, fix, urgent, audit, review |
| **Knowledge** | knowledge-base (16) | URL/link, simpan, bookmark, referensi, tutorial, tools |

Kalau tidak ada yang cocok → reply ❓, minta pilih manual.

---

## Mapping Project → Path

| Lo bilang... | Path | Topic |
|---|---|---|
| "NIRVA" | `clients/nirva/` | tasks |
| "SentraChat" | `clients/sentrachat/` | tasks |
| "STOP TB" / "StopTB" / "Dede" | `clients/stop-tb/` | tasks |
| "APPS" | `clients/apps/` | tasks |
| "APPSSYNC" | `clients/appssync/` | tasks |
| "PT SIN" | `clients/pt-sin/` | tasks |
| "Brand OS" / "konten" | `Brand OS - Bani Risset/` | content |

---

## Tips Biar Routing Akurat

- Sebut nama project/client secara eksplisit: "StopTB", "NIRVA", "PT SIN"
- Kalau content: sebut "thread", "draft", "utas"
- Kalau CRM: sebut nama orang atau "follow up"
- Ada URL → otomatis masuk Knowledge

---

## Quick Commands (dari Mac)

```bash
# Cek status inbox monitor
ssh openclaw "XDG_RUNTIME_DIR=/run/user/1001 systemctl --user status inbox-monitor.service --no-pager"

# Lihat log live
ssh openclaw "tail -f /home/openclaw/banirisset/inbox/monitor_v2.log"

# Restart inbox monitor
ssh openclaw "XDG_RUNTIME_DIR=/run/user/1001 systemctl --user restart inbox-monitor.service"

# Restart REED
ssh openclaw "XDG_RUNTIME_DIR=/run/user/1001 systemctl --user restart openclaw-gateway.service"

# Cek inbox processed
ssh openclaw "ls -lt /home/openclaw/banirisset/inbox/processed/ | head -10"
```

---

## Troubleshooting

### Routing tidak muncul setelah 30 detik?
```bash
# Cek service masih jalan
ssh openclaw "XDG_RUNTIME_DIR=/run/user/1001 systemctl --user status inbox-monitor.service"

# Kalau stopped → restart
ssh openclaw "XDG_RUNTIME_DIR=/run/user/1001 systemctl --user restart inbox-monitor.service"
```

### Routing salah bucket?
Tambah/edit keyword di `inbox_monitor_v2.py`, section `RULES`.
Setelah edit — pakai git sync (lebih aman dari scp):
```bash
cd ~/banirisset && git add openclaw/scripts/inbox_monitor_v2.py && git commit -m "fix: update routing rules" && git push vps main
ssh openclaw "XDG_RUNTIME_DIR=/run/user/1001 systemctl --user restart inbox-monitor.service"
```

### Mau reset (proses ulang semua pesan lama)?
```bash
ssh openclaw "rm /home/openclaw/banirisset/inbox/.monitor_v2_state.json"
```
⚠️ Semua pesan lama akan dapat routing confirmation lagi.

### Tambah client/project baru?
1. Buat folder lokal: `mkdir -p ~/banirisset/clients/[nama]/`
2. Tambah keyword di `RULES` → `inbox_monitor_v2.py`
3. Tambah entry di `path_map`
4. `git push vps main` + restart inbox-monitor

---

## File Penting

| File | Lokasi (VPS) | Fungsi |
|------|-------------|--------|
| Script router | `openclaw/scripts/inbox_monitor_v2.py` | Logika classify + routing |
| Systemd service | `~/.config/systemd/user/inbox-monitor.service` | Auto-start + restart |
| State file | `inbox/.monitor_v2_state.json` | Track message IDs yang sudah diproses |
| Log | `inbox/monitor_v2.log` | Semua aktivitas routing |
| Processed | `inbox/processed/` | Arsip markdown per pesan |

**Lokal (Mac):**
- `~/banirisset/openclaw/scripts/inbox_monitor_v2.py`
- `~/banirisset/openclaw/scripts/inbox-monitor.service`

---

## Topic IDs Reference

| Topic | Thread ID |
|-------|-----------|
| Inbox | 11 |
| Tasks | 10 |
| Personal CRM | 9 |
| Content | 3 |
| Ops | 27 |
| Knowledge Base | 16 |
| Updates | 13 |

---

## Kenapa Pakai File-based (Bukan Polling Telegram)?

Telegram hanya izinkan **1 consumer `getUpdates`** per bot token.
REED sudah pakai token itu → conflict kalau ada script lain yang juga polling.

**Solusi:** `inbox_monitor_v2.py` baca dari session JSONL yang sudah ditulis OpenClaw.
Script hanya pakai `sendMessage` + `copyMessage` untuk balas → tidak conflict sama sekali.

---

## Ringkasan Singkat

- Kalau tidak yakin kirim ke mana, kirim ke `Inbox`
- Kalau sudah yakin lane-nya, kirim langsung ke topic yang relevan
- Dokumen ini fokus pada router `Inbox`, bukan panduan utama semua topic
