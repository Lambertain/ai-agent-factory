"""
Example configuration for Infrastructure Security Audit.

This configuration sets up the Security Audit Agent for cloud infrastructure,
containers, and Infrastructure as Code (IaC) security testing.
"""

import asyncio
from ..agent import run_security_audit, run_focused_scan
from ..dependencies import SecurityAuditDependencies


async def audit_cloud_infrastructure():
    """Run security audit for cloud infrastructure (AWS/Azure/GCP)."""

    # Configure dependencies for cloud infrastructure
    deps = SecurityAuditDependencies(
        project_type="infrastructure",
        project_path="/path/to/infrastructure/code",
        project_name="Production Cloud Environment",

        # Focus on infrastructure security
        security_focus="infrastructure",
        compliance_frameworks=["cis-benchmarks", "iso27001", "pci-dss"],

        # Infrastructure-specific exclusions
        excluded_paths=[
            ".terraform",
            ".git",
            "*.tfstate",
            "*.tfstate.backup",
            ".terragrunt-cache"
        ],

        # Custom scan preferences
        scan_preferences={
            "scan_type": "infrastructure-focused",
            "cloud_provider": "aws",  # aws, azure, gcp
            "check_iac": True,
            "check_containers": True,
            "check_kubernetes": True,
            "focus_areas": [
                "public-exposure",
                "overly-permissive-policies",
                "unencrypted-storage",
                "missing-monitoring",
                "network-segmentation",
                "access-control",
                "secrets-in-code"
            ],
            "infrastructure_checks": {
                "s3_public_access": True,
                "security_groups": True,
                "iam_policies": True,
                "encryption_at_rest": True,
                "vpc_configuration": True,
                "logging_enabled": True
            }
        }
    )

    # Run the security audit
    results = await run_security_audit(
        target_path=deps.project_path,
        scan_type="comprehensive",
        session_id="infra-audit-001"
    )

    return results


async def audit_kubernetes_cluster():
    """Run security audit for Kubernetes cluster configuration."""

    # Configure for Kubernetes security
    deps = SecurityAuditDependencies(
        project_type="infrastructure",
        project_path="/path/to/k8s/manifests",
        project_name="Production Kubernetes Cluster",

        security_focus="comprehensive",
        compliance_frameworks=["cis-benchmarks", "nist"],

        scan_preferences={
            "scan_type": "kubernetes-focused",
            "k8s_version": "1.28",
            "focus_areas": [
                "rbac-configuration",
                "pod-security-policies",
                "network-policies",
                "secrets-management",
                "container-images",
                "admission-controllers"
            ],
            "kubernetes_checks": {
                "check_rbac": True,
                "check_pod_security": True,
                "check_network_policies": True,
                "check_resource_limits": True,
                "check_image_vulnerabilities": True
            }
        }
    )

    # Run focused Kubernetes scan
    results = await run_focused_scan(
        target_path=deps.project_path,
        focus_areas=["kubernetes-security", "container-security"],
        session_id="k8s-audit-001"
    )

    return results


async def audit_terraform_code():
    """Run security audit for Terraform Infrastructure as Code."""

    # Configure for Terraform/IaC security
    deps = SecurityAuditDependencies(
        project_type="infrastructure",
        project_path="/path/to/terraform/modules",
        project_name="Infrastructure as Code",

        security_focus="comprehensive",
        compliance_frameworks=["cis-benchmarks"],

        scan_preferences={
            "scan_type": "iac-focused",
            "iac_tool": "terraform",
            "terraform_version": "1.5.0",
            "focus_areas": [
                "hardcoded-secrets",
                "insecure-defaults",
                "public-resources",
                "missing-encryption",
                "overly-permissive-access"
            ],
            "terraform_checks": {
                "check_variables": True,
                "check_outputs": True,
                "check_modules": True,
                "check_provider_configs": True
            }
        }
    )

    # Run the security audit
    results = await run_security_audit(
        target_path=deps.project_path,
        scan_type="comprehensive",
        session_id="terraform-audit-001"
    )

    return results


async def audit_docker_containers():
    """Run security audit for Docker containers and images."""

    # Configure for container security
    deps = SecurityAuditDependencies(
        project_type="infrastructure",
        project_path="/path/to/docker/files",
        project_name="Container Infrastructure",

        security_focus="comprehensive",
        compliance_frameworks=["cis-benchmarks"],

        scan_preferences={
            "scan_type": "container-focused",
            "container_runtime": "docker",
            "focus_areas": [
                "vulnerable-base-images",
                "exposed-secrets",
                "insecure-dockerfile",
                "root-user",
                "unnecessary-packages"
            ],
            "docker_checks": {
                "scan_images": True,
                "check_dockerfile": True,
                "check_compose": True,
                "check_registry": True
            }
        }
    )

    results = await run_security_audit(
        target_path=deps.project_path,
        scan_type="comprehensive",
        session_id="docker-audit-001"
    )

    return results


# Example usage patterns
async def main():
    """Example usage of infrastructure security audit."""

    print("🏗️ Starting Infrastructure Security Audit...")

    # Cloud infrastructure audit
    print("\n☁️ Auditing Cloud Infrastructure...")
    cloud_results = await audit_cloud_infrastructure()
    print(f"✅ Cloud audit complete: {cloud_results['scan_summary'].get('status')}")

    # Kubernetes audit
    print("\n⚓ Auditing Kubernetes Cluster...")
    k8s_results = await audit_kubernetes_cluster()
    print(f"✅ K8s audit complete: {len(k8s_results.get('results', []))} issues found")

    # Terraform audit
    print("\n📝 Auditing Terraform Code...")
    terraform_results = await audit_terraform_code()
    print(f"✅ Terraform audit complete: {terraform_results['scan_summary'].get('status')}")

    # Docker audit
    print("\n🐳 Auditing Docker Containers...")
    docker_results = await audit_docker_containers()
    print(f"✅ Docker audit complete: {docker_results['scan_summary'].get('status')}")

    # Infrastructure security checklist
    print("\n📋 Infrastructure Security Summary:")
    checks = [
        ("Public S3 buckets", cloud_results),
        ("Exposed databases", cloud_results),
        ("Hardcoded secrets", terraform_results),
        ("Vulnerable images", docker_results),
        ("RBAC issues", k8s_results)
    ]

    for check_name, results in checks:
        found = check_name.lower() in str(results).lower()
        status = "❌ Found" if found else "✅ Clear"
        print(f"  {status}: {check_name}")


if __name__ == "__main__":
    asyncio.run(main())