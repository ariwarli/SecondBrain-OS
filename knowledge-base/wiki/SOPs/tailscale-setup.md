# Tailscale Setup Guide — DeepThree VPS

## Overview
Tailscale provides a secure, encrypted mesh VPN network that allows devices to communicate as if they were on the same local network, regardless of their physical location. This guide covers installation, configuration, and operational best practices for the VPS environment.

## Prerequisites
- Admin access to the VPS (`root` or `sudo` privileges)
- Access to the Tailscale admin console (or Tailscale SSH key for headless setup)
- A Tailscale account (free tier supports up to 20 devices)

## 1. Installation

### VPS (Ubuntu/Debian)
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```
Follow the authentication URL printed in the terminal to link the device to your tailnet.

### macOS (Local Machine)
Download the app from [tailscale.com/download](https://tailscale.com/download) or use Homebrew:
```bash
brew install --cask tailscale
```

## 2. Network Verification

### From Local Machine
```bash
# Verify connectivity to the VPS via Tailscale IP
ping 100.113.246.119
ssh root@100.113.246.119
```

### From VPS
```bash
# Verify connectivity to local machine
ping 100.118.155.29
```

A successful reply confirms the Tailscale mesh network is active.

## 3. Common Operations

| Command | Description |
|---------|-------------|
| `sudo tailscale status` | Display all devices in the tailnet |
| `sudo tailscale up` | Connect to the tailnet |
| `sudo tailscale down` | Disconnect from the tailnet |
| `sudo tailscale ip -4` | Show the Tailscale IPv4 address of the current device |
| `sudo tailscale netcheck` | Analyze NAT and firewall path to coordination servers |
| `sudo tailscale ping <ip>` | Ping via Tailscale DERP relay (useful for debugging) |
| `sudo tailscale status --json` | Machine-readable status output |

---

## 4. Security Hardening

### SSH Lockdown (Mandatory)
Restrict the SSH daemon to only listen on the Tailscale interface. This completely removes SSH from the public internet.

**Configuration file:** `/etc/ssh/sshd_config`

```bash
# Listen ONLY on the Tailscale IP
ListenAddress 100.113.246.119

# Disable password authentication for all users
PasswordAuthentication no

# Keep root login key-only
PermitRootLogin prohibit-password

# Restrict which users can log in
AllowUsers root <your-non-root-user>
```

**Restart SSH to apply:**
```bash
sudo systemctl restart sshd
```

**Verify:**
```bash
ss -tlnp | grep :22
# Expected output: ONLY 100.113.246.119:22
```

### Tailscale SSH (Alternative Authentication)
Tailscale provides its own built-in SSH server, allowing authentication via Tailscale identity instead of traditional SSH keys.

**Enable on VPS:**
```bash
sudo tailscale set --ssh
```

**Connect from Local Machine:**
```bash
tailscale ssh root@deepthree
```

**Advantages:**
- No manual `authorized_keys` management
- Centralized access control via the Tailscale admin console
- Audit logs available at [login.tailscale.com/admin/logs](https://login.tailscale.com/admin/logs)

**Note:** When using Tailscale SSH alongside a locked-down `sshd`, ensure `sshd` is still running and listening on the Tailscale IP as the fallback.

---

## 5. Access Control Lists (ACLs)

By default, all devices in a tailnet can reach each other. To implement granular access control (e.g., restrict local machine to only SSH into the VPS):

**Management URL:** [login.tailscale.com/admin/acls](https://login.tailscale.com/admin/acls)

**Example ACL Policy:**
```json
{
  "acls": [
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

## 6. Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Device not appearing in tailnet | Authentication expired / `tailscaled` stopped | Run `sudo tailscale up` and re-authenticate |
| Ping fails between devices | Host firewall blocking Tailscale interface | Check `ufw`/`iptables` rules for the `tailscale0` interface |
| SSH via Tailscale IP refused | `sshd` not listening on Tailscale IP | Verify `ListenAddress` in `sshd_config` and restart `sshd` |
| Tailscale disconnects randomly | `tailscaled` service crashed | Check `systemctl status tailscaled` and restart if necessary |

## 7. Operational Notes for Hermes

When integrating with the Hermes agent framework, remember that SSH access to the VPS is now exclusively via the Tailscale IP.

**VPS Details:**
- **Public IP:** `167.253.158.103` (SSH: Refused)
- **Tailscale IP:** `100.113.246.119` (SSH: Active)
- **Non-root User:** `banirisset` (sudo privileges)

Always use `100.113.246.119` for automated scripts and agent operations.
