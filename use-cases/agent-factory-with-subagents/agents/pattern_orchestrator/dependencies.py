# -*- coding: utf-8 -*-
"""
Зависимости Pattern Orchestrator Agent.

Полная архитектура координации 17 Pattern агентов и делегирования Universal агентам.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import sys
from pathlib import Path

# Добавляем путь к универсальным агентам
AGENT_FACTORY_PATH = Path("D:/Automation/agent-factory/use-cases/agent-factory-with-subagents")
if str(AGENT_FACTORY_PATH) not in sys.path:
    sys.path.insert(0, str(AGENT_FACTORY_PATH))


@dataclass
class PatternOrchestratorDependencies:
    """
    Зависимости Pattern Orchestrator Agent.

    Главный координатор всех 17 Pattern агентов и мост к Universal агентам.
    """

    # Основные настройки
    llm_api_key: str
    project_path: str = "D:\\Automation\\Development\\projects\\PatternShift"

    # PatternShift специфичные настройки
    patternshift_architecture_file: str = field(
        default="docs/final-kontent-architecture-complete.md"
    )
    patternshift_workflow_file: str = field(
        default="docs/pattern-agents-complete-workflow.md"
    )

    # 17 Pattern Agents
    pattern_agents: List[str] = field(
        default_factory=lambda: [
            "pattern_nlp_technique_master",
            "pattern_ericksonian_hypnosis_scriptwriter",
            "pattern_exercise_architect",
            "pattern_microhabit_designer",
            "pattern_metaphor_weaver",
            "pattern_gamification_architect",
            "pattern_integration_synthesizer",
            "pattern_feedback_orchestrator",
            "pattern_progress_narrator",
            "pattern_transition_craftsman",
            "pattern_safety_protocol",
            "pattern_scientific_validator",
            "pattern_gender_adaptation",
            "pattern_age_adaptation",
            "pattern_vak_adaptation",
            "pattern_cultural_adaptation",
            "pattern_test_architect"
        ]
    )

    # 5-уровневая система деградации
    degradation_levels: Dict[str, Dict[str, Any]] = field(
        default_factory=lambda: {
            "program": {"duration": 45, "modules": "all"},
            "phase": {"duration": 25, "modules": "key"},
            "day": {"duration": 15, "modules": "daily"},
            "session": {"duration": 5, "modules": "express"},
            "emergency": {"duration": 1, "modules": "critical"}
        }
    )

    # Психографические измерения
    psychographic_dimensions: Dict[str, List[str]] = field(
        default_factory=lambda: {
            "gender": ["masculine", "feminine", "neutral"],
            "age": ["teens", "young_adults", "early_middle_age", "middle_age", "seniors"],
            "vak": ["visual", "audial", "kinesthetic"],
            "culture": ["individualistic", "collectivistic", "balanced"]
        }
    )

    # Модульная статистика
    total_base_modules: int = 460
    gender_multiplier: int = 3
    age_multiplier: int = 5
    vak_multiplier: int = 3

    # Emergency режим
    enable_emergency_mode: bool = True

    # Интеграция с универсальными агентами
    agent_name: str = "pattern_orchestrator_agent"
    agent_type: str = "pattern_orchestrator"

    # RAG и база знаний
    knowledge_tags: List[str] = field(
        default_factory=lambda: [
            "pattern-orchestrator",
            "system-architecture",
            "agent-coordination",
            "content-degradation",
            "psychographic-routing",
            "pydantic-ai",
            "patternshift"
        ]
    )
    knowledge_domain: str = ""

    # Archon интеграция
    archon_project_id: str = ""
    enable_task_delegation: bool = True

    # Universal Agents для делегирования
    universal_agents_registry: Dict[str, str] = field(
        default_factory=lambda: {
            "blueprint_architect": "Blueprint Architect",
            "implementation_engineer": "Implementation Engineer",
            "api_development": "API Development Agent",
            "typescript_architecture": "Typescript Architecture Agent",
            "prisma_database": "Prisma Database Agent",
            "queue_worker": "Queue Worker Agent",
            "quality_guardian": "Quality Guardian"
        }
    )

    def __post_init__(self):
        """Инициализация после создания."""
        project_path = Path(self.project_path)
        if not project_path.exists():
            raise ValueError(f"Путь к проекту PatternShift не существует: {self.project_path}")

        architecture_file = project_path / self.patternshift_architecture_file
        if not architecture_file.exists():
            raise ValueError(f"Файл архитектуры не найден: {architecture_file}")

    def get_architecture_path(self) -> Path:
        """Получить путь к файлу архитектуры PatternShift."""
        return Path(self.project_path) / self.patternshift_architecture_file

    def get_workflow_path(self) -> Path:
        """Получить путь к файлу workflow Pattern агентов."""
        return Path(self.project_path) / self.patternshift_workflow_file

    def get_total_adapted_modules(self) -> int:
        """Получить итоговое количество адаптированных модулей."""
        return (
            self.total_base_modules *
            self.gender_multiplier *
            self.age_multiplier *
            self.vak_multiplier
        )

    def get_degradation_level_config(self, level: str) -> Dict[str, Any]:
        """
        Получить конфигурацию уровня деградации.

        Args:
            level: Уровень (program, phase, day, session, emergency)

        Returns:
            Конфигурация уровня
        """
        return self.degradation_levels.get(level, {})


# === ПОЛНАЯ АРХИТЕКТУРА PATTERNSHIFT ===

class PatternShiftArchitecture:
    """
    Полная архитектура PatternShift: 17 Pattern агентов → Orchestrator → Universal агенты → Движок.
    """

    # === PHASE 1: CONTENT CREATION (Days 1-14) ===
    PHASE_1_AGENTS = {
        "pattern_nlp_technique_master": {
            "role": "Мастер НЛП техник",
            "creates": "100+ НЛП техник (рефрейминг, якорение, субмодальности)",
            "output_to": "pattern_integration_synthesizer",
            "days": "1-4"
        },
        "pattern_ericksonian_hypnosis_scriptwriter": {
            "role": "Мастер эриксоновского гипноза",
            "creates": "50+ гипнотических скриптов (метафоры, встроенные команды)",
            "output_to": "pattern_integration_synthesizer",
            "days": "5-7"
        },
        "pattern_exercise_architect": {
            "role": "Архитектор практических упражнений",
            "creates": "80+ упражнений (дыхательные, телесные, когнитивные)",
            "output_to": "pattern_integration_synthesizer",
            "days": "8-10"
        },
        "pattern_microhabit_designer": {
            "role": "Дизайнер микропривычек",
            "creates": "70+ микропривычек для закрепления изменений",
            "output_to": "pattern_integration_synthesizer",
            "days": "11-12"
        },
        "pattern_metaphor_weaver": {
            "role": "Мастер терапевтических метафор",
            "creates": "60+ метафор для подсознательных изменений",
            "output_to": "pattern_integration_synthesizer",
            "days": "13"
        },
        "pattern_gamification_architect": {
            "role": "Архитектор геймификации",
            "creates": "Игровые механики, достижения, прогрессию",
            "output_to": "pattern_integration_synthesizer",
            "days": "14"
        }
    }

    # === PHASE 2: INTEGRATION & POLISH (Days 15-21) ===
    PHASE_2_AGENTS = {
        "pattern_integration_synthesizer": {
            "role": "Системный интегратор",
            "receives_from": ["все агенты Phase 1"],
            "creates": "Интегрированные программы трансформации с логическими связями",
            "output_to": ["pattern_feedback_orchestrator", "pattern_progress_narrator"],
            "days": "15-17"
        },
        "pattern_feedback_orchestrator": {
            "role": "Мастер обратной связи",
            "receives_from": ["pattern_integration_synthesizer"],
            "creates": "Системы отслеживания прогресса, адаптивной обратной связи",
            "output_to": "pattern_transition_craftsman",
            "days": "18-19"
        },
        "pattern_progress_narrator": {
            "role": "Рассказчик прогресса",
            "receives_from": ["pattern_integration_synthesizer"],
            "creates": "Нарративы путешествия пользователя, празднование успехов",
            "output_to": "pattern_transition_craftsman",
            "days": "18-19"
        },
        "pattern_transition_craftsman": {
            "role": "Мастер переходов",
            "receives_from": ["pattern_feedback_orchestrator", "pattern_progress_narrator"],
            "creates": "Плавные переходы между модулями и уровнями",
            "output_to": ["pattern_safety_protocol"],
            "days": "20-21"
        }
    }

    # === PHASE 3: SAFETY & SCIENCE (Days 22-24) ===
    PHASE_3_AGENTS = {
        "pattern_safety_protocol": {
            "role": "Страж безопасности",
            "receives_from": ["pattern_transition_craftsman"],
            "validates": "Отсутствие триггеров, травматичного контента, ethical issues",
            "output_to": "pattern_scientific_validator",
            "days": "22-23"
        },
        "pattern_scientific_validator": {
            "role": "Научный валидатор",
            "receives_from": ["pattern_safety_protocol"],
            "validates": "Соответствие научным исследованиям, evidence-based подходам",
            "output_to": "pattern_gender_adaptation",
            "days": "24"
        }
    }

    # === PHASE 4: MULTIPLIER ADAPTATION (Days 25-35) ===
    PHASE_4_AGENTS = {
        "pattern_gender_adaptation": {
            "role": "Эксперт гендерной адаптации",
            "receives_from": ["pattern_scientific_validator"],
            "creates": "3 версии (masculine, feminine, neutral)",
            "multiplier": 3,
            "output_to": "pattern_age_adaptation",
            "days": "25-28"
        },
        "pattern_age_adaptation": {
            "role": "Эксперт возрастной адаптации",
            "receives_from": ["pattern_gender_adaptation"],
            "creates": "5 версий (teens, young_adults, early_middle, middle, seniors)",
            "multiplier": 5,
            "output_to": "pattern_vak_adaptation",
            "days": "29-32"
        },
        "pattern_vak_adaptation": {
            "role": "Эксперт сенсорной адаптации",
            "receives_from": ["pattern_age_adaptation"],
            "creates": "3 версии (Visual, Audial, Kinesthetic)",
            "multiplier": 3,
            "output_to": "pattern_cultural_adaptation",
            "days": "33-34"
        },
        "pattern_cultural_adaptation": {
            "role": "Эксперт культурной адаптации",
            "receives_from": ["pattern_vak_adaptation"],
            "creates": "Культурно-полированные версии",
            "output_to": "pattern_orchestrator",
            "days": "35"
        }
    }

    # === PHASE 5: FINAL ASSEMBLY (Days 36-42+) ===
    PHASE_5_AGENTS = {
        "pattern_test_architect": {
            "role": "Архитектор психологических тестов",
            "creates": "Диагностические тесты для психографического профилирования",
            "tests": ["Gender preference", "Age-appropriate", "VAK modality", "Cultural context"],
            "output_to": "pattern_orchestrator",
            "days": "36-37"
        },
        "pattern_orchestrator": {
            "role": "Главный координатор и архитектор движка",
            "receives_from": ["pattern_cultural_adaptation", "pattern_test_architect"],
            "compiles": "ENGINE_SPEC.json с правилами маршрутизации",
            "delegates_to": "Universal Agents",
            "days": "38-42+"
        }
    }

    # === UNIVERSAL AGENTS (создание движка) ===
    UNIVERSAL_AGENTS_FOR_ENGINE = {
        "blueprint_architect": {
            "role": "Проектирует архитектуру движка маршрутизации",
            "input_from": "pattern_orchestrator",
            "output": "Архитектурная документация движка",
            "next_agent": "implementation_engineer"
        },
        "implementation_engineer": {
            "role": "Реализует алгоритмы маршрутизации и логику движка",
            "input_from": "blueprint_architect",
            "output": "Код движка на TypeScript/Python",
            "next_agent": "api_development"
        },
        "api_development": {
            "role": "Создает API endpoints для движка",
            "input_from": "implementation_engineer",
            "output": "REST/GraphQL API",
            "next_agent": "typescript_architecture"
        },
        "typescript_architecture": {
            "role": "Типизация и архитектура TypeScript кода",
            "input_from": "api_development",
            "output": "Типизированный код движка",
            "next_agent": "prisma_database"
        },
        "prisma_database": {
            "role": "Схемы БД для хранения 20,700 модулей",
            "input_from": "pattern_orchestrator",
            "output": "Prisma schema + migrations",
            "next_agent": "queue_worker"
        },
        "queue_worker": {
            "role": "Фоновые процессы обработки контента",
            "input_from": "implementation_engineer",
            "output": "Worker система для обработки",
            "next_agent": "quality_guardian"
        },
        "quality_guardian": {
            "role": "Тестирование движка и валидация",
            "input_from": "all_previous",
            "output": "Тестовое покрытие + отчет валидации",
            "next_agent": None
        }
    }

    @staticmethod
    def get_full_workflow() -> Dict[str, Any]:
        """
        Получить полный workflow PatternShift.

        Returns:
            Полный workflow от Phase 1 до production движка
        """
        return {
            "phase_1": {
                "name": "Content Creation",
                "days": "1-14",
                "agents": PatternShiftArchitecture.PHASE_1_AGENTS,
                "output": "~460 базовых модулей"
            },
            "phase_2": {
                "name": "Integration & Polish",
                "days": "15-21",
                "agents": PatternShiftArchitecture.PHASE_2_AGENTS,
                "output": "Интегрированные программы"
            },
            "phase_3": {
                "name": "Safety & Science",
                "days": "22-24",
                "agents": PatternShiftArchitecture.PHASE_3_AGENTS,
                "output": "Валидированные модули"
            },
            "phase_4": {
                "name": "Multiplier Adaptation",
                "days": "25-35",
                "agents": PatternShiftArchitecture.PHASE_4_AGENTS,
                "output": "~20,700 адаптированных модулей"
            },
            "phase_5": {
                "name": "Final Assembly",
                "days": "36-42+",
                "agents": PatternShiftArchitecture.PHASE_5_AGENTS,
                "output": "ENGINE_SPEC.json + Движок"
            },
            "engine_creation": {
                "name": "Engine Implementation",
                "agents": PatternShiftArchitecture.UNIVERSAL_AGENTS_FOR_ENGINE,
                "output": "Production-ready движок маршрутизации"
            }
        }

    @staticmethod
    def get_module_multiplication_stats(base_modules: int = 460) -> Dict[str, int]:
        """
        Получить статистику умножения модулей через все фазы.

        Args:
            base_modules: Количество базовых модулей

        Returns:
            Статистика на каждом этапе
        """
        return {
            "phase_3_output": base_modules,
            "after_gender": base_modules * 3,
            "after_age": base_modules * 3 * 5,
            "after_vak": base_modules * 3 * 5 * 3,
            "final_modules": base_modules * 3 * 5 * 3,
            "total_multiplier": 45
        }


# === DEGRADATION SYSTEM ARCHITECTURE ===

class DegradationSystemArchitecture:
    """
    Архитектура 5-уровневой системы деградации контента.
    """

    DEGRADATION_RULES = {
        "program_to_phase": {
            "from": "program",
            "to": "phase",
            "rules": [
                "Убрать вводную часть (5 мин)",
                "Сократить основные техники до ключевых (15→10 мин)",
                "Убрать полную интеграцию, оставить быструю (5→2 мин)"
            ],
            "duration_change": "45 мин → 25 мин"
        },
        "phase_to_day": {
            "from": "phase",
            "to": "day",
            "rules": [
                "Оставить одну мощную технику (10 мин)",
                "Добавить микропривычку для закрепления (3 мин)",
                "Быстрая настройка (2 мин)"
            ],
            "duration_change": "25 мин → 15 мин"
        },
        "day_to_session": {
            "from": "day",
            "to": "session",
            "rules": [
                "Экспресс-техника (4 мин)",
                "Микродействие (1 мин)",
                "Без подготовки и интеграции"
            ],
            "duration_change": "15 мин → 5 мин"
        },
        "session_to_emergency": {
            "from": "session",
            "to": "emergency",
            "rules": [
                "Одна мгновенная техника (60 сек)",
                "Работает БЕЗ подготовки",
                "Мгновенный эффект",
                "Безопасно в любом состоянии"
            ],
            "duration_change": "5 мин → 1 мин"
        }
    }

    @staticmethod
    def get_degradation_chain() -> List[str]:
        """Получить цепочку деградации."""
        return ["program", "phase", "day", "session", "emergency"]

    @staticmethod
    def get_level_requirements(level: str) -> Dict[str, Any]:
        """
        Получить требования к уровню деградации.

        Args:
            level: Уровень деградации

        Returns:
            Требования и характеристики уровня
        """
        requirements = {
            "program": {
                "duration": 45,
                "modules": "all",
                "depth": "full",
                "requires_preparation": True,
                "context": "Дома, спокойная обстановка"
            },
            "phase": {
                "duration": 25,
                "modules": "key",
                "depth": "focused",
                "requires_preparation": True,
                "context": "Дома или тихое место"
            },
            "day": {
                "duration": 15,
                "modules": "daily",
                "depth": "practical",
                "requires_preparation": False,
                "context": "Любое тихое место"
            },
            "session": {
                "duration": 5,
                "modules": "express",
                "depth": "quick",
                "requires_preparation": False,
                "context": "Где угодно"
            },
            "emergency": {
                "duration": 1,
                "modules": "critical",
                "depth": "instant",
                "requires_preparation": False,
                "context": "В любой экстренной ситуации"
            }
        }
        return requirements.get(level, {})
