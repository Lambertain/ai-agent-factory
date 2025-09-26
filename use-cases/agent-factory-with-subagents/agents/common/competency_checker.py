# -*- coding: utf-8 -*-
"""
Модуль контроля компетенций агентов.

Определяет границы экспертизы каждого агента и автоматически
делегирует задачи соответствующим специалистам через Archon.
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


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


@dataclass
class CompetencyArea:
    """Область компетенции агента."""
    primary_keywords: List[str]  # Ключевые слова основной экспертизы
    secondary_keywords: List[str]  # Смежные области
    exclusions: List[str]  # Что точно НЕ входит в компетенцию
    confidence_threshold: float = 0.7  # Минимальная уверенность для принятия задачи


@dataclass
class CompetencyResult:
    """Результат проверки компетенции."""
    can_handle: bool
    confidence: float
    reason: str
    suggested_agent: Optional[str] = None
    delegation_priority: str = "medium"  # low, medium, high, critical


class CompetencyChecker:
    """Система проверки компетенций агентов."""

    def __init__(self):
        """Инициализация с матрицей компетенций."""
        self.competency_matrix = self._build_competency_matrix()
        self.delegation_matrix = self._build_delegation_matrix()

    def _build_competency_matrix(self) -> Dict[AgentType, CompetencyArea]:
        """Построить матрицу компетенций для всех агентов."""
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

            # Добавим компетенции для NLP агентов
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

            # Компетенции агентов психологии
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

    def _build_delegation_matrix(self) -> Dict[str, List[str]]:
        """Построить матрицу делегирования задач между агентами."""
        return {
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

    def check_competency(
        self,
        task_description: str,
        agent_type: AgentType,
        context: Optional[Dict[str, Any]] = None
    ) -> CompetencyResult:
        """
        Проверить может ли агент выполнить задачу.

        Args:
            task_description: Описание задачи
            agent_type: Тип агента
            context: Дополнительный контекст

        Returns:
            Результат проверки компетенции
        """
        if agent_type not in self.competency_matrix:
            return CompetencyResult(
                can_handle=False,
                confidence=0.0,
                reason=f"Неизвестный тип агента: {agent_type}",
                suggested_agent="archon_analysis_lead"
            )

        competency = self.competency_matrix[agent_type]

        # Анализируем задачу
        task_lower = task_description.lower()

        # Проверяем исключения (что точно НЕ может делать)
        exclusion_matches = self._count_keyword_matches(task_lower, competency.exclusions)
        if exclusion_matches > 0:
            suggested_agent = self._find_suggested_agent(task_description)
            return CompetencyResult(
                can_handle=False,
                confidence=0.0,
                reason=f"Задача содержит области вне компетенции агента: {exclusion_matches} исключающих ключевых слов",
                suggested_agent=suggested_agent,
                delegation_priority="high"
            )

        # Проверяем основные компетенции
        primary_matches = self._count_keyword_matches(task_lower, competency.primary_keywords)
        secondary_matches = self._count_keyword_matches(task_lower, competency.secondary_keywords)

        # Вычисляем уверенность
        total_keywords = len(competency.primary_keywords) + len(competency.secondary_keywords)
        confidence = (primary_matches * 2 + secondary_matches) / max(total_keywords, 1)
        confidence = min(confidence, 1.0)  # Ограничиваем максимум

        can_handle = confidence >= competency.confidence_threshold

        if not can_handle:
            suggested_agent = self._find_suggested_agent(task_description)
            return CompetencyResult(
                can_handle=False,
                confidence=confidence,
                reason=f"Низкая уверенность ({confidence:.2f}) для выполнения задачи. Требуется {competency.confidence_threshold:.2f}",
                suggested_agent=suggested_agent,
                delegation_priority="medium" if confidence > 0.3 else "high"
            )

        return CompetencyResult(
            can_handle=True,
            confidence=confidence,
            reason=f"Агент компетентен для выполнения задачи (уверенность: {confidence:.2f})"
        )

    def _count_keyword_matches(self, text: str, keywords: List[str]) -> int:
        """Подсчитать количество совпадений ключевых слов в тексте."""
        matches = 0
        for keyword in keywords:
            if keyword.lower() in text:
                matches += 1
        return matches

    def _find_suggested_agent(self, task_description: str) -> str:
        """Найти наиболее подходящего агента для задачи."""
        task_lower = task_description.lower()
        best_agent = "archon_analysis_lead"  # По умолчанию
        best_score = 0

        for agent_type, competency in self.competency_matrix.items():
            # Не рекомендуем агента, если задача содержит исключения
            exclusion_matches = self._count_keyword_matches(task_lower, competency.exclusions)
            if exclusion_matches > 0:
                continue

            # Считаем соответствие
            primary_matches = self._count_keyword_matches(task_lower, competency.primary_keywords)
            secondary_matches = self._count_keyword_matches(task_lower, competency.secondary_keywords)

            score = primary_matches * 2 + secondary_matches

            if score > best_score:
                best_score = score
                best_agent = agent_type.value

        return best_agent

    def get_delegation_suggestions(self, agent_type: AgentType) -> List[str]:
        """Получить список агентов, которым можно делегировать задачи."""
        agent_name = agent_type.value
        return self.delegation_matrix.get(agent_name, [])

    def should_escalate_to_project_manager(
        self,
        task_description: str,
        confidence: float
    ) -> Tuple[bool, str]:
        """
        Определить нужно ли эскалировать задачу к Project Manager.

        Args:
            task_description: Описание задачи
            confidence: Уверенность в компетенции

        Returns:
            (нужна ли эскалация, причина)
        """
        task_lower = task_description.lower()

        # Ключевые слова, требующие вмешательства PM
        pm_keywords = [
            "приоритет", "priority", "срочно", "urgent", "критично", "critical",
            "планирование", "planning", "координация", "coordination",
            "ресурсы", "resources", "команда", "team", "deadline",
            "проект", "project", "milestone", "этап", "roadmap"
        ]

        pm_matches = self._count_keyword_matches(task_lower, pm_keywords)

        # Эскалация нужна если:
        # 1. Найдены PM ключевые слова
        # 2. Очень низкая уверенность (< 0.3)
        # 3. Задача содержит слова "все агенты", "команда", "координация"

        if pm_matches > 0:
            return True, f"Задача содержит управленческие аспекты ({pm_matches} ключевых слов)"

        if confidence < 0.3:
            return True, f"Слишком низкая уверенность ({confidence:.2f}) - требуется анализ PM"

        coordination_keywords = ["все агенты", "команда агентов", "координация", "оркестрация"]
        if any(keyword in task_lower for keyword in coordination_keywords):
            return True, "Задача требует координации между несколькими агентами"

        return False, ""


def check_task_competency(
    task_description: str,
    agent_type_name: str,
    context: Optional[Dict[str, Any]] = None
) -> CompetencyResult:
    """
    Универсальная функция проверки компетенции для любого агента.

    Args:
        task_description: Описание задачи
        agent_type_name: Имя типа агента (например, "analytics_tracking_agent")
        context: Дополнительный контекст

    Returns:
        Результат проверки компетенции
    """
    try:
        # Находим соответствующий enum
        agent_type = None
        for at in AgentType:
            if at.value == agent_type_name:
                agent_type = at
                break

        if agent_type is None:
            return CompetencyResult(
                can_handle=False,
                confidence=0.0,
                reason=f"Неизвестный тип агента: {agent_type_name}",
                suggested_agent="archon_analysis_lead"
            )

        checker = CompetencyChecker()
        return checker.check_competency(task_description, agent_type, context)

    except Exception as e:
        return CompetencyResult(
            can_handle=False,
            confidence=0.0,
            reason=f"Ошибка проверки компетенции: {e}",
            suggested_agent="archon_analysis_lead"
        )


def should_delegate_task(
    task_description: str,
    current_agent_type: str,
    confidence_threshold: float = 0.7
) -> Tuple[bool, Optional[str], str]:
    """
    Определить нужно ли делегировать задачу другому агенту.

    Args:
        task_description: Описание задачи
        current_agent_type: Тип текущего агента
        confidence_threshold: Порог уверенности

    Returns:
        (нужно ли делегировать, кому делегировать, причина)
    """
    result = check_task_competency(task_description, current_agent_type)

    if not result.can_handle:
        return True, result.suggested_agent, result.reason

    if result.confidence < confidence_threshold:
        return True, result.suggested_agent, f"Низкая уверенность: {result.confidence:.2f}"

    return False, None, f"Агент компетентен: {result.confidence:.2f}"


# Экспорт для других модулей
__all__ = [
    'CompetencyChecker',
    'CompetencyResult',
    'CompetencyArea',
    'AgentType',
    'check_task_competency',
    'should_delegate_task'
]