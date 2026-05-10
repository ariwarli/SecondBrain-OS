# Panduan Instalasi Agent Business Productivity

Panduan ini untuk setup agent pada Business Productivity Layer agar siap jalan di atas infrastruktur existing (VPS shared, Telegram bot shared, Retrieval API existing, vault Obsidian shared).

## 1) Tujuan dan Scope

- Menyiapkan komponen agent execution tanpa membuat stack terpisah.
- Menjaga prinsip: no new LLM pipeline, retrieval-first, audit-ready.
- Menjamin setup siap masuk status operasional `Full GO` setelah verifikasi.

## 2) Prasyarat

Pastikan prasyarat berikut sudah tersedia:

- VPS shared aktif dan bisa diakses.
- PostgreSQL existing aktif.
- Retrieval API existing aktif.
- Telegram bot existing aktif.
- Vault Obsidian shared tersedia dan bisa diakses dari VPS.
- Kredensial environment sudah disiapkan (jangan hardcode di repo).

## 2.1) Instalasi Hermes Agent dari Source (Official)

Source resmi:

- `https://github.com/NousResearch/hermes-agent`

Pilih salah satu metode berikut.

### Opsi A - Quick Install (Direkomendasikan untuk runtime)

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.zshrc
hermes
```

Catatan:

- Untuk shell `bash`, gunakan `source ~/.bashrc`.
- Windows native tidak didukung; gunakan WSL2.

### Opsi B - Install dari source repo (setup script)

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
./setup-hermes.sh
./hermes
```

Script ini melakukan:

- install `uv`,
- membuat virtual environment,
- install dependency `.[all]`,
- membuat symlink `~/.local/bin/hermes`.

