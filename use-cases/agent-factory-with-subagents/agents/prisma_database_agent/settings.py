"""Настройки для Prisma Database Agent."""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Настройки агента с поддержкой переменных окружения."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ===== LLM CONFIGURATION =====
    # Qwen API (via DashScope)
    llm_api_key: str = Field(..., description="API ключ для Qwen через DashScope")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL для Qwen API"
    )

    # Google Gemini API
    gemini_api_key: str = Field(..., description="Google Gemini API ключ")

    # ===== MODEL SELECTION =====
    # Database architecture analysis (complex tasks) - Premium Qwen
    llm_architecture_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для архитектурного анализа БД"
    )

    # SQL generation and optimization - Qwen Coder
    llm_coding_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для генерации SQL и оптимизации"
    )

    # Migration planning and documentation - Ultra-cheap Gemini
    llm_planning_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для планирования миграций"
    )

    llm_validation_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для валидации изменений"
    )

    # ===== DATABASE SETTINGS =====
    # PostgreSQL configuration
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/your_database",
        description="URL подключения к PostgreSQL"
    )

    # Prisma configuration
    prisma_schema_path: str = Field(
        default="prisma/schema.prisma",
        description="Путь к файлу схемы Prisma"
    )

    prisma_migration_path: str = Field(
        default="prisma/migrations",
        description="Путь к папке миграций Prisma"
    )

    # Performance settings
    slow_query_threshold_ms: float = Field(
        default=1000.0,
        description="Порог медленных запросов в миллисекундах"
    )

    max_query_complexity: int = Field(
        default=10,
        description="Максимальная сложность запросов"
    )

    connection_pool_size: int = Field(
        default=10,
        description="Размер пула соединений"
    )

    # ===== PROJECT PATHS =====
    project_root: str = Field(default=".", description="Корень проекта")
    backup_directory: str = Field(
        default="backups/database",
        description="Папка для backup'ов базы данных"
    )

    # ===== ARCHON INTEGRATION =====
    archon_url: str = Field(
        default="http://localhost:3737",
        description="URL Archon MCP сервера"
    )

    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )

    # ===== OPTIMIZATION SETTINGS =====
    enable_query_cache: bool = Field(
        default=True,
        description="Включить кэширование запросов"
    )

    enable_connection_pooling: bool = Field(
        default=True,
        description="Включить connection pooling"
    )

    enable_prepared_statements: bool = Field(
        default=True,
        description="Включить prepared statements"
    )

    auto_analyze_schema: bool = Field(
        default=True,
        description="Автоматический анализ схемы при изменениях"
    )

    generate_migration_backups: bool = Field(
        default=True,
        description="Создавать backup'ы перед миграциями"
    )

    # ===== LOGGING & MONITORING =====
    enable_query_logging: bool = Field(
        default=True,
        description="Включить логирование запросов"
    )

    log_slow_queries: bool = Field(
        default=True,
        description="Логировать медленные запросы"
    )

    enable_performance_monitoring: bool = Field(
        default=True,
        description="Включить мониторинг производительности"
    )


def load_settings() -> Settings:
    """Загрузить настройки и проверить наличие обязательных переменных."""
    load_dotenv()

    try:
        return Settings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Prisma Database Agent: {e}"

        if "llm_api_key" in str(e).lower():
            error_msg += "\n\nПроверьте наличие следующих переменных в .env файле:"
            error_msg += "\n- LLM_API_KEY (для Qwen через DashScope)"
            error_msg += "\n- GEMINI_API_KEY (для Google Gemini)"

        if "database_url" in str(e).lower():
            error_msg += "\n- DATABASE_URL (для подключения к PostgreSQL)"

        raise ValueError(error_msg) from e


# Экспорт
__all__ = ["Settings", "load_settings"]