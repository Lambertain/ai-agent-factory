# -*- coding: utf-8 -*-
"""
Universal Content Generator Agent

Универсальный агент для генерации различных типов контента:
блоги, документация, маркетинговые материалы, образовательный контент,
социальные медиа, электронные письма и другие текстовые материалы.

Основные возможности:
- Генерация контента для любых доменов и аудиторий
- Адаптивные промпты под различные стили и цели
- SEO оптимизация и структурирование контента
- Культурная и языковая адаптация
- Валидация качества и метрики эффективности
- A/B тестирование вариаций контента
- Коллективная работа с другими агентами

Примеры использования:

```python
from universal_content_generator_agent import run_content_generation_task

# Создание блог-поста
result = await run_content_generation_task(
    message="Создай статью о современных трендах в AI",
    content_type="blog_post",
    domain_type="technology",
    target_audience="professionals",
    seo_focus=True
)

# Техническая документация
result = await run_documentation_generation(
    documentation_type="api",
    technical_level="intermediate",
    framework="FastAPI",
    include_examples=True
)

# Маркетинговый контент
result = await run_marketing_content_generation(
    campaign_type="email",
    product_category="SaaS",
    marketing_goal="conversion",
    tone="professional"
)
```

Структура агента:
- agent.py - основной агент и точки входа
- dependencies.py - управление зависимостями и конфигурация
- tools.py - инструменты генерации и оптимизации контента
- prompts.py - адаптивные промпты под домены и типы контента
- providers.py - оптимизированная система выбора LLM моделей
- settings.py - конфигурируемые параметры через .env
"""

from .agent import (
    content_generator_agent,
    run_content_generation_task,
    run_blog_post_generation,
    run_documentation_generation,
    run_marketing_content_generation,
    run_educational_content_generation,
    run_social_media_generation,
    get_content_suggestions,
    validate_content_requirements
)

from .dependencies import (
    ContentGeneratorDependencies,
    load_dependencies,
    AGENT_COMPETENCIES,
    AGENT_ASSIGNEE_MAP
)

from .settings import (
    ContentGeneratorSettings,
    ContentGenerationConfig,
    load_settings,
    create_content_generation_config,
    get_universal_settings_template
)

from .providers import (
    ContentGeneratorLLMProvider,
    ModelProvider,
    ContentComplexity,
    get_llm_model,
    get_optimal_model_for_content
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Universal Content Generator Agent для создания любых типов контента"

__all__ = [
    # Основные функции
    "content_generator_agent",
    "run_content_generation_task",
    "run_blog_post_generation",
    "run_documentation_generation",
    "run_marketing_content_generation",
    "run_educational_content_generation",
    "run_social_media_generation",
    "get_content_suggestions",
    "validate_content_requirements",

    # Зависимости и конфигурация
    "ContentGeneratorDependencies",
    "load_dependencies",
    "AGENT_COMPETENCIES",
    "AGENT_ASSIGNEE_MAP",

    # Настройки
    "ContentGeneratorSettings",
    "ContentGenerationConfig",
    "load_settings",
    "create_content_generation_config",
    "get_universal_settings_template",

    # Провайдеры LLM
    "ContentGeneratorLLMProvider",
    "ModelProvider",
    "ContentComplexity",
    "get_llm_model",
    "get_optimal_model_for_content",

    # Метаданные
    "__version__",
    "__author__",
    "__description__"
]

# Информация для автоматического обнаружения агента
AGENT_INFO = {
    "name": "Universal Content Generator Agent",
    "type": "content_generator",
    "version": __version__,
    "description": __description__,
    "supported_content_types": [
        "blog_post",
        "documentation",
        "marketing",
        "educational",
        "social_media",
        "email",
        "press_release",
        "white_paper",
        "case_study",
        "tutorial",
        "review",
        "interview"
    ],
    "supported_domains": [
        "technology",
        "business",
        "health",
        "education",
        "finance",
        "lifestyle",
        "science",
        "arts",
        "sports",
        "travel"
    ],
    "capabilities": [
        "multi_format_content_generation",
        "seo_optimization",
        "cultural_adaptation",
        "audience_targeting",
        "style_adaptation",
        "quality_validation",
        "content_variations",
        "performance_insights",
        "collective_problem_solving"
    ],
    "content_styles": [
        "informative",
        "persuasive",
        "educational",
        "entertaining",
        "formal",
        "casual",
        "technical",
        "creative",
        "analytical"
    ],
    "target_audiences": [
        "general",
        "professionals",
        "beginners",
        "experts",
        "students",
        "customers",
        "executives",
        "developers",
        "researchers"
    ],
    "required_env_vars": [
        "LLM_API_KEY"
    ],
    "optional_env_vars": [
        "CONTENT_TYPE",
        "DOMAIN_TYPE",
        "TARGET_AUDIENCE",
        "CONTENT_STYLE",
        "CONTENT_LENGTH",
        "PRIMARY_LANGUAGE",
        "QUALITY_STANDARD",
        "SEO_OPTIMIZATION",
        "CULTURAL_ADAPTATION",
        "ARCHON_PROJECT_ID"
    ],
    "knowledge_base_tags": [
        "content-generation",
        "copywriting",
        "seo",
        "agent-knowledge",
        "pydantic-ai"
    ],
    "delegation_targets": [
        "seo_optimization",
        "technical_writing",
        "creative_design",
        "quality_assurance",
        "performance_optimization",
        "localization"
    ],
    "output_formats": [
        "markdown",
        "html",
        "plain_text",
        "rich_text",
        "json"
    ],
    "quality_standards": [
        "basic",
        "standard",
        "high",
        "premium"
    ],
    "seo_features": [
        "keyword_optimization",
        "meta_descriptions",
        "heading_structure",
        "internal_linking",
        "content_structure"
    ],
    "cultural_adaptations": [
        "language_localization",
        "cultural_references",
        "regional_preferences",
        "currency_formats",
        "date_formats"
    ]
}