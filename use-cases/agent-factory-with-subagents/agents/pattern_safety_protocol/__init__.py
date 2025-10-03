"""
Pattern Safety Protocol Agent

Специализированный Pydantic AI агент для обеспечения безопасности пользователей
в рамках системы PatternShift.
"""

from .agent import agent, run_pattern_safety_protocol
from .dependencies import PatternSafetyProtocolDependencies
from .models import (
    RiskLevel,
    RiskCategory,
    ContraindicationType,
    EscalationAction,
    RiskAssessment,
    Contraindication,
    PharmacologicalInteraction,
    CrisisIndicator,
    SafetyProtocol,
    VulnerableGroupProfile,
    SafetyCheckResult
)
from .tools import (
    assess_user_risk,
    check_technique_contraindications,
    check_pharmacological_interactions,
    generate_crisis_response,
    assess_vulnerable_group,
    search_agent_knowledge
)

__version__ = "1.0.0"

__all__ = [
    # Основной агент
    "agent",
    "run_pattern_safety_protocol",

    # Зависимости
    "PatternSafetyProtocolDependencies",

    # Модели данных
    "RiskLevel",
    "RiskCategory",
    "ContraindicationType",
    "EscalationAction",
    "RiskAssessment",
    "Contraindication",
    "PharmacologicalInteraction",
    "CrisisIndicator",
    "SafetyProtocol",
    "VulnerableGroupProfile",
    "SafetyCheckResult",

    # Инструменты
    "assess_user_risk",
    "check_technique_contraindications",
    "check_pharmacological_interactions",
    "generate_crisis_response",
    "assess_vulnerable_group",
    "search_agent_knowledge"
]
