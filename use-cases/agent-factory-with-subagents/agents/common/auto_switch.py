#!/usr/bin/env python3
"""
Модуль автоматического переключения на Project Manager при определении команд управления.

Интегрируется во все агенты для автоматического анализа задач и переприоритизации.
"""

import asyncio
from typing import Dict, Any, Optional
from .keyword_detector import should_switch_to_pm, get_command_context


class ProjectManagerSwitcher:
    """Обработчик автопереключения на Project Manager."""

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
            # Импортируем Project Manager агент
            import sys
            import os
            sys.path.append(self.pm_agent_path)

            from agent import run_project_manager
            from dependencies import ProjectManagerDependencies

            # Создаем зависимости для PM
            pm_deps = ProjectManagerDependencies(
                project_id=self.archon_project_id,
                archon_project_id=self.archon_project_id
            )

            # Формируем запрос для Project Manager
            pm_query = self._build_pm_query(
                user_input=user_input,
                command_context=command_context,
                source_agent=source_agent
            )

            # Выполняем анализ через Project Manager
            pm_response = await run_project_manager(
                query=pm_query,
                project_id=self.archon_project_id,
                dependencies=pm_deps
            )

            # Парсим ответ и возвращаем структурированный результат
            return self._parse_pm_response(pm_response)

        except ImportError as e:
            return {
                "error": f"Не удалось импортировать Project Manager: {e}",
                "fallback": "Использование базового анализа задач"
            }
        except Exception as e:
            return {
                "error": f"Ошибка выполнения Project Manager: {e}",
                "fallback": "Продолжение работы без PM анализа"
            }

    def _build_pm_query(
        self,
        user_input: str,
        command_context: Dict[str, Any],
        source_agent: str
    ) -> str:
        """
        Построить запрос для Project Manager.

        Args:
            user_input: Исходная команда пользователя
            command_context: Контекст команды
            source_agent: Источник переключения

        Returns:
            Сформированный запрос для PM
        """
        detected_action = command_context.get("detected_action", "unknown")
        confidence = command_context.get("confidence", 0.0)
        has_urgency = command_context.get("has_urgency", False)
        has_priority = command_context.get("has_priority", False)

        query = f"""
**АВТОПЕРЕКЛЮЧЕНИЕ ОТ {source_agent.upper()}**

**Исходная команда пользователя:** {user_input}

**Обнаруженное действие:** {detected_action} (уверенность: {confidence:.2f})

**Анализ команды:**
- Срочность: {'Да' if has_urgency else 'Нет'}
- Высокий приоритет: {'Да' if has_priority else 'Нет'}
- Требует планирования: {command_context.get('requires_planning', False)}
- Упомянутые агенты: {', '.join(command_context.get('mentioned_agents', []))}

**ЗАДАЧИ PROJECT MANAGER:**
1. Проанализировать текущее состояние проекта AI Agent Factory
2. Определить приоритеты активных задач
3. При необходимости переприоритизировать задачи команды
4. Предоставить конкретные рекомендации по дальнейшим действиям
5. Назначить или переназначить задачи соответствующим агентам

**ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:**
- Анализ текущего состояния задач
- Список приоритетных действий
- Конкретные рекомендации по работе команды
- План дальнейших шагов

Выполни полный анализ и предоставь структурированный план действий.
"""
        return query

    def _parse_pm_response(self, pm_response: str) -> Dict[str, Any]:
        """
        Парсить ответ Project Manager и извлечь структурированную информацию.

        Args:
            pm_response: Ответ от Project Manager

        Returns:
            Структурированный результат анализа
        """
        # Базовая структура результата
        result = {
            "status": "completed",
            "raw_response": pm_response,
            "recommended_actions": [],
            "priority_changes": [],
            "task_assignments": [],
            "next_steps": []
        }

        try:
            # Простой парсинг ключевых элементов
            lines = pm_response.split('\n')
            current_section = None

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Определяем секции
                if any(keyword in line.lower() for keyword in ['рекомендации', 'действия', 'recommendations']):
                    current_section = 'actions'
                elif any(keyword in line.lower() for keyword in ['приоритет', 'priority']):
                    current_section = 'priorities'
                elif any(keyword in line.lower() for keyword in ['задачи', 'назначение', 'assignment']):
                    current_section = 'assignments'
                elif any(keyword in line.lower() for keyword in ['шаги', 'план', 'steps']):
                    current_section = 'steps'

                # Извлекаем элементы списков
                if line.startswith('-') or line.startswith('•') or any(line.startswith(f'{i}.') for i in range(1, 10)):
                    clean_line = line.lstrip('-•0123456789. ').strip()
                    if clean_line:
                        if current_section == 'actions':
                            result["recommended_actions"].append(clean_line)
                        elif current_section == 'priorities':
                            result["priority_changes"].append(clean_line)
                        elif current_section == 'assignments':
                            result["task_assignments"].append(clean_line)
                        elif current_section == 'steps':
                            result["next_steps"].append(clean_line)

            # Если не нашли структурированных данных, добавляем базовые рекомендации
            if not result["recommended_actions"] and not result["next_steps"]:
                result["recommended_actions"] = [
                    "Проверить статус текущих задач в Archon",
                    "Продолжить работу согласно приоритетам проекта",
                    "Координировать работу команды агентов"
                ]

        except Exception as e:
            result["parse_error"] = f"Ошибка парсинга: {e}"

        return result


