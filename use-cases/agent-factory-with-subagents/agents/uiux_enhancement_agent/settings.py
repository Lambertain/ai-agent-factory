"""
Настройки UI/UX Enhancement Agent.

Конфигурация для работы с различными провайдерами моделей,
инструментами анализа UI/UX и интеграциями.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import List, Dict, Any


class UIUXAgentSettings(BaseSettings):
    """
    Настройки UI/UX Enhancement Agent с поддержкой переменных окружения.

    Оптимизированная конфигурация для cost-effective использования
    различных моделей LLM в зависимости от типа UI/UX задачи.
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="UIUX_"  # Префикс для переменных окружения
    )

    # ===== LLM CONFIGURATION =====

    # Основные параметры LLM
    llm_provider: str = Field(default="openai", description="Основной провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ основного провайдера")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # ===== COST-OPTIMIZED MODEL ROUTING =====

    # UI/UX анализ и дизайн - Gemini Flash-Lite (ultra-cheap: $0.10-0.40/1M)
    llm_docs_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для UI/UX анализа и документации"
    )
    llm_validation_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для валидации дизайна"
    )

    # Технический анализ accessibility и performance - Qwen Coder
    llm_testing_model: str = Field(
        default="qwen2.5-coder-7b-instruct",
        description="Модель для accessibility тестирования"
    )
    llm_coding_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для анализа кода компонентов"
    )

    # Сложный архитектурный анализ - Premium Qwen (только когда необходимо)
    llm_architecture_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для сложного архитектурного анализа UI"
    )

    # Gemini API конфигурация
    gemini_api_key: str = Field(..., description="Google Gemini API ключ")
    gemini_use_batch_api: bool = Field(
        default=True,
        description="Использовать Batch API для 50% скидки"
    )

    # ===== UI/UX SPECIFIC SETTINGS =====

    # Дизайн система
    design_system: str = Field(default="shadcn/ui", description="Используемая дизайн система")
    css_framework: str = Field(default="tailwind", description="CSS фреймворк")
    component_library_version: str = Field(default="latest", description="Версия библиотеки компонентов")

    # Accessibility настройки
    wcag_compliance_level: str = Field(default="AA", description="Уровень соответствия WCAG")
    accessibility_tools: List[str] = Field(
        default_factory=lambda: ["axe-core", "lighthouse", "wave"],
        description="Инструменты для accessibility аудита"
    )

    # Performance настройки
    performance_budget: Dict[str, Any] = Field(
        default_factory=lambda: {
            "first_contentful_paint": 1500,  # ms
            "cumulative_layout_shift": 0.1,
            "total_blocking_time": 300,
            "bundle_size_limit": 100  # KB
        },
        description="Performance бюджет для UI компонентов"
    )

    # Responsive breakpoints (Tailwind CSS стандартные + кастомные)
    responsive_breakpoints: Dict[str, str] = Field(
        default_factory=lambda: {
            "xs": "475px",
            "sm": "640px",
            "md": "768px",
            "lg": "1024px",
            "xl": "1280px",
            "2xl": "1536px",
            "3xl": "1920px"
        },
        description="Responsive breakpoints"
    )

    # ===== TOOL INTEGRATIONS =====

    # Puppeteer для visual testing
    puppeteer_enabled: bool = Field(default=True, description="Включить Puppeteer для visual testing")
    puppeteer_headless: bool = Field(default=True, description="Запускать Puppeteer в headless режиме")

    # Figma интеграция (опционально)
    figma_api_key: str = Field(default="", description="Figma API ключ для синхронизации дизайна")
    figma_integration_enabled: bool = Field(default=False, description="Включить интеграцию с Figma")

    # Storybook для документации компонентов
    storybook_integration: bool = Field(default=True, description="Интеграция со Storybook")
    storybook_base_url: str = Field(default="http://localhost:6006", description="URL Storybook сервера")

    # ===== ARCHON RAG INTEGRATION =====

    # Archon Knowledge Base
    archon_api_url: str = Field(default="http://localhost:3737", description="URL Archon API")
    archon_project_id: str = Field(
        default="",
        description="ID проекта в Archon (настраивается под конкретный проект)"
    )

    # Knowledge tags for RAG search
    default_knowledge_tags: List[str] = Field(
        default_factory=lambda: [
            "uiux-enhancement",
            "design-systems",
            "accessibility",
            "agent-knowledge",
            "pydantic-ai"
        ],
        description="Теги по умолчанию для поиска в базе знаний"
    )

    # ===== COST OPTIMIZATION =====

    # Умная маршрутизация запросов
    enable_smart_routing: bool = Field(default=True, description="Умная маршрутизация по стоимости")
    auto_compress_prompts: bool = Field(default=True, description="Автоматическое сжатие промптов")
    cache_responses: bool = Field(default=True, description="Кэширование ответов")

    # Rate limiting
    rate_limit_requests_per_minute: int = Field(default=60, description="Лимит запросов в минуту")
    rate_limit_tokens_per_minute: int = Field(default=100000, description="Лимит токенов в минуту")

    # Batch processing
    enable_batch_processing: bool = Field(default=True, description="Батчинг запросов")
    batch_size: int = Field(default=5, description="Размер батча")

    # ===== PROJECT SPECIFIC =====

    # Настройки под конкретный проект (заполняются динамически)
    project_name: str = Field(default="", description="Название проекта")
    project_color_palette: Dict[str, str] = Field(
        default_factory=dict,
        description="Цветовая палитра проекта (настраивается под каждый проект)"
    )
    project_design_system: str = Field(
        default="custom",
        description="Дизайн система проекта (custom, shadcn/ui, chakra-ui, mantine, etc.)"
    )

    # Animation preferences
    animation_config: Dict[str, Any] = Field(
        default_factory=lambda: {
            "duration_fast": "150ms",
            "duration_normal": "300ms",
            "duration_slow": "500ms",
            "easing": "cubic-bezier(0.4, 0, 0.2, 1)",
            "respect_reduced_motion": True
        },
        description="Настройки анимаций"
    )


