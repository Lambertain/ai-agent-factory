# -*- coding: utf-8 -*-
"""
Archon Quality Guardian Agent - Автоматизация контроля качества кода

Универсальный агент для code review, мониторинга метрик качества,
выявления технического долга и интеграции с CI/CD пайплайнами.
"""

from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import os

from .dependencies import QualityGuardianDependencies
from .settings import load_settings
from .prompts import (
    get_system_prompt,
    get_code_review_prompt,
    get_technical_debt_analysis_prompt,
    get_refactoring_suggestion_prompt
)
from .tools import (
    analyze_python_code,
    analyze_typescript_code,
    calculate_code_metrics,
    get_test_coverage,
    detect_code_smells,
    estimate_fix_time,
    find_project_files,
    format_quality_report
)

# Попытка импортировать универсальные декораторы
try:
    from ..common.pydantic_ai_decorators import create_universal_pydantic_agent, with_integrations, register_agent
    DECORATORS_AVAILABLE = True
except ImportError:
    DECORATORS_AVAILABLE = False


def get_llm_model(settings=None):
    """Получить настроенную LLM модель."""
    if settings is None:
        settings = load_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(settings.llm_model, provider=provider)


# Создание агента
if DECORATORS_AVAILABLE:
    # С универсальными декораторами
    agent = create_universal_pydantic_agent(
        model=get_llm_model(),
        deps_type=QualityGuardianDependencies,
        system_prompt=get_system_prompt("general"),
        agent_type="quality_guardian",
        knowledge_tags=["quality-assurance", "code-review", "agent-knowledge"],
        knowledge_domain=None,
        with_collective_tools=True,
        with_knowledge_tool=True
    )

    # Регистрация в глобальном реестре
    register_agent("quality_guardian", agent, agent_type="quality_guardian")
else:
    # Без декораторов - базовая версия
    agent = Agent(
        model=get_llm_model(),
        deps_type=QualityGuardianDependencies,
        system_prompt=get_system_prompt("general")
    )


# ======================
# Инструменты агента
# ======================

@agent.tool
async def analyze_code_file(
    ctx: RunContext[QualityGuardianDependencies],
    file_path: str
) -> str:
    """
    Анализ качества кода в указанном файле.

    Args:
        file_path: Путь к файлу для анализа

    Returns:
        Результаты анализа
    """
    try:
        language = ctx.deps.language
        project_path = ctx.deps.project_path

        # Проверка существования файла
        full_path = os.path.join(project_path, file_path) if not os.path.isabs(file_path) else file_path
        if not os.path.exists(full_path):
            return f"Ошибка: Файл {file_path} не найден"

        # Анализ в зависимости от языка
        if language == "python":
            analysis = await analyze_python_code(full_path, project_path)
        elif language == "typescript":
            analysis = await analyze_typescript_code(full_path, project_path)
        else:
            return f"Язык {language} пока не поддерживается"

        # Подсчет метрик
        metrics = await calculate_code_metrics(full_path, language)

        # Детекция code smells
        with open(full_path, 'r', encoding='utf-8') as f:
            code = f.read()
        smells = await detect_code_smells(code, language)

        # Формирование отчета
        issues = []
        for tool, results in analysis.items():
            if isinstance(results, dict) and "issues" in results:
                issues.extend(results["issues"])

        report = format_quality_report(metrics, issues, smells)

        return f"Анализ файла {file_path}:\n\n{report}"

    except Exception as e:
        return f"Ошибка при анализе файла: {str(e)}"


