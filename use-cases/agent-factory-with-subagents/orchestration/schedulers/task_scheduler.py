"""
Реализация планировщика задач с поддержкой различных стратегий планирования.

Этот модуль содержит планировщик, который управляет временем выполнения задач,
их зависимостями и различными стратегиями планирования.
"""

import asyncio
from typing import List, Optional, Dict, Any, Set
from datetime import datetime, timezone, timedelta
import logging

from ..core.interfaces import ITaskScheduler, IDependencyManager
from ..core.types import Task, TaskStatus, TaskPriority, ExecutionPlan


class SmartTaskScheduler(ITaskScheduler):
    """
    Умный планировщик задач.

    Поддерживает:
    - Временное планирование задач
    - Планирование с учетом зависимостей
    - Различные стратегии планирования
    - Автоматическое перепланирование при сбоях
    """

    def __init__(self, dependency_manager: Optional[IDependencyManager] = None):
        """
        Инициализация планировщика.

        Args:
            dependency_manager: Менеджер зависимостей
        """
        self.dependency_manager = dependency_manager
        self.logger = logging.getLogger(__name__)

        # Запланированные задачи: {task_id: task}
        self._scheduled_tasks: Dict[str, Task] = {}

        # Задачи, готовые к выполнению
        self._ready_tasks: Dict[str, Task] = {}

        # Задачи в процессе выполнения
        self._running_tasks: Dict[str, Task] = {}

        # Завершенные задачи (для анализа зависимостей)
        self._completed_tasks: Dict[str, Task] = {}

        # Планы выполнения
        self._execution_plans: Dict[str, ExecutionPlan] = {}

        # Блокировка для thread-safety
        self._lock = asyncio.Lock()

        # Фоновая задача для проверки готовых задач
        self._monitor_task: Optional[asyncio.Task] = None

    async def start(self):
        """Запустить планировщик."""
        self._monitor_task = asyncio.create_task(self._monitor_scheduled_tasks())
        self.logger.info("Task scheduler started")

    async def stop(self):
        """Остановить планировщик."""
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        self.logger.info("Task scheduler stopped")

    async def schedule_task(self, task: Task) -> bool:
        """
        Запланировать выполнение задачи.

        Args:
            task: Задача для планирования

        Returns:
            True если задача запланирована успешно
        """
        async with self._lock:
            if task.id in self._scheduled_tasks:
                self.logger.warning(f"Task {task.id} already scheduled")
                return False

            # Проверяем зависимости
            if self.dependency_manager:
                is_ready = await self.dependency_manager.is_ready_to_execute(task.id)
                if not is_ready:
                    task.status = TaskStatus.BLOCKED
                    self.logger.info(f"Task {task.id} blocked by dependencies")
                else:
                    await self._make_task_ready(task)
            else:
                await self._make_task_ready(task)

            self._scheduled_tasks[task.id] = task
            self.logger.info(f"Task {task.id} scheduled")
            return True

    async def schedule_tasks(self, tasks: List[Task]) -> bool:
        """
        Запланировать выполнение нескольких задач.

        Args:
            tasks: Список задач для планирования

        Returns:
            True если все задачи запланированы успешно
        """
        async with self._lock:
            # Сортируем задачи с учетом зависимостей
            if self.dependency_manager:
                try:
                    sorted_tasks = await self.dependency_manager.resolve_execution_order(tasks)
                except Exception as e:
                    self.logger.error(f"Failed to resolve task dependencies: {e}")
                    return False
            else:
                sorted_tasks = sorted(tasks, key=lambda t: t.priority.value, reverse=True)

            # Планируем задачи в порядке зависимостей
            success_count = 0
            for task in sorted_tasks:
                if await self.schedule_task(task):
                    success_count += 1

            success_rate = success_count / len(tasks) if tasks else 1.0
            self.logger.info(f"Scheduled {success_count}/{len(tasks)} tasks "
                           f"(success rate: {success_rate:.2%})")

            return success_count == len(tasks)

    async def cancel_task(self, task_id: str) -> bool:
        """
        Отменить запланированную задачу.

        Args:
            task_id: ID задачи

        Returns:
            True если задача отменена
        """
        async with self._lock:
            task = None

            # Ищем задачу в различных состояниях
            if task_id in self._scheduled_tasks:
                task = self._scheduled_tasks.pop(task_id)
            elif task_id in self._ready_tasks:
                task = self._ready_tasks.pop(task_id)
            elif task_id in self._running_tasks:
                task = self._running_tasks[task_id]
                task.status = TaskStatus.CANCELLED
                self.logger.warning(f"Task {task_id} is running, marked for cancellation")
                return True

            if task:
                task.status = TaskStatus.CANCELLED
                self.logger.info(f"Task {task_id} cancelled")

                # Обновляем зависимые задачи
                if self.dependency_manager:
                    await self._handle_task_cancellation(task_id)

                return True

            self.logger.warning(f"Task {task_id} not found for cancellation")
            return False

    async def reschedule_task(self, task_id: str, new_time: Optional[str] = None) -> bool:
        """
        Перепланировать задачу.

        Args:
            task_id: ID задачи
            new_time: Новое время выполнения (ISO format) или None для немедленного выполнения

        Returns:
            True если задача перепланирована
        """
        async with self._lock:
            task = self._scheduled_tasks.get(task_id)
            if not task:
                self.logger.warning(f"Task {task_id} not found for rescheduling")
                return False

            # Устанавливаем новое время
            if new_time:
                try:
                    task.scheduled_at = datetime.fromisoformat(new_time.replace('Z', '+00:00'))
                except ValueError:
                    self.logger.error(f"Invalid time format for task {task_id}: {new_time}")
                    return False
            else:
                task.scheduled_at = None

            # Проверяем, готова ли задача к выполнению сейчас
            if not new_time or task.scheduled_at <= datetime.now(timezone.utc):
                if self.dependency_manager:
                    is_ready = await self.dependency_manager.is_ready_to_execute(task_id)
                    if is_ready:
                        await self._make_task_ready(task)
                else:
                    await self._make_task_ready(task)

            self.logger.info(f"Task {task_id} rescheduled for {task.scheduled_at or 'immediate execution'}")
            return True

    async def get_scheduled_tasks(self) -> List[Task]:
        """
        Получить список запланированных задач.

        Returns:
            Список запланированных задач
        """
        async with self._lock:
            return list(self._scheduled_tasks.values())

    async def get_ready_tasks(self) -> List[Task]:
        """
        Получить задачи, готовые к выполнению.

        Returns:
            Список готовых задач
        """
        async with self._lock:
            return list(self._ready_tasks.values())

    async def _make_task_ready(self, task: Task):
        """
        Перевести задачу в состояние готовности к выполнению.

        Args:
            task: Задача
        """
        # Проверяем время выполнения
        current_time = datetime.now(timezone.utc)
        if task.scheduled_at and task.scheduled_at > current_time:
            task.status = TaskStatus.PENDING
            return

        # Переводим в готовые
        task.status = TaskStatus.QUEUED
        self._ready_tasks[task.id] = task

        self.logger.debug(f"Task {task.id} is ready for execution")

    async def _monitor_scheduled_tasks(self):
        """Фоновый мониторинг запланированных задач."""
        while True:
            try:
                await asyncio.sleep(30)  # Проверяем каждые 30 секунд
                await self._check_ready_tasks()
                await self._cleanup_completed_tasks()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in task monitoring: {e}")

    async def _check_ready_tasks(self):
        """Проверить и переместить готовые задачи."""
        async with self._lock:
            current_time = datetime.now(timezone.utc)
            ready_task_ids = []

            for task_id, task in self._scheduled_tasks.items():
                # Проверяем время выполнения
                if task.scheduled_at and task.scheduled_at <= current_time:
                    if self.dependency_manager:
                        is_ready = await self.dependency_manager.is_ready_to_execute(task_id)
                        if is_ready:
                            ready_task_ids.append(task_id)
                    else:
                        ready_task_ids.append(task_id)

            # Перемещаем готовые задачи
            for task_id in ready_task_ids:
                task = self._scheduled_tasks.pop(task_id)
                await self._make_task_ready(task)

            if ready_task_ids:
                self.logger.info(f"Moved {len(ready_task_ids)} tasks to ready state")

    async def _cleanup_completed_tasks(self):
        """Очистка завершенных задач (старше 1 часа)."""
        async with self._lock:
            current_time = datetime.now(timezone.utc)
            cleanup_threshold = current_time - timedelta(hours=1)

            completed_to_remove = []
            for task_id, task in self._completed_tasks.items():
                if task.completed_at and task.completed_at < cleanup_threshold:
                    completed_to_remove.append(task_id)

            for task_id in completed_to_remove:
                del self._completed_tasks[task_id]

            if completed_to_remove:
                self.logger.debug(f"Cleaned up {len(completed_to_remove)} completed tasks")

    async def _handle_task_cancellation(self, cancelled_task_id: str):
        """
        Обработать отмену задачи и влияние на зависимые задачи.

        Args:
            cancelled_task_id: ID отмененной задачи
        """
        if not self.dependency_manager:
            return

        # Получаем зависимые задачи
        dependent_tasks = await self.dependency_manager.get_dependents(cancelled_task_id)

        for dependent_id in dependent_tasks:
            # Проверяем, можно ли выполнить зависимую задачу без отмененной
            dependent_task = (self._scheduled_tasks.get(dependent_id) or
                            self._ready_tasks.get(dependent_id))

            if dependent_task:
                is_ready = await self.dependency_manager.is_ready_to_execute(dependent_id)
                if not is_ready:
                    dependent_task.status = TaskStatus.BLOCKED
                    if dependent_id in self._ready_tasks:
                        del self._ready_tasks[dependent_id]
                    self.logger.info(f"Task {dependent_id} blocked due to cancellation of {cancelled_task_id}")

    async def mark_task_completed(self, task_id: str, success: bool = True):
        """
        Отметить задачу как завершенную.

        Args:
            task_id: ID задачи
            success: Успешно ли завершена задача
        """
        async with self._lock:
            task = self._running_tasks.pop(task_id, None)
            if not task:
                self.logger.warning(f"Task {task_id} not found in running tasks")
                return

            task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
            task.completed_at = datetime.now(timezone.utc)

            # Вычисляем время выполнения
            if task.started_at:
                duration = (task.completed_at - task.started_at).total_seconds()
                task.actual_duration = duration

            self._completed_tasks[task_id] = task

            # Проверяем зависимые задачи
            if success and self.dependency_manager:
                await self._check_dependent_tasks(task_id)

            self.logger.info(f"Task {task_id} marked as {'completed' if success else 'failed'}")

    async def mark_task_running(self, task_id: str):
        """
        Отметить задачу как выполняющуюся.

        Args:
            task_id: ID задачи
        """
        async with self._lock:
            task = self._ready_tasks.pop(task_id, None)
            if task:
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now(timezone.utc)
                self._running_tasks[task_id] = task
                self.logger.info(f"Task {task_id} started running")

    async def _check_dependent_tasks(self, completed_task_id: str):
        """
        Проверить и разблокировать зависимые задачи.

        Args:
            completed_task_id: ID завершенной задачи
        """
        if not self.dependency_manager:
            return

        dependent_tasks = await self.dependency_manager.get_dependents(completed_task_id)

        for dependent_id in dependent_tasks:
            dependent_task = self._scheduled_tasks.get(dependent_id)
            if dependent_task and dependent_task.status == TaskStatus.BLOCKED:
                is_ready = await self.dependency_manager.is_ready_to_execute(dependent_id)
                if is_ready:
                    await self._make_task_ready(dependent_task)
                    self.logger.info(f"Task {dependent_id} unblocked after completion of {completed_task_id}")

    async def create_execution_plan(self, tasks: List[Task]) -> ExecutionPlan:
        """
        Создать план выполнения для группы задач.

        Args:
            tasks: Список задач

        Returns:
            План выполнения
        """
        plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if self.dependency_manager:
            # Определяем порядок выполнения с учетом зависимостей
            ordered_tasks = await self.dependency_manager.resolve_execution_order(tasks)
            execution_order = [task.id for task in ordered_tasks]

            # Определяем группы для параллельного выполнения
            parallel_groups = await self._identify_parallel_groups(ordered_tasks)
        else:
            # Простая сортировка по приоритету
            ordered_tasks = sorted(tasks, key=lambda t: t.priority.value, reverse=True)
            execution_order = [task.id for task in ordered_tasks]
            parallel_groups = [[task.id] for task in ordered_tasks]  # Каждая задача в отдельной группе

        # Оценка общего времени выполнения
        estimated_time = sum(task.estimated_duration or 300 for task in tasks)

        plan = ExecutionPlan(
            plan_id=plan_id,
            tasks=tasks,
            execution_order=execution_order,
            parallel_groups=parallel_groups,
            estimated_total_time=estimated_time
        )

        self._execution_plans[plan_id] = plan
        self.logger.info(f"Created execution plan {plan_id} for {len(tasks)} tasks")

        return plan

    async def _identify_parallel_groups(self, tasks: List[Task]) -> List[List[str]]:
        """
        Определить группы задач для параллельного выполнения.

        Args:
            tasks: Упорядоченный список задач

        Returns:
            Список групп задач для параллельного выполнения
        """
        if not self.dependency_manager:
            return [[task.id] for task in tasks]

        parallel_groups = []
        remaining_tasks = {task.id: task for task in tasks}

        while remaining_tasks:
            current_group = []

            # Находим задачи без зависимостей среди оставшихся
            for task_id, task in list(remaining_tasks.items()):
                dependencies = await self.dependency_manager.get_dependencies(task_id)
                dependencies_in_remaining = [dep for dep in dependencies if dep in remaining_tasks]

                if not dependencies_in_remaining:
                    current_group.append(task_id)
                    del remaining_tasks[task_id]

            if current_group:
                parallel_groups.append(current_group)
            else:
                # Если нет задач без зависимостей, возможно есть циклические зависимости
                self.logger.warning("Possible circular dependencies detected")
                # Добавляем все оставшиеся задачи в одну группу
                parallel_groups.append(list(remaining_tasks.keys()))
                break

        return parallel_groups

    async def get_scheduler_stats(self) -> Dict[str, Any]:
        """
        Получить статистику планировщика.

        Returns:
            Словарь со статистикой
        """
        async with self._lock:
            return {
                "scheduled_tasks": len(self._scheduled_tasks),
                "ready_tasks": len(self._ready_tasks),
                "running_tasks": len(self._running_tasks),
                "completed_tasks": len(self._completed_tasks),
                "execution_plans": len(self._execution_plans),
                "average_completion_time": self._calculate_average_completion_time(),
                "task_success_rate": self._calculate_success_rate()
            }

    def _calculate_average_completion_time(self) -> Optional[float]:
        """Вычислить среднее время выполнения задач."""
        completion_times = [task.actual_duration for task in self._completed_tasks.values()
                          if task.actual_duration is not None]

        return sum(completion_times) / len(completion_times) if completion_times else None

    def _calculate_success_rate(self) -> float:
        """Вычислить коэффициент успешности выполнения задач."""
        if not self._completed_tasks:
            return 1.0

        successful_tasks = sum(1 for task in self._completed_tasks.values()
                             if task.status == TaskStatus.COMPLETED)

        return successful_tasks / len(self._completed_tasks)