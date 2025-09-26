"""
Security Audit Agent configuration for Enterprise projects.

This configuration is optimized for large-scale enterprise applications with
strict compliance requirements, complex architectures, and high security standards.
"""

from ..dependencies import SecurityAuditDependencies
from ..prompts import get_security_system_prompt


def get_enterprise_security_config(
    project_path: str,
    archon_project_id: str = None
) -> SecurityAuditDependencies:
    """
    Configure Security Audit Agent for enterprise projects.

    Args:
        project_path: Path to the enterprise project
        archon_project_id: Archon project ID for task management

    Returns:
        SecurityAuditDependencies configured for enterprise security
    """
    return SecurityAuditDependencies(
        # Basic configuration
        project_path=project_path,
        domain_type="web_application",
        security_focus="enterprise",

        # Enterprise compliance requirements
        compliance_requirements={
            "sox": True,          # Sarbanes-Oxley Act
            "gdpr": True,         # EU privacy regulation
            "hipaa": True,        # Healthcare compliance
            "pci_dss": True,      # Payment card security
            "iso27001": True,     # Information security standard
            "nist": True,         # NIST Cybersecurity Framework
            "owasp": True,        # OWASP Top 10
            "fedramp": False      # Federal compliance (if applicable)
        },

        # High-priority enterprise security areas
        priority_checks=[
            "identity_access_management",
            "data_loss_prevention",
            "audit_logging",
            "encryption_at_rest",
            "encryption_in_transit",
            "privilege_escalation",
            "supply_chain_security",
            "insider_threat_detection",
            "compliance_monitoring"
        ],

        # Enterprise threat model
        threat_model={
            "insider_threats": "critical",
            "advanced_persistent_threats": "critical",
            "data_exfiltration": "critical",
            "supply_chain_attacks": "high",
            "privilege_escalation": "high",
            "compliance_violations": "high"
        },

        # Comprehensive scanning for enterprise
        scan_config={
            "deep_scan": True,
            "dependency_scan": True,
            "secrets_scan": True,
            "compliance_scan": True,
            "threat_modeling": True,
            "penetration_testing": True,
            "code_review": True,
            "architecture_review": True
        },

        # Knowledge base tags for enterprise security
        knowledge_tags=[
            "security-audit",
            "agent-knowledge",
            "pydantic-ai",
            "enterprise-security",
            "compliance",
            "governance",
            "risk-management",
            "sox",
            "gdpr",
            "iso27001"
        ],
        knowledge_domain="enterprise.security",

        # Archon integration
        archon_project_id=archon_project_id,
        archon_url="http://localhost:3737"
    )


def get_enterprise_system_prompt() -> str:
    """Get optimized system prompt for enterprise security auditing."""
    return get_security_system_prompt(
        domain_type="web_application",
        project_type="enterprise"
    )


# Enterprise specific security patterns
ENTERPRISE_SECURITY_PATTERNS = {
    "privileged_access": [
        r"admin.*password.*hardcoded",
        r"root.*access.*unrestricted",
        r"sudo.*without.*password",
        r"service.*account.*overprivileged",
        r"break.*glass.*access.*unmonitored"
    ],
    "data_protection": [
        r"pii.*unencrypted",
        r"sensitive.*data.*logged",
        r"backup.*unencrypted",
        r"data.*retention.*policy.*missing",
        r"cross.*border.*data.*transfer"
    ],
    "audit_compliance": [
        r"audit.*log.*disabled",
        r"security.*event.*not.*logged",
        r"log.*retention.*insufficient",
        r"privileged.*operation.*unlogged",
        r"compliance.*control.*missing"
    ],
    "architecture_security": [
        r"security.*by.*obscurity",
        r"single.*point.*of.*failure",
        r"trust.*boundary.*violation",
        r"defense.*in.*depth.*missing",
        r"zero.*trust.*not.*implemented"
    ]
}

# Enterprise compliance mappings
ENTERPRISE_COMPLIANCE_MAPPINGS = {
    "sox": {
        "section_302": "financial_reporting_controls",
        "section_404": "internal_controls",
        "section_409": "real_time_disclosure",
        "section_906": "ceo_cfo_certification"
    },
    "nist": {
        "identify": "asset_management",
        "protect": "access_control",
        "detect": "security_monitoring",
        "respond": "incident_response",
        "recover": "business_continuity"
    },
    "iso27001": {
        "a5": "information_security_policies",
        "a6": "organization_information_security",
        "a8": "asset_management",
        "a9": "access_control",
        "a12": "operations_security"
    }
}