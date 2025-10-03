"""
Pydantic модели данных для Pattern Feedback Orchestrator Agent
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    """Типы вопросов обратной связи"""
    LIKERT_SCALE = "likert_scale"  # Шкала Лайкерта (1-5, 1-7, 1-10)
    YES_NO = "yes_no"  # Да/Нет
    OPEN_TEXT = "open_text"  # Открытый текст
    MULTIPLE_CHOICE = "multiple_choice"  # Множественный выбор
    SLIDER = "slider"  # Слайдер
    RATING = "rating"  # Рейтинг
    NPS = "nps"  # Net Promoter Score


class ResponseScaleType(str, Enum):
    """Типы шкал ответов"""
    NUMERIC = "numeric"  # Числовая (1-10)
    AGREEMENT = "agreement"  # Согласие (полностью не согласен - полностью согласен)
    FREQUENCY = "frequency"  # Частота (никогда - всегда)
    SATISFACTION = "satisfaction"  # Удовлетворенность
    IMPROVEMENT = "improvement"  # Улучшение (хуже - лучше)
    DIFFICULTY = "difficulty"  # Сложность (очень легко - очень сложно)


class FeedbackPurpose(str, Enum):
    """Цель сбора обратной связи"""
    PROGRESS_TRACKING = "progress_tracking"  # Отслеживание прогресса
    SATISFACTION = "satisfaction"  # Удовлетворенность
    ENGAGEMENT = "engagement"  # Вовлеченность
    DIFFICULTY_ASSESSMENT = "difficulty_assessment"  # Оценка сложности
    CRISIS_DETECTION = "crisis_detection"  # Детекция кризисных состояний
    CONTENT_QUALITY = "content_quality"  # Качество контента
    BEHAVIORAL_CHANGE = "behavioral_change"  # Поведенческие изменения


class TriggerAction(str, Enum):
    """Действия по триггерам"""
    SEND_SUPPORT_MESSAGE = "send_support_message"  # Отправить поддерживающее сообщение
    ADJUST_DIFFICULTY = "adjust_difficulty"  # Скорректировать сложность
    ESCALATE_TO_PROFESSIONAL = "escalate_to_professional"  # Эскалация к профессионалу
    OFFER_ALTERNATIVE_PATH = "offer_alternative_path"  # Предложить альтернативный путь
    PROVIDE_ADDITIONAL_RESOURCES = "provide_additional_resources"  # Предоставить дополнительные ресурсы
    CELEBRATE_SUCCESS = "celebrate_success"  # Празднование успеха


class FeedbackQuestion(BaseModel):
    """Вопрос обратной связи"""
    id: str = Field(..., description="Уникальный ID вопроса")
    question_text: str = Field(..., description="Текст вопроса")
    question_type: QuestionType
    purpose: FeedbackPurpose

    # Параметры шкалы
    scale_type: Optional[ResponseScaleType] = None
    scale_min: Optional[int] = Field(None, ge=0, le=10)
    scale_max: Optional[int] = Field(None, ge=1, le=10)
    scale_labels: Optional[Dict[int, str]] = Field(default_factory=dict, description="Подписи для значений шкалы")

    # Варианты ответов для multiple choice
    choices: Optional[List[str]] = Field(default_factory=list)

    # Параметры валидации
    required: bool = Field(default=True, description="Обязательность ответа")
    min_length: Optional[int] = Field(None, description="Минимальная длина текстового ответа")
    max_length: Optional[int] = Field(None, description="Максимальная длина текстового ответа")

    # Терапевтический эффект
    therapeutic_intent: Optional[str] = Field(None, description="Терапевтическое намерение вопроса")
    reflection_prompt: Optional[str] = Field(None, description="Промпт для рефлексии")


class TriggerRule(BaseModel):
    """Правило триггера на основе ответа"""
    rule_id: str
    question_id: str = Field(..., description="ID вопроса")

    # Условие срабатывания
    condition: str = Field(..., description="Условие (например: 'score <= 3')")
    priority: int = Field(default=5, ge=1, le=10, description="Приоритет правила")

    # Действие
    action: TriggerAction
    action_params: Dict[str, Any] = Field(default_factory=dict)

    # Описание
    description: str = Field(..., description="Описание что делает правило")


class FeedbackForm(BaseModel):
    """Форма обратной связи"""
    form_id: str
    title: str = Field(..., description="Название формы")
    description: str = Field(..., description="Описание цели формы")

    # Вопросы
    questions: List[FeedbackQuestion] = Field(default_factory=list)

    # Триггерные правила
    trigger_rules: List[TriggerRule] = Field(default_factory=list)

    # Метаданные
    target_day: Optional[int] = Field(None, ge=1, le=28, description="День программы")
    target_module: Optional[str] = Field(None, description="Целевой модуль")
    estimated_completion_time: int = Field(default=3, ge=1, le=10, description="Время заполнения (минуты)")

    # Параметры отображения
    show_progress: bool = Field(default=True, description="Показывать прогресс заполнения")
    allow_skip: bool = Field(default=False, description="Разрешить пропуск вопросов")
    anonymous: bool = Field(default=False, description="Анонимная форма")


class FeedbackResponse(BaseModel):
    """Ответ на форму обратной связи"""
    response_id: str
    form_id: str
    user_id: Optional[str] = None

    # Ответы
    answers: Dict[str, Union[int, str, List[str]]] = Field(default_factory=dict, description="ID вопроса → ответ")

    # Метаданные
    completed_at: Optional[str] = None
    completion_time_seconds: Optional[int] = None

    # Анализ
    triggered_rules: List[str] = Field(default_factory=list, description="Сработавшие правила")
    detected_patterns: Dict[str, Any] = Field(default_factory=dict, description="Обнаруженные паттерны")
    risk_level: Optional[str] = Field(None, description="Уровень риска: low/medium/high/critical")


class FeedbackAnalytics(BaseModel):
    """Аналитика по обратной связи"""
    form_id: str
    total_responses: int = 0

    # Статистика по вопросам
    question_stats: Dict[str, Dict[str, Any]] = Field(default_factory=dict)

    # Паттерны
    common_patterns: List[str] = Field(default_factory=list)
    risk_indicators: List[str] = Field(default_factory=list)

    # Метрики
    avg_completion_time: Optional[float] = None
    completion_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    satisfaction_score: Optional[float] = None


class FeedbackModule(BaseModel):
    """Модуль обратной связи для PatternShift"""
    module_id: str
    module_version: str = Field(default="1.0.0")

    # Метаданные
    title: str = Field(..., description="Заголовок модуля")
    description: str = Field(..., description="Описание модуля")

    # Содержимое
    feedback_form: FeedbackForm

    # Интеграция с PatternShift
    target_phase: str = Field(default="development")
    target_day: Optional[int] = Field(None, ge=1, le=28)
    trigger_timing: str = Field(default="after_module", description="Когда показывать: before_module/after_module/end_of_day")

    # Адаптивность
    adaptive_rules: Dict[str, Any] = Field(default_factory=dict, description="Правила адаптации формы")

    # Метрики
    importance_score: float = Field(default=0.8, ge=0.0, le=1.0)
    expected_response_rate: float = Field(default=0.85, ge=0.0, le=1.0)


class CrisisIndicator(BaseModel):
    """Индикатор кризисного состояния"""
    indicator_id: str
    severity: str = Field(..., description="Уровень серьезности: low/medium/high/critical")

    # Паттерн детекции
    detection_pattern: str = Field(..., description="Паттерн ответов указывающий на кризис")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Уверенность в детекции")

    # Рекомендуемые действия
    recommended_actions: List[str] = Field(default_factory=list)
    escalation_required: bool = Field(default=False)

    # Ресурсы помощи
    support_resources: List[str] = Field(default_factory=list)
    emergency_contacts: Optional[str] = None


__all__ = [
    "QuestionType",
    "ResponseScaleType",
    "FeedbackPurpose",
    "TriggerAction",
    "FeedbackQuestion",
    "TriggerRule",
    "FeedbackForm",
    "FeedbackResponse",
    "FeedbackAnalytics",
    "FeedbackModule",
    "CrisisIndicator"
]
