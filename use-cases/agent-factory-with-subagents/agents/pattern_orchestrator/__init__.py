# -*- coding: utf-8 -*-
"""
Pattern Orchestrator Agent - пакет агента.

Экспорт основных компонентов агента для использования в PatternShift.
"""

from .agent import (
    create_pattern_orchestrator_agent,
    get_pattern_orchestrator_agent,
    run_pattern_orchestrator_agent,
    run_full_orchestration_workflow,
    apply_content_degradation
)
from .dependencies import (
    PatternOrchestratorDependencies,
    PatternShiftArchitecture,
    DegradationSystemArchitecture
)
from .settings import load_settings, get_llm_model
from .workflow import OrchestratorWorkflow, DegradationWorkflow

__version__ = "1.0.0"

__all__ = [
    # Основные функции агента
    "create_pattern_orchestrator_agent",
    "get_pattern_orchestrator_agent",
    "run_pattern_orchestrator_agent",
    "run_full_orchestration_workflow",
    "apply_content_degradation",

    # Зависимости и архитектура
    "PatternOrchestratorDependencies",
    "PatternShiftArchitecture",
    "DegradationSystemArchitecture",

    # Настройки
    "load_settings",
    "get_llm_model",

    # Workflows
    "OrchestratorWorkflow",
    "DegradationWorkflow",

    # Версия
    "__version__"
]
