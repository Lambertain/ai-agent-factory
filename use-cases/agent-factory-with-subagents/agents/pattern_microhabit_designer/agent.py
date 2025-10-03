"""
Pattern Microhabit Designer Agent

Специализированный агент для создания микро-привычек и habit chains
в рамках системы PatternShift.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from pydantic_ai import Agent, RunContext

from .settings import get_llm_model
from .dependencies import PatternMicrohabitDesignerDependencies
from .prompts import get_system_prompt
from .models import (
    Microhabit,
    HabitChain,
    MicrohabitDesignRequest,
    MicrohabitDesignResponse,
    BehaviorChangeGoal,
    MicrohabitModule
)
from .tools import (
    design_microhabit,
    create_habit_chain,
    identify_triggers_rewards,
    generate_module_variants,
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
        deps_type=PatternMicrohabitDesignerDependencies,
        system_prompt=get_system_prompt,
        agent_type="pattern_microhabit_designer",
        knowledge_tags=["pattern-microhabit", "behavior-design", "habits", "agent-knowledge", "patternshift"],
        knowledge_domain=None,  # Не требует специфичного домена
        with_collective_tools=True,
        with_knowledge_tool=True
    )
    logger.info("Pattern Microhabit Designer Agent создан с универсальными декораторами")
else:
    # Fallback для старой архитектуры
    agent = Agent(
        model=get_llm_model(),
        deps_type=PatternMicrohabitDesignerDependencies,
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

    logger.info("Pattern Microhabit Designer Agent создан с fallback архитектурой")

# === РЕГИСТРАЦИЯ СПЕЦИАЛИЗИРОВАННЫХ ИНСТРУМЕНТОВ ДИЗАЙНА ПРИВЫЧЕК ===

# Регистрируем все инструменты из tools.py
agent.tool(design_microhabit)
agent.tool(create_habit_chain)
agent.tool(identify_triggers_rewards)
agent.tool(generate_module_variants)

# === ОСНОВНАЯ ФУНКЦИЯ АГЕНТА ===

async def run_pattern_microhabit_designer(
    user_message: str,
    api_key: str,
    patternshift_project_path: str = "",
    **kwargs
) -> str:
    """
    Запустить Pattern Microhabit Designer Agent

    Args:
        user_message: Сообщение от пользователя с запросом на дизайн привычки
        api_key: API ключ для LLM
        patternshift_project_path: Путь к проекту PatternShift
        **kwargs: Дополнительные параметры для зависимостей

    Returns:
        str: Ответ агента с спроектированной микро-привычкой

    Example:
        >>> result = await run_pattern_microhabit_designer(
        ...     "Создай микро-привычку для утренней медитации",
        ...     api_key="your_api_key"
        ... )
        >>> print(result)
    """

    # Создаем зависимости
    deps = PatternMicrohabitDesignerDependencies(
        api_key=api_key,
        patternshift_project_path=patternshift_project_path,
        **kwargs
    )

    # Запускаем агента
    try:
        result = await agent.run(user_message, deps=deps)
        return result.data
    except Exception as e:
        logger.error(f"Ошибка при выполнении Pattern Microhabit Designer: {e}")
        return f"Ошибка: {e}"


# === ЭКСПОРТ ===
__all__ = [
    "agent",
    "run_pattern_microhabit_designer"
]
