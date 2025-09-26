"""
Settings для NLP Psychology Test Adapter Agent

Конфигурация и настройки для агента адаптации психологических тестов
с поддержкой универсальности и различных типов проектов.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Dict, List, Any, Optional
from enum import Enum


class AdaptationDomainType(str, Enum):
    """Типы доменов для адаптации тестов."""
    CLINICAL_PSYCHOLOGY = "clinical_psychology"
    WELLNESS = "wellness"
    COACHING = "coaching"
    EDUCATIONAL = "educational"
    ORGANIZATIONAL = "organizational"
    RESEARCH = "research"


class ProjectType(str, Enum):
    """Типы проектов для конфигурации."""
    MENTAL_HEALTH_PLATFORM = "mental_health_platform"
    WELLNESS_APP = "wellness_app"
    COACHING_SYSTEM = "coaching_system"
    EDUCATIONAL_TOOL = "educational_tool"
    HR_ASSESSMENT = "hr_assessment"
    RESEARCH_STUDY = "research_study"


class CulturalContext(str, Enum):
    """Культурные контексты для адаптации."""
    UKRAINIAN = "ukrainian"
    RUSSIAN = "russian"
    WESTERN_EUROPEAN = "western_european"
    AMERICAN = "american"
    EASTERN_EUROPEAN = "eastern_european"
    UNIVERSAL = "universal"


class TestAdapterSettings(BaseSettings):
    """Основные настройки агента адаптации тестов."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # === УНИВЕРСАЛЬНАЯ КОНФИГУРАЦИЯ ===
    domain_type: AdaptationDomainType = Field(
        default=AdaptationDomainType.WELLNESS,
        description="Тип домена адаптации"
    )
    project_type: ProjectType = Field(
        default=ProjectType.WELLNESS_APP,
        description="Тип проекта"
    )
    cultural_context: CulturalContext = Field(
        default=CulturalContext.UKRAINIAN,
        description="Культурный контекст"
    )

    # === ЯЗЫКОВЫЕ НАСТРОЙКИ ===
    primary_language: str = Field(default="uk", description="Основной язык")
    supported_languages: List[str] = Field(
        default_factory=lambda: ["uk", "ru", "en"],
        description="Поддерживаемые языки"
    )

    # === МЕТОДОЛОГИЯ PATTERNSHIFT ===
    min_questions: int = Field(default=15, description="Минимальное количество вопросов")
    life_situations_ratio: float = Field(
        default=0.70,
        description="Минимальный процент вопросов в формате жизненных ситуаций",
        ge=0.0, le=1.0
    )
    adaptive_scoring: bool = Field(
        default=True,
        description="Использовать адаптивную систему оценки"
    )
    result_levels: int = Field(
        default=4,
        description="Количество уровней результатов",
        ge=2, le=7
    )
    redirection_logic: bool = Field(
        default=True,
        description="Включить логику перенаправления"
    )

    # === КАЧЕСТВО АДАПТАЦИИ ===
    methodology_compliance_threshold: float = Field(
        default=0.85,
        description="Порог соответствия методологии",
        ge=0.0, le=1.0
    )
    psychological_validity_threshold: float = Field(
        default=0.90,
        description="Порог психологической валидности",
        ge=0.0, le=1.0
    )
    structural_integrity_threshold: float = Field(
        default=0.80,
        description="Порог структурной целостности",
        ge=0.0, le=1.0
    )

    # === RAG КОНФИГУРАЦИЯ ===
    rag_server_url: str = Field(
        default="http://localhost:3737",
        description="URL сервера RAG"
    )
    knowledge_tags: List[str] = Field(
        default_factory=lambda: [
            "psychology-test-adaptation",
            "patternshift-methodology",
            "psychological-assessment",
            "nlp-psychology"
        ],
        description="Теги для поиска знаний в RAG"
    )
    rag_match_count: int = Field(
        default=5,
        description="Количество результатов RAG поиска",
        ge=1, le=20
    )

    # === МОДЕЛИ LLM ===
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_model: str = Field(
        default="claude-sonnet-4",
        description="Основная модель LLM"
    )
    llm_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="Базовый URL API"
    )
    llm_api_key: str = Field(..., description="API ключ LLM")

    # === КЕШИРОВАНИЕ ===
    enable_knowledge_cache: bool = Field(
        default=True,
        description="Включить кеширование RAG запросов"
    )
    cache_ttl_minutes: int = Field(
        default=60,
        description="TTL кеша в минутах"
    )

    # === БЕЗОПАСНОСТЬ ===
    max_concurrent_requests: int = Field(
        default=10,
        description="Максимальное количество одновременных запросов"
    )
    request_timeout_seconds: int = Field(
        default=30,
        description="Таймаут запросов в секундах"
    )


# === КОНФИГУРАЦИИ ДЛЯ РАЗНЫХ ДОМЕНОВ ===

