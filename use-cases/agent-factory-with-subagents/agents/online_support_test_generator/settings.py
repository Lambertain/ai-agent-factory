"""
Конфигурация и настройки для Psychology Test Generator Agent
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from typing import Optional, List
import os


class PsychologyTestGeneratorSettings(BaseSettings):
    """Настройки для агента генерации психологических тестов."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Основные параметры LLM
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Модель для генерации")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Специализированные модели для разных задач
    llm_analysis_model: str = Field(default="qwen2.5-72b-instruct", description="Модель для анализа")
    llm_validation_model: str = Field(default="qwen2.5-coder-7b-instruct", description="Модель для валидации")

    # Настройки генерации тестов
    default_psychological_domain: str = Field(default="general", description="Психологический домен по умолчанию")
    default_target_population: str = Field(default="adults", description="Целевая популяция по умолчанию")
    default_test_type: str = Field(default="assessment", description="Тип теста по умолчанию")
    default_measurement_purpose: str = Field(default="screening", description="Цель измерения по умолчанию")

    # Ограничения качества
    min_question_count: int = Field(default=5, description="Минимальное количество вопросов")
    max_question_count: int = Field(default=100, description="Максимальное количество вопросов")
    min_reliability_threshold: float = Field(default=0.70, description="Минимальный порог надежности")
    max_reliability_threshold: float = Field(default=0.95, description="Максимальный порог надежности")

    # RAG и Archon интеграция
    archon_project_id: str = Field(default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a", description="ID проекта в Archon")
    enable_rag_search: bool = Field(default=True, description="Включить поиск в базе знаний")
    rag_match_count: int = Field(default=5, description="Количество результатов RAG поиска")

    # Поддерживаемые форматы ответов
    supported_response_formats: List[str] = Field(
        default_factory=lambda: ["likert_5", "likert_7", "frequency", "intensity", "binary", "multiple_choice"],
        description="Поддерживаемые форматы ответов"
    )

    # Поддерживаемые языковые уровни
    supported_language_levels: List[str] = Field(
        default_factory=lambda: ["grade_6", "grade_8", "grade_10", "professional"],
        description="Поддерживаемые уровни языка"
    )

    # Поддерживаемые популяции
    supported_populations: List[str] = Field(
        default_factory=lambda: ["children", "adolescents", "adults", "elderly", "special_needs"],
        description="Поддерживаемые целевые популяции"
    )

    # Настройки файловой структуры
    output_directory: str = Field(default="./generated_tests", description="Директория для сохранения тестов")
    knowledge_directory: str = Field(default="./knowledge", description="Директория с базой знаний")
    templates_directory: str = Field(default="./templates", description="Директория с шаблонами")

    # Настройки валидации
    enable_automatic_validation: bool = Field(default=True, description="Автоматическая валидация тестов")
    enable_psychometric_analysis: bool = Field(default=True, description="Психометрический анализ")
    enable_bias_detection: bool = Field(default=True, description="Обнаружение предвзятостей")
    enable_readability_check: bool = Field(default=True, description="Проверка читабельности")

    # Настройки экспорта
    supported_export_formats: List[str] = Field(
        default_factory=lambda: ["json", "yaml", "csv", "pdf", "html"],
        description="Поддерживаемые форматы экспорта"
    )

    # Интеграция с другими агентами
    enable_research_integration: bool = Field(default=True, description="Интеграция с Psychology Research Agent")
    enable_architect_collaboration: bool = Field(default=True, description="Работа с Psychology Content Architect")
    enable_quality_assurance: bool = Field(default=True, description="Проверка через Psychology Quality Guardian")

    # Мультиязычная поддержка
    default_language: str = Field(default="ru", description="Язык по умолчанию")
    supported_languages: List[str] = Field(
        default_factory=lambda: ["ru", "en", "es", "fr", "de"],
        description="Поддерживаемые языки"
    )

    # Настройки безопасности и этики
    enable_ethics_check: bool = Field(default=True, description="Проверка этических принципов")
    enable_confidentiality_protection: bool = Field(default=True, description="Защита конфиденциальности")
    enable_informed_consent: bool = Field(default=True, description="Информированное согласие")

    # Настройки производительности
    max_concurrent_generations: int = Field(default=3, description="Максимум параллельных генераций")
    generation_timeout_seconds: int = Field(default=300, description="Таймаут генерации в секундах")
    cache_enabled: bool = Field(default=True, description="Включить кэширование")

    def __post_init__(self):
        """Постинициализация настроек."""
        # Создание необходимых директорий
        os.makedirs(self.output_directory, exist_ok=True)
        os.makedirs(self.knowledge_directory, exist_ok=True)
        os.makedirs(self.templates_directory, exist_ok=True)


def load_settings() -> PsychologyTestGeneratorSettings:
    """
    Загрузить настройки агента.

    Returns:
        PsychologyTestGeneratorSettings: Настройки агента

    Raises:
        ValueError: Если не удалось загрузить обязательные настройки
    """
    load_dotenv()

    try:
        settings = PsychologyTestGeneratorSettings()
        settings.__post_init__()
        return settings
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Psychology Test Generator: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model(model_type: str = "default") -> OpenAIModel:
    """
    Получить сконфигурированную модель LLM.

    Args:
        model_type: Тип модели ('default', 'analysis', 'validation')

    Returns:
        OpenAIModel: Сконфигурированная модель
    """
    settings = load_settings()

    # Выбор модели в зависимости от типа задачи
    model_map = {
        "default": settings.llm_model,
        "analysis": settings.llm_analysis_model,
        "validation": settings.llm_validation_model
    }

    model_name = model_map.get(model_type, settings.llm_model)

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(model_name, provider=provider)


def get_domain_specific_settings(domain: str) -> dict:
    """
    Получить настройки, специфичные для психологического домена.

    Args:
        domain: Психологический домен

    Returns:
        dict: Специфичные настройки
    """
    domain_settings = {
        "anxiety": {
            "preferred_response_format": "frequency",
            "typical_question_count": 21,
            "reliability_threshold": 0.85,
            "specialized_subscales": ["general_anxiety", "social_anxiety", "panic", "worry"]
        },
        "depression": {
            "preferred_response_format": "frequency",
            "typical_question_count": 18,
            "reliability_threshold": 0.88,
            "specialized_subscales": ["mood", "anhedonia", "cognitive", "somatic"]
        },
        "personality": {
            "preferred_response_format": "likert_7",
            "typical_question_count": 50,
            "reliability_threshold": 0.80,
            "specialized_subscales": ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"]
        },
        "trauma": {
            "preferred_response_format": "intensity",
            "typical_question_count": 25,
            "reliability_threshold": 0.85,
            "specialized_subscales": ["trauma_exposure", "ptsd_symptoms", "dissociation", "functional_impact"]
        },
        "stress": {
            "preferred_response_format": "frequency",
            "typical_question_count": 20,
            "reliability_threshold": 0.82,
            "specialized_subscales": ["stress_sources", "stress_response", "coping_ability", "stress_impact"]
        }
    }

    return domain_settings.get(domain, {
        "preferred_response_format": "likert_5",
        "typical_question_count": 20,
        "reliability_threshold": 0.80,
        "specialized_subscales": ["main_factor"]
    })


def get_population_specific_settings(population: str) -> dict:
    """
    Получить настройки, специфичные для целевой популяции.

    Args:
        population: Целевая популяция

    Returns:
        dict: Специфичные настройки
    """
    population_settings = {
        "children": {
            "language_level": "grade_6",
            "max_question_count": 15,
            "time_limit_minutes": 10,
            "visual_aids_required": True,
            "parental_consent_required": True
        },
        "adolescents": {
            "language_level": "grade_8",
            "max_question_count": 25,
            "time_limit_minutes": 15,
            "privacy_emphasis": True,
            "peer_relevant_examples": True
        },
        "adults": {
            "language_level": "grade_10",
            "max_question_count": 50,
            "time_limit_minutes": 20,
            "professional_terminology_allowed": True
        },
        "elderly": {
            "language_level": "grade_8",
            "max_question_count": 20,
            "time_limit_minutes": 25,
            "large_font_recommended": True,
            "simplified_technology": True
        },
        "special_needs": {
            "language_level": "grade_6",
            "max_question_count": 15,
            "time_limit_minutes": 30,
            "accessibility_features_required": True,
            "flexible_administration": True
        }
    }

    return population_settings.get(population, {
        "language_level": "grade_8",
        "max_question_count": 30,
        "time_limit_minutes": 15
    })


# Константы конфигурации
DEFAULT_RESPONSE_FORMATS = {
    "likert_5": {
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Совершенно не согласен", "Не согласен", "Нейтрально", "Согласен", "Полностью согласен"],
        "neutral_point": 3
    },
    "likert_7": {
        "scale": [1, 2, 3, 4, 5, 6, 7],
        "labels": ["Совершенно не согласен", "Не согласен", "Скорее не согласен", "Нейтрально",
                  "Скорее согласен", "Согласен", "Полностью согласен"],
        "neutral_point": 4
    },
    "frequency": {
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
        "neutral_point": 3
    },
    "intensity": {
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Совсем не беспокоит", "Слегка беспокоит", "Умеренно беспокоит",
                  "Сильно беспокоит", "Очень сильно беспокоит"],
        "neutral_point": 3
    }
}

PSYCHOMETRIC_STANDARDS = {
    "reliability_thresholds": {
        "clinical": 0.85,
        "research": 0.80,
        "screening": 0.75,
        "experimental": 0.70
    },
    "validity_requirements": {
        "content": "Expert review and theoretical alignment",
        "construct": "Factor analysis and convergent/discriminant validity",
        "criterion": "Correlation with established measures",
        "predictive": "Longitudinal outcome prediction"
    },
    "sample_size_recommendations": {
        "pilot": 50,
        "development": 200,
        "validation": 500,
        "normalization": 1000
    }
}