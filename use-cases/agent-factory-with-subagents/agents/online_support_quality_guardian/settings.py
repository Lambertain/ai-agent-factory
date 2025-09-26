"""
Настройки для Psychology Quality Guardian Agent

Универсальная конфигурация для контроля качества психологического контента
с поддержкой различных доменов и стандартов валидации.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import List, Dict, Optional
from dotenv import load_dotenv


class PsychologyQualityGuardianSettings(BaseSettings):
    """
    Настройки Psychology Quality Guardian Agent с поддержкой переменных окружения.

    Обеспечивает универсальную конфигурацию для различных доменов психологии
    и стандартов качества.
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="QUALITY_GUARDIAN_"
    )

    # === БАЗОВЫЕ НАСТРОЙКИ LLM ===
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Основная модель для анализа")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # === СПЕЦИАЛИЗИРОВАННЫЕ МОДЕЛИ ДЛЯ РАЗНЫХ ЗАДАЧ ===
    # Модель для этического анализа (требует понимания нюансов)
    ethical_analysis_model: str = Field(default="qwen2.5-72b-instruct", description="Модель для этического анализа")

    # Модель для научной валидации (требует знания статистики)
    scientific_validation_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Модель для научной валидации")

    # Модель для анализа безопасности (быстрая обработка)
    safety_analysis_model: str = Field(default="qwen2.5-coder-7b-instruct", description="Модель для анализа безопасности")

    # Модель для отчетов (экономичная для текстовых задач)
    reporting_model: str = Field(default="gemini-2.5-flash-lite", description="Модель для генерации отчетов")

    # Alternative API keys для multi-provider setup
    gemini_api_key: Optional[str] = Field(default=None, description="Google Gemini API ключ")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API ключ")

    # === УНИВЕРСАЛЬНЫЕ НАСТРОЙКИ ДОМЕНА ===
    default_domain_type: str = Field(default="general", description="Домен по умолчанию")
    default_target_population: str = Field(default="adults", description="Целевая популяция по умолчанию")
    default_content_type: str = Field(default="assessment", description="Тип контента по умолчанию")

    # === СТАНДАРТЫ КАЧЕСТВА ===
    default_quality_standards: List[str] = Field(
        default=["APA", "ethical_guidelines"],
        description="Стандарты качества по умолчанию"
    )
    default_compliance_level: str = Field(default="standard", description="Уровень соответствия по умолчанию")

    # === ПСИХОМЕТРИЧЕСКИЕ СТАНДАРТЫ ===
    default_reliability_threshold: float = Field(default=0.80, description="Порог надежности по умолчанию")
    default_validity_threshold: float = Field(default=0.70, description="Порог валидности по умолчанию")
    default_factor_loading_min: float = Field(default=0.30, description="Минимальная факторная нагрузка")
    default_item_correlation_min: float = Field(default=0.30, description="Минимальная корреляция заданий")

    # === НАСТРОЙКИ БЕЗОПАСНОСТИ ===
    default_risk_tolerance: str = Field(default="medium", description="Толерантность к риску по умолчанию")
    default_privacy_level: str = Field(default="high", description="Уровень приватности по умолчанию")
    vulnerable_groups_protection: bool = Field(default=True, description="Защита уязвимых групп")

    # === RAG И ИНТЕГРАЦИЯ ===
    enable_rag_search: bool = Field(default=True, description="Включить поиск в базе знаний")
    knowledge_base_url: Optional[str] = Field(default=None, description="URL базы знаний")
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта Archon"
    )

    # === НАСТРОЙКИ ВАЛИДАЦИИ ===
    enable_automated_validation: bool = Field(default=True, description="Автоматическая валидация")
    enable_real_time_monitoring: bool = Field(default=False, description="Мониторинг в реальном времени")
    validation_batch_size: int = Field(default=10, description="Размер пакета для валидации")

    # === ДИРЕКТОРИИ И ПУТИ ===
    output_directory: str = Field(default="./quality_reports", description="Директория для отчетов")
    knowledge_directory: str = Field(default="./knowledge", description="Директория базы знаний")
    templates_directory: str = Field(default="./templates", description="Директория шаблонов")
    cache_directory: str = Field(default="./cache", description="Директория кэша")

    # === НАСТРОЙКИ ОТЧЕТНОСТИ ===
    default_report_format: str = Field(default="comprehensive", description="Формат отчета по умолчанию")
    notification_level: str = Field(default="important", description="Уровень уведомлений")
    enable_email_notifications: bool = Field(default=False, description="Email уведомления")
    email_smtp_server: Optional[str] = Field(default=None, description="SMTP сервер для email")
    email_recipients: List[str] = Field(default_factory=list, description="Получатели email")

    # === ПРОИЗВОДИТЕЛЬНОСТЬ И КЭШИРОВАНИЕ ===
    enable_response_caching: bool = Field(default=True, description="Кэширование ответов")
    cache_ttl_hours: int = Field(default=24, description="Время жизни кэша в часах")
    max_concurrent_evaluations: int = Field(default=5, description="Максимум одновременных оценок")
    request_timeout_seconds: int = Field(default=300, description="Таймаут запроса в секундах")

    # === ЛОГИРОВАНИЕ ===
    log_level: str = Field(default="INFO", description="Уровень логирования")
    log_file_path: Optional[str] = Field(default=None, description="Путь к файлу логов")
    enable_audit_logging: bool = Field(default=True, description="Аудит логирование")

    # === КУЛЬТУРНАЯ АДАПТАЦИЯ ===
    default_cultural_sensitivity: str = Field(default="standard", description="Уровень культурной чувствительности")
    supported_languages: List[str] = Field(
        default=["ru", "en"],
        description="Поддерживаемые языки"
    )
    default_locale: str = Field(default="ru_RU", description="Локаль по умолчанию")

    # === СООТВЕТСТВИЕ РЕГУЛЯТОРНЫМ ТРЕБОВАНИЯМ ===
    gdpr_compliance: bool = Field(default=True, description="Соответствие GDPR")
    hipaa_compliance: bool = Field(default=False, description="Соответствие HIPAA")
    data_retention_days: int = Field(default=2555, description="Срок хранения данных (7 лет)")
    enable_data_anonymization: bool = Field(default=True, description="Анонимизация данных")

    # === ВЕРСИОНИРОВАНИЕ ===
    standards_version: str = Field(default="2024.1", description="Версия стандартов")
    agent_version: str = Field(default="1.0.0", description="Версия агента")

    # === ЭКСПЕРИМЕНТАЛЬНЫЕ ФУНКЦИИ ===
    enable_ai_bias_detection: bool = Field(default=True, description="Детекция AI предвзятости")
    enable_automated_reporting: bool = Field(default=True, description="Автоматическая отчетность")
    enable_cross_validation: bool = Field(default=False, description="Кросс-валидация между агентами")

    def get_domain_specific_settings(self, domain_type: str) -> Dict:
        """Получить настройки специфичные для домена."""
        domain_configs = {
            "clinical": {
                "reliability_threshold": 0.85,
                "validity_threshold": 0.80,
                "quality_standards": ["APA", "DSM5", "ICD11", "clinical_guidelines"],
                "privacy_level": "maximum",
                "compliance_level": "comprehensive",
                "risk_tolerance": "low",
                "model_preference": self.ethical_analysis_model  # Более мощная модель для клиники
            },
            "research": {
                "reliability_threshold": 0.85,
                "validity_threshold": 0.80,
                "quality_standards": ["APA", "research_ethics", "IRB_guidelines"],
                "privacy_level": "maximum",
                "compliance_level": "research_grade",
                "risk_tolerance": "low",
                "model_preference": self.scientific_validation_model
            },
            "educational": {
                "reliability_threshold": 0.75,
                "validity_threshold": 0.70,
                "quality_standards": ["educational_standards", "accessibility"],
                "privacy_level": "high",
                "compliance_level": "standard",
                "risk_tolerance": "medium",
                "model_preference": self.llm_model  # Стандартная модель
            },
            "wellness": {
                "reliability_threshold": 0.70,
                "validity_threshold": 0.65,
                "quality_standards": ["wellness_guidelines", "user_safety"],
                "privacy_level": "standard",
                "compliance_level": "basic",
                "risk_tolerance": "medium",
                "model_preference": self.safety_analysis_model  # Быстрая модель
            },
            "organizational": {
                "reliability_threshold": 0.80,
                "validity_threshold": 0.75,
                "quality_standards": ["workplace_ethics", "fairness"],
                "privacy_level": "high",
                "compliance_level": "standard",
                "risk_tolerance": "medium",
                "model_preference": self.llm_model
            }
        }

        return domain_configs.get(domain_type, {
            "reliability_threshold": self.default_reliability_threshold,
            "validity_threshold": self.default_validity_threshold,
            "quality_standards": self.default_quality_standards,
            "privacy_level": self.default_privacy_level,
            "compliance_level": self.default_compliance_level,
            "risk_tolerance": self.default_risk_tolerance,
            "model_preference": self.llm_model
        })

    def get_population_specific_settings(self, population: str) -> Dict:
        """Получить настройки специфичные для популяции."""
        population_configs = {
            "children": {
                "require_parental_consent": True,
                "enhanced_safety_protocols": True,
                "simplified_language_required": True,
                "max_session_duration": 30,  # минут
                "additional_protections": ["child_protection", "age_verification"]
            },
            "adolescents": {
                "require_parental_consent": True,
                "peer_influence_considerations": True,
                "identity_development_awareness": True,
                "max_session_duration": 45,
                "additional_protections": ["youth_protection", "bullying_prevention"]
            },
            "elderly": {
                "cognitive_accessibility": True,
                "large_text_support": True,
                "simplified_navigation": True,
                "max_session_duration": 60,
                "additional_protections": ["elder_protection", "cognitive_support"]
            },
            "clinical": {
                "enhanced_crisis_protocols": True,
                "professional_supervision": True,
                "clinical_referral_ready": True,
                "max_session_duration": 90,
                "additional_protections": ["clinical_safety", "crisis_intervention"]
            }
        }

        return population_configs.get(population, {
            "require_parental_consent": False,
            "max_session_duration": 60,
            "additional_protections": []
        })

    def get_model_for_task(self, task_type: str) -> str:
        """Получить оптимальную модель для конкретной задачи."""
        task_models = {
            "ethical_analysis": self.ethical_analysis_model,
            "scientific_validation": self.scientific_validation_model,
            "safety_analysis": self.safety_analysis_model,
            "report_generation": self.reporting_model,
            "general_analysis": self.llm_model,
            "quick_check": self.safety_analysis_model,
            "detailed_review": self.ethical_analysis_model
        }

        return task_models.get(task_type, self.llm_model)

    def get_compliance_requirements(self) -> Dict:
        """Получить требования соответствия."""
        requirements = {
            "ethical_review": True,
            "scientific_validation": True,
            "safety_assessment": True,
            "privacy_protection": True
        }

        if self.gdpr_compliance:
            requirements.update({
                "gdpr_compliance": True,
                "data_subject_rights": True,
                "lawful_basis_documented": True,
                "data_protection_impact_assessment": True
            })

        if self.hipaa_compliance:
            requirements.update({
                "hipaa_compliance": True,
                "phi_protection": True,
                "access_controls": True,
                "audit_trails": True
            })

        return requirements

    def get_validation_pipeline(self) -> List[str]:
        """Получить пайплайн валидации."""
        base_pipeline = [
            "content_analysis",
            "ethical_review",
            "scientific_validation",
            "safety_assessment"
        ]

        if self.enable_ai_bias_detection:
            base_pipeline.append("bias_detection")

        if self.vulnerable_groups_protection:
            base_pipeline.append("vulnerability_assessment")

        if self.default_cultural_sensitivity in ["high", "maximum"]:
            base_pipeline.append("cultural_validation")

        return base_pipeline

    def should_use_enhanced_model(self, domain: str, population: str) -> bool:
        """Определить, использовать ли усиленную модель."""
        return (
            domain in ["clinical", "research"] or
            population in ["children", "clinical"] or
            self.default_compliance_level in ["comprehensive", "research_grade"]
        )

    def get_notification_settings(self) -> Dict:
        """Получить настройки уведомлений."""
        return {
            "level": self.notification_level,
            "email_enabled": self.enable_email_notifications,
            "email_recipients": self.email_recipients,
            "smtp_server": self.email_smtp_server,
            "real_time": self.enable_real_time_monitoring
        }

    def get_caching_settings(self) -> Dict:
        """Получить настройки кэширования."""
        return {
            "enabled": self.enable_response_caching,
            "ttl_hours": self.cache_ttl_hours,
            "directory": self.cache_directory,
            "max_size_mb": 1000  # Максимальный размер кэша
        }


