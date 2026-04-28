# PRD: Second Brain for Founders (SBF)
**Version:** 1.0
**Date:** 2026-04-17
**Owner:** Bani Risset
**Status:** Drafting Strategy & Monetization

---

## 1. Overview

**Second Brain for Founders (SBF)** adalah sistem infrastruktur intelijen pribadi (Personal Intelligence Infrastructure) yang dirancang khusus untuk pengambil keputusan tingkat tinggi. Sistem ini memisahkan antara **Capture Layer** (Telegram), **Storage Layer** (Obsidian), dan **Intelligence Layer** (LLM/Vector DB) untuk memastikan data tetap privat, mudah diakses, dan bisa memberikan jawaban cerdas berdasarkan konteks pengetahuan pribadi user.

---

## 2. Problem Statement

Founder dan Consultant memiliki masalah "Information Leakage" dan "Context Fragmentation". Mereka mengonsumsi banyak data tapi gagal mengubahnya menjadi aset strategis karena friction saat mencatat dan kesulitan saat mencari kembali.

**Gap yang diisi SBF:** Menghubungkan kenyamanan chat (Telegram) dengan ketangguhan knowledge base (Obsidian) dan kecerdasan AI (Retrieval-Augmented Generation).

---

## 3. Goals

### Business Goals (Monetization)
- **Revenue Target:** Rp 150.000.000 dalam 3 bulan pertama.
- **Conversion:** Minimum 10% pembeli Kit (Tier 1) upgrade ke High-Ticket Implementation (Tier 3).
- **Productivity:** Mengurangi waktu produksi konten *Authority Architecture* (Day 23 Content Calendar) sebesar 70%.

### Product Goals
- **Zero Friction Capture:** Ide tersimpan dalam < 5 detik via Telegram.
- **High-Fidelity Retrieval:** Jawaban AI harus menyertakan sitasi sumber note asli dari vault Obsidian.
- **Data Sovereignty:** 100% data tersimpan lokal/private cloud milik user, bukan di server proprietary SBF.

---

## 4. Target Users

### Primary Persona — "The Visionary Founder"
- **Siapa:** CEO startup, owner UMKM naik kelas, Business Owner.
- **Pain point:** Punya banyak ide tapi tim sering bingung karena arahan tidak terdokumentasi atau konteks hilang.
- **Need:** Satu tempat yang bisa ditanya "Apa rencana kita untuk Project X?" dan dijawab berdasarkan semua meeting note sebelumnya.

### Secondary Persona — "The Authority Consultant"
- **Siapa:** Coach, strategist, pemikir yang membangun personal brand.
- **Pain point:** Sulit menulis konten rutin karena riset tercecer.
- **Need:** Sistem yang bisa merangkum semua riset menjadi draft konten dalam hitungan detik.

---

## 5. Monetization Strategy & Packaging

Sistem ini dirancang untuk menghasilkan uang melalui tiga lapisan:

### Tier 1: SBF Digital Kit (Low-Ticket Product)
- **Format:** Digital download.
- **Price Point:** Rp 997.000 (Psychological anchor under 1jt).
- **Inclusions:**
    - Obsidian Vault Starter Template (PARA + Authority folders).
    - System Prompt Library (Parsing, Summarizing, Drafting).
    - Video Course: "Setup your AI Second Brain in 60 mins".
    - Telegram Bot Blueprint (No-code setup).

### Tier 2: The Strategic Brain (Mid-Ticket / DWY)
- **Format:** Done-with-You (DWY).
- **Price Point:** Rp 7.500.000.
- **Inclusions:**
    - Everything in Tier 1.
    - 2x Consulting Sessions (Workflow mapping).
    - Custom Classification Logic setup.
    - 30 Days Slack/WhatsApp support.

### Tier 3: Intelligence Command Center (High-Ticket / DFY)
- **Format:** Done-for-You (DFY).
- **Price Point:** Rp 25.000.000 - Rp 75.000.000.
- **Inclusions:**
    - White-glove setup oleh tim Bani Risset.
    - Custom Vector Database (Qdrant/Milvus) integration.
    - Voice-to-Note premium transcription integration.
    - Executive Assistant training (mengelola vault founder).
    - Full "Authority Architecture" setup untuk 3 bulan konten.

---

## 6. Core Features (V1)

### F01: Telegram Quick-Capture
- Integrasi Telegram Bot untuk teks dan audio.
- Auto-tagging berdasarkan keyword atau AI-intent.
- Langsung masuk ke folder `/inbox` di Obsidian.

### F02: Obsidian Semantic Vault
- Folder structure yang dioptimasi untuk Founder (Projects, Decisions, People, Resources).
- Templater scripts untuk metadata otomatis.

### F03: AI Retrieval Interface
- Command `/ask` di Telegram untuk tanya database.
- RAG (Retrieval Augmented Generation) yang membaca file `.md`.
- Citation logic: "Menurut catatan Anda pada 12 April (Project X), strateginya adalah..."

---

## 7. Success Metrics

- **NPS (Net Promoter Score):** > 60.
- **User Activity:** > 5 capture per hari (Founder level).
- **Retrieval Accuracy:** > 90% (AI tidak halusinasi, tetap pada data vault).
