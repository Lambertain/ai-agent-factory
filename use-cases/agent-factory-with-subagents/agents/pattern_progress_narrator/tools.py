"""
Инструменты для Pattern Progress Narrator Agent
"""

import uuid
from typing import List, Dict, Any, Optional
from pydantic_ai import RunContext

from .dependencies import PatternProgressNarratorDependencies
from .models import (
    ProgressNarrative,
    NarrativeType,
    EmotionalTone,
    ProgressMetric,
    UserMilestone,
    ChallengeReframe,
    MomentumIndicators,
    HeroJourneyStage,
    TransformationJourneyMap
)


async def create_progress_narrative(
    ctx: RunContext[PatternProgressNarratorDependencies],
    narrative_type: str,
    day_number: int,
    progress_data: Dict[str, Any],
    emotional_tone: str = "motivating"
) -> str:
    """
    Создать нарратив прогресса для пользователя.

    Args:
        ctx: Контекст выполнения
        narrative_type: Тип нарратива (hero_journey, transformation, milestone_celebration, etc.)
        day_number: День программы (1-21)
        progress_data: Данные о прогрессе пользователя
        emotional_tone: Эмоциональный тон сообщения

    Returns:
        Созданный нарратив прогресса
    """

    narrative_id = f"narr_{uuid.uuid4().hex[:8]}"
    user_name = ctx.deps.user_name or "друг"

    # Определяем заголовок и основную структуру на основе типа
    narrative_templates = {
        "hero_journey": {
            "title": f"День {day_number}: Твой путь героя продолжается",
            "opening": f"{user_name}, каждый день твоего путешествия - это новая глава в твоей истории трансформации."
        },
        "transformation": {
            "title": f"Твоя трансформация: День {day_number}",
            "opening": f"Посмотри, {user_name}, как ты меняешься..."
        },
        "milestone_celebration": {
            "title": f"🎉 Поздравляем! День {day_number}",
            "opening": f"{user_name}, сегодня особенный день - ты достиг важной вехи!"
        },
        "overcoming_challenge": {
            "title": f"Преодоление: День {day_number}",
            "opening": f"{user_name}, помнишь как было сложно? А теперь посмотри..."
        },
        "momentum_building": {
            "title": f"Твой импульс растет: День {day_number}",
            "opening": f"Каждый день, {user_name}, ты создаешь силу, которая ведет тебя вперед."
        },
        "reflection": {
            "title": f"Момент рефлексии: День {day_number}",
            "opening": f"Давай остановимся на мгновение, {user_name}, и посмотрим на пройденный путь..."
        }
    }

    template = narrative_templates.get(narrative_type, narrative_templates["transformation"])

    # Извлекаем метрики прогресса
    progress_summary = ""
    if progress_data.get("metrics"):
        improvements = []
        for metric in progress_data["metrics"]:
            if metric.get("improvement_percentage", 0) > 0:
                improvements.append(f"- {metric['metric_name']}: +{metric['improvement_percentage']:.0f}%")

        if improvements:
            progress_summary = "**Твой прогресс в цифрах:**\n" + "\n".join(improvements)

    # Создаем метафору пути героя
    hero_stage = progress_data.get("hero_journey_stage", "crossing_threshold")
    metaphor = ctx.deps.storytelling_db.heros_journey_stages.get(hero_stage, "Твой путь продолжается")

    # Формируем следующий шаг
    next_step = progress_data.get("next_action", f"Продолжай программу Day {day_number + 1}")

    body = f"""
{template['opening']}

{progress_summary}

**Где ты сейчас на пути героя:**
{metaphor}

**Что это значит:**
Ты не просто выполняешь упражнения - ты проходишь трансформационное путешествие. Каждый шаг имеет значение.

**Твой следующий шаг:**
{next_step}

Помни: великие изменения начинаются с малых, но последовательных шагов. Ты на правильном пути! 🌟
"""

    result = f"""
✅ **Создан нарратив прогресса**

**ID:** {narrative_id}
**Тип:** {narrative_type}
**День:** {day_number}
**Тон:** {emotional_tone}

**Заголовок:** {template['title']}

**Контент:**
{body}
"""

    return result


