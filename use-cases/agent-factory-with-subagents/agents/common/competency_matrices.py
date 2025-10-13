# -*- coding: utf-8 -*-
"""
Матрицы компетенций агентов.

Отдельный модуль с данными для CompetencyChecker.
Разделение на модули для соблюдения лимита 500 строк на файл.
"""

from typing import Dict, List
from enum import Enum
from dataclasses import dataclass


class AgentType(Enum):
    """Типы агентов в системе."""
    ANALYTICS_TRACKING = "analytics_tracking_agent"
    API_DEVELOPMENT = "api_development_agent"
    COMMUNITY_MANAGEMENT = "community_management_agent"
    MCP_CONFIGURATION = "mcp_configuration_agent"
    NLP_CONTENT_QUALITY = "nlp_content_quality_guardian_agent"
    NLP_CONTENT_RESEARCH = "nlp_content_research_agent"
    NLP_PROGRAM_GENERATOR = "nlp_program_generator_agent"
    NLP_PSYCHOLOGY_TEST = "nlp_psychology_test_adapter_agent"
    ONLINE_SUPPORT_CONTENT = "online_support_content_architect_agent"
    ONLINE_SUPPORT_ORCHESTRATOR = "online_support_content_orchestrator_agent"
    ONLINE_SUPPORT_QUALITY = "online_support_quality_guardian_agent"
    ONLINE_SUPPORT_RESEARCH = "online_support_research_agent"
    ONLINE_SUPPORT_TEST = "online_support_test_generator_agent"
    PATTERNSHIFT_TEST = "patternshift_test_generator_agent"
    PAYMENT_INTEGRATION = "payment_integration_agent"
    PERFORMANCE_OPTIMIZATION = "performance_optimization_agent"
    PRISMA_DATABASE = "prisma_database_agent"
    PSYCHOLOGY_CONTENT_ARCHITECT = "psychology_content_architect_agent"
    PSYCHOLOGY_CONTENT_ORCHESTRATOR = "psychology_content_orchestrator_agent"
    PWA_MOBILE = "pwa_mobile_agent"
    QUEUE_WORKER = "queue_worker_agent"
    RAG_AGENT = "rag_agent"
    SECURITY_AUDIT = "security_audit_agent"
    TYPESCRIPT_ARCHITECTURE = "typescript_architecture_agent"
    UIUX_ENHANCEMENT = "uiux_enhancement_agent"
    UNIVERSAL_NLP_CONTENT = "universal_nlp_content_architect_agent"


# [OK] Матрица типов ошибок -> ответственный агент
ERROR_TYPE_MATRIX: Dict[str, str] = {
    # Core Team Agents - Analysis Lead
    "requirements_unclear": "Archon Analysis Lead",
    "user_story_missing": "Archon Analysis Lead",
    "business_logic_missing": "Archon Analysis Lead",
    "requirements_conflict": "Archon Analysis Lead",

    # Core Team Agents - Blueprint Architect
    "architecture_antipattern": "Archon Blueprint Architect",
    "integration_problem": "Archon Blueprint Architect",
    "solid_violation": "Archon Blueprint Architect",
    "scalability_issue": "Archon Blueprint Architect",
    "performance_design": "Archon Blueprint Architect",

    # Core Team Agents - Implementation Engineer
    "typescript_compile": "Archon Implementation Engineer",
    "javascript_runtime": "Archon Implementation Engineer",
    "python_syntax": "Archon Implementation Engineer",
    "missing_import": "Archon Implementation Engineer",
    "null_pointer": "Archon Implementation Engineer",
    "function_signature": "Archon Implementation Engineer",
    "http_status": "Archon Implementation Engineer",
    "async_await": "Archon Implementation Engineer",

    # Core Team Agents - Quality Guardian
    "missing_tests": "Archon Quality Guardian",
    "low_coverage": "Archon Quality Guardian",
    "failing_tests": "Archon Quality Guardian",
    "wrong_assertions": "Archon Quality Guardian",
    "flaky_tests": "Archon Quality Guardian",
    "test_environment": "Archon Quality Guardian",

    # Core Team Agents - Deployment Engineer
    "ci_cd_failure": "Archon Deployment Engineer",
    "docker_build": "Archon Deployment Engineer",
    "kubernetes_error": "Archon Deployment Engineer",
    "missing_env_var": "Archon Deployment Engineer",
    "infrastructure_config": "Archon Deployment Engineer",
    "deployment_timeout": "Archon Deployment Engineer",

    # Specialized Agents - Security Audit
    "xss_vulnerability": "Security Audit Agent",
    "sql_injection": "Security Audit Agent",
    "weak_authentication": "Security Audit Agent",
    "secrets_in_code": "Security Audit Agent",
    "csrf_vulnerability": "Security Audit Agent",

    # Specialized Agents - Prisma Database
    "n_plus_one_query": "Prisma Database Agent",
    "missing_index": "Prisma Database Agent",
    "prisma_schema": "Prisma Database Agent",
    "migration_error": "Prisma Database Agent",
    "slow_query": "Prisma Database Agent",

    # Specialized Agents - UI/UX Enhancement
    "accessibility_issue": "UI/UX Enhancement Agent",
    "responsive_bug": "UI/UX Enhancement Agent",
    "ux_problem": "UI/UX Enhancement Agent",
    "missing_feedback": "UI/UX Enhancement Agent",

    # Specialized Agents - Performance Optimization
    "memory_leak": "Performance Optimization Agent",
    "slow_rendering": "Performance Optimization Agent",
    "large_bundle": "Performance Optimization Agent",
    "unnecessary_api_calls": "Performance Optimization Agent",

    # Specialized Agents - TypeScript Architecture
    "complex_type_error": "TypeScript Architecture Agent",
    "type_inference": "TypeScript Architecture Agent",
    "generic_constraint": "TypeScript Architecture Agent",
    "utility_type_misuse": "TypeScript Architecture Agent",
}


