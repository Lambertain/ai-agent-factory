"""
Инструменты для Pattern Exercise Architect Agent
"""

import uuid
from typing import List, Dict, Any, Optional
from pydantic_ai import RunContext

from .dependencies import PatternExerciseArchitectDependencies
from .models import (
    TransformationalExercise,
    ExerciseStep,
    CompletionCriteria,
    ExerciseVariant,
    ExerciseSequence,
    ExerciseType,
    ExerciseDifficulty,
    LearningChannel
)


async def design_transformational_exercise(
    ctx: RunContext[PatternExerciseArchitectDependencies],
    goal_description: str,
    nlp_technique: Optional[str] = None,
    target_difficulty: str = "intermediate",
    duration_minutes: int = 20,
    primary_channel: str = "cognitive",
    context: str = "home"
) -> str:
    """
    Спроектировать трансформационное упражнение.

    Args:
        ctx: Контекст выполнения
        goal_description: Цель упражнения (что пользователь хочет достичь)
        nlp_technique: НЛП техника для интеграции (опционально)
        target_difficulty: Уровень сложности (beginner/intermediate/advanced/expert)
        duration_minutes: Длительность упражнения в минутах
        primary_channel: Основной канал научения (cognitive/emotional/somatic/social)
        context: Контекст выполнения (home/work/public)

    Returns:
        Описание спроектированного упражнения
    """

    # Генерируем ID упражнения
    exercise_id = f"ex_{uuid.uuid4().hex[:8]}"

    # Определяем тип упражнения на основе НЛП техники
    exercise_type = ExerciseType.NLP_TECHNIQUE if nlp_technique else ExerciseType.INTEGRATION

    # Создаем шаги упражнения
    steps = []
    step_duration = duration_minutes // 4  # Разбиваем на 4 основных шага

    # Шаг 1: Подготовка
    steps.append(ExerciseStep(
        step_number=1,
        title="Подготовка",
        description=f"Подготовка к упражнению: {goal_description}",
        duration_minutes=step_duration,
        instructions=[
            "Найдите тихое место где вас не будут отвлекать",
            f"Настройтесь на работу в канале {primary_channel}",
            "Убедитесь что у вас есть всё необходимое"
        ],
        tips=[
            "Выключите уведомления на телефоне",
            "Сядьте удобно",
            "Сделайте несколько глубоких вдохов"
        ],
        common_mistakes=[
            "Выполнение в спешке",
            "Пропуск подготовки"
        ]
    ))

    # Шаг 2: Основная практика
    practice_description = f"Применение техники {nlp_technique}" if nlp_technique else f"Работа с целью: {goal_description}"
    steps.append(ExerciseStep(
        step_number=2,
        title="Основная практика",
        description=practice_description,
        duration_minutes=step_duration * 2,
        instructions=[
            "Следуйте инструкциям техники пошагово",
            "Обращайте внимание на телесные ощущения",
            "Отмечайте возникающие эмоции"
        ],
        tips=[
            "Не торопитесь",
            "Доверяйте своему опыту",
            "Нет правильных или неправильных ощущений"
        ],
        common_mistakes=[
            "Интеллектуализация вместо проживания",
            "Ожидание мгновенных результатов"
        ]
    ))

    # Шаг 3: Интеграция
    steps.append(ExerciseStep(
        step_number=3,
        title="Интеграция",
        description="Закрепление опыта",
        duration_minutes=step_duration,
        instructions=[
            "Запишите ключевые инсайты",
            "Определите, как применить это в жизни",
            "Создайте план первых шагов"
        ],
        tips=[
            "Будьте конкретны в планах",
            "Начните с малого",
            "Привяжите к существующим привычкам"
        ],
        common_mistakes=[
            "Не записывать инсайты",
            "Слишком амбициозные планы"
        ]
    ))

    # Создаем критерии выполнения
    completion_criteria = [
        CompletionCriteria(
            description="Проживание опыта через выбранный канал",
            measurable=True,
            observable_signs=[
                "Изменение телесных ощущений",
                "Эмоциональный отклик",
                "Новое понимание"
            ],
            self_check_questions=[
                "Что я почувствовал в теле?",
                "Какие эмоции возникли?",
                "Что я понял про себя?"
            ]
        ),
        CompletionCriteria(
            description="Готовность к применению в жизни",
            measurable=True,
            observable_signs=[
                "Конкретный план действий",
                "Понимание контекстов применения",
                "Уверенность в способности применить"
            ],
            self_check_questions=[
                "Когда я буду это использовать?",
                "Как я узнаю что применяю правильно?",
                "С чего начну завтра?"
            ]
        )
    ]

    # Создаем упражнение
    exercise = TransformationalExercise(
        id=exercise_id,
        title=f"Упражнение: {goal_description[:50]}",
        description=f"Трансформационное упражнение для достижения цели: {goal_description}",
        exercise_type=exercise_type,
        difficulty=ExerciseDifficulty(target_difficulty),
        learning_channels=[LearningChannel(primary_channel)],
        primary_channel=LearningChannel(primary_channel),
        steps=steps,
        total_duration_minutes=duration_minutes,
        completion_criteria=completion_criteria,
        self_check_mechanism="Вопросы для самопроверки после каждого шага",
        nlp_technique_integrated=nlp_technique,
        transformation_goal=goal_description
    )

    # Формируем результат
    result = f"""
✅ **Создано трансформационное упражнение**

**ID:** {exercise.id}
**Название:** {exercise.title}
**Тип:** {exercise.exercise_type.value}
**Сложность:** {exercise.difficulty.value}
**Длительность:** {exercise.total_duration_minutes} минут
**Основной канал:** {exercise.primary_channel.value}

**Структура упражнения:**
"""
    for step in exercise.steps:
        result += f"\n{step.step_number}. **{step.title}** ({step.duration_minutes} мин)"
        result += f"\n   {step.description}"

    result += f"\n\n**Критерии выполнения:** {len(exercise.completion_criteria)} критериев"
    result += f"\n**Механизм самопроверки:** {exercise.self_check_mechanism}"

    if nlp_technique:
        result += f"\n**Интегрированная НЛП техника:** {nlp_technique}"

    return result


