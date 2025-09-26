# -*- coding: utf-8 -*-
"""
Зависимости Analytics & Tracking Agent
Универсальная система зависимостей с поддержкой различных analytics провайдеров
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from .settings import Settings, load_analytics_settings, get_project_config, get_privacy_config

# Матрица компетенций для межагентного взаимодействия
AGENT_COMPETENCIES = {
    "performance_optimization": [
        "производительность", "core web vitals", "loading speed", "optimization",
        "performance metrics", "page speed", "bundle size"
    ],
    "security_audit": [
        "безопасность", "privacy", "gdpr", "ccpa", "data protection",
        "compliance", "security", "vulnerability"
    ],
    "uiux_enhancement": [
        "пользовательский опыт", "conversion optimization", "user journey",
        "interface", "usability", "accessibility", "design"
    ]
}

AGENT_ASSIGNEE_MAP = {
    "performance_optimization": "Performance Optimization Agent",
    "security_audit": "Security Audit Agent",
    "uiux_enhancement": "UI/UX Enhancement Agent"
}

@dataclass
class AnalyticsTrackingDependencies:
    """
    Универсальные зависимости для Analytics & Tracking Agent.
    Поддерживает различные analytics провайдеры и типы проектов.
    """

    # Основные настройки
    settings: Settings
    project_path: str = ""

    # Универсальная конфигурация
    domain_type: str = "analytics"  # analytics, tracking, experimentation, performance
    project_type: str = "web_analytics"  # web_analytics, ecommerce_tracking, saas_metrics, etc.
    tracking_focus: str = "conversion"  # conversion, engagement, retention, revenue

    # Analytics провайдеры (конфигурируемые)
    analytics_providers: List[str] = field(default_factory=lambda: ["google_analytics"])
    primary_provider: str = "google_analytics"

    # Межагентное взаимодействие
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
    enable_task_delegation: bool = True
    agent_name: str = "analytics_tracking_agent"

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "analytics-tracking", "agent-knowledge", "pydantic-ai",
        "google-analytics", "mixpanel", "privacy-compliance"
    ])
    knowledge_domain: str = "analytics.google.com"

    # Privacy и compliance настройки
    privacy_config: Dict[str, Any] = field(default_factory=dict)
    gdpr_enabled: bool = True
    ccpa_enabled: bool = True

    # Производительность
    enable_batch_processing: bool = True
    batch_size: int = 50
    async_processing: bool = True

    # Конфигурация провайдеров
    provider_configs: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация дополнительных настроек на основе конфигурации."""

        # Загружаем конфигурацию для типа проекта
        project_config = get_project_config(self.project_type, self.domain_type)

        # Устанавливаем рекомендуемые провайдеры
        if not self.analytics_providers:
            self.analytics_providers = project_config.get("required_providers", ["google_analytics"])

        # Конфигурируем privacy настройки
        if not self.privacy_config:
            self.privacy_config = get_privacy_config(self.gdpr_enabled, self.ccpa_enabled)

        # Инициализируем конфигурации провайдеров
        self._init_provider_configs()

        # Обновляем knowledge tags на основе проекта
        self._update_knowledge_tags()

    def _init_provider_configs(self):
        """Инициализация конфигураций для различных провайдеров."""

        for provider in self.analytics_providers:
            if provider == "google_analytics":
                self.provider_configs["google_analytics"] = {
                    "measurement_id": getattr(self.settings, "ga4_measurement_id", None),
                    "api_secret": getattr(self.settings, "ga4_api_secret", None),
                    "universal_id": getattr(self.settings, "universal_analytics_id", None),
                    "enhanced_ecommerce": self.project_type == "ecommerce_tracking",
                    "anonymize_ip": self.settings.anonymize_ip,
                    "allow_personalization": not self.privacy_config.get("consent_required", True)
                }

            elif provider == "mixpanel":
                self.provider_configs["mixpanel"] = {
                    "project_token": getattr(self.settings, "mixpanel_project_token", None),
                    "api_key": getattr(self.settings, "mixpanel_api_key", None),
                    "api_secret": getattr(self.settings, "mixpanel_api_secret", None),
                    "batch_requests": self.enable_batch_processing,
                    "track_revenue": self.tracking_focus in ["revenue", "conversion"]
                }

            elif provider == "amplitude":
                self.provider_configs["amplitude"] = {
                    "api_key": getattr(self.settings, "amplitude_api_key", None),
                    "secret_key": getattr(self.settings, "amplitude_secret_key", None),
                    "batch_mode": self.enable_batch_processing,
                    "session_timeout": 30  # минуты
                }

            elif provider == "segment":
                self.provider_configs["segment"] = {
                    "write_key": getattr(self.settings, "segment_write_key", None),
                    "batch_size": self.batch_size,
                    "enable_destinations": True
                }

    def _update_knowledge_tags(self):
        """Обновление knowledge tags на основе типа проекта."""

        # Добавляем теги специфичные для проекта
        project_tags = {
            "ecommerce_tracking": ["ecommerce", "conversion-tracking", "revenue-analytics"],
            "saas_metrics": ["saas", "subscription", "user-engagement", "churn-analysis"],
            "mobile_analytics": ["mobile", "app-analytics", "user-retention"],
            "content_analytics": ["content", "engagement", "social-media"],
            "web_analytics": ["web", "traffic", "user-behavior"]
        }

        if self.project_type in project_tags:
            self.knowledge_tags.extend(project_tags[self.project_type])

        # Добавляем теги провайдеров
        provider_tags = {
            "google_analytics": ["google-analytics", "ga4"],
            "mixpanel": ["mixpanel", "event-tracking"],
            "amplitude": ["amplitude", "user-analytics"],
            "segment": ["segment", "cdp"]
        }

        for provider in self.analytics_providers:
            if provider in provider_tags:
                self.knowledge_tags.extend(provider_tags[provider])

        # Убираем дубликаты
        self.knowledge_tags = list(set(self.knowledge_tags))

    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """
        Получить конфигурацию для конкретного провайдера.

        Args:
            provider_name: Название провайдера analytics

        Returns:
            Конфигурация провайдера
        """
        return self.provider_configs.get(provider_name, {})

    def is_provider_enabled(self, provider_name: str) -> bool:
        """
        Проверить включен ли провайдер.

        Args:
            provider_name: Название провайдера

        Returns:
            True если провайдер включен и настроен
        """
        if provider_name not in self.analytics_providers:
            return False

        config = self.get_provider_config(provider_name)

        # Проверяем наличие обязательных ключей для провайдера
        required_keys = {
            "google_analytics": ["measurement_id"],
            "mixpanel": ["project_token"],
            "amplitude": ["api_key"],
            "segment": ["write_key"]
        }

        if provider_name in required_keys:
            return all(config.get(key) for key in required_keys[provider_name])

        return True

    def get_recommended_events(self) -> List[str]:
        """
        Получить рекомендуемые события для текущего типа проекта.

        Returns:
            Список рекомендуемых событий
        """
        project_config = get_project_config(self.project_type, self.domain_type)
        return project_config.get("recommended_events", [])

    def get_key_metrics(self) -> List[str]:
        """
        Получить ключевые метрики для текущего типа проекта.

        Returns:
            Список ключевых метрик
        """
        project_config = get_project_config(self.project_type, self.domain_type)
        return project_config.get("key_metrics", [])

    def should_delegate(self, task_keywords: List[str]) -> Optional[str]:
        """
        Определить нужно ли делегировать задачу и кому.

        Args:
            task_keywords: Ключевые слова задачи

        Returns:
            Название агента для делегирования или None
        """
        if not self.enable_task_delegation:
            return None

        task_keywords_lower = [kw.lower() for kw in task_keywords]

        for agent_type, competencies in AGENT_COMPETENCIES.items():
            overlap = set(task_keywords_lower) & set(competencies)
            if len(overlap) >= 2:  # Значительное пересечение компетенций
                return agent_type

        return None

    def get_privacy_compliance_requirements(self) -> Dict[str, Any]:
        """
        Получить требования privacy compliance для текущей конфигурации.

        Returns:
            Требования privacy compliance
        """
        requirements = {
            "consent_required": self.privacy_config.get("consent_required", False),
            "anonymize_data": True,
            "data_retention_limit": self.privacy_config.get("data_retention_days", 26),
            "user_rights": []
        }

        if self.gdpr_enabled:
            requirements["user_rights"].extend([
                "right_to_access",
                "right_to_deletion",
                "right_to_portability",
                "right_to_rectification"
            ])

        if self.ccpa_enabled:
            requirements["user_rights"].extend([
                "right_to_know",
                "right_to_delete",
                "right_to_opt_out"
            ])

        return requirements

def load_dependencies() -> AnalyticsTrackingDependencies:
    """
    Загрузить зависимости Analytics & Tracking Agent.

    Returns:
        Настроенные зависимости агента
    """
    settings = load_analytics_settings()

    return AnalyticsTrackingDependencies(
        settings=settings,
        domain_type=settings.domain_type,
        project_type=settings.project_type,
        tracking_focus=settings.tracking_focus,
        gdpr_enabled=settings.gdpr_compliance,
        ccpa_enabled=settings.ccpa_compliance,
        enable_batch_processing=settings.enable_batch_events,
        batch_size=settings.batch_size
    )