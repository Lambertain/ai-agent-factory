"""
Security Audit Agent configuration for SaaS projects.

This configuration is optimized for Software-as-a-Service applications with
multi-tenancy, API security, and cloud infrastructure considerations.
"""

from ..dependencies import SecurityAuditDependencies
from ..prompts import get_security_system_prompt


def get_saas_security_config(
    project_path: str,
    archon_project_id: str = None
) -> SecurityAuditDependencies:
    """
    Configure Security Audit Agent for SaaS projects.

    Args:
        project_path: Path to the SaaS project
        archon_project_id: Archon project ID for task management

    Returns:
        SecurityAuditDependencies configured for SaaS security
    """
    return SecurityAuditDependencies(
        # Basic configuration
        project_path=project_path,
        domain_type="api",
        security_focus="saas",

        # SaaS specific compliance
        compliance_requirements={
            "soc2": True,         # Service Organization Control 2
            "gdpr": True,         # EU privacy regulation
            "hipaa": False,       # Healthcare (if applicable)
            "owasp": True,        # OWASP Top 10
            "iso27001": True      # Information security management
        },

        # High-priority areas for SaaS
        priority_checks=[
            "multi_tenant_isolation",
            "api_security",
            "authentication_authorization",
            "data_encryption",
            "audit_logging",
            "rate_limiting",
            "input_validation",
            "cloud_security"
        ],

        # SaaS threat model
        threat_model={
            "tenant_isolation_breach": "critical",
            "api_abuse": "high",
            "data_leakage": "critical",
            "ddos_attacks": "medium",
            "insider_threats": "medium"
        },

        # Scanning configuration
        scan_config={
            "deep_scan": True,
            "dependency_scan": True,
            "secrets_scan": True,
            "compliance_scan": True,
            "api_security": True,
            "cloud_config": True
        },

        # Knowledge base tags for SaaS security
        knowledge_tags=[
            "security-audit",
            "agent-knowledge",
            "pydantic-ai",
            "saas-security",
            "api-security",
            "multi-tenant",
            "cloud-security",
            "soc2"
        ],
        knowledge_domain="saas.security",

        # Archon integration
        archon_project_id=archon_project_id,
        archon_url="http://localhost:3737"
    )


def get_saas_system_prompt() -> str:
    """Get optimized system prompt for SaaS security auditing."""
    return get_security_system_prompt(
        domain_type="api",
        project_type="saas"
    )


# SaaS specific security patterns
SAAS_SECURITY_PATTERNS = {
    "multi_tenant_issues": [
        r"tenant.*id.*hardcoded",
        r"where.*tenant.*id.*missing",
        r"global.*admin.*backdoor",
        r"tenant.*isolation.*bypass",
        r"shared.*resource.*unprotected"
    ],
    "api_vulnerabilities": [
        r"api.*key.*exposed",
        r"rate.*limit.*disabled",
        r"cors.*origin.*\*",
        r"auth.*middleware.*missing",
        r"input.*validation.*skipped"
    ],
    "cloud_misconfigurations": [
        r"aws.*secret.*hardcoded",
        r"s3.*bucket.*public",
        r"database.*public.*access",
        r"ssl.*certificate.*expired",
        r"encryption.*disabled"
    ]
}

# SaaS security compliance mappings
SAAS_COMPLIANCE_MAPPINGS = {
    "soc2": {
        "cc6.1": "logical_access_controls",
        "cc6.2": "system_boundaries",
        "cc6.3": "access_removal",
        "cc7.1": "system_boundaries_security",
        "a1.1": "access_controls"
    },
    "iso27001": {
        "a9": "access_control",
        "a10": "cryptography",
        "a12": "operations_security",
        "a13": "communications_security",
        "a14": "system_acquisition"
    }
}