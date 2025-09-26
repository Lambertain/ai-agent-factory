"""
Psychology Quality Guardian Agent

Универсальный агент для контроля качества психологического контента.
Обеспечивает этическое соответствие, научную валидность и безопасность
психологических программ, тестов и интервенций.

Поддерживает домены:
- Clinical Psychology (клиническая психология)
- Research Psychology (исследовательская психология)
- Educational Psychology (образовательная психология)
- Wellness Psychology (психология благополучия)
- Organizational Psychology (организационная психология)

Возможности:
- Этическая экспертиза по стандартам APA, BPS, ITC
- Научная валидация и психометрическая оценка
- Анализ безопасности и управление рисками
- Культурная адаптация и инклюзивность
- Автоматизированная отчетность и рекомендации
"""

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Universal Psychology Quality Guardian Agent for content validation"

# Основные компоненты агента
from .agent import (
    psychology_quality_guardian_agent,
    QualityEvaluationRequest,
    ComplianceAuditRequest,
    SafetyAssessmentRequest,
    evaluate_content_quality,
    audit_compliance,
    assess_content_safety,
    batch_quality_evaluation,
    create_quality_improvement_plan
)

# Конфигурация и зависимости
from .dependencies import (
    QualityGuardianDependencies,
    create_clinical_dependencies,
    create_research_dependencies,
    create_educational_dependencies,
    create_wellness_dependencies,
    create_organizational_dependencies
)

# Настройки
from .settings import (
    PsychologyQualityGuardianSettings,
    load_settings,
    create_clinical_settings,
    create_research_settings,
    create_educational_settings,
    create_wellness_settings
)

# Провайдеры моделей
from .providers import (
    QualityGuardianModelProvider,
    get_model_provider,
    get_llm_model,
    get_default_model
)

# Промпты
from .prompts import (
    get_system_prompt,
    get_task_specific_prompt,
    get_reporting_prompt
)

# Инструменты
from .tools import (
    search_quality_guardian_knowledge,
    evaluate_ethical_compliance,
    assess_scientific_validity,
    analyze_content_safety,
    validate_psychometric_properties,
    check_cultural_sensitivity,
    generate_quality_report,
    create_improvement_recommendations
)


# Основные экспорты
__all__ = [
    # Основной агент
    "psychology_quality_guardian_agent",

    # Классы запросов
    "QualityEvaluationRequest",
    "ComplianceAuditRequest",
    "SafetyAssessmentRequest",

    # Основные функции
    "evaluate_content_quality",
    "audit_compliance",
    "assess_content_safety",
    "batch_quality_evaluation",
    "create_quality_improvement_plan",

    # Зависимости
    "QualityGuardianDependencies",
    "create_clinical_dependencies",
    "create_research_dependencies",
    "create_educational_dependencies",
    "create_wellness_dependencies",
    "create_organizational_dependencies",

    # Настройки
    "PsychologyQualityGuardianSettings",
    "load_settings",
    "create_clinical_settings",
    "create_research_settings",
    "create_educational_settings",
    "create_wellness_settings",

    # Провайдеры
    "QualityGuardianModelProvider",
    "get_model_provider",
    "get_llm_model",
    "get_default_model",

    # Промпты
    "get_system_prompt",
    "get_task_specific_prompt",
    "get_reporting_prompt",

    # Инструменты
    "search_quality_guardian_knowledge",
    "evaluate_ethical_compliance",
    "assess_scientific_validity",
    "analyze_content_safety",
    "validate_psychometric_properties",
    "check_cultural_sensitivity",
    "generate_quality_report",
    "create_improvement_recommendations"
]


# Удобные функции для быстрого старта
def get_quality_guardian_config(
    domain: str = "general",
    population: str = "adults",
    compliance_level: str = "standard",
    **kwargs
) -> QualityGuardianDependencies:
    """
    Быстрое создание конфигурации Quality Guardian для любого домена.

    Args:
        domain: Домен психологии (clinical, research, educational, wellness, organizational)
        population: Целевая популяция (adults, children, adolescents, elderly)
        compliance_level: Уровень соответствия (basic, standard, comprehensive, research_grade)
        **kwargs: Дополнительные параметры

    Returns:
        Настроенные зависимости агента
    """

    # Фабричные функции для разных доменов
    domain_factories = {
        "clinical": create_clinical_dependencies,
        "research": create_research_dependencies,
        "educational": create_educational_dependencies,
        "wellness": create_wellness_dependencies,
        "organizational": create_organizational_dependencies
    }

    # Используем фабричную функцию если доступна
    if domain in domain_factories:
        factory = domain_factories[domain]
        # Получаем API ключ из kwargs или настроек
        api_key = kwargs.pop("api_key", load_settings().llm_api_key)
        return factory(
            api_key=api_key,
            target_population=population,
            compliance_level=compliance_level,
            **kwargs
        )

    # Общая конфигурация для неспециализированных доменов
    api_key = kwargs.pop("api_key", load_settings().llm_api_key)
    return QualityGuardianDependencies(
        api_key=api_key,
        domain_type=domain,
        target_population=population,
        compliance_level=compliance_level,
        **kwargs
    )


