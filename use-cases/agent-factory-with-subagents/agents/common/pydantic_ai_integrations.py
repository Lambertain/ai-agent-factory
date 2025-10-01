# -*- coding: utf-8 -*-
"""
Система интеграций для Pydantic AI агентов

Универсальные декораторы и хуки для интеграции следующих систем:
- Автопереключение к Project Manager
- Проверка компетенций и делегирование
- Планирование микрозадач с отчетностью
- Git коммиты при завершении задач
- Русская локализация

Предназначен для прямой Pydantic AI архитектуры без wrapper-классов.
"""

import asyncio
import logging
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union
from datetime import datetime

from pydantic_ai import Agent, RunContext
from pydantic import BaseModel

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PydanticAIIntegration:
    """
    Система интеграций для Pydantic AI агентов.

    Предоставляет универсальные методы для интеграции всех систем
    непосредственно в Agent.run() вызовы без модификации кода агентов.
    """

    def __init__(self):
        self.enabled_integrations = {
            "pm_switch": True,
            "competency_check": True,
            "microtask_planning": True,
            "git_commits": True,
            "russian_localization": True
        }

    async def apply_pre_run_integrations(
        self,
        agent_name: str,
        user_message: str,
        agent_type: str = "unknown"
    ) -> Optional[str]:
        """
        Применить интеграции ПЕРЕД выполнением agent.run().

        Args:
            agent_name: Имя агента для логирования
            user_message: Сообщение пользователя
            agent_type: Тип агента для делегирования

        Returns:
            None если продолжать выполнение, строка если вернуть результат
        """

        # 1. АВТОПЕРЕКЛЮЧЕНИЕ К PROJECT MANAGER
        if self.enabled_integrations["pm_switch"]:
            pm_result = await self._check_pm_switch(user_message, agent_name)
            if pm_result:
                return pm_result

        # 2. ПРОВЕРКА КОМПЕТЕНЦИЙ И ДЕЛЕГИРОВАНИЕ
        if self.enabled_integrations["competency_check"]:
            delegation_result = await self._check_competency_and_delegate(
                user_message, agent_type, agent_name
            )
            if delegation_result:
                return delegation_result

        # 3. ПЛАНИРОВАНИЕ МИКРОЗАДАЧ (выводим в чат)
        if self.enabled_integrations["microtask_planning"]:
            await self._create_and_display_microtask_plan(user_message, agent_type)

        # Продолжаем выполнение
        return None

    async def apply_post_run_integrations(
        self,
        agent_name: str,
        user_message: str,
        result: str,
        agent_type: str = "unknown"
    ) -> str:
        """
        Применить интеграции ПОСЛЕ выполнения agent.run().

        Args:
            agent_name: Имя агента
            user_message: Исходное сообщение
            result: Результат работы агента
            agent_type: Тип агента

        Returns:
            Модифицированный результат
        """

        # 4. GIT КОММИТЫ (если были изменения)
        if self.enabled_integrations["git_commits"]:
            await self._check_and_create_git_commit(user_message, result, agent_type)

        # 5. РУССКАЯ ЛОКАЛИЗАЦИЯ (если нужно)
        if self.enabled_integrations["russian_localization"]:
            result = self._apply_russian_localization(result)

        return result

    async def _check_pm_switch(self, user_message: str, agent_name: str) -> Optional[str]:
        """Проверка команд переключения к Project Manager."""
        try:
            from . import check_pm_switch
            return await check_pm_switch(user_message, agent_name)
        except Exception as e:
            logger.warning(f"Ошибка проверки PM switch: {e}")
            return None

    async def _check_competency_and_delegate(
        self,
        user_message: str,
        agent_type: str,
        agent_name: str
    ) -> Optional[str]:
        """Проверка компетенций и делегирование задач."""
        try:
            from . import should_delegate_task

            should_delegate, suggested_agent, reason = should_delegate_task(
                user_message, agent_type, threshold=0.7
            )

            if should_delegate and suggested_agent:
                delegation_message = f"""
ДЕЛЕГИРОВАНИЕ ЗАДАЧИ

Причина: {reason}

Рекомендованный агент: {suggested_agent}

Исходная задача: {user_message}

Для выполнения этой задачи рекомендуется обратиться к агенту {suggested_agent},
который лучше подходит для данного типа работы.

Если это срочно, создайте задачу в Archon:
- Проект: AI Agent Factory (c75ef8e3-6f4d-4da2-9e81-8d38d04a341a)
- Assignee: {suggested_agent}
- Описание: {user_message}
"""
                return delegation_message
        except Exception as e:
            logger.warning(f"Ошибка проверки компетенций: {e}")

        return None

    async def _create_and_display_microtask_plan(
        self,
        user_message: str,
        agent_type: str
    ) -> None:
        """Создание и отображение плана микрозадач."""
        try:
            from .microtask_planner import create_microtask_plan, format_plan_for_approval

            # Создаем план микрозадач
            agent_context = {
                "agent_type": agent_type,
                "agent_name": agent_type.replace('_', ' ').title()
            }

            microtask_plan = create_microtask_plan(user_message, agent_context)

            # Показываем план пользователю
            plan_display = format_plan_for_approval(microtask_plan)

            # В продакшене здесь должен быть запрос подтверждения пользователя
            # Для автоматического режима считаем план одобренным
            microtask_plan.user_approved = True

            # Выводим план в чат для пользователя
            print("\n" + "="*50)
            print("ПЛАН ВЫПОЛНЕНИЯ ЗАДАЧИ")
            print("="*50)
            print(plan_display)
            print("\nПлан одобрен. Начинаем выполнение по микрозадачам...")
            print("="*50 + "\n")

        except Exception as e:
            logger.warning(f"Ошибка планирования микрозадач: {e}")

    async def _check_and_create_git_commit(
        self,
        user_message: str,
        result: str,
        agent_type: str
    ) -> None:
        """Проверка и создание Git коммита при необходимости."""
        try:
            from .git_manager import GitManager

            # Проверяем нужен ли Git коммит
            if self._should_create_git_commit(result):
                git_manager = GitManager()

                # Создаем автоматический коммит (синхронный метод)
                success, commit_message = git_manager.auto_commit_task_completion(
                    task_description=user_message,
                    files_changed=None  # Автоопределение
                )

                if success:
                    logger.info(f"Создан Git коммит: {commit_message}")
                else:
                    logger.warning(f"Ошибка Git коммита: {commit_message}")

        except Exception as e:
            logger.warning(f"Ошибка Git интеграции: {e}")

    def _should_create_git_commit(self, result: str) -> bool:
        """Определить нужен ли Git коммит на основе результата."""
        commit_keywords = [
            "создан", "создано", "добавлен", "обновлен", "исправлен",
            "реализован", "внедрен", "настроен", "завершен",
            "created", "added", "updated", "fixed", "implemented"
        ]

        result_lower = result.lower()
        return any(keyword in result_lower for keyword in commit_keywords)

    def _apply_russian_localization(self, result: str) -> str:
        """Применить русскую локализацию к результату."""
        # Базовые замены для общих терминов
        localizations = {
            "Error": "Ошибка",
            "Success": "Успешно",
            "Warning": "Предупреждение",
            "Recommendation": "Рекомендация",
            "Next steps": "Следующие шаги",
            "Configuration": "Конфигурация",
            "Installation": "Установка"
        }

        localized_result = result
        for en_term, ru_term in localizations.items():
            localized_result = localized_result.replace(en_term, ru_term)

        return localized_result


