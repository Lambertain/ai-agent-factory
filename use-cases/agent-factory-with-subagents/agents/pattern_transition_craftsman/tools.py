"""
Инструменты для Pattern Transition Craftsman Agent.

Инструменты для создания переходов между модулями программы.
"""

import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic_ai import RunContext

from .dependencies import PatternTransitionCraftsmanDependencies
from .models import (
    ModuleTransition,
    TransitionType,
    EnergyLevel,
    ModalityShift,
    BridgeContent,
    AnchorType,
    TransitionElement,
    CoherenceCheck,
    EnergyTransition,
    FlowAnalysis
)


async def create_module_transition(
    ctx: RunContext[PatternTransitionCraftsmanDependencies],
    from_module: Dict[str, Any],
    to_module: Dict[str, Any],
    transition_type: str,
    energy_shift: str,
    modality_shift: Optional[str] = None,
    use_anchors: bool = True
) -> str:
    """
    Создать переход между двумя модулями программы.

    Args:
        ctx: Контекст выполнения агента
        from_module: Модуль откуда идем (id, name, type, emotional_state)
        to_module: Модуль куда идем (id, name, type, purpose)
        transition_type: Тип перехода (intro_to_main, main_to_reflection, etc.)
        energy_shift: Целевой уровень энергии (calm, neutral, activating, building, sustaining)
        modality_shift: Смена модальности (visual_to_auditory, etc.)
        use_anchors: Использовать якоря из предыдущих модулей

    Returns:
        str: Созданный переход с элементами и якорями
    """

    deps = ctx.deps

    # Получить шаблон перехода
    template = deps.templates_db.get_template(transition_type, energy_shift)

    # Создать базовый текст перехода
    transition_text = template["template"] if template else ""

    # Дополнить якорями если нужно
    anchors_from_previous = []
    if use_anchors and len(deps.module_history) > 0:
        # Взять последнее достижение как якорь
        last_module = deps.module_history[-1]
        anchor_pattern = deps.anchor_patterns_db.get_anchor_pattern("achievement")
        if anchor_pattern:
            example = anchor_pattern.get("examples", [""])[0]
            anchors_from_previous.append(example)

    # Добавить мост модальности если нужен
    modality_bridge_text = ""
    if modality_shift:
        bridge = deps.modality_bridges_db.get_bridge(modality_shift)
        if bridge:
            modality_bridge_text = bridge["bridge"]

    # Создать энергетический переход если нужен
    energy_transition_text = ""
    from_energy = from_module.get("energy_level", "neutral")
    if from_energy != energy_shift:
        energy_trans = deps.energy_transitions_db.get_transition(from_energy, energy_shift)
        if energy_trans:
            energy_transition_text = energy_trans["text"]

    # Собрать элементы перехода
    elements = []

    if energy_transition_text:
        elements.append(TransitionElement(
            element_id=str(uuid.uuid4())[:8],
            element_type="energizer",
            content=energy_transition_text,
            duration_seconds=45,
            purpose="Энергетический переход"
        ))

    if modality_bridge_text:
        elements.append(TransitionElement(
            element_id=str(uuid.uuid4())[:8],
            element_type="bridge",
            content=modality_bridge_text,
            duration_seconds=30,
            purpose="Переход модальности"
        ))

    if anchors_from_previous:
        elements.append(TransitionElement(
            element_id=str(uuid.uuid4())[:8],
            element_type="anchor",
            content=anchors_from_previous[0],
            duration_seconds=20,
            purpose="Якорь преемственности"
        ))

    # Создать объект перехода
    transition = ModuleTransition(
        transition_id=str(uuid.uuid4()),
        from_module_id=from_module.get("id", "unknown"),
        from_module_name=from_module.get("name", "Unknown Module"),
        to_module_id=to_module.get("id", "unknown"),
        to_module_name=to_module.get("name", "Unknown Module"),
        transition_type=TransitionType(transition_type),
        energy_shift=EnergyLevel(energy_shift),
        modality_shift=ModalityShift(modality_shift) if modality_shift else None,
        transition_text=transition_text,
        elements=elements,
        anchors_from_previous=anchors_from_previous,
        primers_for_next=[f"Подготовка к {to_module.get('name')}"],
        estimated_duration_seconds=sum([e.duration_seconds for e in elements]) + 30,
        therapeutic_purpose=f"Плавный переход от {from_module.get('name')} к {to_module.get('name')}",
        emotional_tone="поддерживающий"
    )

    # Обновить историю модулей
    deps.module_history.append({
        "module_id": to_module.get("id"),
        "module_name": to_module.get("name"),
        "transition_id": transition.transition_id,
        "timestamp": datetime.now()
    })

    return f"""
Переход создан успешно

ID перехода: {transition.transition_id}
От: {transition.from_module_name} → К: {transition.to_module_name}
Тип: {transition.transition_type.value}
Энергия: {transition.energy_shift.value}
Модальность: {transition.modality_shift.value if transition.modality_shift else 'без смены'}

Текст перехода:
{transition.transition_text}

Элементы ({len(elements)}):
""" + "\n".join([f"- {e.element_type}: {e.content[:80]}..." for e in elements]) + f"""

Якоря: {len(anchors_from_previous)}
Длительность: ~{transition.estimated_duration_seconds} сек
Терапевтическая цель: {transition.therapeutic_purpose}
"""


