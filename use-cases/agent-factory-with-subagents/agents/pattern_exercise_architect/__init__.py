"""
Pattern Exercise Architect Agent

Специализированный Pydantic AI агент для создания трансформационных упражнений
в рамках системы PatternShift.
"""

from .agent import agent, run_pattern_exercise_architect
from .dependencies import PatternExerciseArchitectDependencies
from .models import (
    TransformationalExercise,
    ExerciseStep,
    CompletionCriteria,
    ExerciseVariant,
    ExerciseSequence,
    ExerciseModule,
    ExerciseDesignRequest,
    ExerciseDesignResponse,
    LearningChannel,
    ExerciseDifficulty,
    ExerciseType
)
from .tools import (
    design_transformational_exercise,
    create_exercise_variants,
    design_self_check_criteria,
    adapt_nlp_technique_to_exercise,
    search_agent_knowledge
)

__version__ = "1.0.0"

__all__ = [
    # Основной агент
    "agent",
    "run_pattern_exercise_architect",

    # Зависимости
    "PatternExerciseArchitectDependencies",

    # Модели данных
    "TransformationalExercise",
    "ExerciseStep",
    "CompletionCriteria",
    "ExerciseVariant",
    "ExerciseSequence",
    "ExerciseModule",
    "ExerciseDesignRequest",
    "ExerciseDesignResponse",
    "LearningChannel",
    "ExerciseDifficulty",
    "ExerciseType",

    # Инструменты
    "design_transformational_exercise",
    "create_exercise_variants",
    "design_self_check_criteria",
    "adapt_nlp_technique_to_exercise",
    "search_agent_knowledge"
]
