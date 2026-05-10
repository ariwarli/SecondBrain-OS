# Docs Audit

**Tujuan:** membedakan dokumen yang sebaiknya dianggap final, reference, atau draft/overlap.

## Keep as Primary

Dokumen ini sebaiknya jadi rujukan utama sehari-hari.

### User-facing

- `openclaw/START-HERE.md`
- `openclaw/USER-ONE-PAGER.md`
- `openclaw/DAILY-OPERATING-RHYTHM.md`
- `openclaw/docs/REED-INTERACTION-GUIDE.md`
- `openclaw/docs/REED-STARTER-TEMPLATES.md`
- `openclaw/docs/TELEGRAM-TOPIC-CHEAT-SHEET.md`

### Runtime / System

- `openclaw/AGENTS.md`
- `knowledge-base/README.md`
- `knowledge-base/index.md`
- `knowledge-base/wiki/index.md`
- `openclaw/docs/BOT-MATRIX.md`
- `openclaw/docs/ROUTING-VERIFICATION-REPORT.md`

## Keep as Reference

Dokumen ini penting, tapi bukan entrypoint harian.

- `openclaw/Panduan 2 SecondBrain LLM Architecture.md`
- `openclaw/Blueprint Implementasi SecondBrain LLM.md`
- `openclaw/Panduan Pengguna SecondBrain LLM.md`
- `openclaw/SecondBrain LLM - Naskah Final.md`
- `openclaw/docs/INBOX-ROUTER-GUIDE.md`
- `openclaw/docs/SECONDBRAIN-MASTER-BLUEPRINT.md`
- `openclaw/docs/HANDOFF-PROTOCOL.md`
- `openclaw/docs/SOP-main.md`
- `openclaw/docs/SOP-reed-archivist.md`
- `openclaw/docs/SOP-reed-builder.md`
- `openclaw/docs/SOP-reed-researcher.md`
- `openclaw/docs/SOP-reed-wellbeing.md`

## Keep as Historical / Session Output

Dokumen ini bernilai sebagai artefak proses, bukan acuan utama jangka panjang.

- `openclaw/archive/2026-04-16/Panduan 1 SecondBrain LLM.md`
- `openclaw/archive/2026-04-16/Blueprint 16 April.md`
- `openclaw/archive/2026-04-16/Artikel SecondBrain LLM.md`
- `openclaw/archive/2026-04-16/CHANGELOG-SESSION.md`

## Potential Overlap

Bagian yang perlu disadari agar tidak membingungkan:

### User onboarding

Overlap:

- `START-HERE.md`
- `USER-ONE-PAGER.md`
- `REED-INTERACTION-GUIDE.md`
- `REED-STARTER-TEMPLATES.md`

Rekomendasi:

- pakai `START-HERE.md` sebagai pintu masuk
- pakai `USER-ONE-PAGER.md` sebagai ringkasan
- pakai `REED-INTERACTION-GUIDE.md` untuk pemahaman topic
- pakai `REED-STARTER-TEMPLATES.md` untuk prompt siap copas

### Conceptual docs

Overlap:

- `Panduan Pengguna SecondBrain LLM.md`
- `SecondBrain LLM - Naskah Final.md`
- `Panduan 2 SecondBrain LLM Architecture.md`

Rekomendasi:

- `Panduan 2` = teknis
- `Naskah Final` = narasi utama
- `Panduan Pengguna` = manual user

## Draft / Needs Later Consolidation

Ini bukan berarti buruk. Hanya belum perlu jadi entrypoint utama.

- `openclaw/archive/2026-04-16/Artikel SecondBrain LLM.md`
- `openclaw/archive/2026-04-16/Panduan 1 SecondBrain LLM.md`
- `openclaw/archive/2026-04-16/Blueprint 16 April.md`

## Suggested Reading Order

Kalau user baru masuk:

1. `openclaw/START-HERE.md`
2. `openclaw/USER-ONE-PAGER.md`
3. `openclaw/docs/TELEGRAM-TOPIC-CHEAT-SHEET.md`
4. `openclaw/docs/REED-STARTER-TEMPLATES.md`

Kalau mau paham sistem:

1. `openclaw/docs/REED-INTERACTION-GUIDE.md`
2. `knowledge-base/index.md`
3. `knowledge-base/wiki/index.md`
4. `openclaw/SecondBrain LLM - Naskah Final.md`

Kalau mau audit runtime:

1. `openclaw/AGENTS.md`
2. `openclaw/docs/BOT-MATRIX.md`
3. `openclaw/docs/ROUTING-VERIFICATION-REPORT.md`
