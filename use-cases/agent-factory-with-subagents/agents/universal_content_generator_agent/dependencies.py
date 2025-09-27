# -*- coding: utf-8 -*-
"""
Universal Content Generator Agent - Управление зависимостями

Конфигурация зависимостей для универсального агента генерации контента
с поддержкой различных типов контента, доменов и целевых аудиторий.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from pathlib import Path


@dataclass
class ContentGeneratorDependencies:
    """
    Зависимости для Universal Content Generator Agent.

    Поддерживает конфигурацию для различных типов контента:
    - Блог-посты и статьи
    - Документация (техническая, пользовательская)
    - Маркетинговые материалы
    - Образовательный контент
    - Контент для социальных сетей
    - Электронные письма
    - Пресс-релизы
    """

    # === ОСНОВНЫЕ НАСТРОЙКИ ===
    api_key: str
    project_path: str = ""

    # === КОНФИГУРАЦИЯ КОНТЕНТА ===
    content_type: str = "blog_post"  # blog_post, documentation, marketing, educational, social_media, email, press_release
    domain_type: str = "technology"  # technology, business, health, education, finance, lifestyle, science
    target_audience: str = "general"  # general, professionals, beginners, experts, students, customers
    content_style: str = "informative"  # informative, persuasive, educational, entertaining, formal, casual
    content_length: str = "medium"  # short, medium, long, comprehensive
    language: str = "ukrainian"  # ukrainian, english, polish, multilingual

    # === СПЕЦИАЛИЗАЦИЯ ПО ТИПАМ КОНТЕНТА ===

    # Блог-посты и статьи
    blog_article_focus: str = "thought_leadership"  # thought_leadership, how_to, news, opinion, review
    blog_seo_optimization: bool = True
    blog_target_keywords: List[str] = field(default_factory=list)
    blog_word_count_target: int = 800

    # Документация
    documentation_type: str = "user_guide"  # api, user_guide, technical_spec, installation, tutorial
    documentation_technical_level: str = "intermediate"  # beginner, intermediate, advanced, expert
    documentation_format: str = "markdown"  # markdown, rst, html, wiki, pdf
    documentation_include_examples: bool = True

    # Маркетинговые материалы
    marketing_campaign_type: str = "content_marketing"  # content_marketing, email_campaign, social_ads, landing_page
    marketing_goal: str = "awareness"  # awareness, conversion, retention, engagement, lead_generation
    marketing_tone: str = "professional"  # professional, friendly, urgent, playful, authoritative
    marketing_call_to_action: str = "learn_more"  # learn_more, buy_now, sign_up, download, contact_us

    # Образовательный контент
    educational_subject: str = "general"  # technology, business, science, arts, languages, skills
    educational_level: str = "intermediate"  # beginner, intermediate, advanced, professional
    educational_format: str = "structured"  # structured, narrative, interactive, modular
    educational_learning_style: str = "visual"  # visual, auditory, kinesthetic, reading
    educational_include_assessments: bool = False

    # Социальные сети
    social_platform: str = "general"  # facebook, instagram, linkedin, twitter, youtube, tiktok
    social_post_type: str = "standard"  # standard, story, reel, carousel, video, live
    social_engagement_goal: str = "likes"  # likes, shares, comments, saves, clicks, follows
    social_hashtag_strategy: str = "moderate"  # minimal, moderate, extensive, trending

    # Электронные письма
    email_type: str = "newsletter"  # newsletter, welcome, promotional, transactional, follow_up
    email_personalization_level: str = "medium"  # low, medium, high, dynamic
    email_subject_line_style: str = "informative"  # informative, curious, urgent, benefit_focused

    # === НАСТРОЙКИ КАЧЕСТВА И СТИЛЯ ===
    quality_standard: str = "high"  # basic, standard, high, premium
    readability_level: str = "general"  # simple, general, advanced, academic
    tone_formality: str = "balanced"  # formal, semi_formal, balanced, casual, informal
    brand_voice: str = "neutral"  # neutral, authoritative, friendly, innovative, trustworthy

    # === SEO И ОПТИМИЗАЦИЯ ===
    seo_optimization: bool = True
    seo_primary_keyword: str = ""
    seo_secondary_keywords: List[str] = field(default_factory=list)
    seo_meta_description: bool = True
    seo_internal_linking: bool = False

    # === СТРУКТУРИРОВАНИЕ КОНТЕНТА ===
    content_structure: str = "standard"  # standard, listicle, how_to, case_study, comparison, storytelling
    include_introduction: bool = True
    include_conclusion: bool = True
    include_call_to_action: bool = True
    section_headings_style: str = "descriptive"  # descriptive, creative, seo_optimized, numbered

    # === АДАПТАЦИЯ И ЛОКАЛИЗАЦИЯ ===
    cultural_adaptation: bool = True
    regional_preferences: str = "ukraine"  # ukraine, poland, usa, eu, global
    local_references: bool = True
    currency_format: str = "UAH"  # UAH, USD, EUR, PLN
    date_format: str = "DD.MM.YYYY"

    # === ТВОРЧЕСКИЕ ПАРАМЕТРЫ ===
    creativity_level: str = "balanced"  # conservative, balanced, creative, highly_creative
    humor_usage: str = "minimal"  # none, minimal, moderate, high
    storytelling_elements: bool = False
    personal_anecdotes: bool = False

    # === ТЕХНИЧЕСКИЕ ПАРАМЕТРЫ ===
    output_format: str = "markdown"  # markdown, html, plain_text, rich_text, json
    include_metadata: bool = True
    include_word_count: bool = True
    include_reading_time: bool = True
    generate_excerpt: bool = True

    # === RAG И KNOWLEDGE BASE ===
    agent_name: str = "universal_content_generator"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "content-generation", "copywriting", "seo", "agent-knowledge", "pydantic-ai"
    ])
    knowledge_domain: str = ""
    archon_project_id: str = ""

    # === МЕЖАГЕНТНОЕ ВЗАИМОДЕЙСТВИЕ ===
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"  # low, medium, high
    max_delegation_depth: int = 3

    # === КАСТОМИЗАЦИЯ ПО ДОМЕНАМ ===
    domain_specific_config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Пост-инициализация с настройкой доменно-специфичных параметров."""
        self._setup_domain_specific_config()
        self._setup_content_type_defaults()
        self._validate_configuration()

    def _setup_domain_specific_config(self):
        """Настройка конфигурации в зависимости от домена."""
        domain_configs = {
            "technology": {
                "preferred_style": "technical",
                "target_audience": "professionals",
                "technical_depth": "intermediate",
                "include_code_examples": True,
                "trending_topics": ["AI", "cloud", "security", "devops", "mobile"]
            },
            "business": {
                "preferred_style": "professional",
                "target_audience": "executives",
                "focus_areas": ["strategy", "growth", "efficiency", "innovation"],
                "include_case_studies": True,
                "data_driven": True
            },
            "health": {
                "preferred_style": "educational",
                "target_audience": "general",
                "safety_disclaimers": True,
                "evidence_based": True,
                "expert_review": True
            },
            "education": {
                "preferred_style": "educational",
                "target_audience": "students",
                "learning_objectives": True,
                "interactive_elements": True,
                "assessment_ready": True
            },
            "finance": {
                "preferred_style": "authoritative",
                "target_audience": "investors",
                "regulatory_compliance": True,
                "data_accuracy": "high",
                "risk_disclaimers": True
            },
            "lifestyle": {
                "preferred_style": "engaging",
                "target_audience": "general",
                "personal_touch": True,
                "visual_elements": True,
                "trend_awareness": True
            }
        }

        if self.domain_type in domain_configs:
            self.domain_specific_config.update(domain_configs[self.domain_type])

    def _setup_content_type_defaults(self):
        """Настройка значений по умолчанию в зависимости от типа контента."""
        content_type_configs = {
            "blog_post": {
                "optimal_length": "medium",
                "seo_focus": True,
                "social_sharing": True,
                "comment_ready": True
            },
            "documentation": {
                "optimal_length": "comprehensive",
                "seo_focus": False,
                "technical_accuracy": "high",
                "version_control": True
            },
            "marketing": {
                "optimal_length": "short",
                "seo_focus": True,
                "conversion_focused": True,
                "ab_test_ready": True
            },
            "educational": {
                "optimal_length": "long",
                "seo_focus": False,
                "learning_objectives": True,
                "progressive_disclosure": True
            },
            "social_media": {
                "optimal_length": "short",
                "seo_focus": False,
                "engagement_optimized": True,
                "platform_specific": True
            },
            "email": {
                "optimal_length": "short",
                "seo_focus": False,
                "personalization": True,
                "mobile_optimized": True
            }
        }

        if self.content_type in content_type_configs:
            config = content_type_configs[self.content_type]
            # Применяем настройки только если они не были явно заданы
            if not hasattr(self, '_content_length_set'):
                self.content_length = config.get("optimal_length", self.content_length)

    def _validate_configuration(self):
        """Валидация и коррекция конфигурации."""
        # Проверка совместимости настроек
        if self.content_type == "documentation" and self.seo_optimization:
            # Для документации SEO обычно менее важно
            self.seo_optimization = False

        if self.content_type == "social_media" and self.content_length == "comprehensive":
            # Социальные сети требуют краткого контента
            self.content_length = "short"

        if self.target_audience == "beginners" and self.readability_level == "academic":
            # Для новичков нужен более простой язык
            self.readability_level = "simple"

    def get_content_parameters(self) -> Dict[str, Any]:
        """Получить все параметры контента в виде словаря."""
        return {
            "content_type": self.content_type,
            "domain_type": self.domain_type,
            "target_audience": self.target_audience,
            "content_style": self.content_style,
            "content_length": self.content_length,
            "language": self.language,
            "quality_standard": self.quality_standard,
            "seo_optimization": self.seo_optimization,
            "cultural_adaptation": self.cultural_adaptation
        }

    def get_optimization_settings(self) -> Dict[str, Any]:
        """Получить настройки оптимизации."""
        return {
            "seo_optimization": self.seo_optimization,
            "readability_level": self.readability_level,
            "creativity_level": self.creativity_level,
            "quality_standard": self.quality_standard
        }


