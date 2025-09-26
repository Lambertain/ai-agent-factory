"""
Пример конфигурации Prisma Database Agent для SaaS проекта.

Демонстрирует настройку агента для Software as a Service платформы
с фокусом на subscriptions, users, features и billing.
"""

from ..dependencies import PrismaDatabaseDependencies


def setup_saas_agent():
    """Настройка агента для SaaS проекта."""
    return PrismaDatabaseDependencies(
        project_name="SaasPlatform",
        domain_type="saas",
        analysis_mode="full",

        # SaaS специфичные настройки
        performance_threshold_ms=500.0,  # Быстрые запросы для dashboard
        target_query_performance=200.0,  # Цель для user dashboards
        max_connection_pool=20,  # Много concurrent users

        # Оптимизация для SaaS схемы
        schema_config={
            "core_entities": ["User", "Subscription", "Feature", "Usage", "Billing", "Organization"],
            "relations": [
                "User-Organization",
                "Organization-Subscription",
                "Subscription-Feature",
                "User-Usage",
                "Subscription-Billing"
            ],
            "critical_indexes": [
                "user_email_unique",
                "subscription_status_index",
                "usage_date_user_index",
                "billing_period_index",
                "feature_enabled_index"
            ],
            "performance_focus": [
                "user_dashboard_queries",
                "usage_analytics",
                "billing_calculations",
                "feature_access_checks",
                "multi_tenant_isolation"
            ],
            "scaling_considerations": [
                "Row Level Security для multi-tenancy",
                "Partitioning по organization_id",
                "Usage metrics aggregation",
                "Billing period calculations"
            ]
        },

        # RAG теги для SaaS знаний
        knowledge_tags=[
            "prisma-database",
            "saas",
            "multi-tenancy",
            "subscriptions",
            "billing",
            "usage-analytics",
            "feature-flags",
            "agent-knowledge"
        ]
    )


def example_saas_analysis():
    """Пример анализа SaaS схемы."""
    deps = setup_saas_agent()

    # Пример схемы для анализа
    saas_schema = '''
    model User {
      id             String       @id @default(cuid())
      email          String       @unique
      name           String
      organizationId String
      role           UserRole     @default(MEMBER)
      organization   Organization @relation(fields: [organizationId], references: [id])
      usage          Usage[]
      createdAt      DateTime     @default(now())

      @@index([organizationId])
    }

    model Organization {
      id           String        @id @default(cuid())
      name         String
      slug         String        @unique
      users        User[]
      subscription Subscription?
      createdAt    DateTime      @default(now())
    }

    model Subscription {
      id             String             @id @default(cuid())
      organizationId String             @unique
      plan           SubscriptionPlan
      status         SubscriptionStatus @default(TRIAL)
      features       SubscriptionFeature[]
      billings       Billing[]
      organization   Organization       @relation(fields: [organizationId], references: [id])
      createdAt      DateTime           @default(now())
      expiresAt      DateTime?
    }

    model Feature {
      id           String                @id @default(cuid())
      name         String                @unique
      description  String?
      subscriptions SubscriptionFeature[]
    }

    model Usage {
      id       String   @id @default(cuid())
      userId   String
      feature  String
      count    Int      @default(1)
      date     DateTime @default(now())
      user     User     @relation(fields: [userId], references: [id])

      @@index([userId, date])
      @@index([feature, date])
    }
    '''

    return {
        "dependencies": deps,
        "schema_example": saas_schema,
        "analysis_focus": [
            "Multi-tenant data isolation",
            "Subscription status queries",
            "Usage analytics aggregation",
            "Billing calculations",
            "Feature access validation"
        ],
        "expected_optimizations": [
            "Row Level Security для tenant isolation",
            "Partitioning usage data по месяцам",
            "Indexes для subscription status checks",
            "Materialized views для billing",
            "Connection pooling per organization"
        ]
    }


if __name__ == "__main__":
    print("🚀 SAAS PRISMA CONFIGURATION")
    print("=" * 50)

    config = example_saas_analysis()
    deps = config["dependencies"]

    print(f"Domain: {deps.domain_type}")
    print(f"Project: {deps.project_name}")
    print(f"Performance target: {deps.target_query_performance}ms")
    print(f"Core entities: {deps.schema_config['core_entities']}")
    print("\nReady for SaaS database analysis!")