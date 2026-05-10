# Blueprint Implementasi Second Brain LLM

## Ringkasan

Blueprint ini ditujukan untuk membangun sistem Second Brain berbasis LLM dengan pembagian peran yang tegas:

- `Telegram` sebagai capture layer dan quick-query interface
- `Obsidian` sebagai canonical knowledge store berbasis Markdown
- `LLM` sebagai parsing, retrieval, synthesis, dan drafting layer

Target implementasi:

- input data cepat dari mobile dan desktop
- knowledge tersimpan dalam format terbuka
- retrieval akurat dengan sitasi sumber
- update knowledge dapat diaudit
- arsitektur tahan terhadap perubahan model atau vendor

## Tujuan Sistem

Sistem harus mampu:

1. menangkap data mentah dari chat, voice note, file, dan link
2. mengubah data mentah menjadi note atau record yang terstruktur
3. menyimpan knowledge final ke vault Markdown
4. mengindeks knowledge ke vector database
5. menjawab pertanyaan dengan retrieval yang relevan
6. memperbarui index saat knowledge berubah
7. menjaga audit trail dan data boundary

## Prinsip Arsitektur

- Documents are source of truth
- Vector DB adalah indeks, bukan database utama
- Answers are ephemeral
- Retrieval harus mendahului generation
- Raw capture harus dipisah dari final knowledge
- Metadata wajib ada untuk semua entitas penting
- Update dan re-index adalah workflow inti, bukan pekerjaan tambahan

## Ruang Lingkup

### In Scope

- Telegram bot untuk capture dan quick query
- ingestion service
- transcription untuk voice note
- Markdown knowledge vault
- metadata database
- vector indexing
- retrieval API
- answer generation dengan source citation
- feedback loop dasar
- monitoring minimum

### Out of Scope untuk fase awal

- multi-tenant enterprise RBAC penuh
- fine-tuning model kustom
- autonomous agents yang menulis ke knowledge tanpa review
- multimodal reasoning tingkat lanjut di luar file dasar dan voice note

## Arsitektur Target

### Diagram Konseptual

```text
Telegram user
    ->
Telegram bot webhook
    ->
Ingestion API
    ->
Queue / worker
    ->
Transcription + parsing + classification + metadata extraction
    ->
Obsidian markdown vault
    ->
Embedding pipeline
    ->
Vector DB + PostgreSQL metadata DB
    ->
Retrieval API
    ->
LLM orchestration
    ->
Telegram reply / web UI answer
```

### Komponen

| Komponen | Fungsi | Output |
| --- | --- | --- |
| Telegram bot | Capture pesan, voice note, file, query cepat | raw events |
| Ingestion API | Validasi, normalisasi, enqueue jobs | normalized jobs |
| Worker | Transcription, parsing, classification | structured draft |
| Obsidian vault | Canonical storage | markdown notes |
| PostgreSQL | Metadata, registry, status, feedback | structured records |
| Vector DB | Semantic search index | retrieved chunks |
| Retrieval API | Query assembly, filters, reranking | context bundle |
| LLM orchestrator | Final answer, summary, drafting | user-facing response |

## Data Model

### Entitas Minimum

#### RawCapture

- `id`
- `source_type`
- `source_channel`
- `captured_at`
- `author`
- `raw_text`
- `file_path`
- `transcript`
- `status`

#### KnowledgeNote

- `id`
- `title`
- `slug`
- `note_type`
- `topic`
- `project`
- `summary`
- `markdown_path`
- `source_capture_ids`
- `created_at`
- `updated_at`
- `owner`
- `confidentiality_level`
- `version`

#### Chunk

- `id`
- `knowledge_note_id`
- `chunk_index`
- `chunk_text`
- `embedding_id`
- `token_count`
- `metadata_json`

#### QueryLog

- `id`
- `user_id`
- `query_text`
- `retrieved_note_ids`
- `latency_ms`
- `model_name`
- `answer_quality_signal`
- `created_at`

## Folder dan Storage Strategy

### Telegram

Telegram menyimpan event mentah sebagai transport layer. Jangan perlakukan Telegram sebagai source of truth jangka panjang.

### Obsidian Vault

Vault disarankan memiliki struktur awal:

