"""
Модели данных для Pattern Test Architect Agent
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class DifficultyLevel(str, Enum):
    """Уровень сложности теста"""
    EASY = "easy"          # Простые вопросы для широкой аудитории
    MEDIUM = "medium"      # Средний уровень сложности
    HARD = "hard"          # Сложные вопросы для подготовленной аудитории


class TargetAudience(str, Enum):
    """Целевая аудитория теста"""
    GENERAL = "general"           # Широкая аудитория
    TEENS = "teens"              # Подростки 13-17 лет
    YOUNG_ADULTS = "young_adults" # Молодые взрослые 18-25
    ADULTS = "adults"            # Взрослые 26-45
    MATURE = "mature"            # Зрелые люди 45+
    PROFESSIONALS = "professionals" # Профессиональная аудитория
    STUDENTS = "students"        # Студенты


class QuestionType(str, Enum):
    """Тип вопроса в тесте"""
    LIKERT_5 = "likert_5"        # 5-балльная шкала Ликерта
    LIKERT_7 = "likert_7"        # 7-балльная шкала Ликерта
    YES_NO = "yes_no"            # Да/Нет
    MULTIPLE_CHOICE = "multiple_choice"  # Множественный выбор
    RANKING = "ranking"          # Ранжирование
    SLIDER = "slider"           # Слайдер (0-100)


class PsychologicalConstruct(str, Enum):
    """Психологические конструкты для измерения"""
    DEPRESSION = "depression"
    ANXIETY = "anxiety"
    STRESS = "stress"
    SELF_ESTEEM = "self_esteem"
    PERSONALITY_BIG5 = "personality_big5"
    ATTACHMENT_STYLE = "attachment_style"
    COMMUNICATION_STYLE = "communication_style"
    LOVE_LANGUAGES = "love_languages"
    EGO_STATES = "ego_states"
    CODEPENDENCY = "codependency"
    DRAMA_TRIANGLE = "drama_triangle"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    PERFECTIONISM = "perfectionism"
    PROCRASTINATION = "procrastination"
    ASSERTIVENESS = "assertiveness"
    STRESS_MANAGEMENT = "stress_management"


class TestRequest(BaseModel):
    """Запрос на создание психологического теста"""

    viral_name: str = Field(
        description="Вирусное название теста (например: 'Почему у тебя не складываются отношения?')"
    )

    academic_name: Optional[str] = Field(
        default=None,
        description="Академическое название базовой методики"
    )

    base_methodology: str = Field(
        description="Базовая научная методика (PHQ-9, GAD-7, DASS-21, Big Five и т.д.)"
    )

    psychological_construct: PsychologicalConstruct = Field(
        description="Психологический конструкт для измерения"
    )

    target_audience: TargetAudience = Field(
        default=TargetAudience.GENERAL,
        description="Целевая аудитория теста"
    )

    question_count: int = Field(
        default=15,
        ge=5,
        le=50,
        description="Количество вопросов в тесте"
    )

    difficulty_level: DifficultyLevel = Field(
        default=DifficultyLevel.MEDIUM,
        description="Уровень сложности вопросов"
    )

    result_ranges: int = Field(
        default=5,
        ge=3,
        le=10,
        description="Количество диапазонов результатов (уровней)"
    )

    linked_programs: List[str] = Field(
        default_factory=list,
        description="Связанные программы трансформации"
    )

    desired_emotional_hook: Optional[str] = Field(
        default=None,
        description="Желаемый эмоциональный крючок"
    )

    target_metrics: Dict[str, float] = Field(
        default_factory=dict,
        description="Целевые метрики эффективности"
    )


class TestQuestion(BaseModel):
    """Вопрос психологического теста"""

    id: int = Field(description="Идентификатор вопроса")

    text: str = Field(description="Текст вопроса")

    question_type: QuestionType = Field(description="Тип вопроса")

    options: Optional[List[str]] = Field(
        default=None,
        description="Варианты ответов (для множественного выбора)"
    )

    scale_labels: Optional[Dict[str, str]] = Field(
        default=None,
        description="Подписи к точкам шкалы"
    )

    reverse_scored: bool = Field(
        default=False,
        description="Обратная оценка (для валидации)"
    )

    weight: float = Field(
        default=1.0,
        description="Вес вопроса в общем счете"
    )

    construct_facet: Optional[str] = Field(
        default=None,
        description="Аспект конструкта, который измеряет вопрос"
    )

    clarity_score: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Оценка ясности вопроса"
    )


class InterpretationScale(BaseModel):
    """Шкала интерпретации результатов"""

    level: str = Field(description="Уровень (низкий, средний, высокий и т.д.)")

    score_range: tuple[float, float] = Field(
        description="Диапазон баллов для этого уровня"
    )

    title: str = Field(description="Заголовок интерпретации")

    description: str = Field(description="Описание результата")

    recommendations: List[str] = Field(
        description="Рекомендации для этого уровня"
    )

    linked_programs: List[str] = Field(
        default_factory=list,
        description="Связанные программы трансформации"
    )

    color_code: str = Field(
        default="#808080",
        description="Цветовой код для визуализации"
    )


class PsychometricValidation(BaseModel):
    """Психометрическая валидация теста"""

    is_valid: bool = Field(description="Валиден ли тест")

    validity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Оценка валидности (0-1)"
    )

    reliability_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Оценка надежности (0-1)"
    )

    construct_validity: float = Field(
        ge=0.0,
        le=1.0,
        description="Конструктная валидность"
    )

    content_validity: float = Field(
        ge=0.0,
        le=1.0,
        description="Содержательная валидность"
    )

    criterion_validity: float = Field(
        ge=0.0,
        le=1.0,
        description="Критериальная валидность"
    )

    internal_consistency: float = Field(
        ge=0.0,
        le=1.0,
        description="Внутренняя согласованность (альфа Кронбаха)"
    )

    test_retest_reliability: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Ретестовая надежность"
    )

    issues: List[str] = Field(
        default_factory=list,
        description="Выявленные проблемы валидации"
    )

    ethical_compliance: bool = Field(
        default=True,
        description="Соответствие этическим стандартам"
    )


class ViralTestTransformation(BaseModel):
    """Трансформация академического теста в вирусный"""

    original_name: str = Field(description="Исходное академическое название")

    viral_name: str = Field(description="Вирусное название")

    emotional_hook: str = Field(description="Эмоциональный крючок")

    target_pain_point: str = Field(description="Целевая болевая точка")

    language_style: str = Field(description="Стиль языка (разговорный, простой и т.д.)")

    expected_engagement: float = Field(
        ge=0.0,
        le=1.0,
        description="Ожидаемый уровень вовлеченности"
    )

    viral_potential_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Оценка вирусного потенциала"
    )


class EffectivenessAnalysis(BaseModel):
    """Анализ эффективности теста"""

    completion_rate_prediction: float = Field(
        ge=0.0,
        le=1.0,
        description="Прогноз процента завершения теста"
    )

    viral_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Оценка вирусности"
    )

    engagement_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Оценка вовлеченности"
    )

    transformation_potential: float = Field(
        ge=0.0,
        le=1.0,
        description="Потенциал для трансформации"
    )

    predicted_shares: int = Field(
        default=0,
        description="Прогноз количества репостов"
    )

    predicted_completions: int = Field(
        default=0,
        description="Прогноз количества завершений"
    )

    bottlenecks: List[str] = Field(
        default_factory=list,
        description="Потенциальные узкие места"
    )


class TestResult(BaseModel):
    """Результат прохождения теста"""

    user_id: str = Field(description="Идентификатор пользователя")

    test_id: str = Field(description="Идентификатор теста")

    raw_score: float = Field(description="Сырой балл")

    normalized_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Нормализованный балл (0-1)"
    )

    level: str = Field(description="Уровень результата")

    interpretation: InterpretationScale = Field(
        description="Интерпретация результата"
    )

    completion_time: int = Field(description="Время прохождения в секундах")

    answers: Dict[int, Any] = Field(description="Ответы на вопросы")

    recommended_programs: List[str] = Field(
        default_factory=list,
        description="Рекомендованные программы"
    )

    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Уверенность в результате"
    )


class TestResponse(BaseModel):
    """Ответ с готовым психологическим тестом"""

    viral_name: str = Field(description="Вирусное название теста")

    academic_base: str = Field(description="Академическая основа")

    questions: List[TestQuestion] = Field(description="Вопросы теста")

    interpretation_scales: List[InterpretationScale] = Field(
        description="Шкалы интерпретации"
    )

    psychometric_validation: PsychometricValidation = Field(
        description="Психометрическая валидация"
    )

    effectiveness_analysis: EffectivenessAnalysis = Field(
        description="Анализ эффективности"
    )

    linked_transformation_programs: List[str] = Field(
        description="Связанные программы трансформации"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Метаданные теста"
    )

    estimated_completion_time: int = Field(
        description="Оценочное время прохождения в секундах"
    )