"""
Express.js E-commerce API Configuration Example.

Example configuration for building an e-commerce API using Express.js with TypeScript,
including product management, user authentication, and order processing.
"""

import asyncio
from ..agent import api_development_agent
from ..dependencies import APIAgentDependencies


async def express_ecommerce_example():
    """Express.js e-commerce API development example."""

    # Configure dependencies for Express.js e-commerce API
    deps = APIAgentDependencies(
        # Core settings
        api_key="your_llm_api_key",
        project_path="/path/to/ecommerce/api",
        project_name="E-commerce Express API",

        # Framework configuration
        framework_type="express",
        api_type="rest",
        domain_type="ecommerce",

        # Architecture and patterns
        architecture_pattern="mvc",
        auth_strategy="jwt",
        data_validation="schema",

        # E-commerce specific settings
        caching_strategy="redis",
        rate_limiting=True,
        cors_enabled=True,
        compression_enabled=True,

        # Documentation and testing
        documentation_type="openapi",
        testing_framework="jest",
        api_versioning="header",

        # Database configuration
        database_type="postgresql",
        orm_framework="prisma",

        # TypeScript configuration
        typescript_enabled=True,
        hot_reload=True,
        environment="development",

        # Middleware stack for e-commerce
        middleware_stack=[
            "cors",
            "helmet",
            "compression",
            "morgan",
            "express-rate-limit",
            "express-validator"
        ],

        # Security configuration for e-commerce
        security_headers=True,
        input_sanitization=True,
        sql_injection_protection=True,
        xss_protection=True,

        # E-commerce business logic patterns
        business_logic_patterns=[
            "service-layer",
            "repository-pattern",
            "factory-pattern"
        ],

        # Advanced e-commerce features
        advanced_config={
            "payment_integration": "stripe",
            "email_service": "sendgrid",
            "image_storage": "cloudinary",
            "search_engine": "elasticsearch",
            "cart_session_duration": 3600,
            "max_cart_items": 100,
            "inventory_tracking": True,
            "multi_currency": True,
            "tax_calculation": True,
            "shipping_integration": True
        },

        # RAG configuration
        knowledge_tags=["express", "ecommerce", "api-development", "typescript"],
        knowledge_domain="docs.expressjs.com",
        archon_project_id="express-ecommerce-api"
    )

    print("🛒 Создание Express.js E-commerce API...")

    # 1. Validate configuration
    print("\n1. Валидация конфигурации...")
    result = await api_development_agent.run(
        user_prompt="Validate the current API configuration for e-commerce requirements",
        deps=deps
    )
    print(f"Результат валидации: {result.data}")

    # 2. Create product management endpoints
    print("\n2. Создание endpoints для управления товарами...")
    result = await api_development_agent.run(
        user_prompt="Create a complete product management endpoint with GET, POST, PUT, DELETE operations. Include product search, filtering by category, price range, and availability.",
        deps=deps
    )
    print(f"Product endpoints: {result.data}")

    # 3. Create user authentication system
    print("\n3. Создание системы аутентификации пользователей...")
    result = await api_development_agent.run(
        user_prompt="Create user authentication endpoints including registration, login, password reset, and JWT token management. Include email verification.",
        deps=deps
    )
    print(f"Auth system: {result.data}")

    # 4. Create shopping cart API
    print("\n4. Создание API корзины покупок...")
    result = await api_development_agent.run(
        user_prompt="Create shopping cart endpoints: add to cart, remove from cart, update quantities, get cart contents, and calculate totals with tax and shipping.",
        deps=deps
    )
    print(f"Shopping cart API: {result.data}")

    # 5. Create order processing system
    print("\n5. Создание системы обработки заказов...")
    result = await api_development_agent.run(
        user_prompt="Create order processing endpoints: create order, update order status, order history, payment processing integration with Stripe.",
        deps=deps
    )
    print(f"Order processing: {result.data}")

    # 6. Create middleware for e-commerce security
    print("\n6. Создание middleware для безопасности...")
    result = await api_development_agent.run(
        user_prompt="Create security middleware for e-commerce: rate limiting for API abuse prevention, input validation for product data, CORS for web store frontend.",
        deps=deps
    )
    print(f"Security middleware: {result.data}")

    # 7. Generate API documentation
    print("\n7. Генерация документации API...")
    endpoints_config = [
        {"path": "/api/products", "method": "GET", "description": "Get products with filtering"},
        {"path": "/api/products", "method": "POST", "description": "Create new product"},
        {"path": "/api/auth/register", "method": "POST", "description": "User registration"},
        {"path": "/api/auth/login", "method": "POST", "description": "User login"},
        {"path": "/api/cart", "method": "GET", "description": "Get cart contents"},
        {"path": "/api/cart/add", "method": "POST", "description": "Add item to cart"},
        {"path": "/api/orders", "method": "POST", "description": "Create new order"},
        {"path": "/api/orders/:id", "method": "GET", "description": "Get order details"}
    ]

    result = await api_development_agent.run(
        user_prompt=f"Generate comprehensive OpenAPI documentation for e-commerce API with these endpoints: {endpoints_config}. Include request/response schemas, authentication requirements, and examples.",
        deps=deps
    )
    print(f"API Documentation: {result.data}")

    # 8. Generate tests
    print("\n8. Создание тестов...")
    result = await api_development_agent.run(
        user_prompt="Generate comprehensive Jest tests for the product endpoints including unit tests, integration tests, and e2e tests. Test authentication, validation, error handling.",
        deps=deps
    )
    print(f"Test suite: {result.data}")

    # 9. Generate deployment configuration
    print("\n9. Создание конфигурации развертывания...")
    result = await api_development_agent.run(
        user_prompt="Generate Docker configuration for production deployment including Node.js optimization, Redis for caching, PostgreSQL database, and environment variables setup.",
        deps=deps
    )
    print(f"Deployment config: {result.data}")

    print("\n✅ Express.js E-commerce API создан успешно!")
    print(f"📁 Проект: {deps.project_name}")
    print(f"🚀 Фреймворк: {deps.framework_type}")
    print(f"🛒 Домен: {deps.domain_type}")
    print(f"🔐 Аутентификация: {deps.auth_strategy}")
    print(f"📊 Кэширование: {deps.caching_strategy}")

    return deps


if __name__ == "__main__":
    asyncio.run(express_ecommerce_example())