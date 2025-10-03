"""
Pattern Progress Narrator Agent

Специализированный Pydantic AI агент для создания нарративов прогресса и трансформации
в рамках системы PatternShift.
"""

from .agent import agent, run_pattern_progress_narrator
from .dependencies import PatternProgressNarratorDependencies
from .models import (
    ProgressNarrative,
    NarrativeType,
    EmotionalTone,
    ProgressMetric,
    UserMilestone,
    ChallengeReframe,
    MomentumIndicators,
    HeroJourneyStage,
    TransformationJourneyMap
)
from .tools import (
    create_progress_narrative,
    reframe_challenge,
    generate_momentum_message,
    create_anticipation_builder,
    search_agent_knowledge
)

__version__ = "1.0.0"

__all__ = [
    # Основной агент
    "agent",
    "run_pattern_progress_narrator",

    # Зависимости
    "PatternProgressNarratorDependencies",

    # Модели данных
    "ProgressNarrative",
    "NarrativeType",
    "EmotionalTone",
    "ProgressMetric",
    "UserMilestone",
    "ChallengeReframe",
    "MomentumIndicators",
    "HeroJourneyStage",
    "TransformationJourneyMap",

    # Инструменты
    "create_progress_narrative",
    "reframe_challenge",
    "generate_momentum_message",
    "create_anticipation_builder",
    "search_agent_knowledge"
]
