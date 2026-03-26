from __future__ import annotations
import os
from typing import Dict, Any

try:
    import openai
except ImportError:
    openai = None

class LLMClient:
    """LLM abstraction layer for OpenAI and other backends."""

    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

        if openai is not None and self.api_key:
            openai.api_key = self.api_key

    def call(self, prompt: str, **kwargs) -> Dict[str, Any]:
        if openai is None:
            raise RuntimeError("openai package is not installed")

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": kwargs.get("user_message", "")},
        ]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 500),
        )

        return {
            "text": response.choices[0].message.content,
            "raw": response,
        }

    def echo(self, prompt: str) -> Dict[str, Any]:
        """Fallback for local or testing environments."""
        return {
            "text": f"[LLM mock] {prompt}",
            "raw": None,
        }
