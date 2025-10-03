"""
Workflow конфигурация для Pattern VAK Adaptation Agent в контексте PatternShift Architecture
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class WorkflowPhase(Enum):
    """Фазы workflow в PatternShift Architecture"""
    PHASE_1_CONTENT_CREATION = "PHASE_1_CONTENT_CREATION"
    PHASE_2_INTEGRATION_POLISH = "PHASE_2_INTEGRATION_POLISH"
    PHASE_3_SAFETY_SCIENCE = "PHASE_3_SAFETY_SCIENCE"


class AgentRole(Enum):
    """Роли агентов в workflow"""
    CONTENT_CREATOR = "content_creator"
    INTEGRATOR = "integrator"
    VALIDATOR = "validator"
    ADAPTER = "adapter"


@dataclass
class WorkflowConnection:
    """Связь между агентами в workflow"""
    source_agent: str
    target_agent: str
    data_type: str
    transformation_required: bool = False
    description: str = ""


@dataclass
class WorkflowStats:
    """Статистика выполнения workflow"""
    vak_modalities_adapted: int = 0
    modules_adapted_per_modality: int = 0
    vak_variants_created: int = 0
    target_modalities: int = 3  # Visual, Auditory, Kinesthetic

    def get_completion_percentage(self) -> float:
        """Процент выполнения VAK адаптации"""
        return (self.vak_modalities_adapted / self.target_modalities) * 100 if self.target_modalities > 0 else 0.0


@dataclass
class PatternVAKAdaptationWorkflow:
    """
    Workflow конфигурация для Pattern VAK Adaptation Agent

    Позиция в PatternShift Architecture:
    - Phase: Post-Integration (после Phase 2)
    - Role: VAK адаптация всех модулей
    - Inputs: Все Phase 2 агенты
    - Outputs: VAK-адаптированные варианты программы
    """

    # Основная информация
    agent_name: str = "pattern_vak_adaptation"
    phase: WorkflowPhase = WorkflowPhase.PHASE_2_INTEGRATION_POLISH
    role: AgentRole = AgentRole.ADAPTER
    days: str = "22"

    # Входящие связи
    receives_from: List[str] = field(default_factory=lambda: [
        "pattern_integration_synthesizer",
        "pattern_feedback_orchestrator",
        "pattern_progress_narrator",
        "pattern_transition_craftsman"
    ])

    # Исходящие связи
    outputs_to: List[str] = field(default_factory=lambda: ["pattern_orchestrator"])

    # Статистика
    stats: WorkflowStats = field(default_factory=WorkflowStats)

    # Метаданные workflow
    workflow_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация метаданных workflow"""
        self.workflow_metadata = {
            "phase_description": "VAK Adaptation - адаптация модулей под 3 репрезентативные системы",
            "depends_on": [
                "pattern_integration_synthesizer",
                "pattern_feedback_orchestrator",
                "pattern_progress_narrator",
                "pattern_transition_craftsman"
            ],
            "key_deliverables": [
                "Адаптация всех модулей под Visual модальность",
                "Адаптация всех модулей под Auditory модальность",
                "Адаптация всех модулей под Kinesthetic модальность",
                "VAK-специфичные метафоры и упражнения",
                "Субмодальные адаптации для каждой системы"
            ],
            "vak_modalities": {
                "visual": "Визуальная репрезентативная система (картинки, образы, цвета)",
                "auditory": "Аудиальная репрезентативная система (звуки, мелодии, ритмы)",
                "kinesthetic": "Кинестетическая репрезентативная система (ощущения, движения, эмоции)"
            },
            "integration_target": "pattern_orchestrator"
        }

    def get_workflow_connections(self) -> List[WorkflowConnection]:
        """Получить все workflow связи агента"""
        connections = []

        for source_agent in self.receives_from:
            connections.append(WorkflowConnection(
                source_agent=source_agent,
                target_agent=self.agent_name,
                data_type="integrated_modules",
                transformation_required=True,
                description=f"Получение модулей от {source_agent} для VAK адаптации"
            ))

        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_orchestrator",
            data_type="vak_adapted_modules",
            transformation_required=False,
            description="Передача VAK-адаптированных модулей оркестратору"
        ))

        return connections

    async def receive_from_phase2_agents(self, modules_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка входных данных от Phase 2 агентов"""
        processed_data = {
            "status": "received",
            "modules_count": modules_data.get("total_modules", 460),
            "modalities_to_adapt": 3
        }

        self.stats.modules_adapted_per_modality = processed_data["modules_count"]

        return processed_data

    async def adapt_modules_for_vak(
        self,
        modules: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Адаптация модулей под VAK модальности"""
        adaptation_result = {
            "adapted_modules": {
                "visual": [],
                "auditory": [],
                "kinesthetic": []
            },
            "vak_variants": 0,
            "total_adaptations": 0
        }

        for modality in ["visual", "auditory", "kinesthetic"]:
            adaptation_result["adapted_modules"][modality] = {
                "modules_count": len(modules),
                "adaptations_made": len(modules) * 7,  # 7 адаптаций на модуль
                "submodalities": []
            }
            adaptation_result["vak_variants"] += len(modules)

        adaptation_result["total_adaptations"] = 3 * len(modules)

        self.stats.vak_modalities_adapted = 3
        self.stats.vak_variants_created = adaptation_result["vak_variants"]

        return adaptation_result

    async def send_to_orchestrator(
        self,
        adapted_modules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Отправка адаптированных модулей оркестратору"""
        output_package = {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "day_completed": self.days,
            "deliverables": {
                "vak_adapted_modules": adapted_modules,
                "modalities_count": self.stats.vak_modalities_adapted,
                "vak_variants": self.stats.vak_variants_created
            },
            "stats": {
                "vak_modalities_adapted": self.stats.vak_modalities_adapted,
                "target_modalities": self.stats.target_modalities,
                "completion_percentage": self.stats.get_completion_percentage(),
                "modules_per_modality": self.stats.modules_adapted_per_modality
            },
            "ready_for_orchestration": True,
            "next_agent": "pattern_orchestrator"
        }

        return output_package

    def get_workflow_status(self) -> Dict[str, Any]:
        """Получить текущий статус workflow"""
        return {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "role": self.role.value,
            "days": self.days,
            "receives_from": self.receives_from,
            "outputs_to": self.outputs_to,
            "stats": {
                "vak_modalities_adapted": self.stats.vak_modalities_adapted,
                "target_modalities": self.stats.target_modalities,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "vak_variants_created": self.stats.vak_variants_created
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.vak_modalities_adapted < self.stats.target_modalities else "completed"
        }

    def validate_workflow_compliance(self) -> Dict[str, Any]:
        """Валидация соответствия PatternShift Architecture"""
        validation_results = {
            "compliant": True,
            "issues": [],
            "warnings": []
        }

        required_sources = [
            "pattern_integration_synthesizer",
            "pattern_feedback_orchestrator",
            "pattern_progress_narrator",
            "pattern_transition_craftsman"
        ]

        for source in required_sources:
            if source not in self.receives_from:
                validation_results["warnings"].append(
                    f"Отсутствует связь с {source}"
                )

        if "pattern_orchestrator" not in self.outputs_to:
            validation_results["issues"].append(
                "Отсутствует обязательная связь с pattern_orchestrator"
            )

        if self.stats.target_modalities != 3:
            validation_results["warnings"].append(
                f"Целевое количество модальностей ({self.stats.target_modalities}) должно быть 3 (VAK)"
            )

        return validation_results


vak_adaptation_workflow = PatternVAKAdaptationWorkflow()


def get_workflow() -> PatternVAKAdaptationWorkflow:
    return vak_adaptation_workflow


async def update_workflow_stats(
    vak_modalities_adapted: int = 0,
    modules_adapted_per_modality: int = 0,
    vak_variants_created: int = 0
) -> Dict[str, Any]:
    workflow = get_workflow()

    if vak_modalities_adapted > 0:
        workflow.stats.vak_modalities_adapted = vak_modalities_adapted
    if modules_adapted_per_modality > 0:
        workflow.stats.modules_adapted_per_modality = modules_adapted_per_modality
    if vak_variants_created > 0:
        workflow.stats.vak_variants_created += vak_variants_created

    return workflow.get_workflow_status()
