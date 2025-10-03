"""
Pydantic модели для Pattern Gamification Architect Agent.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import uuid


class PlayerType(str, Enum):
    """Типы игроков по Bartle taxonomy."""
    ACHIEVER = "achiever"  # Ориентация на достижения
    EXPLORER = "explorer"  # Ориентация на исследование
    SOCIALIZER = "socializer"  # Ориентация на социальное взаимодействие
    KILLER = "killer"  # Ориентация на конкуренцию


class MotivationType(str, Enum):
    """Типы мотивации."""
    INTRINSIC = "intrinsic"  # Внутренняя мотивация
    EXTRINSIC = "extrinsic"  # Внешняя мотивация
    MIXED = "mixed"  # Смешанная


class AchievementType(str, Enum):
    """Типы достижений."""
    COMPLETION = "completion"  # За завершение задачи
    CONSISTENCY = "consistency"  # За регулярность
    MASTERY = "mastery"  # За мастерство/совершенство
    MILESTONE = "milestone"  # За прохождение вехи
    BREAKTHROUGH = "breakthrough"  # За прорыв/инсайт
    SOCIAL = "social"  # За социальное взаимодействие


class DifficultyLevel(str, Enum):
    """Уровни сложности."""
    TUTORIAL = "tutorial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class GameMechanic(BaseModel):
    """Игровая механика."""
    mechanic_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    mechanic_type: str  # points, badges, levels, challenges, quests
    trigger_conditions: List[str]
    rewards: List[str]
    therapeutic_goal: str  # Какую терапевтическую цель поддерживает
    player_types: List[PlayerType]  # Для каких типов игроков эффективна
    motivation_type: MotivationType


class Achievement(BaseModel):
    """Достижение (badge/trophy)."""
    achievement_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    achievement_type: AchievementType
    icon_description: str  # Описание визуального образа
    unlock_criteria: Dict[str, Any]  # Критерии открытия
    rarity: str  # common, rare, epic, legendary
    points_value: int
    therapeutic_meaning: str  # Что это достижение значит для трансформации
    celebration_message: str


class ProgressionPath(BaseModel):
    """Путь прогрессии."""
    path_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    path_name: str
    description: str
    levels: List[Dict[str, Any]]  # Уровни с требованиями и наградами
    player_type_affinity: PlayerType
    total_points_required: int
    therapeutic_arc: str  # Терапевтическая дуга развития


class Challenge(BaseModel):
    """Челлендж/квест."""
    challenge_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    difficulty: DifficultyLevel
    tasks: List[Dict[str, str]]  # Список задач с описанием
    time_limit: Optional[int] = None  # В днях, опционально
    rewards: List[str]
    therapeutic_focus: str
    success_criteria: Dict[str, Any]
    fallback_strategy: str  # Что делать если не получается


class PointSystem(BaseModel):
    """Система очков."""
    system_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    point_type: str  # experience, transformation, wisdom, courage
    earning_rules: Dict[str, int]  # action -> points
    spending_options: Optional[List[Dict[str, Any]]] = None
    level_thresholds: List[int]  # Пороги для перехода на уровни
    display_name: str
    therapeutic_meaning: str


class SocialElement(BaseModel):
    """Социальный элемент геймификации."""
    element_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    element_type: str  # sharing, co-op, competition, community
    description: str
    implementation: str  # Как реализовать
    safety_guidelines: List[str]  # Как избежать негативного сравнения
    therapeutic_value: str
    opt_in: bool = True  # Всегда опционально


class FeedbackLoop(BaseModel):
    """Петля обратной связи."""
    loop_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    trigger_event: str
    feedback_message: str
    feedback_type: str  # progress, encouragement, insight, celebration
    timing: str  # immediate, delayed, periodic
    personalization_rules: Dict[str, Any]


class GamificationSystem(BaseModel):
    """Комплексная система геймификации."""
    system_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    program_id: str  # ID программы PatternShift
    game_mechanics: List[GameMechanic]
    achievements: List[Achievement]
    progression_paths: List[ProgressionPath]
    challenges: List[Challenge]
    point_systems: List[PointSystem]
    social_elements: List[SocialElement]
    feedback_loops: List[FeedbackLoop]
    onboarding_flow: Dict[str, Any]  # Как вводить пользователя в систему
    balance_strategy: str  # Как балансировать сложность


class PlayerProfile(BaseModel):
    """Профиль игрока."""
    player_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    primary_player_type: PlayerType
    secondary_player_type: Optional[PlayerType] = None
    motivation_balance: Dict[MotivationType, float]  # Баланс мотиваций
    preferred_mechanics: List[str]
    engagement_patterns: Dict[str, Any]


__all__ = [
    "PlayerType",
    "MotivationType",
    "AchievementType",
    "DifficultyLevel",
    "GameMechanic",
    "Achievement",
    "ProgressionPath",
    "Challenge",
    "PointSystem",
    "SocialElement",
    "FeedbackLoop",
    "GamificationSystem",
    "PlayerProfile"
]
