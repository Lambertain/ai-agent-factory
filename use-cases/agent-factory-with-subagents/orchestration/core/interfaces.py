"""
Интерфейсы для системы оркестрации субагентов.

Этот модуль определяет базовые интерфейсы и абстрактные классы,
которые должны реализовывать компоненты системы оркестрации.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, AsyncIterator
from .types import Task, Agent, TaskResult, ExecutionPlan, OrchestrationEvent


class ITaskQueue(ABC):
    """Интерфейс для очереди задач."""

    @abstractmethod
    async def enqueue(self, task: Task) -> bool:
        """Добавить задачу в очередь."""
        pass

    @abstractmethod
    async def dequeue(self, agent_capabilities: Optional[List[str]] = None) -> Optional[Task]:
        """Извлечь задачу из очереди для агента с указанными возможностями."""
        pass

    @abstractmethod
    async def peek(self, count: int = 1) -> List[Task]:
        """Просмотреть задачи в очереди без извлечения."""
        pass

    @abstractmethod
    async def size(self) -> int:
        """Получить размер очереди."""
        pass

    @abstractmethod
    async def is_empty(self) -> bool:
        """Проверить, пуста ли очередь."""
        pass

    @abstractmethod
    async def remove_task(self, task_id: str) -> bool:
        """Удалить задачу из очереди по ID."""
        pass

    @abstractmethod
    async def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Получить задачи с определенным приоритетом."""
        pass


class ITaskScheduler(ABC):
    """Интерфейс для планировщика задач."""

    @abstractmethod
    async def schedule_task(self, task: Task) -> bool:
        """Запланировать выполнение задачи."""
        pass

    @abstractmethod
    async def schedule_tasks(self, tasks: List[Task]) -> bool:
        """Запланировать выполнение нескольких задач."""
        pass

    @abstractmethod
    async def cancel_task(self, task_id: str) -> bool:
        """Отменить запланированную задачу."""
        pass

    @abstractmethod
    async def reschedule_task(self, task_id: str, new_time: Optional[str] = None) -> bool:
        """Перепланировать задачу."""
        pass

    @abstractmethod
    async def get_scheduled_tasks(self) -> List[Task]:
        """Получить список запланированных задач."""
        pass

    @abstractmethod
    async def get_ready_tasks(self) -> List[Task]:
        """Получить задачи, готовые к выполнению."""
        pass


class IDependencyManager(ABC):
    """Интерфейс для менеджера зависимостей."""

    @abstractmethod
    async def add_dependency(self, task_id: str, dependency_task_id: str,
                           dependency_type: str = "completion") -> bool:
        """Добавить зависимость между задачами."""
        pass

    @abstractmethod
    async def remove_dependency(self, task_id: str, dependency_task_id: str) -> bool:
        """Удалить зависимость между задачами."""
        pass

    @abstractmethod
    async def get_dependencies(self, task_id: str) -> List[str]:
        """Получить список зависимостей для задачи."""
        pass

    @abstractmethod
    async def get_dependents(self, task_id: str) -> List[str]:
        """Получить список задач, зависящих от данной."""
        pass

    @abstractmethod
    async def is_ready_to_execute(self, task_id: str) -> bool:
        """Проверить, готова ли задача к выполнению (все зависимости выполнены)."""
        pass

    @abstractmethod
    async def resolve_execution_order(self, tasks: List[Task]) -> List[Task]:
        """Определить порядок выполнения задач с учетом зависимостей."""
        pass

    @abstractmethod
    async def detect_circular_dependencies(self, tasks: List[Task]) -> List[List[str]]:
        """Обнаружить циклические зависимости."""
        pass


class ILoadBalancer(ABC):
    """Интерфейс для балансировщика нагрузки."""

    @abstractmethod
    async def select_agent(self, task: Task, available_agents: List[Agent]) -> Optional[Agent]:
        """Выбрать наилучшего агента для выполнения задачи."""
        pass

    @abstractmethod
    async def distribute_tasks(self, tasks: List[Task], agents: List[Agent]) -> Dict[str, List[str]]:
        """Распределить задачи между агентами."""
        pass

    @abstractmethod
    async def rebalance(self, agents: List[Agent]) -> Dict[str, List[str]]:
        """Перебалансировать нагрузку между агентами."""
        pass

    @abstractmethod
    async def get_load_metrics(self, agent_id: str) -> Dict[str, float]:
        """Получить метрики нагрузки для агента."""
        pass

    @abstractmethod
    async def update_agent_metrics(self, agent_id: str, metrics: Dict[str, Any]) -> bool:
        """Обновить метрики агента."""
        pass


class IExecutionEngine(ABC):
    """Интерфейс для движка выполнения."""

    @abstractmethod
    async def execute_task(self, task: Task, agent: Agent) -> TaskResult:
        """Выполнить одну задачу."""
        pass

    @abstractmethod
    async def execute_tasks_parallel(self, tasks: List[Task], agents: List[Agent]) -> List[TaskResult]:
        """Выполнить задачи параллельно."""
        pass

    @abstractmethod
    async def execute_tasks_sequential(self, tasks: List[Task], agents: List[Agent]) -> List[TaskResult]:
        """Выполнить задачи последовательно."""
        pass

    @abstractmethod
    async def execute_pipeline(self, plan: ExecutionPlan, agents: List[Agent]) -> List[TaskResult]:
        """Выполнить план как конвейер задач."""
        pass

    @abstractmethod
    async def stop_execution(self, task_id: str) -> bool:
        """Остановить выполнение задачи."""
        pass

    @abstractmethod
    async def pause_execution(self, task_id: str) -> bool:
        """Приостановить выполнение задачи."""
        pass

    @abstractmethod
    async def resume_execution(self, task_id: str) -> bool:
        """Возобновить выполнение задачи."""
        pass


