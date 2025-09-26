"""
NLP Content Quality Guardian Agent Dependencies

Зависимости для агента валидации качества NLP контента и программ трансформации.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime


class ValidationDomain(Enum):
    """Домены валидации контента."""
    PSYCHOLOGY = "psychology"
    ASTROLOGY = "astrology"
    TAROT = "tarot"
    NUMEROLOGY = "numerology"
    UNIVERSAL = "universal"


class ContentType(Enum):
    """Типы контента для валидации."""
    TEST = "test"
    TRANSFORMATION_PROGRAM = "transformation_program"
    NLP_TECHNIQUE = "nlp_technique"
    ERICKSONIAN_PATTERN = "ericksonian_pattern"
    KNOWLEDGE_BASE = "knowledge_base"
    MIXED_CONTENT = "mixed_content"


class QualityLevel(Enum):
    """Уровни качества контента."""
    EXCELLENT = "excellent"      # 90-100%
    GOOD = "good"               # 70-89%
    NEEDS_IMPROVEMENT = "needs_improvement"  # 50-69%
    UNACCEPTABLE = "unacceptable"  # <50%


class ValidationAspect(Enum):
    """Аспекты валидации."""
    METHODOLOGY_COMPLIANCE = "methodology_compliance"
    PSYCHOLOGICAL_CORRECTNESS = "psychological_correctness"
    NLP_TECHNIQUE_QUALITY = "nlp_technique_quality"
    ETHICAL_SAFETY = "ethical_safety"
    SCIENTIFIC_VALIDITY = "scientific_validity"
    CULTURAL_SENSITIVITY = "cultural_sensitivity"
    AGE_APPROPRIATENESS = "age_appropriateness"
    MULTILINGUAL_QUALITY = "multilingual_quality"


class CriticalFlag(Enum):
    """Критические флаги безопасности."""
    POTENTIALLY_HARMFUL = "potentially_harmful"
    MANIPULATIVE_CONTENT = "manipulative_content"
    UNETHICAL_PRACTICE = "unethical_practice"
    PSEUDOSCIENTIFIC_CLAIM = "pseudoscientific_claim"
    LEGAL_VIOLATION = "legal_violation"
    AGE_INAPPROPRIATE = "age_inappropriate"


@dataclass
class ValidationCriteria:
    """Критерии валидации контента."""

    # Методология PatternShift
    min_test_questions: int = 15
    require_life_situations: bool = True
    require_vak_personalization: bool = True
    require_multiformat_content: bool = True
    require_anti_repetition: bool = True

    # Структура программы
    require_three_level_structure: bool = True
    crisis_days: int = 21
    stabilization_days: int = 21
    development_days: int = 14

    # Качество техник
    require_scientific_basis: bool = True
    require_ethical_safety: bool = True
    require_age_adaptation: bool = True
    require_cultural_sensitivity: bool = True

    # Языковые требования
    avoid_clinical_terms: bool = True
    require_life_language: bool = True
    require_positive_framing: bool = True

    # Безопасность
    max_risk_level: str = "low"
    require_contraindications: bool = True
    require_safety_warnings: bool = True


@dataclass
class ValidationResult:
    """Результат валидации контента."""

    overall_quality: QualityLevel
    overall_score: float
    is_ready_for_publication: bool

    # Детальные оценки по аспектам
    aspect_scores: Dict[ValidationAspect, float] = field(default_factory=dict)

    # Найденные проблемы
    critical_flags: List[CriticalFlag] = field(default_factory=list)
    major_issues: List[str] = field(default_factory=list)
    minor_issues: List[str] = field(default_factory=list)

    # Рекомендации
    improvement_recommendations: List[str] = field(default_factory=list)
    priority_fixes: List[str] = field(default_factory=list)

    # Метаданные
    validation_timestamp: datetime = field(default_factory=datetime.now)
    validator_version: str = "1.0.0"
    content_length: int = 0

    def get_quality_description(self) -> str:
        """Получить описание уровня качества."""
        descriptions = {
            QualityLevel.EXCELLENT: "Отличное качество - готово к публикации",
            QualityLevel.GOOD: "Хорошее качество - незначительные доработки",
            QualityLevel.NEEDS_IMPROVEMENT: "Требует улучшения - существенные правки",
            QualityLevel.UNACCEPTABLE: "Неприемлемо - полная переработка"
        }
        return descriptions.get(self.overall_quality, "Неизвестный уровень")

    def has_critical_issues(self) -> bool:
        """Проверить наличие критических проблем."""
        return len(self.critical_flags) > 0

    def get_improvement_priority(self) -> List[str]:
        """Получить приоритизированный список улучшений."""
        priority_list = []

        # Критические проблемы - высший приоритет
        for flag in self.critical_flags:
            priority_list.append(f"КРИТИЧНО: {flag.value}")

        # Приоритетные исправления
        priority_list.extend([f"ВАЖНО: {fix}" for fix in self.priority_fixes])

        # Обычные рекомендации
        priority_list.extend([f"РЕКОМЕНДУЕТСЯ: {rec}" for rec in self.improvement_recommendations])

        return priority_list


@dataclass
class NLPQualityGuardianDependencies:
    """Зависимости для NLP Content Quality Guardian Agent."""

    # Базовые настройки
    api_key: str
    validation_domain: ValidationDomain = ValidationDomain.UNIVERSAL
    target_content_type: ContentType = ContentType.MIXED_CONTENT

    # RAG и база знаний
    agent_name: str = "nlp_content_quality_guardian_agent"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "nlp-quality", "patternshift", "content-validation",
        "agent-knowledge", "pydantic-ai", "psychology-content"
    ])
    knowledge_domain: str = "quality.validation.nlp"
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Критерии валидации
    validation_criteria: ValidationCriteria = field(default_factory=ValidationCriteria)

    # Конфигурация валидации
    enable_deep_analysis: bool = True
    enable_automated_checks: bool = True
    enable_cultural_validation: bool = True
    enable_safety_scanning: bool = True

    # Языковые настройки
    primary_language: str = "ru"
    supported_languages: List[str] = field(default_factory=lambda: ["ru", "uk", "en"])
    enable_multilingual_validation: bool = True

    # Отчетность
    generate_detailed_reports: bool = True
    include_improvement_suggestions: bool = True
    include_examples_in_reports: bool = True
    export_format: str = "markdown"  # markdown, json, html

    # Интеграции
    enable_archon_integration: bool = True
    enable_knowledge_search: bool = True
    enable_pattern_matching: bool = True

    # Временные настройки
    validation_timeout_minutes: int = 10
    max_content_length: int = 100000

    # Настройки качества
    min_acceptable_score: float = 70.0
    excellence_threshold: float = 90.0
    enable_progressive_validation: bool = True

    def __post_init__(self):
        """Инициализация после создания объекта."""
        # Устанавливаем теги знаний в зависимости от домена
        domain_tags = {
            ValidationDomain.PSYCHOLOGY: ["psychology", "therapy", "mental-health"],
            ValidationDomain.ASTROLOGY: ["astrology", "cosmic", "spiritual"],
            ValidationDomain.TAROT: ["tarot", "divination", "symbolism"],
            ValidationDomain.NUMEROLOGY: ["numerology", "numbers", "sacred-geometry"],
            ValidationDomain.UNIVERSAL: ["universal", "cross-domain", "general"]
        }

        domain_specific_tags = domain_tags.get(self.validation_domain, [])
        self.knowledge_tags.extend(domain_specific_tags)

        # Устанавливаем специфичные критерии для типа контента
        if self.target_content_type == ContentType.TEST:
            self.validation_criteria.min_test_questions = 15
            self.validation_criteria.require_life_situations = True
        elif self.target_content_type == ContentType.TRANSFORMATION_PROGRAM:
            self.validation_criteria.require_three_level_structure = True
            self.validation_criteria.require_vak_personalization = True

    def get_domain_specific_requirements(self) -> Dict[str, Any]:
        """Получить специфичные требования для домена."""
        requirements = {
            ValidationDomain.PSYCHOLOGY: {
                "evidence_based": True,
                "therapeutic_ethics": True,
                "clinical_safety": True,
                "age_restrictions": True
            },
            ValidationDomain.ASTROLOGY: {
                "symbolic_accuracy": True,
                "cultural_respect": True,
                "avoid_determinism": True,
                "ethical_guidance": True
            },
            ValidationDomain.TAROT: {
                "symbolic_integrity": True,
                "interpretive_flexibility": True,
                "ethical_reading": True,
                "cultural_sensitivity": True
            },
            ValidationDomain.NUMEROLOGY: {
                "mathematical_accuracy": True,
                "symbolic_consistency": True,
                "cultural_adaptation": True,
                "balanced_interpretation": True
            },
            ValidationDomain.UNIVERSAL: {
                "cross_cultural": True,
                "domain_adaptable": True,
                "scientifically_neutral": True,
                "ethically_universal": True
            }
        }

        return requirements.get(self.validation_domain, {})

    def should_validate_aspect(self, aspect: ValidationAspect) -> bool:
        """Определить нужно ли валидировать конкретный аспект."""
        # Базовые аспекты валидируем всегда
        always_validate = {
            ValidationAspect.ETHICAL_SAFETY,
            ValidationAspect.SCIENTIFIC_VALIDITY
        }

        if aspect in always_validate:
            return True

        # Специфичные аспекты в зависимости от настроек
        conditional_aspects = {
            ValidationAspect.METHODOLOGY_COMPLIANCE: self.validation_domain != ValidationDomain.UNIVERSAL,
            ValidationAspect.CULTURAL_SENSITIVITY: self.enable_cultural_validation,
            ValidationAspect.MULTILINGUAL_QUALITY: self.enable_multilingual_validation,
            ValidationAspect.NLP_TECHNIQUE_QUALITY: self.target_content_type in [
                ContentType.NLP_TECHNIQUE, ContentType.TRANSFORMATION_PROGRAM
            ]
        }

        return conditional_aspects.get(aspect, True)

    def get_quality_thresholds(self) -> Dict[QualityLevel, float]:
        """Получить пороги качества."""
        return {
            QualityLevel.EXCELLENT: 90.0,
            QualityLevel.GOOD: 70.0,
            QualityLevel.NEEDS_IMPROVEMENT: 50.0,
            QualityLevel.UNACCEPTABLE: 0.0
        }


# Предустановленные конфигурации

def create_psychology_quality_guardian_dependencies(
    api_key: str,
    **kwargs
) -> NLPQualityGuardianDependencies:
    """Создать зависимости для валидации психологического контента."""
    return NLPQualityGuardianDependencies(
        api_key=api_key,
        validation_domain=ValidationDomain.PSYCHOLOGY,
        target_content_type=ContentType.TRANSFORMATION_PROGRAM,
        enable_deep_analysis=True,
        enable_safety_scanning=True,
        min_acceptable_score=80.0,  # Повышенные требования для психологии
        **kwargs
    )


def create_universal_quality_guardian_dependencies(
    api_key: str,
    **kwargs
) -> NLPQualityGuardianDependencies:
    """Создать универсальные зависимости для валидации любого контента."""
    return NLPQualityGuardianDependencies(
        api_key=api_key,
        validation_domain=ValidationDomain.UNIVERSAL,
        target_content_type=ContentType.MIXED_CONTENT,
        enable_cultural_validation=True,
        enable_multilingual_validation=True,
        **kwargs
    )


def create_test_quality_guardian_dependencies(
    api_key: str,
    domain: ValidationDomain = ValidationDomain.PSYCHOLOGY,
    **kwargs
) -> NLPQualityGuardianDependencies:
    """Создать зависимости для валидации тестов."""
    return NLPQualityGuardianDependencies(
        api_key=api_key,
        validation_domain=domain,
        target_content_type=ContentType.TEST,
        enable_automated_checks=True,
        **kwargs
    )


def create_nlp_technique_quality_guardian_dependencies(
    api_key: str,
    **kwargs
) -> NLPQualityGuardianDependencies:
    """Создать зависимости для валидации NLP техник."""
    return NLPQualityGuardianDependencies(
        api_key=api_key,
        validation_domain=ValidationDomain.PSYCHOLOGY,
        target_content_type=ContentType.NLP_TECHNIQUE,
        enable_deep_analysis=True,
        enable_safety_scanning=True,
        enable_pattern_matching=True,
        **kwargs
    )