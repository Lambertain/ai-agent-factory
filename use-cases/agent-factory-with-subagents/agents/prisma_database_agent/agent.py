"""Универсальный Prisma Database Agent для оптимизации и управления базами данных."""

import asyncio
from typing import Optional, Any, Dict, List
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

from .settings import load_settings
from ..common import check_pm_switch
from .providers import get_prisma_model_by_task
from .dependencies import PrismaDatabaseDependencies
from .prompts import SYSTEM_PROMPT
from .tools import (
    analyze_schema_performance,
    optimize_queries,
    create_migration_plan,
    analyze_slow_queries,
    search_agent_knowledge
)


# Инициализация настроек
settings = load_settings()

# Создание агента с мультиагентными паттернами
prisma_agent = Agent(
    model=get_prisma_model_by_task("architecture"),  # Используем архитектурную модель по умолчанию
    deps_type=PrismaDatabaseDependencies,
    system_prompt=SYSTEM_PROMPT,
    retries=2
)

# Регистрация инструментов
prisma_agent.tool(analyze_schema_performance)
prisma_agent.tool(optimize_queries)
prisma_agent.tool(create_migration_plan)
prisma_agent.tool(analyze_slow_queries)
prisma_agent.tool(search_agent_knowledge)


@prisma_agent.result_validator
async def validate_result(ctx: RunContext[PrismaDatabaseDependencies], result: str) -> str:
    """Валидация результата с рефлексией."""

    # Простая проверка на пустой результат
    if not result or len(result.strip()) < 50:
        raise ValueError("Результат слишком короткий или пустой")

    # Проверка обязательных секций мультиагентного паттерна
    required_sections = ["ПЛАНИРОВАНИЕ", "ВЫПОЛНЕНИЕ С ИНСТРУМЕНТАМИ", "РЕФЛЕКСИЯ-УЛУЧШЕНИЕ"]
    missing_sections = [section for section in required_sections if section not in result]

    if missing_sections:
        raise ValueError(f"Отсутствуют обязательные секции: {', '.join(missing_sections)}")

    return result


async def run_prisma_analysis(
    context: str,
    project_path: str = "",
    analysis_type: str = "full"
) -> str:
    """
    Запуск анализа Prisma схемы и базы данных.

    Args:
        context: Контекст анализа (схема, запросы, или описание проблемы)
        project_path: Путь к проекту с Prisma схемой
        analysis_type: Тип анализа - "full", "schema", "queries", "migrations", "performance"

    Returns:
        Результат анализа и рекомендации
    """

    # Настройка зависимостей
    deps = PrismaDatabaseDependencies(
        context=context,
        project_path=project_path,
        analysis_mode=analysis_type
    )

    # Выбор модели в зависимости от типа задачи
    if analysis_type in ["performance", "queries"]:
        model = get_prisma_model_by_task("architecture")  # Сложный анализ
    elif analysis_type == "migrations":
        model = get_prisma_model_by_task("coding")  # Генерация кода
    else:
        model = get_prisma_model_by_task("planning")  # Планирование

    # Переопределение модели для конкретной задачи
    agent_with_model = prisma_agent.override(model=model)

    try:
        result = await agent_with_model.run(context, deps=deps)
        return result.data
    except Exception as e:
        error_msg = f"Ошибка выполнения анализа Prisma: {e}"
        print(f"❌ {error_msg}")
        return error_msg


def run_sync(
    context: str,
    project_path: str = "",
    analysis_type: str = "full"
) -> str:
    """Синхронная обёртка для run_prisma_analysis."""
    return asyncio.run(run_prisma_analysis(context, project_path, analysis_type))


# Экспорт для использования как модуль
__all__ = [
    "prisma_agent",
    "run_prisma_analysis",
    "run_sync",
    "PrismaDatabaseDependencies"
]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Использование: python agent.py 'описание анализа' [тип_анализа]")
        sys.exit(1)

    context = sys.argv[1]
    analysis_type = sys.argv[2] if len(sys.argv) > 2 else "full"

    print(f"🗄️ Запуск Prisma Database Agent...")
    print(f"📋 Контекст: {context}")
    print(f"🔍 Тип анализа: {analysis_type}")

    result = run_sync(context, analysis_type=analysis_type)
    print("\n" + "="*60)
    print("📊 РЕЗУЛЬТАТ АНАЛИЗА:")
    print("="*60)
    print(result)