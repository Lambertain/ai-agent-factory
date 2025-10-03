"""
Workflow конфигурация для Pattern Exercise Architect Agent в контексте PatternShift Architecture
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
    exercises_created: int = 0
    exercises_per_technique: int = 50
    techniques_covered: int = 0
    difficulty_levels_created: int = 0
    target_exercises: int = 200  # Целевое количество из архитектуры (50 техник x 4 упражнения)

    def get_completion_percentage(self) -> float:
        """Процент выполнения целевого количества упражнений"""
        return (self.exercises_created / self.target_exercises) * 100 if self.target_exercises > 0 else 0.0


@dataclass
class PatternExerciseArchitectWorkflow:
    """
    Workflow конфигурация для Pattern Exercise Architect Agent

    Позиция в PatternShift Architecture:
    - Phase: PHASE_1_CONTENT_CREATION (Days 6-10)
    - Role: Архитектор упражнений на основе NLP техник
    - Inputs: NLP техники от pattern_nlp_technique_master
    - Outputs: 200+ упражнений для практического применения техник
    """

    # Основная информация
    agent_name: str = "pattern_exercise_architect"
    phase: WorkflowPhase = WorkflowPhase.PHASE_1_CONTENT_CREATION
    role: AgentRole = AgentRole.CONTENT_CREATOR
    days: str = "6-10"

    # Входящие связи
    receives_from: List[str] = field(default_factory=lambda: ["pattern_nlp_technique_master"])

    # Исходящие связи
    outputs_to: List[str] = field(default_factory=lambda: ["pattern_integration_synthesizer"])

    # Статистика
    stats: WorkflowStats = field(default_factory=WorkflowStats)

    # Метаданные workflow
    workflow_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация метаданных workflow"""
        self.workflow_metadata = {
            "phase_description": "Content Creation - создание 200+ упражнений на основе NLP техник",
            "depends_on": ["pattern_nlp_technique_master"],
            "parallel_agents": [
                "pattern_ericksonian_hypnosis_scriptwriter",
                "pattern_microhabit_designer",
                "pattern_metaphor_weaver",
                "pattern_gamification_architect"
            ],
            "key_deliverables": [
                "200+ практических упражнений (50 техник x 4 упражнения)",
                "Упражнения 3 уровней сложности: начальный, средний, продвинутый",
                "Пошаговые инструкции выполнения",
                "Критерии успешного выполнения для каждого упражнения",
                "VAK адаптации упражнений"
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

        # Входящая связь от NLP Technique Master
        connections.append(WorkflowConnection(
            source_agent="pattern_nlp_technique_master",
            target_agent=self.agent_name,
            data_type="nlp_techniques",
            transformation_required=False,
            description="Получение NLP техник для создания практических упражнений"
        ))

        # Исходящая связь к Integration Synthesizer
        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_integration_synthesizer",
            data_type="exercise_modules",
            transformation_required=False,
            description="Передача созданных упражнений для интеграции в программу трансформации"
        ))

        return connections

    async def receive_from_nlp_technique_master(self, techniques_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка входных данных от pattern_nlp_technique_master

        Args:
            techniques_data: Данные с NLP техниками

        Returns:
            Dict с результатом обработки
        """
        processed_data = {
            "status": "received",
            "techniques_count": len(techniques_data.get("techniques", [])),
            "exercises_to_create": 0
        }

        # Планируем создание упражнений: 4 упражнения на каждую технику
        techniques_count = len(techniques_data.get("techniques", []))
        processed_data["exercises_to_create"] = techniques_count * 4

        # Обновляем статистику
        self.stats.techniques_covered = techniques_count

        return processed_data

    async def create_exercises_batch(
        self,
        techniques: List[Dict[str, Any]],
        exercises_per_technique: int = 4
    ) -> Dict[str, Any]:
        """
        Создание batch упражнений для техник

        Args:
            techniques: Список NLP техник
            exercises_per_technique: Количество упражнений на технику (default: 4)

        Returns:
            Dict с созданными упражнениями и статистикой
        """
        batch_result = {
            "exercises": [],
            "difficulty_breakdown": {
                "beginner": 0,
                "intermediate": 0,
                "advanced": 0
            },
            "total_created": 0,
            "techniques_covered": len(techniques)
        }

        # Планируем распределение упражнений по уровням сложности
        for technique in techniques:
            # 2 упражнения начального уровня, 1 среднего, 1 продвинутого
            batch_result["difficulty_breakdown"]["beginner"] += 2
            batch_result["difficulty_breakdown"]["intermediate"] += 1
            batch_result["difficulty_breakdown"]["advanced"] += 1

        batch_result["total_created"] = len(techniques) * exercises_per_technique

        # Обновляем статистику
        self.stats.exercises_created = batch_result["total_created"]
        self.stats.techniques_covered = len(techniques)
        self.stats.difficulty_levels_created = 3

        return batch_result

    async def send_to_integration_synthesizer(
        self,
        exercises: List[Any],
        techniques_covered: int
    ) -> Dict[str, Any]:
        """
        Отправка созданных упражнений в Integration Synthesizer

        Args:
            exercises: Список созданных упражнений
            techniques_covered: Количество покрытых техник

        Returns:
            Dict с результатом передачи
        """
        output_package = {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "day_completed": self.days,
            "deliverables": {
                "exercises": exercises,
                "total_count": len(exercises),
                "techniques_covered": techniques_covered,
                "difficulty_levels": ["beginner", "intermediate", "advanced"]
            },
            "stats": {
                "exercises_created": self.stats.exercises_created,
                "exercises_per_technique": self.stats.exercises_per_technique,
                "techniques_covered": self.stats.techniques_covered,
                "completion_percentage": self.stats.get_completion_percentage()
            },
            "ready_for_integration": True,
            "next_agent": "pattern_integration_synthesizer",
            "integration_instructions": {
                "merge_strategy": "append_to_modules",
                "module_type": "exercise_practice",
                "placement": "after_technique_introduction"
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
                "exercises_created": self.stats.exercises_created,
                "target_exercises": self.stats.target_exercises,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "techniques_covered": self.stats.techniques_covered,
                "difficulty_levels": self.stats.difficulty_levels_created
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.exercises_created < self.stats.target_exercises else "completed"
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
        if "pattern_nlp_technique_master" not in self.receives_from:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                "Отсутствует обязательная связь с pattern_nlp_technique_master"
            )

        # Проверка output target
        if "pattern_integration_synthesizer" not in self.outputs_to:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                "Отсутствует обязательная связь с pattern_integration_synthesizer"
            )

        # Проверка целевого количества
        if self.stats.target_exercises < 200:
            validation_results["warnings"].append(
                f"Целевое количество упражнений ({self.stats.target_exercises}) ниже рекомендованного (200)"
            )

        # Проверка days alignment
        if self.days != "6-10":
            validation_results["warnings"].append(
                f"Days '{self.days}' не соответствуют архитектуре (ожидается '6-10')"
            )

        return validation_results


# Создание глобального экземпляра workflow для использования в агенте
exercise_architect_workflow = PatternExerciseArchitectWorkflow()


def get_workflow() -> PatternExerciseArchitectWorkflow:
    """
    Получить экземпляр workflow конфигурации

    Returns:
        PatternExerciseArchitectWorkflow: Конфигурация workflow агента
    """
    return exercise_architect_workflow


async def update_workflow_stats(
    exercises_created: int = 0,
    techniques_covered: int = 0,
    difficulty_levels_created: int = 0
) -> Dict[str, Any]:
    """
    Обновить статистику workflow

    Args:
        exercises_created: Количество созданных упражнений
        techniques_covered: Количество покрытых техник
        difficulty_levels_created: Количество уровней сложности

    Returns:
        Dict с обновленной статистикой
    """
    workflow = get_workflow()

    if exercises_created > 0:
        workflow.stats.exercises_created += exercises_created
    if techniques_covered > 0:
        workflow.stats.techniques_covered = techniques_covered
    if difficulty_levels_created > 0:
        workflow.stats.difficulty_levels_created = difficulty_levels_created

    return workflow.get_workflow_status()
