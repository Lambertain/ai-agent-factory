#!/usr/bin/env python3
"""
Archon Blueprint Architect Agent - главный архитектор команды Archon.

Специализация: проектирование архитектуры, дизайн системы, структурные решения.
"""

from pydantic_ai import Agent, RunContext
from .dependencies import BlueprintArchitectDependencies
from ..common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations,
    register_agent
)
from .tools import (
    design_architecture,
    create_system_blueprint,
    analyze_architectural_patterns,
    validate_architecture
)
from .prompts import get_system_prompt
from .settings import get_llm_model

# Создание агента с универсальными интеграциями
blueprint_architect_agent = create_universal_pydantic_agent(
    model=get_llm_model(),
    deps_type=BlueprintArchitectDependencies,
    system_prompt=get_system_prompt(),
    agent_type="archon_blueprint_architect",
    knowledge_tags=["architecture", "design-patterns", "blueprints", "agent-knowledge"],
    knowledge_domain="architecture.archon.local",
    with_collective_tools=True,
    with_knowledge_tool=True
)

# Регистрация специализированных инструментов
blueprint_architect_agent.tool(design_architecture)
blueprint_architect_agent.tool(create_system_blueprint)
blueprint_architect_agent.tool(analyze_architectural_patterns)
blueprint_architect_agent.tool(validate_architecture)

# Регистрация агента в глобальном реестре
register_agent("archon_blueprint_architect", blueprint_architect_agent, agent_type="archon_blueprint_architect")


@with_integrations(agent_type="archon_blueprint_architect")
async def run_blueprint_architect(
    query: str,
    project_id: str = None,
    dependencies: BlueprintArchitectDependencies = None
) -> str:
    """
    Запустить Blueprint Architect агент для архитектурного планирования.

    АВТОМАТИЧЕСКИЕ ИНТЕГРАЦИИ:
    - Переключение на Project Manager для приоритизации
    - Контроль компетенций и делегирование задач
    - Планирование микрозадач
    - Автоматические Git коммиты
    - Русская локализация сообщений
    - Расширенная система рефлексии

    Args:
        query: Запрос для архитектурного проектирования
        project_id: ID проекта в Archon
        dependencies: Зависимости агента

    Returns:
        Результат архитектурного проектирования с применёнными интеграциями
    """
    if not dependencies:
        dependencies = BlueprintArchitectDependencies(
            project_id=project_id or "default",
            archon_project_id=project_id,
            agent_name="archon_blueprint_architect"
        )

    async with blueprint_architect_agent:
        result = await blueprint_architect_agent.run(query, deps=dependencies)
        return result.data


if __name__ == "__main__":
    import asyncio

    async def main():
        result = await run_blueprint_architect(
            "Спроектируй архитектуру микросервисной системы управления задачами"
        )
        print(result)

    asyncio.run(main())