# -*- coding: utf-8 -*-
"""
Настройки Pattern Age Adaptation Agent.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os


class PatternAgeAgentSettings(BaseSettings):
    """Настройки Pattern Age Adaptation Agent."""

    # LLM настройки
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель LLM для агента"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Base URL для LLM API"
    )
    llm_api_key: str = Field(
        default="",
        description="API ключ для LLM (берется из env)"
    )

    # PatternShift пути
    patternshift_project_path: str = Field(
        default="D:\\Automation\\Development\\projects\\PatternShift",
        description="Путь к проекту PatternShift"
    )

    # Возрастные версии
    age_versions: List[str] = Field(
        default=["teens", "young_adults", "early_middle_age", "middle_age", "seniors"],
        description="Возрастные версии для адаптации"
    )

    age_ranges: dict = Field(
        default={
            "teens": "14-18",
            "young_adults": "19-25",
            "early_middle_age": "26-35",
            "middle_age": "36-50",
            "seniors": "50+"
        },
        description="Возрастные диапазоны"
    )

    developmental_tasks: dict = Field(
        default={
            "teens": "identity_formation",
            "young_adults": "intimacy_vs_isolation",
            "early_middle_age": "generativity_beginning",
            "middle_age": "generativity_peak",
            "seniors": "integrity_vs_despair"
        },
        description="Задачи развития по Эриксону"
    )

    # Валидация
    enable_developmental_validation: bool = Field(
        default=True,
        description="Включить валидацию соответствия задачам развития"
    )

    # RAG и база знаний (для интеграции с Archon)
    knowledge_tags: List[str] = Field(
        default=[
            "pattern-age-adaptation",
            "developmental-psychology",
            "erikson",
            "lifespan-development",
            "pydantic-ai",
            "patternshift"
        ],
        description="Теги для поиска знаний"
    )

    knowledge_domain: str = Field(
        default="",
        description="Домен знаний агента"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_settings() -> PatternAgeAgentSettings:
    """
    Загрузить настройки агента из env файла.

    Returns:
        Объект настроек
    """
    settings = PatternAgeAgentSettings()

    # API ключ из переменной окружения
    if not settings.llm_api_key:
        settings.llm_api_key = os.getenv("DASHSCOPE_API_KEY", "")

    return settings


def get_llm_model():
    """
    Получить настроенную модель LLM.

    Returns:
        Настроенная модель для Pydantic AI
    """
    from pydantic_ai.models.openai import OpenAIModel

    settings = load_settings()

    return OpenAIModel(
        settings.llm_model,
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
