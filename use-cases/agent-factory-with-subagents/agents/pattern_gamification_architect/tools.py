"""
Инструменты для Pattern Gamification Architect Agent.
"""

import uuid
from typing import Dict, Any, List, Optional
from pydantic_ai import RunContext
from .dependencies import PatternGamificationArchitectDependencies
from .models import (
    GameMechanic,
    Achievement,
    ProgressionPath,
    Challenge,
    PointSystem,
    GamificationSystem,
    PlayerType,
    MotivationType,
    AchievementType,
    DifficultyLevel
)


async def design_game_mechanic(
    ctx: RunContext[PatternGamificationArchitectDependencies],
    mechanic_type: str,
    therapeutic_goal: str,
    target_player_types: List[str]
) -> str:
    """Разработать игровую механику для программы."""
    deps = ctx.deps

    # Получаем шаблон механики из библиотеки
    mechanics_lib = deps.game_mechanics_library.core_mechanics

    if mechanic_type not in mechanics_lib:
        return f"Неизвестный тип механики: {mechanic_type}"

    template = mechanics_lib[mechanic_type]

    mechanic = GameMechanic(
        name=template["description"],
        description=f"Механика {mechanic_type} для {therapeutic_goal}",
        mechanic_type=mechanic_type,
        trigger_conditions=[
            "Завершение модуля",
            "Выполнение упражнения",
            "Запись insight"
        ],
        rewards=[
            f"Очки {mechanic_type}",
            "Прогресс к следующему уровню"
        ],
        therapeutic_goal=therapeutic_goal,
        player_types=[PlayerType(pt) for pt in target_player_types],
        motivation_type=MotivationType.MIXED
    )

    return f"""✅ Создана игровая механика:

**Тип:** {mechanic.mechanic_type}
**Описание:** {mechanic.description}
**Терапевтическая цель:** {mechanic.therapeutic_goal}
**Для типов игроков:** {', '.join([pt.value for pt in mechanic.player_types])}

**Условия срабатывания:**
{chr(10).join(f"- {c}" for c in mechanic.trigger_conditions)}

**Награды:**
{chr(10).join(f"- {r}" for r in mechanic.rewards)}

**Использование:** {template['therapeutic_use']}
**Имплементация:** {template['implementation']}"""


async def create_achievement_system(
    ctx: RunContext[PatternGamificationArchitectDependencies],
    program_duration_days: int,
    focus_areas: List[str]
) -> str:
    """Создать систему достижений для программы."""
    deps = ctx.deps
    templates = deps.achievement_templates

    achievements = []

    # Достижения за завершение
    for name, data in templates.completion_achievements.items():
        achievements.append(Achievement(
            title=data["title"],
            description=f"Критерий: {data['criteria']}",
            achievement_type=AchievementType.COMPLETION,
            icon_description=f"Значок {data['title']}",
            unlock_criteria={"action": data["criteria"]},
            rarity=data["rarity"],
            points_value=50 if data["rarity"] == "common" else (100 if data["rarity"] == "rare" else 250),
            therapeutic_meaning=data["meaning"],
            celebration_message=f"Поздравляем! Вы получили достижение '{data['title']}'!"
        ))

    # Достижения за consistency
    for name, data in templates.consistency_achievements.items():
        achievements.append(Achievement(
            title=data["title"],
            description=f"Критерий: {data['criteria']}",
            achievement_type=AchievementType.CONSISTENCY,
            icon_description=f"Значок {data['title']}",
            unlock_criteria={"streak_days": data["criteria"]},
            rarity=data["rarity"],
            points_value=75 if data["rarity"] == "common" else (150 if data["rarity"] == "rare" else 500),
            therapeutic_meaning=data["meaning"],
            celebration_message=f"Невероятно! {data['title']} - это большое достижение!"
        ))

    # Достижения за mastery
    for name, data in templates.mastery_achievements.items():
        achievements.append(Achievement(
            title=data["title"],
            description=f"Критерий: {data['criteria']}",
            achievement_type=AchievementType.MASTERY,
            icon_description=f"Значок {data['title']}",
            unlock_criteria={"mastery_level": data["criteria"]},
            rarity=data["rarity"],
            points_value=200,
            therapeutic_meaning=data["meaning"],
            celebration_message=f"Браво! Вы получили {data['title']}!"
        ))

    result = f"""✅ Создана система достижений ({len(achievements)} достижений):

## Достижения за завершение:
{chr(10).join([f"- **{a.title}** ({a.rarity}) - {a.therapeutic_meaning}" for a in achievements if a.achievement_type == AchievementType.COMPLETION])}

## Достижения за регулярность:
{chr(10).join([f"- **{a.title}** ({a.rarity}) - {a.therapeutic_meaning}" for a in achievements if a.achievement_type == AchievementType.CONSISTENCY])}

## Достижения за мастерство:
{chr(10).join([f"- **{a.title}** ({a.rarity}) - {a.therapeutic_meaning}" for a in achievements if a.achievement_type == AchievementType.MASTERY])}

**Всего очков доступно:** {sum(a.points_value for a in achievements)}"""

    return result


