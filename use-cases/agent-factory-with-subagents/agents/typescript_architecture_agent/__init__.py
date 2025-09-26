"""Универсальный TypeScript Architecture Agent для оптимизации архитектуры проектов."""

from .agent import typescript_agent, run_typescript_analysis, run_sync
from .tools import (
    analyze_type_complexity,
    refactor_types,
    generate_type_guards,
    optimize_typescript_config,
    search_agent_knowledge
)
from .dependencies import TypeScriptArchitectureDependencies
from .settings import load_settings

__version__ = "1.0.0"
__all__ = [
    "typescript_agent",
    "run_typescript_analysis",
    "run_sync",
    "analyze_type_complexity",
    "refactor_types",
    "generate_type_guards",
    "optimize_typescript_config",
    "search_agent_knowledge",
    "TypeScriptArchitectureDependencies",
    "load_settings"
]