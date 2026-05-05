#!/usr/bin/env python3
"""REED Model Router - Centralized model selection per use case."""

import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

try:
    import requests
except ImportError:
    os.system("pip3 install requests -q")
    import requests


@dataclass
class ModelConfig:
    provider: str
    model_id: str
    max_tokens: int
    temperature: float


DEFAULT_CONFIG_PATH = Path("/home/openclaw/.openclaw/openclaw.json")
WORKSPACE = Path("/home/openclaw/banirisset")
RESOLUTION_CACHE_PATH = WORKSPACE / "state" / "model-router-cache.json"
ALIASES_PATH = WORKSPACE / "state" / "model-router-aliases.json"
PROBE_TIMEOUT = int(os.environ.get("MODEL_ROUTER_PROBE_TIMEOUT", "15"))
CACHE_TTL_SECONDS = int(os.environ.get("MODEL_ROUTER_CACHE_TTL", "43200"))
PROBE_ENABLED = os.environ.get("MODEL_ROUTER_PROBE", "1").lower() not in {"0", "false", "no"}
USE_RESOLUTION_CACHE = os.environ.get("MODEL_ROUTER_USE_CACHE", "0").lower() in {"1", "true", "yes"}
MANDATORY_PROVIDER = os.environ.get("MODEL_ROUTER_PROVIDER", "9router")


def load_openclaw_config(path: Optional[Path] = None) -> Dict:
    config_path = path or DEFAULT_CONFIG_PATH
    if not config_path.exists():
        raise FileNotFoundError(f"OpenClaw config not found: {config_path}")
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def load_model_aliases(path: Optional[Path] = None, config_path: Optional[Path] = None) -> Dict[str, Dict]:
    aliases_path = path or ALIASES_PATH
    if aliases_path.exists():
        try:
            data = json.loads(aliases_path.read_text(encoding="utf-8"))
            aliases = data.get("modelAliases", data)
            if isinstance(aliases, dict):
                return aliases
        except Exception:
            pass

    config = load_openclaw_config(config_path)
    aliases = config.get("models", {}).get("modelAliases", {})
    return aliases if isinstance(aliases, dict) else {}


def _load_resolution_cache() -> Dict[str, Dict]:
    if not RESOLUTION_CACHE_PATH.exists():
        return {}
    try:
        data = json.loads(RESOLUTION_CACHE_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_resolution_cache(cache: Dict[str, Dict]) -> None:
    RESOLUTION_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESOLUTION_CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _cache_key(use_case: str, alias: Dict, provider: Dict) -> str:
    payload = json.dumps({"use_case": use_case, "alias": alias, "provider": provider}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def _split_model(full_id: str) -> Tuple[str, str]:
    provider, model = full_id.split("/", 1)
    return provider, model


def _ordered_candidates(alias: Dict) -> List[str]:
    ordered: List[str] = []
    for key in ("requestedPrimary", "primary", "requestedFallback", "fallback"):
        value = alias.get(key)
        if isinstance(value, str) and value and value not in ordered:
            ordered.append(value)
    for key in ("primaryCandidates", "fallbackCandidates"):
        extra = alias.get(key)
        if isinstance(extra, list):
            for item in extra:
                if isinstance(item, str) and item and item not in ordered:
                    ordered.append(item)
    return ordered


def _probe_model(provider_name: str, model_id: str, provider_cfg: Dict) -> bool:
    base_url = str(provider_cfg.get("baseUrl", "")).rstrip("/")
    api_key = (
        provider_cfg.get("apiKey")
        or os.environ.get(f"{provider_name.upper().replace('-', '_')}_API_KEY")
        or os.environ.get("NINE_ROUTER_API_KEY")
        or os.environ.get("OLLAMA_CLOUD_API_KEY")
        or ""
    )
    if not base_url or not api_key:
        return False

    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": "Reply with OK only."}],
        "max_tokens": 1,
        "temperature": 0,
    }
    try:
        resp = requests.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=PROBE_TIMEOUT,
        )
        if resp.status_code != 200:
            return False
        data = resp.json()
        return bool(data.get("choices"))
    except Exception:
        return False