### Opsi C - Install manual dari source (full control)

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"
python -m pytest tests/ -q
./hermes
```

### Verifikasi instalasi Hermes

Setelah instalasi, pastikan command berikut berjalan:

```bash
hermes --help
hermes doctor
hermes setup
```

Checklist:

- [ ] Binary `hermes` tersedia di shell.
- [ ] `hermes doctor` tidak menunjukkan error kritikal.
- [ ] Setup wizard selesai.
- [ ] Model dapat dipilih via `hermes model`.
- [ ] Gateway dapat dikonfigurasi via `hermes gateway`.

### Migrasi dari OpenClaw (opsional)

Jika sebelumnya memakai OpenClaw:

```bash
hermes claw migrate --dry-run
hermes claw migrate
```

Gunakan mode `--dry-run` dulu untuk memastikan item yang dimigrasikan aman.

## 3) Struktur Komponen Agent

Komponen minimal yang harus aktif:

- `BusinessExecutionAPI`
- `DailyContentFactory`
- `FunnelPlannerEngine`
- `ProposalDeliverableEngine`
- `RevenuePipelineEngine`
- `GovernanceAuditLayer`
- `TelegramCommandExtension`

Catatan:

- Drafting selalu lewat Retrieval API existing.
- Jalur model resmi: `BusinessExecutionAPI -> Retrieval API existing -> Ollama Cloud API`.

## 4) Langkah Instalasi

### 4.1 Siapkan Schema Database

1. Buat schema `biz`.
2. Buat tabel `biz.*` sesuai blueprint master.
3. Pastikan FK ke `knowledge_note` dan `raw_capture` valid.
4. Tambahkan index untuk query harian (queue, status, date, stage).

Checklist:

- [ ] `biz` schema terbentuk.
- [ ] Semua tabel berhasil dibuat.
- [ ] FK valid.
- [ ] Query read path tidak error.

### 4.2 Siapkan Folder Vault Output

Buat dan validasi folder:

- `knowledge-base/content`
- `knowledge-base/content/personal-brand`
- `knowledge-base/deliverables`
- `knowledge-base/pipeline`
- `knowledge-base/pipeline/weekly`
- `knowledge-base/pipeline/monthly`
- `knowledge-base/pipeline/audit`
- `knowledge-base/templates/business`

Checklist:

- [ ] Semua folder ada.
- [ ] Agent punya hak tulis sesuai policy.
- [ ] Tidak ada vault kedua.

### 4.3 Konfigurasi Environment Agent

Konfigurasi environment wajib:

- `RETRIEVAL_API_URL`
- `POSTGRES_URL`
- `TELEGRAM_BOT_TOKEN`
- `OLLAMA_CLOUD_API_BASE` (dipakai lewat Retrieval API chain resmi)
- `VAULT_ROOT_PATH`

Aturan:

- Simpan secret di env file/secret manager runtime.
- Jangan commit token/key.
- Jangan menulis key ke file config runtime non-secret.

### 4.4 Aktivasi Command Telegram (Extension)

Aktifkan command berikut tanpa mengganti bot lama:

- `/daily_batch`
- `/funnel_gap`
- `/content_draft`
- `/publish_queue`
- `/proposal_gen`
- `/client_add`
- `/project_update`
- `/deal_add`
- `/deal_stage`
- `/invoice_update`
- `/pipeline_report`
- `/brand_idea`
- `/sla_status`

Aturan:

- Gunakan command map versioning.
- Pastikan anti-collision dengan command existing.
- Siapkan rollback ke command map versi sebelumnya.

### 4.5 Terapkan Reliability Contract

Set parameter minimal:

- Timeout retrieval: 10 detik.
- Timeout model via retrieval: 30 detik.
- Retry: 2x (backoff 1 detik, 3 detik).
- Circuit breaker: open setelah 5 failure/60 detik, hold 120 detik.
- Degrade mode: return `context_not_sufficient` jika context/model tidak sehat.

### 4.6 Terapkan Capacity & Cost Guardrail

Set parameter minimal:

- Max parallel workflow: 4.
- Max parallel high-risk draft: 1.
- Queue > 40: throttle 50%.
- Queue > 80: freeze non-critical workflows.

Cost guard:

- Alert budget 70/85/100%.
- 85%: throttle non-critical.
- 100%: stop non-critical, lanjutkan critical ops saja.

### 4.7 Aktifkan Audit dan Reconciliation

Wajib aktif:

- `biz.execution_audit_log` untuk semua command/task.
- Reconciliation harian DB-vs-vault.
- Laporan audit di `knowledge-base/pipeline/audit/`.

## 5) Verifikasi Pasca Instalasi (Go-Live Gate)

Sebelum status `Full GO`, semua berikut harus lulus:

- [ ] Schema `biz` tervalidasi.
- [ ] Semua command extension jalan normal.
- [ ] Tidak ada collision command existing.
- [ ] Drafting terbukti lewat Retrieval API chain resmi.
- [ ] Reliability contract aktif (termasuk degrade mode).
- [ ] Capacity guardrail aktif dan terukur.
- [ ] Cost guardrail aktif dan terukur.
- [ ] Reconciliation harian sukses.
- [ ] Fallback runbook command kritikal diuji:
  - `/daily_batch`
  - `/publish_queue`
  - `/proposal_gen`

## 6) Runbook Fallback Command Kritis

### 6.1 `/daily_batch`

- Gejala: timeout retrieval/model atau queue overload.
- Fallback: conversion-first manual queue shaping.
- Recovery: replay idempotent berdasarkan `idempotency_key`.

### 6.2 `/publish_queue`

- Gejala: route conflict atau write vault gagal.
- Fallback: lock queue manual checklist, publish bertahap.
- Recovery: rollback command map, lalu jalankan reconciliation.

### 6.3 `/proposal_gen`

- Gejala: context tipis atau model unavailable.
- Fallback: gunakan template baseline + retrieval evidence manual.
- Recovery: rerun setelah circuit half-open probe sukses.

## 7) Uji Operasional 7 Hari (Disarankan)

Hari 1-2:

- Uji command map dan collision safety.
- Uji retrieval path dengan citation.

Hari 3-4:

- Uji throughput batch + queue backpressure.
- Uji fallback 3 command kritikal.

Hari 5-6:

- Uji budget threshold 70/85/100 (simulasi).
- Uji incident kelas B (model outage/desync vault).

Hari 7:

- Review KPI baseline + incident review.
- Putuskan `Full GO` atau lanjut hardening.

## 8) Kriteria Full GO

Status `Full GO` hanya jika:

- Semua gate verifikasi lulus.
- Tidak ada incident kritikal terbuka.
- Audit trail end-to-end dapat ditelusuri.
- Reconciliation sukses konsisten.
- Owner modul menyetujui readiness operasional.

Jika ada 1 item kritikal gagal, status harus `NO-GO` sampai remediasi selesai.

## Appendix A) Systemd Service Hermes Gateway (Auto-Start VPS)

Appendix ini untuk menjalankan `hermes gateway` sebagai daemon agar otomatis hidup saat reboot.

### A.1 Prasyarat

- Hermes sudah terpasang dan command `hermes` bisa dieksekusi oleh user service.
- Environment gateway sudah siap (token dan konfigurasi platform).
- Disarankan pakai user service (bukan root service) untuk isolasi dan keamanan.

### A.2 Buat Environment File

Contoh file:

- `~/.config/hermes/gateway.env`

Contoh isi minimal:

```bash
# Sesuaikan dengan konfigurasi runtime Anda
TELEGRAM_BOT_TOKEN=replace_me
HERMES_HOME=/home/openclaw/.hermes
```

Aturan:

- Set permission ketat: hanya owner yang bisa baca.
- Jangan commit file env ini ke git.

### A.3 Buat Unit File (User Service)

Buat file:

- `~/.config/systemd/user/hermes-gateway.service`

Isi unit file:

```ini
[Unit]
Description=Hermes Gateway Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=%h/.config/hermes/gateway.env
WorkingDirectory=%h
ExecStart=/bin/bash -lc 'hermes gateway'
Restart=always
RestartSec=5
TimeoutStopSec=30
KillMode=process

