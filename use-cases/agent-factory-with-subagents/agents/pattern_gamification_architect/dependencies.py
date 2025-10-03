"""
Зависимости для Pattern Gamification Architect Agent.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class GameMechanicsLibrary:
    """База данных игровых механик."""

    def __post_init__(self):
        """Инициализация библиотеки игровых механик."""

        self.core_mechanics = {
            "points": {
                "description": "Система очков за действия",
                "best_for": ["achiever", "explorer"],
                "therapeutic_use": "Визуализация прогресса",
                "implementation": "Награждать очками за завершение модулей, упражнений, insights"
            },
            "badges": {
                "description": "Достижения за выполнение критериев",
                "best_for": ["achiever", "collector"],
                "therapeutic_use": "Празднование вех трансформации",
                "implementation": "Награды за серии дней, прорывы, мастерство техник"
            },
            "levels": {
                "description": "Прогрессия через уровни",
                "best_for": ["achiever", "explorer"],
                "therapeutic_use": "Ощущение роста и развития",
                "implementation": "Уровни соответствуют этапам трансформации"
            },
            "quests": {
                "description": "Структурированные челленджи",
                "best_for": ["explorer", "achiever"],
                "therapeutic_use": "Направленное применение техник",
                "implementation": "Серии связанных упражнений с нарративом"
            },
            "progress_bars": {
                "description": "Визуализация завершенности",
                "best_for": ["all"],
                "therapeutic_use": "Мотивация к завершению",
                "implementation": "Прогресс дня, недели, программы"
            },
            "streaks": {
                "description": "Серии последовательных действий",
                "best_for": ["achiever"],
                "therapeutic_use": "Построение consistency",
                "implementation": "Дни подряд, недельные серии"
            },
            "unlocks": {
                "description": "Открытие нового контента",
                "best_for": ["explorer"],
                "therapeutic_use": "Anticipation и curiosity",
                "implementation": "Новые техники, insights, бонусные материалы"
            }
        }

        self.player_type_preferences = {
            "achiever": {
                "preferred_mechanics": ["points", "badges", "levels", "leaderboards"],
                "motivation": "Достижение целей и мастерства",
                "rewards": "Видимые признаки прогресса"
            },
            "explorer": {
                "preferred_mechanics": ["unlocks", "secrets", "quests", "discovery"],
                "motivation": "Открытие нового знания",
                "rewards": "Доступ к эксклюзивному контенту"
            },
            "socializer": {
                "preferred_mechanics": ["sharing", "co-op", "community"],
                "motivation": "Связь с другими",
                "rewards": "Социальное признание"
            },
            "killer": {
                "preferred_mechanics": ["challenges", "competition", "rankings"],
                "motivation": "Превосходство",
                "rewards": "Доказательство силы"
            }
        }


@dataclass
class AchievementTemplates:
    """Шаблоны достижений."""

    def __post_init__(self):
        """Инициализация шаблонов."""

        self.completion_achievements = {
            "first_step": {
                "title": "Первый шаг",
                "criteria": "Завершить первый день программы",
                "rarity": "common",
                "meaning": "Преодоление инерции, начало пути"
            },
            "week_warrior": {
                "title": "Воин недели",
                "criteria": "Завершить все модули недели",
                "rarity": "rare",
                "meaning": "Commitment и persistence"
            },
            "transformation_complete": {
                "title": "Трансформация завершена",
                "criteria": "Завершить всю 21-дневную программу",
                "rarity": "epic",
                "meaning": "Полный цикл изменения"
            }
        }

        self.consistency_achievements = {
            "three_day_streak": {
                "title": "Три дня подряд",
                "criteria": "3 дня активности без пропусков",
                "rarity": "common",
                "meaning": "Формирование привычки"
            },
            "weekly_rhythm": {
                "title": "Недельный ритм",
                "criteria": "7 дней подряд",
                "rarity": "rare",
                "meaning": "Интеграция в жизнь"
            },
            "unstoppable": {
                "title": "Неудержимый",
                "criteria": "21 день подряд",
                "rarity": "legendary",
                "meaning": "Полная commitment"
            }
        }

        self.mastery_achievements = {
            "technique_master": {
                "title": "Мастер техники",
                "criteria": "Выполнить технику идеально 3 раза",
                "rarity": "rare",
                "meaning": "Освоение навыка"
            },
            "insight_seeker": {
                "title": "Искатель инсайтов",
                "criteria": "Записать 10 глубоких осознаний",
                "rarity": "rare",
                "meaning": "Глубина рефлексии"
            }
        }


@dataclass
class ProgressionDesigns:
    """Дизайны систем прогрессии."""

    def __post_init__(self):
        """Инициализация дизайнов."""

        self.level_structures = {
            "beginner_path": {
                "levels": [
                    {"level": 1, "name": "Пробуждение", "points": 0},
                    {"level": 2, "name": "Осознание", "points": 100},
                    {"level": 3, "name": "Исследование", "points": 300}
                ],
                "therapeutic_arc": "От бессознательного к осознанности"
            },
            "transformation_path": {
                "levels": [
                    {"level": 1, "name": "Ученик", "points": 0},
                    {"level": 2, "name": "Практик", "points": 500},
                    {"level": 3, "name": "Адепт", "points": 1200},
                    {"level": 4, "name": "Мастер", "points": 2500},
                    {"level": 5, "name": "Преобразованный", "points": 5000}
                ],
                "therapeutic_arc": "Полный путь трансформации"
            }
        }

        self.point_earning_rules = {
            "module_completion": 50,
            "exercise_completion": 25,
            "technique_mastery": 100,
            "daily_reflection": 30,
            "insight_recording": 40,
            "consistency_bonus": 20,
            "perfect_day": 150  # Все модули + упражнения + рефлексия
        }


@dataclass
class BalancingStrategies:
    """Стратегии балансировки."""

    def __post_init__(self):
        """Инициализация стратегий."""

        self.difficulty_progression = {
            "tutorial": {
                "days": [1, 2],
                "challenges": "Очень простые, обучающие",
                "rewards": "Частые, небольшие"
            },
            "easy": {
                "days": [3, 4, 5, 6, 7],
                "challenges": "Доступные, building confidence",
                "rewards": "Регулярные"
            },
            "medium": {
                "days": [8, 9, 10, 11, 12, 13, 14],
                "challenges": "Требуют усилий, но достижимы",
                "rewards": "За effort и результат"
            },
            "hard": {
                "days": [15, 16, 17, 18, 19, 20],
                "challenges": "Интенсивные, deep work",
                "rewards": "Значимые достижения"
            },
            "integration": {
                "days": [21],
                "challenges": "Synthesis всего пройденного",
                "rewards": "Epic completion"
            }
        }

        self.feedback_timing = {
            "immediate": ["points", "task_completion", "simple_achievements"],
            "delayed": ["insights", "patterns", "long_term_progress"],
            "periodic": ["weekly_summaries", "milestone_celebrations"]
        }


@dataclass
class SafeGamificationGuidelines:
    """Руководства по безопасной геймификации."""

    def __post_init__(self):
        """Инициализация руководств."""

        self.safety_principles = [
            "Никогда не сравнивать пользователей друг с другом публично",
            "Фокус на личном прогрессе, не на конкуренции",
            "Всегда предоставлять multiple paths to success",
            "Награждать effort, а не только результат",
            "Делать все социальные функции opt-in",
            "Избегать FOMO (fear of missing out)",
            "Баланс challenge и achievability",
            "Не наказывать за пропуски, только поощрять активность"
        ]

        self.anti_patterns = {
            "public_shaming": "Никогда не показывать кто отстает",
            "forced_social": "Не требовать социального участия",
            "pay_to_win": "Не давать преимуществ за деньги",
            "infinite_grind": "Ограничивать daily tasks",
            "dark_patterns": "Честность в прогрессе и наградах"
        }


@dataclass
class PatternGamificationArchitectDependencies:
    """Зависимости агента."""

    api_key: str
    patternshift_project_path: str = ""

    # Базы данных
    game_mechanics_library: GameMechanicsLibrary = field(
        default_factory=GameMechanicsLibrary
    )
    achievement_templates: AchievementTemplates = field(
        default_factory=AchievementTemplates
    )
    progression_designs: ProgressionDesigns = field(
        default_factory=ProgressionDesigns
    )
    balancing_strategies: BalancingStrategies = field(
        default_factory=BalancingStrategies
    )
    safe_gamification_guidelines: SafeGamificationGuidelines = field(
        default_factory=SafeGamificationGuidelines
    )

    # RAG конфигурация
    agent_name: str = "pattern_gamification_architect"
    knowledge_tags: List[str] = field(
        default_factory=lambda: [
            "pattern-gamification-architect",
            "gamification",
            "behavioral-psychology",
            "agent-knowledge",
            "patternshift"
        ]
    )
    knowledge_domain: str | None = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"


__all__ = [
    "GameMechanicsLibrary",
    "AchievementTemplates",
    "ProgressionDesigns",
    "BalancingStrategies",
    "SafeGamificationGuidelines",
    "PatternGamificationArchitectDependencies"
]
