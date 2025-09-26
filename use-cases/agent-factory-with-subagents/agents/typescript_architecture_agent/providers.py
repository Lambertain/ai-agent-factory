"""LLM providers configuration for TypeScript Architecture Agent."""

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.gemini import GeminiProvider
from .settings import load_settings


def get_llm_model():
    """
    Получение оптимальной модели для TypeScript архитектурных задач.

    Использует cost-optimized конфигурацию:
    - Qwen 2.5 Coder 32B для сложных архитектурных задач
    - Gemini 2.5 Flash для планирования и документации
    """
    settings = load_settings()

    # Для архитектурных задач используем специализированную модель кодирования
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    # Используем Qwen Coder для TypeScript архитектуры
    return OpenAIModel(
        settings.llm_architecture_model,  # qwen2.5-72b-instruct для сложных задач
        provider=provider
    )


def get_planning_model():
    """
    Модель для планирования и документации (более дешевая).
    """
    settings = load_settings()

    # Используем Gemini для текстовых задач
    provider = GeminiProvider(api_key=settings.gemini_api_key)

    return GeminiModel(
        settings.llm_planning_model,  # gemini-2.5-flash-lite
        provider=provider
    )


def get_coding_model():
    """
    Специализированная модель для генерации и рефакторинга кода.
    """
    settings = load_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(
        settings.llm_coding_model,  # qwen2.5-coder-32b-instruct
        provider=provider
    )


def get_validation_model():
    """
    Модель для валидации и проверки качества (экономичная).
    """
    settings = load_settings()

    provider = GeminiProvider(api_key=settings.gemini_api_key)

    return GeminiModel(
        settings.llm_validation_model,  # gemini-2.5-flash-lite
        provider=provider
    )


# Конфигурация моделей для разных типов задач
MODEL_ROUTING = {
    "architecture_analysis": get_llm_model,
    "code_refactoring": get_coding_model,
    "documentation": get_planning_model,
    "validation": get_validation_model,
    "planning": get_planning_model
}


def get_model_for_task(task_type: str):
    """
    Получение оптимальной модели для конкретного типа задачи.

    Args:
        task_type: Тип задачи (architecture_analysis, code_refactoring, etc.)

    Returns:
        Настроенная модель для задачи
    """
    model_getter = MODEL_ROUTING.get(task_type, get_llm_model)
    return model_getter()


# Настройки для оптимизации затрат
COST_OPTIMIZATION_CONFIG = {
    "enable_caching": True,
    "batch_requests": True,
    "prefer_cheaper_models": True,
    "context_compression": True
}