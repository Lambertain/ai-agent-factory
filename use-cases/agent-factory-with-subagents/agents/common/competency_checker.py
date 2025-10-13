# -*- coding: utf-8 -*-
"""
Модуль контроля компетенций агентов.

Определяет границы экспертизы каждого агента и автоматически
делегирует задачи соответствующим специалистам через Archon.
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

# Импорт матриц из отдельного модуля
from .competency_matrices import (
    AgentType,
    ERROR_TYPE_MATRIX,
    DELEGATION_MATRIX,
    CompetencyArea,
    build_keyword_competency_matrix
)


@dataclass
class CompetencyResult:
    """Результат проверки компетенции."""
    can_handle: bool
    confidence: float
    reason: str
    suggested_agent: Optional[str] = None
    delegation_priority: str = "medium"  # low, medium, high, critical


class CompetencyChecker:
    """Система проверки компетенций агентов."""

    def __init__(self):
        """Инициализация с матрицей компетенций."""
        # Импортируем готовые матрицы из competency_matrices.py
        self.competency_matrix = build_keyword_competency_matrix()
        self.delegation_matrix = DELEGATION_MATRIX
        self.error_type_matrix = ERROR_TYPE_MATRIX

    def is_in_competency(
        self,
        agent_role: str,
        error_type: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Проверить находится ли тип ошибки в компетенции агента.

        Главный метод для протокола обработки ошибок (09_problem_analysis_protocol.md).

        Args:
            agent_role: Роль текущего агента (например, "Archon Implementation Engineer")
            error_type: Тип обнаруженной ошибки (например, "typescript_compile")

        Returns:
            (в_компетенции, рекомендуемый_агент)
            - в_компетенции: True если агент может исправить эту ошибку
            - рекомендуемый_агент: Кому эскалировать если False

        Examples:
            >>> checker = CompetencyChecker()
            >>> checker.is_in_competency("Archon Implementation Engineer", "typescript_compile")
            (True, None)

            >>> checker.is_in_competency("Archon Implementation Engineer", "n_plus_one_query")
            (False, "Prisma Database Agent")
        """
        # Получаем ответственного агента для данного типа ошибки
        responsible_agent = self.error_type_matrix.get(error_type)

        if responsible_agent is None:
            # Неизвестный тип ошибки → эскалация к Analysis Lead
            return False, "Archon Analysis Lead"

        # Проверяем совпадает ли ответственный агент с текущим
        is_competent = (agent_role == responsible_agent)

        if is_competent:
            return True, None
        else:
            return False, responsible_agent

    def check_competency(
        self,
        task_description: str,
        agent_type: AgentType,
        context: Optional[Dict[str, Any]] = None
    ) -> CompetencyResult:
        """
        Проверить может ли агент выполнить задачу.

        Args:
            task_description: Описание задачи
            agent_type: Тип агента
            context: Дополнительный контекст

        Returns:
            Результат проверки компетенции
        """
        if agent_type not in self.competency_matrix:
            return CompetencyResult(
                can_handle=False,
                confidence=0.0,
                reason=f"Неизвестный тип агента: {agent_type}",
                suggested_agent="archon_analysis_lead"
            )

        competency = self.competency_matrix[agent_type]

        # Анализируем задачу
        task_lower = task_description.lower()

        # Проверяем исключения (что точно НЕ может делать)
        exclusion_matches = self._count_keyword_matches(task_lower, competency.exclusions)
        if exclusion_matches > 0:
            suggested_agent = self._find_suggested_agent(task_description)
            return CompetencyResult(
                can_handle=False,
                confidence=0.0,
                reason=f"Задача содержит области вне компетенции агента: {exclusion_matches} исключающих ключевых слов",
                suggested_agent=suggested_agent,
                delegation_priority="high"
            )

        # Проверяем основные компетенции
        primary_matches = self._count_keyword_matches(task_lower, competency.primary_keywords)
        secondary_matches = self._count_keyword_matches(task_lower, competency.secondary_keywords)

        # Вычисляем уверенность
        total_keywords = len(competency.primary_keywords) + len(competency.secondary_keywords)
        confidence = (primary_matches * 2 + secondary_matches) / max(total_keywords, 1)
        confidence = min(confidence, 1.0)  # Ограничиваем максимум

        can_handle = confidence >= competency.confidence_threshold

        if not can_handle:
            suggested_agent = self._find_suggested_agent(task_description)
            return CompetencyResult(
                can_handle=False,
                confidence=confidence,
                reason=f"Низкая уверенность ({confidence:.2f}) для выполнения задачи. Требуется {competency.confidence_threshold:.2f}",
                suggested_agent=suggested_agent,
                delegation_priority="medium" if confidence > 0.3 else "high"
            )

        return CompetencyResult(
            can_handle=True,
            confidence=confidence,
            reason=f"Агент компетентен для выполнения задачи (уверенность: {confidence:.2f})"
        )

    def _count_keyword_matches(self, text: str, keywords: List[str]) -> int:
        """Подсчитать количество совпадений ключевых слов в тексте."""
        matches = 0
        for keyword in keywords:
            if keyword.lower() in text:
                matches += 1
        return matches

    def _find_suggested_agent(self, task_description: str) -> str:
        """Найти наиболее подходящего агента для задачи."""
        task_lower = task_description.lower()
        best_agent = "archon_analysis_lead"  # По умолчанию
        best_score = 0

        for agent_type, competency in self.competency_matrix.items():
            # Не рекомендуем агента, если задача содержит исключения
            exclusion_matches = self._count_keyword_matches(task_lower, competency.exclusions)
            if exclusion_matches > 0:
                continue

            # Считаем соответствие
            primary_matches = self._count_keyword_matches(task_lower, competency.primary_keywords)
            secondary_matches = self._count_keyword_matches(task_lower, competency.secondary_keywords)

            score = primary_matches * 2 + secondary_matches

            if score > best_score:
                best_score = score
                best_agent = agent_type.value

        return best_agent

    def get_delegation_suggestions(self, agent_type: AgentType) -> List[str]:
        """Получить список агентов, которым можно делегировать задачи."""
        agent_name = agent_type.value
        return self.delegation_matrix.get(agent_name, [])

    def should_escalate_to_project_manager(
        self,
        task_description: str,
        confidence: float
    ) -> Tuple[bool, str]:
        """
        Определить нужно ли эскалировать задачу к Project Manager.

        Args:
            task_description: Описание задачи
            confidence: Уверенность в компетенции

        Returns:
            (нужна ли эскалация, причина)
        """
        task_lower = task_description.lower()

        # Ключевые слова, требующие вмешательства PM
        pm_keywords = [
            "приоритет", "priority", "срочно", "urgent", "критично", "critical",
            "планирование", "planning", "координация", "coordination",
            "ресурсы", "resources", "команда", "team", "deadline",
            "проект", "project", "milestone", "этап", "roadmap"
        ]

        pm_matches = self._count_keyword_matches(task_lower, pm_keywords)

        # Эскалация нужна если:
        # 1. Найдены PM ключевые слова
        # 2. Очень низкая уверенность (< 0.3)
        # 3. Задача содержит слова "все агенты", "команда", "координация"

        if pm_matches > 0:
            return True, f"Задача содержит управленческие аспекты ({pm_matches} ключевых слов)"

        if confidence < 0.3:
            return True, f"Слишком низкая уверенность ({confidence:.2f}) - требуется анализ PM"

        coordination_keywords = ["все агенты", "команда агентов", "координация", "оркестрация"]
        if any(keyword in task_lower for keyword in coordination_keywords):
            return True, "Задача требует координации между несколькими агентами"

        return False, ""


