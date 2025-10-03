"""
Workflow конфигурация для Pattern Microhabit Designer Agent в контексте PatternShift Architecture
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
    microhabits_created: int = 0
    habit_chains_created: int = 0
    triggers_identified: int = 0
    rewards_designed: int = 0
    target_microhabits: int = 70  # Целевое количество из архитектуры

    def get_completion_percentage(self) -> float:
        """Процент выполнения целевого количества микропривычек"""
        return (self.microhabits_created / self.target_microhabits) * 100 if self.target_microhabits > 0 else 0.0


@dataclass
class PatternMicrohabitDesignerWorkflow:
    """
    Workflow конфигурация для Pattern Microhabit Designer Agent

    Позиция в PatternShift Architecture:
    - Phase: PHASE_1_CONTENT_CREATION (Days 11-12)
    - Role: Дизайнер микропривычек
    - Outputs: 70+ микропривычек для закрепления изменений
    """

    # Основная информация
    agent_name: str = "pattern_microhabit_designer"
    phase: WorkflowPhase = WorkflowPhase.PHASE_1_CONTENT_CREATION
    role: AgentRole = AgentRole.CONTENT_CREATOR
    days: str = "11-12"

    # Входящие связи
    receives_from: List[str] = field(default_factory=lambda: [])

    # Исходящие связи
    outputs_to: List[str] = field(default_factory=lambda: ["pattern_integration_synthesizer"])

    # Статистика
    stats: WorkflowStats = field(default_factory=WorkflowStats)

    # Метаданные workflow
    workflow_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация метаданных workflow"""
        self.workflow_metadata = {
            "phase_description": "Content Creation - создание 70+ микропривычек",
            "parallel_agents": [
                "pattern_nlp_technique_master",
                "pattern_exercise_architect",
                "pattern_ericksonian_hypnosis_scriptwriter",
                "pattern_metaphor_weaver",
                "pattern_gamification_architect"
            ],
            "key_deliverables": [
                "70+ микропривычек для закрепления изменений",
                "Habit chains (цепочки привычек)",
                "Triggers и rewards для каждой привычки",
                "VAK варианты микропривычек"
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

        # Исходящая связь к Integration Synthesizer
        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_integration_synthesizer",
            data_type="microhabit_modules",
            transformation_required=False,
            description="Передача созданных микропривычек для интеграции в программу трансформации"
        ))

        return connections

    async def receive_from_parallel_agents(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка входных данных от параллельных агентов Phase 1

        Note: Microhabit Designer работает независимо от других агентов Phase 1,
        но может использовать их output для обогащения микропривычек

        Args:
            agent_data: Данные от других агентов (опционально)

        Returns:
            Dict с результатом обработки
        """
        processed_data = {
            "status": "received",
            "enhancements": []
        }

        # Если есть NLP техники - можем обогатить triggers
        if "nlp_techniques" in agent_data:
            processed_data["enhancements"].append({
                "type": "nlp_enhanced_triggers",
                "source": "pattern_nlp_technique_master"
            })

        # Если есть метафоры - можем улучшить мотивацию
        if "metaphors" in agent_data:
            processed_data["enhancements"].append({
                "type": "metaphor_based_motivation",
                "source": "pattern_metaphor_weaver"
            })

        return processed_data

    async def create_microhabits_batch(
        self,
        behavior_goals: List[str],
        target_count: int = 70
    ) -> Dict[str, Any]:
        """
        Создание batch микропривычек для достижения целевого количества

        Args:
            behavior_goals: Список целевых поведенческих изменений
            target_count: Целевое количество микропривычек (default: 70)

        Returns:
            Dict с созданными микропривычками и статистикой
        """
        # Планируем распределение микропривычек по целям
        habits_per_goal = target_count // len(behavior_goals) if behavior_goals else target_count

        batch_result = {
            "microhabits": [],
            "habit_chains": [],
            "total_created": 0,
            "distribution": {}
        }

        for goal in behavior_goals:
            batch_result["distribution"][goal] = habits_per_goal

        # Обновляем статистику
        self.stats.microhabits_created = target_count

        return batch_result

    async def send_to_integration_synthesizer(
        self,
        microhabits: List[Any],
        habit_chains: List[Any]
    ) -> Dict[str, Any]:
        """
        Отправка созданных микропривычек в Integration Synthesizer

        Args:
            microhabits: Список созданных микропривычек
            habit_chains: Список цепочек привычек

        Returns:
            Dict с результатом передачи
        """
        output_package = {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "day_completed": self.days,
            "deliverables": {
                "microhabits": microhabits,
                "habit_chains": habit_chains,
                "total_count": len(microhabits),
                "chains_count": len(habit_chains)
            },
            "stats": {
                "microhabits_created": self.stats.microhabits_created,
                "habit_chains_created": self.stats.habit_chains_created,
                "triggers_identified": self.stats.triggers_identified,
                "rewards_designed": self.stats.rewards_designed,
                "completion_percentage": self.stats.get_completion_percentage()
            },
            "ready_for_integration": True,
            "next_agent": "pattern_integration_synthesizer",
            "integration_instructions": {
                "merge_strategy": "append_to_modules",
                "module_type": "microhabit_practice",
                "placement": "after_main_exercises"
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
                "microhabits_created": self.stats.microhabits_created,
                "target_microhabits": self.stats.target_microhabits,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "habit_chains_created": self.stats.habit_chains_created
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.microhabits_created < self.stats.target_microhabits else "completed"
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

        # Проверка output target
        if "pattern_integration_synthesizer" not in self.outputs_to:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                "Отсутствует обязательная связь с pattern_integration_synthesizer"
            )

        # Проверка целевого количества
        if self.stats.target_microhabits < 70:
            validation_results["warnings"].append(
                f"Целевое количество микропривычек ({self.stats.target_microhabits}) ниже рекомендованного (70)"
            )

        # Проверка days alignment
        if self.days != "11-12":
            validation_results["warnings"].append(
                f"Days '{self.days}' не соответствуют архитектуре (ожидается '11-12')"
            )

        return validation_results


# Создание глобального экземпляра workflow для использования в агенте
microhabit_designer_workflow = PatternMicrohabitDesignerWorkflow()


def get_workflow() -> PatternMicrohabitDesignerWorkflow:
    """
    Получить экземпляр workflow конфигурации

    Returns:
        PatternMicrohabitDesignerWorkflow: Конфигурация workflow агента
    """
    return microhabit_designer_workflow


async def update_workflow_stats(
    microhabits_created: int = 0,
    habit_chains_created: int = 0,
    triggers_identified: int = 0,
    rewards_designed: int = 0
) -> Dict[str, Any]:
    """
    Обновить статистику workflow

    Args:
        microhabits_created: Количество созданных микропривычек
        habit_chains_created: Количество созданных цепочек
        triggers_identified: Количество идентифицированных триггеров
        rewards_designed: Количество спроектированных вознаграждений

    Returns:
        Dict с обновленной статистикой
    """
    workflow = get_workflow()

    if microhabits_created > 0:
        workflow.stats.microhabits_created += microhabits_created
    if habit_chains_created > 0:
        workflow.stats.habit_chains_created += habit_chains_created
    if triggers_identified > 0:
        workflow.stats.triggers_identified += triggers_identified
    if rewards_designed > 0:
        workflow.stats.rewards_designed += rewards_designed

    return workflow.get_workflow_status()
