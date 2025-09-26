"""
Утилиты для коммуникации агентов при работе с задачами.

Обеспечивает стандартизированное представление задач и переходов между ними
согласно обновленным коммуникационным паттернам AI Agent Factory.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class TaskInfo:
    """Информация о задаче для форматированного представления."""
    id: str
    title: str
    assignee: str
    task_order: int
    feature: str = ""
    status: str = "todo"
    description: str = ""


class TaskCommunicationFormatter:
    """Форматтер для стандартизированной коммуникации о задачах."""

    @staticmethod
    def format_next_task_prompt(task: TaskInfo) -> str:
        """
        Форматирует приглашение к выполнению следующей задачи.

        Args:
            task: Информация о задаче

        Returns:
            Отформатированное приглашение в стандартном формате
        """
        # Определяем приоритет по task_order
        priority_level = TaskCommunicationFormatter._get_priority_level(task.task_order)

        return f"Следующая задача: '{task.title}' (приоритет {priority_level}, {task.assignee}). Приступать?"

    @staticmethod
    def format_task_list_summary(tasks: List[TaskInfo], limit: int = 5) -> str:
        """
        Форматирует краткую сводку списка задач.

        Args:
            tasks: Список задач
            limit: Максимальное количество задач для отображения

        Returns:
            Отформатированная сводка задач
        """
        if not tasks:
            return "📋 Нет доступных задач"

        # Сортируем по приоритету (task_order)
        sorted_tasks = sorted(tasks, key=lambda t: t.task_order, reverse=True)

        summary = "📋 **Приоритетные задачи:**\n"

        for i, task in enumerate(sorted_tasks[:limit]):
            priority = TaskCommunicationFormatter._get_priority_level(task.task_order)
            status_emoji = TaskCommunicationFormatter._get_status_emoji(task.status)

            summary += f"{i+1}. {status_emoji} '{task.title}' ({priority}, {task.assignee})\n"

        if len(sorted_tasks) > limit:
            remaining = len(sorted_tasks) - limit
            summary += f"   ...и еще {remaining} задач\n"

        return summary

    @staticmethod
    def format_task_transition_announcement(
        completed_task: TaskInfo,
        next_task: TaskInfo
    ) -> str:
        """
        Форматирует объявление о переходе от завершенной к следующей задаче.

        Args:
            completed_task: Завершенная задача
            next_task: Следующая задача

        Returns:
            Отформатированное объявление о переходе
        """
        completed_priority = TaskCommunicationFormatter._get_priority_level(completed_task.task_order)
        next_priority = TaskCommunicationFormatter._get_priority_level(next_task.task_order)

        return f"""✅ **Завершена задача:** '{completed_task.title}' ({completed_priority})

{TaskCommunicationFormatter.format_next_task_prompt(next_task)}"""

    @staticmethod
    def format_delegation_announcement(
        current_task: TaskInfo,
        delegated_to_agent: str,
        delegation_reason: str
    ) -> str:
        """
        Форматирует объявление о делегировании задачи.

        Args:
            current_task: Текущая задача
            delegated_to_agent: Агент, которому делегируется
            delegation_reason: Причина делегирования

        Returns:
            Отформатированное объявление о делегировании
        """
        priority = TaskCommunicationFormatter._get_priority_level(current_task.task_order)

        return f"""🤝 **Делегирование задачи:**

📋 Задача: '{current_task.title}' ({priority})
👤 Делегирована: {delegated_to_agent}
💡 Причина: {delegation_reason}

