"""
Security Audit Agent configuration for E-commerce projects.

This configuration is optimized for online retail applications with payment processing,
user authentication, and sensitive customer data handling.
"""

from ..dependencies import SecurityAuditDependencies
from ..prompts import get_security_system_prompt


def get_ecommerce_security_config(
    project_path: str,
    archon_project_id: str = None
) -> SecurityAuditDependencies:
    """
    Configure Security Audit Agent for e-commerce projects.

    Args:
        project_path: Path to the e-commerce project
        archon_project_id: Archon project ID for task management

    Returns:
        SecurityAuditDependencies configured for e-commerce security
    """
    return SecurityAuditDependencies(
        # Basic configuration
        project_path=project_path,
        domain_type="web_application",
        security_focus="ecommerce",

        # E-commerce specific settings
        compliance_requirements={
            "pci_dss": True,      # Payment Card Industry compliance
            "gdpr": True,         # EU privacy regulation
            "ccpa": True,         # California privacy law
            "owasp": True,        # OWASP Top 10
            "iso27001": False     # Optional for enterprises
        },

        # High-priority security areas for e-commerce
        priority_checks=[
            "payment_security",
            "customer_data_protection",
            "authentication_security",
            "session_management",
            "input_validation",
            "sql_injection",
            "xss_protection",
            "csrf_protection"
        ],

        # E-commerce threat model
        threat_model={
            "payment_fraud": "critical",
            "data_breaches": "critical",
            "account_takeover": "high",
            "injection_attacks": "high",
            "business_logic_flaws": "medium"
        },

        # Scanning configuration
        scan_config={
            "deep_scan": True,
            "dependency_scan": True,
            "secrets_scan": True,
            "compliance_scan": True,
            "performance_security": False  # Delegate to Performance Agent
        },

        # Knowledge base tags for e-commerce security
        knowledge_tags=[
            "security-audit",
            "agent-knowledge",
            "pydantic-ai",
            "ecommerce-security",
            "payment-security",
            "pci-dss",
            "customer-data",
            "web-application"
        ],
        knowledge_domain="ecommerce.security",

        # Archon integration
        archon_project_id=archon_project_id,
        archon_url="http://localhost:3737"
    )


def get_ecommerce_system_prompt() -> str:
    """Get optimized system prompt for e-commerce security auditing."""
    return get_security_system_prompt(
        domain_type="web_application",
        project_type="ecommerce"
    )


# E-commerce specific security checks configuration
ECOMMERCE_SECURITY_PATTERNS = {
    "payment_vulnerabilities": [
        r"hardcoded.*api.*key",
        r"stripe.*secret",
        r"paypal.*token",
        r"payment.*debug.*true",
        r"test.*credit.*card"
    ],
    "customer_data_exposure": [
        r"customer.*password.*plain",
        r"email.*address.*log",
        r"credit.*card.*number",
        r"ssn.*social.*security",
        r"personal.*info.*debug"
    ],
    "session_vulnerabilities": [
        r"session.*cookie.*insecure",
        r"remember.*me.*forever",
        r"auth.*token.*localStorage",
        r"csrf.*disabled",
        r"cors.*origin.*\*"
    ]
}

# E-commerce security compliance mappings
ECOMMERCE_COMPLIANCE_MAPPINGS = {
    "pci_dss": {
        "requirement_1": "firewall_configuration",
        "requirement_3": "stored_data_protection",
        "requirement_4": "encrypted_transmission",
        "requirement_6": "secure_development",
        "requirement_8": "access_control"
    },
    "gdpr": {
        "article_25": "privacy_by_design",
        "article_32": "security_of_processing",
        "article_35": "data_protection_impact"
    }
}