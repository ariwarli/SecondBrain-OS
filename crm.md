# CRM Operating File — Inbox-Driven

File ini di-generate otomatis dari inbox items yang terkait kontak/relasi.

**Sumber:** Inbox Telegram → REED Routing → crm.md
**Update:** Auto (oleh REED) + Manual (oleh user kalau perlu)

---

## Follow-Up Queue (dari Inbox)

| Nama | Company | Status | Last Contact | Next Action | Due |
|------|---------|--------|-------------|-------------|-----|
| DEDE | STOP TB | Proposal stage | Apr 11 | Meeting follow-up | Apr 12 |
| Contact missing | NIRVA | Active delivery | Apr 8 | Feedback request | Apr 12 |
| Contact missing | APPS | Active delivery | Apr 8 | Progress check | Apr 13 |
| Contact missing | SentraChat | Retainer | Apr 6 | Monthly update | Apr 15 |
| Contact missing | APPSSYNC | Retainer | Apr 6 | Monthly update | Apr 15 |
| Contact missing | PT SIN | Active delivery | Apr 6 | Project check-in | Apr 15 |

---

## Key Relationships (dari Inbox)

### DEDE — STOP TB Partnership

- **Role:** Contact owner for STOP TB proposal / partnership lane
- **Relationship type:** Potential client / partnership
- **Last interaction:** Apr 11 - Meeting scheduled
- **Current context:** TOR draft in progress
- **Pain points / goals:** Need TOR clarity, proposal review, and meeting alignment before close
- **Open loop:** TOR → Proposal → Meeting
- **Suggested next message:** "Pak DEDE, TOR sudah gw draft. Bisa kita review bareng sebelum meeting?"

---

## Stale Deals / Cold Threads (dari Inbox)

| Nama | Last Touch | Reason Stalled | Re-engagement Angle |
|------|-----------|----------------|--------------------|
| [TBD - from inbox] | - | - | - |

---

## Revenue Pipeline

| Client | Stage | Value | Probability | Expected Close |
|--------|-------|-------|-------------|----------------|
| STOP TB | Proposal | IDR 8jt | 60% | Apr 2026 |
| NIRVA | Delivery | IDR 15jt | 90% | Active |
| APPS | Delivery | IDR 12jt | 90% | Active |

## CRM Data Gaps — Must Fill

| Client | Missing Data | Why It Blocks Automation |
|---|---|---|
| NIRVA | Primary contact name | REED cannot draft personalized follow-up |
| APPS | Primary contact name | REED cannot draft personalized progress check |
| SentraChat | Primary contact name | Monthly update lane remains generic |
| APPSSYNC | Primary contact name | Monthly update lane remains generic |
| PT SIN | Primary contact name | Check-in cannot be addressed properly |

---

## Notes For Hermes

- File ini auto-update dari inbox items yang terkait orang/kontak.
- REED DULL kirim reminder di topic `personal-crm` kalau ada follow-up yang overdue.
- Prioritaskan follow-up yang paling dekat ke revenue.
- Draft pesan singkat, langsung, personal. Voice: percaya diri tanpa arogan.
- Jika user membalas follow-up atau reminder CRM dengan `done`, follow-up aktif terakhir dianggap selesai atau next action cleared.
- Setelah `done`, reminder yang sama tidak perlu diulang kecuali user membuat next action baru.

---

## Personal Relationships (Non-Client)

Kontak personal yang relevan untuk context Hermes — bukan pipeline revenue.

| Nama | Relasi | Context | Catatan |
|------|--------|---------|---------|
| Azril | Anak | Keluarga inti | Nama anak Bani |
| Fariz | Kolaborator | Ruang Curhat project | Contact personal, bukan via grup |
| Dr. Ronald / Dr. Suryalena | Dokter | Kesehatan | Dokter yang sudah kenal riwayat Bani sejak lama — kontak darurat bila perlu |
| Sindi | Relasi personal | Finansial | Pernah ada transaksi pinjaman |
