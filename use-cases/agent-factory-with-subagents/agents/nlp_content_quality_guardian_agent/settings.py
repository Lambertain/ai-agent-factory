"""
NLP Content Quality Guardian Agent Settings

Настройки для агента валидации качества NLP контента.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import List, Dict, Any


class NLPQualityGuardianSettings(BaseSettings):
    """Настройки NLP Content Quality Guardian Agent."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ===== CORE LLM SETTINGS =====
    llm_api_key: str = Field(..., description="API ключ провайдера LLM")
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # ===== COST-OPTIMIZED MODEL CONFIGURATION =====
    # Validation analysis - Premium Qwen for complex quality analysis
    llm_validation_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для сложного анализа качества"
    )

    # Safety checking - Qwen Coder for pattern detection
    llm_safety_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для проверки безопасности"
    )

    # Report generation - Ultra-cheap Gemini for text generation
    llm_reporting_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для генерации отчетов"
    )

    # Knowledge search - Gemini for semantic understanding
    llm_knowledge_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для поиска знаний"
    )

    # Alternative API Keys
    gemini_api_key: str = Field(..., description="Google Gemini API ключ")
    openai_api_key: str = Field(default="", description="OpenAI API ключ (опционально)")

    # ===== VALIDATION DOMAIN SETTINGS =====
    default_validation_domain: str = Field(default="universal", description="Домен валидации по умолчанию")
    default_content_type: str = Field(default="mixed_content", description="Тип контента по умолчанию")

    # Quality thresholds
    excellence_threshold: float = Field(default=90.0, description="Порог отличного качества")
    good_threshold: float = Field(default=70.0, description="Порог хорошего качества")
    acceptable_threshold: float = Field(default=50.0, description="Минимально приемлемый порог")

    # ===== PATTERNSHIFT METHODOLOGY VALIDATION =====
    # Test validation
    min_test_questions: int = Field(default=15, description="Минимум вопросов в тестах")
    require_life_situations: bool = Field(default=True, description="Требовать жизненные ситуации")
    avoid_clinical_terms: bool = Field(default=True, description="Избегать клинических терминов")

    # Program structure validation
    require_three_level_structure: bool = Field(default=True, description="Требовать трехуровневую структуру")
    crisis_days: int = Field(default=21, description="Дни кризисного этапа")
    stabilization_days: int = Field(default=21, description="Дни стабилизации")
    development_days: int = Field(default=14, description="Дни развития")

    # VAK personalization
    require_vak_personalization: bool = Field(default=True, description="Требовать VAK персонализацию")
    require_multiformat_content: bool = Field(default=True, description="Требовать мультиформатный контент")
    require_anti_repetition: bool = Field(default=True, description="Требовать антиповторную систему")

    # ===== NLP TECHNIQUES VALIDATION =====
    require_scientific_basis: bool = Field(default=True, description="Требовать научное обоснование")
    require_ethical_safety: bool = Field(default=True, description="Требовать этическую безопасность")
    require_informed_consent: bool = Field(default=True, description="Требовать информированное согласие")
    require_contraindications: bool = Field(default=True, description="Требовать противопоказания")

    # Ericksonian patterns validation
    validate_ericksonian_principles: bool = Field(default=True, description="Валидировать принципы Эриксона")
    require_utilization_approach: bool = Field(default=True, description="Требовать подход utilization")
    require_indirect_methods: bool = Field(default=True, description="Требовать непрямые методы")

    # ===== SAFETY AND ETHICS SETTINGS =====
    enable_safety_scanning: bool = Field(default=True, description="Включить сканирование безопасности")
    enable_ethics_validation: bool = Field(default=True, description="Включить валидацию этики")

    # Critical flags sensitivity
    strict_safety_mode: bool = Field(default=True, description="Строгий режим безопасности")
    auto_flag_manipulation: bool = Field(default=True, description="Автоматически помечать манипуляции")
    auto_flag_pseudoscience: bool = Field(default=True, description="Автоматически помечать псевдонауку")

    # Age appropriateness
    min_age_restriction: int = Field(default=16, description="Минимальный возраст")
    max_age_restriction: int = Field(default=80, description="Максимальный возраст")
    enable_age_validation: bool = Field(default=True, description="Включить валидацию возраста")

    # ===== MULTILINGUAL AND CULTURAL SETTINGS =====
    primary_language: str = Field(default="ru", description="Основной язык")
    supported_languages: List[str] = Field(
        default_factory=lambda: ["ru", "uk", "en"],
        description="Поддерживаемые языки"
    )
    enable_multilingual_validation: bool = Field(default=True, description="Мультиязычная валидация")
    enable_cultural_validation: bool = Field(default=True, description="Культурная валидация")

    # Cultural sensitivity
    cultural_contexts: List[str] = Field(
        default_factory=lambda: ["slavic", "western", "eastern"],
        description="Культурные контексты"
    )

    # ===== RAG AND KNOWLEDGE SETTINGS =====
    enable_knowledge_search: bool = Field(default=True, description="Включить поиск знаний")
    knowledge_match_count: int = Field(default=5, description="Количество результатов поиска")
    enable_pattern_matching: bool = Field(default=True, description="Включить паттерн-матчинг")

    # Archon integration
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта Archon"
    )
    enable_archon_integration: bool = Field(default=True, description="Интеграция с Archon")
    enable_task_delegation: bool = Field(default=True, description="Делегирование задач")

    # ===== PERFORMANCE AND OPTIMIZATION =====
    validation_timeout_minutes: int = Field(default=10, description="Таймаут валидации в минутах")
    max_content_length: int = Field(default=100000, description="Максимальная длина контента")
    enable_parallel_validation: bool = Field(default=True, description="Параллельная валидация")

    # Cost optimization
    enable_smart_routing: bool = Field(default=True, description="Умная маршрутизация моделей")
    gemini_use_batch_api: bool = Field(default=True, description="Использовать Batch API Gemini")
    qwen_enable_context_cache: bool = Field(default=True, description="Кэш контекста Qwen")
    auto_compress_context: bool = Field(default=True, description="Автосжатие контекста")

    # ===== REPORTING AND OUTPUT SETTINGS =====
    generate_detailed_reports: bool = Field(default=True, description="Детальные отчеты")
    include_improvement_suggestions: bool = Field(default=True, description="Включить предложения")
    include_examples_in_reports: bool = Field(default=True, description="Включить примеры")
    export_format: str = Field(default="markdown", description="Формат экспорта")

    # Report customization
    report_include_scores: bool = Field(default=True, description="Включить баллы в отчет")
    report_include_metadata: bool = Field(default=True, description="Включить метаданные")
    report_include_recommendations: bool = Field(default=True, description="Включить рекомендации")

    # ===== VALIDATION WORKFLOW SETTINGS =====
    enable_four_stage_process: bool = Field(default=True, description="4-этапный процесс")
    enable_progressive_validation: bool = Field(default=True, description="Прогрессивная валидация")
    enable_automated_checks: bool = Field(default=True, description="Автоматические проверки")

    # Validation aspects
    validate_methodology_compliance: bool = Field(default=True, description="Валидировать методологию")
    validate_psychological_correctness: bool = Field(default=True, description="Психологическая корректность")
    validate_nlp_technique_quality: bool = Field(default=True, description="Качество NLP техник")
    validate_ethical_safety: bool = Field(default=True, description="Этическая безопасность")
    validate_scientific_validity: bool = Field(default=True, description="Научная валидность")
    validate_cultural_sensitivity: bool = Field(default=True, description="Культурная чувствительность")

    # ===== DEBUGGING AND MONITORING =====
    log_level: str = Field(default="INFO", description="Уровень логирования")
    enable_detailed_logging: bool = Field(default=True, description="Детальное логирование")
    track_validation_metrics: bool = Field(default=True, description="Отслеживать метрики")

    # Performance monitoring
    enable_performance_tracking: bool = Field(default=True, description="Отслеживание производительности")
    max_validation_time_seconds: int = Field(default=300, description="Максимальное время валидации")

    # ===== RATE LIMITING =====
    max_requests_per_minute: int = Field(default=30, description="Максимум запросов в минуту")
    enable_rate_limiting: bool = Field(default=True, description="Включить ограничение частоты")

    def get_model_for_task(self, task_type: str) -> str:
        """Получить оптимальную модель для типа задачи."""
        model_mapping = {
            "validation": self.llm_validation_model,
            "safety": self.llm_safety_model,
            "reporting": self.llm_reporting_model,
            "knowledge": self.llm_knowledge_model
        }
        return model_mapping.get(task_type, self.llm_validation_model)

    def get_quality_thresholds(self) -> Dict[str, float]:
        """Получить пороги качества."""
        return {
            "excellent": self.excellence_threshold,
            "good": self.good_threshold,
            "acceptable": self.acceptable_threshold,
            "unacceptable": 0.0
        }

    def get_patternshift_requirements(self) -> Dict[str, Any]:
        """Получить требования PatternShift методологии."""
        return {
            "min_test_questions": self.min_test_questions,
            "require_life_situations": self.require_life_situations,
            "avoid_clinical_terms": self.avoid_clinical_terms,
            "require_three_level_structure": self.require_three_level_structure,
            "crisis_days": self.crisis_days,
            "stabilization_days": self.stabilization_days,
            "development_days": self.development_days,
            "require_vak_personalization": self.require_vak_personalization,
            "require_multiformat_content": self.require_multiformat_content,
            "require_anti_repetition": self.require_anti_repetition
        }

    def get_safety_requirements(self) -> Dict[str, Any]:
        """Получить требования безопасности."""
        return {
            "enable_safety_scanning": self.enable_safety_scanning,
            "enable_ethics_validation": self.enable_ethics_validation,
            "strict_safety_mode": self.strict_safety_mode,
            "auto_flag_manipulation": self.auto_flag_manipulation,
            "auto_flag_pseudoscience": self.auto_flag_pseudoscience,
            "require_informed_consent": self.require_informed_consent,
            "require_contraindications": self.require_contraindications,
            "min_age_restriction": self.min_age_restriction,
            "max_age_restriction": self.max_age_restriction
        }

    def get_validation_config(self) -> Dict[str, Any]:
        """Получить полную конфигурацию валидации."""
        return {
            "quality_thresholds": self.get_quality_thresholds(),
            "patternshift_requirements": self.get_patternshift_requirements(),
            "safety_requirements": self.get_safety_requirements(),
            "languages": self.supported_languages,
            "cultural_contexts": self.cultural_contexts,
            "validation_aspects": {
                "methodology_compliance": self.validate_methodology_compliance,
                "psychological_correctness": self.validate_psychological_correctness,
                "nlp_technique_quality": self.validate_nlp_technique_quality,
                "ethical_safety": self.validate_ethical_safety,
                "scientific_validity": self.validate_scientific_validity,
                "cultural_sensitivity": self.validate_cultural_sensitivity
            }
        }


