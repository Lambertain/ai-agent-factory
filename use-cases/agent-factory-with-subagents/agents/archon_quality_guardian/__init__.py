# -*- coding: utf-8 -*-
"""
Archon Quality Guardian Agent

Универсальный агент для автоматизации контроля качества кода,
AI-powered code review, мониторинга метрик и интеграции с CI/CD.
"""

from .agent import agent, run_quality_guardian
from .dependencies import QualityGuardianDependencies
from .settings import QualityGuardianSettings, load_settings

__all__ = [
    "agent",
    "run_quality_guardian",
    "QualityGuardianDependencies",
    "QualityGuardianSettings",
    "load_settings"
]

__version__ = "1.0.0"
__author__ = "Archon AI Agent Factory"
