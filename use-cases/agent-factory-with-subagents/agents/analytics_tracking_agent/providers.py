# -*- coding: utf-8 -*-
"""
Провайдеры LLM для Analytics & Tracking Agent
Конфигурация моделей с поддержкой универсальных настроек
"""

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from .settings import load_analytics_settings

def get_llm_model():
    """Получить сконфигурированную модель LLM для analytics задач."""
    settings = load_analytics_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(
        settings.llm_model,
        provider=provider
    )

def get_analytics_model():
    """Получить оптимизированную модель для analytics задач."""
    settings = load_analytics_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    # Используем модель для планирования/документации (дешевле)
    model_name = getattr(settings, 'llm_planning_model', settings.llm_model)

    return OpenAIModel(
        model_name,
        provider=provider
    )

def get_coding_model():
    """Получить модель для кодирования analytics интеграций."""
    settings = load_analytics_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    # Используем модель для кодирования
    model_name = getattr(settings, 'llm_coding_model', settings.llm_model)

    return OpenAIModel(
        model_name,
        provider=provider
    )