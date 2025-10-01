# -*- coding: utf-8 -*-
"""
Пример конфигурации Quality Guardian для Python проекта
"""

from ..dependencies import QualityGuardianDependencies

# Конфигурация для Python проекта
python_config = QualityGuardianDependencies(
    project_path="/path/to/python/project",
    project_type="python",
    language="python",
    framework="fastapi",  # или "flask", "django", None

    # Quality Standards для Python
    test_coverage_threshold=85.0,  # Высокий стандарт для Python
    complexity_threshold=10,  # PEP 8 рекомендует <= 10
    maintainability_threshold=60.0,

    # Security для Python
    security_scan_enabled=True,
    security_severity_threshold="medium",

    # Auto-fix для Python
    enable_auto_fix=True,  # Autopep8, black, isort
    enable_ai_review=True,

    # CI/CD
    ci_cd_platform="github",  # GitHub Actions

    # Archon Integration
    archon_project_id="your-project-id",
    enable_task_delegation=True
)

# Использование
async def analyze_python_project():
    from ..agent import run_quality_guardian

    result = await run_quality_guardian(
        user_message="Проведи полный анализ качества Python проекта",
        project_path=python_config.project_path,
        language="python",
        project_type="python"
    )

    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(analyze_python_project())
