"""
Pydantic модели данных для Pattern Microhabit Designer Agent
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class HabitTriggerType(str, Enum):
    """Типы триггеров для привычек"""
    TIME = "time"  # Временной триггер (после пробуждения, перед сном)
    LOCATION = "location"  # Локация (на работе, дома)
    EMOTION = "emotion"  # Эмоциональное состояние (стресс, радость)
    EXISTING_HABIT = "existing_habit"  # Существующая привычка (после чистки зубов)
    EVENT = "event"  # Событие (получение уведомления)


class RewardType(str, Enum):
    """Типы вознаграждений"""
    INTRINSIC = "intrinsic"  # Внутреннее (удовольствие от процесса)
    EXTRINSIC = "extrinsic"  # Внешнее (очки, достижения)
    SOCIAL = "social"  # Социальное (признание, одобрение)
    IMMEDIATE = "immediate"  # Немедленное (физическое удовольствие)
    DELAYED = "delayed"  # Отложенное (долгосрочный результат)


class DifficultyLevel(str, Enum):
    """Уровень сложности микропривычки"""
    MICRO = "micro"  # Микро: <30 секунд, не требует усилий
    EASY = "easy"  # Легкий: 1-2 минуты, минимальные усилия
    MEDIUM = "medium"  # Средний: 3-5 минут, умеренные усилия
    CHALLENGING = "challenging"  # Сложный: 5-10 минут, значительные усилия


class HabitChainPosition(str, Enum):
    """Позиция в цепочке привычек"""
    STANDALONE = "standalone"  # Отдельная привычка
    ANCHOR = "anchor"  # Якорная привычка (первая в цепи)
    LINKED = "linked"  # Связанная привычка (в середине цепи)
    CAPSTONE = "capstone"  # Завершающая привычка (последняя в цепи)


class MicrohabitTrigger(BaseModel):
    """Триггер для микропривычки"""
    type: HabitTriggerType
    description: str = Field(..., description="Описание триггера")
    example: str = Field(..., description="Пример триггера")
    reliability_score: float = Field(default=0.8, ge=0.0, le=1.0, description="Надежность триггера")


class HabitReward(BaseModel):
    """Вознаграждение за выполнение привычки"""
    type: RewardType
    description: str = Field(..., description="Описание вознаграждения")
    effectiveness: float = Field(default=0.7, ge=0.0, le=1.0, description="Эффективность вознаграждения")
    immediate: bool = Field(default=True, description="Немедленное вознаграждение?")


class Microhabit(BaseModel):
    """Микропривычка"""
    id: str = Field(..., description="Уникальный ID микропривычки")
    name: str = Field(..., description="Название микропривычки")
    description: str = Field(..., description="Детальное описание")
    difficulty: DifficultyLevel
    duration_seconds: int = Field(..., ge=5, le=600, description="Длительность выполнения в секундах")

    # Триггеры и вознаграждения
    triggers: List[MicrohabitTrigger] = Field(default_factory=list)
    rewards: List[HabitReward] = Field(default_factory=list)

    # Барьеры и мотиваторы
    barriers: List[str] = Field(default_factory=list, description="Потенциальные барьеры")
    motivators: List[str] = Field(default_factory=list, description="Мотивационные факторы")

    # Цепочки привычек
    chain_position: HabitChainPosition = HabitChainPosition.STANDALONE
    linked_habit_id: Optional[str] = Field(None, description="ID связанной привычки в цепи")

    # Метрики
    measurable: bool = Field(default=True, description="Измеримость выполнения")
    success_criteria: str = Field(..., description="Критерии успешного выполнения")
    estimated_impact: float = Field(default=0.5, ge=0.0, le=1.0, description="Оценочное влияние на цель")


class HabitChain(BaseModel):
    """Цепочка взаимосвязанных привычек (domino effect)"""
    chain_id: str
    name: str = Field(..., description="Название цепочки")
    description: str = Field(..., description="Описание цепочки и её эффекта")
    habits: List[Microhabit] = Field(default_factory=list)
    total_duration_seconds: int = Field(default=0)
    cumulative_impact: float = Field(default=0.0, ge=0.0, le=1.0)


class BehaviorChangeGoal(BaseModel):
    """Цель поведенческого изменения"""
    goal_id: str
    description: str = Field(..., description="Описание целевого изменения")
    target_behavior: str = Field(..., description="Целевое поведение")
    current_state: str = Field(..., description="Текущее состояние")
    desired_state: str = Field(..., description="Желаемое состояние")
    timeframe_days: int = Field(default=21, ge=7, le=90)


class MicrohabitDesignRequest(BaseModel):
    """Запрос на дизайн микропривычки"""
    goal: BehaviorChangeGoal
    user_context: Dict[str, Any] = Field(default_factory=dict, description="Контекст пользователя")
    existing_routines: List[str] = Field(default_factory=list)
    available_time_minutes: int = Field(default=5, ge=1, le=60)
    difficulty_preference: DifficultyLevel = DifficultyLevel.MICRO


class MicrohabitDesignResponse(BaseModel):
    """Ответ с дизайном микропривычки"""
    request_id: str
    microhabits: List[Microhabit] = Field(default_factory=list)
    recommended_chains: List[HabitChain] = Field(default_factory=list)
    implementation_plan: str = Field(..., description="План внедрения")
    success_probability: float = Field(default=0.7, ge=0.0, le=1.0)
    estimated_results: str = Field(..., description="Ожидаемые результаты")


class HabitProgressTracking(BaseModel):
    """Отслеживание прогресса привычки"""
    habit_id: str
    days_completed: int = Field(default=0)
    total_days: int = Field(default=21)
    completion_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    current_streak: int = Field(default=0)
    longest_streak: int = Field(default=0)
    barriers_encountered: List[str] = Field(default_factory=list)
    adjustments_made: List[str] = Field(default_factory=list)


class MicrohabitModule(BaseModel):
    """Модуль микропривычки для PatternShift"""
    module_id: str
    module_version: str = Field(default="1.0.0", description="Версия модуля (semver)")

    # Метаданные модуля
    title: str = Field(..., description="Заголовок модуля")
    description: str = Field(..., description="Описание модуля")

    # Содержимое
    microhabits: List[Microhabit] = Field(default_factory=list)
    chains: List[HabitChain] = Field(default_factory=list)

    # Интеграция с PatternShift
    target_phase: str = Field(default="development", description="Целевая фаза программы")
    target_day: Optional[int] = Field(None, ge=1, le=28)
    session_slot: Optional[str] = Field(None, description="Слот сессии (morning/afternoon/evening)")

    # Варианты модуля
    variants: Dict[str, Any] = Field(default_factory=dict, description="Варианты модуля (vak/age/culture)")

    # Метрики
    estimated_completion_time: int = Field(..., description="Оценочное время выполнения (минуты)")
    difficulty_rating: DifficultyLevel
    therapeutic_value: float = Field(default=0.7, ge=0.0, le=1.0)