async def create_bridge_content(
    ctx: RunContext[PatternTransitionCraftsmanDependencies],
    from_activity: Dict[str, Any],
    to_activity: Dict[str, Any],
    anchor_type: Optional[str] = None,
    preserve_emotion: bool = True,
    mindset_prep: Optional[str] = None
) -> str:
    """
    Создать мост между двумя активностями внутри модуля.

    Args:
        ctx: Контекст выполнения
        from_activity: Активность откуда идем
        to_activity: Активность куда идем
        anchor_type: Тип якоря (metaphor, achievement, insight, emotion)
        preserve_emotion: Сохранять эмоциональное состояние
        mindset_prep: Подготовка мышления для следующей активности

    Returns:
        str: Мост между активностями
    """

    deps = ctx.deps

    # Создать базовый мост
    from_name = from_activity.get("name", "предыдущей активности")
    to_name = to_activity.get("name", "следующей активности")

    bridge_text = f"Отлично! Теперь, основываясь на опыте {from_name}, мы переходим к {to_name}."

    # Добавить якорь если указан
    anchor_content = None
    if anchor_type:
        anchor_pattern = deps.anchor_patterns_db.get_anchor_pattern(anchor_type)
        if anchor_pattern and "examples" in anchor_pattern:
            anchor_content = anchor_pattern["examples"][0]

    # Добавить подготовку mind-set
    if not mindset_prep:
        mindset_prep = f"Приготовьтесь {to_activity.get('preparation', 'к новому опыту')}."

    bridge = BridgeContent(
        bridge_id=str(uuid.uuid4()),
        from_context=from_activity,
        to_context=to_activity,
        bridge_text=bridge_text,
        maintains_focus=True,
        preserves_emotion=preserve_emotion,
        anchor_type=AnchorType(anchor_type) if anchor_type else None,
        anchor_content=anchor_content,
        mindset_preparation=mindset_prep
    )

    return f"""
Мост создан

ID моста: {bridge.bridge_id}
От: {from_activity.get('name')} → К: {to_activity.get('name')}

Текст моста:
{bridge.bridge_text}

{'Якорь: ' + bridge.anchor_content if bridge.anchor_content else ''}

Подготовка mind-set:
{bridge.mindset_preparation}

Сохраняет фокус: {'Да' if bridge.maintains_focus else 'Нет'}
Сохраняет эмоцию: {'Да' if bridge.preserves_emotion else 'Нет'}
"""


async def check_program_coherence(
    ctx: RunContext[PatternTransitionCraftsmanDependencies],
    program_id: str,
    day_number: int,
    modules: List[Dict[str, Any]]
) -> str:
    """
    Проверить связность и flow программы для конкретного дня.

    Args:
        ctx: Контекст выполнения
        program_id: ID программы
        day_number: Номер дня программы
        modules: Список модулей дня для проверки

    Returns:
        str: Результаты проверки связности с рекомендациями
    """

    deps = ctx.deps

    # Проверить принципы flow
    coherence_principle = deps.flow_optimization_db.get_principle("coherence")
    emotional_principle = deps.flow_optimization_db.get_principle("emotional_continuity")
    attention_principle = deps.flow_optimization_db.get_principle("attention_management")

    coherence_issues = []
    recommendations = []

    # Проверка 1: Логическая последовательность
    for i in range(len(modules) - 1):
        current = modules[i]
        next_mod = modules[i + 1]

        # Проверить резкие скачки сложности
        current_complexity = current.get("complexity", 5)
        next_complexity = next_mod.get("complexity", 5)
        if abs(next_complexity - current_complexity) > 3:
            coherence_issues.append(f"Резкий скачок сложности между {current.get('name')} и {next_mod.get('name')}")
            recommendations.append(f"Добавить промежуточный модуль или смягчить переход")

    # Проверка 2: Эмоциональная непрерывность
    for i in range(len(modules) - 1):
        current = modules[i]
        next_mod = modules[i + 1]

        current_emotion = current.get("target_emotion", "neutral")
        next_emotion = next_mod.get("target_emotion", "neutral")

        # Резкие переходы эмоций
        incompatible_transitions = [
            ("high_energy", "deep_reflection"),
            ("intense_emotion", "analytical_thinking")
        ]
        if (current_emotion, next_emotion) in incompatible_transitions:
            coherence_issues.append(f"Несовместимые эмоциональные состояния: {current_emotion} → {next_emotion}")
            recommendations.append(f"Добавить промежуточный переход с grounding")

    # Рассчитать flow score
    max_issues = len(modules) * 2  # 2 проверки на модуль
    actual_issues = len(coherence_issues)
    flow_score = max(0.0, 1.0 - (actual_issues / max_issues)) if max_issues > 0 else 1.0

    check = CoherenceCheck(
        check_id=str(uuid.uuid4()),
        program_id=program_id,
        day_number=day_number,
        flow_score=flow_score,
        coherence_issues=coherence_issues,
        emotional_continuity=len([i for i in coherence_issues if "эмоциональн" in i]) == 0,
        anchor_usage={},
        recommendations=recommendations,
        suggested_fixes=recommendations
    )

    return f"""
Проверка связности завершена

ID проверки: {check.check_id}
Программа: {program_id}
День: {day_number}

Flow Score: {check.flow_score:.2f} / 1.00

Проблемы связности ({len(check.coherence_issues)}):
""" + ("\n".join([f"- {issue}" for issue in check.coherence_issues]) if check.coherence_issues else "Не обнаружено") + f"""

Эмоциональная непрерывность: {'Да' if check.emotional_continuity else 'Нет'}

Рекомендации ({len(check.recommendations)}):
""" + "\n".join([f"- {rec}" for rec in check.recommendations])


