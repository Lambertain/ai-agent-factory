"""
Example configuration for Mobile Application Security Audit.

This configuration sets up the Security Audit Agent for iOS and Android
mobile application security testing.
"""

import asyncio
from ..agent import run_security_audit, perform_threat_modeling
from ..dependencies import SecurityAuditDependencies


async def audit_android_app():
    """Run security audit for Android application."""

    # Configure dependencies for Android app security
    deps = SecurityAuditDependencies(
        project_type="mobile",
        project_path="/path/to/android/app",
        project_name="Banking Mobile App",

        # Focus on mobile-specific security
        security_focus="comprehensive",
        compliance_frameworks=["mobile-owasp-top10", "pci-dss", "gdpr"],

        # Android-specific exclusions
        excluded_paths=[
            "build",
            "gradle",
            ".gradle",
            ".idea",
            ".git",
            "app/build"
        ],

        # Custom scan preferences
        scan_preferences={
            "scan_type": "android-focused",
            "platform": "android",
            "min_sdk_version": 23,
            "target_sdk_version": 33,
            "check_manifest": True,
            "check_permissions": True,
            "check_certificate": True,
            "focus_areas": [
                "insecure-data-storage",
                "insecure-communication",
                "insecure-authentication",
                "insufficient-cryptography",
                "insecure-authorization",
                "client-code-quality",
                "code-tampering",
                "reverse-engineering",
                "extraneous-functionality"
            ],
            "apk_analysis": {
                "decompile": True,
                "check_obfuscation": True,
                "analyze_native_libs": True
            }
        }
    )

    # Run the security audit
    results = await run_security_audit(
        target_path=deps.project_path,
        scan_type="comprehensive",
        session_id="android-audit-001"
    )

    return results


async def audit_ios_app():
    """Run security audit for iOS application."""

    # Configure dependencies for iOS app security
    deps = SecurityAuditDependencies(
        project_type="mobile",
        project_path="/path/to/ios/app",
        project_name="Healthcare iOS App",

        security_focus="privacy",
        compliance_frameworks=["mobile-owasp-top10", "hipaa", "gdpr"],

        # iOS-specific exclusions
        excluded_paths=[
            "Pods",
            "build",
            "DerivedData",
            ".git",
            "*.xcworkspace"
        ],

        scan_preferences={
            "scan_type": "ios-focused",
            "platform": "ios",
            "deployment_target": "14.0",
            "check_info_plist": True,
            "check_entitlements": True,
            "check_ats_settings": True,
            "focus_areas": [
                "keychain-security",
                "biometric-authentication",
                "jailbreak-detection",
                "ssl-pinning",
                "data-protection-api",
                "app-transport-security"
            ],
            "ipa_analysis": {
                "check_encryption": True,
                "analyze_binary": True,
                "check_signing": True
            }
        }
    )

    # Run the security audit
    results = await run_security_audit(
        target_path=deps.project_path,
        scan_type="comprehensive",
        session_id="ios-audit-001"
    )

    return results


async def mobile_threat_modeling():
    """Perform threat modeling for mobile application."""

    deps = SecurityAuditDependencies(
        project_type="mobile",
        project_path="/path/to/mobile/app",
        project_name="Mobile Banking App",
        security_focus="comprehensive",
        compliance_frameworks=["mobile-owasp-top10", "pci-dss"]
    )

    system_description = """
    Mobile banking application with:
    - Biometric authentication (fingerprint/face)
    - Account management and transactions
    - Push notifications for alerts
    - Offline mode with encrypted local storage
    - Certificate pinning for API communication
    """

    # Perform threat modeling
    threats = await perform_threat_modeling(
        target_path=deps.project_path,
        system_description=system_description,
        session_id="mobile-threat-model-001"
    )

    return threats


# Example usage patterns
async def main():
    """Example usage of mobile application security audit."""

    print("📱 Starting Mobile Application Security Audit...")

    # Android app audit
    print("\n🤖 Auditing Android Application...")
    android_results = await audit_android_app()
    print(f"✅ Android audit complete: {android_results['scan_summary'].get('status')}")

    # iOS app audit
    print("\n🍎 Auditing iOS Application...")
    ios_results = await audit_ios_app()
    print(f"✅ iOS audit complete: {ios_results['scan_summary'].get('status')}")

    # Threat modeling
    print("\n🎯 Performing Mobile Threat Modeling...")
    threats = await mobile_threat_modeling()
    print(f"✅ Identified {len(threats.get('threats_identified', []))} potential threats")

    # Display critical mobile-specific issues
    mobile_issues = [
        "Insecure local storage",
        "Missing jailbreak/root detection",
        "Weak encryption",
        "Certificate pinning not implemented"
    ]

    print("\n📋 Mobile Security Checklist:")
    for issue in mobile_issues:
        status = "❌" if issue in str(android_results) else "✅"
        print(f"  {status} {issue}")


if __name__ == "__main__":
    asyncio.run(main())