"""
Специализированные инструменты для Pattern Microhabit Designer Agent
"""

import asyncio
import json
import uuid
from typing import List, Dict, Any, Optional, Tuple
from pydantic_ai import RunContext

from .models import (
    Microhabit,
    HabitChain,
    MicrohabitTrigger,
    HabitReward,
    HabitTriggerType,
    RewardType,
    DifficultyLevel,
    HabitChainPosition,
    MicrohabitModule,
    BehaviorChangeGoal
)
from .dependencies import PatternMicrohabitDesignerDependencies


async def design_microhabit(
    ctx: RunContext[PatternMicrohabitDesignerDependencies],
    goal_description: str,
    target_behavior: str,
    existing_routines: List[str],
    available_time_seconds: int = 120,
    difficulty_preference: str = "micro"
) -> Microhabit:
    """
    Создать микро-привычку под конкретную цель

    Args:
        ctx: Контекст выполнения с зависимостями
        goal_description: Описание цели изменения
        target_behavior: Целевое поведение
        existing_routines: Существующие рутины для habit stacking
        available_time_seconds: Доступное время (default: 120 секунд)
        difficulty_preference: Предпочтительная сложность (micro/easy/medium)

    Returns:
        Microhabit: Спроектированная микро-привычка
    """

    # Поиск знаний о формировании привычек
    habit_knowledge = await ctx.deps.search_habit_knowledge("habit loop atomic habits")

    # Определение триггеров на основе существующих рутин
    triggers = []
    for routine in existing_routines[:2]:  # Топ-2 рутины
        triggers.append(MicrohabitTrigger(
            type=HabitTriggerType.EXISTING_HABIT,
            description=f"После того как {routine.lower()}",
            example=f"После того как {routine.lower()}, я сделаю {target_behavior.lower()}",
            reliability_score=0.85
        ))

    # Подбор вознаграждений
    reward_recs = await ctx.deps.get_reward_recommendations(
        habit_type=target_behavior,
        user_motivation_profile=None
    )

    rewards = []
    for rec in reward_recs[:2]:  # Топ-2 вознаграждения
        rewards.append(HabitReward(
            type=RewardType(rec["type"]),
            description=rec.get("description", "Внутреннее удовлетворение"),
            effectiveness=rec.get("effectiveness", 0.7),
            immediate=rec.get("timing", "immediate") == "immediate"
        ))

    # Определение барьеров и способов их устранения
    barriers = await ctx.deps.behavior_toolkit.identify_friction_points(target_behavior)
    strategies = await ctx.deps.get_behavior_change_strategies(target_behavior)

    # Создание микро-привычки
    microhabit = Microhabit(
        id=f"microhabit_{uuid.uuid4().hex[:8]}",
        name=f"{target_behavior} (микро-версия)",
        description=f"Атомарная версия поведения '{target_behavior}' для формирования устойчивой привычки",
        difficulty=DifficultyLevel(difficulty_preference),
        duration_seconds=min(available_time_seconds, 120),  # Max 2 минуты для micro
        triggers=triggers,
        rewards=rewards,
        barriers=barriers[:3],
        motivators=strategies[:3],
        chain_position=HabitChainPosition.STANDALONE,
        measurable=True,
        success_criteria=f"Выполнить '{target_behavior}' в течение {available_time_seconds} секунд после триггера",
        estimated_impact=0.75
    )

    return microhabit


