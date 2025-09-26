"""
Пример конфигурации Prisma Database Agent для E-commerce проекта.

Демонстрирует настройку агента для интернет-магазина
с фокусом на products, orders, customers и inventory management.
"""

from ..dependencies import PrismaDatabaseDependencies


def setup_ecommerce_agent():
    """Настройка агента для E-commerce проекта."""
    return PrismaDatabaseDependencies(
        project_name="EcommerceStore",
        domain_type="e-commerce",
        analysis_mode="full",

        # E-commerce специфичные настройки производительности
        performance_threshold_ms=800.0,  # Быстрые запросы для каталога
        target_query_performance=300.0,  # Цель для product listings
        max_connection_pool=15,  # Больше соединений для высокой нагрузки

        # Оптимизация для e-commerce схемы
        schema_config={
            "core_entities": ["Product", "Order", "Customer", "Category", "Cart", "Inventory"],
            "relations": [
                "Product-Category",
                "Order-Product",
                "Customer-Order",
                "Cart-Customer",
                "Product-Inventory"
            ],
            "critical_indexes": [
                "product_sku_unique",
                "product_category_index",
                "order_status_date_index",
                "customer_email_unique",
                "cart_session_index"
            ],
            "performance_focus": [
                "product_search_queries",
                "order_processing_speed",
                "inventory_updates",
                "customer_session_management"
            ]
        },

        # RAG теги для e-commerce знаний
        knowledge_tags=[
            "prisma-database",
            "ecommerce",
            "product-catalog",
            "order-management",
            "inventory-tracking",
            "customer-data",
            "payment-processing",
            "agent-knowledge"
        ]
    )


def example_ecommerce_analysis():
    """Пример анализа e-commerce схемы."""
    deps = setup_ecommerce_agent()

    # Пример схемы для анализа
    ecommerce_schema = '''
    model Product {
      id          String   @id @default(cuid())
      sku         String   @unique
      name        String
      description String?
      price       Decimal
      categoryId  String
      inventory   Int      @default(0)
      category    Category @relation(fields: [categoryId], references: [id])
      orderItems  OrderItem[]
      cartItems   CartItem[]
      createdAt   DateTime @default(now())
      updatedAt   DateTime @updatedAt
    }

    model Category {
      id       String    @id @default(cuid())
      name     String
      slug     String    @unique
      products Product[]
    }

    model Customer {
      id       String @id @default(cuid())
      email    String @unique
      name     String
      orders   Order[]
      cart     Cart?
      address  String?
    }

    model Order {
      id          String      @id @default(cuid())
      customerId  String
      status      OrderStatus @default(PENDING)
      total       Decimal
      customer    Customer    @relation(fields: [customerId], references: [id])
      items       OrderItem[]
      createdAt   DateTime    @default(now())
      updatedAt   DateTime    @updatedAt
    }
    '''

    return {
        "dependencies": deps,
        "schema_example": ecommerce_schema,
        "analysis_focus": [
            "Оптимизация product search queries",
            "Индексирование для быстрого каталога",
            "Order processing performance",
            "Customer session management",
            "Inventory tracking efficiency"
        ],
        "expected_optimizations": [
            "Composite indexes для product filtering",
            "Partitioning для больших order tables",
            "Caching strategies для популярных products",
            "Connection pooling для high traffic"
        ]
    }


if __name__ == "__main__":
    print("🛒 E-COMMERCE PRISMA CONFIGURATION")
    print("=" * 50)

    config = example_ecommerce_analysis()
    deps = config["dependencies"]

    print(f"Domain: {deps.domain_type}")
    print(f"Project: {deps.project_name}")
    print(f"Performance target: {deps.target_query_performance}ms")
    print(f"Core entities: {deps.schema_config['core_entities']}")
    print("\nReady for e-commerce database analysis!")