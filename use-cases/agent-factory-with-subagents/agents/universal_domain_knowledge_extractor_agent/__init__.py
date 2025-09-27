# -*- coding: utf-8 -*-
"""
Universal Domain Knowledge Extractor Agent

Универсальный агент для извлечения, структурирования и модуляризации знаний
из любых доменов: психология, астрология, нумерология, бизнес и другие.

Основные возможности:
- Извлечение знаний из различных источников
- Анализ паттернов и структур знаний
- Создание модульных компонентов знаний
- Научная валидация и проверка качества
- Поддержка множественных доменов и языков
- Интеграция с Archon Knowledge Base
"""

from .agent import (
    domain_knowledge_extractor_agent,
    run_domain_knowledge_extraction
)
from .dependencies import (
    DomainKnowledgeExtractorDependencies,
    load_dependencies
)
from .settings import (
    UniversalKnowledgeExtractionSettings,
    load_settings,
    get_settings
)
from .providers import (
    get_llm_model,
    get_model_provider,
    get_cost_optimized_model
)
from .tools import (
    extract_domain_knowledge,
    analyze_knowledge_patterns,
    create_knowledge_modules,
    search_domain_knowledge,
    validate_knowledge_structure
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Universal Domain Knowledge Extractor Agent для модульных систем знаний"

# Экспорт основных компонентов
__all__ = [
    # Основной агент
    "domain_knowledge_extractor_agent",
    "run_domain_knowledge_extraction",

    # Зависимости и настройки
    "DomainKnowledgeExtractorDependencies",
    "load_dependencies",
    "UniversalKnowledgeExtractionSettings",
    "load_settings",
    "get_settings",

    # Провайдеры моделей
    "get_llm_model",
    "get_model_provider",
    "get_cost_optimized_model",

    # Основные инструменты
    "extract_domain_knowledge",
    "analyze_knowledge_patterns",
    "create_knowledge_modules",
    "search_domain_knowledge",
    "validate_knowledge_structure",

    # Метаинформация
    "__version__",
    "__author__",
    "__description__"
]

# Конфигурация агента
AGENT_CONFIG = {
    "name": "Universal Domain Knowledge Extractor Agent",
    "version": __version__,
    "supported_domains": [
        "psychology",
        "astrology",
        "numerology",
        "business",
        "generic"
    ],
    "supported_languages": [
        "ukrainian",
        "polish",
        "english"
    ],
    "capabilities": [
        "knowledge_extraction",
        "pattern_analysis",
        "module_creation",
        "scientific_validation",
        "cultural_adaptation",
        "multi_domain_support"
    ],
    "integration": [
        "archon_knowledge_base",
        "rag_search",
        "task_delegation",
        "quality_validation"
    ]
}

def get_agent_info() -> dict:
    """Получить информацию об агенте."""
    return AGENT_CONFIG.copy()

def get_supported_domains() -> list:
    """Получить список поддерживаемых доменов."""
    return AGENT_CONFIG["supported_domains"].copy()

def get_supported_languages() -> list:
    """Получить список поддерживаемых языков."""
    return AGENT_CONFIG["supported_languages"].copy()

def get_agent_capabilities() -> list:
    """Получить список возможностей агента."""
    return AGENT_CONFIG["capabilities"].copy()