def _resolve_available_models(
    candidates: Iterable[str],
    provider_cfg: Dict,
    cache: Dict[str, Dict],
    cache_key: str,
) -> List[str]:
    now = time.time()
    cached = cache.get(cache_key)
    if USE_RESOLUTION_CACHE and cached:
        cached_model = cached.get("resolved")
        cached_at = cached.get("resolved_at", 0)
        if isinstance(cached_model, list) and (now - float(cached_at)) <= CACHE_TTL_SECONDS:
            return [m for m in cached_model if isinstance(m, str) and m]

    resolved: List[str] = []
    for full_id in candidates:
        provider_name, model_id = _split_model(full_id)
        if _probe_model(provider_name, model_id, provider_cfg) and full_id not in resolved:
            resolved.append(full_id)
            if len(resolved) >= 2:
                break

    if resolved:
        cache[cache_key] = {"resolved": resolved, "resolved_at": now}
    return resolved


def get_model_for_use_case(
    use_case: str,
    config_path: Optional[Path] = None
) -> Tuple[ModelConfig, Optional[ModelConfig]]:
    """
    Get model config for a use case with fallback.

    Args:
        use_case: One of 'classifier', 'wiki_ingest', 'reed_dm', 'wellbeing'

    Returns:
        Tuple of (primary_config, fallback_config or None)
    """
    config = load_openclaw_config(config_path)
    aliases = load_model_aliases(config_path=config_path)

    if use_case not in aliases:
        raise ValueError(f"Unknown use_case: {use_case}. Available: {list(aliases.keys())}")

    alias = aliases[use_case]
    provider_cfg = config.get("models", {}).get("providers", {}).get(MANDATORY_PROVIDER, {})
    if not isinstance(provider_cfg, dict):
        provider_cfg = {}

    def parse_model(full_id: str) -> ModelConfig:
        provider, model = full_id.split("/", 1)
        return ModelConfig(
            provider=provider,
            model_id=model,
            max_tokens=alias.get("maxTokens", 2048),
            temperature=alias.get("temperature", 0.7),
        )

    ordered_candidates = [item for item in _ordered_candidates(alias) if item.split("/", 1)[0] == MANDATORY_PROVIDER]

    cache = _load_resolution_cache()
    cache_key = _cache_key(use_case, alias, provider_cfg)

    if PROBE_ENABLED:
        resolved_models = _resolve_available_models(ordered_candidates, provider_cfg, cache, cache_key)
    else:
        resolved_models = ordered_candidates[:2]

    if not resolved_models and ordered_candidates:
        resolved_models = ordered_candidates[:2]

    if cache:
        _save_resolution_cache(cache)

    primary = parse_model(resolved_models[0]) if resolved_models else parse_model(alias["primary"])
    fallback = (
        parse_model(resolved_models[1])
        if len(resolved_models) > 1
        else (parse_model(alias["fallback"]) if alias.get("fallback") else None)
    )

    return primary, fallback


def get_classifier_model() -> Tuple[ModelConfig, Optional[ModelConfig]]:
    """Get model config for inbox classification."""
    return get_model_for_use_case("classifier")


def get_wiki_model() -> Tuple[ModelConfig, Optional[ModelConfig]]:
    """Get model config for wiki ingestion."""
    return get_model_for_use_case("wiki_ingest")


def get_dm_model() -> Tuple[ModelConfig, Optional[ModelConfig]]:
    """Get model config for REED DM."""
    return get_model_for_use_case("reed_dm")


def get_wellbeing_model() -> Tuple[ModelConfig, Optional[ModelConfig]]:
    """Get model config for wellbeing lane."""
    return get_model_for_use_case("wellbeing")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: model_router.py <use_case>")
        print("Available: classifier, wiki_ingest, reed_dm, wellbeing")
        sys.exit(1)

    use_case = sys.argv[1]
    try:
        primary, fallback = get_model_for_use_case(use_case)
        print(f"Primary: {primary.provider}/{primary.model_id}")
        print(f"  max_tokens={primary.max_tokens}, temperature={primary.temperature}")
        if fallback:
            print(f"Fallback: {fallback.provider}/{fallback.model_id}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
