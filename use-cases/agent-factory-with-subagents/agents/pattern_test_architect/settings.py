"""
Настройки для Pattern Test Architect Agent
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

# Загружаем переменные окружения
load_dotenv()

class PatternTestArchitectSettings(BaseSettings):
    """Настройки приложения с поддержкой переменных окружения."""

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

    # Специализированные модели для Pattern Test Architect
    llm_psychometry_model: str = Field(default="qwen2.5-72b-instruct", description="Модель для психометрии")
    llm_test_generation_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Модель для генерации тестов")

    # Пути проекта
    project_path: str = Field(default="", description="Путь к проекту")

    # Настройки Pattern Test Architect
    agent_name: str = "Pattern Test Architect"
    agent_version: str = "1.0.0"
    agent_description: str = "Эксперт по созданию психологических тестов и диагностических инструментов"

    # Модель AI для агента
    temperature: float = 0.7
    max_tokens: int = 4000

    # Настройки создания тестов
    default_question_count: int = 15
    max_question_count: int = 50
    min_question_count: int = 5

    default_result_ranges: int = 5
    max_result_ranges: int = 10
    min_result_ranges: int = 3

    # Пороговые значения качества
    min_validity_score: float = 0.7
    min_reliability_score: float = 0.7
    min_clarity_score: float = 0.6
    min_viral_score: float = 0.5

    # Языковые настройки
    default_language: str = "ru"
    supported_languages: List[str] = field(default_factory=lambda: ["ru", "uk", "en"])

    # Настройки валидации
    enable_psychometric_validation: bool = True
    enable_ethical_compliance_check: bool = True
    enable_viral_potential_analysis: bool = True

    # Безопасность и этика
    restricted_constructs: List[str] = field(default_factory=lambda: [
        "суицидальность",
        "психоз",
        "шизофрения",
        "биполярное_расстройство",
        "посттравматическое_стрессовое_расстройство"
    ])

    age_restricted_content: Dict[str, int] = field(default_factory=lambda: {
        "depression_assessment": 16,
        "anxiety_assessment": 14,
        "personality_assessment": 18,
        "relationship_assessment": 16
    })

    # Настройки интеграции
    enable_transformation_program_linking: bool = True
    auto_generate_recommendations: bool = True
    enable_cultural_adaptation: bool = True

    # Кэширование
    cache_psychometric_data: bool = True
    cache_viral_patterns: bool = True
    cache_ttl_hours: int = 24

    # Метрики и аналитика
    track_test_effectiveness: bool = True
    track_completion_rates: bool = True
    track_viral_metrics: bool = True

    # Экспорт и интеграция
    export_formats: List[str] = field(default_factory=lambda: ["json", "yaml", "xml"])
    api_integration_enabled: bool = True

    # Настройки базы данных
    psychometric_db_path: str = "data/psychometric_methodologies.json"
    viral_patterns_db_path: str = "data/viral_patterns.json"
    programs_registry_path: str = "data/transformation_programs.json"

    # Настройки логирования
    log_level: str = "INFO"
    log_test_creations: bool = True
    log_validation_results: bool = True

    # Производительность
    max_concurrent_validations: int = 5
    validation_timeout_seconds: int = 30
    question_generation_batch_size: int = 10

    # Культурная адаптация
    default_cultural_context: str = "russian_speaking"
    cultural_adaptation_enabled: bool = True
    cultural_sensitivity_check: bool = True

    # Вирусные метрики
    viral_score_weights: Dict[str, float] = field(default_factory=lambda: {
        "emotional_trigger": 0.3,
        "curiosity_gap": 0.25,
        "personal_relevance": 0.25,
        "shareability": 0.2
    })

    # Шаблоны вопросов
    question_templates_enabled: bool = True
    custom_templates_path: str = "templates/questions"

    # Качество контента
    auto_readability_check: bool = True
    target_reading_level: str = "8th_grade"  # Уровень чтения 8 класса
    max_sentence_length: int = 20  # Максимальная длина предложения в словах

    # Интерпретации результатов
    interpretation_min_length: int = 100  # Минимальная длина интерпретации в символах
    interpretation_max_length: int = 500  # Максимальная длина
    recommendations_count: int = 5  # Количество рекомендаций

    # A/B тестирование
    enable_ab_testing: bool = False
    ab_test_variants: int = 2

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование настроек в словарь"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PatternTestArchitectSettings":
        """Создание настроек из словаря"""
        return cls(**data)

    def validate_settings(self) -> List[str]:
        """Валидация настроек"""
        issues = []

        # Проверка числовых значений
        if self.min_question_count >= self.max_question_count:
            issues.append("min_question_count должно быть меньше max_question_count")

        if self.min_result_ranges >= self.max_result_ranges:
            issues.append("min_result_ranges должно быть меньше max_result_ranges")

        # Проверка пороговых значений
        if not (0.0 <= self.min_validity_score <= 1.0):
            issues.append("min_validity_score должно быть между 0.0 и 1.0")

        if not (0.0 <= self.temperature <= 2.0):
            issues.append("temperature должно быть между 0.0 и 2.0")

        # Проверка путей к файлам
        required_paths = [
            self.psychometric_db_path,
            self.viral_patterns_db_path,
            self.programs_registry_path
        ]

        for path in required_paths:
            if not path:
                issues.append(f"Путь {path} не может быть пустым")

        return issues


def load_settings() -> PatternTestArchitectSettings:
    """Загрузить настройки и проверить наличие переменных."""
    load_dotenv()

    try:
        return PatternTestArchitectSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедись, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e

def get_llm_model():
    """Сконфигурировать модель LLM с учётом настроек."""
    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)

# Глобальный экземпляр настроек
settings = load_settings()


# Предустановленные конфигурации
PRODUCTION_CONFIG = PatternTestArchitectSettings(
    agent_version="1.0.0",
    temperature=0.5,
    enable_ethical_compliance_check=True,
    enable_psychometric_validation=True,
    log_level="WARNING",
    cache_ttl_hours=48
)

DEVELOPMENT_CONFIG = PatternTestArchitectSettings(
    agent_version="1.0.0-dev",
    temperature=0.8,
    log_level="DEBUG",
    cache_ttl_hours=1,
    enable_ab_testing=True
)

TEST_CONFIG = PatternTestArchitectSettings(
    agent_version="1.0.0-test",
    temperature=0.9,
    log_level="DEBUG",
    cache_ttl_hours=0,
    max_concurrent_validations=1,
    validation_timeout_seconds=5
)