# [OK] Матрица делегирования задач между агентами
DELEGATION_MATRIX: Dict[str, List[str]] = {
    # Агент аналитики может делегировать
    "analytics_tracking_agent": [
        "uiux_enhancement_agent",  # UX аналитика
        "performance_optimization_agent",  # Производительность метрик
        "security_audit_agent"  # Приватность данных
    ],

    # Агент безопасности может делегировать
    "security_audit_agent": [
        "api_development_agent",  # API безопасность
        "prisma_database_agent",  # Безопасность БД
        "payment_integration_agent"  # PCI DSS compliance
    ],

    # UI/UX агент может делегировать
    "uiux_enhancement_agent": [
        "performance_optimization_agent",  # Frontend performance
        "pwa_mobile_agent",  # Мобильная адаптация
        "typescript_architecture_agent"  # Типизация компонентов
    ],

    # Агент производительности может делегировать
    "performance_optimization_agent": [
        "prisma_database_agent",  # Оптимизация запросов
        "typescript_architecture_agent",  # Архитектурная оптимизация
        "queue_worker_agent"  # Асинхронная обработка
    ],

    # API агент может делегировать
    "api_development_agent": [
        "security_audit_agent",  # API security
        "prisma_database_agent",  # Data layer
        "payment_integration_agent",  # Payment endpoints
        "queue_worker_agent"  # Background processing
    ],

    # Prisma агент может делегировать
    "prisma_database_agent": [
        "security_audit_agent",  # DB security
        "performance_optimization_agent",  # Query optimization
        "typescript_architecture_agent"  # Type generation
    ]
}


@dataclass
class CompetencyArea:
    """Область компетенции агента."""
    primary_keywords: List[str]  # Ключевые слова основной экспертизы
    secondary_keywords: List[str]  # Смежные области
    exclusions: List[str]  # Что точно НЕ входит в компетенцию
    confidence_threshold: float = 0.7  # Минимальная уверенность для принятия задачи


