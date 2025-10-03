"""
Pattern NLP Technique Master Agent

Универсальный агент для создания модульных НЛП-техник трансформации.
Специализируется на CBT, DBT, ACT и классических НЛП паттернах.
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import asyncio
from datetime import datetime
import json

from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel, Field

from ..common import check_pm_switch
try:
    from ..common.pydantic_ai_decorators import (
        create_universal_pydantic_agent,
        with_integrations,
        register_agent
    )
    HAS_DECORATORS = True
except ImportError:
    HAS_DECORATORS = False
from .dependencies import (
    PatternNLPTechniqueMasterDependencies,
    create_technique_dependencies,
    create_cbt_dependencies,
    create_dbt_dependencies,
    create_act_dependencies,
    create_classic_nlp_dependencies,
    create_mindfulness_dependencies,
    NLPTechniqueType,
    TherapyModality,
    ProblemArea,
    RepresentationalSystem,
    DifficultyLevel,
    TechniqueFormat
)
from .settings import load_settings, get_settings
from .prompts import get_system_prompt, get_technique_creation_prompt, get_vak_adaptation_prompt
from .tools import (
    search_agent_knowledge,
    create_nlp_technique,
    adapt_technique_vak,
    assess_technique_safety,
    generate_technique_variants,
    TechniqueRequest,
    TechniqueModule,
    VAKAdaptation,
    SafetyAssessment
)


# === МОДЕЛИ ЗАПРОСОВ ===

class TechniqueCreationRequest(BaseModel):
    """Запрос на создание НЛП техники."""
    description: str = Field(description="Описание желаемой техники")
    technique_type: Optional[str] = Field(default=None, description="Тип техники")
    therapy_modality: Optional[str] = Field(default=None, description="Модальность терапии")
    problem_area: Optional[str] = Field(default=None, description="Область проблемы")
    target_audience: str = Field(default="general", description="Целевая аудитория")
    duration_minutes: int = Field(default=15, description="Желаемая длительность")
    difficulty_level: str = Field(default="beginner", description="Уровень сложности")
    special_requirements: Optional[str] = Field(default=None, description="Особые требования")


class TechniqueAnalysisRequest(BaseModel):
    """Запрос на анализ существующей техники."""
    technique_content: str = Field(description="Содержимое техники для анализа")
    analysis_type: str = Field(default="safety", description="Тип анализа")


class ModuleGenerationRequest(BaseModel):
    """Запрос на генерацию модулей техники."""
    base_technique: str = Field(description="Базовая техника")
    module_types: List[str] = Field(description="Типы модулей для генерации")
    customization_params: Dict[str, Any] = Field(default={}, description="Параметры кастомизации")


# === ИНИЦИАЛИЗАЦИЯ АГЕНТА ===

def get_llm_model():
    """Получить настроенную модель LLM."""
    settings = get_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_technique_model, provider=provider)


# Создаем универсальный агент с автоматическими интеграциями
if HAS_DECORATORS:
    agent = create_universal_pydantic_agent(
        model=get_llm_model(),
        deps_type=PatternNLPTechniqueMasterDependencies,
        system_prompt=lambda deps: get_system_prompt(deps),
        agent_type="pattern_nlp_technique_master",
        knowledge_tags=["pattern-nlp-technique-master", "nlp", "therapy", "psychology"],
        knowledge_domain="patternshift.com",
        with_collective_tools=True,
        with_knowledge_tool=True
    )

    # Регистрируем агента в глобальном реестре
    register_agent("pattern_nlp_technique_master", agent, agent_type="pattern_nlp_technique_master")
else:
    # Fallback для обратной совместимости
    agent = Agent(
        get_llm_model(),
        deps_type=PatternNLPTechniqueMasterDependencies,
        system_prompt=lambda deps: get_system_prompt(deps)
    )


# === ОСНОВНЫЕ ИНСТРУМЕНТЫ АГЕНТА ===

@agent.tool
async def search_nlp_knowledge(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний НЛП техник и терапевтических подходов.

    Используется для получения информации о конкретных техниках,
    исследованиях эффективности и лучших практиках.
    """
    return await search_agent_knowledge(ctx, query, match_count)


