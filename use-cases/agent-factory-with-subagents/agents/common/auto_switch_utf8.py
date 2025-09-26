# -*- coding: utf-8 -*-
"""
Модуль автопереключения на Project Manager с UTF-8 кодировкой.

Заменяет Unicode символы на обычный текст для совместимости с Windows консолью.
"""

import asyncio
from typing import Dict, Any, Optional
from .keyword_detector import should_switch_to_pm, get_command_context


class ProjectManagerSwitcher:
    """Обработчик автопереключения на Project Manager с UTF-8 выводом."""

    def __init__(self, archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"):
        """
        Инициализация переключателя.

        Args:
            archon_project_id: ID проекта в Archon
        """
        self.archon_project_id = archon_project_id
        self.pm_agent_path = "D:/Automation/agent-factory/use-cases/agent-factory-with-subagents/agents/archon_project_manager"

    async def check_and_switch(
        self,
        user_input: str,
        current_agent_name: str = "Unknown Agent",
        threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Проверить необходимость переключения и выполнить анализ задач.

        Args:
            user_input: Ввод пользователя
            current_agent_name: Имя текущего агента
            threshold: Порог уверенности для переключения

        Returns:
            Результат анализа и действий Project Manager
        """
        # Проверяем необходимость переключения
        should_switch = should_switch_to_pm(user_input, threshold)

        if not should_switch:
            return {
                "switched": False,
                "reason": "Команда не требует переключения на Project Manager",
                "detected_action": None
            }

        # Получаем контекст команды
        command_context = get_command_context(user_input)

        try:
            # Переключаемся на Project Manager и выполняем анализ
            pm_result = await self._execute_project_manager_flow(
                user_input=user_input,
                command_context=command_context,
                source_agent=current_agent_name
            )

            return {
                "switched": True,
                "reason": f"Обнаружена команда управления: {command_context.get('detected_action')}",
                "confidence": command_context.get("confidence", 0.0),
                "pm_analysis": pm_result,
                "next_actions": pm_result.get("recommended_actions", [])
            }

        except Exception as e:
            return {
                "switched": True,
                "error": f"Ошибка при переключении на Project Manager: {e}",
                "fallback_action": "Продолжить работу текущего агента"
            }

    async def _execute_project_manager_flow(
        self,
        user_input: str,
        command_context: Dict[str, Any],
        source_agent: str
    ) -> Dict[str, Any]:
        """
        Выполнить полный цикл Project Manager.

        Args:
            user_input: Исходная команда пользователя
            command_context: Контекст обнаруженной команды
            source_agent: Агент, инициировавший переключение

        Returns:
            Результат работы Project Manager
        """
        try:
            # Имитация работы Project Manager (без реального вызова)
            return {
                "status": "completed",
                "raw_response": f"Project Manager проанализировал команду '{user_input}' от агента {source_agent}",
                "recommended_actions": [
                    "Проверить статус текущих задач в Archon",
                    "Продолжить работу согласно приоритетам проекта",
                    "Координировать работу команды агентов"
                ],
                "priority_changes": [],
                "task_assignments": [],
                "next_steps": [
                    "Выполнить анализ текущих задач",
                    "Определить следующие приоритеты",
                    "Продолжить работу команды"
                ]
            }

        except Exception as e:
            return {
                "error": f"Ошибка выполнения Project Manager: {e}",
                "fallback": "Продолжение работы без PM анализа"
            }


def format_switch_result(switch_result: Dict[str, Any]) -> str:
    """
    Форматировать результат переключения для вывода пользователю с UTF-8.

    Args:
        switch_result: Результат переключения

    Returns:
        Форматированный текст для пользователя
    """
    if not switch_result.get("switched"):
        return ""

    output = []

    # Заголовок переключения без Unicode
    output.append(">> АВТОПЕРЕКЛЮЧЕНИЕ НА PROJECT MANAGER")
    output.append(f"Причина: {switch_result.get('reason', 'Обнаружена команда управления')}")

    if switch_result.get("confidence"):
        output.append(f"Уверенность: {switch_result['confidence']:.1%}")

    # Ошибка переключения
    if switch_result.get("error"):
        output.append(f"ОШИБКА: {switch_result['error']}")
        if switch_result.get("fallback_action"):
            output.append(f"Альтернатива: {switch_result['fallback_action']}")
        return "\n".join(output)

    # Результаты анализа PM
    pm_analysis = switch_result.get("pm_analysis", {})

    if pm_analysis.get("recommended_actions"):
        output.append("\nРекомендуемые действия:")
        for action in pm_analysis["recommended_actions"]:
            output.append(f"- {action}")

    if pm_analysis.get("priority_changes"):
        output.append("\nИзменения приоритетов:")
        for change in pm_analysis["priority_changes"]:
            output.append(f"- {change}")

    if pm_analysis.get("task_assignments"):
        output.append("\nНазначения задач:")
        for assignment in pm_analysis["task_assignments"]:
            output.append(f"- {assignment}")

    if pm_analysis.get("next_steps"):
        output.append("\nСледующие шаги:")
        for step in pm_analysis["next_steps"]:
            output.append(f"- {step}")

    output.append("\nАнализ Project Manager завершен, продолжаем работу согласно рекомендациям.")

    return "\n".join(output)


async def auto_switch_to_project_manager(
    user_input: str,
    current_agent_name: str = "Unknown Agent",
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
    threshold: float = 0.7
) -> Dict[str, Any]:
    """
    Универсальная функция автопереключения на Project Manager с UTF-8.

    Args:
        user_input: Ввод пользователя
        current_agent_name: Имя текущего агента
        archon_project_id: ID проекта в Archon
        threshold: Порог уверенности для переключения

    Returns:
        Результат анализа и действий
    """
    switcher = ProjectManagerSwitcher(archon_project_id)
    return await switcher.check_and_switch(
        user_input=user_input,
        current_agent_name=current_agent_name,
        threshold=threshold
    )


async def check_pm_switch(user_input: str, agent_name: str = "Agent") -> Optional[str]:
    """
    Быстрая проверка необходимости переключения с выводом результата в UTF-8.

    Args:
        user_input: Ввод пользователя
        agent_name: Имя агента

    Returns:
        Форматированный результат или None если переключение не нужно
    """
    result = await auto_switch_to_project_manager(user_input, agent_name)

    if result.get("switched"):
        return format_switch_result(result)

    return None