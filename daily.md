# Daily Operations — Inbox-Driven

File ini di-generate otomatis dari inbox items yang masuk. REED update ini setiap kali ada task/task baru.

**Sumber:** Inbox Telegram → REED Routing → daily.md
**Update:** Auto (oleh REED) + Manual (oleh user kalau perlu)

---

## Date

- Tanggal: 2026-04-10
- Hari: Jumat

---

## Top 3 Priorities (dari Inbox)

1. Membuat TOR StopTB (meeting DEDE)
2. Landing page v2 → NIRVA APPS
3. AI chatbot integration doc → SentraChat

---

## Delegated To Hermes (dari Inbox Items)

### Task: TOR StopTB
- **Source:** Inbox Telegram
- **Outcome:** TOR draft untuk partnership STOP TB
- **Deadline:** Before meeting DEDE
- **Status:** In Progress
- **Context:** `clients/stop-tb/context.md`

### Task: Landing Page v2 NIRVA
- **Source:** Inbox Telegram
- **Outcome:** Revised landing page copy
- **Deadline:** ASAP
- **Status:** In Progress
- **Context:** `clients/nirva/context.md`

### Task: SentraChat Integration Doc
- **Source:** Inbox Telegram
- **Outcome:** Integration document untuk dev team
- **Deadline:** This week
- **Status:** Pending
- **Context:** `clients/sentrachat/context.md`

---

## Waiting For

| Who | Item | Since | Next Follow-up |
|-----|------|-------|----------------|
| DEDE (STOP TB) | Meeting confirmation | Apr 11 | Apr 12 |
| NIRVA | Feedback landing page v1 | Apr 8 | Apr 12 |
| APPS | Progress approval | Apr 8 | Apr 13 |

---

## Content Queue (dari Inbox)

| Item | Platform | Status | Scheduled |
|------|----------|--------|-----------|
| [TBD - from inbox voice notes] | Threads | Draft | - |
| [TBD - from inbox ideas] | LinkedIn | Idea | - |

---

## End Of Day Auto-Summary

*Scheduler internal REED mengisi ini setiap 18:00 dari inbox items yang diproses hari ini.*

- Yang selesai hari ini:
- Yang pending:
- Blocker:
- Parkir ke besok:
- Overnight tasks:

---

## Rules

- File ini di-update otomatis dari inbox items. Jangan edit manual kecuali koreksi.
- Setiap inbox item yang jadi task → masuk ke section "Delegated To Hermes".
- Setiap inbox item yang jadi follow-up → masuk ke section "Waiting For".
- Setiap inbox item yang jadi konten → masuk ke section "Content Queue".
- Top 3 Priorities = 3 task paling urgent dari semua yang pending.
- Jika user membalas reminder/task dengan `done`, item aktif terakhir yang relevan dianggap selesai saat refresh berikutnya.
- Jika `done` ambigu karena ada beberapa item aktif, REED harus minta klarifikasi singkat sebelum menutup task.
