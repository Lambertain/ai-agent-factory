"""
Workflow конфигурация для Pattern Feedback Orchestrator Agent в контексте PatternShift Architecture
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
    feedback_forms_created: int = 0
    trigger_rules_designed: int = 0
    crisis_detection_systems: int = 0
    actionable_insights_generated: int = 0
    target_feedback_forms: int = 15  # Целевое количество из архитектуры

    def get_completion_percentage(self) -> float:
        """Процент выполнения целевого количества форм обратной связи"""
        return (self.feedback_forms_created / self.target_feedback_forms) * 100 if self.target_feedback_forms > 0 else 0.0


@dataclass
class PatternFeedbackOrchestratorWorkflow:
    """
    Workflow конфигурация для Pattern Feedback Orchestrator Agent

    Позиция в PatternShift Architecture:
    - Phase: PHASE_2_INTEGRATION_POLISH (Day 18)
    - Role: Интегратор обратной связи
    - Outputs: Системы обратной связи и триггерные правила
    """

    # Основная информация
    agent_name: str = "pattern_feedback_orchestrator"
    phase: WorkflowPhase = WorkflowPhase.PHASE_2_INTEGRATION_POLISH
    role: AgentRole = AgentRole.INTEGRATOR
    days: str = "18"

    # Входящие связи (получает от Integration Synthesizer)
    receives_from: List[str] = field(default_factory=lambda: ["pattern_integration_synthesizer"])

    # Исходящие связи (отправляет в Phase 3 валидаторам)
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
            "phase_description": "Integration & Polish - создание систем обратной связи и триггеров",
            "parallel_agents": [
                "pattern_progress_narrator",
                "pattern_transition_craftsman"
            ],
            "key_deliverables": [
                "Формы обратной связи для каждого модуля программы",
                "Триггерные правила маршрутизации",
                "Системы детекции кризисных состояний",
                "Actionable insights генераторы"
            ],
            "integration_source": "pattern_integration_synthesizer",
            "validation_targets": ["pattern_safety_protocol", "pattern_scientific_validator"],
            "timing_strategy": {
                "end_of_module": "Immediate feedback после модуля",
                "end_of_day": "Daily check-in",
                "mid_program": "Day 10-11 промежуточная оценка",
                "end_of_program": "Day 21 финальная оценка"
            }
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
            data_type="integrated_program_modules",
            transformation_required=True,
            description="Получение интегрированных модулей программы для создания систем обратной связи"
        ))

        # Исходящие связи к валидаторам Phase 3
        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_safety_protocol",
            data_type="feedback_systems_with_crisis_detection",
            transformation_required=False,
            description="Передача систем обратной связи с детекцией кризисов для валидации безопасности"
        ))

        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_scientific_validator",
            data_type="psychometric_instruments",
            transformation_required=False,
            description="Передача психометрических инструментов для научной валидации"
        ))

        return connections

    async def receive_from_integration_synthesizer(
        self,
        integrated_modules: List[Any]
    ) -> Dict[str, Any]:
        """
        Обработка интегрированной программы от Integration Synthesizer

        Args:
            integrated_modules: Модули интегрированной программы трансформации

        Returns:
            Dict с результатом обработки
        """
        processed_data = {
            "status": "received",
            "modules_count": len(integrated_modules),
            "feedback_points": []
        }

        # Определяем точки обратной связи для каждого модуля
        for module in integrated_modules:
            feedback_point = {
                "module_id": module.get("id"),
                "module_name": module.get("name"),
                "feedback_types": ["end_of_module", "difficulty_check"],
                "estimated_completion_time": module.get("duration_minutes", 30)
            }
            processed_data["feedback_points"].append(feedback_point)

        return processed_data

    async def create_feedback_forms_batch(
        self,
        modules: List[Any],
        target_count: int = 15
    ) -> Dict[str, Any]:
        """
        Создание batch форм обратной связи

        Args:
            modules: Список модулей программы
            target_count: Целевое количество форм (default: 15)

        Returns:
            Dict с созданными формами обратной связи
        """
        batch_result = {
            "feedback_forms": [],
            "trigger_rules": [],
            "crisis_detection_configs": [],
            "total_created": 0,
            "distribution": {}
        }

        # Создаем формы для разных типов обратной связи
        feedback_types = [
            "end_of_module",
            "end_of_day",
            "mid_program",
            "end_of_program",
            "difficulty_check"
        ]

        for feedback_type in feedback_types:
            batch_result["distribution"][feedback_type] = {
                "forms": target_count // len(feedback_types),
                "questions_per_form": 5
            }

        # Обновляем статистику
        self.stats.feedback_forms_created = target_count

        return batch_result

    async def design_trigger_rules(
        self,
        feedback_forms: List[Any]
    ) -> Dict[str, Any]:
        """
        Проектирование триггерных правил маршрутизации

        Args:
            feedback_forms: Список форм обратной связи

        Returns:
            Dict с триггерными правилами
        """
        trigger_rules = {
            "low_satisfaction": {
                "condition": "satisfaction_score <= 2",
                "action": "send_support_message",
                "params": {
                    "template": "support_low_satisfaction",
                    "delay_hours": 2,
                    "personalization": True
                },
                "priority": 8
            },
            "high_difficulty": {
                "condition": "difficulty_score >= 8",
                "action": "adjust_difficulty",
                "params": {
                    "adjustment": "reduce",
                    "percentage": 20,
                    "notify_user": True
                },
                "priority": 7
            },
            "crisis_detection": {
                "condition": "wellbeing_score <= 3 OR crisis_keywords_detected",
                "action": "escalate_to_professional",
                "params": {
                    "urgency": "high",
                    "notify_team": True,
                    "resources": ["crisis_hotline", "emergency_contacts"],
                    "auto_followup": "24_hours"
                },
                "priority": 10
            },
            "success_celebration": {
                "condition": "satisfaction >= 4 AND consistency_high",
                "action": "celebrate_success",
                "params": {
                    "celebration_type": "personalized",
                    "next_step_hint": True,
                    "badge_unlock": "check_eligibility"
                },
                "priority": 5
            }
        }

        # Обновляем статистику
        self.stats.trigger_rules_designed = len(trigger_rules)

        return {
            "trigger_rules": trigger_rules,
            "total_rules": len(trigger_rules),
            "high_priority_rules": sum(1 for rule in trigger_rules.values() if rule["priority"] >= 8)
        }

    async def create_crisis_detection_system(
        self,
        feedback_forms: List[Any]
    ) -> Dict[str, Any]:
        """
        Создание системы детекции кризисных состояний

        Args:
            feedback_forms: Список форм обратной связи

        Returns:
            Dict с конфигурацией системы детекции кризисов
        """
        crisis_detection = {
            "patterns": {
                "extreme_low_scores": {
                    "condition": "score <= 3 on 3+ questions",
                    "confidence": 0.75,
                    "action": "send_support_message"
                },
                "critical_keywords": {
                    "keywords": [
                        "хочу умереть",
                        "не вижу смысла жить",
                        "покончить с собой",
                        "безнадежно",
                        "не могу больше",
                        "нет выхода"
                    ],
                    "confidence": 0.95,
                    "action": "immediate_escalation"
                },
                "sharp_decline": {
                    "condition": "decrease > 30% over 3-5 days",
                    "confidence": 0.65,
                    "action": "check_in_message"
                },
                "contradictory_responses": {
                    "condition": "inconsistent answers on related questions",
                    "confidence": 0.50,
                    "action": "follow_up_clarification"
                }
            },
            "escalation_protocol": {
                "level_1": "Automated supportive message",
                "level_2": "Team notification + resources",
                "level_3": "Immediate professional escalation"
            },
            "resources": {
                "crisis_hotlines": ["988 (US)", "116 123 (UK)", "8-800-2000-122 (RU)"],
                "emergency_contacts": [],
                "professional_support": []
            }
        }

        # Обновляем статистику
        self.stats.crisis_detection_systems += 1

        return crisis_detection

    async def generate_actionable_insights(
        self,
        feedback_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Генерация действенных инсайтов из данных обратной связи

        Args:
            feedback_data: Данные обратной связи

        Returns:
            Dict с действенными инсайтами
        """
        insights = {
            "specific": [],
            "measurable": [],
            "achievable": [],
            "relevant": [],
            "time_bound": []
        }

        # Примеры структуры инсайтов
        example_insight = {
            "type": "content_improvement",
            "description": "Добавить 2 дополнительных примера в модуль Day 5",
            "metric": "Снизить avg_difficulty с 7.5 до 6.0",
            "timeline": "1 week",
            "priority": "high"
        }

        # Обновляем статистику
        self.stats.actionable_insights_generated += 1

        return {
            "insights": insights,
            "example_structure": example_insight,
            "criteria": "SMART (Specific, Measurable, Achievable, Relevant, Time-bound)"
        }

    async def send_to_phase3_validators(
        self,
        feedback_systems: Dict[str, Any],
        trigger_rules: Dict[str, Any],
        crisis_detection: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Отправка систем обратной связи в валидаторы Phase 3

        Args:
            feedback_systems: Системы обратной связи
            trigger_rules: Триггерные правила
            crisis_detection: Системы детекции кризисов

        Returns:
            Dict с результатом передачи
        """
        output_package = {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "day_completed": self.days,
            "deliverables": {
                "feedback_systems": feedback_systems,
                "trigger_rules": trigger_rules,
                "crisis_detection": crisis_detection,
                "total_forms": self.stats.feedback_forms_created,
                "total_triggers": self.stats.trigger_rules_designed,
                "crisis_systems": self.stats.crisis_detection_systems
            },
            "stats": {
                "feedback_forms_created": self.stats.feedback_forms_created,
                "trigger_rules_designed": self.stats.trigger_rules_designed,
                "crisis_detection_systems": self.stats.crisis_detection_systems,
                "actionable_insights_generated": self.stats.actionable_insights_generated,
                "completion_percentage": self.stats.get_completion_percentage()
            },
            "ready_for_validation": True,
            "next_agents": self.outputs_to,
            "validation_instructions": {
                "safety_protocol": {
                    "focus": "Проверка систем детекции кризисов и протоколов эскалации",
                    "criteria": ["Accuracy > 80%", "False positives < 15%", "Response time < 5 minutes"]
                },
                "scientific_validator": {
                    "focus": "Психометрическая валидация инструментов обратной связи",
                    "criteria": ["Reliability (Cronbach's alpha > 0.7)", "Validity evidence", "Response bias minimization"]
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
                "feedback_forms_created": self.stats.feedback_forms_created,
                "target_feedback_forms": self.stats.target_feedback_forms,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "trigger_rules_designed": self.stats.trigger_rules_designed,
                "crisis_detection_systems": self.stats.crisis_detection_systems,
                "actionable_insights_generated": self.stats.actionable_insights_generated
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.feedback_forms_created < self.stats.target_feedback_forms else "completed"
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

        # Проверка days alignment
        if self.days != "18":
            validation_results["warnings"].append(
                f"Days '{self.days}' не соответствуют архитектуре (ожидается '18')"
            )

        # Проверка систем детекции кризисов
        if self.stats.feedback_forms_created > 0 and self.stats.crisis_detection_systems == 0:
            validation_results["warnings"].append(
                "Формы обратной связи созданы, но система детекции кризисов отсутствует"
            )

        # Проверка триггерных правил
        if self.stats.feedback_forms_created > 0 and self.stats.trigger_rules_designed == 0:
            validation_results["warnings"].append(
                "Формы обратной связи созданы, но триггерные правила не разработаны"
            )

        return validation_results


# Создание глобального экземпляра workflow для использования в агенте
feedback_orchestrator_workflow = PatternFeedbackOrchestratorWorkflow()


def get_workflow() -> PatternFeedbackOrchestratorWorkflow:
    """
    Получить экземпляр workflow конфигурации

    Returns:
        PatternFeedbackOrchestratorWorkflow: Конфигурация workflow агента
    """
    return feedback_orchestrator_workflow


async def update_workflow_stats(
    feedback_forms_created: int = 0,
    trigger_rules_designed: int = 0,
    crisis_detection_systems: int = 0,
    actionable_insights_generated: int = 0
) -> Dict[str, Any]:
    """
    Обновить статистику workflow

    Args:
        feedback_forms_created: Количество созданных форм обратной связи
        trigger_rules_designed: Количество триггерных правил
        crisis_detection_systems: Количество систем детекции кризисов
        actionable_insights_generated: Количество действенных инсайтов

    Returns:
        Dict с обновленной статистикой
    """
    workflow = get_workflow()

    if feedback_forms_created > 0:
        workflow.stats.feedback_forms_created += feedback_forms_created
    if trigger_rules_designed > 0:
        workflow.stats.trigger_rules_designed += trigger_rules_designed
    if crisis_detection_systems > 0:
        workflow.stats.crisis_detection_systems += crisis_detection_systems
    if actionable_insights_generated > 0:
        workflow.stats.actionable_insights_generated += actionable_insights_generated

    return workflow.get_workflow_status()
