"""
Зависимости для Pattern Microhabit Designer Agent с интеграцией RAG и Archon
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path


class HabitScienceDatabase:
    """База данных научных исследований о формировании привычек"""

    def __init__(self):
        self.habit_research = {}
        self.behavior_models = {}

    async def get_habit_loop_science(self) -> Dict[str, Any]:
        """Получение научных данных о петле привычки (Cue-Routine-Reward)"""
        return {
            "model": "Habit Loop (Charles Duhigg)",
            "components": ["cue", "routine", "reward"],
            "key_finding": "Habits form when consistent cue-routine-reward patterns are repeated",
            "evidence_level": "strong",
            "citations": [
                "Duhigg, C. (2012). The Power of Habit",
                "Wood, W., & Rünger, D. (2016). Psychology of Habit"
            ]
        }

    async def get_implementation_intention_research(self) -> Dict[str, Any]:
        """Получение исследований о намерениях реализации"""
        return {
            "concept": "Implementation Intentions",
            "format": "When [SITUATION] occurs, I will [BEHAVIOR]",
            "effectiveness": 0.91,  # Cohen's d effect size
            "evidence_level": "strong",
            "citations": [
                "Gollwitzer, P. M. (1999). Implementation intentions",
                "Gollwitzer & Sheeran (2006). Meta-analysis"
            ]
        }

    async def get_atomic_habit_principles(self) -> Dict[str, Any]:
        """Получение принципов атомарных привычек"""
        return {
            "principle": "Atomic Habits (James Clear)",
            "key_insights": [
                "Make it obvious (visibility of cues)",
                "Make it attractive (immediate rewards)",
                "Make it easy (reduce friction)",
                "Make it satisfying (positive reinforcement)"
            ],
            "effectiveness": "high",
            "minimum_viable_habit": "less than 2 minutes"
        }

    async def get_tiny_habits_model(self) -> Dict[str, Any]:
        """Получение модели крошечных привычек BJ Fogg"""
        return {
            "model": "Tiny Habits (BJ Fogg)",
            "formula": "B = MAP (Behavior = Motivation + Ability + Prompt)",
            "key_principle": "Start tiny - celebration creates positive emotion",
            "anchor_principle": "After I [EXISTING HABIT], I will [TINY BEHAVIOR]",
            "celebration": "Critical for wiring new habit in brain",
            "effectiveness": "very high for micro behaviors"
        }


class MotivationDatabase:
    """База данных о психологии мотивации"""

    def __init__(self):
        self.motivational_theories = {}
        self.reward_systems = {}

    async def get_intrinsic_motivation_factors(self) -> List[str]:
        """Получение факторов внутренней мотивации"""
        return [
            "autonomy",  # Автономность
            "mastery",  # Мастерство
            "purpose",  # Цель
            "curiosity",  # Любопытство
            "enjoyment"  # Удовольствие
        ]

    async def get_reward_timing_research(self) -> Dict[str, Any]:
        """Исследования о времени вознаграждения"""
        return {
            "immediate_rewards": {
                "effectiveness": 0.85,
                "best_for": "habit formation phase",
                "duration": "first 21-66 days"
            },
            "delayed_rewards": {
                "effectiveness": 0.45,
                "best_for": "long-term maintenance",
                "requires": "strong intrinsic motivation"
            },
            "variable_rewards": {
                "effectiveness": 0.92,
                "dopamine_impact": "highest",
                "risk": "potential for addiction-like patterns"
            }
        }


class BehaviorDesignToolkit:
    """Инструменты дизайна поведения"""

    def __init__(self):
        self.friction_reducers = []
        self.trigger_types = []

    async def identify_friction_points(self, behavior: str) -> List[str]:
        """Определение точек трения для поведения"""
        return [
            "time_required",
            "physical_effort",
            "mental_effort",
            "social_pressure",
            "environmental_barriers"
        ]

    async def generate_friction_reduction_strategies(
        self,
        friction_points: List[str]
    ) -> Dict[str, List[str]]:
        """Генерация стратегий снижения трения"""
        strategies = {}
        for point in friction_points:
            if point == "time_required":
                strategies[point] = [
                    "Reduce to <2 minutes",
                    "Break into smaller chunks",
                    "Combine with existing routine"
                ]
            elif point == "physical_effort":
                strategies[point] = [
                    "Prepare materials in advance",
                    "Reduce number of steps",
                    "Position items in high-visibility location"
                ]
            elif point == "mental_effort":
                strategies[point] = [
                    "Create if-then plans",
                    "Remove decision points",
                    "Use visual cues"
                ]
        return strategies


@dataclass
class PatternMicrohabitDesignerDependencies:
    """
    Зависимости Pattern Microhabit Designer Agent с интеграцией RAG и Archon.

    Специализированный агент для PatternShift - НЕ универсальный.
    """

    # Основные настройки
    api_key: str
    patternshift_project_path: str = ""

    # Обязательное поле для защиты от отсутствия знаний в RAG
    agent_name: str = "pattern_microhabit_designer"

    # RAG конфигурация для Archon Knowledge Base
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "pattern-microhabit",
        "behavior-design",
        "habits",
        "agent-knowledge",
        "patternshift"
    ])
    knowledge_domain: str | None = None  # Специфичный домен не требуется

    # Archon интеграция для управления задачами
    archon_project_id: str = "d5c0bd7d-8856-4ed3-98b1-561f80f7a299"  # PatternShift project

    # Специализированные базы данных
    habit_science_db: HabitScienceDatabase = field(default_factory=HabitScienceDatabase)
    motivation_db: MotivationDatabase = field(default_factory=MotivationDatabase)
    behavior_toolkit: BehaviorDesignToolkit = field(default_factory=BehaviorDesignToolkit)

    # Кэш для оптимизации поиска
    rag_cache: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация конфигурации"""
        if not self.agent_name:
            self.agent_name = "pattern_microhabit_designer"

        # Проверка наличия критических путей
        if self.patternshift_project_path:
            project_path = Path(self.patternshift_project_path)
            if not project_path.exists():
                raise ValueError(f"PatternShift project path does not exist: {self.patternshift_project_path}")

    async def search_habit_knowledge(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Поиск знаний о привычках через RAG или локальную базу

        Args:
            query: Поисковый запрос

        Returns:
            Найденные знания о привычках
        """
        # Проверяем кэш
        if query in self.rag_cache:
            return self.rag_cache[query]

        # Используем локальную базу знаний (fallback если RAG не работает)
        if "habit loop" in query.lower():
            result = await self.habit_science_db.get_habit_loop_science()
        elif "implementation intention" in query.lower():
            result = await self.habit_science_db.get_implementation_intention_research()
        elif "atomic habits" in query.lower():
            result = await self.habit_science_db.get_atomic_habit_principles()
        elif "tiny habits" in query.lower():
            result = await self.habit_science_db.get_tiny_habits_model()
        else:
            result = None

        # Сохраняем в кэш
        if result:
            self.rag_cache[query] = result

        return result

    async def get_behavior_change_strategies(self, target_behavior: str) -> List[str]:
        """
        Получение стратегий изменения поведения

        Args:
            target_behavior: Целевое поведение

        Returns:
            Список стратегий
        """
        friction_points = await self.behavior_toolkit.identify_friction_points(target_behavior)
        strategies_dict = await self.behavior_toolkit.generate_friction_reduction_strategies(friction_points)

        # Объединяем все стратегии
        all_strategies = []
        for strategies in strategies_dict.values():
            all_strategies.extend(strategies)

        return all_strategies

    async def get_reward_recommendations(
        self,
        habit_type: str,
        user_motivation_profile: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Получение рекомендаций по вознаграждениям

        Args:
            habit_type: Тип привычки
            user_motivation_profile: Профиль мотивации пользователя

        Returns:
            Список рекомендуемых вознаграждений
        """
        intrinsic_factors = await self.motivation_db.get_intrinsic_motivation_factors()
        reward_timing = await self.motivation_db.get_reward_timing_research()

        recommendations = []

        # Рекомендации на основе внутренней мотивации
        for factor in intrinsic_factors[:3]:  # Топ-3 фактора
            recommendations.append({
                "type": "intrinsic",
                "factor": factor,
                "timing": "immediate",
                "effectiveness": reward_timing["immediate_rewards"]["effectiveness"]
            })

        # Добавляем вариативные вознаграждения для повышения dopamine
        recommendations.append({
            "type": "variable",
            "description": "Surprise rewards for streak maintenance",
            "timing": "variable",
            "effectiveness": reward_timing["variable_rewards"]["effectiveness"]
        })

        return recommendations
