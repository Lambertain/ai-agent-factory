"""
Зависимости для Psychology Quality Guardian Agent

Конфигурация зависимостей для универсального контроля качества
психологического контента с поддержкой различных доменов и стандартов.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import uuid


@dataclass
class QualityGuardianDependencies:
    """
    Зависимости для Psychology Quality Guardian Agent.

    Поддерживает универсальную конфигурацию для различных доменов
    психологического контента и стандартов качества.
    """

    # Основные настройки
    api_key: str
    project_path: str = ""

    # Универсальные настройки домена
    domain_type: str = "general"  # clinical, educational, research, wellness, organizational
    target_population: str = "adults"  # adults, children, adolescents, elderly, mixed
    content_type: str = "assessment"  # test, intervention, program, survey, screening

    # Стандарты качества
    quality_standards: List[str] = field(default_factory=lambda: ["APA", "ethical_guidelines"])
    compliance_level: str = "standard"  # basic, standard, comprehensive, research_grade
    validation_requirements: List[str] = field(default_factory=lambda: ["ethical", "scientific", "safety"])

    # Настройки оценки
    evaluation_depth: str = "standard"  # basic, standard, comprehensive, forensic
    risk_tolerance: str = "medium"  # low, medium, high
    cultural_sensitivity_level: str = "standard"  # basic, standard, high

    # Психометрические стандарты
    psychometric_standards: Dict[str, float] = field(default_factory=lambda: {
        "reliability_threshold": 0.80,
        "validity_threshold": 0.70,
        "factor_loading_min": 0.30,
        "item_total_correlation_min": 0.30
    })

    # Этические параметры
    ethical_frameworks: List[str] = field(default_factory=lambda: ["beneficence", "justice", "respect", "integrity"])
    informed_consent_required: bool = True
    vulnerable_groups_protection: bool = True

    # Настройки безопасности
    safety_protocols: List[str] = field(default_factory=lambda: ["risk_assessment", "crisis_protocols", "monitoring"])
    privacy_level: str = "high"  # basic, standard, high, maximum
    data_protection_standards: List[str] = field(default_factory=lambda: ["GDPR", "local_requirements"])

    # Интеграция с RAG и знаниями
    knowledge_base_enabled: bool = True
    knowledge_tags: List[str] = field(default_factory=lambda: ["psychology_quality_guardian", "quality_control", "validation"])
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Автоматизация и отчетность
    automated_checks: bool = True
    real_time_monitoring: bool = False
    report_format: str = "comprehensive"  # summary, detailed, comprehensive
    notification_level: str = "important"  # all, important, critical_only

    # Версионирование и отслеживание
    standards_version: str = "2024.1"
    agent_version: str = "1.0.0"
    tracking_enabled: bool = True

    def __post_init__(self):
        """Инициализация и валидация конфигурации."""
        self._validate_configuration()
        self._setup_domain_specific_settings()
        self._configure_knowledge_tags()

    def _validate_configuration(self):
        """Валидация параметров конфигурации."""

        # Валидация domain_type
        valid_domains = ["general", "clinical", "educational", "research", "wellness", "organizational"]
        if self.domain_type not in valid_domains:
            raise ValueError(f"domain_type должен быть одним из: {valid_domains}")

        # Валидация target_population
        valid_populations = ["adults", "children", "adolescents", "elderly", "mixed"]
        if self.target_population not in valid_populations:
            raise ValueError(f"target_population должен быть одним из: {valid_populations}")

        # Валидация content_type
        valid_content_types = ["test", "intervention", "program", "survey", "screening", "assessment"]
        if self.content_type not in valid_content_types:
            raise ValueError(f"content_type должен быть одним из: {valid_content_types}")

        # Валидация compliance_level
        valid_compliance = ["basic", "standard", "comprehensive", "research_grade"]
        if self.compliance_level not in valid_compliance:
            raise ValueError(f"compliance_level должен быть одним из: {valid_compliance}")

        # Валидация психометрических стандартов
        if not 0.5 <= self.psychometric_standards["reliability_threshold"] <= 1.0:
            raise ValueError("reliability_threshold должен быть между 0.5 и 1.0")

        if not 0.5 <= self.psychometric_standards["validity_threshold"] <= 1.0:
            raise ValueError("validity_threshold должен быть между 0.5 и 1.0")

    def _setup_domain_specific_settings(self):
        """Настройка специфичных для домена параметров."""

        domain_configs = {
            "clinical": {
                "quality_standards": ["APA", "DSM5", "ICD11", "clinical_guidelines"],
                "psychometric_standards": {
                    "reliability_threshold": 0.85,
                    "validity_threshold": 0.80,
                    "factor_loading_min": 0.40,
                    "item_total_correlation_min": 0.35
                },
                "safety_protocols": ["clinical_risk_assessment", "crisis_intervention", "referral_protocols"],
                "ethical_frameworks": ["clinical_ethics", "beneficence", "justice", "respect", "integrity"],
                "privacy_level": "maximum"
            },

            "educational": {
                "quality_standards": ["educational_standards", "accessibility", "age_appropriateness"],
                "psychometric_standards": {
                    "reliability_threshold": 0.75,
                    "validity_threshold": 0.70,
                    "factor_loading_min": 0.30,
                    "item_total_correlation_min": 0.30
                },
                "safety_protocols": ["academic_risk_assessment", "parent_notification", "school_integration"],
                "ethical_frameworks": ["educational_ethics", "beneficence", "justice", "respect"],
                "privacy_level": "high"
            },

            "research": {
                "quality_standards": ["APA", "research_ethics", "IRB_guidelines", "scientific_rigor"],
                "psychometric_standards": {
                    "reliability_threshold": 0.85,
                    "validity_threshold": 0.80,
                    "factor_loading_min": 0.40,
                    "item_total_correlation_min": 0.35
                },
                "safety_protocols": ["research_ethics_protocols", "participant_monitoring", "data_security"],
                "ethical_frameworks": ["research_ethics", "beneficence", "justice", "respect", "integrity"],
                "privacy_level": "maximum",
                "compliance_level": "research_grade"
            },

            "wellness": {
                "quality_standards": ["wellness_guidelines", "user_safety", "engagement"],
                "psychometric_standards": {
                    "reliability_threshold": 0.70,
                    "validity_threshold": 0.65,
                    "factor_loading_min": 0.25,
                    "item_total_correlation_min": 0.25
                },
                "safety_protocols": ["wellness_monitoring", "user_support", "progress_tracking"],
                "ethical_frameworks": ["wellness_ethics", "beneficence", "respect"],
                "privacy_level": "standard"
            },

            "organizational": {
                "quality_standards": ["workplace_ethics", "fairness", "non_discrimination"],
                "psychometric_standards": {
                    "reliability_threshold": 0.80,
                    "validity_threshold": 0.75,
                    "factor_loading_min": 0.35,
                    "item_total_correlation_min": 0.30
                },
                "safety_protocols": ["workplace_safety", "privacy_protection", "legal_compliance"],
                "ethical_frameworks": ["workplace_ethics", "justice", "respect", "integrity"],
                "privacy_level": "high"
            }
        }

        if self.domain_type in domain_configs:
            domain_config = domain_configs[self.domain_type]

            # Обновляем настройки только если они не были явно заданы
            if self.quality_standards == ["APA", "ethical_guidelines"]:
                self.quality_standards = domain_config["quality_standards"]

            # Обновляем психометрические стандарты
            self.psychometric_standards.update(domain_config["psychometric_standards"])

            # Обновляем другие параметры
            if self.safety_protocols == ["risk_assessment", "crisis_protocols", "monitoring"]:
                self.safety_protocols = domain_config["safety_protocols"]

            if self.ethical_frameworks == ["beneficence", "justice", "respect", "integrity"]:
                self.ethical_frameworks = domain_config["ethical_frameworks"]

            if self.privacy_level == "high":
                self.privacy_level = domain_config.get("privacy_level", "high")

    def _configure_knowledge_tags(self):
        """Настройка тегов для поиска в базе знаний."""
        base_tags = ["psychology_quality_guardian", "quality_control", "validation"]

        # Добавляем теги специфичные для домена
        domain_tags = {
            "clinical": ["clinical_validation", "clinical_ethics", "DSM5", "diagnostic_tools"],
            "educational": ["educational_assessment", "school_psychology", "learning_evaluation"],
            "research": ["research_methodology", "psychometrics", "scientific_validation"],
            "wellness": ["wellness_psychology", "positive_psychology", "mental_health"],
            "organizational": ["organizational_psychology", "workplace_assessment", "HR_psychology"]
        }

        if self.domain_type in domain_tags:
            base_tags.extend(domain_tags[self.domain_type])

        # Добавляем теги для целевой популяции
        population_tags = {
            "children": ["child_psychology", "developmental_assessment"],
            "adolescents": ["adolescent_psychology", "youth_development"],
            "elderly": ["geropsychology", "aging_assessment"],
            "mixed": ["lifespan_psychology", "age_adapted_assessment"]
        }

        if self.target_population in population_tags:
            base_tags.extend(population_tags[self.target_population])

        self.knowledge_tags = base_tags

    def get_evaluation_criteria(self) -> Dict[str, Any]:
        """Получить критерии оценки для текущей конфигурации."""
        return {
            "domain_type": self.domain_type,
            "target_population": self.target_population,
            "content_type": self.content_type,
            "quality_standards": self.quality_standards,
            "compliance_level": self.compliance_level,
            "psychometric_standards": self.psychometric_standards,
            "ethical_frameworks": self.ethical_frameworks,
            "safety_protocols": self.safety_protocols,
            "validation_requirements": self.validation_requirements
        }

    def get_risk_assessment_parameters(self) -> Dict[str, Any]:
        """Получить параметры оценки рисков."""
        return {
            "risk_tolerance": self.risk_tolerance,
            "vulnerable_groups_protection": self.vulnerable_groups_protection,
            "safety_protocols": self.safety_protocols,
            "privacy_level": self.privacy_level,
            "target_population": self.target_population,
            "content_type": self.content_type
        }

    def get_cultural_sensitivity_parameters(self) -> Dict[str, Any]:
        """Получить параметры культурной чувствительности."""
        return {
            "sensitivity_level": self.cultural_sensitivity_level,
            "target_population": self.target_population,
            "domain_type": self.domain_type,
            "ethical_frameworks": self.ethical_frameworks,
            "quality_standards": self.quality_standards
        }

    def is_high_risk_population(self) -> bool:
        """Проверить, является ли целевая популяция высокорискованной."""
        high_risk_populations = ["children", "elderly", "clinical"]
        return (
            self.target_population in high_risk_populations or
            self.domain_type == "clinical" or
            self.vulnerable_groups_protection
        )

    def requires_enhanced_validation(self) -> bool:
        """Определить, требуется ли усиленная валидация."""
        return (
            self.compliance_level in ["comprehensive", "research_grade"] or
            self.domain_type in ["clinical", "research"] or
            self.is_high_risk_population() or
            "research_ethics" in self.quality_standards
        )

    def get_minimum_reliability_threshold(self) -> float:
        """Получить минимальный порог надежности для текущей конфигурации."""
        base_threshold = self.psychometric_standards["reliability_threshold"]

        # Повышаем требования для критических доменов
        if self.domain_type == "clinical" and self.content_type in ["test", "assessment"]:
            return max(base_threshold, 0.85)
        elif self.compliance_level == "research_grade":
            return max(base_threshold, 0.80)
        else:
            return base_threshold

    def get_validation_scope(self) -> List[str]:
        """Получить полный объем валидации для текущей конфигурации."""
        base_scope = self.validation_requirements.copy()

        # Добавляем дополнительные требования для специфических случаев
        if self.domain_type == "clinical":
            if "clinical_validity" not in base_scope:
                base_scope.append("clinical_validity")

        if self.is_high_risk_population():
            if "enhanced_safety" not in base_scope:
                base_scope.append("enhanced_safety")

        if self.cultural_sensitivity_level == "high":
            if "cultural_validation" not in base_scope:
                base_scope.append("cultural_validation")

        if self.compliance_level == "research_grade":
            research_requirements = ["psychometric_validation", "statistical_validation", "replication"]
            for req in research_requirements:
                if req not in base_scope:
                    base_scope.append(req)

        return base_scope

    def get_reporting_configuration(self) -> Dict[str, Any]:
        """Получить конфигурацию отчетности."""
        return {
            "report_format": self.report_format,
            "notification_level": self.notification_level,
            "tracking_enabled": self.tracking_enabled,
            "automated_checks": self.automated_checks,
            "real_time_monitoring": self.real_time_monitoring,
            "standards_version": self.standards_version,
            "agent_version": self.agent_version
        }

    def generate_session_id(self) -> str:
        """Генерация уникального ID сессии."""
        return f"qg_{self.domain_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"

    def generate_batch_id(self) -> str:
        """Генерация ID для пакетной обработки."""
        return f"batch_{self.domain_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def get_current_timestamp(self) -> str:
        """Получить текущую временную метку."""
        return datetime.now().isoformat()

    def assess_overall_risk_level(self, evaluation_results: Any) -> str:
        """Оценить общий уровень риска на основе результатов."""
        # Простая логика оценки риска (может быть расширена)
        if isinstance(evaluation_results, str):
            if "высокий" in evaluation_results.lower() or "critical" in evaluation_results.lower():
                return "high"
            elif "средний" in evaluation_results.lower() or "moderate" in evaluation_results.lower():
                return "medium"
        return "low"

    def requires_expert_review(self, evaluation_results: Any) -> bool:
        """Определить, требуется ли экспертная проверка."""
        risk_level = self.assess_overall_risk_level(evaluation_results)

        return (
            risk_level == "high" or
            self.domain_type == "clinical" or
            self.compliance_level == "research_grade" or
            self.is_high_risk_population()
        )

    def estimate_implementation_complexity(self, quality_issues: List[Any]) -> str:
        """Оценить сложность внедрения улучшений."""
        if not quality_issues:
            return "minimal"

        issue_count = len(quality_issues)
        if issue_count <= 3:
            return "low"
        elif issue_count <= 7:
            return "medium"
        else:
            return "high"

    def get_processing_time(self) -> str:
        """Получить время обработки (заглушка для реальной реализации)."""
        return "processing_time_placeholder"

    def should_enable_automated_monitoring(self) -> bool:
        """Определить, следует ли включить автоматический мониторинг."""
        return (
            self.automated_checks and
            self.real_time_monitoring and
            self.domain_type in ["clinical", "research"]
        )

    def get_data_retention_policy(self) -> Dict[str, Any]:
        """Получить политику хранения данных."""
        retention_policies = {
            "clinical": {"retention_period": "7_years", "encryption_required": True},
            "research": {"retention_period": "10_years", "encryption_required": True},
            "educational": {"retention_period": "3_years", "encryption_required": False},
            "wellness": {"retention_period": "1_year", "encryption_required": False},
            "organizational": {"retention_period": "5_years", "encryption_required": True}
        }

        default_policy = {"retention_period": "2_years", "encryption_required": False}
        return retention_policies.get(self.domain_type, default_policy)

    def get_compliance_checklist(self) -> List[str]:
        """Получить чек-лист соответствия для текущей конфигурации."""
        base_checklist = [
            "Этическое соответствие проверено",
            "Научная валидность подтверждена",
            "Безопасность контента оценена",
            "Информированное согласие получено"
        ]

        if self.domain_type == "clinical":
            base_checklist.extend([
                "Клинические стандарты соблюдены",
                "Диагностическая валидность подтверждена",
                "Протоколы кризисного реагирования готовы"
            ])

        if self.is_high_risk_population():
            base_checklist.extend([
                "Защита уязвимых групп обеспечена",
                "Дополнительные меры безопасности внедрены"
            ])

        if "GDPR" in self.data_protection_standards:
            base_checklist.extend([
                "GDPR соответствие подтверждено",
                "Права субъектов данных обеспечены"
            ])

        return base_checklist


# Фабричные функции для быстрого создания конфигураций

def create_clinical_dependencies(
    api_key: str,
    target_population: str = "adults",
    **kwargs
) -> QualityGuardianDependencies:
    """Создать зависимости для клинического домена."""
    return QualityGuardianDependencies(
        api_key=api_key,
        domain_type="clinical",
        target_population=target_population,
        content_type="assessment",
        compliance_level="comprehensive",
        privacy_level="maximum",
        **kwargs
    )


def create_research_dependencies(
    api_key: str,
    research_type: str = "experimental",
    **kwargs
) -> QualityGuardianDependencies:
    """Создать зависимости для исследовательского домена."""
    return QualityGuardianDependencies(
        api_key=api_key,
        domain_type="research",
        content_type="test",
        compliance_level="research_grade",
        validation_requirements=["ethical", "scientific", "psychometric", "statistical"],
        **kwargs
    )


def create_educational_dependencies(
    api_key: str,
    age_group: str = "adolescents",
    **kwargs
) -> QualityGuardianDependencies:
    """Создать зависимости для образовательного домена."""
    return QualityGuardianDependencies(
        api_key=api_key,
        domain_type="educational",
        target_population=age_group,
        content_type="assessment",
        cultural_sensitivity_level="high",
        **kwargs
    )


def create_wellness_dependencies(
    api_key: str,
    wellness_focus: str = "general",
    **kwargs
) -> QualityGuardianDependencies:
    """Создать зависимости для wellness домена."""
    return QualityGuardianDependencies(
        api_key=api_key,
        domain_type="wellness",
        content_type="program",
        compliance_level="standard",
        risk_tolerance="medium",
        **kwargs
    )


def create_organizational_dependencies(
    api_key: str,
    assessment_type: str = "selection",
    **kwargs
) -> QualityGuardianDependencies:
    """Создать зависимости для организационного домена."""
    return QualityGuardianDependencies(
        api_key=api_key,
        domain_type="organizational",
        content_type="test",
        quality_standards=["workplace_ethics", "fairness", "non_discrimination"],
        privacy_level="high",
        **kwargs
    )