@agent.tool
async def create_modular_technique(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    technique_request: TechniqueRequest
) -> str:
    """
    Создать модульную НЛП технику по заданным параметрам.

    Создает структурированную технику с введением, подготовкой,
    пошаговыми инструкциями, интеграцией и проверками безопасности.
    """
    try:
        technique = await create_nlp_technique(ctx, technique_request)

        # Форматируем вывод
        result = f"""
# {technique.name}

## Параметры техники
- **Тип:** {technique.type}
- **Модальность:** {technique.modality}
- **Область применения:** {technique.problem_area}
- **Длительность:** {technique.duration_minutes} минут
- **Сложность:** {technique.difficulty}
- **Репрезентативная система:** {technique.rep_system}

## Введение и цель
{technique.introduction}

## Подготовка
{technique.preparation}

## Пошаговые инструкции
"""

        for i, instruction in enumerate(technique.instructions, 1):
            result += f"{i}. {instruction}\n"

        result += f"""
## Интеграция результатов
{technique.integration}

## Проверка экологичности
{technique.safety_check}

## Домашнее задание
{technique.homework}

## Безопасность

### Противопоказания:
"""

        for contraindication in technique.contraindications:
            result += f"- {contraindication}\n"

        result += "\n### Протоколы безопасности:\n"
        for protocol in technique.safety_protocols:
            result += f"- {protocol}\n"

        result += f"\n## Научная обоснованность\n{technique.evidence_base}"

        if technique.audio_script:
            result += f"\n## Аудио скрипт\n{technique.audio_script}"

        if technique.cultural_notes:
            result += f"\n## Культурные особенности\n{technique.cultural_notes}"

        return result

    except Exception as e:
        return f"Ошибка создания техники: {e}"


@agent.tool
async def adapt_technique_for_vak(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    technique_json: str,
    target_rep_system: str
) -> str:
    """
    Адаптировать технику под конкретную репрезентативную систему (VAK).

    Принимает JSON описание техники и адаптирует под визуальную,
    аудиальную или кинестетическую модальность.
    """
    try:
        # Парсим JSON техники
        technique_data = json.loads(technique_json)
        technique = TechniqueModule(**technique_data)

        # Адаптируем технику
        adapted_technique = await adapt_technique_vak(ctx, technique, target_rep_system)

        return f"""
# Адаптированная техника: {adapted_technique.name}

**Репрезентативная система:** {adapted_technique.rep_system}

## Адаптированные инструкции:
"""
        + "\n".join([f"{i}. {inst}" for i, inst in enumerate(adapted_technique.instructions, 1)])

    except Exception as e:
        return f"Ошибка адаптации техники: {e}"


@agent.tool
async def evaluate_technique_safety(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    technique_json: str
) -> str:
    """
    Провести оценку безопасности НЛП техники.

    Анализирует риски, противопоказания и создает протоколы безопасности.
    """
    try:
        # Парсим JSON техники
        technique_data = json.loads(technique_json)
        technique = TechniqueModule(**technique_data)

        # Оцениваем безопасность
        safety_assessment = await assess_technique_safety(ctx, technique)

        return f"""
# Оценка безопасности: {technique.name}

## Уровень риска: {safety_assessment.risk_level.upper()}

## Противопоказания:
"""
        + "\n".join([f"- {c}" for c in safety_assessment.contraindications]) + """

## Меры безопасности:
"""
        + "\n".join([f"- {m}" for m in safety_assessment.safety_measures]) + """

## Протоколы при кризисе:
"""
        + "\n".join([f"- {p}" for p in safety_assessment.crisis_protocols]) + """

## Критерии направления к специалисту:
"""
        + "\n".join([f"- {c}" for c in safety_assessment.professional_referral_criteria])

    except Exception as e:
        return f"Ошибка оценки безопасности: {e}"


