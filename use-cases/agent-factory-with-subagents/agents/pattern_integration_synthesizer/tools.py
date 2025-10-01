"""
Специализированные инструменты для Pattern Integration Synthesizer Agent.
"""

from pydantic_ai import RunContext
from typing import List, Dict, Any, Optional
from .dependencies import PatternIntegrationSynthesizerDependencies
from .models import (
    PhaseType,
    SessionSlot,
    EmotionalCurveStage,
    SynergyLevel,
    Program,
    ModuleSynergy,
    ResistancePoint
)


async def orchestrate_module_sequence(
    ctx: RunContext[PatternIntegrationSynthesizerDependencies],
    module_ids: List[str],
    phase_type: str,
    target_goals: List[str]
) -> str:
    """
    Оркестровать последовательность модулей для максимальной синергии.

    Args:
        ctx: Контекст с зависимостями
        module_ids: Список ID модулей для оркестрации
        phase_type: Тип фазы (beginning, development, integration)
        target_goals: Целевые цели программы

    Returns:
        Оптимальная последовательность с обоснованием
    """
    patterns_db = ctx.deps.orchestration_patterns_db

    # Определяем подходящий паттерн оркестрации
    phase_patterns = {
        "beginning": "progressive_intensity",
        "development": "technique_sandwich",
        "integration": "spiral_deepening"
    }

    pattern_name = phase_patterns.get(phase_type, "progressive_intensity")
    pattern = patterns_db.patterns[pattern_name]

    result = f"""
## Оркестрация модулей для фазы: {phase_type}

**Выбранный паттерн:** {pattern_name}
**Обоснование:** {pattern['rationale']}

**Рекомендуемая последовательность ({len(module_ids)} модулей):**

"""

    # Применяем паттерн к модулям
    sequence = pattern['sequence']
    modules_per_stage = len(module_ids) // len(sequence)

    for idx, module_id in enumerate(module_ids):
        stage_idx = min(idx // max(modules_per_stage, 1), len(sequence) - 1)
        stage = sequence[stage_idx]

        result += f"{idx + 1}. {module_id} → Стадия: {stage}\n"

    # Добавляем правила синергии
    result += f"\n**Правила синергии:**\n"
    for rule in patterns_db.synergy_rules["high_synergy_pairs"][:3]:
        result += f"- ✅ {rule}\n"

    result += f"\n**Избегать:**\n"
    for avoid in patterns_db.synergy_rules["avoid_combinations"]:
        result += f"- ⚠️ {avoid}\n"

    result += f"\n**Ожидаемый эффект:** Синергичное взаимодействие модулей создаст кумулятивный эффект превышающий сумму отдельных частей."

    return result


async def manage_emotional_curve(
    ctx: RunContext[PatternIntegrationSynthesizerDependencies],
    program_duration_days: int,
    program_intensity: str = "medium"
) -> str:
    """
    Управлять эмоциональной кривой на протяжении программы.

    Args:
        ctx: Контекст с зависимостями
        program_duration_days: Длительность программы в днях
        program_intensity: Интенсивность программы (light, medium, intensive)

    Returns:
        План управления эмоциональной кривой
    """
    curve_db = ctx.deps.emotional_curve_db

    result = f"""
## Управление эмоциональной кривой: {program_duration_days} дней

**Интенсивность программы:** {program_intensity}

**Этапы эмоциональной кривой:**

"""

    # Распределяем стадии по дням
    for stage_key, stage_data in curve_db.curve_stages.items():
        result += f"\n### {stage_data['stage'].upper()}\n"
        result += f"**Энергия:** {stage_data['energy']} | **Мотивация:** {stage_data['motivation']}\n\n"

        result += "**Характеристики:**\n"
        for char in stage_data['characteristics']:
            result += f"- {char}\n"

        result += "\n**Оптимальные активности:**\n"
        for activity in stage_data['optimal_activities']:
            result += f"- ✅ {activity}\n"

        if 'avoid' in stage_data:
            result += f"\n**Избегать:** {', '.join(stage_data['avoid'])}\n"

        if 'critical' in stage_data:
            result += f"\n⚠️ **КРИТИЧНО:** {stage_data['critical']}\n"

        if 'opportunity' in stage_data:
            result += f"\n💡 **ВОЗМОЖНОСТЬ:** {stage_data['opportunity']}\n"

    # Добавляем точки сопротивления
    result += f"\n## Точки сопротивления и митигация:\n\n"
    for rp in curve_db.resistance_points:
        result += f"**Дни {rp['day_range']}** - {rp['type']} (Severity: {rp['severity']})\n"
        result += "Стратегии митигации:\n"
        for strategy in rp['mitigation']:
            result += f"  - {strategy}\n"
        result += "\n"

    return result


async def identify_resistance_points(
    ctx: RunContext[PatternIntegrationSynthesizerDependencies],
    program: Dict[str, Any],
    user_profile: Optional[Dict[str, Any]] = None
) -> str:
    """
    Предвидеть точки сопротивления и встроить поддержку.

    Args:
        ctx: Контекст с зависимостями
        program: Структура программы
        user_profile: Профиль пользователя (опционально)

    Returns:
        Анализ точек сопротивления с рекомендациями
    """
    curve_db = ctx.deps.emotional_curve_db
    load_db = ctx.deps.module_load_db

    result = f"""
## Анализ точек сопротивления

**Программа:** {program.get('program_name', 'Unknown')}
**Длительность:** {program.get('total_days', 21)} дней

### 🔴 Выявленные точки сопротивления:

"""

    # Стандартные точки сопротивления из базы
    for idx, rp in enumerate(curve_db.resistance_points, 1):
        result += f"\n**{idx}. Дни {rp['day_range']}** - {rp['type']}\n"
        result += f"   - **Severity:** {rp['severity']}\n"
        result += f"   - **Описание:** Типичная точка dropout связанная с {rp['type']}\n"
        result += f"   - **Митигация:**\n"
        for strategy in rp['mitigation']:
            result += f"     - ✅ {strategy}\n"

    # Анализ нагрузки программы
    result += f"\n### 📊 Анализ нагрузки:\n\n"
    guidelines = load_db.load_guidelines

    result += f"**Рекомендуемые лимиты:**\n"
    optimal_range = guidelines['daily_limits']['total_minutes']['optimal_range']
    result += f"- Общее время в день: {optimal_range[0]}-{optimal_range[1]} минут\n"
    result += f"- Количество сессий: {guidelines['daily_limits']['sessions_per_day']['optimal']}\n"
    result += f"- Интенсивных модулей: максимум {guidelines['daily_limits']['intensive_modules']['max_per_day']} в день\n"

    result += f"\n**Индикаторы перегрузки (мониторить):**\n"
    for indicator in load_db.fatigue_indicators:
        result += f"- ⚠️ {indicator}\n"

    # Персонализированные рекомендации
    if user_profile:
        result += f"\n### 👤 Персонализированные риски:\n"
        if user_profile.get('previous_dropout', False):
            result += "- ⚠️ История dropout → усилить поддержку на днях 4-7\n"
        if user_profile.get('low_motivation', False):
            result += "- ⚠️ Низкая базовая мотивация → увеличить quick wins и gamification\n"

    result += f"\n### 💡 Общие рекомендации:\n"
    result += "- Встроить check-in точки в дни высокого риска\n"
    result += "- Подготовить motivational content заранее\n"
    result += "- Обеспечить легкий доступ к support resources\n"
    result += "- Создать emergency lightweight версии для дней низкой мотивации\n"

    return result


async def ensure_module_synergy(
    ctx: RunContext[PatternIntegrationSynthesizerDependencies],
    module_a_id: str,
    module_b_id: str,
    gap_days: int = 0
) -> str:
    """
    Обеспечить синергию между модулями программы.

    Args:
        ctx: Контекст с зависимостями
        module_a_id: ID первого модуля
        module_b_id: ID второго модуля
        gap_days: Промежуток в днях между модулями

    Returns:
        Анализ синергии с рекомендациями
    """
    patterns_db = ctx.deps.orchestration_patterns_db

    result = f"""
## Анализ синергии модулей

**Модуль A:** {module_a_id}
**Модуль B:** {module_b_id}
**Промежуток:** {gap_days} дней

"""

    # Проверяем известные синергетические пары
    synergy_found = False
    for pair in patterns_db.synergy_rules["high_synergy_pairs"]:
        if (module_a_id in pair or module_b_id in pair):
            result += f"✅ **Высокая синергия обнаружена!**\n"
            result += f"   Паттерн: {pair}\n"
            synergy_found = True
            break

    if not synergy_found:
        result += f"⚠️ Синергия не выявлена в известных паттернах\n"
        result += f"   Требуется ручная оценка совместимости\n"

    # Проверяем конфликты
    result += f"\n### Проверка конфликтов:\n"
    conflict_found = False
    for avoid_pattern in patterns_db.synergy_rules["avoid_combinations"]:
        if module_a_id in avoid_pattern or module_b_id in avoid_pattern:
            result += f"⛔ **КОНФЛИКТ:** {avoid_pattern}\n"
            conflict_found = True

    if not conflict_found:
        result += "✅ Конфликтов не обнаружено\n"

    # Рекомендации по промежутку
    result += f"\n### Рекомендации по временному интервалу:\n"
    if gap_days == 0:
        result += "- Модули в один день: возможно если оба не intensive\n"
        result += "- Рекомендуется минимум 2-4 часа между сессиями\n"
    elif gap_days == 1:
        result += "- Оптимальный промежуток для закрепления\n"
        result += "- Достаточно времени для интеграции\n"
    elif gap_days >= 3:
        result += "- Большой промежуток: может потребоваться recap\n"
        result += "- Добавить bridge transition для связности\n"

    result += f"\n### Оптимизация синергии:\n"
    result += "1. Добавить explicit reference в модуле B к результатам модуля A\n"
    result += "2. Создать transition bridge подчеркивающий связь\n"
    result += "3. В feedback модуля B спросить о применении знаний из модуля A\n"

    return result


async def analyze_program_coherence(
    ctx: RunContext[PatternIntegrationSynthesizerDependencies],
    program_structure: Dict[str, Any]
) -> str:
    """
    Проанализировать целостность и связность программы.

    Args:
        ctx: Контекст с зависимостями
        program_structure: Структура программы для анализа

    Returns:
        Отчет о coherence с рекомендациями
    """
    result = f"""
## Анализ целостности программы

**Программа:** {program_structure.get('program_name', 'Unknown')}
**Длительность:** {program_structure.get('total_days', 21)} дней

### 📊 Метрики целостности:

"""

    # Анализ фаз
    phases = program_structure.get('phases', [])
    result += f"**Количество фаз:** {len(phases)}\n"

    if len(phases) == 3:
        result += "✅ Оптимальная структура 3 фазы (Beginning, Development, Integration)\n"
    else:
        result += f"⚠️ Нестандартное количество фаз: рекомендуется 3\n"

    # Проверка баланса между фазами
    result += f"\n**Баланс фаз:**\n"
    for phase in phases:
        phase_name = phase.get('phase_type', 'unknown')
        days_count = len(phase.get('days', []))
        result += f"- {phase_name}: {days_count} дней\n"

    # Анализ переходов
    result += f"\n### 🔗 Анализ переходов:\n"
    transition_db = ctx.deps.transition_patterns_db

    for transition_type, transition_data in transition_db.transition_types.items():
        result += f"**{transition_type}:** {transition_data['purpose']}\n"
        result += f"  - Длительность: {transition_data['duration']}\n"

    # Общие рекомендации
    result += f"\n### 💡 Рекомендации по улучшению coherence:\n"
    result += "1. Убедиться что каждая фаза имеет четкие цели\n"
    result += "2. Создать narrative arc через всю программу\n"
    result += "3. Обеспечить логические transitions между днями\n"
    result += "4. Добавить recap элементы для связи с прошлым опытом\n"
    result += "5. Включить forward-looking элементы для anticipation\n"

    return result


async def search_agent_knowledge(
    ctx: RunContext[PatternIntegrationSynthesizerDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в специализированной базе знаний агента через Archon RAG.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    search_tags = ctx.deps.knowledge_tags

    try:
        # Используем MCP Archon для RAG поиска
        # (в реальной имплементации здесь был бы вызов mcp__archon__rag_search_knowledge_base)

        # Fallback: используем локальные базы знаний
        result = f"Поиск в базе знаний по запросу: '{query}'\n\n"

        # Поиск в базах данных dependencies
        if "orchestration" in query.lower() or "pattern" in query.lower():
            patterns = ctx.deps.orchestration_patterns_db.patterns
            result += "**Найденные паттерны оркестрации:**\n"
            for pattern_name, pattern_data in list(patterns.items())[:match_count]:
                result += f"- {pattern_name}: {pattern_data['description']}\n"

        if "emotional" in query.lower() or "curve" in query.lower():
            stages = ctx.deps.emotional_curve_db.curve_stages
            result += "\n**Стадии эмоциональной кривой:**\n"
            for stage_name, stage_data in list(stages.items())[:match_count]:
                result += f"- {stage_data['stage']}: {stage_data.get('characteristics', [])[0] if stage_data.get('characteristics') else 'N/A'}\n"

        if "load" in query.lower() or "intensity" in query.lower():
            guidelines = ctx.deps.module_load_db.load_guidelines
            optimal_range = guidelines['daily_limits']['total_minutes']['optimal_range']
            result += "\n**Рекомендации по нагрузке:**\n"
            result += f"- Оптимальная длительность дня: {optimal_range[0]}-{optimal_range[1]} минут\n"

        if "transition" in query.lower():
            transitions = ctx.deps.transition_patterns_db.transition_types
            result += "\n**Типы переходов:**\n"
            for trans_name, trans_data in list(transitions.items())[:match_count]:
                result += f"- {trans_name}: {trans_data['purpose']}\n"

        if not any(keyword in query.lower() for keyword in ["orchestration", "emotional", "load", "transition"]):
            result += "\n💡 Попробуйте поиск по ключевым словам: orchestration, emotional curve, load, transition\n"

        return result

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"


__all__ = [
    "orchestrate_module_sequence",
    "manage_emotional_curve",
    "identify_resistance_points",
    "ensure_module_synergy",
    "analyze_program_coherence",
    "search_agent_knowledge"
]