DOMAIN_CONFIGURATIONS = {
    AdaptationDomainType.CLINICAL_PSYCHOLOGY: {
        "methodology_compliance_threshold": 0.95,
        "psychological_validity_threshold": 0.95,
        "min_questions": 20,
        "life_situations_ratio": 0.60,  # Более консервативный подход
        "result_levels": 5,
        "knowledge_tags": [
            "clinical-psychology", "diagnostic-tools",
            "psychological-assessment", "clinical-validation"
        ]
    },
    AdaptationDomainType.WELLNESS: {
        "methodology_compliance_threshold": 0.85,
        "psychological_validity_threshold": 0.90,
        "min_questions": 15,
        "life_situations_ratio": 0.80,  # Больше жизненных ситуаций
        "result_levels": 4,
        "knowledge_tags": [
            "wellness", "mental-health", "life-situations",
            "personal-growth"
        ]
    },
    AdaptationDomainType.COACHING: {
        "methodology_compliance_threshold": 0.80,
        "psychological_validity_threshold": 0.85,
        "min_questions": 12,
        "life_situations_ratio": 0.90,  # Максимум жизненных ситуаций
        "result_levels": 3,
        "knowledge_tags": [
            "coaching", "personal-development",
            "goal-setting", "performance"
        ]
    },
    AdaptationDomainType.EDUCATIONAL: {
        "methodology_compliance_threshold": 0.85,
        "psychological_validity_threshold": 0.90,
        "min_questions": 15,
        "life_situations_ratio": 0.75,
        "result_levels": 4,
        "knowledge_tags": [
            "educational-psychology", "learning-assessment",
            "student-wellbeing", "academic-performance"
        ]
    },
    AdaptationDomainType.ORGANIZATIONAL: {
        "methodology_compliance_threshold": 0.85,
        "psychological_validity_threshold": 0.90,
        "min_questions": 18,
        "life_situations_ratio": 0.85,
        "result_levels": 5,
        "knowledge_tags": [
            "organizational-psychology", "workplace-assessment",
            "employee-wellbeing", "team-dynamics"
        ]
    },
    AdaptationDomainType.RESEARCH: {
        "methodology_compliance_threshold": 0.95,
        "psychological_validity_threshold": 0.95,
        "min_questions": 25,
        "life_situations_ratio": 0.65,
        "result_levels": 6,
        "knowledge_tags": [
            "research-methods", "psychometrics",
            "validation-studies", "test-development"
        ]
    }
}


# === КУЛЬТУРНЫЕ КОНФИГУРАЦИИ ===

CULTURAL_CONFIGURATIONS = {
    CulturalContext.UKRAINIAN: {
        "primary_language": "uk",
        "cultural_values": ["family", "community", "resilience", "tradition"],
        "communication_style": "warm_personal",
        "formality_level": "informal_respectful"
    },
    CulturalContext.RUSSIAN: {
        "primary_language": "ru",
        "cultural_values": ["strength", "endurance", "collective", "emotional_depth"],
        "communication_style": "direct_emotional",
        "formality_level": "formal_respectful"
    },
    CulturalContext.WESTERN_EUROPEAN: {
        "primary_language": "en",
        "cultural_values": ["individualism", "privacy", "efficiency", "work_life_balance"],
        "communication_style": "polite_reserved",
        "formality_level": "professional_friendly"
    },
    CulturalContext.AMERICAN: {
        "primary_language": "en",
        "cultural_values": ["achievement", "optimism", "individualism", "innovation"],
        "communication_style": "enthusiastic_direct",
        "formality_level": "casual_professional"
    },
    CulturalContext.EASTERN_EUROPEAN: {
        "primary_language": "en",
        "cultural_values": ["family", "perseverance", "education", "respect"],
        "communication_style": "sincere_thoughtful",
        "formality_level": "respectful_warm"
    },
    CulturalContext.UNIVERSAL: {
        "primary_language": "en",
        "cultural_values": ["human_dignity", "wellbeing", "growth", "connection"],
        "communication_style": "inclusive_neutral",
        "formality_level": "professional_accessible"
    }
}


# === ПРОЕКТНЫЕ КОНФИГУРАЦИИ ===

