"""
Pydantic модели для Pattern Transition Craftsman Agent.

Модели для создания переходов между модулями программы трансформации.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TransitionType(str, Enum):
    """Типы переходов между модулями."""
    INTRO_TO_MAIN = "intro_to_main"  # Вводная часть -> основной модуль
    MAIN_TO_REFLECTION = "main_to_reflection"  # Основная часть -> рефлексия
    REFLECTION_TO_INTEGRATION = "reflection_to_integration"  # Рефлексия -> интеграция
    INTEGRATION_TO_NEXT = "integration_to_next"  # Интеграция -> следующий день
    DAY_TO_DAY = "day_to_day"  # Между днями программы
    WEEK_TO_WEEK = "week_to_week"  # Между неделями программы
    ACTIVITY_TO_ACTIVITY = "activity_to_activity"  # Между активностями внутри модуля
    TECHNIQUE_TO_EXERCISE = "technique_to_exercise"  # Техника -> упражнение
    EXERCISE_TO_FEEDBACK = "exercise_to_feedback"  # Упражнение -> обратная связь


class EnergyLevel(str, Enum):
    """Уровни энергии в переходе."""
    CALM = "calm"  # Успокаивающий переход
    NEUTRAL = "neutral"  # Нейтральный переход
    ACTIVATING = "activating"  # Активирующий переход
    BUILDING = "building"  # Нарастающая энергия
    SUSTAINING = "sustaining"  # Поддерживающая энергия


class ModalityShift(str, Enum):
    """Смена модальности восприятия."""
    VISUAL_TO_AUDITORY = "visual_to_auditory"
    AUDITORY_TO_KINESTHETIC = "auditory_to_kinesthetic"
    KINESTHETIC_TO_VISUAL = "kinesthetic_to_visual"
    SAME_MODALITY = "same_modality"  # Без смены модальности
    MULTI_TO_SINGLE = "multi_to_single"  # Мультисенсорный -> одна модальность
    SINGLE_TO_MULTI = "single_to_multi"  # Одна модальность -> мультисенсорный


class AnchorType(str, Enum):
    """Типы якорей для преемственности."""
    METAPHOR = "metaphor"  # Метафора из предыдущего модуля
    ACHIEVEMENT = "achievement"  # Отсылка к достижению
    INSIGHT = "insight"  # Инсайт из предыдущего опыта
    EMOTION = "emotion"  # Эмоциональное состояние
    SYMBOL = "symbol"  # Символ или образ
    PHRASE = "phrase"  # Ключевая фраза


class TransitionElement(BaseModel):
    """Элемент перехода между модулями."""
    element_id: str
    element_type: str  # "bridge", "anchor", "energizer", "primer", "summary"
    content: str
    duration_seconds: int = Field(default=30)
    purpose: str
    optional: bool = Field(default=False)


class ModuleTransition(BaseModel):
    """Переход между модулями программы."""
    transition_id: str
    from_module_id: str
    from_module_name: str
    to_module_id: str
    to_module_name: str
    transition_type: TransitionType
    energy_shift: EnergyLevel
    modality_shift: Optional[ModalityShift] = None

    # Содержание перехода
    transition_text: str
    elements: List[TransitionElement] = Field(default_factory=list)

    # Преемственность
    anchors_from_previous: List[str] = Field(default_factory=list)
    primers_for_next: List[str] = Field(default_factory=list)

    # Метаданные
    estimated_duration_seconds: int = Field(default=60)
    therapeutic_purpose: str
    emotional_tone: str

    created_at: datetime = Field(default_factory=datetime.now)


class BridgeContent(BaseModel):
    """Контент моста между активностями."""
    bridge_id: str
    from_context: Dict[str, Any]  # Откуда идем (модуль, активность)
    to_context: Dict[str, Any]  # Куда идем

    # Мост
    bridge_text: str
    maintains_focus: bool = Field(default=True)
    preserves_emotion: bool = Field(default=True)

    # Якоря
    anchor_type: Optional[AnchorType] = None
    anchor_content: Optional[str] = None

    # Подготовка mind-set
    mindset_preparation: Optional[str] = None
    expectation_setting: Optional[str] = None


class CoherenceCheck(BaseModel):
    """Проверка связности переходов."""
    check_id: str
    program_id: str
    day_number: int

    # Результаты проверки
    flow_score: float = Field(ge=0.0, le=1.0)  # 0-1, насколько плавный flow
    coherence_issues: List[str] = Field(default_factory=list)
    emotional_continuity: bool
    anchor_usage: Dict[str, int] = Field(default_factory=dict)

    # Рекомендации
    recommendations: List[str] = Field(default_factory=list)
    suggested_fixes: List[str] = Field(default_factory=list)

    checked_at: datetime = Field(default_factory=datetime.now)


class EnergyTransition(BaseModel):
    """Переход энергетических состояний."""
    from_energy: EnergyLevel
    to_energy: EnergyLevel
    transition_technique: str
    transition_text: str
    duration_seconds: int = Field(default=45)

    # Техники перехода
    breath_work: bool = Field(default=False)
    movement: bool = Field(default=False)
    visualization: bool = Field(default=False)
    grounding: bool = Field(default=False)


class TransitionLibrary(BaseModel):
    """Библиотека готовых переходов."""
    library_id: str
    name: str
    description: str

    # Категории переходов
    by_type: Dict[TransitionType, List[str]] = Field(default_factory=dict)
    by_energy: Dict[EnergyLevel, List[str]] = Field(default_factory=dict)
    by_modality: Dict[ModalityShift, List[str]] = Field(default_factory=dict)

    # Готовые шаблоны
    templates: List[ModuleTransition] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class MicroIntervention(BaseModel):
    """Микро-интервенция в переходе."""
    intervention_id: str
    intervention_type: str  # "reframe", "anchor", "motivate", "validate", "prepare"
    trigger_context: str  # Когда применять
    intervention_text: str
    therapeutic_effect: str
    duration_seconds: int = Field(default=20)


class FlowAnalysis(BaseModel):
    """Анализ потока программы."""
    analysis_id: str
    program_id: str

    # Метрики flow
    overall_flow_score: float = Field(ge=0.0, le=1.0)
    transition_count: int
    average_transition_duration: float

    # Проблемные зоны
    jarring_transitions: List[str] = Field(default_factory=list)
    missing_bridges: List[str] = Field(default_factory=list)
    energy_mismatches: List[str] = Field(default_factory=list)

    # Сильные стороны
    smooth_transitions: List[str] = Field(default_factory=list)
    effective_anchors: List[str] = Field(default_factory=list)

    # Рекомендации
    improvement_suggestions: List[str] = Field(default_factory=list)

    analyzed_at: datetime = Field(default_factory=datetime.now)


__all__ = [
    "TransitionType",
    "EnergyLevel",
    "ModalityShift",
    "AnchorType",
    "TransitionElement",
    "ModuleTransition",
    "BridgeContent",
    "CoherenceCheck",
    "EnergyTransition",
    "TransitionLibrary",
    "MicroIntervention",
    "FlowAnalysis"
]