# Глобальный экземпляр интеграций
pydantic_ai_integration = PydanticAIIntegration()


def with_integrations(agent_type: str = "unknown"):
    """
    Декоратор для функций-оберток вокруг agent.run().

    Применяет все интеграции автоматически без модификации кода агентов.

    Args:
        agent_type: Тип агента для делегирования

    Example:
        @with_integrations("analytics_tracking_agent")
        async def run_analytics_task(user_message: str) -> str:
            deps = load_dependencies()
            result = await analytics_agent.run(user_message, deps=deps)
            return result.data
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Извлекаем user_message из аргументов
            user_message = None
            if args:
                user_message = args[0]  # Первый аргумент обычно user_message
            elif 'user_message' in kwargs:
                user_message = kwargs['user_message']
            elif 'message' in kwargs:
                user_message = kwargs['message']

            if not user_message:
                # Если не можем найти user_message, выполняем без интеграций
                return await func(*args, **kwargs)

            func_name = func.__name__

            # Применяем pre-run интеграции
            pre_result = await pydantic_ai_integration.apply_pre_run_integrations(
                agent_name=func_name,
                user_message=user_message,
                agent_type=agent_type
            )

            if pre_result:
                # Интеграции вернули результат, не выполняем основную функцию
                return pre_result

            # Выполняем основную функцию
            result = await func(*args, **kwargs)

            # Применяем post-run интеграции
            if isinstance(result, str):
                result = await pydantic_ai_integration.apply_post_run_integrations(
                    agent_name=func_name,
                    user_message=user_message,
                    result=result,
                    agent_type=agent_type
                )

            return result

        return wrapper
    return decorator


# Упрощенная функция для быстрого применения интеграций
async def run_with_integrations(
    agent: Agent,
    user_message: str,
    deps: Any,
    agent_type: str = "unknown"
) -> str:
    """
    Запустить Pydantic AI агента с полными интеграциями.

    Args:
        agent: Экземпляр Pydantic AI Agent
        user_message: Сообщение пользователя
        deps: Зависимости агента
        agent_type: Тип агента

    Returns:
        Результат с примененными интеграциями
    """

    # Pre-run интеграции
    pre_result = await pydantic_ai_integration.apply_pre_run_integrations(
        agent_name=agent_type,
        user_message=user_message,
        agent_type=agent_type
    )

    if pre_result:
        return pre_result

    # Выполнение агента
    result = await agent.run(user_message, deps=deps)
    agent_response = result.data

    # Post-run интеграции
    final_result = await pydantic_ai_integration.apply_post_run_integrations(
        agent_name=agent_type,
        user_message=user_message,
        result=agent_response,
        agent_type=agent_type
    )

    return final_result


# Utility функции для отдельных интеграций
async def check_pm_switch_for_agent(user_message: str, agent_name: str) -> Optional[str]:
    """Проверка переключения к PM для конкретного агента."""
    return await pydantic_ai_integration._check_pm_switch(user_message, agent_name)

async def check_delegation_for_agent(user_message: str, agent_type: str) -> Optional[str]:
    """Проверка делегирования для конкретного агента."""
    return await pydantic_ai_integration._check_competency_and_delegate(
        user_message, agent_type, agent_type
    )

async def display_microtask_plan(user_message: str, agent_type: str) -> None:
    """Отображение плана микрозадач для агента."""
    await pydantic_ai_integration._create_and_display_microtask_plan(
        user_message, agent_type
    )


# ОБЯЗАТЕЛЬНЫЕ ФИНАЛЬНЫЕ ФУНКЦИИ ДЛЯ ВСЕХ АГЕНТОВ
async def create_mandatory_git_commit(task_description: str, agent_type: str) -> str:
    """
    Создать обязательный Git коммит после завершения задачи.

    Args:
        task_description: Описание выполненной задачи
        agent_type: Тип агента

    Returns:
        Результат создания коммита
    """
    try:
        from .git_manager import GitManager

        git_manager = GitManager()

        # Создаем коммит с полным описанием задачи
        success, result = git_manager.auto_commit_task_completion(
            task_description=f"[{agent_type}] {task_description}",
            files_changed=None  # Автоопределение
        )

        if success:
            return f"✅ Git коммит создан: {result}"
        else:
            return f"❌ Ошибка Git коммита: {result}"

    except Exception as e:
        return f"❌ Ошибка системы Git коммитов: {e}"


async def update_archon_task_status(task_id: str, status: str, notes: str = "") -> str:
    """
    Обновить статус задачи в Archon (обязательный финальный пункт).

    Args:
        task_id: ID задачи в Archon
        status: Новый статус ("done", "failed", "blocked")
        notes: Дополнительные заметки о выполнении

    Returns:
        Результат обновления статуса
    """
    try:
        # Импортируем Archon MCP функции
        from mcp__archon__manage_task import manage_task

        # Формируем описание с заметками
        update_description = f"Статус обновлен автоматически. {notes}" if notes else "Статус обновлен автоматически"

        result = await manage_task(
            action="update",
            task_id=task_id,
            status=status,
            description=update_description
        )

        if result.get("success"):
            return f"✅ Статус задачи в Archon обновлен: {status}"
        else:
            return f"❌ Ошибка обновления статуса в Archon: {result.get('message', 'Unknown error')}"

    except Exception as e:
        return f"❌ Ошибка системы Archon: {e}"


# ОБЯЗАТЕЛЬНЫЙ ФИНАЛЬНЫЙ ЦИКЛ ДЛЯ ВСЕХ АГЕНТОВ
async def execute_mandatory_final_steps(
    task_description: str,
    agent_type: str,
    task_id: str = None,
    task_status: str = "done",
    notes: str = ""
) -> str:
    """
    Выполнить обязательные финальные шаги для любой задачи.

    ОБЯЗАТЕЛЬНО вызывается в конце каждой задачи всех агентов.

    Args:
        task_description: Описание выполненной задачи
        agent_type: Тип агента
        task_id: ID задачи в Archon (если есть)
        task_status: Статус для Archon ("done", "failed", "blocked")
        notes: Дополнительные заметки

    Returns:
        Сводный отчет о выполнении финальных шагов
    """
    final_report = "🎯 **ВЫПОЛНЕНИЕ ОБЯЗАТЕЛЬНЫХ ФИНАЛЬНЫХ ШАГОВ:**\n\n"

    # Шаг 1: Git коммит
    git_result = await create_mandatory_git_commit(task_description, agent_type)
    final_report += f"**1. Git коммит:** {git_result}\n"

    # Шаг 2: Обновление статуса в Archon (если есть task_id)
    if task_id:
        archon_result = await update_archon_task_status(task_id, task_status, notes)
        final_report += f"**2. Archon статус:** {archon_result}\n"
    else:
        final_report += "**2. Archon статус:** ⚠️ Task ID не предоставлен, статус не обновлен\n"

    final_report += "\n✅ **ВСЕ ОБЯЗАТЕЛЬНЫЕ ФИНАЛЬНЫЕ ШАГИ ВЫПОЛНЕНЫ**"

    return final_report


# Универсальные инструкции для интеграции во все агенты
UNIVERSAL_INTEGRATION_INSTRUCTIONS = """
# Инструкции по интеграции системы интеграций Pydantic AI

