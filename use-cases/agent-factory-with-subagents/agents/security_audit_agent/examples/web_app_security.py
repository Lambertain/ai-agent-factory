"""
Example configuration for Web Application Security Audit.

This configuration sets up the Security Audit Agent for comprehensive
web application security testing including OWASP Top 10 vulnerabilities.
"""

import asyncio
from ..agent import run_security_audit
from ..dependencies import SecurityAuditDependencies


async def audit_web_application():
    """Run security audit for a web application."""

    # Configure dependencies for web application security
    deps = SecurityAuditDependencies(
        project_type="web-app",
        project_path="/path/to/web/app",
        project_name="E-Commerce Platform",

        # Focus on web-specific security concerns
        security_focus="owasp-top10",
        compliance_frameworks=["owasp-top10", "pci-dss"],

        # Web-specific exclusions
        excluded_paths=[
            "node_modules",
            "dist",
            "build",
            ".git",
            "public/assets",
            "vendor"
        ],

        # Custom scan preferences
        scan_preferences={
            "scan_type": "comprehensive",
            "include_dependencies": True,
            "include_secrets": True,
            "check_ssl": True,
            "check_headers": True,
            "check_cookies": True,
            "focus_areas": [
                "xss",
                "sql-injection",
                "csrf",
                "authentication",
                "session-management",
                "access-control"
            ]
        }
    )

    # Run the security audit
    results = await run_security_audit(
        target_path=deps.project_path,
        scan_type="comprehensive",
        session_id="web-app-audit-001"
    )

    return results


# Example usage patterns
async def main():
    """Example usage of web application security audit."""

    print("🔒 Starting Web Application Security Audit...")

    # Basic web app audit
    results = await audit_web_application()

    print(f"✅ Audit complete. Found {results['scan_summary'].get('total_findings', 0)} issues")

    # Check for critical vulnerabilities
    if results.get('critical_findings'):
        print("🚨 Critical vulnerabilities found:")
        for finding in results['critical_findings']:
            print(f"  - {finding['description']}")

    # Generate recommendations
    if results.get('recommendations'):
        print("\n📋 Recommendations:")
        for rec in results['recommendations'][:5]:
            print(f"  • {rec}")


if __name__ == "__main__":
    asyncio.run(main())