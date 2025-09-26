"""
Настройки для Psychology Research Agent

Универсальная система настроек для агента валидации психологических исследований
с поддержкой различных доменов и типов исследований.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
import os


class PsychologyResearchAgentSettings(BaseSettings):
    """
    Настройки для Psychology Research Agent.

    Поддерживает конфигурацию для различных типов исследований и доменов психологии.
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ===== ОСНОВНЫЕ НАСТРОЙКИ LLM =====
    llm_provider: str = Field(default="qwen", description="Провайдер LLM (qwen, openai, gemini)")
    llm_api_key: str = Field(..., description="API-ключ основного провайдера")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL для Qwen API"
    )

    # ===== СПЕЦИАЛИЗИРОВАННЫЕ МОДЕЛИ ДЛЯ ИССЛЕДОВАНИЙ =====
    # Основная модель для анализа исследований
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Основная модель для анализа исследований"
    )

    # Модель для методологического анализа (требует высокой точности)
    methodology_analysis_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для глубокого методологического анализа"
    )

    # Модель для статистической валидации
    statistical_validation_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для статистического анализа"
    )

    # Модель для литературного обзора (экономичная)
    literature_review_model: str = Field(
        default="qwen2.5-coder-7b-instruct",
        description="Модель для поиска и анализа литературы"
    )

    # Модель для создания отчетов (очень экономичная)
    reporting_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для генерации отчетов"
    )

    # ===== ДОПОЛНИТЕЛЬНЫЕ API КЛЮЧИ =====
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API ключ (опционально)")
    gemini_api_key: Optional[str] = Field(default=None, description="Google Gemini API ключ")

    # ===== ИССЛЕДОВАТЕЛЬСКИЕ НАСТРОЙКИ =====
    # Тип исследовательского домена
    research_domain: str = Field(
        default="general",
        description="Домен исследований (clinical, cognitive, social, developmental, educational)"
    )

    # Уровень строгости валидации
    validation_level: str = Field(
        default="standard",
        description="Уровень валидации (basic, standard, rigorous, publication_grade)"
    )

    # Целевая популяция исследований
    target_population: str = Field(
        default="adults",
        description="Целевая популяция (adults, children, adolescents, elderly, clinical, mixed)"
    )

    # Тип методологии
    methodology_focus: str = Field(
        default="quantitative",
        description="Фокус методологии (quantitative, qualitative, mixed_methods)"
    )

    # ===== НАСТРОЙКИ КАЧЕСТВА ИССЛЕДОВАНИЙ =====
    # Минимальные требования к качеству
    min_sample_size: int = Field(default=30, description="Минимальный размер выборки")
    min_effect_size: float = Field(default=0.2, description="Минимальный размер эффекта")
    min_power: float = Field(default=0.8, description="Минимальная статистическая мощность")
    alpha_level: float = Field(default=0.05, description="Уровень альфа для статистических тестов")

    # Требования к валидности инструментов
    min_reliability: float = Field(default=0.7, description="Минимальная надежность (Cronbach's α)")
    min_validity_coefficient: float = Field(default=0.3, description="Минимальный коэффициент валидности")

    # ===== СТАНДАРТЫ СООТВЕТСТВИЯ =====
    # Стандарты отчетности
    reporting_standards: List[str] = Field(
        default_factory=lambda: ["CONSORT", "STROBE", "PRISMA", "STARD"],
        description="Применяемые стандарты отчетности"
    )

    # Этические стандарты
    ethics_standards: List[str] = Field(
        default_factory=lambda: ["APA_Ethics", "Declaration_of_Helsinki", "Belmont_Report"],
        description="Этические стандарты для соблюдения"
    )

    # Статистические стандарты
    statistical_standards: List[str] = Field(
        default_factory=lambda: ["APA_Style", "CONSORT_Statistical", "ASA_Guidelines"],
        description="Статистические стандарты отчетности"
    )

    # ===== RAG И БАЗА ЗНАНИЙ =====
    # Настройки для поиска литературы
    literature_search_databases: List[str] = Field(
        default_factory=lambda: ["PubMed", "PsycINFO", "Cochrane", "Web_of_Science"],
        description="Базы данных для поиска литературы"
    )

    # Теги для поиска в базе знаний
    knowledge_search_tags: List[str] = Field(
        default_factory=lambda: ["research", "methodology", "statistics", "psychology"],
        description="Теги для поиска в базе знаний"
    )

    # Домен знаний для RAG
    knowledge_domain: Optional[str] = Field(
        default="psychology.research",
        description="Домен знаний для фильтрации RAG"
    )

    # ===== НАСТРОЙКИ ПРОИЗВОДИТЕЛЬНОСТИ =====
    # Размеры пакетов для обработки
    batch_size_studies: int = Field(default=10, description="Размер пакета для анализа исследований")
    batch_size_literature: int = Field(default=50, description="Размер пакета для литературного поиска")

    # Таймауты
    analysis_timeout: int = Field(default=300, description="Таймаут анализа исследования (секунды)")
    search_timeout: int = Field(default=60, description="Таймаут поиска литературы (секунды)")

    # Кэширование
    enable_caching: bool = Field(default=True, description="Включить кэширование результатов")
    cache_duration: int = Field(default=3600, description="Длительность кэша (секунды)")

    # ===== СПЕЦИФИЧНЫЕ НАСТРОЙКИ ПО ДОМЕНАМ =====
    # Клинические исследования
    clinical_requirements: Dict[str, Any] = Field(
        default_factory=lambda: {
            "min_sample_size": 100,
            "control_group_required": True,
            "randomization_required": True,
            "blinding_preferred": True,
            "ethical_approval_required": True,
            "adverse_events_monitoring": True
        },
        description="Требования для клинических исследований"
    )

    # Когнитивные исследования
    cognitive_requirements: Dict[str, Any] = Field(
        default_factory=lambda: {
            "min_sample_size": 30,
            "reaction_time_outliers": "3SD",
            "counterbalancing_required": True,
            "practice_trials_required": True,
            "ceiling_floor_threshold": 0.15
        },
        description="Требования для когнитивных исследований"
    )

    # Социальные исследования
    social_requirements: Dict[str, Any] = Field(
        default_factory=lambda: {
            "min_sample_size": 50,
            "cultural_diversity_required": True,
            "social_desirability_control": True,
            "demand_characteristics_minimized": True,
            "ecological_validity_considered": True
        },
        description="Требования для социальных исследований"
    )

    # ===== ИНТЕГРАЦИЯ С ARCHON =====
    # Настройки Archon проекта
    archon_project_id: Optional[str] = Field(default=None, description="ID проекта в Archon")
    archon_enabled: bool = Field(default=True, description="Включить интеграцию с Archon")

    # ===== ОТЧЕТНОСТЬ =====
    # Формат отчетов
    report_format: str = Field(default="comprehensive", description="Формат отчетов (brief, standard, comprehensive)")
    include_recommendations: bool = Field(default=True, description="Включать рекомендации в отчеты")
    include_literature_citations: bool = Field(default=True, description="Включать цитирование литературы")

    # Языковые настройки
    report_language: str = Field(default="ru", description="Язык отчетов (ru, en)")
    citation_style: str = Field(default="APA", description="Стиль цитирования (APA, AMA, Vancouver)")


