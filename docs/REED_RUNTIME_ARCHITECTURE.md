<!--
Tujuan: source of truth arsitektur runtime REED/Hermes
Caller: operator workspace, agent utama, builder, dan auditor runtime
Dependensi: hermes.md, automation/reed-runtime-spec.yaml, docs/INBOX_ROUTING.md, docs/REED_MEMORY_AND_LEARNING.md
Main Functions: mendefinisikan komponen inti runtime, boundary service, dan kontrak otonomi
Side Effects: jadi acuan implementasi REED agar tidak kembali ke model runtime lama yang terfragmentasi
-->

# REED Runtime Architecture

Dokumen ini menggantikan model mental lama `REED + REED DULL + script terpisah` menjadi satu runtime REED yang utuh.

## Target State

REED harus beroperasi sebagai satu autonomous agent platform dengan feature-class parity terhadap Hermes pada level capability:
- gateway multi-channel
- persistent memory
- session recall
- skills system
- MCP/tool orchestration
- cron / scheduled autonomy
- subagents
- voice
- approvals
- sandboxed execution
- auditability

Fase implementasi tetap boleh bertahap. Arsitektur targetnya tidak boleh ambigu.

## Runtime Core

REED runtime dibagi menjadi 7 subsistem:

1. `gateway`
- menerima input dari Telegram dan channel lain
- memegang session per thread/channel key
- menjalankan cron tick
- mengirim delivery balik ke channel asal atau target yang ditentukan

2. `agent-core`
- loop inferensi utama
- context assembly
- tool routing
- skill loading
- subagent delegation
- approval checks

3. `memory`
- compact operational memory
- session recall/search
- promotion bridge ke wiki canon

4. `skills`
- registry skill sistem dan domain
- instalasi, versi, evaluasi, dan self-improvement

5. `scheduler`
- one-shot reminders
- recurring jobs
- skill-backed cron jobs
- overnight work orchestration

6. `execution`
- trusted local execution
- guarded internal execution
- sandboxed execution untuk job berisiko atau berat

7. `observability`
- logs
- audit trail
- job status
- memory write audit
- approval history

## Canonical Boundaries

Boundary baru yang harus dipakai:
- `REED runtime` = satu platform terpadu yang memiliki gateway, cron, memory, tools, dan delegation
- `scheduler` = subsystem internal REED, bukan persona/bot terpisah
- `subagents` = worker internal REED, bukan interface pengguna utama
- `wiki canon` = pustaka/journal jangka panjang, bukan live agent RAM

Boundary lama yang harus dihentikan:
- memikirkan `REED DULL` sebagai sistem kedua yang berdiri sendiri
- memisahkan reminder/cron dari session agent seolah-olah itu lane lain
- menaruh terlalu banyak state kerja di dokumen naratif tanpa kontrak runtime

## Session Model

Setiap percakapan harus memiliki session key yang stabil:
- platform
- conversation/chat id
- thread/topic id jika ada

Per session, REED harus punya:
- active context
- checkpoint summary
- recent tool actions
- approval state
- memory candidates

Reset policy target:
- idle-based reset
- periodic checkpointing
- carry-over summary, bukan full transcript

## Channel Strategy

Arsitektur harus siap untuk:
- Telegram
- Email
- voice-capable channel
- web/file/URL ingestion lane

Telegram tetap jadi jalur aktivasi paling awal, tapi bukan satu-satunya asumsi desain.

## Execution Tiers

Semua aksi REED harus jatuh ke salah satu tier ini:

### Tier 1: Autonomous Internal
- routing inbox
- update internal state non-destruktif
- summaries
- memory writes
- wiki promotion prep
- research synthesis

### Tier 2: Guarded Internal
- file edits
- script execution
- internal maintenance
- local builds/checks
- scheduled internal jobs

### Tier 3: Approval-Gated
- destructive shell actions
- public posting
- external outreach
- production config mutation
- risky service restarts
- actions that spend money or expose data

## Tool Surface

REED harus mengelola tool surface seperti Hermes:
- tools dikelompokkan per risk class
- channel tertentu hanya melihat subset tool yang aman
- MCP server/tool bisa difilter, bukan semua langsung terbuka

Minimum tool classes yang harus ada:
- terminal
- web/search/browse
- file/context
- memory
- cron
- messaging send/read
- subagent delegation
- MCP
- code execution for multi-step pipelines

## Service Contract

Implementasi apapun ke depan harus memenuhi kontrak ini:
- satu gateway process atau service group yang menjadi pintu masuk utama
- scheduler tick terintegrasi dengan gateway
- session store persisten
- memory store persisten
- logs dan audit terpisah dari content canon
- skill registry punya source of truth tunggal

## Source Of Truth

Urutan acuan:
1. `docs/REED_RUNTIME_ARCHITECTURE.md`
2. `automation/reed-runtime-spec.yaml`
3. `docs/REED_MEMORY_AND_LEARNING.md`
4. `docs/INBOX_ROUTING.md`
5. `hermes.md` untuk state transisi dan compat notes

`hermes.md` tetap relevan selama masa migrasi, tetapi bukan lagi satu-satunya brain runtime.