async def create_habit_chain(
    ctx: RunContext[PatternMicrohabitDesignerDependencies],
    anchor_habit: str,
    target_habits: List[str],
    total_duration_seconds: int = 300
) -> HabitChain:
    """
    Построить цепочку усиливающих друг друга привычек (domino effect)

    Args:
        ctx: Контекст выполнения
        anchor_habit: Якорная привычка (первая в цепи)
        target_habits: Список целевых привычек для добавления в цепь
        total_duration_seconds: Общее время цепочки (default: 5 минут)

    Returns:
        HabitChain: Построенная цепочка привычек
    """

    # Получаем знания о Tiny Habits модели
    tiny_habits = await ctx.deps.search_habit_knowledge("tiny habits model")

    chain_habits = []
    current_duration = 0

    # Создаём якорную привычку
    anchor = await design_microhabit(
        ctx,
        goal_description=f"Начать цепочку с {anchor_habit}",
        target_behavior=anchor_habit,
        existing_routines=["Проснуться", "Встать с кровати"],
        available_time_seconds=30,
        difficulty_preference="micro"
    )
    anchor.chain_position = HabitChainPosition.ANCHOR
    chain_habits.append(anchor)
    current_duration += anchor.duration_seconds

    # Добавляем связанные привычки
    previous_habit = anchor
    for i, habit_name in enumerate(target_habits):
        if current_duration >= total_duration_seconds:
            break

        remaining_time = total_duration_seconds - current_duration
        habit_duration = min(remaining_time // (len(target_habits) - i), 90)

        linked_habit = await design_microhabit(
            ctx,
            goal_description=f"Добавить {habit_name} в цепочку",
            target_behavior=habit_name,
            existing_routines=[previous_habit.name],
            available_time_seconds=habit_duration,
            difficulty_preference="micro"
        )

        linked_habit.chain_position = (
            HabitChainPosition.CAPSTONE if i == len(target_habits) - 1
            else HabitChainPosition.LINKED
        )
        linked_habit.linked_habit_id = previous_habit.id

        chain_habits.append(linked_habit)
        current_duration += linked_habit.duration_seconds
        previous_habit = linked_habit

    # Рассчитываем кумулятивное влияние
    cumulative_impact = sum(h.estimated_impact for h in chain_habits) / len(chain_habits)
    cumulative_impact = min(cumulative_impact * 1.2, 1.0)  # Bonus за синергию

    chain = HabitChain(
        chain_id=f"chain_{uuid.uuid4().hex[:8]}",
        name=f"Цепочка: {anchor_habit} + {len(target_habits)} привычек",
        description=f"Последовательность из {len(chain_habits)} микро-привычек с cumulative effect",
        habits=chain_habits,
        total_duration_seconds=current_duration,
        cumulative_impact=cumulative_impact
    )

    return chain


async def identify_triggers_rewards(
    ctx: RunContext[PatternMicrohabitDesignerDependencies],
    target_behavior: str,
    user_context: Dict[str, Any]
) -> Tuple[List[MicrohabitTrigger], List[HabitReward]]:
    """
    Анализ и подбор оптимальных триггеров и вознаграждений

    Args:
        ctx: Контекст выполнения
        target_behavior: Целевое поведение
        user_context: Контекст пользователя (расписание, предпочтения)

    Returns:
        Tuple[List[MicrohabitTrigger], List[HabitReward]]: Триггеры и вознаграждения
    """

    # Извлекаем данные из контекста
    existing_routines = user_context.get("existing_routines", [])
    motivation_profile = user_context.get("motivation_profile", {})

    # Поиск знаний об implementation intentions
    implementation_research = await ctx.deps.search_habit_knowledge("implementation intention")

    # Генерация триггеров разных типов
    triggers = []

    # Time-based triggers
    if "preferred_times" in user_context:
        for time in user_context["preferred_times"][:2]:
            triggers.append(MicrohabitTrigger(
                type=HabitTriggerType.TIME,
                description=f"В {time}",
                example=f"Каждый день в {time} я {target_behavior}",
                reliability_score=0.7
            ))

    # Existing habit triggers (habit stacking)
    for routine in existing_routines[:3]:
        triggers.append(MicrohabitTrigger(
            type=HabitTriggerType.EXISTING_HABIT,
            description=f"После {routine}",
            example=f"После того как {routine.lower()}, я {target_behavior.lower()}",
            reliability_score=0.85
        ))

    # Location-based triggers
    if "frequent_locations" in user_context:
        for location in user_context["frequent_locations"][:2]:
            triggers.append(MicrohabitTrigger(
                type=HabitTriggerType.LOCATION,
                description=f"Когда прихожу в {location}",
                example=f"Когда прихожу в {location}, я {target_behavior}",
                reliability_score=0.75
            ))

    # Подбор вознаграждений
    rewards = []

    # Intrinsic rewards (предпочтительны)
    intrinsic_factors = await ctx.deps.motivation_db.get_intrinsic_motivation_factors()
    for factor in intrinsic_factors[:3]:
        rewards.append(HabitReward(
            type=RewardType.INTRINSIC,
            description=f"Чувство {factor} от выполнения",
            effectiveness=0.85,
            immediate=True
        ))

    # Immediate physical rewards
    rewards.append(HabitReward(
        type=RewardType.IMMEDIATE,
        description="Микро-празднование (fist pump, улыбка)",
        effectiveness=0.8,
        immediate=True
    ))

    # Variable rewards для повышения dopamine
    rewards.append(HabitReward(
        type=RewardType.EXTRINSIC,
        description="Случайное вознаграждение за streak (surprise factor)",
        effectiveness=0.75,
        immediate=False
    ))

    return triggers, rewards


async def generate_module_variants(
    ctx: RunContext[PatternMicrohabitDesignerDependencies],
    base_microhabit: Microhabit,
    variant_types: List[str]
) -> Dict[str, Microhabit]:
    """
    Генерация вариантов модуля микро-привычки для разных аудиторий

    Args:
        ctx: Контекст выполнения
        base_microhabit: Базовая микро-привычка
        variant_types: Типы вариантов (vak, age, culture)

    Returns:
        Dict[str, Microhabit]: Словарь вариантов микро-привычки
    """

    variants = {}

    for variant_type in variant_types:
        if variant_type == "vak":
            # VAK варианты (Visual, Auditory, Kinesthetic)
            variants["visual"] = await _create_visual_variant(base_microhabit)
            variants["auditory"] = await _create_auditory_variant(base_microhabit)
            variants["kinesthetic"] = await _create_kinesthetic_variant(base_microhabit)

        elif variant_type == "age":
            # Age варианты
            variants["young_adults"] = await _create_age_variant(base_microhabit, "young_adults")
            variants["adults"] = await _create_age_variant(base_microhabit, "adults")
            variants["seniors"] = await _create_age_variant(base_microhabit, "seniors")

        elif variant_type == "culture":
            # Culture варианты
            variants["western"] = base_microhabit  # Base variant
            variants["eastern"] = await _create_culture_variant(base_microhabit, "eastern")

    return variants


# Вспомогательные функции для генерации вариантов
async def _create_visual_variant(habit: Microhabit) -> Microhabit:
    """Создать визуальный вариант привычки"""
    visual_habit = habit.model_copy(deep=True)
    visual_habit.id = f"{habit.id}_visual"
    visual_habit.description += "\n\nВизуальный акцент: используйте визуальные напоминания, charts для tracking"
    return visual_habit


async def _create_auditory_variant(habit: Microhabit) -> Microhabit:
    """Создать аудиальный вариант привычки"""
    auditory_habit = habit.model_copy(deep=True)
    auditory_habit.id = f"{habit.id}_auditory"
    auditory_habit.description += "\n\nАудиальный акцент: используйте звуковые напоминания, verbal affirmations"
    return auditory_habit


async def _create_kinesthetic_variant(habit: Microhabit) -> Microhabit:
    """Создать кинестетический вариант привычки"""
    kinesthetic_habit = habit.model_copy(deep=True)
    kinesthetic_habit.id = f"{habit.id}_kinesthetic"
    kinesthetic_habit.description += "\n\nКинестетический акцент: physical movement, tactile reminders"
    return kinesthetic_habit


async def _create_age_variant(habit: Microhabit, age_group: str) -> Microhabit:
    """Создать возрастной вариант привычки"""
    age_habit = habit.model_copy(deep=True)
    age_habit.id = f"{habit.id}_{age_group}"

    if age_group == "young_adults":
        age_habit.description += "\n\nАдаптация для молодых: gamification, social sharing"
    elif age_group == "adults":
        age_habit.description += "\n\nАдаптация для взрослых: efficiency, integration с работой"
    elif age_group == "seniors":
        age_habit.description += "\n\nАдаптация для пожилых: simplicity, health benefits"

    return age_habit


async def _create_culture_variant(habit: Microhabit, culture: str) -> Microhabit:
    """Создать культурный вариант привычки"""
    culture_habit = habit.model_copy(deep=True)
    culture_habit.id = f"{habit.id}_{culture}"

    if culture == "eastern":
        culture_habit.description += "\n\nКультурная адаптация: коллективные ценности, семейная ориентация"

    return culture_habit


async def search_agent_knowledge(
    ctx: RunContext[PatternMicrohabitDesignerDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в специализированной базе знаний агента через локальную DB и RAG fallback

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """

    # Сначала пробуем локальную базу знаний
    local_knowledge = await ctx.deps.search_habit_knowledge(query)

    if local_knowledge:
        knowledge_str = json.dumps(local_knowledge, ensure_ascii=False, indent=2)
        return f"Найдено в локальной базе знаний:\n{knowledge_str}"

    # Fallback: возвращаем полезную информацию о привычках
    return """
База знаний о формировании привычек:

1. Habit Loop (Charles Duhigg): Cue → Routine → Reward
2. Atomic Habits (James Clear): Make it obvious, attractive, easy, satisfying
3. Tiny Habits (BJ Fogg): B = MAP (Behavior = Motivation + Ability + Prompt)
4. Implementation Intentions: "When X happens, I will do Y"
5. The 2-Minute Rule: Scale down habits to 2 minutes or less

Используйте эти принципы для дизайна эффективных микро-привычек.
"""
