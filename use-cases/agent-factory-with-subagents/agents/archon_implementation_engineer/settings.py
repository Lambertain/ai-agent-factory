#!/usr/bin/env python3
"""
Настройки для Archon Implementation Engineer Agent.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv


class ImplementationEngineerSettings(BaseSettings):
    """Настройки Implementation Engineer агента."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM настройки
    llm_api_key: str = Field(..., description="API ключ для LLM")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Основная модель для разработки кода"
    )

    # Специализированные модели для разных типов задач разработки
    llm_coding_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для написания кода"
    )
    llm_optimization_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Продвинутая модель для оптимизации кода"
    )
    llm_testing_model: str = Field(
        default="qwen2.5-coder-7b-instruct",
        description="Экономичная модель для генерации тестов"
    )
    llm_validation_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для валидации качества кода"
    )

    # Настройки разработки
    default_language: str = Field(
        default="python",
        description="Язык программирования по умолчанию"
    )
    default_framework: str = Field(
        default="fastapi",
        description="Фреймворк по умолчанию"
    )
    code_style_guide: str = Field(
        default="pep8",
        description="Руководство по стилю кода (pep8/google/airbnb)"
    )

    # Настройки качества кода
    quality_standard: str = Field(
        default="standard",
        description="Стандарт качества (basic/standard/high/enterprise)"
    )
    max_file_lines: int = Field(
        default=500,
        description="Максимальное количество строк в файле"
    )
    max_function_complexity: int = Field(
        default=10,
        description="Максимальная сложность функции"
    )
    min_test_coverage: float = Field(
        default=80.0,
        description="Минимальное покрытие тестами (%)"
    )

    # Настройки тестирования
    enable_unit_tests: bool = Field(
        default=True,
        description="Включить создание unit тестов"
    )
    enable_integration_tests: bool = Field(
        default=True,
        description="Включить создание интеграционных тестов"
    )
    enable_e2e_tests: bool = Field(
        default=False,
        description="Включить создание end-to-end тестов"
    )
    test_framework: str = Field(
        default="pytest",
        description="Фреймворк для тестирования (pytest/unittest/jest)"
    )

    # Настройки безопасности
    enable_security_checks: bool = Field(
        default=True,
        description="Включить проверки безопасности"
    )
    enable_dependency_scanning: bool = Field(
        default=True,
        description="Включить сканирование зависимостей"
    )
    security_level: str = Field(
        default="standard",
        description="Уровень безопасности (basic/standard/high)"
    )

    # Настройки производительности
    enable_performance_optimization: bool = Field(
        default=True,
        description="Включить оптимизацию производительности"
    )
    performance_target: str = Field(
        default="balanced",
        description="Цель оптимизации (memory/speed/balanced)"
    )
    enable_async_patterns: bool = Field(
        default=True,
        description="Использовать асинхронные паттерны"
    )

    # Настройки базы данных
    default_database: str = Field(
        default="postgresql",
        description="База данных по умолчанию"
    )
    use_orm: bool = Field(
        default=True,
        description="Использовать ORM"
    )
    orm_framework: str = Field(
        default="sqlalchemy",
        description="ORM фреймворк (sqlalchemy/prisma/mongoose)"
    )

    # Archon интеграция
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )
    archon_enabled: bool = Field(
        default=True,
        description="Включена ли интеграция с Archon"
    )

    # RAG и база знаний
    knowledge_base_enabled: bool = Field(
        default=True,
        description="Использование базы знаний для разработки"
    )
    rag_search_threshold: float = Field(
        default=0.8,
        description="Порог релевантности для RAG поиска"
    )

    # Настройки коллаборации
    collaborate_with_quality_guardian: bool = Field(
        default=True,
        description="Коллаборация с Quality Guardian"
    )
    collaborate_with_blueprint_architect: bool = Field(
        default=True,
        description="Коллаборация с Blueprint Architect"
    )
    auto_create_tasks: bool = Field(
        default=True,
        description="Автоматическое создание задач в Archon"
    )

    # Настройки CI/CD
    enable_cicd: bool = Field(
        default=True,
        description="Включить настройку CI/CD"
    )
    cicd_platform: str = Field(
        default="github_actions",
        description="Платформа CI/CD (github_actions/gitlab_ci/jenkins)"
    )
    enable_docker: bool = Field(
        default=True,
        description="Использовать Docker для контейнеризации"
    )

    # Настройки мониторинга и логирования
    enable_logging: bool = Field(
        default=True,
        description="Включить логирование"
    )
    log_level: str = Field(
        default="INFO",
        description="Уровень логирования"
    )
    enable_monitoring: bool = Field(
        default=False,
        description="Включить мониторинг производительности"
    )


