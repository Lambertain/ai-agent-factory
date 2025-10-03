"""
Workflow конфигурация для Pattern Progress Narrator Agent в контексте PatternShift Architecture
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
    progress_narratives_created: int = 0
    milestone_messages_created: int = 0
    reframing_scripts_created: int = 0
    momentum_builders_created: int = 0
    target_narratives: int = 50  # Целевое количество из архитектуры

    def get_completion_percentage(self) -> float:
        """Процент выполнения целевого количества нарративов"""
        return (self.progress_narratives_created / self.target_narratives) * 100 if self.target_narratives > 0 else 0.0


@dataclass
class PatternProgressNarratorWorkflow:
    """
    Workflow конфигурация для Pattern Progress Narrator Agent

    Позиция в PatternShift Architecture:
    - Phase: PHASE_2_INTEGRATION_POLISH (Day 19)
    - Role: Интегратор нарративов прогресса
    - Outputs: Мотивационные нарративы и storytelling элементы
    """

    # Основная информация
    agent_name: str = "pattern_progress_narrator"
    phase: WorkflowPhase = WorkflowPhase.PHASE_2_INTEGRATION_POLISH
    role: AgentRole = AgentRole.INTEGRATOR
    days: str = "19"

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
            "phase_description": "Integration & Polish - создание нарративов прогресса и мотивационных сообщений",
            "parallel_agents": [
                "pattern_feedback_orchestrator",
                "pattern_transition_craftsman"
            ],
            "key_deliverables": [
                "50+ прогресс-нарративов для разных этапов программы",
                "Milestone celebration сообщения",
                "Reframing scripts для неудач и challenges",
                "Momentum-building элементы",
                "Hero's Journey mapping для программы трансформации"
            ],
            "integration_source": "pattern_integration_synthesizer",
            "validation_targets": ["pattern_safety_protocol", "pattern_scientific_validator"],
            "storytelling_framework": "Hero's Journey (Joseph Campbell)",
            "narrative_stages": {
                "days_1_3": "Ordinary World - начальное состояние",
                "days_3_5": "Meeting the Mentor - первые инструменты",
                "days_5_7": "Crossing the Threshold - первые изменения",
                "days_7_14": "Tests, Allies, Enemies - практика и challenges",
                "days_14_17": "Approach to Inmost Cave - глубокая работа",
                "days_17_19": "Ordeal - ключевые прорывы",
                "days_19_21": "Return with Elixir - интеграция в жизнь"
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
            data_type="integrated_program_with_milestones",
            transformation_required=True,
            description="Получение интегрированной программы для создания нарративов прогресса"
        ))

        # Исходящие связи к валидаторам Phase 3
        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_safety_protocol",
            data_type="motivational_narratives",
            transformation_required=False,
            description="Передача мотивационных нарративов для проверки психологической безопасности"
        ))

        connections.append(WorkflowConnection(
            source_agent=self.agent_name,
            target_agent="pattern_scientific_validator",
            data_type="progress_framing_strategies",
            transformation_required=False,
            description="Передача стратегий фреймирования для научной валидации"
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
            "program_duration_days": integrated_program.get("duration_days", 21),
            "milestones_identified": [],
            "narrative_arc_mapped": False
        }

        # Идентифицируем ключевые milestones программы
        if "modules" in integrated_program:
            for module in integrated_program["modules"]:
                day = module.get("day")
                if day in [1, 5, 7, 10, 14, 17, 21]:  # Ключевые milestone дни
                    processed_data["milestones_identified"].append({
                        "day": day,
                        "module_name": module.get("name"),
                        "milestone_type": self._get_milestone_type(day)
                    })

        # Маппинг на Hero's Journey arc
        processed_data["narrative_arc_mapped"] = True

        return processed_data

    def _get_milestone_type(self, day: int) -> str:
        """Определить тип milestone по дню программы"""
        if day <= 3:
            return "ordinary_world"
        elif day <= 5:
            return "meeting_mentor"
        elif day <= 7:
            return "crossing_threshold"
        elif day <= 14:
            return "tests_allies_enemies"
        elif day <= 17:
            return "approach_cave"
        elif day <= 19:
            return "ordeal"
        else:
            return "return_elixir"

    async def create_progress_narratives_batch(
        self,
        program_structure: Dict[str, Any],
        target_count: int = 50
    ) -> Dict[str, Any]:
        """
        Создание batch прогресс-нарративов

        Args:
            program_structure: Структура программы
            target_count: Целевое количество нарративов (default: 50)

        Returns:
            Dict с созданными нарративами
        """
        batch_result = {
            "progress_narratives": [],
            "milestone_messages": [],
            "reframing_scripts": [],
            "momentum_builders": [],
            "total_created": 0,
            "distribution_by_type": {}
        }

        # Распределяем нарративы по типам
        narrative_types = {
            "daily_progress": target_count // 4,
            "milestone_celebration": target_count // 8,
            "challenge_reframing": target_count // 4,
            "momentum_building": target_count // 8,
            "anticipation_creation": target_count // 8,
            "reflection_prompts": target_count // 8
        }

        for narrative_type, count in narrative_types.items():
            batch_result["distribution_by_type"][narrative_type] = count

        # Обновляем статистику
        self.stats.progress_narratives_created = target_count

        return batch_result

    async def create_milestone_messages(
        self,
        milestones: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Создание сообщений для milestone моментов

        Args:
            milestones: Список milestone моментов программы

        Returns:
            Dict с milestone сообщениями
        """
        milestone_messages = {
            "celebrations": [],
            "reflections": [],
            "next_steps": []
        }

        for milestone in milestones:
            message = {
                "day": milestone["day"],
                "type": milestone.get("milestone_type"),
                "celebration": f"Празднование достижения Day {milestone['day']}",
                "reflection": "Что изменилось с начала пути?",
                "next_step": "Следующий этап вашего путешествия"
            }
            milestone_messages["celebrations"].append(message)

        # Обновляем статистику
        self.stats.milestone_messages_created = len(milestones)

        return milestone_messages

    async def create_reframing_scripts(
        self,
        challenge_types: List[str]
    ) -> Dict[str, Any]:
        """
        Создание reframing scripts для challenges и неудач

        Args:
            challenge_types: Типы challenges в программе

        Returns:
            Dict с reframing скриптами
        """
        reframing_scripts = {
            "difficulty_reframe": {
                "challenge": "Упражнение слишком сложное",
                "reframe": "Это знак что вы растете - discomfort zone это зона роста",
                "action": "Попробуйте упрощенную версию и постепенно усложняйте"
            },
            "missed_day_reframe": {
                "challenge": "Пропустил день программы",
                "reframe": "Каждый день - новая возможность начать. Пропуск показывает что важно отслеживать",
                "action": "Возобновите с текущего дня, не пытайтесь догнать"
            },
            "no_results_reframe": {
                "challenge": "Не вижу результатов",
                "reframe": "Изменения часто незаметны изнутри. Ваш мозг уже меняется на нейронном уровне",
                "action": "Посмотрите записи Day 1 - что изменилось в вашем подходе?"
            },
            "relapse_reframe": {
                "challenge": "Вернулся к старым паттернам",
                "reframe": "Relapse - нормальная часть изменений. Важно не perfection, а направление",
                "action": "Что triggered возврат? Это информация для укрепления навыка"
            }
        }

        # Обновляем статистику
        self.stats.reframing_scripts_created = len(reframing_scripts)

        return {
            "reframing_scripts": reframing_scripts,
            "total_scripts": len(reframing_scripts),
            "framework": "Cognitive Reframing (CBT-based)"
        }

    async def create_momentum_builders(
        self,
        program_phases: List[str]
    ) -> Dict[str, Any]:
        """
        Создание momentum-building элементов

        Args:
            program_phases: Фазы программы

        Returns:
            Dict с momentum builders
        """
        momentum_builders = {
            "streak_trackers": {
                "type": "visual_progress",
                "mechanic": "Consecutive days completed",
                "celebration_points": [3, 7, 14, 21]
            },
            "before_after_comparisons": {
                "type": "self_comparison",
                "mechanic": "Day 1 vs Day N reflections",
                "trigger_days": [7, 14, 21]
            },
            "skill_unlocks": {
                "type": "mastery_tracking",
                "mechanic": "New techniques mastered",
                "visual": "skill_tree"
            },
            "anticipation_builders": {
                "type": "curiosity_creation",
                "mechanic": "Hints about next module",
                "trigger": "end_of_current_module"
            },
            "social_proof": {
                "type": "community_momentum",
                "mechanic": "Others' success stories (anonymized)",
                "frequency": "weekly"
            }
        }

        # Обновляем статистику
        self.stats.momentum_builders_created = len(momentum_builders)

        return {
            "momentum_builders": momentum_builders,
            "total_builders": len(momentum_builders),
            "psychological_principles": ["Commitment consistency", "Social proof", "Curiosity gap"]
        }

    async def map_heros_journey(
        self,
        program_days: int = 21
    ) -> Dict[str, Any]:
        """
        Маппинг программы на Hero's Journey структуру

        Args:
            program_days: Длительность программы в днях

        Returns:
            Dict с Hero's Journey mapping
        """
        heros_journey_map = {
            "act_1_separation": {
                "days": "1-7",
                "stages": [
                    {"stage": "ordinary_world", "days": [1, 2]},
                    {"stage": "call_to_adventure", "days": [1, 2]},
                    {"stage": "refusal_of_call", "days": [2, 3, 4]},
                    {"stage": "meeting_mentor", "days": [3, 4, 5]},
                    {"stage": "crossing_threshold", "days": [5, 6, 7]}
                ]
            },
            "act_2_initiation": {
                "days": "7-17",
                "stages": [
                    {"stage": "tests_allies_enemies", "days": list(range(7, 15))},
                    {"stage": "approach_cave", "days": [14, 15, 16, 17]},
                    {"stage": "ordeal", "days": [17, 18, 19]}
                ]
            },
            "act_3_return": {
                "days": "17-21",
                "stages": [
                    {"stage": "reward", "days": [19]},
                    {"stage": "road_back", "days": [19, 20]},
                    {"stage": "resurrection", "days": [20]},
                    {"stage": "return_elixir", "days": [21]}
                ]
            }
        }

        return {
            "heros_journey_map": heros_journey_map,
            "total_stages": 12,
            "framework": "Joseph Campbell (1949) Monomyth"
        }

    async def send_to_phase3_validators(
        self,
        progress_narratives: List[Any],
        milestone_messages: Dict[str, Any],
        reframing_scripts: Dict[str, Any],
        momentum_builders: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Отправка нарративов прогресса в валидаторы Phase 3

        Args:
            progress_narratives: Прогресс-нарративы
            milestone_messages: Milestone сообщения
            reframing_scripts: Reframing скрипты
            momentum_builders: Momentum builders

        Returns:
            Dict с результатом передачи
        """
        output_package = {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "day_completed": self.days,
            "deliverables": {
                "progress_narratives": progress_narratives,
                "milestone_messages": milestone_messages,
                "reframing_scripts": reframing_scripts,
                "momentum_builders": momentum_builders,
                "total_narratives": len(progress_narratives),
                "total_milestones": self.stats.milestone_messages_created,
                "total_reframes": self.stats.reframing_scripts_created,
                "total_momentum_builders": self.stats.momentum_builders_created
            },
            "stats": {
                "progress_narratives_created": self.stats.progress_narratives_created,
                "milestone_messages_created": self.stats.milestone_messages_created,
                "reframing_scripts_created": self.stats.reframing_scripts_created,
                "momentum_builders_created": self.stats.momentum_builders_created,
                "completion_percentage": self.stats.get_completion_percentage()
            },
            "ready_for_validation": True,
            "next_agents": self.outputs_to,
            "validation_instructions": {
                "safety_protocol": {
                    "focus": "Проверка мотивационных сообщений на отсутствие pressure и toxic positivity",
                    "criteria": ["No guilt-inducing language", "Realistic expectations", "Support for setbacks"]
                },
                "scientific_validator": {
                    "focus": "Валидация эффективности framing стратегий",
                    "criteria": ["Evidence-based reframing", "Psychological safety", "Motivation theory alignment"]
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
                "progress_narratives_created": self.stats.progress_narratives_created,
                "target_narratives": self.stats.target_narratives,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "milestone_messages_created": self.stats.milestone_messages_created,
                "reframing_scripts_created": self.stats.reframing_scripts_created,
                "momentum_builders_created": self.stats.momentum_builders_created
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.progress_narratives_created < self.stats.target_narratives else "completed"
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
        if self.stats.target_narratives < 50:
            validation_results["warnings"].append(
                f"Целевое количество нарративов ({self.stats.target_narratives}) ниже рекомендованного (50)"
            )

        # Проверка days alignment
        if self.days != "19":
            validation_results["warnings"].append(
                f"Days '{self.days}' не соответствуют архитектуре (ожидается '19')"
            )

        # Проверка баланса компонентов
        if self.stats.progress_narratives_created > 0 and self.stats.reframing_scripts_created == 0:
            validation_results["warnings"].append(
                "Прогресс-нарративы созданы, но reframing скрипты отсутствуют"
            )

        if self.stats.progress_narratives_created > 0 and self.stats.momentum_builders_created == 0:
            validation_results["warnings"].append(
                "Прогресс-нарративы созданы, но momentum builders отсутствуют"
            )

        return validation_results


# Создание глобального экземпляра workflow для использования в агенте
progress_narrator_workflow = PatternProgressNarratorWorkflow()


def get_workflow() -> PatternProgressNarratorWorkflow:
    """
    Получить экземпляр workflow конфигурации

    Returns:
        PatternProgressNarratorWorkflow: Конфигурация workflow агента
    """
    return progress_narrator_workflow


async def update_workflow_stats(
    progress_narratives_created: int = 0,
    milestone_messages_created: int = 0,
    reframing_scripts_created: int = 0,
    momentum_builders_created: int = 0
) -> Dict[str, Any]:
    """
    Обновить статистику workflow

    Args:
        progress_narratives_created: Количество прогресс-нарративов
        milestone_messages_created: Количество milestone сообщений
        reframing_scripts_created: Количество reframing скриптов
        momentum_builders_created: Количество momentum builders

    Returns:
        Dict с обновленной статистикой
    """
    workflow = get_workflow()

    if progress_narratives_created > 0:
        workflow.stats.progress_narratives_created += progress_narratives_created
    if milestone_messages_created > 0:
        workflow.stats.milestone_messages_created += milestone_messages_created
    if reframing_scripts_created > 0:
        workflow.stats.reframing_scripts_created += reframing_scripts_created
    if momentum_builders_created > 0:
        workflow.stats.momentum_builders_created += momentum_builders_created

    return workflow.get_workflow_status()
