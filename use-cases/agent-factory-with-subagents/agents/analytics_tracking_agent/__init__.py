# -*- coding: utf-8 -*-
"""
Universal Analytics & Tracking Agent

Универсальный агент для настройки, оптимизации и анализа систем аналитики
для различных типов проектов: веб-аналитика, e-commerce, SaaS, блоги и др.

Основные возможности:
- Настройка Google Analytics 4, Mixpanel, Amplitude, Segment
- Privacy-compliant tracking (GDPR/CCPA)
- Conversion funnel analysis
- User behavior analytics
- Custom dashboards
- Performance optimization

Примеры использования:
    # Веб-аналитика
    from analytics_tracking_agent import create_web_analytics_agent
    agent = create_web_analytics_agent()

    # E-commerce
    from analytics_tracking_agent import create_ecommerce_agent
    agent = create_ecommerce_agent()

    # SaaS метрики
    from analytics_tracking_agent import create_saas_agent
    agent = create_saas_agent()

    # Блог аналитика
    from analytics_tracking_agent import create_blog_agent
    agent = create_blog_agent()
"""

from .agent import (
    UniversalAnalyticsTrackingAgent,
    create_web_analytics_agent,
    create_ecommerce_agent,
    create_saas_agent,
    create_blog_agent
)

from .dependencies import AnalyticsTrackingDependencies, load_dependencies
from .settings import Settings, load_analytics_settings

__version__ = "1.0.0"
__author__ = "AI Agent Factory"

__all__ = [
    # Основной класс агента
    "UniversalAnalyticsTrackingAgent",

    # Фабричные функции
    "create_web_analytics_agent",
    "create_ecommerce_agent",
    "create_saas_agent",
    "create_blog_agent",

    # Зависимости и настройки
    "AnalyticsTrackingDependencies",
    "load_dependencies",
    "Settings",
    "load_analytics_settings"
]