"""
Инструменты для Pattern Safety Protocol Agent
"""

import uuid
from typing import List, Dict, Any, Optional
from pydantic_ai import RunContext

from .dependencies import PatternSafetyProtocolDependencies
from .models import (
    RiskAssessment,
    RiskLevel,
    RiskCategory,
    Contraindication,
    ContraindicationType,
    EscalationAction,
    SafetyCheckResult,
    CrisisIndicator,
    SafetyProtocol
)


async def assess_user_risk(
    ctx: RunContext[PatternSafetyProtocolDependencies],
    user_data: Dict[str, Any],
    data_sources: List[str] = None
) -> str:
    """
    Оценить уровень риска для пользователя на основе предоставленных данных.

    Args:
        ctx: Контекст выполнения
        user_data: Данные пользователя (feedback, behavior, responses)
        data_sources: Источники данных для оценки

    Returns:
        Строка с оценкой риска и рекомендациями
    """

    assessment_id = f"risk_{uuid.uuid4().hex[:8]}"

    # Анализируем данные на наличие индикаторов риска
    risk_indicators_db = ctx.deps.risk_indicators_db

    detected_risks = []
    risk_level = RiskLevel.MINIMAL
    recommended_actions = []

    # Проверка суицидальных индикаторов
    user_text = " ".join([
        str(user_data.get("feedback", "")),
        str(user_data.get("responses", "")),
        str(user_data.get("notes", ""))
    ]).lower()

    suicidal_count = sum(
        1 for indicator in risk_indicators_db.suicidal_indicators
        if any(keyword in user_text for keyword in indicator.lower().split())
    )

    if suicidal_count >= 3:
        detected_risks.append(RiskCategory.SUICIDAL)
        risk_level = RiskLevel.CRITICAL
        recommended_actions.extend([
            EscalationAction.IMMEDIATE_REFERRAL,
            EscalationAction.CRISIS_RESOURCES,
            EscalationAction.EMERGENCY_PROTOCOL
        ])
    elif suicidal_count >= 1:
        detected_risks.append(RiskCategory.SUICIDAL)
        risk_level = RiskLevel.HIGH if risk_level == RiskLevel.MINIMAL else risk_level
        recommended_actions.extend([
            EscalationAction.CRISIS_RESOURCES,
            EscalationAction.MONITOR_CLOSELY
        ])

    # Проверка признаков кризиса
    crisis_count = sum(
        1 for indicator in risk_indicators_db.crisis_indicators
        if any(keyword in user_text for keyword in indicator.lower().split())
    )

    if crisis_count >= 2:
        detected_risks.append(RiskCategory.CRISIS)
        if risk_level in [RiskLevel.MINIMAL, RiskLevel.LOW]:
            risk_level = RiskLevel.HIGH

        recommended_actions.extend([
            EscalationAction.PAUSE_PROGRAM,
            EscalationAction.CRISIS_RESOURCES
        ])

    # Проверка индикаторов самоповреждения
    self_harm_count = sum(
        1 for indicator in risk_indicators_db.self_harm_indicators
        if any(keyword in user_text for keyword in indicator.lower().split())
    )

    if self_harm_count >= 1:
        detected_risks.append(RiskCategory.SELF_HARM)
        if risk_level in [RiskLevel.MINIMAL, RiskLevel.LOW]:
            risk_level = RiskLevel.MODERATE

        recommended_actions.append(EscalationAction.MONITOR_CLOSELY)

    # Если не обнаружено высоких рисков
    if not detected_risks:
        risk_level = RiskLevel.LOW
        explanation = "Оценка не выявила значительных индикаторов риска. Пользователь может продолжать программу с обычным мониторингом."
    else:
        explanation = f"Обнаружены индикаторы риска: {', '.join([r.value for r in detected_risks])}. Требуются меры безопасности."

    # Формируем результат
    result = f"""
✅ **Оценка риска завершена**

**ID оценки:** {assessment_id}
**Уровень риска:** {risk_level.value.upper()}
**Категории рисков:** {', '.join([r.value for r in detected_risks]) if detected_risks else 'Не обнаружено'}

**Объяснение:**
{explanation}

**Рекомендуемые действия:**
{chr(10).join([f"- {action.value}" for action in set(recommended_actions)]) if recommended_actions else "- Продолжить обычный мониторинг"}

**Источники данных:** {', '.join(data_sources) if data_sources else 'user_data'}
"""

    return result


