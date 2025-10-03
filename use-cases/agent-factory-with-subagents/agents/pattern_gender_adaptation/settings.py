# -*- coding: utf-8 -*-
"""
Настройки Pattern Gender Adaptation Agent.

Конфигурация для адаптации психологического контента под гендерные особенности.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv


class PatternGenderAgentSettings(BaseSettings):
    """Настройки Pattern Gender Adaptation Agent."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM конфигурация
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API ключ провайдера")
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для гендерной адаптации"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # PatternShift интеграция
    patternshift_project_path: str = Field(
        default="D:\\Automation\\Development\\projects\\PatternShift",
        description="Путь к проекту PatternShift"
    )

    # Гендерная адаптация
    gender_versions: list = Field(
        default=["masculine", "feminine", "neutral"],
        description="Версии гендерной адаптации"
    )

    # Валидация стереотипов
    enable_stereotype_validation: bool = Field(
        default=True,
        description="Включить проверку на токсичные стереотипы"
    )

    # Archon интеграция
    archon_project_id: str = Field(
        default="",
        description="ID проекта в Archon (если используется)"
    )

    # Знания агента
    knowledge_tags: list = Field(
        default=["pattern-gender-adaptation", "gender-psychology", "pydantic-ai"],
        description="Теги для поиска в базе знаний"
    )
    knowledge_domain: str = Field(
        default="",
        description="Домен знаний (если есть)"
    )


def load_settings() -> PatternGenderAgentSettings:
    """
    Загрузить настройки агента.

    Returns:
        PatternGenderAgentSettings: Настройки агента
    """
    load_dotenv()

    try:
        return PatternGenderAgentSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедись, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model():
    """
    Получить сконфигурированную LLM модель.

    Returns:
        OpenAIModel: Настроенная модель
    """
    from pydantic_ai.providers.openai import OpenAIProvider
    from pydantic_ai.models.openai import OpenAIModel

    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)
