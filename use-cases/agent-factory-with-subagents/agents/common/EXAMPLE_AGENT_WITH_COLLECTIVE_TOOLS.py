# -*- coding: utf-8 -*-
"""
Пример агента с интегрированными инструментами коллективной работы

Этот файл демонстрирует:
- Правильное создание агента через create_universal_pydantic_agent
- Использование run_with_integrations для автоматических интеграций
- Структуру dependencies с полями для RAG и Archon
- Обязательные финальные шаги
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional
from pydantic_ai import Agent, RunContext

# Импорты для универсального создания агента
from .pydantic_ai_decorators import create_universal_pydantic_agent
from .pydantic_ai_integrations import run_with_integrations, execute_mandatory_final_steps


# ============================================================================
# DEPENDENCIES - Зависимости агента
# ============================================================================

@dataclass
class ExampleAgentDependencies:
    """
    Зависимости для примера агента с поддержкой коллективной работы.

    ОБЯЗАТЕЛЬНЫЕ ПОЛЯ для коллективной работы:
    - agent_name: для идентификации в системе
    - archon_project_id: для интеграции с Archon
    - knowledge_tags: для поиска в базе знаний
    """

    # Основные настройки
    api_key: str
    project_path: str = ""

    # ОБЯЗАТЕЛЬНЫЕ для коллективной работы
    agent_name: str = "example_agent"
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"  # AI Agent Factory

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "example-agent",
        "agent-knowledge",
        "pydantic-ai"
    ])
    knowledge_domain: Optional[str] = None

    def __post_init__(self):
        """Инициализация после создания dataclass."""
        if not self.knowledge_domain:
            self.knowledge_domain = "example.domain.com"


# ============================================================================
# SYSTEM PROMPT - Системный промпт агента
# ============================================================================

def get_system_prompt() -> str:
    """
    Системный промпт агента.

    ОБЯЗАТЕЛЬНО включает:
    - Описание экспертизы
    - Инструкции по использованию коллективных инструментов
    - Обязательный рабочий процесс
    """
    return """
Ты Example Agent - эксперт по демонстрации коллективной работы агентов.

## Твоя экспертиза:
- Демонстрация правильного использования инструментов коллективной работы
- Разбивка задач на микрозадачи
- Отчетность о прогрессе
- Рефлексия и улучшение результатов
- Делегирование задач другим агентам

## ОБЯЗАТЕЛЬНЫЙ рабочий процесс:

### 1. В НАЧАЛЕ КАЖДОЙ ЗАДАЧИ:
- Используй инструмент break_down_to_microtasks() для разбивки задачи
- Покажи план пользователю перед началом работы
- Получи подтверждение (в автоматическом режиме считается одобренным)

### 2. ВО ВРЕМЯ ВЫПОЛНЕНИЯ:
- Используй report_microtask_progress() для каждой микрозадачи
- Вызывай check_delegation_need() для проверки необходимости делегирования
- Если нужно - делегируй через delegate_task_to_agent()

### 3. ПЕРЕД ЗАВЕРШЕНИЕМ (ОБЯЗАТЕЛЬНО):
- Используй reflect_and_improve() для критического анализа
- Найди минимум 2-3 конкретных недостатка
- Улучши результат перед финализацией

### 4. ФИНАЛИЗАЦИЯ:
- Обязательные шаги выполняются автоматически через run_with_integrations()
- Git коммит создается автоматически
- Статус в Archon обновляется автоматически

## Инструменты доступные тебе:
- break_down_to_microtasks(main_task, complexity_level)
- report_microtask_progress(microtask_number, description, status, details)
- reflect_and_improve(completed_work, work_type)
- check_delegation_need(current_task, current_agent_type)
- delegate_task_to_agent(target_agent, task_title, task_description, priority)
- search_agent_knowledge(query, match_count)

## Правила:
1. НИКОГДА не пропускай разбивку на микрозадачи
2. ВСЕГДА отчитывайся о прогрессе каждой микрозадачи
3. ОБЯЗАТЕЛЬНО проводи рефлексию перед завершением
4. Делегируй задачи вне твоей компетенции

