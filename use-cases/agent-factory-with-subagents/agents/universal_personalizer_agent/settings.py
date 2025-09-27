# -*- coding: utf-8 -*-
"""
Настройки для Universal Personalizer Agent
Конфигурируемые параметры для персонализации в различных доменах
"""

import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv

class PersonalizerSettings(BaseSettings):
    """
    Настройки Universal Personalizer Agent с поддержкой переменных окружения.

    Поддерживает персонализацию для различных доменов:
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
        description="Тип домена для персонализации (psychology, astrology, numerology, business, etc.)"
    )
    project_type: str = Field(
        default="transformation_platform",
        description="Тип проекта (transformation_platform, educational_system, consultation_platform, etc.)"
    )
    framework: str = Field(
        default="pydantic_ai",
        description="Технологический фреймворк (pydantic_ai, fastapi, django, etc.)"
    )

    # === НАСТРОЙКИ ПЕРСОНАЛИЗАЦИИ ===
    personalization_mode: str = Field(
        default="adaptive",
        description="Режим персонализации (adaptive, rule_based, ml_driven, hybrid)"
    )
    personalization_depth: str = Field(
        default="comprehensive",
        description="Глубина персонализации (basic, comprehensive, deep)"
    )
    adaptation_strategy: str = Field(
        default="dynamic",
        description="Стратегия адаптации (static, dynamic, predictive)"
    )
    learning_approach: str = Field(
        default="behavioral",
        description="Подход к обучению (behavioral, preference_based, contextual, hybrid)"
    )

    # === АЛГОРИТМЫ ПЕРСОНАЛИЗАЦИИ ===
    recommendation_algorithm: str = Field(
        default="hybrid",
        description="Алгоритм рекомендаций (collaborative, content_based, hybrid, ml)"
    )
    similarity_threshold: float = Field(
        default=0.7,
        description="Порог схожести для рекомендаций"
    )
    min_interaction_count: int = Field(
        default=5,
        description="Минимальное количество взаимодействий для персонализации"
    )
    personalization_confidence_threshold: float = Field(
        default=0.6,
        description="Порог уверенности в персонализации"
    )

    # === ПОЛЬЗОВАТЕЛЬСКАЯ СЕГМЕНТАЦИЯ ===
    user_segmentation: str = Field(
        default="behavioral",
        description="Метод сегментации (demographic, behavioral, psychographic, hybrid)"
    )
    segment_update_frequency: str = Field(
        default="weekly",
        description="Частота обновления сегментов (daily, weekly, monthly)"
    )
    max_segments_per_user: int = Field(
        default=3,
        description="Максимальное количество сегментов на пользователя"
    )

    # === АДАПТАЦИЯ КОНТЕНТА ===
    content_adaptation: str = Field(
        default="comprehensive",
        description="Уровень адаптации контента (basic, comprehensive, advanced)"
    )
    real_time_optimization: bool = Field(
        default=True,
        description="Оптимизация в реальном времени"
    )
    a_b_testing_enabled: bool = Field(
        default=True,
        description="Включить A/B тестирование персонализации"
    )
    content_freshness_weight: float = Field(
        default=0.3,
        description="Вес свежести контента в алгоритмах"
    )

    # === ПРИВАТНОСТЬ И БЕЗОПАСНОСТЬ ===
    privacy_protection_level: str = Field(
        default="high",
        description="Уровень защиты приватности (basic, medium, high, maximum)"
    )
    data_anonymization: bool = Field(
        default=True,
        description="Анонимизация пользовательских данных"
    )
    consent_management: bool = Field(
        default=True,
        description="Управление согласием пользователей"
    )
    data_retention_days: int = Field(
        default=365,
        description="Срок хранения данных в днях"
    )

    # === ВРЕМЕННЫЕ ПАРАМЕТРЫ ===
    personalization_timeline: str = Field(
        default="immediate",
        description="Временные рамки персонализации (immediate, short_term, long_term)"
    )
    context_awareness: str = Field(
        default="full",
        description="Уровень контекстной осведомленности (minimal, partial, full)"
    )
    session_timeout_minutes: int = Field(
        default=30,
        description="Таймаут сессии в минутах"
    )

    # === КУЛЬТУРНАЯ АДАПТАЦИЯ ===
    cultural_adaptation: bool = Field(
        default=True,
        description="Включить культурную адаптацию"
    )
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
        default="universal_personalizer",
        description="Имя агента для RAG"
    )
    knowledge_tags: str = Field(
        default="personalization,user-experience,agent-knowledge,pydantic-ai",
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

    # === LLM КОНФИГУРАЦИЯ ===
    llm_provider: str = Field(
        default="qwen",
        description="Основной провайдер LLM (qwen, gemini, openai, claude)"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL для LLM API"
    )

    # Модели для разных типов задач персонализации
    llm_user_profiling_model: str = Field(
        default="qwen2.5:7b",
        description="Модель для анализа профиля пользователя"
    )
    llm_content_generation_model: str = Field(
        default="qwen2.5:14b",
        description="Модель для генерации персонализированного контента"
    )
    llm_ux_optimization_model: str = Field(
        default="qwen2.5:14b",
        description="Модель для оптимизации UX"
    )
    llm_effectiveness_analysis_model: str = Field(
        default="qwen2.5:7b",
        description="Модель для анализа эффективности"
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

    # === ВЕСОВЫЕ КОЭФФИЦИЕНТЫ ===
    personalization_weights: str = Field(
        default="relevance:0.25,engagement:0.20,satisfaction:0.20,effectiveness:0.15,accuracy:0.10,usability:0.10",
        description="Веса для оценки персонализации (через запятую, формат: критерий:вес)"
    )
    user_feedback_weight: float = Field(
        default=0.4,
        description="Вес обратной связи пользователя в алгоритмах"
    )
    behavioral_data_weight: float = Field(
        default=0.6,
        description="Вес поведенческих данных в алгоритмах"
    )

    # === ДОМЕННО-СПЕЦИФИЧНЫЕ НАСТРОЙКИ ===
    psychology_personalization_factors: str = Field(
        default="personality_traits,therapeutic_goals,cultural_background,psychological_state",
        description="Факторы персонализации для психологического домена"
    )
    astrology_personalization_factors: str = Field(
        default="birth_chart_data,cultural_tradition,experience_level,spiritual_orientation",
        description="Факторы персонализации для астрологического домена"
    )
    numerology_personalization_factors: str = Field(
        default="core_numbers,life_path,cultural_context,application_purpose",
        description="Факторы персонализации для нумерологического домена"
    )
    business_personalization_factors: str = Field(
        default="industry_sector,company_size,role_level,business_goals",
        description="Факторы персонализации для бизнес-домена"
    )

    # === МЕТРИКИ КАЧЕСТВА ===
    min_personalization_quality: float = Field(
        default=0.7,
        description="Минимальное качество персонализации"
    )
    target_user_satisfaction: float = Field(
        default=0.85,
        description="Целевой уровень удовлетворенности пользователей"
    )
    max_personalization_error_rate: float = Field(
        default=0.05,
        description="Максимальный уровень ошибок персонализации"
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
    save_personalization_logs: bool = Field(
        default=True,
        description="Сохранять логи персонализации"
    )
    personalization_output_format: str = Field(
        default="json",
        description="Формат вывода персонализации (json, yaml, xml)"
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

    def get_personalization_weights(self) -> Dict[str, float]:
        """Получить веса для оценки персонализации."""
        weights = {}
        for item in self.personalization_weights.split(","):
            if ":" in item:
                key, value = item.split(":", 1)
                try:
                    weights[key.strip()] = float(value.strip())
                except ValueError:
                    continue
        return weights

    def get_domain_personalization_factors(self) -> List[str]:
        """Получить факторы персонализации для текущего домена."""
        factors_map = {
            "psychology": self.psychology_personalization_factors.split(","),
            "astrology": self.astrology_personalization_factors.split(","),
            "numerology": self.numerology_personalization_factors.split(","),
            "business": self.business_personalization_factors.split(",")
        }
        return [f.strip() for f in factors_map.get(self.domain_type, []) if f.strip()]

    def get_llm_config_for_task(self, task_type: str) -> Dict[str, Any]:
        """Получить конфигурацию LLM для конкретного типа задачи персонализации."""
        model_map = {
            "user_profiling": self.llm_user_profiling_model,
            "content_generation": self.llm_content_generation_model,
            "ux_optimization": self.llm_ux_optimization_model,
            "effectiveness_analysis": self.llm_effectiveness_analysis_model
        }

        return {
            "model": model_map.get(task_type, self.llm_user_profiling_model),
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

    def get_privacy_settings(self) -> Dict[str, Any]:
        """Получить настройки приватности."""
        return {
            "protection_level": self.privacy_protection_level,
            "data_anonymization": self.data_anonymization,
            "consent_management": self.consent_management,
            "data_retention_days": self.data_retention_days,
            "session_timeout_minutes": self.session_timeout_minutes
        }

    def get_personalization_algorithm_config(self) -> Dict[str, Any]:
        """Получить конфигурацию алгоритмов персонализации."""
        return {
            "recommendation_algorithm": self.recommendation_algorithm,
            "similarity_threshold": self.similarity_threshold,
            "min_interaction_count": self.min_interaction_count,
            "confidence_threshold": self.personalization_confidence_threshold,
            "user_feedback_weight": self.user_feedback_weight,
            "behavioral_data_weight": self.behavioral_data_weight,
            "content_freshness_weight": self.content_freshness_weight
        }

    def get_quality_requirements(self) -> Dict[str, float]:
        """Получить требования к качеству персонализации."""
        return {
            "min_personalization_quality": self.min_personalization_quality,
            "target_user_satisfaction": self.target_user_satisfaction,
            "max_error_rate": self.max_personalization_error_rate
        }

@dataclass
class PersonalizationConfig:
    """Конфигурация персонализации для конкретного домена."""
    name: str
    personalization_factors: List[str] = field(default_factory=list)
    content_types: List[str] = field(default_factory=list)
    adaptation_rules: List[str] = field(default_factory=list)
    quality_metrics: List[str] = field(default_factory=list)
    privacy_requirements: List[str] = field(default_factory=list)
    algorithms: List[str] = field(default_factory=list)

def load_settings() -> PersonalizerSettings:
    """
    Загрузить настройки и проверить наличие обязательных переменных.

    Returns:
        Настроенный объект PersonalizerSettings

    Raises:
        ValueError: Если отсутствуют обязательные переменные окружения
    """
    load_dotenv()

    try:
        return PersonalizerSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e

def create_personalization_config(
    domain_type: str = "psychology",
    project_type: str = "transformation_platform",
    personalization_mode: str = "adaptive"
) -> PersonalizationConfig:
    """
    Создать конфигурацию персонализации для конкретного домена.

    Args:
        domain_type: Тип домена
        project_type: Тип проекта
        personalization_mode: Режим персонализации

    Returns:
        Настроенная конфигурация персонализации
    """
    settings = load_settings()

    domain_configs = {
        "psychology": PersonalizationConfig(
            name="Psychology Personalization",
            personalization_factors=[
                "personality_traits", "psychological_state", "therapeutic_goals",
                "cultural_background", "age_group", "severity_level"
            ],
            content_types=[
                "therapeutic_content", "educational_materials", "assessment_tools",
                "progress_tracking", "motivational_messages", "intervention_strategies"
            ],
            adaptation_rules=[
                "evidence_based_matching", "therapeutic_alliance", "cultural_sensitivity",
                "trauma_informed", "progress_based_adjustment", "safety_prioritization"
            ],
            quality_metrics=[
                "therapeutic_engagement", "outcome_improvement", "user_satisfaction",
                "content_relevance", "session_completion", "goal_achievement"
            ],
            privacy_requirements=["hipaa_compliance", "therapeutic_confidentiality", "consent_management"],
            algorithms=["collaborative_filtering", "content_based", "therapeutic_matching"]
        ),

        "astrology": PersonalizationConfig(
            name="Astrology Personalization",
            personalization_factors=[
                "birth_chart_data", "cultural_tradition", "astrological_preferences",
                "experience_level", "consultation_type", "spiritual_orientation"
            ],
            content_types=[
                "personal_horoscopes", "compatibility_analysis", "timing_guidance",
                "chart_interpretations", "educational_content", "spiritual_insights"
            ],
            adaptation_rules=[
                "traditional_accuracy", "cultural_context", "personal_resonance",
                "system_preference", "depth_level_matching", "timing_sensitivity"
            ],
            quality_metrics=[
                "accuracy_perception", "personal_relevance", "spiritual_connection",
                "guidance_usefulness", "cultural_appropriateness", "user_engagement"
            ],
            privacy_requirements=["birth_data_protection", "consultation_confidentiality"],
            algorithms=["astrological_matching", "cultural_filtering", "tradition_based"]
        ),

        "numerology": PersonalizationConfig(
            name="Numerology Personalization",
            personalization_factors=[
                "core_numbers", "life_path", "personal_year", "name_vibrations",
                "cultural_context", "numerological_system_preference"
            ],
            content_types=[
                "personal_numerology_reports", "compatibility_analysis", "timing_guidance",
                "business_numerology", "name_analysis", "cycles_interpretation"
            ],
            adaptation_rules=[
                "system_consistency", "cultural_relevance", "practical_application",
                "personal_resonance", "accuracy_validation", "actionable_insights"
            ],
            quality_metrics=[
                "calculation_accuracy", "personal_relevance", "practical_usefulness",
                "cultural_appropriateness", "insight_quality", "user_satisfaction"
            ],
            privacy_requirements=["personal_data_protection", "calculation_privacy"],
            algorithms=["number_pattern_matching", "system_based_filtering", "cultural_adaptation"]
        ),

        "business": PersonalizationConfig(
            name="Business Personalization",
            personalization_factors=[
                "industry_sector", "company_size", "role_level", "business_goals",
                "market_position", "growth_stage", "technology_adoption"
            ],
            content_types=[
                "strategic_recommendations", "market_insights", "operational_guidance",
                "performance_analytics", "training_materials", "decision_support"
            ],
            adaptation_rules=[
                "industry_relevance", "company_size_appropriateness", "role_based_filtering",
                "goal_alignment", "market_context", "resource_constraints"
            ],
            quality_metrics=[
                "business_impact", "roi_improvement", "decision_quality",
                "operational_efficiency", "strategic_alignment", "user_adoption"
            ],
            privacy_requirements=["commercial_confidentiality", "competitive_data_protection"],
            algorithms=["role_based_filtering", "industry_clustering", "business_value_optimization"]
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

        "# === НАСТРОЙКИ ПЕРСОНАЛИЗАЦИИ ===": "",
        "PERSONALIZATION_MODE": "adaptive",  # adaptive, rule_based, ml_driven, hybrid
        "PERSONALIZATION_DEPTH": "comprehensive",  # basic, comprehensive, deep
        "ADAPTATION_STRATEGY": "dynamic",  # static, dynamic, predictive
        "LEARNING_APPROACH": "behavioral",  # behavioral, preference_based, contextual, hybrid

        "# === АЛГОРИТМЫ ===": "",
        "RECOMMENDATION_ALGORITHM": "hybrid",  # collaborative, content_based, hybrid, ml
        "SIMILARITY_THRESHOLD": "0.7",
        "MIN_INTERACTION_COUNT": "5",
        "PERSONALIZATION_CONFIDENCE_THRESHOLD": "0.6",

        "# === ПОЛЬЗОВАТЕЛЬСКАЯ СЕГМЕНТАЦИЯ ===": "",
        "USER_SEGMENTATION": "behavioral",  # demographic, behavioral, psychographic, hybrid
        "SEGMENT_UPDATE_FREQUENCY": "weekly",
        "MAX_SEGMENTS_PER_USER": "3",

        "# === ПРИВАТНОСТЬ И БЕЗОПАСНОСТЬ ===": "",
        "PRIVACY_PROTECTION_LEVEL": "high",  # basic, medium, high, maximum
        "DATA_ANONYMIZATION": "true",
        "CONSENT_MANAGEMENT": "true",
        "DATA_RETENTION_DAYS": "365",

        "# === КУЛЬТУРНАЯ АДАПТАЦИЯ ===": "",
        "CULTURAL_ADAPTATION": "true",
        "PRIMARY_LANGUAGE": "ukrainian",
        "SECONDARY_LANGUAGES": "polish,english",
        "TARGET_REGIONS": "ukraine,poland",

        "# === RAG И ARCHON ===": "",
        "AGENT_NAME": "universal_personalizer",
        "KNOWLEDGE_TAGS": "personalization,user-experience,agent-knowledge,pydantic-ai",
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
        "SAVE_PERSONALIZATION_LOGS": "true"
    }