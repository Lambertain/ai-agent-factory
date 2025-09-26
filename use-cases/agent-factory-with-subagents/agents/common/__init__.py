#!/usr/bin/env python3
"""
Общие модули для всех агентов фабрики.

Содержит функциональность, используемую всеми агентами:
- Определение ключевых команд
- Автопереключение на Project Manager
- Проверка компетенций и делегирование задач
- Утилиты для работы с Archon
"""

from .keyword_detector import (
    KeywordDetector,
    should_switch_to_pm,
    get_command_context,
    detector
)

from .auto_switch_utf8 import (
    ProjectManagerSwitcher,
    auto_switch_to_project_manager,
    format_switch_result,
    check_pm_switch
)

from .competency_checker import (
    CompetencyChecker,
    CompetencyResult,
    AgentType,
    check_task_competency,
    should_delegate_task
)

__all__ = [
    # Детектор команд
    'KeywordDetector',
    'should_switch_to_pm',
    'get_command_context',
    'detector',

    # Автопереключение
    'ProjectManagerSwitcher',
    'auto_switch_to_project_manager',
    'format_switch_result',
    'check_pm_switch',

    # Проверка компетенций
    'CompetencyChecker',
    'CompetencyResult',
    'AgentType',
    'check_task_competency',
    'should_delegate_task'
]
# Планирование микрозадач
from .microtask_planner import (
    MicrotaskPlanner,
    TaskPlan,
    Microtask,
    TaskComplexity,
    MicrotaskStatus,
    create_microtask_plan,
    format_plan_for_approval,
    track_microtask_progress
)
