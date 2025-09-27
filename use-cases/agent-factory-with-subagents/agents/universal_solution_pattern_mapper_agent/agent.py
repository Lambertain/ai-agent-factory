# -*- coding: utf-8 -*-
"""
Universal Solution Pattern Mapper Agent
Универсальный агент для маппинга решений и паттернов в любых доменах
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any

from pydantic_ai import Agent, RunContext
from .dependencies import load_dependencies, SolutionPatternMapperDependencies
from .providers import get_llm_model
from .tools import (
    map_solution_patterns,
    analyze_problem_solution_fit,
    generate_solution_blueprints,
    search_pattern_knowledge,
    validate_solution_patterns,
    adapt_patterns_to_domain,
    delegate_task_to_agent,
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
solution_pattern_mapper_agent = Agent(
    get_llm_model(),
    deps_type=SolutionPatternMapperDependencies,
    system_prompt=get_system_prompt()
)

# Регистрируем универсальные инструменты маппинга паттернов
solution_pattern_mapper_agent.tool(map_solution_patterns)
solution_pattern_mapper_agent.tool(analyze_problem_solution_fit)
solution_pattern_mapper_agent.tool(generate_solution_blueprints)
solution_pattern_mapper_agent.tool(search_pattern_knowledge)
solution_pattern_mapper_agent.tool(validate_solution_patterns)
solution_pattern_mapper_agent.tool(adapt_patterns_to_domain)

# Регистрируем инструменты коллективной работы
solution_pattern_mapper_agent.tool(break_down_to_microtasks)
solution_pattern_mapper_agent.tool(report_microtask_progress)
solution_pattern_mapper_agent.tool(reflect_and_improve)
solution_pattern_mapper_agent.tool(check_delegation_need)
solution_pattern_mapper_agent.tool(delegate_task_to_agent)

async def run_solution_pattern_mapping(
    message: str,
    domain_type: str = "psychology",
    project_type: str = "transformation_platform",
    framework: str = "pydantic_ai"
) -> str:
    """
    Запуск универсального маппинга решений и паттернов в домене.

    Args:
        message: Задача для маппинга решений
        domain_type: Тип домена (psychology, astrology, numerology, business, etc.)
        project_type: Тип проекта (transformation_platform, educational_system, etc.)
        framework: Технологический фреймворк (pydantic_ai, fastapi, etc.)

    Returns:
        Результат маппинга решений и паттернов
    """
    try:
        # Загружаем зависимости с учетом домена
        deps = load_dependencies(
            domain_type=domain_type,
            project_type=project_type,
            framework=framework
        )

        logger.info(f"Запуск маппинга решений для домена: {domain_type}")

        # Выполняем маппинг решений и паттернов
        result = await solution_pattern_mapper_agent.run(message, deps=deps)

        logger.info(f"Маппинг решений завершен успешно")
        return result.data

    except Exception as e:
        error_msg = f"Ошибка при маппинге решений: {e}"
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
    result = asyncio.run(run_solution_pattern_mapping(
        message, domain_type, project_type, framework
    ))
    print(result)