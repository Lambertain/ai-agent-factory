"""Зависимости для Prisma Database Agent с поддержкой RAG."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class PrismaDatabaseDependencies:
    """Зависимости для Prisma Database Agent с интеграцией RAG."""

    # Основные настройки
    context: str = "Universal Prisma database analysis"
    project_path: str = ""
    analysis_mode: str = "full"

    # Универсальные настройки домена
    domain_type: str = "custom"  # e-commerce, crm, saas, blog, social, custom
    project_type: str = "web_application"  # web_application, api, mobile_app, desktop_app
    schema_config: Dict[str, Any] = field(default_factory=dict)  # Конфигурируемые схемы
    project_name: str = ""  # Название проекта для контекста

    # RAG конфигурация для Archon Knowledge Base
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "prisma-database",
        "agent-knowledge",
        "pydantic-ai",
        "postgresql",
        "database-optimization"
    ])
    knowledge_domain: str = "prisma.io"  # Для фильтрации документации Prisma
    archon_url: str = "http://localhost:3737"
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Специфичные настройки Prisma
    database_url: str = ""
    schema_path: str = "prisma/schema.prisma"
    migration_path: str = "prisma/migrations"

    # Конфигурация анализа
    performance_threshold_ms: float = 1000.0  # Порог медленных запросов
    max_query_complexity: int = 10  # Максимальная сложность запросов
    enable_query_logging: bool = True

    # Optimization settings
    target_query_performance: float = 500.0  # Целевое время запроса в мс
    max_connection_pool: int = 10
    enable_prepared_statements: bool = True

    # Tracking улучшений и изменений
    improvements_made: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    migration_history: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        """Инициализация конфигурации после создания объекта."""
        if not self.context:
            self.context = f"Prisma database analysis for {self.project_name or 'project'}"

        # Настройка схем по умолчанию для разных доменов
        self._setup_domain_defaults()

        # Обновление тегов знаний в зависимости от режима анализа
        mode_tags = {
            "schema": ["schema-design", "normalization"],
            "queries": ["query-optimization", "performance"],
            "migrations": ["migrations", "schema-evolution"],
            "performance": ["performance-tuning", "indexing"],
            "full": ["comprehensive-analysis", "best-practices"]
        }

        if self.analysis_mode in mode_tags:
            self.knowledge_tags.extend(mode_tags[self.analysis_mode])

        # Убираем дубликаты
        self.knowledge_tags = list(set(self.knowledge_tags))

    def add_improvement(self, improvement: str, is_breaking: bool = False):
        """Добавить улучшение в трекинг."""
        timestamp = datetime.now().isoformat()
        improvement_record = f"[{timestamp}] {improvement}"

        self.improvements_made.append(improvement_record)

        if is_breaking:
            self.breaking_changes.append(improvement_record)

    def add_migration_record(self, migration_name: str, description: str, sql_changes: List[str]):
        """Добавить запись о миграции."""
        migration_record = {
            "name": migration_name,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "sql_changes": sql_changes,
            "analysis_mode": self.analysis_mode
        }

        self.migration_history.append(migration_record)

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Получить сводку анализа."""
        return {
            "mode": self.analysis_mode,
            "improvements_count": len(self.improvements_made),
            "breaking_changes_count": len(self.breaking_changes),
            "migrations_count": len(self.migration_history),
            "performance_threshold": self.performance_threshold_ms,
            "target_performance": self.target_query_performance,
            "knowledge_tags": self.knowledge_tags,
            "project_path": self.project_path
        }

    def get_database_config(self) -> Dict[str, Any]:
        """Получить конфигурацию базы данных."""
        return {
            "database_url": self.database_url if self.database_url else "Not configured",
            "schema_path": self.schema_path,
            "migration_path": self.migration_path,
            "connection_pool_size": self.max_connection_pool,
            "prepared_statements": self.enable_prepared_statements,
            "query_logging": self.enable_query_logging
        }

    def should_use_rag(self) -> bool:
        """Определить, нужно ли использовать RAG для текущей задачи."""
        # RAG полезен для сложных задач анализа и оптимизации
        complex_modes = ["full", "performance", "schema"]
        return self.analysis_mode in complex_modes

    def get_rag_query_context(self, base_query: str) -> str:
        """Создать контекст для RAG запроса."""
        context_parts = [
            base_query,
            f"Analysis mode: {self.analysis_mode}",
            f"Database: PostgreSQL with Prisma ORM",
            f"Domain: {self.get_domain_context()}"
        ]

        if self.improvements_made:
            context_parts.append(f"Previous improvements: {len(self.improvements_made)}")

        return " | ".join(context_parts)

    def _setup_domain_defaults(self):
        """Настройка схем по умолчанию для разных доменов."""
        domain_schemas = {
            "e-commerce": {
                "core_entities": ["Product", "Order", "Customer", "Category", "Cart"],
                "relations": ["Product-Category", "Order-Product", "Customer-Order"],
                "indexes": ["product_sku", "order_status", "customer_email"]
            },
            "crm": {
                "core_entities": ["Contact", "Deal", "Activity", "Company", "Pipeline"],
                "relations": ["Contact-Company", "Deal-Contact", "Activity-Deal"],
                "indexes": ["contact_email", "deal_stage", "activity_date"]
            },
            "saas": {
                "core_entities": ["User", "Subscription", "Feature", "Usage", "Billing"],
                "relations": ["User-Subscription", "Subscription-Feature", "User-Usage"],
                "indexes": ["user_email", "subscription_status", "usage_date"]
            },
            "blog": {
                "core_entities": ["Post", "Author", "Comment", "Tag", "Category"],
                "relations": ["Post-Author", "Post-Tag", "Comment-Post"],
                "indexes": ["post_slug", "author_email", "publish_date"]
            },
            "social": {
                "core_entities": ["User", "Post", "Like", "Follow", "Comment"],
                "relations": ["Post-User", "Like-User-Post", "Follow-User"],
                "indexes": ["user_username", "post_created_at", "like_created_at"]
            }
        }

        if self.domain_type in domain_schemas and not self.schema_config:
            self.schema_config = domain_schemas[self.domain_type]

    def get_domain_context(self) -> str:
        """Получить контекст домена для RAG запросов."""
        if self.domain_type == "custom":
            return f"Custom domain project: {self.project_name}"

        domain_descriptions = {
            "e-commerce": "E-commerce platform with products, orders, and customers",
            "crm": "Customer Relationship Management system",
            "saas": "Software as a Service platform with subscriptions",
            "blog": "Blog/CMS platform with posts and authors",
            "social": "Social network platform with users and posts"
        }

        return domain_descriptions.get(self.domain_type, "Unknown domain")

    def validate_configuration(self) -> List[str]:
        """Валидация конфигурации агента."""
        errors = []

        # Проверка domain_type
        valid_domains = ["e-commerce", "crm", "saas", "blog", "social", "custom"]
        if self.domain_type not in valid_domains:
            errors.append(f"Invalid domain_type: {self.domain_type}. Must be one of {valid_domains}")

        # Проверка analysis_mode
        valid_modes = ["full", "schema", "queries", "migrations", "performance"]
        if self.analysis_mode not in valid_modes:
            errors.append(f"Invalid analysis_mode: {self.analysis_mode}. Must be one of {valid_modes}")

        # Проверка performance настроек
        if self.performance_threshold_ms <= 0:
            errors.append("performance_threshold_ms must be positive")

        if self.target_query_performance <= 0:
            errors.append("target_query_performance must be positive")

        # Проверка project_name для custom domain
        if self.domain_type == "custom" and not self.project_name:
            errors.append("project_name is required for custom domain type")

        return errors

    def get_recommended_settings(self) -> Dict[str, Any]:
        """Получить рекомендуемые настройки для текущего домена."""
        recommendations = {
            "e-commerce": {
                "performance_threshold_ms": 800.0,
                "target_query_performance": 300.0,
                "max_connection_pool": 15,
                "critical_queries": ["product_search", "order_processing", "inventory_updates"]
            },
            "crm": {
                "performance_threshold_ms": 600.0,
                "target_query_performance": 250.0,
                "max_connection_pool": 12,
                "critical_queries": ["contact_search", "deal_pipeline", "activity_timeline"]
            },
            "saas": {
                "performance_threshold_ms": 500.0,
                "target_query_performance": 200.0,
                "max_connection_pool": 20,
                "critical_queries": ["user_dashboard", "usage_analytics", "billing_calc"]
            },
            "blog": {
                "performance_threshold_ms": 400.0,
                "target_query_performance": 150.0,
                "max_connection_pool": 8,
                "critical_queries": ["post_listing", "search", "comment_threads"]
            },
            "social": {
                "performance_threshold_ms": 300.0,
                "target_query_performance": 100.0,
                "max_connection_pool": 25,
                "critical_queries": ["feed_generation", "real_time_updates", "search"]
            }
        }

        return recommendations.get(self.domain_type, {
            "performance_threshold_ms": 1000.0,
            "target_query_performance": 500.0,
            "max_connection_pool": 10,
            "critical_queries": ["general_queries"]
        })