def load_settings() -> PsychologyQualityGuardianSettings:
    """
    Загрузить настройки Psychology Quality Guardian Agent.

    Returns:
        Настройки агента с проверкой обязательных параметров
    """
    load_dotenv()

    try:
        settings = PsychologyQualityGuardianSettings()

        # Проверяем критически важные настройки
        if not settings.llm_api_key:
            raise ValueError("LLM_API_KEY обязателен для работы агента")

        # Создаем директории если они не существуют
        import os
        for directory in [
            settings.output_directory,
            settings.knowledge_directory,
            settings.templates_directory,
            settings.cache_directory
        ]:
            os.makedirs(directory, exist_ok=True)

        return settings

    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Psychology Quality Guardian: {e}"
        raise ValueError(error_msg) from e


# Фабричные функции для создания конфигураций

def create_clinical_settings(api_key: str, **overrides) -> PsychologyQualityGuardianSettings:
    """Создать настройки для клинического использования."""
    clinical_overrides = {
        "default_domain_type": "clinical",
        "default_compliance_level": "comprehensive",
        "default_privacy_level": "maximum",
        "default_risk_tolerance": "low",
        "vulnerable_groups_protection": True,
        "hipaa_compliance": True,
        "enable_real_time_monitoring": True,
        **overrides
    }

    return PsychologyQualityGuardianSettings(
        llm_api_key=api_key,
        **clinical_overrides
    )