def load_settings() -> PsychologyResearchAgentSettings:
    """
    Загрузить настройки агента с проверкой переменных окружения.

    Returns:
        Экземпляр настроек агента

    Raises:
        ValueError: Если отсутствуют обязательные переменные
    """
    load_dotenv()

    try:
        return PsychologyResearchAgentSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Psychology Research Agent: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\n\nПроверьте наличие LLM_API_KEY в файле .env"
        if "gemini_api_key" in str(e).lower() and not os.getenv("GEMINI_API_KEY"):
            error_msg += "\nДля использования Gemini моделей укажите GEMINI_API_KEY в .env"
        raise ValueError(error_msg) from e


def create_clinical_settings(
    api_key: str,
    population: str = "clinical",
    validation_level: str = "rigorous",
    **kwargs
) -> PsychologyResearchAgentSettings:
    """
    Создать настройки для клинических исследований.

    Args:
        api_key: API ключ провайдера
        population: Целевая популяция
        validation_level: Уровень валидации
        **kwargs: Дополнительные параметры

    Returns:
        Настройки для клинических исследований
    """
    return PsychologyResearchAgentSettings(
        llm_api_key=api_key,
        research_domain="clinical",
        target_population=population,
        validation_level=validation_level,
        min_sample_size=100,
        methodology_analysis_model="qwen2.5-72b-instruct",  # Высокая точность для клиники
        statistical_validation_model="qwen2.5-coder-32b-instruct",
        reporting_standards=["CONSORT", "STROBE", "SPIRIT"],
        ethics_standards=["APA_Ethics", "Declaration_of_Helsinki", "ICH_GCP"],
        **kwargs
    )


