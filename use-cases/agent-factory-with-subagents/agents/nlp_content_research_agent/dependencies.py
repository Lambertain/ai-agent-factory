"""
NLP Content Research Agent Dependencies

Зависимости для универсального исследовательского агента с NLP специализацией.
Поддерживает работу в любых доменах: психология, астрология, таро, нумерология и др.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from .settings import load_settings


class ResearchDomain(str, Enum):
    """Поддерживаемые домены исследования."""
    PSYCHOLOGY = "psychology"
    ASTROLOGY = "astrology"
    TAROT = "tarot"
    NUMEROLOGY = "numerology"
    COACHING = "coaching"
    SPIRITUALITY = "spirituality"
    RELATIONSHIPS = "relationships"
    PERSONAL_GROWTH = "personal_growth"
    GENERAL = "general"


class NLPTechnique(str, Enum):
    """NLP техники для адаптации контента."""
    ANCHORING = "anchoring"
    RAPPORT_BUILDING = "rapport_building"
    REFRAMING = "reframing"
    PRESUPPOSITIONS = "presuppositions"
    VAK_ADAPTATION = "vak_adaptation"
    ERICKSONIAN_HYPNOSIS = "ericksonian_hypnosis"
    STORYTELLING = "storytelling"
    LANGUAGE_PATTERNS = "language_patterns"


class AudienceType(str, Enum):
    """Типы целевой аудитории."""
    GENERAL_PUBLIC = "general_public"
    PROFESSIONALS = "professionals"
    STUDENTS = "students"
    CLINICAL_POPULATION = "clinical_population"
    SPECIFIC_AGE_GROUP = "specific_age_group"
    SPECIFIC_GENDER = "specific_gender"


@dataclass
class NLPContentResearchDependencies:
    """
    Зависимости для NLP Content Research Agent.

    Универсальная конфигурация для работы в любых доменах.
    """

    # Основные настройки
    api_key: str
    project_path: str = ""

    # Домен и специализация
    research_domain: ResearchDomain = ResearchDomain.PSYCHOLOGY
    domain_expertise_level: str = "advanced"  # basic, intermediate, advanced, expert

    # NLP конфигурация
    primary_nlp_techniques: List[NLPTechnique] = field(
        default_factory=lambda: [
            NLPTechnique.VAK_ADAPTATION,
            NLPTechnique.RAPPORT_BUILDING,
            NLPTechnique.REFRAMING
        ]
    )
    ericksonian_intensity: str = "moderate"  # light, moderate, intensive

    # Аудитория
    target_audience: AudienceType = AudienceType.GENERAL_PUBLIC
    audience_education_level: str = "mixed"  # low, mixed, high
    audience_language_preference: str = "simple"  # simple, mixed, scientific

    # Исследовательские параметры
    research_depth: str = "comprehensive"  # quick, standard, comprehensive, exhaustive
    scientific_rigor_level: str = "balanced"  # relaxed, balanced, strict, academic

    # Источники данных
    enable_web_search: bool = True
    enable_academic_search: bool = True
    enable_competitive_analysis: bool = True
    enable_viral_content_analysis: bool = True

    # Выходные форматы
    output_formats: List[str] = field(
        default_factory=lambda: ["research_brief", "content_outline", "vak_adaptations"]
    )
    include_statistics: bool = True
    include_case_studies: bool = True
    include_expert_quotes: bool = False

    # Языковые настройки
    content_language: str = "ru"
    secondary_language: Optional[str] = None
    dual_language_mode: bool = False  # Научный 20% + Простой 80%

    # RAG и база знаний
    agent_name: str = "nlp_content_research_agent"
    knowledge_tags: List[str] = field(
        default_factory=lambda: ["nlp-content-research", "agent-knowledge", "pydantic-ai"]
    )
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Патлернификация (PatternShift методология)
    enable_patternshift_methodology: bool = True
    viral_potential_analysis: bool = True
    pain_point_identification: bool = True
    conversion_optimization: bool = True

    # Лимиты и производительность
    max_search_results: int = 50
    max_sources_per_domain: int = 10
    research_timeout_minutes: int = 30
    batch_processing_enabled: bool = True

    def __post_init__(self):
        """Инициализация и валидация настроек."""
        # Автоматическая настройка тегов знаний
        if not self.knowledge_tags:
            domain_tag = self.research_domain.value.replace("_", "-")
            self.knowledge_tags = [
                "nlp-content-research",
                f"{domain_tag}-research",
                "agent-knowledge",
                "pydantic-ai"
            ]

        # Настройка специфичных для домена параметров
        self._configure_domain_specifics()

    def _configure_domain_specifics(self):
        """Настройка параметров специфичных для домена."""
        domain_configs = {
            ResearchDomain.PSYCHOLOGY: {
                "knowledge_domain": "psychology.research",
                "scientific_rigor_level": "strict",
                "include_expert_quotes": True
            },
            ResearchDomain.ASTROLOGY: {
                "knowledge_domain": "astrology.popular",
                "scientific_rigor_level": "relaxed",
                "audience_language_preference": "mystical"
            },
            ResearchDomain.TAROT: {
                "knowledge_domain": "tarot.interpretation",
                "scientific_rigor_level": "relaxed",
                "audience_language_preference": "symbolic"
            },
            ResearchDomain.NUMEROLOGY: {
                "knowledge_domain": "numerology.systems",
                "scientific_rigor_level": "balanced",
                "audience_language_preference": "analytical"
            }
        }

        config = domain_configs.get(self.research_domain, {})
        for key, value in config.items():
            if hasattr(self, key) and getattr(self, key) is None:
                setattr(self, key, value)

    def get_domain_context(self) -> Dict[str, Any]:
        """Получить контекст для текущего домена исследования."""
        return {
            "domain": self.research_domain.value,
            "expertise_level": self.domain_expertise_level,
            "target_audience": self.target_audience.value,
            "language_preference": self.audience_language_preference,
            "nlp_techniques": [t.value for t in self.primary_nlp_techniques],
            "scientific_rigor": self.scientific_rigor_level,
            "research_depth": self.research_depth
        }

    def get_search_parameters(self) -> Dict[str, Any]:
        """Получить параметры для поисковых запросов."""
        return {
            "max_results": self.max_search_results,
            "max_sources_per_domain": self.max_sources_per_domain,
            "timeout_minutes": self.research_timeout_minutes,
            "enable_web_search": self.enable_web_search,
            "enable_academic_search": self.enable_academic_search,
            "enable_competitive_analysis": self.enable_competitive_analysis,
            "enable_viral_analysis": self.enable_viral_content_analysis
        }

    def get_nlp_configuration(self) -> Dict[str, Any]:
        """Получить конфигурацию NLP техник."""
        return {
            "primary_techniques": [t.value for t in self.primary_nlp_techniques],
            "ericksonian_intensity": self.ericksonian_intensity,
            "vak_adaptation_enabled": NLPTechnique.VAK_ADAPTATION in self.primary_nlp_techniques,
            "storytelling_enabled": NLPTechnique.STORYTELLING in self.primary_nlp_techniques,
            "rapport_building_enabled": NLPTechnique.RAPPORT_BUILDING in self.primary_nlp_techniques
        }


def create_research_dependencies(
    api_key: str,
    research_domain: str = "psychology",
    target_audience: str = "general_public",
    nlp_techniques: Optional[List[str]] = None,
    **kwargs
) -> NLPContentResearchDependencies:
    """
    Создать настроенные зависимости для исследовательского агента.

    Args:
        api_key: API ключ для LLM
        research_domain: Домен исследования
        target_audience: Целевая аудитория
        nlp_techniques: Список NLP техник
        **kwargs: Дополнительные параметры

    Returns:
        Настроенные зависимости
    """
    # Конвертируем строки в enum
    domain = ResearchDomain(research_domain) if isinstance(research_domain, str) else research_domain
    audience = AudienceType(target_audience) if isinstance(target_audience, str) else target_audience

    # Конвертируем NLP техники
    techniques = []
    if nlp_techniques:
        techniques = [NLPTechnique(t) for t in nlp_techniques if t in NLPTechnique.__members__.values()]

    return NLPContentResearchDependencies(
        api_key=api_key,
        research_domain=domain,
        target_audience=audience,
        primary_nlp_techniques=techniques if techniques else None,
        **kwargs
    )


def create_psychology_research_dependencies(api_key: str) -> NLPContentResearchDependencies:
    """Создать зависимости для психологических исследований."""
    return create_research_dependencies(
        api_key=api_key,
        research_domain=ResearchDomain.PSYCHOLOGY,
        target_audience=AudienceType.GENERAL_PUBLIC,
        nlp_techniques=[
            NLPTechnique.VAK_ADAPTATION.value,
            NLPTechnique.RAPPORT_BUILDING.value,
            NLPTechnique.ERICKSONIAN_HYPNOSIS.value
        ],
        scientific_rigor_level="strict",
        include_expert_quotes=True,
        dual_language_mode=True
    )


def create_astrology_research_dependencies(api_key: str) -> NLPContentResearchDependencies:
    """Создать зависимости для астрологических исследований."""
    return create_research_dependencies(
        api_key=api_key,
        research_domain=ResearchDomain.ASTROLOGY,
        target_audience=AudienceType.GENERAL_PUBLIC,
        nlp_techniques=[
            NLPTechnique.STORYTELLING.value,
            NLPTechnique.LANGUAGE_PATTERNS.value,
            NLPTechnique.ANCHORING.value
        ],
        scientific_rigor_level="relaxed",
        audience_language_preference="mystical",
        enable_viral_content_analysis=True
    )


def create_universal_research_dependencies(
    api_key: str,
    domain: str = "general"
) -> NLPContentResearchDependencies:
    """Создать универсальные зависимости для любого домена."""
    return create_research_dependencies(
        api_key=api_key,
        research_domain=domain,
        target_audience=AudienceType.GENERAL_PUBLIC,
        nlp_techniques=[
            NLPTechnique.VAK_ADAPTATION.value,
            NLPTechnique.RAPPORT_BUILDING.value,
            NLPTechnique.REFRAMING.value
        ],
        research_depth="comprehensive",
        enable_patternshift_methodology=True
    )


# Алиасы для совместимости
ResearchDependencies = NLPContentResearchDependencies
create_dependencies = create_research_dependencies


__all__ = [
    "NLPContentResearchDependencies",
    "ResearchDomain",
    "NLPTechnique",
    "AudienceType",
    "create_research_dependencies",
    "create_psychology_research_dependencies",
    "create_astrology_research_dependencies",
    "create_universal_research_dependencies",
    "ResearchDependencies",
    "create_dependencies"
]