"""
Пример конфигурации Prisma Database Agent для CRM проекта.

Демонстрирует настройку агента для Customer Relationship Management системы
с фокусом на contacts, deals, activities и analytics.
"""

from ..dependencies import PrismaDatabaseDependencies


def setup_crm_agent():
    """Настройка агента для CRM проекта."""
    return PrismaDatabaseDependencies(
        project_name="CRMSystem",
        domain_type="crm",
        analysis_mode="full",

        # CRM специфичные настройки
        performance_threshold_ms=600.0,  # Сложные analytics запросы
        target_query_performance=250.0,  # Цель для contact searches
        max_connection_pool=12,  # Moderate concurrent users

        # Оптимизация для CRM схемы
        schema_config={
            "core_entities": ["Contact", "Company", "Deal", "Activity", "Pipeline", "Task"],
            "relations": [
                "Contact-Company",
                "Deal-Contact",
                "Deal-Company",
                "Activity-Deal",
                "Activity-Contact",
                "Task-User"
            ],
            "critical_indexes": [
                "contact_email_index",
                "contact_company_index",
                "deal_stage_index",
                "deal_value_index",
                "activity_date_index",
                "task_due_date_index"
            ],
            "performance_focus": [
                "contact_search_queries",
                "deal_pipeline_views",
                "activity_timelines",
                "sales_analytics",
                "task_management"
            ],
            "analytics_requirements": [
                "Sales funnel metrics",
                "Deal conversion rates",
                "Activity frequency analysis",
                "Contact engagement scoring",
                "Revenue forecasting"
            ]
        },

        # RAG теги для CRM знаний
        knowledge_tags=[
            "prisma-database",
            "crm",
            "sales-management",
            "contact-management",
            "deal-pipeline",
            "sales-analytics",
            "activity-tracking",
            "agent-knowledge"
        ]
    )


def example_crm_analysis():
    """Пример анализа CRM схемы."""
    deps = setup_crm_agent()

    # Пример схемы для анализа
    crm_schema = '''
    model Contact {
      id        String     @id @default(cuid())
      email     String     @unique
      firstName String
      lastName  String
      phone     String?
      companyId String?
      company   Company?   @relation(fields: [companyId], references: [id])
      deals     Deal[]
      activities Activity[]
      score     Int        @default(0)
      createdAt DateTime   @default(now())
      updatedAt DateTime   @updatedAt

      @@index([email])
      @@index([companyId])
      @@index([score])
    }

    model Company {
      id        String    @id @default(cuid())
      name      String
      domain    String?   @unique
      industry  String?
      size      String?
      contacts  Contact[]
      deals     Deal[]
      createdAt DateTime  @default(now())

      @@index([domain])
      @@index([industry])
    }

    model Deal {
      id          String     @id @default(cuid())
      title       String
      value       Decimal
      stage       DealStage  @default(PROSPECT)
      probability Int        @default(10)
      contactId   String
      companyId   String?
      ownerId     String
      contact     Contact    @relation(fields: [contactId], references: [id])
      company     Company?   @relation(fields: [companyId], references: [id])
      activities  Activity[]
      closedAt    DateTime?
      createdAt   DateTime   @default(now())
      updatedAt   DateTime   @updatedAt

      @@index([stage])
      @@index([ownerId])
      @@index([value])
      @@index([createdAt])
    }

    model Activity {
      id        String       @id @default(cuid())
      type      ActivityType
      subject   String
      notes     String?
      dealId    String?
      contactId String?
      userId    String
      deal      Deal?        @relation(fields: [dealId], references: [id])
      contact   Contact?     @relation(fields: [contactId], references: [id])
      dueDate   DateTime?
      createdAt DateTime     @default(now())

      @@index([userId, createdAt])
      @@index([type, dueDate])
    }
    '''

    return {
        "dependencies": deps,
        "schema_example": crm_schema,
        "analysis_focus": [
            "Contact search performance",
            "Deal pipeline queries",
            "Activity timeline generation",
            "Sales analytics aggregation",
            "Contact scoring calculations"
        ],
        "expected_optimizations": [
            "Full-text search для contacts",
            "Composite indexes для deal filtering",
            "Materialized views для sales metrics",
            "Partitioning activities по датам",
            "Optimization для reporting queries"
        ]
    }


if __name__ == "__main__":
    print("📊 CRM PRISMA CONFIGURATION")
    print("=" * 50)

    config = example_crm_analysis()
    deps = config["dependencies"]

    print(f"Domain: {deps.domain_type}")
    print(f"Project: {deps.project_name}")
    print(f"Performance target: {deps.target_query_performance}ms")
    print(f"Core entities: {deps.schema_config['core_entities']}")
    print("\nReady for CRM database analysis!")