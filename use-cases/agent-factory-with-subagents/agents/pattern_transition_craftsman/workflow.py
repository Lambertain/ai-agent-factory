"""
Workflow конфигурация для Pattern Transition Craftsman Agent в контексте PatternShift Architecture
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
    transitions_created: int = 0
    bridge_elements_created: int = 0
    closure_scripts_created: int = 0
    opening_scripts_created: int = 0
    target_transitions: int = 40  # Целевое количество из архитектуры (между ~40+ модулями)

    def get_completion_percentage(self) -> float:
        """Процент выполнения целевого количества переходов"""
        return (self.transitions_created / self.target_transitions) * 100 if self.target_transitions > 0 else 0.0


@dataclass
class PatternTransitionCraftsmanWorkflow:
    """
    Workflow конфигурация для Pattern Transition Craftsman Agent

    Позиция в PatternShift Architecture:
    - Phase: PHASE_2_INTEGRATION_POLISH (Day 20)
    - Role: Интегратор переходов и связей
    - Outputs: Связующие элементы между модулями программы
    """

    # Основная информация
    agent_name: str = "pattern_transition_craftsman"
    phase: WorkflowPhase = WorkflowPhase.PHASE_2_INTEGRATION_POLISH
    role: AgentRole = AgentRole.INTEGRATOR
    days: str = "20"

    # Входящие связи (получает от Integration Synthesizer)
    receives_from: List[str] = field(default_factory=lambda: ["pattern_integration_synthesizer"])

    # Исходящие связи (отправляет в Phase 3 валидаторов)
    outputs_to: List[str] = field(default_factory=lambda: [
        "pattern_safety_protocol",
        "pattern_scientific_validator"
    ])

    # Статистика
    stats: WorkflowStats = field(default_factory=WorkflowStats)

    # Метаданные workflow
    workflow_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация метаданных workflow"""
        self.workflow_metadata = {
            "phase_description": "Integration & Polish - создание связующих элементов между модулями",
            "parallel_agents": [
                "pattern_feedback_orchestrator",
                "pattern_progress_narrator"
            ],
            "key_deliverables": [
                "40+ переходов между модулями программы",
                "Closure scripts для завершения модулей",
                "Opening scripts для начала новых модулей",
                "Bridge elements связывающие разные типы активностей",
                "Flow maintenance механизмы"
            ],
            "integration_source": "pattern_integration_synthesizer",
            "validation_targets": ["pattern_safety_protocol", "pattern_scientific_validator"],
            "transition_structure": {
                "closure": "30% - завершение предыдущего модуля",
                "bridge": "40% - связь старого и нового",
                "opening": "30% - подготовка к новому модулю"
            },
            "theoretical_frameworks": [
                "Flow Theory (Csikszentmihalyi, 1990)",
                "Gestalt Closure Principle",
                "Attention Management",
                "Energy Transitions"
            ]
        }

    def get_workflow_connections(self) -> List[WorkflowConnection]:
        """
        Получить все workflow связи агента

        Returns:
            List[WorkflowConnection]: Список связей с другими агентами
        """
        connections = []

        # Входящая связь от Integration Synthesizer
        connections.append(WorkflowConnection(
            source_agent="pattern_integration_synthesizer",
            target_agent=self.agent_name,
            data_type="integrated_program_with_module_sequence",
            transformation_required=True,
            description="Получение интегрированной программы для создания переходов между модулями"
        ))

        # Исходящие связи к валидаторам Phase 3
        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_safety_protocol",
            data_type="transition_elements_with_flow",
            transformation_required=False,
            description="Передача связующих элементов для проверки безопасности переходов"
        ))

        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_scientific_validator",
            data_type="coherence_mechanisms",
            transformation_required=False,
            description="Передача механизмов когерентности для научной валидации"
        ))

        return connections

    async def receive_from_integration_synthesizer(
        self,
        integrated_program: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Обработка интегрированной программы от Integration Synthesizer

        Args:
            integrated_program: Интегрированная программа трансформации

        Returns:
            Dict с результатом обработки
        """
        processed_data = {
            "status": "received",
            "total_modules": len(integrated_program.get("modules", [])),
            "transitions_needed": 0,
            "module_pairs": []
        }

        # Определяем пары модулей для создания переходов
        modules = integrated_program.get("modules", [])
        for i in range(len(modules) - 1):
            current_module = modules[i]
            next_module = modules[i + 1]

            module_pair = {
                "from_module": current_module.get("name"),
                "to_module": next_module.get("name"),
                "modality_shift": self._detect_modality_shift(current_module, next_module),
                "energy_shift": self._detect_energy_shift(current_module, next_module)
            }

            processed_data["module_pairs"].append(module_pair)
            processed_data["transitions_needed"] += 1

        return processed_data

    def _detect_modality_shift(self, current: Dict[str, Any], next_module: Dict[str, Any]) -> str:
        """Определить смену модальности между модулями"""
        current_type = current.get("type", "")
        next_type = next_module.get("type", "")

        if current_type == next_type:
            return "same_modality"
        elif "cognitive" in current_type and "somatic" in next_type:
            return "cognitive_to_somatic"
        elif "somatic" in current_type and "cognitive" in next_type:
            return "somatic_to_cognitive"
        else:
            return "mixed_modality"

    def _detect_energy_shift(self, current: Dict[str, Any], next_module: Dict[str, Any]) -> str:
        """Определить смену энергетического уровня между модулями"""
        current_intensity = current.get("intensity", 5)
        next_intensity = next_module.get("intensity", 5)

        if next_intensity > current_intensity + 2:
            return "significant_increase"
        elif next_intensity < current_intensity - 2:
            return "significant_decrease"
        elif next_intensity > current_intensity:
            return "gradual_increase"
        elif next_intensity < current_intensity:
            return "gradual_decrease"
        else:
            return "stable"

    async def create_transitions_batch(
        self,
        module_pairs: List[Dict[str, Any]],
        target_count: int = 40
    ) -> Dict[str, Any]:
        """
        Создание batch переходов между модулями

        Args:
            module_pairs: Пары модулей для создания переходов
            target_count: Целевое количество переходов (default: 40)

        Returns:
            Dict с созданными переходами
        """
        batch_result = {
            "transitions": [],
            "closure_scripts": [],
            "bridge_elements": [],
            "opening_scripts": [],
            "total_created": 0,
            "distribution_by_type": {}
        }

        # Распределяем переходы по типам
        transition_types = {
            "cognitive_to_cognitive": len([p for p in module_pairs if p.get("modality_shift") == "same_modality"]),
            "cognitive_to_somatic": len([p for p in module_pairs if p.get("modality_shift") == "cognitive_to_somatic"]),
            "somatic_to_cognitive": len([p for p in module_pairs if p.get("modality_shift") == "somatic_to_cognitive"]),
            "energy_increase": len([p for p in module_pairs if "increase" in p.get("energy_shift", "")]),
            "energy_decrease": len([p for p in module_pairs if "decrease" in p.get("energy_shift", "")])
        }

        for transition_type, count in transition_types.items():
            batch_result["distribution_by_type"][transition_type] = count

        # Обновляем статистику
        self.stats.transitions_created = min(target_count, len(module_pairs))

        return batch_result

    async def create_closure_scripts(
        self,
        modules: List[Any]
    ) -> Dict[str, Any]:
        """
        Создание closure scripts для завершения модулей

        Args:
            modules: Список модулей программы

        Returns:
            Dict с closure скриптами
        """
        closure_scripts = {
            "general_closure": {
                "structure": "Отлично! Вы завершили [модуль]. Это важный milestone.",
                "elements": [
                    "Acknowledgment - признание выполненной работы",
                    "Summary - краткое резюме ключевых моментов",
                    "Integration - связь с общей целью программы"
                ],
                "duration": "30-60 секунд"
            },
            "cognitive_module_closure": {
                "structure": "Вы освоили [техника/концепция]. Этот навык станет частью вашего инструментария.",
                "focus": "Закрепление понимания",
                "next_step_hint": "Намек на практическое применение"
            },
            "somatic_module_closure": {
                "structure": "Заметьте изменения в теле. Это ваш новый ресурсный опыт.",
                "focus": "Anchoring телесного опыта",
                "grounding": "Возвращение к baseline состоянию"
            },
            "emotional_module_closure": {
                "structure": "Вы работали с глубокими чувствами. Это требует мужества.",
                "focus": "Validation эмоционального процесса",
                "safety": "Обеспечение эмоциональной безопасности"
            }
        }

        # Обновляем статистику
        self.stats.closure_scripts_created = len(closure_scripts)

        return {
            "closure_scripts": closure_scripts,
            "total_scripts": len(closure_scripts),
            "framework": "Gestalt Closure Principle"
        }

    async def create_bridge_elements(
        self,
        module_pairs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Создание bridge elements для связи модулей

        Args:
            module_pairs: Пары модулей

        Returns:
            Dict с bridge элементами
        """
        bridge_elements = {
            "conceptual_bridges": {
                "type": "Связь через общую концепцию",
                "structure": "В [предыдущий модуль] вы изучили [X]. Теперь применим это к [Y].",
                "purpose": "Создание преемственности понимания"
            },
            "anchor_bridges": {
                "type": "Использование якорей из предыдущего",
                "structure": "Помните ощущение [якорь из предыдущего]? Используйте его как ресурс.",
                "purpose": "Активация предыдущего опыта"
            },
            "metaphor_bridges": {
                "type": "Расширение метафоры",
                "structure": "Если [предыдущая метафора], то следующий шаг - [продолжение метафоры].",
                "purpose": "Поддержание нарративной целостности"
            },
            "contrast_bridges": {
                "type": "Контраст для выделения нового",
                "structure": "Мы работали с [X]. Теперь посмотрим на это с другой стороны - [Y].",
                "purpose": "Подготовка к смене перспективы"
            }
        }

        # Обновляем статистику
        self.stats.bridge_elements_created = len(bridge_elements)

        return {
            "bridge_elements": bridge_elements,
            "total_elements": len(bridge_elements),
            "optimal_length": "2-3 sentences"
        }

    async def create_opening_scripts(
        self,
        modules: List[Any]
    ) -> Dict[str, Any]:
        """
        Создание opening scripts для начала новых модулей

        Args:
            modules: Список модулей программы

        Returns:
            Dict с opening скриптами
        """
        opening_scripts = {
            "general_opening": {
                "structure": "Добро пожаловать в [модуль]. Здесь мы исследуем [тема].",
                "elements": [
                    "Welcoming - создание комфорта",
                    "Preview - краткое представление",
                    "Relevance - почему это важно",
                    "First step - конкретное первое действие"
                ],
                "duration": "30-60 секунд"
            },
            "challenge_opening": {
                "structure": "Следующее упражнение может показаться сложным. Это нормально - вы готовы.",
                "focus": "Подготовка к сложности",
                "reassurance": "Нормализация трудностей"
            },
            "ease_opening": {
                "structure": "Этот модуль дает передышку. Наслаждайтесь процессом.",
                "focus": "Разрешение расслабиться",
                "permission": "Отпустить усилия"
            },
            "integration_opening": {
                "structure": "Теперь соединим все изученное. Вы увидите как части складываются в целое.",
                "focus": "Synthesis и большая картина",
                "anticipation": "Создание ожидания инсайта"
            }
        }

        # Обновляем статистику
        self.stats.opening_scripts_created = len(opening_scripts)

        return {
            "opening_scripts": opening_scripts,
            "total_scripts": len(opening_scripts),
            "framework": "Attention Management"
        }

    async def create_flow_maintenance_mechanisms(
        self,
        program_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Создание механизмов поддержания flow

        Args:
            program_structure: Структура программы

        Returns:
            Dict с flow maintenance механизмами
        """
        flow_mechanisms = {
            "challenge_balance": {
                "principle": "Поддерживать баланс сложности и навыков",
                "implementation": "Gradual difficulty scaling через модули",
                "monitoring": "Feedback на perceived difficulty"
            },
            "clear_goals": {
                "principle": "Ясные цели на каждом этапе",
                "implementation": "Explicit mini-goals в переходах",
                "verification": "User awareness check"
            },
            "immediate_feedback": {
                "principle": "Немедленная обратная связь",
                "implementation": "In-module progress indicators",
                "timing": "Within 30 seconds of action"
            },
            "focus_maintenance": {
                "principle": "Сохранение фокуса внимания",
                "implementation": "Minimal cognitive load в переходах",
                "duration": "Transitions under 90 seconds"
            }
        }

        return {
            "flow_mechanisms": flow_mechanisms,
            "total_mechanisms": len(flow_mechanisms),
            "framework": "Flow Theory (Csikszentmihalyi, 1990)"
        }

    async def send_to_phase3_validators(
        self,
        transitions: List[Any],
        closure_scripts: Dict[str, Any],
        bridge_elements: Dict[str, Any],
        opening_scripts: Dict[str, Any],
        flow_mechanisms: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Отправка связующих элементов в валидаторы Phase 3

        Args:
            transitions: Переходы между модулями
            closure_scripts: Closure скрипты
            bridge_elements: Bridge элементы
            opening_scripts: Opening скрипты
            flow_mechanisms: Flow maintenance механизмы

        Returns:
            Dict с результатом передачи
        """
        output_package = {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "day_completed": self.days,
            "deliverables": {
                "transitions": transitions,
                "closure_scripts": closure_scripts,
                "bridge_elements": bridge_elements,
                "opening_scripts": opening_scripts,
                "flow_mechanisms": flow_mechanisms,
                "total_transitions": len(transitions),
                "total_closures": self.stats.closure_scripts_created,
                "total_bridges": self.stats.bridge_elements_created,
                "total_openings": self.stats.opening_scripts_created
            },
            "stats": {
                "transitions_created": self.stats.transitions_created,
                "closure_scripts_created": self.stats.closure_scripts_created,
                "bridge_elements_created": self.stats.bridge_elements_created,
                "opening_scripts_created": self.stats.opening_scripts_created,
                "completion_percentage": self.stats.get_completion_percentage()
            },
            "ready_for_validation": True,
            "next_agents": self.outputs_to,
            "validation_instructions": {
                "safety_protocol": {
                    "focus": "Проверка переходов на отсутствие резких shift'ов и дезориентации",
                    "criteria": ["Smooth transitions", "Clear orientation", "No jarring shifts"]
                },
                "scientific_validator": {
                    "focus": "Валидация эффективности flow maintenance",
                    "criteria": ["Flow Theory alignment", "Coherence evidence", "Attention management"]
                }
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
                "transitions_created": self.stats.transitions_created,
                "target_transitions": self.stats.target_transitions,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "closure_scripts_created": self.stats.closure_scripts_created,
                "bridge_elements_created": self.stats.bridge_elements_created,
                "opening_scripts_created": self.stats.opening_scripts_created
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.transitions_created < self.stats.target_transitions else "completed"
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

        # Проверка входящей связи
        if "pattern_integration_synthesizer" not in self.receives_from:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                "Отсутствует обязательная входящая связь от pattern_integration_synthesizer"
            )

        # Проверка исходящих связей к валидаторам
        required_validators = ["pattern_safety_protocol", "pattern_scientific_validator"]
        for validator in required_validators:
            if validator not in self.outputs_to:
                validation_results["warnings"].append(
                    f"Отсутствует связь с валидатором {validator}"
                )

        # Проверка целевого количества
        if self.stats.target_transitions < 40:
            validation_results["warnings"].append(
                f"Целевое количество переходов ({self.stats.target_transitions}) ниже рекомендованного (40)"
            )

        # Проверка days alignment
        if self.days != "20":
            validation_results["warnings"].append(
                f"Days '{self.days}' не соответствуют архитектуре (ожидается '20')"
            )

        # Проверка баланса компонентов переходов
        if self.stats.transitions_created > 0:
            if self.stats.closure_scripts_created == 0:
                validation_results["warnings"].append(
                    "Переходы созданы, но closure скрипты отсутствуют"
                )
            if self.stats.opening_scripts_created == 0:
                validation_results["warnings"].append(
                    "Переходы созданы, но opening скрипты отсутствуют"
                )
            if self.stats.bridge_elements_created == 0:
                validation_results["warnings"].append(
                    "Переходы созданы, но bridge элементы отсутствуют"
                )

        return validation_results


# Создание глобального экземпляра workflow для использования в агенте
transition_craftsman_workflow = PatternTransitionCraftsmanWorkflow()


def get_workflow() -> PatternTransitionCraftsmanWorkflow:
    """
    Получить экземпляр workflow конфигурации

    Returns:
        PatternTransitionCraftsmanWorkflow: Конфигурация workflow агента
    """
    return transition_craftsman_workflow


async def update_workflow_stats(
    transitions_created: int = 0,
    closure_scripts_created: int = 0,
    bridge_elements_created: int = 0,
    opening_scripts_created: int = 0
) -> Dict[str, Any]:
    """
    Обновить статистику workflow

    Args:
        transitions_created: Количество созданных переходов
        closure_scripts_created: Количество closure скриптов
        bridge_elements_created: Количество bridge элементов
        opening_scripts_created: Количество opening скриптов

    Returns:
        Dict с обновленной статистикой
    """
    workflow = get_workflow()

    if transitions_created > 0:
        workflow.stats.transitions_created += transitions_created
    if closure_scripts_created > 0:
        workflow.stats.closure_scripts_created += closure_scripts_created
    if bridge_elements_created > 0:
        workflow.stats.bridge_elements_created += bridge_elements_created
    if opening_scripts_created > 0:
        workflow.stats.opening_scripts_created += opening_scripts_created

    return workflow.get_workflow_status()