async def reframe_challenge(
    ctx: RunContext[PatternProgressNarratorDependencies],
    challenge_description: str,
    context: Dict[str, Any] = None
) -> str:
    """
    Рефреймировать вызов/неудачу в возможность научения.

    Args:
        ctx: Контекст выполнения
        challenge_description: Описание вызова или неудачи
        context: Дополнительный контекст

    Returns:
        Рефреймированное описание с извлеченным научением
    """

    reframe_id = f"ref_{uuid.uuid4().hex[:6]}"

    # Применяем формулу рефрейминга
    reframing_steps = {
        "acknowledge": f"Я понимаю, что {challenge_description.lower()} было непросто.",
        "normalize": "Это нормальная часть процесса трансформации. Сопротивление - сигнал роста.",
        "extract_learning": "Из этого опыта ты узнал важное о себе: свои границы, триггеры, и то, что нужно адаптировать.",
        "identify_growth": "Теперь у тебя есть информация, которая поможет двигаться дальше более осознанно.",
        "next_action": "Следующий шаг: попробуем адаптированную версию или другой подход."
    }

    result = f"""
🔄 **Рефрейминг вызова**

**ID:** {reframe_id}
**Оригинал:** {challenge_description}

**Рефреймированная перспектива:**

1. **Признание:** {reframing_steps['acknowledge']}

2. **Нормализация:** {reframing_steps['normalize']}

3. **Извлечение научения:** {reframing_steps['extract_learning']}

4. **Идентификация роста:** {reframing_steps['identify_growth']}

5. **Следующее действие:** {reframing_steps['next_action']}

**Новый фрейм:**
"{challenge_description}" → "Возможность научиться и адаптироваться"

💡 **Помни:** Каждый вызов - это учитель. Неудачи не существует, есть только feedback.
"""

    return result


async def generate_momentum_message(
    ctx: RunContext[PatternProgressNarratorDependencies],
    momentum_data: Dict[str, Any]
) -> str:
    """
    Сгенерировать сообщение для поддержания импульса прогресса.

    Args:
        ctx: Контекст выполнения
        momentum_data: Данные об импульсе (consistency, engagement, completion)

    Returns:
        Сообщение для поддержания импульса
    """

    consistency_score = momentum_data.get("consistency_score", 0.5)
    engagement_level = momentum_data.get("engagement_level", 0.5)
    completion_rate = momentum_data.get("completion_rate", 0.5)

    # Определяем уровень импульса
    momentum_level = (consistency_score + engagement_level + completion_rate) / 3

    if momentum_level >= 0.8:
        message_type = "high_momentum"
        emoji = "🚀"
        tone = "celebratory"
    elif momentum_level >= 0.6:
        message_type = "good_momentum"
        emoji = "✨"
        tone = "encouraging"
    elif momentum_level >= 0.4:
        message_type = "building_momentum"
        emoji = "🌱"
        tone = "supportive"
    else:
        message_type = "need_boost"
        emoji = "💪"
        tone = "motivating"

    messages = {
        "high_momentum": {
            "title": f"{emoji} Твой импульс невероятен!",
            "body": f"""
Ты в потрясающей форме! Consistency: {consistency_score * 100:.0f}%, engagement: {engagement_level * 100:.0f}%.

Это то, что называется momentum - сила, которая делает каждый следующий шаг легче предыдущего.

**Что происходит:**
- Твой мозг формирует новые нейронные пути
- Привычки становятся автоматическими
- Мотивация растет from doing, не наоборот

**Продолжай:**
Просто не останавливайся. Сейчас momentum работает на тебя.
"""
        },
        "good_momentum": {
            "title": f"{emoji} Отличный прогресс!",
            "body": f"""
У тебя стабильный momentum: consistency {consistency_score * 100:.0f}%.

**Ты на правильном пути:**
Регулярность важнее интенсивности. Ты делаешь именно то, что нужно.

**Чтобы усилить momentum:**
- Продолжай показывать up каждый день
- Celebrate малые победы
- Трек свой прогресс

Ты создаешь что-то устойчивое! ✨
"""
        },
        "building_momentum": {
            "title": f"{emoji} Momentum начинает расти",
            "body": f"""
Ты закладываешь фундамент: {consistency_score * 100:.0f}% consistency.

**Это нормально:**
Начало всегда требует больше effort. Momentum еще не набран, но ты движешься в правильном направлении.

**Фокус на:**
- Показывать up, даже когда трудно
- Малые consistent actions
- Один день за раз

Скоро станет легче - обещаю! 🌱
"""
        },
        "need_boost": {
            "title": f"{emoji} Время перезапустить momentum",
            "body": f"""
Я вижу, было challenging последнее время (consistency: {consistency_score * 100:.0f}%).

**Хорошие новости:**
Momentum можно восстановить. Всё, что нужно - начать again.

**Твой план:**
1. Выбери самое простое упражнение
2. Сделай его сегодня
3. Повтори завтра
4. Momentum вернется

Ты не начинаешь с нуля - весь опыт с тобой. Просто следующий шаг. 💪
"""
        }
    }

    selected_message = messages[message_type]

    result = f"""
{selected_message['title']}

{selected_message['body']}

**Твои показатели momentum:**
- Consistency: {consistency_score * 100:.0f}%
- Engagement: {engagement_level * 100:.0f}%
- Completion: {completion_rate * 100:.0f}%

Momentum level: {momentum_level * 100:.0f}% - {"Отлично!" if momentum_level >= 0.7 else "Растет!" if momentum_level >= 0.5 else "В процессе построения"}
"""

    return result


