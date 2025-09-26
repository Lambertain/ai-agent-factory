#!/usr/bin/env python3
"""
Настройки для Archon Blueprint Architect Agent.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv


class BlueprintArchitectSettings(BaseSettings):
    """Настройки Blueprint Architect агента."""

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
        description="Модель для архитектурного проектирования"
    )

    # Специализированные модели для разных типов архитектурных задач
    llm_architecture_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Продвинутая модель для сложного архитектурного анализа"
    )
    llm_design_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для детального проектирования компонентов"
    )
    llm_validation_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Экономичная модель для валидации архитектуры"
    )

    # Настройки архитектурного проектирования
    default_architectural_pattern: str = Field(
        default="layered",
        description="Архитектурный паттерн по умолчанию"
    )
    default_scalability_level: str = Field(
        default="medium",
        description="Уровень масштабируемости по умолчанию"
    )
    max_components_per_blueprint: int = Field(
        default=15,
        description="Максимальное количество компонентов в одном чертеже"
    )

    # Настройки безопасности и производительности
    include_security_by_default: bool = Field(
        default=True,
        description="Включать слои безопасности по умолчанию"
    )
    include_monitoring_by_default: bool = Field(
        default=True,
        description="Включать компоненты мониторинга по умолчанию"
    )
    performance_optimization_level: str = Field(
        default="standard",
        description="Уровень оптимизации производительности (basic/standard/advanced)"
    )

    # Технологические предпочтения
    preferred_database_type: str = Field(
        default="postgresql",
        description="Предпочтительный тип базы данных"
    )
    preferred_cache_system: str = Field(
        default="redis",
        description="Предпочтительная система кэширования"
    )
    preferred_message_queue: str = Field(
        default="rabbitmq",
        description="Предпочтительная очередь сообщений"
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
        description="Использование базы архитектурных знаний"
    )
    rag_search_threshold: float = Field(
        default=0.7,
        description="Порог релевантности для RAG поиска"
    )

    # Настройки валидации архитектуры
    validation_strict_mode: bool = Field(
        default=False,
        description="Строгий режим валидации архитектуры"
    )
    auto_validate_blueprints: bool = Field(
        default=True,
        description="Автоматическая валидация создаваемых чертежей"
    )

    # Настройки документации
    generate_diagrams: bool = Field(
        default=True,
        description="Генерировать диаграммы архитектуры"
    )
    diagram_format: str = Field(
        default="mermaid",
        description="Формат диаграмм (mermaid/plantuml/drawio)"
    )
    include_deployment_docs: bool = Field(
        default=True,
        description="Включать документацию по развертыванию"
    )

    # Настройки коллаборации
    auto_delegate_implementation: bool = Field(
        default=True,
        description="Автоматически делегировать реализацию Implementation Engineer"
    )
    collaboration_mode: str = Field(
        default="interactive",
        description="Режим коллаборации (silent/interactive/verbose)"
    )


def load_blueprint_architect_settings() -> BlueprintArchitectSettings:
    """Загрузить настройки Blueprint Architect."""
    load_dotenv()

    try:
        return BlueprintArchitectSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Blueprint Architect: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model(task_type: str = "general"):
    """
    Получить сконфигурированную LLM модель для конкретного типа задач.

    Args:
        task_type: Тип задачи (general, architecture, design, validation)

    Returns:
        Сконфигурированная модель
    """
    settings = load_blueprint_architect_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    # Выбираем модель в зависимости от типа задачи
    model_mapping = {
        "general": settings.llm_model,
        "architecture": settings.llm_architecture_model,
        "design": settings.llm_design_model,
        "validation": settings.llm_validation_model
    }

    selected_model = model_mapping.get(task_type, settings.llm_model)
    return OpenAIModel(selected_model, provider=provider)


def get_architecture_defaults():
    """Получить архитектурные настройки по умолчанию."""
    settings = load_blueprint_architect_settings()

    return {
        "pattern": settings.default_architectural_pattern,
        "scalability": settings.default_scalability_level,
        "max_components": settings.max_components_per_blueprint,
        "security": settings.include_security_by_default,
        "monitoring": settings.include_monitoring_by_default,
        "performance_level": settings.performance_optimization_level,
        "database": settings.preferred_database_type,
        "cache": settings.preferred_cache_system,
        "queue": settings.preferred_message_queue
    }


def get_collaboration_config():
    """Получить настройки коллаборации."""
    settings = load_blueprint_architect_settings()

    return {
        "auto_delegate": settings.auto_delegate_implementation,
        "mode": settings.collaboration_mode,
        "archon_enabled": settings.archon_enabled,
        "archon_project_id": settings.archon_project_id
    }


def get_validation_config():
    """Получить настройки валидации."""
    settings = load_blueprint_architect_settings()

    return {
        "strict_mode": settings.validation_strict_mode,
        "auto_validate": settings.auto_validate_blueprints,
        "rag_threshold": settings.rag_search_threshold
    }


def get_documentation_config():
    """Получить настройки документации."""
    settings = load_blueprint_architect_settings()

    return {
        "generate_diagrams": settings.generate_diagrams,
        "diagram_format": settings.diagram_format,
        "include_deployment": settings.include_deployment_docs
    }