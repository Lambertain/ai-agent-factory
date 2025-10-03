"""
Модели данных для Pattern Progress Narrator Agent
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class NarrativeType(str, Enum):
    """Типы нарративов прогресса"""
    HERO_JOURNEY = "hero_journey"  # Путь героя
    TRANSFORMATION = "transformation"  # Трансформационный нарратив
    MILESTONE_CELEBRATION = "milestone_celebration"  # Празднование вех
    OVERCOMING_CHALLENGE = "overcoming_challenge"  # Преодоление препятствий
    MOMENTUM_BUILDING = "momentum_building"  # Наращивание импульса
    REFLECTION = "reflection"  # Рефлексивный нарратив


class EmotionalTone(str, Enum):
    """Эмоциональный тон сообщения"""
    ENCOURAGING = "encouraging"  # Ободряющий
    CELEBRATORY = "celebratory"  # Праздничный
    REFLECTIVE = "reflective"  # Рефлексивный
    MOTIVATING = "motivating"  # Мотивирующий
    SUPPORTIVE = "supportive"  # Поддерживающий
    INSPIRING = "inspiring"  # Вдохновляющий


class ProgressMetric(BaseModel):
    """Метрика прогресса пользователя"""
    metric_id: str = Field(..., description="ID метрики")
    metric_name: str = Field(..., description="Название метрики")
    current_value: float = Field(..., description="Текущее значение")
    previous_value: Optional[float] = Field(None, description="Предыдущее значение")
    baseline_value: Optional[float] = Field(None, description="Базовое значение")
    improvement_percentage: Optional[float] = Field(None, description="Процент улучшения")
    trend: str = Field(default="stable", description="Тренд: improving, stable, declining")


class UserMilestone(BaseModel):
    """Веха в пути пользователя"""
    milestone_id: str = Field(..., description="ID вехи")
    milestone_type: str = Field(..., description="Тип вехи")
    description: str = Field(..., description="Описание вехи")
    achieved_at: datetime = Field(..., description="Когда достигнута")
    significance_level: int = Field(default=5, ge=1, le=10, description="Уровень значимости 1-10")
    celebration_message: Optional[str] = Field(None, description="Сообщение празднования")


class ProgressNarrative(BaseModel):
    """Нарратив прогресса"""
    narrative_id: str = Field(..., description="ID нарратива")
    narrative_type: NarrativeType = Field(..., description="Тип нарратива")
    title: str = Field(..., description="Заголовок нарратива")
    body: str = Field(..., description="Основной текст нарратива")
    emotional_tone: EmotionalTone = Field(..., description="Эмоциональный тон")

    # Персонализация
    user_name: Optional[str] = Field(None, description="Имя пользователя")
    personalization_data: Dict[str, Any] = Field(default_factory=dict, description="Данные персонализации")

    # Метафоры и образы
    metaphor_used: Optional[str] = Field(None, description="Использованная метафора")
    archetypal_image: Optional[str] = Field(None, description="Архетипический образ")

    # Действие
    next_step: Optional[str] = Field(None, description="Следующий конкретный шаг")
    call_to_action: Optional[str] = Field(None, description="Призыв к действию")

    # Контекст
    day_number: int = Field(..., ge=1, le=21, description="День программы")
    progress_metrics: List[ProgressMetric] = Field(default_factory=list, description="Метрики прогресса")
    milestones: List[UserMilestone] = Field(default_factory=list, description="Достигнутые вехи")


class ChallengeReframe(BaseModel):
    """Рефрейминг вызова/неудачи"""
    challenge_id: str = Field(..., description="ID вызова")
    original_frame: str = Field(..., description="Оригинальная формулировка")
    reframed_as: str = Field(..., description="Рефреймированная формулировка")
    learning_extracted: str = Field(..., description="Извлеченное научение")
    growth_opportunity: str = Field(..., description="Возможность роста")


class MomentumIndicators(BaseModel):
    """Индикаторы импульса прогресса"""
    consistency_score: float = Field(..., ge=0, le=1, description="Оценка последовательности 0-1")
    engagement_level: float = Field(..., ge=0, le=1, description="Уровень вовлеченности 0-1")
    completion_rate: float = Field(..., ge=0, le=1, description="Процент завершения 0-1")

    # Качественные индикаторы
    positive_trend: bool = Field(default=True, description="Позитивный тренд")
    acceleration_detected: bool = Field(default=False, description="Обнаружено ускорение")
    plateau_risk: bool = Field(default=False, description="Риск плато")

    # Рекомендации
    momentum_message: str = Field(..., description="Сообщение о импульсе")
    recommended_action: Optional[str] = Field(None, description="Рекомендуемое действие")


class HeroJourneyStage(str, Enum):
    """Этапы пути героя (Joseph Campbell)"""
    ORDINARY_WORLD = "ordinary_world"  # Обычный мир
    CALL_TO_ADVENTURE = "call_to_adventure"  # Зов к приключению
    REFUSAL_OF_CALL = "refusal_of_call"  # Отказ от зова
    MEETING_MENTOR = "meeting_mentor"  # Встреча с наставником
    CROSSING_THRESHOLD = "crossing_threshold"  # Пересечение порога
    TESTS_ALLIES_ENEMIES = "tests_allies_enemies"  # Испытания, союзники, враги
    APPROACH_INMOST_CAVE = "approach_inmost_cave"  # Приближение к сокровенной пещере
    ORDEAL = "ordeal"  # Испытание
    REWARD = "reward"  # Награда
    ROAD_BACK = "road_back"  # Дорога назад
    RESURRECTION = "resurrection"  # Воскрешение
    RETURN_WITH_ELIXIR = "return_with_elixir"  # Возвращение с эликсиром


class TransformationJourneyMap(BaseModel):
    """Карта трансформационного путешествия"""
    user_id: str = Field(..., description="ID пользователя")
    current_stage: HeroJourneyStage = Field(..., description="Текущий этап пути героя")
    day_number: int = Field(..., ge=1, le=21, description="День программы")

    # Достижения
    completed_stages: List[HeroJourneyStage] = Field(default_factory=list, description="Завершенные этапы")
    milestones_achieved: List[UserMilestone] = Field(default_factory=list, description="Достигнутые вехи")

    # Прогресс
    progress_metrics: List[ProgressMetric] = Field(default_factory=list, description="Метрики прогресса")
    momentum_indicators: Optional[MomentumIndicators] = Field(None, description="Индикаторы импульса")

    # Нарратив
    personal_story: str = Field(..., description="Персональная история трансформации")
    key_insights: List[str] = Field(default_factory=list, description="Ключевые инсайты")
    challenges_reframed: List[ChallengeReframe] = Field(default_factory=list, description="Рефреймированные вызовы")

    # Следующие шаги
    next_milestone: Optional[str] = Field(None, description="Следующая веха")
    anticipation_builder: Optional[str] = Field(None, description="Создание предвкушения")


__all__ = [
    "NarrativeType",
    "EmotionalTone",
    "ProgressMetric",
    "UserMilestone",
    "ProgressNarrative",
    "ChallengeReframe",
    "MomentumIndicators",
    "HeroJourneyStage",
    "TransformationJourneyMap"
]
