# -*- coding: utf-8 -*-
"""
Настройки Universal Opportunity Analyzer Agent
Универсальная конфигурация для анализа возможностей в любых доменах
"""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

@dataclass
class OpportunityAnalyzerSettings:
    """
    Универсальные настройки агента анализа возможностей.

    Поддерживает психологию, астрологию, нумерологию, бизнес и другие домены.
    """

    # Основные настройки агента
    agent_name: str = "universal_opportunity_analyzer"
    agent_version: str = "1.0.0"
    debug_mode: bool = False

    # LLM конфигурация
    llm_provider: str = "qwen"
    llm_api_key: str = ""
    llm_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm_model: str = "qwen2.5-coder-32b-instruct"
    llm_temperature: float = 0.1  # Низкая для аналитических задач
    llm_max_tokens: int = 8192

    # Альтернативные провайдеры
    gemini_api_key: str = ""
    openai_api_key: str = ""

    # Доменная конфигурация
    domain_type: str = "psychology"  # psychology, astrology, numerology, business, etc.
    project_type: str = "transformation_platform"  # educational_system, consultancy, etc.
    framework: str = "pydantic_ai"  # fastapi, django, etc.

    # Конфигурация анализа
    analysis_depth: str = "comprehensive"  # surface, comprehensive, deep
    market_scope: str = "regional"  # local, regional, global
    time_horizon: str = "medium_term"  # short_term, medium_term, long_term
    competition_analysis: bool = True
    risk_assessment: bool = True

    # RAG и база знаний
    knowledge_base_url: str = "http://localhost:3737"
    knowledge_domain: str = ""  # Домен источника знаний (если есть)
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "opportunity-analysis", "market-research", "agent-knowledge", "pydantic-ai"
    ])

    # Archon интеграция
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"

    # Локализация
    primary_language: str = "ukrainian"  # ukrainian, polish, english
    secondary_languages: List[str] = field(default_factory=lambda: ["polish", "english"])
    target_markets: List[str] = field(default_factory=lambda: ["ukraine", "poland"])

    # Критерии анализа возможностей
    scoring_weights: Dict[str, float] = field(default_factory=lambda: {
        "market_size": 0.25,
        "growth_potential": 0.25,
        "competition_level": 0.20,
        "implementation_complexity": 0.15,
        "roi_potential": 0.15
    })

    # Пороговые значения
    min_opportunity_score: float = 60.0  # Минимальный скор для рекомендации
    max_competition_level: float = 80.0  # Максимальный уровень конкуренции
    min_market_size: int = 1000000  # Минимальный размер рынка в USD

    # Тайм-ауты и лимиты
    analysis_timeout: int = 300  # 5 минут на анализ
    max_opportunities_per_analysis: int = 10
    max_pain_points_per_analysis: int = 15

    # Настройки логирования
    log_level: str = "INFO"
    save_analysis_logs: bool = True
    analysis_log_path: str = "logs/opportunity_analysis.log"

    # Экспериментальные настройки
    enable_ai_scoring: bool = True
    enable_cross_domain_analysis: bool = False
    enable_predictive_analytics: bool = False

    def __post_init__(self):
        """Постобработка настроек после инициализации."""
        # Обновляем теги знаний с учетом домена
        domain_tag = self.domain_type.replace("_", "-")
        if domain_tag not in self.knowledge_tags:
            self.knowledge_tags.append(domain_tag)

        # Валидация критических настроек
        self._validate_settings()

        # Доменно-специфичные настройки
        self._apply_domain_specific_settings()

    def _validate_settings(self):
        """Валидация критических настроек."""
        if not self.llm_api_key:
            raise ValueError("LLM_API_KEY обязателен для работы агента")

        if self.analysis_depth not in ["surface", "comprehensive", "deep"]:
            self.analysis_depth = "comprehensive"

        if self.market_scope not in ["local", "regional", "global"]:
            self.market_scope = "regional"

        if self.time_horizon not in ["short_term", "medium_term", "long_term"]:
            self.time_horizon = "medium_term"

        # Валидация весов скоринга
        total_weight = sum(self.scoring_weights.values())
        if abs(total_weight - 1.0) > 0.01:
            # Нормализуем веса
            for key in self.scoring_weights:
                self.scoring_weights[key] /= total_weight

    def _apply_domain_specific_settings(self):
        """Применить настройки специфичные для домена."""
        domain_configs = {
            "psychology": {
                "temperature": 0.05,  # Очень низкая для научной точности
                "scoring_weights": {
                    "scientific_validation": 0.30,
                    "market_size": 0.20,
                    "ethical_compliance": 0.25,
                    "growth_potential": 0.15,
                    "implementation_complexity": 0.10
                },
                "knowledge_tags": ["psychology", "therapy", "diagnostics", "mental-health"]
            },
            "astrology": {
                "temperature": 0.15,  # Умеренная для творческих интерпретаций
                "scoring_weights": {
                    "cultural_acceptance": 0.25,
                    "calculation_accuracy": 0.25,
                    "market_size": 0.20,
                    "traditional_alignment": 0.20,
                    "growth_potential": 0.10
                },
                "knowledge_tags": ["astrology", "horoscope", "consultation", "predictions"]
            },
            "numerology": {
                "temperature": 0.1,  # Низкая для точных расчетов
                "scoring_weights": {
                    "accuracy_requirements": 0.30,
                    "market_size": 0.25,
                    "cultural_relevance": 0.20,
                    "system_compatibility": 0.15,
                    "growth_potential": 0.10
                },
                "knowledge_tags": ["numerology", "calculations", "compatibility", "naming"]
            },
            "business": {
                "temperature": 0.2,  # Умеренная для креативных бизнес-решений
                "scoring_weights": {
                    "roi_potential": 0.30,
                    "market_readiness": 0.25,
                    "scalability": 0.20,
                    "competitive_advantage": 0.15,
                    "implementation_complexity": 0.10
                },
                "knowledge_tags": ["business", "strategy", "analytics", "consulting"]
            }
        }

        domain_config = domain_configs.get(self.domain_type, {})

        # Применяем доменно-специфичные настройки
        if "temperature" in domain_config:
            self.llm_temperature = domain_config["temperature"]

        if "scoring_weights" in domain_config:
            self.scoring_weights.update(domain_config["scoring_weights"])

        if "knowledge_tags" in domain_config:
            for tag in domain_config["knowledge_tags"]:
                if tag not in self.knowledge_tags:
                    self.knowledge_tags.append(tag)

    def get_domain_prompt_variables(self) -> Dict[str, Any]:
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
        """Получить критерии анализа для текущего домена."""
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
                "regulatory_requirements": True,
                "cultural_sensitivity": True
            },
            "astrology": {
                "cultural_acceptance": True,
                "traditional_alignment": True,
                "calculation_accuracy": True,
                "interpretation_quality": True
            },
            "numerology": {
                "system_compatibility": True,
                "cultural_relevance": True,
                "accuracy_requirements": True,
                "practical_applicability": True
            },
            "business": {
                "market_readiness": True,
                "scalability": True,
                "competitive_advantage": True,
                "financial_viability": True
            }
        }

        base_criteria.update(domain_criteria.get(self.domain_type, {}))
        return base_criteria

    def get_pain_points_config(self) -> Dict[str, List[str]]:
        """Получить конфигурацию болевых точек для домена."""
        pain_points_configs = {
            "psychology": [
                "depression", "anxiety", "relationships", "self_esteem",
                "addiction", "trauma", "stress", "burnout", "phobias"
            ],
            "astrology": [
                "life_direction", "relationship_compatibility", "career_guidance",
                "timing_decisions", "personal_understanding", "spiritual_growth"
            ],
            "numerology": [
                "name_selection", "date_planning", "compatibility_questions",
                "life_path_guidance", "business_naming", "lucky_numbers"
            ],
            "business": [
                "market_entry", "competition_analysis", "growth_strategy",
                "operational_efficiency", "customer_acquisition", "funding"
            ]
        }

        return {
            "pain_points": pain_points_configs.get(self.domain_type, []),
            "priority_weight": 0.8,  # Вес болевых точек в общем анализе
            "validation_required": self.domain_type == "psychology"
        }

    def export_config(self) -> Dict[str, Any]:
        """Экспортировать конфигурацию в словарь."""
        return {
            "agent_info": {
                "name": self.agent_name,
                "version": self.agent_version,
                "domain": self.domain_type,
                "project_type": self.project_type
            },
            "llm_settings": {
                "provider": self.llm_provider,
                "model": self.llm_model,
                "temperature": self.llm_temperature,
                "max_tokens": self.llm_max_tokens
            },
            "analysis_config": {
                "depth": self.analysis_depth,
                "scope": self.market_scope,
                "horizon": self.time_horizon,
                "scoring_weights": self.scoring_weights
            },
            "localization": {
                "primary_language": self.primary_language,
                "target_markets": self.target_markets
            }
        }

