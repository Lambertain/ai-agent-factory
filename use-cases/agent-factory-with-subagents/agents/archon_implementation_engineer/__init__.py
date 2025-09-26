#!/usr/bin/env python3
"""
Archon Implementation Engineer Agent - главный инженер реализации команды Archon.

Экспорт основных компонентов агента.
"""

from .agent import implementation_engineer_agent, run_implementation_engineer
from .dependencies import (
    ImplementationEngineerDependencies,
    DevelopmentFramework,
    ProgrammingLanguage,
    DatabaseType,
    QualityStandard
)
from .settings import (
    load_implementation_engineer_settings,
    get_llm_model,
    get_development_defaults,
    get_quality_config,
    get_testing_config,
    get_security_config,
    get_performance_config,
    get_collaboration_config,
    get_cicd_config
)
from .tools import (
    implement_feature,
    create_code_structure,
    generate_tests,
    optimize_performance,
    validate_code_quality,
    search_implementation_knowledge,
    delegate_to_quality_guardian
)
from .prompts import get_system_prompt

__all__ = [
    # Основной агент
    "implementation_engineer_agent",
    "run_implementation_engineer",

    # Конфигурация
    "ImplementationEngineerDependencies",
    "DevelopmentFramework",
    "ProgrammingLanguage",
    "DatabaseType",
    "QualityStandard",

    # Настройки
    "load_implementation_engineer_settings",
    "get_llm_model",
    "get_development_defaults",
    "get_quality_config",
    "get_testing_config",
    "get_security_config",
    "get_performance_config",
    "get_collaboration_config",
    "get_cicd_config",

    # Инструменты
    "implement_feature",
    "create_code_structure",
    "generate_tests",
    "optimize_performance",
    "validate_code_quality",
    "search_implementation_knowledge",
    "delegate_to_quality_guardian",

    # Промпты
    "get_system_prompt"
]