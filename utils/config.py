import json
import os
from typing import Any, Dict

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

_cached: Dict[str, Any] = {}


def load_config() -> Dict[str, Any]:
    global _cached
    if _cached:
        return _cached
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            _cached = json.load(f)
    except Exception:
        _cached = {}
    return _cached


def get(key: str, default: Any = None) -> Any:
    cfg = load_config()
    return cfg.get(key, default)


def searxng_url() -> str:
    # env var wins, then config.json, else empty
    return os.environ.get('SEARXNG_URL') or str(get('searxng_url', '')).strip()


def yacy_url() -> str:
    return os.environ.get('YACY_URL') or str(get('yacy_url', '')).strip()
