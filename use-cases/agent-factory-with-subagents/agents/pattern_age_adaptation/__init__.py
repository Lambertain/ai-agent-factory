# -*- coding: utf-8 -*-
"""
Pattern Age Adaptation Agent - пакет агента.

Экспорт основных компонентов агента для использования в PatternShift.
"""

from .agent import (
    create_pattern_age_agent,
    get_pattern_age_agent,
    run_pattern_age_agent,
    run_age_adaptation_workflow
)
from .dependencies import PatternAgeAdaptationDependencies, PatternAgeToUniversalBridge
from .settings import load_settings, get_llm_model
from .workflow import AgeAdaptationWorkflow

__version__ = "1.0.0"

__all__ = [
    # Основные функции агента
    "create_pattern_age_agent",
    "get_pattern_age_agent",
    "run_pattern_age_agent",
    "run_age_adaptation_workflow",

    # Зависимости и настройки
    "PatternAgeAdaptationDependencies",
    "PatternAgeToUniversalBridge",
    "load_settings",
    "get_llm_model",

    # Workflow
    "AgeAdaptationWorkflow",

    # Версия
    "__version__"
]