def create_cognitive_settings(
    api_key: str,
    population: str = "adults",
    validation_level: str = "standard",
    **kwargs
) -> PsychologyResearchAgentSettings:
    """
    Создать настройки для когнитивных исследований.

    Args:
        api_key: API ключ провайдера
        population: Целевая популяция
        validation_level: Уровень валидации
        **kwargs: Дополнительные параметры

    Returns:
        Настройки для когнитивных исследований
    """
    return PsychologyResearchAgentSettings(
        llm_api_key=api_key,
        research_domain="cognitive",
        target_population=population,
        validation_level=validation_level,
        min_sample_size=30,
        methodology_focus="quantitative",
        statistical_validation_model="qwen2.5-coder-32b-instruct",
        literature_review_model="qwen2.5-coder-7b-instruct",
        reporting_standards=["APA_Style", "JARS"],
        **kwargs
    )


def create_social_settings(
    api_key: str,
    population: str = "adults",
    validation_level: str = "standard",
    **kwargs
) -> PsychologyResearchAgentSettings:
    """
    Создать настройки для социально-психологических исследований.

    Args:
        api_key: API ключ провайдера
        population: Целевая популяция
        validation_level: Уровень валидации
        **kwargs: Дополнительные параметры

    Returns:
        Настройки для социальных исследований
    """
    return PsychologyResearchAgentSettings(
        llm_api_key=api_key,
        research_domain="social",
        target_population=population,
        validation_level=validation_level,
        min_sample_size=50,
        methodology_focus="mixed_methods",
        literature_search_databases=["PubMed", "PsycINFO", "Sociological_Abstracts"],
        reporting_standards=["APA_Style", "JARS", "COREQ"],
        **kwargs
    )


def create_developmental_settings(
    api_key: str,
    population: str = "children",
    validation_level: str = "rigorous",
    **kwargs
) -> PsychologyResearchAgentSettings:
    """
    Создать настройки для исследований психологии развития.

    Args:
        api_key: API ключ провайдера
        population: Целевая популяция
        validation_level: Уровень валидации
        **kwargs: Дополнительные параметры

    Returns:
        Настройки для исследований развития
    """
    return PsychologyResearchAgentSettings(
        llm_api_key=api_key,
        research_domain="developmental",
        target_population=population,
        validation_level=validation_level,
        min_sample_size=40,  # Меньше из-за сложности работы с детьми
        methodology_analysis_model="qwen2.5-72b-instruct",  # Особая осторожность с детьми
        ethics_standards=["APA_Ethics", "SRCD_Ethical_Standards", "Declaration_of_Helsinki"],
        **kwargs
    )


def create_educational_settings(
    api_key: str,
    population: str = "students",
    validation_level: str = "standard",
    **kwargs
) -> PsychologyResearchAgentSettings:
    """
    Создать настройки для образовательных исследований.

    Args:
        api_key: API ключ провайдера
        population: Целевая популяция
        validation_level: Уровень валидации
        **kwargs: Дополнительные параметры

    Returns:
        Настройки для образовательных исследований
    """
    return PsychologyResearchAgentSettings(
        llm_api_key=api_key,
        research_domain="educational",
        target_population=population,
        validation_level=validation_level,
        min_sample_size=60,
        methodology_focus="mixed_methods",
        literature_search_databases=["PubMed", "PsycINFO", "ERIC", "Education_Database"],
        reporting_standards=["APA_Style", "CONSORT", "COREQ"],
        **kwargs
    )


# Экспорт основных функций
__all__ = [
    "PsychologyResearchAgentSettings",
    "load_settings",
    "create_clinical_settings",
    "create_cognitive_settings",
    "create_social_settings",
    "create_developmental_settings",
    "create_educational_settings"
]