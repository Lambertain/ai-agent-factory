"""
Universal Quality Validator Agent

Универсальный агент для валидации и контроля качества различных типов проектов
с поддержкой множественных стандартов, автоматизированных проверок и отчетности.
"""

from .agent import universal_quality_validator_agent
from .dependencies import (
    QualityValidatorDependencies,
    QualityStandard,
    ValidationLevel,
    ProjectDomain,
    QualityMetrics,
    CodeQualityRules,
    SecurityValidation,
    PerformanceValidation,
    ComplianceValidation,
    TestingConfiguration,
    DocumentationValidation,
    QualityGates,
    ReportingSettings,
    AutomationSettings
)
from .tools import (
    validate_code_quality,
    run_security_scan,
    perform_performance_tests,
    check_compliance,
    generate_quality_report,
    validate_documentation,
    run_automated_tests,
    check_quality_gates
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"

__all__ = [
    "universal_quality_validator_agent",
    "QualityValidatorDependencies",
    "QualityStandard",
    "ValidationLevel",
    "ProjectDomain",
    "QualityMetrics",
    "CodeQualityRules",
    "SecurityValidation",
    "PerformanceValidation",
    "ComplianceValidation",
    "TestingConfiguration",
    "DocumentationValidation",
    "QualityGates",
    "ReportingSettings",
    "AutomationSettings",
    "validate_code_quality",
    "run_security_scan",
    "perform_performance_tests",
    "check_compliance",
    "generate_quality_report",
    "validate_documentation",
    "run_automated_tests",
    "check_quality_gates"
]