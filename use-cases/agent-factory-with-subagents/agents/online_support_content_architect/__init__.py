"""
Psychology Content Architect Agent

Универсальный агент для проектирования архитектуры психологических программ.
Специализируется на создании структурированных, модульных и адаптивных программ
для различных психологических доменов и целевых аудиторий.
"""

from .agent import (
    psychology_architect,
    design_psychological_program
)
from .dependencies import (
    ArchitectDependencies,
    get_architect_config,
    ArchitecturalTemplate,
    ARCHITECTURAL_TEMPLATES,
    get_template
)
from .tools import (
    analyze_program_requirements,
    design_modular_structure,
    optimize_sequence,
    create_adaptation_framework,
    search_architectural_patterns
)
from .prompts import (
    get_architect_prompt,
    get_analysis_prompt,
    get_optimization_prompt,
    get_adaptation_prompt
)
from .settings import (
    ArchitectSettings,
    PsychologicalDomain,
    TargetPopulation,
    ProgramType,
    DeliveryFormat,
    ComplexityLevel,
    PRESET_CONFIGURATIONS,
    get_preset_configuration,
    list_available_presets
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Universal Psychology Content Architect Agent"

# Основные функции для экспорта
__all__ = [
    # Главный агент и функции
    "psychology_architect",
    "design_psychological_program",

    # Зависимости и конфигурация
    "ArchitectDependencies",
    "get_architect_config",
    "ArchitecturalTemplate",
    "ARCHITECTURAL_TEMPLATES",
    "get_template",

    # Инструменты
    "analyze_program_requirements",
    "design_modular_structure",
    "optimize_sequence",
    "create_adaptation_framework",
    "search_architectural_patterns",

    # Промпты
    "get_architect_prompt",
    "get_analysis_prompt",
    "get_optimization_prompt",
    "get_adaptation_prompt",

    # Настройки и енумы
    "ArchitectSettings",
    "PsychologicalDomain",
    "TargetPopulation",
    "ProgramType",
    "DeliveryFormat",
    "ComplexityLevel",
    "PRESET_CONFIGURATIONS",
    "get_preset_configuration",
    "list_available_presets"
]

# Метаинформация о агенте
AGENT_INFO = {
    "name": "Psychology Content Architect",
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "specialization": "Архитектура психологических программ",
    "supported_domains": [
        "anxiety", "depression", "trauma", "relationships",
        "addiction", "stress", "grief", "parenting"
    ],
    "supported_populations": [
        "adults", "adolescents", "children", "elderly",
        "couples", "families", "groups"
    ],
    "program_types": [
        "therapeutic", "educational", "preventive",
        "developmental", "assessment", "crisis_intervention"
    ],
    "key_features": [
        "Модульная архитектура",
        "Адаптивное проектирование",
        "Научная обоснованность",
        "Безопасность по дизайну",
        "Интеграция с другими агентами"
    ],
    "quality_standards": [
        "Evidence-based design",
        "Clinical safety protocols",
        "Ethical compliance",
        "Outcome measurement",
        "Cultural adaptation"
    ]
}

def get_agent_info() -> dict:
    """Получить информацию об агенте"""
    return AGENT_INFO.copy()

def get_quick_start_guide() -> str:
    """Получить краткое руководство по использованию"""
    return """
    Psychology Content Architect - Быстрый старт

    1. Базовое использование:
       ```python
       from psychology_content_architect import design_psychological_program

       result = await design_psychological_program(
           requirements="Программа КПТ для тревожности",
           psychological_domain="anxiety",
           target_population="adults",
           duration_weeks=12
       )
       ```

    2. С предустановленной конфигурацией:
       ```python
       from psychology_content_architect import get_preset_configuration

       settings = get_preset_configuration("cbt_anxiety_adults")
       # Использовать settings для кастомизации
       ```

    3. Кастомная настройка:
       ```python
       from psychology_content_architect import ArchitectSettings

       settings = ArchitectSettings(
           psychological_domain="depression",
           target_population="adolescents",
           duration_weeks=10,
           session_length_minutes=45
       )
       ```

    4. Использование инструментов напрямую:
       ```python
       from psychology_content_architect import analyze_program_requirements

       analysis = await analyze_program_requirements(
           ctx, requirements_text, target_outcomes
       )
       ```
    """

# Проверка совместимости при импорте
def _check_dependencies():
    """Проверка необходимых зависимостей"""
    try:
        import pydantic_ai
        import dataclasses
        from typing import Dict, List, Optional
        return True
    except ImportError as e:
        print(f"Warning: Missing dependency - {e}")
        return False

# Автоматическая проверка при импорте
_dependencies_ok = _check_dependencies()

if not _dependencies_ok:
    print("Warning: Some dependencies are missing. Some features may not work correctly.")