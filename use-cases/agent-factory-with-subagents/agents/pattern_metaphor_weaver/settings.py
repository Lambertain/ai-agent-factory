"""
Настройки для Pattern Metaphor Weaver Agent.
"""

import os
from typing import Optional


def get_llm_model() -> str:
    return os.getenv("PYDANTIC_AI_MODEL", "openai:gpt-4o")


def get_api_key() -> Optional[str]:
    return os.getenv("OPENAI_API_KEY")


__all__ = ["get_llm_model", "get_api_key"]
