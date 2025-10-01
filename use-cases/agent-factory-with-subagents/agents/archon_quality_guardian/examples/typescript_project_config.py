# -*- coding: utf-8 -*-
"""
Пример конфигурации Quality Guardian для TypeScript проекта
"""

from ..dependencies import QualityGuardianDependencies

# Конфигурация для TypeScript/Next.js проекта
typescript_config = QualityGuardianDependencies(
    project_path="/path/to/typescript/project",
    project_type="typescript",
    language="typescript",
    framework="nextjs",  # или "react", "vue", "angular"

    # Quality Standards для TypeScript
    test_coverage_threshold=80.0,
    complexity_threshold=15,  # TypeScript может быть сложнее
    maintainability_threshold=55.0,

    # Security для TypeScript
    security_scan_enabled=True,
    security_severity_threshold="high",  # Строже для frontend

    # Auto-fix для TypeScript
    enable_auto_fix=True,  # ESLint --fix, Prettier
    enable_ai_review=True,

    # CI/CD
    ci_cd_platform="github",  # GitHub Actions

    # Archon Integration
    archon_project_id="your-project-id",
    enable_task_delegation=True
)

# Использование
async def analyze_typescript_project():
    from ..agent import run_quality_guardian

    result = await run_quality_guardian(
        user_message="Проанализируй TypeScript/Next.js проект на качество и производительность",
        project_path=typescript_config.project_path,
        language="typescript",
        project_type="typescript"
    )

    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(analyze_typescript_project())
