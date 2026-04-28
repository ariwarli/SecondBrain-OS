# SKILL: product-launch-pack
# FOR: Bani Risset — Brand OS Project
# Last updated: April 2026

---

## Name
Digital Product Launch Pack Generator

## Description
Generate full launch asset pack untuk satu digital product dalam satu output: pricing structure, promo copy per platform, launch timeline, dan CTA hooks. Dirancang untuk Bani yang operate solo — semua asset dibuat sekaligus, zero back-and-forth.

Gunakan Alex Hormozi scarcity ladder sebagai default pricing model.

---

## Trigger Phrases
- "launch [nama produk]"
- "buatkan launch pack untuk..."
- "mau jualan [produk digital] — bantu dari pricing sampai copy"
- "siap launch [nama] — butuh semua assetnya"
- "full launch system untuk..."
- "GPT bundle / prompt pack / mini course / workshop — mau launch"
- "buatkan pricing + promo copy untuk..."

---

## Pre-Work
1. Baca `offer-library.md` → cek apakah produk sudah ada
2. Baca `funnel-knowledge.md` → Section 2.3 (Pricing Structure) dan Section 3.3 (Objection Handling)
3. Baca `voice-guide.md` → tone dan CTA library

Tanya user hanya jika belum ada:
1. Nama produk + deskripsi 1 kalimat
2. Format: PDF / GPT / Video / Live / Bundle?
3. Harga target (atau minta Claude rekomendasikan)
4. Platform launch utama: Lynk.id / Gumroad / Instagram DM / WA?

---

## Default Pricing Model — Hormozi Scarcity Ladder

```
Slot 1–10:    Harga A (terendah — early bird)
Slot 11–20:   Harga B (naik Rp50K–100K)
Slot 21–30:   Harga C
Slot 31–50:   Harga D
Slot 50+:     Harga Full (regular)

Rumus umum:
- Harga A = ~60% dari harga full
- Tiap 10 pembeli naik Rp50K (produk < Rp500K) atau Rp200–500K (produk > Rp1 juta)
- Harga full = benchmark kompetitor x 1.2 (Bani = premium brand)

Contoh untuk produk Rp297K full:
Slot 1–10:   Rp97.000
Slot 11–20:  Rp147.000
Slot 21–30:  Rp197.000
Slot 31–50:  Rp247.000
Slot 50+:    Rp297.000
```

---

## Step-by-Step Workflow

### ASSET 1 — Pricing Table

```
Format output:
| Slot | Harga | Hemat |
|------|-------|-------|
| 1–10 | Rp X | Rp Y dari harga normal |
| ... | ... | ... |
| 50+  | Rp [FULL] | — |

Sertakan:
- Framing ROI: "Balik modal kalau dapat 1 [outcome]"
- Framing scarcity: genuine reason kenapa harga naik (bukan fake)
```

### ASSET 2 — Lynk.id / Sales Page Description

```
Format: 150-250 kata, siap paste ke Lynk.id atau Gumroad

Struktur:
[1 kalimat hook — hasil yang didapat]
[2-3 kalimat: untuk siapa + apa yang ada di dalamnya]
[Bullet list: 4-6 deliverables spesifik]
[1 kalimat social proof — dari credential atau klien]
[CTA + current pricing tier]
```

### ASSET 3 — Threads Launch Thread (7-10 post)

```
Struktur thread:
Post 1: Hook — curiosity atau pain point
Post 2: Problem agitation
Post 3: Tease solusi
Post 4: Reveal produk + apa isinya
Post 5: Social proof / case study mini
Post 6: Pricing ladder explanation ("kenapa harga naik setiap 10 pembeli")
Post 7: Objection handling (1 keberatan paling umum)
Post 8: FAQ singkat
Post 9: Urgency post ("sudah X pembeli, harga naik besok")
Post 10: Last call

Tone: gw/lo, casual, direct
Format per post: maks 280 karakter (Threads limit)
```

### ASSET 4 — Instagram Caption Set (3 post)

