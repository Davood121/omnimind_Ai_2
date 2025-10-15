import os
import json
import requests
from typing import Dict, Any, Optional


class OllamaInterface:
    """
    Thin client for interacting with a local Ollama server via its HTTP API.
    Default model is phi3:medium as the primary reasoning engine.
    """

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "phi3:medium"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def set_model(self, model: str):
        """Allow hot-swapping the model, e.g., to codellama:7b-instruct."""
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2, 
                 max_tokens: Optional[int] = None) -> str:
        """
        Calls Ollama's /api/generate with a simple prompt. Assumes Ollama is running locally.
        """
        url = f"{self.base_url}/api/generate"
        prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{user_prompt}\n<|assistant|>"
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "options": {
                "temperature": temperature,
            },
            "stream": False,
        }
        if max_tokens is not None:
            payload["options"]["num_predict"] = max_tokens

        try:
            resp = requests.post(url, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            # Ollama returns { "response": "...", ... }
            return data.get("response", "")
        except requests.RequestException as e:
            return f"[Error] Failed to reach local Ollama server at {url}: {e}"
