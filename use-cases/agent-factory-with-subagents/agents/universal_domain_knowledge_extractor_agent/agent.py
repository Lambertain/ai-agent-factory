# -*- coding: utf-8 -*-
"""
Universal Domain Knowledge Extractor Agent
Универсальный агент для извлечения знаний из любых доменов (психология, астрология, нумерология и т.д.)
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any

from pydantic_ai import Agent, RunContext
from .dependencies import load_dependencies, DomainKnowledgeExtractorDependencies
from .providers import get_llm_model
from .tools import (
    extract_domain_knowledge,
    analyze_knowledge_patterns,
    create_knowledge_modules,
    search_domain_knowledge,
    delegate_task_to_agent,
    validate_knowledge_structure,
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
domain_knowledge_extractor_agent = Agent(
    get_llm_model(),
    deps_type=DomainKnowledgeExtractorDependencies,
    system_prompt=get_system_prompt()
)

# Регистрируем универсальные инструменты извлечения знаний
domain_knowledge_extractor_agent.tool(extract_domain_knowledge)
domain_knowledge_extractor_agent.tool(analyze_knowledge_patterns)
domain_knowledge_extractor_agent.tool(create_knowledge_modules)
domain_knowledge_extractor_agent.tool(search_domain_knowledge)
domain_knowledge_extractor_agent.tool(validate_knowledge_structure)

# Регистрируем инструменты коллективной работы
domain_knowledge_extractor_agent.tool(break_down_to_microtasks)
domain_knowledge_extractor_agent.tool(report_microtask_progress)
domain_knowledge_extractor_agent.tool(reflect_and_improve)
domain_knowledge_extractor_agent.tool(check_delegation_need)
domain_knowledge_extractor_agent.tool(delegate_task_to_agent)

async def run_domain_knowledge_extraction(
    message: str,
    domain_type: str = "psychology",
    project_type: str = "transformation_platform",
    framework: str = "pydantic_ai"
) -> str:
    """
    Запуск универсального извлечения знаний из домена.

    Args:
        message: Задача для извлечения знаний
        domain_type: Тип домена (psychology, astrology, numerology, business, etc.)
        project_type: Тип проекта (transformation_platform, educational_system, etc.)
        framework: Технологический фреймворк (pydantic_ai, fastapi, etc.)

    Returns:
        Результат извлечения знаний
    """
    try:
        # Загружаем зависимости с учетом домена
        deps = load_dependencies(
            domain_type=domain_type,
            project_type=project_type,
            framework=framework
        )

        logger.info(f"Запуск извлечения знаний для домена: {domain_type}")

        # Выполняем извлечение знаний
        result = await domain_knowledge_extractor_agent.run(message, deps=deps)

        logger.info(f"Извлечение знаний завершено успешно")
        return result.data

    except Exception as e:
        error_msg = f"Ошибка при извлечении знаний: {e}"
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
    result = asyncio.run(run_domain_knowledge_extraction(
        message, domain_type, project_type, framework
    ))
    print(result)