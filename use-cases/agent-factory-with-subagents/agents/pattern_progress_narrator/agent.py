"""
Pattern Progress Narrator Agent

Специализированный агент для создания нарративов прогресса и трансформации
в рамках системы PatternShift.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from pydantic_ai import Agent, RunContext

from .settings import get_llm_model
from .dependencies import PatternProgressNarratorDependencies
from .prompts import get_system_prompt
from .models import (
    ProgressNarrative,
    NarrativeType,
    EmotionalTone,
    ProgressMetric,
    UserMilestone,
    TransformationJourneyMap
)
from .tools import (
    create_progress_narrative,
    reframe_challenge,
    generate_momentum_message,
    create_anticipation_builder,
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
    agent = create_universal_pydantic_agent(
        model=get_llm_model(),
        deps_type=PatternProgressNarratorDependencies,
        system_prompt=get_system_prompt,
        agent_type="pattern_progress_narrator",
        knowledge_tags=["pattern-progress-narrator", "storytelling", "motivation", "hero-journey", "agent-knowledge", "patternshift"],
        knowledge_domain=None,
        with_collective_tools=True,
        with_knowledge_tool=True
    )
    logger.info("Pattern Progress Narrator Agent создан с универсальными декораторами")
else:
    agent = Agent(
        model=get_llm_model(),
        deps_type=PatternProgressNarratorDependencies,
        system_prompt=get_system_prompt
    )

    agent.tool(search_agent_knowledge)

    if HAS_COLLECTIVE_TOOLS:
        agent.tool(break_down_to_microtasks)
        agent.tool(report_microtask_progress)
        agent.tool(reflect_and_improve)
        agent.tool(check_delegation_need)
        agent.tool(delegate_task_to_agent)
        logger.info("Добавлены обязательные инструменты коллективной работы")

    logger.info("Pattern Progress Narrator Agent создан с fallback архитектурой")

# === РЕГИСТРАЦИЯ СПЕЦИАЛИЗИРОВАННЫХ ИНСТРУМЕНТОВ ===

agent.tool(create_progress_narrative)
agent.tool(reframe_challenge)
agent.tool(generate_momentum_message)
agent.tool(create_anticipation_builder)

# === ОСНОВНАЯ ФУНКЦИЯ АГЕНТА ===

async def run_pattern_progress_narrator(
    user_message: str,
    api_key: str,
    patternshift_project_path: str = "",
    **kwargs
) -> str:
    """
    Запустить Pattern Progress Narrator Agent

    Args:
        user_message: Сообщение от пользователя с запросом на нарратив прогресса
        api_key: API ключ для LLM
        patternshift_project_path: Путь к проекту PatternShift
        **kwargs: Дополнительные параметры для зависимостей

    Returns:
        str: Ответ агента с созданным нарративом прогресса
    """

    deps = PatternProgressNarratorDependencies(
        api_key=api_key,
        patternshift_project_path=patternshift_project_path,
        **kwargs
    )

    try:
        result = await agent.run(user_message, deps=deps)
        return result.data
    except Exception as e:
        logger.error(f"Ошибка при выполнении Pattern Progress Narrator: {e}")
        return f"Ошибка: {e}"


__all__ = [
    "agent",
    "run_pattern_progress_narrator"
]