```
Post A — Announce (hari launch):
- Hook kuat + reveal produk
- 100-150 kata
- 20 hashtag (5 besar / 10 medium / 5 niche)
- CTA: "Link di bio" atau "DM [kata kunci]"

Post B — Social Proof (H+2):
- Mini testimonial atau hasil early buyers
- Format storytelling: before → after
- CTA: urgency (harga naik setelah X pembeli)

Post C — Last Call (H+5 atau saat slot hampir habis):
- "X slot tersisa di harga Y"
- Direct CTA
```

### ASSET 5 — WhatsApp Broadcast Copy (2 versi)

```
Versi A — Short (untuk WA status / broadcast singkat):
Maks 3 kalimat + link

Versi B — Long (untuk WA group atau blast):
- Context: siapa yang kirim, kenapa relevan untuk penerima
- Produk: apa, untuk siapa, apa yang didapat
- Harga current + deadline
- Link atau cara beli
Maks 200 kata
```

### ASSET 6 — Launch Timeline

```
Format:
H-3: [action]
H-1: [action]
H0 (Launch Day): [action — post apa, di mana, jam berapa]
H+1: [follow-up action]
H+2: [social proof post]
H+3–5: [engagement + objection handling]
H+7 / Last Day: [last call across all platforms]

Default launch window: 7 hari
Optimal posting time Indonesia: 07:00, 12:00, 19:00 WIB
```

---

## Output Format

```
Deliver semua 6 asset dalam satu response:

═══════════════════════════════
LAUNCH PACK: [NAMA PRODUK]
Generated: [tanggal]
═══════════════════════════════

ASSET 1 — PRICING TABLE
[...]

ASSET 2 — LYNK.ID DESCRIPTION
[...]

ASSET 3 — THREADS THREAD
[Post 1] [...]
[Post 2] [...]
...

ASSET 4 — INSTAGRAM CAPTIONS
[Post A] ...
[Post B] ...
[Post C] ...

ASSET 5 — WA BROADCAST
[Versi A] ...
[Versi B] ...

ASSET 6 — LAUNCH TIMELINE
[...]

═══════════════════════════════
⚠️ KONFIRMASI SEBELUM LAUNCH:
- [item yang perlu Bani verify]
═══════════════════════════════
```

---

## Tone & Style Guidelines

**Threads & Instagram:** gw/lo, casual, punchy, banyak whitespace
**Lynk.id / Gumroad:** semi-formal, benefit-first, angka konkret
**WA Broadcast:** personal, langsung ke poin, tidak spam-feel
**Pricing framing:** selalu ROI-based ("balik modal kalau dapat X"), bukan discount-based

---

## Credential Anchors (Selalu Sertakan Minimal 1)
- "18 tahun experience"
- "1000+ clients di 4 negara"
- "Google & Meta Certified"
- "Trainer untuk C-suite & UN Agency"
- Angka hasil klien: "Rp300 juta dari Instagram" / "10 tahun retention"

---

## Example Input

```
Launch pack untuk:
Nama: "100 Prompt ChatGPT untuk Business Owner Indonesia"
Format: PDF
Harga target: Rp297.000 full
Platform: Lynk.id + Instagram + Threads
```

## Example Output — ASSET 1 (Pricing Table)

```
ASSET 1 — PRICING TABLE

| Slot    | Harga       | Hemat dari Normal |
|---------|-------------|-------------------|
| 1–10    | Rp 97.000   | Rp 200.000        |
| 11–20   | Rp 147.000  | Rp 150.000        |
| 21–30   | Rp 197.000  | Rp 100.000        |
| 31–50   | Rp 247.000  | Rp 50.000         |
| 51+     | Rp 297.000  | —                 |

ROI Framing:
"1 prompt yang berhasil menghemat 2 jam kerja = balik modal.
Kalau lo business owner, itu bukan pertanyaan — itu investasi."

Scarcity Reason (genuine):
"Harga naik setiap 10 pembeli karena gw mau reward orang yang
action duluan — bukan karena marketing trick."
```

---

## Notes
- Scarcity harus genuine — jangan tulis slot limit kalau tidak ada sistem trackingnya
- Jika Lynk.id, reminder: platform ini charge fee transaksi — factor in ke pricing
- Digital product = tidak ada batas kapasitas, tapi Hormozi ladder tetap berlaku untuk urgency
- Kalau ada alumni discount (contoh kasus email Lebaran), buat versi terpisah copy untuk segmen itu
