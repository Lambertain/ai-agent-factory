"""
Настройки для Pattern Exercise Architect Agent
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class PatternExerciseArchitectSettings(BaseSettings):
    """Настройки Pattern Exercise Architect Agent с поддержкой переменных окружения."""

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
        description="Название модели для дизайна упражнений"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Специфичные настройки агента
    agent_name: str = Field(default="pattern_exercise_architect", description="Имя агента")
    patternshift_project_path: str = Field(
        default="D:\\Automation\\Development\\projects\\patternshift",
        description="Путь к проекту PatternShift"
    )

    # Archon интеграция
    archon_project_id: str = Field(
        default="d5c0bd7d-8856-4ed3-98b1-561f80f7a299",
        description="ID проекта PatternShift в Archon"
    )


def load_settings() -> PatternExerciseArchitectSettings:
    """Загрузить настройки и проверить наличие переменных."""
    load_dotenv()

    try:
        return PatternExerciseArchitectSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Pattern Exercise Architect: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедись, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model():
    """Сконфигурировать модель LLM для Pattern Exercise Architect."""
    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)


__all__ = [
    "PatternExerciseArchitectSettings",
    "load_settings",
    "get_llm_model"
]