async def create_anticipation_builder(
    ctx: RunContext[PatternProgressNarratorDependencies],
    current_day: int,
    upcoming_content: Dict[str, Any]
) -> str:
    """
    Создать сообщение, создающее предвкушение следующих этапов.

    Args:
        ctx: Контекст выполнения
        current_day: Текущий день программы
        upcoming_content: Информация о предстоящем контенте

    Returns:
        Сообщение, создающее anticipation
    """

    next_day = current_day + 1
    days_remaining = 21 - current_day

    # Определяем ключевые вехи впереди
    milestones_ahead = []
    if next_day == 7:
        milestones_ahead.append("Завершение первой недели - первая важная веха")
    if next_day == 14:
        milestones_ahead.append("Середина программы - время глубокой трансформации")
    if next_day == 21:
        milestones_ahead.append("Финал программы - интеграция всех изменений")

    upcoming_module = upcoming_content.get("module_name", f"Day {next_day} Module")
    upcoming_technique = upcoming_content.get("technique", "новая мощная техника")

    result = f"""
🔮 **Что тебя ждет впереди**

**Следующий шаг: Day {next_day}**
{upcoming_module}

**Почему это важно:**
Ты будешь работать с {upcoming_technique} - это следующий естественный шаг после того, что ты уже освоил.

**Предвкушение:**
{"🎯 " + milestones_ahead[0] if milestones_ahead else "Каждый день открывает новые возможности"}

**Еще впереди:**
- {days_remaining} дней трансформационного путешествия
- Новые навыки и инсайты
- Растущая осознанность и сила
- Версия себя, о которой ты пока только мечтаешь

**Интрига:**
То, что ты узнаешь в ближайшие дни, изменит твое понимание... но я не буду спойлерить. Ты увидишь сам 😊

**Твой следующий move:**
Просто открой Day {next_day}, когда будешь готов. Momentum тебя понесет.

✨ Лучшее еще впереди!
"""

    return result


async def search_agent_knowledge(
    ctx: RunContext[PatternProgressNarratorDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний Pattern Progress Narrator Agent через Archon RAG.

    Args:
        ctx: Контекст выполнения
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """

    search_tags = ctx.deps.knowledge_tags

    try:
        return f"""
🔍 **Поиск в базе знаний Pattern Progress Narrator**

**Запрос:** {query}
**Теги:** {', '.join(search_tags)}
**Результаты:** {match_count}

Функция поиска будет активирована после загрузки базы знаний в Archon.

💡 **Рекомендация:** Загрузите файл knowledge/pattern_progress_narrator_knowledge.md в Archon Knowledge Base.
"""

    except Exception as e:
        return f"❌ Ошибка поиска в базе знаний: {e}"


__all__ = [
    "create_progress_narrative",
    "reframe_challenge",
    "generate_momentum_message",
    "create_anticipation_builder",
    "search_agent_knowledge"
]
