# -*- coding: utf-8 -*-
"""
Настройки Analytics & Tracking Agent
Универсальная конфигурация для различных типов проектов
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import Optional, List

class Settings(BaseSettings):
    """Настройки агента аналитики с поддержкой различных провайдеров."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Основные настройки LLM
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API ключ провайдера")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Модель LLM")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Универсальная конфигурация проекта
    project_type: str = Field(
        default="web_analytics",
        description="Тип проекта: web_analytics, mobile_analytics, ecommerce_tracking, saas_metrics, content_analytics, blog_analytics"
    )
    domain_type: str = Field(
        default="analytics",
        description="Домен: analytics, tracking, experimentation, performance, attribution"
    )
    tracking_focus: str = Field(
        default="conversion",
        description="Фокус трекинга: conversion, engagement, retention, performance, revenue, user_journey"
    )

    # Google Analytics настройки
    ga4_measurement_id: Optional[str] = Field(None, description="Google Analytics 4 Measurement ID")
    ga4_api_secret: Optional[str] = Field(None, description="GA4 Measurement Protocol API Secret")
    universal_analytics_id: Optional[str] = Field(None, description="Universal Analytics Tracking ID")

    # Mixpanel настройки
    mixpanel_project_token: Optional[str] = Field(None, description="Mixpanel Project Token")
    mixpanel_api_key: Optional[str] = Field(None, description="Mixpanel API Key")
    mixpanel_api_secret: Optional[str] = Field(None, description="Mixpanel API Secret")

    # Amplitude настройки
    amplitude_api_key: Optional[str] = Field(None, description="Amplitude API Key")
    amplitude_secret_key: Optional[str] = Field(None, description="Amplitude Secret Key")

    # Segment настройки
    segment_write_key: Optional[str] = Field(None, description="Segment Write Key")

    # A/B Testing платформы
    optimizely_sdk_key: Optional[str] = Field(None, description="Optimizely SDK Key")
    google_optimize_id: Optional[str] = Field(None, description="Google Optimize Container ID")
    vwo_account_id: Optional[str] = Field(None, description="VWO Account ID")

    # Hotjar настройки
    hotjar_site_id: Optional[str] = Field(None, description="Hotjar Site ID")

    # Privacy и compliance
    gdpr_compliance: bool = Field(default=True, description="Включить GDPR compliance")
    ccpa_compliance: bool = Field(default=True, description="Включить CCPA compliance")
    anonymize_ip: bool = Field(default=True, description="Анонимизировать IP адреса")
    cookie_consent_required: bool = Field(default=True, description="Требовать согласие на cookies")

    # Производительность
    enable_batch_events: bool = Field(default=True, description="Батчевая отправка событий")
    batch_size: int = Field(default=50, description="Размер батча событий")
    flush_interval: int = Field(default=5000, description="Интервал отправки батчей (мс)")

    # Real-time dashboard
    enable_realtime_dashboard: bool = Field(default=False, description="Включить real-time dashboard")
    dashboard_update_interval: int = Field(default=30000, description="Интервал обновления dashboard (мс)")

    # Конфигурация по типу проекта
    enable_ecommerce_tracking: bool = Field(default=False, description="E-commerce трекинг")
    enable_content_tracking: bool = Field(default=False, description="Контент трекинг")
    enable_user_journey_mapping: bool = Field(default=False, description="User journey mapping")
    enable_cohort_analysis: bool = Field(default=False, description="Cohort анализ")

    # Custom events конфигурация
    custom_events_enabled: bool = Field(default=True, description="Кастомные события")
    max_custom_parameters: int = Field(default=25, description="Максимум custom параметров на событие")

    # API endpoints для получения данных
    analytics_api_base_url: str = Field(
        default="https://analyticsreporting.googleapis.com/v4",
        description="Base URL для Analytics API"
    )

def load_analytics_settings() -> Settings:
    """Загрузить настройки аналитики и проверить наличие переменных."""
    load_dotenv()

    try:
        return Settings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки аналитики: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e

