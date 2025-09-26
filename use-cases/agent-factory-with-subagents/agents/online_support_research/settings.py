"""
Settings для Psychology Research Agent
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchDomain(Enum):
    """Домены психологических исследований"""
    GENERAL = "general"
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    TRAUMA = "trauma"
    RELATIONSHIPS = "relationships"
    ADDICTION = "addiction"
    PERSONALITY = "personality"
    EATING_DISORDERS = "eating_disorders"
    STRESS = "stress"
    GRIEF = "grief"
    PARENTING = "parenting"

class TargetPopulation(Enum):
    """Целевые популяции"""
    ADULTS = "adults"
    ADOLESCENTS = "adolescents"
    CHILDREN = "children"
    ELDERLY = "elderly"
    COUPLES = "couples"
    FAMILIES = "families"
    GROUPS = "groups"

class EvidenceStandard(Enum):
    """Стандарты доказательности"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    EXPERT = "expert"

class ResearchQuestionType(Enum):
    """Типы исследовательских вопросов"""
    EFFECTIVENESS = "effectiveness"
    SAFETY = "safety"
    COMPARISON = "comparison"
    MECHANISM = "mechanism"
    POPULATION = "population"

class StudyType(Enum):
    """Типы исследований"""
    RCT = "rct"
    META_ANALYSIS = "meta-analysis"
    SYSTEMATIC_REVIEW = "systematic-review"
    COHORT = "cohort"
    CASE_CONTROL = "case-control"
    CROSS_SECTIONAL = "cross-sectional"
    QUALITATIVE = "qualitative"

