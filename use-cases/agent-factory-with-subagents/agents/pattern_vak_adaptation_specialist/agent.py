"""
Pattern VAK Adaptation Specialist Agent.

Специализированный агент для адаптации психологических и терапевтических
материалов под сенсорные репрезентативные системы (Visual, Auditory, Kinesthetic)
в рамках проекта PatternShift.

Основные возможности:
- Анализ контента на доминирующую VAK модальность
- Адаптация под целевую модальность с сохранением терапевтической целостности
- Создание мультимодальных вариантов
- Валидация безопасности и эффективности
- Интеграция с архитектурой PatternShift
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model
from pydantic import BaseModel, Field

from .dependencies import (
    PatternVAKAdaptationDependencies,
    VAKModalityType,
    AdaptationDepth,
    PatternShiftModuleType,
    ContentAdaptationRequest,
    VAKProfile,
    ModuleVariant,
    VAKMetrics
)
from .settings import get_settings, PatternVAKSettings
from .prompts import (
    get_base_system_prompt,
    get_analysis_prompt,
    get_adaptation_prompt,
    get_multimodal_prompt,
    get_validation_prompt,
    get_context_aware_prompt
)
from .tools import (
    search_agent_knowledge,
    analyze_content_vak_modalities,
    adapt_content_to_vak_modality,
    create_multimodal_variant,
    validate_adaptation_safety,
    generate_vak_metrics,
    VAKAnalysisResult,
    AdaptedContent,
    MultimodalVariant
)


# Настройка логирования
logger = logging.getLogger(__name__)


class VAKAdaptationRequest(BaseModel):
    """Запрос на VAK адаптацию с дополнительными параметрами."""

    content: str = Field(description="Контент для адаптации")
    target_modality: Optional[VAKModalityType] = Field(
        default=None,
        description="Целевая модальность (если не указана, будет определена автоматически)"
    )
    adaptation_depth: AdaptationDepth = Field(
        default=AdaptationDepth.MODERATE,
        description="Уровень глубины адаптации"
    )
    module_type: Optional[PatternShiftModuleType] = Field(
        default=None,
        description="Тип модуля PatternShift"
    )
    user_profile: Optional[VAKProfile] = Field(
        default=None,
        description="Профиль пользователя для персонализации"
    )
    preserve_therapeutic_goals: bool = Field(
        default=True,
        description="Сохранять терапевтические цели"
    )
    create_multimodal: bool = Field(
        default=False,
        description="Создать мультимодальный вариант"
    )
    safety_requirements: List[str] = Field(
        default_factory=list,
        description="Дополнительные требования безопасности"
    )


class VAKAdaptationResponse(BaseModel):
    """Ответ системы VAK адаптации."""

    success: bool = Field(description="Успешность операции")
    original_analysis: Optional[VAKAnalysisResult] = Field(
        default=None,
        description="Анализ исходного контента"
    )
    adapted_content: Optional[AdaptedContent] = Field(
        default=None,
        description="Адаптированный контент"
    )
    multimodal_variant: Optional[MultimodalVariant] = Field(
        default=None,
        description="Мультимодальный вариант (если запрошен)"
    )
    safety_validation: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Результаты валидации безопасности"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Рекомендации по использованию"
    )
    metrics: Optional[VAKMetrics] = Field(
        default=None,
        description="Метрики качества адаптации"
    )
    processing_time: float = Field(
        default=0.0,
        description="Время обработки в секундах"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Сообщение об ошибке (если success=False)"
    )


def create_llm_model() -> Model:
    """Создать модель LLM для VAK агента."""
    from pydantic_ai.models.openai import OpenAIModel
    from pydantic_ai.providers.openai import OpenAIProvider

    settings = get_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(
        model_name=settings.llm_model,
        provider=provider,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens
    )


# Создаем основного агента
vak_adaptation_agent = Agent(
    model=create_llm_model(),
    deps_type=PatternVAKAdaptationDependencies,
    system_prompt=get_base_system_prompt()
)


# Регистрируем инструменты агента
vak_adaptation_agent.tool(search_agent_knowledge)
vak_adaptation_agent.tool(analyze_content_vak_modalities)
vak_adaptation_agent.tool(adapt_content_to_vak_modality)
vak_adaptation_agent.tool(create_multimodal_variant)
vak_adaptation_agent.tool(validate_adaptation_safety)
vak_adaptation_agent.tool(generate_vak_metrics)


@vak_adaptation_agent.tool
async def process_vak_adaptation_request(
    ctx: RunContext[PatternVAKAdaptationDependencies],
    request: VAKAdaptationRequest
) -> VAKAdaptationResponse:
    """
    Обработать полный запрос на VAK адаптацию.

    Этот инструмент координирует весь процесс адаптации:
    1. Анализ исходного контента
    2. Определение целевой модальности (если не указана)
    3. Адаптация контента
    4. Создание мультимодального варианта (если запрошено)
    5. Валидация безопасности
    6. Генерация метрик

    Args:
        ctx: Контекст выполнения
        request: Запрос на адаптацию

    Returns:
        Полный ответ с результатами адаптации
    """
    start_time = datetime.now()
    settings = get_settings()

    try:
        response = VAKAdaptationResponse(success=True)

        # 1. Анализ исходного контента
        logger.info("Начинаем анализ исходного контента")
        original_analysis = await analyze_content_vak_modalities(
            ctx, request.content, include_detailed_analysis=True
        )
        response.original_analysis = original_analysis

        # 2. Определение целевой модальности
        target_modality = request.target_modality
        if not target_modality:
            # Автоматическое определение на основе профиля пользователя или анализа
            if request.user_profile:
                target_modality = request.user_profile.primary_modality
            else:
                # Выбираем модальность, которая меньше всего представлена в исходном контенте
                # для максимального улучшения
                modality_scores = original_analysis.modality_scores
                target_modality = VAKModalityType(
                    min(modality_scores.items(), key=lambda x: x[1])[0]
                )

        logger.info(f"Целевая модальность: {target_modality}")

        # 3. Адаптация контента
        adaptation_request = ContentAdaptationRequest(
            original_content=request.content,
            target_modality=target_modality,
            adaptation_depth=request.adaptation_depth,
            module_type=request.module_type or PatternShiftModuleType.TECHNIQUE,
            preserve_therapeutic_goals=request.preserve_therapeutic_goals,
            safety_considerations=request.safety_requirements
        )

        adapted_content = await adapt_content_to_vak_modality(ctx, adaptation_request)
        response.adapted_content = adapted_content

        # 4. Создание мультимодального варианта (если запрошено)
        if request.create_multimodal and settings.enable_multimodal_variants:
            logger.info("Создаем мультимодальный вариант")
            multimodal_variant = await create_multimodal_variant(
                ctx,
                request.content,
                request.module_type or PatternShiftModuleType.TECHNIQUE,
                include_all_modalities=True
            )
            response.multimodal_variant = multimodal_variant

        # 5. Валидация безопасности
        if settings.require_safety_validation:
            logger.info("Выполняем валидацию безопасности")
            safety_validation = await validate_adaptation_safety(
                ctx,
                request.content,
                adapted_content.adapted_content,
                target_audience="adults"
            )
            response.safety_validation = safety_validation

            # Проверяем, прошла ли валидация
            if not safety_validation.get("is_safe", True):
                response.success = False
                response.error_message = (
                    f"Адаптация не прошла валидацию безопасности: "
                    f"{'; '.join(safety_validation.get('warnings', []))}"
                )
                return response

        # 6. Генерация метрик
        if settings.collect_usage_metrics:
            logger.info("Генерируем метрики качества")
            metrics = await generate_vak_metrics(
                ctx,
                [adapted_content],
                request.user_profile
            )
            response.metrics = metrics

        # 7. Генерация рекомендаций
        response.recommendations = _generate_usage_recommendations(
            original_analysis,
            adapted_content,
            request.user_profile,
            target_modality
        )

        # Вычисляем время обработки
        end_time = datetime.now()
        response.processing_time = (end_time - start_time).total_seconds()

        logger.info(f"VAK адаптация завершена успешно за {response.processing_time:.2f} сек")
        return response

    except Exception as e:
        logger.error(f"Ошибка при обработке VAK адаптации: {e}")
        end_time = datetime.now()
        return VAKAdaptationResponse(
            success=False,
            error_message=str(e),
            processing_time=(end_time - start_time).total_seconds()
        )


@vak_adaptation_agent.tool
async def batch_vak_adaptation(
    ctx: RunContext[PatternVAKAdaptationDependencies],
    content_items: List[str],
    target_modality: VAKModalityType,
    adaptation_depth: AdaptationDepth = AdaptationDepth.MODERATE
) -> List[VAKAdaptationResponse]:
    """
    Массовая адаптация нескольких элементов контента.

    Args:
        ctx: Контекст выполнения
        content_items: Список контента для адаптации
        target_modality: Целевая модальность для всех элементов
        adaptation_depth: Уровень адаптации

    Returns:
        Список результатов адаптации
    """
    settings = get_settings()
    batch_size = settings.batch_adaptation_size
    concurrent_limit = settings.concurrent_adaptations

    logger.info(f"Начинаем массовую адаптацию {len(content_items)} элементов")

    results = []

    # Обрабатываем пакетами
    for i in range(0, len(content_items), batch_size):
        batch = content_items[i:i + batch_size]
        logger.info(f"Обрабатываем пакет {i//batch_size + 1}")

        # Создаем задачи для текущего пакета
        tasks = []
        for content in batch:
            request = VAKAdaptationRequest(
                content=content,
                target_modality=target_modality,
                adaptation_depth=adaptation_depth
            )
            task = process_vak_adaptation_request(ctx, request)
            tasks.append(task)

        # Выполняем задачи с ограничением параллелизма
        semaphore = asyncio.Semaphore(concurrent_limit)

        async def limited_task(task):
            async with semaphore:
                return await task

        batch_results = await asyncio.gather(
            *[limited_task(task) for task in tasks],
            return_exceptions=True
        )

        # Обрабатываем результаты пакета
        for result in batch_results:
            if isinstance(result, Exception):
                error_response = VAKAdaptationResponse(
                    success=False,
                    error_message=str(result)
                )
                results.append(error_response)
            else:
                results.append(result)

    logger.info(f"Массовая адаптация завершена. Успешно: {sum(1 for r in results if r.success)}")
    return results


@vak_adaptation_agent.tool
async def analyze_user_vak_profile(
    ctx: RunContext[PatternVAKAdaptationDependencies],
    user_responses: List[str],
    interaction_history: Optional[List[Dict[str, Any]]] = None
) -> VAKProfile:
    """
    Анализ VAK профиля пользователя на основе его ответов и истории взаимодействий.

    Args:
        ctx: Контекст выполнения
        user_responses: Ответы пользователя для анализа
        interaction_history: История взаимодействий (опционально)

    Returns:
        VAK профиль пользователя
    """
    logger.info("Анализируем VAK профиль пользователя")

    # Объединяем все ответы пользователя
    combined_text = " ".join(user_responses)

    # Анализируем доминирующую модальность
    analysis = await analyze_content_vak_modalities(ctx, combined_text)

    # Определяем первичную и вторичную модальности
    sorted_modalities = sorted(
        analysis.modality_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    primary_modality = VAKModalityType(sorted_modalities[0][0])
    secondary_modality = VAKModalityType(sorted_modalities[1][0]) if len(sorted_modalities) > 1 else None

    # Создаем профиль
    profile = VAKProfile(
        primary_modality=primary_modality,
        secondary_modality=secondary_modality,
        visual_preference=analysis.modality_scores.get("visual", 0.33),
        auditory_preference=analysis.modality_scores.get("auditory", 0.33),
        kinesthetic_preference=analysis.modality_scores.get("kinesthetic", 0.33),
        adaptation_effectiveness={}
    )

    # Если есть история взаимодействий, анализируем эффективность
    if interaction_history:
        effectiveness = _analyze_adaptation_effectiveness(interaction_history)
        profile.adaptation_effectiveness = effectiveness

    logger.info(f"VAK профиль: {primary_modality} (основная), {secondary_modality} (вторичная)")
    return profile


def _generate_usage_recommendations(
    original_analysis: VAKAnalysisResult,
    adapted_content: AdaptedContent,
    user_profile: Optional[VAKProfile],
    target_modality: VAKModalityType
) -> List[str]:
    """Генерация рекомендаций по использованию адаптированного контента."""
    recommendations = []

    # Базовые рекомендации по модальности
    modality_recommendations = {
        VAKModalityType.VISUAL: [
            "Используйте визуальные материалы и схемы для усиления эффекта",
            "Читайте в хорошо освещенном месте",
            "Делайте заметки и рисунки во время изучения"
        ],
        VAKModalityType.AUDITORY: [
            "Читайте текст вслух или используйте аудио-версию",
            "Обсуждайте материал с другими людьми",
            "Используйте ритмичную подачу информации"
        ],
        VAKModalityType.KINESTHETIC: [
            "Делайте перерывы для физических упражнений",
            "Практикуйте техники в движении",
            "Сосредоточьтесь на телесных ощущениях"
        ]
    }

    recommendations.extend(modality_recommendations.get(target_modality, []))

    # Рекомендации на основе качества адаптации
    if adapted_content.quality_score >= 0.9:
        recommendations.append("Высокое качество адаптации - можно использовать как основную версию")
    elif adapted_content.quality_score >= 0.7:
        recommendations.append("Хорошее качество адаптации - рекомендуется для основного использования")
    else:
        recommendations.append("Умеренное качество адаптации - используйте в сочетании с оригиналом")

    # Рекомендации на основе профиля пользователя
    if user_profile:
        if user_profile.primary_modality == target_modality:
            recommendations.append("Адаптация соответствует вашей доминирующей модальности")
        else:
            recommendations.append("Адаптация поможет развить альтернативные каналы восприятия")

    # Рекомендации по безопасности
    if adapted_content.therapeutic_integrity_preserved:
        recommendations.append("Терапевтическая целостность сохранена - безопасно для использования")
    else:
        recommendations.append("ВНИМАНИЕ: Используйте под наблюдением специалиста")

    return recommendations


def _analyze_adaptation_effectiveness(interaction_history: List[Dict[str, Any]]) -> Dict[str, float]:
    """Анализ эффективности адаптации на основе истории взаимодействий."""
    effectiveness = {
        "visual": 0.5,
        "auditory": 0.5,
        "kinesthetic": 0.5
    }

    for interaction in interaction_history:
        modality = interaction.get("modality")
        success_rate = interaction.get("success_rate", 0.5)

        if modality in effectiveness:
            # Простое усреднение (в реальной системе может быть более сложная логика)
            effectiveness[modality] = (effectiveness[modality] + success_rate) / 2

    return effectiveness


async def run_pattern_vak_adaptation_specialist(
    user_message: str,
    deps: Optional[PatternVAKAdaptationDependencies] = None,
    **kwargs
) -> VAKAdaptationResponse:
    """
    Основная функция запуска Pattern VAK Adaptation Specialist Agent.

    Args:
        user_message: Сообщение пользователя или контент для адаптации
        deps: Зависимости агента (если не указаны, создаются автоматически)
        **kwargs: Дополнительные параметры

    Returns:
        Результат VAK адаптации
    """
    # Создаем зависимости если не переданы
    if deps is None:
        settings = get_settings()
        deps = PatternVAKAdaptationDependencies(
            api_key=settings.llm_api_key,
            patternshift_project_path=settings.patternshift_project_path
        )

    try:
        # Пытаемся распарсить как JSON запрос
        try:
            request_data = json.loads(user_message)
            request = VAKAdaptationRequest(**request_data)
        except (json.JSONDecodeError, ValueError):
            # Если не JSON, создаем простой запрос с контентом
            request = VAKAdaptationRequest(
                content=user_message,
                **kwargs
            )

        # Обрабатываем запрос
        result = await vak_adaptation_agent.run(
            f"Обработай VAK адаптацию: {request.model_dump_json()}",
            deps=deps
        )

        # Если результат - строка, парсим JSON
        if isinstance(result.data, str):
            try:
                response_data = json.loads(result.data)
                return VAKAdaptationResponse(**response_data)
            except (json.JSONDecodeError, ValueError):
                # Возвращаем простой ответ
                return VAKAdaptationResponse(
                    success=True,
                    adapted_content=AdaptedContent(
                        original_content=request.content,
                        adapted_content=result.data,
                        target_modality=request.target_modality or VAKModalityType.VISUAL,
                        adaptation_depth=request.adaptation_depth,
                        changes_made=["Адаптация выполнена LLM"],
                        quality_score=0.8,
                        therapeutic_integrity_preserved=True
                    )
                )
        else:
            return result.data

    except Exception as e:
        logger.error(f"Ошибка в run_pattern_vak_adaptation_specialist: {e}")
        return VAKAdaptationResponse(
            success=False,
            error_message=str(e)
        )


# Экспорт основных компонентов
__all__ = [
    "vak_adaptation_agent",
    "run_pattern_vak_adaptation_specialist",
    "VAKAdaptationRequest",
    "VAKAdaptationResponse",
    "PatternVAKAdaptationDependencies"
]