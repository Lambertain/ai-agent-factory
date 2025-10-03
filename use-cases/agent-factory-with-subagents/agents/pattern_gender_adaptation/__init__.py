# -*- coding: utf-8 -*-
"""
Pattern Gender Adaptation Agent - пакет агента.

Экспорт основных компонентов агента для использования в PatternShift.
"""

from .agent import (
    create_pattern_gender_agent,
    get_pattern_gender_agent,
    run_pattern_gender_agent,
    run_gender_adaptation_workflow
)
from .dependencies import PatternGenderAdaptationDependencies, PatternToUniversalBridge
from .settings import load_settings, get_llm_model
from .workflow import GenderAdaptationWorkflow

__version__ = "1.0.0"

__all__ = [
    # Основные функции агента
    "create_pattern_gender_agent",
    "get_pattern_gender_agent",
    "run_pattern_gender_agent",
    "run_gender_adaptation_workflow",

    # Зависимости и настройки
    "PatternGenderAdaptationDependencies",
    "PatternToUniversalBridge",
    "load_settings",
    "get_llm_model",

    # Workflow
    "GenderAdaptationWorkflow",

    # Версия
    "__version__"
]
