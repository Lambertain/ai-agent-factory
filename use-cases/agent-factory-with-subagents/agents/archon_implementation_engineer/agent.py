#!/usr/bin/env python3
"""
Archon Implementation Engineer Agent - главный инженер реализации команды Archon.

Специализация: разработка кода, реализация функций, техническая реализация архитектурных решений.
"""

from pydantic_ai import Agent, RunContext
from .dependencies import ImplementationEngineerDependencies
from ..common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations,
    register_agent
)
from .tools import (
    implement_feature,
    create_code_structure,
    generate_tests,
    optimize_performance,
    validate_code_quality,
    delegate_to_quality_guardian
)
from .prompts import get_system_prompt
from .settings import get_llm_model

# Создание агента с универсальными интеграциями
implementation_engineer_agent = create_universal_pydantic_agent(
    model=get_llm_model(),
    deps_type=ImplementationEngineerDependencies,
    system_prompt=get_system_prompt(),
    agent_type="archon_implementation_engineer",
    knowledge_tags=["implementation", "coding", "best-practices", "agent-knowledge"],
    knowledge_domain="implementation.archon.local",
    with_collective_tools=True,
    with_knowledge_tool=True
)

# Регистрация специализированных инструментов
implementation_engineer_agent.tool(implement_feature)
implementation_engineer_agent.tool(create_code_structure)
implementation_engineer_agent.tool(generate_tests)
implementation_engineer_agent.tool(optimize_performance)
implementation_engineer_agent.tool(validate_code_quality)
implementation_engineer_agent.tool(delegate_to_quality_guardian)

# Регистрация агента в глобальном реестре
register_agent("archon_implementation_engineer", implementation_engineer_agent, agent_type="archon_implementation_engineer")


@with_integrations(agent_type="archon_implementation_engineer")
async def run_implementation_engineer(
    query: str,
    project_id: str = None,
    dependencies: ImplementationEngineerDependencies = None
) -> str:
    """
    Запустить Implementation Engineer агент для реализации функций.

    АВТОМАТИЧЕСКИЕ ИНТЕГРАЦИИ:
    - Переключение на Project Manager для приоритизации
    - Контроль компетенций и делегирование задач
    - Планирование микрозадач
    - Автоматические Git коммиты
    - Русская локализация сообщений
    - Расширенная система рефлексии

    Args:
        query: Запрос для реализации
        project_id: ID проекта в Archon
        dependencies: Зависимости агента

    Returns:
        Результат реализации с применёнными интеграциями
    """
    if not dependencies:
        dependencies = ImplementationEngineerDependencies(
            project_id=project_id or "default",
            archon_project_id=project_id,
            agent_name="archon_implementation_engineer"
        )

    async with implementation_engineer_agent:
        result = await implementation_engineer_agent.run(query, deps=dependencies)
        return result.data


if __name__ == "__main__":
    import asyncio

    async def main():
        result = await run_implementation_engineer(
            "Реализуй REST API для управления пользователями с методами CRUD"
        )
        print(result)

    asyncio.run(main())