```text
knowledge-base/
  inbox/
  raw/
  notes/
  projects/
  people/
  decisions/
  meetings/
  references/
  index.md
  log.md
```

### Aturan Folder

- `raw/` untuk material mentah yang perlu dipertahankan
- `inbox/` untuk draft yang belum dibersihkan
- `notes/`, `projects/`, `decisions/`, dan `meetings/` untuk knowledge final
- `index.md` untuk navigasi
- `log.md` untuk audit trail

## Workflow Detail

### 1. Capture Workflow

#### Input

- text message
- voice note
- forwarded link
- file attachment
- question ke bot

#### Langkah

1. Telegram bot menerima event
2. webhook mengirim event ke ingestion API
3. ingestion API membuat record `RawCapture`
4. event dimasukkan ke queue
5. worker memproses berdasarkan tipe input

#### Exit Criteria

- semua input punya raw record
- semua input punya status processing
- file atau transcript dapat dirujuk ulang

### 2. Processing Workflow

#### Untuk text message

- normalisasi text
- deteksi intent
- ekstrak metadata dasar
- klasifikasikan note type
- buat structured draft

#### Untuk voice note

- download file
- transcription
- cleanup transcript
- ekstrak intent dan summary
- buat structured draft

#### Untuk link atau file

- parse content
- ekstrak title, source, dan timestamp
- summarize
- tentukan apakah masuk `reference`, `research`, atau `project note`

#### Exit Criteria

- ada structured draft yang siap dipetakan ke markdown
- metadata minimum tersedia

### 3. Markdown Conversion Workflow

#### Tujuan

Mengubah draft terstruktur menjadi canonical note di Obsidian vault.

#### Template Minimum

```md
# Judul

## Summary

...

## Key Points

- ...

## Source

- Capture ID:
- Source:
- Timestamp:

## Tags

- ...
```

#### Exit Criteria

- note tersimpan di vault
- path note tercatat di database metadata
- provenance jelas

### 4. Indexing Workflow

#### Langkah

1. note markdown baru atau terupdate terdeteksi
2. parser membaca file
3. chunking dilakukan
4. metadata chunk dibentuk
5. embeddings dibuat
6. chunks dikirim ke vector DB
7. status index di PostgreSQL diperbarui

#### Exit Criteria

- note dapat ditemukan melalui semantic retrieval
- versi index sesuai versi dokumen

### 5. Query Workflow

#### Langkah

1. user bertanya via Telegram atau UI
2. query dinormalisasi
3. retrieval berjalan terhadap vector DB
4. metadata filter diterapkan
5. reranking dijalankan bila perlu
6. context bundle dirakit
7. LLM menghasilkan jawaban
8. jawaban dikembalikan dengan referensi sumber

#### Exit Criteria

- jawaban menyertakan note sumber
- sistem bisa menyatakan konteks tidak cukup jika retrieval lemah

### 6. Update Workflow

#### Langkah

1. note di Obsidian berubah
2. versi note meningkat
3. chunk lama ditandai stale
4. re-index dilakukan
5. query berikutnya hanya membaca versi terbaru

#### Exit Criteria

- tidak ada stale chunk yang masih dipakai
- perubahan knowledge bisa diaudit

## Pilihan Teknologi Referensi

### Jalur Pragmatic Managed

- Telegram Bot API
- FastAPI atau Express untuk ingestion API
- PostgreSQL
- pgvector atau Qdrant
- S3-compatible storage
- model proprietary untuk synthesis
- model embedding API

### Jalur Self-Hosted

- Telegram Bot API
- FastAPI
- PostgreSQL
- Qdrant atau Milvus
- local object storage atau MinIO
- open-source transcription
- open-source LLM untuk sebagian atau seluruh pipeline

## Fase Implementasi

### Fase 1: Foundation

#### Tujuan

Menetapkan boundary sistem dan storage yang benar.

#### Tugas

- definisikan use case prioritas
- tentukan taxonomy vault Obsidian
- definisikan metadata schema
- siapkan PostgreSQL
- siapkan vault repository
- siapkan Telegram bot

#### Verifikasi

- bot bisa menerima pesan
- vault bisa ditulis
- metadata DB tersedia

