"""Универсальный TypeScript Architecture Agent для оптимизации архитектуры проектов."""

from pydantic_ai import Agent
from .dependencies import TypeScriptArchitectureDependencies
from ..common import check_pm_switch
from .tools import (
    analyze_type_complexity,
    refactor_types,
    generate_type_guards,
    optimize_typescript_config,
    search_agent_knowledge
)
from .prompts import SYSTEM_PROMPT
from .providers import get_llm_model

# Create the TypeScript Architecture Agent
typescript_agent = Agent(
    model=get_llm_model(),
    deps_type=TypeScriptArchitectureDependencies,
    system_prompt=SYSTEM_PROMPT,
    tools=[
        analyze_type_complexity,
        refactor_types,
        generate_type_guards,
        optimize_typescript_config,
        search_agent_knowledge
    ]
)

async def run_typescript_analysis(
    context: str,
    project_path: str = "",
    analysis_type: str = "full"
) -> str:
    """
    Запуск анализа TypeScript архитектуры.

    Args:
        context: Контекст анализа (код, файлы, требования)
        project_path: Путь к проекту (опционально)
        analysis_type: Тип анализа (full, types, performance, refactor)

    Returns:
        Результат анализа с рекомендациями
    """
    deps = TypeScriptArchitectureDependencies(
        context=context,
        project_path=project_path,
        analysis_mode=analysis_type
    )

    prompt = f"""
    ## 📋 ПЛАНИРОВАНИЕ
    Проанализируй TypeScript архитектуру проекта:

    **Контекст:** {context}
    **Тип анализа:** {analysis_type}

    Выполни анализ согласно мультиагентным паттернам:
    1. Используй инструменты для анализа сложности типов
    2. Найди проблемные места в архитектуре
    3. Предложи конкретные улучшения
    4. Обеспечь type safety на 95%+

    ## 🔄 РЕФЛЕКСИЯ-УЛУЧШЕНИЕ
    После анализа:
    1. Проанализируй качество предложенных решений
    2. Выяви 2-3 недостатка в подходе
    3. Создай улучшенную версию рекомендаций
    """

    result = await typescript_agent.run(prompt, deps=deps)
    return result.data

def run_sync(context: str, **kwargs) -> str:
    """Синхронная версия для CLI."""
    import asyncio
    return asyncio.run(run_typescript_analysis(context, **kwargs))

# Экспорт для использования в других модулях
__all__ = ['typescript_agent', 'run_typescript_analysis', 'run_sync']