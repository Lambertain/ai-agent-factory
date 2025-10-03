"""
Инструменты для Pattern Feedback Orchestrator Agent
"""

import uuid
from typing import List, Dict, Any, Optional
from pydantic_ai import RunContext

from .dependencies import PatternFeedbackOrchestratorDependencies
from .models import (
    FeedbackQuestion,
    FeedbackForm,
    TriggerRule,
    QuestionType,
    ResponseScaleType,
    FeedbackPurpose,
    TriggerAction,
    CrisisIndicator
)


async def design_feedback_form(
    ctx: RunContext[PatternFeedbackOrchestratorDependencies],
    purpose: str,
    target_module: str,
    duration_minutes: int = 3,
    include_crisis_detection: bool = True
) -> str:
    """
    Спроектировать форму обратной связи.

    Args:
        ctx: Контекст выполнения
        purpose: Цель формы (progress_tracking, satisfaction, engagement, etc.)
        target_module: Целевой модуль
        duration_minutes: Длительность заполнения
        include_crisis_detection: Включить детекцию кризисов

    Returns:
        Описание спроектированной формы
    """

    form_id = f"fb_{uuid.uuid4().hex[:8]}"

    # Определяем количество вопросов исходя из времени
    questions_count = min(duration_minutes * 2, 7)  # ~2 вопроса на минуту, макс 7

    questions = []

    # Базовый вопрос - общая оценка
    questions.append(FeedbackQuestion(
        id=f"q_{uuid.uuid4().hex[:6]}_general",
        question_text=f"Как вы оцениваете {target_module}?",
        question_type=QuestionType.LIKERT_SCALE,
        purpose=FeedbackPurpose(purpose),
        scale_type=ResponseScaleType.SATISFACTION,
        scale_min=1,
        scale_max=5,
        scale_labels={1: "Очень плохо", 3: "Нормально", 5: "Отлично"},
        therapeutic_intent="Осознание своего опыта через оценку"
    ))

    # Вопрос о сложности
    questions.append(FeedbackQuestion(
        id=f"q_{uuid.uuid4().hex[:6]}_difficulty",
        question_text="Насколько сложным было упражнение?",
        question_type=QuestionType.SLIDER,
        purpose=FeedbackPurpose.DIFFICULTY_ASSESSMENT,
        scale_type=ResponseScaleType.DIFFICULTY,
        scale_min=1,
        scale_max=10,
        scale_labels={1: "Очень легко", 5: "Оптимально", 10: "Очень сложно"}
    ))

    # Открытый вопрос для качественных инсайтов
    questions.append(FeedbackQuestion(
        id=f"q_{uuid.uuid4().hex[:6]}_insights",
        question_text="Что было самым ценным для вас?",
        question_type=QuestionType.OPEN_TEXT,
        purpose=FeedbackPurpose(purpose),
        max_length=200,
        therapeutic_intent="Рефлексия через артикуляцию ценности"
    ))

    if include_crisis_detection:
        # Вопрос для детекции кризисных состояний
        questions.append(FeedbackQuestion(
            id=f"q_{uuid.uuid4().hex[:6]}_wellbeing",
            question_text="Как вы себя чувствуете прямо сейчас?",
            question_type=QuestionType.SLIDER,
            purpose=FeedbackPurpose.CRISIS_DETECTION,
            scale_type=ResponseScaleType.NUMERIC,
            scale_min=1,
            scale_max=10,
            scale_labels={1: "Очень плохо", 10: "Отлично"}
        ))

    # Формируем результат
    result = f"""
✅ **Создана форма обратной связи**

**ID:** {form_id}
**Цель:** {purpose}
**Модуль:** {target_module}
**Длительность:** {duration_minutes} минут
**Вопросов:** {len(questions)}

**Структура формы:**
"""

    for i, q in enumerate(questions, 1):
        result += f"\n{i}. {q.question_text} ({q.question_type.value})"

    result += f"\n\n**Детекция кризисов:** {'✅ Включена' if include_crisis_detection else '❌ Выключена'}"

    return result


