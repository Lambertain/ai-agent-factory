# -*- coding: utf-8 -*-
"""
Universal Personalizer Agent
Универсальный агент для персонализации контента и опыта в различных доменах
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any

from pydantic_ai import Agent, RunContext
from .dependencies import load_dependencies, PersonalizerDependencies
from .providers import get_llm_model
from .tools import (
    analyze_user_profile,
    generate_personalized_content,
    create_personalization_rules,
    adapt_content_to_user,
    track_personalization_effectiveness,
    search_personalization_patterns,
    validate_personalization_quality,
    optimize_user_experience,
    break_down_to_microtasks,
    report_microtask_progress,
    reflect_and_improve,
    check_delegation_need,
    delegate_task_to_agent
)
from .prompts import get_system_prompt

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Pydantic AI агента (универсальная архитектура)
personalizer_agent = Agent(
    get_llm_model(),
    deps_type=PersonalizerDependencies,
    system_prompt=get_system_prompt()
)

# Регистрируем универсальные инструменты персонализации
personalizer_agent.tool(analyze_user_profile)
personalizer_agent.tool(generate_personalized_content)
personalizer_agent.tool(create_personalization_rules)
personalizer_agent.tool(adapt_content_to_user)
personalizer_agent.tool(track_personalization_effectiveness)
personalizer_agent.tool(search_personalization_patterns)
personalizer_agent.tool(validate_personalization_quality)
personalizer_agent.tool(optimize_user_experience)

# Регистрируем инструменты коллективной работы
personalizer_agent.tool(break_down_to_microtasks)
personalizer_agent.tool(report_microtask_progress)
personalizer_agent.tool(reflect_and_improve)
personalizer_agent.tool(check_delegation_need)
personalizer_agent.tool(delegate_task_to_agent)

async def run_personalization_task(
    message: str,
    domain_type: str = "psychology",
    project_type: str = "transformation_platform",
    framework: str = "pydantic_ai",
    personalization_mode: str = "adaptive"
) -> str:
    """
    Запуск универсальной персонализации контента и опыта.

    Args:
        message: Задача для персонализации
        domain_type: Тип домена (psychology, astrology, numerology, business, etc.)
        project_type: Тип проекта (transformation_platform, educational_system, etc.)
        framework: Технологический фреймворк (pydantic_ai, fastapi, etc.)
        personalization_mode: Режим персонализации (adaptive, rule_based, ml_driven, hybrid)

    Returns:
        Результат персонализации контента и опыта
    """
    try:
        # Загружаем зависимости с учетом домена
        deps = load_dependencies(
            domain_type=domain_type,
            project_type=project_type,
            framework=framework,
            personalization_mode=personalization_mode
        )

        logger.info(f"Запуск персонализации для домена: {domain_type}")

        # Выполняем персонализацию
        result = await personalizer_agent.run(message, deps=deps)

        logger.info(f"Персонализация завершена успешно")
        return result.data

    except Exception as e:
        error_msg = f"Ошибка при персонализации: {e}"
        logger.error(error_msg)
        return error_msg

async def run_user_profile_analysis(
    user_data: Dict[str, Any],
    domain_type: str = "psychology",
    analysis_depth: str = "comprehensive"
) -> Dict[str, Any]:
    """
    Анализ профиля пользователя для персонализации.

    Args:
        user_data: Данные пользователя для анализа
        domain_type: Тип домена для контекстуального анализа
        analysis_depth: Глубина анализа (basic, comprehensive, deep)

    Returns:
        Результат анализа профиля пользователя
    """
    try:
        deps = load_dependencies(domain_type=domain_type)

        # Создаем сообщение для анализа профиля
        message = f"""
        Проанализируй профиль пользователя для персонализации в домене {domain_type}.

        Данные пользователя: {user_data}
        Глубина анализа: {analysis_depth}

        Создай комплексный профиль для персонализации контента и опыта.
        """

        result = await personalizer_agent.run(message, deps=deps)
        return {"success": True, "profile_analysis": result.data}

    except Exception as e:
        logger.error(f"Ошибка анализа профиля: {e}")
        return {"success": False, "error": str(e)}

async def run_content_personalization(
    content: str,
    user_profile: Dict[str, Any],
    domain_type: str = "psychology",
    personalization_strategy: str = "adaptive"
) -> Dict[str, Any]:
    """
    Персонализация контента под конкретного пользователя.

    Args:
        content: Исходный контент для персонализации
        user_profile: Профиль пользователя
        domain_type: Тип домена
        personalization_strategy: Стратегия персонализации

    Returns:
        Персонализированный контент
    """
    try:
        deps = load_dependencies(domain_type=domain_type)

        message = f"""
        Персонализируй контент под пользователя в домене {domain_type}.

        Исходный контент: {content}
        Профиль пользователя: {user_profile}
        Стратегия: {personalization_strategy}

        Создай персонализированную версию контента.
        """

        result = await personalizer_agent.run(message, deps=deps)
        return {"success": True, "personalized_content": result.data}

    except Exception as e:
        logger.error(f"Ошибка персонализации контента: {e}")
        return {"success": False, "error": str(e)}

async def run_ux_optimization(
    user_journey: Dict[str, Any],
    domain_type: str = "psychology",
    optimization_goals: List[str] = None
) -> Dict[str, Any]:
    """
    Оптимизация пользовательского опыта.

    Args:
        user_journey: Данные о пользовательском пути
        domain_type: Тип домена
        optimization_goals: Цели оптимизации

    Returns:
        Рекомендации по оптимизации UX
    """
    try:
        deps = load_dependencies(domain_type=domain_type)

        if optimization_goals is None:
            optimization_goals = ["engagement", "conversion", "satisfaction"]

        message = f"""
        Оптимизируй пользовательский опыт в домене {domain_type}.

        Пользовательский путь: {user_journey}
        Цели оптимизации: {optimization_goals}

        Предложи конкретные улучшения для персонализации UX.
        """

        result = await personalizer_agent.run(message, deps=deps)
        return {"success": True, "ux_optimization": result.data}

    except Exception as e:
        logger.error(f"Ошибка оптимизации UX: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Использование: python agent.py <сообщение> [domain_type] [project_type] [framework] [personalization_mode]")
        sys.exit(1)

    message = sys.argv[1]
    domain_type = sys.argv[2] if len(sys.argv) > 2 else "psychology"
    project_type = sys.argv[3] if len(sys.argv) > 3 else "transformation_platform"
    framework = sys.argv[4] if len(sys.argv) > 4 else "pydantic_ai"
    personalization_mode = sys.argv[5] if len(sys.argv) > 5 else "adaptive"

    # Запуск в асинхронном контексте
    result = asyncio.run(run_personalization_task(
        message, domain_type, project_type, framework, personalization_mode
    ))
    print(result)