def load_dependencies() -> ContentGeneratorDependencies:
    """
    Загрузить зависимости из переменных окружения.

    Returns:
        Настроенный экземпляр ContentGeneratorDependencies
    """
    return ContentGeneratorDependencies(
        api_key=os.getenv("LLM_API_KEY", ""),
        project_path=os.getenv("PROJECT_PATH", ""),

        # Конфигурация контента
        content_type=os.getenv("CONTENT_TYPE", "blog_post"),
        domain_type=os.getenv("DOMAIN_TYPE", "technology"),
        target_audience=os.getenv("TARGET_AUDIENCE", "general"),
        content_style=os.getenv("CONTENT_STYLE", "informative"),
        content_length=os.getenv("CONTENT_LENGTH", "medium"),
        language=os.getenv("PRIMARY_LANGUAGE", "ukrainian"),

        # SEO настройки
        seo_optimization=os.getenv("SEO_OPTIMIZATION", "true").lower() == "true",
        seo_primary_keyword=os.getenv("SEO_PRIMARY_KEYWORD", ""),

        # Качество и стиль
        quality_standard=os.getenv("QUALITY_STANDARD", "high"),
        readability_level=os.getenv("READABILITY_LEVEL", "general"),
        creativity_level=os.getenv("CREATIVITY_LEVEL", "balanced"),

        # Культурная адаптация
        cultural_adaptation=os.getenv("CULTURAL_ADAPTATION", "true").lower() == "true",
        regional_preferences=os.getenv("TARGET_REGION", "ukraine"),

        # RAG и Knowledge Base
        agent_name="universal_content_generator",
        knowledge_tags=os.getenv("KNOWLEDGE_TAGS", "content-generation,copywriting,seo,agent-knowledge,pydantic-ai").split(","),
        archon_project_id=os.getenv("ARCHON_PROJECT_ID", ""),

        # Межагентное взаимодействие
        enable_task_delegation=os.getenv("ENABLE_TASK_DELEGATION", "true").lower() == "true",
        delegation_threshold=os.getenv("DELEGATION_THRESHOLD", "medium")
    )


