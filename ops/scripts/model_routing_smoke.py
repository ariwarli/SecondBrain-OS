#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import sys

import requests

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from ops.reed_runtime.env import load_runtime_env


def _parse_json_best_effort(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Some gateways may append extra bytes/chunks after a valid JSON object.
        decoder = json.JSONDecoder()
        obj, _ = decoder.raw_decode(text)
        return obj if isinstance(obj, dict) else {"raw_response": text[:500]}


def _parse_sse_payload(text: str) -> dict:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("data:"):
            continue
        chunk = stripped[len("data:") :].strip()
        if not chunk or chunk == "[DONE]":
            continue
        try:
            parsed = _parse_json_best_effort(chunk)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            continue
    return {"raw_response": text[:500]}


def main() -> int:
    load_runtime_env()
    base_url = os.environ.get("NINE_ROUTER_BASE_URL", "http://100.113.246.119:20128/v1").rstrip("/")
    api_key = os.environ.get("NINE_ROUTER_API_KEY", "")
    model = os.environ.get("NINE_ROUTER_SMOKE_MODEL", "reed")

    if not api_key:
        print(json.dumps({"ok": False, "error": "missing NINE_ROUTER_API_KEY"}, indent=2))
        return 1

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Reply with OK only."}],
        "max_tokens": 5,
        "temperature": 0,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        resp = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=20)
        try:
            body = resp.json()
        except ValueError:
            try:
                body = _parse_sse_payload(resp.text)
                if "choices" not in body:
                    body = _parse_json_best_effort(resp.text)
            except Exception:
                body = {"raw_response": resp.text[:500]}
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2, ensure_ascii=False))
        return 1

    choices = body.get("choices") if isinstance(body, dict) else None
    ok = resp.status_code == 200 and bool(choices)
    output = {
        "ok": ok,
        "status_code": resp.status_code,
        "model": model,
        "base_url": base_url,
        "response_preview": (
            body.get("choices", [{}])[0].get("message", {}).get("content", "")[:120]
            if isinstance(body, dict) and body.get("choices")
            else str(body)[:120]
        ),
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
