#!/usr/bin/env python3
"""
Archon Project Manager Agent - главный координатор команды Archon.

Экспорт основных компонентов агента.
"""

from .agent import project_manager_agent, run_project_manager
from .dependencies import (
    ProjectManagerDependencies,
    ProjectPhase,
    TaskPriority,
    TeamRole,
    ManagementStyle
)
from .settings import (
    load_project_manager_settings,
    get_llm_model,
    get_management_defaults,
    get_communication_config,
    get_risk_management_config,
    get_monitoring_config,
    get_quality_requirements,
    get_automation_config,
    get_reporting_config,
    get_escalation_config,
    get_archon_integration_config
)
from .tools import (
    create_project_plan,
    manage_task_priorities,
    coordinate_team_work,
    generate_status_report,
    manage_project_risks,
    schedule_tasks,
    track_progress,
    search_management_knowledge,
    delegate_task
)
from .prompts import get_system_prompt

__all__ = [
    # Основной агент
    "project_manager_agent",
    "run_project_manager",

    # Конфигурация
    "ProjectManagerDependencies",
    "ProjectPhase",
    "TaskPriority",
    "TeamRole",
    "ManagementStyle",

    # Настройки
    "load_project_manager_settings",
    "get_llm_model",
    "get_management_defaults",
    "get_communication_config",
    "get_risk_management_config",
    "get_monitoring_config",
    "get_quality_requirements",
    "get_automation_config",
    "get_reporting_config",
    "get_escalation_config",
    "get_archon_integration_config",

    # Инструменты
    "create_project_plan",
    "manage_task_priorities",
    "coordinate_team_work",
    "generate_status_report",
    "manage_project_risks",
    "schedule_tasks",
    "track_progress",
    "search_management_knowledge",
    "delegate_task",

    # Промпты
    "get_system_prompt"
]