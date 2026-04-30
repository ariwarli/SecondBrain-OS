# Tailscale Setup Guide — DeepThree VPS

> **Fungsi:** VPN meshnetwork private. Semua device lo (MacBook, VPS, HP, dll) bisa komunikasi seolah-olah di LAN yang sama, meskipun beda network publik. Aman, encrypted, tanpa expose port ke internet.

---

## 1. Install Tailscale

### VPS (Ubuntu/Debian)
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```
Ikuti link autentikasi di terminal untuk login via browser.

### MacBook
Download dari [tailscale.com/download](https://tailscale.com/download) atau via Homebrew:
```bash
brew install --cask tailscale
```

---

## 2. Login & Connect

Setiap device wajib login ke **Tailscale account yang sama** (Google, Microsoft, GitHub, etc).

```bash
# VPS
sudo tailscale up

# Mac: buka app Tailscale → toggle ON → login via browser
```

Verify status:
```bash
sudo tailscale status
# Atau di browser: https://login.tailscale.com/admin/machines
```

---

## 3. Verify Connectivity

Dari MacBook:
```bash
ping 100.113.246.119
ssh root@100.113.246.119
```

Dari VPS:
```bash
ping 100.118.155.29
```

Kalau reply → Tailscale mesh sudah aktif di level OS.

---

## 4. Useful Commands

| Command | Fungsi |
|---------|--------|
| `sudo tailscale status` | Lihat semua device di tailnet |
| `sudo tailscale up` | Connect ke tailnet |
| `sudo tailscale down` | Disconnect |
| `sudo tailscale ip -4` | Lihat Tailscale IP device ini |
| `sudo tailscale netcheck` | Cek NAT/firewall path ke coord server |
| `sudo tailscale ping <ip>` | Ping via Tailscale DERP relay (berguna debug) |
| `sudo tailscale status --json` | Output JSON untuk script/automation |
| `sudo tailscale set --ssh` | Enable Tailscale SSH built-in auth |
| `sudo tailscale logout` | Unlink device dari account |

---

## 5. Tailscale SSH (Opsional — Built-in Auth)

Tailscale punya fitur `tailscale ssh` yang gak perlu manual authorized_keys. Autentikasi via Tailscale identity (whoami device), bukan SSH key.

**Enable di VPS:**
```bash
sudo tailscale set --ssh
```

**Akses dari MacBook (atau device lain di tailnet):**
```bash
tailscale ssh root@deepthree
# Atau pakai IP
tailscale ssh root@100.113.246.119
```

**Keuntungan:**
- Gak perlu manage `~/.ssh/authorized_keys`
- Revoke akses via Tailscale admin console (bukan edit file di server)
- Audit log: https://login.tailscale.com/admin/logs

**Caveat:** Tailscale SSH masih pakai port 22, tapi autentikasi via Tailscale layer. Kalau lo sudah lock SSH ke `ListenAddress 100.113.246.119`, ini tetap compatible.

---

## 6. ACL (Access Control List) — Opsional tapi Recommended

Secara default, semua device di tailnet bisa reach semua device lain. Kalau mau restrict (misalnya MacBook cuma boleh SSH ke VPS, tapi VPS gak boleh reach MacBook):

1. Buka https://login.tailscale.com/admin/acls
2. Edit JSON, contoh minimal ACL:

```json
{
  "acls": [
    {
      "action": "accept",
      "src":    ["tag:admin"],
      "dst":    ["*:*"]
    },
    {
      "action": "accept",
      "src":    ["ariwarli.github"],
      "dst":    ["100.113.246.119:22"]
    }
  ],
  "ssh": [
    {
      "action": "check",
      "src":    ["ariwarli.github"],
      "dst":    ["tag:server"],
      "users":  ["autogroup:nonroot", "root"]
    }
  ]
}
```

---

## 7. Security Cheat Sheet

| Layer | Config | File/Command |
|-------|--------|------------|
| Tailscale Network | Private mesh IP | `tailscale up` (udah running) |
| SSH Listen | Cuma Tailscale IP | `/etc/ssh/sshd_config: ListenAddress 100.113.246.119` |
| SSH Key Only | No password brute force | `/etc/ssh/sshd_config: PasswordAuthentication no` |
| User Non-Root | Safety first | `banirisset` → sudo tanpa password |
| Firewall (host) | Fail2Ban aktif | `systemctl status fail2ban` |
| Tailscale ACL | Restrict cross-device | https://login.tailscale.com/admin/acls |

---

## 8. Troubleshooting

| Problem | Fix |
|---------|-----|
| Device gak muncul di tailnet | `sudo tailscale up` ulang, cek login |
| Ping gak reply | Cek firewall host (`ufw status`), pastikan Tailscale IP gak di-block |
| SSH via Tailscale IP refused | Cek `ss -tlnp` apakah sshd listen di `100.113.246.119:22`, bukan `0.0.0.0:22` |
| Tailscale disconnected random | Check if `tailscaled` service running: `systemctl status tailscaled` |

---

## 9. Admin Console
Web UI untuk manage devices, ACLs, logs, DNS:
https://login.tailscale.com/admin/machines

---

**Status saat ini:** ✅ Connected (`ariwarli.github` tailnet, 2 devices: `banis-macbook-air` + `deepthree`)
