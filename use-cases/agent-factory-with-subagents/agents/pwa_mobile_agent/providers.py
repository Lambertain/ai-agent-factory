"""
Провайдеры моделей для PWA Mobile Agent.

Настраивает LLM модели для разработки PWA приложений.
"""

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from .settings import load_settings


def get_llm_model():
    """Сконфигурировать модель LLM для PWA разработки."""
    settings = load_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(settings.llm_model, provider=provider)


def get_coding_model():
    """Получить модель оптимизированную для генерации кода."""
    settings = load_settings()

    # Используем специализированную модель для кода если доступна
    coding_model = getattr(settings, 'llm_coding_model', settings.llm_model)

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(coding_model, provider=provider)


def get_analysis_model():
    """Получить модель для анализа производительности."""
    settings = load_settings()

    # Используем более мощную модель для анализа если доступна
    analysis_model = getattr(settings, 'llm_architecture_model', settings.llm_model)

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(analysis_model, provider=provider)