def load_settings() -> NLPQualityGuardianSettings:
    """Загрузить настройки агента валидации качества."""
    load_dotenv()

    try:
        return NLPQualityGuardianSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки NLP Quality Guardian: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\n🔑 Убедитесь, что LLM_API_KEY указан в файле .env"
        if "gemini_api_key" in str(e).lower():
            error_msg += "\n🔑 Убедитесь, что GEMINI_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_domain_specific_settings(domain: str) -> Dict[str, Any]:
    """Получить настройки, специфичные для домена."""
    domain_configs = {
        "psychology": {
            "excellence_threshold": 85.0,  # Повышенные требования
            "require_scientific_basis": True,
            "strict_safety_mode": True,
            "enable_age_validation": True,
            "min_age_restriction": 16
        },
        "astrology": {
            "excellence_threshold": 75.0,
            "require_scientific_basis": False,  # Символическая система
            "enable_cultural_validation": True,
            "validate_cultural_sensitivity": True
        },
        "tarot": {
            "excellence_threshold": 75.0,
            "require_scientific_basis": False,
            "enable_cultural_validation": True,
            "validate_cultural_sensitivity": True
        },
        "numerology": {
            "excellence_threshold": 75.0,
            "require_scientific_basis": False,
            "enable_cultural_validation": True
        },
        "universal": {
            "excellence_threshold": 80.0,
            "require_scientific_basis": True,
            "enable_cultural_validation": True,
            "validate_cultural_sensitivity": True
        }
    }

    return domain_configs.get(domain, domain_configs["universal"])


def create_validation_settings_for_domain(
    domain: str,
    api_key: str,
    **overrides
) -> NLPQualityGuardianSettings:
    """Создать настройки валидации для конкретного домена."""
    base_settings = {
        "llm_api_key": api_key,
        "default_validation_domain": domain,
        **get_domain_specific_settings(domain),
        **overrides
    }

    # Временно сохраняем в переменные среды
    import os
    for key, value in base_settings.items():
        env_key = key.upper()
        os.environ[env_key] = str(value)

    return NLPQualityGuardianSettings(**base_settings)