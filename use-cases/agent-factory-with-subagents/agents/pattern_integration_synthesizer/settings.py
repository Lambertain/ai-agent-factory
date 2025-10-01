"""
Настройки для Pattern Integration Synthesizer Agent.
"""

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

    # LLM параметры
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(
        default="gpt-4o",
        description="Название модели"
    )
    llm_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="Базовый URL API"
    )

    # Archon интеграция
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )
    archon_api_url: str = Field(
        default="http://localhost:3737",
        description="URL Archon API"
    )

    # PatternShift пути
    patternshift_project_path: str = Field(
        default="",
        description="Путь к проекту PatternShift"
    )

    # Knowledge Base
    knowledge_tags: list = Field(
        default_factory=lambda: [
            "pattern-integration-synthesizer",
            "orchestration",
            "synergy",
            "agent-knowledge",
            "patternshift"
        ],
        description="Теги для поиска в базе знаний"
    )

    # Logging
    log_level: str = Field(default="INFO", description="Уровень логирования")
    verbose: bool = Field(default=True, description="Подробные логи")


def load_settings() -> Settings:
    """Загрузить настройки и проверить наличие переменных."""
    load_dotenv()

    try:
        return Settings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедись, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model():
    """Получить настроенную модель LLM."""
    from pydantic_ai.providers.openai import OpenAIProvider
    from pydantic_ai.models.openai import OpenAIModel

    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)


__all__ = ["Settings", "load_settings", "get_llm_model"]
