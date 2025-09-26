"""
NLP Content Research Agent Settings

Универсальная конфигурация для исследовательского агента с NLP специализацией.
"""

from typing import Optional, List, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv


class NLPContentResearchSettings(BaseSettings):
    """Настройки NLP Content Research Agent."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # === ОСНОВНЫЕ НАСТРОЙКИ LLM ===
    llm_api_key: str = Field(..., description="API ключ для LLM провайдера")
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Основная модель")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # === COST-OPTIMIZED MODELS ===
    # Исследовательские задачи - используем Gemini Flash (дешево)
    llm_research_model: str = Field(
        default="gemini-2.0-flash-exp",
        description="Модель для исследовательских задач"
    )
    llm_analysis_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для глубокого анализа"
    )
    llm_content_creation_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для создания контента"
    )

    # Альтернативные ключи
    gemini_api_key: Optional[str] = Field(default=None, description="Google Gemini API ключ")

    # === ИССЛЕДОВАТЕЛЬСКИЕ НАСТРОЙКИ ===
    research_domain: str = Field(default="psychology", description="Домен исследования")
    target_audience: str = Field(default="general_public", description="Целевая аудитория")
    research_depth: str = Field(default="comprehensive", description="Глубина исследования")
    scientific_rigor_level: str = Field(default="balanced", description="Уровень научной строгости")

    # === NLP КОНФИГУРАЦИЯ ===
    primary_nlp_techniques: List[str] = Field(
        default=["vak_adaptation", "rapport_building", "reframing"],
        description="Основные NLP техники"
    )
    ericksonian_intensity: str = Field(default="moderate", description="Интенсивность эриксоновского гипноза")
    enable_vak_adaptation: bool = Field(default=True, description="Включить VAK адаптацию")
    enable_storytelling: bool = Field(default=True, description="Включить сторителлинг")

    # === ИСТОЧНИКИ ДАННЫХ ===
    enable_web_search: bool = Field(default=True, description="Включить веб-поиск")
    enable_academic_search: bool = Field(default=True, description="Включить академический поиск")
    enable_competitive_analysis: bool = Field(default=True, description="Включить конкурентный анализ")
    enable_viral_content_analysis: bool = Field(default=True, description="Включить анализ вирусного контента")

    # === ЯЗЫКОВЫЕ НАСТРОЙКИ ===
    content_language: str = Field(default="ru", description="Язык контента")
    audience_language_preference: str = Field(default="simple", description="Языковые предпочтения аудитории")
    dual_language_mode: bool = Field(default=False, description="Двуязычный режим")

    # === PATERNSHIFT МЕТОДОЛОГИЯ ===
    enable_patternshift_methodology: bool = Field(default=True, description="Включить методологию PatternShift")
    viral_potential_analysis: bool = Field(default=True, description="Анализ вирусного потенциала")
    pain_point_identification: bool = Field(default=True, description="Выявление болевых точек")
    conversion_optimization: bool = Field(default=True, description="Оптимизация конверсии")

    # === ЛИМИТЫ И ПРОИЗВОДИТЕЛЬНОСТЬ ===
    max_search_results: int = Field(default=50, description="Максимум результатов поиска")
    max_sources_per_domain: int = Field(default=10, description="Максимум источников на домен")
    research_timeout_minutes: int = Field(default=30, description="Таймаут исследования в минутах")
    batch_processing_enabled: bool = Field(default=True, description="Включить пакетную обработку")

    # === RAG И БАЗА ЗНАНИЙ ===
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )
    knowledge_tags: List[str] = Field(
        default=["nlp-content-research", "agent-knowledge", "pydantic-ai"],
        description="Теги для поиска в базе знаний"
    )
    knowledge_domain: Optional[str] = Field(default=None, description="Домен базы знаний")

    # === ВЫХОДНЫЕ ФОРМАТЫ ===
    output_formats: List[str] = Field(
        default=["research_brief", "content_outline", "vak_adaptations"],
        description="Форматы вывода результатов"
    )
    include_statistics: bool = Field(default=True, description="Включать статистику")
    include_case_studies: bool = Field(default=True, description="Включать кейс-стади")
    include_expert_quotes: bool = Field(default=False, description="Включать экспертные цитаты")

    # === СПЕЦИАЛИЗИРОВАННЫЕ НАСТРОЙКИ ===
    expertise_level: str = Field(default="advanced", description="Уровень экспертизы")
    domain_expertise_areas: List[str] = Field(
        default=[],
        description="Области доменной экспертизы"
    )

    def get_domain_configuration(self) -> Dict[str, Any]:
        """Получить конфигурацию для текущего домена."""
        domain_configs = {
            "psychology": {
                "scientific_rigor": "strict",
                "expertise_areas": ["clinical", "cognitive", "social", "developmental"],
                "preferred_sources": ["pubmed", "psychologytoday", "apa.org"],
                "nlp_focus": ["therapeutic_language", "empathy_building", "reframing"]
            },
            "astrology": {
                "scientific_rigor": "relaxed",
                "expertise_areas": ["natal_charts", "transits", "compatibility"],
                "preferred_sources": ["astro.com", "cafeastrology.com", "astrologyzone.com"],
                "nlp_focus": ["mystical_language", "future_pacing", "symbolic_thinking"]
            },
            "tarot": {
                "scientific_rigor": "intuitive",
                "expertise_areas": ["card_meanings", "spreads", "symbolism"],
                "preferred_sources": ["biddytarot.com", "learntarot.com", "aeclectic.net"],
                "nlp_focus": ["symbolic_language", "intuitive_guidance", "metaphorical_thinking"]
            },
            "numerology": {
                "scientific_rigor": "analytical",
                "expertise_areas": ["life_path", "compatibility", "cycles"],
                "preferred_sources": ["numerology.com", "worldnumerology.com"],
                "nlp_focus": ["pattern_recognition", "analytical_language", "number_symbolism"]
            }
        }

        return domain_configs.get(self.research_domain, {
            "scientific_rigor": "balanced",
            "expertise_areas": ["general"],
            "preferred_sources": [],
            "nlp_focus": ["general_rapport", "clarity", "engagement"]
        })

    def get_model_for_task(self, task_type: str) -> str:
        """Получить оптимальную модель для типа задачи."""
        task_model_mapping = {
            "research": self.llm_research_model,
            "analysis": self.llm_analysis_model,
            "content_creation": self.llm_content_creation_model,
            "quick_lookup": "gemini-2.0-flash-thinking-exp",
            "deep_analysis": self.llm_analysis_model,
            "viral_analysis": self.llm_research_model,
            "competitive_analysis": self.llm_analysis_model
        }

        return task_model_mapping.get(task_type, self.llm_model)

    def get_search_configuration(self) -> Dict[str, Any]:
        """Получить конфигурацию поиска."""
        return {
            "web_search": self.enable_web_search,
            "academic_search": self.enable_academic_search,
            "competitive_analysis": self.enable_competitive_analysis,
            "viral_analysis": self.enable_viral_content_analysis,
            "max_results": self.max_search_results,
            "max_sources_per_domain": self.max_sources_per_domain,
            "timeout_minutes": self.research_timeout_minutes
        }

    def get_nlp_configuration(self) -> Dict[str, Any]:
        """Получить конфигурацию NLP."""
        return {
            "techniques": self.primary_nlp_techniques,
            "ericksonian_intensity": self.ericksonian_intensity,
            "vak_adaptation": self.enable_vak_adaptation,
            "storytelling": self.enable_storytelling,
            "domain_language_style": self.audience_language_preference
        }


def load_settings() -> NLPContentResearchSettings:
    """
    Загрузить настройки с проверкой обязательных параметров.

    Returns:
        Настройки агента

    Raises:
        ValueError: Если не указаны обязательные параметры
    """
    load_dotenv()

    try:
        return NLPContentResearchSettings()
    except Exception as e:
        error_msg = f"Ошибка загрузки настроек: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += """

