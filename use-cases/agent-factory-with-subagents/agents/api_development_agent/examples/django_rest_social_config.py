"""
Django REST Framework Social Media API Configuration Example.

Example configuration for building a social media platform API using Django REST Framework,
including user profiles, content management, real-time features, and social interactions.
"""

import asyncio
from ..agent import api_development_agent
from ..dependencies import APIAgentDependencies


async def django_rest_social_example():
    """Django REST Framework social media API development example."""

    # Configure dependencies for Django REST social media API
    deps = APIAgentDependencies(
        # Core settings
        api_key="your_llm_api_key",
        project_path="/path/to/social/api",
        project_name="Social Media Django API",

        # Framework configuration
        framework_type="django-rest",
        api_type="rest",
        domain_type="social",

        # Social media architecture patterns
        architecture_pattern="mvc",
        auth_strategy="jwt",
        data_validation="serializer",

        # Social media performance requirements
        caching_strategy="redis",
        rate_limiting=True,
        cors_enabled=True,
        compression_enabled=True,

        # Social media documentation and testing
        documentation_type="openapi",
        testing_framework="pytest",
        api_versioning="url",

        # Social media database configuration
        database_type="postgresql",
        orm_framework="django-orm",

        # Python configuration
        typescript_enabled=False,
        hot_reload=True,
        environment="development",

        # Social media middleware stack
        middleware_stack=[
            "cors",
            "security",
            "common",
            "sessions",
            "csrf",
            "authentication",
            "messages",
            "clickjacking",
            "throttling"
        ],

        # Social media security requirements
        security_headers=True,
        input_sanitization=True,
        sql_injection_protection=True,
        xss_protection=True,

        # Social media business logic patterns
        business_logic_patterns=[
            "service-layer",
            "repository-pattern",
            "observer-pattern",
            "strategy-pattern"
        ],

        # Advanced social media features
        advanced_config={
            "real_time_messaging": True,
            "websocket_support": True,
            "push_notifications": True,
            "content_moderation": "automatic",
            "image_processing": "pillow",
            "video_processing": "ffmpeg",
            "media_storage": "aws-s3",
            "cdn": "cloudfront",
            "search_engine": "elasticsearch",
            "recommendation_engine": "collaborative-filtering",
            "analytics": "google-analytics",
            "social_graph": "neo4j",
            "feed_algorithm": "machine-learning",
            "trending_topics": True,
            "hashtag_support": True,
            "mention_system": True,
            "story_feature": True,
            "live_streaming": True,
            "group_management": True,
            "event_system": True,
            "privacy_controls": "granular",
            "content_reporting": True,
            "user_verification": True,
            "anti_spam": "machine-learning",
            "sentiment_analysis": True,
            "location_services": True,
            "multi_language": True
        },

        # RAG configuration
        knowledge_tags=["django-rest", "social-media", "api-development", "scalability"],
        knowledge_domain="django-rest-framework.org",
        archon_project_id="django-social-api"
    )

    print("📱 Создание Django REST Social Media API...")

    # 1. Validate social media configuration
    print("\n1. Валидация social media конфигурации...")
    result = await api_development_agent.run(
        user_prompt="Validate the current Django REST configuration for social media requirements including scalability, real-time features, and content moderation capabilities.",
        deps=deps
    )
    print(f"Результат валидации: {result.data}")

    # 2. Create user profile management
    print("\n2. Создание user profile management...")
    result = await api_development_agent.run(
        user_prompt="Create comprehensive user profile management with Django REST Framework including user registration, profile customization, privacy settings, follower/following system, and profile verification.",
        deps=deps
    )
    print(f"User profile system: {result.data}")

    # 3. Create content management system
    print("\n3. Создание content management системы...")
    result = await api_development_agent.run(
        user_prompt="Create content management system for posts, images, videos, stories with Django models and serializers. Include content creation, editing, deletion, and media upload handling.",
        deps=deps
    )
    print(f"Content management: {result.data}")

    # 4. Create social interaction system
    print("\n4. Создание social interaction системы...")
    result = await api_development_agent.run(
        user_prompt="Create social interaction system including likes, comments, shares, mentions, hashtags, and reactions. Implement efficient database queries and caching for high performance.",
        deps=deps
    )
    print(f"Social interactions: {result.data}")

    # 5. Create news feed algorithm
    print("\n5. Создание news feed алгоритма...")
    result = await api_development_agent.run(
        user_prompt="Create intelligent news feed system with Django that aggregates content from followed users, applies ranking algorithms, handles pagination, and provides personalized content recommendations.",
        deps=deps
    )
    print(f"News feed system: {result.data}")

    # 6. Create messaging system
    print("\n6. Создание messaging системы...")
    result = await api_development_agent.run(
        user_prompt="Create real-time messaging system with Django Channels for direct messages, group chats, message status tracking, media sharing, and push notifications.",
        deps=deps
    )
    print(f"Messaging system: {result.data}")

    # 7. Create content moderation
    print("\n7. Создание content moderation...")
    result = await api_development_agent.run(
        user_prompt="Create automated content moderation system with machine learning integration for detecting inappropriate content, spam, hate speech, and copyright violations. Include reporting and review workflows.",
        deps=deps
    )
    print(f"Content moderation: {result.data}")

    # 8. Create search and discovery
    print("\n8. Создание search и discovery...")
    result = await api_development_agent.run(
        user_prompt="Create search and discovery system with Elasticsearch integration for finding users, posts, hashtags, and locations. Include trending topics, suggestions, and advanced filtering.",
        deps=deps
    )
    print(f"Search system: {result.data}")

    # 9. Create analytics and insights
    print("\n9. Создание analytics и insights...")
    result = await api_development_agent.run(
        user_prompt="Create analytics system for tracking user engagement, content performance, platform metrics, and providing insights to users and administrators.",
        deps=deps
    )
    print(f"Analytics system: {result.data}")

    # 10. Create API throttling and security
    print("\n10. Создание API throttling и security...")
    result = await api_development_agent.run(
        user_prompt="Create comprehensive API throttling and security system using Django REST Framework throttling, authentication, permissions, and rate limiting to prevent abuse and ensure fair usage.",
        deps=deps
    )
    print(f"Security system: {result.data}")

    # 11. Generate social media API documentation
    print("\n11. Генерация social media API документации...")
    endpoints_config = [
        {"path": "/api/v1/auth/register", "method": "POST", "description": "User registration"},
        {"path": "/api/v1/auth/login", "method": "POST", "description": "User login"},
        {"path": "/api/v1/profiles/me", "method": "GET", "description": "Get current user profile"},
        {"path": "/api/v1/posts", "method": "POST", "description": "Create new post"},
        {"path": "/api/v1/posts", "method": "GET", "description": "Get posts feed"},
        {"path": "/api/v1/posts/{id}/like", "method": "POST", "description": "Like a post"},
        {"path": "/api/v1/posts/{id}/comment", "method": "POST", "description": "Comment on post"},
        {"path": "/api/v1/users/{id}/follow", "method": "POST", "description": "Follow user"},
        {"path": "/api/v1/messages", "method": "GET", "description": "Get messages"},
        {"path": "/api/v1/messages", "method": "POST", "description": "Send message"},
        {"path": "/api/v1/search", "method": "GET", "description": "Search content"},
        {"path": "/api/v1/trending", "method": "GET", "description": "Get trending content"}
    ]

    result = await api_development_agent.run(
        user_prompt=f"Generate comprehensive social media API documentation with Django REST Framework for these endpoints: {endpoints_config}. Include authentication, permissions, throttling, and social media specific features.",
        deps=deps
    )
    print(f"Social Media API Documentation: {result.data}")

    # 12. Generate performance tests
    print("\n12. Создание performance тестов...")
    result = await api_development_agent.run(
        user_prompt="Generate comprehensive performance test suite for social media API including load tests for feed generation, concurrent user tests, message delivery tests, and database optimization tests.",
        deps=deps
    )
    print(f"Performance test suite: {result.data}")

    # 13. Generate deployment configuration
    print("\n13. Создание scalable deployment конфигурации...")
    result = await api_development_agent.run(
        user_prompt="Generate scalable deployment configuration for social media API including Docker containers, Kubernetes orchestration, Redis caching, PostgreSQL database, Elasticsearch, and CDN integration.",
        deps=deps
    )
    print(f"Scalable deployment config: {result.data}")

    print("\n✅ Django REST Social Media API создан успешно!")
    print(f"📁 Проект: {deps.project_name}")
    print(f"🚀 Фреймворк: {deps.framework_type}")
    print(f"📱 Домен: {deps.domain_type}")
    print(f"🔐 Аутентификация: {deps.auth_strategy}")
    print(f"🏗️ Архитектура: {deps.architecture_pattern}")
    print(f"📊 Кэширование: {deps.caching_strategy}")
    print(f"🔍 Поиск: {deps.advanced_config.get('search_engine', 'elasticsearch')}")
    print(f"📈 Analytics: {deps.advanced_config.get('analytics', 'enabled')}")

    return deps


if __name__ == "__main__":
    asyncio.run(django_rest_social_example())