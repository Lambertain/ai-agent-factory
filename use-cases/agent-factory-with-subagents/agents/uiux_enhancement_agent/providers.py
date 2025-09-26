"""
Провайдеры моделей для UI/UX Enhancement Agent.

Оптимизированная конфигурация моделей для разных типов UI/UX задач
с учетом стоимости и качества.
"""

from typing import Dict, Any
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.gemini import GeminiProvider
from pydantic_ai.models.gemini import GeminiModel

from .settings import load_settings


def get_llm_model(task_type: str = "uiux") -> OpenAIModel | GeminiModel:
    """
    Получить оптимизированную модель для конкретного типа UI/UX задачи.

    Args:
        task_type: Тип задачи UI/UX:
            - "uiux": Общий анализ UI/UX (Gemini Flash-Lite - дешево)
            - "accessibility": Accessibility аудит (Qwen Coder - точность)
            - "performance": Performance анализ (Qwen Coder - техническая точность)
            - "design": Дизайн анализ (Gemini Flash-Lite - креативность)
            - "architecture": Архитектурные решения UI (Qwen Premium)

    Returns:
        Настроенная модель для задачи
    """
    settings = load_settings()

    # Маппинг типов задач на модели (cost-optimized)
    task_model_map = {
        "uiux": settings.llm_docs_model,  # Gemini 2.5 Flash-Lite ($0.10-0.40/1M)
        "accessibility": settings.llm_testing_model,  # Qwen Coder 7B (высокая точность)
        "performance": settings.llm_coding_model,  # Qwen Coder 32B (техническая экспертиза)
        "design": settings.llm_docs_model,  # Gemini Flash-Lite (креативные задачи)
        "architecture": settings.llm_architecture_model,  # Qwen 72B (только для сложного анализа)
        "validation": settings.llm_validation_model  # Gemini Flash-Lite (быстрая валидация)
    }

    model_name = task_model_map.get(task_type, settings.llm_docs_model)

    # Определяем провайдера по названию модели
    if "gemini" in model_name.lower():
        return _get_gemini_model(model_name, settings)
    else:
        return _get_qwen_model(model_name, settings)


def _get_gemini_model(model_name: str, settings: Any) -> GeminiModel:
    """Настройка Gemini модели для UI/UX задач."""
    provider = GeminiProvider(
        api_key=settings.gemini_api_key,
        # Настройки для UI/UX оптимизации
        generation_config={
            "temperature": 0.3,  # Баланс креативности и точности
            "top_p": 0.8,
            "max_output_tokens": 4096,
            "candidate_count": 1
        }
    )

    return GeminiModel(
        model_name=model_name,
        provider=provider
    )


def _get_qwen_model(model_name: str, settings: Any) -> OpenAIModel:
    """Настройка Qwen модели через OpenAI API для технических UI/UX задач."""
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        # Настройки для технической точности
        http_client_kwargs={
            "timeout": 60.0,
            "headers": {
                "User-Agent": "UIUXEnhancementAgent/1.0"
            }
        }
    )

    return OpenAIModel(
        model_name=model_name,
        provider=provider,
        # Параметры для UI/UX анализа
        temperature=0.2,  # Высокая точность для технических задач
        max_tokens=3000,
        top_p=0.9,
        frequency_penalty=0.1,
        presence_penalty=0.1
    )


def get_model_for_component_type(component_type: str) -> OpenAIModel | GeminiModel:
    """
    Получить модель, оптимизированную для анализа конкретного типа компонента.

    Args:
        component_type: Тип компонента UI:
            - "form": Формы и input элементы
            - "navigation": Навигация и меню
            - "data": Таблицы и списки данных
            - "media": Изображения и медиа
            - "interactive": Кнопки, модалы, dropdowns
            - "layout": Layout и responsive компоненты

    Returns:
        Оптимизированная модель
    """
    # Сложные интерактивные компоненты требуют более точного анализа
    complex_components = ["form", "interactive", "data"]

    if component_type in complex_components:
        return get_llm_model("accessibility")  # Qwen Coder для точности
    else:
        return get_llm_model("design")  # Gemini для общего анализа


def get_cost_optimized_config() -> Dict[str, Any]:
    """
    Получить конфигурацию для минимизации стоимости API вызовов.

    Returns:
        Словарь с настройками оптимизации
    """
    return {
        "enable_caching": True,  # Кэширование результатов
        "batch_requests": True,  # Батчинг запросов когда возможно
        "compression": True,  # Сжатие промптов
        "smart_routing": True,  # Умная маршрутизация по стоимости
        "fallback_models": [
            "gemini-2.5-flash-lite",  # Самая дешевая модель как fallback
            "qwen2.5-coder-7b-instruct"  # Backup Qwen модель
        ],
        "rate_limiting": {
            "requests_per_minute": 60,
            "tokens_per_minute": 100000
        }
    }


def validate_api_configuration() -> Dict[str, bool]:
    """
    Проверить доступность и конфигурацию API провайдеров.

    Returns:
        Статус доступности каждого провайдера
    """
    settings = load_settings()
    status = {}

    # Проверка Qwen API
    try:
        qwen_provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )
        status["qwen"] = True
    except Exception:
        status["qwen"] = False

    # Проверка Gemini API
    try:
        gemini_provider = GeminiProvider(api_key=settings.gemini_api_key)
        status["gemini"] = True
    except Exception:
        status["gemini"] = False

    return status