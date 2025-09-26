#!/usr/bin/env python3
"""
Archon Analysis Lead Agent - главный аналитик команды Archon.

Экспорт основных компонентов агента.
"""

from .agent import analysis_lead_agent, run_analysis_lead
from .dependencies import AnalysisLeadDependencies, AnalysisMethod, RequirementType
from .settings import load_analysis_settings, get_llm_model
from .tools import (
    analyze_requirements,
    decompose_task,
    research_solutions,
    create_analysis_report,
    search_analysis_knowledge
)
from .prompts import get_system_prompt

__all__ = [
    # Основной агент
    "analysis_lead_agent",
    "run_analysis_lead",

    # Конфигурация
    "AnalysisLeadDependencies",
    "AnalysisMethod",
    "RequirementType",

    # Настройки
    "load_analysis_settings",
    "get_llm_model",

    # Инструменты
    "analyze_requirements",
    "decompose_task",
    "research_solutions",
    "create_analysis_report",
    "search_analysis_knowledge",

    # Промпты
    "get_system_prompt"
]