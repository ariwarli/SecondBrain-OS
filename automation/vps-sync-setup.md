# VPS Sync Setup — SecondBrain-OS

Single repo `ariwarli/SecondBrain-OS` syncs to both Mac and VPS.

## Locations
- **Mac:** `/Users/banirisset/2_Areas/banirisset`
- **VPS:** `/home/banirisset/secondbrain-os/`

## VPS Setup (one-time)

```bash
# Clone repo to VPS
cd /home/banirisset
git clone https://github.com/ariwarli/SecondBrain-OS.git secondbrain-os

# Set up auto-pull cron (every 5 minutes)
(crontab -l 2>/dev/null; echo "*/5 * * * * cd /home/banirisset/secondbrain-os && git pull --ff-only origin main >> /home/banirisset/.secondbrain-sync.log 2>&1") | crontab -
```

## Pushing from VPS
```bash
cd /home/banirisset/secondbrain-os
git add -A && git commit -m "update from VPS" && git push origin main
```

## Notes
- Symlinks at repo root (SOUL.md, USER.md, etc.) point to Mac paths — they will be broken on VPS, but the actual files live in `core/` which works everywhere.
- VPS-specific runtime config (Hermes, 9Router) lives outside this repo at `/home/hermes/.hermes/` and `/etc/systemd/system/`.