class IPriorityManager(ABC):
    """Интерфейс для менеджера приоритетов."""

    @abstractmethod
    async def assign_priority(self, task: Task) -> Task:
        """Назначить приоритет задаче."""
        pass

    @abstractmethod
    async def update_priority(self, task_id: str, new_priority: str) -> bool:
        """Обновить приоритет задачи."""
        pass

    @abstractmethod
    async def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Отсортировать задачи по приоритету."""
        pass

    @abstractmethod
    async def escalate_priority(self, task_id: str, reason: str) -> bool:
        """Повысить приоритет задачи."""
        pass

    @abstractmethod
    async def calculate_dynamic_priority(self, task: Task) -> float:
        """Вычислить динамический приоритет на основе различных факторов."""
        pass


class IAgentRegistry(ABC):
    """Интерфейс для реестра агентов."""

    @abstractmethod
    async def register_agent(self, agent: Agent) -> bool:
        """Зарегистрировать агента."""
        pass

    @abstractmethod
    async def unregister_agent(self, agent_id: str) -> bool:
        """Отменить регистрацию агента."""
        pass

    @abstractmethod
    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Получить агента по ID."""
        pass

    @abstractmethod
    async def get_all_agents(self) -> List[Agent]:
        """Получить всех зарегистрированных агентов."""
        pass

    @abstractmethod
    async def get_available_agents(self) -> List[Agent]:
        """Получить доступных агентов."""
        pass

    @abstractmethod
    async def get_agents_by_capability(self, capability: str) -> List[Agent]:
        """Получить агентов с определенной возможностью."""
        pass

    @abstractmethod
    async def update_agent_status(self, agent_id: str, status: str) -> bool:
        """Обновить статус агента."""
        pass

    @abstractmethod
    async def health_check(self, agent_id: str) -> bool:
        """Проверить здоровье агента."""
        pass


class IEventDispatcher(ABC):
    """Интерфейс для диспетчера событий."""

    @abstractmethod
    async def publish_event(self, event: OrchestrationEvent) -> bool:
        """Опубликовать событие."""
        pass

    @abstractmethod
    async def subscribe(self, event_type: str, callback) -> bool:
        """Подписаться на события определенного типа."""
        pass

    @abstractmethod
    async def unsubscribe(self, event_type: str, callback) -> bool:
        """Отписаться от событий."""
        pass

    @abstractmethod
    async def get_events(self, event_type: Optional[str] = None,
                        limit: int = 100) -> List[OrchestrationEvent]:
        """Получить события."""
        pass


class IOrchestrator(ABC):
    """Главный интерфейс оркестратора."""

    @abstractmethod
    async def submit_task(self, task: Task) -> str:
        """Подать задачу на выполнение."""
        pass

    @abstractmethod
    async def submit_tasks(self, tasks: List[Task]) -> List[str]:
        """Подать несколько задач на выполнение."""
        pass

    @abstractmethod
    async def get_task_status(self, task_id: str) -> Optional[str]:
        """Получить статус задачи."""
        pass

    @abstractmethod
    async def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """Получить результат выполнения задачи."""
        pass

    @abstractmethod
    async def cancel_task(self, task_id: str) -> bool:
        """Отменить задачу."""
        pass

    @abstractmethod
    async def wait_for_completion(self, task_id: str, timeout: Optional[int] = None) -> TaskResult:
        """Ждать завершения задачи."""
        pass

    @abstractmethod
    async def get_system_status(self) -> Dict[str, Any]:
        """Получить статус системы оркестрации."""
        pass

    @abstractmethod
    async def shutdown(self) -> bool:
        """Корректно завершить работу оркестратора."""
        pass

    @abstractmethod
    async def start(self) -> bool:
        """Запустить оркестратор."""
        pass


class IMonitor(ABC):
    """Интерфейс для мониторинга системы."""

    @abstractmethod
    async def collect_metrics(self) -> Dict[str, Any]:
        """Собрать метрики системы."""
        pass

    @abstractmethod
    async def get_performance_stats(self) -> Dict[str, Any]:
        """Получить статистику производительности."""
        pass

    @abstractmethod
    async def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Обнаружить аномалии в работе системы."""
        pass

    @abstractmethod
    async def generate_report(self, period: str = "hour") -> Dict[str, Any]:
        """Сгенерировать отчет за период."""
        pass


class IErrorHandler(ABC):
    """Интерфейс для обработки ошибок."""

    @abstractmethod
    async def handle_error(self, error: Exception, context: Dict[str, Any]) -> bool:
        """Обработать ошибку."""
        pass

    @abstractmethod
    async def should_retry(self, error: Exception, retry_count: int) -> bool:
        """Определить, следует ли повторить операцию."""
        pass

    @abstractmethod
    async def get_retry_delay(self, retry_count: int) -> int:
        """Получить задержку перед повтором."""
        pass

    @abstractmethod
    async def escalate_error(self, error: Exception, context: Dict[str, Any]) -> bool:
        """Эскалировать ошибку."""
        pass