async def design_progression_path(
    ctx: RunContext[PatternGamificationArchitectDependencies],
    player_type: str,
    program_id: str
) -> str:
    """Разработать путь прогрессии для типа игрока."""
    deps = ctx.deps
    designs = deps.progression_designs

    # Выбираем структуру прогрессии
    structure = designs.level_structures["transformation_path"]

    path = ProgressionPath(
        path_name=f"Путь трансформации ({player_type})",
        description=f"Специализированный путь развития для {player_type}",
        levels=structure["levels"],
        player_type_affinity=PlayerType(player_type),
        total_points_required=structure["levels"][-1]["points"],
        therapeutic_arc=structure["therapeutic_arc"]
    )

    return f"""✅ Создан путь прогрессии:

**Название:** {path.path_name}
**Тип игрока:** {path.player_type_affinity.value}
**Терапевтическая дуга:** {path.therapeutic_arc}

**Уровни:**
{chr(10).join([f"Уровень {l['level']}: {l['name']} (от {l['points']} очков)" for l in path.levels])}

**Всего очков для максимального уровня:** {path.total_points_required}"""


async def create_challenge(
    ctx: RunContext[PatternGamificationArchitectDependencies],
    challenge_title: str,
    difficulty: str,
    therapeutic_focus: str,
    duration_days: Optional[int] = None
) -> str:
    """Создать челлендж/квест."""

    challenge = Challenge(
        title=challenge_title,
        description=f"Челлендж фокусируется на {therapeutic_focus}",
        difficulty=DifficultyLevel(difficulty),
        tasks=[
            {"task": "Выполнить основную технику дня", "points": 50},
            {"task": "Записать минимум 1 insight", "points": 30},
            {"task": "Сделать reflection упражнение", "points": 20}
        ],
        time_limit=duration_days,
        rewards=[
            f"Badge: {challenge_title}",
            "Bonus points",
            "Unlock: exclusive content"
        ],
        therapeutic_focus=therapeutic_focus,
        success_criteria={
            "min_tasks_completed": 2,
            "min_quality_score": 7
        },
        fallback_strategy="Если не получается - попробуйте упрощенную версию техники"
    )

    return f"""✅ Создан челлендж:

**Название:** {challenge.title}
**Сложность:** {challenge.difficulty.value}
**Фокус:** {challenge.therapeutic_focus}
{'**Ограничение по времени:** ' + str(challenge.time_limit) + ' дней' if challenge.time_limit else '**Без ограничения по времени**'}

**Задачи:**
{chr(10).join([f"- {t['task']} (+{t['points']} очков)" for t in challenge.tasks])}

**Награды:**
{chr(10).join([f"- {r}" for r in challenge.rewards])}

**Критерии успеха:**
- Минимум задач: {challenge.success_criteria['min_tasks_completed']}
- Минимальное качество: {challenge.success_criteria['min_quality_score']}/10

**Стратегия при трудностях:** {challenge.fallback_strategy}"""


async def design_point_system(
    ctx: RunContext[PatternGamificationArchitectDependencies],
    point_type_name: str,
    therapeutic_meaning: str
) -> str:
    """Разработать систему очков."""
    deps = ctx.deps
    earning_rules = deps.progression_designs.point_earning_rules

    point_system = PointSystem(
        point_type=point_type_name,
        earning_rules=earning_rules,
        level_thresholds=[0, 100, 300, 500, 1200, 2500, 5000],
        display_name=point_type_name.capitalize(),
        therapeutic_meaning=therapeutic_meaning
    )

    return f"""✅ Создана система очков:

**Название:** {point_system.display_name}
**Терапевтическое значение:** {point_system.therapeutic_meaning}

**Правила начисления:**
{chr(10).join([f"- {action.replace('_', ' ').capitalize()}: +{points} очков" for action, points in point_system.earning_rules.items()])}

**Пороги уровней:**
{chr(10).join([f"Уровень {i+1}: от {threshold} очков" for i, threshold in enumerate(point_system.level_thresholds)])}"""


async def balance_gamification_system(
    ctx: RunContext[PatternGamificationArchitectDependencies],
    program_id: str,
    target_completion_rate: float = 0.7
) -> str:
    """Сбалансировать систему геймификации."""
    deps = ctx.deps
    balancing = deps.balancing_strategies

    # Анализ сложности по дням
    difficulty_curve = []
    for phase, config in balancing.difficulty_progression.items():
        difficulty_curve.append(f"**{phase.capitalize()}** (дни {config['days']}): {config['challenges']}")

    # Стратегии обратной связи
    feedback_strategies = []
    for timing, events in balancing.feedback_timing.items():
        feedback_strategies.append(f"**{timing.capitalize()}**: {', '.join(events)}")

    return f"""✅ Система геймификации сбалансирована:

**Целевой completion rate:** {target_completion_rate * 100}%

## Кривая сложности:
{chr(10).join(difficulty_curve)}

## Стратегии обратной связи:
{chr(10).join(feedback_strategies)}

## Принципы балансировки:
- Начало легкое для onboarding
- Постепенное увеличение challenge
- Peak difficulty в дни 15-20
- Integration и celebration в конце
- Награды соответствуют effort
- Multiple paths для разных типов игроков

**Рекомендации:**
1. Тестировать с фокус-группой
2. Собирать метрики engagement
3. Адаптировать на основе данных
4. Всегда иметь fallback для struggling users"""


async def search_agent_knowledge(
    ctx: RunContext[PatternGamificationArchitectDependencies],
    query: str
) -> str:
    """Поиск в базе знаний агента."""
    return f"Результаты поиска для: {query}"


__all__ = [
    "design_game_mechanic",
    "create_achievement_system",
    "design_progression_path",
    "create_challenge",
    "design_point_system",
    "balance_gamification_system",
    "search_agent_knowledge"
]