# === КОНСТАНТЫ КОМПЕТЕНЦИЙ ===

AGENT_COMPETENCIES = {
    "content_types": [
        "blog_post", "documentation", "marketing", "educational",
        "social_media", "email", "press_release", "white_paper",
        "case_study", "tutorial", "review", "interview"
    ],
    "content_domains": [
        "technology", "business", "health", "education", "finance",
        "lifestyle", "science", "arts", "sports", "travel"
    ],
    "content_styles": [
        "informative", "persuasive", "educational", "entertaining",
        "formal", "casual", "technical", "creative", "analytical"
    ],
    "specializations": [
        "seo_optimization", "copywriting", "technical_writing",
        "creative_writing", "content_strategy", "brand_messaging",
        "localization", "social_media_content"
    ]
}

AGENT_ASSIGNEE_MAP = {
    "seo_optimization": "SEO Specialist Agent",
    "technical_writing": "Documentation Agent",
    "creative_design": "UI/UX Enhancement Agent",
    "quality_assurance": "Quality Guardian Agent",
    "performance_optimization": "Performance Optimization Agent",
    "localization": "Localization Engine Agent"
}

# Экспорт
__all__ = [
    "ContentGeneratorDependencies",
    "load_dependencies",
    "AGENT_COMPETENCIES",
    "AGENT_ASSIGNEE_MAP"
]