"""
Зависимости для Pattern Cultural Adaptation Expert Agent.

Этот модуль определяет зависимости, необходимые для агента культурной адаптации
психологических интервенций.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class CultureType(Enum):
    """Типы культур для адаптации."""
    UKRAINIAN = "ukrainian"
    POLISH = "polish"
    ENGLISH = "english"
    GERMAN = "german"
    SPANISH = "spanish"
    FRENCH = "french"
    UNIVERSAL = "universal"


class ReligiousContext(Enum):
    """Религиозные контексты."""
    ORTHODOX = "orthodox"
    CATHOLIC = "catholic"
    PROTESTANT = "protestant"
    ISLAMIC = "islamic"
    BUDDHIST = "buddhist"
    SECULAR = "secular"
    MIXED = "mixed"


class CommunicationStyle(Enum):
    """Стили коммуникации."""
    HIGH_CONTEXT = "high_context"
    LOW_CONTEXT = "low_context"
    DIRECT = "direct"
    INDIRECT = "indirect"
    FORMAL = "formal"
    INFORMAL = "informal"


class ValueSystem(Enum):
    """Системы ценностей."""
    INDIVIDUALISTIC = "individualistic"
    COLLECTIVISTIC = "collectivistic"
    TRADITIONAL = "traditional"
    MODERN = "modern"
    MIXED_VALUES = "mixed_values"


@dataclass
class CulturalProfile:
    """Профиль культурной адаптации."""
    culture_type: CultureType
    religious_context: ReligiousContext
    communication_style: CommunicationStyle
    value_system: ValueSystem
    sensitive_topics: List[str] = field(default_factory=list)
    preferred_metaphors: List[str] = field(default_factory=list)
    cultural_heroes: List[str] = field(default_factory=list)
    historical_context: Dict[str, Any] = field(default_factory=dict)
    language_specifics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AdaptationSettings:
    """Настройки адаптации контента."""
    adaptation_depth: str = "moderate"  # shallow, moderate, deep
    preserve_core_message: bool = True
    cultural_validation: bool = True
    local_expert_review: bool = False
    adaptation_methodology: str = "evidence_based"

    # Уровни адаптации
    metaphor_adaptation: bool = True
    example_localization: bool = True
    communication_style_adjustment: bool = True
    value_alignment: bool = True
    religious_sensitivity: bool = True


@dataclass
class PatternCulturalAdaptationExpertDependencies:
    """
    Зависимости для агента культурной адаптации психологических интервенций.

    Обеспечивает гибкую настройку под различные культурные контексты
    и требования проектов.
    """

    # Основные настройки
    api_key: str
    agent_name: str = "pattern_cultural_adaptation_expert"

    # Настройки проекта
    project_path: str = ""
    domain_type: str = "psychology"  # psychology, education, healthcare
    project_type: str = "content_adaptation"  # content_adaptation, localization, research
    framework: str = "cross_cultural_psychology"

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "cultural_adaptation", "cross_cultural_psychology", "agent_knowledge", "pydantic_ai"
    ])
    knowledge_domain: str = "cultural_psychology"
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Культурные настройки
    target_culture: CultureType = CultureType.UNIVERSAL
    cultural_profile: Optional[CulturalProfile] = None
    adaptation_settings: AdaptationSettings = field(default_factory=AdaptationSettings)

    # Поддерживаемые культуры
    supported_cultures: List[CultureType] = field(default_factory=lambda: [
        CultureType.UKRAINIAN,
        CultureType.POLISH,
        CultureType.ENGLISH,
        CultureType.GERMAN
    ])

    # Настройки качества
    quality_threshold: float = 0.8
    expert_validation: bool = False
    a_b_testing_enabled: bool = False

    # Ограничения безопасности
    cultural_safety_checks: bool = True
    avoid_stereotypes: bool = True
    religious_sensitivity_mode: bool = True

    # Метрики и отслеживание
    track_adaptation_metrics: bool = True
    cultural_acceptance_tracking: bool = True
    effectiveness_monitoring: bool = True

    def __post_init__(self):
        """Инициализация зависимостей после создания."""
        # Создание культурного профиля по умолчанию если не указан
        if self.cultural_profile is None:
            self.cultural_profile = self._create_default_profile()

        # Валидация настроек
        self._validate_settings()

    def _create_default_profile(self) -> CulturalProfile:
        """Создает профиль культуры по умолчанию."""
        default_profiles = {
            CultureType.UKRAINIAN: CulturalProfile(
                culture_type=CultureType.UKRAINIAN,
                religious_context=ReligiousContext.ORTHODOX,
                communication_style=CommunicationStyle.HIGH_CONTEXT,
                value_system=ValueSystem.COLLECTIVISTIC,
                sensitive_topics=["война", "оккупация", "национальная идентичность"],
                preferred_metaphors=["поле", "дуб", "река", "домашний очаг"],
                cultural_heroes=["Тарас Шевченко", "Леся Украинка", "Иван Франко"],
                historical_context={"current_conflict": True, "independence": "1991"},
                language_specifics={"formality": "moderate", "emotion_expression": "expressive"}
            ),
            CultureType.POLISH: CulturalProfile(
                culture_type=CultureType.POLISH,
                religious_context=ReligiousContext.CATHOLIC,
                communication_style=CommunicationStyle.DIRECT,
                value_system=ValueSystem.TRADITIONAL,
                sensitive_topics=["католическая мораль", "национальная гордость"],
                preferred_metaphors=["католические образы", "исторические события"],
                cultural_heroes=["Иоанн Павел II", "Лех Валенса", "Мария Склодовская-Кюри"],
                historical_context={"solidarity_movement": True, "eu_membership": "2004"},
                language_specifics={"formality": "high", "emotion_expression": "moderate"}
            ),
            CultureType.ENGLISH: CulturalProfile(
                culture_type=CultureType.ENGLISH,
                religious_context=ReligiousContext.SECULAR,
                communication_style=CommunicationStyle.LOW_CONTEXT,
                value_system=ValueSystem.INDIVIDUALISTIC,
                sensitive_topics=["политика", "расовые отношения"],
                preferred_metaphors=["светские", "универсальные"],
                cultural_heroes=["Martin Luther King", "Shakespeare", "Einstein"],
                historical_context={"diversity": True, "globalization": True},
                language_specifics={"formality": "low", "emotion_expression": "controlled"}
            )
        }

        return default_profiles.get(self.target_culture, CulturalProfile(
            culture_type=self.target_culture,
            religious_context=ReligiousContext.SECULAR,
            communication_style=CommunicationStyle.DIRECT,
            value_system=ValueSystem.MIXED_VALUES
        ))

    def _validate_settings(self):
        """Валидация настроек зависимостей."""
        if self.quality_threshold < 0.0 or self.quality_threshold > 1.0:
            raise ValueError("quality_threshold должен быть между 0.0 и 1.0")

        if self.target_culture not in self.supported_cultures:
            raise ValueError(f"Культура {self.target_culture} не поддерживается")

    def get_cultural_context(self) -> Dict[str, Any]:
        """Получить контекст культуры для адаптации."""
        if not self.cultural_profile:
            return {}

        return {
            "culture": self.cultural_profile.culture_type.value,
            "religious_context": self.cultural_profile.religious_context.value,
            "communication_style": self.cultural_profile.communication_style.value,
            "value_system": self.cultural_profile.value_system.value,
            "sensitive_topics": self.cultural_profile.sensitive_topics,
            "preferred_metaphors": self.cultural_profile.preferred_metaphors,
            "cultural_heroes": self.cultural_profile.cultural_heroes,
            "adaptation_settings": {
                "depth": self.adaptation_settings.adaptation_depth,
                "preserve_core": self.adaptation_settings.preserve_core_message,
                "validation": self.adaptation_settings.cultural_validation
            }
        }

    def update_target_culture(self, culture: CultureType):
        """Обновить целевую культуру и профиль."""
        self.target_culture = culture
        self.cultural_profile = self._create_default_profile()

    def is_culture_supported(self, culture: CultureType) -> bool:
        """Проверить, поддерживается ли культура."""
        return culture in self.supported_cultures


def create_cultural_adaptation_dependencies(
    api_key: str,
    target_culture: CultureType = CultureType.UNIVERSAL,
    project_path: str = "",
    domain_type: str = "psychology",
    **kwargs
) -> PatternCulturalAdaptationExpertDependencies:
    """
    Создать зависимости для агента культурной адаптации.

    Args:
        api_key: Ключ API для LLM
        target_culture: Целевая культура для адаптации
        project_path: Путь к проекту
        domain_type: Тип домена (psychology, education, healthcare)
        **kwargs: Дополнительные параметры

    Returns:
        Настроенные зависимости агента
    """
    return PatternCulturalAdaptationExpertDependencies(
        api_key=api_key,
        target_culture=target_culture,
        project_path=project_path,
        domain_type=domain_type,
        **kwargs
    )


# Предустановленные конфигурации для разных культур
UKRAINIAN_CONFIG = {
    "target_culture": CultureType.UKRAINIAN,
    "domain_type": "psychology",
    "knowledge_tags": ["ukrainian_culture", "orthodox_context", "post_soviet", "cultural_adaptation"]
}

POLISH_CONFIG = {
    "target_culture": CultureType.POLISH,
    "domain_type": "psychology",
    "knowledge_tags": ["polish_culture", "catholic_context", "solidarity", "cultural_adaptation"]
}

ENGLISH_CONFIG = {
    "target_culture": CultureType.ENGLISH,
    "domain_type": "psychology",
    "knowledge_tags": ["western_culture", "secular_context", "individualistic", "cultural_adaptation"]
}

UNIVERSAL_CONFIG = {
    "target_culture": CultureType.UNIVERSAL,
    "domain_type": "psychology",
    "knowledge_tags": ["universal_principles", "cross_cultural", "inclusive", "cultural_adaptation"]
}