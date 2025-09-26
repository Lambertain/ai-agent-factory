# -*- coding: utf-8 -*-
"""
Пример конфигурации Analytics & Tracking Agent для SaaS проектов
Настроен для программных продуктов с подписочной моделью и отслеживанием пользовательской активности
"""

import os
from ..settings import Settings
from ..dependencies import AnalyticsTrackingDependencies

def get_saas_config() -> AnalyticsTrackingDependencies:
    """
    Конфигурация агента для SaaS проектов.

    Включает:
    - User activation и onboarding tracking
    - Feature usage и adoption analytics
    - Subscription lifecycle tracking
    - Churn prediction и retention analysis
    - Product-led growth metrics
    """

    # Настройки для SaaS
    settings = Settings(
        # Основные настройки LLM
        llm_api_key=os.getenv("LLM_API_KEY", "your-llm-api-key"),

        # Тип проекта
        project_type="saas_metrics",
        domain_type="analytics",
        tracking_focus="engagement",

        # Mixpanel для detailed event tracking и cohorts
        mixpanel_project_token=os.getenv("MIXPANEL_TOKEN"),
        mixpanel_api_key=os.getenv("MIXPANEL_API_KEY"),

        # Amplitude для user behavior analytics
        amplitude_api_key=os.getenv("AMPLITUDE_API_KEY"),
        amplitude_secret_key=os.getenv("AMPLITUDE_SECRET_KEY"),

        # Google Analytics для web traffic (если есть web версия)
        ga4_measurement_id=os.getenv("GA4_MEASUREMENT_ID", "G-XXXXXXXXXX"),
        ga4_api_secret=os.getenv("GA4_API_SECRET"),

        # SaaS специфичные настройки
        enable_cohort_analysis=True,
        enable_user_journey_mapping=True,

        # Privacy compliance для SaaS
        gdpr_compliance=True,
        ccpa_compliance=True,
        anonymize_ip=True,
        cookie_consent_required=True,

        # Performance настройки
        enable_batch_events=True,
        batch_size=30,  # Средний batch для SaaS событий
        flush_interval=4000  # Средняя скорость отправки для пользовательских действий
    )

    return AnalyticsTrackingDependencies(
        settings=settings,
        domain_type="analytics",
        project_type="saas_metrics",
        tracking_focus="engagement",

        # SaaS провайдеры
        analytics_providers=["mixpanel", "amplitude", "google_analytics"],
        primary_provider="mixpanel",

        # Специализированные knowledge tags
        knowledge_tags=[
            "analytics-tracking", "agent-knowledge", "pydantic-ai",
            "saas", "user-engagement", "product-analytics",
            "mixpanel", "amplitude", "subscription-metrics",
            "churn-analysis", "activation-tracking", "feature-adoption"
        ],

        # SaaS оптимизации
        enable_batch_processing=True,
        batch_size=30,
        gdpr_enabled=True,
        ccpa_enabled=True
    )

# Пример событий для SaaS
SAAS_EVENTS = {
    "signup": {
        "description": "Регистрация нового пользователя",
        "parameters": ["user_id", "email", "signup_method", "utm_source", "utm_campaign"],
        "example": {
            "user_id": "user_12345",
            "email": "user@example.com",
            "signup_method": "google_oauth",
            "utm_source": "google",
            "utm_campaign": "product_launch"
        }
    },

    "activation": {
        "description": "Активация пользователя (ключевое действие)",
        "parameters": ["user_id", "activation_event", "time_to_activation", "onboarding_step"],
        "example": {
            "user_id": "user_12345",
            "activation_event": "first_project_created",
            "time_to_activation": 180,  # секунд
            "onboarding_step": "project_setup"
        }
    },

    "feature_used": {
        "description": "Использование функции продукта",
        "parameters": ["user_id", "feature_name", "feature_category", "usage_context", "subscription_tier"],
        "example": {
            "user_id": "user_12345",
            "feature_name": "advanced_analytics",
            "feature_category": "analytics",
            "usage_context": "dashboard",
            "subscription_tier": "pro"
        }
    },

    "subscription_started": {
        "description": "Начало подписки",
        "parameters": ["user_id", "plan_name", "billing_cycle", "price", "currency", "trial_used"],
        "example": {
            "user_id": "user_12345",
            "plan_name": "pro_monthly",
            "billing_cycle": "monthly",
            "price": 29.99,
            "currency": "USD",
            "trial_used": True
        }
    },

    "subscription_cancelled": {
        "description": "Отмена подписки",
        "parameters": ["user_id", "plan_name", "cancellation_reason", "tenure_days", "retention_attempt"],
        "example": {
            "user_id": "user_12345",
            "plan_name": "pro_monthly",
            "cancellation_reason": "too_expensive",
            "tenure_days": 45,
            "retention_attempt": "discount_offered"
        }
    },

    "upgrade": {
        "description": "Повышение тарифного плана",
        "parameters": ["user_id", "from_plan", "to_plan", "upgrade_trigger", "mrr_change"],
        "example": {
            "user_id": "user_12345",
            "from_plan": "starter",
            "to_plan": "pro",
            "upgrade_trigger": "feature_limit_reached",
            "mrr_change": 20.00
        }
    },

    "downgrade": {
        "description": "Понижение тарифного плана",
        "parameters": ["user_id", "from_plan", "to_plan", "downgrade_reason", "mrr_change"],
        "example": {
            "user_id": "user_12345",
            "from_plan": "pro",
            "to_plan": "starter",
            "downgrade_reason": "reduced_usage",
            "mrr_change": -20.00
        }
    }
}

