"""
Pattern Ericksonian Hypnosis Scriptwriter Agent

Специализированный агент для создания эриксоновских гипнотических скриптов
в рамках трансформационной системы PatternShift.
"""

from .agent import agent, run_pattern_ericksonian_hypnosis_scriptwriter
from .dependencies import PatternEricksonianHypnosisScriptwriterDependencies
from .models import (
    HypnoticScript,
    TranceDepth,
    HypnoticTechnique,
    TherapeuticGoal,
    ScriptComponent,
    TherapeuticMetaphor,
    SafetyAssessment
)
from .settings import load_settings, get_llm_model

__all__ = [
    "agent",
    "run_pattern_ericksonian_hypnosis_scriptwriter",
    "PatternEricksonianHypnosisScriptwriterDependencies",
    "HypnoticScript",
    "TranceDepth",
    "HypnoticTechnique",
    "TherapeuticGoal",
    "ScriptComponent",
    "TherapeuticMetaphor",
    "SafetyAssessment",
    "load_settings",
    "get_llm_model"
]

__version__ = "0.1.0"