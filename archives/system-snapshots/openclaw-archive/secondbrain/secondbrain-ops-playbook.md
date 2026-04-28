# SecondBrain OS Emergency Ops Playbook

Playbook ini dipakai kalau ada masalah di REED, scheduler, atau automation layer.

## Rule

- semua insiden ditangani lewat topic `ops`
- REED DULL hanya untuk alert/scheduler
- REED tetap jadi bot utama untuk diagnosis operasional
- kalau masalahnya cron, alert, atau job terjadwal, anggap itu domain REED DULL
- kalau masalahnya respons chat asisten di group, anggap itu domain REED

## Symptom 1: Morning Brief Tidak Masuk

### Di Telegram

Kirim ke `ops`:
```text
@survivorset_bot Cek kenapa morning brief hari ini tidak masuk.
```

### Di VPS

```bash
/home/openclaw/automation/scheduler-status.sh
```

Cek:
- apakah crontab masih ada
- apakah `morning_brief.log` punya entry terbaru
- apakah `scheduler_health.log` menunjukkan masalah

## Symptom 2: Scheduler Terlihat Mati

### Di Telegram

Kirim ke `ops`:
```text
@survivorset_bot Cek health scheduler sekarang dan kasih root cause paling mungkin.
```

### Di VPS

```bash
crontab -l
/home/openclaw/automation/scheduler-status.sh
ls -la /home/openclaw/automation/logs
```

## Symptom 3: Alert Masuk, Tapi Job Tidak Jalan

Kemungkinan:
- cron aktif tapi prompt job gagal
- Telegram runner error
- env token tidak terbaca
- topic mapping salah

### Cek

```bash
tail -n 30 /home/openclaw/automation/logs/morning_brief.log
tail -n 30 /home/openclaw/automation/logs/scheduler_health.log
cat /home/openclaw/automation/telegram-config.json
```

## Symptom 4: Bot Tidak Merespons di Group

### Cek cepat

- pastikan kirim di topic yang benar
- mention `@survivorset_bot`
- jangan pakai `@survivorsched_bot` untuk kerja harian
- cek apakah privacy mode BotFather untuk `@survivorset_bot` sudah `Disable`
- cek apakah `pm2-openclaw.service` aktif

### Prompt

```text
@survivorset_bot Tes respons. Kalau kamu baca ini, jawab singkat dan konfirmasi topic ini aktif.
```

### Di VPS

```bash
systemctl status pm2-openclaw.service --no-pager --lines=30
sudo -u openclaw -H env PATH=/usr/local/bin:/usr/bin:/bin pm2 list
```

Kalau bot masih diam padahal PM2 sehat:
- cek `getMe` Telegram bot dan pastikan `can_read_all_group_messages=true`
- cek `/home/openclaw/.openclaw/openclaw.json`

## Symptom 5: Topic Salah / Pesan Masuk ke Thread Salah

### Cek config

```bash
cat /home/openclaw/automation/telegram-config.json
```

Topic mapping saat ini:
- `updates`: `13`
- `inbox`: `11`
- `tasks`: `10`
- `personal-crm`: `9`
- `content`: `3`
- `ops`: `27`
- `knowledge-base`: `16`

## Symptom 6: Log Membesar / Sulit Audit

Sudah ada logrotate:
- `/etc/logrotate.d/openclaw-scheduler`

### Cek

```bash
ls -la /home/openclaw/automation/logs
sudo logrotate -d /etc/logrotate.d/openclaw-scheduler
```

## Symptom 7: Scheduler Bot Jalan, Tapi Alert Tidak Terkirim

### Cek env

```bash
cat /home/openclaw/automation/telegram-runner.env
```

### Test live alert

```bash
set -a
. /home/openclaw/automation/telegram-runner.env
set +a
/usr/bin/python3 /home/openclaw/automation/telegram_runner.py \
  --job-id scheduler_health_alert \
  --thread-key ops \
  --config /home/openclaw/automation/telegram-config.json \
  --label scheduler_health_alert \
  --message "Manual ops alert test from VPS"
```

## Post-Reboot Verification

Pakai ini setiap habis reboot VPS atau habis ubah startup/runtime PM2.

### 1. Cek service startup REED

```bash
systemctl status pm2-openclaw.service --no-pager --lines=30
```

Harus terlihat:
- `active (running)`
- main process = `PM2`
- app `openclaw` direstore

### 2. Cek app PM2

```bash
sudo -u openclaw -H env PATH=/usr/local/bin:/usr/bin:/bin pm2 list
```

Harus terlihat:
- app `openclaw`
- status `online`

### 3. Cek config runtime REED

```bash
sed -n '1,40p' /home/openclaw/.openclaw/openclaw.json
```

Pastikan:
- `channels.telegram.groups` memuat `-1003344368011`
- tidak ada group ID stale yang tidak dipakai

### 4. Cek scheduler layer

```bash
/home/openclaw/automation/scheduler-status.sh
```

### 5. Test dari Telegram

Kirim ke topic `ops`:

```text
@survivorset_bot Tes pasca reboot. Jawab singkat kalau jalur group normal.
```

Kalau balas, berarti:
- startup PM2 aman
- polling Telegram aman
- routing group aman
- REED siap dipakai lagi

## Escalation Order

1. cek `ops` topic
2. jalankan `/home/openclaw/automation/scheduler-status.sh`
3. cek log per job
4. cek `telegram-config.json`
5. cek `telegram-runner.env`
6. test live alert

## Quick Commands

```bash
/home/openclaw/automation/scheduler-status.sh
```

```bash
systemctl status pm2-openclaw.service --no-pager --lines=30
```

```bash
sudo -u openclaw -H env PATH=/usr/local/bin:/usr/bin:/bin pm2 list
```

```bash
tail -n 30 /home/openclaw/automation/logs/morning_brief.log
```

```bash
tail -n 30 /home/openclaw/automation/logs/scheduler_health.log
```

```bash
crontab -l
```

## Anti-Panic Rule

Kalau ada error:
- jangan ubah banyak hal sekaligus
- cek logs dulu
- cek config dulu
- test satu jalur saja
- baru perbaiki
