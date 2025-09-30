"""
Настройки для Pattern Ericksonian Hypnosis Scriptwriter Agent
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class Settings(BaseSettings):
    """Настройки агента с поддержкой переменных окружения."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Параметры LLM
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Название модели")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Настройки PatternShift проекта
    patternshift_project_path: str = Field(
        default="D:/Automation/Development/projects/patternshift",
        description="Путь к проекту PatternShift"
    )

    # Настройки RAG
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )
    knowledge_domain: str = Field(
        default="patternshift.com",
        description="Домен знаний агента"
    )

    # Настройки гипнотических скриптов
    default_trance_depth: str = Field(
        default="medium",
        description="Глубина транса по умолчанию (light/medium/deep)"
    )
    default_duration_minutes: int = Field(
        default=20,
        description="Длительность скрипта по умолчанию в минутах"
    )
    safety_checks_enabled: bool = Field(
        default=True,
        description="Включить проверки безопасности тем"
    )


def load_settings() -> Settings:
    """Загрузить настройки и проверить наличие переменных."""
    load_dotenv()

    try:
        return Settings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model():
    """Сконфигурировать модель LLM с учетом настроек."""
    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)