PROJECT_CONFIGURATIONS = {
    ProjectType.MENTAL_HEALTH_PLATFORM: {
        "domain_type": AdaptationDomainType.CLINICAL_PSYCHOLOGY,
        "focus_areas": ["clinical_assessment", "symptom_tracking", "intervention_planning"],
        "compliance_requirements": ["HIPAA", "GDPR", "clinical_standards"],
        "target_audience": "patients_clinicians"
    },
    ProjectType.WELLNESS_APP: {
        "domain_type": AdaptationDomainType.WELLNESS,
        "focus_areas": ["mood_tracking", "lifestyle_assessment", "personal_growth"],
        "compliance_requirements": ["privacy_basic", "data_protection"],
        "target_audience": "general_public"
    },
    ProjectType.COACHING_SYSTEM: {
        "domain_type": AdaptationDomainType.COACHING,
        "focus_areas": ["goal_setting", "performance_tracking", "motivation_assessment"],
        "compliance_requirements": ["professional_coaching", "confidentiality"],
        "target_audience": "clients_coaches"
    },
    ProjectType.EDUCATIONAL_TOOL: {
        "domain_type": AdaptationDomainType.EDUCATIONAL,
        "focus_areas": ["learning_style", "academic_stress", "student_wellbeing"],
        "compliance_requirements": ["FERPA", "child_protection"],
        "target_audience": "students_educators"
    },
    ProjectType.HR_ASSESSMENT: {
        "domain_type": AdaptationDomainType.ORGANIZATIONAL,
        "focus_areas": ["employee_engagement", "team_dynamics", "workplace_stress"],
        "compliance_requirements": ["employment_law", "equal_opportunity"],
        "target_audience": "employees_hr_professionals"
    },
    ProjectType.RESEARCH_STUDY: {
        "domain_type": AdaptationDomainType.RESEARCH,
        "focus_areas": ["construct_validation", "cross_cultural_research", "psychometrics"],
        "compliance_requirements": ["IRB_approval", "research_ethics"],
        "target_audience": "researchers_participants"
    }
}


def load_settings() -> TestAdapterSettings:
    """Загружает настройки агента."""
    try:
        return TestAdapterSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедись, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_domain_config(domain_type: AdaptationDomainType) -> Dict[str, Any]:
    """Получает конфигурацию для конкретного домена."""
    return DOMAIN_CONFIGURATIONS.get(domain_type, DOMAIN_CONFIGURATIONS[AdaptationDomainType.WELLNESS])


def get_cultural_config(cultural_context: CulturalContext) -> Dict[str, Any]:
    """Получает культурную конфигурацию."""
    return CULTURAL_CONFIGURATIONS.get(cultural_context, CULTURAL_CONFIGURATIONS[CulturalContext.UNIVERSAL])


def get_project_config(project_type: ProjectType) -> Dict[str, Any]:
    """Получает конфигурацию проекта."""
    return PROJECT_CONFIGURATIONS.get(project_type, PROJECT_CONFIGURATIONS[ProjectType.WELLNESS_APP])


def create_adaptive_config(
    domain_type: AdaptationDomainType,
    cultural_context: CulturalContext,
    project_type: Optional[ProjectType] = None
) -> Dict[str, Any]:
    """
    Создает адаптивную конфигурацию на основе домена, культуры и типа проекта.

    Args:
        domain_type: Тип домена адаптации
        cultural_context: Культурный контекст
        project_type: Тип проекта (опционально)

    Returns:
        Объединенная конфигурация
    """
    # Базовая конфигурация
    config = {
        "domain_type": domain_type,
        "cultural_context": cultural_context
    }

    # Добавляем конфигурацию домена
    domain_config = get_domain_config(domain_type)
    config.update(domain_config)

    # Добавляем культурную конфигурацию
    cultural_config = get_cultural_config(cultural_context)
    config.update(cultural_config)

    # Добавляем проектную конфигурацию
    if project_type:
        project_config = get_project_config(project_type)
        config.update(project_config)

    return config


# === ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===

EXAMPLE_CONFIGS = {
    "wellness_app_ukrainian": create_adaptive_config(
        AdaptationDomainType.WELLNESS,
        CulturalContext.UKRAINIAN,
        ProjectType.WELLNESS_APP
    ),
    "clinical_platform_american": create_adaptive_config(
        AdaptationDomainType.CLINICAL_PSYCHOLOGY,
        CulturalContext.AMERICAN,
        ProjectType.MENTAL_HEALTH_PLATFORM
    ),
    "coaching_system_universal": create_adaptive_config(
        AdaptationDomainType.COACHING,
        CulturalContext.UNIVERSAL,
        ProjectType.COACHING_SYSTEM
    ),
    "hr_assessment_eastern_european": create_adaptive_config(
        AdaptationDomainType.ORGANIZATIONAL,
        CulturalContext.EASTERN_EUROPEAN,
        ProjectType.HR_ASSESSMENT
    )
}


if __name__ == "__main__":
    # Демонстрация конфигураций
    settings = load_settings()
    print(f"Базовые настройки: {settings.domain_type} / {settings.cultural_context}")

    for name, config in EXAMPLE_CONFIGS.items():
        print(f"\n{name}:")
        print(f"  - Домен: {config['domain_type']}")
        print(f"  - Культура: {config['cultural_context']}")
        print(f"  - Мин. вопросов: {config['min_questions']}")
        print(f"  - Жизненные ситуации: {config['life_situations_ratio']:.0%}")
        print(f"  - Уровни результатов: {config['result_levels']}")