Ожидаем результатов от специализированного агента."""

    @staticmethod
    def format_microtask_progress_update(
        main_task: TaskInfo,
        microtask_number: int,
        microtask_description: str,
        status: str = "completed"
    ) -> str:
        """
        Форматирует обновление прогресса микрозадачи.

        Args:
            main_task: Основная задача
            microtask_number: Номер микрозадачи
            microtask_description: Описание микрозадачи
            status: Статус (started, in_progress, completed, blocked)

        Returns:
            Отформатированное обновление прогресса
        """
        status_emoji = {
            "started": "🔄",
            "in_progress": "⏳",
            "completed": "✅",
            "blocked": "🚫"
        }.get(status, "📝")

        return f"{status_emoji} **Микрозадача {microtask_number}** ({status}): {microtask_description}"

    @staticmethod
    def _get_priority_level(task_order: int) -> str:
        """
        Определяет уровень приоритета по task_order.

        Args:
            task_order: Порядковый номер задачи

        Returns:
            Уровень приоритета в формате P[X]-[Level]
        """
        if task_order >= 90:
            return f"P0-Critical/task_order {task_order}"
        elif task_order >= 70:
            return f"P1-High/task_order {task_order}"
        elif task_order >= 50:
            return f"P2-Medium/task_order {task_order}"
        else:
            return f"P3-Low/task_order {task_order}"

    @staticmethod
    def _get_status_emoji(status: str) -> str:
        """
        Получает эмодзи для статуса задачи.

        Args:
            status: Статус задачи

        Returns:
            Соответствующий эмодзи
        """
        status_emojis = {
            "todo": "📋",
            "doing": "🔄",
            "review": "👀",
            "done": "✅",
            "blocked": "🚫"
        }
        return status_emojis.get(status, "📝")


def parse_archon_task_to_task_info(archon_task: Dict[str, Any]) -> TaskInfo:
    """
    Преобразует задачу из Archon в TaskInfo объект.

    Args:
        archon_task: Задача из Archon API

    Returns:
        TaskInfo объект
    """
    return TaskInfo(
        id=archon_task.get("id", ""),
        title=archon_task.get("title", ""),
        assignee=archon_task.get("assignee", "Unknown"),
        task_order=archon_task.get("task_order", 0),
        feature=archon_task.get("feature", ""),
        status=archon_task.get("status", "todo"),
        description=archon_task.get("description", "")
    )


def parse_archon_task_list_to_task_info_list(archon_tasks: List[Dict[str, Any]]) -> List[TaskInfo]:
    """
    Преобразует список задач из Archon в список TaskInfo объектов.

    Args:
        archon_tasks: Список задач из Archon API

    Returns:
        Список TaskInfo объектов
    """
    return [parse_archon_task_to_task_info(task) for task in archon_tasks]


def get_next_priority_task(archon_tasks: List[Dict[str, Any]], exclude_status: List[str] = None) -> Optional[TaskInfo]:
    """
    Находит следующую приоритетную задачу из списка Archon.

    Args:
        archon_tasks: Список задач из Archon API
        exclude_status: Статусы для исключения (по умолчанию исключает done, doing)

    Returns:
        TaskInfo следующей приоритетной задачи или None
    """
    if exclude_status is None:
        exclude_status = ["done", "doing"]

    # Обработка edge case: пустой или некорректный список задач
    if not archon_tasks or not isinstance(archon_tasks, list):
        return None

    # Фильтруем и сортируем задачи
    available_tasks = []
    for task in archon_tasks:
        # Защита от некорректных данных
        if not isinstance(task, dict):
            continue

        task_status = task.get("status", "unknown")
        if task_status not in exclude_status:
            try:
                task_info = parse_archon_task_to_task_info(task)
                available_tasks.append(task_info)
            except Exception:
                # Пропускаем задачи с некорректными данными
                continue

    if not available_tasks:
        return None

    # Сортируем по приоритету (task_order по убыванию)
    sorted_tasks = sorted(available_tasks, key=lambda t: t.task_order, reverse=True)

    return sorted_tasks[0]


# Примеры использования для документации
USAGE_EXAMPLES = {
    "basic_next_task": {
        "description": "Форматирование приглашения к следующей задаче",
        "code": """
task = TaskInfo(
    id="123",
    title="Тестирование и активация Puppeteer MCP",
    assignee="Implementation Engineer",
    task_order=77
)

prompt = TaskCommunicationFormatter.format_next_task_prompt(task)
print(prompt)
# Вывод: "Следующая задача: 'Тестирование и активация Puppeteer MCP' (приоритет P1-High/task_order 77, Implementation Engineer). Приступать?"
"""
    },

    "task_transition": {
        "description": "Объявление о переходе между задачами",
        "code": """
completed = TaskInfo(id="1", title="Оптимизация Fetch MCP", assignee="Engineer", task_order=71)
next_task = TaskInfo(id="2", title="Тестирование Puppeteer MCP", assignee="Engineer", task_order=77)

announcement = TaskCommunicationFormatter.format_task_transition_announcement(completed, next_task)
print(announcement)
"""
    },

    "archon_integration": {
        "description": "Интеграция с Archon для получения следующей задачи",
        "code": """
# Получение задач из Archon
archon_response = await mcp__archon__find_tasks(
    project_id="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
    filter_by="status",
    filter_value="todo"
)

# Поиск следующей приоритетной задачи
next_task = get_next_priority_task(archon_response["tasks"])

if next_task:
    prompt = TaskCommunicationFormatter.format_next_task_prompt(next_task)
    print(prompt)
else:
    print("📋 Все задачи выполнены!")
"""
    },

    "microtask_progress": {
        "description": "Отчетность о прогрессе микрозадач",
        "code": """
main_task = TaskInfo(id="1", title="Создание агента", assignee="Engineer", task_order=80)

