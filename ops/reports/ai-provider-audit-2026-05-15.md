# AI Provider Audit Report
**Date:** 2026-05-15  
**Scope:** `/home/openclaw/banirisset` (VPS Production)  
**Auditor:** Claude Code

---

## Executive Summary

**Total Active Providers:** 3  
**Total Models in Use:** 3  
**Primary Use Cases:** Voice transcription, brand summary generation, conversational AI  
**Critical Dependencies:** Groq (mandatory for voice), DeepSeek (brand monitoring)

### Key Findings
- ✅ Groq Whisper operational for voice transcription
- ✅ DeepSeek operational for brand summary generation
- ⚠️ MAIAROUTER configured but not actively used in production scripts
- ⚠️ No fallback mechanism for provider failures
- ⚠️ API keys managed via environment variables (good practice)

---

## Provider Inventory

### 1. Groq (Voice Transcription)

**Status:** ✅ Active  
**API Endpoint:** `https://api.groq.com/openai/v1/audio/transcriptions`  
**Model:** `whisper-large-v3`  
**Language:** Indonesian (`id`)  
**Response Format:** JSON

**Environment Variables:**
```bash
GROQ_API_KEY=<required>
```

**Usage Location:**
- File: `/home/openclaw/banirisset/openclaw/scripts/voice_watcher.py`
- Function: `transcribe(file_id)`
- Trigger: Telegram voice messages in monitored threads (Inbox #11, Wellbeing #19)

**Request Pattern:**
```bash
curl -X POST https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: bearer ${GROQ_API_KEY}" \
  -F "file=@/tmp/voice.ogg" \
  -F "model=whisper-large-v3" \
  -F "language=id" \
  -F "response_format=json"
```

**Error Handling:**
- Startup validation: Script exits if `GROQ_API_KEY` not set
- Runtime: Silent failure, no retry mechanism

**Cost Implications:**
- Pay-per-use (per audio minute)
- No rate limiting implemented

---

### 2. DeepSeek (Brand Summary Generation)

**Status:** ✅ Active  
**API Endpoint:** `https://api.deepseek.com/chat/completions`  
**Model:** `deepseek-chat`  
**Max Tokens:** 350  
**Temperature:** 0 (deterministic)

**Environment Variables:**
```bash
DEEPSEEK_API_KEY=<required>
```

**Usage Location:**
- File: `/home/openclaw/banirisset/openclaw/scripts/brand_summary_notify.py`
- Function: `summarize_diff(diff: str) -> str`
- Trigger: Git commits to tracked paths (Brand OS docs, memory.md)

**Tracked Paths:**
```python
TRACKED_PATHS = [
    "Brand OS - Bani Risset/claude-project/docs",
    "Brand OS - Bani Risset/claude-project/memory.md",
]
```

**Request Pattern:**
```python
payload = {
    "model": "deepseek-chat",
    "max_tokens": 350,
    "messages": [
        {"role": "system", "content": "Asisten ringkas. Fokus ke delta/perubahan terbaru saja. Bahasa Indonesia. No basa-basi."},
        {"role": "user", "content": prompt},
    ],
}
```

**Notification Target:**
- Telegram chat: `-1003344368011`
- Thread: `11` (Ops)

**State Management:**
- Last commit tracked: `/home/openclaw/.openclaw/workspace/.brand-summary-last-commit`
- Prevents duplicate notifications

**Error Handling:**
- No explicit error handling for API failures
- Silent failure if API key missing

---

### 3. MAIAROUTER (Configured, Not Active)

**Status:** ⚠️ Configured but unused  
**Environment Variables:**
```bash
MAIAROUTER_API_KEY=REPLACE_WITH_MAIAROUTER_API_KEY
```

**Configuration Files:**
- `/home/openclaw/banirisset/ops/openclaw-providers.env.example`
- `/home/openclaw/banirisset/openclaw/ops/openclaw-providers.env.example`

**Notes:**
- No active scripts reference MAIAROUTER
- Likely legacy or planned future integration
- Placeholder API key in example files

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Telegram Gateway                         │
│                  (Scheduler Bot Token)                       │
└────────────┬────────────────────────────────┬───────────────┘
             │                                │
             │ Voice Messages                 │ Git Commits
             │ (Inbox #11, Wellbeing #19)     │ (Brand OS paths)
             │                                │
             ▼                                ▼
    ┌────────────────┐              ┌────────────────────┐
    │ voice_watcher  │              │ brand_summary      │
    │     .py        │              │   _notify.py       │
    └────────┬───────┘              └─────────┬──────────┘
             │                                │
             │ /audio/transcriptions          │ /chat/completions
             │                                │
             ▼                                ▼
    ┌────────────────┐              ┌────────────────────┐
    │  Groq Whisper  │              │   DeepSeek Chat    │
    │ whisper-large  │              │  deepseek-chat     │
    │     -v3        │              │  (temp=0, 350tok)  │
    └────────┬───────┘              └─────────┬──────────┘
             │                                │
             │ Transcription                  │ Summary
             │                                │
             ▼                                ▼
    ┌────────────────────────────────────────────────────┐
    │           OpenClaw Agent Processing                │
    │         (REED conversational engine)               │
    └────────────────────────────────────────────────────┘
```

---

## Environment Variables Inventory

### Required Variables

| Variable | Provider | Used By | Validation |
|----------|----------|---------|------------|
| `GROQ_API_KEY` | Groq | voice_watcher.py | Startup check ✅ |
| `DEEPSEEK_API_KEY` | DeepSeek | brand_summary_notify.py | No validation ⚠️ |
| `SCHEDULER_BOT_TOKEN` | Telegram | voice_watcher.py | No validation ⚠️ |
| `TELEGRAM_BOT_TOKEN` | Telegram | brand_summary_notify.py | No validation ⚠️ |

### Optional Variables

| Variable | Provider | Status |
|----------|----------|--------|
| `MAIAROUTER_API_KEY` | MAIAROUTER | Configured, unused |

### Configuration Files

| File | Purpose | Status |
|------|---------|--------|
| `/home/openclaw/banirisset/automation/telegram-config.json` | Chat IDs, thread mappings | Active |
| `/home/openclaw/.openclaw/openclaw-gateway.env` | Gateway environment | Active |
| `/home/openclaw/.openclaw/workspace/.brand-summary-last-commit` | State tracking | Active |

---

## API Call Patterns

### Groq Whisper (Voice Transcription)

**Endpoint:** `POST https://api.groq.com/openai/v1/audio/transcriptions`

**Headers:**
```
Authorization: bearer ${GROQ_API_KEY}
```

**Body (multipart/form-data):**
```
file: @/tmp/voice.ogg
model: whisper-large-v3
language: id
response_format: json
```

**Response:**
```json
{
  "text": "transcribed text in Indonesian"
}
```

**Timeout:** None configured (relies on urllib defaults)

---

### DeepSeek Chat (Brand Summary)

**Endpoint:** `POST https://api.deepseek.com/chat/completions`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer ${DEEPSEEK_API_KEY}
```

**Body:**
```json
{
  "model": "deepseek-chat",
  "max_tokens": 350,
  "messages": [
    {
      "role": "system",
      "content": "Asisten ringkas. Fokus ke delta/perubahan terbaru saja. Bahasa Indonesia. No basa-basi."
    },
    {
      "role": "user",
      "content": "Diff:\n<git diff output>"
    }
  ]
}
```

**Response:**
```json
{
  "choices": [
    {
      "message": {
        "content": "summary text"
      }
    }
  ]
}
```

**Timeout:** None configured (relies on urllib defaults)

---

## Service Integration

### Voice Watcher Flow

1. **Polling:** Long-polling Telegram API (30s timeout, 40s urllib timeout)
2. **Filter:** Only process voice messages in monitored threads
3. **Download:** Fetch voice file via Telegram File API
4. **Transcribe:** Send to Groq Whisper
5. **Process:** Pass transcription to OpenClaw agent
6. **Respond:** Agent response sent back to Telegram thread

**Monitored Threads:**
- Inbox: Thread ID `11`
- Wellbeing: Thread ID `19`

**OpenClaw Integration:**
```bash
/home/openclaw/.npm-global/bin/openclaw \
  --mode dm \
  --user-message "<transcription>" \
  --telegram-thread-id <thread_id>
```

---

### Brand Summary Flow

1. **Git Hook:** Triggered on commits to tracked paths
2. **Diff Extraction:** `git diff <last_commit> HEAD -- <tracked_paths>`
3. **Summarization:** Send diff to DeepSeek
4. **Notification:** Post summary to Telegram Ops thread
5. **State Update:** Save current commit hash

**Notification Format:**
```
📝 Brand OS Update

<DeepSeek summary>

Commit: <short_hash>
```

---

## Health Checks & Monitoring

### Current State

❌ **No automated health checks**  
❌ **No uptime monitoring**  
❌ **No rate limit tracking**  
❌ **No cost monitoring**  
❌ **No fallback providers**

### Recommended Additions

1. **Provider Health Check Script**
   ```bash
   # ops/scripts/ai_provider_health.sh
   - Test Groq API connectivity
   - Test DeepSeek API connectivity
   - Check API key validity
   - Report to monitoring system
   ```

2. **Rate Limit Monitoring**
   - Track API calls per hour/day
   - Alert on approaching limits
   - Log response headers for rate limit info

3. **Cost Tracking**
   - Log token usage per request
   - Estimate monthly costs
   - Alert on budget thresholds

4. **Fallback Strategy**
   - Secondary transcription provider (OpenAI Whisper API)
   - Secondary summarization provider (Claude/GPT)
   - Graceful degradation messages

---

## Security Assessment

### ✅ Good Practices

1. **Environment Variables:** API keys not hardcoded
2. **File Permissions:** State files in user home directory
3. **No Key Logging:** Keys not logged in error messages

### ⚠️ Concerns

1. **No Key Rotation:** No evidence of periodic key rotation
2. **No Secrets Manager:** Keys stored in plain environment variables
3. **No Request Signing:** Relying solely on bearer tokens
4. **No Input Validation:** Voice files and git diffs not sanitized before API calls
5. **No Output Validation:** API responses not validated before use

### 🔴 Critical Issues

1. **Missing Startup Validation:** DeepSeek script doesn't validate API key at startup
2. **No Timeout Configuration:** urllib requests can hang indefinitely
3. **No Retry Logic:** Single-shot API calls with no retry on transient failures

---

## Cost Analysis

### Groq Whisper

**Pricing:** ~$0.111 per hour of audio (as of 2024)  
**Usage Pattern:** Ad-hoc voice messages  
**Estimated Monthly Volume:** Unknown (no logging)  
**Estimated Monthly Cost:** $5-20 (low volume assumption)

### DeepSeek

**Pricing:** ~$0.14 per 1M input tokens, ~$0.28 per 1M output tokens  
**Usage Pattern:** Git commits to Brand OS paths  
**Max Tokens per Request:** 350 output  
**Estimated Monthly Volume:** 50-100 commits  
**Estimated Monthly Cost:** <$1 (very low)

### Total Estimated Monthly Cost

**$6-21** (very low operational cost)

---

## Recommendations

### Priority 1 (Critical)

1. **Add Startup Validation for DeepSeek**
   ```python
   if not DEEPSEEK_KEY:
       raise RuntimeError("DEEPSEEK_API_KEY not set")
   ```

2. **Configure Timeouts**
   ```python
   urllib.request.urlopen(req, timeout=30)
   ```

3. **Add Retry Logic**
   ```python
   from tenacity import retry, stop_after_attempt, wait_exponential
   
   @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
   def api_call_with_retry():
       ...
   ```

### Priority 2 (High)

4. **Implement Health Checks**
   - Create `ops/scripts/ai_provider_health.py`
   - Run via cron every 5 minutes
   - Alert on failures

5. **Add Request/Response Logging**
   ```python
   LOGGER.info("API call: provider=%s model=%s tokens=%d", provider, model, token_count)
   ```

6. **Secrets Management**
   - Migrate to systemd credentials or HashiCorp Vault
   - Implement key rotation schedule (quarterly)

### Priority 3 (Medium)

7. **Fallback Providers**
   - Add OpenAI Whisper as fallback for Groq
   - Add Claude/GPT as fallback for DeepSeek

8. **Cost Monitoring**
   - Log token usage to database
   - Create monthly cost report
   - Set budget alerts

9. **Input Validation**
   - Validate voice file size/format before transcription
   - Sanitize git diffs before summarization

### Priority 4 (Low)

10. **MAIAROUTER Integration**
    - Document intended use case
    - Remove if not needed
    - Implement if planned

11. **API Response Caching**
    - Cache transcriptions for duplicate voice messages
    - Cache summaries for identical diffs

---

## Appendix A: File Locations

### Active Scripts

| File | Purpose | Provider |
|------|---------|----------|
| `/home/openclaw/banirisset/openclaw/scripts/voice_watcher.py` | Voice transcription | Groq |
| `/home/openclaw/banirisset/openclaw/scripts/brand_summary_notify.py` | Brand summary | DeepSeek |

### Configuration Files

| File | Purpose |
|------|---------|
| `/home/openclaw/banirisset/automation/telegram-config.json` | Telegram chat/thread IDs |
| `/home/openclaw/.openclaw/openclaw-gateway.env` | Gateway environment |
| `/home/openclaw/banirisset/ops/openclaw-providers.env.example` | Provider env template |

### State Files

| File | Purpose |
|------|---------|
| `/home/openclaw/.openclaw/workspace/.brand-summary-last-commit` | Last processed commit |

---

## Appendix B: Environment Template

```bash
# AI Provider API Keys
GROQ_API_KEY=sk-...                    # Required for voice transcription
DEEPSEEK_API_KEY=sk-...                # Required for brand summaries
MAIAROUTER_API_KEY=...                 # Optional, not currently used

# Telegram Bot Tokens
SCHEDULER_BOT_TOKEN=...                # Required for voice_watcher
TELEGRAM_BOT_TOKEN=...                 # Required for brand_summary_notify

# Optional Overrides
MODEL_ROUTER_PROVIDER=9router          # Default provider
MODEL_ROUTER_PROBE_TIMEOUT=15          # Probe timeout (seconds)
MODEL_ROUTER_CACHE_TTL=43200           # Cache TTL (seconds)
```

---

## Appendix C: Next Steps

1. ✅ **Audit Complete** - This report
2. ⏳ **Implement Priority 1 Fixes** - Startup validation, timeouts, retries
3. ⏳ **Set Up Health Checks** - Monitoring script + cron
4. ⏳ **Migrate to Secrets Manager** - Remove plain env vars
5. ⏳ **Document MAIAROUTER** - Clarify intended use or remove

---

**Report Generated:** 2026-05-15 09:39 UTC  
**Next Review:** 2026-08-15 (Quarterly)