def load_settings() -> UIUXAgentSettings:
    """
    Загрузить настройки UI/UX агента с проверкой переменных окружения.

    Returns:
        Конфигурация агента

    Raises:
        ValueError: Если обязательные переменные не установлены
    """
    load_dotenv()

    try:
        settings = UIUXAgentSettings()

        # Проверяем обязательные API ключи
        if not settings.llm_api_key:
            raise ValueError("LLM_API_KEY не установлен в переменных окружения")

        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY не установлен в переменных окружения")

        return settings

    except Exception as e:
        error_msg = f"Не удалось загрузить настройки UI/UX агента: {e}"
        raise ValueError(error_msg) from e


def get_model_cost_estimate(model_name: str, input_tokens: int, output_tokens: int) -> float:
    """
    Оценить стоимость запроса к модели.

    Args:
        model_name: Название модели
        input_tokens: Количество входных токенов
        output_tokens: Количество выходных токенов

    Returns:
        Оценочная стоимость в USD
    """
    # Стоимость за 1M токенов (приблизительно)
    cost_per_million = {
        "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40},
        "qwen2.5-coder-7b-instruct": {"input": 0.50, "output": 1.50},
        "qwen2.5-coder-32b-instruct": {"input": 1.20, "output": 2.40},
        "qwen2.5-72b-instruct": {"input": 2.40, "output": 4.80}
    }

    if model_name not in cost_per_million:
        return 0.0  # Неизвестная модель

    costs = cost_per_million[model_name]
    input_cost = (input_tokens / 1_000_000) * costs["input"]
    output_cost = (output_tokens / 1_000_000) * costs["output"]

    return input_cost + output_cost


def validate_environment() -> Dict[str, bool]:
    """
    Проверить корректность настройки окружения.

    Returns:
        Словарь с результатами проверок
    """
    checks = {}

    try:
        settings = load_settings()

        # Проверка API ключей
        checks["llm_api_key"] = bool(settings.llm_api_key)
        checks["gemini_api_key"] = bool(settings.gemini_api_key)

        # Проверка Archon подключения
        checks["archon_configured"] = bool(settings.archon_api_url and settings.archon_project_id)

        # Проверка дизайн системы
        checks["design_system"] = settings.design_system in ["shadcn/ui", "chakra-ui", "mantine"]
        checks["css_framework"] = settings.css_framework in ["tailwind", "emotion", "styled-components"]

        # Проверка accessibility настроек
        checks["wcag_level"] = settings.wcag_compliance_level in ["A", "AA", "AAA"]

        return checks

    except Exception:
        return {"environment_valid": False}