### Fase 2: Ingestion

#### Tujuan

Membuat input Telegram bisa menjadi note terstruktur.

#### Tugas

- bangun webhook receiver
- bangun queue dan worker
- tambahkan transcription untuk voice note
- buat classifier note type
- buat markdown template generator

#### Verifikasi

- text, voice note, dan link menghasilkan structured draft
- note masuk ke vault dengan format konsisten

### Fase 3: Indexing dan Retrieval

#### Tujuan

Membuat knowledge yang tersimpan bisa dicari secara andal.

#### Tugas

- implement parser vault
- implement chunking strategy
- tambahkan embedding pipeline
- simpan ke vector DB
- bangun retrieval API
- tambahkan metadata filters

#### Verifikasi

- query test mengembalikan chunk yang relevan
- note penting bisa ditemukan lintas format query

### Fase 4: Answer Generation

#### Tujuan

Menyambungkan retrieval ke answer layer.

#### Tugas

- buat prompt template retrieval QA
- tambahkan citation formatting
- buat fallback "context not sufficient"
- log query dan retrieval results

#### Verifikasi

- jawaban memakai sumber yang benar
- jawaban tidak mengarang saat konteks kosong

### Fase 5: Feedback dan Maintenance

#### Tujuan

Membuat sistem tetap segar dan bisa diukur.

#### Tugas

- simpan feedback relevan/tidak relevan
- tambahkan stale index detection
- implement re-index trigger
- buat log operasional
- ukur latency dan token usage

#### Verifikasi

- perubahan note memicu re-index
- feedback dapat ditinjau
- query health bisa dipantau

## Prompt Contract

### Retrieval QA Prompt Harus Memaksa

- hanya gunakan konteks yang diberikan
- tampilkan jawaban ringkas
- sertakan note sumber
- jika konteks tidak cukup, nyatakan itu
- jangan mengarang detail yang tidak ada di knowledge base

### Processing Prompt Harus Memaksa

- ubah raw input menjadi note terstruktur
- simpan fakta, jangan menambah opini baru
- simpan source metadata
- tandai ambiguity jika ada

## Best Practices Implementasi

- simpan raw dan final note secara terpisah
- pakai Markdown sebagai source of truth
- simpan provenance untuk setiap note
- jangan menjadikan Telegram sebagai knowledge base utama
- jangan biarkan LLM menulis final knowledge tanpa audit trail
- chunk berdasarkan batas semantik, bukan angka token semata
- gunakan metadata filter sebanyak mungkin
- ukur retrieval quality secara rutin

## Acceptance Criteria

Sistem dianggap mencapai baseline jika:

- Telegram bisa menangkap text, voice note, dan link
- input dapat diubah menjadi markdown note terstruktur
- note tersimpan di Obsidian vault
- note terindeks ke vector DB
- query dapat mengembalikan jawaban dengan sumber
- perubahan note memicu re-index
- query dan ingestion punya log dasar
- batas raw capture vs canonical knowledge jelas

## Risiko Utama

| Risiko | Dampak | Mitigasi |
| --- | --- | --- |
| Vault penuh noise | Retrieval buruk | review loop dan classification yang tegas |
| Metadata lemah | Filter buruk | schema minimum wajib |
| Stale embeddings | Jawaban salah konteks | versioning dan re-index trigger |
| Over-automation | Knowledge drift | human review untuk note penting |
| Vendor lock-in | Sulit migrasi | Markdown source of truth |

## Default Keputusan

- Telegram dipakai untuk capture dan quick query, bukan canonical storage
- Obsidian dipakai untuk canonical note store
- PostgreSQL dipakai untuk metadata dan operational logs
- vector DB dipakai sebagai retrieval index
- embeddings dan generation model dipisah
- retrieval dengan citation adalah baseline wajib

## Langkah Berikutnya

Urutan implementasi paling aman:

1. siapkan vault dan metadata schema
2. siapkan Telegram bot dan ingestion API
3. bangun worker text dan voice note
4. generate markdown notes
5. bangun indexing pipeline
6. bangun retrieval endpoint
7. tambahkan answer generation
8. tambahkan feedback, logging, dan re-index maintenance
