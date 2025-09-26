"""
Example configuration for API Security Audit.

This configuration sets up the Security Audit Agent for REST API
and GraphQL endpoint security testing.
"""

import asyncio
from ..agent import run_security_audit, run_focused_scan
from ..dependencies import SecurityAuditDependencies


async def audit_api_service():
    """Run security audit for API service."""

    # Configure dependencies for API security
    deps = SecurityAuditDependencies(
        project_type="api",
        project_path="/path/to/api/service",
        project_name="Payment Processing API",

        # Focus on API-specific security
        security_focus="comprehensive",
        compliance_frameworks=["owasp-api-top10", "pci-dss"],

        # API-specific exclusions
        excluded_paths=[
            "tests",
            "docs",
            ".git",
            "swagger-ui",
            "postman-collections"
        ],

        # Custom scan preferences
        scan_preferences={
            "scan_type": "api-focused",
            "include_dependencies": True,
            "check_authentication": True,
            "check_rate_limiting": True,
            "check_input_validation": True,
            "focus_areas": [
                "broken-authentication",
                "excessive-data-exposure",
                "lack-of-resources-rate-limiting",
                "broken-authorization",
                "security-misconfiguration",
                "injection",
                "improper-asset-management"
            ],
            "api_specifications": [
                "openapi.json",
                "swagger.yaml"
            ]
        }
    )

    # Run the security audit
    results = await run_security_audit(
        target_path=deps.project_path,
        scan_type="comprehensive",
        session_id="api-audit-001"
    )

    return results


async def audit_graphql_api():
    """Run specialized GraphQL API security audit."""

    # GraphQL-specific configuration
    deps = SecurityAuditDependencies(
        project_type="api",
        project_path="/path/to/graphql/api",
        project_name="GraphQL Data API",

        security_focus="comprehensive",
        compliance_frameworks=["owasp-api-top10"],

        scan_preferences={
            "scan_type": "graphql-focused",
            "graphql_endpoint": "/graphql",
            "check_introspection": True,
            "check_depth_limiting": True,
            "check_query_complexity": True,
            "focus_areas": [
                "introspection-exposure",
                "query-depth-attacks",
                "resource-exhaustion",
                "injection",
                "broken-authorization"
            ]
        }
    )

    # Run focused GraphQL scan
    results = await run_focused_scan(
        target_path=deps.project_path,
        focus_areas=["graphql-security", "api-authorization"],
        session_id="graphql-audit-001"
    )

    return results


# Example usage patterns
async def main():
    """Example usage of API security audit."""

    print("🔒 Starting API Security Audit...")

    # REST API audit
    print("\n📡 Auditing REST API...")
    rest_results = await audit_api_service()
    print(f"✅ REST API audit complete: {rest_results['scan_summary'].get('status')}")

    # GraphQL API audit
    print("\n🔮 Auditing GraphQL API...")
    graphql_results = await audit_graphql_api()
    print(f"✅ GraphQL audit complete: {len(graphql_results.get('results', []))} issues found")

    # Check for authentication issues
    auth_issues = [
        issue for issue in rest_results.get('agent_response', '').split('\n')
        if 'auth' in issue.lower()
    ]
    if auth_issues:
        print("\n⚠️ Authentication Issues Found:")
        for issue in auth_issues[:3]:
            print(f"  • {issue}")


if __name__ == "__main__":
    asyncio.run(main())