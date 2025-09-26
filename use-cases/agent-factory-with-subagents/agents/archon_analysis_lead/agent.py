#!/usr/bin/env python3
"""
Archon Analysis Lead Agent - главный аналитик команды Archon.

Специализация: анализ требований, декомпозиция задач, исследование и планирование.
"""

from pydantic_ai import Agent, RunContext
from .dependencies import AnalysisLeadDependencies
from ..common import check_pm_switch
from .tools import (
    analyze_requirements,
    decompose_task,
    research_solutions,
    create_analysis_report,
    search_analysis_knowledge
)
from .prompts import get_system_prompt
from .settings import get_llm_model

# Создание агента
analysis_lead_agent = Agent(
    model=get_llm_model(),
    deps_type=AnalysisLeadDependencies,
    system_prompt=get_system_prompt()
)

# Регистрация инструментов
analysis_lead_agent.tool(analyze_requirements)
analysis_lead_agent.tool(decompose_task)
analysis_lead_agent.tool(research_solutions)
analysis_lead_agent.tool(create_analysis_report)
analysis_lead_agent.tool(search_analysis_knowledge)


async def run_analysis_lead(
    query: str,
    project_id: str = None,
    dependencies: AnalysisLeadDependencies = None
) -> str:
    """
    Запустить Analysis Lead агент для анализа требований.

    Args:
        query: Запрос для анализа
        project_id: ID проекта в Archon
        dependencies: Зависимости агента

    Returns:
        Результат анализа
    """
    if not dependencies:
        dependencies = AnalysisLeadDependencies(
            project_id=project_id or "default",
            archon_project_id=project_id
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