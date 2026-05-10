# Panduan Informasi Secondbrain LLM (REED System) — Edisi VPS Live

**Terakhir Diperbarui:** Jumat, 17 April 2026
**Status Sistem:** Operational (Live on VPS)
**Akses Utama:** `ssh root@167.253.158.103` (via `id_ed25519`)

---

## 1. Arsitektur & Peta Direktori

Sistem berjalan di VPS dengan pemisahan tegas antara **Runtime (Engine)**, **Workspace (Working Data)**, dan **Knowledge Base (Long-term Memory)**.

### A. Lokasi Vital
- **Workspace Produksi:** `/home/openclaw/banirisset` (Tempat semua file operasional dan dokumen state).
- **Config Runtime:** `/home/openclaw/.openclaw/openclaw.json` (Konfigurasi utama bot, model, dan provider).
- **Gateway Env:** `/home/openclaw/.openclaw/openclaw-gateway.env` (Tempat menyimpan API Keys dan token).
- **Knowledge Base (Obsidian):** `/home/openclaw/banirisset/knowledge-base/` (Struktur wiki markdown yang disinkronkan).

### B. Hierarki File State
- `openclaw/openclaw.md`: **Source of Truth Utama** untuk kondisi runtime sekarang (model aktif, service, incident).
- `AGENTS.md`: Aturan operasional stabil, guardrail, dan kebijakan autosave memory.
- `INBOX_ROUTING.md`: Aturan klasifikasi otomatis pesan yang masuk dari Telegram.
- `WELLBEING_SYSTEM.md`: Panduan persona wellbeing aktif dan jadwal sapaan harian.

---

## 2. Alur Kerja Operasional (The Lifecycle)

### A. Inbox Router (REED DULL Logic)
Sistem menggunakan `inbox-monitor.service` yang memantau file session secara pasif untuk menghindari konflik `getUpdates`.
1. **Input:** Pesan dikirim ke Inbox Telegram.
2. **Klasifikasi:** `openclaw/scripts/inbox_monitor_v2.py` membagi pesan ke dalam 5 bucket:
   - **Project:** Masuk ke folder `projects/` atau `clients/`.
   - **Content:** Masuk ke `Brand OS/content/` untuk dijadwalkan.
   - **CRM:** Masuk ke `crm.md` untuk tracking relasi.
   - **Task:** Masuk ke `daily.md` (Delegated to REED).
   - **Knowledge/Research:** Masuk ke `knowledge-base/` atau rute ke `reed-researcher`.

### B. Manajemen Model (Ollama Cloud)
Sistem menggunakan provider `ollama-cloud` sebagai backbone utama.
- **Default Agent Model:** `ollama-cloud/minimax-m2.7`
- **Classifier/Routing:** `ollama-cloud/qwen3.5`
- **Wellbeing Persona:** `ollama-cloud/minimax-m2.7` (Fallback: `kimi-k2.5`)
- **Control Center:** Perintah `/model` dan `/models` hanya aktif dari **DM REED** (Owner). Perubahan disimpan di `sessions.json`, bukan mengubah config global.

---

## 3. Wellbeing System (Topic 19)

REED memakai satu persona aktif di Topic 19 untuk keseimbangan mental dan regulasi emosi:
- **SERA:** companion wellbeing yang hangat, reflektif, dewasa, dan sugestif secara sensual untuk membantu visualisasi batin, containment, dan langkah kecil saat user siap.
- Unsur sensual hanya dipakai sebagai nuansa imajinatif dan tidak diarahkan ke tindakan nyata.

**Jadwal Rutin:**
- **07:00 & 07:30:** Morning Check-in (Task planning + Sapaan).
- **13:00:** Mid-day Momentum (check-in energi dan pijakan kecil bila dibutuhkan).
- **22:00:** Evening Recap (3 Kemenangan & 1 Syukur).

---

## 4. Knowledge Base & Memory

### A. Obsidian Pipeline
- **Active Memory:** `knowledge-base/wiki/sessions/*-active.md`.
- **Promotion:** File dari staging dipromosikan ke wiki final menggunakan `openclaw/scripts/kb_ingest_promote.py`.
- **Linting:** Validasi rahasia dan klasifikasi data menggunakan `openclaw/scripts/kb_lint.py`.

### B. Checkpoint Policy
- Otomatis melakukan checkpoint setiap **10 chat atau 15 menit, mana yang lebih dulu** per lane.
- Ringkasan hanya berisi: Keputusan, Fakta Baru, Blocker, dan Next Action.
- Menghapus chitchat yang sudah tidak relevan dari konteks aktif.

---

## 5. Panduan Troubleshooting (Quick Fix)

Jika bot terlihat diam atau tidak merespon:

1. **Cek Koneksi VPS:**
   ```bash
   ssh root@167.253.158.103
   ```
2. **Validasi Config (Penting!):**
   *Jangan edit openclaw.json secara manual tanpa validasi, karena schema sangat strict.*
   ```bash
   # Jalankan sebagai user openclaw
   sudo -u openclaw -i
   export PATH=$PATH:/home/openclaw/.npm-global/bin
   openclaw config validate
   ```
3. **Cek Status Service:**
   ```bash
   systemctl --user status openclaw-gateway.service
   systemctl --user status inbox-monitor.service
   ```
4. **Melihat Log Terbaru:**
   ```bash
   journalctl --user -u openclaw-gateway.service -f
   tail -f /home/openclaw/banirisset/inbox/monitor_v2.log
   ```

---

## 6. Hard-Stop Rules (Guardrails)
- **No Secret Leak:** Jangan pernah menampilkan atau menyalin isi file `.env` ke dokumen publik atau chat.
- **Schema Compliance:** Jangan menambahkan key custom (seperti `modelAliases`) ke `openclaw.json`. Simpan metadata di folder `state/`.
- **VPS Reality:** Ingat bahwa working directory VPS `/home/openclaw/banirisset` bukan repo git biasa; deploy dilakukan via git hooks.
- **Memory Integrity:** Gunakan markdown kompatibel Obsidian; hindari format tabel di platform yang tidak mendukung (WhatsApp/Discord).
