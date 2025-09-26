"""
NLP Psychology Test Adapter Agent

Универсальный агент для адаптации существующих валидированных психологических тестов
под методологию PatternShift с сохранением научной обоснованности.

Framework: Pydantic AI + Claude 4 Sonnet
Architecture: Universal, modular, RAG-integrated
"""

from pydantic_ai import Agent, RunContext
from typing import Dict, List, Any, Optional, Union
import json
import asyncio

from .dependencies import (
from ..common import check_pm_switch
    PatternShiftTestAdapterDeps,
    TestConfiguration,
    AdaptationResult,
    TestValidationResult
)
from .tools import (
    adapt_test_questions,
    validate_test_structure,
    generate_life_situations,
    create_multilingual_variants,
    calculate_adaptive_thresholds,
    integrate_redirection_logic,
    validate_psychological_correctness
)
from .prompts import (
    MAIN_SYSTEM_PROMPT,
    ADAPTATION_PROMPT,
    VALIDATION_PROMPT,
    MULTILINGUAL_PROMPT
)


nlp_psychology_test_adapter_agent = Agent(
    model='claude-sonnet-4',
    deps_type=PatternShiftTestAdapterDeps,
    system_prompt=MAIN_SYSTEM_PROMPT,
    result_type=AdaptationResult
)


@nlp_psychology_test_adapter_agent.system_prompt
async def get_system_prompt(ctx: RunContext[PatternShiftTestAdapterDeps]) -> str:
    """Динамический системный промпт с учетом конфигурации."""
    deps = ctx.deps

    # Получение релевантных знаний из RAG
    knowledge = await deps.search_agent_knowledge(
        query="test adaptation PatternShift methodology psychological assessment",
        match_count=3
    )

    knowledge_context = "\n".join([
        f"- {item['content'][:200]}..."
        for item in knowledge.get('results', [])
    ])

    return f"""{MAIN_SYSTEM_PROMPT}

## Контекст текущей адаптации:
**Исходный тест:** {deps.config.source_test_name}
**Целевая методология:** PatternShift
**Язык:** {deps.config.target_language}
**Культурный контекст:** {deps.config.cultural_context}

## Релевантные знания:
{knowledge_context}

## Приоритеты адаптации:
{deps.get_adaptation_priorities()}
"""


@nlp_psychology_test_adapter_agent.tool
async def adapt_existing_test(
    ctx: RunContext[PatternShiftTestAdapterDeps],
    source_test_data: Dict[str, Any],
    adaptation_type: str = "full"  # full, questions_only, scoring_only
) -> AdaptationResult:
    """
    Адаптирует существующий тест под методологию PatternShift.

    Args:
        source_test_data: Данные исходного теста
        adaptation_type: Тип адаптации (полная/только вопросы/только система оценки)
    """
    deps = ctx.deps

    try:
        # Этап 1: Анализ исходного теста
        test_analysis = await deps.analyze_source_test(source_test_data)

        # Этап 2: Адаптация вопросов под жизненные ситуации
        if adaptation_type in ["full", "questions_only"]:
            adapted_questions = await adapt_test_questions(
                ctx,
                source_questions=source_test_data.get('questions', []),
                target_methodology=deps.config.methodology_config
            )
        else:
            adapted_questions = source_test_data.get('questions', [])

        # Этап 3: Адаптация системы оценки
        if adaptation_type in ["full", "scoring_only"]:
            adapted_scoring = await calculate_adaptive_thresholds(
                ctx,
                source_scoring=source_test_data.get('scoring', {}),
                target_levels=deps.config.result_levels
            )
        else:
            adapted_scoring = source_test_data.get('scoring', {})

        # Этап 4: Создание мультиязычных вариантов
        multilingual_variants = await create_multilingual_variants(
            ctx,
            base_questions=adapted_questions,
            target_languages=deps.config.supported_languages
        )

        # Этап 5: Интеграция логики перенаправления
        redirection_logic = await integrate_redirection_logic(
            ctx,
            test_type=source_test_data.get('type'),
            scoring_system=adapted_scoring
        )

        # Этап 6: Валидация адаптированного теста
        validation_result = await validate_test_structure(
            ctx,
            adapted_test={
                'questions': adapted_questions,
                'scoring': adapted_scoring,
                'multilingual_variants': multilingual_variants,
                'redirection_logic': redirection_logic
            }
        )

        return AdaptationResult(
            adapted_test={
                'id': f"patternshift_{source_test_data.get('id', 'unknown')}",
                'title': deps.generate_patternshift_title(source_test_data.get('title', '')),
                'questions': adapted_questions,
                'scoring': adapted_scoring,
                'multilingual_variants': multilingual_variants,
                'redirection_logic': redirection_logic,
                'methodology_compliance': validation_result.methodology_compliance,
                'psychological_validation': validation_result.psychological_validation
            },
            validation_results=validation_result,
            adaptation_metadata={
                'source_test': source_test_data.get('id'),
                'adaptation_type': adaptation_type,
                'adaptation_timestamp': deps.get_timestamp(),
                'quality_score': validation_result.overall_quality_score
            }
        )

    except Exception as e:
        return AdaptationResult(
            adapted_test=None,
            validation_results=TestValidationResult(
                is_valid=False,
                validation_errors=[f"Adaptation failed: {str(e)}"]
            ),
            adaptation_metadata={
                'error': str(e),
                'adaptation_type': adaptation_type
            }
        )


