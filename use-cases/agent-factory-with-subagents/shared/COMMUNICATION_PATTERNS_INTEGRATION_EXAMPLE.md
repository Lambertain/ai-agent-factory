# 🗣️ Пример интеграции коммуникационных паттернов в агента

## 📋 Обновление существующего агента

Этот пример показывает, как интегрировать новые коммуникационные паттерны в уже существующий агент.

### 1. Обновление dependencies.py

```python
from dataclasses import dataclass
from typing import Optional
from shared.task_communication_utils import TaskCommunicationFormatter, ArchonFallbackHandler

@dataclass
class AgentDependencies:
    """Зависимости агента с поддержкой новых коммуникационных паттернов."""

    # Основные настройки
    api_key: str
    project_path: str = ""

    # Новые поля для коммуникации
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
    enable_task_communication: bool = True
    agent_name: str = ""

    def __post_init__(self):
        """Инициализация agent_name если не указан."""
        if not self.agent_name:
            # Извлекаем из модуля
            module_parts = self.__class__.__module__.split('.')
            if 'agents' in module_parts:
                agent_index = module_parts.index('agents')
                if agent_index + 1 < len(module_parts):
                    self.agent_name = module_parts[agent_index + 1]
```

### 2. Добавление инструментов коммуникации в tools.py

```python
from pydantic_ai import RunContext
from shared.task_communication_utils import (
    TaskCommunicationFormatter,
    get_next_priority_task,
    ArchonFallbackHandler
)

@agent.tool
async def transition_to_next_task(
    ctx: RunContext[AgentDependencies],
    completed_task_title: str = ""
) -> str:
    """
    Завершить текущую задачу и перейти к следующей приоритетной.

    ОБЯЗАТЕЛЬНО используется в конце каждой задачи для стандартизированного перехода.

    Args:
        completed_task_title: Название завершенной задачи (опционально)

    Returns:
        Форматированное приглашение к следующей задаче
    """
    if not ctx.deps.enable_task_communication:
        return "📋 Коммуникационные паттерны отключены"

    try:
        # Получаем задачи из Archon
        archon_response = await mcp__archon__find_tasks(
            project_id=ctx.deps.archon_project_id,
            filter_by="status",
            filter_value="todo"
        )

        if not archon_response.get("success", False):
            raise Exception(f"Archon API error: {archon_response.get('message', 'Unknown error')}")

        # Находим следующую приоритетную задачу
        next_task = get_next_priority_task(archon_response.get("tasks", []))

        if next_task:
            # Форматируем переход с завершенной задачей (если указана)
            if completed_task_title:
                from shared.task_communication_utils import TaskInfo
                completed_task_info = TaskInfo(
                    id="completed",
                    title=completed_task_title,
                    assignee=ctx.deps.agent_name or "Current Agent",
                    task_order=0,
                    status="done"
                )

                return TaskCommunicationFormatter.format_task_transition_announcement(
                    completed_task_info, next_task
                )
            else:
                # Простое приглашение к следующей задаче
                return TaskCommunicationFormatter.format_next_task_prompt(next_task)
        else:
            completion_msg = ""
            if completed_task_title:
                completion_msg = f"✅ **Завершена задача:** '{completed_task_title}'\n\n"

            return f"{completion_msg}📋 Все приоритетные задачи выполнены!"

    except Exception as e:
        error_msg = str(e)

        # Проверяем нужен ли fallback режим
        if ArchonFallbackHandler.should_use_fallback(error_msg):
            return ArchonFallbackHandler.get_fallback_message("task_transition")
        else:
            return f"❌ Ошибка перехода к следующей задаче: {error_msg}"


@agent.tool
async def report_task_progress(
    ctx: RunContext[AgentDependencies],
    task_title: str,
    progress_description: str,
    completion_percentage: int = 0
) -> str:
    """
    Отчитаться о прогрессе выполнения текущей задачи.

    Args:
        task_title: Название задачи
        progress_description: Описание прогресса
        completion_percentage: Процент выполнения (0-100)

    Returns:
        Форматированный отчет о прогрессе
    """
    progress_emoji = "🔄" if completion_percentage < 100 else "✅"

    return f"""
{progress_emoji} **Прогресс задачи:** '{task_title}'

📊 **Выполнено:** {completion_percentage}%
📝 **Статус:** {progress_description}

{"🎯 Задача завершена!" if completion_percentage == 100 else "⏳ Работа продолжается..."}
"""


@agent.tool
async def show_current_task_list(
    ctx: RunContext[AgentDependencies],
    limit: int = 5
) -> str:
    """
    Показать текущий список приоритетных задач.

    Args:
        limit: Максимальное количество задач для отображения

    Returns:
        Форматированный список задач
    """
    try:
        # Получаем задачи из Archon
        archon_response = await mcp__archon__find_tasks(
            project_id=ctx.deps.archon_project_id,
            filter_by="status",
            filter_value="todo"
        )

        if not archon_response.get("success", False):
            raise Exception("Ошибка получения задач из Archon")

        tasks = archon_response.get("tasks", [])

        if not tasks:
            return "📋 Нет доступных задач"

        # Используем форматтер для отображения списка
        from shared.task_communication_utils import parse_archon_task_list_to_task_info_list
        task_info_list = parse_archon_task_list_to_task_info_list(tasks)

        return TaskCommunicationFormatter.format_task_list_summary(task_info_list, limit)

    except Exception as e:
        if ArchonFallbackHandler.should_use_fallback(str(e)):
            return ArchonFallbackHandler.get_fallback_message("task_transition")
        else:
            return f"❌ Ошибка получения списка задач: {e}"
```

