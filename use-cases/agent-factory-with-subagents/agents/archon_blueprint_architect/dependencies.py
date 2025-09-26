#!/usr/bin/env python3
"""
Зависимости для Archon Blueprint Architect Agent.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class ArchitecturalPattern(Enum):
    """Архитектурные паттерны."""
    MICROSERVICES = "microservices"
    MONOLITH = "monolith"
    LAYERED = "layered"
    EVENT_DRIVEN = "event_driven"
    HEXAGONAL = "hexagonal"
    CLEAN_ARCHITECTURE = "clean_architecture"


class ScalabilityLevel(Enum):
    """Уровни масштабируемости."""
    SMALL = "small"        # < 1000 пользователей
    MEDIUM = "medium"      # 1K-100K пользователей
    LARGE = "large"        # 100K-1M пользователей
    ENTERPRISE = "enterprise" # > 1M пользователей


@dataclass
class BlueprintArchitectDependencies:
    """
    Зависимости для Blueprint Architect Agent.

    Конфигурирует поведение агента для различных типов архитектурного проектирования.
    """

    # Основные настройки
    project_id: str = "default"
    architectural_pattern: ArchitecturalPattern = ArchitecturalPattern.LAYERED
    scalability_level: ScalabilityLevel = ScalabilityLevel.MEDIUM

    # Archon интеграция
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
    archon_enabled: bool = True

    # Технологические предпочтения
    preferred_technologies: List[str] = field(default_factory=lambda: [
        "Python", "TypeScript", "PostgreSQL", "Redis"
    ])
    
    # Настройки проектирования
    include_security_patterns: bool = True
    include_performance_patterns: bool = True
    include_monitoring_patterns: bool = True
    
    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "architecture", "design-patterns", "blueprints", "agent-knowledge"
    ])
    knowledge_domain: str = "architecture.archon.local"

    # Коллаборация
    delegate_implementation_details: bool = True
    collaborate_with_quality_guardian: bool = True

    def get_architecture_config(self) -> Dict[str, Any]:
        """Получить конфигурацию архитектуры."""
        return {
            "pattern": self.architectural_pattern.value,
            "scalability": self.scalability_level.value,
            "technologies": self.preferred_technologies,
            "security_patterns": self.include_security_patterns,
            "performance_patterns": self.include_performance_patterns,
            "monitoring_patterns": self.include_monitoring_patterns
        }

    def get_design_constraints(self) -> Dict[str, Any]:
        """Получить ограничения проектирования."""
        constraints = {}
        
        if self.scalability_level == ScalabilityLevel.SMALL:
            constraints["max_services"] = 3
            constraints["complexity"] = "low"
        elif self.scalability_level == ScalabilityLevel.ENTERPRISE:
            constraints["max_services"] = 50
            constraints["complexity"] = "high"
        else:
            constraints["max_services"] = 10
            constraints["complexity"] = "medium"
            
        return constraints