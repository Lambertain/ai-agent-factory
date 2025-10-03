# -*- coding: utf-8 -*-
"""
Зависимости Pattern Age Adaptation Agent.

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
class PatternAgeAdaptationDependencies:
    """
    Зависимости Pattern Age Adaptation Agent.

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

    # Возрастная адаптация
    age_versions: List[str] = field(
        default_factory=lambda: [
            "teens",           # 14-18 лет
            "young_adults",    # 19-25 лет
            "early_middle_age", # 26-35 лет
            "middle_age",      # 36-50 лет
            "seniors"          # 50+ лет
        ]
    )

    age_ranges: Dict[str, str] = field(
        default_factory=lambda: {
            "teens": "14-18",
            "young_adults": "19-25",
            "early_middle_age": "26-35",
            "middle_age": "36-50",
            "seniors": "50+"
        }
    )

    developmental_tasks: Dict[str, str] = field(
        default_factory=lambda: {
            "teens": "identity_formation",
            "young_adults": "intimacy_vs_isolation",
            "early_middle_age": "generativity_beginning",
            "middle_age": "generativity_peak",
            "seniors": "integrity_vs_despair"
        }
    )

    enable_developmental_validation: bool = True

    # Интеграция с универсальными агентами
    agent_name: str = "pattern_age_adaptation_agent"
    agent_type: str = "pattern_age_adaptation"

    # RAG и база знаний (для интеграции с Archon)
    knowledge_tags: List[str] = field(
        default_factory=lambda: [
            "pattern-age-adaptation",
            "developmental-psychology",
            "erikson",
            "lifespan-development",
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

    def get_developmental_task(self, age_version: str) -> str:
        """
        Получить задачу развития для возрастной версии.

        Args:
            age_version: Возрастная версия (teens, young_adults и т.д.)

        Returns:
            Задача развития по Эриксону
        """
        return self.developmental_tasks.get(age_version, "unknown")

    def get_age_range(self, age_version: str) -> str:
        """
        Получить возрастной диапазон для версии.

        Args:
            age_version: Возрастная версия

        Returns:
            Возрастной диапазон (например "14-18")
        """
        return self.age_ranges.get(age_version, "unknown")

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

class PatternAgeToUniversalBridge:
    """
    Мост между Pattern Age Adaptation Agent и остальной системой.

    Pattern Age Agent:
    - Получает гендерно-адаптированные модули от Gender Agent
    - Создает 5 возрастных версий каждого модуля
    - Передает результат VAK Adaptation Specialist
    """

    # Карта ответственности Pattern Age Agent
    PATTERN_AGE_RESPONSIBILITIES = {
        "input_from": "pattern_gender_adaptation",
        "input_format": "3 гендерные версии каждого модуля (masculine, feminine, neutral)",
        "output": "5 возрастных версий (teens, young_adults, early_middle_age, middle_age, seniors)",
        "output_to": "pattern_vak_adaptation",
        "multiplication_factor": 5,
        "total_modules_per_base": 15,  # 3 гендерные × 5 возрастных
        "workflow_stage": "Step 4.2 (Days 29-32)"
    }

    # Взаимодействие с другими Pattern агентами
    PATTERN_AGENTS_CHAIN = {
        "previous": {
            "agent": "pattern_gender_adaptation",
            "output": "Гендерно-адаптированные модули",
            "versions": 3  # masculine, feminine, neutral
        },
        "current": {
            "agent": "pattern_age_adaptation",
            "output": "Возрастно-адаптированные модули",
            "versions": 5  # teens, young_adults, early_middle, middle, seniors
        },
        "next": {
            "agent": "pattern_vak_adaptation",
            "output": "VAK-адаптированные модули",
            "versions": 3  # visual, audial, kinesthetic
        }
    }

    @staticmethod
    def get_workflow_position() -> Dict[str, Any]:
        """
        Получить позицию в workflow PatternShift.

        Returns:
            Словарь с описанием позиции workflow
        """
        return {
            "phase": "Phase 4: Multiplier Adaptation",
            "step": "Step 4.2 (Days 29-32)",
            "description": "Возрастная адаптация",
            "input": {
                "from_agent": "Pattern Gender Adaptation Agent",
                "format": "3 гендерные версии каждого модуля",
                "example_count": "Для 1 базового модуля → 3 модуля"
            },
            "processing": {
                "creates": "5 возрастных версий каждого входного модуля",
                "developmental_tasks": [
                    "Identity Formation (teens)",
                    "Intimacy vs Isolation (young adults)",
                    "Generativity Beginning (early middle)",
                    "Generativity Peak (middle age)",
                    "Integrity vs Despair (seniors)"
                ]
            },
            "output": {
                "to_agent": "Pattern VAK Adaptation Specialist",
                "format": "15 модулей (3 гендерные × 5 возрастных)",
                "example_count": "Для 1 базового модуля → 15 модулей"
            },
            "after_full_chain": {
                "pattern_orchestrator": "Компилирует ENGINE_SPEC.json",
                "universal_agents": "Создают движок маршрутизации"
            }
        }

    @staticmethod
    def get_age_adaptation_stats(base_modules_count: int) -> Dict[str, int]:
        """
        Получить статистику адаптации для заданного количества модулей.

        Args:
            base_modules_count: Количество базовых модулей

        Returns:
            Статистика обработки
        """
        gender_versions = 3  # от Gender Agent
        age_versions = 5     # создаем здесь

        return {
            "base_modules": base_modules_count,
            "input_modules": base_modules_count * gender_versions,
            "output_modules": base_modules_count * gender_versions * age_versions,
            "multiplication_factor": age_versions,
            "total_factor_so_far": gender_versions * age_versions  # 15x
        }
