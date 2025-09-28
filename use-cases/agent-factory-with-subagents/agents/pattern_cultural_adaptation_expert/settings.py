"""
Настройки для Pattern Cultural Adaptation Expert Agent.

Управление конфигурацией агента культурной адаптации через environment variables
и pydantic-settings.
"""

import os
from typing import Optional, List, Dict, Any
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from .dependencies import CultureType, ReligiousContext, CommunicationStyle, ValueSystem


class PatternCulturalAdaptationExpertSettings(BaseSettings):
    """
    Настройки для агента культурной адаптации.

    Поддерживает конфигурацию через переменные окружения и файлы .env.
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="CULTURAL_ADAPTATION_"
    )

    # Основные настройки LLM
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для культурной адаптации"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Специализированные модели для разных задач
    llm_analysis_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для глубокого культурного анализа"
    )
    llm_validation_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для валидации адаптации"
    )

    # Настройки агента
    agent_name: str = Field(
        default="pattern_cultural_adaptation_expert",
        description="Имя агента"
    )
    agent_version: str = Field(default="1.0.0", description="Версия агента")

    # Культурные настройки
    default_target_culture: str = Field(
        default="universal",
        description="Культура по умолчанию"
    )
    supported_cultures: List[str] = Field(
        default_factory=lambda: ["ukrainian", "polish", "english", "german", "universal"],
        description="Поддерживаемые культуры"
    )

    # Настройки адаптации
    default_adaptation_depth: str = Field(
        default="moderate",
        description="Глубина адаптации по умолчанию"
    )
    cultural_safety_checks: bool = Field(
        default=True,
        description="Включить проверки культурной безопасности"
    )
    avoid_stereotypes: bool = Field(
        default=True,
        description="Избегать стереотипов"
    )
    religious_sensitivity_mode: bool = Field(
        default=True,
        description="Режим религиозной чувствительности"
    )

    # Настройки качества
    quality_threshold: float = Field(
        default=0.8,
        description="Порог качества адаптации",
        ge=0.0,
        le=1.0
    )
    expert_validation_required: bool = Field(
        default=False,
        description="Требовать валидацию экспертом"
    )
    a_b_testing_enabled: bool = Field(
        default=False,
        description="Включить A/B тестирование"
    )

    # RAG и база знаний
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )
    knowledge_domain: str = Field(
        default="cultural_psychology",
        description="Домен знаний"
    )
    knowledge_tags: List[str] = Field(
        default_factory=lambda: [
            "cultural_adaptation",
            "cross_cultural_psychology",
            "agent_knowledge",
            "pydantic_ai"
        ],
        description="Теги для поиска в базе знаний"
    )

    # Настройки производительности
    max_concurrent_adaptations: int = Field(
        default=3,
        description="Максимум одновременных адаптаций"
    )
    adaptation_timeout: int = Field(
        default=300,
        description="Таймаут адаптации в секундах"
    )
    cache_adaptations: bool = Field(
        default=True,
        description="Кешировать результаты адаптации"
    )

    # Настройки логирования и мониторинга
    log_level: str = Field(default="INFO", description="Уровень логирования")
    track_adaptation_metrics: bool = Field(
        default=True,
        description="Отслеживать метрики адаптации"
    )
    cultural_acceptance_tracking: bool = Field(
        default=True,
        description="Отслеживать культурную приемлемость"
    )

    # Языковые настройки
    default_language: str = Field(default="ru", description="Язык по умолчанию")
    supported_languages: List[str] = Field(
        default_factory=lambda: ["ru", "uk", "pl", "en", "de"],
        description="Поддерживаемые языки"
    )

    # Региональные настройки
    timezone: str = Field(default="Europe/Kiev", description="Часовой пояс")
    date_format: str = Field(default="%d.%m.%Y", description="Формат даты")
    cultural_calendar: str = Field(
        default="gregorian",
        description="Календарная система"
    )

    # Безопасность и приватность
    anonymize_examples: bool = Field(
        default=True,
        description="Анонимизировать примеры"
    )
    gdpr_compliance: bool = Field(
        default=True,
        description="Соответствие GDPR"
    )
    data_retention_days: int = Field(
        default=90,
        description="Дни хранения данных"
    )

    # Интеграции
    enable_external_validation: bool = Field(
        default=False,
        description="Включить внешнюю валидацию"
    )
    cultural_expert_api_key: Optional[str] = Field(
        default=None,
        description="API ключ для экспертной валидации"
    )

    def get_culture_config(self, culture_type: str) -> Dict[str, Any]:
        """Получить конфигурацию для конкретной культуры."""
        culture_configs = {
            "ukrainian": {
                "language": "uk",
                "religious_context": "orthodox",
                "communication_style": "high_context",
                "value_system": "collectivistic",
                "date_format": "%d.%m.%Y",
                "formal_address": True,
                "emotion_expression": "expressive"
            },
            "polish": {
                "language": "pl",
                "religious_context": "catholic",
                "communication_style": "direct",
                "value_system": "traditional",
                "date_format": "%d.%m.%Y",
                "formal_address": True,
                "emotion_expression": "moderate"
            },
            "english": {
                "language": "en",
                "religious_context": "secular",
                "communication_style": "low_context",
                "value_system": "individualistic",
                "date_format": "%m/%d/%Y",
                "formal_address": False,
                "emotion_expression": "controlled"
            },
            "german": {
                "language": "de",
                "religious_context": "secular",
                "communication_style": "direct",
                "value_system": "structured",
                "date_format": "%d.%m.%Y",
                "formal_address": True,
                "emotion_expression": "reserved"
            },
            "universal": {
                "language": "en",
                "religious_context": "secular",
                "communication_style": "moderate",
                "value_system": "mixed",
                "date_format": "%Y-%m-%d",
                "formal_address": False,
                "emotion_expression": "balanced"
            }
        }

        return culture_configs.get(culture_type, culture_configs["universal"])

    def is_culture_supported(self, culture: str) -> bool:
        """Проверить поддержку культуры."""
        return culture.lower() in [c.lower() for c in self.supported_cultures]

    def get_adaptation_config(self) -> Dict[str, Any]:
        """Получить конфигурацию адаптации."""
        return {
            "depth": self.default_adaptation_depth,
            "quality_threshold": self.quality_threshold,
            "safety_checks": self.cultural_safety_checks,
            "avoid_stereotypes": self.avoid_stereotypes,
            "religious_sensitivity": self.religious_sensitivity_mode,
            "expert_validation": self.expert_validation_required,
            "timeout": self.adaptation_timeout
        }


def load_settings() -> PatternCulturalAdaptationExpertSettings:
    """
    Загрузить настройки из переменных окружения.

    Returns:
        Настройки агента культурной адаптации

    Raises:
        ValueError: Если не удалось загрузить критические настройки
    """
    load_dotenv()

    try:
        settings = PatternCulturalAdaptationExpertSettings()

        # Валидация критических настроек
        if not settings.llm_api_key:
            raise ValueError("LLM_API_KEY не установлен. Добавьте его в файл .env")

        # Проверка поддерживаемых культур
        if settings.default_target_culture not in settings.supported_cultures:
            settings.default_target_culture = "universal"

        return settings

    except Exception as e:
        error_msg = f"Ошибка загрузки настроек агента культурной адаптации: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\n\nТребуемые переменные окружения:"
            error_msg += "\n- CULTURAL_ADAPTATION_LLM_API_KEY: API ключ для LLM"
            error_msg += "\n\nОпциональные переменные:"
            error_msg += "\n- CULTURAL_ADAPTATION_DEFAULT_TARGET_CULTURE: ukrainian/polish/english/universal"
            error_msg += "\n- CULTURAL_ADAPTATION_DEFAULT_ADAPTATION_DEPTH: shallow/moderate/deep"
            error_msg += "\n- CULTURAL_ADAPTATION_QUALITY_THRESHOLD: 0.0-1.0"

        raise ValueError(error_msg) from e


def get_settings() -> PatternCulturalAdaptationExpertSettings:
    """
    Получить настройки агента (кешированная версия).

    Returns:
        Настройки агента
    """
    if not hasattr(get_settings, '_cached_settings'):
        get_settings._cached_settings = load_settings()

    return get_settings._cached_settings


# Предустановленные конфигурации для разных сред
DEVELOPMENT_CONFIG = {
    "log_level": "DEBUG",
    "cultural_safety_checks": True,
    "expert_validation_required": False,
    "a_b_testing_enabled": False,
    "cache_adaptations": False,
    "track_adaptation_metrics": True
}

PRODUCTION_CONFIG = {
    "log_level": "WARNING",
    "cultural_safety_checks": True,
    "expert_validation_required": True,
    "a_b_testing_enabled": True,
    "cache_adaptations": True,
    "track_adaptation_metrics": True
}

TESTING_CONFIG = {
    "log_level": "INFO",
    "cultural_safety_checks": True,
    "expert_validation_required": False,
    "a_b_testing_enabled": False,
    "cache_adaptations": False,
    "track_adaptation_metrics": False
}


def configure_for_environment(env: str = "development") -> Dict[str, Any]:
    """
    Получить конфигурацию для конкретной среды.

    Args:
        env: Среда (development, production, testing)

    Returns:
        Конфигурация для среды
    """
    configs = {
        "development": DEVELOPMENT_CONFIG,
        "production": PRODUCTION_CONFIG,
        "testing": TESTING_CONFIG
    }

    return configs.get(env.lower(), DEVELOPMENT_CONFIG)