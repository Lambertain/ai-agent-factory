"""
Pydantic модели данных для Pattern Exercise Architect Agent
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LearningChannel(str, Enum):
    """Каналы научения"""
    COGNITIVE = "cognitive"  # Когнитивный
    EMOTIONAL = "emotional"  # Эмоциональный
    SOMATIC = "somatic"  # Телесный/соматический
    SOCIAL = "social"  # Социальный


class ExerciseDifficulty(str, Enum):
    """Уровень сложности упражнения"""
    BEGINNER = "beginner"  # Начальный
    INTERMEDIATE = "intermediate"  # Средний
    ADVANCED = "advanced"  # Продвинутый
    EXPERT = "expert"  # Экспертный


class ExerciseType(str, Enum):
    """Тип упражнения"""
    NLP_TECHNIQUE = "nlp_technique"  # Закрепление НЛП техники
    INTEGRATION = "integration"  # Интеграция изменений
    EMBODIMENT = "embodiment"  # Воплощение опыта
    REFLECTION = "reflection"  # Рефлексия
    PRACTICE = "practice"  # Практическое применение


class CompletionCriteria(BaseModel):
    """Критерии выполнения упражнения"""
    description: str = Field(..., description="Описание критерия")
    measurable: bool = Field(default=True, description="Измеримость критерия")
    observable_signs: List[str] = Field(default_factory=list, description="Наблюдаемые признаки")
    self_check_questions: List[str] = Field(default_factory=list, description="Вопросы для самопроверки")


class ExerciseStep(BaseModel):
    """Шаг упражнения"""
    step_number: int = Field(..., ge=1)
    title: str = Field(..., description="Название шага")
    description: str = Field(..., description="Детальное описание")
    duration_minutes: int = Field(..., ge=1, le=60)
    instructions: List[str] = Field(default_factory=list)
    tips: List[str] = Field(default_factory=list, description="Подсказки для выполнения")
    common_mistakes: List[str] = Field(default_factory=list, description="Частые ошибки")


class TransformationalExercise(BaseModel):
    """Трансформационное упражнение"""
    id: str = Field(..., description="Уникальный ID упражнения")
    title: str = Field(..., description="Название упражнения")
    description: str = Field(..., description="Описание и цель")
    exercise_type: ExerciseType
    difficulty: ExerciseDifficulty

    # Каналы научения
    learning_channels: List[LearningChannel] = Field(default_factory=list)
    primary_channel: LearningChannel

    # Структура упражнения
    steps: List[ExerciseStep] = Field(default_factory=list)
    total_duration_minutes: int = Field(..., ge=5, le=90)

    # Критерии и проверка
    completion_criteria: List[CompletionCriteria] = Field(default_factory=list)
    self_check_mechanism: str = Field(..., description="Механизм самопроверки")

    # НЛП интеграция
    nlp_technique_integrated: Optional[str] = Field(None, description="Интегрированная НЛП техника")
    transformation_goal: str = Field(..., description="Цель трансформации")

    # Адаптация
    difficulty_variants: Dict[str, Any] = Field(default_factory=dict)
    context_variations: Dict[str, str] = Field(default_factory=dict)


class ExerciseVariant(BaseModel):
    """Вариант упражнения для разного контекста"""
    variant_id: str
    context: str = Field(..., description="Контекст выполнения (дом, работа, публично)")
    difficulty: ExerciseDifficulty
    adapted_steps: List[ExerciseStep] = Field(default_factory=list)
    special_considerations: List[str] = Field(default_factory=list)


class ExerciseSequence(BaseModel):
    """Последовательность упражнений"""
    sequence_id: str
    title: str = Field(..., description="Название последовательности")
    description: str = Field(..., description="Описание и цель последовательности")
    exercises: List[TransformationalExercise] = Field(default_factory=list)
    total_duration_minutes: int = Field(default=0)
    progression_logic: str = Field(..., description="Логика прогрессии сложности")


class ExerciseDesignRequest(BaseModel):
    """Запрос на дизайн упражнения"""
    goal: str = Field(..., description="Цель упражнения")
    nlp_technique: Optional[str] = Field(None, description="НЛП техника для закрепления")
    target_difficulty: ExerciseDifficulty = ExerciseDifficulty.INTERMEDIATE
    preferred_channels: List[LearningChannel] = Field(default_factory=list)
    available_time_minutes: int = Field(default=20, ge=5, le=90)
    context: str = Field(default="home", description="Контекст выполнения")


class ExerciseDesignResponse(BaseModel):
    """Ответ с дизайном упражнения"""
    request_id: str
    exercise: TransformationalExercise
    variants: List[ExerciseVariant] = Field(default_factory=list)
    integration_tips: List[str] = Field(default_factory=list)
    expected_outcomes: List[str] = Field(default_factory=list)


class ExerciseModule(BaseModel):
    """Модуль упражнения для PatternShift"""
    module_id: str
    module_version: str = Field(default="1.0.0")

    # Метаданные
    title: str = Field(..., description="Заголовок модуля")
    description: str = Field(..., description="Описание модуля")

    # Содержимое
    exercise: TransformationalExercise
    variants: List[ExerciseVariant] = Field(default_factory=list)

    # Интеграция с PatternShift
    target_phase: str = Field(default="development")
    target_day: Optional[int] = Field(None, ge=1, le=28)
    session_slot: Optional[str] = Field(None)

    # Варианты модуля
    vak_variants: Dict[str, Any] = Field(default_factory=dict)
    age_variants: Dict[str, Any] = Field(default_factory=dict)

    # Метрики
    estimated_completion_time: int = Field(..., description="Время выполнения (минуты)")
    difficulty_rating: ExerciseDifficulty
    therapeutic_value: float = Field(default=0.8, ge=0.0, le=1.0)
