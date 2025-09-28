"""
Примеры конфигураций Pattern Cultural Adaptation Expert Agent для разных доменов.

Этот модуль содержит предустановленные конфигурации агента для различных
областей применения, обеспечивая универсальность и простоту интеграции.
"""

from .therapy_config import (
    create_therapy_config,
    THERAPY_UKRAINIAN_CONFIG,
    THERAPY_POLISH_CONFIG,
    THERAPY_ENGLISH_CONFIG,
    get_therapy_examples
)

from .education_config import (
    create_education_config,
    EDUCATION_UKRAINIAN_CONFIG,
    EDUCATION_POLISH_CONFIG,
    EDUCATION_ENGLISH_CONFIG,
    get_education_examples
)

from .corporate_config import (
    create_corporate_config,
    CORPORATE_UKRAINIAN_CONFIG,
    CORPORATE_POLISH_CONFIG,
    CORPORATE_ENGLISH_CONFIG,
    get_corporate_examples
)

__all__ = [
    # Therapy domain
    'create_therapy_config',
    'THERAPY_UKRAINIAN_CONFIG',
    'THERAPY_POLISH_CONFIG',
    'THERAPY_ENGLISH_CONFIG',
    'get_therapy_examples',

    # Education domain
    'create_education_config',
    'EDUCATION_UKRAINIAN_CONFIG',
    'EDUCATION_POLISH_CONFIG',
    'EDUCATION_ENGLISH_CONFIG',
    'get_education_examples',

    # Corporate domain
    'create_corporate_config',
    'CORPORATE_UKRAINIAN_CONFIG',
    'CORPORATE_POLISH_CONFIG',
    'CORPORATE_ENGLISH_CONFIG',
    'get_corporate_examples',
]


def get_all_domain_examples():
    """
    Получить примеры для всех доменов.

    Returns:
        Dict с примерами для therapy, education и corporate доменов
    """
    return {
        'therapy': get_therapy_examples(),
        'education': get_education_examples(),
        'corporate': get_corporate_examples()
    }


def list_available_configs():
    """
    Получить список всех доступных конфигураций.

    Returns:
        Dict со всеми предустановленными конфигурациями
    """
    return {
        'therapy': {
            'ukrainian': THERAPY_UKRAINIAN_CONFIG,
            'polish': THERAPY_POLISH_CONFIG,
            'english': THERAPY_ENGLISH_CONFIG
        },
        'education': {
            'ukrainian': EDUCATION_UKRAINIAN_CONFIG,
            'polish': EDUCATION_POLISH_CONFIG,
            'english': EDUCATION_ENGLISH_CONFIG
        },
        'corporate': {
            'ukrainian': CORPORATE_UKRAINIAN_CONFIG,
            'polish': CORPORATE_POLISH_CONFIG,
            'english': CORPORATE_ENGLISH_CONFIG
        }
    }