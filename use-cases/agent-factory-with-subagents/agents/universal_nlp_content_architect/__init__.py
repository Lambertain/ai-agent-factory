"""
Universal NLP Content Architect Agent Package
Универсальный пакет для создания NLP контента любых доменов
"""

from .agent import universal_nlp_content_architect, create_nlp_content
from .dependencies import UniversalNLPDependencies, get_nlp_config
from .settings import UniversalNLPSettings, create_universal_nlp_settings
from .prompts import get_universal_nlp_prompt, get_domain_adaptation_prompt
from .tools import (
    research_domain_topic,
    create_content_draft,
    reflect_and_improve_content,
    finalize_nlp_content,
    create_transformation_program,
    adapt_content_for_vak,
    validate_nlp_structure,
    search_nlp_knowledge,
    delegate_specialized_task
)

__version__ = "1.0.0"
__author__ = "Universal NLP Content Architect"
__description__ = "Универсальный агент для создания контента с NLP/Эриксоновскими техниками"

# Основные экспорты
__all__ = [
    # Главный агент
    "universal_nlp_content_architect",
    "create_nlp_content",

    # Конфигурация и зависимости
    "UniversalNLPDependencies",
    "get_nlp_config",
    "UniversalNLPSettings",
    "create_universal_nlp_settings",

    # Промпты
    "get_universal_nlp_prompt",
    "get_domain_adaptation_prompt",

    # Инструменты
    "research_domain_topic",
    "create_content_draft",
    "reflect_and_improve_content",
    "finalize_nlp_content",
    "create_transformation_program",
    "adapt_content_for_vak",
    "validate_nlp_structure",
    "search_nlp_knowledge",
    "delegate_specialized_task"
]

# Константы для доменов
SUPPORTED_DOMAINS = [
    "psychology",      # Психология
    "astrology",       # Астрология
    "tarot",          # Таро
    "numerology",     # Нумерология
    "coaching",       # Коучинг
    "wellness",       # Велнес/медитация
    "spirituality",   # Духовность
    "self_development" # Саморазвитие
]

SUPPORTED_CONTENT_TYPES = [
    "diagnostic_test",        # Диагностический тест
    "transformation_program", # Программа трансформации
    "guidance_system",        # Система наставничества
    "assessment_tool",        # Инструмент оценки
    "meditation_program",     # Программа медитации
    "coaching_framework",     # Коучинговая рамка
    "divination_system",      # Система предсказания
    "analysis_framework"      # Аналитическая рамка
]

SUPPORTED_LANGUAGES = ["ukrainian", "russian", "english"]

# Базовая функция для быстрого создания контента
async def quick_create_nlp_content(
    topic: str,
    domain: str = "psychology",
    language: str = "ukrainian"
):
    """Быстрое создание NLP контента с дефолтными настройками"""
    return await create_nlp_content(
        content_topic=topic,
        domain_type=domain,
        target_language=language,
        content_count=16,
        transformation_days=21
    )