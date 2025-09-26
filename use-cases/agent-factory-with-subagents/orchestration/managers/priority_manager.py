"""
Менеджер приоритетов для умного управления приоритетами задач.

Этот модуль содержит логику для назначения, обновления и динамического
вычисления приоритетов задач на основе различных факторов.
"""

import asyncio
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime, timezone, timedelta
from enum import Enum
import logging
import math

from ..core.interfaces import IPriorityManager
from ..core.types import Task, TaskPriority, TaskStatus


class PriorityFactor(Enum):
    """Факторы, влияющие на приоритет."""
    DEADLINE = "deadline"
    AGE = "age"
    DEPENDENCIES = "dependencies"
    RESOURCE_COST = "resource_cost"
    BUSINESS_VALUE = "business_value"
    USER_PRIORITY = "user_priority"
    RETRY_COUNT = "retry_count"
    ESTIMATED_DURATION = "estimated_duration"


class PriorityRule:
    """Правило для вычисления приоритета."""

    def __init__(self, factor: PriorityFactor, weight: float,
                 calculator: Callable[[Task], float]):
        """
        Инициализация правила приоритета.

        Args:
            factor: Фактор приоритета
            weight: Вес фактора (0.0 - 1.0)
            calculator: Функция для вычисления значения фактора
        """
        self.factor = factor
        self.weight = weight
        self.calculator = calculator


