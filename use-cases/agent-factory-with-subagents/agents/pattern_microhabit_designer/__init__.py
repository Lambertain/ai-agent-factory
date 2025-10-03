"""
Pattern Microhabit Designer Agent

Специализированный Pydantic AI агент для создания микро-привычек и habit chains
в рамках системы PatternShift.
"""

from .agent import agent, run_pattern_microhabit_designer
from .dependencies import PatternMicrohabitDesignerDependencies
from .models import (
    Microhabit,
    HabitChain,
    MicrohabitDesignRequest,
    MicrohabitDesignResponse,
    BehaviorChangeGoal,
    MicrohabitModule,
    HabitTriggerType,
    RewardType,
    DifficultyLevel
)
from .tools import (
    design_microhabit,
    create_habit_chain,
    identify_triggers_rewards,
    generate_module_variants,
    search_agent_knowledge
)

__version__ = "1.0.0"

__all__ = [
    # Основной агент
    "agent",
    "run_pattern_microhabit_designer",

    # Зависимости
    "PatternMicrohabitDesignerDependencies",

    # Модели данных
    "Microhabit",
    "HabitChain",
    "MicrohabitDesignRequest",
    "MicrohabitDesignResponse",
    "BehaviorChangeGoal",
    "MicrohabitModule",
    "HabitTriggerType",
    "RewardType",
    "DifficultyLevel",

    # Инструменты
    "design_microhabit",
    "create_habit_chain",
    "identify_triggers_rewards",
    "generate_module_variants",
    "search_agent_knowledge"
]
