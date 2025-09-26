#!/usr/bin/env python3
"""
Archon Blueprint Architect Agent - главный архитектор команды Archon.

Экспорт основных компонентов агента.
"""

from .agent import blueprint_architect_agent, run_blueprint_architect
from .dependencies import BlueprintArchitectDependencies, ArchitecturalPattern, ScalabilityLevel
from .settings import (
    load_blueprint_architect_settings,
    get_llm_model,
    get_architecture_defaults,
    get_collaboration_config,
    get_validation_config,
    get_documentation_config
)
from .tools import (
    design_architecture,
    create_system_blueprint,
    analyze_architectural_patterns,
    validate_architecture,
    search_architecture_knowledge
)
from .prompts import get_system_prompt

__all__ = [
    # Основной агент
    "blueprint_architect_agent",
    "run_blueprint_architect",

    # Конфигурация
    "BlueprintArchitectDependencies",
    "ArchitecturalPattern",
    "ScalabilityLevel",

    # Настройки
    "load_blueprint_architect_settings",
    "get_llm_model",
    "get_architecture_defaults",
    "get_collaboration_config",
    "get_validation_config",
    "get_documentation_config",

    # Инструменты
    "design_architecture",
    "create_system_blueprint",
    "analyze_architectural_patterns",
    "validate_architecture",
    "search_architecture_knowledge",

    # Промпты
    "get_system_prompt"
]