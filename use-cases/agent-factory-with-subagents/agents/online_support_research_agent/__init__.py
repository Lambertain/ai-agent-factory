"""
Psychology Research Agent

Универсальный агент для валидации психологических исследований, обеспечения
научной строгости и методологической корректности в области психологии.

Основные возможности:
- Валидация методологии исследований
- Статистический анализ и проверка
- Систематический поиск литературы
- Мета-анализ и систематические обзоры
- Этическая экспертиза
- Оценка качества исследований
- Исследовательские консультации

Поддерживаемые домены:
- Clinical Psychology (клиническая психология)
- Cognitive Psychology (когнитивная психология)
- Social Psychology (социальная психология)
- Developmental Psychology (психология развития)
- Educational Psychology (образовательная психология)

Возможности:
- Методологическая валидация по международным стандартам
- Статистическая экспертиза и анализ мощности
- Систематический поиск и анализ литературы
- Планирование мета-анализов
- Этическая экспертиза исследований
- Автоматизированная отчетность
- Интеграция с Psychology Quality Guardian Agent
"""

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Universal Psychology Research Agent for research validation and methodology"

# Основные компоненты агента
from .agent import (
    psychology_research_agent,
    create_psychology_research_agent,
    validate_research_study,
    conduct_literature_review,
    assess_study_quality,
    create_meta_analysis_plan,
    provide_research_consultation,
    batch_validate_studies,
    create_clinical_research_agent,
    create_cognitive_research_agent,
    create_social_research_agent,
    get_research_recommendations,
    get_validation_summary,
    ResearchValidationRequest,
    LiteratureReviewRequest,
    QualityAssessmentRequest
)

# Зависимости и конфигурация
from .dependencies import (
    ResearchAgentDependencies,
    create_clinical_dependencies,
    create_cognitive_dependencies,
    create_social_dependencies,
    create_developmental_dependencies,
    create_educational_dependencies
)

# Настройки
from .settings import (
    PsychologyResearchAgentSettings,
    load_settings,
    create_clinical_settings,
    create_cognitive_settings,
    create_social_settings,
    create_developmental_settings,
    create_educational_settings
)

# Провайдеры моделей
from .providers import (
    ResearchModelProvider,
    get_model_provider,
    get_llm_model,
    get_default_model
)

# Промпты
from .prompts import (
    get_system_prompt,
    get_methodology_analysis_prompt,
    get_statistical_validation_prompt,
    get_literature_search_prompt,
    get_meta_analysis_prompt,
    get_ethics_review_prompt
)

# Инструменты
from .tools import (
    search_research_knowledge,
    analyze_study_methodology,
    validate_statistical_analysis,
    search_literature,
    evaluate_study_quality,
    perform_meta_analysis_planning,
    break_down_to_microtasks,
    delegate_task_to_agent,
    check_delegation_need,
    StudyAnalysisRequest,
    LiteratureSearchRequest,
    StatisticalValidationRequest,
    MethodologyAssessmentRequest
)


# Основные экспорты
__all__ = [
    # Основной агент
    "psychology_research_agent",

    # Классы запросов
    "ResearchValidationRequest",
    "LiteratureReviewRequest",
    "QualityAssessmentRequest",
    "StudyAnalysisRequest",
    "LiteratureSearchRequest",
    "StatisticalValidationRequest",
    "MethodologyAssessmentRequest",

    # Основные функции
    "validate_research_study",
    "conduct_literature_review",
    "assess_study_quality",
    "create_meta_analysis_plan",
    "provide_research_consultation",
    "batch_validate_studies",

    # Фабричные функции агентов
    "create_psychology_research_agent",
    "create_clinical_research_agent",
    "create_cognitive_research_agent",
    "create_social_research_agent",

    # Зависимости
    "ResearchAgentDependencies",
    "create_clinical_dependencies",
    "create_cognitive_dependencies",
    "create_social_dependencies",
    "create_developmental_dependencies",
    "create_educational_dependencies",

    # Настройки
    "PsychologyResearchAgentSettings",
    "load_settings",
    "create_clinical_settings",
    "create_cognitive_settings",
    "create_social_settings",
    "create_developmental_settings",
    "create_educational_settings",

    # Провайдеры
    "ResearchModelProvider",
    "get_model_provider",
    "get_llm_model",
    "get_default_model",

    # Промпты
    "get_system_prompt",
    "get_methodology_analysis_prompt",
    "get_statistical_validation_prompt",
    "get_literature_search_prompt",
    "get_meta_analysis_prompt",
    "get_ethics_review_prompt",

    # Инструменты
    "search_research_knowledge",
    "analyze_study_methodology",
    "validate_statistical_analysis",
    "search_literature",
    "evaluate_study_quality",
    "perform_meta_analysis_planning",
    "break_down_to_microtasks",
    "delegate_task_to_agent",
    "check_delegation_need",

    # Утилиты
    "get_research_recommendations",
    "get_validation_summary"
]