async def check_technique_contraindications(
    ctx: RunContext[PatternSafetyProtocolDependencies],
    technique_name: str,
    user_conditions: List[str]
) -> str:
    """
    Проверить противопоказания для психологической техники.

    Args:
        ctx: Контекст выполнения
        technique_name: Название техники (hypnosis, breathwork, visualization, etc.)
        user_conditions: Медицинские/психологические состояния пользователя

    Returns:
        Информация о противопоказаниях и рекомендации
    """

    contraindications_db = ctx.deps.contraindications_db

    # Нормализуем название техники
    technique_key = technique_name.lower().replace(" ", "_")

    # Проверяем абсолютные противопоказания
    absolute_contraindications = []
    if technique_key in contraindications_db.absolute_contraindications:
        for condition in contraindications_db.absolute_contraindications[technique_key]:
            if any(user_cond.lower() in condition.lower() for user_cond in user_conditions):
                absolute_contraindications.append(condition)

    # Проверяем относительные противопоказания
    relative_contraindications = []
    if technique_key in contraindications_db.relative_contraindications:
        for condition in contraindications_db.relative_contraindications[technique_key]:
            if any(user_cond.lower() in condition.lower() for user_cond in user_conditions):
                relative_contraindications.append(condition)

    # Проверяем временные противопоказания
    temporary_contraindications = [
        cond for cond in contraindications_db.temporary_contraindications
        if any(user_cond.lower() in cond.lower() for user_cond in user_conditions)
    ]

    # Формируем результат
    if absolute_contraindications:
        recommendation = f"⛔ **ТЕХНИКА ПРОТИВОПОКАЗАНА** - обнаружены абсолютные противопоказания. Использовать альтернативную технику."
        safe_to_use = False
    elif relative_contraindications:
        recommendation = f"⚠️ **ТРЕБУЕТСЯ АДАПТАЦИЯ** - обнаружены относительные противопоказания. Техника может использоваться с модификациями."
        safe_to_use = True
    elif temporary_contraindications:
        recommendation = f"⏸️ **ВРЕМЕННО ПРОТИВОПОКАЗАНО** - дождитесь стабилизации состояния перед использованием техники."
        safe_to_use = False
    else:
        recommendation = f"✅ **БЕЗОПАСНО** - противопоказания не обнаружены. Техника может использоваться."
        safe_to_use = True

    result = f"""
🔍 **Проверка противопоказаний для техники "{technique_name}"**

**Состояния пользователя:** {', '.join(user_conditions)}

**Абсолютные противопоказания:**
{chr(10).join([f"- {c}" for c in absolute_contraindications]) if absolute_contraindications else "Не обнаружено"}

**Относительные противопоказания (требуют адаптации):**
{chr(10).join([f"- {c}" for c in relative_contraindications]) if relative_contraindications else "Не обнаружено"}

**Временные противопоказания:**
{chr(10).join([f"- {c}" for c in temporary_contraindications]) if temporary_contraindications else "Не обнаружено"}

{recommendation}

**Можно использовать технику:** {'Да' if safe_to_use else 'Нет'}
"""

    return result


async def check_pharmacological_interactions(
    ctx: RunContext[PatternSafetyProtocolDependencies],
    medications: List[str],
    planned_techniques: List[str]
) -> str:
    """
    Проверить фармакологические взаимодействия с психотехниками.

    Args:
        ctx: Контекст выполнения
        medications: Список принимаемых медикаментов
        planned_techniques: Планируемые техники

    Returns:
        Информация о взаимодействиях и рекомендации
    """

    pharmacological_db = ctx.deps.pharmacological_interactions_db
    detected_interactions = []

    # Проверяем каждый класс медикаментов
    for med_class, med_data in pharmacological_db.medication_interactions.items():
        for med_type, details in med_data.items():
            # Проверяем, принимает ли пользователь медикаменты из этого класса
            user_takes_medication = any(
                any(med.lower() in user_med.lower() for user_med in medications)
                for med in details.get("medications", [])
            )

            if user_takes_medication:
                # Проверяем взаимодействия с планируемыми техниками
                for interaction in details.get("interactions", []):
                    technique = interaction.get("technique", "")
                    if any(planned_tech.lower() in technique.lower() for planned_tech in planned_techniques):
                        detected_interactions.append({
                            "medication_class": f"{med_class} - {med_type}",
                            "technique": technique,
                            "risk": interaction.get("risk", "unknown"),
                            "description": interaction.get("description", ""),
                            "recommendation": interaction.get("recommendation", "")
                        })

    # Формируем результат
    if not detected_interactions:
        result = f"""
✅ **Фармакологические взаимодействия не обнаружены**

**Медикаменты:** {', '.join(medications)}
**Планируемые техники:** {', '.join(planned_techniques)}

Нет значимых взаимодействий между принимаемыми медикаментами и планируемыми психотехниками.

**Рекомендация:** Техники могут использоваться в обычном режиме.
"""
    else:
        interactions_text = []
        for interaction in detected_interactions:
            risk_emoji = {
                "high": "🔴",
                "moderate": "🟡",
                "low": "🟢"
            }.get(interaction["risk"], "⚪")

            interactions_text.append(f"""
{risk_emoji} **{interaction['medication_class']}** ↔ **{interaction['technique']}**
- Риск: {interaction['risk']}
- Описание: {interaction['description']}
- Рекомендация: {interaction['recommendation']}
""")

        result = f"""
⚠️ **Обнаружены фармакологические взаимодействия**

**Медикаменты:** {', '.join(medications)}
**Планируемые техники:** {', '.join(planned_techniques)}

**Взаимодействия:**
{''.join(interactions_text)}

**Важно:** Проконсультируйтесь с лечащим врачом перед использованием этих техник.
"""

    return result


