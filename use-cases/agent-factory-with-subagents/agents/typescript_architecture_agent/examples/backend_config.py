"""
Пример конфигурации TypeScript Architecture Agent для Backend проекта.

Демонстрирует настройку агента для Node.js/NestJS/Express сервисов
с фокусом на API type safety и производительность.
"""

from ..dependencies import TypeScriptArchitectureDependencies


def setup_nestjs_backend_agent():
    """Настройка агента для NestJS backend проекта."""
    return TypeScriptArchitectureDependencies(
        project_name="NestJSAPI",
        project_type="backend",
        framework="nestjs",
        architecture_focus="type-safety",
        analysis_mode="full",

        # Backend специфичные настройки
        target_type_coverage=0.98,  # Максимальная типизация для API
        performance_budget_ms=5000,  # Больше времени для сложной типизации
        max_complexity_score=12,  # Сложные типы для бизнес-логики

        # Domain-specific типы для NestJS
        domain_types={
            "nestjs_types": [
                "Controller", "Injectable", "Module", "Guard",
                "Interceptor", "Pipe", "Filter", "Middleware"
            ],
            "api_types": [
                "Request", "Response", "Body", "Param", "Query",
                "Headers", "UploadedFile", "Session"
            ],
            "dto_types": [
                "CreateDTO", "UpdateDTO", "ResponseDTO", "QueryDTO",
                "PaginationDTO", "FilterDTO"
            ],
            "entity_types": [
                "Entity", "Repository", "Service", "Model",
                "Schema", "Document"
            ]
        },

        # Архитектурные паттерны для NestJS
        architectural_patterns=[
            "Dependency Injection",
            "Repository Pattern",
            "Service Layer",
            "DTO Pattern",
            "Guard Pattern",
            "Interceptor Pattern",
            "Pipe Validation",
            "Exception Filters"
        ],

        # RAG теги для NestJS знаний
        knowledge_tags=[
            "typescript-architecture",
            "nestjs",
            "backend-architecture",
            "api-design",
            "decorators",
            "dependency-injection",
            "modules",
            "guards",
            "database-types",
            "agent-knowledge"
        ]
    )


def setup_express_backend_agent():
    """Настройка агента для Express backend проекта."""
    return TypeScriptArchitectureDependencies(
        project_name="ExpressAPI",
        project_type="backend",
        framework="express",
        architecture_focus="maintainability",
        analysis_mode="full",

        # Express специфичные настройки
        target_type_coverage=0.96,
        performance_budget_ms=4500,
        max_complexity_score=10,

        # Domain-specific типы для Express
        domain_types={
            "express_types": [
                "Request", "Response", "NextFunction", "Router",
                "Application", "RequestHandler", "ErrorRequestHandler"
            ],
            "middleware_types": [
                "Middleware", "AuthMiddleware", "ValidationMiddleware",
                "LoggingMiddleware", "CorsMiddleware"
            ],
            "api_types": [
                "APIResponse", "APIError", "RequestBody", "RouteParams",
                "QueryParams", "AuthenticatedRequest"
            ]
        },

        # Архитектурные паттерны для Express
        architectural_patterns=[
            "Middleware Pattern",
            "Router Pattern",
            "Service Layer",
            "Repository Pattern",
            "Error Handling",
            "Authentication Strategy"
        ],

        # RAG теги для Express знаний
        knowledge_tags=[
            "typescript-architecture",
            "express",
            "backend-architecture",
            "middleware",
            "routing",
            "req-res",
            "api-design",
            "agent-knowledge"
        ]
    )


def example_backend_analysis():
    """Пример анализа backend TypeScript проекта."""
    nestjs_deps = setup_nestjs_backend_agent()

    return {
        "dependencies": nestjs_deps,
        "analysis_focus": [
            "API endpoint type safety",
            "DTO validation schemas",
            "Database entity type mapping",
            "Service layer type contracts",
            "Middleware type definitions"
        ],
        "expected_optimizations": [
            "Strict API request/response typing",
            "Database entity type generation",
            "DTO validation with class-validator",
            "Service interface definitions",
            "Error type standardization",
            "Authentication type guards",
            "Configuration type safety"
        ],
        "performance_targets": {
            "api_type_check": "< 5s",
            "entity_compilation": "< 3s",
            "dto_validation": "< 1s",
            "service_resolution": "< 2s"
        },
        "backend_patterns": [
            "Generic repository with typed entities",
            "DTO transformation with mapped types",
            "Service layer with dependency injection",
            "Middleware with typed context",
            "Database queries with type safety",
            "API versioning with typed contracts"
        ]
    }


if __name__ == "__main__":
    print("🚀 BACKEND TYPESCRIPT ARCHITECTURE")
    print("=" * 50)

    config = example_backend_analysis()
    deps = config["dependencies"]

    print(f"Project type: {deps.project_type}")
    print(f"Framework: {deps.framework}")
    print(f"Architecture focus: {deps.architecture_focus}")
    print(f"Type coverage target: {deps.target_type_coverage * 100}%")
    print(f"Performance budget: {deps.performance_budget_ms}ms")
    print("\nReady for backend TypeScript architecture analysis!")