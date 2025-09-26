#!/usr/bin/env python3
"""
Настройки для Archon Project Manager Agent.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv


class ProjectManagerSettings(BaseSettings):
    """Настройки Project Manager агента."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM настройки
    llm_api_key: str = Field(..., description="API ключ для LLM")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )
    llm_model: str = Field(
        default="qwen2.5-32b-instruct",
        description="Основная модель для управления проектами"
    )

    # Специализированные модели для разных типов управленческих задач
    llm_planning_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Экономичная модель для планирования"
    )
    llm_coordination_model: str = Field(
        default="qwen2.5-32b-instruct",
        description="Модель для координации команды"
    )
    llm_reporting_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для генерации отчетов"
    )
    llm_analysis_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Продвинутая модель для анализа проектов"
    )

    # Настройки управления проектами
    default_management_style: str = Field(
        default="agile",
        description="Стиль управления по умолчанию (agile/waterfall/hybrid/lean)"
    )
    default_team_size: int = Field(
        default=4,
        description="Размер команды по умолчанию"
    )
    sprint_duration_days: int = Field(
        default=14,
        description="Длительность спринта в днях"
    )
    planning_horizon_weeks: int = Field(
        default=8,
        description="Горизонт планирования в неделях"
    )

    # Настройки задач и приоритизации
    max_parallel_tasks: int = Field(
        default=10,
        description="Максимальное количество параллельных задач"
    )
    default_task_priority: str = Field(
        default="medium",
        description="Приоритет задач по умолчанию"
    )
    enable_automated_scheduling: bool = Field(
        default=True,
        description="Включить автоматическое планирование задач"
    )
    enable_dependency_tracking: bool = Field(
        default=True,
        description="Отслеживать зависимости между задачами"
    )

    # Настройки коммуникации
    daily_standup_enabled: bool = Field(
        default=True,
        description="Включить ежедневные stand-up встречи"
    )
    weekly_status_reports: bool = Field(
        default=True,
        description="Еженедельные отчеты о статусе"
    )
    milestone_notifications: bool = Field(
        default=True,
        description="Уведомления о достижении вех"
    )
    stakeholder_update_frequency: str = Field(
        default="weekly",
        description="Частота обновлений для стейкхолдеров"
    )

    # Настройки управления рисками
    enable_risk_management: bool = Field(
        default=True,
        description="Включить управление рисками"
    )
    risk_assessment_frequency: str = Field(
        default="weekly",
        description="Частота оценки рисков"
    )
    enable_risk_mitigation_planning: bool = Field(
        default=True,
        description="Планирование митигации рисков"
    )

    # Настройки мониторинга и метрик
    enable_progress_tracking: bool = Field(
        default=True,
        description="Отслеживание прогресса проекта"
    )
    enable_velocity_tracking: bool = Field(
        default=True,
        description="Отслеживание скорости выполнения задач"
    )
    enable_burndown_charts: bool = Field(
        default=True,
        description="Генерация burndown диаграмм"
    )
    enable_team_performance_metrics: bool = Field(
        default=True,
        description="Метрики производительности команды"
    )

    # Настройки качества
    enable_code_review_enforcement: bool = Field(
        default=True,
        description="Обязательные code review"
    )
    enable_testing_requirements: bool = Field(
        default=True,
        description="Обязательные требования к тестированию"
    )
    minimum_test_coverage: float = Field(
        default=80.0,
        description="Минимальное покрытие тестами (%)"
    )

    # Archon интеграция
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )
    archon_enabled: bool = Field(
        default=True,
        description="Включена ли интеграция с Archon"
    )

    # RAG и база знаний
    knowledge_base_enabled: bool = Field(
        default=True,
        description="Использование базы знаний для управления"
    )
    rag_search_threshold: float = Field(
        default=0.75,
        description="Порог релевантности для RAG поиска"
    )

    # Настройки автоматизации
    enable_automated_delegation: bool = Field(
        default=True,
        description="Автоматическое делегирование задач"
    )
    enable_resource_optimization: bool = Field(
        default=True,
        description="Оптимизация распределения ресурсов"
    )
    enable_cross_team_coordination: bool = Field(
        default=True,
        description="Межкомандная координация"
    )

    # Настройки отчетности
    report_generation_frequency: str = Field(
        default="daily",
        description="Частота генерации отчетов"
    )
    enable_dashboard_updates: bool = Field(
        default=True,
        description="Обновления дашборда в реальном времени"
    )
    enable_stakeholder_notifications: bool = Field(
        default=True,
        description="Уведомления стейкхолдеров"
    )

    # Настройки эскалации
    enable_automatic_escalation: bool = Field(
        default=True,
        description="Автоматическая эскалация проблем"
    )
    escalation_threshold_hours: int = Field(
        default=24,
        description="Порог времени для эскалации (часы)"
    )


