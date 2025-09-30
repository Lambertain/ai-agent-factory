"""
Инструменты для Pattern Test Architect Agent
"""

import asyncio
import json
import re
from typing import Any, Dict, List, Optional, Tuple
from .models import (
    TestQuestion,
    QuestionType,
    PsychometricValidation,
    ViralTestTransformation,
    InterpretationScale,
    EffectivenessAnalysis,
    PsychologicalConstruct,
    TargetAudience,
    DifficultyLevel
)


async def validate_psychometric_properties(
    methodology: str,
    target_construct: PsychologicalConstruct
) -> PsychometricValidation:
    """
    Валидация психометрических свойств базовой методики

    Args:
        methodology: Название базовой методики (PHQ-9, GAD-7, etc.)
        target_construct: Целевой психологический конструкт

    Returns:
        PsychometricValidation: Результаты валидации
    """

    # База данных валидированных методик
    validated_methodologies = {
        "PHQ-9": {
            "construct": PsychologicalConstruct.DEPRESSION,
            "validity": 0.89,
            "reliability": 0.87,
            "construct_validity": 0.91,
            "content_validity": 0.85,
            "criterion_validity": 0.88,
            "internal_consistency": 0.89,
            "test_retest": 0.84
        },
        "GAD-7": {
            "construct": PsychologicalConstruct.ANXIETY,
            "validity": 0.86,
            "reliability": 0.89,
            "construct_validity": 0.88,
            "content_validity": 0.83,
            "criterion_validity": 0.85,
            "internal_consistency": 0.92,
            "test_retest": 0.83
        },
        "DASS-21": {
            "construct": PsychologicalConstruct.STRESS,
            "validity": 0.85,
            "reliability": 0.88,
            "construct_validity": 0.87,
            "content_validity": 0.82,
            "criterion_validity": 0.84,
            "internal_consistency": 0.91,
            "test_retest": 0.86
        },
        "Big Five": {
            "construct": PsychologicalConstruct.PERSONALITY_BIG5,
            "validity": 0.92,
            "reliability": 0.90,
            "construct_validity": 0.94,
            "content_validity": 0.88,
            "criterion_validity": 0.89,
            "internal_consistency": 0.88,
            "test_retest": 0.92
        },
        "Rosenberg Self-Esteem Scale": {
            "construct": PsychologicalConstruct.SELF_ESTEEM,
            "validity": 0.84,
            "reliability": 0.86,
            "construct_validity": 0.85,
            "content_validity": 0.82,
            "criterion_validity": 0.83,
            "internal_consistency": 0.87,
            "test_retest": 0.85
        }
    }

    issues = []

    if methodology not in validated_methodologies:
        return PsychometricValidation(
            is_valid=False,
            validity_score=0.0,
            reliability_score=0.0,
            construct_validity=0.0,
            content_validity=0.0,
            criterion_validity=0.0,
            internal_consistency=0.0,
            test_retest_reliability=None,
            issues=[f"Методика '{methodology}' не найдена в базе валидированных методик"],
            ethical_compliance=False
        )

    method_data = validated_methodologies[methodology]

    # Проверка соответствия конструкта
    if method_data["construct"] != target_construct:
        issues.append(f"Методика '{methodology}' не подходит для измерения {target_construct}")

    # Проверка минимальных пороговых значений
    min_thresholds = {
        "validity": 0.7,
        "reliability": 0.7,
        "internal_consistency": 0.7
    }

    for metric, threshold in min_thresholds.items():
        if method_data[metric] < threshold:
            issues.append(f"Низкий показатель {metric}: {method_data[metric]} < {threshold}")

    is_valid = len(issues) == 0 and method_data["validity"] >= 0.7

    return PsychometricValidation(
        is_valid=is_valid,
        validity_score=method_data["validity"],
        reliability_score=method_data["reliability"],
        construct_validity=method_data["construct_validity"],
        content_validity=method_data["content_validity"],
        criterion_validity=method_data["criterion_validity"],
        internal_consistency=method_data["internal_consistency"],
        test_retest_reliability=method_data.get("test_retest"),
        issues=issues,
        ethical_compliance=is_valid and "депрессия" not in methodology.lower()
    )


