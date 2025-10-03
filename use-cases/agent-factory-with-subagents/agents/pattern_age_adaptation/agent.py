# -*- coding: utf-8 -*-
"""
Pattern Age Adaptation Agent - главный модуль агента.

Полноценный Pydantic AI агент с интеграцией универсальных декораторов
и специализированными инструментами для возрастной адаптации контента PatternShift.
"""

import logging
from typing import Optional
from pydantic_ai import Agent

# Импорт универсальных декораторов и инструментов
import sys
from pathlib import Path

AGENT_FACTORY_PATH = Path("D:/Automation/agent-factory/use-cases/agent-factory-with-subagents")
if str(AGENT_FACTORY_PATH) not in sys.path:
    sys.path.insert(0, str(AGENT_FACTORY_PATH))

from agents.common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    register_agent,
    with_integrations
)

# Импорт локальных модулей
from .settings import get_llm_model, load_settings
from .dependencies import PatternAgeAdaptationDependencies
from .prompts import get_system_prompt
from .tools import (
    analyze_age_patterns,
    adapt_for_teens,
    adapt_for_young_adults,
    adapt_for_early_middle_age,
    adapt_for_middle_age,
    adapt_for_seniors,
    validate_developmental_tasks
)
from .workflow import AgeAdaptationWorkflow

logger = logging.getLogger(__name__)


def create_pattern_age_agent(
    deps: Optional[PatternAgeAdaptationDependencies] = None
) -> Agent[PatternAgeAdaptationDependencies, str]:
    """
    Создать Pattern Age Adaptation Agent с полными интеграциями.

    Args:
        deps: Зависимости агента (опционально)

    Returns:
        Настроенный Pydantic AI агент с универсальными интеграциями
    """
    settings = load_settings()

    # Создаем агента с универсальными декораторами и интеграциями
    agent = create_universal_pydantic_agent(
        model=get_llm_model(),
        deps_type=PatternAgeAdaptationDependencies,
        system_prompt=get_system_prompt(deps),
        agent_type="pattern_age_adaptation",
        knowledge_tags=settings.knowledge_tags,
        knowledge_domain=settings.knowledge_domain,
        with_collective_tools=True,  # Добавляет break_down_to_microtasks, reflect_and_improve и т.д.
        with_knowledge_tool=True     # Добавляет search_agent_knowledge для RAG
    )

    # Добавляем специализированные инструменты Pattern Age Agent
    agent.tool(analyze_age_patterns)
    agent.tool(adapt_for_teens)
    agent.tool(adapt_for_young_adults)
    agent.tool(adapt_for_early_middle_age)
    agent.tool(adapt_for_middle_age)
    agent.tool(adapt_for_seniors)
    agent.tool(validate_developmental_tasks)

    logger.info("Pattern Age Adaptation Agent создан с полными интеграциями")

    return agent


# Глобальный экземпляр агента
pattern_age_agent: Optional[Agent[PatternAgeAdaptationDependencies, str]] = None


def get_pattern_age_agent(
    deps: Optional[PatternAgeAdaptationDependencies] = None
) -> Agent[PatternAgeAdaptationDependencies, str]:
    """
    Получить или создать экземпляр Pattern Age Adaptation Agent.

    Args:
        deps: Зависимости агента

    Returns:
        Экземпляр агента
    """
    global pattern_age_agent

    if pattern_age_agent is None or deps is not None:
        if deps is None:
            settings = load_settings()
            deps = PatternAgeAdaptationDependencies(
                llm_api_key=settings.llm_api_key,
                project_path=settings.patternshift_project_path
            )

        pattern_age_agent = create_pattern_age_agent(deps)

        # Регистрируем в глобальном реестре агентов
        register_agent(
            "pattern_age_adaptation",
            pattern_age_agent,
            agent_type="pattern_age_adaptation",
            knowledge_tags=settings.knowledge_tags,
            knowledge_domain=settings.knowledge_domain
        )

    return pattern_age_agent


@with_integrations(agent_type="pattern_age_adaptation")
async def run_pattern_age_agent(
    user_message: str,
    deps: Optional[PatternAgeAdaptationDependencies] = None
) -> str:
    """
    Запустить Pattern Age Adaptation Agent с полными интеграциями.

    Автоматически применяет:
    - PM Switch - автопереключение к Project Manager
    - Competency Check - проверка компетенций и делегирование
    - Microtask Planning - планирование и вывод микрозадач
    - Git Commits - автоматические коммиты
    - Russian Localization - русская локализация

    Args:
        user_message: Сообщение пользователя / задача
        deps: Зависимости агента

    Returns:
        Результат работы агента с примененными интеграциями
    """
    agent = get_pattern_age_agent(deps)

    # Запускаем агента
    result = await agent.run(user_message, deps=deps)

    return result.data


async def run_age_adaptation_workflow(
    modules: list,
    module_type: str,
    deps: Optional[PatternAgeAdaptationDependencies] = None
) -> dict:
    """
    Запустить полный workflow возрастной адаптации модулей.

    Args:
        modules: Список гендерно-адаптированных модулей для адаптации
        module_type: Тип модулей (nlp_technique, hypnosis_script и т.д.)
        deps: Зависимости агента

    Returns:
        Результаты адаптации со статистикой
    """
    if deps is None:
        settings = load_settings()
        deps = PatternAgeAdaptationDependencies(
            llm_api_key=settings.llm_api_key,
            project_path=settings.patternshift_project_path
        )

    # Создаем workflow
    workflow = AgeAdaptationWorkflow(deps)

    # Обрабатываем модули
    adapted_modules = await workflow.process_module_batch(modules, module_type)

    # Сохраняем результаты
    output_path = await workflow.save_adapted_modules(adapted_modules)

    # Возвращаем результаты
    return {
        "success": True,
        "adapted_modules": adapted_modules,
        "output_path": output_path,
        "stats": workflow.get_workflow_stats()
    }


# Экспорт основных функций
__all__ = [
    "create_pattern_age_agent",
    "get_pattern_age_agent",
    "run_pattern_age_agent",
    "run_age_adaptation_workflow",
    "PatternAgeAdaptationDependencies"
]