def create_research_settings(api_key: str, **overrides) -> PsychologyQualityGuardianSettings:
    """Создать настройки для исследовательского использования."""
    research_overrides = {
        "default_domain_type": "research",
        "default_compliance_level": "research_grade",
        "default_privacy_level": "maximum",
        "enable_audit_logging": True,
        "enable_cross_validation": True,
        "data_retention_days": 3650,  # 10 лет для исследований
        **overrides
    }

    return PsychologyQualityGuardianSettings(
        llm_api_key=api_key,
        **research_overrides
    )


def create_educational_settings(api_key: str, **overrides) -> PsychologyQualityGuardianSettings:
    """Создать настройки для образовательного использования."""
    educational_overrides = {
        "default_domain_type": "educational",
        "default_target_population": "adolescents",
        "default_cultural_sensitivity": "high",
        "vulnerable_groups_protection": True,
        "enable_ai_bias_detection": True,
        **overrides
    }

    return PsychologyQualityGuardianSettings(
        llm_api_key=api_key,
        **educational_overrides
    )


def create_wellness_settings(api_key: str, **overrides) -> PsychologyQualityGuardianSettings:
    """Создать настройки для wellness приложений."""
    wellness_overrides = {
        "default_domain_type": "wellness",
        "default_compliance_level": "standard",
        "default_privacy_level": "standard",
        "enable_automated_reporting": True,
        "enable_real_time_monitoring": False,
        **overrides
    }

    return PsychologyQualityGuardianSettings(
        llm_api_key=api_key,
        **wellness_overrides
    )


# Экспорт
__all__ = [
    "PsychologyQualityGuardianSettings",
    "load_settings",
    "create_clinical_settings",
    "create_research_settings",
    "create_educational_settings",
    "create_wellness_settings"
]