# KPI для SaaS
SAAS_KPIS = {
    "monthly_active_users": {
        "name": "Monthly Active Users (MAU)",
        "description": "Количество активных пользователей за месяц",
        "formula": "Unique Users with activity in last 30 days",
        "target": "Рост месяц к месяцу ≥ 5%"
    },

    "activation_rate": {
        "name": "Activation Rate",
        "description": "Процент пользователей, достигших ключевого действия",
        "formula": "Activated Users / Total Signups * 100",
        "target": "> 25%"
    },

    "churn_rate": {
        "name": "Monthly Churn Rate",
        "description": "Процент пользователей, отказавшихся от подписки за месяц",
        "formula": "Churned Users / Total Users at Month Start * 100",
        "target": "< 5% (для SaaS B2B)"
    },

    "net_revenue_retention": {
        "name": "Net Revenue Retention (NRR)",
        "description": "Удержание дохода с учетом expansion revenue",
        "formula": "(MRR from cohort + Expansion - Contraction - Churn) / Starting MRR * 100",
        "target": "> 100% (лучше > 120%)"
    },

    "time_to_value": {
        "name": "Time to Value (TTV)",
        "description": "Время до получения первой ценности от продукта",
        "formula": "Median time from signup to activation event",
        "target": "< 24 часа"
    },

    "feature_adoption": {
        "name": "Feature Adoption Rate",
        "description": "Процент пользователей, использующих ключевые функции",
        "formula": "Users using feature / Total Active Users * 100",
        "target": "> 40% для ключевых функций"
    },

    "customer_acquisition_cost": {
        "name": "Customer Acquisition Cost (CAC)",
        "description": "Стоимость привлечения одного клиента",
        "formula": "Total Marketing + Sales Costs / New Customers Acquired",
        "target": "CAC < LTV/3"
    }
}

# Сегменты пользователей для SaaS
USER_SEGMENTS = {
    "new_signups": {
        "description": "Новые зарегистрированные пользователи",
        "criteria": "Signup date within last 7 days",
        "marketing_focus": "Onboarding optimization, activation"
    },

    "activated_users": {
        "description": "Активированные пользователи",
        "criteria": "Completed activation event",
        "marketing_focus": "Feature adoption, upgrade prompts"
    },

    "power_users": {
        "description": "Продвинутые пользователи",
        "criteria": "High feature usage, multiple sessions per week",
        "marketing_focus": "Advanced features, referral programs"
    },

    "at_risk_users": {
        "description": "Пользователи в риске оттока",
        "criteria": "Declining usage in last 14 days",
        "marketing_focus": "Re-engagement, support outreach"
    },

    "churned_users": {
        "description": "Ушедшие пользователи",
        "criteria": "Cancelled subscription or inactive > 30 days",
        "marketing_focus": "Win-back campaigns, exit surveys"
    },

    "expansion_candidates": {
        "description": "Кандидаты на upgrade",
        "criteria": "Approaching plan limits or using premium features heavily",
        "marketing_focus": "Upgrade campaigns, limit notifications"
    }
}

