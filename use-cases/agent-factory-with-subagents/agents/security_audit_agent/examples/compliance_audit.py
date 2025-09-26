"""
Example configuration for Compliance Security Audit.

This configuration sets up the Security Audit Agent for regulatory
compliance auditing (GDPR, HIPAA, PCI-DSS, SOX, ISO27001).
"""

import asyncio
from ..agent import run_security_audit, generate_compliance_report
from ..dependencies import SecurityAuditDependencies


async def audit_gdpr_compliance():
    """Run GDPR compliance security audit."""

    # Configure dependencies for GDPR compliance
    deps = SecurityAuditDependencies(
        project_type="compliance",
        project_path="/path/to/application",
        project_name="Data Processing Application",

        # Focus on privacy and data protection
        security_focus="privacy",
        compliance_frameworks=["gdpr", "iso27001"],

        # Compliance-specific exclusions
        excluded_paths=[
            "test-data",
            "mock-data",
            ".git",
            "node_modules",
            "vendor"
        ],

        # Custom scan preferences
        scan_preferences={
            "scan_type": "gdpr-focused",
            "check_data_processing": True,
            "check_consent_mechanisms": True,
            "check_data_portability": True,
            "check_right_to_erasure": True,
            "focus_areas": [
                "pii-detection",
                "data-minimization",
                "consent-management",
                "data-portability",
                "encryption-at-rest",
                "encryption-in-transit",
                "audit-logging",
                "breach-notification"
            ],
            "gdpr_requirements": {
                "lawful_basis": True,
                "data_subject_rights": True,
                "privacy_by_design": True,
                "dpo_requirements": True,
                "cross_border_transfers": True
            }
        }
    )

    # Generate GDPR compliance report
    results = await generate_compliance_report(
        target_path=deps.project_path,
        frameworks=["gdpr"],
        session_id="gdpr-audit-001"
    )

    return results


async def audit_hipaa_compliance():
    """Run HIPAA compliance security audit."""

    # Configure for HIPAA compliance
    deps = SecurityAuditDependencies(
        project_type="compliance",
        project_path="/path/to/healthcare/app",
        project_name="Healthcare Management System",

        security_focus="comprehensive",
        compliance_frameworks=["hipaa", "iso27001"],

        scan_preferences={
            "scan_type": "hipaa-focused",
            "check_phi_handling": True,
            "check_access_controls": True,
            "check_audit_logs": True,
            "focus_areas": [
                "phi-protection",
                "access-control",
                "audit-logging",
                "encryption",
                "backup-recovery",
                "incident-response",
                "workforce-training",
                "business-associate-agreements"
            ],
            "hipaa_safeguards": {
                "administrative": True,
                "physical": True,
                "technical": True
            }
        }
    )

    # Generate HIPAA compliance report
    results = await generate_compliance_report(
        target_path=deps.project_path,
        frameworks=["hipaa"],
        session_id="hipaa-audit-001"
    )

    return results


async def audit_pci_dss_compliance():
    """Run PCI-DSS compliance security audit."""

    # Configure for PCI-DSS compliance
    deps = SecurityAuditDependencies(
        project_type="compliance",
        project_path="/path/to/payment/system",
        project_name="Payment Processing System",

        security_focus="comprehensive",
        compliance_frameworks=["pci-dss", "owasp-top10"],

        scan_preferences={
            "scan_type": "pci-dss-focused",
            "check_cardholder_data": True,
            "check_network_segmentation": True,
            "check_vulnerability_management": True,
            "focus_areas": [
                "cardholder-data-protection",
                "strong-access-controls",
                "vulnerability-management",
                "secure-networks",
                "information-security-policy",
                "regular-monitoring"
            ],
            "pci_requirements": {
                "firewall_configuration": True,
                "default_passwords": True,
                "cardholder_data_protection": True,
                "encrypted_transmission": True,
                "antivirus_software": True,
                "secure_systems": True,
                "access_control": True,
                "unique_ids": True,
                "physical_access": True,
                "network_monitoring": True,
                "security_testing": True,
                "security_policy": True
            }
        }
    )

    # Generate PCI-DSS compliance report
    results = await generate_compliance_report(
        target_path=deps.project_path,
        frameworks=["pci_dss"],
        session_id="pci-audit-001"
    )

    return results


