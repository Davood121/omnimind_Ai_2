import traceback
from typing import Dict, Any

from .safety_guard import SAFE_BASE_DIR


COMMON_HINTS = {
    'ollama': "Ensure Ollama is running and the model is pulled. Run: 'ollama pull phi3:medium' then 'ollama run phi3:medium'.",
    'searxng': "Set SEARXNG_URL to your SearXNG instance, e.g., setx SEARXNG_URL \"https://searxng.example.org\".",
    'yacy': "Start YaCy locally (http://localhost:8090) and set YACY_URL accordingly, e.g., setx YACY_URL \"http://localhost:8090\".",
    'transformers': "Install transformers/torch or run CPU-only: pip install transformers && pip install torch --index-url https://download.pytorch.org/whl/cpu",
    'mic': "Check microphone permissions/settings in the OS. For web, use the browser mic permission.",
}


def ai_mini_error_doctor(context: str, err: Exception) -> Dict[str, Any]:
    """
    Lightweight heuristic error analyzer that categorizes the error, suggests fixes,
    and indicates if an automatic fallback was used.
    """
    etype = type(err).__name__
    trace = ''.join(traceback.format_exception(type(err), err, err.__traceback__))
    lower = (str(err) + ' ' + trace).lower()

    category = 'generic'
    advice = 'Try again. If the issue persists, check logs.'
    auto_action = 'none'

    if 'connection refused' in lower or 'failed to establish a new connection' in lower or '11434' in lower:
        category = 'ollama'
        advice = COMMON_HINTS['ollama']
        auto_action = 'fallback-without-llm'
    elif 'searx' in lower:
        category = 'searxng'
        advice = COMMON_HINTS['searxng']
        auto_action = 'fallback-partial-search'
    elif 'yacy' in lower:
        category = 'yacy'
        advice = COMMON_HINTS['yacy']
        auto_action = 'fallback-partial-search'
    elif 'transformers' in lower or 'torch' in lower:
        category = 'transformers'
        advice = COMMON_HINTS['transformers']
        auto_action = 'disable-emotion-temporarily'

    return {
        'category': category,
        'error_type': etype,
        'message': str(err),
        'advice': advice,
        'auto_action_taken': auto_action,
        'context': context,
    }