def build_keyword_competency_matrix() -> Dict[AgentType, CompetencyArea]:
    """
    Построить матрицу компетенций для keyword matching.

    Используется в старом методе check_competency() для анализа задач.
    Для анализа ошибок используйте ERROR_TYPE_MATRIX.

    Returns:
        Словарь {тип_агента: область_компетенции}
    """
    return {
        AgentType.ANALYTICS_TRACKING: CompetencyArea(
            primary_keywords=[
                "аналитика", "analytics", "трекинг", "tracking", "метрики", "metrics",
                "google analytics", "яндекс метрика", "конверсия", "conversion",
                "пользовательское поведение", "user behavior", "воронка", "funnel"
            ],
            secondary_keywords=[
                "отчеты", "reports", "статистика", "кликстрим", "event tracking",
                "цели", "goals", "сегментация", "attribution"
            ],
            exclusions=[
                "безопасность", "дизайн", "база данных", "архитектура",
                "оптимизация производительности", "тестирование"
            ]
        ),

        AgentType.API_DEVELOPMENT: CompetencyArea(
            primary_keywords=[
                "api", "rest", "graphql", "endpoint", "swagger", "openapi",
                "fastapi", "flask", "django", "микросервисы", "microservices",
                "webhook", "authentication", "авторизация", "jwt"
            ],
            secondary_keywords=[
                "http", "json", "xml", "soap", "rate limiting", "версионирование",
                "документация api", "postman", "insomnia"
            ],
            exclusions=[
                "фронтенд", "ui", "дизайн", "аналитика", "психология",
                "контент", "мобильная разработка"
            ]
        ),

        AgentType.SECURITY_AUDIT: CompetencyArea(
            primary_keywords=[
                "безопасность", "security", "уязвимости", "vulnerability", "audit",
                "penetration testing", "owasp", "cve", "compliance", "gdpr",
                "шифрование", "encryption", "аутентификация", "авторизация",
                "sql injection", "xss", "csrf", "secrets", "ключи"
            ],
            secondary_keywords=[
                "firewall", "ssl", "tls", "oauth", "2fa", "privacy",
                "data protection", "backup", "incident response"
            ],
            exclusions=[
                "дизайн", "аналитика", "контент", "психология",
                "производительность", "мобильная разработка"
            ]
        ),

        AgentType.UIUX_ENHANCEMENT: CompetencyArea(
            primary_keywords=[
                "дизайн", "ui", "ux", "пользовательский интерфейс", "usability",
                "accessibility", "a11y", "wireframe", "mockup", "prototype",
                "user experience", "пользовательский опыт", "figma", "sketch",
                "adobe xd", "компоненты", "design system", "дизайн система"
            ],
            secondary_keywords=[
                "цвета", "типография", "иконки", "анимация", "transitions",
                "responsive", "mobile first", "grid", "flexbox"
            ],
            exclusions=[
                "backend", "база данных", "безопасность", "аналитика",
                "производительность сервера", "devops"
            ]
        ),

        AgentType.PERFORMANCE_OPTIMIZATION: CompetencyArea(
            primary_keywords=[
                "производительность", "performance", "оптимизация", "optimization",
                "скорость", "speed", "memory", "cpu", "профилирование", "profiling",
                "кэширование", "caching", "load testing", "нагрузочное тестирование",
                "bottleneck", "узкое место", "scalability", "масштабируемость"
            ],
            secondary_keywords=[
                "bundle size", "tree shaking", "lazy loading", "code splitting",
                "cdn", "compression", "minification", "webpack optimization"
            ],
            exclusions=[
                "дизайн", "контент", "психология", "безопасность аудит",
                "пользовательский интерфейс", "аналитика"
            ]
        ),

        AgentType.PRISMA_DATABASE: CompetencyArea(
            primary_keywords=[
                "prisma", "база данных", "database", "sql", "postgresql", "mysql",
                "sqlite", "mongodb", "orm", "миграции", "migrations", "схема",
                "schema", "query", "запросы", "индексы", "indexes", "relations"
            ],
            secondary_keywords=[
                "crud", "transactions", "connection pool", "backup", "replication",
                "normalization", "denormalization", "triggers", "procedures"
            ],
            exclusions=[
                "фронтенд", "дизайн", "аналитика", "психология",
                "контент", "мобильная разработка"
            ]
        ),

        AgentType.TYPESCRIPT_ARCHITECTURE: CompetencyArea(
            primary_keywords=[
                "typescript", "архитектура", "architecture", "типизация", "types",
                "type safety", "interfaces", "generics", "decorators",
                "модули", "modules", "namespace", "рефакторинг", "refactoring",
                "code organization", "структура кода", "patterns", "паттерны"
            ],
            secondary_keywords=[
                "eslint", "prettier", "tsconfig", "compilation", "type checking",
                "strict mode", "utility types", "mapped types"
            ],
            exclusions=[
                "дизайн", "аналитика", "психология", "контент",
                "backend инфраструктура", "devops"
            ]
        ),

        AgentType.PWA_MOBILE: CompetencyArea(
            primary_keywords=[
                "pwa", "progressive web app", "мобильная разработка", "mobile",
                "service worker", "offline", "app manifest", "push notifications",
                "мобильная адаптация", "responsive", "touch", "gestures",
                "react native", "ionic", "cordova", "capacitor"
            ],
            secondary_keywords=[
                "app store", "play store", "hybrid app", "native app",
                "device api", "camera", "geolocation", "sensors"
            ],
            exclusions=[
                "backend", "безопасность", "аналитика", "психология",
                "контент", "база данных"
            ]
        ),

        AgentType.RAG_AGENT: CompetencyArea(
            primary_keywords=[
                "rag", "retrieval augmented generation", "поиск", "search",
                "семантический поиск", "semantic search", "vector database",
                "векторная база", "embeddings", "knowledge base", "база знаний",
                "document retrieval", "информационный поиск", "nlp", "llm"
            ],
            secondary_keywords=[
                "elasticsearch", "opensearch", "pinecone", "weaviate", "chroma",
                "faiss", "similarity search", "text processing", "chunking"
            ],
            exclusions=[
                "дизайн", "мобильная разработка", "devops", "безопасность аудит",
                "frontend архитектура", "payment"
            ]
        ),

        AgentType.PAYMENT_INTEGRATION: CompetencyArea(
            primary_keywords=[
                "платежи", "payment", "stripe", "paypal", "яндекс касса", "сбербанк",
                "billing", "биллинг", "subscription", "подписка", "checkout",
                "оплата", "эквайринг", "acquiring", "pci dss", "webhook"
            ],
            secondary_keywords=[
                "refund", "возврат", "invoice", "счет", "tax", "налоги",
                "currency", "валюта", "fraud detection", "chargeback"
            ],
            exclusions=[
                "дизайн", "аналитика", "психология", "контент",
                "мобильная разработка", "производительность"
            ]
        ),

        AgentType.QUEUE_WORKER: CompetencyArea(
            primary_keywords=[
                "очереди", "queue", "worker", "background jobs", "celery", "redis",
                "rabbitmq", "kafka", "асинхронные задачи", "async tasks",
                "job processing", "task scheduling", "cron", "scheduler"
            ],
            secondary_keywords=[
                "message broker", "pub/sub", "retry logic", "dead letter queue",
                "rate limiting", "backpressure", "monitoring"
            ],
            exclusions=[
                "дизайн", "аналитика", "психология", "контент",
                "пользовательский интерфейс", "мобильная разработка"
            ]
        ),

        AgentType.NLP_CONTENT_QUALITY: CompetencyArea(
            primary_keywords=[
                "nlp", "качество контента", "content quality", "text analysis",
                "анализ текста", "grammar", "грамматика", "style", "стиль",
                "readability", "читаемость", "sentiment", "tone", "тон"
            ],
            secondary_keywords=[
                "proofreading", "редактирование", "plagiarism", "плагиат",
                "fact checking", "проверка фактов", "content scoring"
            ],
            exclusions=[
                "backend", "database", "payment", "mobile", "security audit"
            ]
        ),

        AgentType.NLP_CONTENT_RESEARCH: CompetencyArea(
            primary_keywords=[
                "nlp", "исследования контента", "content research", "text mining",
                "data mining", "corpus analysis", "анализ корпуса", "topic modeling",
                "keyword research", "контент анализ", "trend analysis"
            ],
            secondary_keywords=[
                "web scraping", "data collection", "statistical analysis",
                "clustering", "classification", "information extraction"
            ],
            exclusions=[
                "ui design", "payment", "mobile development", "performance optimization"
            ]
        ),

        AgentType.PSYCHOLOGY_CONTENT_ARCHITECT: CompetencyArea(
            primary_keywords=[
                "психология", "psychology", "контент архитектура", "content architecture",
                "психологические тесты", "psychological tests", "когнитивная психология",
                "behavior analysis", "анализ поведения", "user psychology"
            ],
            secondary_keywords=[
                "personality tests", "тесты личности", "cognitive assessment",
                "behavioral patterns", "поведенческие паттерны", "psychology framework"
            ],
            exclusions=[
                "backend development", "database", "payment", "mobile", "security"
            ]
        )
    }