async def create_exercise_variants(
    ctx: RunContext[PatternExerciseArchitectDependencies],
    base_exercise_id: str,
    variant_types: List[str]
) -> str:
    """
    Создать варианты упражнения под разные типы.

    Args:
        ctx: Контекст выполнения
        base_exercise_id: ID базового упражнения
        variant_types: Типы вариантов (vak, age, difficulty, context)

    Returns:
        Описание созданных вариантов
    """

    variants_created = []

    for variant_type in variant_types:
        if variant_type == "vak":
            # VAK варианты
            for vak_type in ["visual", "auditory", "kinesthetic"]:
                adaptation = ctx.deps.get_vak_adaptation(vak_type)
                variants_created.append(f"VAK вариант ({vak_type}): {adaptation}")

        elif variant_type == "age":
            # Возрастные варианты
            for age_group in ["young_adults", "adults", "mature"]:
                adaptation = ctx.deps.get_age_adaptation(age_group)
                variants_created.append(f"Возрастной вариант ({age_group}): {adaptation}")

        elif variant_type == "difficulty":
            # Варианты сложности
            for difficulty in ["beginner", "intermediate", "advanced", "expert"]:
                variants_created.append(f"Уровень сложности ({difficulty})")

        elif variant_type == "context":
            # Контекстные варианты
            for context in ["home", "work", "public", "travel"]:
                variants_created.append(f"Контекст выполнения ({context})")

    result = f"""
✅ **Создано {len(variants_created)} вариантов упражнения**

**Базовое упражнение:** {base_exercise_id}
**Типы вариантов:** {', '.join(variant_types)}

**Варианты:**
"""
    for i, variant in enumerate(variants_created, 1):
        result += f"\n{i}. {variant}"

    return result


