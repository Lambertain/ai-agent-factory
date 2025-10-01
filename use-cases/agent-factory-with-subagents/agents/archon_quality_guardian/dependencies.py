# -*- coding: utf-8 -*-
"""
Зависимости для Archon Quality Guardian Agent
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from .settings import QualityGuardianSettings, load_settings


@dataclass
class QualityGuardianDependencies:
    """Зависимости агента Quality Guardian с поддержкой RAG и конфигурируемости."""

    # Основные настройки
    settings: QualityGuardianSettings = field(default_factory=load_settings)
    api_key: str = field(default="")
    project_path: str = field(default="")

    # Имя агента для защиты от отсутствия знаний в RAG
    agent_name: str = field(default="archon_quality_guardian")

    # RAG конфигурация
    knowledge_tags: List[str] = field(
        default_factory=lambda: [
            "quality-assurance",
            "code-review",
            "agent-knowledge",
            "pydantic-ai"
        ]
    )
    knowledge_domain: Optional[str] = field(default=None)
    archon_project_id: str = field(default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a")

    # Конфигурация проекта
    project_type: str = field(default="general")  # python, typescript, fullstack, general
    language: str = field(default="python")
    framework: Optional[str] = field(default=None)

    # Quality Standards
    test_coverage_threshold: float = field(default=80.0)
    complexity_threshold: int = field(default=10)
    maintainability_threshold: float = field(default=50.0)

    # CI/CD Integration
    ci_cd_platform: Optional[str] = field(default=None)  # github, gitlab, jenkins
    enable_auto_fix: bool = field(default=True)
    enable_ai_review: bool = field(default=True)

    # Security Configuration
    security_scan_enabled: bool = field(default=True)
    security_severity_threshold: str = field(default="medium")

    # Archon Task Management
    enable_task_delegation: bool = field(default=True)
    delegation_threshold: str = field(default="medium")

    def __post_init__(self):
        """Инициализация зависимостей."""
        # Установка API ключа из настроек если не указан
        if not self.api_key and self.settings:
            self.api_key = self.settings.llm_api_key

        # Установка порогов из настроек
        if self.settings:
            self.test_coverage_threshold = self.settings.test_coverage_threshold
            self.complexity_threshold = self.settings.complexity_threshold
            self.maintainability_threshold = self.settings.maintainability_threshold
            self.security_scan_enabled = self.settings.security_scan_enabled
            self.enable_auto_fix = self.settings.enable_auto_fix
            self.enable_ai_review = self.settings.enable_ai_review

        # Автоопределение имени агента если не указано
        if not self.agent_name:
            module_parts = self.__class__.__module__.split('.')
            if 'agents' in module_parts:
                agent_index = module_parts.index('agents')
                if agent_index + 1 < len(module_parts):
                    self.agent_name = module_parts[agent_index + 1]

    def should_delegate(self, task_keywords: List[str]) -> Optional[str]:
        """
        Определить нужно ли делегировать задачу другому агенту.

        Args:
            task_keywords: Ключевые слова из задачи

        Returns:
            Тип агента для делегирования или None
        """
        # Матрица компетенций для делегирования
        competency_matrix = {
            "security_audit": ["security", "vulnerability", "penetration", "cve"],
            "performance_optimization": ["performance", "optimization", "profiling", "speed"],
            "uiux_enhancement": ["ui", "ux", "design", "interface"],
            "typescript_architecture": ["typescript", "architecture", "types"]
        }

        # Проверяем пересечение с компетенциями других агентов
        for agent_type, competencies in competency_matrix.items():
            overlap = set(task_keywords) & set(competencies)
            if len(overlap) >= 2:  # Значительное пересечение
                return agent_type

        return None

    def get_quality_config(self) -> Dict[str, Any]:
        """
        Получить конфигурацию качества для текущего проекта.

        Returns:
            Словарь с настройками качества
        """
        return {
            "test_coverage_threshold": self.test_coverage_threshold,
            "complexity_threshold": self.complexity_threshold,
            "maintainability_threshold": self.maintainability_threshold,
            "security_scan_enabled": self.security_scan_enabled,
            "security_severity_threshold": self.security_severity_threshold,
            "enable_auto_fix": self.enable_auto_fix,
            "enable_ai_review": self.enable_ai_review
        }

    def get_tool_config(self) -> Dict[str, Any]:
        """
        Получить конфигурацию инструментов для текущего языка/фреймворка.

        Returns:
            Словарь с настройками инструментов
        """
        if self.language == "python":
            return {
                "linting": ["pylint", "flake8"],
                "type_checking": ["mypy"],
                "security": ["bandit", "safety"],
                "complexity": ["radon"],
                "coverage": ["pytest-cov"]
            }
        elif self.language == "typescript":
            return {
                "linting": ["eslint"],
                "type_checking": ["tsc"],
                "security": ["snyk", "npm_audit"],
                "complexity": ["complexity-report"],
                "coverage": ["jest"]
            }
        else:
            return {
                "linting": [],
                "type_checking": [],
                "security": [],
                "complexity": [],
                "coverage": []
            }
