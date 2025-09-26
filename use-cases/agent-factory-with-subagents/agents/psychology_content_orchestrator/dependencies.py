"""
Dependencies for Psychology Content Orchestrator Agent
Зависимости для агента-оркестратора психологического контента
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class OrchestratorDependencies:
    """
    Зависимости для Psychology Content Orchestrator Agent
    Управляет координацией всех агентов в пайплайне создания психологических тестов
    """
    # Основные параметры оркестрации
    project_type: str = "psychology_testing"  # psychology_testing, quality_assurance, coordination
    orchestration_level: str = "full_pipeline"  # full_pipeline, targeted, quality_focused
    target_language: str = "ukrainian"  # ukrainian, russian, english
    workflow_complexity: str = "standard"  # simple, standard, advanced, expert

    # Конфигурация агентов
    agent_workflow: Dict[str, Dict] = field(default_factory=lambda: {
        "content_architect": {
            "role": "test_creation",
            "priority": 1,
            "dependencies": [],
            "outputs": ["psychological_tests"]
        },
        "test_generator": {
            "role": "test_instantiation",
            "priority": 2,
            "dependencies": ["content_architect"],
            "outputs": ["generated_test_instances"]
        },
        "quality_guardian": {
            "role": "quality_assurance",
            "priority": 3,
            "dependencies": ["content_architect", "test_generator"],
            "outputs": ["quality_reports"]
        },
        "transformation_planner": {
            "role": "program_creation",
            "priority": 4,
            "dependencies": ["content_architect", "quality_guardian"],
            "outputs": ["transformation_programs"]
        }
    })

    # Гейты качества
    quality_gates: Dict[str, Dict] = field(default_factory=lambda: {
        "patternshift_compliance": {
            "threshold": 0.85,
            "required": True,
            "validator": "quality_guardian"
        },
        "clinical_accuracy": {
            "threshold": 0.90,
            "required": True,
            "validator": "quality_guardian"
        },
        "vak_adaptations": {
            "threshold": 0.80,
            "required": True,
            "validator": "content_architect"
        },
        "language_quality": {
            "threshold": 0.85,
            "required": True,
            "validator": "quality_guardian"
        }
    })

    # Спецификация проекта
    project_specification: Dict[str, Any] = field(default_factory=dict)

    # Матрица делегирования
    delegation_matrix: Dict[str, List[str]] = field(default_factory=lambda: {
        "test_creation": ["psychology_content_architect"],
        "test_generation": ["psychology_test_generator"],
        "quality_assurance": ["psychology_quality_guardian"],
        "transformation_planning": ["psychology_transformation_planner"],
        "research": ["psychology_research_agent"],
        "content_optimization": ["psychology_content_architect", "psychology_quality_guardian"]
    })

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "psychology-content",
        "orchestration",
        "project-management"
    ])
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"  # AI Agent Factory

    # Имя агента для RAG
    agent_name: str = "psychology_content_orchestrator"

    # Межагентное взаимодействие
    enable_agent_coordination: bool = True
    coordination_timeout: int = 300  # секунд
    max_parallel_agents: int = 3

    # Мониторинг и отчетность
    enable_progress_tracking: bool = True
    enable_detailed_logging: bool = True
    report_frequency: str = "per_stage"  # per_task, per_stage, final_only

    def __post_init__(self):
        """Инициализация дополнительных параметров"""
        # Добавляем теги на основе типа проекта
        if self.project_type and self.project_type not in self.knowledge_tags:
            self.knowledge_tags.append(self.project_type)

        # Устанавливаем domain для RAG
        if not self.knowledge_domain:
            self.knowledge_domain = f"orchestration.{self.project_type}.ai"

    def get_workflow_sequence(self) -> List[str]:
        """Получить последовательность агентов по приоритету"""
        sorted_agents = sorted(
            self.agent_workflow.items(),
            key=lambda x: x[1]["priority"]
        )
        return [agent_name for agent_name, _ in sorted_agents]

    def get_agent_dependencies(self, agent_name: str) -> List[str]:
        """Получить зависимости конкретного агента"""
        return self.agent_workflow.get(agent_name, {}).get("dependencies", [])

    def get_parallel_execution_groups(self) -> List[List[str]]:
        """Определить группы агентов для параллельного выполнения"""
        execution_groups = []

        # Группа 1: Независимые агенты (priority 1)
        group1 = [
            agent for agent, config in self.agent_workflow.items()
            if config["priority"] == 1 and not config["dependencies"]
        ]
        if group1:
            execution_groups.append(group1)

        # Группа 2: Агенты с зависимостями от группы 1
        group2 = [
            agent for agent, config in self.agent_workflow.items()
            if config["priority"] == 2 and all(dep in group1 for dep in config["dependencies"])
        ]
        if group2:
            execution_groups.append(group2)

        # Группа 3: Агенты финального этапа
        group3 = [
            agent for agent, config in self.agent_workflow.items()
            if config["priority"] >= 3
        ]
        if group3:
            execution_groups.append(group3)

        return execution_groups

    def should_delegate_to_agent(self, task_type: str) -> Optional[str]:
        """
        Определить нужно ли делегировать задачу и какому агенту
        """
        candidates = self.delegation_matrix.get(task_type, [])

        if candidates:
            # Возвращаем первого подходящего агента
            return candidates[0]

        return None

    def check_quality_gate(self, gate_name: str, score: float) -> bool:
        """Проверить прохождение гейта качества"""
        gate_config = self.quality_gates.get(gate_name, {})
        threshold = gate_config.get("threshold", 0.5)
        required = gate_config.get("required", False)

        passed = score >= threshold

        if required and not passed:
            raise ValueError(f"Качественный гейт {gate_name} не пройден: {score} < {threshold}")

        return passed

    def get_quality_validator(self, gate_name: str) -> Optional[str]:
        """Получить валидатора для гейта качества"""
        gate_config = self.quality_gates.get(gate_name, {})
        return gate_config.get("validator")

    def get_orchestration_summary(self) -> Dict[str, Any]:
        """Получить сводку по оркестрации"""
        return {
            "project_type": self.project_type,
            "orchestration_level": self.orchestration_level,
            "workflow_complexity": self.workflow_complexity,
            "agents_count": len(self.agent_workflow),
            "quality_gates_count": len(self.quality_gates),
            "required_gates": sum(1 for gate in self.quality_gates.values() if gate.get("required", False)),
            "execution_groups": len(self.get_parallel_execution_groups()),
            "coordination_enabled": self.enable_agent_coordination
        }

def get_orchestrator_config() -> OrchestratorDependencies:
    """
    Получить конфигурацию оркестратора из переменных окружения
    """
    return OrchestratorDependencies(
        project_type=os.getenv("PROJECT_TYPE", "psychology_testing"),
        orchestration_level=os.getenv("ORCHESTRATION_LEVEL", "full_pipeline"),
        target_language=os.getenv("TARGET_LANGUAGE", "ukrainian"),
        workflow_complexity=os.getenv("WORKFLOW_COMPLEXITY", "standard"),
        archon_project_id=os.getenv("ARCHON_PROJECT_ID", "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"),
        enable_agent_coordination=os.getenv("ENABLE_AGENT_COORDINATION", "true").lower() == "true",
        enable_progress_tracking=os.getenv("ENABLE_PROGRESS_TRACKING", "true").lower() == "true"
    )

# Предустановленные конфигурации для разных типов проектов

SIMPLE_PROJECT_CONFIG = OrchestratorDependencies(
    project_type="psychology_testing",
    orchestration_level="targeted",
    workflow_complexity="simple",
    agent_workflow={
        "content_architect": {
            "role": "test_creation",
            "priority": 1,
            "dependencies": [],
            "outputs": ["basic_test"]
        },
        "quality_guardian": {
            "role": "basic_validation",
            "priority": 2,
            "dependencies": ["content_architect"],
            "outputs": ["validation_report"]
        }
    },
    quality_gates={
        "basic_compliance": {
            "threshold": 0.70,
            "required": True,
            "validator": "quality_guardian"
        }
    }
)

COMPREHENSIVE_PROJECT_CONFIG = OrchestratorDependencies(
    project_type="psychology_testing",
    orchestration_level="full_pipeline",
    workflow_complexity="expert",
    agent_workflow={
        "research_agent": {
            "role": "research",
            "priority": 1,
            "dependencies": [],
            "outputs": ["research_data"]
        },
        "content_architect": {
            "role": "test_creation",
            "priority": 2,
            "dependencies": ["research_agent"],
            "outputs": ["psychological_tests"]
        },
        "test_generator": {
            "role": "test_instantiation",
            "priority": 3,
            "dependencies": ["content_architect"],
            "outputs": ["test_instances"]
        },
        "quality_guardian": {
            "role": "comprehensive_qa",
            "priority": 4,
            "dependencies": ["content_architect", "test_generator"],
            "outputs": ["detailed_quality_reports"]
        },
        "transformation_planner": {
            "role": "program_creation",
            "priority": 5,
            "dependencies": ["content_architect", "quality_guardian"],
            "outputs": ["transformation_programs"]
        }
    },
    quality_gates={
        "patternshift_compliance": {"threshold": 0.90, "required": True, "validator": "quality_guardian"},
        "clinical_accuracy": {"threshold": 0.95, "required": True, "validator": "quality_guardian"},
        "vak_adaptations": {"threshold": 0.85, "required": True, "validator": "content_architect"},
        "language_quality": {"threshold": 0.90, "required": True, "validator": "quality_guardian"},
        "transformation_viability": {"threshold": 0.80, "required": True, "validator": "transformation_planner"}
    }
)

QUALITY_FOCUSED_CONFIG = OrchestratorDependencies(
    project_type="quality_assurance",
    orchestration_level="quality_focused",
    workflow_complexity="advanced",
    agent_workflow={
        "quality_guardian": {
            "role": "primary_validation",
            "priority": 1,
            "dependencies": [],
            "outputs": ["quality_assessment"]
        },
        "content_architect": {
            "role": "improvement_recommendations",
            "priority": 2,
            "dependencies": ["quality_guardian"],
            "outputs": ["improvement_plan"]
        }
    },
    quality_gates={
        "overall_quality": {"threshold": 0.85, "required": True, "validator": "quality_guardian"},
        "methodology_compliance": {"threshold": 0.90, "required": True, "validator": "quality_guardian"},
        "improvement_feasibility": {"threshold": 0.75, "required": False, "validator": "content_architect"}
    }
)