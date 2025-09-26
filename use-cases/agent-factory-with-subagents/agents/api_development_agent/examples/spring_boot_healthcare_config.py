"""
Spring Boot Healthcare API Configuration Example.

Example configuration for building a healthcare management API using Spring Boot,
including patient records, HIPAA compliance, telemedicine features, and medical data security.
"""

import asyncio
from ..agent import api_development_agent
from ..dependencies import APIAgentDependencies


async def spring_boot_healthcare_example():
    """Spring Boot healthcare API development example."""

    # Configure dependencies for Spring Boot healthcare API
    deps = APIAgentDependencies(
        # Core settings
        api_key="your_llm_api_key",
        project_path="/path/to/healthcare/api",
        project_name="Healthcare Spring Boot API",

        # Framework configuration
        framework_type="spring-boot",
        api_type="rest",
        domain_type="healthcare",

        # Healthcare architecture patterns
        architecture_pattern="hexagonal",
        auth_strategy="oauth2",
        data_validation="annotation",

        # Healthcare performance requirements
        caching_strategy="redis",
        rate_limiting=True,
        cors_enabled=True,
        compression_enabled=True,

        # Healthcare documentation and testing
        documentation_type="openapi",
        testing_framework="junit",
        api_versioning="header",

        # Healthcare database configuration
        database_type="postgresql",
        orm_framework="hibernate",

        # Java configuration
        typescript_enabled=False,
        hot_reload=True,
        environment="development",

        # Healthcare security middleware stack
        middleware_stack=[
            "security",
            "cors",
            "actuator",
            "logging",
            "audit",
            "encryption"
        ],

        # HIPAA compliance security requirements
        security_headers=True,
        input_sanitization=True,
        sql_injection_protection=True,
        xss_protection=True,

        # Healthcare business logic patterns
        business_logic_patterns=[
            "service-layer",
            "repository-pattern",
            "factory-pattern",
            "strategy-pattern",
            "audit-pattern"
        ],

        # Advanced healthcare features
        advanced_config={
            "hipaa_compliance": True,
            "phi_encryption": True,
            "audit_logging": "comprehensive",
            "access_controls": "role-based",
            "patient_consent": True,
            "data_anonymization": True,
            "hl7_fhir": "r4",
            "dicom_support": True,
            "ehr_integration": ["epic", "cerner"],
            "telemedicine": True,
            "appointment_scheduling": True,
            "prescription_management": True,
            "lab_results": True,
            "medical_imaging": True,
            "clinical_decision_support": True,
            "population_health": True,
            "quality_measures": True,
            "icd_10_codes": True,
            "cpt_codes": True,
            "drug_interaction_checking": True,
            "allergy_alerts": True,
            "emergency_access": True,
            "data_backup": "encrypted",
            "disaster_recovery": True,
            "uptime_requirement": "99.9%",
            "response_time": "<200ms",
            "concurrent_users": 10000,
            "data_retention": "legal-requirements",
            "gdpr_compliance": True,
            "breach_notification": "automatic"
        },

        # RAG configuration
        knowledge_tags=["spring-boot", "healthcare", "api-development", "hipaa", "medical"],
        knowledge_domain="spring.io/projects/spring-boot",
        archon_project_id="spring-healthcare-api"
    )

    print("🏥 Создание Spring Boot Healthcare API...")

    # 1. Validate HIPAA compliance configuration
    print("\n1. Валидация HIPAA compliance конфигурации...")
    result = await api_development_agent.run(
        user_prompt="Validate the current Spring Boot configuration for HIPAA compliance including data encryption, audit logging, access controls, and healthcare-specific security requirements.",
        deps=deps
    )
    print(f"Результат валидации: {result.data}")

    # 2. Create secure patient management system
    print("\n2. Создание secure patient management системы...")
    result = await api_development_agent.run(
        user_prompt="Create secure patient management system with Spring Boot including patient registration, medical records, demographics, emergency contacts, and HIPAA-compliant data handling.",
        deps=deps
    )
    print(f"Patient management: {result.data}")

    # 3. Create electronic health records (EHR) system
    print("\n3. Создание electronic health records (EHR) системы...")
    result = await api_development_agent.run(
        user_prompt="Create comprehensive EHR system with HL7 FHIR R4 compliance including medical history, diagnoses, treatments, medications, allergies, and clinical notes with proper versioning.",
        deps=deps
    )
    print(f"EHR system: {result.data}")

    # 4. Create appointment scheduling system
    print("\n4. Создание appointment scheduling системы...")
    result = await api_development_agent.run(
        user_prompt="Create appointment scheduling system with provider availability, patient booking, reminder notifications, cancellation handling, and integration with calendar systems.",
        deps=deps
    )
    print(f"Appointment scheduling: {result.data}")

    # 5. Create prescription management system
    print("\n5. Создание prescription management системы...")
    result = await api_development_agent.run(
        user_prompt="Create prescription management system with drug interaction checking, allergy alerts, dosage calculations, pharmacy integration, and electronic prescribing (e-prescribing) capabilities.",
        deps=deps
    )
    print(f"Prescription management: {result.data}")

    # 6. Create telemedicine platform
    print("\n6. Создание telemedicine платформы...")
    result = await api_development_agent.run(
        user_prompt="Create telemedicine platform API with video consultation scheduling, secure messaging, document sharing, virtual waiting rooms, and integration with EHR systems.",
        deps=deps
    )
    print(f"Telemedicine platform: {result.data}")

    # 7. Create lab results management
    print("\n7. Создание lab results management...")
    result = await api_development_agent.run(
        user_prompt="Create lab results management system with test ordering, result processing, normal/abnormal flagging, provider notifications, and patient portal access with appropriate permissions.",
        deps=deps
    )
    print(f"Lab results system: {result.data}")

    # 8. Create medical imaging system
    print("\n8. Создание medical imaging системы...")
    result = await api_development_agent.run(
        user_prompt="Create medical imaging system with DICOM support, image storage, viewer integration, radiologist reporting, and secure image sharing between healthcare providers.",
        deps=deps
    )
    print(f"Medical imaging system: {result.data}")

    # 9. Create clinical decision support
    print("\n9. Создание clinical decision support...")
    result = await api_development_agent.run(
        user_prompt="Create clinical decision support system with evidence-based guidelines, alert systems, drug interaction warnings, and integration with clinical workflows for improved patient care.",
        deps=deps
    )
    print(f"Clinical decision support: {result.data}")

    # 10. Create audit and compliance system
    print("\n10. Создание audit и compliance системы...")
    result = await api_development_agent.run(
        user_prompt="Create comprehensive audit and compliance system for HIPAA requirements including access logging, data modification tracking, breach detection, and compliance reporting.",
        deps=deps
    )
    print(f"Audit system: {result.data}")

    # 11. Create security and access control
    print("\n11. Создание security и access control...")
    result = await api_development_agent.run(
        user_prompt="Create robust security and access control system with Spring Security including role-based access, multi-factor authentication, session management, and PHI protection.",
        deps=deps
    )
    print(f"Security system: {result.data}")

    # 12. Generate healthcare API documentation
    print("\n12. Генерация healthcare API документации...")
    endpoints_config = [
        {"path": "/api/v1/auth/oauth2", "method": "POST", "description": "OAuth2 authentication for healthcare providers"},
        {"path": "/api/v1/patients", "method": "GET", "description": "Get patient list (with proper authorization)"},
        {"path": "/api/v1/patients/{id}", "method": "GET", "description": "Get patient details"},
        {"path": "/api/v1/patients/{id}/records", "method": "GET", "description": "Get patient medical records"},
        {"path": "/api/v1/appointments", "method": "POST", "description": "Schedule appointment"},
        {"path": "/api/v1/prescriptions", "method": "POST", "description": "Create prescription"},
        {"path": "/api/v1/lab-results", "method": "GET", "description": "Get lab results"},
        {"path": "/api/v1/imaging", "method": "GET", "description": "Get medical imaging"},
        {"path": "/api/v1/telemedicine/session", "method": "POST", "description": "Start telemedicine session"},
        {"path": "/api/v1/fhir/Patient", "method": "GET", "description": "FHIR Patient resource"},
        {"path": "/api/v1/audit/logs", "method": "GET", "description": "Get audit logs (admin only)"}
    ]

    result = await api_development_agent.run(
        user_prompt=f"Generate comprehensive healthcare API documentation with OpenAPI 3.0 for these endpoints: {endpoints_config}. Include HIPAA compliance annotations, security requirements, and healthcare-specific data models.",
        deps=deps
    )
    print(f"Healthcare API Documentation: {result.data}")

    # 13. Generate security tests
    print("\n13. Создание security тестов...")
    result = await api_development_agent.run(
        user_prompt="Generate comprehensive security test suite for healthcare API including HIPAA compliance tests, PHI protection tests, access control validation, and penetration testing scenarios.",
        deps=deps
    )
    print(f"Security test suite: {result.data}")

    # 14. Generate deployment configuration
    print("\n14. Создание secure deployment конфигурации...")
    result = await api_development_agent.run(
        user_prompt="Generate secure deployment configuration for healthcare API including Docker security hardening, Kubernetes HIPAA-compliant setup, encrypted storage, network security, and monitoring.",
        deps=deps
    )
    print(f"Secure deployment config: {result.data}")

    print("\n✅ Spring Boot Healthcare API создан успешно!")
    print(f"📁 Проект: {deps.project_name}")
    print(f"🚀 Фреймворк: {deps.framework_type}")
    print(f"🏥 Домен: {deps.domain_type}")
    print(f"🔐 Аутентификация: {deps.auth_strategy}")
    print(f"🏗️ Архитектура: {deps.architecture_pattern}")
    print(f"🛡️ HIPAA Compliance: {deps.advanced_config.get('hipaa_compliance', 'Yes')}")
    print(f"📊 HL7 FHIR: {deps.advanced_config.get('hl7_fhir', 'R4')}")
    print(f"🎯 Uptime: {deps.advanced_config.get('uptime_requirement', '99.9%')}")

    return deps


if __name__ == "__main__":
    asyncio.run(spring_boot_healthcare_example())