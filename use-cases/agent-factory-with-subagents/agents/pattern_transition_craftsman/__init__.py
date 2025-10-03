"""
Pattern Transition Craftsman Agent

Специализированный Pydantic AI агент для создания переходов между модулями
программы трансформации PatternShift.
"""

from .agent import agent, run_pattern_transition_craftsman
from .dependencies import PatternTransitionCraftsmanDependencies
from .models import (
    TransitionType,
    EnergyLevel,
    ModalityShift,
    AnchorType,
    TransitionElement,
    ModuleTransition,
    BridgeContent,
    CoherenceCheck,
    EnergyTransition,
    TransitionLibrary,
    MicroIntervention,
    FlowAnalysis
)
from .tools import (
    create_module_transition,
    create_bridge_content,
    check_program_coherence,
    generate_micro_intervention,
    analyze_program_flow,
    search_agent_knowledge
)

__version__ = "1.0.0"

__all__ = [
    # Основной агент
    "agent",
    "run_pattern_transition_craftsman",

    # Зависимости
    "PatternTransitionCraftsmanDependencies",

    # Модели данных
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
    "FlowAnalysis",

    # Инструменты
    "create_module_transition",
    "create_bridge_content",
    "check_program_coherence",
    "generate_micro_intervention",
    "analyze_program_flow",
    "search_agent_knowledge"
]
