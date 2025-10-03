"""
Настройки для Pattern Transition Craftsman Agent.
"""

import os
from typing import Optional


def get_llm_model() -> str:
    """
    Получить модель LLM для агента.

    Returns:
        str: Название модели (по умолчанию openai:gpt-4o)
    """
    return os.getenv("PYDANTIC_AI_MODEL", "openai:gpt-4o")


def get_api_key() -> Optional[str]:
    """
    Получить API ключ из переменных окружения.

    Returns:
        Optional[str]: API ключ или None
    """
    return os.getenv("OPENAI_API_KEY")


__all__ = ["get_llm_model", "get_api_key"]
