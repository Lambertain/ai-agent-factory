# -*- coding: utf-8 -*-
"""
Universal Content Generator Agent - Настройки

Конфигурация и настройки для универсального агента генерации контента.
"""

import os
from typing import List, Dict, Any, Optional
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class ContentGeneratorSettings(BaseSettings):
    """
    Настройки для Universal Content Generator Agent.

    Поддерживает конфигурацию через переменные окружения
    с адаптацией под различные типы контента и домены.
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # === ОСНОВНЫЕ НАСТРОЙКИ ===
    llm_api_key: str = Field(..., description="API ключ для LLM провайдера")
    project_path: str = Field(default="", description="Путь к проекту")

    # === КОНФИГУРАЦИЯ КОНТЕНТА ===
    content_type: str = Field(default="blog_post", description="Тип контента по умолчанию")
    domain_type: str = Field(default="technology", description="Домен контента по умолчанию")
    target_audience: str = Field(default="general", description="Целевая аудитория по умолчанию")
    content_style: str = Field(default="informative", description="Стиль контента по умолчанию")
    content_length: str = Field(default="medium", description="Длина контента по умолчанию")
    primary_language: str = Field(default="ukrainian", description="Основной язык контента")

    # === НАСТРОЙКИ КАЧЕСТВА ===
    quality_standard: str = Field(default="high", description="Стандарт качества контента")
    readability_level: str = Field(default="general", description="Уровень читабельности")
    creativity_level: str = Field(default="balanced", description="Уровень креативности")
    tone_formality: str = Field(default="balanced", description="Формальность тона")

    # === SEO И ОПТИМИЗАЦИЯ ===
    seo_optimization: bool = Field(default=True, description="Включить SEO оптимизацию")
    seo_primary_keyword: str = Field(default="", description="Основное ключевое слово")
    seo_secondary_keywords: str = Field(default="", description="Дополнительные ключевые слова (через запятую)")
    seo_meta_description: bool = Field(default=True, description="Генерировать мета-описания")
    seo_internal_linking: bool = Field(default=False, description="Предлагать внутренние ссылки")

    # === СТРУКТУРА КОНТЕНТА ===
    content_structure: str = Field(default="standard", description="Структура контента")
    include_introduction: bool = Field(default=True, description="Включать введение")
    include_conclusion: bool = Field(default=True, description="Включать заключение")
    include_call_to_action: bool = Field(default=True, description="Включать призыв к действию")
    section_headings_style: str = Field(default="descriptive", description="Стиль заголовков секций")

    # === КУЛЬТУРНАЯ АДАПТАЦИЯ ===
    cultural_adaptation: bool = Field(default=True, description="Включить культурную адаптацию")
    target_region: str = Field(default="ukraine", description="Целевой регион")
    secondary_languages: str = Field(default="polish,english", description="Дополнительные языки")
    local_references: bool = Field(default=True, description="Использовать местные ссылки")
    currency_format: str = Field(default="UAH", description="Формат валюты")
    date_format: str = Field(default="DD.MM.YYYY", description="Формат даты")

    # === ТВОРЧЕСКИЕ ПАРАМЕТРЫ ===
    humor_usage: str = Field(default="minimal", description="Использование юмора")
    storytelling_elements: bool = Field(default=False, description="Элементы storytelling")
    personal_anecdotes: bool = Field(default=False, description="Личные анекдоты")
    brand_voice: str = Field(default="neutral", description="Голос бренда")

    # === ТЕХНИЧЕСКИЕ ПАРАМЕТРЫ ===
    output_format: str = Field(default="markdown", description="Формат вывода")
    include_metadata: bool = Field(default=True, description="Включать метаданные")
    include_word_count: bool = Field(default=True, description="Включать подсчет слов")
    include_reading_time: bool = Field(default=True, description="Включать время чтения")
    generate_excerpt: bool = Field(default=True, description="Генерировать выдержку")

    # === LLM ПРОВАЙДЕРЫ И МОДЕЛИ ===
    llm_provider: str = Field(default="qwen", description="Провайдер LLM")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Модели для разных типов контента
    llm_blog_model: str = Field(default="qwen2.5-32b-instruct", description="Модель для блог-постов")
    llm_documentation_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Модель для документации")
    llm_marketing_model: str = Field(default="qwen2.5-32b-instruct", description="Модель для маркетинга")
    llm_educational_model: str = Field(default="qwen2.5-32b-instruct", description="Модель для образовательного контента")
    llm_social_model: str = Field(default="qwen2.5-32b-instruct", description="Модель для социальных сетей")

    # Альтернативные API ключи
    gemini_api_key: str = Field(default="", description="Google Gemini API ключ")
    openai_api_key: str = Field(default="", description="OpenAI API ключ")
    claude_api_key: str = Field(default="", description="Anthropic Claude API ключ")

    # === НАСТРОЙКИ ПРОИЗВОДИТЕЛЬНОСТИ ===
    max_tokens: int = Field(default=4096, description="Максимальное количество токенов")
    temperature: float = Field(default=0.6, description="Температура генерации")
    request_timeout: int = Field(default=120, description="Таймаут запроса в секундах")
    retry_attempts: int = Field(default=3, description="Количество попыток при ошибке")

    # === ВЕСОВЫЕ КОЭФФИЦИЕНТЫ ===
    content_quality_weights: str = Field(
        default="clarity:0.25,engagement:0.20,accuracy:0.20,seo:0.15,structure:0.10,creativity:0.10",
        description="Весовые коэффициенты качества контента"
    )
    audience_preference_weight: float = Field(default=0.6, description="Вес предпочтений аудитории")
    seo_importance_weight: float = Field(default=0.3, description="Важность SEO факторов")
    brand_consistency_weight: float = Field(default=0.1, description="Важность соответствия бренду")

    # === ДОМЕННО-СПЕЦИФИЧНЫЕ ФАКТОРЫ ===
    # Технологии
    technology_content_factors: str = Field(
        default="technical_accuracy,code_examples,latest_trends,practical_applications",
        description="Факторы для технологического контента"
    )

    # Бизнес
    business_content_factors: str = Field(
        default="roi_focus,case_studies,industry_insights,actionable_advice",
        description="Факторы для бизнес-контента"
    )

    # Здоровье
    health_content_factors: str = Field(
        default="evidence_based,safety_disclaimers,expert_review,accessibility",
        description="Факторы для контента о здоровье"
    )

    # Образование
    education_content_factors: str = Field(
        default="learning_objectives,progressive_difficulty,interactive_elements,assessment_ready",
        description="Факторы для образовательного контента"
    )

    # === МЕТРИКИ КАЧЕСТВА ===
    min_content_quality_score: float = Field(default=0.7, description="Минимальный балл качества контента")
    target_engagement_score: float = Field(default=0.8, description="Целевой уровень вовлечения")
    max_content_error_rate: float = Field(default=0.05, description="Максимальная частота ошибок в контенте")

    # === RAG И KNOWLEDGE BASE ===
    agent_name: str = Field(default="universal_content_generator", description="Имя агента")
    knowledge_tags: str = Field(
        default="content-generation,copywriting,seo,agent-knowledge,pydantic-ai",
        description="Теги базы знаний (через запятую)"
    )
    knowledge_domain: str = Field(default="", description="Домен базы знаний")
    archon_project_id: str = Field(default="", description="ID проекта в Archon")

    # === МЕЖАГЕНТНОЕ ВЗАИМОДЕЙСТВИЕ ===
    enable_task_delegation: bool = Field(default=True, description="Включить делегирование задач")
    delegation_threshold: str = Field(default="medium", description="Порог делегирования")
    max_delegation_depth: int = Field(default=3, description="Максимальная глубина делегирования")

    # === ОТЛАДКА И ЛОГИРОВАНИЕ ===
    debug_mode: bool = Field(default=False, description="Режим отладки")
    log_level: str = Field(default="INFO", description="Уровень логирования")
    save_content_logs: bool = Field(default=True, description="Сохранять логи генерации контента")
    content_output_format: str = Field(default="json", description="Формат вывода контента")

    def get_seo_keywords_list(self) -> List[str]:
        """Получить список SEO ключевых слов."""
        if not self.seo_secondary_keywords:
            return []
        return [kw.strip() for kw in self.seo_secondary_keywords.split(",")]

    def get_knowledge_tags_list(self) -> List[str]:
        """Получить список тегов базы знаний."""
        return [tag.strip() for tag in self.knowledge_tags.split(",")]

    def get_secondary_languages_list(self) -> List[str]:
        """Получить список дополнительных языков."""
        return [lang.strip() for lang in self.secondary_languages.split(",")]

    def get_content_quality_weights(self) -> Dict[str, float]:
        """Получить весовые коэффициенты качества контента."""
        weights = {}
        try:
            for weight_pair in self.content_quality_weights.split(","):
                key, value = weight_pair.split(":")
                weights[key.strip()] = float(value.strip())
        except ValueError:
            # Значения по умолчанию при ошибке парсинга
            weights = {
                "clarity": 0.25,
                "engagement": 0.20,
                "accuracy": 0.20,
                "seo": 0.15,
                "structure": 0.10,
                "creativity": 0.10
            }
        return weights

    def get_domain_factors(self, domain: str) -> List[str]:
        """Получить факторы для конкретного домена."""
        domain_factors_map = {
            "technology": self.technology_content_factors,
            "business": self.business_content_factors,
            "health": self.health_content_factors,
            "education": self.education_content_factors
        }

        factors_str = domain_factors_map.get(domain, "")
        if not factors_str:
            return []

        return [factor.strip() for factor in factors_str.split(",")]


class ContentGenerationConfig:
    """
    Конфигурация процесса генерации контента.

    Объединяет настройки и предоставляет удобные методы
    для работы с конфигурацией генерации.
    """

    def __init__(self, settings: ContentGeneratorSettings):
        self.settings = settings
        self._content_type_configs = self._initialize_content_type_configs()
        self._domain_configs = self._initialize_domain_configs()

    def _initialize_content_type_configs(self) -> Dict[str, Dict[str, Any]]:
        """Инициализация конфигураций по типам контента."""
        return {
            "blog_post": {
                "recommended_length": "medium",
                "seo_importance": "high",
                "creativity_level": "balanced",
                "structure": "introduction-body-conclusion",
                "engagement_priority": True
            },
            "documentation": {
                "recommended_length": "comprehensive",
                "seo_importance": "low",
                "creativity_level": "conservative",
                "structure": "hierarchical",
                "technical_accuracy": True
            },
            "marketing": {
                "recommended_length": "short",
                "seo_importance": "high",
                "creativity_level": "creative",
                "structure": "hook-benefits-cta",
                "conversion_focused": True
            },
            "educational": {
                "recommended_length": "long",
                "seo_importance": "medium",
                "creativity_level": "balanced",
                "structure": "learning-objectives-content-assessment",
                "pedagogy_focused": True
            },
            "social_media": {
                "recommended_length": "short",
                "seo_importance": "medium",
                "creativity_level": "highly_creative",
                "structure": "hook-content-hashtags",
                "viral_potential": True
            },
            "email": {
                "recommended_length": "short",
                "seo_importance": "low",
                "creativity_level": "balanced",
                "structure": "subject-body-cta",
                "personalization": True
            }
        }

    def _initialize_domain_configs(self) -> Dict[str, Dict[str, Any]]:
        """Инициализация конфигураций по доменам."""
        return {
            "technology": {
                "expertise_required": "high",
                "terminology_complexity": "high",
                "example_importance": "high",
                "update_frequency": "high"
            },
            "business": {
                "expertise_required": "medium",
                "terminology_complexity": "medium",
                "case_study_importance": "high",
                "roi_focus": "high"
            },
            "health": {
                "expertise_required": "high",
                "disclaimer_required": True,
                "evidence_based": True,
                "regulatory_compliance": "high"
            },
            "education": {
                "expertise_required": "medium",
                "learning_structure": True,
                "assessment_integration": "medium",
                "accessibility": "high"
            },
            "finance": {
                "expertise_required": "high",
                "regulatory_compliance": "high",
                "risk_disclaimers": True,
                "data_accuracy": "critical"
            },
            "lifestyle": {
                "expertise_required": "low",
                "visual_elements": "high",
                "trend_awareness": "high",
                "personal_touch": "high"
            }
        }

    def get_optimized_config(
        self,
        content_type: str,
        domain_type: str,
        target_audience: str
    ) -> Dict[str, Any]:
        """
        Получить оптимизированную конфигурацию для конкретной задачи.

        Args:
            content_type: Тип контента
            domain_type: Домен
            target_audience: Целевая аудитория

        Returns:
            Оптимизированная конфигурация
        """
        base_config = {
            "content_type": content_type,
            "domain_type": domain_type,
            "target_audience": target_audience,
            "language": self.settings.primary_language,
            "quality_standard": self.settings.quality_standard
        }

        # Добавление конфигурации типа контента
        if content_type in self._content_type_configs:
            base_config.update(self._content_type_configs[content_type])

        # Добавление конфигурации домена
        if domain_type in self._domain_configs:
            base_config.update(self._domain_configs[domain_type])

        # Адаптация под аудиторию
        audience_adaptations = {
            "beginners": {
                "complexity_level": "simple",
                "explanation_depth": "high",
                "example_count": "many"
            },
            "professionals": {
                "complexity_level": "advanced",
                "efficiency_focus": "high",
                "actionable_content": "high"
            },
            "experts": {
                "complexity_level": "expert",
                "innovation_focus": "high",
                "research_depth": "high"
            }
        }

        if target_audience in audience_adaptations:
            base_config.update(audience_adaptations[target_audience])

        return base_config

    def should_use_seo(self, content_type: str) -> bool:
        """Определить нужно ли использовать SEO для типа контента."""
        seo_important_types = ["blog_post", "marketing", "social_media"]
        return self.settings.seo_optimization and content_type in seo_important_types

    def get_recommended_model(self, content_type: str) -> str:
        """Получить рекомендуемую модель для типа контента."""
        model_mapping = {
            "blog_post": self.settings.llm_blog_model,
            "documentation": self.settings.llm_documentation_model,
            "marketing": self.settings.llm_marketing_model,
            "educational": self.settings.llm_educational_model,
            "social_media": self.settings.llm_social_model,
            "email": self.settings.llm_marketing_model  # Используем маркетинговую модель для email
        }

        return model_mapping.get(content_type, self.settings.llm_blog_model)


def load_settings() -> ContentGeneratorSettings:
    """
    Загрузить настройки из переменных окружения.

    Returns:
        Настроенный экземпляр ContentGeneratorSettings
    """
    load_dotenv()

    try:
        return ContentGeneratorSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def create_content_generation_config(settings: ContentGeneratorSettings = None) -> ContentGenerationConfig:
    """
    Создать конфигурацию генерации контента.

    Args:
        settings: Настройки (если не указаны, загружаются автоматически)

    Returns:
        Конфигурация генерации контента
    """
    if settings is None:
        settings = load_settings()

    return ContentGenerationConfig(settings)


def get_universal_settings_template() -> Dict[str, str]:
    """
    Получить шаблон универсальных настроек для .env файла.

    Returns:
        Словарь с описанием всех доступных настроек
    """
    return {
        "# === ОСНОВНЫЕ НАСТРОЙКИ ===": "",
        "LLM_API_KEY": "your_api_key_here",
        "PROJECT_PATH": "",

        "# === КОНФИГУРАЦИЯ КОНТЕНТА ===": "",
        "CONTENT_TYPE": "blog_post  # blog_post, documentation, marketing, educational, social_media, email",
        "DOMAIN_TYPE": "technology  # technology, business, health, education, finance, lifestyle",
        "TARGET_AUDIENCE": "general  # general, professionals, beginners, experts, students, customers",
        "CONTENT_STYLE": "informative  # informative, persuasive, educational, entertaining, formal, casual",
        "CONTENT_LENGTH": "medium  # short, medium, long, comprehensive",
        "PRIMARY_LANGUAGE": "ukrainian",

        "# === НАСТРОЙКИ КАЧЕСТВА ===": "",
        "QUALITY_STANDARD": "high  # basic, standard, high, premium",
        "READABILITY_LEVEL": "general  # simple, general, advanced, academic",
        "CREATIVITY_LEVEL": "balanced  # conservative, balanced, creative, highly_creative",

        "# === SEO И ОПТИМИЗАЦИЯ ===": "",
        "SEO_OPTIMIZATION": "true",
        "SEO_PRIMARY_KEYWORD": "",
        "SEO_SECONDARY_KEYWORDS": "",
        "SEO_META_DESCRIPTION": "true",

        "# === КУЛЬТУРНАЯ АДАПТАЦИЯ ===": "",
        "CULTURAL_ADAPTATION": "true",
        "TARGET_REGION": "ukraine",
        "SECONDARY_LANGUAGES": "polish,english",
        "CURRENCY_FORMAT": "UAH",

        "# === LLM ПРОВАЙДЕРЫ ===": "",
        "LLM_PROVIDER": "qwen",
        "LLM_BASE_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "GEMINI_API_KEY": "",
        "OPENAI_API_KEY": "",
        "CLAUDE_API_KEY": "",

        "# === RAG И KNOWLEDGE BASE ===": "",
        "AGENT_NAME": "universal_content_generator",
        "KNOWLEDGE_TAGS": "content-generation,copywriting,seo,agent-knowledge,pydantic-ai",
        "ARCHON_PROJECT_ID": "",

        "# === МЕЖАГЕНТНОЕ ВЗАИМОДЕЙСТВИЕ ===": "",
        "ENABLE_TASK_DELEGATION": "true",
        "DELEGATION_THRESHOLD": "medium",

        "# === ОТЛАДКА ===": "",
        "DEBUG_MODE": "false",
        "LOG_LEVEL": "INFO"
    }


# === ЭКСПОРТ ===

__all__ = [
    "ContentGeneratorSettings",
    "ContentGenerationConfig",
    "load_settings",
    "create_content_generation_config",
    "get_universal_settings_template"
]