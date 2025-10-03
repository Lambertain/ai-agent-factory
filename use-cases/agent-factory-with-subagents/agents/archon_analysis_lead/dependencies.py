#!/usr/bin/env python3
"""
Зависимости для Archon Analysis Lead Agent.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class AnalysisMethod(Enum):
    """Методы анализа требований."""
    STRUCTURED = "structured"
    EXPLORATORY = "exploratory"
    COMPARATIVE = "comparative"
    RISK_ANALYSIS = "risk_analysis"


class RequirementType(Enum):
    """Типы требований."""
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS = "business"
    TECHNICAL = "technical"
    USER_STORY = "user_story"


@dataclass
class AnalysisLeadDependencies:
    """
    Зависимости для Analysis Lead Agent.

    Конфигурирует поведение агента для различных типов анализа.
    """

    # Основные настройки
    project_id: str = "default"
    agent_name: str = "archon_analysis_lead"
    analysis_method: AnalysisMethod = AnalysisMethod.STRUCTURED

    # Archon интеграция
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
    archon_enabled: bool = True

    # Настройки анализа
    requirement_types: List[RequirementType] = field(default_factory=lambda: [
        RequirementType.FUNCTIONAL,
        RequirementType.BUSINESS,
        RequirementType.TECHNICAL
    ])

    # Параметры декомпозиции
    max_decomposition_depth: int = 4
    min_task_granularity: str = "1-4 часа работы"

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "analysis", "requirements", "planning", "agent-knowledge"
    ])
    knowledge_domain: str = "analysis.archon.local"

    # Настройки отчетности
    generate_detailed_reports: bool = True
    include_risk_assessment: bool = True
    include_timeline_estimates: bool = True

    # Коллаборация с другими агентами
    delegate_architecture_tasks: bool = True
    delegate_implementation_research: bool = True

    def get_analysis_config(self) -> Dict[str, Any]:
        """Получить конфигурацию анализа."""
        return {
            "method": self.analysis_method.value,
            "requirement_types": [rt.value for rt in self.requirement_types],
            "max_depth": self.max_decomposition_depth,
            "granularity": self.min_task_granularity,
            "detailed_reports": self.generate_detailed_reports,
            "risk_assessment": self.include_risk_assessment,
            "timeline_estimates": self.include_timeline_estimates
        }

    def get_collaboration_config(self) -> Dict[str, bool]:
        """Получить настройки коллаборации."""
        return {
            "delegate_architecture": self.delegate_architecture_tasks,
            "delegate_implementation": self.delegate_implementation_research,
            "archon_enabled": self.archon_enabled
        }