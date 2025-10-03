"""
Pattern Exercise Architect Agent

Специализированный агент для создания трансформационных упражнений
в рамках системы PatternShift.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from pydantic_ai import Agent, RunContext

from .settings import get_llm_model
from .dependencies import PatternExerciseArchitectDependencies
from .prompts import get_system_prompt
from .models import (
    TransformationalExercise,
    ExerciseStep,
    CompletionCriteria,
    ExerciseVariant,
    ExerciseSequence,
    ExerciseModule
)
from .tools import (
    design_transformational_exercise,
    create_exercise_variants,
    design_self_check_criteria,
    adapt_nlp_technique_to_exercise,
    search_agent_knowledge
)

# Попытка импорта универсальных декораторов
try:
    from ..common.pydantic_ai_decorators import (
        create_universal_pydantic_agent,
        with_integrations,
        register_agent
    )
    HAS_DECORATORS = True
except ImportError:
    HAS_DECORATORS = False

# Импорт обязательных инструментов коллективной работы
try:
    from ..common.collective_work_tools import (
        break_down_to_microtasks,
        report_microtask_progress,
        reflect_and_improve,
        check_delegation_need,
        delegate_task_to_agent
    )
    HAS_COLLECTIVE_TOOLS = True
except ImportError:
    HAS_COLLECTIVE_TOOLS = False

logger = logging.getLogger(__name__)

# === СОЗДАНИЕ АГЕНТА С ПОЛНОЙ ИНТЕГРАЦИЕЙ ===

if HAS_DECORATORS:
    # Используем новую универсальную архитектуру с автоматическими интеграциями
    agent = create_universal_pydantic_agent(
        model=get_llm_model(),
        deps_type=PatternExerciseArchitectDependencies,
        system_prompt=get_system_prompt,
        agent_type="pattern_exercise_architect",
        knowledge_tags=["pattern-exercise", "transformational-exercises", "nlp-techniques", "embodiment", "agent-knowledge", "patternshift"],
        knowledge_domain=None,  # Не требует специфичного домена
        with_collective_tools=True,
        with_knowledge_tool=True
    )
    logger.info("Pattern Exercise Architect Agent создан с универсальными декораторами")
else:
    # Fallback для старой архитектуры
    agent = Agent(
        model=get_llm_model(),
        deps_type=PatternExerciseArchitectDependencies,
        system_prompt=get_system_prompt
    )

    # Добавляем инструменты вручную
    agent.tool(search_agent_knowledge)

    # Добавляем обязательные инструменты коллективной работы вручную
    if HAS_COLLECTIVE_TOOLS:
        agent.tool(break_down_to_microtasks)
        agent.tool(report_microtask_progress)
        agent.tool(reflect_and_improve)
        agent.tool(check_delegation_need)
        agent.tool(delegate_task_to_agent)
        logger.info("Добавлены обязательные инструменты коллективной работы")

    logger.info("Pattern Exercise Architect Agent создан с fallback архитектурой")

# === РЕГИСТРАЦИЯ СПЕЦИАЛИЗИРОВАННЫХ ИНСТРУМЕНТОВ ДИЗАЙНА УПРАЖНЕНИЙ ===

# Регистрируем все инструменты из tools.py
agent.tool(design_transformational_exercise)
agent.tool(create_exercise_variants)
agent.tool(design_self_check_criteria)
agent.tool(adapt_nlp_technique_to_exercise)

# === ОСНОВНАЯ ФУНКЦИЯ АГЕНТА ===

async def run_pattern_exercise_architect(
    user_message: str,
    api_key: str,
    patternshift_project_path: str = "",
    **kwargs
) -> str:
    """
    Запустить Pattern Exercise Architect Agent

    Args:
        user_message: Сообщение от пользователя с запросом на дизайн упражнения
        api_key: API ключ для LLM
        patternshift_project_path: Путь к проекту PatternShift
        **kwargs: Дополнительные параметры для зависимостей

    Returns:
        str: Ответ агента со спроектированным упражнением

    Example:
        >>> result = await run_pattern_exercise_architect(
        ...     "Создай упражнение для интеграции техники рефрейминга",
        ...     api_key="your_api_key"
        ... )
        >>> print(result)
    """

    # Создаем зависимости
    deps = PatternExerciseArchitectDependencies(
        api_key=api_key,
        patternshift_project_path=patternshift_project_path,
        **kwargs
    )

    # Запускаем агента
    try:
        result = await agent.run(user_message, deps=deps)
        return result.data
    except Exception as e:
        logger.error(f"Ошибка при выполнении Pattern Exercise Architect: {e}")
        return f"Ошибка: {e}"


# === ЭКСПОРТ ===
__all__ = [
    "agent",
    "run_pattern_exercise_architect"
]