def load_settings() -> OpportunityAnalyzerSettings:
    """
    Загрузить настройки агента из переменных окружения.

    Returns:
        Настроенный объект OpportunityAnalyzerSettings

    Raises:
        ValueError: Если критически важные настройки отсутствуют
    """
    # Загружаем переменные окружения
    load_dotenv()

    try:
        settings = OpportunityAnalyzerSettings(
            # Основные настройки
            debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",

            # LLM настройки
            llm_provider=os.getenv("LLM_PROVIDER", "qwen"),
            llm_api_key=os.getenv("LLM_API_KEY", ""),
            llm_base_url=os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
            llm_model=os.getenv("LLM_MODEL", "qwen2.5-coder-32b-instruct"),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
            llm_max_tokens=int(os.getenv("LLM_MAX_TOKENS", "8192")),

            # Альтернативные провайдеры
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),

            # Доменная конфигурация
            domain_type=os.getenv("DOMAIN_TYPE", "psychology"),
            project_type=os.getenv("PROJECT_TYPE", "transformation_platform"),
            framework=os.getenv("FRAMEWORK", "pydantic_ai"),

            # Анализ настройки
            analysis_depth=os.getenv("ANALYSIS_DEPTH", "comprehensive"),
            market_scope=os.getenv("MARKET_SCOPE", "regional"),
            time_horizon=os.getenv("TIME_HORIZON", "medium_term"),
            competition_analysis=os.getenv("COMPETITION_ANALYSIS", "true").lower() == "true",
            risk_assessment=os.getenv("RISK_ASSESSMENT", "true").lower() == "true",

            # RAG настройки
            knowledge_base_url=os.getenv("KNOWLEDGE_BASE_URL", "http://localhost:3737"),
            knowledge_domain=os.getenv("KNOWLEDGE_DOMAIN", ""),

            # Archon настройки
            archon_project_id=os.getenv("ARCHON_PROJECT_ID", "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"),
            enable_task_delegation=os.getenv("ENABLE_TASK_DELEGATION", "true").lower() == "true",

            # Локализация
            primary_language=os.getenv("PRIMARY_LANGUAGE", "ukrainian"),

            # Лимиты и тайм-ауты
            analysis_timeout=int(os.getenv("ANALYSIS_TIMEOUT", "300")),
            max_opportunities_per_analysis=int(os.getenv("MAX_OPPORTUNITIES", "10")),
            max_pain_points_per_analysis=int(os.getenv("MAX_PAIN_POINTS", "15")),

            # Логирование
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            save_analysis_logs=os.getenv("SAVE_ANALYSIS_LOGS", "true").lower() == "true"
        )

        return settings

    except Exception as e:
        raise ValueError(f"Ошибка загрузки настроек: {e}")

def create_domain_config(
    domain_type: str,
    project_type: str = "platform",
    analysis_depth: str = "comprehensive"
) -> OpportunityAnalyzerSettings:
    """
    Создать настройки для конкретного домена.

    Args:
        domain_type: Тип домена (psychology, astrology, numerology, business)
        project_type: Тип проекта
        analysis_depth: Глубина анализа

    Returns:
        Настроенный объект для домена
    """
    base_settings = load_settings()

    # Обновляем доменно-специфичные настройки
    base_settings.domain_type = domain_type
    base_settings.project_type = project_type
    base_settings.analysis_depth = analysis_depth

    # Пересчитываем доменную конфигурацию
    base_settings._apply_domain_specific_settings()

    return base_settings