## Критерии качества:
- ✅ План работы показан пользователю
- ✅ Прогресс отображается в реальном времени
- ✅ Рефлексия проведена с выявлением недостатков
- ✅ Результат улучшен на основе рефлексии
- ✅ Финальные шаги выполнены (Git + Archon)
"""


# ============================================================================
# MODEL CONFIGURATION - Настройка LLM модели
# ============================================================================

def get_llm_model():
    """Получить настроенную LLM модель."""
    from pydantic_ai.providers.openai import OpenAIProvider
    from pydantic_ai.models.openai import OpenAIModel

    api_key = os.getenv("LLM_API_KEY", "")
    base_url = os.getenv(
        "LLM_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    model_name = os.getenv("LLM_MODEL", "qwen2.5-coder-32b-instruct")

    provider = OpenAIProvider(base_url=base_url, api_key=api_key)
    return OpenAIModel(model_name, provider=provider)


# ============================================================================
# AGENT CREATION - Создание агента
# ============================================================================

# Создаем агента с автоматическими интеграциями
example_agent = create_universal_pydantic_agent(
    model=get_llm_model(),
    deps_type=ExampleAgentDependencies,
    system_prompt=get_system_prompt(),
    agent_type="example_agent",
    knowledge_tags=["example-agent", "agent-knowledge", "pydantic-ai"],
    knowledge_domain="example.domain.com",
    with_collective_tools=True,  # ✅ Автоматически добавляет коллективные инструменты
    with_knowledge_tool=True     # ✅ Автоматически добавляет поиск в базе знаний
)


# ============================================================================
# CUSTOM TOOLS - Специфичные инструменты агента (опционально)
# ============================================================================

@example_agent.tool
async def example_specific_tool(
    ctx: RunContext[ExampleAgentDependencies],
    parameter: str
) -> str:
    """
    Пример специфичного инструмента агента.

    Добавляется к уже существующим коллективным инструментам.

    Args:
        ctx: Контекст выполнения
        parameter: Какой-то параметр

    Returns:
        Результат работы инструмента
    """
    return f"Выполнен специфичный инструмент с параметром: {parameter}"


# ============================================================================
# RUNNER FUNCTION - Функция запуска агента
# ============================================================================

async def run_example_agent(
    user_message: str,
    api_key: str,
    project_path: str = "",
    archon_task_id: Optional[str] = None
) -> str:
    """
    Запустить Example Agent с полными интеграциями.

    Эта функция демонстрирует правильный способ запуска агента с:
    - Автоматической разбивкой на микрозадачи
    - Отчетностью о прогрессе
    - Проверкой делегирования
    - Рефлексией и улучшением
    - Обязательными финальными шагами (Git + Archon)

    Args:
        user_message: Сообщение пользователя
        api_key: API ключ для LLM
        project_path: Путь к проекту (опционально)
        archon_task_id: ID задачи в Archon (опционально)

    Returns:
        Результат работы агента с примененными интеграциями

    Example:
        >>> result = await run_example_agent(
        ...     user_message="Демонстрация коллективной работы",
        ...     api_key=os.getenv("LLM_API_KEY"),
        ...     archon_task_id="task-123"
        ... )
    """

    # Создаем зависимости
    deps = ExampleAgentDependencies(
        api_key=api_key,
        project_path=project_path
    )

    # ✅ ПРАВИЛЬНЫЙ СПОСОБ: Используем run_with_integrations
    # Это автоматически применяет ВСЕ интеграции:
    # - Разбивка на микрозадачи (показывается пользователю)
    # - Проверка делегирования
    # - Отчетность о прогрессе
    # - Рефлексия и улучшение
    # - Git коммит
    # - Обновление Archon

    result = await run_with_integrations(
        agent=example_agent,
        user_message=user_message,
        deps=deps,
        agent_type="example_agent"
    )

    # Обязательные финальные шаги (если нужно вручную)
    # Обычно выполняются автоматически через run_with_integrations,
    # но можно вызвать вручную для полного контроля:

    if archon_task_id:
        final_report = await execute_mandatory_final_steps(
            task_description=user_message,
            agent_type="example_agent",
            task_id=archon_task_id,
            task_status="done",
            notes=f"Результат: {result[:100]}..."
        )
        print("\n" + "="*60)
        print(final_report)
        print("="*60 + "\n")

    return result


# ============================================================================
# АЛЬТЕРНАТИВНЫЙ СПОСОБ - Ручное использование инструментов
# ============================================================================

async def run_example_agent_manual(
    user_message: str,
    api_key: str,
    archon_task_id: Optional[str] = None
) -> str:
    """
    Альтернативный способ запуска с ручным использованием инструментов.

    ⚠️ НЕ РЕКОМЕНДУЕТСЯ для обычного использования.
    Используйте run_with_integrations вместо этого.

    Этот способ демонстрирует что происходит "под капотом".
    """

    from .collective_work_tools import (
        break_down_to_microtasks,
        report_microtask_progress,
        reflect_and_improve,
        check_delegation_need
    )

    deps = ExampleAgentDependencies(api_key=api_key)

    # Создаем фейковый контекст для демонстрации
    class FakeContext:
        def __init__(self, deps):
            self.deps = deps

    ctx = FakeContext(deps)

    # 1. Разбивка на микрозадачи
    print("\n🔹 ШАГ 1: Разбивка на микрозадачи")
    microtasks_plan = await break_down_to_microtasks(
        ctx, user_message, complexity_level="medium"
    )
    print(microtasks_plan)

    # 2. Выполнение с отчетностью
    print("\n🔹 ШАГ 2: Выполнение микрозадач")
    progress_1 = await report_microtask_progress(
        ctx, 1, "Анализ задачи", "completed", "Задача проанализирована"
    )
    print(progress_1)

    # 3. Проверка делегирования
    print("\n🔹 ШАГ 3: Проверка делегирования")
    delegation_check = await check_delegation_need(
        ctx, user_message, "example_agent"
    )
    print(delegation_check)

    # 4. Основное выполнение
    print("\n🔹 ШАГ 4: Основное выполнение")
    result = await example_agent.run(user_message, deps=deps)
    agent_response = result.data

    # 5. Рефлексия
    print("\n🔹 ШАГ 5: Рефлексия и улучшение")
    reflection = await reflect_and_improve(
        ctx, agent_response, work_type="implementation"
    )
    print(reflection)

    # 6. Финальные шаги
    if archon_task_id:
        print("\n🔹 ШАГ 6: Финальные шаги")
        final_report = await execute_mandatory_final_steps(
            task_description=user_message,
            agent_type="example_agent",
            task_id=archon_task_id,
            task_status="done"
        )
        print(final_report)

    return agent_response


# ============================================================================
# QUICK START FUNCTION - Быстрый старт для тестирования
# ============================================================================

async def quick_start_example():
    """
    Быстрый старт для тестирования агента.

    Демонстрирует минимальный код для запуска агента с коллективными инструментами.
    """
    import os
    from dotenv import load_dotenv

    # Загружаем переменные окружения
    load_dotenv()

    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        print("❌ Ошибка: LLM_API_KEY не найден в переменных окружения")
        return

    # Запускаем агента
    result = await run_example_agent(
        user_message="Демонстрация работы коллективных инструментов",
        api_key=api_key
    )

    print("\n" + "="*60)
    print("РЕЗУЛЬТАТ РАБОТЫ АГЕНТА:")
    print("="*60)
    print(result)
    print("="*60)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "example_agent",
    "run_example_agent",
    "run_example_agent_manual",
    "quick_start_example",
    "ExampleAgentDependencies"
]


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
ПРИМЕР 1: Базовое использование

```python
import asyncio
from agents.common.EXAMPLE_AGENT_WITH_COLLECTIVE_TOOLS import run_example_agent

async def main():
    result = await run_example_agent(
        user_message="Твоя задача",
        api_key="your_api_key"
    )
    print(result)

asyncio.run(main())
```

ПРИМЕР 2: С Archon task ID

```python
result = await run_example_agent(
    user_message="Твоя задача",
    api_key="your_api_key",
    archon_task_id="f5250349-9315-46d0-9969-760f3018f6e5"
)
```

ПРИМЕР 3: Быстрый старт

```python
from agents.common.EXAMPLE_AGENT_WITH_COLLECTIVE_TOOLS import quick_start_example
import asyncio

asyncio.run(quick_start_example())
```

ПРИМЕР 4: Создание собственного агента на основе этого примера

1. Скопируйте этот файл в вашу директорию агента
2. Переименуйте класс зависимостей: ExampleAgentDependencies → YourAgentDependencies
3. Обновите system_prompt с вашей экспертизой
4. Добавьте специфичные инструменты через @agent.tool
5. Обновите knowledge_tags и agent_type
6. Используйте run_with_integrations для запуска

Все коллективные инструменты будут работать автоматически!
"""
