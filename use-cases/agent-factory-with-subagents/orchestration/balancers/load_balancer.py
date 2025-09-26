"""
Умный балансировщик нагрузки для распределения задач между субагентами.

Этот модуль содержит различные стратегии балансировки нагрузки и
алгоритмы для оптимального распределения задач между агентами.
"""

import asyncio
from typing import List, Dict, Optional, Callable, Any, Tuple
from datetime import datetime, timezone, timedelta
from enum import Enum
import logging
import random
import math

from ..core.interfaces import ILoadBalancer
from ..core.types import Task, Agent, TaskPriority, AgentStatus, LoadBalancingStrategy


class BalancingStrategy(Enum):
    """Стратегии балансировки нагрузки."""
    ROUND_ROBIN = "round_robin"
    LEAST_LOADED = "least_loaded"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    CAPABILITY_BASED = "capability_based"
    PERFORMANCE_BASED = "performance_based"
    ADAPTIVE = "adaptive"


class SmartLoadBalancer(ILoadBalancer):
    """
    Умный балансировщик нагрузки.

    Поддерживает:
    - Множественные стратегии балансировки
    - Адаптивное распределение на основе производительности
    - Учет возможностей агентов
    - Динамическое перебалансирование
    - Метрики производительности
    """

    def __init__(self, default_strategy: BalancingStrategy = BalancingStrategy.ADAPTIVE):
        """
        Инициализация балансировщика.

        Args:
            default_strategy: Стратегия балансировки по умолчанию
        """
        self.default_strategy = default_strategy
        self.logger = logging.getLogger(__name__)

        # Метрики агентов
        self._agent_metrics: Dict[str, Dict[str, Any]] = {}

        # Кэш производительности
        self._performance_cache: Dict[str, float] = {}

        # Счетчики для round-robin
        self._round_robin_counters: Dict[str, int] = {}

        # История распределения задач
        self._task_history: List[Dict[str, Any]] = []

        # Блокировка для thread-safety
        self._lock = asyncio.Lock()

        # Временные окна для анализа производительности
        self._performance_window = timedelta(hours=1)
        self._metrics_update_interval = timedelta(minutes=5)

    async def select_agent(self, task: Task, available_agents: List[Agent]) -> Optional[Agent]:
        """
        Выбрать наилучшего агента для выполнения задачи.

        Args:
            task: Задача для выполнения
            available_agents: Список доступных агентов

        Returns:
            Выбранный агент или None
        """
        async with self._lock:
            if not available_agents:
                return None

            # Фильтруем агентов по возможностям
            suitable_agents = await self._filter_agents_by_capability(task, available_agents)
            if not suitable_agents:
                self.logger.warning(f"No suitable agents found for task {task.id}")
                return None

            # Выбираем стратегию
            strategy = await self._select_strategy(task, suitable_agents)

            # Применяем стратегию
            selected_agent = await self._apply_strategy(strategy, task, suitable_agents)

            if selected_agent:
                await self._record_assignment(task, selected_agent)
                self.logger.info(f"Selected agent {selected_agent.id} for task {task.id} "
                               f"using {strategy.value} strategy")

            return selected_agent

    async def distribute_tasks(self, tasks: List[Task], agents: List[Agent]) -> Dict[str, List[str]]:
        """
        Распределить задачи между агентами.

        Args:
            tasks: Список задач
            agents: Список агентов

        Returns:
            Словарь {agent_id: [task_ids]}
        """
        async with self._lock:
            distribution: Dict[str, List[str]] = {agent.id: [] for agent in agents}

            # Сортируем задачи по приоритету
            sorted_tasks = sorted(tasks, key=lambda t: t.priority.value, reverse=True)

            # Распределяем задачи
            for task in sorted_tasks:
                # Получаем доступных агентов для этой задачи
                available_agents = [agent for agent in agents
                                  if agent.status == AgentStatus.IDLE and
                                  len(distribution[agent.id]) < agent.max_concurrent_tasks]

                if not available_agents:
                    self.logger.warning(f"No available agents for task {task.id}")
                    continue

                # Выбираем агента
                selected_agent = await self.select_agent(task, available_agents)
                if selected_agent:
                    distribution[selected_agent.id].append(task.id)

            # Логируем результаты распределения
            total_assigned = sum(len(task_list) for task_list in distribution.values())
            self.logger.info(f"Distributed {total_assigned}/{len(tasks)} tasks among {len(agents)} agents")

            return distribution

    async def rebalance(self, agents: List[Agent]) -> Dict[str, List[str]]:
        """
        Перебалансировать нагрузку между агентами.

        Args:
            agents: Список агентов

        Returns:
            Новое распределение задач
        """
        async with self._lock:
            # Анализируем текущую нагрузку
            load_analysis = await self._analyze_current_load(agents)

            # Определяем необходимость перебалансирования
            if not await self._needs_rebalancing(load_analysis):
                self.logger.debug("No rebalancing needed")
                return {agent.id: [] for agent in agents}

            # Выполняем перебалансирование
            rebalancing_plan = await self._create_rebalancing_plan(agents, load_analysis)

            self.logger.info(f"Rebalancing plan created for {len(agents)} agents")
            return rebalancing_plan

    async def get_load_metrics(self, agent_id: str) -> Dict[str, float]:
        """
        Получить метрики нагрузки для агента.

        Args:
            agent_id: ID агента

        Returns:
            Словарь с метриками
        """
        async with self._lock:
            metrics = self._agent_metrics.get(agent_id, {})

            return {
                "current_load": metrics.get("current_load", 0.0),
                "average_execution_time": metrics.get("avg_execution_time", 0.0),
                "success_rate": metrics.get("success_rate", 1.0),
                "tasks_completed_per_hour": metrics.get("tasks_per_hour", 0.0),
                "cpu_utilization": metrics.get("cpu_utilization", 0.0),
                "memory_utilization": metrics.get("memory_utilization", 0.0),
                "error_rate": metrics.get("error_rate", 0.0),
                "response_time_p95": metrics.get("response_time_p95", 0.0)
            }

    async def update_agent_metrics(self, agent_id: str, metrics: Dict[str, Any]) -> bool:
        """
        Обновить метрики агента.

        Args:
            agent_id: ID агента
            metrics: Новые метрики

        Returns:
            True если метрики обновлены успешно
        """
        async with self._lock:
            if agent_id not in self._agent_metrics:
                self._agent_metrics[agent_id] = {}

            # Обновляем метрики
            self._agent_metrics[agent_id].update(metrics)
            self._agent_metrics[agent_id]["last_updated"] = datetime.now(timezone.utc)

            # Обновляем кэш производительности
            await self._update_performance_cache(agent_id)

            self.logger.debug(f"Updated metrics for agent {agent_id}")
            return True

    async def _filter_agents_by_capability(self, task: Task, agents: List[Agent]) -> List[Agent]:
        """
        Фильтровать агентов по возможностям для выполнения задачи.

        Args:
            task: Задача
            agents: Список агентов

        Returns:
            Подходящие агенты
        """
        suitable_agents = []

        for agent in agents:
            # Проверяем статус агента
            if agent.status != AgentStatus.IDLE or not agent.is_available:
                continue

            # Проверяем загрузку агента
            if agent.current_load >= agent.max_concurrent_tasks:
                continue

            # Проверяем возможности
            if task.agent_type:
                if (task.agent_type in agent.capabilities or
                    task.agent_type in agent.supported_tasks or
                    any(task.agent_type in cap for cap in agent.capabilities)):
                    suitable_agents.append(agent)
            else:
                # Если тип агента не указан, подходит любой
                suitable_agents.append(agent)

        return suitable_agents

    async def _select_strategy(self, task: Task, agents: List[Agent]) -> BalancingStrategy:
        """
        Выбрать оптимальную стратегию балансировки.

        Args:
            task: Задача
            agents: Доступные агенты

        Returns:
            Выбранная стратегия
        """
        # Для адаптивной стратегии выбираем наилучшую
        if self.default_strategy == BalancingStrategy.ADAPTIVE:
            # Анализируем условия
            if task.priority in [TaskPriority.URGENT, TaskPriority.CRITICAL]:
                return BalancingStrategy.PERFORMANCE_BASED

            if len(agents) == 1:
                return BalancingStrategy.ROUND_ROBIN

            # Проверяем разброс нагрузки
            loads = [agent.current_load for agent in agents]
            load_variance = await self._calculate_variance(loads)

            if load_variance > 2.0:  # Высокий разброс нагрузки
                return BalancingStrategy.LEAST_LOADED
            else:
                return BalancingStrategy.CAPABILITY_BASED

        return self.default_strategy

    async def _apply_strategy(self, strategy: BalancingStrategy, task: Task,
                            agents: List[Agent]) -> Optional[Agent]:
        """
        Применить стратегию балансировки.

        Args:
            strategy: Стратегия
            task: Задача
            agents: Агенты

        Returns:
            Выбранный агент
        """
        if strategy == BalancingStrategy.ROUND_ROBIN:
            return await self._round_robin_selection(agents)

        elif strategy == BalancingStrategy.LEAST_LOADED:
            return await self._least_loaded_selection(agents)

        elif strategy == BalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return await self._weighted_round_robin_selection(agents)

        elif strategy == BalancingStrategy.CAPABILITY_BASED:
            return await self._capability_based_selection(task, agents)

        elif strategy == BalancingStrategy.PERFORMANCE_BASED:
            return await self._performance_based_selection(agents)

        else:
            # Fallback к least_loaded
            return await self._least_loaded_selection(agents)

    async def _round_robin_selection(self, agents: List[Agent]) -> Agent:
        """Round-robin выбор агента."""
        agents_key = "_".join(sorted(agent.id for agent in agents))
        counter = self._round_robin_counters.get(agents_key, 0)
        selected_agent = agents[counter % len(agents)]
        self._round_robin_counters[agents_key] = counter + 1
        return selected_agent

    async def _least_loaded_selection(self, agents: List[Agent]) -> Agent:
        """Выбор наименее загруженного агента."""
        return min(agents, key=lambda agent: agent.current_load)

    async def _weighted_round_robin_selection(self, agents: List[Agent]) -> Agent:
        """Взвешенный round-robin на основе производительности."""
        # Вычисляем веса на основе производительности
        weights = []
        for agent in agents:
            performance = self._performance_cache.get(agent.id, 1.0)
            # Инвертируем загрузку для веса (меньше загрузка = больше вес)
            load_factor = max(0.1, 1.0 - (agent.current_load / agent.max_concurrent_tasks))
            weight = performance * load_factor
            weights.append(weight)

        # Выбираем агента с вероятностью пропорциональной весу
        total_weight = sum(weights)
        if total_weight == 0:
            return random.choice(agents)

        rand_value = random.uniform(0, total_weight)
        cumulative_weight = 0

        for i, weight in enumerate(weights):
            cumulative_weight += weight
            if rand_value <= cumulative_weight:
                return agents[i]

        return agents[-1]  # Fallback

    async def _capability_based_selection(self, task: Task, agents: List[Agent]) -> Agent:
        """Выбор на основе соответствия возможностей."""
        # Оцениваем соответствие каждого агента задаче
        agent_scores = []

        for agent in agents:
            score = 0.0

            # Очки за точное соответствие типа задачи
            if task.agent_type in agent.supported_tasks:
                score += 10.0

            # Очки за соответствие возможностей
            if task.agent_type in agent.capabilities:
                score += 5.0

            # Штраф за загрузку
            load_penalty = agent.current_load / agent.max_concurrent_tasks
            score -= load_penalty * 3.0

            # Бонус за успешность
            score += agent.success_rate * 2.0

            agent_scores.append((score, agent))

        # Выбираем агента с наивысшим счетом
        agent_scores.sort(key=lambda x: x[0], reverse=True)
        return agent_scores[0][1]

    async def _performance_based_selection(self, agents: List[Agent]) -> Agent:
        """Выбор на основе производительности."""
        best_agent = None
        best_score = float('-inf')

        for agent in agents:
            # Вычисляем комплексный показатель производительности
            performance = self._performance_cache.get(agent.id, 1.0)
            load_factor = 1.0 - (agent.current_load / agent.max_concurrent_tasks)
            success_rate = agent.success_rate

            # Время выполнения (меньше = лучше)
            avg_time = agent.average_execution_time or 300.0  # 5 минут по умолчанию
            time_factor = 1.0 / (avg_time / 300.0)  # Нормализуем к 5 минутам

            # Комплексный счет
            score = performance * load_factor * success_rate * time_factor

            if score > best_score:
                best_score = score
                best_agent = agent

        return best_agent or agents[0]

    async def _record_assignment(self, task: Task, agent: Agent):
        """
        Записать назначение задачи агенту.

        Args:
            task: Задача
            agent: Агент
        """
        assignment = {
            "task_id": task.id,
            "agent_id": agent.id,
            "timestamp": datetime.now(timezone.utc),
            "task_priority": task.priority.value,
            "agent_load_before": agent.current_load
        }

        self._task_history.append(assignment)

        # Ограничиваем размер истории
        if len(self._task_history) > 10000:
            self._task_history = self._task_history[-5000:]

    async def _analyze_current_load(self, agents: List[Agent]) -> Dict[str, Any]:
        """
        Анализировать текущую нагрузку агентов.

        Args:
            agents: Список агентов

        Returns:
            Анализ нагрузки
        """
        loads = [agent.current_load for agent in agents]
        max_loads = [agent.max_concurrent_tasks for agent in agents]

        utilizations = [load / max_load if max_load > 0 else 0
                       for load, max_load in zip(loads, max_loads)]

        return {
            "agents": len(agents),
            "total_load": sum(loads),
            "total_capacity": sum(max_loads),
            "average_utilization": sum(utilizations) / len(utilizations) if utilizations else 0,
            "max_utilization": max(utilizations) if utilizations else 0,
            "min_utilization": min(utilizations) if utilizations else 0,
            "load_variance": await self._calculate_variance(utilizations),
            "utilizations": utilizations
        }

    async def _needs_rebalancing(self, load_analysis: Dict[str, Any]) -> bool:
        """
        Определить необходимость перебалансирования.

        Args:
            load_analysis: Анализ нагрузки

        Returns:
            True если нужно перебалансирование
        """
        # Проверяем разброс нагрузки
        if load_analysis["load_variance"] > 0.25:  # 25% variance threshold
            return True

        # Проверяем наличие перегруженных агентов
        if load_analysis["max_utilization"] > 0.9:  # 90% utilization
            return True

        # Проверяем наличие недогруженных агентов при высокой средней нагрузке
        if (load_analysis["average_utilization"] > 0.7 and
            load_analysis["min_utilization"] < 0.3):
            return True

        return False

    async def _create_rebalancing_plan(self, agents: List[Agent],
                                     load_analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Создать план перебалансирования.

        Args:
            agents: Список агентов
            load_analysis: Анализ нагрузки

        Returns:
            План перемещения задач
        """
        plan: Dict[str, List[str]] = {agent.id: [] for agent in agents}

        # Простая стратегия: перемещаем задачи с наиболее загруженных к наименее загруженным
        utilizations = load_analysis["utilizations"]
        agent_utils = list(zip(agents, utilizations))

        # Сортируем по загрузке
        agent_utils.sort(key=lambda x: x[1], reverse=True)

        overloaded_agents = [agent for agent, util in agent_utils if util > 0.8]
        underloaded_agents = [agent for agent, util in agent_utils if util < 0.5]

        # Логируем план (в реальной реализации здесь был бы более сложный алгоритм)
        if overloaded_agents and underloaded_agents:
            self.logger.info(f"Planning to rebalance from {len(overloaded_agents)} "
                           f"overloaded to {len(underloaded_agents)} underloaded agents")

        return plan

    async def _update_performance_cache(self, agent_id: str):
        """
        Обновить кэш производительности агента.

        Args:
            agent_id: ID агента
        """
        metrics = self._agent_metrics.get(agent_id, {})

        # Вычисляем комплексный показатель производительности
        success_rate = metrics.get("success_rate", 1.0)
        avg_time = metrics.get("avg_execution_time", 300.0)
        tasks_per_hour = metrics.get("tasks_per_hour", 1.0)

        # Нормализуем метрики
        time_score = min(1.0, 300.0 / avg_time) if avg_time > 0 else 1.0
        throughput_score = min(1.0, tasks_per_hour / 10.0)  # Нормализуем к 10 задач/час

        performance = success_rate * time_score * throughput_score
        self._performance_cache[agent_id] = performance

    async def _calculate_variance(self, values: List[float]) -> float:
        """
        Вычислить дисперсию значений.

        Args:
            values: Список значений

        Returns:
            Дисперсия
        """
        if not values:
            return 0.0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance

    async def get_balancer_stats(self) -> Dict[str, Any]:
        """
        Получить статистику балансировщика.

        Returns:
            Словарь со статистикой
        """
        async with self._lock:
            recent_assignments = [
                assignment for assignment in self._task_history
                if assignment["timestamp"] > datetime.now(timezone.utc) - self._performance_window
            ]

            strategy_usage = {}
            for assignment in recent_assignments:
                strategy = assignment.get("strategy", "unknown")
                strategy_usage[strategy] = strategy_usage.get(strategy, 0) + 1

            return {
                "total_assignments": len(self._task_history),
                "recent_assignments": len(recent_assignments),
                "agents_tracked": len(self._agent_metrics),
                "strategy_usage": strategy_usage,
                "performance_cache_size": len(self._performance_cache),
                "average_assignment_rate": len(recent_assignments) / 24 if recent_assignments else 0
            }