"""
Universal Performance & Next.js Optimization Agent - универсальный агент для оптимизации производительности с расширенной поддержкой Next.js.

Специализируется на анализе и улучшении производительности различных типов проектов:
- Frontend приложения (React, Vue, Angular, Next.js 14)
- Backend API (FastAPI, Django, Express)
- Database optimization (PostgreSQL, MySQL, MongoDB)
- Full-stack web applications
- Next.js App Router, Server Components, Edge Runtime

Автоматически адаптируется под тип проекта и используемые технологии.
"""

import asyncio
from typing import Optional
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

from .dependencies import PerformanceOptimizationDependencies, load_performance_settings
from ..common import check_pm_switch
from .prompts import get_system_prompt
from .tools import (
    analyze_performance,
    optimize_performance,
    monitor_performance,
    search_performance_knowledge,
    generate_performance_report,
    # Context7 MCP Integration
    resolve_library_id_context7,
    get_library_docs_context7,
    analyze_project_context,
    track_performance_patterns,
    identify_bottlenecks,
    generate_optimization_plan
)


def get_llm_model():
    """Конфигурация LLM модели для агента."""
    settings = load_performance_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)


# Создание агента с динамическим системным промптом
performance_agent = Agent(
    model=get_llm_model(),
    deps_type=PerformanceOptimizationDependencies,
    system_prompt=lambda ctx: get_system_prompt(ctx.deps),
    retries=2
)


# Регистрация инструментов
@performance_agent.tool
async def analyze_project_performance(
    ctx: RunContext[PerformanceOptimizationDependencies],
    target_path: str,
    analysis_type: str = "full"
) -> str:
    """
    Провести анализ производительности проекта.

    Args:
        target_path: Путь к проекту для анализа
        analysis_type: Тип анализа - 'full', 'frontend', 'backend', 'database'

    Returns:
        Детальный отчет об анализе производительности
    """
    return await analyze_performance(ctx, target_path, analysis_type)


@performance_agent.tool
async def apply_performance_optimizations(
    ctx: RunContext[PerformanceOptimizationDependencies],
    target_path: str,
    optimization_areas: list[str]
) -> str:
    """
    Применить конкретные оптимизации производительности.

    Args:
        target_path: Путь к проекту
        optimization_areas: Список областей для оптимизации:
                          ['bundle', 'caching', 'compression', 'database', 'images']

    Returns:
        Результат применения оптимизаций
    """
    return await optimize_performance(ctx, target_path, optimization_areas)


@performance_agent.tool
async def monitor_real_time_performance(
    ctx: RunContext[PerformanceOptimizationDependencies],
    duration_seconds: int = 60,
    metrics: Optional[list[str]] = None
) -> str:
    """
    Запустить мониторинг производительности в реальном времени.

    Args:
        duration_seconds: Длительность мониторинга в секундах
        metrics: Список метрик для отслеживания: ['cpu', 'memory', 'disk', 'network']

    Returns:
        Результаты мониторинга с анализом трендов
    """
    return await monitor_performance(ctx, duration_seconds, metrics)


