# -*- coding: utf-8 -*-
"""
Зависимости для Universal Solution Pattern Mapper Agent
Универсальная конфигурация для маппинга решений в любых доменах
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Матрица компетенций агентов для делегирования
AGENT_COMPETENCIES = {
    "security_audit": [
        "безопасность", "уязвимости", "compliance", "аудит безопасности",
        "secrets detection", "penetration testing", "OWASP", "CVE"
    ],
    "rag_agent": [
        "поиск информации", "семантический анализ", "knowledge base",
        "document retrieval", "информационный поиск", "текстовый анализ"
    ],
    "uiux_enhancement": [
        "дизайн", "пользовательский интерфейс", "accessibility", "UX/UI",
        "компонентные библиотеки", "дизайн системы", "пользовательский опыт"
    ],
    "performance_optimization": [
        "производительность", "оптимизация", "скорость", "memory usage",
        "cpu optimization", "caching", "load testing", "профилирование"
    ]
}

AGENT_ASSIGNEE_MAP = {
    "security_audit": "Security Audit Agent",
    "rag_agent": "Archon Analysis Lead",
    "uiux_enhancement": "Archon UI/UX Designer",
    "performance_optimization": "Performance Optimization Agent"
}

@dataclass
class SolutionPatternMapperDependencies:
    """
    Универсальные зависимости для маппинга решений в любых доменах.

    Поддерживает психологию, астрологию, нумерологию, бизнес и другие области.
    """

    # Основные настройки
    api_key: str
    project_path: str = ""

    # Универсальная конфигурация домена
    domain_type: str = "psychology"  # psychology, astrology, numerology, business, etc.
    project_type: str = "transformation_platform"  # educational_system, consultancy, etc.
    framework: str = "pydantic_ai"  # fastapi, django, etc.

    # RAG конфигурация
    agent_name: str = "universal_solution_pattern_mapper"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "solution-patterns", "pattern-mapping", "agent-knowledge", "pydantic-ai"
    ])
    knowledge_domain: str | None = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Межагентное взаимодействие
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"

    # Доменно-специфичные настройки маппинга
    mapping_config: Dict[str, Any] = field(default_factory=dict)

    # Конфигурация маппинга паттернов
    pattern_complexity: str = "comprehensive"  # simple, comprehensive, advanced
    solution_scope: str = "domain_specific"  # universal, domain_specific, project_specific
    validation_level: str = "standard"  # basic, standard, rigorous
    adaptation_mode: str = "automatic"  # manual, automatic, hybrid

    # Временные рамки и контекст
    solution_timeline: str = "medium_term"  # short_term, medium_term, long_term
    implementation_context: str = "production"  # prototype, development, production

    # Локализация
    primary_language: str = "ukrainian"  # ukrainian, polish, english
    secondary_languages: List[str] = field(default_factory=lambda: ["polish", "english"])
    target_regions: List[str] = field(default_factory=lambda: ["ukraine", "poland"])

    def __post_init__(self):
        """Инициализация конфигурации после создания объекта."""
        # Настройка доменно-специфичных конфигураций
        if not self.mapping_config:
            self.mapping_config = self._get_domain_mapping_config()

        # Обновление тегов знаний с учетом домена
        domain_tag = self.domain_type.replace("_", "-")
        if domain_tag not in self.knowledge_tags:
            self.knowledge_tags.append(domain_tag)

    def _get_domain_mapping_config(self) -> Dict[str, Any]:
        """Получить конфигурацию маппинга для конкретного домена."""
        domain_configs = {
            "psychology": {
                "solution_types": [
                    "diagnostic_solutions", "therapeutic_interventions", "educational_programs",
                    "support_systems", "assessment_tools", "treatment_protocols"
                ],
                "pattern_categories": [
                    "evidence_based_practices", "therapeutic_modalities", "assessment_frameworks",
                    "intervention_strategies", "recovery_models", "prevention_approaches"
                ],
                "validation_criteria": [
                    "scientific_evidence", "clinical_efficacy", "ethical_compliance",
                    "cultural_appropriateness", "accessibility", "safety_profile"
                ],
                "adaptation_factors": [
                    "age_group", "cultural_background", "severity_level",
                    "comorbidities", "treatment_history", "resource_availability"
                ],
                "compliance_requirements": ["HIPAA", "GDPR", "ethical_guidelines"],
                "quality_standards": ["APA_guidelines", "evidence_based", "peer_reviewed"]
            },
            "astrology": {
                "solution_types": [
                    "consultation_frameworks", "calculation_systems", "interpretation_models",
                    "prediction_algorithms", "compatibility_analysis", "timing_systems"
                ],
                "pattern_categories": [
                    "house_systems", "aspect_patterns", "planetary_transits",
                    "chart_interpretation", "predictive_techniques", "compatibility_methods"
                ],
                "validation_criteria": [
                    "calculation_accuracy", "traditional_alignment", "cultural_relevance",
                    "interpretive_consistency", "user_satisfaction", "predictive_value"
                ],
                "adaptation_factors": [
                    "cultural_tradition", "astrological_system", "user_experience_level",
                    "consultation_type", "time_sensitivity", "geographic_location"
                ],
                "quality_standards": ["traditional_accuracy", "modern_relevance", "cultural_sensitivity"],
                "calculation_requirements": ["ephemeris_accuracy", "house_system_precision"]
            },
            "numerology": {
                "solution_types": [
                    "calculation_engines", "interpretation_systems", "compatibility_analyzers",
                    "timing_calculators", "name_analyzers", "business_consultancy"
                ],
                "pattern_categories": [
                    "core_numbers", "life_path_analysis", "compatibility_patterns",
                    "timing_cycles", "name_vibrations", "business_numerology"
                ],
                "validation_criteria": [
                    "calculation_accuracy", "system_consistency", "cultural_relevance",
                    "practical_applicability", "user_comprehension", "actionable_insights"
                ],
                "adaptation_factors": [
                    "numerological_system", "cultural_context", "application_purpose",
                    "user_beliefs", "complexity_preference", "output_format"
                ],
                "calculation_systems": ["pythagorean", "chaldean", "kabbalah"],
                "quality_standards": ["system_accuracy", "cultural_adaptation", "practical_utility"]
            },
            "business": {
                "solution_types": [
                    "strategic_frameworks", "operational_solutions", "analytical_tools",
                    "optimization_systems", "decision_support", "automation_solutions"
                ],
                "pattern_categories": [
                    "business_models", "process_patterns", "organizational_structures",
                    "market_strategies", "operational_frameworks", "technology_solutions"
                ],
                "validation_criteria": [
                    "roi_potential", "implementation_feasibility", "scalability",
                    "competitive_advantage", "risk_assessment", "resource_efficiency"
                ],
                "adaptation_factors": [
                    "industry_sector", "company_size", "market_maturity",
                    "resource_constraints", "competitive_position", "growth_stage"
                ],
                "metrics_focus": ["kpi_alignment", "measurable_outcomes", "business_impact"],
                "quality_standards": ["proven_effectiveness", "industry_best_practices", "measurable_results"]
            }
        }
        return domain_configs.get(self.domain_type, {})

    def get_solution_types_for_domain(self) -> List[str]:
        """Получить типы решений для домена."""
        return self.mapping_config.get("solution_types", [])

    def get_pattern_categories_for_domain(self) -> List[str]:
        """Получить категории паттернов для домена."""
        return self.mapping_config.get("pattern_categories", [])

    def get_validation_criteria_for_domain(self) -> List[str]:
        """Получить критерии валидации для домена."""
        return self.mapping_config.get("validation_criteria", [])

    def get_adaptation_factors_for_domain(self) -> List[str]:
        """Получить факторы адаптации для домена."""
        return self.mapping_config.get("adaptation_factors", [])

    def should_delegate(self, task_keywords: List[str], current_agent_type: str = "solution_pattern_mapper") -> Optional[str]:
        """Определить нужно ли делегировать задачу и кому."""
        for agent_type, competencies in AGENT_COMPETENCIES.items():
            if agent_type != current_agent_type:
                overlap = set(task_keywords) & set(competencies)
                if len(overlap) >= 2:  # Значительное пересечение компетенций
                    return agent_type
        return None

    def get_domain_specific_prompt_variables(self) -> Dict[str, str]:
        """Получить переменные для адаптации промптов под домен."""
        return {
            "domain_type": self.domain_type,
            "project_type": self.project_type,
            "framework": self.framework,
            "primary_language": self.primary_language,
            "pattern_complexity": self.pattern_complexity,
            "solution_scope": self.solution_scope,
            "validation_level": self.validation_level,
            "solution_timeline": self.solution_timeline
        }

    def get_pattern_mapping_criteria(self) -> Dict[str, Any]:
        """Получить критерии маппинга паттернов для домена."""
        base_criteria = {
            "relevance": True,
            "applicability": True,
            "effectiveness": True,
            "feasibility": True,
            "scalability": True,
            "maintainability": True
        }

        # Доменно-специфичные критерии
        domain_criteria = {
            "psychology": {
                "evidence_based": True,
                "ethical_compliance": True,
                "clinical_validity": True,
                "cultural_sensitivity": True
            },
            "astrology": {
                "traditional_accuracy": True,
                "cultural_relevance": True,
                "calculation_precision": True,
                "interpretive_consistency": True
            },
            "numerology": {
                "system_consistency": True,
                "calculation_accuracy": True,
                "practical_utility": True,
                "cultural_adaptation": True
            },
            "business": {
                "roi_impact": True,
                "competitive_advantage": True,
                "implementation_cost": True,
                "measurable_outcomes": True
            }
        }

        base_criteria.update(domain_criteria.get(self.domain_type, {}))
        return base_criteria

def load_dependencies(
    domain_type: str = "psychology",
    project_type: str = "transformation_platform",
    framework: str = "pydantic_ai"
) -> SolutionPatternMapperDependencies:
    """
    Загрузить зависимости для Universal Solution Pattern Mapper Agent.

    Args:
        domain_type: Тип домена для маппинга решений
        project_type: Тип проекта
        framework: Технологический фреймворк

    Returns:
        Настроенные зависимости агента
    """
    load_dotenv()

    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise ValueError("LLM_API_KEY не найден в переменных окружения")

    return SolutionPatternMapperDependencies(
        api_key=api_key,
        project_path=os.getenv("PROJECT_PATH", ""),
        domain_type=domain_type,
        project_type=project_type,
        framework=framework,
        knowledge_domain=os.getenv("KNOWLEDGE_DOMAIN"),
        primary_language=os.getenv("PRIMARY_LANGUAGE", "ukrainian"),
        pattern_complexity=os.getenv("PATTERN_COMPLEXITY", "comprehensive"),
        solution_scope=os.getenv("SOLUTION_SCOPE", "domain_specific"),
        validation_level=os.getenv("VALIDATION_LEVEL", "standard")
    )