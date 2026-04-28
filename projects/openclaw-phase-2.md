# Project Brief

Fase ini melanjutkan setup inti OpenClaw setelah infra, scheduler, dan workspace dasar sudah stabil.

## Project

- Name: OpenClaw Phase 2
- Owner: banirisset
- Status: active
- Start date: 2026-04-09
- Deadline: rolling

## Objective

- Outcome yang diinginkan: workspace berubah dari "sudah terpasang" menjadi "siap dipakai harian"
- Kenapa ini penting: setup inti sudah sehat, tapi visibilitas task, voice capture, dan jalur integrasi kerja sehari-hari belum rapi
- Apa yang dianggap selesai: ada jalur jelas untuk Todoist, voice-first capture, helper Google Workspace, dan output riset overnight

## Scope

- In scope:
  - definisi fase kerja lanjutan
  - scaffolding folder kerja untuk integrasi berikutnya
  - aturan rekonsiliasi NotebookLM vs state lokal
  - konvensi output riset
- Out of scope:
  - implementasi penuh OAuth Google
  - implementasi penuh sync Todoist tanpa token dan project mapping
  - perubahan runtime VPS yang belum perlu
- Batasan:
  - topic Telegram aktif harus mengikuti mapping `SecondBrain OS`
  - state lokal menang kalau berbeda dengan contoh di NotebookLM

## Core Features / Deliverables

1. Todoist visibility layer
2. Voice-first intake path
3. Research output convention

## Inputs / Context

- Repos / files: `openclaw.md`, `daily.md`, `crm.md`, `openclaw-rules.md`, `automation/schedule.yaml`
- URLs / references: NotebookLM `OpenClaw` `05667e4d-493c-4236-83a4-ae74dadb178e`
- Existing assets: VPS scheduler, PM2 runtime, Telegram topics, automation jobs
- Dependencies: Todoist token, Google auth flow, voice transcription provider

## Execution Rules

- Mulai dari workflow, bukan integrasi acak.
- Jangan implementasi penuh integrasi yang masih butuh secret tanpa kebutuhan operasional yang jelas.
- Semua tambahan harus memperkecil friction harian, bukan menambah panel baru.
- Telegram tetap interface utama.

## Subagent Split

- Main agent: jaga struktur workspace, rules, dan orchestration
- Research subagent: eksperimen flow Todoist / Google / voice capture
- Build subagent: implement script kecil yang bounded
- QA / review subagent: review noise, failure mode, dan cost

## Output Format

- Artifact yang diharapkan: brief fase kerja + folder scaffolding + aturan yang konsisten
- Summary yang diharapkan: next actions yang bisa langsung dipilih
- Where to store: workspace root dan `projects/`

## Risks

- Technical risk: integrasi terburu-buru tanpa secret management yang rapi
- Dependency risk: NotebookLM memberi pola umum, bukan state aktual runtime
- Decision risk: terlalu cepat menambah integrasi sebelum problem harian tervalidasi

## Next Step

- Immediate next action: siapkan `scripts/` dan `research/` sebagai jalur kerja lanjutan, lalu pilih mana yang diimplementasikan lebih dulu
