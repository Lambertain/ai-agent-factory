"""
Конфигурация LLM для Pattern Microhabit Designer Agent
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class Settings(BaseSettings):
    """Настройки агента с поддержкой переменных окружения"""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Параметры LLM
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для дизайна привычек"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Специализированные модели для разных задач
    llm_behavior_analysis_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для анализа поведения"
    )
    llm_habit_design_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для дизайна привычек"
    )

    # Параметры генерации
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Температура генерации")
    max_tokens: int = Field(default=2000, ge=100, le=4000, description="Максимум токенов")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p sampling")

    # PatternShift конфигурация
    patternshift_project_id: str = Field(
        default="d5c0bd7d-8856-4ed3-98b1-561f80f7a299",
        description="ID проекта PatternShift в Archon"
    )
    patternshift_project_path: str = Field(
        default="D:\\Automation\\Development\\projects\\patternshift",
        description="Путь к проекту PatternShift"
    )

    # RAG конфигурация
    enable_rag: bool = Field(default=True, description="Включить поиск через RAG")
    rag_match_count: int = Field(default=5, ge=1, le=10, description="Количество результатов RAG")

    # Параметры дизайна привычек
    default_habit_duration_seconds: int = Field(
        default=120,
        ge=30,
        le=600,
        description="Стандартная длительность микропривычки (секунды)"
    )
    max_habit_chain_length: int = Field(
        default=5,
        ge=2,
        le=10,
        description="Максимальная длина цепочки привычек"
    )
    min_success_probability: float = Field(
        default=0.7,
        ge=0.5,
        le=1.0,
        description="Минимальная вероятность успеха"
    )


def load_settings() -> Settings:
    """
    Загрузить настройки и проверить наличие переменных

    Returns:
        Settings: Загруженные настройки

    Raises:
        ValueError: Если не удалось загрузить настройки
    """
    load_dotenv()

    try:
        return Settings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедись, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model():
    """
    Сконфигурировать модель LLM с учётом настроек

    Returns:
        OpenAIModel: Сконфигурированная модель
    """
    settings = load_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(settings.llm_model, provider=provider)


def get_behavior_analysis_model():
    """
    Сконфигурировать модель для анализа поведения (более мощная)

    Returns:
        OpenAIModel: Модель для анализа поведения
    """
    settings = load_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(settings.llm_behavior_analysis_model, provider=provider)
