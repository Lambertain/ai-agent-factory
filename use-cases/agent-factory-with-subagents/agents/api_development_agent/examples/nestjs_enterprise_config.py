"""
NestJS Enterprise API Configuration Example.

Example configuration for building an enterprise-grade API using NestJS with TypeScript,
including microservices architecture, advanced security, and comprehensive monitoring.
"""

import asyncio
from ..agent import api_development_agent
from ..dependencies import APIAgentDependencies


async def nestjs_enterprise_example():
    """NestJS enterprise API development example."""

    # Configure dependencies for NestJS enterprise API
    deps = APIAgentDependencies(
        # Core settings
        api_key="your_llm_api_key",
        project_path="/path/to/enterprise/api",
        project_name="Enterprise NestJS API",

        # Framework configuration
        framework_type="nestjs",
        api_type="rest",
        domain_type="enterprise",

        # Enterprise architecture patterns
        architecture_pattern="clean-architecture",
        auth_strategy="oauth2",
        data_validation="decorator",

        # Enterprise performance requirements
        caching_strategy="redis",
        rate_limiting=True,
        cors_enabled=True,
        compression_enabled=True,

        # Enterprise documentation and testing
        documentation_type="openapi",
        testing_framework="jest",
        api_versioning="header",

        # Enterprise database configuration
        database_type="postgresql",
        orm_framework="typeorm",

        # TypeScript configuration (required for NestJS)
        typescript_enabled=True,
        hot_reload=True,
        environment="development",

        # Enterprise middleware stack
        middleware_stack=[
            "cors",
            "helmet",
            "compression",
            "morgan",
            "express-rate-limit",
            "class-validator",
            "class-transformer"
        ],

        # Enterprise security requirements
        security_headers=True,
        input_sanitization=True,
        sql_injection_protection=True,
        xss_protection=True,

        # Enterprise business logic patterns
        business_logic_patterns=[
            "service-layer",
            "repository-pattern",
            "factory-pattern",
            "strategy-pattern",
            "observer-pattern"
        ],

        # Advanced enterprise features
        advanced_config={
            "microservices": True,
            "event_sourcing": True,
            "cqrs_pattern": True,
            "graphql_enabled": True,
            "websocket_enabled": True,
            "health_checks": True,
            "metrics_collection": "prometheus",
            "distributed_tracing": "jaeger",
            "audit_logging": True,
            "multi_tenant": True,
            "rbac_enabled": True,
            "sso_integration": "okta",
            "message_queue": "rabbitmq",
            "file_storage": "aws-s3",
            "search_engine": "elasticsearch",
            "monitoring": "datadog",
            "alerting": "pagerduty"
        },

        # RAG configuration
        knowledge_tags=["nestjs", "enterprise", "api-development", "microservices"],
        knowledge_domain="docs.nestjs.com",
        archon_project_id="nestjs-enterprise-api"
    )

    print("🏢 Создание NestJS Enterprise API...")

    # 1. Validate enterprise configuration
    print("\n1. Валидация enterprise конфигурации...")
    result = await api_development_agent.run(
        user_prompt="Validate the current NestJS configuration for enterprise requirements including security, scalability, and monitoring capabilities.",
        deps=deps
    )
    print(f"Результат валидации: {result.data}")

    # 2. Create modular architecture
    print("\n2. Создание модульной архитектуры...")
    result = await api_development_agent.run(
        user_prompt="Create a modular NestJS architecture with separate modules for Users, Organizations, Projects, and Audit. Include proper dependency injection and module organization.",
        deps=deps
    )
    print(f"Modular architecture: {result.data}")

    # 3. Create enterprise authentication with RBAC
    print("\n3. Создание enterprise аутентификации с RBAC...")
    result = await api_development_agent.run(
        user_prompt="Create enterprise authentication system with OAuth2, JWT guards, role-based access control (RBAC), and SSO integration. Include user management, roles, and permissions.",
        deps=deps
    )
    print(f"Enterprise auth system: {result.data}")

    # 4. Create microservices communication
    print("\n4. Создание communication между микросервисами...")
    result = await api_development_agent.run(
        user_prompt="Create microservices communication layer with NestJS using message patterns, event-driven architecture, and service discovery. Include health checks and circuit breakers.",
        deps=deps
    )
    print(f"Microservices communication: {result.data}")

    # 5. Create CQRS and Event Sourcing
    print("\n5. Создание CQRS и Event Sourcing...")
    result = await api_development_agent.run(
        user_prompt="Implement CQRS pattern with Event Sourcing for enterprise data management. Create command handlers, query handlers, and event store integration.",
        deps=deps
    )
    print(f"CQRS implementation: {result.data}")

    # 6. Create enterprise middleware and interceptors
    print("\n6. Создание enterprise middleware и interceptors...")
    result = await api_development_agent.run(
        user_prompt="Create enterprise-grade middleware and interceptors: audit logging, performance monitoring, error handling, request/response transformation, and security headers.",
        deps=deps
    )
    print(f"Enterprise middleware: {result.data}")

    # 7. Create GraphQL API layer
    print("\n7. Создание GraphQL API layer...")
    result = await api_development_agent.run(
        user_prompt="Create GraphQL API layer alongside REST endpoints using NestJS GraphQL module. Include resolvers, schemas, and integration with existing services.",
        deps=deps
    )
    print(f"GraphQL layer: {result.data}")

    # 8. Create comprehensive monitoring
    print("\n8. Создание comprehensive monitoring...")
    result = await api_development_agent.run(
        user_prompt="Create comprehensive monitoring solution with Prometheus metrics, health check endpoints, distributed tracing with Jaeger, and integration with enterprise monitoring tools.",
        deps=deps
    )
    print(f"Monitoring system: {result.data}")

    # 9. Generate enterprise API documentation
    print("\n9. Генерация enterprise API документации...")
    endpoints_config = [
        {"path": "/api/auth/oauth", "method": "POST", "description": "OAuth2 authentication"},
        {"path": "/api/users", "method": "GET", "description": "Get users with RBAC filtering"},
        {"path": "/api/organizations", "method": "POST", "description": "Create organization"},
        {"path": "/api/projects", "method": "GET", "description": "Get projects with permissions"},
        {"path": "/api/audit/logs", "method": "GET", "description": "Get audit logs"},
        {"path": "/api/health", "method": "GET", "description": "Health check endpoint"},
        {"path": "/graphql", "method": "POST", "description": "GraphQL endpoint"},
        {"path": "/api/metrics", "method": "GET", "description": "Prometheus metrics"}
    ]

    result = await api_development_agent.run(
        user_prompt=f"Generate comprehensive enterprise API documentation with OpenAPI 3.0 for these endpoints: {endpoints_config}. Include security schemes, RBAC annotations, and enterprise compliance requirements.",
        deps=deps
    )
    print(f"Enterprise API Documentation: {result.data}")

    # 10. Generate enterprise tests
    print("\n10. Создание enterprise тестов...")
    result = await api_development_agent.run(
        user_prompt="Generate comprehensive test suite for enterprise NestJS API including unit tests, integration tests, e2e tests, security tests, and performance tests. Include mocking for external services.",
        deps=deps
    )
    print(f"Enterprise test suite: {result.data}")

    # 11. Generate deployment configuration
    print("\n11. Создание enterprise deployment конфигурации...")
    result = await api_development_agent.run(
        user_prompt="Generate enterprise deployment configuration including Kubernetes manifests, Helm charts, Docker multi-stage builds, CI/CD pipelines, and production environment setup.",
        deps=deps
    )
    print(f"Enterprise deployment config: {result.data}")

    print("\n✅ NestJS Enterprise API создан успешно!")
    print(f"📁 Проект: {deps.project_name}")
    print(f"🚀 Фреймворк: {deps.framework_type}")
    print(f"🏢 Домен: {deps.domain_type}")
    print(f"🔐 Аутентификация: {deps.auth_strategy}")
    print(f"🏗️ Архитектура: {deps.architecture_pattern}")
    print(f"📊 Кэширование: {deps.caching_strategy}")
    print(f"🔍 Мониторинг: {deps.advanced_config.get('monitoring', 'enabled')}")

    return deps


if __name__ == "__main__":
    asyncio.run(nestjs_enterprise_example())