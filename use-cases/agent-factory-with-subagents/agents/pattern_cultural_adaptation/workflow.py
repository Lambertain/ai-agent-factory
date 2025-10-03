"""
Workflow конфигурация для Pattern Cultural Adaptation Agent в контексте PatternShift Architecture
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
    ADAPTER = "adapter"  # Адаптер контента


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
    cultures_adapted: int = 0
    modules_adapted_per_culture: int = 0
    cultural_variants_created: int = 0
    target_cultures: int = 10  # Целевое количество культурных контекстов

    def get_completion_percentage(self) -> float:
        """Процент выполнения культурной адаптации"""
        return (self.cultures_adapted / self.target_cultures) * 100 if self.target_cultures > 0 else 0.0


@dataclass
class PatternCulturalAdaptationWorkflow:
    """
    Workflow конфигурация для Pattern Cultural Adaptation Agent

    Позиция в PatternShift Architecture:
    - Phase: Post-Integration (после Phase 2)
    - Role: Культурная адаптация всех модулей
    - Inputs: Все Phase 2 агенты
    - Outputs: Культурно-адаптированные варианты программы
    """

    # Основная информация
    agent_name: str = "pattern_cultural_adaptation"
    phase: WorkflowPhase = WorkflowPhase.PHASE_2_INTEGRATION_POLISH
    role: AgentRole = AgentRole.ADAPTER
    days: str = "23"

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
            "phase_description": "Cultural Adaptation - адаптация модулей под 10+ культурных контекстов",
            "depends_on": [
                "pattern_integration_synthesizer",
                "pattern_feedback_orchestrator",
                "pattern_progress_narrator",
                "pattern_transition_craftsman"
            ],
            "key_deliverables": [
                "Адаптация всех модулей под 10+ культурных контекстов",
                "Культурно-специфичные метафоры и примеры",
                "Учет культурных табу и ценностей",
                "Локализация языка и терминологии",
                "Культурно-адаптированные коммуникационные стили"
            ],
            "target_cultures": [
                "Западная (США, Европа)",
                "Восточная (Китай, Япония, Корея)",
                "Славянская (Россия, Украина, Беларусь)",
                "Арабская",
                "Латиноамериканская",
                "Индийская",
                "Африканская",
                "Скандинавская",
                "Средиземноморская",
                "Юго-Восточная Азия"
            ],
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
                description=f"Получение модулей от {source_agent} для культурной адаптации"
            ))

        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_orchestrator",
            data_type="culturally_adapted_modules",
            transformation_required=False,
            description="Передача культурно-адаптированных модулей оркестратору"
        ))

        return connections

    async def receive_from_phase2_agents(self, modules_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка входных данных от Phase 2 агентов"""
        processed_data = {
            "status": "received",
            "modules_count": modules_data.get("total_modules", 460),
            "cultures_to_adapt": len(self.workflow_metadata["target_cultures"])
        }

        self.stats.modules_adapted_per_culture = processed_data["modules_count"]

        return processed_data

    async def adapt_modules_for_cultures(
        self,
        modules: List[Dict[str, Any]],
        cultures: List[str]
    ) -> Dict[str, Any]:
        """Адаптация модулей под различные культуры"""
        adaptation_result = {
            "adapted_modules": {},
            "cultural_variants": 0,
            "total_adaptations": 0
        }

        for culture in cultures:
            adaptation_result["adapted_modules"][culture] = {
                "modules_count": len(modules),
                "adaptations_made": len(modules) * 5,  # 5 адаптаций на модуль
                "cultural_specifics": []
            }
            adaptation_result["cultural_variants"] += len(modules)

        adaptation_result["total_adaptations"] = len(cultures) * len(modules)

        self.stats.cultures_adapted = len(cultures)
        self.stats.cultural_variants_created = adaptation_result["cultural_variants"]

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
                "culturally_adapted_modules": adapted_modules,
                "cultures_count": self.stats.cultures_adapted,
                "cultural_variants": self.stats.cultural_variants_created
            },
            "stats": {
                "cultures_adapted": self.stats.cultures_adapted,
                "target_cultures": self.stats.target_cultures,
                "completion_percentage": self.stats.get_completion_percentage(),
                "modules_per_culture": self.stats.modules_adapted_per_culture
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
                "cultures_adapted": self.stats.cultures_adapted,
                "target_cultures": self.stats.target_cultures,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "cultural_variants_created": self.stats.cultural_variants_created
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.cultures_adapted < self.stats.target_cultures else "completed"
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

        if self.stats.target_cultures < 10:
            validation_results["warnings"].append(
                f"Целевое количество культур ({self.stats.target_cultures}) ниже рекомендованного (10)"
            )

        return validation_results


cultural_adaptation_workflow = PatternCulturalAdaptationWorkflow()


def get_workflow() -> PatternCulturalAdaptationWorkflow:
    return cultural_adaptation_workflow


async def update_workflow_stats(
    cultures_adapted: int = 0,
    modules_adapted_per_culture: int = 0,
    cultural_variants_created: int = 0
) -> Dict[str, Any]:
    workflow = get_workflow()

    if cultures_adapted > 0:
        workflow.stats.cultures_adapted += cultures_adapted
    if modules_adapted_per_culture > 0:
        workflow.stats.modules_adapted_per_culture = modules_adapted_per_culture
    if cultural_variants_created > 0:
        workflow.stats.cultural_variants_created += cultural_variants_created

    return workflow.get_workflow_status()
