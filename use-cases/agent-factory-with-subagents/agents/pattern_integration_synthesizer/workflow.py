"""
Workflow конфигурация для Pattern Integration Synthesizer Agent в контексте PatternShift Architecture

⚠️ КРИТИЧЕСКИ ВАЖНЫЙ АГЕНТ - Интегратор всех компонентов Phase 1 в единую программу
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
    modules_integrated: int = 0
    components_merged: int = 0
    synergies_created: int = 0
    conflicts_resolved: int = 0
    target_modules: int = 460  # 460 модулей из архитектуры

    # Статистика по каждому источнику
    nlp_techniques_integrated: int = 0
    exercises_integrated: int = 0
    hypnosis_scripts_integrated: int = 0
    microhabits_integrated: int = 0
    metaphors_integrated: int = 0
    gamification_integrated: int = 0

    def get_completion_percentage(self) -> float:
        """Процент выполнения интеграции"""
        return (self.modules_integrated / self.target_modules) * 100 if self.target_modules > 0 else 0.0

    def get_source_coverage(self) -> Dict[str, bool]:
        """Проверка покрытия всех источников"""
        return {
            "nlp_techniques": self.nlp_techniques_integrated > 0,
            "exercises": self.exercises_integrated > 0,
            "hypnosis_scripts": self.hypnosis_scripts_integrated > 0,
            "microhabits": self.microhabits_integrated > 0,
            "metaphors": self.metaphors_integrated > 0,
            "gamification": self.gamification_integrated > 0
        }


@dataclass
class PatternIntegrationSynthesizerWorkflow:
    """
    Workflow конфигурация для Pattern Integration Synthesizer Agent

    ⚠️ КРИТИЧЕСКАЯ ПОЗИЦИЯ В АРХИТЕКТУРЕ:
    - Phase: PHASE_2_INTEGRATION_POLISH (Days 15-17)
    - Role: Интегратор-синтезатор - СОБИРАЕТ ВСЕ компоненты из Phase 1
    - Receives from: 6 агентов Phase 1
    - Outputs to: 3 агента Phase 2 (feedback_orchestrator, progress_narrator, transition_craftsman)
    """

    # Основная информация
    agent_name: str = "pattern_integration_synthesizer"
    phase: WorkflowPhase = WorkflowPhase.PHASE_2_INTEGRATION_POLISH
    role: AgentRole = AgentRole.INTEGRATOR
    days: str = "15-17"

    # Входящие связи - ВСЕ 6 агентов Phase 1
    receives_from: List[str] = field(default_factory=lambda: [
        "pattern_nlp_technique_master",
        "pattern_exercise_architect",
        "pattern_ericksonian_hypnosis_scriptwriter",
        "pattern_microhabit_designer",
        "pattern_metaphor_weaver",
        "pattern_gamification_architect"
    ])

    # Исходящие связи - 3 агента Phase 2
    outputs_to: List[str] = field(default_factory=lambda: [
        "pattern_feedback_orchestrator",
        "pattern_progress_narrator",
        "pattern_transition_craftsman"
    ])

    # Статистика
    stats: WorkflowStats = field(default_factory=WorkflowStats)

    # Метаданные workflow
    workflow_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация метаданных workflow"""
        self.workflow_metadata = {
            "phase_description": "Integration & Polish - сборка 460 модулей в единую программу",
            "critical_role": "ЕДИНСТВЕННЫЙ АГЕНТ, который получает ВСЕ outputs Phase 1",
            "integration_strategy": "Модульная архитектура с синергией компонентов",
            "key_deliverables": [
                "460 интегрированных модулей программы трансформации",
                "Единая структура программы с логическими связями",
                "Синергетические комбинации компонентов",
                "Разрешение конфликтов между техниками",
                "Оптимизированная последовательность модулей"
            ],
            "integration_targets": {
                "feedback_orchestrator": "Адаптивная обратная связь",
                "progress_narrator": "Нарратив прогресса",
                "transition_craftsman": "Плавные переходы между модулями"
            },
            "expected_duration": "3 дня (Days 15-17)"
        }

    def get_workflow_connections(self) -> List[WorkflowConnection]:
        """
        Получить все workflow связи агента

        Returns:
            List[WorkflowConnection]: Список связей с другими агентами
        """
        connections = []

        # ВХОДЯЩИЕ связи от 6 агентов Phase 1
        phase1_agents = {
            "pattern_nlp_technique_master": "nlp_modules",
            "pattern_exercise_architect": "exercise_modules",
            "pattern_ericksonian_hypnosis_scriptwriter": "hypnosis_modules",
            "pattern_microhabit_designer": "microhabit_modules",
            "pattern_metaphor_weaver": "metaphor_modules",
            "pattern_gamification_architect": "gamification_modules"
        }

        for source_agent, data_type in phase1_agents.items():
            connections.append(WorkflowConnection(
                source_agent=source_agent,
                target_agent=self.agent_name,
                data_type=data_type,
                transformation_required=True,
                description=f"Получение {data_type} для интеграции в программу"
            ))

        # ИСХОДЯЩИЕ связи к 3 агентам Phase 2
        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_feedback_orchestrator",
            data_type="integrated_program",
            transformation_required=False,
            description="Передача интегрированной программы для настройки обратной связи"
        ))

        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_progress_narrator",
            data_type="integrated_program",
            transformation_required=False,
            description="Передача программы для создания нарратива прогресса"
        ))

        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_transition_craftsman",
            data_type="integrated_program",
            transformation_required=False,
            description="Передача программы для создания плавных переходов"
        ))

        return connections

    async def receive_from_phase1_agents(self, phase1_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        КРИТИЧЕСКАЯ ФУНКЦИЯ: Прием outputs от ВСЕХ 6 агентов Phase 1

        Args:
            phase1_outputs: Словарь с outputs от каждого агента Phase 1
                Expected keys: nlp_techniques, exercises, hypnosis_scripts,
                              microhabits, metaphors, gamification

        Returns:
            Dict с результатом обработки и готовностью к интеграции
        """
        processing_result = {
            "status": "processing",
            "received_components": {},
            "missing_components": [],
            "ready_for_integration": False,
            "conflicts_detected": [],
            "synergy_opportunities": []
        }

        # Проверяем наличие outputs от каждого агента
        required_components = {
            "nlp_techniques": "pattern_nlp_technique_master",
            "exercises": "pattern_exercise_architect",
            "hypnosis_scripts": "pattern_ericksonian_hypnosis_scriptwriter",
            "microhabits": "pattern_microhabit_designer",
            "metaphors": "pattern_metaphor_weaver",
            "gamification": "pattern_gamification_architect"
        }

        for component_key, agent_name in required_components.items():
            if component_key in phase1_outputs and phase1_outputs[component_key]:
                processing_result["received_components"][component_key] = {
                    "source": agent_name,
                    "count": len(phase1_outputs[component_key]) if isinstance(phase1_outputs[component_key], list) else 1,
                    "status": "received"
                }

                # Обновляем статистику по источнику
                if component_key == "nlp_techniques":
                    self.stats.nlp_techniques_integrated = len(phase1_outputs[component_key])
                elif component_key == "exercises":
                    self.stats.exercises_integrated = len(phase1_outputs[component_key])
                elif component_key == "hypnosis_scripts":
                    self.stats.hypnosis_scripts_integrated = len(phase1_outputs[component_key])
                elif component_key == "microhabits":
                    self.stats.microhabits_integrated = len(phase1_outputs[component_key])
                elif component_key == "metaphors":
                    self.stats.metaphors_integrated = len(phase1_outputs[component_key])
                elif component_key == "gamification":
                    self.stats.gamification_integrated = len(phase1_outputs[component_key])
            else:
                processing_result["missing_components"].append({
                    "component": component_key,
                    "source_agent": agent_name,
                    "status": "missing"
                })

        # Определяем готовность к интеграции
        processing_result["ready_for_integration"] = len(processing_result["missing_components"]) == 0

        # Анализ потенциальных синергий
        if len(processing_result["received_components"]) >= 2:
            processing_result["synergy_opportunities"] = await self._identify_synergies(processing_result["received_components"])

        # Анализ потенциальных конфликтов
        processing_result["conflicts_detected"] = await self._detect_conflicts(processing_result["received_components"])

        return processing_result

    async def _identify_synergies(self, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Идентификация синергетических возможностей между компонентами"""
        synergies = []

        # NLP + Hypnosis синергия
        if "nlp_techniques" in components and "hypnosis_scripts" in components:
            synergies.append({
                "type": "linguistic_trance",
                "components": ["nlp_techniques", "hypnosis_scripts"],
                "benefit": "Усиление гипнотических паттернов через NLP техники"
            })

        # Microhabits + Gamification синергия
        if "microhabits" in components and "gamification" in components:
            synergies.append({
                "type": "gamified_habits",
                "components": ["microhabits", "gamification"],
                "benefit": "Геймификация процесса формирования привычек"
            })

        # Metaphors + Exercises синергия
        if "metaphors" in components and "exercises" in components:
            synergies.append({
                "type": "metaphorical_learning",
                "components": ["metaphors", "exercises"],
                "benefit": "Обогащение упражнений метафорами для глубокого обучения"
            })

        self.stats.synergies_created = len(synergies)
        return synergies

    async def _detect_conflicts(self, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Обнаружение потенциальных конфликтов между компонентами"""
        conflicts = []

        # Пример: слишком много hypnosis + gamification может снизить эффективность
        if "hypnosis_scripts" in components and "gamification" in components:
            conflicts.append({
                "type": "focus_conflict",
                "components": ["hypnosis_scripts", "gamification"],
                "issue": "Гипноз требует глубокой релаксации, gamification - активного вовлечения",
                "resolution": "Разделить по разным модулям или временным интервалам"
            })

        return conflicts

    async def integrate_into_program(
        self,
        phase1_components: Dict[str, Any],
        module_count: int = 460
    ) -> Dict[str, Any]:
        """
        КРИТИЧЕСКАЯ ФУНКЦИЯ: Интеграция всех компонентов в 460 модулей программы

        Args:
            phase1_components: Все компоненты от Phase 1 агентов
            module_count: Целевое количество модулей (default: 460)

        Returns:
            Dict с интегрированной программой
        """
        integrated_program = {
            "modules": [],
            "total_modules": module_count,
            "module_structure": {},
            "integration_metadata": {},
            "quality_metrics": {}
        }

        # Распределение компонентов по модулям
        component_distribution = await self._calculate_distribution(phase1_components, module_count)

        # Создание модулей с интеграцией компонентов
        for module_id in range(1, module_count + 1):
            module = await self._create_integrated_module(module_id, phase1_components, component_distribution)
            integrated_program["modules"].append(module)

        # Обновляем статистику
        self.stats.modules_integrated = len(integrated_program["modules"])
        self.stats.components_merged = sum([
            self.stats.nlp_techniques_integrated,
            self.stats.exercises_integrated,
            self.stats.hypnosis_scripts_integrated,
            self.stats.microhabits_integrated,
            self.stats.metaphors_integrated,
            self.stats.gamification_integrated
        ])

        integrated_program["quality_metrics"] = {
            "completion_percentage": self.stats.get_completion_percentage(),
            "source_coverage": self.stats.get_source_coverage(),
            "synergies_created": self.stats.synergies_created,
            "conflicts_resolved": self.stats.conflicts_resolved
        }

        return integrated_program

    async def _calculate_distribution(self, components: Dict[str, Any], module_count: int) -> Dict[str, Any]:
        """Расчет распределения компонентов по модулям"""
        return {
            "modules_per_component": module_count // 6,  # 6 типов компонентов
            "flexible_allocation": True,
            "priority_order": [
                "nlp_techniques",  # Базовые техники идут первыми
                "exercises",
                "microhabits",
                "metaphors",
                "hypnosis_scripts",
                "gamification"
            ]
        }

    async def _create_integrated_module(
        self,
        module_id: int,
        components: Dict[str, Any],
        distribution: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Создание одного интегрированного модуля"""
        return {
            "module_id": module_id,
            "title": f"Transformation Module {module_id}",
            "components": [],
            "duration_minutes": 45,
            "difficulty": "adaptive",
            "integration_type": "synergistic"
        }

    async def send_to_phase2_agents(
        self,
        integrated_program: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Отправка интегрированной программы 3 агентам Phase 2

        Args:
            integrated_program: Полная интегрированная программа

        Returns:
            Dict с результатами передачи каждому агенту
        """
        phase2_outputs = {}

        # Передача feedback_orchestrator
        phase2_outputs["feedback_orchestrator"] = {
            "agent": "pattern_feedback_orchestrator",
            "data_sent": integrated_program,
            "purpose": "Создание системы адаптивной обратной связи",
            "status": "ready"
        }

        # Передача progress_narrator
        phase2_outputs["progress_narrator"] = {
            "agent": "pattern_progress_narrator",
            "data_sent": integrated_program,
            "purpose": "Создание нарратива прогресса пользователя",
            "status": "ready"
        }

        # Передача transition_craftsman
        phase2_outputs["transition_craftsman"] = {
            "agent": "pattern_transition_craftsman",
            "data_sent": integrated_program,
            "purpose": "Создание плавных переходов между модулями",
            "status": "ready"
        }

        return phase2_outputs

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
                "modules_integrated": self.stats.modules_integrated,
                "target_modules": self.stats.target_modules,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "components_merged": self.stats.components_merged,
                "synergies_created": self.stats.synergies_created,
                "conflicts_resolved": self.stats.conflicts_resolved,
                "source_coverage": self.stats.get_source_coverage()
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.modules_integrated < self.stats.target_modules else "completed"
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

        # Проверка Phase 2 requirements
        if self.phase != WorkflowPhase.PHASE_2_INTEGRATION_POLISH:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                f"Agent должен быть в PHASE_2_INTEGRATION_POLISH, текущая phase: {self.phase.value}"
            )

        # Проверка всех 6 входящих связей
        if len(self.receives_from) != 6:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                f"Должно быть 6 входящих связей от Phase 1, текущее количество: {len(self.receives_from)}"
            )

        # Проверка всех 3 исходящих связей
        if len(self.outputs_to) != 3:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                f"Должно быть 3 исходящих связи к Phase 2, текущее количество: {len(self.outputs_to)}"
            )

        # Проверка покрытия источников
        source_coverage = self.stats.get_source_coverage()
        missing_sources = [source for source, covered in source_coverage.items() if not covered]
        if missing_sources:
            validation_results["warnings"].append(
                f"Отсутствуют компоненты от источников: {', '.join(missing_sources)}"
            )

        # Проверка days alignment
        if self.days != "15-17":
            validation_results["warnings"].append(
                f"Days '{self.days}' не соответствуют архитектуре (ожидается '15-17')"
            )

        return validation_results


# Создание глобального экземпляра workflow для использования в агенте
integration_synthesizer_workflow = PatternIntegrationSynthesizerWorkflow()


def get_workflow() -> PatternIntegrationSynthesizerWorkflow:
    """
    Получить экземпляр workflow конфигурации

    Returns:
        PatternIntegrationSynthesizerWorkflow: Конфигурация workflow агента
    """
    return integration_synthesizer_workflow


async def update_workflow_stats(
    modules_integrated: int = 0,
    components_merged: int = 0,
    synergies_created: int = 0,
    conflicts_resolved: int = 0
) -> Dict[str, Any]:
    """
    Обновить статистику workflow

    Args:
        modules_integrated: Количество интегрированных модулей
        components_merged: Количество объединенных компонентов
        synergies_created: Количество созданных синергий
        conflicts_resolved: Количество разрешенных конфликтов

    Returns:
        Dict с обновленной статистикой
    """
    workflow = get_workflow()

    if modules_integrated > 0:
        workflow.stats.modules_integrated += modules_integrated
    if components_merged > 0:
        workflow.stats.components_merged += components_merged
    if synergies_created > 0:
        workflow.stats.synergies_created += synergies_created
    if conflicts_resolved > 0:
        workflow.stats.conflicts_resolved += conflicts_resolved

    return workflow.get_workflow_status()
