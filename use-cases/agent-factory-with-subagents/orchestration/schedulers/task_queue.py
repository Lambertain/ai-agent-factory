"""
Реализация очереди задач с приоритетами и фильтрацией.

Этот модуль содержит умную очередь задач, которая поддерживает приоритеты,
фильтрацию по возможностям агентов и различные стратегии извлечения задач.
"""

import asyncio
import heapq
from typing import List, Optional, Dict, Any, Set
from datetime import datetime, timezone
import logging

from ..core.interfaces import ITaskQueue
from ..core.types import Task, TaskPriority, TaskStatus


class PriorityTaskQueue(ITaskQueue):
    """
    Очередь задач с приоритетами.

    Поддерживает:
    - Приоритетное планирование задач
    - Фильтрацию по возможностям агентов
    - Временное планирование (scheduled_at)
    - Ограничение размера очереди
    """

    def __init__(self, max_size: int = 1000):
        """
        Инициализация очереди.

        Args:
            max_size: Максимальный размер очереди
        """
        self.max_size = max_size
        self.logger = logging.getLogger(__name__)

        # Основная очередь с приоритетами: [(priority_score, timestamp, task), ...]
        self._queue: List[tuple] = []

        # Индекс для быстрого поиска задач по ID
        self._task_index: Dict[str, Task] = {}

        # Задачи, запланированные на будущее
        self._scheduled_tasks: Dict[str, Task] = {}

        # Блокировка для thread-safety
        self._lock = asyncio.Lock()

        # Счетчик для обеспечения стабильной сортировки
        self._counter = 0

    async def enqueue(self, task: Task) -> bool:
        """
        Добавить задачу в очередь.

        Args:
            task: Задача для добавления

        Returns:
            True если задача добавлена успешно
        """
        async with self._lock:
            # Проверяем размер очереди
            if len(self._queue) >= self.max_size:
                self.logger.warning(f"Queue is full (size: {self.max_size})")
                return False

            # Проверяем, что задача еще не в очереди
            if task.id in self._task_index:
                self.logger.warning(f"Task {task.id} already in queue")
                return False

            # Если задача запланирована на будущее
            if task.scheduled_at and task.scheduled_at > datetime.now(timezone.utc):
                self._scheduled_tasks[task.id] = task
                self.logger.info(f"Task {task.id} scheduled for {task.scheduled_at}")
                return True

            # Вычисляем приоритетный счет
            priority_score = self._calculate_priority_score(task)

            # Добавляем в очередь с приоритетом
            self._counter += 1
            heapq.heappush(self._queue, (priority_score, self._counter, task))
            self._task_index[task.id] = task

            # Обновляем статус задачи
            task.status = TaskStatus.QUEUED

            self.logger.info(f"Task {task.id} enqueued with priority score {priority_score}")
            return True

    async def dequeue(self, agent_capabilities: Optional[List[str]] = None) -> Optional[Task]:
        """
        Извлечь задачу из очереди для агента с указанными возможностями.

        Args:
            agent_capabilities: Список возможностей агента

        Returns:
            Задача для выполнения или None
        """
        async with self._lock:
            # Сначала проверяем запланированные задачи
            await self._move_ready_scheduled_tasks()

            if not self._queue:
                return None

            # Если возможности не указаны, берем задачу с наивысшим приоритетом
            if not agent_capabilities:
                _, _, task = heapq.heappop(self._queue)
                del self._task_index[task.id]
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now(timezone.utc)
                self.logger.info(f"Dequeued task {task.id} without capability filter")
                return task

            # Ищем первую подходящую задачу
            temp_tasks = []
            result_task = None

            while self._queue and result_task is None:
                priority_score, counter, task = heapq.heappop(self._queue)

                if self._task_matches_capabilities(task, agent_capabilities):
                    result_task = task
                    del self._task_index[task.id]
                    task.status = TaskStatus.RUNNING
                    task.started_at = datetime.now(timezone.utc)
                    self.logger.info(f"Dequeued task {task.id} for capabilities {agent_capabilities}")
                else:
                    temp_tasks.append((priority_score, counter, task))

            # Возвращаем неподходящие задачи в очередь
            for temp_task in temp_tasks:
                heapq.heappush(self._queue, temp_task)

            return result_task

    async def peek(self, count: int = 1) -> List[Task]:
        """
        Просмотреть задачи в очереди без извлечения.

        Args:
            count: Количество задач для просмотра

        Returns:
            Список задач
        """
        async with self._lock:
            await self._move_ready_scheduled_tasks()

            # Получаем отсортированные задачи
            sorted_queue = sorted(self._queue)
            tasks = [task for _, _, task in sorted_queue[:count]]

            self.logger.debug(f"Peeked {len(tasks)} tasks")
            return tasks

    async def size(self) -> int:
        """Получить размер очереди."""
        async with self._lock:
            total_size = len(self._queue) + len(self._scheduled_tasks)
            return total_size

    async def is_empty(self) -> bool:
        """Проверить, пуста ли очередь."""
        async with self._lock:
            await self._move_ready_scheduled_tasks()
            return len(self._queue) == 0

    async def remove_task(self, task_id: str) -> bool:
        """
        Удалить задачу из очереди по ID.

        Args:
            task_id: ID задачи

        Returns:
            True если задача удалена
        """
        async with self._lock:
            # Проверяем запланированные задачи
            if task_id in self._scheduled_tasks:
                del self._scheduled_tasks[task_id]
                self.logger.info(f"Removed scheduled task {task_id}")
                return True

            # Проверяем основную очередь
            if task_id not in self._task_index:
                return False

            # Удаляем из индекса
            del self._task_index[task_id]

            # Перестраиваем очередь без удаленной задачи
            new_queue = [(score, counter, task)
                        for score, counter, task in self._queue
                        if task.id != task_id]

            self._queue = new_queue
            heapq.heapify(self._queue)

            self.logger.info(f"Removed task {task_id} from queue")
            return True

    async def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """
        Получить задачи с определенным приоритетом.

        Args:
            priority: Уровень приоритета

        Returns:
            Список задач с указанным приоритетом
        """
        async with self._lock:
            try:
                priority_enum = TaskPriority[priority.upper()]
                tasks = [task for _, _, task in self._queue
                        if task.priority == priority_enum]

                # Добавляем запланированные задачи
                scheduled_tasks = [task for task in self._scheduled_tasks.values()
                                 if task.priority == priority_enum]

                return tasks + scheduled_tasks
            except KeyError:
                self.logger.warning(f"Invalid priority: {priority}")
                return []

    def _calculate_priority_score(self, task: Task) -> float:
        """
        Вычислить приоритетный счет для задачи.

        Меньший счет = выше приоритет (для min-heap).

        Args:
            task: Задача

        Returns:
            Приоритетный счет
        """
        # Базовый приоритет (инвертируем для min-heap)
        base_score = 6 - task.priority.value

        # Фактор времени ожидания
        age_factor = 0
        if task.created_at:
            age_hours = (datetime.now(timezone.utc) - task.created_at).total_seconds() / 3600
            age_factor = min(age_hours * 0.1, 2.0)  # Максимум +2 к приоритету

        # Фактор повторных попыток
        retry_factor = task.retry_count * 0.5

        # Итоговый счет
        final_score = base_score - age_factor - retry_factor

        return final_score

    def _task_matches_capabilities(self, task: Task, capabilities: List[str]) -> bool:
        """
        Проверить, соответствует ли задача возможностям агента.

        Args:
            task: Задача
            capabilities: Возможности агента

        Returns:
            True если задача подходит агенту
        """
        # Если у задачи не указан тип агента, она подходит любому
        if not task.agent_type:
            return True

        # Проверяем точное соответствие типа агента
        if task.agent_type in capabilities:
            return True

        # Проверяем частичное соответствие (например, "python" в "python-dev")
        for capability in capabilities:
            if task.agent_type in capability or capability in task.agent_type:
                return True

        return False

    async def _move_ready_scheduled_tasks(self):
        """Переместить готовые запланированные задачи в основную очередь."""
        current_time = datetime.now(timezone.utc)
        ready_tasks = []

        for task_id, task in list(self._scheduled_tasks.items()):
            if not task.scheduled_at or task.scheduled_at <= current_time:
                ready_tasks.append(task)
                del self._scheduled_tasks[task_id]

        for task in ready_tasks:
            priority_score = self._calculate_priority_score(task)
            self._counter += 1
            heapq.heappush(self._queue, (priority_score, self._counter, task))
            self._task_index[task.id] = task
            task.status = TaskStatus.QUEUED

            self.logger.info(f"Moved scheduled task {task.id} to main queue")

    async def get_queue_stats(self) -> Dict[str, Any]:
        """
        Получить статистику очереди.

        Returns:
            Словарь со статистикой
        """
        async with self._lock:
            await self._move_ready_scheduled_tasks()

            # Подсчет задач по приоритетам
            priority_counts = {}
            for _, _, task in self._queue:
                priority = task.priority.name
                priority_counts[priority] = priority_counts.get(priority, 0) + 1

            return {
                "total_tasks": len(self._queue),
                "scheduled_tasks": len(self._scheduled_tasks),
                "priority_breakdown": priority_counts,
                "queue_utilization": len(self._queue) / self.max_size * 100,
                "oldest_task_age": self._get_oldest_task_age(),
                "average_wait_time": self._calculate_average_wait_time()
            }

    def _get_oldest_task_age(self) -> Optional[float]:
        """Получить возраст самой старой задачи в секундах."""
        if not self._queue:
            return None

        current_time = datetime.now(timezone.utc)
        oldest_time = min(task.created_at for _, _, task in self._queue if task.created_at)

        if oldest_time:
            return (current_time - oldest_time).total_seconds()
        return None

    def _calculate_average_wait_time(self) -> Optional[float]:
        """Вычислить среднее время ожидания в очереди."""
        if not self._queue:
            return None

        current_time = datetime.now(timezone.utc)
        wait_times = []

        for _, _, task in self._queue:
            if task.created_at:
                wait_time = (current_time - task.created_at).total_seconds()
                wait_times.append(wait_time)

        return sum(wait_times) / len(wait_times) if wait_times else None