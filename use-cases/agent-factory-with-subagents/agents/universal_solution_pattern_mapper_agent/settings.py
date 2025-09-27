# -*- coding: utf-8 -*-
"""
Настройки для Universal Solution Pattern Mapper Agent
Конфигурируемые параметры для адаптации под различные домены и проекты
"""

import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv

class SolutionPatternMapperSettings(BaseSettings):
    """
    Настройки Universal Solution Pattern Mapper Agent с поддержкой переменных окружения.

    Поддерживает адаптацию под различные домены:
    - Psychology (психология)
    - Astrology (астрология)
    - Numerology (нумерология)
    - Business (бизнес)
    - И любые другие области
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # === БАЗОВЫЕ НАСТРОЙКИ ===
    llm_api_key: str = Field(..., description="API-ключ провайдера LLM")
    project_path: str = Field(default="", description="Путь к проекту")

    # === УНИВЕРСАЛЬНАЯ КОНФИГУРАЦИЯ ДОМЕНА ===
    domain_type: str = Field(
        default="psychology",
        description="Тип домена для маппинга (psychology, astrology, numerology, business, etc.)"
    )
    project_type: str = Field(
        default="transformation_platform",
        description="Тип проекта (transformation_platform, educational_system, consultation_platform, etc.)"
    )
    framework: str = Field(
        default="pydantic_ai",
        description="Технологический фреймворк (pydantic_ai, fastapi, django, etc.)"
    )

    # === НАСТРОЙКИ МАППИНГА ПАТТЕРНОВ ===
    pattern_complexity: str = Field(
        default="comprehensive",
        description="Сложность паттернов (simple, comprehensive, advanced)"
    )
    solution_scope: str = Field(
        default="domain_specific",
        description="Охват решений (universal, domain_specific, project_specific)"
    )
    validation_level: str = Field(
        default="standard",
        description="Уровень валидации (basic, standard, rigorous)"
    )
    adaptation_mode: str = Field(
        default="automatic",
        description="Режим адаптации (manual, automatic, hybrid)"
    )

    # === ВРЕМЕННЫЕ И КОНТЕКСТНЫЕ ПАРАМЕТРЫ ===
    solution_timeline: str = Field(
        default="medium_term",
        description="Временные рамки решений (short_term, medium_term, long_term)"
    )
    implementation_context: str = Field(
        default="production",
        description="Контекст реализации (prototype, development, production)"
    )

    # === ЛОКАЛИЗАЦИЯ ===
    primary_language: str = Field(
        default="ukrainian",
        description="Основной язык (ukrainian, polish, english)"
    )
    secondary_languages: str = Field(
        default="polish,english",
        description="Дополнительные языки через запятую"
    )
    target_regions: str = Field(
        default="ukraine,poland",
        description="Целевые регионы через запятую"
    )

    # === RAG И KNOWLEDGE BASE ===
    agent_name: str = Field(
        default="universal_solution_pattern_mapper",
        description="Имя агента для RAG"
    )
    knowledge_tags: str = Field(
        default="solution-patterns,pattern-mapping,agent-knowledge,pydantic-ai",
        description="Теги для поиска знаний через запятую"
    )
    knowledge_domain: Optional[str] = Field(
        default=None,
        description="Домен источника знаний"
    )
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )

    # === МЕЖАГЕНТНОЕ ВЗАИМОДЕЙСТВИЕ ===
    enable_task_delegation: bool = Field(
        default=True,
        description="Включить делегирование задач другим агентам"
    )
    delegation_threshold: str = Field(
        default="medium",
        description="Порог для делегирования (low, medium, high)"
    )
    max_delegation_depth: int = Field(
        default=3,
        description="Максимальная глубина делегирования"
    )

    # === COST-OPTIMIZED LLM КОНФИГУРАЦИЯ ===
    llm_provider: str = Field(
        default="qwen",
        description="Основной провайдер LLM (qwen, gemini, openai, claude)"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL для LLM API"
    )

    # Модели для разных типов задач маппинга
    llm_pattern_mapping_model: str = Field(
        default="qwen2.5:14b",
        description="Модель для маппинга паттернов"
    )
    llm_solution_analysis_model: str = Field(
        default="qwen2.5:7b",
        description="Модель для анализа решений"
    )
    llm_blueprint_generation_model: str = Field(
        default="qwen2.5:14b",
        description="Модель для генерации чертежей"
    )
    llm_domain_adaptation_model: str = Field(
        default="qwen2.5:14b",
        description="Модель для адаптации под домен"
    )

    # Альтернативные API ключи
    gemini_api_key: Optional[str] = Field(
        default=None,
        description="Google Gemini API ключ"
    )
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API ключ"
    )
    claude_api_key: Optional[str] = Field(
        default=None,
        description="Claude API ключ"
    )

    # === НАСТРОЙКИ ПРОИЗВОДИТЕЛЬНОСТИ ===
    max_tokens: int = Field(
        default=4096,
        description="Максимальное количество токенов"
    )
    temperature: float = Field(
        default=0.4,
        description="Температура генерации"
    )
    request_timeout: int = Field(
        default=120,
        description="Таймаут запросов в секундах"
    )
    retry_attempts: int = Field(
        default=3,
        description="Количество попыток при ошибках"
    )

    # === ВЕСОВЫЕ КОЭФФИЦИЕНТЫ ДЛЯ МАППИНГА ===
    pattern_scoring_weights: str = Field(
        default="relevance:0.25,applicability:0.20,effectiveness:0.20,feasibility:0.15,scalability:0.10,maintainability:0.10",
        description="Веса для скоринга паттернов (через запятую, формат: критерий:вес)"
    )
    solution_quality_weights: str = Field(
        default="technical_quality:0.30,domain_fit:0.25,implementation_ease:0.20,innovation:0.15,risk_level:0.10",
        description="Веса для оценки качества решений"
    )

    # === ДОМЕННО-СПЕЦИФИЧНЫЕ НАСТРОЙКИ ===
    psychology_validation_standards: str = Field(
        default="evidence_based,ethical_compliance,clinical_validity,cultural_sensitivity",
        description="Стандарты валидации для психологического домена"
    )
    astrology_accuracy_requirements: str = Field(
        default="traditional_accuracy,cultural_relevance,calculation_precision,interpretive_consistency",
        description="Требования точности для астрологического домена"
    )
    numerology_system_support: str = Field(
        default="pythagorean,chaldean,kabbalah",
        description="Поддерживаемые нумерологические системы"
    )
    business_success_metrics: str = Field(
        default="roi_impact,competitive_advantage,implementation_cost,measurable_outcomes",
        description="Метрики успеха для бизнес-домена"
    )

    # === ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ ===
    debug_mode: bool = Field(
        default=False,
        description="Режим отладки"
    )
    log_level: str = Field(
        default="INFO",
        description="Уровень логирования (DEBUG, INFO, WARNING, ERROR)"
    )
    save_mapping_results: bool = Field(
        default=True,
        description="Сохранять результаты маппинга"
    )
    results_output_format: str = Field(
        default="markdown",
        description="Формат вывода результатов (markdown, json, yaml)"
    )

    # === МЕТОДЫ ОБРАБОТКИ ===

    def get_secondary_languages_list(self) -> List[str]:
        """Получить список дополнительных языков."""
        return [lang.strip() for lang in self.secondary_languages.split(",") if lang.strip()]

    def get_target_regions_list(self) -> List[str]:
        """Получить список целевых регионов."""
        return [region.strip() for region in self.target_regions.split(",") if region.strip()]

    def get_knowledge_tags_list(self) -> List[str]:
        """Получить список тегов для поиска знаний."""
        base_tags = [tag.strip() for tag in self.knowledge_tags.split(",") if tag.strip()]
        # Добавляем доменный тег
        domain_tag = self.domain_type.replace("_", "-")
        if domain_tag not in base_tags:
            base_tags.append(domain_tag)
        return base_tags

    def get_pattern_scoring_weights(self) -> Dict[str, float]:
        """Получить веса для скоринга паттернов."""
        weights = {}
        for item in self.pattern_scoring_weights.split(","):
            if ":" in item:
                key, value = item.split(":", 1)
                try:
                    weights[key.strip()] = float(value.strip())
                except ValueError:
                    continue
        return weights

    def get_solution_quality_weights(self) -> Dict[str, float]:
        """Получить веса для оценки качества решений."""
        weights = {}
        for item in self.solution_quality_weights.split(","):
            if ":" in item:
                key, value = item.split(":", 1)
                try:
                    weights[key.strip()] = float(value.strip())
                except ValueError:
                    continue
        return weights

    def get_domain_validation_criteria(self) -> List[str]:
        """Получить критерии валидации для текущего домена."""
        criteria_map = {
            "psychology": self.psychology_validation_standards.split(","),
            "astrology": self.astrology_accuracy_requirements.split(","),
            "numerology": self.numerology_system_support.split(","),
            "business": self.business_success_metrics.split(",")
        }
        return [c.strip() for c in criteria_map.get(self.domain_type, []) if c.strip()]

    def get_llm_config_for_task(self, task_type: str) -> Dict[str, Any]:
        """Получить конфигурацию LLM для конкретного типа задачи."""
        model_map = {
            "pattern_mapping": self.llm_pattern_mapping_model,
            "solution_analysis": self.llm_solution_analysis_model,
            "blueprint_generation": self.llm_blueprint_generation_model,
            "domain_adaptation": self.llm_domain_adaptation_model
        }

        return {
            "model": model_map.get(task_type, self.llm_pattern_mapping_model),
            "provider": self.llm_provider,
            "base_url": self.llm_base_url,
            "api_key": self.llm_api_key,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "timeout": self.request_timeout
        }

    def is_delegation_enabled_for_task(self, task_complexity: str) -> bool:
        """Проверить, включено ли делегирование для задачи данной сложности."""
        if not self.enable_task_delegation:
            return False

        complexity_levels = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }

        threshold_level = complexity_levels.get(self.delegation_threshold, 2)
        task_level = complexity_levels.get(task_complexity, 2)

        return task_level >= threshold_level

@dataclass
class DomainConfig:
    """Конфигурация для конкретного домена."""
    name: str
    solution_types: List[str] = field(default_factory=list)
    pattern_categories: List[str] = field(default_factory=list)
    validation_criteria: List[str] = field(default_factory=list)
    adaptation_factors: List[str] = field(default_factory=list)
    quality_standards: List[str] = field(default_factory=list)
    specialized_tools: List[str] = field(default_factory=list)

def load_settings() -> SolutionPatternMapperSettings:
    """
    Загрузить настройки и проверить наличие обязательных переменных.

    Returns:
        Настроенный объект SolutionPatternMapperSettings

    Raises:
        ValueError: Если отсутствуют обязательные переменные окружения
    """
    load_dotenv()

    try:
        return SolutionPatternMapperSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e

def create_domain_config(
    domain_type: str = "psychology",
    project_type: str = "transformation_platform",
    framework: str = "pydantic_ai"
) -> DomainConfig:
    """
    Создать конфигурацию для конкретного домена.

    Args:
        domain_type: Тип домена
        project_type: Тип проекта
        framework: Технологический фреймворк

    Returns:
        Настроенная конфигурация домена
    """
    settings = load_settings()

    domain_configs = {
        "psychology": DomainConfig(
            name="Psychology",
            solution_types=[
                "diagnostic_solutions", "therapeutic_interventions", "educational_programs",
                "support_systems", "assessment_tools", "treatment_protocols"
            ],
            pattern_categories=[
                "evidence_based_practices", "therapeutic_modalities", "assessment_frameworks",
                "intervention_strategies", "recovery_models", "prevention_approaches"
            ],
            validation_criteria=settings.get_domain_validation_criteria(),
            adaptation_factors=[
                "age_group", "cultural_background", "severity_level",
                "comorbidities", "treatment_history", "resource_availability"
            ],
            quality_standards=["APA_guidelines", "evidence_based", "peer_reviewed"],
            specialized_tools=["psychological_assessment", "therapy_planning", "outcome_tracking"]
        ),

        "astrology": DomainConfig(
            name="Astrology",
            solution_types=[
                "consultation_frameworks", "calculation_systems", "interpretation_models",
                "prediction_algorithms", "compatibility_analysis", "timing_systems"
            ],
            pattern_categories=[
                "house_systems", "aspect_patterns", "planetary_transits",
                "chart_interpretation", "predictive_techniques", "compatibility_methods"
            ],
            validation_criteria=settings.get_domain_validation_criteria(),
            adaptation_factors=[
                "cultural_tradition", "astrological_system", "user_experience_level",
                "consultation_type", "time_sensitivity", "geographic_location"
            ],
            quality_standards=["traditional_accuracy", "modern_relevance", "cultural_sensitivity"],
            specialized_tools=["ephemeris_calculation", "chart_generation", "aspect_analysis"]
        ),

        "numerology": DomainConfig(
            name="Numerology",
            solution_types=[
                "calculation_engines", "interpretation_systems", "compatibility_analyzers",
                "timing_calculators", "name_analyzers", "business_consultancy"
            ],
            pattern_categories=[
                "core_numbers", "life_path_analysis", "compatibility_patterns",
                "timing_cycles", "name_vibrations", "business_numerology"
            ],
            validation_criteria=settings.get_domain_validation_criteria(),
            adaptation_factors=[
                "numerological_system", "cultural_context", "application_purpose",
                "user_beliefs", "complexity_preference", "output_format"
            ],
            quality_standards=["system_accuracy", "cultural_adaptation", "practical_utility"],
            specialized_tools=["number_calculation", "pattern_analysis", "compatibility_check"]
        ),

        "business": DomainConfig(
            name="Business",
            solution_types=[
                "strategic_frameworks", "operational_solutions", "analytical_tools",
                "optimization_systems", "decision_support", "automation_solutions"
            ],
            pattern_categories=[
                "business_models", "process_patterns", "organizational_structures",
                "market_strategies", "operational_frameworks", "technology_solutions"
            ],
            validation_criteria=settings.get_domain_validation_criteria(),
            adaptation_factors=[
                "industry_sector", "company_size", "market_maturity",
                "resource_constraints", "competitive_position", "growth_stage"
            ],
            quality_standards=["proven_effectiveness", "industry_best_practices", "measurable_results"],
            specialized_tools=["market_analysis", "financial_modeling", "process_optimization"]
        )
    }

    return domain_configs.get(domain_type, domain_configs["psychology"])

def get_universal_settings_template() -> Dict[str, Any]:
    """
    Получить шаблон универсальных настроек для создания .env файла.

    Returns:
        Словарь с шаблоном настроек
    """
    return {
        "# === ОСНОВНЫЕ НАСТРОЙКИ ===": "",
        "LLM_API_KEY": "your_api_key_here",
        "PROJECT_PATH": "",

        "# === КОНФИГУРАЦИЯ ДОМЕНА ===": "",
        "DOMAIN_TYPE": "psychology",  # psychology, astrology, numerology, business
        "PROJECT_TYPE": "transformation_platform",
        "FRAMEWORK": "pydantic_ai",

        "# === НАСТРОЙКИ МАППИНГА ===": "",
        "PATTERN_COMPLEXITY": "comprehensive",  # simple, comprehensive, advanced
        "SOLUTION_SCOPE": "domain_specific",  # universal, domain_specific, project_specific
        "VALIDATION_LEVEL": "standard",  # basic, standard, rigorous
        "ADAPTATION_MODE": "automatic",  # manual, automatic, hybrid

        "# === ЛОКАЛИЗАЦИЯ ===": "",
        "PRIMARY_LANGUAGE": "ukrainian",
        "SECONDARY_LANGUAGES": "polish,english",
        "TARGET_REGIONS": "ukraine,poland",

        "# === RAG И ARCHON ===": "",
        "AGENT_NAME": "universal_solution_pattern_mapper",
        "KNOWLEDGE_TAGS": "solution-patterns,pattern-mapping,agent-knowledge,pydantic-ai",
        "KNOWLEDGE_DOMAIN": "",
        "ARCHON_PROJECT_ID": "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",

        "# === МЕЖАГЕНТНОЕ ВЗАИМОДЕЙСТВИЕ ===": "",
        "ENABLE_TASK_DELEGATION": "true",
        "DELEGATION_THRESHOLD": "medium",

        "# === ДОПОЛНИТЕЛЬНЫЕ LLM КЛЮЧИ ===": "",
        "GEMINI_API_KEY": "",
        "OPENAI_API_KEY": "",
        "CLAUDE_API_KEY": "",

        "# === ОТЛАДКА ===": "",
        "DEBUG_MODE": "false",
        "LOG_LEVEL": "INFO",
        "SAVE_MAPPING_RESULTS": "true"
    }