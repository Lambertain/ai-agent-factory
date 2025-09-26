"""Security Audit Agent Package."""

from .agent import (
    security_agent,
    run_security_audit,
    run_focused_scan,
    analyze_security_trends,
    generate_compliance_report,
    perform_threat_modeling
)

from .tools import (
    scan_code_security,
    analyze_code_vulnerabilities,
    check_dependency_vulnerabilities,
    generate_security_report,
    SecurityFinding,
    VulnerabilityReport
)

from .settings import (
    SecurityAuditSettings,
    load_security_settings,
    validate_security_configuration
)

from .dependencies import SecurityAuditDependencies

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Comprehensive security audit agent for code and infrastructure analysis"

__all__ = [
    # Main agent functions
    "security_agent",
    "run_security_audit",
    "run_focused_scan",
    "analyze_security_trends",
    "generate_compliance_report",
    "perform_threat_modeling",

    # Security tools
    "scan_code_security",
    "analyze_code_vulnerabilities",
    "check_dependency_vulnerabilities",
    "generate_security_report",

    # Models
    "SecurityFinding",
    "VulnerabilityReport",

    # Configuration
    "SecurityAuditSettings",
    "load_security_settings",
    "validate_security_configuration",
    "SecurityAuditDependencies"
]