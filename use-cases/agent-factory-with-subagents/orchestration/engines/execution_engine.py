"""
Движок выполнения задач с поддержкой параллельного и последовательного выполнения.

Этот модуль содержит логику для выполнения задач различными способами:
параллельно, последовательно, в виде конвейера и с условным выполнением.
"""

import asyncio
from typing import List, Dict, Optional, Any, Callable, Set
from datetime import datetime, timezone, timedelta
import logging
from enum import Enum
import json

from ..core.interfaces import IExecutionEngine, IErrorHandler
from ..core.types import Task, Agent, TaskResult, ExecutionPlan, TaskStatus, ExecutionMode, OrchestrationEvent


class ExecutionStatus(Enum):
    """Статусы выполнения."""
    NOT_STARTED = "not_started"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ParallelExecutionEngine(IExecutionEngine):
    """
    Движок параллельного выполнения задач.

    Поддерживает:
    - Параллельное выполнение независимых задач
    - Последовательное выполнение с зависимостями
    - Конвейерное выполнение (pipeline)
    - Условное выполнение
    - Управление жизненным циклом задач
    - Мониторинг и логирование
    """

    def __init__(self, max_concurrent_tasks: int = 10,
                 error_handler: Optional[IErrorHandler] = None):
        """
        Инициализация движка выполнения.

        Args:
            max_concurrent_tasks: Максимальное количество одновременных задач
            error_handler: Обработчик ошибок
        """
        self.max_concurrent_tasks = max_concurrent_tasks
        self.error_handler = error_handler
        self.logger = logging.getLogger(__name__)

        # Активные выполнения
        self._active_executions: Dict[str, asyncio.Task] = {}

        # Результаты выполнения
        self._execution_results: Dict[str, TaskResult] = {}

        # Контексты выполнения
        self._execution_contexts: Dict[str, Dict[str, Any]] = {}

        # Семафор для ограничения параллельности
        self._semaphore = asyncio.Semaphore(max_concurrent_tasks)

        # События остановки и паузы
        self._stop_events: Dict[str, asyncio.Event] = {}
        self._pause_events: Dict[str, asyncio.Event] = {}

        # Блокировка для thread-safety
        self._lock = asyncio.Lock()

        # Метрики выполнения
        self._execution_metrics: Dict[str, Any] = {
            "total_executed": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "average_execution_time": 0.0,
            "peak_concurrent_tasks": 0
        }

    async def execute_task(self, task: Task, agent: Agent) -> TaskResult:
        """
        Выполнить одну задачу.

        Args:
            task: Задача для выполнения
            agent: Агент для выполнения

        Returns:
            Результат выполнения задачи
        """
        async with self._lock:
            if task.id in self._active_executions:
                self.logger.warning(f"Task {task.id} is already being executed")
                return self._create_error_result(task, "Task already executing")

        # Создаем контекст выполнения
        context = await self._create_execution_context(task, agent)
        self._execution_contexts[task.id] = context

        # Создаем события управления
        self._stop_events[task.id] = asyncio.Event()
        self._pause_events[task.id] = asyncio.Event()

        try:
            # Запускаем выполнение с семафором
            async with self._semaphore:
                result = await self._execute_single_task(task, agent, context)

            # Обновляем метрики
            await self._update_metrics(result)

            self.logger.info(f"Task {task.id} executed successfully by agent {agent.id}")
            return result

        except Exception as e:
            error_result = self._create_error_result(task, str(e))
            await self._update_metrics(error_result)

            if self.error_handler:
                await self.error_handler.handle_error(e, {"task_id": task.id, "agent_id": agent.id})

            self.logger.error(f"Task {task.id} execution failed: {e}")
            return error_result

        finally:
            await self._cleanup_task_execution(task.id)

    async def execute_tasks_parallel(self, tasks: List[Task], agents: List[Agent]) -> List[TaskResult]:
        """
        Выполнить задачи параллельно.

        Args:
            tasks: Список задач
            agents: Список агентов

        Returns:
            Список результатов выполнения
        """
        if not tasks:
            return []

        # Создаем пары задача-агент
        task_agent_pairs = await self._assign_agents_to_tasks(tasks, agents)

        # Запускаем все задачи параллельно
        execution_tasks = []
        for task, agent in task_agent_pairs:
            if agent:  # Если агент найден для задачи
                exec_task = asyncio.create_task(self.execute_task(task, agent))
                execution_tasks.append(exec_task)

                async with self._lock:
                    self._active_executions[task.id] = exec_task
            else:
                # Создаем результат с ошибкой для задач без агента
                error_result = self._create_error_result(task, "No suitable agent available")
                execution_tasks.append(asyncio.create_task(self._return_immediate_result(error_result)))

        # Ждем завершения всех задач
        results = await asyncio.gather(*execution_tasks, return_exceptions=True)

        # Обрабатываем исключения
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                task = tasks[i]
                error_result = self._create_error_result(task, str(result))
                processed_results.append(error_result)
            else:
                processed_results.append(result)

        self.logger.info(f"Parallel execution completed: {len(processed_results)} tasks")
        return processed_results

    async def execute_tasks_sequential(self, tasks: List[Task], agents: List[Agent]) -> List[TaskResult]:
        """
        Выполнить задачи последовательно.

        Args:
            tasks: Список задач
            agents: Список агентов

        Returns:
            Список результатов выполнения
        """
        results = []

        for task in tasks:
            # Выбираем доступного агента
            available_agents = [agent for agent in agents
                              if agent.id not in [ctx.get("agent_id")
                                                 for ctx in self._execution_contexts.values()]]

            if not available_agents:
                available_agents = agents  # Fallback to all agents

            agent = await self._select_best_agent(task, available_agents)

            if agent:
                result = await self.execute_task(task, agent)
                results.append(result)

                # Если задача не выполнена успешно, можем прервать цепочку
                if result.status == TaskStatus.FAILED and task.context.get("fail_fast", False):
                    self.logger.warning(f"Sequential execution stopped due to task {task.id} failure")
                    break
            else:
                error_result = self._create_error_result(task, "No suitable agent available")
                results.append(error_result)

        self.logger.info(f"Sequential execution completed: {len(results)} tasks")
        return results

    async def execute_pipeline(self, plan: ExecutionPlan, agents: List[Agent]) -> List[TaskResult]:
        """
        Выполнить план как конвейер задач.

        Args:
            plan: План выполнения
            agents: Список агентов

        Returns:
            Список результатов выполнения
        """
        all_results = []
        task_map = {task.id: task for task in plan.tasks}

        # Выполняем группы параллельно, но группы последовательно
        for group_task_ids in plan.parallel_groups:
            group_tasks = [task_map[task_id] for task_id in group_task_ids if task_id in task_map]

            if not group_tasks:
                continue

            # Выполняем текущую группу параллельно
            group_results = await self.execute_tasks_parallel(group_tasks, agents)
            all_results.extend(group_results)

            # Проверяем, есть ли критические ошибки
            critical_failures = [result for result in group_results
                               if result.status == TaskStatus.FAILED and
                               task_map[result.task_id].context.get("critical", False)]

            if critical_failures:
                self.logger.error(f"Pipeline execution stopped due to critical failures: "
                                f"{[r.task_id for r in critical_failures]}")
                break

            # Обновляем контекст для следующих групп
            await self._update_pipeline_context(group_results, plan)

        self.logger.info(f"Pipeline execution completed: {len(all_results)} tasks")
        return all_results

    async def stop_execution(self, task_id: str) -> bool:
        """
        Остановить выполнение задачи.

        Args:
            task_id: ID задачи

        Returns:
            True если выполнение остановлено
        """
        async with self._lock:
            if task_id not in self._active_executions:
                return False

            # Устанавливаем событие остановки
            if task_id in self._stop_events:
                self._stop_events[task_id].set()

            # Отменяем задачу
            execution_task = self._active_executions[task_id]
            execution_task.cancel()

            try:
                await execution_task
            except asyncio.CancelledError:
                pass

            self.logger.info(f"Execution of task {task_id} stopped")
            return True

    async def pause_execution(self, task_id: str) -> bool:
        """
        Приостановить выполнение задачи.

        Args:
            task_id: ID задачи

        Returns:
            True если выполнение приостановлено
        """
        async with self._lock:
            if task_id not in self._pause_events:
                return False

            self._pause_events[task_id].set()
            self.logger.info(f"Execution of task {task_id} paused")
            return True

    async def resume_execution(self, task_id: str) -> bool:
        """
        Возобновить выполнение задачи.

        Args:
            task_id: ID задачи

        Returns:
            True если выполнение возобновлено
        """
        async with self._lock:
            if task_id not in self._pause_events:
                return False

            self._pause_events[task_id].clear()
            self.logger.info(f"Execution of task {task_id} resumed")
            return True

    async def _execute_single_task(self, task: Task, agent: Agent, context: Dict[str, Any]) -> TaskResult:
        """
        Выполнить одну задачу с полным контролем жизненного цикла.

        Args:
            task: Задача
            agent: Агент
            context: Контекст выполнения

        Returns:
            Результат выполнения
        """
        start_time = datetime.now(timezone.utc)
        task.status = TaskStatus.RUNNING
        task.started_at = start_time

        try:
            # Проверяем события остановки и паузы
            while self._pause_events.get(task.id, asyncio.Event()).is_set():
                await asyncio.sleep(0.1)
                if self._stop_events.get(task.id, asyncio.Event()).is_set():
                    task.status = TaskStatus.CANCELLED
                    return self._create_result(task, TaskStatus.CANCELLED, "Execution stopped")

            # Симуляция выполнения задачи (в реальной системе здесь был бы вызов агента)
            execution_time = await self._simulate_task_execution(task, agent, context)

            # Проверяем таймаут
            if task.timeout and execution_time > task.timeout:
                task.status = TaskStatus.FAILED
                return self._create_result(task, TaskStatus.FAILED, "Execution timeout")

            # Создаем успешный результат
            task.status = TaskStatus.COMPLETED
            end_time = datetime.now(timezone.utc)
            actual_duration = (end_time - start_time).total_seconds()

            result_data = {
                "agent_id": agent.id,
                "execution_time": actual_duration,
                "context": context,
                "output": f"Task {task.id} completed successfully"
            }

            return self._create_result(task, TaskStatus.COMPLETED, "Success", result_data, actual_duration)

        except Exception as e:
            task.status = TaskStatus.FAILED
            return self._create_result(task, TaskStatus.FAILED, str(e))

    async def _simulate_task_execution(self, task: Task, agent: Agent, context: Dict[str, Any]) -> float:
        """
        Симуляция выполнения задачи (заглушка для реального выполнения).

        Args:
            task: Задача
            agent: Агент
            context: Контекст

        Returns:
            Время выполнения в секундах
        """
        # В реальной системе здесь был бы вызов соответствующего агента
        # Пока симулируем случайное время выполнения
        import random

        base_time = task.estimated_duration or 10  # 10 секунд по умолчанию
        # Добавляем случайность ±50%
        execution_time = base_time * (0.5 + random.random())

        await asyncio.sleep(min(execution_time, 2))  # Максимум 2 секунды для симуляции

        return execution_time

    async def _assign_agents_to_tasks(self, tasks: List[Task], agents: List[Agent]) -> List[tuple]:
        """
        Назначить агентов задачам.

        Args:
            tasks: Список задач
            agents: Список агентов

        Returns:
            Список пар (task, agent)
        """
        assignments = []
        used_agents = set()

        for task in tasks:
            # Выбираем доступного агента
            available_agents = [agent for agent in agents if agent.id not in used_agents]

            if not available_agents:
                # Если все агенты заняты, используем любого (агенты могут выполнять несколько задач)
                available_agents = agents

            agent = await self._select_best_agent(task, available_agents)
            assignments.append((task, agent))

            if agent and len(available_agents) <= len(tasks):
                used_agents.add(agent.id)

        return assignments

    async def _select_best_agent(self, task: Task, agents: List[Agent]) -> Optional[Agent]:
        """
        Выбрать лучшего агента для задачи.

        Args:
            task: Задача
            agents: Доступные агенты

        Returns:
            Выбранный агент или None
        """
        if not agents:
            return None

        # Простая логика выбора: предпочитаем агентов с подходящими возможностями
        suitable_agents = []
        for agent in agents:
            if (not task.agent_type or
                task.agent_type in agent.capabilities or
                task.agent_type in agent.supported_tasks):
                suitable_agents.append(agent)

        if suitable_agents:
            # Выбираем наименее загруженного подходящего агента
            return min(suitable_agents, key=lambda a: a.current_load)
        else:
            # Если подходящих нет, выбираем наименее загруженного
            return min(agents, key=lambda a: a.current_load)

    async def _create_execution_context(self, task: Task, agent: Agent) -> Dict[str, Any]:
        """
        Создать контекст выполнения.

        Args:
            task: Задача
            agent: Агент

        Returns:
            Контекст выполнения
        """
        return {
            "task_id": task.id,
            "agent_id": agent.id,
            "started_at": datetime.now(timezone.utc),
            "input_data": task.input_data.copy(),
            "context": task.context.copy(),
            "execution_id": f"{task.id}_{agent.id}_{int(datetime.now().timestamp())}"
        }

    def _create_result(self, task: Task, status: TaskStatus, message: str,
                      result_data: Optional[Dict[str, Any]] = None,
                      execution_time: Optional[float] = None) -> TaskResult:
        """
        Создать результат выполнения задачи.

        Args:
            task: Задача
            status: Статус выполнения
            message: Сообщение
            result_data: Данные результата
            execution_time: Время выполнения

        Returns:
            Результат выполнения
        """
        return TaskResult(
            task_id=task.id,
            status=status,
            result_data=result_data or {},
            error_message=message if status == TaskStatus.FAILED else None,
            execution_time=execution_time,
            started_at=task.started_at,
            completed_at=datetime.now(timezone.utc)
        )

    def _create_error_result(self, task: Task, error_message: str) -> TaskResult:
        """
        Создать результат с ошибкой.

        Args:
            task: Задача
            error_message: Сообщение об ошибке

        Returns:
            Результат с ошибкой
        """
        return self._create_result(task, TaskStatus.FAILED, error_message)

    async def _return_immediate_result(self, result: TaskResult) -> TaskResult:
        """Вернуть результат немедленно (для использования в async context)."""
        return result

    async def _cleanup_task_execution(self, task_id: str):
        """
        Очистить данные выполнения задачи.

        Args:
            task_id: ID задачи
        """
        async with self._lock:
            self._active_executions.pop(task_id, None)
            self._execution_contexts.pop(task_id, None)
            self._stop_events.pop(task_id, None)
            self._pause_events.pop(task_id, None)

    async def _update_metrics(self, result: TaskResult):
        """
        Обновить метрики выполнения.

        Args:
            result: Результат выполнения
        """
        async with self._lock:
            self._execution_metrics["total_executed"] += 1

            if result.status == TaskStatus.COMPLETED:
                self._execution_metrics["successful_executions"] += 1
            elif result.status == TaskStatus.FAILED:
                self._execution_metrics["failed_executions"] += 1

            # Обновляем среднее время выполнения
            if result.execution_time:
                current_avg = self._execution_metrics["average_execution_time"]
                total = self._execution_metrics["total_executed"]
                new_avg = ((current_avg * (total - 1)) + result.execution_time) / total
                self._execution_metrics["average_execution_time"] = new_avg

            # Обновляем пиковую нагрузку
            current_active = len(self._active_executions)
            if current_active > self._execution_metrics["peak_concurrent_tasks"]:
                self._execution_metrics["peak_concurrent_tasks"] = current_active

    async def _update_pipeline_context(self, results: List[TaskResult], plan: ExecutionPlan):
        """
        Обновить контекст конвейера на основе результатов группы.

        Args:
            results: Результаты выполнения группы
            plan: План выполнения
        """
        # Простая реализация: собираем выходные данные для передачи следующим группам
        for result in results:
            if result.status == TaskStatus.COMPLETED and result.result_data:
                # В реальной системе здесь была бы логика передачи данных между этапами
                pass

    async def get_execution_stats(self) -> Dict[str, Any]:
        """
        Получить статистику выполнения.

        Returns:
            Словарь со статистикой
        """
        async with self._lock:
            active_tasks = len(self._active_executions)
            success_rate = 0.0

            total = self._execution_metrics["total_executed"]
            if total > 0:
                successful = self._execution_metrics["successful_executions"]
                success_rate = successful / total

            return {
                "active_executions": active_tasks,
                "total_executed": total,
                "successful_executions": self._execution_metrics["successful_executions"],
                "failed_executions": self._execution_metrics["failed_executions"],
                "success_rate": success_rate,
                "average_execution_time": self._execution_metrics["average_execution_time"],
                "peak_concurrent_tasks": self._execution_metrics["peak_concurrent_tasks"],
                "current_capacity_utilization": active_tasks / self.max_concurrent_tasks
            }

    async def shutdown(self):
        """Корректно завершить работу движка."""
        # Останавливаем все активные выполнения
        active_task_ids = list(self._active_executions.keys())

        for task_id in active_task_ids:
            await self.stop_execution(task_id)

        # Ждем завершения всех задач
        if self._active_executions:
            await asyncio.gather(*self._active_executions.values(), return_exceptions=True)

        self.logger.info("Execution engine shutdown completed")