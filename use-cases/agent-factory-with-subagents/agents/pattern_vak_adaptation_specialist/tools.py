"""
Инструменты для Pattern VAK Adaptation Specialist Agent.

Содержит инструменты для адаптации контента под сенсорные
репрезентативные системы (Visual, Auditory, Kinesthetic)
в рамках проекта PatternShift.
"""

import re
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import (
    PatternVAKAdaptationDependencies,
    VAKModalityType,
    AdaptationDepth,
    PatternShiftModuleType,
    ContentAdaptationRequest,
    VAKProfile,
    ModuleVariant,
    VAKMetrics,
    VISUAL_PREDICATES,
    AUDITORY_PREDICATES,
    KINESTHETIC_PREDICATES,
    VAK_METAPHORS
)


class VAKAnalysisResult(BaseModel):
    """Результат анализа контента на VAK модальности."""

    dominant_modality: VAKModalityType = Field(description="Доминирующая модальность")
    modality_scores: Dict[str, float] = Field(description="Оценки по модальностям")
    detected_predicates: Dict[str, List[str]] = Field(description="Обнаруженные предикаты")
    structure_analysis: Dict[str, Any] = Field(description="Анализ структуры")
    adaptation_recommendations: List[str] = Field(description="Рекомендации по адаптации")


class AdaptedContent(BaseModel):
    """Адаптированный контент для конкретной VAK модальности."""

    original_content: str = Field(description="Исходный контент")
    adapted_content: str = Field(description="Адаптированный контент")
    target_modality: VAKModalityType = Field(description="Целевая модальность")
    adaptation_depth: AdaptationDepth = Field(description="Уровень адаптации")
    changes_made: List[str] = Field(description="Внесенные изменения")
    quality_score: float = Field(description="Оценка качества адаптации")
    therapeutic_integrity_preserved: bool = Field(description="Сохранена терапевтическая целостность")


class MultimodalVariant(BaseModel):
    """Мультимодальный вариант контента."""

    base_content: str = Field(description="Базовый контент")
    visual_elements: List[str] = Field(description="Визуальные элементы")
    auditory_elements: List[str] = Field(description="Аудиальные элементы")
    kinesthetic_elements: List[str] = Field(description="Кинестетические элементы")
    integration_instructions: str = Field(description="Инструкции по интеграции")
    recommended_sequence: List[str] = Field(description="Рекомендуемая последовательность")


