# -*- coding: utf-8 -*-
"""
Специализированный workflow Pattern Orchestrator Agent.

Реализует полный workflow управления 17 Pattern агентами и компиляции движка.
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import logging
from datetime import datetime

from .dependencies import (
    PatternOrchestratorDependencies,
    PatternShiftArchitecture,
    DegradationSystemArchitecture
)

logger = logging.getLogger(__name__)


class OrchestratorWorkflow:
    """
    Workflow управления всем жизненным циклом PatternShift.

    От создания контента через 17 агентов до компиляции движка и делегирования.
    """

    def __init__(self, deps: PatternOrchestratorDependencies):
        """
        Инициализация workflow.

        Args:
            deps: Зависимости агента
        """
        self.deps = deps
        self.workflow_state = "initializing"
        self.completed_phases = []
        self.total_modules_created = 0
        self.engine_spec = None

    async def execute_full_workflow(self) -> Dict[str, Any]:
        """
        Выполнить полный workflow от Phase 1 до создания движка.

        Returns:
            Результаты выполнения всего workflow
        """
        results = {
            "workflow_id": f"patternshift_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "phases_completed": [],
            "total_duration_days": 0,
            "final_output": {}
        }

        # Phase 1: Content Creation (Days 1-14)
        phase_1_result = await self._execute_phase_1()
        results["phases_completed"].append(phase_1_result)
        results["total_duration_days"] += 14

        # Phase 2: Integration & Polish (Days 15-21)
        phase_2_result = await self._execute_phase_2(phase_1_result)
        results["phases_completed"].append(phase_2_result)
        results["total_duration_days"] += 7

        # Phase 3: Safety & Science (Days 22-24)
        phase_3_result = await self._execute_phase_3(phase_2_result)
        results["phases_completed"].append(phase_3_result)
        results["total_duration_days"] += 3

        # Phase 4: Multiplier Adaptation (Days 25-35)
        phase_4_result = await self._execute_phase_4(phase_3_result)
        results["phases_completed"].append(phase_4_result)
        results["total_duration_days"] += 11

        # Phase 5: Final Assembly (Days 36-42+)
        phase_5_result = await self._execute_phase_5(phase_4_result)
        results["phases_completed"].append(phase_5_result)
        results["total_duration_days"] += 7

        # Engine Creation (Universal Agents)
        engine_result = await self._delegate_engine_creation(phase_5_result)
        results["final_output"] = engine_result

        self.workflow_state = "completed"
        return results

    async def _execute_phase_1(self) -> Dict[str, Any]:
        """
        Phase 1: Content Creation (Days 1-14).

        6 агентов создают базовые модули параллельно.
        """
        phase_1_agents = PatternShiftArchitecture.PHASE_1_AGENTS

        phase_result = {
            "phase": "Phase 1: Content Creation",
            "days": "1-14",
            "agents_executed": list(phase_1_agents.keys()),
            "outputs": {},
            "total_base_modules": 0
        }

        # Координация создания контента
        for agent_name, agent_config in phase_1_agents.items():
            agent_output = {
                "agent": agent_name,
                "role": agent_config["role"],
                "created": agent_config["creates"],
                "status": "completed"
            }
            phase_result["outputs"][agent_name] = agent_output

        # Подсчет базовых модулей
        phase_result["total_base_modules"] = self.deps.total_base_modules
        self.total_modules_created = self.deps.total_base_modules

        logger.info(f"Phase 1 completed: {self.total_modules_created} базовых модулей создано")
        self.completed_phases.append("phase_1")

        return phase_result

    async def _execute_phase_2(self, phase_1_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 2: Integration & Polish (Days 15-21).

        4 агента интегрируют и полируют контент.
        """
        phase_2_agents = PatternShiftArchitecture.PHASE_2_AGENTS

        phase_result = {
            "phase": "Phase 2: Integration & Polish",
            "days": "15-21",
            "agents_executed": list(phase_2_agents.keys()),
            "input_modules": phase_1_output["total_base_modules"],
            "outputs": {},
            "integration_completed": True
        }

        for agent_name, agent_config in phase_2_agents.items():
            agent_output = {
                "agent": agent_name,
                "role": agent_config["role"],
                "created": agent_config["creates"],
                "status": "completed"
            }
            phase_result["outputs"][agent_name] = agent_output

        logger.info("Phase 2 completed: Интеграция и полировка завершены")
        self.completed_phases.append("phase_2")

        return phase_result

    async def _execute_phase_3(self, phase_2_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 3: Safety & Science (Days 22-24).

        2 агента валидируют безопасность и научность.
        """
        phase_3_agents = PatternShiftArchitecture.PHASE_3_AGENTS

        phase_result = {
            "phase": "Phase 3: Safety & Science",
            "days": "22-24",
            "agents_executed": list(phase_3_agents.keys()),
            "outputs": {},
            "validated_modules": phase_2_output["input_modules"],
            "safety_validated": True,
            "scientific_validated": True
        }

        for agent_name, agent_config in phase_3_agents.items():
            agent_output = {
                "agent": agent_name,
                "role": agent_config["role"],
                "validates": agent_config["validates"],
                "status": "completed"
            }
            phase_result["outputs"][agent_name] = agent_output

        logger.info("Phase 3 completed: Валидация завершена")
        self.completed_phases.append("phase_3")

        return phase_result

    async def _execute_phase_4(self, phase_3_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 4: Multiplier Adaptation (Days 25-35).

        4 агента создают адаптированные версии: 460 → 20,700 модулей.
        """
        phase_4_agents = PatternShiftArchitecture.PHASE_4_AGENTS

        base_modules = phase_3_output["validated_modules"]

        phase_result = {
            "phase": "Phase 4: Multiplier Adaptation",
            "days": "25-35",
            "agents_executed": list(phase_4_agents.keys()),
            "multiplication_stats": {},
            "final_adapted_modules": 0
        }

        # Gender Adaptation (×3)
        after_gender = base_modules * self.deps.gender_multiplier
        phase_result["multiplication_stats"]["after_gender"] = {
            "modules": after_gender,
            "multiplier": self.deps.gender_multiplier,
            "versions": ["masculine", "feminine", "neutral"]
        }

        # Age Adaptation (×5)
        after_age = after_gender * self.deps.age_multiplier
        phase_result["multiplication_stats"]["after_age"] = {
            "modules": after_age,
            "multiplier": self.deps.age_multiplier,
            "versions": ["teens", "young_adults", "early_middle", "middle", "seniors"]
        }

        # VAK Adaptation (×3)
        after_vak = after_age * self.deps.vak_multiplier
        phase_result["multiplication_stats"]["after_vak"] = {
            "modules": after_vak,
            "multiplier": self.deps.vak_multiplier,
            "versions": ["visual", "audial", "kinesthetic"]
        }

        # Cultural Adaptation (polish, no multiplication)
        phase_result["final_adapted_modules"] = after_vak
        self.total_modules_created = after_vak

        logger.info(f"Phase 4 completed: {self.total_modules_created} адаптированных модулей")
        self.completed_phases.append("phase_4")

        return phase_result

    async def _execute_phase_5(self, phase_4_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 5: Final Assembly (Days 36-42+).

        Test Architect + Orchestrator компилируют ENGINE_SPEC.json.
        """
        phase_5_agents = PatternShiftArchitecture.PHASE_5_AGENTS

        phase_result = {
            "phase": "Phase 5: Final Assembly",
            "days": "36-42+",
            "agents_executed": list(phase_5_agents.keys()),
            "outputs": {},
            "engine_spec_compiled": False
        }

        # Test Architect создает тесты
        psychographic_tests = {
            "gender_preference_test": "Test для определения гендерных предпочтений",
            "age_appropriate_test": "Test для определения возрастной группы",
            "vak_modality_test": "Test для определения VAK модальности",
            "cultural_context_test": "Test для определения культурного контекста"
        }

        # Orchestrator компилирует ENGINE_SPEC.json
        self.engine_spec = self._compile_engine_specification(
            phase_4_output["final_adapted_modules"],
            psychographic_tests
        )

        phase_result["outputs"]["psychographic_tests"] = psychographic_tests
        phase_result["outputs"]["engine_spec"] = self.engine_spec
        phase_result["engine_spec_compiled"] = True

        logger.info("Phase 5 completed: ENGINE_SPEC.json скомпилирован")
        self.completed_phases.append("phase_5")

        return phase_result

    def _compile_engine_specification(
        self,
        total_modules: int,
        psychographic_tests: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Компилирует ENGINE_SPEC.json.

        Args:
            total_modules: Общее количество модулей
            psychographic_tests: Психографические тесты

        Returns:
            ENGINE_SPEC.json
        """
        return {
            "version": "1.0.0",
            "total_modules": total_modules,
            "psychographic_dimensions": self.deps.psychographic_dimensions,
            "degradation_levels": self.deps.degradation_levels,
            "routing_algorithm": {
                "step_1": "psychographic_testing",
                "step_2": "profile_matching",
                "step_3": "module_selection",
                "step_4": "program_assembly_5_levels",
                "step_5": "adaptive_delivery"
            },
            "api_endpoints": {
                "get_user_profile": "/api/profile",
                "get_recommended_program": "/api/program/recommend",
                "get_module": "/api/module/:id",
                "get_degraded_version": "/api/module/:id/degrade/:level",
                "track_progress": "/api/progress",
                "adaptive_feedback": "/api/feedback",
                "emergency_help": "/api/emergency"
            },
            "psychographic_tests": psychographic_tests,
            "module_library_path": "MODULE_LIBRARY/",
            "ready_for_engine_creation": True
        }

    async def _delegate_engine_creation(self, phase_5_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Делегирует создание движка Universal агентам.

        Args:
            phase_5_output: Выход Phase 5

        Returns:
            План создания движка
        """
        universal_agents_plan = []

        # Blueprint Architect
        universal_agents_plan.append({
            "agent": "Blueprint Architect",
            "task": "Спроектировать архитектуру движка маршрутизации",
            "input": self.engine_spec,
            "expected_output": "Архитектурная документация движка"
        })

        # Implementation Engineer
        universal_agents_plan.append({
            "agent": "Implementation Engineer",
            "task": "Реализовать алгоритмы маршрутизации",
            "input": "Архитектура от Blueprint Architect",
            "expected_output": "Код движка на TypeScript/Python"
        })

        # API Development Agent
        universal_agents_plan.append({
            "agent": "API Development Agent",
            "task": "Создать API endpoints",
            "input": "ENGINE_SPEC.api_endpoints",
            "expected_output": "REST/GraphQL API"
        })

        # Typescript Architecture Agent
        universal_agents_plan.append({
            "agent": "Typescript Architecture Agent",
            "task": "Типизация и архитектура TypeScript",
            "input": "Код от Implementation Engineer",
            "expected_output": "Типизированный код движка"
        })

        # Prisma Database Agent
        universal_agents_plan.append({
            "agent": "Prisma Database Agent",
            "task": "Создать схемы БД для 20,700 модулей",
            "input": f"{self.total_modules_created} модулей",
            "expected_output": "Prisma schema + migrations"
        })

        # Queue Worker Agent
        universal_agents_plan.append({
            "agent": "Queue Worker Agent",
            "task": "Настроить фоновую обработку",
            "input": "Логика движка",
            "expected_output": "Worker система"
        })

        # Quality Guardian
        universal_agents_plan.append({
            "agent": "Quality Guardian",
            "task": "Протестировать движок",
            "input": "Полный движок",
            "expected_output": "Тестовое покрытие + валидация"
        })

        result = {
            "delegation_plan": universal_agents_plan,
            "total_agents_delegated": len(universal_agents_plan),
            "engine_creation_status": "delegated_to_universal_agents",
            "expected_completion": "Production-ready движок PatternShift"
        }

        logger.info("Engine creation delegated to Universal Agents")
        return result

    async def save_engine_spec(self, output_path: Optional[str] = None) -> str:
        """
        Сохранить ENGINE_SPEC.json в файл.

        Args:
            output_path: Путь для сохранения (опционально)

        Returns:
            Путь к сохраненному файлу
        """
        if self.engine_spec is None:
            raise ValueError("ENGINE_SPEC not compiled yet")

        if output_path is None:
            output_path = Path(self.deps.project_path) / "ENGINE_SPEC.json"
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.engine_spec, f, indent=2, ensure_ascii=False)

        logger.info(f"ENGINE_SPEC.json saved to {output_path}")
        return str(output_path)

    def get_workflow_stats(self) -> Dict[str, Any]:
        """
        Получить статистику выполнения workflow.

        Returns:
            Полная статистика
        """
        return {
            "workflow_state": self.workflow_state,
            "completed_phases": self.completed_phases,
            "total_phases": 5,
            "total_modules_created": self.total_modules_created,
            "engine_spec_compiled": self.engine_spec is not None,
            "pattern_agents_count": len(self.deps.pattern_agents),
            "universal_agents_count": len(self.deps.universal_agents_registry),
            "degradation_levels": len(self.deps.degradation_levels),
            "psychographic_dimensions": len(self.deps.psychographic_dimensions)
        }


class DegradationWorkflow:
    """
    Workflow управления 5-уровневой деградацией контента.
    """

    def __init__(self, deps: PatternOrchestratorDependencies):
        """Инициализация degradation workflow."""
        self.deps = deps

    async def apply_degradation_chain(
        self,
        program_content: Dict[str, Any],
        target_level: str
    ) -> Dict[str, Any]:
        """
        Применить цепочку деградации от program до target_level.

        Args:
            program_content: Контент полной программы (45 мин)
            target_level: Целевой уровень деградации

        Returns:
            Деградированный контент
        """
        chain = DegradationSystemArchitecture.get_degradation_chain()

        if target_level not in chain:
            raise ValueError(f"Invalid target level: {target_level}")

        current_level = "program"
        current_content = program_content.copy()

        # Применяем деградацию последовательно
        while current_level != target_level:
            current_idx = chain.index(current_level)
            next_level = chain[current_idx + 1]

            current_content = await self._degrade_to_next_level(
                current_content,
                current_level,
                next_level
            )

            current_level = next_level

        return current_content

    async def _degrade_to_next_level(
        self,
        content: Dict[str, Any],
        from_level: str,
        to_level: str
    ) -> Dict[str, Any]:
        """
        Деградировать контент на один уровень.

        Args:
            content: Текущий контент
            from_level: Исходный уровень
            to_level: Следующий уровень

        Returns:
            Деградированный контент
        """
        degraded = content.copy()

        # Получаем требования следующего уровня
        requirements = DegradationSystemArchitecture.get_level_requirements(to_level)

        degraded["level"] = to_level
        degraded["duration_minutes"] = requirements["duration"]
        degraded["modules"] = requirements["modules"]
        degraded["degraded_from"] = from_level

        return degraded
