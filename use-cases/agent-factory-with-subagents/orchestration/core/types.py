"""
Основные типы данных для системы оркестрации субагентов.

Этот модуль содержит все базовые типы, перечисления и структуры данных,
используемые в системе интеллектуальной оркестрации.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Union
from datetime import datetime
from dataclasses import dataclass, field
from pydantic import BaseModel, Field


class TaskStatus(Enum):
    """Статусы выполнения задач."""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    """Приоритеты задач."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


class AgentStatus(Enum):
    """Статусы субагентов."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    UNAVAILABLE = "unavailable"


class ExecutionMode(Enum):
    """Режимы выполнения задач."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    PIPELINE = "pipeline"
    CONDITIONAL = "conditional"


@dataclass
class TaskDependency:
    """Зависимость между задачами."""
    task_id: str
    dependency_type: str = "completion"  # completion, data, resource
    condition: Optional[str] = None


@dataclass
class TaskResult:
    """Результат выполнения задачи."""
    task_id: str
    status: TaskStatus
    result_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Task(BaseModel):
    """Модель задачи для системы оркестрации."""

    id: str = Field(..., description="Уникальный идентификатор задачи")
    name: str = Field(..., description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")

    # Метаданные выполнения
    status: TaskStatus = Field(TaskStatus.PENDING, description="Статус выполнения")
    priority: TaskPriority = Field(TaskPriority.NORMAL, description="Приоритет задачи")

    # Агент и выполнение
    agent_type: Optional[str] = Field(None, description="Тип субагента для выполнения")
    execution_mode: ExecutionMode = Field(ExecutionMode.SEQUENTIAL, description="Режим выполнения")

    # Зависимости и связи
    dependencies: List[TaskDependency] = Field(default_factory=list, description="Зависимости задачи")
    parent_task_id: Optional[str] = Field(None, description="ID родительской задачи")
    subtasks: List[str] = Field(default_factory=list, description="ID подзадач")

    # Данные и параметры
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Входные данные")
    output_data: Dict[str, Any] = Field(default_factory=dict, description="Выходные данные")
    context: Dict[str, Any] = Field(default_factory=dict, description="Контекст выполнения")

    # Временные параметры
    created_at: datetime = Field(default_factory=datetime.now, description="Время создания")
    scheduled_at: Optional[datetime] = Field(None, description="Время планируемого выполнения")
    started_at: Optional[datetime] = Field(None, description="Время начала выполнения")
    completed_at: Optional[datetime] = Field(None, description="Время завершения")
    timeout: Optional[int] = Field(None, description="Таймаут выполнения в секундах")

    # Метрики и мониторинг
    retry_count: int = Field(0, description="Количество попыток выполнения")
    max_retries: int = Field(3, description="Максимальное количество попыток")
    estimated_duration: Optional[int] = Field(None, description="Оценочное время выполнения")
    actual_duration: Optional[float] = Field(None, description="Фактическое время выполнения")

    # Результат выполнения
    result: Optional[TaskResult] = Field(None, description="Результат выполнения")
    error_message: Optional[str] = Field(None, description="Сообщение об ошибке")


class Agent(BaseModel):
    """Модель субагента в системе оркестрации."""

    id: str = Field(..., description="Уникальный идентификатор агента")
    name: str = Field(..., description="Название агента")
    type: str = Field(..., description="Тип агента")
    description: Optional[str] = Field(None, description="Описание возможностей агента")

    # Статус и доступность
    status: AgentStatus = Field(AgentStatus.IDLE, description="Текущий статус")
    is_available: bool = Field(True, description="Доступность для выполнения задач")

    # Возможности
    capabilities: List[str] = Field(default_factory=list, description="Список возможностей")
    supported_tasks: List[str] = Field(default_factory=list, description="Поддерживаемые типы задач")

    # Нагрузка и производительность
    current_load: int = Field(0, description="Текущая нагрузка (количество активных задач)")
    max_concurrent_tasks: int = Field(1, description="Максимальное количество одновременных задач")
    average_execution_time: Optional[float] = Field(None, description="Среднее время выполнения задач")

    # Метрики
    completed_tasks: int = Field(0, description="Количество завершенных задач")
    failed_tasks: int = Field(0, description="Количество неудачных задач")
    success_rate: float = Field(1.0, description="Коэффициент успешности")

    # Временные метки
    created_at: datetime = Field(default_factory=datetime.now, description="Время создания")
    last_activity: Optional[datetime] = Field(None, description="Время последней активности")

    # Конфигурация
    config: Dict[str, Any] = Field(default_factory=dict, description="Конфигурация агента")


@dataclass
class ExecutionPlan:
    """План выполнения группы задач."""
    plan_id: str
    tasks: List[Task]
    execution_order: List[str]  # Порядок выполнения задач
    parallel_groups: List[List[str]]  # Группы задач для параллельного выполнения
    estimated_total_time: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class OrchestrationConfig:
    """Конфигурация системы оркестрации."""
    max_concurrent_tasks: int = 10
    max_queue_size: int = 1000
    default_task_timeout: int = 300  # 5 минут
    retry_delays: List[int] = field(default_factory=lambda: [1, 5, 15])  # секунды
    enable_parallel_execution: bool = True
    enable_load_balancing: bool = True
    monitoring_interval: int = 30  # секунды
    cleanup_completed_tasks_after: int = 3600  # 1 час


class OrchestrationEvent(BaseModel):
    """События в системе оркестрации."""
    event_id: str = Field(..., description="ID события")
    event_type: str = Field(..., description="Тип события")
    source: str = Field(..., description="Источник события")
    timestamp: datetime = Field(default_factory=datetime.now, description="Время события")
    data: Dict[str, Any] = Field(default_factory=dict, description="Данные события")
    task_id: Optional[str] = Field(None, description="ID связанной задачи")
    agent_id: Optional[str] = Field(None, description="ID связанного агента")


# Типы для функций обратного вызова
TaskCallback = Callable[[Task], None]
AgentCallback = Callable[[Agent], None]
EventCallback = Callable[[OrchestrationEvent], None]

# Типы для стратегий
LoadBalancingStrategy = Callable[[List[Agent], Task], Agent]
PriorityStrategy = Callable[[List[Task]], List[Task]]
SchedulingStrategy = Callable[[List[Task]], List[Task]]