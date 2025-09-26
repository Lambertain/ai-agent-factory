"""Cost-optimized модели для Prisma Database Agent."""

from typing import Union
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.gemini import GeminiProvider

from .settings import load_settings


def get_qwen_provider():
    """Получить Qwen провайдер через OpenAI-совместимый API."""
    settings = load_settings()
    return OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )


def get_gemini_provider():
    """Получить Gemini провайдер."""
    settings = load_settings()
    return GeminiProvider(api_key=settings.gemini_api_key)


def get_prisma_model_by_task(task_type: str) -> Union[OpenAIModel, GeminiModel]:
    """
    Выбрать оптимальную модель для конкретного типа задачи.

    Args:
        task_type: Тип задачи - "architecture", "coding", "planning", "validation", "docs"

    Returns:
        Настроенная модель для задачи
    """
    settings = load_settings()

    # Архитектурный анализ и сложные задачи оптимизации - Premium Qwen
    if task_type == "architecture":
        provider = get_qwen_provider()
        return OpenAIModel(settings.llm_architecture_model, provider=provider)

    # Генерация SQL, миграций, создание схем - Qwen Coder
    elif task_type == "coding":
        provider = get_qwen_provider()
        return OpenAIModel(settings.llm_coding_model, provider=provider)

    # Планирование миграций, документация - дешевый Gemini
    elif task_type in ["planning", "docs", "validation"]:
        provider = get_gemini_provider()
        return GeminiModel(settings.llm_planning_model, provider=provider)

    # По умолчанию - балансированная модель
    else:
        provider = get_qwen_provider()
        return OpenAIModel(settings.llm_coding_model, provider=provider)


def get_model_for_analysis_mode(analysis_mode: str) -> Union[OpenAIModel, GeminiModel]:
    """
    Выбрать модель в зависимости от режима анализа Prisma.

    Args:
        analysis_mode: Режим анализа - "full", "schema", "queries", "migrations", "performance"
    """

    # Полный анализ и производительность - самая мощная модель
    if analysis_mode in ["full", "performance"]:
        return get_prisma_model_by_task("architecture")

    # Анализ схем - архитектурная модель
    elif analysis_mode == "schema":
        return get_prisma_model_by_task("architecture")

    # Оптимизация запросов - coding модель
    elif analysis_mode == "queries":
        return get_prisma_model_by_task("coding")

    # Миграции - планирование и генерация
    elif analysis_mode == "migrations":
        return get_prisma_model_by_task("coding")

    # По умолчанию
    else:
        return get_prisma_model_by_task("planning")


# Стоимость моделей (примерная, за 1M токенов)
MODEL_COSTS = {
    "qwen2.5-72b-instruct": {"input": 2.0, "output": 3.0},      # Premium
    "qwen2.5-coder-32b-instruct": {"input": 1.0, "output": 2.0}, # Balanced
    "qwen2.5-coder-7b-instruct": {"input": 0.5, "output": 1.0},  # Budget
    "gemini-2.5-flash-lite": {"input": 0.1, "output": 0.4},      # Ultra-cheap
}


def estimate_task_cost(task_type: str, estimated_tokens: int = 5000) -> float:
    """
    Оценить стоимость выполнения задачи.

    Args:
        task_type: Тип задачи
        estimated_tokens: Примерное количество токенов

    Returns:
        Стоимость в долларах
    """
    model = get_prisma_model_by_task(task_type)
    model_name = model.name

    if model_name in MODEL_COSTS:
        cost_per_1m = MODEL_COSTS[model_name]["input"] + MODEL_COSTS[model_name]["output"]
        return (estimated_tokens / 1_000_000) * cost_per_1m
    else:
        return 0.01  # Примерная стоимость


def get_budget_model() -> GeminiModel:
    """Получить самую дешевую модель для простых задач."""
    return get_prisma_model_by_task("planning")


def get_premium_model() -> OpenAIModel:
    """Получить самую мощную модель для сложных задач."""
    return get_prisma_model_by_task("architecture")


# Экспорт
__all__ = [
    "get_prisma_model_by_task",
    "get_model_for_analysis_mode",
    "get_qwen_provider",
    "get_gemini_provider",
    "estimate_task_cost",
    "get_budget_model",
    "get_premium_model",
    "MODEL_COSTS"
]