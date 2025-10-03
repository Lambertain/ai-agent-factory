"""
Настройки и конфигурация для Pattern VAK Adaptation Specialist Agent.

Содержит настройки для интеграции с PatternShift и управления
системой адаптации контента под VAK модальности.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseSettings, Field, validator
from pydantic_settings import BaseSettings as PydanticSettings
from dotenv import load_dotenv

from .dependencies import (
    VAKModalityType,
    AdaptationDepth,
    PatternShiftModuleType
)


# Загружаем переменные окружения
load_dotenv()


class PatternVAKSettings(PydanticSettings):
    """
    Настройки для Pattern VAK Adaptation Specialist Agent.

    Поддерживает конфигурацию через переменные окружения
    с префиксом PATTERN_VAK_.
    """

    class Config:
        env_prefix = "PATTERN_VAK_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

    # Базовые настройки LLM
    llm_api_key: str = Field(..., description="API ключ для LLM")
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель LLM для VAK адаптации"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL для LLM API"
    )
    llm_temperature: float = Field(
        default=0.3,
        ge=0.0, le=2.0,
        description="Температура для генерации (творчество vs точность)"
    )
    llm_max_tokens: int = Field(
        default=4000,
        ge=100, le=8000,
        description="Максимальное количество токенов в ответе"
    )

    # Пути к проекту PatternShift
    patternshift_project_path: str = Field(
        default="D:/Automation/Development/projects/patternshift",
        description="Путь к корневой директории проекта PatternShift"
    )
    modules_storage_path: str = Field(
        default="",
        description="Путь к хранилищу модулей (автоматически определяется)"
    )
    content_versions_path: str = Field(
        default="",
        description="Путь к версиям контента (автоматически определяется)"
    )
    knowledge_base_path: str = Field(
        default="",
        description="Путь к базе знаний (автоматически определяется)"
    )

    # Настройки VAK адаптации
    default_adaptation_depth: AdaptationDepth = Field(
        default=AdaptationDepth.MODERATE,
        description="Уровень адаптации по умолчанию"
    )
    enable_multimodal_variants: bool = Field(
        default=True,
        description="Включить создание мультимодальных вариантов"
    )
    auto_detect_user_modality: bool = Field(
        default=True,
        description="Автоматически определять предпочитаемую модальность пользователя"
    )
    preserve_therapeutic_integrity: bool = Field(
        default=True,
        description="Всегда сохранять терапевтическую целостность"
    )

    # Система безопасности PatternShift
    enable_crisis_detection: bool = Field(
        default=True,
        description="Включить систему детекции кризисных состояний"
    )
    require_safety_validation: bool = Field(
        default=True,
        description="Требовать валидацию безопасности для всех адаптаций"
    )
    trauma_informed_adaptations: bool = Field(
        default=True,
        description="Использовать травма-информированный подход"
    )
    max_trigger_risk_level: float = Field(
        default=0.3,
        ge=0.0, le=1.0,
        description="Максимальный допустимый уровень риска триггеров"
    )

    # Производительность и кэширование
    cache_adapted_content: bool = Field(
        default=True,
        description="Кэшировать адаптированный контент"
    )
    cache_ttl_hours: int = Field(
        default=24,
        ge=1, le=168,
        description="Время жизни кэша в часах"
    )
    max_adaptation_time_seconds: float = Field(
        default=30.0,
        ge=5.0, le=120.0,
        description="Максимальное время адаптации в секундах"
    )
    batch_adaptation_size: int = Field(
        default=10,
        ge=1, le=50,
        description="Размер пакета для массовой адаптации"
    )
    concurrent_adaptations: int = Field(
        default=3,
        ge=1, le=10,
        description="Количество одновременных адаптаций"
    )

    # Аналитика и метрики
    collect_usage_metrics: bool = Field(
        default=True,
        description="Собирать метрики использования"
    )
    enable_effectiveness_tracking: bool = Field(
        default=True,
        description="Отслеживать эффективность адаптаций"
    )
    adaptive_learning_enabled: bool = Field(
        default=True,
        description="Включить адаптивное обучение на основе обратной связи"
    )
    metrics_retention_days: int = Field(
        default=90,
        ge=7, le=365,
        description="Период хранения метрик в днях"
    )

    # Интеграция с Archon
    archon_project_id: str = Field(
        default="pattern-shift-vak-system",
        description="ID проекта в Archon MCP"
    )
    archon_api_url: str = Field(
        default="http://localhost:3737",
        description="URL Archon MCP сервера"
    )
    knowledge_tags: List[str] = Field(
        default_factory=lambda: [
            "vak", "adaptation", "sensory-modalities", "nlp", "pattern-shift"
        ],
        description="Теги для поиска в базе знаний"
    )
    knowledge_domain: str = Field(
        default="psychology.patternshift.org",
        description="Домен знаний для фильтрации поиска"
    )

    # Локализация и мультиязычность
    default_language: str = Field(
        default="ru",
        description="Язык по умолчанию"
    )
    supported_languages: List[str] = Field(
        default_factory=lambda: ["ru", "en", "uk"],
        description="Поддерживаемые языки"
    )
    cultural_adaptation_enabled: bool = Field(
        default=True,
        description="Включить культурную адаптацию"
    )

    # A/B тестирование и экспериментация
    enable_ab_testing: bool = Field(
        default=True,
        description="Включить A/B тестирование вариантов"
    )
    variant_distribution: Dict[str, float] = Field(
        default_factory=lambda: {
            "visual": 0.33,
            "auditory": 0.33,
            "kinesthetic": 0.34
        },
        description="Распределение вариантов для A/B тестирования"
    )
    experiment_sample_size: int = Field(
        default=100,
        ge=10, le=1000,
        description="Размер выборки для экспериментов"
    )

    # Система версионирования
    module_versioning_enabled: bool = Field(
        default=True,
        description="Включить версионирование модулей"
    )
    auto_version_variants: bool = Field(
        default=True,
        description="Автоматически создавать версии для вариантов"
    )
    version_retention_days: int = Field(
        default=90,
        ge=7, le=365,
        description="Период хранения версий в днях"
    )
    max_versions_per_module: int = Field(
        default=10,
        ge=3, le=50,
        description="Максимальное количество версий на модуль"
    )

    # Настройки качества и валидации
    min_quality_score: float = Field(
        default=0.7,
        ge=0.0, le=1.0,
        description="Минимальная оценка качества для принятия адаптации"
    )
    therapeutic_integrity_threshold: float = Field(
        default=0.8,
        ge=0.0, le=1.0,
        description="Порог сохранения терапевтической целостности"
    )
    auto_reject_unsafe_content: bool = Field(
        default=True,
        description="Автоматически отклонять небезопасный контент"
    )

    # Интеграция с внешними сервисами
    enable_external_validation: bool = Field(
        default=False,
        description="Включить валидацию через внешние сервисы"
    )
    external_validator_url: Optional[str] = Field(
        default=None,
        description="URL внешнего валидатора (если используется)"
    )
    external_validator_api_key: Optional[str] = Field(
        default=None,
        description="API ключ для внешнего валидатора"
    )

    @validator('patternshift_project_path')
    def validate_project_path(cls, v):
        """Валидация пути к проекту PatternShift."""
        path = Path(v)
        if not path.exists():
            raise ValueError(f"Путь к проекту PatternShift не существует: {v}")
        return str(path.absolute())

    @validator('variant_distribution')
    def validate_distribution(cls, v):
        """Валидация распределения вариантов."""
        total = sum(v.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError("Сумма распределения вариантов должна быть равна 1.0")
        return v

    @validator('llm_temperature')
    def validate_temperature(cls, v):
        """Валидация температуры для разных задач."""
        if v > 1.0:
            # Высокая температура может привести к непредсказуемым результатам
            # в терапевтическом контексте
            raise ValueError("Температура >1.0 может быть небезопасна для терапевтического контента")
        return v

    def __init__(self, **data):
        super().__init__(**data)

        # Автоматически устанавливаем производные пути
        if not self.modules_storage_path:
            self.modules_storage_path = os.path.join(
                self.patternshift_project_path, "data", "modules"
            )

        if not self.content_versions_path:
            self.content_versions_path = os.path.join(
                self.patternshift_project_path, "data", "versions"
            )

        if not self.knowledge_base_path:
            self.knowledge_base_path = os.path.join(
                self.patternshift_project_path, "knowledge"
            )

        # Создаем директории если они не существуют
        self._ensure_directories()

    def _ensure_directories(self):
        """Создание необходимых директорий."""
        directories = [
            self.modules_storage_path,
            self.content_versions_path,
            self.knowledge_base_path,
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

    def get_cache_path(self) -> str:
        """Получить путь к директории кэша."""
        cache_path = os.path.join(self.patternshift_project_path, "cache", "vak_adaptations")
        Path(cache_path).mkdir(parents=True, exist_ok=True)
        return cache_path

    def get_logs_path(self) -> str:
        """Получить путь к директории логов."""
        logs_path = os.path.join(self.patternshift_project_path, "logs", "vak_agent")
        Path(logs_path).mkdir(parents=True, exist_ok=True)
        return logs_path

    def get_metrics_path(self) -> str:
        """Получить путь к директории метрик."""
        metrics_path = os.path.join(self.patternshift_project_path, "data", "metrics", "vak")
        Path(metrics_path).mkdir(parents=True, exist_ok=True)
        return metrics_path

    def is_modality_enabled(self, modality: VAKModalityType) -> bool:
        """Проверить, включена ли конкретная модальность."""
        # В текущей версии все модальности включены
        # В будущем можно добавить настройки для отключения модальностей
        return True

    def get_adaptation_config(self, module_type: PatternShiftModuleType) -> Dict[str, Any]:
        """
        Получить конфигурацию адаптации для конкретного типа модуля.

        Args:
            module_type: Тип модуля PatternShift

        Returns:
            Словарь с настройками адаптации
        """
        base_config = {
            "adaptation_depth": self.default_adaptation_depth,
            "preserve_therapeutic_integrity": self.preserve_therapeutic_integrity,
            "enable_safety_validation": self.require_safety_validation,
            "max_adaptation_time": self.max_adaptation_time_seconds
        }

        # Специфичные настройки для разных типов модулей
        module_specific_configs = {
            PatternShiftModuleType.TECHNIQUE: {
                "adaptation_depth": AdaptationDepth.DEEP,
                "require_step_by_step": True,
                "preserve_sequence": True
            },
            PatternShiftModuleType.MEDITATION: {
                "adaptation_depth": AdaptationDepth.DEEP,
                "enable_relaxation_focus": True,
                "slower_pace_kinesthetic": True
            },
            PatternShiftModuleType.VISUALIZATION: {
                "adaptation_depth": AdaptationDepth.COMPLETE,
                "visual_dominance": True,
                "rich_imagery": True
            },
            PatternShiftModuleType.MOVEMENT: {
                "adaptation_depth": AdaptationDepth.COMPLETE,
                "kinesthetic_dominance": True,
                "physical_instructions": True
            },
            PatternShiftModuleType.AUDIO_SESSION: {
                "adaptation_depth": AdaptationDepth.DEEP,
                "auditory_dominance": True,
                "rhythmic_structure": True
            },
            PatternShiftModuleType.ASSESSMENT: {
                "adaptation_depth": AdaptationDepth.MODERATE,
                "preserve_validity": True,
                "clear_instructions": True
            }
        }

        # Объединяем базовую и специфичную конфигурацию
        specific_config = module_specific_configs.get(module_type, {})
        return {**base_config, **specific_config}

    def get_safety_config(self) -> Dict[str, Any]:
        """Получить конфигурацию системы безопасности."""
        return {
            "enable_crisis_detection": self.enable_crisis_detection,
            "require_safety_validation": self.require_safety_validation,
            "trauma_informed": self.trauma_informed_adaptations,
            "max_trigger_risk": self.max_trigger_risk_level,
            "auto_reject_unsafe": self.auto_reject_unsafe_content,
            "therapeutic_integrity_threshold": self.therapeutic_integrity_threshold
        }

    def get_performance_config(self) -> Dict[str, Any]:
        """Получить конфигурацию производительности."""
        return {
            "cache_enabled": self.cache_adapted_content,
            "cache_ttl_hours": self.cache_ttl_hours,
            "max_adaptation_time": self.max_adaptation_time_seconds,
            "batch_size": self.batch_adaptation_size,
            "concurrent_limit": self.concurrent_adaptations
        }

    def get_experimentation_config(self) -> Dict[str, Any]:
        """Получить конфигурацию экспериментов и A/B тестирования."""
        return {
            "ab_testing_enabled": self.enable_ab_testing,
            "variant_distribution": self.variant_distribution,
            "sample_size": self.experiment_sample_size,
            "adaptive_learning": self.adaptive_learning_enabled
        }


# Глобальный экземпляр настроек
_settings_instance: Optional[PatternVAKSettings] = None


def get_settings() -> PatternVAKSettings:
    """
    Получить экземпляр настроек (синглтон).

    Returns:
        Настройки VAK агента
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = PatternVAKSettings()
    return _settings_instance


