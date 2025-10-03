# -*- coding: utf-8 -*-
"""
Зависимости Pattern Gender Adaptation Agent.

Интеграция с PatternShift архитектурой и универсальными Pydantic AI инструментами.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import sys
from pathlib import Path

# Добавляем путь к универсальным агентам для использования декораторов
AGENT_FACTORY_PATH = Path("D:/Automation/agent-factory/use-cases/agent-factory-with-subagents")
if str(AGENT_FACTORY_PATH) not in sys.path:
    sys.path.insert(0, str(AGENT_FACTORY_PATH))


@dataclass
class PatternGenderAdaptationDependencies:
    """
    Зависимости Pattern Gender Adaptation Agent.

    Включает интеграцию с PatternShift архитектурой и универсальными
    инструментами Pydantic AI.
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

    # Гендерная адаптация
    gender_versions: List[str] = field(
        default_factory=lambda: ["masculine", "feminine", "neutral"]
    )
    enable_stereotype_validation: bool = True

    # Интеграция с универсальными агентами
    agent_name: str = "pattern_gender_adaptation_agent"
    agent_type: str = "pattern_gender_adaptation"

    # RAG и база знаний (для интеграции с Archon)
    knowledge_tags: List[str] = field(
        default_factory=lambda: [
            "pattern-gender-adaptation",
            "gender-psychology",
            "pydantic-ai",
            "patternshift"
        ]
    )
    knowledge_domain: str = ""

    # Archon интеграция
    archon_project_id: str = ""
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"

    # Межагентное взаимодействие
    can_delegate_to_universal_agents: bool = True
    universal_agents_registry: Dict[str, str] = field(
        default_factory=lambda: {
            "api_development": "API Development Agent",
            "typescript_architecture": "Typescript Architecture Agent",
            "prisma_database": "Prisma Database Agent",
            "blueprint_architect": "Blueprint Architect",
            "implementation_engineer": "Implementation Engineer",
            "quality_guardian": "Quality Guardian"
        }
    )

    def __post_init__(self):
        """Инициализация после создания."""
        # Проверяем наличие критических путей
        project_path = Path(self.project_path)
        if not project_path.exists():
            raise ValueError(f"Путь к проекту PatternShift не существует: {self.project_path}")

        architecture_file = project_path / self.patternshift_architecture_file
        if not architecture_file.exists():
            raise ValueError(
                f"Файл архитектуры не найден: {architecture_file}"
            )

    def get_architecture_path(self) -> Path:
        """Получить путь к файлу архитектуры PatternShift."""
        return Path(self.project_path) / self.patternshift_architecture_file

    def get_workflow_path(self) -> Path:
        """Получить путь к файлу workflow Pattern агентов."""
        return Path(self.project_path) / self.patternshift_workflow_file

    def should_delegate(self, task_keywords: List[str]) -> Optional[str]:
        """
        Определить нужно ли делегировать задачу универсальному агенту.

        Args:
            task_keywords: Ключевые слова задачи

        Returns:
            Тип универсального агента для делегирования или None
        """
        # Ключевые слова для делегирования техническим агентам
        delegation_map = {
            "api_development": ["api", "endpoint", "rest", "graphql"],
            "typescript_architecture": ["typescript", "types", "архитектура"],
            "prisma_database": ["database", "схема", "migration", "prisma"],
            "blueprint_architect": ["архитектура движка", "проектирование"],
            "implementation_engineer": ["реализация движка", "код движка"],
            "quality_guardian": ["тестирование", "qa", "валидация"]
        }

        for agent_type, keywords in delegation_map.items():
            task_keywords_lower = [kw.lower() for kw in task_keywords]
            if any(kw in task_keywords_lower for kw in keywords):
                return agent_type

        return None


# === АРХИТЕКТУРА ВЗАИМОДЕЙСТВИЯ PATTERN И УНИВЕРСАЛЬНЫХ АГЕНТОВ ===

