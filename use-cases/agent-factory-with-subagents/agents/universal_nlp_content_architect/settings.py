"""
Settings for Universal NLP Content Architect Agent
Настройки для универсального NLP архитектора контента
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import Dict, List, Any, Literal, Optional
from dataclasses import dataclass

load_dotenv()

# Типы и константы
DomainType = Literal["psychology", "astrology", "tarot", "numerology", "coaching", "wellness", "spirituality"]
ContentType = Literal["diagnostic_test", "transformation_program", "guidance_system", "assessment_tool", "meditation_program"]
ComplexityLevel = Literal["basic", "intermediate", "advanced", "expert"]
NLPTechnique = Literal["reframing", "anchoring", "rapport", "meta_programs", "submodalities", "timeline", "parts", "beliefs"]

class UniversalNLPSettings(BaseSettings):
    """
    Настройки универсального NLP агента с поддержкой всех доменов
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Основные параметры
    domain_type: DomainType = Field(default="psychology", description="Тип домена для контента")
    content_type: ContentType = Field(default="diagnostic_test", description="Тип создаваемого контента")
    target_language: str = Field(default="ukrainian", description="Целевой язык")
    content_count: int = Field(default=16, ge=15, description="Количество элементов контента (минимум 15)")
    complexity_level: ComplexityLevel = Field(default="intermediate", description="Уровень сложности")
    transformation_days: int = Field(default=21, description="Длительность трансформационной программы")

    # NLP конфигурация
    nlp_techniques_per_element: int = Field(default=2, description="Количество NLP техник на элемент")
    ericksonian_density: str = Field(default="optimal", description="Плотность Эриксоновских паттернов")
    vak_adaptation_level: str = Field(default="full", description="Уровень VAK адаптации")

    # Языковые настройки
    age_group_adaptation: bool = Field(default=True, description="Включить адаптацию по возрасту")
    cultural_sensitivity: bool = Field(default=True, description="Учитывать культурные особенности")
    slang_integration: bool = Field(default=True, description="Интегрировать возрастной сленг")

    # Трансформационные программы
    program_structure_type: str = Field(default="three_phase", description="Тип структуры программы")
    daily_exercises_count: int = Field(default=2, description="Количество упражнений в день")
    multiformat_support: bool = Field(default=True, description="Поддержка мультиформатного контента")

    # Качество и безопасность
    safety_checks_enabled: bool = Field(default=True, description="Включить проверки безопасности")
    ethical_guidelines_strict: bool = Field(default=True, description="Строгие этические рамки")
    domain_expertise_validation: bool = Field(default=True, description="Валидация экспертизы домена")

    def get_language_tone(self) -> str:
        """Получить тон языка на основе настроек"""
        tone_mapping = {
            "ukrainian": "warm_emotional",
            "russian": "literary_deep",
            "english": "professional_accessible"
        }
        return tone_mapping.get(self.target_language, "neutral")

    def get_domain_techniques(self, domain: str) -> List[str]:
        """Получить техники специфичные для домена"""
        domain_techniques = {
            "psychology": ["cognitive_reframing", "emotional_regulation", "behavioral_modification", "insight_development"],
            "astrology": ["symbolic_interpretation", "archetypal_analysis", "energy_reading", "cycle_understanding"],
            "tarot": ["intuitive_reading", "symbolic_analysis", "archetypal_guidance", "pattern_recognition"],
            "numerology": ["numerical_analysis", "pattern_calculation", "life_path_reading", "compatibility_analysis"],
            "coaching": ["goal_setting", "action_planning", "obstacle_overcoming", "success_modeling"],
            "wellness": ["mindfulness_techniques", "stress_reduction", "energy_balancing", "holistic_healing"]
        }
        return domain_techniques.get(domain, domain_techniques["psychology"])

    def get_nlp_techniques(self) -> List[str]:
        """Получить список NLP техник для текущей конфигурации"""
        base_techniques = ["reframing", "anchoring", "rapport_building", "presuppositions"]

        if self.complexity_level == "advanced":
            base_techniques.extend(["meta_programs", "submodalities", "timeline_work", "parts_integration"])
        elif self.complexity_level == "expert":
            base_techniques.extend(["belief_change", "strategy_modeling", "deep_trance_work", "generative_change"])

        return base_techniques

    def get_ericksonian_patterns(self) -> List[str]:
        """Получить Эриксоновские паттерны для текущего уровня"""
        base_patterns = ["truisms", "presuppositions", "embedded_commands", "indirect_suggestions"]

        if self.ericksonian_density == "maximum":
            base_patterns.extend(["therapeutic_metaphors", "confusion_technique", "double_binds", "utilization_principle"])
        elif self.ericksonian_density == "optimal":
            base_patterns.extend(["therapeutic_metaphors", "utilization_principle"])

        return base_patterns

    def get_vak_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Получить шаблоны VAK адаптаций"""
        return {
            "visual": {
                "psychology": ["ясность мыслей", "светлые перспективы", "видеть решения"],
                "astrology": ["звездная карта", "космические образы", "планетарные цвета"],
                "tarot": ["символические картины", "образы карт", "визуальные архетипы"],
                "numerology": ["числовые паттерны", "математические образы", "цифровая карта"],
                "coaching": ["визуализация целей", "четкие планы", "яркое будущее"],
                "wellness": ["внутренний свет", "образы природы", "визуальный покой"]
            },
            "auditory": {
                "psychology": ["внутренний голос", "гармония мыслей", "резонанс решений"],
                "astrology": ["музыка сфер", "планетарные вибрации", "зов судьбы"],
                "tarot": ["голос интуиции", "шепот карт", "звуки мудрости"],
                "numerology": ["ритм чисел", "математическая мелодия", "звуки расчетов"],
                "coaching": ["призыв к действию", "эхо успеха", "мотивационные ритмы"],
                "wellness": ["звуки природы", "внутренняя тишина", "дыхательные ритмы"]
            },
            "kinesthetic": {
                "psychology": ["эмоциональное тепло", "легкость бытия", "поток осознания"],
                "astrology": ["энергетические потоки", "планетарные влияния", "космические вибрации"],
                "tarot": ["энергия карт", "тактильная связь", "ощущение истины"],
                "numerology": ["вес чисел", "давление фактов", "поток расчетов"],
                "coaching": ["движение к цели", "сила мотивации", "импульс роста"],
                "wellness": ["телесные ощущения", "энергетический баланс", "физический покой"]
            }
        }

    def get_age_adaptations(self) -> Dict[str, Dict[str, Any]]:
        """Получить адаптации по возрасту"""
        return {
            "youth": {
                "tone": "energetic_modern",
                "nlp_style": "dynamic_metaphors",
                "examples": ["gaming", "social_media", "trends"],
                "language_pattern": "informal_friendly"
            },
            "adult": {
                "tone": "practical_supportive",
                "nlp_style": "balanced_approach",
                "examples": ["work_life", "relationships", "goals"],
                "language_pattern": "conversational"
            },
            "mature": {
                "tone": "wise_respectful",
                "nlp_style": "deep_metaphors",
                "examples": ["experience", "wisdom", "legacy"],
                "language_pattern": "respectful_formal"
            }
        }

    def get_transformation_structure(self) -> Dict[str, Any]:
        """Получить структуру трансформационной программы"""
        structures = {
            "three_phase": {
                "phases": [
                    {"name": "destabilization", "days": 7, "focus": "breaking_patterns"},
                    {"name": "transformation", "days": 7, "focus": "new_patterns"},
                    {"name": "integration", "days": 7, "focus": "stabilization"}
                ],
                "total_days": 21
            },
            "gradual_change": {
                "phases": [
                    {"name": "assessment", "days": 5, "focus": "current_state"},
                    {"name": "gradual_improvement", "days": 11, "focus": "step_by_step"},
                    {"name": "maintenance", "days": 5, "focus": "habit_formation"}
                ],
                "total_days": 21
            },
            "skill_building": {
                "phases": [
                    {"name": "learning", "days": 7, "focus": "technique_acquisition"},
                    {"name": "mastery", "days": 7, "focus": "advanced_application"}
                ],
                "total_days": 14
            }
        }
        return structures.get(self.program_structure_type, structures["three_phase"])

    def get_safety_guidelines(self) -> Dict[str, List[str]]:
        """Получить рекомендации по безопасности для домена"""
        return {
            "psychology": [
                "avoid_clinical_diagnoses",
                "focus_on_resources",
                "provide_professional_referrals",
                "maintain_ethical_boundaries"
            ],
            "astrology": [
                "avoid_fatalistic_predictions",
                "encourage_free_will",
                "provide_empowering_interpretations",
                "respect_cultural_beliefs"
            ],
            "tarot": [
                "avoid_absolute_predictions",
                "encourage_personal_agency",
                "respect_client_boundaries",
                "provide_supportive_guidance"
            ],
            "numerology": [
                "explain_calculation_methods",
                "provide_balanced_interpretations",
                "acknowledge_system_limitations",
                "respect_individual_uniqueness"
            ],
            "coaching": [
                "maintain_professional_boundaries",
                "stay_within_coaching_scope",
                "provide_clear_agreements",
                "focus_on_client_goals"
            ],
            "wellness": [
                "respect_physical_limitations",
                "provide_modification_options",
                "encourage_professional_guidance",
                "avoid_medical_claims"
            ]
        }

    def get_quality_criteria(self) -> Dict[str, float]:
        """Получить критерии качества для оценки"""
        return {
            "nlp_integration_score": 0.85,
            "domain_accuracy_score": 0.90,
            "vak_completeness_score": 0.80,
            "ericksonian_naturalness_score": 0.88,
            "safety_compliance_score": 0.95,
            "user_engagement_score": 0.82,
            "transformation_effectiveness_score": 0.87
        }

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать настройки в словарь"""
        return {
            "domain_type": self.domain_type,
            "content_type": self.content_type,
            "target_language": self.target_language,
            "content_count": self.content_count,
            "complexity_level": self.complexity_level,
            "transformation_days": self.transformation_days,
            "nlp_techniques": self.get_nlp_techniques(),
            "ericksonian_patterns": self.get_ericksonian_patterns(),
            "language_tone": self.get_language_tone(),
            "safety_guidelines": self.get_safety_guidelines().get(self.domain_type, []),
            "quality_criteria": self.get_quality_criteria()
        }

