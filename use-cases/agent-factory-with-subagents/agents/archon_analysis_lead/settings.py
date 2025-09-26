#!/usr/bin/env python3
"""
Настройки для Archon Analysis Lead Agent.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv


class AnalysisLeadSettings(BaseSettings):
    """Настройки Analysis Lead агента."""

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
        description="Модель для анализа"
    )

    # Настройки агента
    max_analysis_depth: int = Field(default=4, description="Максимальная глубина анализа")
    default_granularity: str = Field(default="1-4 часа", description="Целевая детализация задач")

    # Archon интеграция
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )


def load_analysis_settings() -> AnalysisLeadSettings:
    """Загрузить настройки Analysis Lead."""
    load_dotenv()

    try:
        return AnalysisLeadSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Analysis Lead: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model():
    """Получить сконфигурированную LLM модель."""
    settings = load_analysis_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(settings.llm_model, provider=provider)