#!/usr/bin/env python3
"""
Зависимости для Archon Implementation Engineer Agent.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class DevelopmentFramework(Enum):
    """Фреймворки разработки."""
    FASTAPI = "fastapi"
    DJANGO = "django"
    FLASK = "flask"
    NEXTJS = "nextjs"
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"
    EXPRESS = "express"
    NEST = "nestjs"


class ProgrammingLanguage(Enum):
    """Языки программирования."""
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    GO = "go"
    RUST = "rust"
    JAVA = "java"
    CSHARP = "csharp"


class DatabaseType(Enum):
    """Типы баз данных."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    REDIS = "redis"
    SQLITE = "sqlite"
    PRISMA = "prisma"


class QualityStandard(Enum):
    """Стандарты качества кода."""
    BASIC = "basic"          # Базовая функциональность
    STANDARD = "standard"    # Стандартное качество с тестами
    HIGH = "high"           # Высокое качество с полным покрытием
    ENTERPRISE = "enterprise" # Корпоративные стандарты


@dataclass
class ImplementationEngineerDependencies:
    """
    Зависимости для Implementation Engineer Agent.

    Конфигурирует поведение агента для различных типов реализации.
    """

    # Основные настройки
    project_id: str = "default"
    agent_name: str = "archon_implementation_engineer"
    primary_language: ProgrammingLanguage = ProgrammingLanguage.PYTHON
    framework: DevelopmentFramework = DevelopmentFramework.FASTAPI

    # Archon интеграция
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
    archon_enabled: bool = True

    # Технологический стек
    database_type: DatabaseType = DatabaseType.POSTGRESQL
    preferred_languages: List[str] = field(default_factory=lambda: [
        "Python", "TypeScript", "JavaScript"
    ])
    additional_technologies: List[str] = field(default_factory=lambda: [
        "Docker", "Redis", "PostgreSQL", "React"
    ])

    # Настройки качества
    quality_standard: QualityStandard = QualityStandard.STANDARD
    enable_type_checking: bool = True
    enable_linting: bool = True
    enable_testing: bool = True
    test_coverage_threshold: float = 80.0

    # Настройки разработки
    code_style: str = "pep8"  # pep8, google, black
    max_file_lines: int = 500
    max_function_complexity: int = 10
    enable_async_patterns: bool = True

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "implementation", "coding", "best-practices", "agent-knowledge"
    ])
    knowledge_domain: str = "implementation.archon.local"

    # Безопасность и производительность
    enable_security_checks: bool = True
    enable_performance_optimization: bool = True
    enable_dependency_scanning: bool = True

    # Коллаборация
    auto_create_tests: bool = True
    collaborate_with_quality_guardian: bool = True
    delegate_complex_architecture: bool = True

    def get_development_config(self) -> Dict[str, Any]:
        """Получить конфигурацию разработки."""
        return {
            "language": self.primary_language.value,
            "framework": self.framework.value,
            "database": self.database_type.value,
            "quality_standard": self.quality_standard.value,
            "technologies": self.preferred_languages + self.additional_technologies,
            "async_enabled": self.enable_async_patterns,
            "type_checking": self.enable_type_checking
        }

    def get_quality_config(self) -> Dict[str, Any]:
        """Получить конфигурацию качества кода."""
        return {
            "standard": self.quality_standard.value,
            "code_style": self.code_style,
            "max_file_lines": self.max_file_lines,
            "max_complexity": self.max_function_complexity,
            "test_coverage": self.test_coverage_threshold,
            "linting": self.enable_linting,
            "testing": self.enable_testing,
            "security_checks": self.enable_security_checks
        }

    def get_collaboration_config(self) -> Dict[str, Any]:
        """Получить конфигурацию коллаборации."""
        return {
            "auto_tests": self.auto_create_tests,
            "quality_guardian": self.collaborate_with_quality_guardian,
            "delegate_architecture": self.delegate_complex_architecture,
            "archon_enabled": self.archon_enabled
        }

    def should_create_tests(self) -> bool:
        """Определить нужно ли создавать тесты."""
        return (
            self.enable_testing and
            self.quality_standard in [QualityStandard.STANDARD, QualityStandard.HIGH, QualityStandard.ENTERPRISE]
        )

    def get_file_structure_rules(self) -> Dict[str, Any]:
        """Получить правила структуры файлов."""
        rules = {
            "max_lines": self.max_file_lines,
            "separate_concerns": True,
            "use_type_hints": self.enable_type_checking
        }

        if self.primary_language == ProgrammingLanguage.PYTHON:
            rules.update({
                "follow_pep8": self.code_style == "pep8",
                "use_docstrings": True,
                "async_support": self.enable_async_patterns
            })
        elif self.primary_language == ProgrammingLanguage.TYPESCRIPT:
            rules.update({
                "strict_mode": True,
                "use_interfaces": True,
                "prefer_composition": True
            })

        return rules

    def get_security_requirements(self) -> List[str]:
        """Получить требования безопасности."""
        requirements = []

        if self.enable_security_checks:
            requirements.extend([
                "Input validation and sanitization",
                "SQL injection prevention",
                "XSS protection",
                "Authentication and authorization"
            ])

            if self.framework in [DevelopmentFramework.FASTAPI, DevelopmentFramework.DJANGO]:
                requirements.extend([
                    "CORS configuration",
                    "Rate limiting",
                    "Request size limits"
                ])

        return requirements

    def get_performance_requirements(self) -> List[str]:
        """Получить требования производительности."""
        requirements = []

        if self.enable_performance_optimization:
            requirements.extend([
                "Efficient database queries",
                "Proper caching strategies",
                "Memory usage optimization"
            ])

            if self.enable_async_patterns:
                requirements.extend([
                    "Async/await patterns",
                    "Non-blocking I/O operations",
                    "Connection pooling"
                ])

        return requirements

    def get_testing_strategy(self) -> Dict[str, Any]:
        """Получить стратегию тестирования."""
        if not self.enable_testing:
            return {"enabled": False}

        strategy = {
            "enabled": True,
            "coverage_threshold": self.test_coverage_threshold,
            "types": ["unit"]
        }

        if self.quality_standard in [QualityStandard.HIGH, QualityStandard.ENTERPRISE]:
            strategy["types"].extend(["integration", "end-to-end"])

        if self.quality_standard == QualityStandard.ENTERPRISE:
            strategy["types"].extend(["performance", "security"])

        return strategy