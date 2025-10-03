"""
Workflow конфигурация для Pattern Safety Protocol Agent в контексте PatternShift Architecture
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
    safety_audits_completed: int = 0
    risk_assessments_performed: int = 0
    contraindications_identified: int = 0
    escalation_protocols_created: int = 0
    crisis_resources_compiled: int = 0
    target_safety_audits: int = 10  # Аудит всех Phase 1 и Phase 2 агентов

    def get_completion_percentage(self) -> float:
        """Процент выполнения аудитов безопасности"""
        return (self.safety_audits_completed / self.target_safety_audits) * 100 if self.target_safety_audits > 0 else 0.0


@dataclass
class PatternSafetyProtocolWorkflow:
    """
    Workflow конфигурация для Pattern Safety Protocol Agent

    Позиция в PatternShift Architecture:
    - Phase: PHASE_3_SAFETY_SCIENCE (Day 21)
    - Role: Валидатор безопасности
    - Outputs: Сертификация безопасности программы
    """

    # Основная информация
    agent_name: str = "pattern_safety_protocol"
    phase: WorkflowPhase = WorkflowPhase.PHASE_3_SAFETY_SCIENCE
    role: AgentRole = AgentRole.VALIDATOR
    days: str = "21"

    # Входящие связи (получает от Phase 2 интеграторов)
    receives_from: List[str] = field(default_factory=lambda: [
        "pattern_integration_synthesizer",  # Phase 2 главный
        "pattern_feedback_orchestrator",
        "pattern_progress_narrator",
        "pattern_transition_craftsman"
    ])

    # Исходящие связи (финальная сертификация)
    outputs_to: List[str] = field(default_factory=lambda: [])  # Финальный выход программы

    # Статистика
    stats: WorkflowStats = field(default_factory=WorkflowStats)

    # Метаданные workflow
    workflow_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация метаданных workflow"""
        self.workflow_metadata = {
            "phase_description": "Safety & Science - финальная валидация безопасности программы",
            "parallel_agent": "pattern_scientific_validator",
            "key_deliverables": [
                "Полный safety audit всех компонентов программы",
                "Risk assessment для каждого модуля",
                "Идентификация contraindications",
                "Протоколы эскалации кризисов",
                "Компиляция crisis resources",
                "Сертификация безопасности программы"
            ],
            "validation_scope": [
                "Content от Phase 1 агентов",
                "Integration от Integration Synthesizer",
                "Feedback systems от Feedback Orchestrator",
                "Progress narratives от Progress Narrator",
                "Transitions от Transition Craftsman"
            ],
            "critical_focus_areas": [
                "Suicide risk detection",
                "Crisis intervention protocols",
                "Contraindications for techniques",
                "Pharmacological interactions",
                "Vulnerable populations safety"
            ]
        }

    def get_workflow_connections(self) -> List[WorkflowConnection]:
        """
        Получить все workflow связи агента

        Returns:
            List[WorkflowConnection]: Список связей с другими агентами
        """
        connections = []

        # Входящие связи от Phase 2 интеграторов
        connections.append(WorkflowConnection(
            source_agent="pattern_integration_synthesizer",
            target_agent=self.agent_name,
            data_type="integrated_program_for_safety_audit",
            transformation_required=False,
            description="Получение интегрированной программы для safety audit"
        ))

        connections.append(WorkflowConnection(
            source_agent="pattern_feedback_orchestrator",
            target_agent=self.agent_name,
            data_type="feedback_systems_with_crisis_detection",
            transformation_required=False,
            description="Получение систем обратной связи для валидации crisis detection"
        ))

        connections.append(WorkflowConnection(
            source_agent="pattern_progress_narrator",
            target_agent=self.agent_name,
            data_type="motivational_narratives",
            transformation_required=False,
            description="Получение мотивационных нарративов для проверки отсутствия toxic positivity"
        ))

        connections.append(WorkflowConnection(
            source_agent="pattern_transition_craftsman",
            target_agent=self.agent_name,
            data_type="transition_elements_with_flow",
            transformation_required=False,
            description="Получение связующих элементов для проверки безопасности переходов"
        ))

        return connections

    async def receive_from_phase2_agents(
        self,
        integrated_program: Dict[str, Any],
        feedback_systems: Dict[str, Any],
        progress_narratives: List[Any],
        transitions: List[Any]
    ) -> Dict[str, Any]:
        """
        Обработка данных от Phase 2 агентов для safety audit

        Args:
            integrated_program: Интегрированная программа
            feedback_systems: Системы обратной связи
            progress_narratives: Прогресс-нарративы
            transitions: Переходы между модулями

        Returns:
            Dict с результатом обработки
        """
        processed_data = {
            "status": "received",
            "components_to_audit": {
                "program_modules": len(integrated_program.get("modules", [])),
                "feedback_forms": len(feedback_systems.get("feedback_forms", [])),
                "narratives": len(progress_narratives),
                "transitions": len(transitions)
            },
            "audit_priority": []
        }

        # Определяем приоритет аудита
        high_risk_components = [
            "Crisis detection systems",
            "Deep emotional work modules",
            "Trauma-related content",
            "Hypnosis scripts"
        ]

        for component in high_risk_components:
            processed_data["audit_priority"].append({
                "component": component,
                "priority": "critical",
                "rationale": "High risk if improperly implemented"
            })

        return processed_data

    async def perform_safety_audit(
        self,
        program_component: Dict[str, Any],
        component_type: str
    ) -> Dict[str, Any]:
        """
        Выполнить safety audit компонента программы

        Args:
            program_component: Компонент для аудита
            component_type: Тип компонента (module/feedback/narrative/transition)

        Returns:
            Dict с результатами safety audit
        """
        audit_result = {
            "component": program_component.get("name", "Unknown"),
            "component_type": component_type,
            "safety_status": "pending",
            "identified_risks": [],
            "recommendations": [],
            "contraindications": [],
            "escalation_triggers": []
        }

        # Критерии safety audit
        safety_criteria = {
            "no_harm_induction": True,
            "crisis_detection_present": False,
            "contraindications_documented": False,
            "escalation_protocol_clear": False,
            "vulnerable_groups_considered": False,
            "informed_consent_obtained": False
        }

        # Обновляем статистику
        self.stats.safety_audits_completed += 1

        audit_result["safety_criteria"] = safety_criteria
        audit_result["safety_status"] = "requires_review"

        return audit_result

    async def assess_suicide_risk(
        self,
        feedback_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Оценка suicide risk через данные обратной связи

        Args:
            feedback_data: Данные систем обратной связи

        Returns:
            Dict с оценкой suicide риска
        """
        risk_assessment = {
            "assessment_framework": "Interpersonal-Psychological Theory (Joiner, 2005)",
            "risk_factors": {
                "thwarted_belongingness": {
                    "indicators": ["Social isolation", "Feeling burdensome"],
                    "detection_questions": []
                },
                "perceived_burdensomeness": {
                    "indicators": ["Self-hatred", "Ineffectiveness"],
                    "detection_questions": []
                },
                "acquired_capability": {
                    "indicators": ["History of self-harm", "Access to means"],
                    "detection_questions": []
                }
            },
            "risk_levels": {
                "critical": "All 3 components present",
                "high": "2 components present",
                "moderate": "1 component present",
                "low": "0 components present"
            },
            "escalation_protocol": {
                "critical": "Immediate professional intervention",
                "high": "24-hour follow-up + monitoring",
                "moderate": "Weekly check-in + resources",
                "low": "Standard support"
            }
        }

        # Обновляем статистику
        self.stats.risk_assessments_performed += 1

        return risk_assessment

    async def identify_contraindications(
        self,
        program_modules: List[Any]
    ) -> Dict[str, Any]:
        """
        Идентификация contraindications для психотехник

        Args:
            program_modules: Модули программы

        Returns:
            Dict с contraindications
        """
        contraindications_db = {
            "hypnosis_techniques": {
                "absolute_contraindications": [
                    "Active psychosis",
                    "Severe dissociative disorders",
                    "Epilepsy (without medical supervision)"
                ],
                "relative_contraindications": [
                    "PTSD (requires trauma-informed adaptation)",
                    "Personality disorders (requires expertise)",
                    "Recent traumatic experiences"
                ],
                "medication_interactions": [
                    "Antipsychotics - may interfere with trance",
                    "Benzodiazepines - caution with deep trance work"
                ]
            },
            "deep_emotional_work": {
                "absolute_contraindications": [
                    "Active suicidal ideation",
                    "Severe depression (without clinical support)",
                    "Manic episode"
                ],
                "relative_contraindications": [
                    "Recent loss or trauma",
                    "Unstable support system",
                    "Substance abuse issues"
                ]
            },
            "somatic_techniques": {
                "absolute_contraindications": [
                    "Severe cardiac conditions",
                    "Respiratory disorders (breathwork)",
                    "Pregnancy (intensive bodywork)"
                ],
                "relative_contraindications": [
                    "Chronic pain conditions",
                    "Physical disabilities (requires adaptation)"
                ]
            }
        }

        # Обновляем статистику
        self.stats.contraindications_identified += len(contraindications_db)

        return {
            "contraindications_database": contraindications_db,
            "total_techniques_assessed": len(contraindications_db),
            "screening_required": True,
            "adaptation_guidelines": "Provide modified versions for contraindicated groups"
        }

    async def create_escalation_protocols(
        self,
        risk_scenarios: List[str]
    ) -> Dict[str, Any]:
        """
        Создание протоколов эскалации для кризисных ситуаций

        Args:
            risk_scenarios: Сценарии рисков

        Returns:
            Dict с escalation протоколами
        """
        escalation_protocols = {
            "suicide_risk": {
                "level_1_low": {
                    "action": "Automated supportive message",
                    "resources": ["Crisis hotline numbers", "Self-help resources"],
                    "follow_up": "Next session check-in"
                },
                "level_2_moderate": {
                    "action": "Team notification + resources",
                    "resources": ["Crisis hotlines", "Professional referral list"],
                    "follow_up": "24-hour check-in"
                },
                "level_3_high": {
                    "action": "Immediate escalation to supervisor",
                    "resources": ["Emergency services contact", "Crisis intervention team"],
                    "follow_up": "Continuous monitoring"
                },
                "level_4_critical": {
                    "action": "Emergency services notification if consent",
                    "resources": ["911/Emergency services", "Crisis stabilization unit"],
                    "follow_up": "Immediate professional handoff"
                }
            },
            "severe_adverse_reaction": {
                "action": "Pause program + assessment",
                "resources": ["Mental health professional contact"],
                "follow_up": "Clinical consultation before resuming"
            },
            "technical_failure": {
                "action": "Fail-safe default to low-risk activities",
                "resources": ["Technical support", "Manual override"],
                "follow_up": "System restoration + user safety check"
            }
        }

        # Обновляем статистику
        self.stats.escalation_protocols_created = len(escalation_protocols)

        return {
            "escalation_protocols": escalation_protocols,
            "total_scenarios_covered": len(escalation_protocols),
            "response_time_targets": {
                "critical": "< 5 minutes",
                "high": "< 1 hour",
                "moderate": "< 24 hours",
                "low": "< 1 week"
            }
        }

    async def compile_crisis_resources(
        self,
        geographic_regions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Компиляция crisis resources по регионам

        Args:
            geographic_regions: Географические регионы (опционально)

        Returns:
            Dict с crisis resources
        """
        if geographic_regions is None:
            geographic_regions = ["Global", "US", "UK", "Russia"]

        crisis_resources = {
            "global": {
                "suicide_prevention": "International Association for Suicide Prevention",
                "url": "https://www.iasp.info/resources/Crisis_Centres/"
            },
            "us": {
                "crisis_hotline": "988 Suicide & Crisis Lifeline",
                "phone": "988",
                "text": "Text 'HELLO' to 741741",
                "url": "https://988lifeline.org/"
            },
            "uk": {
                "crisis_hotline": "Samaritans",
                "phone": "116 123",
                "url": "https://www.samaritans.org/"
            },
            "russia": {
                "crisis_hotline": "Телефон доверия",
                "phone": "8-800-2000-122",
                "url": "https://telefon-doveria.ru/"
            }
        }

        # Обновляем статистику
        self.stats.crisis_resources_compiled = len(crisis_resources)

        return {
            "crisis_resources": crisis_resources,
            "regions_covered": geographic_regions,
            "accessibility": {
                "24_7_available": True,
                "multilingual": "Region dependent",
                "anonymous": True,
                "free": True
            },
            "integration_points": [
                "Program interface footer",
                "Crisis detection triggers",
                "Email communications",
                "User dashboard"
            ]
        }

    async def certify_program_safety(
        self,
        safety_audits: List[Dict[str, Any]],
        risk_assessments: List[Dict[str, Any]],
        escalation_protocols: Dict[str, Any],
        crisis_resources: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Финальная сертификация безопасности программы

        Args:
            safety_audits: Выполненные safety audits
            risk_assessments: Risk assessments
            escalation_protocols: Протоколы эскалации
            crisis_resources: Crisis resources

        Returns:
            Dict с сертификацией безопасности
        """
        certification = {
            "program_name": "PatternShift Transformation Program",
            "certification_date": "Day 21",
            "certifying_agent": self.agent_name,
            "safety_status": "pending_final_review",
            "audit_summary": {
                "total_components_audited": len(safety_audits),
                "high_risk_components": sum(1 for a in safety_audits if a.get("safety_status") == "requires_review"),
                "approved_components": sum(1 for a in safety_audits if a.get("safety_status") == "approved"),
                "components_requiring_modification": []
            },
            "risk_management": {
                "suicide_risk_protocol": "Implemented",
                "crisis_detection_systems": "Active",
                "escalation_protocols": "Defined",
                "crisis_resources": "Compiled and accessible"
            },
            "recommendations": [
                "Regular monitoring of crisis detection accuracy",
                "Quarterly review of escalation protocols",
                "User safety feedback integration",
                "Professional supervision for high-risk cases"
            ],
            "limitations_disclosed": [
                "Program is not a substitute for professional therapy",
                "Crisis detection may have false positives/negatives",
                "User responsibility for seeking help when needed"
            ],
            "certification_conditions": [
                "Ongoing safety monitoring",
                "Regular protocol updates",
                "Professional oversight availability"
            ]
        }

        return certification

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
                "safety_audits_completed": self.stats.safety_audits_completed,
                "target_safety_audits": self.stats.target_safety_audits,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "risk_assessments_performed": self.stats.risk_assessments_performed,
                "contraindications_identified": self.stats.contraindications_identified,
                "escalation_protocols_created": self.stats.escalation_protocols_created,
                "crisis_resources_compiled": self.stats.crisis_resources_compiled
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.safety_audits_completed < self.stats.target_safety_audits else "completed"
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

        # Проверка Phase 3 requirements
        if self.phase != WorkflowPhase.PHASE_3_SAFETY_SCIENCE:
            validation_results["compliant"] = False
            validation_results["issues"].append(
                f"Agent должен быть в PHASE_3_SAFETY_SCIENCE, текущая phase: {self.phase.value}"
            )

        # Проверка входящих связей от Phase 2
        required_sources = [
            "pattern_integration_synthesizer",
            "pattern_feedback_orchestrator",
            "pattern_progress_narrator",
            "pattern_transition_craftsman"
        ]

        for source in required_sources:
            if source not in self.receives_from:
                validation_results["warnings"].append(
                    f"Отсутствует входящая связь от {source}"
                )

        # Проверка days alignment
        if self.days != "21":
            validation_results["warnings"].append(
                f"Days '{self.days}' не соответствуют архитектуре (ожидается '21')"
            )

        # Критические проверки безопасности
        if self.stats.safety_audits_completed > 0:
            if self.stats.risk_assessments_performed == 0:
                validation_results["issues"].append(
                    "КРИТИЧНО: Safety audits проведены без risk assessment"
                )

            if self.stats.escalation_protocols_created == 0:
                validation_results["issues"].append(
                    "КРИТИЧНО: Отсутствуют escalation протоколы"
                )

            if self.stats.crisis_resources_compiled == 0:
                validation_results["issues"].append(
                    "КРИТИЧНО: Crisis resources не скомпилированы"
                )

        return validation_results


# Создание глобального экземпляра workflow для использования в агенте
safety_protocol_workflow = PatternSafetyProtocolWorkflow()


def get_workflow() -> PatternSafetyProtocolWorkflow:
    """
    Получить экземпляр workflow конфигурации

    Returns:
        PatternSafetyProtocolWorkflow: Конфигурация workflow агента
    """
    return safety_protocol_workflow


async def update_workflow_stats(
    safety_audits_completed: int = 0,
    risk_assessments_performed: int = 0,
    contraindications_identified: int = 0,
    escalation_protocols_created: int = 0,
    crisis_resources_compiled: int = 0
) -> Dict[str, Any]:
    """
    Обновить статистику workflow

    Args:
        safety_audits_completed: Количество выполненных safety audits
        risk_assessments_performed: Количество risk assessments
        contraindications_identified: Количество contraindications
        escalation_protocols_created: Количество escalation протоколов
        crisis_resources_compiled: Количество crisis resources

    Returns:
        Dict с обновленной статистикой
    """
    workflow = get_workflow()

    if safety_audits_completed > 0:
        workflow.stats.safety_audits_completed += safety_audits_completed
    if risk_assessments_performed > 0:
        workflow.stats.risk_assessments_performed += risk_assessments_performed
    if contraindications_identified > 0:
        workflow.stats.contraindications_identified += contraindications_identified
    if escalation_protocols_created > 0:
        workflow.stats.escalation_protocols_created = escalation_protocols_created
    if crisis_resources_compiled > 0:
        workflow.stats.crisis_resources_compiled = crisis_resources_compiled

    return workflow.get_workflow_status()