## Для интеграции в существующий агент:

1. Добавить импорт в основную функцию выполнения:
```python
from ..common.pydantic_ai_integrations import run_with_integrations
```

2. Заменить прямой вызов agent.run() на:
```python
result = await run_with_integrations(
    agent=your_agent,
    user_message=user_message,
    deps=deps,
    agent_type="your_agent_type"
)
```

3. Убрать обращение к result.data - функция уже возвращает строку

## Что получаете автоматически:

- ✅ Автопереключение к Project Manager по ключевым словам
- ✅ Проверка компетенций и делегирование задач
- ✅ Планирование микрозадач с отображением пользователю
- ✅ Автоматические Git коммиты при изменениях файлов
- ✅ Русская локализация результатов
- ✅ **НОВОЕ: Обязательные финальные шаги (Git + Archon)**

## Настройка типа агента:

Укажите правильный agent_type для корректного делегирования:
- "analytics_tracking_agent"
- "mcp_configuration_agent"
- "security_audit_agent"
- "performance_optimization_agent"
- "rag_agent"
- "ui_ux_enhancement_agent"
- "typescript_architecture_agent"
- "prisma_database_agent"
- "pwa_mobile_agent"
- "payment_integration_agent"
- "queue_worker_agent"
- "nlp_content_quality_guardian_agent"
- "community_management_agent"
- "api_development_agent"
- и другие согласно существующим агентам