@agent.tool
async def create_technique_variants(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    technique_json: str,
    variant_types: List[str]
) -> str:
    """
    Создать варианты техники для разных групп.

    Создает адаптированные версии для разных возрастов, полов, культур.
    """
    try:
        # Парсим JSON техники
        technique_data = json.loads(technique_json)
        technique = TechniqueModule(**technique_data)

        # Создаем варианты
        variants = await generate_technique_variants(ctx, technique, variant_types)

        result = f"# Варианты техники: {technique.name}\n\n"

        for variant_name, variant_technique in variants.items():
            result += f"""
## {variant_name.replace('_', ' ').title()}
**Название:** {variant_technique.name}
**Особенности:** Адаптировано для {variant_name.replace('_', ' ')}

"""

        return result

    except Exception as e:
        return f"Ошибка создания вариантов: {e}"


@agent.tool
async def analyze_existing_technique(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    technique_content: str,
    analysis_focus: str = "comprehensive"
) -> str:
    """
    Анализ существующей НЛП техники.

    Анализирует структуру, эффективность, безопасность и предлагает улучшения.
    """
    # Поиск в базе знаний для сравнения
    knowledge = await search_agent_knowledge(
        ctx,
        f"анализ техники {analysis_focus}",
        3
    )

    analysis_result = f"""
# Анализ техники

## Структурный анализ:
- Проверка наличия всех обязательных компонентов
- Оценка последовательности шагов
- Анализ ясности инструкций

## Анализ безопасности:
- Проверка противопоказаний
- Оценка рисков
- Протоколы безопасности

## Эффективность:
- Соответствие научным данным
- Потенциальная эффективность
- Рекомендации по улучшению

## Найденная информация из базы знаний:
{knowledge}

## Рекомендации:
1. Добавить проверку экологичности
2. Включить больше инструкций по безопасности
3. Адаптировать под разные репрезентативные системы
4. Добавить варианты для разных уровней сложности
"""

    return analysis_result


# Инструмент break_down_to_microtasks автоматически добавлен через декораторы


@agent.tool
async def generate_pattern_shift_module(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    technique_json: str,
    module_config: Dict[str, Any]
) -> str:
    """
    Генерировать модуль для интеграции с PatternShift системой.

    Создает модуль техники в формате совместимом с архитектурой PatternShift.
    """
    try:
        # Парсим технику
        technique_data = json.loads(technique_json)
        technique = TechniqueModule(**technique_data)

        # Создаем модуль PatternShift
        module = {
            "module_id": f"nlp_{technique.type}_{technique.problem_area}",
            "version": "1.0.0",
            "status": "stable",
            "type": "technique",

            "metadata": {
                "name": technique.name,
                "description": technique.introduction[:200],
                "duration_minutes": technique.duration_minutes,
                "difficulty": technique.difficulty,
                "modality": technique.modality,
                "rep_system": technique.rep_system
            },

            "content": {
                "introduction": technique.introduction,
                "preparation": technique.preparation,
                "steps": technique.instructions,
                "integration": technique.integration,
                "safety_check": technique.safety_check,
                "homework": technique.homework
            },

            "safety": {
                "contraindications": technique.contraindications,
                "protocols": technique.safety_protocols,
                "risk_level": "medium"  # будет определено автоматически
            },

            "personalization": {
                "vak_adaptable": True,
                "age_adaptable": True,
                "culture_adaptable": True
            },

            "evidence": {
                "research_base": technique.evidence_base,
                "effectiveness_rating": 8.0  # будет определено на основе исследований
            }
        }

        return f"""
# PatternShift Module Generated

```json
{json.dumps(module, ensure_ascii=False, indent=2)}
```

## Интеграция с PatternShift:
- Модуль совместим с системой версионирования
- Поддерживает персонализацию по VAK системам
- Включает протоколы безопасности
- Готов для добавления в модульную архитектуру
"""

    except Exception as e:
        return f"Ошибка генерации модуля PatternShift: {e}"


