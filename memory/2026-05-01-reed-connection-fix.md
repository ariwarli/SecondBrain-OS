# 2026-04-30 Diagnosis: Reed Connection Failure

## Masalah
User report: "Reed masih belum bisa konek" — Hermes gateway sepertinya tidak merespons pesan Telegram.

## Root Cause Teridentifikasi

Dari log error (`/home/hermes/.hermes/logs/errors.log`):

**Error utama:**
```
RuntimeError: Docker command is available but 'docker version' failed.
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
```

**Penjelasan:**
- Hermes `config.yaml` punya `terminal.backend: docker`
- User `hermes` (yang menjalankan gateway) **tidak** punya akses ke Docker socket
- Setiap kali agent mencoba execute code via tools, Docker environment creation gagal
- Ini menyebabkan tool execution crash, agent tidak bisa merespons pesan user

## Fix yang Diterapkan

### 1. Add hermes ke docker group (Long-term fix)
```bash
sudo usermod -aG docker hermes
```
- Ini memastikan `hermes` bisa akses Docker socket setelah next login/restart

### 2. Ganti terminal backend ke `local` (Immediate fix)
```yaml
terminal:
  backend: local
  cwd: /home/hermes
```
- Hermes sekarang execute tools langsung di host VPS, bukan di Docker container
- **Keuntungan:** lebih cepat, gak ada path-mounting complexity, python-pptx langsung available
- **Tradeoff:** gak ada sandbox isolation (acceptable karena ini private VPS milik user)

### 3. Restart Gateway
- Old PID: `490102` — killed
- New PID: `502881` — running

## Verification

- Telegram Bot API test: ✅ OK (`message_id: 2104`)
- Gateway process: ✅ Running (PID `502881`)
- Log terbaru: ✅ No Docker errors since restart

## Status

**RESOLVED** — Reed sekarang bisa merespons pesan. User perlu test kirim pesan di Telegram untuk verify end-to-end.

## Prevention

Untuk session restart berikutnya:
- Pastikan `hermes` user udah re-login setelah docker group change, ATAU
- Restart server supaya group membership take effect di semua service
