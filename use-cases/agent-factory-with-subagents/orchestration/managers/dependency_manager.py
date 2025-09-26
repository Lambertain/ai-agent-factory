"""
Менеджер зависимостей для управления связями между задачами.

Этот модуль содержит логику для определения зависимостей между задачами,
разрешения порядка выполнения и обнаружения циклических зависимостей.
"""

import asyncio
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict, deque
import logging

from ..core.interfaces import IDependencyManager
from ..core.types import Task, TaskDependency, TaskStatus


class TaskDependencyManager(IDependencyManager):
    """
    Менеджер зависимостей задач.

    Поддерживает:
    - Различные типы зависимостей (completion, data, resource)
    - Обнаружение циклических зависимостей
    - Топологическую сортировку задач
    - Условные зависимости
    """

    def __init__(self):
        """Инициализация менеджера зависимостей."""
        self.logger = logging.getLogger(__name__)

        # Граф зависимостей: {task_id: [dependency_task_ids]}
        self._dependencies: Dict[str, List[TaskDependency]] = defaultdict(list)

        # Обратный граф: {task_id: [dependent_task_ids]}
        self._dependents: Dict[str, Set[str]] = defaultdict(set)

        # Кэш для статусов задач
        self._task_statuses: Dict[str, TaskStatus] = {}

        # Блокировка для thread-safety
        self._lock = asyncio.Lock()

    async def add_dependency(self, task_id: str, dependency_task_id: str,
                           dependency_type: str = "completion") -> bool:
        """
        Добавить зависимость между задачами.

        Args:
            task_id: ID задачи, которая зависит
            dependency_task_id: ID задачи-зависимости
            dependency_type: Тип зависимости

        Returns:
            True если зависимость добавлена успешно
        """
        async with self._lock:
            # Проверяем, что задача не зависит от самой себя
            if task_id == dependency_task_id:
                self.logger.warning(f"Task {task_id} cannot depend on itself")
                return False

            # Проверяем на циклическую зависимость
            if await self._would_create_cycle(task_id, dependency_task_id):
                self.logger.warning(f"Adding dependency {dependency_task_id} -> {task_id} "
                                  f"would create a cycle")
                return False

            # Создаем объект зависимости
            dependency = TaskDependency(
                task_id=dependency_task_id,
                dependency_type=dependency_type
            )

            # Проверяем, что такая зависимость еще не существует
            existing_deps = [dep for dep in self._dependencies[task_id]
                           if dep.task_id == dependency_task_id]
            if existing_deps:
                self.logger.warning(f"Dependency {dependency_task_id} -> {task_id} already exists")
                return False

            # Добавляем зависимость
            self._dependencies[task_id].append(dependency)
            self._dependents[dependency_task_id].add(task_id)

            self.logger.info(f"Added {dependency_type} dependency: {dependency_task_id} -> {task_id}")
            return True

    async def remove_dependency(self, task_id: str, dependency_task_id: str) -> bool:
        """
        Удалить зависимость между задачами.

        Args:
            task_id: ID задачи
            dependency_task_id: ID задачи-зависимости

        Returns:
            True если зависимость удалена
        """
        async with self._lock:
            # Удаляем из прямого графа
            dependencies = self._dependencies.get(task_id, [])
            original_length = len(dependencies)

            self._dependencies[task_id] = [dep for dep in dependencies
                                         if dep.task_id != dependency_task_id]

            # Удаляем из обратного графа
            if dependency_task_id in self._dependents:
                self._dependents[dependency_task_id].discard(task_id)

            removed = len(self._dependencies[task_id]) < original_length
            if removed:
                self.logger.info(f"Removed dependency: {dependency_task_id} -> {task_id}")

            return removed

    async def get_dependencies(self, task_id: str) -> List[str]:
        """
        Получить список зависимостей для задачи.

        Args:
            task_id: ID задачи

        Returns:
            Список ID задач-зависимостей
        """
        async with self._lock:
            dependencies = self._dependencies.get(task_id, [])
            return [dep.task_id for dep in dependencies]

    async def get_dependents(self, task_id: str) -> List[str]:
        """
        Получить список задач, зависящих от данной.

        Args:
            task_id: ID задачи

        Returns:
            Список ID зависимых задач
        """
        async with self._lock:
            return list(self._dependents.get(task_id, set()))

    async def is_ready_to_execute(self, task_id: str) -> bool:
        """
        Проверить, готова ли задача к выполнению.

        Args:
            task_id: ID задачи

        Returns:
            True если все зависимости выполнены
        """
        async with self._lock:
            dependencies = self._dependencies.get(task_id, [])

            for dependency in dependencies:
                dep_task_id = dependency.task_id
                dep_type = dependency.dependency_type

                # Проверяем статус зависимости
                dep_status = self._task_statuses.get(dep_task_id)

                if dep_type == "completion":
                    if dep_status != TaskStatus.COMPLETED:
                        return False
                elif dep_type == "data":
                    # Для зависимостей по данным проверяем, что задача завершена успешно
                    if dep_status not in [TaskStatus.COMPLETED]:
                        return False
                elif dep_type == "resource":
                    # Для ресурсных зависимостей проверяем, что ресурс не занят
                    if dep_status == TaskStatus.RUNNING:
                        return False

                # Проверяем условие, если оно есть
                if dependency.condition:
                    if not await self._evaluate_condition(dependency.condition, dep_task_id):
                        return False

            return True

    async def resolve_execution_order(self, tasks: List[Task]) -> List[Task]:
        """
        Определить порядок выполнения задач с учетом зависимостей.

        Args:
            tasks: Список задач

        Returns:
            Упорядоченный список задач
        """
        async with self._lock:
            # Создаем мапинг ID -> Task
            task_map = {task.id: task for task in tasks}
            task_ids = set(task_map.keys())

            # Строим граф зависимостей только для данных задач
            local_dependencies = {}
            local_dependents = defaultdict(set)

            for task_id in task_ids:
                deps = self._dependencies.get(task_id, [])
                # Учитываем только зависимости внутри данной группы задач
                local_deps = [dep for dep in deps if dep.task_id in task_ids]
                local_dependencies[task_id] = local_deps

                for dep in local_deps:
                    local_dependents[dep.task_id].add(task_id)

            # Выполняем топологическую сортировку
            sorted_task_ids = await self._topological_sort(task_ids, local_dependencies)

            # Возвращаем задачи в правильном порядке
            ordered_tasks = [task_map[task_id] for task_id in sorted_task_ids]

            self.logger.info(f"Resolved execution order for {len(tasks)} tasks")
            return ordered_tasks

    async def detect_circular_dependencies(self, tasks: List[Task]) -> List[List[str]]:
        """
        Обнаружить циклические зависимости.

        Args:
            tasks: Список задач для проверки

        Returns:
            Список циклов (каждый цикл - список ID задач)
        """
        async with self._lock:
            task_ids = {task.id for task in tasks}
            cycles = []

            # Состояния для поиска циклов
            WHITE, GRAY, BLACK = 0, 1, 2
            colors = {task_id: WHITE for task_id in task_ids}
            path = []

            async def dfs_visit(node: str) -> bool:
                """DFS для поиска циклов."""
                colors[node] = GRAY
                path.append(node)

                dependencies = self._dependencies.get(node, [])
                for dep in dependencies:
                    if dep.task_id not in task_ids:
                        continue

                    neighbor = dep.task_id

                    if colors[neighbor] == GRAY:
                        # Найден цикл
                        cycle_start = path.index(neighbor)
                        cycle = path[cycle_start:] + [neighbor]
                        cycles.append(cycle)
                        return True

                    if colors[neighbor] == WHITE:
                        if await dfs_visit(neighbor):
                            return True

                colors[node] = BLACK
                path.pop()
                return False

            # Запускаем DFS для всех непосещенных узлов
            for task_id in task_ids:
                if colors[task_id] == WHITE:
                    await dfs_visit(task_id)

            if cycles:
                self.logger.warning(f"Detected {len(cycles)} circular dependencies")

            return cycles

    async def _would_create_cycle(self, task_id: str, dependency_task_id: str) -> bool:
        """
        Проверить, создаст ли добавление зависимости цикл.

        Args:
            task_id: ID задачи
            dependency_task_id: ID потенциальной зависимости

        Returns:
            True если создаст цикл
        """
        # Проверяем, есть ли путь от dependency_task_id к task_id
        visited = set()
        stack = [dependency_task_id]

        while stack:
            current = stack.pop()
            if current == task_id:
                return True

            if current in visited:
                continue

            visited.add(current)

            # Добавляем все зависимости текущей задачи
            dependencies = self._dependencies.get(current, [])
            for dep in dependencies:
                if dep.task_id not in visited:
                    stack.append(dep.task_id)

        return False

    async def _topological_sort(self, task_ids: Set[str],
                              dependencies: Dict[str, List[TaskDependency]]) -> List[str]:
        """
        Выполнить топологическую сортировку задач.

        Args:
            task_ids: Множество ID задач
            dependencies: Словарь зависимостей

        Returns:
            Топологически отсортированный список ID задач
        """
        # Подсчитываем входящие ребра для каждой задачи
        in_degree = {task_id: 0 for task_id in task_ids}

        for task_id in task_ids:
            for dep in dependencies.get(task_id, []):
                if dep.task_id in task_ids:
                    in_degree[task_id] += 1

        # Инициализируем очередь задачами без входящих ребер
        queue = deque([task_id for task_id in task_ids if in_degree[task_id] == 0])
        result = []

        while queue:
            current = queue.popleft()
            result.append(current)

            # Уменьшаем степень входа для всех зависимых задач
            for dependent_id in self._dependents.get(current, set()):
                if dependent_id in task_ids:
                    in_degree[dependent_id] -= 1
                    if in_degree[dependent_id] == 0:
                        queue.append(dependent_id)

        # Проверяем, что все задачи обработаны (нет циклов)
        if len(result) != len(task_ids):
            remaining_tasks = task_ids - set(result)
            self.logger.warning(f"Topological sort incomplete. Remaining tasks: {remaining_tasks}")
            # Добавляем оставшиеся задачи в конец
            result.extend(remaining_tasks)

        return result

    async def _evaluate_condition(self, condition: str, task_id: str) -> bool:
        """
        Оценить условие зависимости.

        Args:
            condition: Условие для оценки
            task_id: ID задачи-зависимости

        Returns:
            True если условие выполнено
        """
        # Простая реализация для базовых условий
        # В более сложных случаях можно использовать eval или специальный парсер

        task_status = self._task_statuses.get(task_id)

        if condition == "success":
            return task_status == TaskStatus.COMPLETED
        elif condition == "failure":
            return task_status == TaskStatus.FAILED
        elif condition == "completion":
            return task_status in [TaskStatus.COMPLETED, TaskStatus.FAILED]
        else:
            # Неизвестное условие считаем выполненным
            self.logger.warning(f"Unknown condition: {condition}")
            return True

    async def update_task_status(self, task_id: str, status: TaskStatus):
        """
        Обновить статус задачи.

        Args:
            task_id: ID задачи
            status: Новый статус
        """
        async with self._lock:
            old_status = self._task_statuses.get(task_id)
            self._task_statuses[task_id] = status

            if old_status != status:
                self.logger.debug(f"Task {task_id} status changed: {old_status} -> {status}")

    async def get_dependency_tree(self, task_id: str, max_depth: int = 10) -> Dict[str, any]:
        """
        Получить дерево зависимостей для задачи.

        Args:
            task_id: ID задачи
            max_depth: Максимальная глубина дерева

        Returns:
            Дерево зависимостей
        """
        async with self._lock:
            return await self._build_dependency_tree(task_id, max_depth, set())

    async def _build_dependency_tree(self, task_id: str, max_depth: int,
                                   visited: Set[str]) -> Dict[str, any]:
        """
        Рекурсивно построить дерево зависимостей.

        Args:
            task_id: ID задачи
            max_depth: Максимальная глубина
            visited: Множество посещенных задач

        Returns:
            Узел дерева зависимостей
        """
        if max_depth <= 0 or task_id in visited:
            return {"task_id": task_id, "dependencies": []}

        visited.add(task_id)

        dependencies = self._dependencies.get(task_id, [])
        dep_trees = []

        for dep in dependencies:
            dep_tree = await self._build_dependency_tree(dep.task_id, max_depth - 1, visited.copy())
            dep_tree["dependency_type"] = dep.dependency_type
            dep_tree["condition"] = dep.condition
            dep_trees.append(dep_tree)

        return {
            "task_id": task_id,
            "status": self._task_statuses.get(task_id, TaskStatus.PENDING).value,
            "dependencies": dep_trees
        }

    async def get_stats(self) -> Dict[str, any]:
        """
        Получить статистику менеджера зависимостей.

        Returns:
            Словарь со статистикой
        """
        async with self._lock:
            total_dependencies = sum(len(deps) for deps in self._dependencies.values())
            tasks_with_dependencies = len([task_id for task_id, deps in self._dependencies.items()
                                         if deps])

            dependency_types = defaultdict(int)
            for deps in self._dependencies.values():
                for dep in deps:
                    dependency_types[dep.dependency_type] += 1

            return {
                "total_tasks": len(self._task_statuses),
                "total_dependencies": total_dependencies,
                "tasks_with_dependencies": tasks_with_dependencies,
                "dependency_types": dict(dependency_types),
                "average_dependencies_per_task": (
                    total_dependencies / tasks_with_dependencies
                    if tasks_with_dependencies > 0 else 0
                )
            }

    async def clear_task_data(self, task_id: str):
        """
        Очистить данные задачи из менеджера.

        Args:
            task_id: ID задачи
        """
        async with self._lock:
            # Удаляем зависимости задачи
            if task_id in self._dependencies:
                del self._dependencies[task_id]

            # Удаляем задачу из зависимых других задач
            if task_id in self._dependents:
                del self._dependents[task_id]

            # Удаляем ссылки на эту задачу из других зависимостей
            for other_task_id, deps in self._dependencies.items():
                self._dependencies[other_task_id] = [
                    dep for dep in deps if dep.task_id != task_id
                ]

            # Удаляем из обратных ссылок
            for dependents_set in self._dependents.values():
                dependents_set.discard(task_id)

            # Удаляем статус
            self._task_statuses.pop(task_id, None)

            self.logger.debug(f"Cleared dependency data for task {task_id}")

    async def validate_dependencies(self, tasks: List[Task]) -> List[str]:
        """
        Валидировать зависимости для группы задач.

        Args:
            tasks: Список задач

        Returns:
            Список ошибок валидации
        """
        async with self._lock:
            errors = []
            task_ids = {task.id for task in tasks}

            # Проверяем циклические зависимости
            cycles = await self.detect_circular_dependencies(tasks)
            for cycle in cycles:
                errors.append(f"Circular dependency detected: {' -> '.join(cycle)}")

            # Проверяем недостающие зависимости
            for task in tasks:
                dependencies = self._dependencies.get(task.id, [])
                for dep in dependencies:
                    if dep.task_id not in task_ids:
                        errors.append(f"Task {task.id} depends on missing task {dep.task_id}")

            return errors