"""
Pattern Test Architect Agent

Специализированный агент для создания психологических тестов и диагностических инструментов
в рамках системы PatternShift с полной интеграцией коллективных инструментов.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Union
from pydantic_ai import Agent, RunContext

from .settings import get_llm_model
from .dependencies import PatternTestArchitectDependencies
from .prompts import get_system_prompt
from .models import (
    TestRequest,
    TestResponse,
    TestQuestion,
    TestResult,
    PsychometricValidation,
    ViralTestTransformation
)
from .tools import (
    validate_psychometric_properties,
    transform_academic_to_viral,
    generate_test_questions,
    create_interpretation_scales,
    analyze_test_effectiveness,
    search_agent_knowledge
)

# Попытка импорта универсальных декораторов
try:
    from ..common.pydantic_ai_decorators import (
        create_universal_pydantic_agent,
        with_integrations,
        register_agent
    )
    HAS_DECORATORS = True
except ImportError:
    HAS_DECORATORS = False

# Импорт обязательных инструментов коллективной работы
try:
    from ..common.collective_work_tools import (
        break_down_to_microtasks,
        report_microtask_progress,
        reflect_and_improve,
        check_delegation_need,
        delegate_task_to_agent
    )
    HAS_COLLECTIVE_TOOLS = True
except ImportError:
    HAS_COLLECTIVE_TOOLS = False

logger = logging.getLogger(__name__)

# === СОЗДАНИЕ АГЕНТА С ПОЛНОЙ ИНТЕГРАЦИЕЙ ===

if HAS_DECORATORS:
    # Используем новую универсальную архитектуру с автоматическими интеграциями
    agent = create_universal_pydantic_agent(
        model=get_llm_model(),
        deps_type=PatternTestArchitectDependencies,
        system_prompt=lambda deps: get_system_prompt(deps),
        agent_type="pattern_test_architect",
        knowledge_tags=["pattern-test-architect", "psychometry", "psychological-tests", "patternshift"],
        knowledge_domain="patternshift.com",
        with_collective_tools=True,
        with_knowledge_tool=True
    )
    logger.info("Pattern Test Architect Agent создан с универсальными декораторами")
else:
    # Fallback для старой архитектуры
    agent = Agent(
        model=get_llm_model(),
        deps_type=PatternTestArchitectDependencies,
        system_prompt=lambda deps: get_system_prompt(deps)
    )

    # Добавляем инструменты вручную
    agent.tool(search_agent_knowledge)

    # Добавляем обязательные инструменты коллективной работы вручную
    if HAS_COLLECTIVE_TOOLS:
        agent.tool(break_down_to_microtasks)
        agent.tool(report_microtask_progress)
        agent.tool(reflect_and_improve)
        agent.tool(check_delegation_need)
        agent.tool(delegate_task_to_agent)
        logger.info("Добавлены обязательные инструменты коллективной работы")

    logger.info("Pattern Test Architect Agent создан с fallback архитектурой")

# === РЕГИСТРАЦИЯ СПЕЦИАЛИЗИРОВАННЫХ ИНСТРУМЕНТОВ ПСИХОМЕТРИИ ===

@agent.tool
async def create_psychological_test(
    ctx: RunContext[PatternTestArchitectDependencies],
    test_name: str,
    base_methodology: str,
    psychological_construct: str,
    question_count: int = 10,
    target_audience: str = "general"
) -> str:
    """
    Создание психологического теста на основе научной методики.

    Args:
        ctx: Контекст выполнения с зависимостями
        test_name: Вирусное название теста
        base_methodology: Базовая методика (PHQ-9, GAD-7, etc.)
        psychological_construct: Психологический конструкт
        question_count: Количество вопросов
        target_audience: Целевая аудитория

    Returns:
        JSON строка с готовым тестом
    """
    try:
        from .models import PsychologicalConstruct, TargetAudience, DifficultyLevel

        # Преобразование строки в enum
        construct_map = {
            "depression": PsychologicalConstruct.DEPRESSION,
            "anxiety": PsychologicalConstruct.ANXIETY,
            "stress": PsychologicalConstruct.STRESS,
            "self_esteem": PsychologicalConstruct.SELF_ESTEEM
        }
        construct = construct_map.get(psychological_construct.lower(), PsychologicalConstruct.DEPRESSION)

        audience_map = {
            "general": TargetAudience.GENERAL,
            "teens": TargetAudience.TEENS,
            "adults": TargetAudience.ADULTS,
            "professionals": TargetAudience.PROFESSIONALS
        }
        audience = audience_map.get(target_audience.lower(), TargetAudience.GENERAL)

        # Валидация методики
        validation = await validate_psychometric_properties(base_methodology, construct)

        if not validation.is_valid:
            return f"Ошибка: Методика '{base_methodology}' не подходит. Проблемы: {', '.join(validation.issues)}"

        # Трансформация в вирусное название
        viral_transformation = await transform_academic_to_viral(
            academic_name=test_name,
            target_audience=audience
        )

        # Генерация вопросов
        questions = await generate_test_questions(
            construct=construct,
            question_count=question_count,
            difficulty_level=DifficultyLevel.MEDIUM,
            language_style=viral_transformation.language_style
        )

        # Создание шкал интерпретации
        scales = await create_interpretation_scales(
            construct=construct,
            result_ranges=5,
            transformation_programs=[]
        )

        # Анализ эффективности
        effectiveness = await analyze_test_effectiveness(questions, {})

        result = {
            "viral_name": viral_transformation.viral_name,
            "academic_base": base_methodology,
            "question_count": len(questions),
            "questions": [
                {
                    "id": q.id,
                    "text": q.text,
                    "type": q.question_type.value,
                    "reverse_scored": q.reverse_scored
                }
                for q in questions
            ],
            "interpretation_scales": [
                {
                    "level": s.level,
                    "title": s.title,
                    "description": s.description,
                    "recommendations": s.recommendations
                }
                for s in scales
            ],
            "psychometric_validation": {
                "valid": validation.is_valid,
                "validity_score": validation.validity_score,
                "reliability_score": validation.reliability_score
            },
            "effectiveness": {
                "viral_score": effectiveness.viral_score,
                "engagement_score": effectiveness.engagement_score,
                "completion_rate": effectiveness.completion_rate_prediction
            }
        }

        import json
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка создания теста: {str(e)}"


# === ФУНКЦИЯ ЗАПУСКА АГЕНТА ===

async def run_pattern_test_architect(
    user_message: str,
    deps: Optional[PatternTestArchitectDependencies] = None
) -> str:
    """
    Основная функция запуска Pattern Test Architect Agent.

    Args:
        user_message: Сообщение пользователя с запросом
        deps: Зависимости агента (опционально)

    Returns:
        Ответ агента
    """
    if deps is None:
        from .settings import load_settings
        settings = load_settings()
        deps = PatternTestArchitectDependencies(
            api_key=settings.llm_api_key,
            patternshift_project_path=settings.patternshift_project_path if hasattr(settings, 'patternshift_project_path') else ""
        )

    try:
        result = await agent.run(user_message, deps=deps)
        return result.data if hasattr(result, 'data') else str(result)
    except Exception as e:
        logger.error(f"Ошибка выполнения агента: {e}")
        return f"Ошибка: {str(e)}"


# === РЕГИСТРАЦИЯ АГЕНТА В ГЛОБАЛЬНОМ РЕЕСТРЕ ===

if HAS_DECORATORS:
    try:
        register_agent(
            "pattern_test_architect",
            agent,
            agent_type="pattern_content_specialist"
        )
        logger.info("Pattern Test Architect Agent зарегистрирован в глобальном реестре")
    except Exception as e:
        logger.warning(f"Не удалось зарегистрировать агента: {e}")