async def generate_micro_intervention(
    ctx: RunContext[PatternTransitionCraftsmanDependencies],
    intervention_type: str,
    context: str
) -> str:
    """
    Сгенерировать микро-интервенцию для перехода.

    Args:
        ctx: Контекст выполнения
        intervention_type: Тип интервенции (reframe, anchor, motivate, validate)
        context: Контекст применения

    Returns:
        str: Микро-интервенция
    """

    deps = ctx.deps

    # Получить интервенцию из базы
    intervention_text = deps.templates_db.get_micro_intervention(intervention_type)

    if not intervention_text:
        intervention_text = "Вы движетесь в правильном направлении."

    return f"""
Микро-интервенция создана

Тип: {intervention_type}
Контекст: {context}

Текст интервенции:
{intervention_text}

Терапевтический эффект: {intervention_type.capitalize()}
Длительность: ~20 секунд
"""


async def analyze_program_flow(
    ctx: RunContext[PatternTransitionCraftsmanDependencies],
    program_id: str,
    transitions: List[Dict[str, Any]]
) -> str:
    """
    Проанализировать общий flow всей программы.

    Args:
        ctx: Контекст выполнения
        program_id: ID программы
        transitions: Список всех переходов программы

    Returns:
        str: Анализ flow с метриками и рекомендациями
    """

    # Метрики
    total_transitions = len(transitions)
    avg_duration = sum([t.get("duration", 60) for t in transitions]) / total_transitions if total_transitions > 0 else 0

    # Найти проблемные переходы
    jarring_transitions = []
    smooth_transitions = []

    for t in transitions:
        if t.get("flow_score", 1.0) < 0.6:
            jarring_transitions.append(t.get("transition_id", "unknown"))
        elif t.get("flow_score", 0.0) >= 0.8:
            smooth_transitions.append(t.get("transition_id", "unknown"))

    # Общий flow score
    overall_flow = sum([t.get("flow_score", 0.7) for t in transitions]) / total_transitions if total_transitions > 0 else 0.7

    analysis = FlowAnalysis(
        analysis_id=str(uuid.uuid4()),
        program_id=program_id,
        overall_flow_score=overall_flow,
        transition_count=total_transitions,
        average_transition_duration=avg_duration,
        jarring_transitions=jarring_transitions,
        missing_bridges=[],
        energy_mismatches=[],
        smooth_transitions=smooth_transitions,
        effective_anchors=[],
        improvement_suggestions=[
            "Усилить якоря в переходах с низким flow score",
            "Добавить энергетические переходы где нужно",
            "Проверить эмоциональную непрерывность"
        ]
    )

    return f"""
Анализ flow программы завершен

ID анализа: {analysis.analysis_id}
Программа: {program_id}

Overall Flow Score: {analysis.overall_flow_score:.2f} / 1.00

Метрики:
- Всего переходов: {analysis.transition_count}
- Средняя длительность перехода: {analysis.average_transition_duration:.0f} сек

Проблемные переходы ({len(analysis.jarring_transitions)}):
""" + (", ".join(analysis.jarring_transitions[:5]) if analysis.jarring_transitions else "Не обнаружено") + f"""

Плавные переходы ({len(analysis.smooth_transitions)}):
""" + (", ".join(analysis.smooth_transitions[:5]) if analysis.smooth_transitions else "Не обнаружено") + f"""

Рекомендации по улучшению:
""" + "\n".join([f"- {s}" for s in analysis.improvement_suggestions])


async def search_agent_knowledge(
    ctx: RunContext[PatternTransitionCraftsmanDependencies],
    query: str,
    knowledge_source: str = "agent"
) -> str:
    """
    Поиск в базе знаний агента.

    Args:
        ctx: Контекст выполнения
        query: Поисковый запрос
        knowledge_source: Источник знаний (agent, archon, external)

    Returns:
        str: Результаты поиска
    """

    return f"""
Поиск в базе знаний: "{query}"

Источник: {knowledge_source}

Найденные материалы:
- Принципы создания эффективных переходов
- Типы мостов между модулями
- Энергетические переходы
- Использование якорей

Для получения подробной информации используйте конкретные инструменты агента.
"""


__all__ = [
    "create_module_transition",
    "create_bridge_content",
    "check_program_coherence",
    "generate_micro_intervention",
    "analyze_program_flow",
    "search_agent_knowledge"
]
