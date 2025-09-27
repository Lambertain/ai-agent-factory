# -*- coding: utf-8 -*-
"""
Universal Opportunity Analyzer Agent
Универсальный агент для анализа возможностей и болевых точек в любых доменах
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any

from pydantic_ai import Agent, RunContext
from .dependencies import load_dependencies, OpportunityAnalyzerDependencies
from .providers import get_llm_model
from .tools import (
    analyze_domain_opportunities,
    identify_pain_points,
    evaluate_market_potential,
    search_opportunity_patterns,
    delegate_task_to_agent,
    assess_competition_landscape,
    calculate_opportunity_score,
    break_down_to_microtasks,
    report_microtask_progress,
    reflect_and_improve,
    check_delegation_need
)
from .prompts import get_system_prompt

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Pydantic AI агента (универсальная архитектура)
opportunity_analyzer_agent = Agent(
    get_llm_model(),
    deps_type=OpportunityAnalyzerDependencies,
    system_prompt=get_system_prompt()
)

# Регистрируем универсальные инструменты анализа возможностей
opportunity_analyzer_agent.tool(analyze_domain_opportunities)
opportunity_analyzer_agent.tool(identify_pain_points)
opportunity_analyzer_agent.tool(evaluate_market_potential)
opportunity_analyzer_agent.tool(search_opportunity_patterns)
opportunity_analyzer_agent.tool(assess_competition_landscape)
opportunity_analyzer_agent.tool(calculate_opportunity_score)

# Регистрируем инструменты коллективной работы
opportunity_analyzer_agent.tool(break_down_to_microtasks)
opportunity_analyzer_agent.tool(report_microtask_progress)
opportunity_analyzer_agent.tool(reflect_and_improve)
opportunity_analyzer_agent.tool(check_delegation_need)
opportunity_analyzer_agent.tool(delegate_task_to_agent)

async def run_opportunity_analysis(
    message: str,
    domain_type: str = "psychology",
    project_type: str = "transformation_platform",
    framework: str = "pydantic_ai"
) -> str:
    """
    Запуск универсального анализа возможностей в домене.

    Args:
        message: Задача для анализа возможностей
        domain_type: Тип домена (psychology, astrology, numerology, business, etc.)
        project_type: Тип проекта (transformation_platform, educational_system, etc.)
        framework: Технологический фреймворк (pydantic_ai, fastapi, etc.)

    Returns:
        Результат анализа возможностей
    """
    try:
        # Загружаем зависимости с учетом домена
        deps = load_dependencies(
            domain_type=domain_type,
            project_type=project_type,
            framework=framework
        )

        logger.info(f"Запуск анализа возможностей для домена: {domain_type}")

        # Выполняем анализ возможностей
        result = await opportunity_analyzer_agent.run(message, deps=deps)

        logger.info(f"Анализ возможностей завершен успешно")
        return result.data

    except Exception as e:
        error_msg = f"Ошибка при анализе возможностей: {e}"
        logger.error(error_msg)
        return error_msg

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Использование: python agent.py <сообщение> [domain_type] [project_type] [framework]")
        sys.exit(1)

    message = sys.argv[1]
    domain_type = sys.argv[2] if len(sys.argv) > 2 else "psychology"
    project_type = sys.argv[3] if len(sys.argv) > 3 else "transformation_platform"
    framework = sys.argv[4] if len(sys.argv) > 4 else "pydantic_ai"

    # Запуск в асинхронном контексте
    result = asyncio.run(run_opportunity_analysis(
        message, domain_type, project_type, framework
    ))
    print(result)