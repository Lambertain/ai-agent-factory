# -*- coding: utf-8 -*-
"""
Зависимости для Universal Personalizer Agent
Универсальная конфигурация для персонализации в любых доменах
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Матрица компетенций агентов для делегирования
AGENT_COMPETENCIES = {
    "security_audit": [
        "безопасность", "приватность", "compliance", "аудит безопасности",
        "gdpr", "data protection", "user privacy", "персональные данные"
    ],
    "rag_agent": [
        "поиск информации", "семантический анализ", "knowledge base",
        "document retrieval", "информационный поиск", "персонализация паттернов"
    ],
    "uiux_enhancement": [
        "дизайн", "пользовательский интерфейс", "accessibility", "UX/UI",
        "персонализация интерфейса", "адаптивный дизайн", "пользовательский опыт"
    ],
    "performance_optimization": [
        "производительность", "оптимизация", "скорость", "memory usage",
        "персонализация производительность", "рекомендательные системы", "кэширование"
    ]
}

AGENT_ASSIGNEE_MAP = {
    "security_audit": "Security Audit Agent",
    "rag_agent": "Archon Analysis Lead",
    "uiux_enhancement": "Archon UI/UX Designer",
    "performance_optimization": "Performance Optimization Agent"
}

@dataclass
class PersonalizerDependencies:
    """
    Универсальные зависимости для персонализации в любых доменах.

    Поддерживает психологию, астрологию, нумерологию, бизнес и другие области.
    """

    # Основные настройки
    api_key: str
    project_path: str = ""

    # Универсальная конфигурация домена
    domain_type: str = "psychology"  # psychology, astrology, numerology, business, etc.
    project_type: str = "transformation_platform"  # educational_system, consultancy, etc.
    framework: str = "pydantic_ai"  # fastapi, django, etc.

    # Конфигурация персонализации
    personalization_mode: str = "adaptive"  # adaptive, rule_based, ml_driven, hybrid
    personalization_depth: str = "comprehensive"  # basic, comprehensive, deep
    adaptation_strategy: str = "dynamic"  # static, dynamic, predictive
    learning_approach: str = "behavioral"  # behavioral, preference_based, contextual, hybrid

    # RAG конфигурация
    agent_name: str = "universal_personalizer"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "personalization", "user-experience", "agent-knowledge", "pydantic-ai"
    ])
    knowledge_domain: str | None = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Межагентное взаимодействие
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"

    # Доменно-специфичные настройки персонализации
    personalization_config: Dict[str, Any] = field(default_factory=dict)

    # Конфигурация персонализации
    user_segmentation: str = "behavioral"  # demographic, behavioral, psychographic, hybrid
    content_adaptation: str = "comprehensive"  # basic, comprehensive, advanced
    real_time_optimization: bool = True
    privacy_protection_level: str = "high"  # basic, medium, high, maximum

    # Временные рамки и контекст
    personalization_timeline: str = "immediate"  # immediate, short_term, long_term
    context_awareness: str = "full"  # minimal, partial, full
    cultural_adaptation: bool = True

    # Локализация
    primary_language: str = "ukrainian"  # ukrainian, polish, english
    secondary_languages: List[str] = field(default_factory=lambda: ["polish", "english"])
    target_regions: List[str] = field(default_factory=lambda: ["ukraine", "poland"])

    # Настройки алгоритмов персонализации
    recommendation_algorithm: str = "hybrid"  # collaborative, content_based, hybrid, ml
    similarity_threshold: float = 0.7
    min_interaction_count: int = 5
    personalization_confidence_threshold: float = 0.6

    def __post_init__(self):
        """Инициализация конфигурации после создания объекта."""
        # Настройка доменно-специфичных конфигураций
        if not self.personalization_config:
            self.personalization_config = self._get_domain_personalization_config()

        # Обновление тегов знаний с учетом домена
        domain_tag = self.domain_type.replace("_", "-")
        if domain_tag not in self.knowledge_tags:
            self.knowledge_tags.append(domain_tag)

    def _get_domain_personalization_config(self) -> Dict[str, Any]:
        """Получить конфигурацию персонализации для конкретного домена."""
        domain_configs = {
            "psychology": {
                "personalization_factors": [
                    "personality_traits", "psychological_state", "therapeutic_goals",
                    "cultural_background", "age_group", "severity_level"
                ],
                "content_types": [
                    "therapeutic_content", "educational_materials", "assessment_tools",
                    "progress_tracking", "motivational_messages", "intervention_strategies"
                ],
                "adaptation_rules": [
                    "evidence_based_matching", "therapeutic_alliance", "cultural_sensitivity",
                    "trauma_informed", "progress_based_adjustment", "safety_prioritization"
                ],
                "personalization_metrics": [
                    "therapeutic_engagement", "outcome_improvement", "user_satisfaction",
                    "content_relevance", "session_completion", "goal_achievement"
                ],
                "privacy_requirements": ["hipaa_compliance", "therapeutic_confidentiality", "consent_management"],
                "ethical_considerations": ["do_no_harm", "beneficence", "autonomy", "justice"]
            },
            "astrology": {
                "personalization_factors": [
                    "birth_chart_data", "cultural_tradition", "astrological_preferences",
                    "experience_level", "consultation_type", "spiritual_orientation"
                ],
                "content_types": [
                    "personal_horoscopes", "compatibility_analysis", "timing_guidance",
                    "chart_interpretations", "educational_content", "spiritual_insights"
                ],
                "adaptation_rules": [
                    "traditional_accuracy", "cultural_context", "personal_resonance",
                    "astrological_system_preference", "depth_level_matching", "timing_sensitivity"
                ],
                "personalization_metrics": [
                    "accuracy_perception", "personal_relevance", "spiritual_connection",
                    "guidance_usefulness", "cultural_appropriateness", "user_engagement"
                ],
                "privacy_requirements": ["birth_data_protection", "consultation_confidentiality"],
                "cultural_factors": ["astrological_tradition", "spiritual_beliefs", "cultural_background"]
            },
            "numerology": {
                "personalization_factors": [
                    "core_numbers", "life_path", "personal_year", "name_vibrations",
                    "cultural_context", "numerological_system_preference"
                ],
                "content_types": [
                    "personal_numerology_reports", "compatibility_analysis", "timing_guidance",
                    "business_numerology", "name_analysis", "cycles_interpretation"
                ],
                "adaptation_rules": [
                    "system_consistency", "cultural_relevance", "practical_application",
                    "personal_resonance", "accuracy_validation", "actionable_insights"
                ],
                "personalization_metrics": [
                    "calculation_accuracy", "personal_relevance", "practical_usefulness",
                    "cultural_appropriateness", "insight_quality", "user_satisfaction"
                ],
                "calculation_systems": ["pythagorean", "chaldean", "kabbalah"],
                "application_areas": ["personal_development", "business_decisions", "relationship_guidance"]
            },
            "business": {
                "personalization_factors": [
                    "industry_sector", "company_size", "role_level", "business_goals",
                    "market_position", "growth_stage", "technology_adoption"
                ],
                "content_types": [
                    "strategic_recommendations", "market_insights", "operational_guidance",
                    "performance_analytics", "training_materials", "decision_support"
                ],
                "adaptation_rules": [
                    "industry_relevance", "company_size_appropriateness", "role_based_filtering",
                    "goal_alignment", "market_context", "resource_constraints"
                ],
                "personalization_metrics": [
                    "business_impact", "roi_improvement", "decision_quality",
                    "operational_efficiency", "strategic_alignment", "user_adoption"
                ],
                "business_contexts": ["strategic_planning", "operational_optimization", "market_analysis"],
                "success_indicators": ["kpi_improvement", "cost_reduction", "revenue_growth"]
            }
        }
        return domain_configs.get(self.domain_type, {})

    def get_personalization_factors_for_domain(self) -> List[str]:
        """Получить факторы персонализации для домена."""
        return self.personalization_config.get("personalization_factors", [])

    def get_content_types_for_domain(self) -> List[str]:
        """Получить типы контента для домена."""
        return self.personalization_config.get("content_types", [])

    def get_adaptation_rules_for_domain(self) -> List[str]:
        """Получить правила адаптации для домена."""
        return self.personalization_config.get("adaptation_rules", [])

    def get_personalization_metrics_for_domain(self) -> List[str]:
        """Получить метрики персонализации для домена."""
        return self.personalization_config.get("personalization_metrics", [])

    def should_delegate(self, task_keywords: List[str], current_agent_type: str = "personalizer") -> Optional[str]:
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
            "personalization_mode": self.personalization_mode,
            "personalization_depth": self.personalization_depth,
            "adaptation_strategy": self.adaptation_strategy,
            "learning_approach": self.learning_approach
        }

    def get_personalization_criteria(self) -> Dict[str, Any]:
        """Получить критерии персонализации для домена."""
        base_criteria = {
            "relevance": True,
            "accuracy": True,
            "engagement": True,
            "usability": True,
            "effectiveness": True,
            "satisfaction": True
        }

        # Доменно-специфичные критерии
        domain_criteria = {
            "psychology": {
                "therapeutic_value": True,
                "evidence_based": True,
                "cultural_sensitivity": True,
                "ethical_compliance": True,
                "safety": True
            },
            "astrology": {
                "traditional_accuracy": True,
                "spiritual_resonance": True,
                "cultural_appropriateness": True,
                "personal_meaning": True
            },
            "numerology": {
                "calculation_accuracy": True,
                "system_consistency": True,
                "practical_utility": True,
                "personal_relevance": True
            },
            "business": {
                "business_impact": True,
                "roi_potential": True,
                "strategic_alignment": True,
                "operational_feasibility": True
            }
        }

        base_criteria.update(domain_criteria.get(self.domain_type, {}))
        return base_criteria

    def get_privacy_settings(self) -> Dict[str, Any]:
        """Получить настройки приватности для домена."""
        base_privacy = {
            "data_anonymization": True,
            "consent_management": True,
            "data_minimization": True,
            "retention_limits": True
        }

        domain_privacy = {
            "psychology": {
                "hipaa_compliance": True,
                "therapeutic_confidentiality": True,
                "sensitive_data_protection": True
            },
            "astrology": {
                "birth_data_protection": True,
                "consultation_privacy": True
            },
            "numerology": {
                "personal_data_protection": True,
                "calculation_privacy": True
            },
            "business": {
                "commercial_confidentiality": True,
                "competitive_data_protection": True
            }
        }

        base_privacy.update(domain_privacy.get(self.domain_type, {}))
        return base_privacy

    def get_algorithm_configuration(self) -> Dict[str, Any]:
        """Получить конфигурацию алгоритмов персонализации."""
        return {
            "recommendation_algorithm": self.recommendation_algorithm,
            "similarity_threshold": self.similarity_threshold,
            "min_interaction_count": self.min_interaction_count,
            "confidence_threshold": self.personalization_confidence_threshold,
            "learning_rate": 0.01,
            "adaptation_speed": "medium",
            "fallback_strategy": "default_content"
        }

def load_dependencies(
    domain_type: str = "psychology",
    project_type: str = "transformation_platform",
    framework: str = "pydantic_ai",
    personalization_mode: str = "adaptive"
) -> PersonalizerDependencies:
    """
    Загрузить зависимости для Universal Personalizer Agent.

    Args:
        domain_type: Тип домена для персонализации
        project_type: Тип проекта
        framework: Технологический фреймворк
        personalization_mode: Режим персонализации

    Returns:
        Настроенные зависимости агента
    """
    load_dotenv()

    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise ValueError("LLM_API_KEY не найден в переменных окружения")

    return PersonalizerDependencies(
        api_key=api_key,
        project_path=os.getenv("PROJECT_PATH", ""),
        domain_type=domain_type,
        project_type=project_type,
        framework=framework,
        personalization_mode=personalization_mode,
        knowledge_domain=os.getenv("KNOWLEDGE_DOMAIN"),
        primary_language=os.getenv("PRIMARY_LANGUAGE", "ukrainian"),
        personalization_depth=os.getenv("PERSONALIZATION_DEPTH", "comprehensive"),
        adaptation_strategy=os.getenv("ADAPTATION_STRATEGY", "dynamic"),
        learning_approach=os.getenv("LEARNING_APPROACH", "behavioral")
    )