class PatternToUniversalBridge:
    """
    Мост между Pattern агентами и универсальными агентами.

    Pattern агенты создают КОНТЕНТ (модули, техники, адаптации).
    Универсальные агенты создают ДВИЖОК (архитектура, API, база данных).

    Схема работы:
    1. Pattern агенты (Gender, Age, VAK, Cultural, Orchestrator) создают контент
    2. Pattern Orchestrator компилирует всё в спецификацию движка
    3. Универсальные агенты получают спецификацию и создают движок:
       - Blueprint Architect -> проектирует архитектуру
       - Implementation Engineer -> реализует алгоритмы маршрутизации
       - API Development Agent -> создает endpoints
       - Typescript Architecture Agent -> типизация
       - Prisma Database Agent -> схемы БД для модулей
       - Queue Worker Agent -> фоновая обработка
    4. Quality Guardian тестирует весь движок
    """

    # Карта ответственности Pattern агентов
    PATTERN_AGENTS_RESPONSIBILITIES = {
        "pattern_gender_adaptation": {
            "output": "3 версии модулей (masculine, feminine, neutral)",
            "consumers": ["pattern_age_adaptation"],
            "format": "JSON модули с гендерными адаптациями"
        },
        "pattern_age_adaptation": {
            "output": "5 возрастных версий модулей (14-18, 19-25, 26-35, 36-50, 50+)",
            "consumers": ["pattern_vak_adaptation"],
            "format": "JSON модули с возрастными адаптациями"
        },
        "pattern_vak_adaptation": {
            "output": "3 VAK версии (Visual, Audial, Kinesthetic)",
            "consumers": ["pattern_cultural_adaptation"],
            "format": "JSON модули с сенсорными адаптациями"
        },
        "pattern_cultural_adaptation": {
            "output": "Культурно-адаптированные модули",
            "consumers": ["pattern_orchestrator"],
            "format": "JSON модули с культурной полировкой"
        },
        "pattern_orchestrator": {
            "output": "Полная спецификация движка + все модули",
            "consumers": [
                "blueprint_architect",
                "implementation_engineer",
                "api_development",
                "typescript_architecture",
                "prisma_database",
                "queue_worker"
            ],
            "format": "ENGINE_SPEC.json + MODULE_LIBRARY/"
        }
    }

    # Карта ответственности Universal агентов (для движка)
    UNIVERSAL_AGENTS_FOR_ENGINE = {
        "blueprint_architect": {
            "role": "Проектирует архитектуру движка",
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
            "role": "Схемы БД для хранения модулей",
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
    def get_delegation_chain(pattern_agent_type: str) -> List[str]:
        """
        Получить цепочку делегирования для Pattern агента.

        Args:
            pattern_agent_type: Тип Pattern агента

        Returns:
            Список универсальных агентов в цепочке
        """
        responsibilities = PatternToUniversalBridge.PATTERN_AGENTS_RESPONSIBILITIES
        if pattern_agent_type in responsibilities:
            return responsibilities[pattern_agent_type].get("consumers", [])
        return []

    @staticmethod
    def get_engine_workflow() -> Dict[str, Any]:
        """
        Получить полный workflow создания движка.

        Returns:
            Словарь с описанием workflow
        """
        return {
            "phase_1_content_creation": {
                "agents": [
                    "pattern_gender_adaptation",
                    "pattern_age_adaptation",
                    "pattern_vak_adaptation",
                    "pattern_cultural_adaptation"
                ],
                "output": "15,000+ адаптированных модулей"
            },
            "phase_2_orchestration": {
                "agents": ["pattern_orchestrator"],
                "output": "ENGINE_SPEC.json + MODULE_LIBRARY/"
            },
            "phase_3_engine_architecture": {
                "agents": ["blueprint_architect"],
                "output": "Архитектура движка"
            },
            "phase_4_engine_implementation": {
                "agents": [
                    "implementation_engineer",
                    "api_development",
                    "typescript_architecture",
                    "prisma_database",
                    "queue_worker"
                ],
                "output": "Полный код движка"
            },
            "phase_5_validation": {
                "agents": ["quality_guardian"],
                "output": "Валидированный движок готовый к production"
            }
        }
