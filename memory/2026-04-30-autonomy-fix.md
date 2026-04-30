# 2026-04-30 Autonomous Execution Fix

## Masalah
Hermes memberikan instruksi manual ke user ("Bro, gw coba dari sini gak bisa — environment VPS ini lagi error Docker... Yang perlu lo lakukan: SSH ke VPS lo, jalanin 2 command ini...") saat diminta generate file atau fix system issue.

## Root Cause
System prompt default Hermes tidak menyebutkan bahwa agent berjalan di VPS dan bisa self-execute. Agent mengira execution environment mungkin beda dari user machine, sehingga fallback ke "kasih user instruksi manual".

## Solusi
Update `config.yaml` keys:
1. `agent.system_prompt` — identity sebagai autonomous system operator
2. `agent.supplementary_prompt` — VPS context + self-healing rules + file generation rules + autonomy first mindset

## Impact
| Sebelum | Sesudah |
|---------|---------|
| "Bro, install npm, save script, run sendiri" | Direct execution via tools |
| "You need to SSH and fix Docker" | Self-heal: `systemctl start docker` |
| Manual steps given to user | Done autonomously, report result |
| PPTX delivery manual | Auto-save + `MEDIA:` tag auto-deliver |

## Config Path
`/home/hermes/.hermes/config.yaml`

## Backup
`config.yaml.bak.<timestamp>`

## Verification
Tanya Hermes: "What environment are you running in?"
Expected: Mentions VPS DeepThree, Tailscale IP, Docker container.

## Restart Required
Gateway perlu restart supaya config baru di-load.