class SmartPriorityManager(IPriorityManager):
    """
    Умный менеджер приоритетов.

    Поддерживает:
    - Статическое и динамическое назначение приоритетов
    - Множественные факторы приоритета
    - Эскалация приоритетов с течением времени
    - Приоритизация на основе бизнес-правил
    - Адаптивное обучение приоритетов
    """

    def __init__(self):
        """Инициализация менеджера приоритетов."""
        self.logger = logging.getLogger(__name__)

        # Правила для вычисления приоритета
        self._priority_rules: List[PriorityRule] = []

        # Кэш динамических приоритетов
        self._dynamic_priorities: Dict[str, float] = {}

        # История эскалаций
        self._escalation_history: Dict[str, List[Dict[str, Any]]] = {}

        # Настройки эскалации
        self._escalation_settings = {
            "age_threshold_hours": 24,
            "retry_escalation_multiplier": 1.5,
            "deadline_urgency_hours": 4
        }

        # Блокировка для thread-safety
        self._lock = asyncio.Lock()

        # Инициализируем стандартные правила
        self._init_default_rules()

    def _init_default_rules(self):
        """Инициализировать стандартные правила приоритета."""
        # Правило по возрасту задачи
        age_rule = PriorityRule(
            factor=PriorityFactor.AGE,
            weight=0.2,
            calculator=self._calculate_age_factor
        )

        # Правило по дедлайну
        deadline_rule = PriorityRule(
            factor=PriorityFactor.DEADLINE,
            weight=0.3,
            calculator=self._calculate_deadline_factor
        )

        # Правило по количеству повторных попыток
        retry_rule = PriorityRule(
            factor=PriorityFactor.RETRY_COUNT,
            weight=0.15,
            calculator=self._calculate_retry_factor
        )

        # Правило по пользовательскому приоритету
        user_priority_rule = PriorityRule(
            factor=PriorityFactor.USER_PRIORITY,
            weight=0.25,
            calculator=self._calculate_user_priority_factor
        )

        # Правило по оценочному времени выполнения
        duration_rule = PriorityRule(
            factor=PriorityFactor.ESTIMATED_DURATION,
            weight=0.1,
            calculator=self._calculate_duration_factor
        )

        self._priority_rules = [
            age_rule, deadline_rule, retry_rule, user_priority_rule, duration_rule
        ]

    async def assign_priority(self, task: Task) -> Task:
        """
        Назначить приоритет задаче.

        Args:
            task: Задача

        Returns:
            Задача с назначенным приоритетом
        """
        async with self._lock:
            # Если приоритет уже назначен вручную, учитываем его
            if task.priority == TaskPriority.NORMAL:
                # Вычисляем динамический приоритет
                dynamic_priority = await self.calculate_dynamic_priority(task)
                task.priority = self._convert_score_to_priority(dynamic_priority)

                self.logger.debug(f"Assigned priority {task.priority.name} to task {task.id} "
                                f"(score: {dynamic_priority:.2f})")

            return task

    async def update_priority(self, task_id: str, new_priority: str) -> bool:
        """
        Обновить приоритет задачи.

        Args:
            task_id: ID задачи
            new_priority: Новый приоритет

        Returns:
            True если приоритет обновлен
        """
        async with self._lock:
            try:
                priority_enum = TaskPriority[new_priority.upper()]

                # Записываем в историю эскалаций
                if task_id not in self._escalation_history:
                    self._escalation_history[task_id] = []

                self._escalation_history[task_id].append({
                    "timestamp": datetime.now(timezone.utc),
                    "new_priority": priority_enum.name,
                    "reason": "manual_update"
                })

                self.logger.info(f"Updated priority for task {task_id} to {priority_enum.name}")
                return True

            except KeyError:
                self.logger.error(f"Invalid priority: {new_priority}")
                return False

    async def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """
        Отсортировать задачи по приоритету.

        Args:
            tasks: Список задач

        Returns:
            Отсортированный список задач
        """
        async with self._lock:
            # Вычисляем динамические приоритеты для всех задач
            task_priorities = []
            for task in tasks:
                dynamic_priority = await self.calculate_dynamic_priority(task)
                task_priorities.append((task, dynamic_priority))

            # Сортируем по убыванию приоритета
            task_priorities.sort(key=lambda x: x[1], reverse=True)

            sorted_tasks = [task for task, _ in task_priorities]

            self.logger.debug(f"Sorted {len(tasks)} tasks by priority")
            return sorted_tasks

    async def escalate_priority(self, task_id: str, reason: str) -> bool:
        """
        Повысить приоритет задачи.

        Args:
            task_id: ID задачи
            reason: Причина эскалации

        Returns:
            True если приоритет повышен
        """
        async with self._lock:
            # Записываем эскалацию в историю
            if task_id not in self._escalation_history:
                self._escalation_history[task_id] = []

            escalation = {
                "timestamp": datetime.now(timezone.utc),
                "reason": reason,
                "escalation_type": "automatic"
            }

            self._escalation_history[task_id].append(escalation)

            # Увеличиваем динамический приоритет
            current_priority = self._dynamic_priorities.get(task_id, 0.0)
            escalated_priority = min(5.0, current_priority + 1.0)  # Максимум 5.0
            self._dynamic_priorities[task_id] = escalated_priority

            self.logger.info(f"Escalated priority for task {task_id}: {reason}")
            return True

    async def calculate_dynamic_priority(self, task: Task) -> float:
        """
        Вычислить динамический приоритет на основе различных факторов.

        Args:
            task: Задача

        Returns:
            Числовой приоритет (чем больше, тем выше приоритет)
        """
        total_score = 0.0
        total_weight = 0.0

        # Применяем все правила приоритета
        for rule in self._priority_rules:
            try:
                factor_value = rule.calculator(task)
                weighted_value = factor_value * rule.weight
                total_score += weighted_value
                total_weight += rule.weight

                self.logger.debug(f"Task {task.id}, {rule.factor.value}: "
                                f"{factor_value:.2f} (weight: {rule.weight})")

            except Exception as e:
                self.logger.warning(f"Error calculating {rule.factor.value} for task {task.id}: {e}")

        # Нормализуем итоговый счет
        if total_weight > 0:
            normalized_score = total_score / total_weight
        else:
            normalized_score = task.priority.value

        # Учитываем предыдущие эскалации
        escalation_bonus = self._calculate_escalation_bonus(task.id)
        final_score = normalized_score + escalation_bonus

        # Кэшируем результат
        self._dynamic_priorities[task.id] = final_score

        return final_score

    def _calculate_age_factor(self, task: Task) -> float:
        """
        Вычислить фактор возраста задачи.

        Args:
            task: Задача

        Returns:
            Фактор возраста (0.0 - 5.0)
        """
        if not task.created_at:
            return 0.0

        age_hours = (datetime.now(timezone.utc) - task.created_at).total_seconds() / 3600

        # Постепенное увеличение приоритета с возрастом
        if age_hours < 1:
            return 0.0
        elif age_hours < 6:
            return 0.5
        elif age_hours < 24:
            return 1.0
        elif age_hours < 72:
            return 2.0
        else:
            return 3.0

    def _calculate_deadline_factor(self, task: Task) -> float:
        """
        Вычислить фактор дедлайна.

        Args:
            task: Задача

        Returns:
            Фактор дедлайна (0.0 - 5.0)
        """
        # Предполагаем, что дедлайн хранится в контексте задачи
        deadline_str = task.context.get("deadline")
        if not deadline_str:
            return 0.0

        try:
            deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
            time_to_deadline = (deadline - datetime.now(timezone.utc)).total_seconds() / 3600

            if time_to_deadline < 0:
                return 5.0  # Просроченные задачи имеют максимальный приоритет
            elif time_to_deadline < 2:
                return 4.0
            elif time_to_deadline < 4:
                return 3.0
            elif time_to_deadline < 12:
                return 2.0
            elif time_to_deadline < 24:
                return 1.0
            else:
                return 0.0

        except (ValueError, TypeError):
            return 0.0

    def _calculate_retry_factor(self, task: Task) -> float:
        """
        Вычислить фактор повторных попыток.

        Args:
            task: Задача

        Returns:
            Фактор повторов (0.0 - 3.0)
        """
        retry_count = task.retry_count
        return min(3.0, retry_count * 0.5)

    def _calculate_user_priority_factor(self, task: Task) -> float:
        """
        Вычислить фактор пользовательского приоритета.

        Args:
            task: Задача

        Returns:
            Фактор пользовательского приоритета (1.0 - 5.0)
        """
        return float(task.priority.value)

    def _calculate_duration_factor(self, task: Task) -> float:
        """
        Вычислить фактор продолжительности выполнения.

        Args:
            task: Задача

        Returns:
            Фактор продолжительности (0.0 - 2.0)
        """
        if not task.estimated_duration:
            return 0.0

        # Короткие задачи получают небольшой бонус к приоритету
        duration_minutes = task.estimated_duration / 60

        if duration_minutes <= 5:
            return 2.0  # Очень короткие задачи
        elif duration_minutes <= 15:
            return 1.0  # Короткие задачи
        elif duration_minutes <= 60:
            return 0.0  # Средние задачи
        else:
            return -0.5  # Длинные задачи получают небольшой штраф

    def _calculate_escalation_bonus(self, task_id: str) -> float:
        """
        Вычислить бонус за эскалации.

        Args:
            task_id: ID задачи

        Returns:
            Бонус за эскалации
        """
        escalations = self._escalation_history.get(task_id, [])
        if not escalations:
            return 0.0

        # Каждая эскалация добавляет 0.5 к приоритету
        escalation_bonus = len(escalations) * 0.5

        # Бонус за недавние эскалации
        recent_escalations = [
            e for e in escalations
            if (datetime.now(timezone.utc) - e["timestamp"]).total_seconds() < 3600
        ]
        recent_bonus = len(recent_escalations) * 0.25

        return min(2.0, escalation_bonus + recent_bonus)

    def _convert_score_to_priority(self, score: float) -> TaskPriority:
        """
        Конвертировать числовой счет в enum приоритета.

        Args:
            score: Числовой счет

        Returns:
            Приоритет
        """
        if score >= 4.0:
            return TaskPriority.CRITICAL
        elif score >= 3.0:
            return TaskPriority.URGENT
        elif score >= 2.0:
            return TaskPriority.HIGH
        elif score >= 1.0:
            return TaskPriority.NORMAL
        else:
            return TaskPriority.LOW

    async def add_priority_rule(self, rule: PriorityRule):
        """
        Добавить новое правило приоритета.

        Args:
            rule: Правило приоритета
        """
        async with self._lock:
            self._priority_rules.append(rule)
            self.logger.info(f"Added priority rule: {rule.factor.value} (weight: {rule.weight})")

    async def remove_priority_rule(self, factor: PriorityFactor):
        """
        Удалить правило приоритета.

        Args:
            factor: Фактор для удаления
        """
        async with self._lock:
            original_length = len(self._priority_rules)
            self._priority_rules = [rule for rule in self._priority_rules if rule.factor != factor]

            if len(self._priority_rules) < original_length:
                self.logger.info(f"Removed priority rule: {factor.value}")

    async def update_escalation_settings(self, settings: Dict[str, Any]):
        """
        Обновить настройки эскалации.

        Args:
            settings: Новые настройки
        """
        async with self._lock:
            self._escalation_settings.update(settings)
            self.logger.info(f"Updated escalation settings: {settings}")

    async def auto_escalate_tasks(self, tasks: List[Task]) -> List[str]:
        """
        Автоматически эскалировать задачи по времени.

        Args:
            tasks: Список задач для проверки

        Returns:
            Список ID эскалированных задач
        """
        escalated_tasks = []
        current_time = datetime.now(timezone.utc)

        for task in tasks:
            should_escalate = False
            reason = ""

            # Проверяем возраст задачи
            if task.created_at:
                age_hours = (current_time - task.created_at).total_seconds() / 3600
                if age_hours > self._escalation_settings["age_threshold_hours"]:
                    should_escalate = True
                    reason = f"Task age exceeds {self._escalation_settings['age_threshold_hours']} hours"

            # Проверяем приближение дедлайна
            deadline_str = task.context.get("deadline")
            if deadline_str:
                try:
                    deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
                    hours_to_deadline = (deadline - current_time).total_seconds() / 3600

                    if (0 < hours_to_deadline < self._escalation_settings["deadline_urgency_hours"] and
                        task.priority.value < TaskPriority.URGENT.value):
                        should_escalate = True
                        reason = f"Deadline approaching in {hours_to_deadline:.1f} hours"

                except (ValueError, TypeError):
                    pass

            # Проверяем количество повторных попыток
            if task.retry_count > 2:
                should_escalate = True
                reason = f"Multiple retry attempts: {task.retry_count}"

            if should_escalate:
                await self.escalate_priority(task.id, reason)
                escalated_tasks.append(task.id)

        if escalated_tasks:
            self.logger.info(f"Auto-escalated {len(escalated_tasks)} tasks")

        return escalated_tasks

    async def get_priority_analytics(self) -> Dict[str, Any]:
        """
        Получить аналитику по приоритетам.

        Returns:
            Словарь с аналитикой
        """
        async with self._lock:
            total_escalations = sum(len(escalations) for escalations in self._escalation_history.values())

            # Подсчет эскалаций по причинам
            escalation_reasons = {}
            for escalations in self._escalation_history.values():
                for escalation in escalations:
                    reason = escalation.get("reason", "unknown")
                    escalation_reasons[reason] = escalation_reasons.get(reason, 0) + 1

            # Активные правила
            active_rules = {rule.factor.value: rule.weight for rule in self._priority_rules}

            return {
                "total_tasks_with_escalations": len(self._escalation_history),
                "total_escalations": total_escalations,
                "escalation_reasons": escalation_reasons,
                "active_priority_rules": active_rules,
                "escalation_settings": self._escalation_settings.copy(),
                "dynamic_priorities_cached": len(self._dynamic_priorities)
            }

    async def cleanup_old_data(self, days: int = 7):
        """
        Очистить старые данные.

        Args:
            days: Количество дней для хранения данных
        """
        async with self._lock:
            cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)

            # Очищаем старые эскалации
            for task_id in list(self._escalation_history.keys()):
                escalations = self._escalation_history[task_id]
                recent_escalations = [
                    e for e in escalations
                    if e["timestamp"] > cutoff_time
                ]

                if recent_escalations:
                    self._escalation_history[task_id] = recent_escalations
                else:
                    del self._escalation_history[task_id]

            # Очищаем старые кэшированные приоритеты
            # (в реальной системе здесь была бы более сложная логика)
            if len(self._dynamic_priorities) > 1000:
                # Оставляем только последние 500 записей
                sorted_items = sorted(self._dynamic_priorities.items())
                self._dynamic_priorities = dict(sorted_items[-500:])

            self.logger.info(f"Cleaned up priority data older than {days} days")