async def design_self_check_criteria(
    ctx: RunContext[PatternExerciseArchitectDependencies],
    exercise_type: str,
    transformation_goal: str
) -> str:
    """
    Создать критерии самопроверки для упражнения.

    Args:
        ctx: Контекст выполнения
        exercise_type: Тип упражнения
        transformation_goal: Цель трансформации

    Returns:
        Описание критериев самопроверки
    """

    # Получаем вопросы для самопроверки из базы данных
    self_check_questions = ctx.deps.get_self_check_questions()

    criteria = []

    # Критерий 1: Наблюдаемые признаки
    criteria.append(CompletionCriteria(
        description="Наблюдаемые признаки выполнения",
        measurable=True,
        observable_signs=[
            "Изменение физического состояния",
            "Новое поведение",
            "Видимые результаты"
        ],
        self_check_questions=[
            "Что изменилось в моем теле?",
            "Какие действия я совершил?",
            "Что стало по-другому?"
        ]
    ))

    # Критерий 2: Внутренние индикаторы
    criteria.append(CompletionCriteria(
        description="Внутренние индикаторы трансформации",
        measurable=True,
        observable_signs=[
            "Изменение эмоционального состояния",
            "Новые мысли и убеждения",
            "Другое восприятие ситуации"
        ],
        self_check_questions=list(self_check_questions.values())
    ))

    # Критерий 3: Интеграция в жизнь
    criteria.append(CompletionCriteria(
        description="Готовность к применению в жизни",
        measurable=True,
        observable_signs=[
            "Конкретный план действий",
            "Привязка к существующим привычкам",
            "Уверенность в применении"
        ],
        self_check_questions=[
            "Как я буду использовать это завтра?",
            "К какой привычке я привяжу это?",
            "Насколько я уверен что смогу применить? (1-10)"
        ]
    ))

    result = f"""
✅ **Создано {len(criteria)} критериев самопроверки**

**Тип упражнения:** {exercise_type}
**Цель трансформации:** {transformation_goal}

**Критерии выполнения:**
"""

    for i, criterion in enumerate(criteria, 1):
        result += f"\n\n{i}. **{criterion.description}**"
        result += f"\n   Измеримость: {'Да' if criterion.measurable else 'Нет'}"
        result += f"\n   Признаки: {', '.join(criterion.observable_signs[:2])}"
        result += f"\n   Вопросы: {criterion.self_check_questions[0]}"

    return result


async def adapt_nlp_technique_to_exercise(
    ctx: RunContext[PatternExerciseArchitectDependencies],
    nlp_technique: str,
    target_context: str,
    duration_minutes: int = 15
) -> str:
    """
    Адаптировать НЛП технику в формат упражнения.

    Args:
        ctx: Контекст выполнения
        nlp_technique: Название НЛП техники
        target_context: Целевой контекст применения
        duration_minutes: Длительность упражнения

    Returns:
        Описание адаптированного упражнения
    """

    # Получаем список НЛП техник
    available_techniques = ctx.deps.get_nlp_techniques()

    if nlp_technique.lower() not in [t.lower() for t in available_techniques]:
        return f"⚠️ НЛП техника '{nlp_technique}' не найдена в базе. Доступные: {', '.join(available_techniques)}"

    # Создаем адаптированное упражнение
    exercise_id = f"nlp_{nlp_technique.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"

    result = f"""
✅ **НЛП техника адаптирована в упражнение**

**Техника:** {nlp_technique}
**ID упражнения:** {exercise_id}
**Контекст:** {target_context}
**Длительность:** {duration_minutes} минут

**Структура адаптированного упражнения:**

1. **Подготовка** (3 мин)
   - Выбор ситуации для применения техники из контекста '{target_context}'
   - Калибровка текущего состояния
   - Установка намерения

2. **Применение техники {nlp_technique}** (8 мин)
   - Пошаговое выполнение техники
   - Проверка экологичности изменений
   - Тестирование результата

3. **Интеграция и закрепление** (4 мин)
   - Future pacing (проверка в будущем)
   - Создание триггеров для автоматического применения
   - План практики на неделю

**Критерии успешного выполнения:**
- Техника применена полностью
- Изменение состояния зафиксировано
- План интеграции создан

**Рекомендации:**
- Практиковать технику 1-2 раза в день
- Начинать с простых ситуаций
- Постепенно усложнять контексты применения
"""

    return result


async def search_agent_knowledge(
    ctx: RunContext[PatternExerciseArchitectDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний Pattern Exercise Architect Agent через Archon RAG.

    Args:
        ctx: Контекст выполнения
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """

    # Используем теги для фильтрации по знаниям агента
    search_tags = ctx.deps.knowledge_tags

    try:
        # Здесь будет вызов Archon RAG через MCP
        # result = await mcp__archon__rag_search_knowledge_base(
        #     query=f"{query} {' '.join(search_tags)}",
        #     match_count=match_count
        # )

        # Заглушка для текущей реализации
        return f"""
🔍 **Поиск в базе знаний Pattern Exercise Architect**

**Запрос:** {query}
**Теги:** {', '.join(search_tags)}
**Результаты:** {match_count}

Функция поиска будет активирована после загрузки базы знаний в Archon.

💡 **Рекомендация:** Загрузите файл knowledge/pattern_exercise_architect_knowledge.md в Archon Knowledge Base.
"""

    except Exception as e:
        return f"❌ Ошибка поиска в базе знаний: {e}"


__all__ = [
    "design_transformational_exercise",
    "create_exercise_variants",
    "design_self_check_criteria",
    "adapt_nlp_technique_to_exercise",
    "search_agent_knowledge"
]