def load_project_manager_settings() -> ProjectManagerSettings:
    """Загрузить настройки Project Manager."""
    load_dotenv()

    try:
        return ProjectManagerSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Project Manager: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model(task_type: str = "coordination"):
    """
    Получить сконфигурированную LLM модель для конкретного типа управленческих задач.

    Args:
        task_type: Тип задачи (coordination, planning, reporting, analysis)

    Returns:
        Сконфигурированная модель
    """
    settings = load_project_manager_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    # Выбираем модель в зависимости от типа задачи
    model_mapping = {
        "coordination": settings.llm_coordination_model,
        "planning": settings.llm_planning_model,
        "reporting": settings.llm_reporting_model,
        "analysis": settings.llm_analysis_model,
        "general": settings.llm_model
    }

    selected_model = model_mapping.get(task_type, settings.llm_model)
    return OpenAIModel(selected_model, provider=provider)


def get_management_defaults():
    """Получить настройки управления по умолчанию."""
    settings = load_project_manager_settings()

    return {
        "style": settings.default_management_style,
        "team_size": settings.default_team_size,
        "sprint_duration": settings.sprint_duration_days,
        "planning_horizon": settings.planning_horizon_weeks,
        "max_parallel_tasks": settings.max_parallel_tasks,
        "task_priority": settings.default_task_priority
    }


def get_communication_config():
    """Получить конфигурацию коммуникации."""
    settings = load_project_manager_settings()

    return {
        "daily_standup": settings.daily_standup_enabled,
        "weekly_reports": settings.weekly_status_reports,
        "milestone_notifications": settings.milestone_notifications,
        "stakeholder_frequency": settings.stakeholder_update_frequency,
        "automated_notifications": settings.enable_stakeholder_notifications
    }


def get_risk_management_config():
    """Получить конфигурацию управления рисками."""
    settings = load_project_manager_settings()

    return {
        "enabled": settings.enable_risk_management,
        "assessment_frequency": settings.risk_assessment_frequency,
        "mitigation_planning": settings.enable_risk_mitigation_planning
    }


def get_monitoring_config():
    """Получить конфигурацию мониторинга."""
    settings = load_project_manager_settings()

    return {
        "progress_tracking": settings.enable_progress_tracking,
        "velocity_tracking": settings.enable_velocity_tracking,
        "burndown_charts": settings.enable_burndown_charts,
        "team_metrics": settings.enable_team_performance_metrics,
        "dashboard_updates": settings.enable_dashboard_updates
    }


def get_quality_requirements():
    """Получить требования к качеству."""
    settings = load_project_manager_settings()

    return {
        "code_review_required": settings.enable_code_review_enforcement,
        "testing_required": settings.enable_testing_requirements,
        "min_test_coverage": settings.minimum_test_coverage
    }


def get_automation_config():
    """Получить конфигурацию автоматизации."""
    settings = load_project_manager_settings()

    return {
        "automated_delegation": settings.enable_automated_delegation,
        "resource_optimization": settings.enable_resource_optimization,
        "cross_team_coordination": settings.enable_cross_team_coordination,
        "automated_scheduling": settings.enable_automated_scheduling,
        "dependency_tracking": settings.enable_dependency_tracking
    }


def get_reporting_config():
    """Получить конфигурацию отчетности."""
    settings = load_project_manager_settings()

    return {
        "generation_frequency": settings.report_generation_frequency,
        "dashboard_enabled": settings.enable_dashboard_updates,
        "stakeholder_notifications": settings.enable_stakeholder_notifications
    }


def get_escalation_config():
    """Получить конфигурацию эскалации."""
    settings = load_project_manager_settings()

    return {
        "automatic_escalation": settings.enable_automatic_escalation,
        "threshold_hours": settings.escalation_threshold_hours
    }


def get_archon_integration_config():
    """Получить конфигурацию интеграции с Archon."""
    settings = load_project_manager_settings()

    return {
        "enabled": settings.archon_enabled,
        "project_id": settings.archon_project_id,
        "knowledge_base": settings.knowledge_base_enabled,
        "rag_threshold": settings.rag_search_threshold
    }