# Удобные функции для быстрого старта
def get_research_agent_config(
    domain: str = "general",
    population: str = "adults",
    validation_level: str = "standard",
    **kwargs
) -> ResearchAgentDependencies:
    """
    Быстрое создание конфигурации Research Agent для любого домена.

    Args:
        domain: Домен психологии (clinical, cognitive, social, developmental, educational)
        population: Целевая популяция (adults, children, adolescents, elderly, clinical)
        validation_level: Уровень валидации (basic, standard, rigorous, publication_grade)
        **kwargs: Дополнительные параметры

    Returns:
        Настроенные зависимости агента
    """

    # Фабричные функции для разных доменов
    domain_factories = {
        "clinical": create_clinical_dependencies,
        "cognitive": create_cognitive_dependencies,
        "social": create_social_dependencies,
        "developmental": create_developmental_dependencies,
        "educational": create_educational_dependencies
    }

    # Используем фабричную функцию если доступна
    if domain in domain_factories:
        factory = domain_factories[domain]
        # Получаем API ключ из kwargs или настроек
        api_key = kwargs.pop("api_key", load_settings().llm_api_key)
        return factory(
            api_key=api_key,
            target_population=population,
            validation_level=validation_level,
            **kwargs
        )

    # Общая конфигурация для неспециализированных доменов
    api_key = kwargs.pop("api_key", load_settings().llm_api_key)
    return ResearchAgentDependencies(
        api_key=api_key,
        research_domain=domain,
        target_population=population,
        validation_level=validation_level,
        **kwargs
    )


async def quick_research_validation(
    research_data: dict,
    domain: str = "general",
    population: str = "adults",
    validation_scope: list = None
) -> dict:
    """
    Быстрая валидация психологического исследования.

    Args:
        research_data: Данные исследования для валидации
        domain: Домен психологии
        population: Целевая популяция
        validation_scope: Области валидации (по умолчанию: methodology, statistics, ethics)

    Returns:
        Результат валидации исследования
    """

    if validation_scope is None:
        validation_scope = ["methodology", "statistics", "ethics"]

    # Создаем конфигурацию
    deps = get_research_agent_config(domain=domain, population=population)

    # Создаем запрос на валидацию
    request = ResearchValidationRequest(
        research_data=research_data,
        validation_scope=validation_scope,
        research_domain=domain,
        target_population=population
    )

    # Выполняем валидацию
    return await validate_research_study(request, deps)


# Примеры использования
USAGE_EXAMPLES = {
    "clinical_study_validation": """
# Пример: Валидация клинического исследования
from psychology_research_agent import quick_research_validation

study_data = {
    "title": "Efficacy of CBT for Depression",
    "design": "randomized_controlled_trial",
    "sample_size": 120,
    "participants": {...},
    "intervention": {...},
    "outcomes": {...}
}

result = await quick_research_validation(
    research_data=study_data,
    domain="clinical",
    population="adults",
    validation_scope=["methodology", "statistics", "ethics", "clinical_validity"]
)
""",

    "literature_review": """
# Пример: Систематический обзор литературы
from psychology_research_agent import conduct_literature_review, LiteratureReviewRequest

request = LiteratureReviewRequest(
    research_question="What is the effectiveness of mindfulness interventions for anxiety?",
    review_type="systematic",
    inclusion_criteria=[
        "randomized controlled trials",
        "adult populations",
        "anxiety disorders",
        "mindfulness interventions"
    ]
)

result = await conduct_literature_review(request)
""",

    "cognitive_experiment": """
# Пример: Валидация когнитивного эксперимента
from psychology_research_agent import create_cognitive_research_agent

agent = create_cognitive_research_agent(
    api_key="your_api_key",
    target_population="adults",
    validation_level="standard"
)

experiment_data = {
    "paradigm": "stroop_task",
    "design": "within_subjects",
    "variables": {...},
    "analysis": {...}
}

result = await agent.run(f"Validate cognitive experiment: {experiment_data}")
""",

    "meta_analysis_planning": """
# Пример: Планирование мета-анализа
from psychology_research_agent import create_meta_analysis_plan

plan = await create_meta_analysis_plan(
    research_question="Effect of exercise on depression in adults",
    inclusion_criteria=[
        "randomized controlled trials",
        "exercise interventions",
        "depression outcomes",
        "adult participants"
    ]
)
""",

    "batch_validation": """
# Пример: Пакетная валидация исследований
from psychology_research_agent import batch_validate_studies

studies = [
    {"study_1_data": {...}},
    {"study_2_data": {...}},
    {"study_3_data": {...}}
]

validation_params = {
    "validation_scope": ["methodology", "statistics"],
    "research_domain": "social",
    "validation_level": "rigorous"
}

results = await batch_validate_studies(studies, validation_params)
"""
}


# Метаданные агента
AGENT_METADATA = {
    "name": "Psychology Research Agent",
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "capabilities": [
        "Methodology validation and analysis",
        "Statistical analysis and power calculation",
        "Systematic literature search and review",
        "Meta-analysis and systematic review planning",
        "Ethics review and compliance checking",
        "Study quality assessment",
        "Research consultation and recommendations",
        "Multi-domain psychology support",
        "Batch processing of multiple studies",
        "Integration with Quality Guardian Agent"
    ],
    "supported_domains": [
        "clinical",
        "cognitive",
        "social",
        "developmental",
        "educational",
        "general"
    ],
    "supported_populations": [
        "adults",
        "children",
        "adolescents",
        "elderly",
        "clinical",
        "mixed"
    ],
    "validation_levels": [
        "basic",
        "standard",
        "rigorous",
        "publication_grade"
    ],
    "research_methodologies": [
        "quantitative",
        "qualitative",
        "mixed_methods"
    ],
    "standards_compliance": [
        "CONSORT - Randomized Trials",
        "STROBE - Observational Studies",
        "PRISMA - Systematic Reviews",
        "STARD - Diagnostic Studies",
        "COREQ - Qualitative Research",
        "APA Style - Reporting Standards",
        "APA Ethics Code",
        "Declaration of Helsinki",
        "Belmont Report"
    ],
    "usage_examples": USAGE_EXAMPLES
}