@nlp_psychology_test_adapter_agent.tool
async def validate_adapted_test(
    ctx: RunContext[PatternShiftTestAdapterDeps],
    adapted_test: Dict[str, Any]
) -> TestValidationResult:
    """
    Проводит комплексную валидацию адаптированного теста.

    Args:
        adapted_test: Адаптированный тест для валидации
    """
    deps = ctx.deps

    validation_errors = []
    validation_warnings = []

    # Валидация соответствия методологии PatternShift
    methodology_check = await deps.validate_methodology_compliance(adapted_test)
    if not methodology_check['is_compliant']:
        validation_errors.extend(methodology_check['errors'])

    # Валидация психологической корректности
    psychological_validation = await validate_psychological_correctness(
        ctx, adapted_test
    )
    if not psychological_validation['is_valid']:
        validation_errors.extend(psychological_validation['errors'])

    # Валидация структуры теста
    structure_validation = await validate_test_structure(ctx, adapted_test)
    validation_errors.extend(structure_validation.validation_errors)
    validation_warnings.extend(structure_validation.validation_warnings)

    # Расчет общего балла качества
    quality_score = deps.calculate_quality_score(
        methodology_compliance=methodology_check['compliance_score'],
        psychological_validity=psychological_validation['validity_score'],
        structural_integrity=structure_validation.structural_score
    )

    return TestValidationResult(
        is_valid=len(validation_errors) == 0,
        validation_errors=validation_errors,
        validation_warnings=validation_warnings,
        methodology_compliance=methodology_check,
        psychological_validation=psychological_validation,
        structural_score=structure_validation.structural_score,
        overall_quality_score=quality_score
    )


@nlp_psychology_test_adapter_agent.tool
async def generate_test_expansion(
    ctx: RunContext[PatternShiftTestAdapterDeps],
    short_test: Dict[str, Any],
    target_question_count: int = 15
) -> Dict[str, Any]:
    """
    Расширяет короткий тест до минимального количества вопросов PatternShift.

    Args:
        short_test: Короткий исходный тест
        target_question_count: Целевое количество вопросов (минимум 15)
    """
    deps = ctx.deps

    current_questions = short_test.get('questions', [])
    current_count = len(current_questions)

    if current_count >= target_question_count:
        return short_test  # Тест уже достаточно длинный

    # Анализ существующих вопросов для понимания конструктов
    constructs_analysis = await deps.analyze_test_constructs(current_questions)

    # Генерация дополнительных вопросов
    additional_questions = await generate_life_situations(
        ctx,
        constructs=constructs_analysis['constructs'],
        existing_questions=current_questions,
        questions_needed=target_question_count - current_count,
        difficulty_distribution=constructs_analysis['difficulty_distribution']
    )

    # Объединение и балансировка вопросов
    expanded_questions = current_questions + additional_questions
    balanced_questions = await deps.balance_question_difficulty(expanded_questions)

    return {
        **short_test,
        'questions': balanced_questions,
        'expansion_metadata': {
            'original_count': current_count,
            'final_count': len(balanced_questions),
            'added_questions': len(additional_questions),
            'constructs_covered': constructs_analysis['constructs']
        }
    }


async def run_test_adaptation_workflow(
    source_test_data: Dict[str, Any],
    config: TestConfiguration
) -> AdaptationResult:
    """
    Запускает полный цикл адаптации теста под методологию PatternShift.

    Args:
        source_test_data: Данные исходного теста
        config: Конфигурация адаптации
    """
    async with PatternShiftTestAdapterDeps.create(config) as deps:
        agent_result = await nlp_psychology_test_adapter_agent.run(
            user_prompt=f"""
            Адаптируй психологический тест под методологию PatternShift:

            Исходный тест: {source_test_data.get('title', 'Unknown')}
            Тип теста: {source_test_data.get('type', 'Unknown')}
            Количество вопросов: {len(source_test_data.get('questions', []))}

            Требования:
            - Минимум 15 вопросов в жизненных ситуациях
            - Адаптивная система оценки
            - Мультиязычная поддержка
            - Интеграция с программами трансформации
            - Сохранение научной валидности
            """,
            deps=deps
        )

        return agent_result.data


if __name__ == "__main__":
    # Пример использования агента
    sample_config = TestConfiguration(
        source_test_name="PHQ-9",
        target_language="uk",
        cultural_context="ukrainian",
        methodology_config={
            "min_questions": 15,
            "life_situations": True,
            "adaptive_scoring": True
        }
    )

    sample_test = {
        "id": "phq9",
        "title": "Patient Health Questionnaire-9",
        "type": "depression",
        "questions": [
            {
                "id": 1,
                "text": "Little interest or pleasure in doing things",
                "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                "values": [0, 1, 2, 3]
            }
            # ... остальные вопросы PHQ-9
        ]
    }

    result = asyncio.run(
        run_test_adaptation_workflow(sample_test, sample_config)
    )
    print(f"Adaptation result: {result}")