[Install]
WantedBy=default.target
```

Catatan:

- Jika binary `hermes` tidak ditemukan oleh systemd PATH, ganti `ExecStart` dengan path absolut binary, misalnya `%h/.local/bin/hermes gateway`.

### A.4 Aktifkan dan Jalankan Service

```bash
systemctl --user daemon-reload
systemctl --user enable hermes-gateway.service
systemctl --user start hermes-gateway.service
systemctl --user status hermes-gateway.service --no-pager
```

Jika service harus tetap aktif walau user logout, aktifkan linger:

```bash
loginctl enable-linger "$USER"
```

### A.5 Verifikasi Auto-Start Reboot

Checklist:

- [ ] `systemctl --user is-enabled hermes-gateway.service` mengembalikan `enabled`.
- [ ] Setelah reboot VPS, service kembali `active (running)`.
- [ ] Gateway merespons command test dari platform (contoh Telegram).

### A.6 Operasional Harian

Command operasional:

```bash
systemctl --user restart hermes-gateway.service
systemctl --user stop hermes-gateway.service
systemctl --user status hermes-gateway.service --no-pager
journalctl --user -u hermes-gateway.service -n 200 --no-pager
journalctl --user -u hermes-gateway.service -f
```

### A.7 Troubleshooting Cepat

- Gagal start:
  - cek `journalctl --user -u hermes-gateway.service -n 200 --no-pager`
  - cek path binary `hermes`
  - cek permission/env di `gateway.env`
- Tidak auto-start:
  - cek `is-enabled`
  - cek `loginctl enable-linger "$USER"`
- Gateway hidup tapi bot diam:
  - validasi token/platform config
  - jalankan `hermes doctor`
  - restart service setelah perbaikan config

### A.8 Rollback Aman

Jika perlu rollback cepat:

```bash
systemctl --user stop hermes-gateway.service
systemctl --user disable hermes-gateway.service
systemctl --user daemon-reload
```

Rollback tidak menghapus data Hermes, hanya menonaktifkan daemon gateway.

## Appendix B) Systemd System Service (/etc/systemd/system)

Appendix ini adalah alternatif jika ingin menjalankan Hermes Gateway sebagai service level mesin (system service), bukan user service.

### B.1 Kapan Pakai System Service

Gunakan system service jika:

- service harus aktif tanpa ketergantungan user session,
- operasi server dikelola sebagai daemon standar level OS,
- dibutuhkan kontrol terpusat via `sudo systemctl`.

Tetap disarankan menjalankan process dengan user non-root khusus service.

### B.2 Buat User Service Khusus

Contoh membuat user sistem:

```bash
sudo useradd --system --create-home --home-dir /opt/hermes --shell /usr/sbin/nologin hermes
```

Catatan:

- Jika user `hermes` sudah ada, lewati langkah ini.
- Pastikan binary `hermes` dapat diakses oleh user tersebut.

### B.3 Buat Environment File (System)

Buat file:

- `/etc/hermes/gateway.env`

Contoh isi:

```bash
TELEGRAM_BOT_TOKEN=replace_me
HERMES_HOME=/opt/hermes/.hermes
PATH=/usr/local/bin:/usr/bin:/bin:/opt/hermes/.local/bin
```

Set permission:

```bash
sudo mkdir -p /etc/hermes
sudo chown root:hermes /etc/hermes/gateway.env
sudo chmod 640 /etc/hermes/gateway.env
```

### B.4 Buat Unit File System Service

Buat file:

- `/etc/systemd/system/hermes-gateway.service`

Isi unit file:

```ini
[Unit]
Description=Hermes Gateway (system service)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=hermes
Group=hermes
EnvironmentFile=/etc/hermes/gateway.env
WorkingDirectory=/opt/hermes
ExecStart=/bin/bash -lc 'hermes gateway'
Restart=always
RestartSec=5
TimeoutStopSec=30
KillMode=process