def get_saas_setup_guide():
    """Руководство по настройке SaaS аналитики."""

    return """
# 🚀 SaaS Analytics Setup Guide

## 1. ОБЯЗАТЕЛЬНАЯ НАСТРОЙКА

### Mixpanel SaaS Events:
```javascript
// Регистрация с важными свойствами
mixpanel.track('Signup', {
    'Signup Method': 'Google OAuth',
    'UTM Source': 'google',
    'UTM Campaign': 'product_launch',
    'Plan Type': 'trial'
});

// Активация пользователя
mixpanel.track('User Activated', {
    'Activation Event': 'First Project Created',
    'Time to Activation': 180, // секунд
    'Onboarding Step': 'project_setup'
});

// Использование функций
mixpanel.track('Feature Used', {
    'Feature Name': 'Advanced Analytics',
    'Feature Category': 'analytics',
    'Subscription Tier': 'pro',
    'Usage Context': 'dashboard'
});

// Подписка
mixpanel.track('Subscription Started', {
    'Plan Name': 'Pro Monthly',
    'Price': 29.99,
    'Billing Cycle': 'monthly',
    'Trial Used': true
});
```

### Amplitude User Journey:
```javascript
// Identify пользователя
amplitude.setUserProperties({
    'Plan Type': 'pro',
    'Signup Date': '2024-01-15',
    'Company Size': '10-50',
    'Industry': 'SaaS'
});

// Critical events для SaaS
amplitude.track('Feature Adoption', {
    feature: 'advanced_reporting',
    adoption_day: 7, // день после регистрации
    user_segment: 'power_user'
});
```

## 2. КЛЮЧЕВЫЕ СОБЫТИЯ ДЛЛ ОТСЛЕЖИВАНИЯ

### User Lifecycle:
- ✅ signup - регистрация
- ✅ email_verified - подтверждение email
- ✅ onboarding_completed - завершение onboarding
- ✅ activation - ключевое действие (создание первого проекта/документа)
- ✅ trial_started - начало пробного периода
- ✅ subscription_started - оплата первой подписки

### Feature Usage:
- ✅ feature_used - использование функции
- ✅ feature_discovered - обнаружение новой функции
- ✅ help_accessed - обращение за помощью
- ✅ integration_connected - подключение интеграции

### Subscription Events:
- ✅ upgrade - повышение плана
- ✅ downgrade - понижение плана
- ✅ subscription_renewed - продление подписки
- ✅ subscription_cancelled - отмена подписки

## 3. SAAS ДАШБОРДЫ И ОТЧЕТЫ

### Product Metrics:
- Daily/Monthly Active Users (DAU/MAU)
- Feature Adoption Rates по каждой функции
- User Engagement Score (использование + активность)
- Session Duration и Frequency

### Business Metrics:
- Monthly Recurring Revenue (MRR)
- Annual Recurring Revenue (ARR)
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- Net Revenue Retention (NRR)

### Growth Analytics:
- Activation Rate по источникам трафика
- Conversion Funnel: Signup → Trial → Paid
- Cohort Analysis по месяцам регистрации
- Churn Rate по сегментам пользователей

## 4. АВТОМАТИЧЕСКИЕ СЕГМЕНТЫ

### Based on Usage:
- Power Users (топ 20% по активности)
- Casual Users (средняя активность)
- At-Risk Users (снижение активности)
- Dormant Users (неактивны > 14 дней)

### Based on Subscription:
- Trial Users
- Paid Users
- Recently Upgraded
- Recently Downgraded
- Churned Users

### Based on Features:
- Advanced Feature Users
- Basic Plan Users
- Integration Heavy Users
- Mobile-First Users

## 5. CHURN PREDICTION

### Leading Indicators:
- Снижение session frequency за 7 дней
- Отсутствие key feature usage за 14 дней
- Поддержка tickets с негативным sentiment
- Отказ от email коммуникаций

### Automated Alerts:
```javascript
// Настройка алерта для at-risk пользователей
mixpanel.createAlert({
    name: 'Users at Risk of Churning',
    criteria: {
        event: 'Feature Used',
        filter: 'last_seen > 7 days AND subscription_status = "active"'
    },
    action: 'send_email_to_success_team'
});
```

## 6. PRIVACY COMPLIANCE ДЛЯ SAAS

### B2B Privacy Requirements:
- ✅ Data Processing Agreements (DPA)
- ✅ GDPR compliance для EU customers
- ✅ SOC2 compliance для enterprise
- ✅ Data residency options

### Technical Implementation:
```javascript
// GDPR-compliant tracking
mixpanel.track('Feature Used', {
    'Feature Name': 'reporting',
    // НЕ передавать PII
    'User ID': hashUserId(actualUserId),
    'Account Type': accountTier
});

// User deletion (GDPR Right to be Forgotten)
mixpanel.people.delete_user(userId);
amplitude.deleteUser(userId);
```

## 7. ИНТЕГРАЦИИ ДЛЯ SAAS

### Customer Success Tools:
- Intercom/Zendesk для support correlation
- ChartMogul/ProfitWell для revenue analytics
- Salesforce для sales-to-usage correlation

### Development Integration:
- Product feature flags correlation
- Error tracking (Sentry) для usage context
- Performance monitoring correlation
"""

if __name__ == "__main__":
    # Пример использования
    config = get_saas_config()
    print("SaaS конфигурация создана:")
    print(f"- Тип проекта: {config.project_type}")
    print(f"- Analytics провайдеры: {config.analytics_providers}")
    print(f"- Ключевые метрики: {config.get_key_metrics()}")
    print(f"- Рекомендуемые события: {config.get_recommended_events()}")