async def create_trigger_rules(
    ctx: RunContext[PatternFeedbackOrchestratorDependencies],
    form_id: str,
    question_ids: List[str],
    sensitivity: str = "medium"
) -> str:
    """
    Создать триггерные правила для формы.

    Args:
        ctx: Контекст выполнения
        form_id: ID формы
        question_ids: ID вопросов
        sensitivity: Чувствительность триггеров (low/medium/high)

    Returns:
        Описание созданных правил
    """

    rules = []

    # Правило: низкая оценка
    rules.append(TriggerRule(
        rule_id=f"tr_{uuid.uuid4().hex[:6]}_low_satisfaction",
        question_id=question_ids[0] if question_ids else "q_general",
        condition="score <= 2",
        priority=8,
        action=TriggerAction.SEND_SUPPORT_MESSAGE,
        action_params={
            "message_template": "support_low_satisfaction",
            "delay_hours": 2
        },
        description="Отправить поддерживающее сообщение при низкой оценке"
    ))

    # Правило: высокая сложность
    rules.append(TriggerRule(
        rule_id=f"tr_{uuid.uuid4().hex[:6]}_high_difficulty",
        question_id=question_ids[1] if len(question_ids) > 1 else "q_difficulty",
        condition="score >= 8",
        priority=7,
        action=TriggerAction.ADJUST_DIFFICULTY,
        action_params={
            "adjustment": "reduce",
            "percentage": 20
        },
        description="Снизить сложность при высокой оценке сложности"
    ))

    # Правило: кризисное состояние
    if sensitivity in ["medium", "high"]:
        rules.append(TriggerRule(
            rule_id=f"tr_{uuid.uuid4().hex[:6]}_crisis",
            question_id=question_ids[-1] if question_ids else "q_wellbeing",
            condition="score <= 3",
            priority=10,
            action=TriggerAction.ESCALATE_TO_PROFESSIONAL,
            action_params={
                "urgency": "high",
                "notify_team": True,
                "resources": ["crisis_hotline", "emergency_contacts"]
            },
            description="Эскалация при критически низком самочувствии"
        ))

    # Правило: успех и прогресс
    rules.append(TriggerRule(
        rule_id=f"tr_{uuid.uuid4().hex[:6]}_success",
        question_id=question_ids[0] if question_ids else "q_general",
        condition="score >= 4",
        priority=5,
        action=TriggerAction.CELEBRATE_SUCCESS,
        action_params={
            "celebration_type": "personalized",
            "next_step_hint": True
        },
        description="Празднование успеха при высокой оценке"
    ))

    result = f"""
✅ **Создано {len(rules)} триггерных правил**

**Форма:** {form_id}
**Чувствительность:** {sensitivity}

**Правила:**
"""

    for i, rule in enumerate(rules, 1):
        result += f"\n{i}. [{rule.priority}/10] {rule.description}"
        result += f"\n   Условие: {rule.condition} → {rule.action.value}"

    return result


