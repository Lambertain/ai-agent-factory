"""
Зависимости для Pattern VAK Adaptation Specialist Agent.

Содержит типы данных и классы зависимостей для адаптации контента
под сенсорные репрезентативные системы (Visual, Auditory, Kinesthetic)
в рамках проекта PatternShift.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class VAKModalityType(str, Enum):
    """Типы сенсорных модальностей VAK."""

    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    MULTIMODAL = "multimodal"


class AdaptationDepth(str, Enum):
    """Уровни глубины адаптации контента."""

    SURFACE = "surface"      # Поверхностная адаптация предикатов
    MODERATE = "moderate"    # Умеренная адаптация структуры и стиля
    DEEP = "deep"           # Глубокая реконструкция под модальность
    COMPLETE = "complete"    # Полная реконструкция с мультимодальными элементами


class PatternShiftModuleType(str, Enum):
    """Типы модулей в архитектуре PatternShift."""

    TECHNIQUE = "technique"              # НЛП техники
    EXERCISE = "exercise"               # Практические упражнения
    MEDITATION = "meditation"           # Медитативные практики
    VISUALIZATION = "visualization"     # Визуализации
    AUDIO_SESSION = "audio_session"     # Аудио сессии
    MOVEMENT = "movement"              # Движенческие практики
    ASSESSMENT = "assessment"          # Диагностические инструменты
    REFLECTION = "reflection"          # Рефлексивные практики


class VAKProfile(BaseModel):
    """Профиль пользователя по модальностям VAK."""

    primary_modality: VAKModalityType = Field(
        description="Доминирующая сенсорная модальность"
    )
    secondary_modality: Optional[VAKModalityType] = Field(
        default=None,
        description="Вторичная модальность"
    )
    visual_preference: float = Field(
        ge=0.0, le=1.0,
        description="Предпочтение визуальной модальности (0-1)"
    )
    auditory_preference: float = Field(
        ge=0.0, le=1.0,
        description="Предпочтение аудиальной модальности (0-1)"
    )
    kinesthetic_preference: float = Field(
        ge=0.0, le=1.0,
        description="Предпочтение кинестетической модальности (0-1)"
    )
    adaptation_effectiveness: Dict[str, float] = Field(
        default_factory=dict,
        description="Эффективность адаптации по типам модулей"
    )


class ModuleVariant(BaseModel):
    """Вариант модуля для конкретной VAK модальности."""

    base_module_id: str = Field(description="ID базового модуля")
    variant_type: VAKModalityType = Field(description="Тип VAK адаптации")
    adaptation_level: AdaptationDepth = Field(description="Уровень адаптации")
    target_profile: VAKProfile = Field(description="Целевой VAK профиль")
    therapeutic_equivalence: bool = Field(
        default=True,
        description="Сохранение терапевтической эквивалентности"
    )
    effectiveness_score: Optional[float] = Field(
        default=None,
        ge=0.0, le=1.0,
        description="Оценка эффективности варианта"
    )
    usage_statistics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Статистика использования варианта"
    )


class ContentAdaptationRequest(BaseModel):
    """Запрос на адаптацию контента под VAK модальность."""

    original_content: str = Field(description="Исходный контент для адаптации")
    target_modality: VAKModalityType = Field(description="Целевая модальность")
    adaptation_depth: AdaptationDepth = Field(description="Уровень адаптации")
    module_type: PatternShiftModuleType = Field(description="Тип модуля PatternShift")
    preserve_structure: bool = Field(
        default=True,
        description="Сохранить общую структуру контента"
    )
    preserve_therapeutic_goals: bool = Field(
        default=True,
        description="Сохранить терапевтические цели"
    )
    cultural_context: Optional[str] = Field(
        default=None,
        description="Культурный контекст (если нужна дополнительная адаптация)"
    )
    safety_considerations: List[str] = Field(
        default_factory=list,
        description="Соображения безопасности"
    )


class VAKMetrics(BaseModel):
    """Метрики эффективности VAK адаптации."""

    completion_rate: float = Field(
        ge=0.0, le=1.0,
        description="Процент завершения упражнений"
    )
    engagement_score: float = Field(
        ge=0.0, le=1.0,
        description="Уровень вовлеченности пользователя"
    )
    comprehension_level: float = Field(
        ge=0.0, le=1.0,
        description="Уровень понимания материала"
    )
    modality_preference_accuracy: float = Field(
        ge=0.0, le=1.0,
        description="Точность определения предпочитаемой модальности"
    )
    therapeutic_effectiveness: float = Field(
        ge=0.0, le=1.0,
        description="Терапевтическая эффективность"
    )
    adaptation_time: float = Field(
        ge=0.0,
        description="Время выполнения адаптации (в секундах)"
    )
    user_satisfaction: float = Field(
        ge=0.0, le=1.0,
        description="Удовлетворенность пользователя"
    )


@dataclass
class PatternVAKAdaptationDependencies:
    """
    Зависимости для Pattern VAK Adaptation Specialist Agent.

    Содержит настройки и конфигурацию для работы с системой
    адаптации контента под VAK модальности в PatternShift.
    """

    # Базовые настройки
    api_key: str
    agent_name: str = "pattern_vak_adaptation_specialist"

    # PatternShift интеграция
    patternshift_project_path: str = "D:/Automation/Development/projects/patternshift"
    module_storage_path: str = ""
    content_versions_path: str = ""

    # VAK конфигурация
    default_adaptation_depth: AdaptationDepth = AdaptationDepth.MODERATE
    enable_multimodal_variants: bool = True
    auto_detect_modality: bool = True
    preserve_therapeutic_integrity: bool = True

    # Системы безопасности PatternShift
    enable_crisis_detection: bool = True
    require_safety_validation: bool = True
    trauma_informed_adaptations: bool = True

    # Производительность и кэширование
    cache_adapted_content: bool = True
    max_adaptation_time: float = 30.0  # секунды
    batch_adaptation_size: int = 10

    # Аналитика и метрики
    collect_usage_metrics: bool = True
    enable_effectiveness_tracking: bool = True
    adaptive_learning: bool = True

    # Интеграция с Archon
    archon_project_id: str = "pattern-shift-vak-system"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "vak", "adaptation", "sensory-modalities", "nlp", "pattern-shift"
    ])
    knowledge_domain: str = "psychology.patternshift.org"

    # Локализация и культурная адаптация
    default_language: str = "ru"
    supported_languages: List[str] = field(default_factory=lambda: ["ru", "en", "uk"])
    cultural_adaptation_enabled: bool = True

    # A/B тестирование
    enable_ab_testing: bool = True
    variant_distribution: Dict[str, float] = field(default_factory=lambda: {
        "visual": 0.33,
        "auditory": 0.33,
        "kinesthetic": 0.34
    })

    # Система версионирования модулей
    module_versioning_enabled: bool = True
    auto_version_variants: bool = True
    version_retention_days: int = 90

    def __post_init__(self):
        """Инициализация дополнительных настроек."""
        if not self.module_storage_path:
            self.module_storage_path = f"{self.patternshift_project_path}/data/modules"

        if not self.content_versions_path:
            self.content_versions_path = f"{self.patternshift_project_path}/data/versions"

        # Валидация процентного распределения
        total_distribution = sum(self.variant_distribution.values())
        if abs(total_distribution - 1.0) > 0.01:
            # Нормализуем распределение
            for key in self.variant_distribution:
                self.variant_distribution[key] /= total_distribution


def create_vak_adaptation_dependencies(
    api_key: str,
    adaptation_depth: AdaptationDepth = AdaptationDepth.MODERATE,
    enable_multimodal: bool = True,
    enable_safety_validation: bool = True,
    **kwargs
) -> PatternVAKAdaptationDependencies:
    """
    Создать зависимости для VAK адаптации с настройками по умолчанию.

    Args:
        api_key: API ключ для LLM
        adaptation_depth: Уровень глубины адаптации
        enable_multimodal: Включить мультимодальные варианты
        enable_safety_validation: Включить валидацию безопасности
        **kwargs: Дополнительные параметры

    Returns:
        Настроенные зависимости для агента
    """
    return PatternVAKAdaptationDependencies(
        api_key=api_key,
        default_adaptation_depth=adaptation_depth,
        enable_multimodal_variants=enable_multimodal,
        require_safety_validation=enable_safety_validation,
        **kwargs
    )


def create_therapy_vak_dependencies(api_key: str) -> PatternVAKAdaptationDependencies:
    """Создать зависимости для терапевтических модулей."""
    return create_vak_adaptation_dependencies(
        api_key=api_key,
        adaptation_depth=AdaptationDepth.DEEP,
        enable_safety_validation=True,
        trauma_informed_adaptations=True,
        enable_crisis_detection=True,
        preserve_therapeutic_integrity=True
    )


def create_educational_vak_dependencies(api_key: str) -> PatternVAKAdaptationDependencies:
    """Создать зависимости для образовательных модулей."""
    return create_vak_adaptation_dependencies(
        api_key=api_key,
        adaptation_depth=AdaptationDepth.MODERATE,
        enable_multimodal=True,
        enable_ab_testing=True,
        adaptive_learning=True
    )


def create_wellness_vak_dependencies(api_key: str) -> PatternVAKAdaptationDependencies:
    """Создать зависимости для велнес модулей."""
    return create_vak_adaptation_dependencies(
        api_key=api_key,
        adaptation_depth=AdaptationDepth.SURFACE,
        enable_multimodal=True,
        enable_safety_validation=False,
        collect_usage_metrics=True
    )


# Константы для предикатов VAK
VISUAL_PREDICATES = [
    "видеть", "смотреть", "наблюдать", "замечать", "представлять", "воображать",
    "фокусировать", "иллюстрировать", "яркий", "ясный", "туманный", "красочный",
    "блестящий", "темный", "прозрачный", "картина", "образ", "перспектива",
    "точка зрения", "сцена", "видение"
]

AUDITORY_PREDICATES = [
    "слышать", "слушать", "говорить", "звучать", "рассказывать", "объяснять",
    "обсуждать", "молчать", "громкий", "тихий", "звучный", "мелодичный",
    "гармоничный", "резкий", "глухой", "голос", "звук", "тон", "ритм",
    "мелодия", "эхо", "резонанс", "диалог"
]

KINESTHETIC_PREDICATES = [
    "чувствовать", "касаться", "двигаться", "давить", "схватывать", "течь",
    "сопротивляться", "расслабляться", "теплый", "холодный", "мягкий", "твердый",
    "гладкий", "шершавый", "тяжелый", "легкий", "ощущение", "чувство",
    "прикосновение", "движение", "давление", "напряжение", "комфорт"
]

# Метафоры для каждой модальности
VAK_METAPHORS = {
    VAKModalityType.VISUAL: [
        "ясная картина", "яркий образ", "светлое будущее", "туманное понимание",
        "фокус внимания", "широкая перспектива", "четкие границы", "цветная палитра"
    ],
    VAKModalityType.AUDITORY: [
        "внутренний голос", "звук души", "гармония мыслей", "эхо прошлого",
        "диалог с собой", "мелодия жизни", "ритм сердца", "тишина разума"
    ],
    VAKModalityType.KINESTHETIC: [
        "почувствовать сердцем", "тепло души", "движение вперед", "легкость бытия",
        "глубокое понимание", "прикосновение к истине", "поток энергии", "внутренняя сила"
    ]
}