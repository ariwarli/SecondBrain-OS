<!--
Tujuan: taxonomy resmi wiki canon untuk workspace Hermes Bani Risset
Caller: agent utama, archivist, builder, researcher, dan sesi startup
Dependensi: AGENTS.md, docs/INBOX_ROUTING.md, knowledge-base/wiki/log.md
Main Functions: definisi bucket canon, aturan klasifikasi, aturan eskalasi dari Hermes ke Wiki
Side Effects: menjadi source of truth untuk penyimpanan canon dan recall agent
-->

# Wiki Canon Index

Wiki adalah layer pengetahuan durable untuk workspace Hermes Bani Risset.

## Boundary

- `INBOX` = intake layer only
- `Hermes` = operational continuity and action memory
- `Wiki` = durable canon for reusable knowledge

Aturan keras:

- jangan pakai `INBOX` sebagai final bucket
- jangan biarkan `Hermes` menjadi wiki
- jangan biarkan `Wiki` menjadi RAM agent

## Canon Buckets

### `Research`

Untuk synthesis, temuan, benchmark, analisis, atau insight yang masih berguna lintas waktu.

Masuk sini bila dokumen menjawab: "apa yang ditemukan?"

### `Frameworks`

Untuk model berpikir, rubric, decision lens, scorecard, atau playbook konseptual.

Masuk sini bila dokumen menjawab: "bagaimana menilai atau memikirkan sesuatu?"

### `SOPs`

Untuk prosedur kerja yang harus diulang konsisten.

Masuk sini bila dokumen menjawab: "bagaimana menjalankan sesuatu?"

Current canon entries:
- `knowledge-base/wiki/SOPs/sop-intake-dokumen-reed.md`
- `knowledge-base/wiki/tailscale-setup.md` — Tailscale install, connect, SSH built-in, ACL

### `Decisions`

Untuk keputusan final, alasan singkat, dan konsekuensi operasionalnya.

Masuk sini bila dokumen menjawab: "apa yang sudah dipilih?"

### `Incidents`

Untuk failure, root cause, fix, dan preventive lesson.

Masuk sini bila dokumen menjawab: "apa yang rusak dan apa pelajarannya?"

## What Is Not Canon

Ini tidak otomatis masuk canon:

- raw links
- PDF mentah
- meeting note status-only
- to-do harian
- daily recap
- dump transcript

`Sources` hanya jadi supporting layer di dalam entry canon yang relevan.

## Classification Rules

- Jika dokumen mengajari **menilai** sesuatu -> `Frameworks`
- Jika dokumen mengajari **menjalankan** sesuatu -> `SOPs`
- Jika dokumen mengunci **pilihan final** -> `Decisions`
- Jika dokumen merangkum **temuan** -> `Research`
- Jika dokumen menjelaskan **failure + fix** -> `Incidents`

## Operational -> Canon Escalation

Item dari `tasks`, `content`, `personal-crm`, `ops`, atau `knowledge-base` baru naik ke wiki jika sudah punya nilai reuse jangka panjang.

Contoh:

- hasil analisis kompetitor -> `Research`
- rubric memilih offer -> `Frameworks`
- alur Inbox -> classify -> route -> confirm -> `SOPs`
- keputusan `INBOX tetap hidup` -> `Decisions`
- bug Hermes salah baca config legacy -> `Incidents`
