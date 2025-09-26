"""
NLP Psychology Test Adapter Agent

Универсальный агент для адаптации психологических тестов под методологию PatternShift
с сохранением научной обоснованности и поддержкой множественных доменов применения.

Основные возможности:
- Трансформация клинических формулировок в жизненные ситуации
- Адаптивная система оценки результатов
- Мультиязычная поддержка с культурной адаптацией
- Логика перенаправления на программы трансформации
- Валидация психометрических свойств

Примеры использования:
- Адаптация PHQ-9, GAD-7, и других валидированных тестов
- Создание wellness-ориентированных оценок
- Разработка коучинговых инструментов оценки
- Исследовательские психологические измерения
"""

from .agent import (
    nlp_psychology_test_adapter_agent,
    run_test_adaptation_workflow
)

from .dependencies import (
    PatternShiftTestAdapterDeps,
    TestConfiguration,
    AdaptationResult,
    TestValidationResult
)

from .tools import (
    adapt_test_questions,
    validate_test_structure,
    generate_life_situations,
    create_multilingual_variants,
    calculate_adaptive_thresholds,
    integrate_redirection_logic,
    validate_psychological_correctness
)

from .prompts import (
    MAIN_SYSTEM_PROMPT,
    ADAPTATION_PROMPT,
    VALIDATION_PROMPT,
    MULTILINGUAL_PROMPT,
    EXPANSION_PROMPT,
    get_adaptive_system_prompt,
    get_validation_criteria
)

from .settings import (
    TestAdapterSettings,
    AdaptationDomainType,
    ProjectType,
    CulturalContext,
    load_settings,
    get_domain_config,
    get_cultural_config,
    get_project_config,
    create_adaptive_config,
    EXAMPLE_CONFIGS
)

# Версия агента
__version__ = "1.0.0"

# Метаданные агента
__agent_info__ = {
    "name": "NLP Psychology Test Adapter Agent",
    "version": __version__,
    "description": "Универсальный агент для адаптации психологических тестов под методологию PatternShift",
    "domain": "psychology, assessment, wellness",
    "framework": "Pydantic AI",
    "model": "Claude 4 Sonnet",
    "capabilities": [
        "Адаптация клинических тестов",
        "Трансформация в жизненные ситуации",
        "Мультиязычная поддержка",
        "Адаптивная система оценки",
        "Валидация психометрических свойств",
        "Культурная адаптация",
        "Логика перенаправления"
    ],
    "supported_domains": [
        "clinical_psychology",
        "wellness",
        "coaching",
        "educational",
        "organizational",
        "research"
    ],
    "supported_languages": ["uk", "ru", "en"],
    "supported_cultural_contexts": [
        "ukrainian", "russian", "western_european",
        "american", "eastern_european", "universal"
    ]
}

# Экспорт основных компонентов
__all__ = [
    # Основной агент
    "nlp_psychology_test_adapter_agent",
    "run_test_adaptation_workflow",

    # Зависимости и модели данных
    "PatternShiftTestAdapterDeps",
    "TestConfiguration",
    "AdaptationResult",
    "TestValidationResult",

    # Инструменты
    "adapt_test_questions",
    "validate_test_structure",
    "generate_life_situations",
    "create_multilingual_variants",
    "calculate_adaptive_thresholds",
    "integrate_redirection_logic",
    "validate_psychological_correctness",

    # Промпты
    "MAIN_SYSTEM_PROMPT",
    "ADAPTATION_PROMPT",
    "VALIDATION_PROMPT",
    "MULTILINGUAL_PROMPT",
    "EXPANSION_PROMPT",
    "get_adaptive_system_prompt",
    "get_validation_criteria",

    # Настройки и конфигурации
    "TestAdapterSettings",
    "AdaptationDomainType",
    "ProjectType",
    "CulturalContext",
    "load_settings",
    "get_domain_config",
    "get_cultural_config",
    "get_project_config",
    "create_adaptive_config",
    "EXAMPLE_CONFIGS",

    # Метаданные
    "__version__",
    "__agent_info__"
]


def get_agent_info():
    """Возвращает информацию о агенте."""
    return __agent_info__


def print_agent_capabilities():
    """Выводит возможности агента."""
    info = __agent_info__

    print(f"\n🧠 {info['name']} v{info['version']}")
    print(f"📝 {info['description']}")
    print(f"🔧 Framework: {info['framework']} + {info['model']}")

    print(f"\n✨ Основные возможности:")
    for capability in info['capabilities']:
        print(f"  • {capability}")

    print(f"\n🎯 Поддерживаемые домены:")
    for domain in info['supported_domains']:
        print(f"  • {domain}")

    print(f"\n🌐 Поддерживаемые языки и культуры:")
    print(f"  Языки: {', '.join(info['supported_languages'])}")
    print(f"  Культурные контексты: {', '.join(info['supported_cultural_contexts'])}")


def create_quick_config(
    domain: str = "wellness",
    culture: str = "ukrainian",
    language: str = "uk"
) -> dict:
    """
    Создает быструю конфигурацию для агента.

    Args:
        domain: Домен применения
        culture: Культурный контекст
        language: Основной язык

    Returns:
        Словарь конфигурации
    """
    # Маппинг строковых значений в енумы
    domain_mapping = {
        "clinical": AdaptationDomainType.CLINICAL_PSYCHOLOGY,
        "wellness": AdaptationDomainType.WELLNESS,
        "coaching": AdaptationDomainType.COACHING,
        "education": AdaptationDomainType.EDUCATIONAL,
        "organizational": AdaptationDomainType.ORGANIZATIONAL,
        "research": AdaptationDomainType.RESEARCH
    }

    culture_mapping = {
        "ukrainian": CulturalContext.UKRAINIAN,
        "russian": CulturalContext.RUSSIAN,
        "western": CulturalContext.WESTERN_EUROPEAN,
        "american": CulturalContext.AMERICAN,
        "eastern": CulturalContext.EASTERN_EUROPEAN,
        "universal": CulturalContext.UNIVERSAL
    }

    domain_enum = domain_mapping.get(domain, AdaptationDomainType.WELLNESS)
    culture_enum = culture_mapping.get(culture, CulturalContext.UKRAINIAN)

    config = create_adaptive_config(domain_enum, culture_enum)
    config["primary_language"] = language

    return config


# Примеры быстрого создания конфигураций
QUICK_CONFIGS = {
    "wellness_uk": create_quick_config("wellness", "ukrainian", "uk"),
    "coaching_universal": create_quick_config("coaching", "universal", "en"),
    "clinical_american": create_quick_config("clinical", "american", "en"),
    "research_eastern": create_quick_config("research", "eastern", "en")
}


if __name__ == "__main__":
    print_agent_capabilities()

    print(f"\n📋 Доступные быстрые конфигурации:")
    for name, config in QUICK_CONFIGS.items():
        print(f"  • {name}: {config['domain_type']} / {config['cultural_context']} / {config.get('primary_language', 'en')}")