def load_settings_from_file(config_file: str) -> PatternVAKSettings:
    """
    Загрузить настройки из файла.

    Args:
        config_file: Путь к файлу конфигурации

    Returns:
        Настройки VAK агента
    """
    global _settings_instance

    # Загружаем переменные из указанного файла
    load_dotenv(config_file)
    _settings_instance = PatternVAKSettings()

    return _settings_instance


def create_development_settings() -> PatternVAKSettings:
    """
    Создать настройки для разработки.

    Returns:
        Настройки с параметрами для разработки
    """
    return PatternVAKSettings(
        llm_temperature=0.5,  # Более высокая креативность для экспериментов
        cache_adapted_content=False,  # Отключить кэш для тестирования
        enable_ab_testing=True,
        collect_usage_metrics=True,
        enable_effectiveness_tracking=True,
        require_safety_validation=True,  # Всегда включено для безопасности
        max_adaptation_time_seconds=60.0  # Больше времени для отладки
    )


def create_production_settings() -> PatternVAKSettings:
    """
    Создать настройки для производства.

    Returns:
        Настройки с параметрами для продакшена
    """
    return PatternVAKSettings(
        llm_temperature=0.3,  # Более предсказуемые результаты
        cache_adapted_content=True,
        cache_ttl_hours=24,
        enable_ab_testing=True,
        collect_usage_metrics=True,
        enable_effectiveness_tracking=True,
        require_safety_validation=True,
        auto_reject_unsafe_content=True,
        max_adaptation_time_seconds=30.0
    )


