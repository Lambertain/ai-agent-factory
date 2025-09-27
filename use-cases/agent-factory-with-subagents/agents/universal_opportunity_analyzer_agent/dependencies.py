# -*- coding: utf-8 -*-
"""
Зависимости для Universal Opportunity Analyzer Agent
Универсальная конфигурация для анализа возможностей в любых доменах
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
class OpportunityAnalyzerDependencies:
    """
    Универсальные зависимости для анализа возможностей в любых доменах.

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
    agent_name: str = "universal_opportunity_analyzer"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "opportunity-analysis", "market-research", "agent-knowledge", "pydantic-ai"
    ])
    knowledge_domain: str | None = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Межагентное взаимодействие
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"

    # Доменно-специфичные настройки анализа
    analysis_config: Dict[str, Any] = field(default_factory=dict)

    # Конфигурация анализа возможностей
    analysis_depth: str = "comprehensive"  # surface, comprehensive, deep
    market_scope: str = "regional"  # local, regional, global
    competition_analysis: bool = True
    risk_assessment: bool = True

    # Временные рамки анализа
    time_horizon: str = "medium_term"  # short_term, medium_term, long_term
    analysis_period: str = "current"  # historical, current, predictive

    # Локализация
    primary_language: str = "ukrainian"  # ukrainian, polish, english
    secondary_languages: List[str] = field(default_factory=lambda: ["polish", "english"])
    target_markets: List[str] = field(default_factory=lambda: ["ukraine", "poland"])

    def __post_init__(self):
        """Инициализация конфигурации после создания объекта."""
        # Настройка доменно-специфичных конфигураций
        if not self.analysis_config:
            self.analysis_config = self._get_domain_analysis_config()

        # Обновление тегов знаний с учетом домена
        domain_tag = self.domain_type.replace("_", "-")
        if domain_tag not in self.knowledge_tags:
            self.knowledge_tags.append(domain_tag)

    def _get_domain_analysis_config(self) -> Dict[str, Any]:
        """Получить конфигурацию анализа для конкретного домена."""
        domain_configs = {
            "psychology": {
                "pain_points_focus": [
                    "depression", "anxiety", "relationships", "self_esteem",
                    "addiction", "trauma", "stress", "burnout"
                ],
                "opportunity_types": [
                    "therapy_platforms", "self_help_apps", "diagnostic_tools",
                    "educational_programs", "support_communities"
                ],
                "market_segments": [
                    "individuals", "therapists", "organizations", "educational_institutions"
                ],
                "validation_required": True,
                "ethical_considerations": True
            },
            "astrology": {
                "pain_points_focus": [
                    "life_direction", "relationship_compatibility", "career_guidance",
                    "timing_decisions", "personal_understanding"
                ],
                "opportunity_types": [
                    "consultation_platforms", "calculation_tools", "education_courses",
                    "compatibility_services", "predictive_analytics"
                ],
                "market_segments": [
                    "astrology_enthusiasts", "professional_astrologers", "curious_newcomers"
                ],
                "cultural_sensitivity": True,
                "tradition_respect": True
            },
            "numerology": {
                "pain_points_focus": [
                    "name_selection", "date_planning", "compatibility_questions",
                    "life_path_guidance", "business_naming"
                ],
                "opportunity_types": [
                    "calculation_services", "consultation_platforms", "naming_tools",
                    "compatibility_analysis", "business_advisory"
                ],
                "market_segments": [
                    "new_parents", "entrepreneurs", "spiritual_seekers", "couples"
                ],
                "calculation_accuracy": True,
                "multiple_systems": True
            },
            "business": {
                "pain_points_focus": [
                    "market_entry", "competition_analysis", "growth_strategy",
                    "operational_efficiency", "customer_acquisition"
                ],
                "opportunity_types": [
                    "consulting_services", "analysis_tools", "strategy_platforms",
                    "optimization_software", "market_research"
                ],
                "market_segments": [
                    "startups", "sme", "enterprises", "consultants", "investors"
                ],
                "data_driven": True,
                "roi_focused": True
            }
        }
        return domain_configs.get(self.domain_type, {})

    def get_pain_points_for_domain(self) -> List[str]:
        """Получить основные болевые точки для домена."""
        return self.analysis_config.get("pain_points_focus", [])

    def get_opportunity_types_for_domain(self) -> List[str]:
        """Получить типы возможностей для домена."""
        return self.analysis_config.get("opportunity_types", [])

    def get_target_segments_for_domain(self) -> List[str]:
        """Получить целевые сегменты для домена."""
        return self.analysis_config.get("market_segments", [])

    def should_delegate(self, task_keywords: List[str], current_agent_type: str = "opportunity_analyzer") -> Optional[str]:
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
            "analysis_depth": self.analysis_depth,
            "market_scope": self.market_scope,
            "time_horizon": self.time_horizon
        }

    def get_analysis_criteria(self) -> Dict[str, Any]:
        """Получить критерии анализа для домена."""
        base_criteria = {
            "market_size": True,
            "growth_potential": True,
            "competition_level": self.competition_analysis,
            "risk_level": self.risk_assessment,
            "implementation_complexity": True,
            "roi_potential": True
        }

        # Доменно-специфичные критерии
        domain_criteria = {
            "psychology": {
                "scientific_validation": True,
                "ethical_compliance": True,
                "regulatory_requirements": True
            },
            "astrology": {
                "cultural_acceptance": True,
                "traditional_alignment": True,
                "calculation_accuracy": True
            },
            "numerology": {
                "system_compatibility": True,
                "cultural_relevance": True,
                "accuracy_requirements": True
            },
            "business": {
                "market_readiness": True,
                "scalability": True,
                "competitive_advantage": True
            }
        }

        base_criteria.update(domain_criteria.get(self.domain_type, {}))
        return base_criteria

def load_dependencies(
    domain_type: str = "psychology",
    project_type: str = "transformation_platform",
    framework: str = "pydantic_ai"
) -> OpportunityAnalyzerDependencies:
    """
    Загрузить зависимости для Universal Opportunity Analyzer Agent.

    Args:
        domain_type: Тип домена для анализа возможностей
        project_type: Тип проекта
        framework: Технологический фреймворк

    Returns:
        Настроенные зависимости агента
    """
    load_dotenv()

    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise ValueError("LLM_API_KEY не найден в переменных окружения")

    return OpportunityAnalyzerDependencies(
        api_key=api_key,
        project_path=os.getenv("PROJECT_PATH", ""),
        domain_type=domain_type,
        project_type=project_type,
        framework=framework,
        knowledge_domain=os.getenv("KNOWLEDGE_DOMAIN"),
        primary_language=os.getenv("PRIMARY_LANGUAGE", "ukrainian"),
        analysis_depth=os.getenv("ANALYSIS_DEPTH", "comprehensive"),
        market_scope=os.getenv("MARKET_SCOPE", "regional")
    )