async def transform_academic_to_viral(
    academic_name: str,
    target_audience: TargetAudience,
    emotional_hook: Optional[str] = None
) -> ViralTestTransformation:
    """
    Трансформация академического названия теста в вирусное

    Args:
        academic_name: Академическое название
        target_audience: Целевая аудитория
        emotional_hook: Желаемый эмоциональный крючок

    Returns:
        ViralTestTransformation: Результат трансформации
    """

    # Паттерны вирусных названий по болевым точкам
    viral_patterns = {
        "depression": [
            "Почему ты постоянно грустный?",
            "Что отнимает у тебя энергию?",
            "Почему жизнь кажется серой?",
            "Почему ты не радуешься жизни?"
        ],
        "anxiety": [
            "Почему ты постоянно переживаешь?",
            "Что тебя так беспокоит?",
            "Почему ты боишься жить?",
            "Откуда твои страхи?"
        ],
        "relationships": [
            "Почему у тебя не складываются отношения?",
            "Почему тебя не понимают в отношениях?",
            "Что ты делаешь не так в любви?",
            "Почему ты притягиваешь не тех людей?"
        ],
        "self_esteem": [
            "Почему ты не ценишь себя?",
            "Почему ты не веришь в себя?",
            "Что мешает тебе любить себя?",
            "Почему ты сравниваешь себя с другими?"
        ],
        "career": [
            "Что мешает твоей карьере?",
            "Почему ты застрял на работе?",
            "Что блокирует твой успех?",
            "Почему ты не добиваешься целей?"
        ],
        "communication": [
            "Почему тебя не понимают окружающие?",
            "Почему твои слова игнорируют?",
            "Что не так с твоим общением?",
            "Почему конфликты повторяются?"
        ]
    }

    # Определение категории по академическому названию
    category = "general"
    if any(word in academic_name.lower() for word in ["depression", "депрессия", "phq"]):
        category = "depression"
    elif any(word in academic_name.lower() for word in ["anxiety", "тревога", "gad"]):
        category = "anxiety"
    elif any(word in academic_name.lower() for word in ["relationship", "attachment", "отношения"]):
        category = "relationships"
    elif any(word in academic_name.lower() for word in ["self-esteem", "самооценка", "rosenberg"]):
        category = "self_esteem"
    elif any(word in academic_name.lower() for word in ["career", "карьера", "работа"]):
        category = "career"
    elif any(word in academic_name.lower() for word in ["communication", "общение"]):
        category = "communication"

    # Выбор вирусного названия
    if emotional_hook:
        viral_name = emotional_hook
    elif category in viral_patterns:
        viral_name = viral_patterns[category][0]  # Берем первый вариант
    else:
        viral_name = f"Что говорит о тебе этот тест?"

    # Определение болевой точки
    pain_points = {
        "depression": "Отсутствие энергии и радости жизни",
        "anxiety": "Постоянные переживания и страхи",
        "relationships": "Проблемы в личных отношениях",
        "self_esteem": "Низкая самооценка и неуверенность",
        "career": "Застой в карьере и недостижение целей",
        "communication": "Непонимание в общении",
        "general": "Неясность в понимании себя"
    }

    # Адаптация стиля под аудиторию
    language_styles = {
        TargetAudience.TEENS: "молодежный, с сленгом",
        TargetAudience.YOUNG_ADULTS: "современный, прямой",
        TargetAudience.ADULTS: "серьезный, но понятный",
        TargetAudience.MATURE: "уважительный, мудрый",
        TargetAudience.PROFESSIONALS: "деловой, точный",
        TargetAudience.STUDENTS: "энергичный, мотивирующий",
        TargetAudience.GENERAL: "универсальный, простой"
    }

    # Расчет вирусного потенциала
    viral_factors = {
        "question_format": 0.8 if viral_name.startswith("Почему") else 0.6,
        "emotional_impact": 0.9 if any(word in viral_name.lower() for word in ["не", "мешает", "проблема"]) else 0.7,
        "personal_relevance": 0.8 if "ты" in viral_name else 0.6,
        "curiosity_gap": 0.7
    }

    viral_score = sum(viral_factors.values()) / len(viral_factors)

    return ViralTestTransformation(
        original_name=academic_name,
        viral_name=viral_name,
        emotional_hook=emotional_hook or f"Болевая точка: {pain_points[category]}",
        target_pain_point=pain_points[category],
        language_style=language_styles[target_audience],
        expected_engagement=min(viral_score + 0.1, 1.0),
        viral_potential_score=viral_score
    )