ТРЕБУЕТСЯ НАСТРОЙКА:
Создайте файл .env со следующими параметрами:

# Основной LLM провайдер
LLM_API_KEY=your_api_key_here
LLM_PROVIDER=openai
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# Опционально: Gemini для дешевых задач
GEMINI_API_KEY=your_gemini_key_here

# Настройки исследования
RESEARCH_DOMAIN=psychology
TARGET_AUDIENCE=general_public
"""
        raise ValueError(error_msg) from e


def get_domain_examples() -> Dict[str, Dict[str, Any]]:
    """Получить примеры конфигураций для различных доменов."""
    return {
        "psychology": {
            "research_domain": "psychology",
            "target_audience": "general_public",
            "scientific_rigor_level": "strict",
            "primary_nlp_techniques": ["vak_adaptation", "rapport_building", "ericksonian_hypnosis"],
            "include_expert_quotes": True,
            "enable_academic_search": True
        },
        "astrology": {
            "research_domain": "astrology",
            "target_audience": "general_public",
            "scientific_rigor_level": "relaxed",
            "primary_nlp_techniques": ["storytelling", "language_patterns", "anchoring"],
            "audience_language_preference": "mystical",
            "enable_viral_content_analysis": True
        },
        "tarot": {
            "research_domain": "tarot",
            "target_audience": "general_public",
            "scientific_rigor_level": "intuitive",
            "primary_nlp_techniques": ["storytelling", "metaphorical_thinking", "intuitive_guidance"],
            "audience_language_preference": "symbolic",
            "enable_competitive_analysis": True
        },
        "business_coaching": {
            "research_domain": "coaching",
            "target_audience": "professionals",
            "scientific_rigor_level": "balanced",
            "primary_nlp_techniques": ["goal_setting", "reframing", "rapport_building"],
            "audience_language_preference": "professional",
            "include_case_studies": True
        }
    }


__all__ = [
    "NLPContentResearchSettings",
    "load_settings",
    "get_domain_examples"
]