def check_task_competency(
    task_description: str,
    agent_type_name: str,
    context: Optional[Dict[str, Any]] = None
) -> CompetencyResult:
    """
    Универсальная функция проверки компетенции для любого агента.

    Args:
        task_description: Описание задачи
        agent_type_name: Имя типа агента (например, "analytics_tracking_agent")
        context: Дополнительный контекст

    Returns:
        Результат проверки компетенции
    """
    try:
        # Находим соответствующий enum
        agent_type = None
        for at in AgentType:
            if at.value == agent_type_name:
                agent_type = at
                break

        if agent_type is None:
            return CompetencyResult(
                can_handle=False,
                confidence=0.0,
                reason=f"Неизвестный тип агента: {agent_type_name}",
                suggested_agent="archon_analysis_lead"
            )

        checker = CompetencyChecker()
        return checker.check_competency(task_description, agent_type, context)

    except Exception as e:
        return CompetencyResult(
            can_handle=False,
            confidence=0.0,
            reason=f"Ошибка проверки компетенции: {e}",
            suggested_agent="archon_analysis_lead"
        )


def should_delegate_task(
    task_description: str,
    current_agent_type: str,
    confidence_threshold: float = 0.7
) -> Tuple[bool, Optional[str], str]:
    """
    Определить нужно ли делегировать задачу другому агенту.

    Args:
        task_description: Описание задачи
        current_agent_type: Тип текущего агента
        confidence_threshold: Порог уверенности

    Returns:
        (нужно ли делегировать, кому делегировать, причина)
    """
    result = check_task_competency(task_description, current_agent_type)

    if not result.can_handle:
        return True, result.suggested_agent, result.reason

    if result.confidence < confidence_threshold:
        return True, result.suggested_agent, f"Низкая уверенность: {result.confidence:.2f}"

    return False, None, f"Агент компетентен: {result.confidence:.2f}"


# Экспорт для других модулей
__all__ = [
    'CompetencyChecker',
    'CompetencyResult',
    'CompetencyArea',
    'AgentType',
    'check_task_competency',
    'should_delegate_task',
    # Главный метод для протокола обработки ошибок
    'is_in_competency'
]


def is_in_competency(
    agent_role: str,
    error_type: str
) -> Tuple[bool, Optional[str]]:
    """
    Быстрая проверка компетенции без создания экземпляра класса.

    Это удобная функция-обертка для использования в протоколе обработки ошибок.

    Args:
        agent_role: Роль текущего агента
        error_type: Тип обнаруженной ошибки

    Returns:
        (в_компетенции, рекомендуемый_агент)

    Examples:
        >>> from agents.common.competency_checker import is_in_competency
        >>> is_in_competency("Archon Implementation Engineer", "typescript_compile")
        (True, None)
    """
    checker = CompetencyChecker()
    return checker.is_in_competency(agent_role, error_type)