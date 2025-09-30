"""
Pydantic модели для Pattern Ericksonian Hypnosis Scriptwriter Agent
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class TranceDepth(str, Enum):
    """Глубина гипнотического транса"""
    LIGHT = "light"      # Альфа-состояние, легкая релаксация
    MEDIUM = "medium"    # Тета-состояние, терапевтический транс
    DEEP = "deep"        # Глубокая тета, трансформационный транс


class HypnoticTechnique(str, Enum):
    """Типы гипнотических техник"""
    EMBEDDED_COMMANDS = "embedded_commands"
    METAPHOR = "metaphor"
    DOUBLE_BIND = "double_bind"
    PRESUPPOSITION = "presupposition"
    TEMPORAL_PREDICATES = "temporal_predicates"
    DISSOCIATION = "dissociation"
    FRACTIONATION = "fractionation"


class TherapeuticGoal(str, Enum):
    """Терапевтические цели скрипта"""
    RELAXATION = "relaxation"
    ANXIETY_REDUCTION = "anxiety_reduction"
    CONFIDENCE_BUILDING = "confidence_building"
    HABIT_CHANGE = "habit_change"
    PAIN_MANAGEMENT = "pain_management"
    SLEEP_IMPROVEMENT = "sleep_improvement"
    STRESS_MANAGEMENT = "stress_management"
    MOTIVATION = "motivation"


class ScriptComponent(BaseModel):
    """Компонент гипнотического скрипта"""
    name: str = Field(description="Название компонента")
    type: str = Field(description="Тип компонента (induction, deepening, etc.)")
    content: str = Field(description="Текстовое содержимое")
    duration_minutes: int = Field(description="Длительность компонента")
    techniques_used: List[HypnoticTechnique] = Field(default_factory=list)


class HypnoticScript(BaseModel):
    """Полный гипнотический скрипт"""
    title: str = Field(description="Название скрипта")
    therapeutic_goal: TherapeuticGoal
    trance_depth: TranceDepth
    total_duration_minutes: int

    induction: ScriptComponent
    deepening: ScriptComponent
    therapeutic_work: ScriptComponent
    posthypnotic_suggestions: ScriptComponent
    emergence: ScriptComponent

    embedded_commands: List[str] = Field(default_factory=list)
    metaphors: List[str] = Field(default_factory=list)
    safety_notes: List[str] = Field(default_factory=list)


class TherapeuticMetaphor(BaseModel):
    """Терапевтическая метафора"""
    title: str
    problem_addressed: str
    metaphor_text: str
    therapeutic_message: str
    application_context: str


class SafetyAssessment(BaseModel):
    """Оценка безопасности скрипта"""
    is_safe: bool
    risk_level: str  # "low", "medium", "high"
    contraindications: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    requires_professional: bool = False