def load_implementation_engineer_settings() -> ImplementationEngineerSettings:
    """Загрузить настройки Implementation Engineer."""
    load_dotenv()

    try:
        return ImplementationEngineerSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Implementation Engineer: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model(task_type: str = "coding"):
    """
    Получить сконфигурированную LLM модель для конкретного типа задач.

    Args:
        task_type: Тип задачи (coding, optimization, testing, validation)

    Returns:
        Сконфигурированная модель
    """
    settings = load_implementation_engineer_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    # Выбираем модель в зависимости от типа задачи
    model_mapping = {
        "coding": settings.llm_coding_model,
        "optimization": settings.llm_optimization_model,
        "testing": settings.llm_testing_model,
        "validation": settings.llm_validation_model,
        "general": settings.llm_model
    }

    selected_model = model_mapping.get(task_type, settings.llm_model)
    return OpenAIModel(selected_model, provider=provider)


def get_development_defaults():
    """Получить настройки разработки по умолчанию."""
    settings = load_implementation_engineer_settings()

    return {
        "language": settings.default_language,
        "framework": settings.default_framework,
        "code_style": settings.code_style_guide,
        "quality_standard": settings.quality_standard,
        "max_file_lines": settings.max_file_lines,
        "database": settings.default_database,
        "orm": settings.orm_framework if settings.use_orm else None,
        "async_enabled": settings.enable_async_patterns
    }


def get_quality_config():
    """Получить конфигурацию качества кода."""
    settings = load_implementation_engineer_settings()

    return {
        "standard": settings.quality_standard,
        "max_lines": settings.max_file_lines,
        "max_complexity": settings.max_function_complexity,
        "test_coverage": settings.min_test_coverage,
        "security_checks": settings.enable_security_checks,
        "performance_optimization": settings.enable_performance_optimization
    }


def get_testing_config():
    """Получить конфигурацию тестирования."""
    settings = load_implementation_engineer_settings()

    return {
        "unit_tests": settings.enable_unit_tests,
        "integration_tests": settings.enable_integration_tests,
        "e2e_tests": settings.enable_e2e_tests,
        "framework": settings.test_framework,
        "coverage_threshold": settings.min_test_coverage
    }


def get_security_config():
    """Получить конфигурацию безопасности."""
    settings = load_implementation_engineer_settings()

    return {
        "security_checks": settings.enable_security_checks,
        "dependency_scanning": settings.enable_dependency_scanning,
        "security_level": settings.security_level
    }


def get_performance_config():
    """Получить конфигурацию производительности."""
    settings = load_implementation_engineer_settings()

    return {
        "optimization_enabled": settings.enable_performance_optimization,
        "target": settings.performance_target,
        "async_patterns": settings.enable_async_patterns
    }


def get_collaboration_config():
    """Получить настройки коллаборации."""
    settings = load_implementation_engineer_settings()

    return {
        "quality_guardian": settings.collaborate_with_quality_guardian,
        "blueprint_architect": settings.collaborate_with_blueprint_architect,
        "auto_tasks": settings.auto_create_tasks,
        "archon_enabled": settings.archon_enabled,
        "archon_project_id": settings.archon_project_id
    }


def get_cicd_config():
    """Получить настройки CI/CD."""
    settings = load_implementation_engineer_settings()

    return {
        "enabled": settings.enable_cicd,
        "platform": settings.cicd_platform,
        "docker": settings.enable_docker,
        "logging": settings.enable_logging,
        "log_level": settings.log_level,
        "monitoring": settings.enable_monitoring
    }