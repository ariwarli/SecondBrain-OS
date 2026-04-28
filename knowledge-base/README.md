<!--
Tujuan: orientasi singkat knowledge-base sebagai jalur antara bahan operasional dan wiki canon
Caller: agent utama, archivist, dan operator workspace
Dependensi: knowledge-base/wiki/index.md, docs/INBOX_ROUTING.md, AGENTS.md
Main Functions: menjelaskan boundary knowledge-base vs wiki dan alur eskalasi
Side Effects: menjadi acuan saat menyimpan atau mempromosikan knowledge baru
-->

# Knowledge Base

`knowledge-base` adalah lane kerja untuk bahan, ringkasan, dan knowledge yang masih diproses.

## Boundary

- `knowledge-base` = bahan operasional dan ingestion lane
- `knowledge-base/wiki` = canon durable

Jangan pakai `knowledge-base` sebagai gudang link mentah tanpa tindak lanjut.

## Canon Rule

Canon resmi ada di `knowledge-base/wiki/` dengan bucket:

- `Research`
- `Frameworks`
- `SOPs`
- `Decisions`
- `Incidents`

`Sources` bukan bucket canon utama. Source disimpan sebagai referensi pendukung di entry canon yang relevan.
