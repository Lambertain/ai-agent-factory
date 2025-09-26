"""
Центральный оркестратор для координации всех компонентов системы.

Этот модуль является главным координатором, который объединяет все компоненты
системы оркестрации и предоставляет единый интерфейс для управления задачами.
"""

import asyncio
from typing import List, Dict, Optional, Any, Set
from datetime import datetime, timezone, timedelta
import logging
import uuid

from ..interfaces import (
    IOrchestrator, ITaskQueue, ITaskScheduler, IDependencyManager,
    ILoadBalancer, IExecutionEngine, IPriorityManager, IAgentRegistry,
    IEventDispatcher, IMonitor, IErrorHandler
)
from ..types import (
    Task, Agent, TaskResult, TaskStatus, AgentStatus, OrchestrationConfig,
    OrchestrationEvent, ExecutionPlan
)

from ...schedulers.task_queue import PriorityTaskQueue
from ...schedulers.task_scheduler import SmartTaskScheduler
from ...managers.dependency_manager import TaskDependencyManager
from ...managers.priority_manager import SmartPriorityManager
from ...balancers.load_balancer import SmartLoadBalancer
from ...engines.execution_engine import ParallelExecutionEngine


class AgentOrchestrator(IOrchestrator):
    """
    Центральный оркестратор субагентов.

    Координирует работу всех компонентов системы:
    - Управление очередью задач
    - Планирование выполнения
    - Балансировка нагрузки
    - Выполнение задач
    - Мониторинг и логирование
    """

    def __init__(self, config: Optional[OrchestrationConfig] = None):
        """
        Инициализация оркестратора.

        Args:
            config: Конфигурация оркестрации
        """
        self.config = config or OrchestrationConfig()
        self.logger = logging.getLogger(__name__)

        # Инициализация компонентов
        self._init_components()

        # Состояние оркестратора
        self._is_running = False
        self._shutdown_event = asyncio.Event()

        # Мониторинг
        self._monitoring_task: Optional[asyncio.Task] = None
        self._auto_escalation_task: Optional[asyncio.Task] = None

        # Метрики
        self._metrics = {
            "tasks_submitted": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "average_wait_time": 0.0,
            "average_execution_time": 0.0,
            "system_uptime": datetime.now(timezone.utc)
        }

        # Блокировка для thread-safety
        self._lock = asyncio.Lock()

    def _init_components(self):
        """Инициализировать все компоненты системы."""
        # Очередь задач
        self.task_queue: ITaskQueue = PriorityTaskQueue(
            max_size=self.config.max_queue_size
        )

        # Менеджер зависимостей
        self.dependency_manager: IDependencyManager = TaskDependencyManager()

        # Планировщик
        self.scheduler: ITaskScheduler = SmartTaskScheduler(
            dependency_manager=self.dependency_manager
        )

        # Менеджер приоритетов
        self.priority_manager: IPriorityManager = SmartPriorityManager()

        # Балансировщик нагрузки
        self.load_balancer: ILoadBalancer = SmartLoadBalancer()

        # Движок выполнения
        self.execution_engine: IExecutionEngine = ParallelExecutionEngine(
            max_concurrent_tasks=self.config.max_concurrent_tasks
        )

        # Реестр агентов (простая реализация)
        self._agents: Dict[str, Agent] = {}

        # События (простая реализация)
        self._event_subscribers: Dict[str, List] = {}

        self.logger.info("All orchestration components initialized")

    async def start(self) -> bool:
        """
        Запустить оркестратор.

        Returns:
            True если запуск успешен
        """
        if self._is_running:
            self.logger.warning("Orchestrator is already running")
            return False

        try:
            # Запускаем компоненты
            await self.scheduler.start()

            # Запускаем фоновые задачи
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            self._auto_escalation_task = asyncio.create_task(self._auto_escalation_loop())

            self._is_running = True
            self._metrics["system_uptime"] = datetime.now(timezone.utc)

            self.logger.info("Agent Orchestrator started successfully")

            # Публикуем событие запуска
            await self._publish_event("orchestrator.started", {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "config": self.config.__dict__
            })

            return True

        except Exception as e:
            self.logger.error(f"Failed to start orchestrator: {e}")
            return False

    async def shutdown(self) -> bool:
        """
        Корректно завершить работу оркестратора.

        Returns:
            True если завершение успешно
        """
        if not self._is_running:
            return True

        self.logger.info("Shutting down Agent Orchestrator...")

        try:
            # Устанавливаем флаг завершения
            self._shutdown_event.set()
            self._is_running = False

            # Останавливаем фоновые задачи
            if self._monitoring_task:
                self._monitoring_task.cancel()
                try:
                    await self._monitoring_task
                except asyncio.CancelledError:
                    pass

            if self._auto_escalation_task:
                self._auto_escalation_task.cancel()
                try:
                    await self._auto_escalation_task
                except asyncio.CancelledError:
                    pass

            # Останавливаем компоненты
            await self.scheduler.stop()
            await self.execution_engine.shutdown()

            # Публикуем событие завершения
            await self._publish_event("orchestrator.shutdown", {
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

            self.logger.info("Agent Orchestrator shutdown completed")
            return True

        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
            return False

    async def submit_task(self, task: Task) -> str:
        """
        Подать задачу на выполнение.

        Args:
            task: Задача для выполнения

        Returns:
            ID задачи
        """
        if not self._is_running:
            raise RuntimeError("Orchestrator is not running")

        async with self._lock:
            # Назначаем приоритет
            task = await self.priority_manager.assign_priority(task)

            # Планируем задачу
            scheduled = await self.scheduler.schedule_task(task)
            if not scheduled:
                raise RuntimeError(f"Failed to schedule task {task.id}")

            # Добавляем в очередь
            queued = await self.task_queue.enqueue(task)
            if not queued:
                raise RuntimeError(f"Failed to enqueue task {task.id}")

            # Обновляем метрики
            self._metrics["tasks_submitted"] += 1

            # Публикуем событие
            await self._publish_event("task.submitted", {
                "task_id": task.id,
                "priority": task.priority.name,
                "agent_type": task.agent_type
            })

            self.logger.info(f"Task {task.id} submitted successfully")
            return task.id

    async def submit_tasks(self, tasks: List[Task]) -> List[str]:
        """
        Подать несколько задач на выполнение.

        Args:
            tasks: Список задач

        Returns:
            Список ID задач
        """
        task_ids = []
        for task in tasks:
            try:
                task_id = await self.submit_task(task)
                task_ids.append(task_id)
            except Exception as e:
                self.logger.error(f"Failed to submit task {task.id}: {e}")

        return task_ids

    async def get_task_status(self, task_id: str) -> Optional[str]:
        """
        Получить статус задачи.

        Args:
            task_id: ID задачи

        Returns:
            Статус задачи или None
        """
        # Проверяем в различных местах
        scheduled_tasks = await self.scheduler.get_scheduled_tasks()
        for task in scheduled_tasks:
            if task.id == task_id:
                return task.status.value

        ready_tasks = await self.scheduler.get_ready_tasks()
        for task in ready_tasks:
            if task.id == task_id:
                return task.status.value

        return None

    async def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """
        Получить результат выполнения задачи.

        Args:
            task_id: ID задачи

        Returns:
            Результат выполнения или None
        """
        # В реальной системе здесь был бы поиск в хранилище результатов
        return None

    async def cancel_task(self, task_id: str) -> bool:
        """
        Отменить задачу.

        Args:
            task_id: ID задачи

        Returns:
            True если задача отменена
        """
        try:
            # Пытаемся отменить в планировщике
            cancelled_in_scheduler = await self.scheduler.cancel_task(task_id)

            # Пытаемся остановить выполнение
            stopped_execution = await self.execution_engine.stop_execution(task_id)

            # Удаляем из очереди
            removed_from_queue = await self.task_queue.remove_task(task_id)

            success = cancelled_in_scheduler or stopped_execution or removed_from_queue

            if success:
                await self._publish_event("task.cancelled", {"task_id": task_id})
                self.logger.info(f"Task {task_id} cancelled")

            return success

        except Exception as e:
            self.logger.error(f"Failed to cancel task {task_id}: {e}")
            return False

    async def wait_for_completion(self, task_id: str, timeout: Optional[int] = None) -> TaskResult:
        """
        Ждать завершения задачи.

        Args:
            task_id: ID задачи
            timeout: Таймаут ожидания в секундах

        Returns:
            Результат выполнения задачи
        """
        start_time = datetime.now(timezone.utc)
        timeout_seconds = timeout or self.config.default_task_timeout

        while True:
            # Проверяем результат
            result = await self.get_task_result(task_id)
            if result:
                return result

            # Проверяем таймаут
            elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
            if elapsed > timeout_seconds:
                raise TimeoutError(f"Task {task_id} did not complete within {timeout_seconds} seconds")

            # Ждем перед следующей проверкой
            await asyncio.sleep(1)

    async def get_system_status(self) -> Dict[str, Any]:
        """
        Получить статус системы оркестрации.

        Returns:
            Словарь со статусом системы
        """
        async with self._lock:
            # Собираем статистику от всех компонентов
            queue_stats = await self.task_queue.get_queue_stats()
            scheduler_stats = await self.scheduler.get_scheduler_stats()
            execution_stats = await self.execution_engine.get_execution_stats()
            balancer_stats = await self.load_balancer.get_balancer_stats()
            priority_analytics = await self.priority_manager.get_priority_analytics()

            uptime = (datetime.now(timezone.utc) - self._metrics["system_uptime"]).total_seconds()

            return {
                "orchestrator": {
                    "is_running": self._is_running,
                    "uptime_seconds": uptime,
                    "registered_agents": len(self._agents),
                    "config": self.config.__dict__
                },
                "metrics": self._metrics.copy(),
                "task_queue": queue_stats,
                "scheduler": scheduler_stats,
                "execution": execution_stats,
                "load_balancer": balancer_stats,
                "priority_manager": priority_analytics
            }

    async def register_agent(self, agent: Agent) -> bool:
        """
        Зарегистрировать агента.

        Args:
            agent: Агент для регистрации

        Returns:
            True если агент зарегистрирован
        """
        async with self._lock:
            if agent.id in self._agents:
                self.logger.warning(f"Agent {agent.id} is already registered")
                return False

            self._agents[agent.id] = agent
            await self._publish_event("agent.registered", {
                "agent_id": agent.id,
                "agent_type": agent.type,
                "capabilities": agent.capabilities
            })

            self.logger.info(f"Agent {agent.id} registered successfully")
            return True

    async def unregister_agent(self, agent_id: str) -> bool:
        """
        Отменить регистрацию агента.

        Args:
            agent_id: ID агента

        Returns:
            True если регистрация отменена
        """
        async with self._lock:
            if agent_id not in self._agents:
                return False

            del self._agents[agent_id]
            await self._publish_event("agent.unregistered", {"agent_id": agent_id})

            self.logger.info(f"Agent {agent_id} unregistered")
            return True

    async def get_available_agents(self) -> List[Agent]:
        """
        Получить список доступных агентов.

        Returns:
            Список доступных агентов
        """
        async with self._lock:
            return [agent for agent in self._agents.values()
                   if agent.status == AgentStatus.IDLE and agent.is_available]

    async def _monitoring_loop(self):
        """Цикл мониторинга системы."""
        while not self._shutdown_event.is_set():
            try:
                await self._perform_monitoring_cycle()
                await asyncio.sleep(self.config.monitoring_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)

    async def _perform_monitoring_cycle(self):
        """Выполнить цикл мониторинга."""
        # Обработка готовых задач
        await self._process_ready_tasks()

        # Обновление метрик
        await self._update_system_metrics()

        # Проверка здоровья агентов
        await self._check_agent_health()

        # Балансировка нагрузки (если нужно)
        if self.config.enable_load_balancing:
            await self._perform_load_balancing()

    async def _process_ready_tasks(self):
        """Обработать готовые к выполнению задачи."""
        ready_tasks = await self.scheduler.get_ready_tasks()
        available_agents = await self.get_available_agents()

        if not ready_tasks or not available_agents:
            return

        # Ограничиваем количество задач текущей пропускной способностью
        max_tasks = min(
            len(ready_tasks),
            len(available_agents),
            self.config.max_concurrent_tasks
        )

        tasks_to_process = ready_tasks[:max_tasks]

        for task in tasks_to_process:
            try:
                # Выбираем агента
                agent = await self.load_balancer.select_agent(task, available_agents)
                if agent:
                    # Отмечаем задачу как выполняющуюся
                    await self.scheduler.mark_task_running(task.id)

                    # Запускаем выполнение асинхронно
                    asyncio.create_task(self._execute_task_with_monitoring(task, agent))

                    # Удаляем агента из доступных для этого цикла
                    available_agents = [a for a in available_agents if a.id != agent.id]

            except Exception as e:
                self.logger.error(f"Failed to process task {task.id}: {e}")

    async def _execute_task_with_monitoring(self, task: Task, agent: Agent):
        """
        Выполнить задачу с мониторингом.

        Args:
            task: Задача
            agent: Агент
        """
        try:
            # Обновляем статус агента
            agent.status = AgentStatus.BUSY
            agent.current_load += 1

            # Выполняем задачу
            result = await self.execution_engine.execute_task(task, agent)

            # Отмечаем задачу как завершенную
            success = result.status == TaskStatus.COMPLETED
            await self.scheduler.mark_task_completed(task.id, success)

            # Обновляем метрики
            if success:
                self._metrics["tasks_completed"] += 1
            else:
                self._metrics["tasks_failed"] += 1

            # Публикуем событие
            await self._publish_event("task.completed", {
                "task_id": task.id,
                "agent_id": agent.id,
                "success": success,
                "execution_time": result.execution_time
            })

        except Exception as e:
            self.logger.error(f"Error executing task {task.id}: {e}")
            await self.scheduler.mark_task_completed(task.id, False)
            self._metrics["tasks_failed"] += 1

        finally:
            # Освобождаем агента
            agent.status = AgentStatus.IDLE
            agent.current_load = max(0, agent.current_load - 1)

    async def _auto_escalation_loop(self):
        """Цикл автоматической эскалации приоритетов."""
        while not self._shutdown_event.is_set():
            try:
                # Получаем все активные задачи
                scheduled_tasks = await self.scheduler.get_scheduled_tasks()
                ready_tasks = await self.scheduler.get_ready_tasks()
                all_tasks = scheduled_tasks + ready_tasks

                # Выполняем автоэскалацию
                escalated = await self.priority_manager.auto_escalate_tasks(all_tasks)

                if escalated:
                    self.logger.info(f"Auto-escalated {len(escalated)} tasks")

                await asyncio.sleep(300)  # Проверяем каждые 5 минут

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in auto-escalation loop: {e}")
                await asyncio.sleep(60)

    async def _update_system_metrics(self):
        """Обновить системные метрики."""
        # Здесь можно добавить более сложную логику сбора метрик
        pass

    async def _check_agent_health(self):
        """Проверить здоровье агентов."""
        for agent in self._agents.values():
            # Простая проверка: если агент давно не активен, помечаем как недоступный
            if agent.last_activity:
                inactive_time = datetime.now(timezone.utc) - agent.last_activity
                if inactive_time > timedelta(minutes=10):
                    agent.status = AgentStatus.UNAVAILABLE

    async def _perform_load_balancing(self):
        """Выполнить балансировку нагрузки."""
        available_agents = list(self._agents.values())
        if len(available_agents) > 1:
            rebalancing_plan = await self.load_balancer.rebalance(available_agents)
            # Здесь можно применить план перебалансирования

    async def _publish_event(self, event_type: str, data: Dict[str, Any]):
        """
        Опубликовать событие.

        Args:
            event_type: Тип события
            data: Данные события
        """
        event = OrchestrationEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source="orchestrator",
            data=data
        )

        # Уведомляем подписчиков
        subscribers = self._event_subscribers.get(event_type, [])
        for callback in subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                self.logger.error(f"Error in event subscriber: {e}")

    async def subscribe_to_events(self, event_type: str, callback):
        """
        Подписаться на события.

        Args:
            event_type: Тип события
            callback: Функция обратного вызова
        """
        if event_type not in self._event_subscribers:
            self._event_subscribers[event_type] = []

        self._event_subscribers[event_type].append(callback)

    async def create_execution_plan(self, tasks: List[Task]) -> ExecutionPlan:
        """
        Создать план выполнения для группы задач.

        Args:
            tasks: Список задач

        Returns:
            План выполнения
        """
        return await self.scheduler.create_execution_plan(tasks)

    async def execute_plan(self, plan: ExecutionPlan) -> List[TaskResult]:
        """
        Выполнить план выполнения.

        Args:
            plan: План выполнения

        Returns:
            Результаты выполнения
        """
        available_agents = await self.get_available_agents()
        return await self.execution_engine.execute_pipeline(plan, available_agents)