async def detect_crisis_patterns(
    ctx: RunContext[PatternFeedbackOrchestratorDependencies],
    responses: Dict[str, Any],
    threshold: float = 0.7
) -> str:
    """
    Детектировать кризисные паттерны в ответах.

    Args:
        ctx: Контекст выполнения
        responses: Ответы пользователя
        threshold: Порог уверенности для детекции

    Returns:
        Результат детекции кризисных паттернов
    """

    indicators = []

    # Проверка на экстремально низкие оценки
    low_scores = [v for v in responses.values() if isinstance(v, (int, float)) and v <= 3]
    if len(low_scores) >= 2:
        indicators.append(CrisisIndicator(
            indicator_id=f"ci_{uuid.uuid4().hex[:6]}_low_scores",
            severity="medium",
            detection_pattern="Множественные низкие оценки",
            confidence=0.75,
            recommended_actions=[
                "Отправить поддерживающее сообщение",
                "Предложить альтернативные ресурсы",
                "Мониторить следующие ответы"
            ],
            escalation_required=False
        ))

    # Проверка текстовых ответов на ключевые слова риска
    risk_keywords = ["безнадежно", "не вижу смысла", "хочу закончить", "не могу больше"]
    text_responses = [v for v in responses.values() if isinstance(v, str)]

    for text in text_responses:
        if any(keyword in text.lower() for keyword in risk_keywords):
            indicators.append(CrisisIndicator(
                indicator_id=f"ci_{uuid.uuid4().hex[:6]}_keywords",
                severity="high",
                detection_pattern="Ключевые слова риска в текстовых ответах",
                confidence=0.85,
                recommended_actions=[
                    "Немедленная эскалация",
                    "Предоставить контакты кризисной помощи",
                    "Уведомить команду поддержки"
                ],
                escalation_required=True,
                support_resources=[
                    "Телефон доверия: 8-800-2000-122",
                    "Психологическая помощь онлайн"
                ]
            ))

    if not indicators:
        return "✅ Кризисных паттернов не обнаружено. Состояние в пределах нормы."

    result = f"""
⚠️ **Обнаружено {len(indicators)} индикаторов**

**Детали:**
"""

    for i, indicator in enumerate(indicators, 1):
        result += f"\n{i}. **[{indicator.severity.upper()}]** {indicator.detection_pattern}"
        result += f"\n   Уверенность: {indicator.confidence * 100:.0f}%"
        result += f"\n   Эскалация: {'✅ Требуется' if indicator.escalation_required else '❌ Не требуется'}"

        if indicator.recommended_actions:
            result += f"\n   Рекомендуемые действия:"
            for action in indicator.recommended_actions[:2]:
                result += f"\n   - {action}"

    return result


async def generate_actionable_insights(
    ctx: RunContext[PatternFeedbackOrchestratorDependencies],
    feedback_data: Dict[str, Any]
) -> str:
    """
    Генерировать действенные инсайты из обратной связи.

    Args:
        ctx: Контекст выполнения
        feedback_data: Данные обратной связи

    Returns:
        Действенные инсайты и рекомендации
    """

    insights = []

    # Анализ общих паттернов
    avg_satisfaction = feedback_data.get("avg_satisfaction", 0)
    avg_difficulty = feedback_data.get("avg_difficulty", 0)

    if avg_satisfaction < 3.0:
        insights.append({
            "insight": "Низкая удовлетворенность",
            "action": "Пересмотреть содержание модуля",
            "measurable": "Повышение avg_satisfaction до >= 3.5",
            "timeframe": "Следующая итерация"
        })

    if avg_difficulty > 7.0:
        insights.append({
            "insight": "Слишком высокая сложность",
            "action": "Упростить упражнения, добавить промежуточные шаги",
            "measurable": "Снижение avg_difficulty до 5-6",
            "timeframe": "Немедленно"
        })

    if avg_satisfaction >= 4.0 and avg_difficulty <= 6.0:
        insights.append({
            "insight": "Оптимальный баланс",
            "action": "Сохранить текущий подход, масштабировать",
            "measurable": "Поддержание показателей",
            "timeframe": "Ongoing"
        })

    result = f"""
💡 **Сгенерировано {len(insights)} действенных инсайтов**

**Рекомендации:**
"""

    for i, insight in enumerate(insights, 1):
        result += f"\n{i}. **{insight['insight']}**"
        result += f"\n   Действие: {insight['action']}"
        result += f"\n   Метрика: {insight['measurable']}"
        result += f"\n   Срок: {insight['timeframe']}"

    return result


async def search_agent_knowledge(
    ctx: RunContext[PatternFeedbackOrchestratorDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний Pattern Feedback Orchestrator Agent через Archon RAG.

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
🔍 **Поиск в базе знаний Pattern Feedback Orchestrator**

**Запрос:** {query}
**Теги:** {', '.join(search_tags)}
**Результаты:** {match_count}

Функция поиска будет активирована после загрузки базы знаний в Archon.

💡 **Рекомендация:** Загрузите файл knowledge/pattern_feedback_orchestrator_knowledge.md в Archon Knowledge Base.
"""

    except Exception as e:
        return f"❌ Ошибка поиска в базе знаний: {e}"


__all__ = [
    "design_feedback_form",
    "create_trigger_rules",
    "detect_crisis_patterns",
    "generate_actionable_insights",
    "search_agent_knowledge"
]