async def auto_switch_to_project_manager(
    user_input: str,
    current_agent_name: str = "Unknown Agent",
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
    threshold: float = 0.7
) -> Dict[str, Any]:
    """
    Универсальная функция автопереключения на Project Manager.

    Используется всеми агентами для проверки команд управления.

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


def format_switch_result(switch_result: Dict[str, Any]) -> str:
    """
    Форматировать результат переключения для вывода пользователю.

    Args:
        switch_result: Результат переключения

    Returns:
        Форматированный текст для пользователя
    """
    if not switch_result.get("switched"):
        return ""

    output = []

    # Заголовок переключения
    output.append("🔄 **АВТОПЕРЕКЛЮЧЕНИЕ НА PROJECT MANAGER**")
    output.append(f"📝 Причина: {switch_result.get('reason', 'Обнаружена команда управления')}")

    if switch_result.get("confidence"):
        output.append(f"🎯 Уверенность: {switch_result['confidence']:.1%}")

    # Ошибка переключения
    if switch_result.get("error"):
        output.append(f"❌ Ошибка: {switch_result['error']}")
        if switch_result.get("fallback_action"):
            output.append(f"🔄 Альтернатива: {switch_result['fallback_action']}")
        return "\n".join(output)

    # Результаты анализа PM
    pm_analysis = switch_result.get("pm_analysis", {})

    if pm_analysis.get("recommended_actions"):
        output.append("\n🎯 **Рекомендуемые действия:**")
        for action in pm_analysis["recommended_actions"]:
            output.append(f"• {action}")

    if pm_analysis.get("priority_changes"):
        output.append("\n📊 **Изменения приоритетов:**")
        for change in pm_analysis["priority_changes"]:
            output.append(f"• {change}")

    if pm_analysis.get("task_assignments"):
        output.append("\n👥 **Назначения задач:**")
        for assignment in pm_analysis["task_assignments"]:
            output.append(f"• {assignment}")

    if pm_analysis.get("next_steps"):
        output.append("\n📋 **Следующие шаги:**")
        for step in pm_analysis["next_steps"]:
            output.append(f"• {step}")

    output.append("\n✅ Анализ Project Manager завершен, продолжаем работу согласно рекомендациям.")

    return "\n".join(output)


# Глобальная функция для быстрого доступа
async def check_pm_switch(user_input: str, agent_name: str = "Agent") -> Optional[str]:
    """
    Быстрая проверка необходимости переключения с выводом результата.

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