async def generate_test_questions(
    construct: PsychologicalConstruct,
    question_count: int,
    difficulty_level: DifficultyLevel,
    language_style: str
) -> List[TestQuestion]:
    """
    Генерация вопросов для психологического теста

    Args:
        construct: Психологический конструкт
        question_count: Количество вопросов
        difficulty_level: Уровень сложности
        language_style: Стиль языка

    Returns:
        List[TestQuestion]: Список сгенерированных вопросов
    """

    # Базы вопросов по конструктам
    question_templates = {
        PsychologicalConstruct.DEPRESSION: [
            "Как часто ты чувствуешь себя подавленно?",
            "Бывает ли так, что ничего не хочется делать?",
            "Насколько часто ты теряешь интерес к вещам, которые раньше нравились?",
            "Как часто ты чувствуешь усталость без видимой причины?",
            "Бывает ли у тебя ощущение безнадежности?",
            "Как часто ты винишь себя за неудачи?",
            "Насколько трудно тебе концентрироваться?",
            "Как часто у тебя бывают мысли о смерти?",
            "Бывает ли так, что ты чувствуешь себя никчемным?",
            "Как часто ты избегаешь общения с людьми?"
        ],
        PsychologicalConstruct.ANXIETY: [
            "Как часто ты переживаешь о будущем?",
            "Бывает ли у тебя ощущение, что сердце колотится без причины?",
            "Насколько часто ты чувствуешь напряжение в теле?",
            "Как часто ты не можешь расслабиться?",
            "Бывает ли так, что ты накручиваешь себя по мелочам?",
            "Как часто ты избегаешь ситуаций из-за страха?",
            "Насколько часто у тебя потеют ладони в стрессе?",
            "Как часто ты чувствуешь головокружение от волнения?",
            "Бывает ли у тебя ощущение нехватки воздуха?",
            "Как часто ты просыпаешься от тревожных мыслей?"
        ],
        PsychologicalConstruct.SELF_ESTEEM: [
            "Насколько ты доволен собой?",
            "Как часто ты сравниваешь себя с другими?",
            "Бывает ли так, что ты считаешь себя неудачником?",
            "Как часто ты сомневаешься в своих способностях?",
            "Насколько легко тебе принимать комплименты?",
            "Как часто ты критикуешь себя?",
            "Бывает ли у тебя ощущение, что ты недостоин любви?",
            "Как часто ты боишься показаться глупым?",
            "Насколько комфортно тебе быть в центре внимания?",
            "Как часто ты извиняешься без причины?"
        ]
    }

    # Определение шкал ответов
    likert_5_labels = {
        "1": "Никогда",
        "2": "Редко",
        "3": "Иногда",
        "4": "Часто",
        "5": "Всегда"
    }

    questions = []
    base_questions = question_templates.get(construct, [])

    # Если базовых вопросов недостаточно, дополняем общими
    if len(base_questions) < question_count:
        general_questions = [
            f"Как это влияет на твою жизнь?",
            f"Что ты чувствуешь в таких ситуациях?",
            f"Как часто это происходит?",
            f"Насколько это мешает тебе?"
        ]
        base_questions.extend(general_questions)

    # Отбираем нужное количество вопросов
    selected_questions = base_questions[:question_count]

    for i, question_text in enumerate(selected_questions):
        # Адаптация сложности
        if difficulty_level == DifficultyLevel.EASY:
            question_text = question_text.replace("Насколько", "Как")
        elif difficulty_level == DifficultyLevel.HARD:
            question_text = question_text.replace("Как часто", "В какой степени")

        # Определение типа вопроса
        question_type = QuestionType.LIKERT_5
        if "или" in question_text.lower():
            question_type = QuestionType.MULTIPLE_CHOICE

        # Создание объекта вопроса
        question = TestQuestion(
            id=i + 1,
            text=question_text,
            question_type=question_type,
            scale_labels=likert_5_labels if question_type == QuestionType.LIKERT_5 else None,
            reverse_scored=(i % 4 == 3),  # Каждый 4-й вопрос с обратной оценкой
            weight=1.0,
            construct_facet=f"{construct.value}_facet_{(i % 3) + 1}",
            clarity_score=0.8 + (0.2 * (i % 2))  # Варьируем оценку ясности
        )

        questions.append(question)

    return questions


