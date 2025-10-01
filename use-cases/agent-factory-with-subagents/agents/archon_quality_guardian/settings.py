# -*- coding: utf-8 -*-
"""
Настройки для Archon Quality Guardian Agent
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv

class QualityGuardianSettings(BaseSettings):
    """Настройки агента Quality Guardian."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM Configuration
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API ключ провайдера")
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для code review"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Quality Check Configuration
    test_coverage_threshold: float = Field(default=80.0, ge=0.0, le=100.0)
    complexity_threshold: int = Field(default=10, ge=1)
    maintainability_threshold: float = Field(default=50.0, ge=0.0, le=100.0)

    # Security Configuration
    security_scan_enabled: bool = Field(default=True)
    security_severity_threshold: str = Field(default="medium")

    # CI/CD Integration
    github_token: str = Field(default="", description="GitHub API token")
    gitlab_token: str = Field(default="", description="GitLab API token")

    # Archon Integration
    archon_api_url: str = Field(default="http://localhost:3737", description="URL Archon API")
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )

    # Tools Configuration
    enable_auto_fix: bool = Field(default=True, description="Включить автоисправление")
    enable_ai_review: bool = Field(default=True, description="Включить AI code review")

def load_settings() -> QualityGuardianSettings:
    """Загрузить настройки агента."""
    load_dotenv()

    try:
        return QualityGuardianSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедись, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e
