"""
Pattern NLP Technique Master Agent Settings

Конфигурация для создания модульных НЛП-техник трансформации.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import Optional


class PatternNLPTechniqueMasterSettings(BaseSettings):
    """Настройки Pattern NLP Technique Master Agent."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Основные настройки LLM
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Модель для кодирования")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Специализированные модели для NLP техник
    llm_technique_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для создания сложных НЛП техник"
    )
    llm_therapy_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для терапевтических техник"
    )
    llm_validation_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для валидации техник"
    )

    # Альтернативные API ключи
    gemini_api_key: Optional[str] = Field(default=None, description="Google Gemini API ключ")

    # Путь к проекту
    project_path: str = Field(
        default="D:\\Automation\\agent-factory\\use-cases\\agent-factory-with-subagents",
        description="Путь к проекту"
    )

    # Настройки Pattern NLP Technique Master
    default_technique_duration: int = Field(default=15, description="Длительность техники в минутах")
    enable_vak_adaptation: bool = Field(default=True, description="Включить VAK адаптацию")
    enable_cultural_adaptation: bool = Field(default=True, description="Включить культурную адаптацию")
    enable_safety_checks: bool = Field(default=True, description="Включить проверки безопасности")

    # Научная валидация
    require_evidence_base: bool = Field(default=True, description="Требовать научное обоснование")
    include_contraindications: bool = Field(default=True, description="Включать противопоказания")
    enable_crisis_detection: bool = Field(default=True, description="Включить обнаружение кризиса")

    # Персонализация
    enable_user_profiling: bool = Field(default=True, description="Включить профилирование пользователя")
    adaptive_difficulty: bool = Field(default=True, description="Адаптивная сложность")
    track_progress: bool = Field(default=True, description="Отслеживать прогресс")

    # Интеграция с PatternShift
    patternshift_api_url: Optional[str] = Field(default=None, description="URL API PatternShift")
    patternshift_api_key: Optional[str] = Field(default=None, description="API ключ PatternShift")

    # Модули и форматы
    default_output_format: str = Field(default="structured_json", description="Формат вывода по умолчанию")
    enable_multimodal_output: bool = Field(default=True, description="Мультимодальный вывод")
    include_audio_scripts: bool = Field(default=True, description="Включать аудио скрипты")

    # Безопасность и этика
    ethical_guidelines_check: bool = Field(default=True, description="Проверка этических принципов")
    informed_consent_required: bool = Field(default=True, description="Требовать информированное согласие")
    confidentiality_protection: bool = Field(default=True, description="Защита конфиденциальности")

    # RAG и база знаний
    enable_knowledge_search: bool = Field(default=True, description="Включить поиск в базе знаний")
    knowledge_search_threshold: float = Field(default=0.7, description="Порог релевантности для поиска")
    max_knowledge_results: int = Field(default=5, description="Максимум результатов поиска")

    # Архитектура техник
    modular_technique_structure: bool = Field(default=True, description="Модульная структура техник")
    versioned_techniques: bool = Field(default=True, description="Версионирование техник")
    technique_immutability: bool = Field(default=True, description="Неизменяемость техник")


def load_settings() -> PatternNLPTechniqueMasterSettings:
    """
    Загрузить настройки Pattern NLP Technique Master Agent.

    Returns:
        Настройки агента

    Raises:
        ValueError: Если не удалось загрузить настройки
    """
    load_dotenv()

    try:
        return PatternNLPTechniqueMasterSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Pattern NLP Technique Master: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедись, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


# Глобальный экземпляр настроек
_settings: Optional[PatternNLPTechniqueMasterSettings] = None


def get_settings() -> PatternNLPTechniqueMasterSettings:
    """Получить глобальный экземпляр настроек."""
    global _settings
    if _settings is None:
        _settings = load_settings()
    return _settings