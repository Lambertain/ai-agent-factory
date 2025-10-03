#!/usr/bin/env python3
"""
Archon Project Manager Agent - главный координатор команды Archon.

Специализация: управление проектами, координация команды, планирование и контроль выполнения.
"""

from pydantic_ai import Agent, RunContext
from .dependencies import ProjectManagerDependencies
from ..common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations,
    register_agent
)
from .tools import (
    create_project_plan,
    manage_task_priorities,
    coordinate_team_work,
    generate_status_report,
    manage_project_risks,
    schedule_tasks,
    track_progress,
    delegate_task
)
from .prompts import get_system_prompt
from .settings import get_llm_model

# Создание агента с универсальными интеграциями
project_manager_agent = create_universal_pydantic_agent(
    model=get_llm_model(),
    deps_type=ProjectManagerDependencies,
    system_prompt=get_system_prompt(),
    agent_type="archon_project_manager",
    knowledge_tags=["project-management", "agile", "coordination", "agent-knowledge"],
    knowledge_domain="management.archon.local",
    with_collective_tools=True,
    with_knowledge_tool=True
)

# Регистрация специализированных инструментов
project_manager_agent.tool(create_project_plan)
project_manager_agent.tool(manage_task_priorities)
project_manager_agent.tool(coordinate_team_work)
project_manager_agent.tool(generate_status_report)
project_manager_agent.tool(manage_project_risks)
project_manager_agent.tool(schedule_tasks)
project_manager_agent.tool(track_progress)
project_manager_agent.tool(delegate_task)

# Регистрация агента в глобальном реестре
register_agent("archon_project_manager", project_manager_agent, agent_type="archon_project_manager")


@with_integrations(agent_type="archon_project_manager")
async def run_project_manager(
    query: str,
    project_id: str = None,
    dependencies: ProjectManagerDependencies = None
) -> str:
    """
    Запустить Project Manager агент для управления проектом.

    АВТОМАТИЧЕСКИЕ ИНТЕГРАЦИИ:
    - Переключение на Project Manager для приоритизации
    - Контроль компетенций и делегирование задач
    - Планирование микрозадач
    - Автоматические Git коммиты
    - Русская локализация сообщений
    - Расширенная система рефлексии

    Args:
        query: Запрос для управления проектом
        project_id: ID проекта в Archon
        dependencies: Зависимости агента

    Returns:
        Результат управления проектом с применёнными интеграциями
    """
    if not dependencies:
        dependencies = ProjectManagerDependencies(
            project_id=project_id or "default",
            archon_project_id=project_id,
            agent_name="archon_project_manager"
        )

    async with project_manager_agent:
        result = await project_manager_agent.run(query, deps=dependencies)
        return result.data


if __name__ == "__main__":
    import asyncio

    async def main():
        result = await run_project_manager(
            "Создай план проекта для разработки системы управления задачами"
        )
        print(result)

    asyncio.run(main())