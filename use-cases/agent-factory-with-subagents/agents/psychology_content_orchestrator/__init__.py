"""
Psychology Content Orchestrator Agent
Агент-оркестратор для координации создания психологических тестов

Координирует работу всех агентов в пайплайне:
- Psychology Research Agent (исследования)
- Psychology Content Architect (создание тестов)
- Psychology Test Generator (генерация экземпляров)
- Psychology Quality Guardian (контроль качества)
- Psychology Transformation Planner (программы трансформации)
"""

from .agent import (
    psychology_content_orchestrator,
    create_complete_psychology_project,
    coordinate_existing_project,
    quality_orchestration
)
from .dependencies import (
    OrchestratorDependencies,
    get_orchestrator_config,
    SIMPLE_PROJECT_CONFIG,
    COMPREHENSIVE_PROJECT_CONFIG,
    QUALITY_FOCUSED_CONFIG
)
from .settings import (
    OrchestratorSettings,
    load_orchestrator_settings,
    SIMPLE_ORCHESTRATION_CONFIG,
    STANDARD_ORCHESTRATION_CONFIG,
    ADVANCED_ORCHESTRATION_CONFIG,
    EXPERT_ORCHESTRATION_CONFIG
)
from .tools import (
    orchestrate_test_creation,
    coordinate_agent_workflow,
    manage_test_lifecycle,
    validate_final_output,
    track_project_progress,
    delegate_to_specialist
)

__all__ = [
    "psychology_content_orchestrator",
    "create_complete_psychology_project",
    "coordinate_existing_project",
    "quality_orchestration",
    "OrchestratorDependencies",
    "get_orchestrator_config",
    "SIMPLE_PROJECT_CONFIG",
    "COMPREHENSIVE_PROJECT_CONFIG",
    "QUALITY_FOCUSED_CONFIG",
    "OrchestratorSettings",
    "load_orchestrator_settings",
    "SIMPLE_ORCHESTRATION_CONFIG",
    "STANDARD_ORCHESTRATION_CONFIG",
    "ADVANCED_ORCHESTRATION_CONFIG",
    "EXPERT_ORCHESTRATION_CONFIG",
    "orchestrate_test_creation",
    "coordinate_agent_workflow",
    "manage_test_lifecycle",
    "validate_final_output",
    "track_project_progress",
    "delegate_to_specialist"
]

__version__ = "1.0.0"
__description__ = "Psychology Content Orchestrator Agent для координации создания психологических тестов"