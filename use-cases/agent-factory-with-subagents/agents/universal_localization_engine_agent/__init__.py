"""
Universal Localization Engine Agent

Универсальный агент для автоматизации процессов локализации и интернационализации (i18n/l10n)
различных типов проектов с поддержкой 20+ языков и культурной адаптации.

Основные возможности:
- Поддержка веб, мобильных, десктопных, API, игровых проектов и документации
- 20+ языков с региональными вариантами и RTL поддержкой
- 4 уровня качества перевода (basic, standard, professional, native)
- Автоматизированное извлечение, перевод, валидация и культурная адаптация
- Интеграция с TMS, CAT-инструментами и CI/CD пайплайнами
"""

from .agent import universal_localization_engine_agent
from .dependencies import LocalizationEngineDependencies
from .settings import LocalizationEngineConfig, localization_config
from .tools import (
    extract_translatable_content,
    translate_content_batch,
    validate_translation_quality,
    generate_locale_files,
    manage_terminology,
    validate_ui_compatibility,
    optimize_translation_workflow,
    calculate_localization_metrics
)
from .prompts import get_system_prompt, LocalizationPromptConfig
from .providers import LocalizationModelProvider

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Universal Localization Engine Agent для автоматизации процессов локализации"

__all__ = [
    # Основной агент
    "universal_localization_engine_agent",

    # Конфигурация и зависимости
    "LocalizationEngineDependencies",
    "LocalizationEngineConfig",
    "localization_config",

    # Инструменты
    "extract_translatable_content",
    "translate_content_batch",
    "validate_translation_quality",
    "generate_locale_files",
    "manage_terminology",
    "validate_ui_compatibility",
    "optimize_translation_workflow",
    "calculate_localization_metrics",

    # Промпты и провайдеры
    "get_system_prompt",
    "LocalizationPromptConfig",
    "LocalizationModelProvider",
]

# Метаданные агента
AGENT_METADATA = {
    "name": "Universal Localization Engine Agent",
    "version": __version__,
    "description": __description__,
    "capabilities": [
        "Извлечение переводимого контента",
        "Автоматический и профессиональный перевод",
        "Контроль качества переводов",
        "Культурная адаптация контента",
        "UI совместимость и валидация",
        "Терминологическое управление",
        "Оптимизация рабочих процессов",
        "Метрики и аналитика локализации"
    ],
    "supported_project_types": [
        "web", "mobile", "desktop", "api", "game", "documentation"
    ],
    "supported_languages": [
        "en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko",
        "ar", "hi", "nl", "sv", "da", "no", "fi", "pl", "tr", "he", "th"
    ],
    "quality_levels": [
        "basic", "standard", "professional", "native"
    ],
    "file_formats": [
        "json", "yaml", "xml", "properties", "po", "pot", "strings",
        "stringsdict", "arb", "resx", "csv"
    ]
}