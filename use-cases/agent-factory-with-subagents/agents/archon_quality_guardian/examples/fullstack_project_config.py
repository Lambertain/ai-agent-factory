# -*- coding: utf-8 -*-
"""
Пример конфигурации Quality Guardian для Fullstack проекта
"""

from ..dependencies import Quality GuardianDependencies

# Конфигурация для Fullstack проекта (Python backend + TypeScript frontend)
fullstack_config = QualityGuardianDependencies(
    project_path="/path/to/fullstack/project",
    project_type="fullstack",
    language="python",  # Основной язык (можно переключать)
    framework="fastapi",  # Backend framework

    # Quality Standards (усредненные)
    test_coverage_threshold=82.0,  # Среднее между Python и TypeScript
    complexity_threshold=12,
    maintainability_threshold=57.0,

    # Security (строже для fullstack)
    security_scan_enabled=True,
    security_severity_threshold="high",

    # Auto-fix
    enable_auto_fix=True,
    enable_ai_review=True,

    # CI/CD
    ci_cd_platform="gitlab",  # GitLab CI

    # Archon Integration
    archon_project_id="your-project-id",
    enable_task_delegation=True
)

# Использование для fullstack анализа
async def analyze_fullstack_project():
    from ..agent import run_quality_guardian

    # Анализ backend
    print("=== Backend Analysis ===")
    backend_result = await run_quality_guardian(
        user_message="Проанализируй качество backend (Python/FastAPI)",
        project_path=fullstack_config.project_path + "/backend",
        language="python",
        project_type="fullstack"
    )
    print(backend_result)

    # Анализ frontend
    print("\n=== Frontend Analysis ===")
    frontend_result = await run_quality_guardian(
        user_message="Проанализируй качество frontend (TypeScript/React)",
        project_path=fullstack_config.project_path + "/frontend",
        language="typescript",
        project_type="fullstack"
    )
    print(frontend_result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(analyze_fullstack_project())