@dataclass
class ResearchSettings:
    """Настройки для исследователя психологических методик"""

    # Основные параметры исследования
    research_domain: str = ResearchDomain.GENERAL.value
    target_population: str = TargetPopulation.ADULTS.value
    evidence_standard: str = EvidenceStandard.MODERATE.value
    research_question_type: str = ResearchQuestionType.EFFECTIVENESS.value

    # Параметры поиска литературы
    databases: List[str] = field(default_factory=lambda: ["pubmed", "psycinfo", "cochrane"])
    years_range: str = "2010-2024"
    languages: List[str] = field(default_factory=lambda: ["en", "ru"])
    study_types: List[str] = field(default_factory=lambda: ["rct", "meta-analysis", "systematic-review"])
    max_results: int = 50

    # Критерии качества исследований
    minimum_sample_size: int = 30
    require_control_group: bool = True
    require_randomization: bool = True
    require_blinding: bool = False
    maximum_dropout_rate: float = 0.3
    require_intention_to_treat: bool = True

    # Статистические параметры
    alpha_level: float = 0.05
    power: float = 0.80
    effect_size_threshold: float = 0.2
    heterogeneity_threshold: float = 0.75
    publication_bias_tests: List[str] = field(default_factory=lambda: ["egger", "begg"])

    # Настройки клинической значимости
    mcid_threshold: float = 0.3  # Минимальная клинически важная разность
    nnt_calculation: bool = True  # Расчет числа пациентов для лечения
    cost_effectiveness_analysis: bool = False

    # Параметры безопасности
    safety_monitoring: bool = True
    crisis_protocols: bool = True
    adverse_events_tracking: bool = True
    special_populations_safety: bool = True

    # Временные ограничения
    search_timeout_seconds: int = 120
    analysis_timeout_minutes: int = 30
    max_concurrent_searches: int = 3

    # Интеграция с системой
    enable_rag_integration: bool = True
    enable_archon_integration: bool = True
    enable_web_search: bool = True
    save_intermediate_results: bool = True

    # Настройки отчетности
    report_format: str = "structured"  # structured, narrative, tabular
    include_forest_plots: bool = True
    include_risk_tables: bool = True
    include_grade_assessment: bool = True

    def __post_init__(self):
        """Пост-инициализация и валидация настроек"""
        self._validate_settings()
        self._adjust_for_domain()
        self._adjust_for_population()
        self._adjust_for_evidence_standard()

    def _validate_settings(self):
        """Валидация настроек"""
        # Валидация временных диапазонов
        if not self._is_valid_year_range(self.years_range):
            self.years_range = "2010-2024"

        # Валидация статистических параметров
        if not 0 < self.alpha_level < 1:
            self.alpha_level = 0.05

        if not 0 < self.power < 1:
            self.power = 0.80

        # Валидация размера выборки
        if self.minimum_sample_size < 10:
            self.minimum_sample_size = 30

        # Валидация dropout rate
        if not 0 <= self.maximum_dropout_rate <= 1:
            self.maximum_dropout_rate = 0.3

        # Валидация баз данных
        valid_databases = ["pubmed", "psycinfo", "cochrane", "embase", "web_of_science"]
        self.databases = [db for db in self.databases if db in valid_databases]
        if not self.databases:
            self.databases = ["pubmed", "psycinfo"]

    def _adjust_for_domain(self):
        """Настройка параметров под конкретный домен"""
        domain_adjustments = {
            "anxiety": {
                "effect_size_threshold": 0.3,
                "crisis_protocols": True,
                "include_panic_measures": True
            },
            "depression": {
                "effect_size_threshold": 0.35,
                "crisis_protocols": True,
                "require_suicide_screening": True,
                "minimum_sample_size": 40
            },
            "trauma": {
                "effect_size_threshold": 0.4,
                "crisis_protocols": True,
                "special_populations_safety": True,
                "require_trauma_informed_care": True,
                "minimum_sample_size": 50
            },
            "relationships": {
                "effect_size_threshold": 0.25,
                "target_population": "couples",
                "session_length_considerations": True
            },
            "addiction": {
                "effect_size_threshold": 0.3,
                "relapse_prevention_focus": True,
                "harm_reduction_considerations": True
            }
        }

        if self.research_domain in domain_adjustments:
            adjustments = domain_adjustments[self.research_domain]
            for key, value in adjustments.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def _adjust_for_population(self):
        """Настройка параметров под целевую популяцию"""
        population_adjustments = {
            "children": {
                "minimum_sample_size": 20,
                "require_parental_consent": True,
                "developmental_considerations": True,
                "session_length_limit": 45
            },
            "adolescents": {
                "minimum_sample_size": 25,
                "crisis_protocols": True,
                "suicide_risk_monitoring": True,
                "developmental_considerations": True
            },
            "elderly": {
                "minimum_sample_size": 25,
                "cognitive_screening": True,
                "medical_comorbidity_tracking": True,
                "medication_interactions": True
            },
            "couples": {
                "minimum_sample_size": 15,  # пар
                "relationship_measures": True,
                "dyadic_analysis": True
            }
        }

        if self.target_population in population_adjustments:
            adjustments = population_adjustments[self.target_population]
            for key, value in adjustments.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def _adjust_for_evidence_standard(self):
        """Настройка параметров под стандарт доказательности"""
        standard_adjustments = {
            "low": {
                "minimum_sample_size": 20,
                "require_control_group": False,
                "require_randomization": False,
                "require_blinding": False,
                "study_types": ["rct", "cohort", "case-control"],
                "maximum_dropout_rate": 0.4
            },
            "moderate": {
                "minimum_sample_size": 30,
                "require_control_group": True,
                "require_randomization": True,
                "require_blinding": False,
                "study_types": ["rct", "meta-analysis", "systematic-review"]
            },
            "high": {
                "minimum_sample_size": 50,
                "require_control_group": True,
                "require_randomization": True,
                "require_blinding": True,
                "require_intention_to_treat": True,
                "study_types": ["rct", "meta-analysis"],
                "maximum_dropout_rate": 0.2
            },
            "expert": {
                "minimum_sample_size": 100,
                "require_control_group": True,
                "require_randomization": True,
                "require_blinding": True,
                "require_intention_to_treat": True,
                "study_types": ["meta-analysis", "systematic-review"],
                "maximum_dropout_rate": 0.15,
                "require_multiple_sites": True
            }
        }

        if self.evidence_standard in standard_adjustments:
            adjustments = standard_adjustments[self.evidence_standard]
            for key, value in adjustments.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def _is_valid_year_range(self, year_range: str) -> bool:
        """Проверка валидности диапазона лет"""
        try:
            if "-" in year_range:
                start, end = year_range.split("-")
                start_year = int(start.strip())
                end_year = int(end.strip())
                return 1990 <= start_year <= end_year <= 2024
            else:
                year = int(year_range.strip())
                return 1990 <= year <= 2024
        except (ValueError, AttributeError):
            return False

    def get_search_parameters(self) -> Dict[str, Any]:
        """Получить параметры поиска для литературного обзора"""
        return {
            "databases": self.databases,
            "years": self.years_range,
            "languages": self.languages,
            "study_types": self.study_types,
            "max_results": self.max_results,
            "timeout_seconds": self.search_timeout_seconds
        }

    def get_quality_criteria(self) -> Dict[str, Any]:
        """Получить критерии качества исследований"""
        return {
            "minimum_sample_size": self.minimum_sample_size,
            "require_control_group": self.require_control_group,
            "require_randomization": self.require_randomization,
            "require_blinding": self.require_blinding,
            "maximum_dropout_rate": self.maximum_dropout_rate,
            "require_intention_to_treat": self.require_intention_to_treat
        }

    def get_statistical_parameters(self) -> Dict[str, Any]:
        """Получить статистические параметры анализа"""
        return {
            "alpha_level": self.alpha_level,
            "power": self.power,
            "effect_size_threshold": self.effect_size_threshold,
            "heterogeneity_threshold": self.heterogeneity_threshold,
            "publication_bias_tests": self.publication_bias_tests
        }

    def get_safety_requirements(self) -> Dict[str, bool]:
        """Получить требования к безопасности"""
        return {
            "safety_monitoring": self.safety_monitoring,
            "crisis_protocols": self.crisis_protocols,
            "adverse_events_tracking": self.adverse_events_tracking,
            "special_populations_safety": self.special_populations_safety
        }

    def is_compatible_with(self, other: 'ResearchSettings') -> bool:
        """Проверить совместимость с другими настройками"""
        compatibility_factors = [
            self.research_domain == other.research_domain,
            self.target_population == other.target_population,
            self.evidence_standard == other.evidence_standard,
            abs(self.minimum_sample_size - other.minimum_sample_size) <= 20
        ]
        return sum(compatibility_factors) >= 3

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        return {
            "research_domain": self.research_domain,
            "target_population": self.target_population,
            "evidence_standard": self.evidence_standard,
            "research_question_type": self.research_question_type,
            "search_parameters": self.get_search_parameters(),
            "quality_criteria": self.get_quality_criteria(),
            "statistical_parameters": self.get_statistical_parameters(),
            "safety_requirements": self.get_safety_requirements()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResearchSettings':
        """Создание из словаря"""
        # Извлекаем основные параметры
        settings = cls(
            research_domain=data.get("research_domain", "general"),
            target_population=data.get("target_population", "adults"),
            evidence_standard=data.get("evidence_standard", "moderate"),
            research_question_type=data.get("research_question_type", "effectiveness")
        )

        # Обновляем дополнительные параметры если они есть
        search_params = data.get("search_parameters", {})
        for key, value in search_params.items():
            if hasattr(settings, key):
                setattr(settings, key, value)

        return settings

# Предустановленные конфигурации для различных типов исследований
RESEARCH_PRESETS = {
    "anxiety_adults_high": ResearchSettings(
        research_domain="anxiety",
        target_population="adults",
        evidence_standard="high",
        research_question_type="effectiveness",
        minimum_sample_size=50,
        crisis_protocols=True
    ),

    "depression_adolescents": ResearchSettings(
        research_domain="depression",
        target_population="adolescents",
        evidence_standard="moderate",
        research_question_type="effectiveness",
        minimum_sample_size=25,
        crisis_protocols=True,
        special_populations_safety=True
    ),

    "trauma_expert_review": ResearchSettings(
        research_domain="trauma",
        target_population="adults",
        evidence_standard="expert",
        research_question_type="effectiveness",
        study_types=["meta-analysis", "systematic-review"],
        minimum_sample_size=100,
        crisis_protocols=True
    ),

    "couples_therapy": ResearchSettings(
        research_domain="relationships",
        target_population="couples",
        evidence_standard="moderate",
        research_question_type="effectiveness",
        minimum_sample_size=15
    ),

    "safety_assessment": ResearchSettings(
        research_domain="general",
        target_population="adults",
        evidence_standard="moderate",
        research_question_type="safety",
        safety_monitoring=True,
        adverse_events_tracking=True
    )
}

def get_research_preset(preset_name: str) -> Optional[ResearchSettings]:
    """Получить предустановленную конфигурацию исследования"""
    return RESEARCH_PRESETS.get(preset_name)

def list_available_presets() -> List[str]:
    """Список доступных предустановок"""
    return list(RESEARCH_PRESETS.keys())

def get_preset_info() -> Dict[str, str]:
    """Информация о доступных предустановках"""
    return {
        "anxiety_adults_high": "Высококачественные исследования тревожности у взрослых",
        "depression_adolescents": "Исследования депрессии у подростков с усиленной безопасностью",
        "trauma_expert_review": "Экспертный обзор травма-терапии (только мета-анализы)",
        "couples_therapy": "Исследования парной и семейной терапии",
        "safety_assessment": "Оценка безопасности психологических интервенций"
    }

def create_domain_specific_settings(
    domain: str,
    population: str = "adults",
    evidence_level: str = "moderate"
) -> ResearchSettings:
    """Создать настройки, оптимизированные для конкретного домена"""

    settings = ResearchSettings(
        research_domain=domain,
        target_population=population,
        evidence_standard=evidence_level
    )

    # Дополнительные настройки по доменам
    domain_optimizations = {
        "anxiety": {
            "databases": ["pubmed", "psycinfo", "cochrane"],
            "study_types": ["rct", "meta-analysis", "systematic-review"],
            "effect_size_threshold": 0.3,
            "crisis_protocols": True
        },
        "depression": {
            "databases": ["pubmed", "psycinfo", "cochrane", "embase"],
            "study_types": ["rct", "meta-analysis"],
            "effect_size_threshold": 0.35,
            "crisis_protocols": True,
            "minimum_sample_size": 40
        },
        "trauma": {
            "databases": ["pubmed", "psycinfo", "cochrane"],
            "study_types": ["rct", "meta-analysis"],
            "effect_size_threshold": 0.4,
            "crisis_protocols": True,
            "special_populations_safety": True,
            "minimum_sample_size": 50
        }
    }

    if domain in domain_optimizations:
        optimizations = domain_optimizations[domain]
        for key, value in optimizations.items():
            if hasattr(settings, key):
                setattr(settings, key, value)

    return settings