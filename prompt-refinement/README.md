# Prompt Refinery

Sistem untuk mengubah prompt mentah jadi prompt berkualitas tinggi — siap pakai, reusable, dan terstruktur.

---

## Setup Awal

### 1. Siapkan Notion Databases
Buat 4 database di Notion (schema lengkap → `docs/notion-schema.md`):
- **Prompt Intake** — tempat dump prompt mentah
- **Refinement Queue** — tracking progress refine
- **QA Staging** — review sebelum publish
- **Prompt Library** — koleksi final

Setelah dibuat, paste Database IDs ke `CLAUDE.md`.

### 2. Mulai Sesi Refine
Claude akan baca `CLAUDE.md` otomatis. Lalu gunakan perintah dari `docs/workflow-commands.md`.

---

## Alur Kerja

```
Prompt Mentah
     ↓
  [INTAKE]        → dump ke prompts/intake/
     ↓
 [REFINE]         → 5-Layer Method → prompts/in-progress/
     ↓
  [QA SCORE]      → scoring 0–50 → prompts/refined/
     ↓
  ≥ 40?
  ├─ Ya  → prompts/library/ + Notion Library
  └─ Tidak → revisi ulang dari layer yang lemah
```

---

## Folder Structure

```
prompt-refinement/
├── CLAUDE.md               ← instruksi permanen Claude
├── README.md               ← file ini
├── docs/
│   ├── 5-layer-method.md   ← metode ROLE-CONTEXT-TASK-FORMAT-CONSTRAINT
│   ├── qa-scorecard.md     ← rubrik scoring + testing protocol
│   ├── id-convention.md    ← format ID per kategori
│   ├── notion-schema.md    ← schema 4 database Notion
│   ├── prompt-examples.md  ← benchmark 2 contoh prompt QA 44-46/50
│   └── workflow-commands.md ← template perintah siap copas
└── prompts/
    ├── intake/             ← prompt mentah masuk di sini
    ├── in-progress/        ← sedang direfine
    ├── refined/            ← sudah direfine, menunggu QA review
    └── library/            ← approved, score ≥ 40
```

---

## Quick Start

```
# Mulai refine 1 prompt
"Refine prompt ini: [paste prompt mentah]"

# Batch refine dari Notion
"Ambil 5 prompt Status=New dari Intake DB, refine semua"

# Cek QA score
"Beri QA score untuk prompt [ID] ini: [paste prompt]"
```

Template lengkap → `docs/workflow-commands.md`

---

*Dibuat: 2026-03-29*
