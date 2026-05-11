---
title: Pixelle-Video
created: 2026-05-05
updated: 2026-05-05
type: tool
tags: [ai-tool, video, opensource, comfyui, tts, github]
url: https://github.com/AIDC-AI/Pixelle-Video
sources: [raw/articles/pixelle-video.md]
status: active
---

# Pixelle-Video

**AI fully automated short video engine.** Apache 2.0 open-source, 11.5k stars.

## Overview
Input a topic → Pixelle-Video handles everything: script writing, AI image/video generation, TTS voiceover, background music, and video compilation. Built on ComfyUI architecture with modular workflow composition.

## Key Features
- **Automatic pipeline:** topic → script → ai-media → tts → bgm → video
- **Media generation:** supports WAN 2.1, FLUX, image-to-video, motion transfer, digital human
- **Voice:** Edge-TTS, Index-TTS, voice cloning with reference audio
- **Custom media:** upload your own photos/videos, AI analyzes + writes script
- **Multiple templates:** static, image-based, video-based templates
- **Multi-LLM:** GPT, Qwen, DeepSeek, Ollama

## Architecture
- **Web UI:** Streamlit on localhost:8501
- **Image/Video:** ComfyUI workflows (local GPU or RunningHub cloud)
- **LLM:** API-based (any OpenAI-compatible provider)

## Pricing
- Free tier: Ollama (local) + ComfyUI local = $0
- Low-cost: Qwen API + ComfyUI local
- Cloud: OpenAI + RunningHub (highest cost, no local GPU)

## Related
- [[entities/open-design.md|Open Design]] — design agent, also open-source creative tooling
- [[entities/command-code.md|Command Code AI]] — coding agent CLI, different domain but same self-hosted/API model
- [[comparisons/ai-content-tools-comparison.md|Content Tools Comparison]] — perbandingan dengan tool content creation lain

## Why Relevant for Bani
- Content creation automation — video marketing for clients
- Self-hosted, no monthly SaaS fees
- Can pair with API-based LLMs Bani already uses
