"""
Pattern VAK Adaptation Specialist Agent.

Агент для адаптации психологического контента под различные сенсорные модальности
(Visual, Auditory, Kinesthetic) в рамках PatternShift системы.

Улучшения v1.1.0:
- Добавлены расширенные валидаторы безопасности
- Улучшена обработка ошибок в инструментах
- Добавлена комплексная система проверки качества
- Расширены примеры конфигураций
"""

from .agent import (
    PatternVAKAdaptationAgent,
    VAKAdaptationRequest,
    VAKAdaptationResponse,
    BatchVAKAdaptationRequest,
    BatchVAKAdaptationResponse
)
from .dependencies import (
    PatternVAKAdaptationDependencies,
    VAKModalityType,
    AdaptationDepth,
    PatternShiftModuleType,
    create_vak_adaptation_dependencies,
    VISUAL_PREDICATES,
    AUDITORY_PREDICATES,
    KINESTHETIC_PREDICATES
)
from .tools import (
    analyze_content_vak_modalities,
    adapt_content_to_vak_modality,
    create_multimodal_variants,
    validate_vak_adaptation,
    search_vak_knowledge_base,
    generate_vak_adaptation_report
)
from .validators import (
    SafetyValidator,
    QualityValidator,
    IntegrityValidator,
    CompositeValidator,
    ValidationSeverity,
    ValidationResult,
    create_safety_validator,
    create_quality_validator,
    create_integrity_validator,
    create_composite_validator
)
from .settings import get_settings, PatternVAKSettings
from .examples import (
    get_example_for_module_type,
    get_all_available_examples,
    get_recommended_config_for_context,
    create_multi_modal_example_set
)

__version__ = "1.1.0"

__all__ = [
    # Основной агент
    "PatternVAKAdaptationAgent",

    # Модели запросов и ответов
    "VAKAdaptationRequest",
    "VAKAdaptationResponse",
    "BatchVAKAdaptationRequest",
    "BatchVAKAdaptationResponse",

    # Зависимости и конфигурация
    "PatternVAKAdaptationDependencies",
    "PatternVAKSettings",

    # Типы и энумы
    "VAKModalityType",
    "AdaptationDepth",
    "PatternShiftModuleType",
    "ValidationSeverity",

    # Результаты валидации
    "ValidationResult",

    # Функции создания зависимостей
    "create_vak_adaptation_dependencies",

    # Основные инструменты адаптации
    "analyze_content_vak_modalities",
    "adapt_content_to_vak_modality",
    "create_multimodal_variants",
    "validate_vak_adaptation",
    "search_vak_knowledge_base",
    "generate_vak_adaptation_report",

    # Валидаторы
    "SafetyValidator",
    "QualityValidator",
    "IntegrityValidator",
    "CompositeValidator",
    "create_safety_validator",
    "create_quality_validator",
    "create_integrity_validator",
    "create_composite_validator",

    # Примеры и конфигурации
    "get_example_for_module_type",
    "get_all_available_examples",
    "get_recommended_config_for_context",
    "create_multi_modal_example_set",

    # Настройки
    "get_settings",

    # Константы предикатов
    "VISUAL_PREDICATES",
    "AUDITORY_PREDICATES",
    "KINESTHETIC_PREDICATES"
]


# Удобные функции для быстрого старта

def quick_adapt(
    content: dict,
    target_modality: VAKModalityType,
    api_key: str = None,
    preserve_safety: bool = True
) -> dict:
    """
    Быстрая адаптация контента под модальность.

    Args:
        content: Словарь с контентом (title, content, module_type)
        target_modality: Целевая модальность
        api_key: API ключ (если не указан, берется из настроек)
        preserve_safety: Включить проверки безопасности

    Returns:
        Адаптированный контент

    Example:
        adapted = quick_adapt(
            content={"title": "Техника", "content": "...", "module_type": "technique"},
            target_modality=VAKModalityType.VISUAL
        )
    """
    import asyncio
    from .settings import get_settings

    if not api_key:
        settings = get_settings()
        api_key = settings.llm_api_key

    deps = create_vak_adaptation_dependencies(
        api_key=api_key,
        enable_safety_validation=preserve_safety
    )

    async def _adapt():
        return await adapt_content_to_vak_modality(
            dependencies=deps,
            content=content,
            target_modality=target_modality,
            preserve_core_message=True
        )

    return asyncio.run(_adapt())


def quick_analyze(content: dict, api_key: str = None) -> dict:
    """
    Быстрый анализ VAK модальностей контента.

    Args:
        content: Словарь с контентом для анализа
        api_key: API ключ (если не указан, берется из настроек)

    Returns:
        Результаты анализа модальностей

    Example:
        analysis = quick_analyze({"title": "Техника", "content": "..."})
        print(f"Доминирующая модальность: {analysis['dominant_modality']}")
    """
    import asyncio
    from .settings import get_settings

    if not api_key:
        settings = get_settings()
        api_key = settings.llm_api_key

    deps = create_vak_adaptation_dependencies(api_key=api_key)

    async def _analyze():
        return await analyze_content_vak_modalities(
            dependencies=deps,
            content=content,
            include_recommendations=True
        )

    return asyncio.run(_analyze())


def create_therapy_agent(api_key: str) -> PatternVAKAdaptationAgent:
    """
    Создать агент для терапевтического контекста.

    Args:
        api_key: API ключ для LLM

    Returns:
        Настроенный агент для терапии

    Example:
        agent = create_therapy_agent("your_api_key")
        response = await agent.adapt_content(request)
    """
    deps = create_vak_adaptation_dependencies(
        api_key=api_key,
        adaptation_depth=AdaptationDepth.DEEP,
        trauma_informed_adaptations=True,
        preserve_therapeutic_integrity=True,
        enable_safety_validation=True,
        safety_keywords=["безопасно", "комфортно", "границы", "выбор"],
        therapeutic_frameworks=["trauma-informed", "person-centered"]
    )
    return PatternVAKAdaptationAgent(dependencies=deps)


def create_coaching_agent(api_key: str) -> PatternVAKAdaptationAgent:
    """
    Создать агент для коучингового контекста.

    Args:
        api_key: API ключ для LLM

    Returns:
        Настроенный агент для коучинга

    Example:
        agent = create_coaching_agent("your_api_key")
        variants = await agent.create_multimodal_variants(content)
    """
    deps = create_vak_adaptation_dependencies(
        api_key=api_key,
        adaptation_depth=AdaptationDepth.MODERATE,
        enable_multimodal=True,
        batch_adaptation_size=10,
        knowledge_tags=["coaching", "goal-achievement", "performance"]
    )
    return PatternVAKAdaptationAgent(dependencies=deps)


# Добавляем quick функции в __all__
__all__.extend([
    "quick_adapt",
    "quick_analyze",
    "create_therapy_agent",
    "create_coaching_agent"
])