# Basic hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=true
ReadWritePaths=/opt/hermes

[Install]
WantedBy=multi-user.target
```

Catatan:

- Jika `hermes` tidak ada di PATH service, gunakan path absolut pada `ExecStart`, contoh `/opt/hermes/.local/bin/hermes gateway`.
- Sesuaikan `ReadWritePaths` jika data runtime berada di lokasi lain.

### B.5 Enable dan Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable hermes-gateway.service
sudo systemctl start hermes-gateway.service
sudo systemctl status hermes-gateway.service --no-pager
```

### B.6 Verifikasi Reboot

Checklist:

- [ ] `sudo systemctl is-enabled hermes-gateway.service` = `enabled`.
- [ ] Setelah reboot, status kembali `active (running)`.
- [ ] Gateway merespons command test dari platform.

### B.7 Operasional Harian

```bash
sudo systemctl restart hermes-gateway.service
sudo systemctl stop hermes-gateway.service
sudo systemctl status hermes-gateway.service --no-pager
sudo journalctl -u hermes-gateway.service -n 200 --no-pager
sudo journalctl -u hermes-gateway.service -f
```

### B.8 Troubleshooting Cepat

- Service gagal start:
  - cek log `journalctl`,
  - verifikasi `ExecStart` dan PATH,
  - cek permission `/etc/hermes/gateway.env`.
- Service start tapi gateway tidak merespons:
  - validasi token/config platform,
  - jalankan `hermes doctor` dengan user service (`sudo -u hermes -H hermes doctor`).
- Permission error saat write state:
  - cek owner folder runtime (`/opt/hermes`, `HERMES_HOME`),
  - cek `ReadWritePaths` pada unit file.

### B.9 Rollback Aman