async def create_interpretation_scales(
    construct: PsychologicalConstruct,
    result_ranges: int,
    transformation_programs: List[str]
) -> List[InterpretationScale]:
    """
    Создание шкал интерпретации результатов

    Args:
        construct: Психологический конструкт
        result_ranges: Количество диапазонов
        transformation_programs: Связанные программы

    Returns:
        List[InterpretationScale]: Шкалы интерпретации
    """

    # Базовые интерпретации по конструктам
    interpretation_templates = {
        PsychologicalConstruct.DEPRESSION: {
            "low": {
                "title": "Легкая грусть",
                "description": "Твое эмоциональное состояние в пределах нормы. Иногда грусть - это нормальная реакция на жизненные события.",
                "recommendations": [
                    "Поддерживай активный образ жизни",
                    "Общайся с близкими людьми",
                    "Занимайся тем, что приносит радость"
                ],
                "color": "#4CAF50"
            },
            "medium": {
                "title": "Периодическая подавленность",
                "description": "Ты переживаешь сложный период. Это не критично, но стоит уделить внимание своему эмоциональному состоянию.",
                "recommendations": [
                    "Обратись к специалисту для консультации",
                    "Попробуй техники релаксации",
                    "Пересмотри режим сна и питания"
                ],
                "color": "#FF9800"
            },
            "high": {
                "title": "Серьезная подавленность",
                "description": "Твое состояние требует внимания. Рекомендуется обратиться к психологу или психотерапевту.",
                "recommendations": [
                    "Обязательно обратись к специалисту",
                    "Не оставайся один на один с проблемой",
                    "Рассмотри возможность психотерапии"
                ],
                "color": "#F44336"
            }
        },
        PsychologicalConstruct.ANXIETY: {
            "low": {
                "title": "Спокойствие и уверенность",
                "description": "Ты хорошо справляешься со стрессом и редко испытываешь тревогу. Это отличный результат!",
                "recommendations": [
                    "Продолжай использовать свои навыки",
                    "Делись опытом с другими",
                    "Поддерживай здоровый баланс"
                ],
                "color": "#4CAF50"
            },
            "medium": {
                "title": "Умеренная тревожность",
                "description": "Иногда ты переживаешь больше обычного. Это нормально, но можно научиться справляться лучше.",
                "recommendations": [
                    "Изучи техники дыхания",
                    "Попробуй медитацию",
                    "Определи источники стресса"
                ],
                "color": "#FF9800"
            },
            "high": {
                "title": "Повышенная тревожность",
                "description": "Тревога существенно влияет на твою жизнь. Стоит поработать над этим с профессионалом.",
                "recommendations": [
                    "Обратись к психологу",
                    "Рассмотри когнитивно-поведенческую терапию",
                    "Изучи техники управления тревогой"
                ],
                "color": "#F44336"
            }
        }
    }

    # Получаем шаблоны для конструкта или используем общие
    templates = interpretation_templates.get(construct, interpretation_templates[PsychologicalConstruct.ANXIETY])

    scales = []
    level_names = ["low", "medium", "high"]

    # Адаптируем под количество диапазонов
    if result_ranges == 5:
        level_names = ["very_low", "low", "medium", "high", "very_high"]
    elif result_ranges == 4:
        level_names = ["low", "medium-low", "medium-high", "high"]

    # Создаем шкалы
    range_size = 1.0 / result_ranges
    for i in range(result_ranges):
        level_key = level_names[min(i, len(level_names) - 1)]

        # Берем соответствующий шаблон или адаптируем
        if level_key in templates:
            template = templates[level_key]
        else:
            # Адаптируем существующие шаблоны
            if i < result_ranges // 2:
                template = templates["low"]
            elif i == result_ranges // 2:
                template = templates["medium"]
            else:
                template = templates["high"]

        # Вычисляем диапазон баллов
        score_min = i * range_size
        score_max = (i + 1) * range_size

        # Связываем программы в зависимости от уровня
        linked_programs = []
        if i >= result_ranges // 2 and transformation_programs:
            linked_programs = transformation_programs[:2]  # Даем первые 2 программы

        scale = InterpretationScale(
            level=f"level_{i+1}",
            score_range=(score_min, score_max),
            title=template["title"],
            description=template["description"],
            recommendations=template["recommendations"],
            linked_programs=linked_programs,
            color_code=template["color"]
        )

        scales.append(scale)

    return scales


