"""
FastAPI Fintech API Configuration Example.

Example configuration for building a fintech API using FastAPI with Python,
including high security, compliance features, and real-time transaction processing.
"""

import asyncio
from ..agent import api_development_agent
from ..dependencies import APIAgentDependencies


async def fastapi_fintech_example():
    """FastAPI fintech API development example."""

    # Configure dependencies for FastAPI fintech API
    deps = APIAgentDependencies(
        # Core settings
        api_key="your_llm_api_key",
        project_path="/path/to/fintech/api",
        project_name="Fintech FastAPI System",

        # Framework configuration
        framework_type="fastapi",
        api_type="rest",
        domain_type="fintech",

        # Fintech architecture patterns
        architecture_pattern="hexagonal",
        auth_strategy="oauth2",
        data_validation="schema",

        # Fintech performance requirements
        caching_strategy="redis",
        rate_limiting=True,
        cors_enabled=True,
        compression_enabled=True,

        # Fintech documentation and testing
        documentation_type="openapi",
        testing_framework="pytest",
        api_versioning="url",

        # Fintech database configuration
        database_type="postgresql",
        orm_framework="sqlalchemy",

        # Python configuration
        typescript_enabled=False,
        hot_reload=True,
        environment="development",

        # Fintech security middleware stack
        middleware_stack=[
            "cors",
            "security-headers",
            "rate-limiting",
            "request-logging",
            "encryption",
            "audit-trail"
        ],

        # High security requirements for fintech
        security_headers=True,
        input_sanitization=True,
        sql_injection_protection=True,
        xss_protection=True,

        # Fintech business logic patterns
        business_logic_patterns=[
            "service-layer",
            "repository-pattern",
            "saga-pattern",
            "event-sourcing",
            "audit-pattern"
        ],

        # Advanced fintech features
        advanced_config={
            "encryption_at_rest": True,
            "encryption_in_transit": True,
            "pci_dss_compliance": True,
            "sox_compliance": True,
            "fraud_detection": "machine-learning",
            "transaction_monitoring": "real-time",
            "kyc_verification": True,
            "aml_screening": True,
            "risk_scoring": True,
            "audit_logging": "comprehensive",
            "data_retention": "7-years",
            "backup_strategy": "continuous",
            "disaster_recovery": True,
            "high_availability": "99.99%",
            "payment_processing": ["stripe", "paypal", "bank-transfer"],
            "currency_support": "multi-currency",
            "exchange_rates": "real-time",
            "regulatory_reporting": True,
            "stress_testing": True,
            "load_balancing": "geographic",
            "cdn": "global",
            "monitoring": "24/7",
            "alerting": "immediate"
        },

        # RAG configuration
        knowledge_tags=["fastapi", "fintech", "api-development", "security", "compliance"],
        knowledge_domain="fastapi.tiangolo.com",
        archon_project_id="fastapi-fintech-api"
    )

    print("💰 Создание FastAPI Fintech API...")

    # 1. Validate fintech compliance configuration
    print("\n1. Валидация fintech compliance конфигурации...")
    result = await api_development_agent.run(
        user_prompt="Validate the current FastAPI configuration for fintech compliance including PCI DSS, SOX requirements, encryption standards, and regulatory compliance.",
        deps=deps
    )
    print(f"Результат валидации: {result.data}")

    # 2. Create secure authentication system
    print("\n2. Создание secure authentication системы...")
    result = await api_development_agent.run(
        user_prompt="Create secure OAuth2 authentication system with JWT tokens, multi-factor authentication (MFA), session management, and compliance with financial regulations. Include password policies and account lockout mechanisms.",
        deps=deps
    )
    print(f"Secure auth system: {result.data}")

    # 3. Create account management API
    print("\n3. Создание account management API...")
    result = await api_development_agent.run(
        user_prompt="Create secure account management endpoints with KYC verification, account creation, balance inquiries, account statements, and fraud detection integration.",
        deps=deps
    )
    print(f"Account management: {result.data}")

    # 4. Create transaction processing system
    print("\n4. Создание transaction processing системы...")
    result = await api_development_agent.run(
        user_prompt="Create high-performance transaction processing system with real-time validation, fraud detection, transaction history, pending transactions, and atomic operations with rollback capability.",
        deps=deps
    )
    print(f"Transaction processing: {result.data}")

    # 5. Create payment gateway integration
    print("\n5. Создание payment gateway интеграции...")
    result = await api_development_agent.run(
        user_prompt="Create secure payment gateway integration supporting multiple providers (Stripe, PayPal), webhook handling, payment validation, and PCI DSS compliant card processing.",
        deps=deps
    )
    print(f"Payment gateway: {result.data}")

    # 6. Create compliance and audit system
    print("\n6. Создание compliance и audit системы...")
    result = await api_development_agent.run(
        user_prompt="Create comprehensive audit and compliance system with transaction logging, regulatory reporting, AML screening, risk assessment, and compliance dashboard.",
        deps=deps
    )
    print(f"Compliance system: {result.data}")

    # 7. Create real-time fraud detection
    print("\n7. Создание real-time fraud detection...")
    result = await api_development_agent.run(
        user_prompt="Create real-time fraud detection system with machine learning integration, risk scoring, transaction monitoring, suspicious activity detection, and automated blocking mechanisms.",
        deps=deps
    )
    print(f"Fraud detection: {result.data}")

    # 8. Create security middleware
    print("\n8. Создание security middleware...")
    result = await api_development_agent.run(
        user_prompt="Create comprehensive security middleware for fintech including encryption/decryption, security headers, rate limiting, input validation, audit logging, and threat detection.",
        deps=deps
    )
    print(f"Security middleware: {result.data}")

    # 9. Create monitoring and alerting
    print("\n9. Создание monitoring и alerting...")
    result = await api_development_agent.run(
        user_prompt="Create comprehensive monitoring and alerting system for fintech operations including transaction monitoring, system health, security alerts, compliance violations, and real-time dashboards.",
        deps=deps
    )
    print(f"Monitoring system: {result.data}")

    # 10. Generate fintech API documentation
    print("\n10. Генерация fintech API документации...")
    endpoints_config = [
        {"path": "/api/v1/auth/oauth2", "method": "POST", "description": "OAuth2 authentication with MFA"},
        {"path": "/api/v1/accounts", "method": "GET", "description": "Get account information"},
        {"path": "/api/v1/accounts/balance", "method": "GET", "description": "Get account balance"},
        {"path": "/api/v1/transactions", "method": "POST", "description": "Create new transaction"},
        {"path": "/api/v1/transactions/history", "method": "GET", "description": "Get transaction history"},
        {"path": "/api/v1/payments/process", "method": "POST", "description": "Process payment"},
        {"path": "/api/v1/kyc/verify", "method": "POST", "description": "KYC verification"},
        {"path": "/api/v1/compliance/report", "method": "GET", "description": "Generate compliance report"},
        {"path": "/api/v1/fraud/check", "method": "POST", "description": "Fraud detection check"}
    ]

    result = await api_development_agent.run(
        user_prompt=f"Generate comprehensive fintech API documentation with OpenAPI 3.0 for these endpoints: {endpoints_config}. Include security requirements, compliance annotations, error responses, and rate limiting information.",
        deps=deps
    )
    print(f"Fintech API Documentation: {result.data}")

    # 11. Generate security tests
    print("\n11. Создание security тестов...")
    result = await api_development_agent.run(
        user_prompt="Generate comprehensive security test suite for fintech API including penetration tests, vulnerability assessments, authentication tests, authorization tests, and compliance validation tests.",
        deps=deps
    )
    print(f"Security test suite: {result.data}")

    # 12. Generate deployment configuration
    print("\n12. Создание secure deployment конфигурации...")
    result = await api_development_agent.run(
        user_prompt="Generate secure deployment configuration for fintech API including Docker security hardening, Kubernetes security policies, secret management, network security, and compliance monitoring.",
        deps=deps
    )
    print(f"Secure deployment config: {result.data}")

    print("\n✅ FastAPI Fintech API создан успешно!")
    print(f"📁 Проект: {deps.project_name}")
    print(f"🚀 Фреймворк: {deps.framework_type}")
    print(f"💰 Домен: {deps.domain_type}")
    print(f"🔐 Аутентификация: {deps.auth_strategy}")
    print(f"🏗️ Архитектура: {deps.architecture_pattern}")
    print(f"🛡️ Безопасность: High-level compliance")
    print(f"📊 Мониторинг: {deps.advanced_config.get('monitoring', '24/7')}")
    print(f"🎯 Availability: {deps.advanced_config.get('high_availability', '99.99%')}")

    return deps


if __name__ == "__main__":
    asyncio.run(fastapi_fintech_example())