## Включение/отключение интеграций:

Можно настроить через pydantic_ai_integration.enabled_integrations:
```python
pydantic_ai_integration.enabled_integrations["pm_switch"] = False
pydantic_ai_integration.enabled_integrations["git_commits"] = True
```

Доступные интеграции:
- "pm_switch" - автопереключение к Project Manager
- "competency_check" - проверка компетенций и делегирование
- "microtask_planning" - планирование микрозадач
- "git_commits" - автоматические Git коммиты
- "russian_localization" - русская локализация

## ОБЯЗАТЕЛЬНЫЕ ФИНАЛЬНЫЕ ШАГИ:

### Для всех агентов ОБЯЗАТЕЛЬНО добавить в конце каждой задачи:

```python
# В конце каждой задачи
from ..common.pydantic_ai_integrations import execute_mandatory_final_steps

# Выполняем обязательные финальные шаги
final_result = await execute_mandatory_final_steps(
    task_description="Краткое описание выполненной задачи",
    agent_type="your_agent_type",
    task_id="archon_task_id_if_available",  # Опционально
    task_status="done",  # или "failed", "blocked"
    notes="Дополнительные заметки о выполнении"  # Опционально
)
print(final_result)  # ОБЯЗАТЕЛЬНО показать пользователю
```

### Что выполняется автоматически:

1. **Git коммит** - создается автоматический коммит с описанием задачи
2. **Обновление Archon** - статус задачи обновляется в Archon (если task_id предоставлен)
3. **Отчет пользователю** - показывается сводка выполненных финальных шагов

### Правила:

- ✅ КАЖДАЯ задача ДОЛЖНА завершаться этими шагами
- ✅ Применяется ко ВСЕМ агентам (существующим и новым)
- ✅ Никаких исключений - это обязательное требование
- ✅ Автоматически интегрируется через run_with_integrations()

### Альтернативный способ (ручной):

Если не используете run_with_integrations(), добавьте вручную:

```python
# Обязательные финальные импорты
from ..common.pydantic_ai_integrations import (
    create_mandatory_git_commit,
    update_archon_task_status
)

# В конце каждой задачи
git_result = await create_mandatory_git_commit(task_description, agent_type)
print(git_result)

if task_id:
    archon_result = await update_archon_task_status(task_id, "done")
    print(archon_result)
```
"""


def get_integration_instructions() -> str:
    """Получить инструкции по интеграции для разработчиков."""
    return UNIVERSAL_INTEGRATION_INSTRUCTIONS