def get_project_config(project_type: str, domain_type: str) -> dict:
    """
    Получить специфичную конфигурацию для типа проекта.

    Args:
        project_type: Тип проекта (web_analytics, ecommerce_tracking, etc.)
        domain_type: Домен (analytics, tracking, experimentation)

    Returns:
        Словарь с конфигурацией для данного типа проекта
    """

    configs = {
        "web_analytics": {
            "required_providers": ["google_analytics", "mixpanel"],
            "recommended_events": [
                "page_view", "session_start", "user_engagement",
                "scroll_depth", "file_download", "outbound_click"
            ],
            "key_metrics": [
                "sessions", "users", "pageviews", "bounce_rate",
                "avg_session_duration", "pages_per_session"
            ]
        },

        "ecommerce_tracking": {
            "required_providers": ["google_analytics", "mixpanel"],
            "recommended_events": [
                "view_item", "add_to_cart", "begin_checkout",
                "purchase", "refund", "view_promotion"
            ],
            "key_metrics": [
                "conversion_rate", "average_order_value", "revenue",
                "cart_abandonment_rate", "customer_lifetime_value"
            ]
        },

        "saas_metrics": {
            "required_providers": ["mixpanel", "amplitude"],
            "recommended_events": [
                "signup", "activation", "feature_used", "subscription_started",
                "subscription_cancelled", "upgrade", "downgrade"
            ],
            "key_metrics": [
                "monthly_active_users", "churn_rate", "activation_rate",
                "feature_adoption", "time_to_value", "net_revenue_retention"
            ]
        },

        "mobile_analytics": {
            "required_providers": ["mixpanel", "amplitude"],
            "recommended_events": [
                "app_open", "screen_view", "app_update", "push_notification_received",
                "in_app_purchase", "crash", "custom_event"
            ],
            "key_metrics": [
                "daily_active_users", "session_length", "retention_rate",
                "app_crashes", "push_notification_open_rate"
            ]
        },

        "content_analytics": {
            "required_providers": ["google_analytics", "mixpanel"],
            "recommended_events": [
                "article_view", "video_play", "social_share",
                "comment_posted", "subscription", "newsletter_signup"
            ],
            "key_metrics": [
                "content_engagement", "time_on_page", "social_shares",
                "subscriber_growth", "content_performance_score"
            ]
        },

        "blog_analytics": {
            "required_providers": ["google_analytics"],
            "recommended_events": [
                "post_view", "comment", "share", "newsletter_signup",
                "author_follow", "category_view"
            ],
            "key_metrics": [
                "unique_visitors", "returning_visitors", "post_engagement",
                "subscriber_conversion", "author_popularity"
            ]
        }
    }

    return configs.get(project_type, {
        "required_providers": ["google_analytics"],
        "recommended_events": ["page_view", "user_engagement"],
        "key_metrics": ["sessions", "users", "pageviews"]
    })

def get_privacy_config(gdpr_enabled: bool = True, ccpa_enabled: bool = True) -> dict:
    """
    Получить конфигурацию privacy compliance.

    Args:
        gdpr_enabled: Включить GDPR compliance
        ccpa_enabled: Включить CCPA compliance

    Returns:
        Конфигурация privacy settings
    """

    config = {
        "consent_required": gdpr_enabled or ccpa_enabled,
        "anonymize_ip": True,
        "data_retention_days": 26 if gdpr_enabled else 50,  # GDPR требует 26 месяцев max
        "allow_personalization": False,  # По умолчанию выключено до получения согласия
        "cookie_settings": {
            "necessary": True,  # Всегда разрешены
            "analytics": False,  # Требует согласия
            "marketing": False,  # Требует согласия
            "personalization": False  # Требует согласия
        }
    }

    if gdpr_enabled:
        config.update({
            "gdpr_consent_text": "Мы используем cookies и аналитику для улучшения работы сайта. Нажимая 'Принять', вы соглашаетесь на обработку данных.",
            "data_processing_basis": "consent",  # или "legitimate_interest"
            "right_to_deletion": True,
            "data_portability": True
        })

    if ccpa_enabled:
        config.update({
            "ccpa_opt_out_available": True,
            "do_not_sell_link": True,
            "california_consumer_rights": True
        })

    return config