async def search_agent_knowledge(
    ctx: RunContext[PatternVAKAdaptationDependencies],
    query: str,
    knowledge_type: str = "vak_adaptation"
) -> str:
    """
    Поиск в базе знаний VAK адаптации через Archon RAG.

    Args:
        ctx: Контекст выполнения с зависимостями
        query: Поисковый запрос
        knowledge_type: Тип знаний для поиска

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Временная заглушка для поиска в базе знаний
        # В реальной реализации здесь будет интеграция с Archon RAG

        # Поиск в локальных знаниях агента
        knowledge_content = f"""
        База знаний VAK адаптации по запросу "{query}":

        ОСНОВНЫЕ ПРИНЦИПЫ VAK АДАПТАЦИИ:

        Visual (Визуальная модальность):
        - Предикаты: видеть, смотреть, представлять, фокусироваться
        - Структура: короткие абзацы, списки, схемы
        - Темп: быстрый, с акцентом на результаты
        - Метафоры: яркие образы, пространственные ориентиры

        Auditory (Аудиальная модальность):
        - Предикаты: слышать, говорить, звучать, резонировать
        - Структура: ритмичная, с повторами и логическими связями
        - Темп: средний, с паузами для обработки
        - Метафоры: звуковые аналогии, музыкальные образы

        Kinesthetic (Кинестетическая модальность):
        - Предикаты: чувствовать, касаться, двигаться, ощущать
        - Структура: детальные описания процессов
        - Темп: медленный, с паузами для внутренней обработки
        - Метафоры: текстуры, движения, физические ощущения

        ТЕХНИКИ АДАПТАЦИИ:
        1. Замена предикатов на соответствующие модальности
        2. Адаптация структуры и темпа изложения
        3. Интеграция специфичных метафор
        4. Создание мультисенсорных вариантов
        5. Валидация терапевтической целостности
        """

        return knowledge_content

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"


async def analyze_content_vak_modalities(
    ctx: RunContext[PatternVAKAdaptationDependencies],
    content: str,
    include_detailed_analysis: bool = True
) -> VAKAnalysisResult:
    """
    Анализ контента на присутствие VAK модальностей.

    Args:
        ctx: Контекст выполнения
        content: Контент для анализа
        include_detailed_analysis: Включить детальный анализ

    Returns:
        Результат анализа VAK модальностей
    """
    content_lower = content.lower()

    # Подсчет предикатов по модальностям
    visual_count = sum(1 for predicate in VISUAL_PREDICATES if predicate in content_lower)
    auditory_count = sum(1 for predicate in AUDITORY_PREDICATES if predicate in content_lower)
    kinesthetic_count = sum(1 for predicate in KINESTHETIC_PREDICATES if predicate in content_lower)

    total_predicates = visual_count + auditory_count + kinesthetic_count

    # Вычисление оценок модальностей
    if total_predicates > 0:
        visual_score = visual_count / total_predicates
        auditory_score = auditory_count / total_predicates
        kinesthetic_score = kinesthetic_count / total_predicates
    else:
        # Равномерное распределение при отсутствии предикатов
        visual_score = auditory_score = kinesthetic_score = 0.33

    # Определение доминирующей модальности
    scores = {
        "visual": visual_score,
        "auditory": auditory_score,
        "kinesthetic": kinesthetic_score
    }
    dominant_modality = VAKModalityType(max(scores.items(), key=lambda x: x[1])[0])

    # Детальный анализ найденных предикатов
    detected_predicates = {}
    if include_detailed_analysis:
        detected_predicates = {
            "visual": [p for p in VISUAL_PREDICATES if p in content_lower],
            "auditory": [p for p in AUDITORY_PREDICATES if p in content_lower],
            "kinesthetic": [p for p in KINESTHETIC_PREDICATES if p in content_lower]
        }

    # Анализ структуры контента
    structure_analysis = {
        "paragraph_count": len(content.split('\n\n')),
        "sentence_count": len(re.findall(r'[.!?]+', content)),
        "word_count": len(content.split()),
        "avg_sentence_length": len(content.split()) / max(1, len(re.findall(r'[.!?]+', content))),
        "has_lists": bool(re.findall(r'^\s*[-*•]\s', content, re.MULTILINE)),
        "has_numbered_lists": bool(re.findall(r'^\s*\d+\.', content, re.MULTILINE))
    }

    # Рекомендации по адаптации
    recommendations = []
    if visual_score < 0.2:
        recommendations.append("Добавить визуальные предикаты и метафоры")
    if auditory_score < 0.2:
        recommendations.append("Включить аудиальные элементы и ритмичность")
    if kinesthetic_score < 0.2:
        recommendations.append("Усилить кинестетические ощущения и движения")

    if structure_analysis["avg_sentence_length"] > 20:
        recommendations.append("Сократить длину предложений для визуалов")
    elif structure_analysis["avg_sentence_length"] < 10:
        recommendations.append("Добавить детализацию для кинестетиков")

    return VAKAnalysisResult(
        dominant_modality=dominant_modality,
        modality_scores=scores,
        detected_predicates=detected_predicates,
        structure_analysis=structure_analysis,
        adaptation_recommendations=recommendations
    )


async def adapt_content_to_vak_modality(
    ctx: RunContext[PatternVAKAdaptationDependencies],
    request: ContentAdaptationRequest
) -> AdaptedContent:
    """
    Адаптация контента под конкретную VAK модальность.

    Args:
        ctx: Контекст выполнения
        request: Запрос на адаптацию

    Returns:
        Адаптированный контент
    """
    original_content = request.original_content
    target_modality = request.target_modality
    adaptation_depth = request.adaptation_depth

    # Сначала анализируем исходный контент
    analysis = await analyze_content_vak_modalities(ctx, original_content)

    adapted_content = original_content
    changes_made = []

    # Адаптация предикатов
    if adaptation_depth in [AdaptationDepth.SURFACE, AdaptationDepth.MODERATE, AdaptationDepth.DEEP]:
        adapted_content, predicate_changes = await _adapt_predicates(
            adapted_content, target_modality, adaptation_depth
        )
        changes_made.extend(predicate_changes)

    # Адаптация структуры (для умеренной и глубокой адаптации)
    if adaptation_depth in [AdaptationDepth.MODERATE, AdaptationDepth.DEEP]:
        adapted_content, structure_changes = await _adapt_structure(
            adapted_content, target_modality, analysis.structure_analysis
        )
        changes_made.extend(structure_changes)

    # Адаптация метафор (для глубокой адаптации)
    if adaptation_depth in [AdaptationDepth.DEEP, AdaptationDepth.COMPLETE]:
        adapted_content, metaphor_changes = await _adapt_metaphors(
            adapted_content, target_modality
        )
        changes_made.extend(metaphor_changes)

    # Полная реконструкция (только для complete)
    if adaptation_depth == AdaptationDepth.COMPLETE:
        adapted_content, complete_changes = await _complete_reconstruction(
            adapted_content, target_modality, request.module_type
        )
        changes_made.extend(complete_changes)

    # Проверка сохранения терапевтической целостности
    therapeutic_preserved = await _validate_therapeutic_integrity(
        original_content, adapted_content, request.preserve_therapeutic_goals
    )

    # Оценка качества адаптации
    quality_score = await _calculate_adaptation_quality(
        original_content, adapted_content, target_modality
    )

    return AdaptedContent(
        original_content=original_content,
        adapted_content=adapted_content,
        target_modality=target_modality,
        adaptation_depth=adaptation_depth,
        changes_made=changes_made,
        quality_score=quality_score,
        therapeutic_integrity_preserved=therapeutic_preserved
    )


async def create_multimodal_variant(
    ctx: RunContext[PatternVAKAdaptationDependencies],
    base_content: str,
    module_type: PatternShiftModuleType,
    include_all_modalities: bool = True
) -> MultimodalVariant:
    """
    Создание мультимодального варианта контента.

    Args:
        ctx: Контекст выполнения
        base_content: Базовый контент
        module_type: Тип модуля PatternShift
        include_all_modalities: Включить все модальности

    Returns:
        Мультимодальный вариант
    """
    # Создаем адаптации для каждой модальности
    visual_adaptation = await adapt_content_to_vak_modality(ctx, ContentAdaptationRequest(
        original_content=base_content,
        target_modality=VAKModalityType.VISUAL,
        adaptation_depth=AdaptationDepth.MODERATE,
        module_type=module_type
    ))

    auditory_adaptation = await adapt_content_to_vak_modality(ctx, ContentAdaptationRequest(
        original_content=base_content,
        target_modality=VAKModalityType.AUDITORY,
        adaptation_depth=AdaptationDepth.MODERATE,
        module_type=module_type
    ))

    kinesthetic_adaptation = await adapt_content_to_vak_modality(ctx, ContentAdaptationRequest(
        original_content=base_content,
        target_modality=VAKModalityType.KINESTHETIC,
        adaptation_depth=AdaptationDepth.MODERATE,
        module_type=module_type
    ))

    # Извлекаем специфичные элементы для каждой модальности
    visual_elements = _extract_visual_elements(visual_adaptation.adapted_content)
    auditory_elements = _extract_auditory_elements(auditory_adaptation.adapted_content)
    kinesthetic_elements = _extract_kinesthetic_elements(kinesthetic_adaptation.adapted_content)

    # Создаем инструкции по интеграции
    integration_instructions = await _create_integration_instructions(
        module_type, visual_elements, auditory_elements, kinesthetic_elements
    )

    # Рекомендуемая последовательность активации модальностей
    recommended_sequence = _create_activation_sequence(module_type)

    return MultimodalVariant(
        base_content=base_content,
        visual_elements=visual_elements,
        auditory_elements=auditory_elements,
        kinesthetic_elements=kinesthetic_elements,
        integration_instructions=integration_instructions,
        recommended_sequence=recommended_sequence
    )


async def validate_adaptation_safety(
    ctx: RunContext[PatternVAKAdaptationDependencies],
    original_content: str,
    adapted_content: str,
    target_audience: str = "adults"
) -> Dict[str, Any]:
    """
    Валидация безопасности адаптированного контента.

    Args:
        ctx: Контекст выполнения
        original_content: Исходный контент
        adapted_content: Адаптированный контент
        target_audience: Целевая аудитория

    Returns:
        Результаты валидации безопасности
    """
    validation_results = {
        "is_safe": True,
        "warnings": [],
        "therapeutic_integrity": True,
        "cultural_sensitivity": True,
        "trauma_considerations": []
    }

    # Проверка терапевтической целостности
    therapeutic_preserved = await _validate_therapeutic_integrity(
        original_content, adapted_content, True
    )
    validation_results["therapeutic_integrity"] = therapeutic_preserved

    if not therapeutic_preserved:
        validation_results["warnings"].append(
            "Возможное нарушение терапевтической целостности"
        )

    # Проверка на потенциально триггерные элементы
    trigger_patterns = [
        r'\b(травма|боль|страх|паника)\b',
        r'\b(насилие|агрессия|конфликт)\b',
        r'\b(смерть|утрата|потеря)\b'
    ]

    for pattern in trigger_patterns:
        if re.search(pattern, adapted_content, re.IGNORECASE):
            validation_results["trauma_considerations"].append(
                f"Обнаружен потенциально триггерный контент: {pattern}"
            )

    # Проверка соответствия PatternShift принципам безопасности
    safety_violations = []

    # Недопустимые техники или подходы
    forbidden_patterns = [
        r'\b(гипноз|транс)\b(?!.*эриксон)',  # Гипноз без контекста Эриксона
        r'\b(принуждение|заставить|должен)\b',  # Принудительные формулировки
        r'\b(диагноз|лечение|терапия)\b(?!.*метафор)'  # Медицинские термины без контекста
    ]

    for pattern in forbidden_patterns:
        if re.search(pattern, adapted_content, re.IGNORECASE):
            safety_violations.append(f"Нарушение безопасности: {pattern}")

    if safety_violations:
        validation_results["is_safe"] = False
        validation_results["warnings"].extend(safety_violations)

    # Проверка культурной чувствительности
    cultural_issues = await _check_cultural_sensitivity(adapted_content)
    if cultural_issues:
        validation_results["cultural_sensitivity"] = False
        validation_results["warnings"].extend(cultural_issues)

    return validation_results


async def generate_vak_metrics(
    ctx: RunContext[PatternVAKAdaptationDependencies],
    adaptation_results: List[AdaptedContent],
    user_profile: Optional[VAKProfile] = None
) -> VAKMetrics:
    """
    Генерация метрик эффективности VAK адаптации.

    Args:
        ctx: Контекст выполнения
        adaptation_results: Результаты адаптации
        user_profile: Профиль пользователя (если доступен)

    Returns:
        Метрики эффективности
    """
    if not adaptation_results:
        return VAKMetrics(
            completion_rate=0.0,
            engagement_score=0.0,
            comprehension_level=0.0,
            modality_preference_accuracy=0.0,
            therapeutic_effectiveness=0.0,
            adaptation_time=0.0,
            user_satisfaction=0.0
        )

    # Рассчитываем средние значения
    avg_quality = sum(result.quality_score for result in adaptation_results) / len(adaptation_results)
    therapeutic_preservation_rate = sum(
        1 for result in adaptation_results if result.therapeutic_integrity_preserved
    ) / len(adaptation_results)

    # Симуляция метрик (в реальной системе будут собираться от пользователей)
    completion_rate = min(avg_quality + 0.1, 1.0)
    engagement_score = avg_quality
    comprehension_level = min(avg_quality + 0.05, 1.0)

    # Точность определения модальности (если есть профиль пользователя)
    modality_accuracy = 0.8  # Базовое значение
    if user_profile:
        # Проверяем соответствие адаптации профилю
        profile_matches = 0
        for result in adaptation_results:
            if result.target_modality == user_profile.primary_modality:
                profile_matches += 1
        modality_accuracy = profile_matches / len(adaptation_results)

    return VAKMetrics(
        completion_rate=completion_rate,
        engagement_score=engagement_score,
        comprehension_level=comprehension_level,
        modality_preference_accuracy=modality_accuracy,
        therapeutic_effectiveness=therapeutic_preservation_rate,
        adaptation_time=2.5,  # Среднее время адаптации
        user_satisfaction=avg_quality
    )


# Вспомогательные функции

async def _adapt_predicates(content: str, target_modality: VAKModalityType, depth: AdaptationDepth) -> Tuple[str, List[str]]:
    """Адаптация предикатов под целевую модальность."""
    changes = []
    adapted_content = content

    # Определяем предикаты для замены
    target_predicates = {
        VAKModalityType.VISUAL: VISUAL_PREDICATES,
        VAKModalityType.AUDITORY: AUDITORY_PREDICATES,
        VAKModalityType.KINESTHETIC: KINESTHETIC_PREDICATES
    }.get(target_modality, [])

    if not target_predicates:
        return adapted_content, changes

    # Создаем словарь замен (упрощенная версия)
    replacements = {
        "чувствовать": {
            VAKModalityType.VISUAL: "видеть",
            VAKModalityType.AUDITORY: "слышать",
            VAKModalityType.KINESTHETIC: "ощущать"
        },
        "понимать": {
            VAKModalityType.VISUAL: "ясно видеть",
            VAKModalityType.AUDITORY: "услышать",
            VAKModalityType.KINESTHETIC: "почувствовать"
        },
        "знать": {
            VAKModalityType.VISUAL: "представлять",
            VAKModalityType.AUDITORY: "слышать внутренним голосом",
            VAKModalityType.KINESTHETIC: "ощущать внутренне"
        }
    }

    for original, modality_replacements in replacements.items():
        if original in adapted_content.lower() and target_modality in modality_replacements:
            replacement = modality_replacements[target_modality]
            adapted_content = re.sub(
                rf'\b{original}\b', replacement, adapted_content, flags=re.IGNORECASE
            )
            changes.append(f"Заменен предикат '{original}' на '{replacement}'")

    return adapted_content, changes


async def _adapt_structure(content: str, target_modality: VAKModalityType, structure_info: Dict) -> Tuple[str, List[str]]:
    """Адаптация структуры контента под модальность."""
    changes = []
    adapted_content = content

    if target_modality == VAKModalityType.VISUAL:
        # Для визуалов: короткие абзацы, списки
        if structure_info.get("avg_sentence_length", 0) > 15:
            # Разбиваем длинные предложения
            sentences = re.split(r'[.!?]+', adapted_content)
            adapted_sentences = []
            for sentence in sentences:
                if len(sentence.split()) > 15:
                    # Простое разбиение по запятым
                    parts = sentence.split(', ')
                    adapted_sentences.extend([part.strip() + '.' for part in parts if part.strip()])
                else:
                    adapted_sentences.append(sentence.strip())
            adapted_content = ' '.join(adapted_sentences)
            changes.append("Разбиты длинные предложения для визуального восприятия")

    elif target_modality == VAKModalityType.AUDITORY:
        # Для аудиалов: ритмичность, повторы
        if not re.search(r'\b(во-первых|во-вторых|затем|далее)\b', adapted_content, re.IGNORECASE):
            # Добавляем структурные маркеры
            paragraphs = adapted_content.split('\n\n')
            if len(paragraphs) > 1:
                structured_paragraphs = []
                for i, paragraph in enumerate(paragraphs):
                    if i == 0:
                        structured_paragraphs.append(f"Прежде всего, {paragraph}")
                    elif i == len(paragraphs) - 1:
                        structured_paragraphs.append(f"И наконец, {paragraph}")
                    else:
                        structured_paragraphs.append(f"Далее, {paragraph}")
                adapted_content = '\n\n'.join(structured_paragraphs)
                changes.append("Добавлены аудиальные структурные маркеры")

    elif target_modality == VAKModalityType.KINESTHETIC:
        # Для кинестетиков: более детальные описания, процессы
        if structure_info.get("avg_sentence_length", 0) < 12:
            # Добавляем детализацию
            adapted_content = re.sub(
                r'\b(сделать|выполнить)\b',
                r'медленно и осознанно \1',
                adapted_content,
                flags=re.IGNORECASE
            )
            changes.append("Добавлена детализация для кинестетического восприятия")

    return adapted_content, changes


async def _adapt_metaphors(content: str, target_modality: VAKModalityType) -> Tuple[str, List[str]]:
    """Адаптация метафор под модальность."""
    changes = []
    adapted_content = content

    metaphors = VAK_METAPHORS.get(target_modality, [])
    if not metaphors:
        return adapted_content, changes

    # Простая замена общих метафор на специфичные для модальности
    general_metaphors = {
        "понять суть": {
            VAKModalityType.VISUAL: "увидеть ясную картину",
            VAKModalityType.AUDITORY: "услышать внутренний голос",
            VAKModalityType.KINESTHETIC: "почувствовать глубинную истину"
        },
        "найти решение": {
            VAKModalityType.VISUAL: "увидеть светлый путь",
            VAKModalityType.AUDITORY: "услышать правильный ответ",
            VAKModalityType.KINESTHETIC: "нащупать верное направление"
        }
    }

    for general, specific in general_metaphors.items():
        if general in adapted_content.lower() and target_modality in specific:
            replacement = specific[target_modality]
            adapted_content = re.sub(
                general, replacement, adapted_content, flags=re.IGNORECASE
            )
            changes.append(f"Адаптирована метафора: '{general}' → '{replacement}'")

    return adapted_content, changes


async def _complete_reconstruction(
    content: str, target_modality: VAKModalityType, module_type: PatternShiftModuleType
) -> Tuple[str, List[str]]:
    """Полная реконструкция контента под модальность и тип модуля."""
    changes = []

    # Эта функция выполняет глубокую реконструкцию контента
    # В реальной реализации здесь был бы сложный алгоритм
    # с использованием AI для полной переработки

    reconstruction_templates = {
        (VAKModalityType.VISUAL, PatternShiftModuleType.VISUALIZATION): {
            "prefix": "Представьте себе яркую, детальную картину...",
            "structure": "визуальная последовательность образов",
            "suffix": "...удерживайте этот ясный образ в сознании."
        },
        (VAKModalityType.AUDITORY, PatternShiftModuleType.MEDITATION): {
            "prefix": "Прислушайтесь к внутреннему звучанию...",
            "structure": "ритмичная последовательность звуков",
            "suffix": "...позвольте этой мелодии наполнить ваше сознание."
        },
        (VAKModalityType.KINESTHETIC, PatternShiftModuleType.MOVEMENT): {
            "prefix": "Почувствуйте, как ваше тело медленно...",
            "structure": "последовательность физических ощущений",
            "suffix": "...ощутите глубокое расслабление и покой."
        }
    }

    template_key = (target_modality, module_type)
    if template_key in reconstruction_templates:
        template = reconstruction_templates[template_key]
        reconstructed = f"{template['prefix']}\n\n{content}\n\n{template['suffix']}"
        changes.append(f"Полная реконструкция для {target_modality.value} + {module_type.value}")
        return reconstructed, changes

    return content, changes


async def _validate_therapeutic_integrity(
    original: str, adapted: str, preserve_goals: bool
) -> bool:
    """Валидация сохранения терапевтической целостности."""
    if not preserve_goals:
        return True

    # Проверяем ключевые терапевтические элементы
    therapeutic_keywords = [
        "осознание", "понимание", "принятие", "изменение", "рост",
        "развитие", "исцеление", "трансформация", "интеграция"
    ]

    original_therapeutic_count = sum(
        1 for keyword in therapeutic_keywords
        if keyword in original.lower()
    )

    adapted_therapeutic_count = sum(
        1 for keyword in therapeutic_keywords
        if keyword in adapted.lower()
    )

    # Считаем целостность сохраненной, если количество терапевтических
    # элементов не уменьшилось более чем на 30%
    if original_therapeutic_count == 0:
        return True

    preservation_ratio = adapted_therapeutic_count / original_therapeutic_count
    return preservation_ratio >= 0.7


async def _calculate_adaptation_quality(
    original: str, adapted: str, target_modality: VAKModalityType
) -> float:
    """Расчет качества адаптации."""
    # Анализируем оба текста
    original_analysis = await analyze_content_vak_modalities(
        None, original, False  # Упрощенный анализ без контекста
    )
    adapted_analysis = await analyze_content_vak_modalities(
        None, adapted, False
    )

    # Получаем оценку целевой модальности в адаптированном тексте
    target_score_adapted = adapted_analysis.modality_scores.get(target_modality.value, 0)
    target_score_original = original_analysis.modality_scores.get(target_modality.value, 0)

    # Качество = улучшение + базовое качество
    improvement = max(0, target_score_adapted - target_score_original)
    base_quality = min(target_score_adapted, 0.8)

    return min(base_quality + improvement, 1.0)


def _extract_visual_elements(content: str) -> List[str]:
    """Извлечение визуальных элементов из контента."""
    visual_elements = []

    # Поиск визуальных описаний
    visual_patterns = [
        r'представ[ьл][яте][ете]?\s+[^.]+',
        r'вообраз[ить][те]?\s+[^.]+',
        r'увид[ьл][ите]?\s+[^.]+',
        r'(яркий|ясный|четкий|красочный)\s+[^.]+',
    ]

    for pattern in visual_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        visual_elements.extend(matches)

    return visual_elements[:5]  # Ограничиваем количество


def _extract_auditory_elements(content: str) -> List[str]:
    """Извлечение аудиальных элементов из контента."""
    auditory_elements = []

    auditory_patterns = [
        r'послуша[йте]+\s+[^.]+',
        r'услыш[ьл][ите]?\s+[^.]+',
        r'звуч[ит]+\s+[^.]+',
        r'(мелодичн[ый]|ритмичн[ый]|гармоничн[ый])\s+[^.]+',
    ]

    for pattern in auditory_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        auditory_elements.extend(matches)

    return auditory_elements[:5]


def _extract_kinesthetic_elements(content: str) -> List[str]:
    """Извлечение кинестетических элементов из контента."""
    kinesthetic_elements = []

    kinesthetic_patterns = [
        r'почувству[йте]+\s+[^.]+',
        r'ощут[ить][те]?\s+[^.]+',
        r'прикосн[уться][итесь]?\s+[^.]+',
        r'(теплый|мягкий|легкий|глубокий)\s+[^.]+',
    ]

    for pattern in kinesthetic_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        kinesthetic_elements.extend(matches)

    return kinesthetic_elements[:5]


async def _create_integration_instructions(
    module_type: PatternShiftModuleType,
    visual_elements: List[str],
    auditory_elements: List[str],
    kinesthetic_elements: List[str]
) -> str:
    """Создание инструкций по интеграции мультимодальных элементов."""
    instructions = f"Инструкции по интеграции для модуля типа {module_type.value}:\n\n"

    if visual_elements:
        instructions += "1. Визуальная активация:\n"
        instructions += "   - Начните с визуализации\n"
        instructions += f"   - Ключевые образы: {', '.join(visual_elements[:2])}\n\n"

    if auditory_elements:
        instructions += "2. Аудиальная поддержка:\n"
        instructions += "   - Добавьте звуковое сопровождение\n"
        instructions += f"   - Ключевые звуки: {', '.join(auditory_elements[:2])}\n\n"

    if kinesthetic_elements:
        instructions += "3. Кинестетическое закрепление:\n"
        instructions += "   - Завершите физическими ощущениями\n"
        instructions += f"   - Ключевые ощущения: {', '.join(kinesthetic_elements[:2])}\n\n"

    instructions += "4. Синестетическая интеграция:\n"
    instructions += "   - Объедините все модальности в единый опыт\n"
    instructions += "   - Переходите плавно между модальностями\n"
    instructions += "   - Позвольте пользователю выбрать доминирующую модальность"

    return instructions


def _create_activation_sequence(module_type: PatternShiftModuleType) -> List[str]:
    """Создание рекомендуемой последовательности активации модальностей."""
    sequences = {
        PatternShiftModuleType.VISUALIZATION: [
            "Визуальная активация",
            "Кинестетическое углубление",
            "Аудиальное закрепление"
        ],
        PatternShiftModuleType.MEDITATION: [
            "Аудиальная настройка",
            "Кинестетическое расслабление",
            "Визуальная фокусировка"
        ],
        PatternShiftModuleType.MOVEMENT: [
            "Кинестетическая активация",
            "Визуальная координация",
            "Аудиальная синхронизация"
        ],
        PatternShiftModuleType.TECHNIQUE: [
            "Аудиальное объяснение",
            "Визуальная демонстрация",
            "Кинестетическая практика"
        ]
    }

    return sequences.get(module_type, [
        "Универсальная активация",
        "Адаптивная интеграция",
        "Пользовательский выбор"
    ])


async def _check_cultural_sensitivity(content: str) -> List[str]:
    """Проверка культурной чувствительности контента."""
    issues = []

    # Проверка на потенциально проблематичные формулировки
    sensitive_patterns = [
        (r'\b(мужчин[аы]|женщин[аы])\s+(должн[ыа]|обязан[ыа])\b', "Гендерные стереотипы"),
        (r'\b(национальност[ьи]|раса)\b', "Упоминание расовых/национальных различий"),
        (r'\b(религи[яи]|бог|церковь)\b', "Религиозные упоминания без контекста")
    ]

    for pattern, issue_type in sensitive_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"Потенциальная проблема культурной чувствительности: {issue_type}")

    return issues