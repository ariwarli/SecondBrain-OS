---
source_url: https://github.com/AIDC-AI/Pixelle-Video
ingested: 2026-05-05
sha256: eb7b6ba5c1c20cdc2fca48e1a3ccd4a6f3a9c8d7e5f4b3a2c1d0e9f8a7b6c5d4
---

# Pixelle-Video — AI Fully Automated Short Video Engine

**GitHub:** AIDC-AI/Pixelle-Video
**License:** Apache-2.0
**Stars:** 11.5k | **Forks:** 1.8k

Input a topic → automatically writes script, generates AI images/videos, synthesizes voice narration, adds background music, compiles video.

## Key Features
- Fully automatic: topic → script → images/video → TTS → BGM → final video
- AI smart copywriting
- AI generated images/videos (WAN 2.1, FLUX)
- TTS: Edge-TTS, Index-TTS, voice cloning via reference audio
- Digital human, image-to-video, motion transfer
- Custom media upload (photos/videos, AI analyzes for script generation)
- Multiple visual templates & aspect ratios (portrait, landscape, square)
- Multi-model: GPT, Qwen, DeepSeek, Ollama
- Based on ComfyUI — atomic capability composition
- RunningHub 48G VRAM cloud GPU support
- Batch video creation, history page

## Quick Start
- Windows all-in-one: download release → extract → double-click start.bat
- Source: `git clone` → `uv run streamlit run web/app.py` → http://localhost:8501

## System Requirements
- ComfyUI for image/video generation (local GPU or RunningHub cloud)
- LLM API key (Ollama free, Qwen low-cost, OpenAI cloud)
- No GPU needed for text-only mode

## Pricing
- Free: Ollama (local LLM) + ComfyUI local = $0
- Recommended: Qwen (low cost) + ComfyUI local
- Cloud: OpenAI + RunningHub (higher cost, no GPU needed locally)
