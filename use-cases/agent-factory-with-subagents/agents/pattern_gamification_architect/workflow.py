"""
Workflow конфигурация для Pattern Gamification Architect Agent в контексте PatternShift Architecture
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
    game_mechanics_created: int = 0
    achievement_systems_created: int = 0
    progression_tracks_created: int = 0
    reward_loops_designed: int = 0
    target_game_mechanics: int = 20  # Целевое количество из архитектуры

    def get_completion_percentage(self) -> float:
        """Процент выполнения целевого количества игровых механик"""
        return (self.game_mechanics_created / self.target_game_mechanics) * 100 if self.target_game_mechanics > 0 else 0.0


@dataclass
class PatternGamificationArchitectWorkflow:
    """
    Workflow конфигурация для Pattern Gamification Architect Agent

    Позиция в PatternShift Architecture:
    - Phase: PHASE_1_CONTENT_CREATION (Day 14)
    - Role: Архитектор геймификации
    - Outputs: Игровые механики для вовлечения
    """

    # Основная информация
    agent_name: str = "pattern_gamification_architect"
    phase: WorkflowPhase = WorkflowPhase.PHASE_1_CONTENT_CREATION
    role: AgentRole = AgentRole.CONTENT_CREATOR
    days: str = "14"

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
            "phase_description": "Content Creation - создание игровых механик для вовлечения",
            "parallel_agents": [
                "pattern_nlp_technique_master",
                "pattern_exercise_architect",
                "pattern_ericksonian_hypnosis_scriptwriter",
                "pattern_microhabit_designer",
                "pattern_metaphor_weaver"
            ],
            "key_deliverables": [
                "Игровые механики для повышения вовлеченности",
                "Системы достижений и прогресса",
                "Треки прогрессии пользователя",
                "Reward loops (петли вознаграждений)"
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
            data_type="gamification_modules",
            transformation_required=False,
            description="Передача игровых механик для интеграции в программу"
        ))

        return connections

    async def receive_from_parallel_agents(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка входных данных от параллельных агентов Phase 1

        Note: Gamification Architect может обогатить игровую механику данными других агентов

        Args:
            agent_data: Данные от других агентов (опционально)

        Returns:
            Dict с результатом обработки
        """
        processed_data = {
            "status": "received",
            "enhancements": []
        }

        # Если есть микропривычки - можем создать систему достижений вокруг них
        if "microhabits" in agent_data:
            processed_data["enhancements"].append({
                "type": "achievement_system_for_habits",
                "source": "pattern_microhabit_designer",
                "description": "Создание систем достижений для микропривычек"
            })

        # Если есть упражнения - можем добавить прогрессивные уровни сложности
        if "exercises" in agent_data:
            processed_data["enhancements"].append({
                "type": "progressive_difficulty_tracks",
                "source": "pattern_exercise_architect",
                "description": "Прогрессивные треки сложности упражнений"
            })

        return processed_data

    async def create_game_mechanics_batch(
        self,
        program_modules: List[str],
        target_count: int = 20
    ) -> Dict[str, Any]:
        """
        Создание batch игровых механик

        Args:
            program_modules: Список модулей программы
            target_count: Целевое количество механик (default: 20)

        Returns:
            Dict с созданными игровыми механиками
        """
        # Планируем распределение механик по модулям
        mechanics_per_module = target_count // len(program_modules) if program_modules else target_count

        batch_result = {
            "game_mechanics": [],
            "achievement_systems": [],
            "progression_tracks": [],
            "total_created": 0,
            "distribution": {}
        }

        for module in program_modules:
            batch_result["distribution"][module] = mechanics_per_module

        # Обновляем статистику
        self.stats.game_mechanics_created = target_count

        return batch_result

    async def design_achievement_system(
        self,
        program_goals: List[str]
    ) -> Dict[str, Any]:
        """
        Проектирование системы достижений

        Args:
            program_goals: Цели программы трансформации

        Returns:
            Dict с системой достижений
        """
        achievement_system = {
            "tiers": [
                {"name": "Bronze", "requirements": "Базовое участие"},
                {"name": "Silver", "requirements": "Регулярное выполнение"},
                {"name": "Gold", "requirements": "Экспертное мастерство"}
            ],
            "badges": [],
            "milestones": [],
            "leaderboards": False  # Avoid competitive pressure
        }

        # Обновляем статистику
        self.stats.achievement_systems_created += 1

        return achievement_system

    async def create_progression_tracks(
        self,
        skill_areas: List[str],
        difficulty_levels: int = 5
    ) -> Dict[str, Any]:
        """
        Создание треков прогрессии по навыкам

        Args:
            skill_areas: Области навыков
            difficulty_levels: Количество уровней сложности

        Returns:
            Dict с треками прогрессии
        """
        progression_tracks = {
            "tracks": [],
            "total_levels": difficulty_levels,
            "unlock_system": "progressive",
            "mastery_criteria": {}
        }

        for skill in skill_areas:
            progression_tracks["tracks"].append({
                "skill": skill,
                "levels": difficulty_levels,
                "current_level": 1
            })

        # Обновляем статистику
        self.stats.progression_tracks_created += len(skill_areas)

        return progression_tracks

    async def design_reward_loops(
        self,
        user_motivations: List[str]
    ) -> Dict[str, Any]:
        """
        Проектирование петель вознаграждений

        Args:
            user_motivations: Мотивации пользователей

        Returns:
            Dict с reward loops
        """
        reward_loops = {
            "immediate_rewards": [],
            "delayed_rewards": [],
            "variable_rewards": [],  # Для повышения dopamine
            "intrinsic_rewards": []
        }

        # Обновляем статистику
        self.stats.reward_loops_designed += len(user_motivations)

        return reward_loops

    async def send_to_integration_synthesizer(
        self,
        game_mechanics: List[Any],
        achievement_systems: List[Any],
        progression_tracks: List[Any]
    ) -> Dict[str, Any]:
        """
        Отправка игровых механик в Integration Synthesizer

        Args:
            game_mechanics: Список игровых механик
            achievement_systems: Системы достижений
            progression_tracks: Треки прогрессии

        Returns:
            Dict с результатом передачи
        """
        output_package = {
            "agent": self.agent_name,
            "phase": self.phase.value,
            "day_completed": self.days,
            "deliverables": {
                "game_mechanics": game_mechanics,
                "achievement_systems": achievement_systems,
                "progression_tracks": progression_tracks,
                "total_mechanics": len(game_mechanics),
                "total_achievements": len(achievement_systems),
                "total_tracks": len(progression_tracks)
            },
            "stats": {
                "game_mechanics_created": self.stats.game_mechanics_created,
                "achievement_systems_created": self.stats.achievement_systems_created,
                "progression_tracks_created": self.stats.progression_tracks_created,
                "reward_loops_designed": self.stats.reward_loops_designed,
                "completion_percentage": self.stats.get_completion_percentage()
            },
            "ready_for_integration": True,
            "next_agent": "pattern_integration_synthesizer",
            "integration_instructions": {
                "merge_strategy": "layer_onto_modules",
                "module_type": "gamification_layer",
                "placement": "throughout_program",
                "activation": "progressive_unlock"
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
                "game_mechanics_created": self.stats.game_mechanics_created,
                "target_game_mechanics": self.stats.target_game_mechanics,
                "completion_percentage": f"{self.stats.get_completion_percentage():.1f}%",
                "achievement_systems_created": self.stats.achievement_systems_created,
                "progression_tracks_created": self.stats.progression_tracks_created,
                "reward_loops_designed": self.stats.reward_loops_designed
            },
            "workflow_metadata": self.workflow_metadata,
            "connections": [conn.__dict__ for conn in self.get_workflow_connections()],
            "status": "active" if self.stats.game_mechanics_created < self.stats.target_game_mechanics else "completed"
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

        # Проверка days alignment
        if self.days != "14":
            validation_results["warnings"].append(
                f"Days '{self.days}' не соответствуют архитектуре (ожидается '14')"
            )

        # Проверка баланса вовлеченности
        if self.stats.reward_loops_designed > 0 and self.stats.achievement_systems_created == 0:
            validation_results["warnings"].append(
                "Reward loops созданы, но нет системы достижений для их поддержки"
            )

        return validation_results


# Создание глобального экземпляра workflow для использования в агенте
gamification_architect_workflow = PatternGamificationArchitectWorkflow()


def get_workflow() -> PatternGamificationArchitectWorkflow:
    """
    Получить экземпляр workflow конфигурации

    Returns:
        PatternGamificationArchitectWorkflow: Конфигурация workflow агента
    """
    return gamification_architect_workflow


async def update_workflow_stats(
    game_mechanics_created: int = 0,
    achievement_systems_created: int = 0,
    progression_tracks_created: int = 0,
    reward_loops_designed: int = 0
) -> Dict[str, Any]:
    """
    Обновить статистику workflow

    Args:
        game_mechanics_created: Количество игровых механик
        achievement_systems_created: Количество систем достижений
        progression_tracks_created: Количество треков прогрессии
        reward_loops_designed: Количество reward loops

    Returns:
        Dict с обновленной статистикой
    """
    workflow = get_workflow()

    if game_mechanics_created > 0:
        workflow.stats.game_mechanics_created += game_mechanics_created
    if achievement_systems_created > 0:
        workflow.stats.achievement_systems_created += achievement_systems_created
    if progression_tracks_created > 0:
        workflow.stats.progression_tracks_created += progression_tracks_created
    if reward_loops_designed > 0:
        workflow.stats.reward_loops_designed += reward_loops_designed

    return workflow.get_workflow_status()
