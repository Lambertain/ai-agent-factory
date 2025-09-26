"""
Система зависимостей для Psychology Research Agent

Универсальная система управления зависимостями с поддержкой различных
типов исследований и интеграцией с Archon Knowledge Base.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from pathlib import Path

from .settings import PsychologyResearchAgentSettings, load_settings
from .providers import get_model_provider, ResearchModelProvider


@dataclass
class ResearchAgentDependencies:
    """
    Зависимости для Psychology Research Agent.

    Универсальная система зависимостей поддерживающая различные домены
    исследований и типы валидации.
    """

    # ===== ОСНОВНЫЕ НАСТРОЙКИ =====
    api_key: str
    project_path: str = ""

    # ===== АГЕНТ И ДОМЕН =====
    agent_name: str = "psychology_research_agent"
    research_domain: str = "general"  # clinical, cognitive, social, developmental, educational
    target_population: str = "adults"  # adults, children, adolescents, elderly, clinical
    methodology_focus: str = "quantitative"  # quantitative, qualitative, mixed_methods

    # ===== УРОВЕНЬ ВАЛИДАЦИИ =====
    validation_level: str = "standard"  # basic, standard, rigorous, publication_grade

    # Требования к качеству исследований
    min_sample_size: int = 30
    min_effect_size: float = 0.2
    min_power: float = 0.8
    alpha_level: float = 0.05
    min_reliability: float = 0.7
    min_validity_coefficient: float = 0.3

    # ===== СТАНДАРТЫ СООТВЕТСТВИЯ =====
    reporting_standards: List[str] = field(
        default_factory=lambda: ["CONSORT", "STROBE", "PRISMA"]
    )
    ethics_standards: List[str] = field(
        default_factory=lambda: ["APA_Ethics", "Declaration_of_Helsinki"]
    )
    statistical_standards: List[str] = field(
        default_factory=lambda: ["APA_Style", "CONSORT_Statistical"]
    )

    # ===== RAG И БАЗА ЗНАНИЙ =====
    knowledge_tags: List[str] = field(
        default_factory=lambda: ["psychology_research", "methodology", "statistics", "agent-knowledge"]
    )
    knowledge_domain: Optional[str] = "psychology.research"
    literature_search_databases: List[str] = field(
        default_factory=lambda: ["PubMed", "PsycINFO", "Cochrane", "Web_of_Science"]
    )

    # ===== ARCHON ИНТЕГРАЦИЯ =====
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"  # AI Agent Factory
    archon_enabled: bool = True

    # ===== ПРОИЗВОДИТЕЛЬНОСТЬ =====
    batch_size_studies: int = 10
    batch_size_literature: int = 50
    analysis_timeout: int = 300
    search_timeout: int = 60
    enable_caching: bool = True
    cache_duration: int = 3600

    # ===== ОТЧЕТНОСТЬ =====
    report_format: str = "comprehensive"  # brief, standard, comprehensive
    report_language: str = "ru"  # ru, en
    citation_style: str = "APA"  # APA, AMA, Vancouver
    include_recommendations: bool = True
    include_literature_citations: bool = True

    # ===== НАСТРОЙКИ МОДЕЛЕЙ =====
    model_provider: Optional[ResearchModelProvider] = field(default=None, init=False)

    # ===== СПЕЦИФИЧНЫЕ ТРЕБОВАНИЯ ПО ДОМЕНАМ =====
    domain_specific_requirements: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Пост-инициализация зависимостей."""
        # Инициализация провайдера моделей
        self.model_provider = get_model_provider()

        # Настройка доменных требований
        self._setup_domain_requirements()

        # Настройка тегов для поиска знаний
        self._setup_knowledge_tags()

    def _setup_domain_requirements(self):
        """Настроить требования специфичные для домена."""

        if self.research_domain == "clinical":
            self.domain_specific_requirements = {
                "min_sample_size": max(self.min_sample_size, 100),
                "control_group_required": True,
                "randomization_required": True,
                "blinding_preferred": True,
                "ethical_approval_required": True,
                "adverse_events_monitoring": True,
                "followup_period_required": True,
                "intention_to_treat_analysis": True
            }

        elif self.research_domain == "cognitive":
            self.domain_specific_requirements = {
                "min_sample_size": max(self.min_sample_size, 30),
                "reaction_time_outliers": "3SD",
                "counterbalancing_required": True,
                "practice_trials_required": True,
                "ceiling_floor_threshold": 0.15,
                "experimental_control_required": True,
                "repeated_measures_ok": True
            }

        elif self.research_domain == "social":
            self.domain_specific_requirements = {
                "min_sample_size": max(self.min_sample_size, 50),
                "cultural_diversity_required": True,
                "social_desirability_control": True,
                "demand_characteristics_minimized": True,
                "ecological_validity_considered": True,
                "replication_encouraged": True,
                "effect_size_reporting": True
            }

        elif self.research_domain == "developmental":
            self.domain_specific_requirements = {
                "min_sample_size": max(self.min_sample_size, 40),
                "age_appropriate_measures": True,
                "parental_consent_required": True,
                "child_assent_when_appropriate": True,
                "developmental_considerations": True,
                "longitudinal_design_preferred": True,
                "attrition_analysis_required": True
            }

        elif self.research_domain == "educational":
            self.domain_specific_requirements = {
                "min_sample_size": max(self.min_sample_size, 60),
                "classroom_clustering_considered": True,
                "teacher_training_documented": True,
                "implementation_fidelity_checked": True,
                "educational_relevance_established": True,
                "practical_significance_reported": True
            }

    def _setup_knowledge_tags(self):
        """Настроить теги для поиска в базе знаний."""
        base_tags = ["psychology_research", "agent-knowledge", "pydantic-ai"]

        # Добавляем доменные теги
        if self.research_domain != "general":
            base_tags.append(f"{self.research_domain}_psychology")

        # Добавляем методологические теги
        if self.methodology_focus != "quantitative":
            base_tags.append(self.methodology_focus)

        # Добавляем популяционные теги
        if self.target_population != "adults":
            base_tags.append(f"{self.target_population}_population")

        self.knowledge_tags = base_tags

    def get_model_for_task(
        self,
        task_type: str,
        complexity: str = "standard"
    ) -> Any:
        """
        Получить модель для конкретной задачи.

        Args:
            task_type: Тип задачи
            complexity: Сложность задачи

        Returns:
            Модель LLM
        """
        if not self.model_provider:
            raise ValueError("Model provider не инициализирован")

        return self.model_provider.get_model_for_task(
            task_type=task_type,
            research_domain=self.research_domain,
            complexity=complexity
        )

    def get_validation_criteria(self) -> Dict[str, Any]:
        """
        Получить критерии валидации для текущей конфигурации.

        Returns:
            Словарь с критериями валидации
        """
        base_criteria = {
            "sample_size": self.min_sample_size,
            "effect_size": self.min_effect_size,
            "statistical_power": self.min_power,
            "alpha_level": self.alpha_level,
            "reliability": self.min_reliability,
            "validity": self.min_validity_coefficient,
            "reporting_standards": self.reporting_standards,
            "ethics_standards": self.ethics_standards
        }

        # Добавляем доменные требования
        base_criteria.update(self.domain_specific_requirements)

        return base_criteria

    def get_literature_search_strategy(self) -> Dict[str, Any]:
        """
        Получить стратегию поиска литературы.

        Returns:
            Стратегия поиска литературы
        """
        return {
            "databases": self.literature_search_databases,
            "domain_keywords": self._get_domain_keywords(),
            "search_filters": self._get_search_filters(),
            "inclusion_criteria": self._get_inclusion_criteria(),
            "quality_thresholds": self._get_quality_thresholds()
        }

    def _get_domain_keywords(self) -> List[str]:
        """Получить ключевые слова для домена."""
        domain_keywords = {
            "clinical": [
                "clinical psychology", "psychotherapy", "treatment", "intervention",
                "randomized controlled trial", "efficacy", "effectiveness"
            ],
            "cognitive": [
                "cognitive psychology", "experimental psychology", "attention",
                "memory", "perception", "cognition", "reaction time"
            ],
            "social": [
                "social psychology", "social cognition", "attitudes", "behavior",
                "interpersonal", "group dynamics", "cultural psychology"
            ],
            "developmental": [
                "developmental psychology", "child development", "adolescent",
                "lifespan", "longitudinal", "age differences"
            ],
            "educational": [
                "educational psychology", "learning", "academic achievement",
                "classroom", "pedagogy", "instruction", "assessment"
            ]
        }

        return domain_keywords.get(self.research_domain, ["psychology", "research"])

    def _get_search_filters(self) -> Dict[str, Any]:
        """Получить фильтры поиска."""
        return {
            "publication_types": ["journal article", "review", "meta-analysis"],
            "languages": ["english", "russian"] if self.report_language == "ru" else ["english"],
            "date_range": "last_10_years",
            "study_designs": self._get_preferred_study_designs(),
            "population": self.target_population
        }

    def _get_preferred_study_designs(self) -> List[str]:
        """Получить предпочтительные дизайны исследований."""
        if self.research_domain == "clinical":
            return ["randomized controlled trial", "controlled trial", "cohort study"]
        elif self.research_domain == "cognitive":
            return ["experimental study", "controlled experiment", "factorial design"]
        elif self.research_domain == "social":
            return ["experimental study", "correlational study", "field study"]
        elif self.research_domain == "developmental":
            return ["longitudinal study", "cross-sectional study", "cohort study"]
        elif self.research_domain == "educational":
            return ["educational intervention", "quasi-experimental", "mixed methods"]
        else:
            return ["experimental study", "correlational study", "review"]

    def _get_inclusion_criteria(self) -> Dict[str, Any]:
        """Получить критерии включения исследований."""
        return {
            "peer_reviewed": True,
            "empirical_data": True,
            "adequate_sample_size": self.min_sample_size,
            "clear_methodology": True,
            "appropriate_statistics": True,
            "ethical_compliance": True
        }

    def _get_quality_thresholds(self) -> Dict[str, float]:
        """Получить пороги качества исследований."""
        return {
            "min_impact_factor": 0.5 if self.validation_level == "basic" else 1.0,
            "min_citation_count": 5 if self.validation_level == "basic" else 10,
            "min_study_quality_score": 6.0 if self.validation_level == "rigorous" else 4.0,
            "min_effect_size_precision": 0.1,
            "max_risk_of_bias": 0.3 if self.validation_level == "rigorous" else 0.5
        }

    def should_delegate_task(self, task_keywords: List[str]) -> Optional[str]:
        """
        Определить нужно ли делегировать задачу другому агенту.

        Args:
            task_keywords: Ключевые слова задачи

        Returns:
            Имя агента для делегирования или None
        """
        # Определяем компетенции других агентов
        security_keywords = ['безопасность', 'security', 'уязвимости', 'privacy', 'data protection']
        ui_keywords = ['интерфейс', 'ui', 'ux', 'дизайн', 'пользователь', 'accessibility']
        performance_keywords = ['производительность', 'performance', 'optimization', 'speed']
        quality_keywords = ['качество', 'quality', 'testing', 'validation', 'review']

        keywords_lower = [kw.lower() for kw in task_keywords]

        # Проверяем пересечения
        if any(kw in keywords_lower for kw in security_keywords):
            return "security_audit_agent"
        elif any(kw in keywords_lower for kw in ui_keywords):
            return "uiux_enhancement_agent"
        elif any(kw in keywords_lower for kw in performance_keywords):
            return "performance_optimization_agent"
        elif any(kw in keywords_lower for kw in quality_keywords) and "research" not in keywords_lower:
            return "quality_guardian_agent"

        return None

    def get_cost_estimate(self, task_type: str, content_length: int) -> Dict[str, Any]:
        """
        Получить оценку стоимости задачи.

        Args:
            task_type: Тип задачи
            content_length: Длина контента

        Returns:
            Оценка стоимости
        """
        if not self.model_provider:
            return {"error": "Model provider не инициализирован"}

        return self.model_provider.estimate_cost(
            task_type=task_type,
            content_length=content_length,
            research_domain=self.research_domain,
            complexity=self.validation_level
        )

    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать зависимости в словарь."""
        return {
            "agent_name": self.agent_name,
            "research_domain": self.research_domain,
            "target_population": self.target_population,
            "methodology_focus": self.methodology_focus,
            "validation_level": self.validation_level,
            "validation_criteria": self.get_validation_criteria(),
            "knowledge_tags": self.knowledge_tags,
            "domain_requirements": self.domain_specific_requirements,
            "archon_project_id": self.archon_project_id
        }


def create_clinical_dependencies(
    api_key: str,
    target_population: str = "clinical",
    validation_level: str = "rigorous",
    **kwargs
) -> ResearchAgentDependencies:
    """
    Создать зависимости для клинических исследований.

    Args:
        api_key: API ключ провайдера
        target_population: Целевая популяция
        validation_level: Уровень валидации
        **kwargs: Дополнительные параметры

    Returns:
        Зависимости для клинических исследований
    """
    return ResearchAgentDependencies(
        api_key=api_key,
        research_domain="clinical",
        target_population=target_population,
        validation_level=validation_level,
        min_sample_size=100,
        reporting_standards=["CONSORT", "STROBE", "SPIRIT"],
        ethics_standards=["APA_Ethics", "Declaration_of_Helsinki", "ICH_GCP"],
        **kwargs
    )


def create_cognitive_dependencies(
    api_key: str,
    target_population: str = "adults",
    validation_level: str = "standard",
    **kwargs
) -> ResearchAgentDependencies:
    """
    Создать зависимости для когнитивных исследований.

    Args:
        api_key: API ключ провайдера
        target_population: Целевая популяция
        validation_level: Уровень валидации
        **kwargs: Дополнительные параметры

    Returns:
        Зависимости для когнитивных исследований
    """
    return ResearchAgentDependencies(
        api_key=api_key,
        research_domain="cognitive",
        target_population=target_population,
        validation_level=validation_level,
        methodology_focus="quantitative",
        min_sample_size=30,
        reporting_standards=["APA_Style", "JARS"],
        **kwargs
    )


def create_social_dependencies(
    api_key: str,
    target_population: str = "adults",
    validation_level: str = "standard",
    **kwargs
) -> ResearchAgentDependencies:
    """
    Создать зависимости для социально-психологических исследований.

    Args:
        api_key: API ключ провайдера
        target_population: Целевая популяция
        validation_level: Уровень валидации
        **kwargs: Дополнительные параметры

    Returns:
        Зависимости для социальных исследований
    """
    return ResearchAgentDependencies(
        api_key=api_key,
        research_domain="social",
        target_population=target_population,
        validation_level=validation_level,
        methodology_focus="mixed_methods",
        min_sample_size=50,
        literature_search_databases=["PubMed", "PsycINFO", "Sociological_Abstracts"],
        reporting_standards=["APA_Style", "JARS", "COREQ"],
        **kwargs
    )


def create_developmental_dependencies(
    api_key: str,
    target_population: str = "children",
    validation_level: str = "rigorous",
    **kwargs
) -> ResearchAgentDependencies:
    """
    Создать зависимости для исследований психологии развития.

    Args:
        api_key: API ключ провайдера
        target_population: Целевая популяция
        validation_level: Уровень валидации
        **kwargs: Дополнительные параметры

    Returns:
        Зависимости для исследований развития
    """
    return ResearchAgentDependencies(
        api_key=api_key,
        research_domain="developmental",
        target_population=target_population,
        validation_level=validation_level,
        min_sample_size=40,
        ethics_standards=["APA_Ethics", "SRCD_Ethical_Standards", "Declaration_of_Helsinki"],
        **kwargs
    )


def create_educational_dependencies(
    api_key: str,
    target_population: str = "students",
    validation_level: str = "standard",
    **kwargs
) -> ResearchAgentDependencies:
    """
    Создать зависимости для образовательных исследований.

    Args:
        api_key: API ключ провайдера
        target_population: Целевая популяция
        validation_level: Уровень валидации
        **kwargs: Дополнительные параметры

    Returns:
        Зависимости для образовательных исследований
    """
    return ResearchAgentDependencies(
        api_key=api_key,
        research_domain="educational",
        target_population=target_population,
        validation_level=validation_level,
        methodology_focus="mixed_methods",
        min_sample_size=60,
        literature_search_databases=["PubMed", "PsycINFO", "ERIC", "Education_Database"],
        reporting_standards=["APA_Style", "CONSORT", "COREQ"],
        **kwargs
    )


# Экспорт
__all__ = [
    "ResearchAgentDependencies",
    "create_clinical_dependencies",
    "create_cognitive_dependencies",
    "create_social_dependencies",
    "create_developmental_dependencies",
    "create_educational_dependencies"
]