```bash
sudo systemctl stop hermes-gateway.service
sudo systemctl disable hermes-gateway.service
sudo rm -f /etc/systemd/system/hermes-gateway.service
sudo systemctl daemon-reload
```

Rollback ini hanya menonaktifkan service. Data Hermes tetap aman jika folder runtime tidak dihapus.

## Appendix C) Template Systemd "Production Hardened"

Appendix ini untuk VPS dengan traffic gateway tinggi. Fokusnya: resource control, restart burst protection, dan log rate control.

### C.1 Unit File Hardened (Contoh)

File:

- `/etc/systemd/system/hermes-gateway.service`

Template:

```ini
[Unit]
Description=Hermes Gateway (Production Hardened)
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=300
StartLimitBurst=5

[Service]
Type=simple
User=hermes
Group=hermes
EnvironmentFile=/etc/hermes/gateway.env
WorkingDirectory=/opt/hermes
ExecStart=/bin/bash -lc 'hermes gateway'

# Restart policy + burst protection
Restart=on-failure
RestartSec=8
TimeoutStartSec=60
TimeoutStopSec=45
KillMode=process

# CPU / Memory limits
CPUAccounting=true
MemoryAccounting=true
CPUQuota=150%
MemoryMax=2G
MemoryHigh=1536M
TasksMax=512
LimitNOFILE=65536

# I/O and scheduler tuning
Nice=5
IOSchedulingClass=best-effort
IOSchedulingPriority=4

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectSystem=full
ProtectHome=true
ProtectControlGroups=true
ProtectKernelModules=true
ProtectKernelTunables=true
RestrictSUIDSGID=true
LockPersonality=true
RestrictRealtime=true
SystemCallArchitectures=native
ReadWritePaths=/opt/hermes

# Log rate control (stdout/stderr to journald)
StandardOutput=journal
StandardError=journal
LogRateLimitIntervalSec=30s
LogRateLimitBurst=500

[Install]
WantedBy=multi-user.target
```

### C.2 Catatan Tuning Parameter

- `CPUQuota=150%`
  - artinya service boleh pakai maksimum 1.5 core setara CPU time.
  - naikkan ke `200%` jika throughput tinggi dan CPU idle masih tersedia.
- `MemoryMax=2G` + `MemoryHigh=1536M`
  - `MemoryHigh` memicu pressure sebelum menyentuh limit keras.
  - sesuaikan dengan kapasitas total VPS agar tidak mengganggu service lain.
- `StartLimitIntervalSec=300` + `StartLimitBurst=5`
  - mencegah restart loop tak terkendali saat ada fault berulang.
- `LogRateLimitIntervalSec=30s` + `LogRateLimitBurst=500`
  - menahan flooding log ke journald saat traffic spike.

### C.3 Perintah Aktivasi

```bash
sudo systemctl daemon-reload
sudo systemctl enable hermes-gateway.service
sudo systemctl restart hermes-gateway.service
sudo systemctl status hermes-gateway.service --no-pager
```

### C.4 Verifikasi Hardening

```bash
sudo systemctl show hermes-gateway.service \
  -p CPUQuotaPerSecUSec -p MemoryMax -p MemoryHigh -p TasksMax \
  -p StartLimitIntervalUSec -p StartLimitBurst \
  -p LogRateLimitIntervalUSec -p LogRateLimitBurst
```

Checklist:

- [ ] CPU quota terbaca sesuai target.
- [ ] Memory limit aktif sesuai target.
- [ ] Start limit aktif.
- [ ] Log rate limit aktif.
- [ ] Service tetap `active (running)` saat spike simulasi.

### C.5 Monitoring Operasional

- Pantau restart burst:
  - `sudo systemctl status hermes-gateway.service`
- Pantau log throttling:
  - `sudo journalctl -u hermes-gateway.service -n 200 --no-pager`
- Pantau resource usage:
  - `systemd-cgtop` atau observability stack yang sudah ada.

### C.6 Guardrail Perubahan

