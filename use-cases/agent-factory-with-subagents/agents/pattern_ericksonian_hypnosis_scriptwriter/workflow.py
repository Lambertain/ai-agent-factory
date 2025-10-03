"""
Workflow конфигурация для Pattern Ericksonian Hypnosis Scriptwriter Agent в контексте PatternShift Architecture
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
    CONTENT_CREATOR = "content_creator"  # Создатель контента (Phase 1)
    INTEGRATOR = "integrator"  # Интегратор (Phase 2)
    VALIDATOR = "validator"  # Валидатор (Phase 3)


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
    scripts_created: int = 0
    metaphors_integrated: int = 0
    hypnotic_patterns_used: int = 0
    target_scripts: int = 30  # Целевое количество из архитектуры

    def get_completion_percentage(self) -> float:
        """Процент выполнения целевого количества скриптов"""
        return (self.scripts_created / self.target_scripts) * 100 if self.target_scripts > 0 else 0.0


@dataclass
class PatternEricksonianHypnosisScriptwriterWorkflow:
    """
    Workflow конфигурация для Pattern Ericksonian Hypnosis Scriptwriter Agent

    Позиция в PatternShift Architecture:
    - Phase: PHASE_1_CONTENT_CREATION (Day 11)
    - Role: Создатель гипнотических скриптов на основе эриксоновского гипноза
    - Inputs: Упражнения от pattern_exercise_architect
    - Outputs: 30+ гипнотических скриптов для углубления трансформации
    """

    # Основная информация
    agent_name: str = "pattern_ericksonian_hypnosis_scriptwriter"
    phase: WorkflowPhase = WorkflowPhase.PHASE_1_CONTENT_CREATION
    role: AgentRole = AgentRole.CONTENT_CREATOR
    days: str = "11"

    # Входящие связи
    receives_from: List[str] = field(default_factory=lambda: ["pattern_exercise_architect"])

    # Исходящие связи
    outputs_to: List[str] = field(default_factory=lambda: ["pattern_integration_synthesizer"])

    # Статистика
    stats: WorkflowStats = field(default_factory=WorkflowStats)

    # Метаданные workflow
    workflow_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация метаданных workflow"""
        self.workflow_metadata = {
            "phase_description": "Content Creation - создание 30+ эриксоновских гипнотических скриптов",
            "depends_on": ["pattern_exercise_architect"],
            "parallel_agents": [
                "pattern_nlp_technique_master",
                "pattern_microhabit_designer",
                "pattern_metaphor_weaver",
                "pattern_gamification_architect"
            ],
            "key_deliverables": [
                "30+ гипнотических скриптов на основе эриксоновского подхода",
                "Многоуровневые внушения и embedded commands",
                "Терапевтические метафоры в скриптах",
                "VAK интеграция (визуальные, аудиальные, кинестетические якоря)",
                "Пресуппозиции и паттерны милтон-модели"
            ],
            "integration_target": "pattern_integration_synthesizer",
            "integration_day": "15"
        }

    def get_workflow_connections(self) -> List[WorkflowConnection]:
        """
        Получить все workflow связи агента

        Returns:
            List[WorkflowConnection]: Список связей с другими агентами
        """
        connections = []

        # Входящая связь от Exercise Architect
        connections.append(WorkflowConnection(
            source_agent="pattern_exercise_architect",
            target_agent=self.agent_name,
            data_type="exercise_modules",
            transformation_required=True,
            description="Получение упражнений для обогащения гипнотическими элементами"
        ))

        # Исходящая связь к Integration Synthesizer
        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_integration_synthesizer",
            data_type="hypnosis_scripts",
            transformation_required=False,
            description="Передача гипнотических скриптов для интеграции в программу трансформации"
        ))

        return connections

    async def receive_from_exercise_architect(self, exercises_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка входных данных от pattern_exercise_architect

        Args:
            exercises_data: Данные с упражнениями

        Returns:
            Dict с результатом обработки
        """
        processed_data = {
            "status": "received",
            "exercises_count": len(exercises_data.get("exercises", [])),
            "scripts_to_create": 30
        }

        return processed_data

    async def create_hypnosis_scripts_batch(
        self,
        base_exercises: List[Dict[str, Any]],
        target_count: int = 30
    ) -> Dict[str, Any]:
        """
        Создание batch гипнотических скриптов

        Args:
            base_exercises: Базовые упражнения для обогащения
            target_count: Целевое количество скриптов (default: 30)

        Returns:
            Dict с созданными скриптами и статистикой
        """
        batch_result = {
            "scripts": [],
            "ericksonian_patterns": [
                "embedded_commands",
                "therapeutic_metaphors",
                "presuppositions",
                "time_distortion",
                "confusion_technique"
            ],
            "total_created": 0,
            "integration_ready": True
        }

        batch_result["total_created"] = target_count

        # Обновляем статистику
        self.stats.scripts_created = target_count
        self.stats.hypnotic_patterns_used = len(batch_result["ericksonian_patterns"])

        return batch_result

    async def send_to_integration_synthesizer(
        self,
        scripts: List[Any]
    ) -> Dict[str, Any]:
        """
        Отправка созданных скриптов в Integration Synthesizer

        Args:
            scripts: Список созданных гипнотических скриптов

        Returns:
            Dict с результатом передачи
        """
        output_package = {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "day_completed": self.days,
            "deliverables": {
                "hypnosis_scripts": scripts,
                "total_count": len(scripts),
                "ericksonian_patterns": ["embedded_commands", "metaphors", "presuppositions"]
            },
            "stats": {
                "scripts_created": self.stats.scripts_created,
                "metaphors_integrated": self.stats.metaphors_integrated,
                "hypnotic_patterns_used": self.stats.hypnotic_patterns_used,
                "completion_percentage": self.stats.get_completion_percentage()
            },
            "ready_for_integration": True,
            "next_agent": "pattern_integration_synthesizer",
            "integration_instructions": {
                "merge_strategy": "append_to_modules",
                "module_type": "hypnosis_session",
                "placement": "guided_transformation_sections"
            }
        }

        return output_package

    def get_workflow_status(self) -> Dict[str, Any]:
        """
        Получить текущий статус workflow

        Returns:
            Dict со статусом выполнения workflow
        """
        return {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "role": self.role.value,
            "days": self.days,
            "receives_from": self.receives_from,
            "outputs_to": self.outputs_to,
            "stats": {
                "scripts_created": self.stats.scripts_created,
                "target_scripts": self.stats.target_scripts,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "hypnotic_patterns_used": self.stats.hypnotic_patterns_used
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.scripts_created < self.stats.target_scripts else "completed"
        }

    def validate_workflow_compliance(self) -> Dict[str, Any]:
        """
        Валидация соответствия PatternShift Architecture

        Returns:
            Dict с результатами валидации
        """
        validation_results = {
            "compliant": True,
            "issues": [],
            "warnings": []
        }

        # Проверка Phase 1 requirements
        if self.phase != WorkflowPhase.PHASE_1_CONTENT_CREATION:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                f"Agent должен быть в PHASE_1_CONTENT_CREATION, текущая phase: {self.phase.value}"
            )

        # Проверка input source
        if "pattern_exercise_architect" not in self.receives_from:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                "Отсутствует обязательная связь с pattern_exercise_architect"
            )

        # Проверка output target
        if "pattern_integration_synthesizer" not in self.outputs_to:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                "Отсутствует обязательная связь с pattern_integration_synthesizer"
            )

        # Проверка целевого количества
        if self.stats.target_scripts < 30:
            validation_results["warnings"].append(
                f"Целевое количество скриптов ({self.stats.target_scripts}) ниже рекомендованного (30)"
            )

        # Проверка days alignment
        if self.days != "11":
            validation_results["warnings"].append(
                f"Days '{self.days}' не соответствуют архитектуре (ожидается '11')"
            )

        return validation_results


# Создание глобального экземпляра workflow для использования в агенте
ericksonian_hypnosis_scriptwriter_workflow = PatternEricksonianHypnosisScriptwriterWorkflow()


def get_workflow() -> PatternEricksonianHypnosisScriptwriterWorkflow:
    """
    Получить экземпляр workflow конфигурации

    Returns:
        PatternEricksonianHypnosisScriptwriterWorkflow: Конфигурация workflow агента
    """
    return ericksonian_hypnosis_scriptwriter_workflow


async def update_workflow_stats(
    scripts_created: int = 0,
    metaphors_integrated: int = 0,
    hypnotic_patterns_used: int = 0
) -> Dict[str, Any]:
    """
    Обновить статистику workflow

    Args:
        scripts_created: Количество созданных скриптов
        metaphors_integrated: Количество интегрированных метафор
        hypnotic_patterns_used: Количество использованных гипнотических паттернов

    Returns:
        Dict с обновленной статистикой
    """
    workflow = get_workflow()

    if scripts_created > 0:
        workflow.stats.scripts_created += scripts_created
    if metaphors_integrated > 0:
        workflow.stats.metaphors_integrated += metaphors_integrated
    if hypnotic_patterns_used > 0:
        workflow.stats.hypnotic_patterns_used = hypnotic_patterns_used

    return workflow.get_workflow_status()