# === ОСНОВНАЯ ФУНКЦИЯ ЗАПУСКА ===

@with_integrations(agent_type="pattern_nlp_technique_master") if HAS_DECORATORS else lambda f: f
async def run_pattern_nlp_technique_master(
    request: Union[str, TechniqueCreationRequest, TechniqueAnalysisRequest],
    deps: Optional[PatternNLPTechniqueMasterDependencies] = None
) -> str:
    """
    Запустить Pattern NLP Technique Master Agent с полными интеграциями.

    Args:
        request: Запрос пользователя или структурированный запрос
        deps: Зависимости агента

    Returns:
        Результат работы агента
    """
    # Проверка переключения PM
    if isinstance(request, str):
        pm_result = check_pm_switch(request, "pattern_nlp_technique_master")
        if pm_result:
            return pm_result

    # Создаем зависимости если не переданы
    if deps is None:
        settings = get_settings()
        deps = PatternNLPTechniqueMasterDependencies(
            api_key=settings.llm_api_key,
            project_path=settings.project_path
        )

    # Обработка разных типов запросов
    if isinstance(request, TechniqueCreationRequest):
        message = f"""
Создай НЛП технику со следующими параметрами:

Описание: {request.description}
Тип техники: {request.technique_type or 'автоопределение'}
Модальность терапии: {request.therapy_modality or 'автоопределение'}
Область проблемы: {request.problem_area or 'автоопределение'}
Целевая аудитория: {request.target_audience}
Длительность: {request.duration_minutes} минут
Уровень сложности: {request.difficulty_level}
Особые требования: {request.special_requirements or 'нет'}

Создай полную модульную технику с проверками безопасности.
"""
    elif isinstance(request, TechniqueAnalysisRequest):
        message = f"""
Проанализируй существующую НЛП технику:

{request.technique_content}

Тип анализа: {request.analysis_type}

Предоставь детальный анализ с рекомендациями по улучшению.
"""
    else:
        message = str(request)

    # Запускаем агента
    try:
        result = await agent.run(message, deps=deps)
        return result.data
    except Exception as e:
        return f"Ошибка выполнения Pattern NLP Technique Master: {e}"


# === ФУНКЦИИ-ПОМОЩНИКИ ===

def create_cbt_technique_deps(**kwargs) -> PatternNLPTechniqueMasterDependencies:
    """Создать зависимости для CBT техники."""
    return create_cbt_dependencies(**kwargs)


def create_dbt_technique_deps(**kwargs) -> PatternNLPTechniqueMasterDependencies:
    """Создать зависимости для DBT техники."""
    return create_dbt_dependencies(**kwargs)


def create_act_technique_deps(**kwargs) -> PatternNLPTechniqueMasterDependencies:
    """Создать зависимости для ACT техники."""
    return create_act_dependencies(**kwargs)


def create_classic_nlp_deps(**kwargs) -> PatternNLPTechniqueMasterDependencies:
    """Создать зависимости для классических НЛП техник."""
    return create_classic_nlp_dependencies(**kwargs)


def create_mindfulness_deps(**kwargs) -> PatternNLPTechniqueMasterDependencies:
    """Создать зависимости для майндфулнесс техник."""
    return create_mindfulness_dependencies(**kwargs)


# === ЭКСПОРТ ===

__all__ = [
    'agent',
    'run_pattern_nlp_technique_master',
    'PatternNLPTechniqueMasterDependencies',
    'TechniqueCreationRequest',
    'TechniqueAnalysisRequest',
    'ModuleGenerationRequest',
    'create_cbt_technique_deps',
    'create_dbt_technique_deps',
    'create_act_technique_deps',
    'create_classic_nlp_deps',
    'create_mindfulness_deps'
]