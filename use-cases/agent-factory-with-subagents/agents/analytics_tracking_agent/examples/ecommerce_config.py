# -*- coding: utf-8 -*-
"""
Пример конфигурации Analytics & Tracking Agent для E-commerce проектов
Настроен для интернет-магазинов с полным отслеживанием покупательского пути
"""

import os
from ..settings import Settings
from ..dependencies import AnalyticsTrackingDependencies

def get_ecommerce_config() -> AnalyticsTrackingDependencies:
    """
    Конфигурация агента для E-commerce проектов.

    Включает:
    - Enhanced E-commerce tracking
    - Revenue attribution
    - Cart abandonment analysis
    - Customer lifetime value tracking
    - Product performance analytics
    """

    # Настройки для e-commerce
    settings = Settings(
        # Основные настройки LLM
        llm_api_key=os.getenv("LLM_API_KEY", "your-llm-api-key"),

        # Тип проекта
        project_type="ecommerce_tracking",
        domain_type="analytics",
        tracking_focus="conversion",

        # Google Analytics 4 с Enhanced E-commerce
        ga4_measurement_id=os.getenv("GA4_MEASUREMENT_ID", "G-XXXXXXXXXX"),
        ga4_api_secret=os.getenv("GA4_API_SECRET"),

        # Mixpanel для детального event tracking
        mixpanel_project_token=os.getenv("MIXPANEL_TOKEN"),
        mixpanel_api_key=os.getenv("MIXPANEL_API_KEY"),

        # E-commerce специфичные настройки
        enable_ecommerce_tracking=True,
        enable_cohort_analysis=True,

        # Privacy compliance для e-commerce
        gdpr_compliance=True,
        ccpa_compliance=True,
        anonymize_ip=True,
        cookie_consent_required=True,

        # Performance настройки
        enable_batch_events=True,
        batch_size=25,  # Меньший batch для e-commerce событий
        flush_interval=3000  # Быстрая отправка для покупок
    )

    return AnalyticsTrackingDependencies(
        settings=settings,
        domain_type="analytics",
        project_type="ecommerce_tracking",
        tracking_focus="conversion",

        # E-commerce провайдеры
        analytics_providers=["google_analytics", "mixpanel"],
        primary_provider="google_analytics",

        # Специализированные knowledge tags
        knowledge_tags=[
            "analytics-tracking", "agent-knowledge", "pydantic-ai",
            "ecommerce", "conversion-tracking", "revenue-analytics",
            "enhanced-ecommerce", "google-analytics", "mixpanel",
            "cart-abandonment", "customer-lifetime-value"
        ],

        # E-commerce оптимизации
        enable_batch_processing=True,
        batch_size=25,
        gdpr_enabled=True,
        ccpa_enabled=True
    )

# Пример событий для E-commerce
ECOMMERCE_EVENTS = {
    "view_item": {
        "description": "Просмотр товара",
        "parameters": ["item_id", "item_name", "item_category", "value", "currency"],
        "example": {
            "item_id": "SKU_12345",
            "item_name": "Wireless Headphones",
            "item_category": "Electronics",
            "value": 99.99,
            "currency": "USD"
        }
    },

    "add_to_cart": {
        "description": "Добавление в корзину",
        "parameters": ["item_id", "item_name", "item_category", "value", "currency", "quantity"],
        "example": {
            "item_id": "SKU_12345",
            "item_name": "Wireless Headphones",
            "item_category": "Electronics",
            "value": 99.99,
            "currency": "USD",
            "quantity": 1
        }
    },

    "begin_checkout": {
        "description": "Начало оформления заказа",
        "parameters": ["value", "currency", "items", "coupon"],
        "example": {
            "value": 199.98,
            "currency": "USD",
            "items": [{"item_id": "SKU_12345", "quantity": 2}],
            "coupon": "SUMMER2024"
        }
    },

    "purchase": {
        "description": "Завершение покупки",
        "parameters": ["transaction_id", "value", "currency", "items", "shipping", "tax"],
        "example": {
            "transaction_id": "T_12345",
            "value": 219.98,
            "currency": "USD",
            "items": [{"item_id": "SKU_12345", "quantity": 2}],
            "shipping": 9.99,
            "tax": 10.01
        }
    },

    "refund": {
        "description": "Возврат покупки",
        "parameters": ["transaction_id", "value", "currency"],
        "example": {
            "transaction_id": "T_12345",
            "value": 99.99,
            "currency": "USD"
        }
    }
}

