"""
Система интеллектуальной оркестрации субагентов.

Этот пакет содержит полную систему для умного управления субагентами,
включая планирование, балансировку нагрузки, управление зависимостями
и параллельное выполнение задач.
"""

from .core.orchestrator import AgentOrchestrator
from .core.types import (
    Task, Agent, TaskResult, TaskStatus, TaskPriority, AgentStatus,
    ExecutionMode, OrchestrationConfig, OrchestrationEvent
)
from .core.interfaces import IOrchestrator

# Основные компоненты
from .schedulers.task_queue import PriorityTaskQueue
from .schedulers.task_scheduler import SmartTaskScheduler
from .managers.dependency_manager import TaskDependencyManager
from .managers.priority_manager import SmartPriorityManager
from .balancers.load_balancer import SmartLoadBalancer
from .engines.execution_engine import ParallelExecutionEngine

__version__ = "1.0.0"

__all__ = [
    # Основной оркестратор
    "AgentOrchestrator",

    # Типы данных
    "Task",
    "Agent",
    "TaskResult",
    "TaskStatus",
    "TaskPriority",
    "AgentStatus",
    "ExecutionMode",
    "OrchestrationConfig",
    "OrchestrationEvent",

    # Интерфейсы
    "IOrchestrator",

    # Компоненты
    "PriorityTaskQueue",
    "SmartTaskScheduler",
    "TaskDependencyManager",
    "SmartPriorityManager",
    "SmartLoadBalancer",
    "ParallelExecutionEngine",
]