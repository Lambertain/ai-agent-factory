"""
Pydantic модели для Pattern Integration Synthesizer Agent.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime


class PhaseType(str, Enum):
    """Типы фаз программы."""
    BEGINNING = "beginning"
    DEVELOPMENT = "development"
    INTEGRATION = "integration"


class SessionSlot(str, Enum):
    """Слоты сессий в течение дня."""
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"


class ActivityType(str, Enum):
    """Типы активностей."""
    TECHNIQUE = "technique"
    EXERCISE = "exercise"
    HYPNOSIS = "hypnosis"
    FEEDBACK = "feedback"
    EDUCATION = "education"
    TRANSITION = "transition"


class EmotionalCurveStage(str, Enum):
    """Этапы эмоциональной кривой."""
    EXCITEMENT = "excitement"
    RESISTANCE = "resistance"
    BREAKTHROUGH = "breakthrough"
    INTEGRATION = "integration"
    MASTERY = "mastery"


class SynergyLevel(str, Enum):
    """Уровни синергии между модулями."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    CONFLICTING = "conflicting"


# ===== БАЗОВЫЕ МОДЕЛИ =====

class ModuleReference(BaseModel):
    """Ссылка на модуль контента."""
    module_id: str
    module_name: str
    module_type: str
    version: str = "1.0.0"
    duration_minutes: int


class Activity(BaseModel):
    """Активность в сессии."""
    activity_id: str
    activity_type: ActivityType
    module: ModuleReference
    order: int
    transition_before: Optional[str] = None
    transition_after: Optional[str] = None


class Session(BaseModel):
    """Сессия в дне."""
    session_id: str
    day_number: int
    slot: SessionSlot
    activities: List[Activity]
    total_duration_minutes: int
    theme: str


class Day(BaseModel):
    """День в программе."""
    day_number: int
    phase: PhaseType
    sessions: List[Session]
    daily_theme: str
    emotional_stage: EmotionalCurveStage


class Phase(BaseModel):
    """Фаза программы."""
    phase_type: PhaseType
    phase_name: str
    days: List[Day]
    phase_goals: List[str]
    duration_days: int


class Program(BaseModel):
    """Полная программа трансформации."""
    program_id: str
    program_name: str
    total_days: int
    phases: List[Phase]
    target_conditions: List[str]
    overall_goals: List[str]


# ===== АНАЛИЗ И СИНЕРГИЯ =====

class ModuleSynergy(BaseModel):
    """Анализ синергии между модулями."""
    module_a_id: str
    module_b_id: str
    synergy_level: SynergyLevel
    synergy_description: str
    recommended_sequence: Optional[str] = None
    recommended_gap: Optional[int] = None  # в днях


class ResistancePoint(BaseModel):
    """Точка сопротивления в программе."""
    day_number: int
    session_slot: SessionSlot
    resistance_type: str
    severity: str  # low, medium, high
    description: str
    mitigation_strategies: List[str]
    support_modules: List[str]


class EmotionalCurvePoint(BaseModel):
    """Точка на эмоциональной кривой."""
    day_number: int
    emotional_stage: EmotionalCurveStage
    energy_level: int = Field(ge=1, le=10, description="Уровень энергии от 1 до 10")
    motivation_level: int = Field(ge=1, le=10, description="Уровень мотивации от 1 до 10")
    recommended_intensity: str  # low, medium, high
    notes: str


# ===== ОРКЕСТРАЦИЯ =====

class ModuleSequence(BaseModel):
    """Последовательность модулей с обоснованием."""
    sequence: List[str]  # module_ids
    rationale: str
    cumulative_effects: List[str]
    synergy_score: float = Field(ge=0.0, le=1.0, description="Оценка синергии от 0 до 1")


class IntegrationPlan(BaseModel):
    """План интеграции программы."""
    program: Program
    module_sequences: List[ModuleSequence]
    synergy_analysis: List[ModuleSynergy]
    resistance_points: List[ResistancePoint]
    emotional_curve: List[EmotionalCurvePoint]
    optimization_notes: List[str]


# ===== ВЫХОДНЫЕ ОТЧЕТЫ =====

class DayAnalysis(BaseModel):
    """Анализ одного дня программы."""
    day_number: int
    phase: PhaseType
    emotional_stage: EmotionalCurveStage
    total_load_minutes: int
    module_count: int
    synergy_rating: float = Field(ge=0.0, le=1.0, description="Оценка синергии от 0 до 1")
    potential_issues: List[str]
    recommendations: List[str]


class PhaseAnalysis(BaseModel):
    """Анализ фазы программы."""
    phase_type: PhaseType
    duration_days: int
    total_modules: int
    average_daily_load: int
    synergy_score: float = Field(ge=0.0, le=1.0, description="Оценка синергии от 0 до 1")
    coherence_score: float = Field(ge=0.0, le=1.0, description="Оценка coherence от 0 до 1")
    issues: List[str]
    recommendations: List[str]


class ProgramAnalysis(BaseModel):
    """Полный анализ программы."""
    program_id: str
    program_name: str
    total_days: int
    phase_analyses: List[PhaseAnalysis]
    day_analyses: List[DayAnalysis]
    overall_synergy_score: float = Field(ge=0.0, le=1.0, description="Общая оценка синергии от 0 до 1")
    overall_coherence_score: float = Field(ge=0.0, le=1.0, description="Общая оценка coherence от 0 до 1")
    critical_issues: List[str]
    optimization_opportunities: List[str]


class IntegrationReport(BaseModel):
    """Итоговый отчет интеграции."""
    program_analysis: ProgramAnalysis
    integration_plan: IntegrationPlan
    implementation_ready: bool
    quality_score: float = Field(ge=0.0, le=100.0, description="Общая оценка качества от 0 до 100")
    approval_notes: str


__all__ = [
    "PhaseType",
    "SessionSlot",
    "ActivityType",
    "EmotionalCurveStage",
    "SynergyLevel",
    "ModuleReference",
    "Activity",
    "Session",
    "Day",
    "Phase",
    "Program",
    "ModuleSynergy",
    "ResistancePoint",
    "EmotionalCurvePoint",
    "ModuleSequence",
    "IntegrationPlan",
    "DayAnalysis",
    "PhaseAnalysis",
    "ProgramAnalysis",
    "IntegrationReport"
]