# Отчет о выполнении микрозадачи
progress = TaskCommunicationFormatter.format_microtask_progress_update(
    main_task=main_task,
    microtask_number=1,
    microtask_description="Анализ требований",
    status="completed"
)
print(progress)
# Вывод: "✅ **Микрозадача 1** (completed): Анализ требований"
"""
    }
}


def create_agent_task_communication_mixin():
    """
    Создает mixin класс для добавления в AgentDependencies.

    Returns:
        Класс-миксин с методами коммуникации о задачах
    """

    class TaskCommunicationMixin:
        """Mixin для добавления коммуникационных возможностей в агенты."""

        async def get_next_task_formatted(self, project_id: str = None) -> str:
            """
            Получить отформатированное приглашение к следующей задаче.

            Args:
                project_id: ID проекта в Archon

            Returns:
                Отформатированное приглашение или сообщение об отсутствии задач
            """
            try:
                if not project_id and hasattr(self, 'archon_project_id'):
                    project_id = self.archon_project_id

                # Получаем задачи из Archon (предполагается доступность mcp__archon__find_tasks)
                # В реальной реализации здесь будет вызов MCP функции
                # Пока возвращаем заглушку
                return "📋 Требуется интеграция с Archon MCP для получения задач"

            except Exception as e:
                return f"❌ Ошибка получения следующей задачи: {e}"

        def format_microtask_completion(self, microtask_number: int, description: str) -> str:
            """
            Форматирует сообщение о завершении микрозадачи.

            Args:
                microtask_number: Номер микрозадачи
                description: Описание микрозадачи

            Returns:
                Отформатированное сообщение
            """
            return f"✅ **Микрозадача {microtask_number}** (completed): {description}"

    return TaskCommunicationMixin


# Константы для использования в агентах
TASK_PRIORITY_THRESHOLDS = {
    "CRITICAL": 90,
    "HIGH": 70,
    "MEDIUM": 50,
    "LOW": 0
}

DEFAULT_EXCLUDE_STATUS = ["done", "doing", "archived"]

# Шаблоны сообщений
MESSAGE_TEMPLATES = {
    "no_tasks": "📋 Все приоритетные задачи выполнены!",
    "task_blocked": "🚫 Следующая задача заблокирована: '{title}' ({reason})",
    "delegation_needed": "🤝 Задача '{title}' требует делегирования агенту {agent_type}",
    "waiting_approval": "⏳ Ожидаем подтверждения для начала задачи '{title}'",
    "archon_unavailable": "❌ Archon недоступен. Переключение на локальный режим работы."
}

# Fallback механизм при недоступности Archon
class ArchonFallbackHandler:
    """Обработчик fallback режима при недоступности Archon."""

    @staticmethod
    def get_fallback_message(context: str = "task_transition") -> str:
        """
        Получить fallback сообщение при недоступности Archon.

        Args:
            context: Контекст использования (task_transition, task_creation, etc.)

        Returns:
            Соответствующее fallback сообщение
        """
        fallback_messages = {
            "task_transition": """
❌ **Archon недоступен** - не удается получить следующую задачу.

💡 **Рекомендации:**
1. Проверьте доступность Archon по адресу http://localhost:3737/
2. Убедитесь, что MCP сервер Archon запущен
3. Временно работайте в локальном режиме с TodoWrite

🔄 **Автоматическое восстановление:** При восстановлении связи система вернется к работе с Archon.
""",
            "task_creation": """
❌ **Archon недоступен** - не удается создать задачу в проекте.

💡 **Действия:**
1. Сохраните задачу локально для последующей синхронизации
2. Проверьте статус Archon: http://localhost:3737/health
3. После восстановления синхронизируйте задачи с Archon
""",
            "task_status": """
❌ **Archon недоступен** - не удается обновить статус задачи.

📋 **Локальное отслеживание:** Задача выполняется в автономном режиме.
Синхронизация произойдет автоматически при восстановлении связи с Archon.
"""
        }

        return fallback_messages.get(context, MESSAGE_TEMPLATES["archon_unavailable"])

    @staticmethod
    def should_use_fallback(error_message: str) -> bool:
        """
        Определить нужно ли использовать fallback режим.

        Args:
            error_message: Сообщение об ошибке

        Returns:
            True если нужен fallback режим
        """
        fallback_indicators = [
            "connection",
            "network",
            "timeout",
            "unavailable",
            "refused",
            "archon"
        ]

        error_lower = error_message.lower()
        return any(indicator in error_lower for indicator in fallback_indicators)

if __name__ == "__main__":
    # Демонстрация использования
    print("=== Демонстрация TaskCommunicationFormatter ===\n")

    # Пример задачи
    sample_task = TaskInfo(
        id="test-123",
        title="Тестирование и активация Puppeteer MCP для автоматизации браузера",
        assignee="Implementation Engineer",
        task_order=77,
        feature="mcp-testing",
        status="todo"
    )

    # Форматирование приглашения
    next_prompt = TaskCommunicationFormatter.format_next_task_prompt(sample_task)
    print("📋 Приглашение к задаче:")
    print(next_prompt)
    print()

    # Пример списка задач
    sample_tasks = [
        TaskInfo("1", "Критическая безопасность", "Security Agent", 95),
        TaskInfo("2", "Оптимизация производительности", "Performance Agent", 75),
        TaskInfo("3", "Обновление документации", "Docs Agent", 45),
    ]

    task_summary = TaskCommunicationFormatter.format_task_list_summary(sample_tasks)
    print("📊 Сводка задач:")
    print(task_summary)
    print()

    # Пример прогресса микрозадачи
    progress = TaskCommunicationFormatter.format_microtask_progress_update(
        sample_task, 1, "Анализ требований и планирование", "completed"
    )
    print("⏳ Прогресс микрозадачи:")
    print(progress)