@agent.tool
async def review_code_with_ai(
    ctx: RunContext[QualityGuardianDependencies],
    file_path: str,
    context: str = ""
) -> str:
    """
    AI-powered code review указанного файла.

    Args:
        file_path: Путь к файлу
        context: Дополнительный контекст для review

    Returns:
        Результаты code review от AI
    """
    try:
        if not ctx.deps.enable_ai_review:
            return "AI code review отключен в настройках"

        project_path = ctx.deps.project_path
        language = ctx.deps.language

        full_path = os.path.join(project_path, file_path) if not os.path.isabs(file_path) else file_path
        if not os.path.exists(full_path):
            return f"Ошибка: Файл {file_path} не найден"

        # Читаем код
        with open(full_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # Создаем промпт для review
        review_prompt = get_code_review_prompt(code, file_path, language, context)

        # AI review через основной агент
        # Примечание: здесь можно использовать отдельный вызов LLM
        # для более детального review

        return f"AI Code Review для {file_path}:\n\n{review_prompt}\n\n(Детальный AI review будет добавлен в следующей итерации)"

    except Exception as e:
        return f"Ошибка AI code review: {str(e)}"


@agent.tool
async def calculate_technical_debt(
    ctx: RunContext[QualityGuardianDependencies]
) -> str:
    """
    Рассчитать технический долг проекта.

    Returns:
        Отчет по техническому долгу
    """
    try:
        project_path = ctx.deps.project_path
        language = ctx.deps.language

        # Определяем расширения файлов для анализа
        extensions = [".py"] if language == "python" else [".ts", ".tsx"]

        # Находим все файлы проекта
        project_files = await find_project_files(project_path, extensions)

        if not project_files:
            return "Не найдено файлов для анализа"

        # Анализируем каждый файл
        total_issues = 0
        total_smells = 0
        total_debt_hours = 0.0

        for file in project_files[:20]:  # Ограничиваем первыми 20 файлами
            try:
                # Анализ
                if language == "python":
                    analysis = await analyze_python_code(file, project_path)
                elif language == "typescript":
                    analysis = await analyze_typescript_code(file, project_path)
                else:
                    continue

                # Подсчет проблем
                for tool, results in analysis.items():
                    if isinstance(results, dict) and "issues" in results:
                        issues = results["issues"]
                        total_issues += len(issues)
                        for issue in issues:
                            debt_hours = await estimate_fix_time(issue)
                            total_debt_hours += debt_hours

                # Code smells
                with open(file, 'r', encoding='utf-8') as f:
                    code = f.read()
                smells = await detect_code_smells(code, language)
                total_smells += len(smells)

            except Exception:
                continue

        report = f"""
# Technical Debt Report

## Summary
- **Analyzed Files:** {len(project_files[:20])} / {len(project_files)}
- **Total Issues:** {total_issues}
- **Code Smells:** {total_smells}
- **Estimated Debt:** {total_debt_hours:.1f} hours

## Recommendations
1. Prioritize critical and blocker issues
2. Refactor files with high code smell count
3. Increase test coverage
4. Setup automated quality checks in CI/CD

## Next Steps
- Run full analysis on all {len(project_files)} files
- Create tasks in Archon for high-priority issues
- Implement automated quality gates
"""

        return report

    except Exception as e:
        return f"Ошибка расчета технического долга: {str(e)}"


@agent.tool
async def get_project_quality_metrics(
    ctx: RunContext[QualityGuardianDependencies]
) -> str:
    """
    Получить общие метрики качества проекта.

    Returns:
        Метрики качества
    """
    try:
        project_path = ctx.deps.project_path
        language = ctx.deps.language

        # Test coverage
        coverage = await get_test_coverage(project_path, language)

        # Находим файлы для анализа
        extensions = [".py"] if language == "python" else [".ts", ".tsx"]
        project_files = await find_project_files(project_path, extensions)

        # Базовые метрики
        total_loc = 0
        for file in project_files[:50]:  # Первые 50 файлов
            metrics = await calculate_code_metrics(file, language)
            total_loc += metrics.get("lines_of_code", 0)

        report = f"""
# Project Quality Metrics

## Code Metrics
- **Total Files:** {len(project_files)}
- **Total Lines of Code:** {total_loc}
- **Average LOC per File:** {total_loc / max(len(project_files), 1):.0f}

## Test Coverage
- **Coverage:** {coverage.get('coverage_percentage', 0):.1f}%
- **Branch Coverage:** {coverage.get('branch_coverage', 0):.1f}%
- **Status:** {'✅ Meets threshold' if coverage.get('coverage_percentage', 0) >= ctx.deps.test_coverage_threshold else '❌ Below threshold'}

## Quality Thresholds
- **Required Coverage:** {ctx.deps.test_coverage_threshold}%
- **Max Complexity:** {ctx.deps.complexity_threshold}
- **Min Maintainability:** {ctx.deps.maintainability_threshold}

## Recommendations
"""

        if coverage.get('coverage_percentage', 0) < ctx.deps.test_coverage_threshold:
            report += f"- Increase test coverage to at least {ctx.deps.test_coverage_threshold}%\n"
        else:
            report += "- Maintain current excellent test coverage\n"

        report += "- Regular code reviews to maintain quality\n"
        report += "- Continuous monitoring of technical debt\n"

        return report

    except Exception as e:
        return f"Ошибка получения метрик: {str(e)}"


# ======================
# Точка входа агента
# ======================

async def run_quality_guardian(
    user_message: str,
    project_path: str,
    language: str = "python",
    project_type: str = "general"
) -> str:
    """
    Запуск агента Quality Guardian.

    Args:
        user_message: Сообщение пользователя
        project_path: Путь к проекту
        language: Язык программирования
        project_type: Тип проекта

    Returns:
        Ответ агента
    """
    deps = QualityGuardianDependencies(
        project_path=project_path,
        language=language,
        project_type=project_type
    )

    if DECORATORS_AVAILABLE:
        # С интеграциями
        @with_integrations(agent_type="quality_guardian")
        async def run_with_integrations():
            result = await agent.run(user_message, deps=deps)
            return result.data

        return await run_with_integrations()
    else:
        # Без интеграций
        result = await agent.run(user_message, deps=deps)
        return result.data


if __name__ == "__main__":
    import asyncio

    async def main():
        # Пример использования
        result = await run_quality_guardian(
            user_message="Проанализируй качество кода в проекте",
            project_path=".",
            language="python"
        )
        print(result)

    asyncio.run(main())