def create_testing_settings() -> PatternVAKSettings:
    """
    Создать настройки для тестирования.

    Returns:
        Настройки с параметрами для тестов
    """
    return PatternVAKSettings(
        llm_temperature=0.1,  # Максимальная предсказуемость
        cache_adapted_content=False,
        enable_ab_testing=False,
        collect_usage_metrics=False,
        enable_effectiveness_tracking=False,
        require_safety_validation=True,
        max_adaptation_time_seconds=10.0,
        batch_adaptation_size=3,
        concurrent_adaptations=1
    )


# Константы для настроек
DEFAULT_VAK_DISTRIBUTION = {
    VAKModalityType.VISUAL: 0.33,
    VAKModalityType.AUDITORY: 0.33,
    VAKModalityType.KINESTHETIC: 0.34
}

ADAPTATION_QUALITY_THRESHOLDS = {
    "excellent": 0.9,
    "good": 0.7,
    "acceptable": 0.5,
    "poor": 0.3
}

SAFETY_RISK_LEVELS = {
    "low": 0.2,
    "medium": 0.5,
    "high": 0.7,
    "critical": 0.9
}

MODULE_TYPE_PRIORITIES = {
    PatternShiftModuleType.TECHNIQUE: 1,      # Высший приоритет
    PatternShiftModuleType.ASSESSMENT: 2,
    PatternShiftModuleType.MEDITATION: 3,
    PatternShiftModuleType.VISUALIZATION: 4,
    PatternShiftModuleType.MOVEMENT: 5,
    PatternShiftModuleType.AUDIO_SESSION: 6,
    PatternShiftModuleType.EXERCISE: 7,
    PatternShiftModuleType.REFLECTION: 8     # Низший приоритет
}