"""
Pattern Integration Synthesizer Agent - системный интегратор программ трансформации.

Агент специализируется на оркестрации модулей контента в целостные программы,
управлении эмоциональной кривой и обеспечении синергии между модулями для
проекта PatternShift.
"""

from .agent import (
    agent,
    run_pattern_integration_synthesizer,
    analyze_program_synergy,
    optimize_emotional_curve,
    create_module_sequence
)
from .dependencies import PatternIntegrationSynthesizerDependencies
from .settings import Settings, load_settings, get_llm_model
from .models import (
    PhaseType,
    SessionSlot,
    ActivityType,
    EmotionalCurveStage,
    SynergyLevel,
    ModuleReference,
    Activity,
    Session,
    Day,
    Phase,
    Program,
    ModuleSynergy,
    ResistancePoint,
    EmotionalCurvePoint,
    ModuleSequence,
    IntegrationPlan,
    DayAnalysis,
    PhaseAnalysis,
    ProgramAnalysis,
    IntegrationReport
)


__version__ = "1.0.0"

__all__ = [
    # Главный агент
    "agent",
    "run_pattern_integration_synthesizer",

    # Вспомогательные функции
    "analyze_program_synergy",
    "optimize_emotional_curve",
    "create_module_sequence",

    # Зависимости и настройки
    "PatternIntegrationSynthesizerDependencies",
    "Settings",
    "load_settings",
    "get_llm_model",

    # Pydantic модели - Enums
    "PhaseType",
    "SessionSlot",
    "ActivityType",
    "EmotionalCurveStage",
    "SynergyLevel",

    # Pydantic модели - Структура программы
    "ModuleReference",
    "Activity",
    "Session",
    "Day",
    "Phase",
    "Program",

    # Pydantic модели - Анализ
    "ModuleSynergy",
    "ResistancePoint",
    "EmotionalCurvePoint",
    "ModuleSequence",
    "IntegrationPlan",

    # Pydantic модели - Отчеты
    "DayAnalysis",
    "PhaseAnalysis",
    "ProgramAnalysis",
    "IntegrationReport",

    # Версия
    "__version__"
]
