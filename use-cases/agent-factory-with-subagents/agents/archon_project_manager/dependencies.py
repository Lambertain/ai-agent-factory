#!/usr/bin/env python3
"""
Зависимости для Archon Project Manager Agent.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class ProjectPhase(Enum):
    """Фазы проекта."""
    PLANNING = "planning"
    ANALYSIS = "analysis"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"


class TaskPriority(Enum):
    """Приоритеты задач."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TeamRole(Enum):
    """Роли команды."""
    ANALYSIS_LEAD = "analysis_lead"
    BLUEPRINT_ARCHITECT = "blueprint_architect"
    IMPLEMENTATION_ENGINEER = "implementation_engineer"
    QUALITY_GUARDIAN = "quality_guardian"
    PROJECT_MANAGER = "project_manager"


class ManagementStyle(Enum):
    """Стили управления проектом."""
    AGILE = "agile"
    WATERFALL = "waterfall"
    HYBRID = "hybrid"
    LEAN = "lean"


@dataclass
class ProjectManagerDependencies:
    """
    Зависимости для Project Manager Agent.

    Конфигурирует поведение агента для различных типов управления проектами.
    """

    # Основные настройки
    project_id: str = "default"
    management_style: ManagementStyle = ManagementStyle.AGILE
    current_phase: ProjectPhase = ProjectPhase.PLANNING

    # Archon интеграция
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
    archon_enabled: bool = True

    # Команда и роли
    team_size: int = 4
    available_roles: List[str] = field(default_factory=lambda: [
        "Analysis Lead", "Blueprint Architect", "Implementation Engineer", "Quality Guardian"
    ])

    # Настройки планирования
    sprint_duration_days: int = 14
    planning_horizon_weeks: int = 8
    enable_risk_management: bool = True
    enable_resource_optimization: bool = True

    # Управление задачами
    default_task_priority: TaskPriority = TaskPriority.MEDIUM
    max_parallel_tasks: int = 10
    enable_dependency_tracking: bool = True
    enable_automated_scheduling: bool = True

    # Коммуникации и отчетность
    daily_standup_enabled: bool = True
    weekly_status_reports: bool = True
    milestone_notifications: bool = True
    stakeholder_updates_frequency: str = "weekly"

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "project-management", "agile", "coordination", "agent-knowledge"
    ])
    knowledge_domain: str = "management.archon.local"

    # Мониторинг и метрики
    enable_progress_tracking: bool = True
    enable_velocity_tracking: bool = True
    enable_burndown_charts: bool = True
    enable_team_performance_metrics: bool = True

    # Настройки качества
    enable_code_review_enforcement: bool = True
    enable_testing_requirements: bool = True
    minimum_test_coverage: float = 80.0

    # Коллаборация
    enable_cross_team_coordination: bool = True
    enable_stakeholder_communication: bool = True
    enable_automated_delegation: bool = True

    def get_management_config(self) -> Dict[str, Any]:
        """Получить конфигурацию управления проектом."""
        return {
            "style": self.management_style.value,
            "phase": self.current_phase.value,
            "sprint_duration": self.sprint_duration_days,
            "planning_horizon": self.planning_horizon_weeks,
            "team_size": self.team_size,
            "max_parallel_tasks": self.max_parallel_tasks,
            "risk_management": self.enable_risk_management,
            "resource_optimization": self.enable_resource_optimization
        }

    def get_communication_config(self) -> Dict[str, Any]:
        """Получить конфигурацию коммуникации."""
        return {
            "daily_standup": self.daily_standup_enabled,
            "weekly_reports": self.weekly_status_reports,
            "milestone_notifications": self.milestone_notifications,
            "stakeholder_frequency": self.stakeholder_updates_frequency,
            "cross_team_coordination": self.enable_cross_team_coordination
        }

    def get_quality_requirements(self) -> Dict[str, Any]:
        """Получить требования к качеству."""
        return {
            "code_review_required": self.enable_code_review_enforcement,
            "testing_required": self.enable_testing_requirements,
            "min_test_coverage": self.minimum_test_coverage,
            "dependency_tracking": self.enable_dependency_tracking
        }

    def get_team_allocation_strategy(self) -> Dict[str, Any]:
        """Получить стратегию распределения команды."""
        if self.management_style == ManagementStyle.AGILE:
            return {
                "approach": "cross_functional_teams",
                "task_assignment": "pull_based",
                "capacity_planning": "story_points",
                "retrospectives": True
            }
        elif self.management_style == ManagementStyle.WATERFALL:
            return {
                "approach": "phase_based_teams",
                "task_assignment": "push_based",
                "capacity_planning": "time_estimation",
                "retrospectives": False
            }
        else:  # HYBRID or LEAN
            return {
                "approach": "flexible_teams",
                "task_assignment": "adaptive",
                "capacity_planning": "hybrid",
                "retrospectives": True
            }

    def get_priority_matrix(self) -> Dict[str, int]:
        """Получить матрицу приоритетов для задач."""
        return {
            TaskPriority.CRITICAL.value: 1,
            TaskPriority.HIGH.value: 2,
            TaskPriority.MEDIUM.value: 3,
            TaskPriority.LOW.value: 4
        }

    def get_scheduling_rules(self) -> Dict[str, Any]:
        """Получить правила планирования задач."""
        rules = {
            "respect_dependencies": self.enable_dependency_tracking,
            "balance_workload": True,
            "consider_skills": True,
            "automated_scheduling": self.enable_automated_scheduling
        }

        if self.management_style == ManagementStyle.AGILE:
            rules.update({
                "sprint_based": True,
                "story_estimation": True,
                "velocity_consideration": self.enable_velocity_tracking
            })

        return rules

    def get_risk_management_config(self) -> Dict[str, Any]:
        """Получить конфигурацию управления рисками."""
        if not self.enable_risk_management:
            return {"enabled": False}

        return {
            "enabled": True,
            "risk_assessment_frequency": "weekly",
            "mitigation_planning": True,
            "stakeholder_communication": True,
            "risk_categories": [
                "technical_risk",
                "resource_risk",
                "timeline_risk",
                "quality_risk",
                "integration_risk"
            ]
        }

    def get_reporting_config(self) -> Dict[str, Any]:
        """Получить конфигурацию отчетности."""
        return {
            "progress_tracking": self.enable_progress_tracking,
            "velocity_tracking": self.enable_velocity_tracking,
            "burndown_charts": self.enable_burndown_charts,
            "team_metrics": self.enable_team_performance_metrics,
            "automated_reports": True,
            "dashboard_updates": "real_time"
        }

    def should_delegate_task(self, task_type: str, complexity: str) -> Optional[str]:
        """
        Определить кому следует делегировать задачу.

        Args:
            task_type: Тип задачи
            complexity: Сложность задачи

        Returns:
            Роль исполнителя или None если задачу выполняет PM
        """
        delegation_rules = {
            "analysis": "Analysis Lead",
            "architecture": "Blueprint Architect",
            "implementation": "Implementation Engineer",
            "testing": "Quality Guardian",
            "code_review": "Quality Guardian",
            "documentation": "Implementation Engineer",
            "planning": None,  # PM выполняет сам
            "coordination": None,  # PM выполняет сам
            "reporting": None   # PM выполняет сам
        }

        # Для критически важных задач всегда привлекаем специалистов
        if complexity == "critical" and task_type in delegation_rules:
            return delegation_rules.get(task_type)

        return delegation_rules.get(task_type, None)

    def get_milestone_schedule(self) -> List[Dict[str, Any]]:
        """Получить расписание вех проекта."""
        if self.management_style == ManagementStyle.AGILE:
            return [
                {"name": "Sprint Planning", "frequency": f"{self.sprint_duration_days} days"},
                {"name": "Sprint Review", "frequency": f"{self.sprint_duration_days} days"},
                {"name": "Sprint Retrospective", "frequency": f"{self.sprint_duration_days} days"},
                {"name": "Release Planning", "frequency": "monthly"}
            ]
        elif self.management_style == ManagementStyle.WATERFALL:
            return [
                {"name": "Requirements Sign-off", "phase": "analysis"},
                {"name": "Design Review", "phase": "design"},
                {"name": "Implementation Complete", "phase": "implementation"},
                {"name": "Testing Complete", "phase": "testing"},
                {"name": "Production Deployment", "phase": "deployment"}
            ]
        else:
            return [
                {"name": "Phase Review", "frequency": "bi-weekly"},
                {"name": "Quality Gate", "frequency": "monthly"},
                {"name": "Stakeholder Review", "frequency": "monthly"}
            ]