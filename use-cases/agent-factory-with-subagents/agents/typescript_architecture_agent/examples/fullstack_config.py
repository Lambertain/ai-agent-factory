"""
Пример конфигурации TypeScript Architecture Agent для Full-stack проекта.

Демонстрирует настройку агента для Next.js/T3 Stack/Remix приложений
с фокусом на end-to-end type safety.
"""

from ..dependencies import TypeScriptArchitectureDependencies


def setup_nextjs_fullstack_agent():
    """Настройка агента для Next.js full-stack проекта."""
    return TypeScriptArchitectureDependencies(
        project_name="NextJSApp",
        project_type="full-stack",
        framework="nextjs",
        architecture_focus="type-safety",
        analysis_mode="full",

        # Full-stack специфичные настройки
        target_type_coverage=0.96,  # Высокая типизация для E2E safety
        performance_budget_ms=4000,  # Баланс между типизацией и скоростью
        max_complexity_score=10,  # Умеренная сложность для maintainability

        # Domain-specific типы для Next.js
        domain_types={
            "nextjs_types": [
                "NextPage", "NextApiRequest", "NextApiResponse",
                "GetServerSideProps", "GetStaticProps", "GetStaticPaths",
                "NextComponentType", "AppProps", "DocumentProps"
            ],
            "app_router_types": [
                "PageProps", "LayoutProps", "LoadingProps", "ErrorProps",
                "NotFoundProps", "ServerComponent", "ClientComponent"
            ],
            "api_types": [
                "APIRoute", "RouteHandler", "RequestContext",
                "ResponseData", "NextRequest", "NextResponse"
            ],
            "data_fetching": [
                "ServerAction", "FormData", "SearchParams",
                "DynamicRoute", "StaticParams"
            ]
        },

        # Архитектурные паттерны для Next.js
        architectural_patterns=[
            "App Router Architecture",
            "Server Components",
            "Client Components",
            "API Routes",
            "Server Actions",
            "Middleware Pattern",
            "Dynamic Routes",
            "Static Generation"
        ],

        # RAG теги для Next.js знаний
        knowledge_tags=[
            "typescript-architecture",
            "nextjs",
            "full-stack-architecture",
            "ssr",
            "app-router",
            "server-components",
            "api-routes",
            "server-actions",
            "agent-knowledge"
        ]
    )


def setup_t3_stack_agent():
    """Настройка агента для T3 Stack проекта."""
    return TypeScriptArchitectureDependencies(
        project_name="T3StackApp",
        project_type="full-stack",
        framework="t3-stack",
        architecture_focus="scalability",
        analysis_mode="full",

        # T3 Stack специфичные настройки
        target_type_coverage=0.97,  # Очень высокая типизация
        performance_budget_ms=4500,
        max_complexity_score=12,  # Сложные типы для tRPC

        # Domain-specific типы для T3 Stack
        domain_types={
            "t3_types": [
                "NextPage", "AppRouter", "TRPCRouter", "PrismaClient",
                "NextAuthConfig", "NextAuthSession"
            ],
            "trpc_types": [
                "TRPCContext", "TRPCProcedure", "TRPCQuery", "TRPCMutation",
                "TRPCSubscription", "TRPCMiddleware"
            ],
            "prisma_types": [
                "PrismaModel", "PrismaDelegate", "PrismaTransaction",
                "PrismaSelect", "PrismaInclude"
            ],
            "auth_types": [
                "Session", "User", "Account", "JWT",
                "CallbacksConfig", "EventsConfig"
            ]
        },

        # Архитектурные паттерны для T3 Stack
        architectural_patterns=[
            "tRPC API Layer",
            "Prisma ORM Integration",
            "NextAuth Authentication",
            "Type-safe Database Queries",
            "End-to-end Type Safety",
            "Server-side Validation"
        ],

        # RAG теги для T3 Stack знаний
        knowledge_tags=[
            "typescript-architecture",
            "t3-stack",
            "trpc",
            "prisma",
            "nextauth",
            "nextjs",
            "end-to-end-typesafety",
            "agent-knowledge"
        ]
    )


def example_fullstack_analysis():
    """Пример анализа full-stack TypeScript проекта."""
    nextjs_deps = setup_nextjs_fullstack_agent()

    return {
        "dependencies": nextjs_deps,
        "analysis_focus": [
            "End-to-end type safety from DB to UI",
            "API route type definitions",
            "Server component prop types",
            "Client-server data contract",
            "Authentication type flow"
        ],
        "expected_optimizations": [
            "Shared type definitions between client/server",
            "API response schema validation",
            "Database to TypeScript type generation",
            "Form validation with type safety",
            "Authentication flow typing",
            "Error boundary type handling",
            "Middleware type safety"
        ],
        "performance_targets": {
            "full_stack_build": "< 30s",
            "type_check_time": "< 4s",
            "api_route_inference": "< 1s",
            "component_compilation": "< 2s"
        },
        "fullstack_patterns": [
            "Shared types package for monorepo",
            "API contract validation with Zod",
            "Database schema to TypeScript types",
            "Server action type safety",
            "Client-server state synchronization",
            "Authentication context typing"
        ]
    }


if __name__ == "__main__":
    print("🌐 FULL-STACK TYPESCRIPT ARCHITECTURE")
    print("=" * 50)

    config = example_fullstack_analysis()
    deps = config["dependencies"]

    print(f"Project type: {deps.project_type}")
    print(f"Framework: {deps.framework}")
    print(f"Architecture focus: {deps.architecture_focus}")
    print(f"Type coverage target: {deps.target_type_coverage * 100}%")
    print(f"Performance budget: {deps.performance_budget_ms}ms")
    print("\nReady for full-stack TypeScript architecture analysis!")