async def generate_crisis_response(
    ctx: RunContext[PatternSafetyProtocolDependencies],
    risk_category: str,
    severity: str = "high"
) -> str:
    """
    Сгенерировать протокол ответа на кризисную ситуацию.

    Args:
        ctx: Контекст выполнения
        risk_category: Категория риска (suicidal, self_harm, crisis, trauma_trigger)
        severity: Уровень серьезности (low, moderate, high, critical)

    Returns:
        Протокол ответа с кризисными ресурсами
    """

    crisis_resources = ctx.deps.crisis_resources

    protocol_id = f"protocol_{uuid.uuid4().hex[:6]}"

    # Формируем ответ в зависимости от категории риска
    if risk_category == "suicidal":
        communication_script = """
Я вижу, что вам сейчас очень тяжело. Это важный момент - вы обратились за помощью.

**Пожалуйста, знайте:**
- То, что вы чувствуете сейчас, временно, даже если кажется вечным
- Есть профессиональная помощь, которая может облегчить вашу боль
- Вы не одиноки в этом - многие прошли через подобное и нашли выход

**Немедленные действия:**
1. Если есть immediate danger - звоните 112 или 103
2. Позвоните на круглосуточный телефон доверия
3. Обратитесь к близкому человеку прямо сейчас
4. Уберите средства самоповреждения из доступа
"""

        resources = crisis_resources.crisis_hotlines["russia"] + [
            {
                "name": "Скорая помощь",
                "phone": crisis_resources.emergency_services["medical_emergency"],
                "available": "24/7",
                "description": "Экстренная медицинская помощь"
            }
        ]

    elif risk_category == "self_harm":
        communication_script = """
Я понимаю, что самоповреждение может казаться способом справиться с болью. Но есть более безопасные альтернативы.

**Вместо самоповреждения попробуйте:**
- Сжать кусочек льда в руке
- Резко хлопнуть резинкой по запястью
- Интенсивную физическую активность
- Написать о чувствах или порвать бумагу

**Если не можете остановиться:**
1. Позвоните на телефон доверия для поддержки
2. Обратитесь к терапевту или психиатру
3. Рассмотрите госпитализацию при высоком риске
"""

        resources = crisis_resources.crisis_hotlines["russia"]

    elif risk_category == "crisis":
        communication_script = """
Вы переживаете острый кризис. Это нормальная реакция на экстремальный стресс.

**Сейчас важно:**
1. Обеспечить безопасность (физическую и психологическую)
2. Получить немедленную поддержку
3. Не оставаться в одиночестве
4. Отложить важные решения

**Кризис временный** - с профессиональной помощью вы пройдете через это.
"""

        resources = crisis_resources.crisis_hotlines["russia"] + crisis_resources.online_resources

    else:  # trauma_trigger или другие
        communication_script = """
Вы испытали триггер травмы. Это не ваша вина, и это проходит.

**Техники grounding (здесь и сейчас):**
1. 5-4-3-2-1: Назовите 5 вещей, которые видите, 4 - которые слышите, 3 - которые чувствуете, 2 - которые нюхаете, 1 - которую пробуете
2. Физический контакт с землей: почувствуйте ноги на полу
3. Холодная вода на лицо или руки
4. Медленное дыхание: 4 счета вдох, 4 задержка, 4 выдох

**Если не помогает** - обратитесь к травма-терапевту.
"""

        resources = crisis_resources.online_resources

    # Форматируем ресурсы
    resources_text = []
    for resource in resources:
        if "phone" in resource:
            resources_text.append(f"**{resource['name']}**\nТелефон: {resource['phone']}\nДоступность: {resource['available']}\n{resource['description']}")
        else:
            resources_text.append(f"**{resource['name']}**\n{resource.get('url', resource.get('website', ''))}\n{resource['description']}")

    result = f"""
🚨 **ПРОТОКОЛ КРИЗИСНОГО РЕАГИРОВАНИЯ**

**ID протокола:** {protocol_id}
**Категория:** {risk_category}
**Уровень серьезности:** {severity}

---

{communication_script}

---

**📞 РЕСУРСЫ ПОМОЩИ:**

{chr(10).join(resources_text)}

---

**⚠️ ВАЖНО:**
- Эта программа НЕ заменяет профессиональную помощь
- При кризисе обращайтесь к специалистам
- Сохраните эти контакты для быстрого доступа
"""

    return result