- Ubah satu parameter per siklus, lalu observasi minimal 24 jam.
- Jika terjadi throughput drop signifikan:
  - longgarkan `CPUQuota`,
  - evaluasi `MemoryHigh/MemoryMax`,
  - cek bottleneck I/O dan network sebelum menaikkan semua limit sekaligus.

### C.7 Preset Siap Pakai (Copy-Paste)

Gunakan salah satu preset berikut sesuai ukuran VPS.

#### Preset 1 - `small-vps` (1-2 vCPU)

Rekomendasi untuk VPS kecil dengan resource ketat.

```ini
[Unit]
Description=Hermes Gateway (small-vps preset)
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=300
StartLimitBurst=4

[Service]
Type=simple
User=hermes
Group=hermes
EnvironmentFile=/etc/hermes/gateway.env
WorkingDirectory=/opt/hermes
ExecStart=/bin/bash -lc 'hermes gateway'
Restart=on-failure
RestartSec=10
TimeoutStartSec=60
TimeoutStopSec=45
KillMode=process

CPUAccounting=true
MemoryAccounting=true
CPUQuota=90%
MemoryHigh=768M
MemoryMax=1024M
TasksMax=256
LimitNOFILE=32768

Nice=8
IOSchedulingClass=best-effort
IOSchedulingPriority=6

NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectSystem=full
ProtectHome=true
ProtectControlGroups=true
ProtectKernelModules=true
ProtectKernelTunables=true
RestrictSUIDSGID=true
LockPersonality=true
RestrictRealtime=true
SystemCallArchitectures=native
ReadWritePaths=/opt/hermes

StandardOutput=journal
StandardError=journal
LogRateLimitIntervalSec=30s
LogRateLimitBurst=250

[Install]
WantedBy=multi-user.target
```

#### Preset 2 - `medium-vps` (4+ vCPU)

Rekomendasi untuk VPS menengah dengan traffic lebih tinggi.

```ini
[Unit]
Description=Hermes Gateway (medium-vps preset)
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=300
StartLimitBurst=6

[Service]
Type=simple
User=hermes
Group=hermes
EnvironmentFile=/etc/hermes/gateway.env
WorkingDirectory=/opt/hermes
ExecStart=/bin/bash -lc 'hermes gateway'
Restart=on-failure
RestartSec=6
TimeoutStartSec=60
TimeoutStopSec=45
KillMode=process

CPUAccounting=true
MemoryAccounting=true
CPUQuota=250%
MemoryHigh=3G
MemoryMax=4G
TasksMax=1024
LimitNOFILE=65536

Nice=3
IOSchedulingClass=best-effort
IOSchedulingPriority=4

NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectSystem=full
ProtectHome=true
ProtectControlGroups=true
ProtectKernelModules=true
ProtectKernelTunables=true
RestrictSUIDSGID=true
LockPersonality=true
RestrictRealtime=true
SystemCallArchitectures=native
ReadWritePaths=/opt/hermes

StandardOutput=journal
StandardError=journal
LogRateLimitIntervalSec=30s
LogRateLimitBurst=800

[Install]
WantedBy=multi-user.target
```

### C.8 Cara Pakai Preset

1. Pilih satu preset sesuai ukuran VPS.
2. Simpan ke `/etc/systemd/system/hermes-gateway.service`.
3. Jalankan:

```bash
sudo systemctl daemon-reload
sudo systemctl enable hermes-gateway.service
sudo systemctl restart hermes-gateway.service
sudo systemctl status hermes-gateway.service --no-pager
```

4. Verifikasi nilai limit:

```bash
sudo systemctl show hermes-gateway.service \
  -p CPUQuotaPerSecUSec -p MemoryMax -p MemoryHigh -p TasksMax \
  -p StartLimitIntervalUSec -p StartLimitBurst \
  -p LogRateLimitIntervalUSec -p LogRateLimitBurst
```
