# Obsidian-First with 3 Premium Stack

## Summary

- `knowledge-base/` tetap source of truth memory dan knowledge jangka panjang.
- `REED` adalah orchestrator tunggal yang memilih tool, menormalkan hasil, dan memutuskan promotion ke wiki.
- `Firecrawl` dipakai untuk web, URL, PDF, dan dokumen berbasis web.
- `AssemblyAI` dipakai untuk YouTube, audio, video, voice note, dan meeting recording.
- `You.com Research` dipakai untuk research query multi-source yang butuh jawaban bersitasi cepat.
- Output vendor adalah **transient object**, bukan canonical memory.

## Operating Model

### 1. Intake

`REED` menerima input lalu mengklasifikasikannya:

- `web_doc`
- `audio_video`
- `research_query`
- `direct_reasoning`

### 2. Tool Routing

| Input | Tool Default | Output |
| --- | --- | --- |
| URL artikel / docs / landing page | `Firecrawl` | markdown + metadata |
| PDF / docx / xlsx URL | `Firecrawl` | parsed text + metadata |
| YouTube / podcast / audio / video | `AssemblyAI` | transcript + metadata |
| Pertanyaan research kompleks | `You.com Research` | cited answer + sources |
| Chat biasa / refleksi / keputusan langsung | none / `REED` | reasoning langsung |

### 3. Normalization

Semua hasil tool diubah dulu ke object kerja internal:

- `source_type`
- `source_url`
- `title`
- `captured_at`
- `content`
- `metadata`
- `provenance`
- `confidence`
- `promotion_candidate`

Object ini hidup di context sesi dan staging, bukan langsung jadi note final.

### 4. Memory Decision

Setelah baca source, `REED` memilih salah satu:

- `transient only`
- `update active session memory`
- `promote to canonical wiki`

## Promotion Rules

### Promote ke wiki bila:

- ada keputusan yang perlu dilacak
- ada fakta reusable lintas sesi
- ada referensi luar yang akan dipakai ulang
- ada meeting atau voice capture dengan action items
- ada memo riset yang bernilai compounding
- ada perubahan state proyek, SOP, atau operating context

### Tetap transient bila:

- hanya dipakai untuk menjawab satu pertanyaan sesaat
- hasil search/snippet belum cukup kuat
- transcript mentah belum punya nilai reuse
- isi duplikat dengan canonical note yang sudah ada
- isi terlalu noisy, terlalu mentah, atau terlalu sensitif

### Hard Rules

- Jangan dump hasil mentah vendor ke folder canonical.
- Raw scrape, transcript penuh, dan payload research tetap di staging/raw bila perlu audit.
- Wiki final hanya berisi sintesis ringkas dengan source jelas.
- Summary ke user hanya dibuat jika diminta eksplisit.
- Distilled note internal boleh dibuat tanpa mengirim summary ke user jika promotion threshold terpenuhi.

## Folder Mapping

| Jenis Hasil | Folder Final |
| --- | --- |
| Insight umum / operating note | `knowledge-base/notes/` |
| Konteks proyek | `knowledge-base/projects/` |
| Keputusan penting | `knowledge-base/decisions/` |
| Artikel / PDF / docs / video referensi | `knowledge-base/references/` |
| Memo komparasi / vendor scan / market scan | `knowledge-base/research/` |
| Meeting / call / sync | `knowledge-base/meetings/` |
| Working memory aktif | `knowledge-base/wiki/sessions/*-active.md` |

## Retrieval Order

Saat menjawab query:

1. baca `wiki/sessions/*-active.md`
2. baca note canonical di `knowledge-base/`
3. jika context internal tidak cukup, ambil live source via tool
4. jika hasil live bernilai tinggi, pertimbangkan promotion sesudahnya

`raw/` dan staging bukan corpus retrieval utama.

## Vendor-Specific Notes

### Firecrawl

- Default untuk web/doc ingestion
- paling sehat untuk menambah breadth mini-RAG
- promote hanya jika source authoritative atau reusable

### AssemblyAI

- Default untuk media ingestion
- transcript mentah tidak langsung jadi canonical
- chapter/topic/speaker metadata dipakai untuk note meeting atau reference yang lebih rapi

### You.com Research

- hanya untuk research lane
- hasilnya memo percepatan, bukan canonical truth mentah
- source URL wajib ikut tersimpan jika dipromosikan

## Mini-RAG Impact

- `Firecrawl` menaikkan kualitas chunk web/doc karena markdown lebih bersih
- `AssemblyAI` membuat media menjadi searchable text
- `You.com Research` mempercepat lahirnya memo riset berkualitas
- `Obsidian/wiki` tetap jadi filter terakhir agar retrieval tetap presisi dan tidak banjir noise