async def assess_vulnerable_group(
    ctx: RunContext[PatternSafetyProtocolDependencies],
    user_profile: Dict[str, Any]
) -> str:
    """
    Оценить принадлежность пользователя к уязвимой группе и дать рекомендации.

    Args:
        ctx: Контекст выполнения
        user_profile: Профиль пользователя (age, conditions, life_stage, etc.)

    Returns:
        Рекомендации по адаптации программы
    """

    vulnerable_groups_db = ctx.deps.vulnerable_groups_db
    identified_groups = []

    age = user_profile.get("age")
    conditions = user_profile.get("conditions", [])
    life_stage = user_profile.get("life_stage", "")

    # Проверка возрастных групп
    if age and age < 18:
        identified_groups.append("children_adolescents")
    elif age and age > 65:
        identified_groups.append("elderly")

    # Проверка беременности/послеродового периода
    if life_stage and ("pregnant" in life_stage.lower() or "postpartum" in life_stage.lower()):
        identified_groups.append("pregnancy_postpartum")

    # Проверка выживших после травмы
    trauma_keywords = ["ptsd", "травма", "trauma", "abuse", "насилие"]
    if any(keyword in " ".join(conditions).lower() for keyword in trauma_keywords):
        identified_groups.append("trauma_survivors")

    # Если не входит в уязвимые группы
    if not identified_groups:
        return """
✅ **Оценка уязвимости**

Пользователь не входит в специальные уязвимые группы.
Программа может использоваться в стандартном режиме с обычным мониторингом.

**Рекомендации:**
- Регулярный мониторинг прогресса
- Стандартные протоколы безопасности
- Обратная связь после каждого модуля
"""

    # Формируем рекомендации для каждой группы
    recommendations_text = []
    for group in identified_groups:
        group_data = vulnerable_groups_db.vulnerable_groups.get(group, {})

        recommendations_text.append(f"""
### {group_data.get('age_range', group).upper()}

**Факторы уязвимости:**
{chr(10).join([f"- {v}" for v in group_data.get('vulnerabilities', [])])}

**Необходимые модификации:**
{chr(10).join([f"- {m}" for m in group_data.get('modifications', [])])}

**Красные флаги (мониторить):**
{chr(10).join([f"- {f}" for f in group_data.get('red_flags', [])])}
""")

    result = f"""
⚠️ **ОЦЕНКА УЯЗВИМОЙ ГРУППЫ**

**Профиль пользователя:**
- Возраст: {age if age else 'Не указан'}
- Состояния: {', '.join(conditions) if conditions else 'Не указаны'}
- Жизненный этап: {life_stage if life_stage else 'Не указан'}

**Идентифицированные уязвимые группы:** {', '.join(identified_groups)}

---

{''.join(recommendations_text)}

---

**🔒 ОБЩИЕ РЕКОМЕНДАЦИИ ПО БЕЗОПАСНОСТИ:**
1. Усиленный мониторинг прогресса
2. Адаптация интенсивности и сложности модулей
3. Более частая обратная связь
4. Готовность к эскалации помощи при необходимости
5. Trauma-informed подход ко всем интервенциям
"""

    return result


async def search_agent_knowledge(
    ctx: RunContext[PatternSafetyProtocolDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний Pattern Safety Protocol Agent через Archon RAG.

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
🔍 **Поиск в базе знаний Pattern Safety Protocol**

**Запрос:** {query}
**Теги:** {', '.join(search_tags)}
**Результаты:** {match_count}

Функция поиска будет активирована после загрузки базы знаний в Archon.

💡 **Рекомендация:** Загрузите файл knowledge/pattern_safety_protocol_knowledge.md в Archon Knowledge Base.
"""

    except Exception as e:
        return f"❌ Ошибка поиска в базе знаний: {e}"


__all__ = [
    "assess_user_risk",
    "check_technique_contraindications",
    "check_pharmacological_interactions",
    "generate_crisis_response",
    "assess_vulnerable_group",
    "search_agent_knowledge"
]