async def audit_sox_compliance():
    """Run SOX compliance security audit."""

    # Configure for SOX compliance
    deps = SecurityAuditDependencies(
        project_type="compliance",
        project_path="/path/to/financial/system",
        project_name="Financial Reporting System",

        security_focus="comprehensive",
        compliance_frameworks=["sox", "iso27001"],

        scan_preferences={
            "scan_type": "sox-focused",
            "check_financial_controls": True,
            "check_audit_trails": True,
            "check_segregation_duties": True,
            "focus_areas": [
                "internal-controls",
                "financial-reporting",
                "audit-trails",
                "segregation-of-duties",
                "change-management",
                "access-controls",
                "data-integrity"
            ],
            "sox_controls": {
                "entity_level": True,
                "activity_level": True,
                "it_general": True,
                "application": True
            }
        }
    )

    # Generate SOX compliance report
    results = await generate_compliance_report(
        target_path=deps.project_path,
        frameworks=["sox"],
        session_id="sox-audit-001"
    )

    return results


async def comprehensive_compliance_audit():
    """Run comprehensive multi-framework compliance audit."""

    # Configure for multiple compliance frameworks
    deps = SecurityAuditDependencies(
        project_type="compliance",
        project_path="/path/to/enterprise/system",
        project_name="Enterprise Multi-Compliance System",

        security_focus="comprehensive",
        compliance_frameworks=["gdpr", "hipaa", "pci-dss", "sox", "iso27001"],

        scan_preferences={
            "scan_type": "multi-compliance",
            "comprehensive_coverage": True,
            "focus_areas": [
                "data-protection",
                "access-control",
                "audit-logging",
                "encryption",
                "incident-response",
                "risk-management",
                "business-continuity"
            ]
        }
    )

    # Generate comprehensive compliance report
    results = await generate_compliance_report(
        target_path=deps.project_path,
        frameworks=["gdpr", "hipaa", "pci_dss", "sox"],
        session_id="comprehensive-audit-001"
    )

    return results


# Example usage patterns
async def main():
    """Example usage of compliance security audit."""

    print("📋 Starting Compliance Security Audit...")

    # GDPR compliance audit
    print("\n🇪🇺 Auditing GDPR Compliance...")
    gdpr_results = await audit_gdpr_compliance()
    print(f"✅ GDPR audit complete: {gdpr_results.get('compliance_status', {}).get('gdpr', 'unknown')}")

    # HIPAA compliance audit
    print("\n🏥 Auditing HIPAA Compliance...")
    hipaa_results = await audit_hipaa_compliance()
    print(f"✅ HIPAA audit complete: {hipaa_results.get('compliance_status', {}).get('hipaa', 'unknown')}")

    # PCI-DSS compliance audit
    print("\n💳 Auditing PCI-DSS Compliance...")
    pci_results = await audit_pci_dss_compliance()
    print(f"✅ PCI-DSS audit complete: {pci_results.get('compliance_status', {}).get('pci_dss', 'unknown')}")

    # SOX compliance audit
    print("\n📊 Auditing SOX Compliance...")
    sox_results = await audit_sox_compliance()
    print(f"✅ SOX audit complete: {sox_results.get('compliance_status', {}).get('sox', 'unknown')}")

    # Comprehensive audit
    print("\n🏢 Running Comprehensive Compliance Audit...")
    comprehensive_results = await comprehensive_compliance_audit()
    compliance_summary = comprehensive_results.get('compliance_status', {})

    print("\n📋 Compliance Summary:")
    frameworks = ["gdpr", "hipaa", "pci_dss", "sox"]
    for framework in frameworks:
        status = compliance_summary.get(framework, 'not-assessed')
        emoji = "✅" if status == "compliant" else "❌" if status == "non-compliant" else "⚠️"
        print(f"  {emoji} {framework.upper()}: {status}")

    # Risk assessment
    high_risk_areas = [
        "Data encryption",
        "Access controls",
        "Audit logging",
        "Incident response",
        "Regular monitoring"
    ]

    print("\n🎯 High-Risk Areas Assessment:")
    for area in high_risk_areas:
        # Simulate assessment based on results
        status = "✅" if "compliant" in str(comprehensive_results).lower() else "⚠️"
        print(f"  {status} {area}")


if __name__ == "__main__":
    asyncio.run(main())