async def analyze_test_effectiveness(
    questions: List[TestQuestion],
    target_metrics: Dict[str, float]
) -> EffectivenessAnalysis:
    """
    Анализ эффективности созданного теста

    Args:
        questions: Список вопросов теста
        target_metrics: Целевые метрики

    Returns:
        EffectivenessAnalysis: Анализ эффективности
    """

    # Анализ длины теста
    question_count = len(questions)
    completion_rate_base = 0.9 if question_count <= 10 else 0.8 if question_count <= 20 else 0.7

    # Анализ сложности вопросов
    avg_clarity = sum(q.clarity_score for q in questions) / len(questions)
    complexity_penalty = 0.1 if avg_clarity < 0.7 else 0

    # Анализ вирусности
    viral_indicators = 0
    for question in questions:
        if any(word in question.text.lower() for word in ["ты", "твой", "почему", "как часто"]):
            viral_indicators += 1

    viral_score = min(viral_indicators / len(questions), 1.0)

    # Анализ вовлеченности
    engagement_factors = {
        "personal_pronouns": viral_score,
        "question_variety": len(set(q.question_type for q in questions)) / 3,  # Разнообразие типов
        "clarity": avg_clarity,
        "optimal_length": 1.0 if 10 <= question_count <= 20 else 0.8
    }

    engagement_score = sum(engagement_factors.values()) / len(engagement_factors)

    # Прогноз завершений
    completion_rate = max(0.1, completion_rate_base - complexity_penalty)

    # Базовые прогнозы (можно улучшить с помощью ML)
    predicted_shares = int(viral_score * engagement_score * 1000)
    predicted_completions = int(predicted_shares * completion_rate * 0.7)

    # Определение узких мест
    bottlenecks = []
    if question_count > 25:
        bottlenecks.append("Слишком много вопросов - может снизить завершаемость")
    if avg_clarity < 0.7:
        bottlenecks.append("Низкая ясность вопросов")
    if viral_score < 0.5:
        bottlenecks.append("Низкий вирусный потенциал")
    if engagement_score < 0.6:
        bottlenecks.append("Недостаточная вовлеченность")

    # Потенциал трансформации
    transformation_potential = min(
        engagement_score * 0.4 +
        viral_score * 0.3 +
        avg_clarity * 0.3,
        1.0
    )

    return EffectivenessAnalysis(
        completion_rate_prediction=completion_rate,
        viral_score=viral_score,
        engagement_score=engagement_score,
        transformation_potential=transformation_potential,
        predicted_shares=predicted_shares,
        predicted_completions=predicted_completions,
        bottlenecks=bottlenecks
    )


async def search_agent_knowledge(
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в специализированной базе знаний Pattern Test Architect Agent.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    # Поиск в знаниях агента по тегам PatternShift и психометрики
    search_tags = ["pattern-test-architect", "psychometry", "psychological-tests", "patternshift"]

    try:
        # Используем Archon MCP для поиска
        from ..common.archon_integration import mcp__archon__rag_search_knowledge_base

        result = await mcp__archon__rag_search_knowledge_base(
            query=f"{query} {' '.join(search_tags)}",
            match_count=match_count
        )

        if result["success"] and result["results"]:
            knowledge = "\n".join([
                f"**{r['metadata']['title']}:**\n{r['content']}"
                for r in result["results"]
            ])
            return f"База знаний Pattern Test Architect:\n{knowledge}"
        else:
            # Fallback поиск по названию агента
            fallback_result = await mcp__archon__rag_search_knowledge_base(
                query="pattern test architect knowledge base psychometry",
                match_count=1
            )

            if fallback_result["success"] and fallback_result["results"]:
                knowledge = "\n".join([
                    f"**{r['metadata']['title']}:**\n{r['content']}"
                    for r in fallback_result["results"]
                ])
                return f"База знаний (fallback поиск):\n{knowledge}"

            # Локальные знания агента при отсутствии RAG
            return """
База знаний Pattern Test Architect:

**Основные принципы психометрии:**
- Надёжность (reliability) - стабильность измерений
- Валидность (validity) - измерение того, что заявлено
- Стандартизация - единые условия проведения

**Этические ограничения:**
- Запрет диагностики серьёзных расстройств без специалиста
- Возрастные ограничения для деликатных тем
- Культурная адаптация

**Вирусные принципы:**
- Эмоциональная привлекательность названий
- Простота языка для широкой аудитории
- Фокус на практической пользе результатов

**Методики-основы:**
- PHQ-9 для депрессии
- GAD-7 для тревожности
- Большая пятёрка для личности
- Шкала самооценки Розенберга
"""

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"