# KPI для E-commerce
ECOMMERCE_KPIS = {
    "conversion_rate": {
        "name": "Conversion Rate",
        "description": "Процент посетителей, совершивших покупку",
        "formula": "Transactions / Sessions * 100",
        "target": "> 2%"
    },

    "average_order_value": {
        "name": "Average Order Value (AOV)",
        "description": "Средняя стоимость заказа",
        "formula": "Revenue / Number of Transactions",
        "target": "Рост месяц к месяцу"
    },

    "cart_abandonment_rate": {
        "name": "Cart Abandonment Rate",
        "description": "Процент брошенных корзин",
        "formula": "(Carts Created - Transactions) / Carts Created * 100",
        "target": "< 70%"
    },

    "customer_lifetime_value": {
        "name": "Customer Lifetime Value (CLV)",
        "description": "Общая стоимость клиента за весь период",
        "formula": "AOV * Purchase Frequency * Customer Lifespan",
        "target": "Максимизация"
    },

    "revenue_per_visitor": {
        "name": "Revenue per Visitor (RPV)",
        "description": "Доход на одного посетителя",
        "formula": "Total Revenue / Total Visitors",
        "target": "Рост квартал к кварталу"
    }
}

# Сегменты пользователей для E-commerce
USER_SEGMENTS = {
    "new_customers": {
        "description": "Новые покупатели (первая покупка)",
        "criteria": "Transaction count = 1",
        "marketing_focus": "Onboarding, продукт satisfaction"
    },

    "repeat_customers": {
        "description": "Повторные покупатели",
        "criteria": "Transaction count > 1",
        "marketing_focus": "Loyalty programs, cross-selling"
    },

    "high_value_customers": {
        "description": "Высокоценные клиенты",
        "criteria": "CLV > 90th percentile",
        "marketing_focus": "VIP treatment, premium products"
    },

    "at_risk_customers": {
        "description": "Клиенты в риске оттока",
        "criteria": "No purchase in last 90 days + Previous regular buyer",
        "marketing_focus": "Win-back campaigns, special offers"
    },

    "cart_abandoners": {
        "description": "Пользователи с брошенными корзинами",
        "criteria": "Added to cart but no purchase in last 24 hours",
        "marketing_focus": "Remarketing, cart recovery emails"
    }
}

def get_ecommerce_setup_guide():
    """Руководство по настройке E-commerce аналитики."""

    return """
# 🛒 E-commerce Analytics Setup Guide

## 1. ОБЯЗАТЕЛЬНАЯ НАСТРОЙКА

### Google Analytics 4 Enhanced E-commerce:
```javascript
gtag('config', 'GA_MEASUREMENT_ID', {
    enhanced_ecommerce: true,
    custom_map: {
        'customer_type': 'new_vs_returning',
        'product_category': 'item_category'
    }
});
```

### Mixpanel E-commerce Events:
```javascript
// Отслеживание покупки с revenue
mixpanel.track('Order Completed', {
    'Order Value': 199.99,
    'Product Categories': ['Electronics', 'Audio'],
    'Payment Method': 'Credit Card',
    'Customer Type': 'Returning'
});

mixpanel.people.track_charge(199.99, {
    'Order ID': 'T_12345',
    'Products': 2
});
```

## 2. КЛЮЧЕВЫЕ СОБЫТИЯ ДЛЯ ОТСЛЕЖИВАНИЯ

- ✅ view_item - просмотр товара
- ✅ add_to_cart - добавление в корзину
- ✅ remove_from_cart - удаление из корзины
- ✅ begin_checkout - начало оформления
- ✅ add_payment_info - добавление способа оплаты
- ✅ add_shipping_info - добавление адреса доставки
- ✅ purchase - завершение покупки
- ✅ refund - возврат

## 3. ДАШБОРДЫ И ОТЧЕТЫ

### Основные метрики:
- Conversion Rate по источникам трафика
- Average Order Value по категориям
- Cart Abandonment Rate по этапам
- Customer Lifetime Value по сегментам
- Revenue Attribution по каналам

### Воронка E-commerce:
1. Product Page View
2. Add to Cart
3. Begin Checkout
4. Payment Info
5. Purchase

## 4. АВТОМАТИЧЕСКИЕ СЕГМЕНТЫ

- Новые vs Возвращающиеся покупатели
- Высокоценные клиенты (top 10% по CLV)
- Клиенты в риске оттока
- Активные корзины (последние 24 часа)

## 5. PRIVACY COMPLIANCE

- ✅ Cookie consent для tracking
- ✅ GDPR compliance для EU клиентов
- ✅ CCPA compliance для California
- ✅ Anonymized IP addresses
- ✅ Data retention policies

## 6. ИНТЕГРАЦИИ

- CRM система для customer data
- Email marketing для abandoned carts
- Inventory management для product data
- Customer support для refund tracking
"""

if __name__ == "__main__":
    # Пример использования
    config = get_ecommerce_config()
    print("E-commerce конфигурация создана:")
    print(f"- Тип проекта: {config.project_type}")
    print(f"- Analytics провайдеры: {config.analytics_providers}")
    print(f"- Ключевые метрики: {config.get_key_metrics()}")
    print(f"- Рекомендуемые события: {config.get_recommended_events()}")