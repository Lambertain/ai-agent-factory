# -*- coding: utf-8 -*-
"""
Pattern Orchestrator Agent - главный модуль агента.

Полноценный Pydantic AI агент с интеграцией универсальных декораторов
и специализированными инструментами для оркестрации всех 17 Pattern агентов.
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
from .dependencies import PatternOrchestratorDependencies
from .prompts import get_system_prompt
from .tools import (
    orchestrate_agents,
    manage_degradation_levels,
    coordinate_workflow,
    delegate_to_pattern_agent,
    manage_module_pipeline,
    validate_integration,
    compile_engine_spec,
    emergency_mode_handler,
    delegate_to_universal_agents
)
from .workflow import OrchestratorWorkflow, DegradationWorkflow

logger = logging.getLogger(__name__)


def create_pattern_orchestrator_agent(
    deps: Optional[PatternOrchestratorDependencies] = None
) -> Agent[PatternOrchestratorDependencies, str]:
    """
    Создать Pattern Orchestrator Agent с полными интеграциями.

    Args:
        deps: Зависимости агента (опционально)

    Returns:
        Настроенный Pydantic AI агент с универсальными интеграциями
    """
    settings = load_settings()

    # Создаем агента с универсальными декораторами и интеграциями
    agent = create_universal_pydantic_agent(
        model=get_llm_model(),
        deps_type=PatternOrchestratorDependencies,
        system_prompt=get_system_prompt(deps),
        agent_type="pattern_orchestrator",
        knowledge_tags=settings.knowledge_tags,
        knowledge_domain=settings.knowledge_domain,
        with_collective_tools=True,  # Добавляет break_down_to_microtasks, reflect_and_improve
        with_knowledge_tool=True     # Добавляет search_agent_knowledge для RAG
    )

    # Добавляем специализированные инструменты Pattern Orchestrator
    agent.tool(orchestrate_agents)
    agent.tool(manage_degradation_levels)
    agent.tool(coordinate_workflow)
    agent.tool(delegate_to_pattern_agent)
    agent.tool(manage_module_pipeline)
    agent.tool(validate_integration)
    agent.tool(compile_engine_spec)
    agent.tool(emergency_mode_handler)
    agent.tool(delegate_to_universal_agents)

    logger.info("Pattern Orchestrator Agent создан с полными интеграциями")

    return agent


# Глобальный экземпляр агента
pattern_orchestrator_agent: Optional[Agent[PatternOrchestratorDependencies, str]] = None


def get_pattern_orchestrator_agent(
    deps: Optional[PatternOrchestratorDependencies] = None
) -> Agent[PatternOrchestratorDependencies, str]:
    """
    Получить или создать экземпляр Pattern Orchestrator Agent.

    Args:
        deps: Зависимости агента

    Returns:
        Экземпляр агента
    """
    global pattern_orchestrator_agent

    if pattern_orchestrator_agent is None or deps is not None:
        if deps is None:
            settings = load_settings()
            deps = PatternOrchestratorDependencies(
                llm_api_key=settings.llm_api_key,
                project_path=settings.patternshift_project_path
            )

        pattern_orchestrator_agent = create_pattern_orchestrator_agent(deps)

        # Регистрируем в глобальном реестре агентов
        register_agent(
            "pattern_orchestrator",
            pattern_orchestrator_agent,
            agent_type="pattern_orchestrator",
            knowledge_tags=settings.knowledge_tags,
            knowledge_domain=settings.knowledge_domain
        )

    return pattern_orchestrator_agent


@with_integrations(agent_type="pattern_orchestrator")
async def run_pattern_orchestrator_agent(
    user_message: str,
    deps: Optional[PatternOrchestratorDependencies] = None
) -> str:
    """
    Запустить Pattern Orchestrator Agent с полными интеграциями.

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
    agent = get_pattern_orchestrator_agent(deps)

    # Запускаем агента
    result = await agent.run(user_message, deps=deps)

    return result.data


async def run_full_orchestration_workflow(
    deps: Optional[PatternOrchestratorDependencies] = None
) -> dict:
    """
    Запустить полный orchestration workflow.

    Выполняет все 5 фаз PatternShift:
    - Phase 1: Content Creation (Days 1-14)
    - Phase 2: Integration & Polish (Days 15-21)
    - Phase 3: Safety & Science (Days 22-24)
    - Phase 4: Multiplier Adaptation (Days 25-35)
    - Phase 5: Final Assembly (Days 36-42+)
    - Engine Creation (Universal Agents)

    Args:
        deps: Зависимости агента

    Returns:
        Результаты полного workflow
    """
    if deps is None:
        settings = load_settings()
        deps = PatternOrchestratorDependencies(
            llm_api_key=settings.llm_api_key,
            project_path=settings.patternshift_project_path
        )

    # Создаем orchestration workflow
    workflow = OrchestratorWorkflow(deps)

    # Выполняем полный workflow
    results = await workflow.execute_full_workflow()

    # Сохраняем ENGINE_SPEC.json
    engine_spec_path = await workflow.save_engine_spec()

    # Возвращаем результаты
    return {
        "success": True,
        "workflow_results": results,
        "engine_spec_path": engine_spec_path,
        "stats": workflow.get_workflow_stats()
    }


async def apply_content_degradation(
    program_content: dict,
    target_level: str,
    deps: Optional[PatternOrchestratorDependencies] = None
) -> dict:
    """
    Применить деградацию контента с program до target_level.

    Args:
        program_content: Контент полной программы (45 мин)
        target_level: Целевой уровень (phase, day, session, emergency)
        deps: Зависимости агента

    Returns:
        Деградированный контент
    """
    if deps is None:
        settings = load_settings()
        deps = PatternOrchestratorDependencies(
            llm_api_key=settings.llm_api_key,
            project_path=settings.patternshift_project_path
        )

    # Создаем degradation workflow
    degradation_workflow = DegradationWorkflow(deps)

    # Применяем деградацию
    degraded_content = await degradation_workflow.apply_degradation_chain(
        program_content,
        target_level
    )

    return {
        "success": True,
        "degraded_content": degraded_content,
        "original_level": "program",
        "target_level": target_level
    }


# Экспорт основных функций
__all__ = [
    "create_pattern_orchestrator_agent",
    "get_pattern_orchestrator_agent",
    "run_pattern_orchestrator_agent",
    "run_full_orchestration_workflow",
    "apply_content_degradation",
    "PatternOrchestratorDependencies"
]
