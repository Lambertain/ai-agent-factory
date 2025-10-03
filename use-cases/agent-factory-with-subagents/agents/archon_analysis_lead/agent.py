#!/usr/bin/env python3
"""
Archon Analysis Lead Agent - главный аналитик команды Archon.

Специализация: анализ требований, декомпозиция задач, исследование и планирование.
"""

from pydantic_ai import Agent, RunContext
from .dependencies import AnalysisLeadDependencies
from ..common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations,
    register_agent
)
from .tools import (
    analyze_requirements,
    decompose_task,
    research_solutions,
    create_analysis_report
)
from .prompts import get_system_prompt
from .settings import get_llm_model

# Создание агента с универсальными интеграциями
analysis_lead_agent = create_universal_pydantic_agent(
    model=get_llm_model(),
    deps_type=AnalysisLeadDependencies,
    system_prompt=get_system_prompt(),
    agent_type="archon_analysis_lead",
    knowledge_tags=["analysis", "requirements", "planning", "agent-knowledge"],
    knowledge_domain="analysis.archon.local",
    with_collective_tools=True,
    with_knowledge_tool=True
)

# Регистрация специализированных инструментов
analysis_lead_agent.tool(analyze_requirements)
analysis_lead_agent.tool(decompose_task)
analysis_lead_agent.tool(research_solutions)
analysis_lead_agent.tool(create_analysis_report)

# Регистрация агента в глобальном реестре
register_agent("archon_analysis_lead", analysis_lead_agent, agent_type="archon_analysis_lead")


@with_integrations(agent_type="archon_analysis_lead")
async def run_analysis_lead(
    query: str,
    project_id: str = None,
    dependencies: AnalysisLeadDependencies = None
) -> str:
    """
    Запустить Analysis Lead агент для анализа требований.

    АВТОМАТИЧЕСКИЕ ИНТЕГРАЦИИ:
    - Переключение на Project Manager для приоритизации
    - Контроль компетенций и делегирование задач
    - Планирование микрозадач
    - Автоматические Git коммиты
    - Русская локализация сообщений
    - Расширенная система рефлексии

    Args:
        query: Запрос для анализа
        project_id: ID проекта в Archon
        dependencies: Зависимости агента

    Returns:
        Результат анализа с применёнными интеграциями
    """
    if not dependencies:
        dependencies = AnalysisLeadDependencies(
            project_id=project_id or "default",
            archon_project_id=project_id,
            agent_name="archon_analysis_lead"
        )

    async with analysis_lead_agent:
        result = await analysis_lead_agent.run(query, deps=dependencies)
        return result.data


if __name__ == "__main__":
    import asyncio

    async def main():
        result = await run_analysis_lead(
            "Проанализируй требования для создания системы управления задачами"
        )
        print(result)

    asyncio.run(main())