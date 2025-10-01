"""
Pattern Integration Synthesizer Agent - системный интегратор программ трансформации.

Специализируется на оркестрации модулей контента в целостные программы,
управлении эмоциональной кривой и обеспечении синергии между модулями.
"""

from pydantic_ai import Agent
from .dependencies import PatternIntegrationSynthesizerDependencies
from .settings import get_llm_model
from .prompts import get_system_prompt
from .tools import (
    orchestrate_module_sequence,
    manage_emotional_curve,
    identify_resistance_points,
    ensure_module_synergy,
    analyze_program_coherence,
    search_agent_knowledge
)


# Создание агента с зависимостями
agent = Agent(
    model=get_llm_model(),
    deps_type=PatternIntegrationSynthesizerDependencies,
    system_prompt=get_system_prompt()
)


# Регистрация инструментов
agent.tool(orchestrate_module_sequence)
agent.tool(manage_emotional_curve)
agent.tool(identify_resistance_points)
agent.tool(ensure_module_synergy)
agent.tool(analyze_program_coherence)
agent.tool(search_agent_knowledge)


async def run_pattern_integration_synthesizer(
    user_message: str,
    api_key: str,
    patternshift_project_path: str = "",
    knowledge_tags: list = None,
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
) -> str:
    """
    Запустить Pattern Integration Synthesizer Agent.

    Args:
        user_message: Сообщение пользователя с запросом
        api_key: API ключ для LLM провайдера
        patternshift_project_path: Путь к проекту PatternShift
        knowledge_tags: Теги для поиска в базе знаний
        archon_project_id: ID проекта в Archon

    Returns:
        Ответ агента

    Examples:
        >>> result = await run_pattern_integration_synthesizer(
        ...     user_message="Оркеструй модули для 21-дневной программы по работе с тревогой",
        ...     api_key=os.getenv("OPENAI_API_KEY"),
        ...     patternshift_project_path="/path/to/patternshift"
        ... )
    """
    if knowledge_tags is None:
        knowledge_tags = [
            "pattern-integration-synthesizer",
            "orchestration",
            "synergy",
            "agent-knowledge",
            "patternshift"
        ]

    # Создание зависимостей
    deps = PatternIntegrationSynthesizerDependencies(
        api_key=api_key,
        patternshift_project_path=patternshift_project_path,
        knowledge_tags=knowledge_tags,
        archon_project_id=archon_project_id
    )

    # Запуск агента
    result = await agent.run(user_message, deps=deps)

    return result.data


async def analyze_program_synergy(
    program_structure: dict,
    api_key: str,
    patternshift_project_path: str = ""
) -> str:
    """
    Анализировать синергию между модулями в программе.

    Args:
        program_structure: Структура программы для анализа
        api_key: API ключ для LLM провайдера
        patternshift_project_path: Путь к проекту PatternShift

    Returns:
        Отчет о синергии модулей

    Examples:
        >>> program = {
        ...     "program_name": "Anxiety Management Program",
        ...     "total_days": 21,
        ...     "phases": [...]
        ... }
        >>> result = await analyze_program_synergy(
        ...     program_structure=program,
        ...     api_key=os.getenv("OPENAI_API_KEY")
        ... )
    """
    message = f"""
Проанализируй синергию модулей в этой программе:

{program_structure}

Оцени:
1. Высокосинергичные комбинации модулей
2. Потенциальные конфликты
3. Оптимальность последовательности
4. Возможности усиления эффектов
"""

    return await run_pattern_integration_synthesizer(
        user_message=message,
        api_key=api_key,
        patternshift_project_path=patternshift_project_path
    )


async def optimize_emotional_curve(
    program_duration_days: int,
    target_conditions: list,
    api_key: str,
    program_intensity: str = "medium"
) -> str:
    """
    Оптимизировать эмоциональную кривую программы.

    Args:
        program_duration_days: Длительность программы в днях
        target_conditions: Целевые состояния (anxiety, depression и т.д.)
        api_key: API ключ для LLM провайдера
        program_intensity: Интенсивность программы (light, medium, intensive)

    Returns:
        План управления эмоциональной кривой

    Examples:
        >>> result = await optimize_emotional_curve(
        ...     program_duration_days=21,
        ...     target_conditions=["anxiety", "stress"],
        ...     api_key=os.getenv("OPENAI_API_KEY"),
        ...     program_intensity="medium"
        ... )
    """
    message = f"""
Оптимизируй эмоциональную кривую для программы:

Длительность: {program_duration_days} дней
Целевые состояния: {', '.join(target_conditions)}
Интенсивность: {program_intensity}

Предоставь:
1. Распределение активностей по стадиям эмоциональной кривой
2. Точки сопротивления и стратегии митигации
3. Оптимальные активности для каждого этапа
4. Рекомендации по поддержке пользователя
"""

    return await run_pattern_integration_synthesizer(
        user_message=message,
        api_key=api_key
    )


async def create_module_sequence(
    module_ids: list,
    phase_type: str,
    target_goals: list,
    api_key: str
) -> str:
    """
    Создать оптимальную последовательность модулей.

    Args:
        module_ids: Список ID модулей для оркестрации
        phase_type: Тип фазы (beginning, development, integration)
        target_goals: Целевые цели программы
        api_key: API ключ для LLM провайдера

    Returns:
        Оптимальная последовательность с обоснованием

    Examples:
        >>> result = await create_module_sequence(
        ...     module_ids=["mod_001", "mod_002", "mod_003"],
        ...     phase_type="beginning",
        ...     target_goals=["reduce anxiety", "build coping skills"],
        ...     api_key=os.getenv("OPENAI_API_KEY")
        ... )
    """
    message = f"""
Оркеструй последовательность модулей:

Модули: {', '.join(module_ids)}
Фаза: {phase_type}
Цели: {', '.join(target_goals)}

Предоставь:
1. Оптимальную последовательность модулей
2. Обоснование выбора паттерна оркестрации
3. Правила синергии для этих модулей
4. Рекомендации по промежуткам между модулями
"""

    return await run_pattern_integration_synthesizer(
        user_message=message,
        api_key=api_key
    )


__all__ = [
    "agent",
    "run_pattern_integration_synthesizer",
    "analyze_program_synergy",
    "optimize_emotional_curve",
    "create_module_sequence"
]
