"""
Настройки для PWA Mobile Agent.

Загружает конфигурацию из environment variables.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv


class PWAMobileAgentSettings(BaseSettings):
    """Настройки PWA Mobile Agent с поддержкой переменных окружения."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Параметры LLM
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Модель для PWA разработки")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # PWA специфичные настройки
    pwa_app_name: str = Field(default="", description="Название PWA приложения")
    pwa_short_name: str = Field(default="", description="Короткое название PWA")
    pwa_description: str = Field(default="", description="Описание PWA приложения")
    pwa_theme_color: str = Field(default="#000000", description="Цвет темы PWA")
    pwa_background_color: str = Field(default="#ffffff", description="Цвет фона PWA")

    # Performance настройки
    pwa_max_cache_size: int = Field(default=50, description="Максимальный размер кэша в MB")
    pwa_cache_strategy: str = Field(default="adaptive", description="Стратегия кэширования")

    # Feature flags
    pwa_enable_push: bool = Field(default=True, description="Включить push notifications")
    pwa_enable_background_sync: bool = Field(default=True, description="Включить background sync")
    pwa_enable_geolocation: bool = Field(default=False, description="Включить geolocation API")
    pwa_enable_camera: bool = Field(default=False, description="Включить camera API")
    pwa_enable_share: bool = Field(default=True, description="Включить share API")
    pwa_enable_payment: bool = Field(default=False, description="Включить payment API")

    # Archon интеграция
    archon_url: str = Field(default="http://localhost:3737", description="URL Archon сервера")
    archon_project_id: str = Field(default="", description="ID проекта в Archon")


def load_settings() -> PWAMobileAgentSettings:
    """Загрузить настройки и проверить наличие переменных."""
    load_dotenv()

    try:
        return PWAMobileAgentSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки PWA Mobile Agent: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедись, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e