async def quick_quality_check(
    content: dict,
    domain: str = "general",
    population: str = "adults",
    focus_areas: list = None
) -> dict:
    """
    Быстрая проверка качества психологического контента.

    Args:
        content: Контент для проверки
        domain: Домен психологии
        population: Целевая популяция
        focus_areas: Области фокуса (по умолчанию: ethical, scientific, safety)

    Returns:
        Результат оценки качества
    """

    if focus_areas is None:
        focus_areas = ["ethical", "scientific", "safety"]

    # Создаем конфигурацию
    deps = get_quality_guardian_config(domain=domain, population=population)

    # Создаем запрос на оценку
    request = QualityEvaluationRequest(
        content_type="assessment",
        content_data=content,
        evaluation_scope=focus_areas,
        target_population=population,
        domain=domain
    )

    # Выполняем оценку
    return await evaluate_content_quality(request, deps)


# Примеры использования
USAGE_EXAMPLES = {
    "clinical_assessment": """
# Пример: Оценка клинического теста
from psychology_quality_guardian import quick_quality_check

test_content = {
    "name": "Depression Screening Scale",
    "questions": [...],
    "scoring": {...}
}

result = await quick_quality_check(
    content=test_content,
    domain="clinical",
    population="adults",
    focus_areas=["ethical", "clinical_validity", "safety"]
)
""",

    "research_validation": """
# Пример: Валидация исследовательского инструмента
from psychology_quality_guardian import evaluate_content_quality, create_research_dependencies

deps = create_research_dependencies(
    api_key="your_api_key",
    target_population="adults"
)

request = QualityEvaluationRequest(
    content_type="test",
    content_data=research_instrument,
    evaluation_scope=["scientific", "psychometric", "ethical"],
    standards_level="research_grade"
)

result = await evaluate_content_quality(request, deps)
""",

    "educational_content": """
# Пример: Проверка образовательного контента
from psychology_quality_guardian import get_quality_guardian_config, assess_content_safety

deps = get_quality_guardian_config(
    domain="educational",
    population="adolescents",
    compliance_level="standard"
)

safety_request = SafetyAssessmentRequest(
    content_data=educational_material,
    risk_categories=["psychological", "privacy", "ethical"],
    vulnerability_groups=["adolescents"]
)

safety_report = await assess_content_safety(safety_request, deps)
""",

    "wellness_app": """
# Пример: Валидация wellness приложения
from psychology_quality_guardian import batch_quality_evaluation, create_wellness_dependencies

deps = create_wellness_dependencies(
    api_key="your_api_key",
    wellness_focus="mental_health"
)

app_components = [
    {"type": "mood_tracker", "content": mood_tracker_data},
    {"type": "meditation", "content": meditation_content},
    {"type": "progress_report", "content": reporting_system}
]

batch_result = await batch_quality_evaluation(
    content_items=app_components,
    evaluation_parameters={
        "scope": ["safety", "engagement", "effectiveness"],
        "domain": "wellness",
        "population": "adults"
    },
    dependencies=deps
)
"""
}


# Метаданные агента
AGENT_METADATA = {
    "name": "Psychology Quality Guardian Agent",
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "capabilities": [
        "Ethical compliance validation",
        "Scientific validity assessment",
        "Safety risk analysis",
        "Cultural sensitivity checking",
        "Psychometric properties validation",
        "Automated quality reporting",
        "Improvement recommendations",
        "Multi-domain support",
        "Batch processing",
        "Real-time monitoring"
    ],
    "supported_domains": [
        "clinical",
        "research",
        "educational",
        "wellness",
        "organizational",
        "general"
    ],
    "supported_populations": [
        "adults",
        "children",
        "adolescents",
        "elderly",
        "mixed",
        "clinical"
    ],
    "standards_compliance": [
        "APA Ethics Code",
        "BPS Guidelines",
        "ITC Standards",
        "GDPR",
        "HIPAA (optional)",
        "DSM-5",
        "ICD-11"
    ],
    "usage_examples": USAGE_EXAMPLES
}