### 3. Обновление основного агента (agent.py)

```python
from pydantic_ai import Agent
from .dependencies import AgentDependencies
from .tools import transition_to_next_task, report_task_progress, show_current_task_list

# Создание агента с обновленными инструментами коммуникации
agent = Agent(
    get_llm_model(),
    deps_type=AgentDependencies,
    system_prompt="""
Ты специализированный агент с улучшенными коммуникационными паттернами.

## ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА КОММУНИКАЦИИ:

### ПРИ ЗАВЕРШЕНИИ ЗАДАЧИ:
ВСЕГДА используй transition_to_next_task() для перехода к следующей задаче.

❌ НЕПРАВИЛЬНО: "Переходим к следующей задаче?"
✅ ПРАВИЛЬНО: Вызвать transition_to_next_task("Название завершенной задачи")

### ВО ВРЕМЯ РАБОТЫ:
Используй report_task_progress() для отчетности о прогрессе.

### ФОРМАТ СЛЕДУЮЩЕЙ ЗАДАЧИ:
Система автоматически форматирует в виде:
"Следующая задача: '[название]' (приоритет P[X]-[уровень]/task_order [число], [assignee]). Приступать?"

### FALLBACK РЕЖИМ:
При недоступности Archon система автоматически переключается в локальный режим.
""",
    tools=[
        transition_to_next_task,
        report_task_progress,
        show_current_task_list,
        # ... другие инструменты агента
    ]
)

# Пример использования в функции агента
async def complete_analysis_task():
    """Пример выполнения задачи с новыми паттернами коммуникации."""

    # Отчет о начале работы
    progress_report = await report_task_progress(
        task_title="Анализ требований",
        progress_description="Начинаю анализ технических требований",
        completion_percentage=10
    )
    print(progress_report)

    # ... выполнение работы ...

    # Отчет о прогрессе
    progress_report = await report_task_progress(
        task_title="Анализ требований",
        progress_description="Завершен анализ API требований",
        completion_percentage=50
    )
    print(progress_report)

    # ... завершение работы ...

    # Финальный отчет и переход к следующей задаче
    transition_message = await transition_to_next_task(
        completed_task_title="Анализ требований"
    )
    print(transition_message)
    # Вывод: "✅ **Завершена задача:** 'Анализ требований'
    #
    #         Следующая задача: 'Проектирование архитектуры' (приоритет P1-High/task_order 75, Blueprint Architect). Приступать?"
```

### 4. Обновление README агента

```markdown
# Agent Name

## Коммуникационные возможности

Этот агент поддерживает новые стандартизированные коммуникационные паттерны:

### Автоматический переход между задачами
- Конкретные названия следующих задач
- Уровни приоритета (P0-Critical, P1-High, P2-Medium, P3-Low)
- Назначенные исполнители
- Подтверждение готовности

### Отчетность о прогрессе
- Процентное выполнение задач
- Детальные обновления статуса
- Промежуточные результаты

### Fallback режим
- Автоматическое переключение при недоступности Archon
- Локальное отслеживание прогресса
- Восстановление синхронизации

## Примеры использования

```python
# Переход к следующей задаче
await transition_to_next_task("Завершенная задача")

# Отчет о прогрессе
await report_task_progress("Текущая задача", "Описание прогресса", 75)

# Показать список задач
await show_current_task_list(limit=5)
```
```

## 🔧 Инструкции по обновлению существующих агентов

### Шаг 1: Проверка совместимости
```bash
# Убедитесь, что task_communication_utils.py доступен
python -c "from shared.task_communication_utils import TaskCommunicationFormatter; print('✅ Модуль доступен')"
```

### Шаг 2: Обновление зависимостей
1. Добавить поля `archon_project_id`, `enable_task_communication`, `agent_name` в dependencies
2. Реализовать `__post_init__` для автоопределения agent_name

### Шаг 3: Интеграция инструментов
1. Добавить `transition_to_next_task` в список инструментов агента
2. Обновить системный промпт с новыми правилами коммуникации
3. Заменить старые паттерны перехода между задачами

### Шаг 4: Тестирование
1. Проверить работу с доступным Archon
2. Протестировать fallback режим при недоступности Archon
3. Убедиться в корректности форматирования сообщений

## 📊 Преимущества новых паттернов

- ✅ **Прозрачность**: Пользователи видят точные названия и приоритеты задач
- ✅ **Контроль**: Явные запросы подтверждения перед началом задач
- ✅ **Отказоустойчивость**: Graceful degradation при проблемах с Archon
- ✅ **Консистентность**: Единообразный формат во всех агентах фабрики
- ✅ **Отслеживаемость**: Детальная отчетность о прогрессе выполнения

---

*Документ создан в рамках улучшения коммуникационных паттернов AI Agent Factory*