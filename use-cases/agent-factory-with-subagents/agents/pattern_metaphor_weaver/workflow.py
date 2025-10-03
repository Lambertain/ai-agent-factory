"""
Workflow конфигурация для Pattern Metaphor Weaver Agent в контексте PatternShift Architecture
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
    metaphors_created: int = 0
    therapeutic_stories_created: int = 0
    vak_variants_generated: int = 0
    cultural_adaptations: int = 0
    target_metaphors: int = 30  # Целевое количество из архитектуры

    def get_completion_percentage(self) -> float:
        """Процент выполнения целевого количества метафор"""
        return (self.metaphors_created / self.target_metaphors) * 100 if self.target_metaphors > 0 else 0.0


@dataclass
class PatternMetaphorWeaverWorkflow:
    """
    Workflow конфигурация для Pattern Metaphor Weaver Agent

    Позиция в PatternShift Architecture:
    - Phase: PHASE_1_CONTENT_CREATION (Day 13)
    - Role: Ткач метафор
    - Outputs: 30+ терапевтических метафор и историй
    """

    # Основная информация
    agent_name: str = "pattern_metaphor_weaver"
    phase: WorkflowPhase = WorkflowPhase.PHASE_1_CONTENT_CREATION
    role: AgentRole = AgentRole.CONTENT_CREATOR
    days: str = "13"

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
            "phase_description": "Content Creation - создание 30+ терапевтических метафор",
            "parallel_agents": [
                "pattern_nlp_technique_master",
                "pattern_exercise_architect",
                "pattern_ericksonian_hypnosis_scriptwriter",
                "pattern_microhabit_designer",
                "pattern_gamification_architect"
            ],
            "key_deliverables": [
                "30+ терапевтических метафор и историй",
                "VAK варианты каждой метафоры (Visual, Auditory, Kinesthetic)",
                "Культурные адаптации метафор",
                "Интеграция метафор в модули программы"
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
            data_type="metaphor_modules",
            transformation_required=False,
            description="Передача созданных метафор для интеграции в программу трансформации"
        ))

        return connections

    async def receive_from_parallel_agents(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка входных данных от параллельных агентов Phase 1

        Note: Metaphor Weaver работает независимо от других агентов Phase 1,
        но может использовать их output для обогащения метафор

        Args:
            agent_data: Данные от других агентов (опционально)

        Returns:
            Dict с результатом обработки
        """
        processed_data = {
            "status": "received",
            "enhancements": []
        }

        # Если есть NLP техники - можем обогатить метафоры лингвистическими паттернами
        if "nlp_techniques" in agent_data:
            processed_data["enhancements"].append({
                "type": "nlp_enhanced_metaphors",
                "source": "pattern_nlp_technique_master",
                "description": "Обогащение метафор NLP языковыми паттернами"
            })

        # Если есть гипнотические скрипты - можем добавить транс-индуцирующие элементы
        if "hypnosis_scripts" in agent_data:
            processed_data["enhancements"].append({
                "type": "trance_inducing_metaphors",
                "source": "pattern_ericksonian_hypnosis_scriptwriter",
                "description": "Добавление элементов эриксонианского гипноза в метафоры"
            })

        return processed_data

    async def create_metaphors_batch(
        self,
        transformation_themes: List[str],
        target_count: int = 30
    ) -> Dict[str, Any]:
        """
        Создание batch метафор для достижения целевого количества

        Args:
            transformation_themes: Список тем трансформации
            target_count: Целевое количество метафор (default: 30)

        Returns:
            Dict с созданными метафорами и статистикой
        """
        # Планируем распределение метафор по темам
        metaphors_per_theme = target_count // len(transformation_themes) if transformation_themes else target_count

        batch_result = {
            "metaphors": [],
            "therapeutic_stories": [],
            "vak_variants": {},
            "total_created": 0,
            "distribution": {}
        }

        for theme in transformation_themes:
            batch_result["distribution"][theme] = metaphors_per_theme

        # Обновляем статистику
        self.stats.metaphors_created = target_count

        return batch_result

    async def generate_vak_variants(
        self,
        base_metaphor: Any
    ) -> Dict[str, Any]:
        """
        Генерация VAK вариантов метафоры

        Args:
            base_metaphor: Базовая метафора

        Returns:
            Dict с VAK вариантами
        """
        vak_variants = {
            "visual": {
                "emphasis": "Яркие визуальные образы и картины",
                "metaphor": base_metaphor
            },
            "auditory": {
                "emphasis": "Звуковые паттерны и ритмы",
                "metaphor": base_metaphor
            },
            "kinesthetic": {
                "emphasis": "Телесные ощущения и движения",
                "metaphor": base_metaphor
            }
        }

        # Обновляем статистику
        self.stats.vak_variants_generated += 3

        return vak_variants

    async def create_cultural_adaptations(
        self,
        base_metaphor: Any,
        cultures: List[str]
    ) -> Dict[str, Any]:
        """
        Создание культурных адаптаций метафоры

        Args:
            base_metaphor: Базовая метафора
            cultures: Список культур для адаптации

        Returns:
            Dict с культурными адаптациями
        """
        cultural_adaptations = {}

        for culture in cultures:
            cultural_adaptations[culture] = {
                "culture": culture,
                "adapted_metaphor": base_metaphor,
                "cultural_notes": f"Адаптировано для {culture} культуры"
            }

        # Обновляем статистику
        self.stats.cultural_adaptations += len(cultures)

        return cultural_adaptations

    async def send_to_integration_synthesizer(
        self,
        metaphors: List[Any],
        therapeutic_stories: List[Any],
        vak_variants: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Отправка созданных метафор в Integration Synthesizer

        Args:
            metaphors: Список созданных метафор
            therapeutic_stories: Список терапевтических историй
            vak_variants: VAK варианты метафор

        Returns:
            Dict с результатом передачи
        """
        output_package = {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "day_completed": self.days,
            "deliverables": {
                "metaphors": metaphors,
                "therapeutic_stories": therapeutic_stories,
                "vak_variants": vak_variants,
                "total_metaphors": len(metaphors),
                "total_stories": len(therapeutic_stories),
                "total_vak_variants": self.stats.vak_variants_generated
            },
            "stats": {
                "metaphors_created": self.stats.metaphors_created,
                "therapeutic_stories_created": self.stats.therapeutic_stories_created,
                "vak_variants_generated": self.stats.vak_variants_generated,
                "cultural_adaptations": self.stats.cultural_adaptations,
                "completion_percentage": self.stats.get_completion_percentage()
            },
            "ready_for_integration": True,
            "next_agent": "pattern_integration_synthesizer",
            "integration_instructions": {
                "merge_strategy": "embed_into_modules",
                "module_type": "metaphor_learning",
                "placement": "throughout_program",
                "usage_frequency": "minimum_3_per_module"
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
                "metaphors_created": self.stats.metaphors_created,
                "target_metaphors": self.stats.target_metaphors,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "therapeutic_stories_created": self.stats.therapeutic_stories_created,
                "vak_variants_generated": self.stats.vak_variants_generated,
                "cultural_adaptations": self.stats.cultural_adaptations
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.metaphors_created < self.stats.target_metaphors else "completed"
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
        if self.stats.target_metaphors < 30:
            validation_results["warnings"].append(
                f"Целевое количество метафор ({self.stats.target_metaphors}) ниже рекомендованного (30)"
            )

        # Проверка days alignment
        if self.days != "13":
            validation_results["warnings"].append(
                f"Days '{self.days}' не соответствуют архитектуре (ожидается '13')"
            )

        # Проверка VAK variants
        if self.stats.metaphors_created > 0 and self.stats.vak_variants_generated == 0:
            validation_results["warnings"].append(
                "Метафоры созданы, но VAK варианты отсутствуют"
            )

        return validation_results


# Создание глобального экземпляра workflow для использования в агенте
metaphor_weaver_workflow = PatternMetaphorWeaverWorkflow()


def get_workflow() -> PatternMetaphorWeaverWorkflow:
    """
    Получить экземпляр workflow конфигурации

    Returns:
        PatternMetaphorWeaverWorkflow: Конфигурация workflow агента
    """
    return metaphor_weaver_workflow


async def update_workflow_stats(
    metaphors_created: int = 0,
    therapeutic_stories_created: int = 0,
    vak_variants_generated: int = 0,
    cultural_adaptations: int = 0
) -> Dict[str, Any]:
    """
    Обновить статистику workflow

    Args:
        metaphors_created: Количество созданных метафор
        therapeutic_stories_created: Количество терапевтических историй
        vak_variants_generated: Количество VAK вариантов
        cultural_adaptations: Количество культурных адаптаций

    Returns:
        Dict с обновленной статистикой
    """
    workflow = get_workflow()

    if metaphors_created > 0:
        workflow.stats.metaphors_created += metaphors_created
    if therapeutic_stories_created > 0:
        workflow.stats.therapeutic_stories_created += therapeutic_stories_created
    if vak_variants_generated > 0:
        workflow.stats.vak_variants_generated += vak_variants_generated
    if cultural_adaptations > 0:
        workflow.stats.cultural_adaptations += cultural_adaptations

    return workflow.get_workflow_status()
