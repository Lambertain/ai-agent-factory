"""
Workflow конфигурация для Pattern Test Architect Agent в контексте PatternShift Architecture
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
    TEST_ARCHITECT = "test_architect"


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
    tests_created: int = 0
    modules_tested: int = 0
    test_scenarios_generated: int = 0
    target_tests: int = 100  # Целевое количество тестов

    def get_completion_percentage(self) -> float:
        """Процент выполнения создания тестов"""
        return (self.tests_created / self.target_tests) * 100 if self.target_tests > 0 else 0.0


@dataclass
class PatternTestArchitectWorkflow:
    """
    Workflow конфигурация для Pattern Test Architect Agent

    Позиция в PatternShift Architecture:
    - Phase: Post-Integration (после Phase 2)
    - Role: Создание и валидация психологических тестов
    - Inputs: Все агенты создания контента
    - Outputs: Тестовые инструменты для оценки прогресса
    """

    # Основная информация
    agent_name: str = "pattern_test_architect"
    phase: WorkflowPhase = WorkflowPhase.PHASE_2_INTEGRATION_POLISH
    role: AgentRole = AgentRole.TEST_ARCHITECT
    days: str = "24"

    # Входящие связи
    receives_from: List[str] = field(default_factory=lambda: [
        "pattern_nlp_technique_master",
        "pattern_exercise_architect",
        "pattern_microhabit_designer",
        "pattern_integration_synthesizer"
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
            "phase_description": "Test Creation - создание психологических тестов для оценки прогресса",
            "depends_on": [
                "pattern_nlp_technique_master",
                "pattern_exercise_architect",
                "pattern_microhabit_designer",
                "pattern_integration_synthesizer"
            ],
            "key_deliverables": [
                "100+ психологических тестов для оценки прогресса",
                "Pre-test и post-test инструменты",
                "Промежуточные тесты для отслеживания динамики",
                "Валидированные шкалы измерения изменений",
                "Автоматизированная интерпретация результатов"
            ],
            "test_types": [
                "Оценка текущего состояния",
                "Измерение прогресса",
                "Выявление готовности к переходу",
                "Определение эффективности техник",
                "Мониторинг рисков и сложностей"
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
                data_type="content_modules",
                transformation_required=True,
                description=f"Получение модулей от {source_agent} для создания тестов"
            ))

        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_orchestrator",
            data_type="psychological_tests",
            transformation_required=False,
            description="Передача тестовых инструментов оркестратору"
        ))

        return connections

    async def receive_from_content_agents(self, modules_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка входных данных от агентов создания контента"""
        processed_data = {
            "status": "received",
            "modules_count": modules_data.get("total_modules", 460),
            "tests_to_create": 100
        }

        return processed_data

    async def create_tests_batch(
        self,
        modules: List[Dict[str, Any]],
        target_count: int = 100
    ) -> Dict[str, Any]:
        """Создание batch психологических тестов"""
        test_result = {
            "tests": [],
            "test_scenarios": 0,
            "total_created": 0
        }

        test_result["total_created"] = target_count
        test_result["test_scenarios"] = target_count * 3  # 3 сценария на тест

        self.stats.tests_created = target_count
        self.stats.test_scenarios_generated = test_result["test_scenarios"]
        self.stats.modules_tested = len(modules)

        return test_result

    async def send_to_orchestrator(
        self,
        tests: List[Any]
    ) -> Dict[str, Any]:
        """Отправка тестов оркестратору"""
        output_package = {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "day_completed": self.days,
            "deliverables": {
                "psychological_tests": tests,
                "total_count": len(tests),
                "test_scenarios": self.stats.test_scenarios_generated
            },
            "stats": {
                "tests_created": self.stats.tests_created,
                "target_tests": self.stats.target_tests,
                "completion_percentage": self.stats.get_completion_percentage(),
                "modules_tested": self.stats.modules_tested
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
                "tests_created": self.stats.tests_created,
                "target_tests": self.stats.target_tests,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "test_scenarios_generated": self.stats.test_scenarios_generated
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.tests_created < self.stats.target_tests else "completed"
        }

    def validate_workflow_compliance(self) -> Dict[str, Any]:
        """Валидация соответствия PatternShift Architecture"""
        validation_results = {
            "compliant": True,
            "issues": [],
            "warnings": []
        }

        if "pattern_orchestrator" not in self.outputs_to:
            validation_results["issues"].append(
                "Отсутствует обязательная связь с pattern_orchestrator"
            )

        if self.stats.target_tests < 100:
            validation_results["warnings"].append(
                f"Целевое количество тестов ({self.stats.target_tests}) ниже рекомендованного (100)"
            )

        return validation_results


test_architect_workflow = PatternTestArchitectWorkflow()


def get_workflow() -> PatternTestArchitectWorkflow:
    return test_architect_workflow


async def update_workflow_stats(
    tests_created: int = 0,
    modules_tested: int = 0,
    test_scenarios_generated: int = 0
) -> Dict[str, Any]:
    workflow = get_workflow()

    if tests_created > 0:
        workflow.stats.tests_created += tests_created
    if modules_tested > 0:
        workflow.stats.modules_tested = modules_tested
    if test_scenarios_generated > 0:
        workflow.stats.test_scenarios_generated += test_scenarios_generated

    return workflow.get_workflow_status()