@dataclass
class DomainConfiguration:
    """Конфигурация для конкретного домена"""

    domain_type: str
    approach: str  # scientific, symbolic, intuitive, analytical, transformational, holistic
    safety_level: str  # high, medium, standard
    ethical_framework: str
    evidence_requirements: str
    cultural_sensitivity: bool
    age_restrictions: Optional[Dict[str, int]] = None

    def get_nlp_adaptation_style(self) -> str:
        """Получить стиль адаптации NLP для домена"""
        styles = {
            "psychology": "therapeutic_scientific",
            "astrology": "symbolic_metaphorical",
            "tarot": "intuitive_archetypal",
            "numerology": "analytical_systematic",
            "coaching": "goal_oriented_practical",
            "wellness": "holistic_natural"
        }
        return styles.get(self.domain_type, "universal_adaptive")

# Предустановленные конфигурации доменов
DOMAIN_CONFIGURATIONS = {
    "psychology": DomainConfiguration(
        domain_type="psychology",
        approach="scientific",
        safety_level="high",
        ethical_framework="therapeutic_ethics",
        evidence_requirements="research_based",
        cultural_sensitivity=True,
        age_restrictions={"min_age": 16, "max_age": 80}
    ),
    "astrology": DomainConfiguration(
        domain_type="astrology",
        approach="symbolic",
        safety_level="medium",
        ethical_framework="empowerment_ethics",
        evidence_requirements="traditional_knowledge",
        cultural_sensitivity=True
    ),
    "tarot": DomainConfiguration(
        domain_type="tarot",
        approach="intuitive",
        safety_level="medium",
        ethical_framework="guidance_ethics",
        evidence_requirements="symbolic_wisdom",
        cultural_sensitivity=True
    ),
    "numerology": DomainConfiguration(
        domain_type="numerology",
        approach="analytical",
        safety_level="standard",
        ethical_framework="transparency_ethics",
        evidence_requirements="mathematical_accuracy",
        cultural_sensitivity=True
    ),
    "coaching": DomainConfiguration(
        domain_type="coaching",
        approach="transformational",
        safety_level="high",
        ethical_framework="coaching_ethics",
        evidence_requirements="practical_results",
        cultural_sensitivity=True
    ),
    "wellness": DomainConfiguration(
        domain_type="wellness",
        approach="holistic",
        safety_level="high",
        ethical_framework="wellness_ethics",
        evidence_requirements="safety_first",
        cultural_sensitivity=True,
        age_restrictions={"min_age": 12, "max_age": 99}
    )
}

def get_domain_configuration(domain_type: str) -> DomainConfiguration:
    """Получить конфигурацию для домена"""
    return DOMAIN_CONFIGURATIONS.get(domain_type, DOMAIN_CONFIGURATIONS["psychology"])

def create_universal_nlp_settings(
    domain_type: str = "psychology",
    content_type: str = "diagnostic_test",
    target_language: str = "ukrainian",
    complexity_level: str = "intermediate"
) -> UniversalNLPSettings:
    """Создать настройки для универсального NLP агента"""

    return UniversalNLPSettings(
        domain_type=domain_type,
        content_type=content_type,
        target_language=target_language,
        complexity_level=complexity_level
    )