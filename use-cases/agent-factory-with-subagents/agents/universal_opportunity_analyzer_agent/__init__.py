# -*- coding: utf-8 -*-
"""
Universal Opportunity Analyzer Agent
Универсальный агент для анализа возможностей в любых доменах

Поддерживает психологию, астрологию, нумерологию, бизнес и другие области.
"""

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Универсальный агент анализа возможностей и болевых точек"

from .agent import opportunity_analyzer_agent, run_opportunity_analysis
from .dependencies import load_dependencies, OpportunityAnalyzerDependencies
from .settings import load_settings, OpportunityAnalyzerSettings, create_domain_config
from .providers import get_llm_model, get_cost_optimized_model
from .prompts import get_system_prompt

# Публичный API
__all__ = [
    # Основные компоненты
    "opportunity_analyzer_agent",
    "run_opportunity_analysis",

    # Конфигурация
    "load_dependencies",
    "OpportunityAnalyzerDependencies",
    "load_settings",
    "OpportunityAnalyzerSettings",
    "create_domain_config",

    # LLM провайдеры
    "get_llm_model",
    "get_cost_optimized_model",

    # Промпты
    "get_system_prompt",

    # Метаданные
    "__version__",
    "__author__",
    "__description__"
]

# Поддерживаемые домены
SUPPORTED_DOMAINS = [
    "psychology",      # Психология
    "astrology",       # Астрология
    "numerology",      # Нумерология
    "business",        # Бизнес
    "education",       # Образование
    "healthcare",      # Здравоохранение
    "technology",      # Технологии
    "finance",         # Финансы
    "marketing",       # Маркетинг
    "consulting"       # Консалтинг
]

# Поддерживаемые типы проектов
SUPPORTED_PROJECT_TYPES = [
    "transformation_platform",  # Платформа трансформации
    "educational_system",       # Образовательная система
    "consultation_platform",    # Платформа консультаций
    "analytics_platform",       # Аналитическая платформа
    "marketplace",              # Маркетплейс
    "mobile_app",              # Мобильное приложение
    "web_service",             # Веб-сервис
    "api_service",             # API сервис
    "saas_platform",           # SaaS платформа
    "enterprise_solution"      # Корпоративное решение
]

# Поддерживаемые языки
SUPPORTED_LANGUAGES = [
    "ukrainian",  # Украинский (основной)
    "polish",     # Польский
    "english"     # Английский
]

def get_agent_info() -> dict:
    """
    Получить информацию об агенте.

    Returns:
        Словарь с метаданными агента
    """
    return {
        "name": "Universal Opportunity Analyzer Agent",
        "version": __version__,
        "description": __description__,
        "author": __author__,
        "supported_domains": SUPPORTED_DOMAINS,
        "supported_project_types": SUPPORTED_PROJECT_TYPES,
        "supported_languages": SUPPORTED_LANGUAGES,
        "framework": "pydantic-ai",
        "capabilities": [
            "Анализ возможностей в любых доменах",
            "Выявление болевых точек аудитории",
            "Оценка рыночного потенциала",
            "Анализ конкурентной среды",
            "Расчет скоринга возможностей",
            "Поиск паттернов через RAG",
            "Межагентное взаимодействие",
            "Коллективное решение задач"
        ]
    }

def create_agent_for_domain(
    domain_type: str,
    project_type: str = "platform",
    primary_language: str = "ukrainian"
):
    """
    Создать агент для конкретного домена.

    Args:
        domain_type: Тип домена из SUPPORTED_DOMAINS
        project_type: Тип проекта из SUPPORTED_PROJECT_TYPES
        primary_language: Основной язык из SUPPORTED_LANGUAGES

    Returns:
        Настроенный агент для домена

    Raises:
        ValueError: Если домен не поддерживается
    """
    if domain_type not in SUPPORTED_DOMAINS:
        raise ValueError(f"Домен '{domain_type}' не поддерживается. Доступные: {SUPPORTED_DOMAINS}")

    if project_type not in SUPPORTED_PROJECT_TYPES:
        raise ValueError(f"Тип проекта '{project_type}' не поддерживается. Доступные: {SUPPORTED_PROJECT_TYPES}")

    if primary_language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Язык '{primary_language}' не поддерживается. Доступные: {SUPPORTED_LANGUAGES}")

    # Создаем настройки для домена
    settings = create_domain_config(domain_type, project_type)
    settings.primary_language = primary_language

    # Создаем зависимости
    deps = load_dependencies(domain_type, project_type)

    return {
        "agent": opportunity_analyzer_agent,
        "settings": settings,
        "dependencies": deps,
        "run_analysis": lambda message: run_opportunity_analysis(
            message, domain_type, project_type
        )
    }

# Примеры использования для разных доменов
DOMAIN_EXAMPLES = {
    "psychology": {
        "description": "Анализ возможностей в области психологии и ментального здоровья",
        "example_query": "Проанализируй возможности создания платформы онлайн-терапии для украинской аудитории",
        "focus_areas": ["диагностика", "терапия", "самопомощь", "образование"]
    },
    "astrology": {
        "description": "Анализ возможностей в области астрологии и духовных практик",
        "example_query": "Оцени потенциал сервиса персональных гороскопов с элементами IA",
        "focus_areas": ["консультации", "расчеты", "образование", "совместимость"]
    },
    "numerology": {
        "description": "Анализ возможностей в области нумерологии и символических наук",
        "example_query": "Исследуй рынок нумерологических услуг для выбора имен и дат",
        "focus_areas": ["расчеты", "именование", "совместимость", "бизнес-консультации"]
    },
    "business": {
        "description": "Анализ бизнес-возможностей и стратегических решений",
        "example_query": "Проанализируй возможности запуска SaaS платформы для малого бизнеса",
        "focus_areas": ["стратегия", "аналитика", "оптимизация", "автоматизация"]
    }
}

def get_domain_examples() -> dict:
    """
    Получить примеры использования для разных доменов.

    Returns:
        Словарь с примерами для каждого домена
    """
    return DOMAIN_EXAMPLES