@performance_agent.tool
async def search_optimization_knowledge(
    ctx: RunContext[PerformanceOptimizationDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Найти релевантную информацию в базе знаний по оптимизации производительности.

    Args:
        query: Поисковый запрос (например, "React bundle optimization")
        match_count: Количество результатов для возврата

    Returns:
        Найденная информация и рекомендации из базы знаний
    """
    return await search_performance_knowledge(ctx, query, match_count)


@performance_agent.tool
async def create_performance_report(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    include_recommendations: bool = True
) -> str:
    """
    Сгенерировать комплексный отчет о производительности проекта.

    Args:
        project_path: Путь к анализируемому проекту
        include_recommendations: Включить рекомендации по улучшению

    Returns:
        Детальный отчет с анализом, метриками и рекомендациями
    """
    return await generate_performance_report(ctx, project_path, include_recommendations)


# Context7 MCP Integration Tools

@performance_agent.tool
async def resolve_framework_library_id(
    ctx: RunContext[PerformanceOptimizationDependencies],
    library_name: str
) -> str:
    """
    Получить Context7 ID для библиотеки/фреймворка для анализа производительности.

    Args:
        library_name: Название библиотеки или фреймворка (например, "react", "nextjs", "vue")

    Returns:
        Context7-совместимый ID библиотеки
    """
    return await resolve_library_id_context7(ctx, library_name)


@performance_agent.tool
async def get_performance_documentation(
    ctx: RunContext[PerformanceOptimizationDependencies],
    context7_library_id: str,
    topic: str = "performance optimization",
    tokens: int = 8000
) -> str:
    """
    Получить документацию по производительности через Context7 MCP.

    Args:
        context7_library_id: Context7 ID библиотеки
        topic: Тема документации (performance, optimization, best practices)
        tokens: Максимальное количество токенов

    Returns:
        Документация с фокусом на производительность
    """
    return await get_library_docs_context7(ctx, context7_library_id, topic, tokens)


@performance_agent.tool
async def analyze_project_with_context7(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    framework_focus: str = None
) -> str:
    """
    Глубокий анализ контекста проекта с использованием Context7 знаний.

    Args:
        project_path: Путь к проекту для анализа
        framework_focus: Фреймворк для фокуса анализа

    Returns:
        Подробный анализ контекста проекта с Context7 рекомендациями
    """
    return await analyze_project_context(ctx, project_path, framework_focus)


@performance_agent.tool
async def analyze_performance_patterns(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    pattern_types: list[str] = None
) -> str:
    """
    Анализ паттернов производительности в проекте через Context7.

    Args:
        project_path: Путь к проекту
        pattern_types: Типы паттернов ['anti-patterns', 'optimization-patterns', 'performance-patterns']

    Returns:
        Анализ найденных паттернов и рекомендации по улучшению
    """
    return await track_performance_patterns(ctx, project_path, pattern_types)


@performance_agent.tool
async def find_performance_bottlenecks(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    analysis_depth: str = "medium"
) -> str:
    """
    Идентификация узких мест производительности через Context7 анализ.

    Args:
        project_path: Путь к проекту
        analysis_depth: Глубина анализа ('shallow', 'medium', 'deep')

    Returns:
        Детальный анализ узких мест с приоритизацией исправлений
    """
    return await identify_bottlenecks(ctx, project_path, analysis_depth)


@performance_agent.tool
async def create_optimization_plan(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    target_metrics: dict = None
) -> str:
    """
    Создание комплексного плана оптимизации на основе Context7 анализа.

    Args:
        project_path: Путь к проекту
        target_metrics: Целевые метрики производительности

    Returns:
        Детальный план оптимизации с фазами реализации и критериями успеха
    """
    return await generate_optimization_plan(ctx, project_path, target_metrics)


# Основные функции для работы с агентом

async def run_performance_optimization(
    project_path: str,
    domain_type: str = "web_application",
    project_type: str = "full_stack",
    framework: str = "react",
    task: str = "analyze",
    **kwargs
) -> str:
    """
    Асинхронный запуск Performance Optimization Agent.

    Args:
        project_path: Путь к проекту
        domain_type: Тип домена (frontend, backend, database, web_application)
        project_type: Тип проекта (spa, rest_api, postgresql, full_stack)
        framework: Используемый фреймворк (react, vue, fastapi, django)
        task: Задача для выполнения (analyze, optimize, monitor, report)
        **kwargs: Дополнительные параметры

    Returns:
        Результат выполнения задачи
    """
    try:
        # Загрузка настроек
        settings = load_performance_settings()

        # Создание зависимостей агента
        deps = PerformanceOptimizationDependencies(
            api_key=settings.llm_api_key,
            project_path=project_path,
            domain_type=domain_type,
            project_type=project_type,
            framework=framework,
            archon_project_id=settings.archon_project_id,
            enable_caching=settings.enable_caching,
            enable_compression=settings.enable_compression,
            enable_monitoring=settings.enable_monitoring,
            enable_lazy_loading=settings.enable_lazy_loading,
            target_response_time_ms=settings.target_response_time_ms,
            target_throughput_rps=settings.target_throughput_rps,
            target_error_rate=settings.target_error_rate
        )

        # Формирование промпта в зависимости от задачи
        if task == "analyze":
            prompt = f"Проанализируй производительность {domain_type} проекта по пути {project_path}"
        elif task == "optimize":
            areas = kwargs.get("optimization_areas", ["bundle", "caching", "compression"])
            prompt = f"Оптимизируй производительность проекта {project_path} в областях: {', '.join(areas)}"
        elif task == "monitor":
            duration = kwargs.get("duration", 60)
            prompt = f"Запусти мониторинг производительности проекта {project_path} на {duration} секунд"
        elif task == "report":
            prompt = f"Создай полный отчет о производительности проекта {project_path}"
        else:
            prompt = f"Помоги с оптимизацией производительности {domain_type} проекта: {kwargs.get('custom_prompt', task)}"

        # Запуск агента
        result = await performance_agent.run(prompt, deps=deps)
        return result.data

    except Exception as e:
        return f"Ошибка при выполнении Performance Optimization Agent: {e}"


def run_performance_optimization_sync(
    project_path: str,
    domain_type: str = "web_application",
    project_type: str = "full_stack",
    framework: str = "react",
    task: str = "analyze",
    **kwargs
) -> str:
    """
    Синхронный запуск Performance Optimization Agent.

    Args:
        project_path: Путь к проекту
        domain_type: Тип домена (frontend, backend, database, web_application)
        project_type: Тип проекта (spa, rest_api, postgresql, full_stack)
        framework: Используемый фреймворк (react, vue, fastapi, django)
        task: Задача для выполнения (analyze, optimize, monitor, report)
        **kwargs: Дополнительные параметры

    Returns:
        Результат выполнения задачи
    """
    return asyncio.run(run_performance_optimization(
        project_path=project_path,
        domain_type=domain_type,
        project_type=project_type,
        framework=framework,
        task=task,
        **kwargs
    ))


# Вспомогательные функции для быстрого запуска

async def analyze_project(project_path: str, **kwargs) -> str:
    """Быстрый анализ производительности проекта."""
    return await run_performance_optimization(
        project_path=project_path,
        task="analyze",
        **kwargs
    )


async def optimize_project(project_path: str, areas: list[str], **kwargs) -> str:
    """Быстрая оптимизация проекта в указанных областях."""
    return await run_performance_optimization(
        project_path=project_path,
        task="optimize",
        optimization_areas=areas,
        **kwargs
    )


async def monitor_project(project_path: str, duration: int = 60, **kwargs) -> str:
    """Быстрый мониторинг производительности проекта."""
    return await run_performance_optimization(
        project_path=project_path,
        task="monitor",
        duration=duration,
        **kwargs
    )


async def create_project_report(project_path: str, **kwargs) -> str:
    """Быстрое создание отчета о производительности."""
    return await run_performance_optimization(
        project_path=project_path,
        task="report",
        **kwargs
    )


# CLI интерфейс (опционально)
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Performance Optimization Agent")
    parser.add_argument("project_path", help="Путь к проекту")
    parser.add_argument("--domain", default="web_application",
                       choices=["frontend", "backend", "database", "api", "web_application"],
                       help="Тип домена проекта")
    parser.add_argument("--framework", default="react",
                       help="Используемый фреймворк")
    parser.add_argument("--task", default="analyze",
                       choices=["analyze", "optimize", "monitor", "report"],
                       help="Задача для выполнения")
    parser.add_argument("--areas", nargs="*",
                       default=["bundle", "caching", "compression"],
                       help="Области для оптимизации")

    args = parser.parse_args()

    try:
        result = run_performance_optimization_sync(
            project_path=args.project_path,
            domain_type=args.domain,
            framework=args.framework,
            task=args.task,
            optimization_areas=args.areas
        )
        print(result)
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)