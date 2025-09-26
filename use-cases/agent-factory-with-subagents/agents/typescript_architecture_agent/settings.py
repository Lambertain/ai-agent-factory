"""Settings configuration for TypeScript Architecture Agent."""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import Optional


class Settings(BaseSettings):
    """Настройки TypeScript Architecture Agent с поддержкой переменных окружения."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ===== LLM CONFIGURATION =====
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # ===== COST-OPTIMIZED MODEL CONFIGURATION =====
    # Complex architectural tasks - Premium Qwen (только для сложного анализа)
    llm_architecture_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для архитектурного анализа"
    )

    # Specialized coding tasks - Qwen Coder models
    llm_coding_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для кодирования и рефакторинга"
    )

    # Text-based tasks - Ultra-cheap Gemini 2.5 Flash-Lite ($0.10-0.40/1M)
    llm_planning_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для планирования"
    )
    llm_validation_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для валидации"
    )

    # Alternative API keys for multi-provider setup
    gemini_api_key: str = Field(..., description="Google Gemini API ключ")

    # ===== TYPESCRIPT SPECIFIC SETTINGS =====
    typescript_strict_mode: bool = Field(
        default=True,
        description="Включить строгий режим TypeScript"
    )
    target_type_coverage: float = Field(
        default=0.95,
        description="Целевое покрытие типами (95%)"
    )
    max_complexity_score: int = Field(
        default=7,
        description="Максимальная допустимая сложность типов"
    )
    performance_budget_ms: int = Field(
        default=5000,
        description="Бюджет времени компиляции в миллисекундах"
    )

    # ===== PROJECT PATHS =====
    project_root: str = Field(
        default=".",
        description="Корневая директория проекта"
    )
    typescript_config_path: str = Field(
        default="tsconfig.json",
        description="Путь к конфигурации TypeScript"
    )
    types_directory: str = Field(
        default="src/types",
        description="Директория с типами"
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

    # ===== CACHING AND OPTIMIZATION =====
    enable_analysis_cache: bool = Field(
        default=True,
        description="Включить кэширование результатов анализа"
    )
    cache_ttl_seconds: int = Field(
        default=3600,
        description="Время жизни кэша в секундах"
    )

    # ===== REPORTING =====
    generate_reports: bool = Field(
        default=True,
        description="Генерировать отчеты об анализе"
    )
    reports_directory: str = Field(
        default="reports/typescript",
        description="Директория для отчетов"
    )


def load_settings() -> Settings:
    """
    Загрузить настройки и проверить наличие обязательных переменных.

    Returns:
        Настройки TypeScript Architecture Agent

    Raises:
        ValueError: Если отсутствуют обязательные переменные
    """
    load_dotenv()

    try:
        settings = Settings()

        # Проверка критичных настроек
        if not settings.llm_api_key:
            raise ValueError("LLM_API_KEY обязателен для работы агента")

        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY обязателен для cost-optimized моделей")

        return settings

    except Exception as e:
        error_msg = f"Не удалось загрузить настройки TypeScript Agent: {e}"

        if "llm_api_key" in str(e).lower():
            error_msg += "\n\nДобавьте в .env файл:"
            error_msg += "\nLLM_API_KEY=your_api_key_here"
            error_msg += "\nGEMINI_API_KEY=your_gemini_key_here"

        raise ValueError(error_msg) from e


# Экспорт настроек по умолчанию
default_settings = load_settings()