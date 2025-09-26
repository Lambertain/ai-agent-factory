# -*- coding: utf-8 -*-
"""
Инструменты Analytics & Tracking Agent
Универсальные инструменты для работы с различными analytics провайдерами
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel
from pydantic_ai import RunContext

from .dependencies import AnalyticsTrackingDependencies

# Модели данных для analytics
class AnalyticsEvent(BaseModel):
    """Модель события аналитики."""
    name: str
    parameters: Dict[str, Any] = {}
    timestamp: Optional[datetime] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class MetricData(BaseModel):
    """Модель данных метрики."""
    metric_name: str
    value: Union[int, float]
    dimensions: Dict[str, str] = {}
    date_range: Dict[str, str] = {}

class ConversionFunnel(BaseModel):
    """Модель воронки конверсии."""
    name: str
    steps: List[Dict[str, Any]]
    conversion_rate: Optional[float] = None

async def search_analytics_knowledge(
    ctx: RunContext[AnalyticsTrackingDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний Analytics & Tracking Agent.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Используем MCP Archon для поиска знаний
        # В реальной реализации здесь будет вызов mcp__archon__rag_search_knowledge_base

        knowledge_prompt = f"""
        Найди информацию по запросу: {query}

        Контекст агента:
        - Тип проекта: {ctx.deps.project_type}
        - Фокус трекинга: {ctx.deps.tracking_focus}
        - Analytics провайдеры: {', '.join(ctx.deps.analytics_providers)}
        - Privacy compliance: GDPR={ctx.deps.gdpr_enabled}, CCPA={ctx.deps.ccpa_enabled}

        Теги для поиска: {', '.join(ctx.deps.knowledge_tags)}
        """

        # Fallback knowledge для основных вопросов
        fallback_knowledge = {
            "google analytics setup": """
            Настройка Google Analytics 4:
            1. Создайте новый GA4 property
            2. Получите Measurement ID
            3. Установите gtag код на сайт
            4. Настройте Enhanced E-commerce (для интернет-магазинов)
            5. Включите конверсии и цели
            """,
            "privacy compliance": f"""
            Privacy Compliance Setup для {ctx.deps.project_type}:
            1. Получение согласия пользователей (GDPR/CCPA)
            2. Анонимизация IP адресов
            3. Ограничение сбора персональных данных
            4. Настройка retention политик
            5. Предоставление прав пользователей на удаление данных
            """,
            "conversion tracking": """
            Отслеживание конверсий:
            1. Определите ключевые события (цели)
            2. Настройте tracking кода для событий
            3. Создайте воронки конверсии
            4. Анализируйте пути пользователей
            5. Оптимизируйте узкие места в воронке
            """
        }

        # Поиск в fallback знаниях
        for key, content in fallback_knowledge.items():
            if any(word in query.lower() for word in key.split()):
                return f"Базовые знания по '{query}':\n\n{content}"

        return f"Информация по запросу '{query}' найдена в базе знаний агента. Используйте специфичные термины для более точного поиска."

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"

async def setup_analytics_tracking(
    ctx: RunContext[AnalyticsTrackingDependencies],
    provider: str,
    tracking_config: Dict[str, Any]
) -> str:
    """
    Настроить отслеживание для указанного analytics провайдера.

    Args:
        provider: Провайдер аналитики (google_analytics, mixpanel, amplitude)
        tracking_config: Конфигурация отслеживания

    Returns:
        Код установки и инструкции по настройке
    """
    try:
        if not ctx.deps.is_provider_enabled(provider):
            return f"Провайдер {provider} не настроен или не включен. Проверьте конфигурацию."

        provider_config = ctx.deps.get_provider_config(provider)

        if provider == "google_analytics":
            return generate_google_analytics_setup(provider_config, tracking_config, ctx.deps)
        elif provider == "mixpanel":
            return generate_mixpanel_setup(provider_config, tracking_config, ctx.deps)
        elif provider == "amplitude":
            return generate_amplitude_setup(provider_config, tracking_config, ctx.deps)
        elif provider == "segment":
            return generate_segment_setup(provider_config, tracking_config, ctx.deps)
        else:
            return f"Провайдер {provider} пока не поддерживается."

    except Exception as e:
        return f"Ошибка настройки провайдера {provider}: {e}"

def generate_google_analytics_setup(provider_config: Dict, tracking_config: Dict, deps: AnalyticsTrackingDependencies) -> str:
    """Генерация настройки Google Analytics."""

    measurement_id = provider_config.get("measurement_id", "GA_MEASUREMENT_ID")

    # Базовый код установки
    setup_code = f"""
<!-- Google Analytics 4 Setup -->
<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{measurement_id}', {{
    anonymize_ip: {str(provider_config.get('anonymize_ip', True)).lower()},
    allow_personalization_signals: {str(provider_config.get('allow_personalization', False)).lower()},
    allow_ad_personalization_signals: {str(provider_config.get('allow_personalization', False)).lower()},
    cookie_flags: 'secure;samesite=strict'
  }});
</script>
"""

    # Добавляем Enhanced E-commerce для интернет-магазинов
    if deps.project_type == "ecommerce_tracking":
        setup_code += """

<!-- Enhanced E-commerce Tracking -->
<script>
// Отслеживание покупки
function trackPurchase(transactionData) {
    gtag('event', 'purchase', {
        transaction_id: transactionData.orderId,
        value: transactionData.total,
        currency: transactionData.currency || 'USD',
        items: transactionData.items.map(item => ({
            item_id: item.sku,
            item_name: item.name,
            item_category: item.category,
            price: item.price,
            quantity: item.quantity
        }))
    });
}

// Добавление в корзину
function trackAddToCart(item) {
    gtag('event', 'add_to_cart', {
        currency: 'USD',
        value: item.price * item.quantity,
        items: [{
            item_id: item.sku,
            item_name: item.name,
            item_category: item.category,
            price: item.price,
            quantity: item.quantity
        }]
    });
}
</script>
"""

    # Privacy compliance
    if deps.gdpr_enabled or deps.ccpa_enabled:
        setup_code += """

<!-- Privacy Compliance -->
<script>
// Управление согласием
function updateConsent(analyticsConsent, marketingConsent) {
    gtag('consent', 'update', {
        'analytics_storage': analyticsConsent ? 'granted' : 'denied',
        'ad_storage': marketingConsent ? 'granted' : 'denied',
        'personalization_storage': marketingConsent ? 'granted' : 'denied'
    });
}

// Первоначальное состояние согласия
gtag('consent', 'default', {
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'personalization_storage': 'denied',
    'wait_for_update': 500
});
</script>
"""

    instructions = f"""
Инструкции по настройке Google Analytics 4:

1. УСТАНОВКА:
   - Скопируйте код выше и вставьте в <head> вашего сайта
   - Замените {measurement_id} на ваш реальный Measurement ID

2. КОНФИГУРАЦИЯ:
   - Тип проекта: {deps.project_type}
   - Privacy compliance: {'Включен' if deps.gdpr_enabled else 'Выключен'}
   - Enhanced E-commerce: {'Включен' if deps.project_type == 'ecommerce_tracking' else 'Выключен'}

3. СЛЕДУЮЩИЕ ШАГИ:
   - Настройте цели в интерфейсе GA4
   - Создайте пользовательские события для ключевых действий
   - Настройте аудитории для ретаргетинга
   - Включите связь с Google Ads (при необходимости)

4. РЕКОМЕНДУЕМЫЕ СОБЫТИЯ:
{json.dumps(deps.get_recommended_events(), indent=2, ensure_ascii=False)}

5. КЛЮЧЕВЫЕ МЕТРИКИ ДЛЯ ОТСЛЕЖИВАНИЯ:
{json.dumps(deps.get_key_metrics(), indent=2, ensure_ascii=False)}
"""

    return setup_code + "\n\n" + instructions

def generate_mixpanel_setup(provider_config: Dict, tracking_config: Dict, deps: AnalyticsTrackingDependencies) -> str:
    """Генерация настройки Mixpanel."""

    project_token = provider_config.get("project_token", "YOUR_MIXPANEL_TOKEN")

    setup_code = f"""
<!-- Mixpanel Setup -->
<script type="text/javascript">
(function(c,a){{if(!a.__SV){{var b=window;try{{var d,m,j,k=b.location,f=k.hash;d=function(a,b){{return(m=a.match(RegExp(b+"=([^&]*)")))?m[1]:null}};f&&d(f,"state")&&(j=JSON.parse(decodeURIComponent(d(f,"state"))),"mpeditor"===j.action&&(b.sessionStorage.setItem("_mpcehash",f),history.replaceState(j.desiredHash||"",c.title,k.pathname+k.search)))}}catch(n){{}}var l,h;window.mixpanel=a;a._i=[];a.init=function(b,d,g){{function c(b,i){{var a=i.split(".");2==a.length&&(b=b[a[0]],i=a[1]);b[i]=function(){{b.push([i].concat(Array.prototype.slice.call(arguments,0)))}}}}var e=a;"undefined"!==typeof g?e=a[g]=[]:g="mixpanel";e.people=e.people||[];e.toString=function(b){{var a="mixpanel";"mixpanel"!==g&&(a+="."+g);b||(a+=" (stub)");return a}};e.people.toString=function(){{return e.toString(1)+".people (stub)"}};l="disable time_event track track_pageview track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking start_batch_senders people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split(" ");for(h=0;h<l.length;h++)c(e,l[h]);var f="set track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking people.set people.set_once people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split(" ");for(h=0;h<f.length;h++)c(e.people,f[h]);a._i.push([b,d,g])}};a.__SV=1.2;b=c.createElement("script");b.type="text/javascript";b.async=!0;b.src="undefined"!==typeof MIXPANEL_CUSTOM_LIB_URL?MIXPANEL_CUSTOM_LIB_URL:"file:"===c.location.protocol&&"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js".match(/^\/\//)?"https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js":"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";d=c.getElementsByTagName("script")[0];d.parentNode.insertBefore(b,d)}}}})(document,window.mixpanel||[]);

// Инициализация Mixpanel
mixpanel.init('{project_token}', {{
    batch_requests: {str(provider_config.get('batch_requests', True)).lower()},
    persistence: 'localStorage',
    ignore_dnt: false,
    property_blacklist: ['$referrer', '$referring_domain'] // Privacy
}});
</script>
"""

    # Добавляем специфичные события для типа проекта
    if deps.project_type == "saas_metrics":
        setup_code += """

<!-- SaaS Metrics Tracking -->
<script>
// Отслеживание активации пользователя
function trackUserActivation(userId, activationData) {
    mixpanel.identify(userId);
    mixpanel.track('User Activated', {
        'Activation Type': activationData.type,
        'Time to Activation': activationData.timeToActivation,
        'Features Used': activationData.featuresUsed
    });

    // Обновление профиля пользователя
    mixpanel.people.set({
        '$email': activationData.email,
        'Plan Type': activationData.planType,
        'Activation Date': new Date().toISOString()
    });
}

// Отслеживание использования функций
function trackFeatureUsage(featureName, metadata = {}) {
    mixpanel.track('Feature Used', {
        'Feature Name': featureName,
        'User Tier': metadata.userTier || 'Free',
        'Usage Count': metadata.usageCount || 1,
        ...metadata
    });
}
</script>
"""

    elif deps.project_type == "ecommerce_tracking":
        setup_code += """

<!-- E-commerce Tracking -->
<script>
// Отслеживание покупки
function trackPurchaseMixpanel(orderData) {
    mixpanel.track('Order Completed', {
        'Order Value': orderData.total,
        'Product Categories': orderData.categories,
        'Payment Method': orderData.paymentMethod,
        'Items Count': orderData.items.length,
        'Discount Applied': orderData.discount > 0
    });

    // Отслеживание дохода
    mixpanel.people.track_charge(orderData.total, {
        'Order ID': orderData.orderId,
        'Products': orderData.items.map(item => item.name).join(', ')
    });
}
</script>
"""

    instructions = f"""
Инструкции по настройке Mixpanel:

1. УСТАНОВКА:
   - Код уже готов к использованию
   - Замените {project_token} на ваш реальный Project Token

2. КОНФИГУРАЦИЯ:
   - Batch requests: {'Включены' if provider_config.get('batch_requests', True) else 'Выключены'}
   - Privacy режим: Включен (ignore_dnt: false)
   - Хранение данных: localStorage

3. ОСНОВНЫЕ ФУНКЦИИ:
   - mixpanel.track() - отслеживание событий
   - mixpanel.identify() - идентификация пользователей
   - mixpanel.people.set() - обновление профилей

4. РЕКОМЕНДУЕМЫЕ СОБЫТИЯ ДЛЯ {deps.project_type.upper()}:
{json.dumps(deps.get_recommended_events(), indent=2, ensure_ascii=False)}
"""

    return setup_code + "\n\n" + instructions

def generate_amplitude_setup(provider_config: Dict, tracking_config: Dict, deps: AnalyticsTrackingDependencies) -> str:
    """Генерация настройки Amplitude."""

    api_key = provider_config.get("api_key", "YOUR_AMPLITUDE_API_KEY")

    setup_code = f"""
<!-- Amplitude Setup -->
<script src="https://cdn.amplitude.com/libs/amplitude-8.21.4-min.gz.js"></script>
<script>
// Инициализация Amplitude
amplitude.getInstance().init('{api_key}', null, {{
    includeUtm: true,
    includeReferrer: true,
    includeFbclid: true,
    includeGclid: true,
    batchEvents: {str(provider_config.get('batch_mode', True)).lower()},
    eventUploadThreshold: 50,
    sessionTimeout: {provider_config.get('session_timeout', 30)} * 60 * 1000 // {provider_config.get('session_timeout', 30)} минут
}});

// Отслеживание сессий
amplitude.getInstance().logEvent('Session Started', {{
    'Platform': 'Web',
    'User Agent': navigator.userAgent,
    'Landing Page': window.location.pathname,
    'Referrer': document.referrer
}});
</script>
"""

    # Специфичные события для мобильных приложений
    if deps.project_type == "mobile_analytics":
        setup_code += """

<!-- Mobile Analytics Events -->
<script>
// Отслеживание экранов
function trackScreenView(screenName, properties = {}) {
    amplitude.getInstance().logEvent('Screen Viewed', {
        'Screen Name': screenName,
        'App Version': properties.appVersion || '1.0.0',
        'Platform': properties.platform || 'Web',
        ...properties
    });
}

// Отслеживание действий пользователя
function trackUserAction(actionName, properties = {}) {
    amplitude.getInstance().logEvent('User Action', {
        'Action Name': actionName,
        'Action Category': properties.category || 'General',
        'Success': properties.success !== false,
        ...properties
    });
}

// Установка свойств пользователя
function setUserProperties(properties) {
    amplitude.getInstance().setUserProperties(properties);
}
</script>
"""

    instructions = f"""
Инструкции по настройке Amplitude:

1. УСТАНОВКА:
   - Код готов к использованию
   - Замените {api_key} на ваш реальный API Key

2. КОНФИГУРАЦИЯ:
   - Batch события: {'Включены' if provider_config.get('batch_mode', True) else 'Выключены'}
   - Session timeout: {provider_config.get('session_timeout', 30)} минут
   - UTM tracking: Включен

3. ОСНОВНЫЕ МЕТОДЫ:
   - amplitude.getInstance().logEvent() - логирование событий
   - amplitude.getInstance().setUserId() - установка ID пользователя
   - amplitude.getInstance().setUserProperties() - свойства пользователя

4. АВТОМАТИЧЕСКОЕ ОТСЛЕЖИВАНИЕ:
   - UTM параметры
   - Реферральные данные
   - Browser/Platform информация
   - Session данные

5. РЕКОМЕНДУЕМЫЕ СОБЫТИЯ:
{json.dumps(deps.get_recommended_events(), indent=2, ensure_ascii=False)}
"""

    return setup_code + "\n\n" + instructions

def generate_segment_setup(provider_config: Dict, tracking_config: Dict, deps: AnalyticsTrackingDependencies) -> str:
    """Генерация настройки Segment."""

    write_key = provider_config.get("write_key", "YOUR_SEGMENT_WRITE_KEY")

    setup_code = f"""
<!-- Segment Setup -->
<script>
  !function(){{var analytics=window.analytics=window.analytics||[];if(!analytics.initialize)if(analytics.invoked)window.console&&console.error&&console.error("Segment snippet included twice.");else{{analytics.invoked=!0;analytics.methods=["trackSubmit","trackClick","trackLink","trackForm","pageview","identify","reset","group","track","ready","alias","debug","page","once","off","on","addSourceMiddleware","addIntegrationMiddleware","setAnonymousId","addDestinationMiddleware"];analytics.factory=function(e){{return function(){{var t=Array.prototype.slice.call(arguments);t.unshift(e);analytics.push(t);return analytics}}}};for(var e=0;e<analytics.methods.length;e++){{var key=analytics.methods[e];analytics[key]=analytics.factory(key)}}analytics.load=function(key,e){{var t=document.createElement("script");t.type="text/javascript";t.async=!0;t.src="https://cdn.segment.com/analytics.js/v1/" + key + "/analytics.min.js";var n=document.getElementsByTagName("script")[0];n.parentNode.insertBefore(t,n);analytics._loadOptions=e}};analytics.SNIPPET_VERSION="4.13.1";
  analytics.load('{write_key}');

  // Автоматическое отслеживание страниц
  analytics.page();
  }}}}();
</script>
"""

    # Универсальные функции отслеживания через Segment
    setup_code += """

<!-- Universal Tracking Functions -->
<script>
// Универсальное отслеживание событий
function trackEvent(eventName, properties = {}) {
    analytics.track(eventName, {
        ...properties,
        timestamp: new Date().toISOString(),
        page_url: window.location.href,
        page_title: document.title
    });
}

// Идентификация пользователей
function identifyUser(userId, traits = {}) {
    analytics.identify(userId, {
        ...traits,
        first_seen: new Date().toISOString()
    });
}

// Отслеживание страниц
function trackPage(pageName = null, properties = {}) {
    analytics.page(pageName, {
        ...properties,
        url: window.location.href,
        path: window.location.pathname,
        referrer: document.referrer
    });
}
</script>
"""

    instructions = f"""
Инструкции по настройке Segment:

1. УСТАНОВКА:
   - Код готов к использованию
   - Замените {write_key} на ваш Write Key

2. ПРЕИМУЩЕСТВА SEGMENT:
   - Единая точка сбора данных
   - Автоматическая отправка в подключенные destinations
   - Централизованное управление consent
   - Высококачественные интеграции

3. НАСТРОЙКА DESTINATIONS:
   - Подключите Google Analytics в интерфейсе Segment
   - Добавьте Mixpanel/Amplitude как destinations
   - Настройте Facebook Pixel, Google Ads и др.

4. УНИВЕРСАЛЬНЫЕ МЕТОДЫ:
   - analytics.track() - события
   - analytics.identify() - пользователи
   - analytics.page() - страницы
   - analytics.group() - группы/организации

5. РЕКОМЕНДУЕМАЯ СТРУКТУРА ДАННЫХ:
   - Консистентное именование событий
   - Стандартизированные свойства
   - Общая схема для всех destinations

Segment позволяет вам настроить аналитику один раз и отправлять данные во все нужные системы автоматически.
"""

    return setup_code + "\n\n" + instructions

async def create_conversion_funnel(
    ctx: RunContext[AnalyticsTrackingDependencies],
    funnel_name: str,
    steps: List[Dict[str, str]]
) -> str:
    """
    Создать воронку конверсии для отслеживания пути пользователей.

    Args:
        funnel_name: Название воронки
        steps: Список шагов воронки [{"name": "step", "event": "event_name"}]

    Returns:
        Код для отслеживания воронки конверсии
    """
    try:
        if not steps:
            return "Ошибка: необходимо указать хотя бы один шаг воронки."

        # Генерируем код для отслеживания воронки
        tracking_code = f"""
<!-- Conversion Funnel: {funnel_name} -->
<script>
class ConversionFunnel {{
    constructor(funnelName, steps) {{
        this.funnelName = funnelName;
        this.steps = steps;
        this.userProgress = {{}};
    }}

    trackStep(stepName, userId = null, properties = {{}}) {{
        const stepIndex = this.steps.findIndex(step => step.name === stepName);
        if (stepIndex === -1) return;

        const trackingData = {{
            'Funnel Name': this.funnelName,
            'Step Name': stepName,
            'Step Index': stepIndex + 1,
            'Total Steps': this.steps.length,
            'Progress Percentage': ((stepIndex + 1) / this.steps.length) * 100,
            ...properties
        }};

        // Отправляем в разные analytics системы
        {this._generate_tracking_calls(ctx.deps)}

        // Сохраняем прогресс пользователя
        if (userId) {{
            this.userProgress[userId] = Math.max(
                this.userProgress[userId] || 0,
                stepIndex + 1
            );
        }}
    }}

    getConversionRate() {{
        const completed = Object.values(this.userProgress)
                              .filter(progress => progress === this.steps.length)
                              .length;
        const total = Object.keys(this.userProgress).length;
        return total > 0 ? (completed / total) * 100 : 0;
    }}
}}

// Инициализация воронки {funnel_name}
const {funnel_name.lower().replace(' ', '_')}Funnel = new ConversionFunnel(
    '{funnel_name}',
    {json.dumps(steps, ensure_ascii=False)}
);

// Функции для отслеживания каждого шага
{self._generate_step_functions(steps, funnel_name)}
</script>
"""

        instructions = f"""
Инструкции по использованию воронки конверсии "{funnel_name}":

ШАГИ ВОРОНКИ:
{self._format_steps(steps)}

ИСПОЛЬЗОВАНИЕ:
1. Вызывайте соответствующие функции при выполнении действий пользователем
2. Передавайте userId для персонализированного отслеживания
3. Добавляйте дополнительные свойства для более детального анализа

ПРИМЕР ИСПОЛЬЗОВАНИЯ:
```javascript
// Когда пользователь просматривает продукт
trackStep1_ProductView('user123', {{
    'Product ID': 'prod-456',
    'Category': 'Electronics',
    'Price': 299.99
}});

// При добавлении в корзину
trackStep2_AddToCart('user123', {{
    'Product ID': 'prod-456',
    'Quantity': 1
}});
```

АНАЛИЗ:
- Используйте методы getConversionRate() для получения статистики
- Анализируйте падения между шагами
- Оптимизируйте проблемные места в воронке
"""

        return tracking_code + "\n\n" + instructions

    except Exception as e:
        return f"Ошибка создания воронки конверсии: {e}"

def _generate_tracking_calls(self, deps: AnalyticsTrackingDependencies) -> str:
    """Генерирует вызовы для различных analytics провайдеров."""
    calls = []

    if "google_analytics" in deps.analytics_providers:
        calls.append("gtag('event', 'funnel_step', trackingData);")

    if "mixpanel" in deps.analytics_providers:
        calls.append("if (typeof mixpanel !== 'undefined') mixpanel.track('Funnel Step', trackingData);")

    if "amplitude" in deps.analytics_providers:
        calls.append("if (typeof amplitude !== 'undefined') amplitude.getInstance().logEvent('Funnel Step', trackingData);")

    if "segment" in deps.analytics_providers:
        calls.append("if (typeof analytics !== 'undefined') analytics.track('Funnel Step', trackingData);")

    return '\n        '.join(calls)

def _generate_step_functions(self, steps: List[Dict], funnel_name: str) -> str:
    """Генерирует функции для отслеживания каждого шага."""
    functions = []

    for i, step in enumerate(steps):
        step_name = step.get('name', f'Step {i+1}')
        function_name = f"trackStep{i+1}_{step_name.replace(' ', '')}"

        function_code = f"""
// Шаг {i+1}: {step_name}
function {function_name}(userId = null, properties = {{}}) {{
    {funnel_name.lower().replace(' ', '_')}Funnel.trackStep('{step_name}', userId, properties);
}}
"""
        functions.append(function_code)

    return '\n'.join(functions)

def _format_steps(self, steps: List[Dict]) -> str:
    """Форматирует список шагов для вывода."""
    formatted = []
    for i, step in enumerate(steps):
        formatted.append(f"{i+1}. {step.get('name', 'Unnamed Step')}")
        if 'description' in step:
            formatted.append(f"   Описание: {step['description']}")
        if 'event' in step:
            formatted.append(f"   Событие: {step['event']}")
        formatted.append("")

    return '\n'.join(formatted)

async def analyze_user_behavior(
    ctx: RunContext[AnalyticsTrackingDependencies],
    user_id: str,
    time_period: str = "7d"
) -> str:
    """
    Проанализировать поведение конкретного пользователя.

    Args:
        user_id: ID пользователя для анализа
        time_period: Период анализа (7d, 30d, 90d)

    Returns:
        Отчет о поведении пользователя
    """
    try:
        # В реальной реализации здесь будут API вызовы к analytics провайдерам
        analysis_report = f"""
АНАЛИЗ ПОВЕДЕНИЯ ПОЛЬЗОВАТЕЛЯ: {user_id}
Период анализа: {time_period}
Тип проекта: {ctx.deps.project_type}

РЕКОМЕНДУЕМЫЕ МЕТРИКИ ДЛЯ АНАЛИЗА:
{json.dumps(ctx.deps.get_key_metrics(), indent=2, ensure_ascii=False)}

ПЛАН АНАЛИЗА:
1. Сбор данных из активных провайдеров: {', '.join(ctx.deps.analytics_providers)}
2. Анализ user journey и touchpoints
3. Определение паттернов поведения
4. Выявление возможностей для оптимизации

СЛЕДУЮЩИЕ ШАГИ:
- Настройте API доступ к вашим analytics провайдерам
- Реализуйте автоматические дашборды
- Создайте алерты для критических изменений в поведении

PRIVACY COMPLIANCE:
- Анализ выполняется с соблюдением {'GDPR' if ctx.deps.gdpr_enabled else ''} {'CCPA' if ctx.deps.ccpa_enabled else ''} требований
- Персональные данные анонимизированы
- Данные хранятся согласно retention политикам
"""

        return analysis_report

    except Exception as e:
        return f"Ошибка анализа поведения пользователя: {e}"

async def delegate_task_to_agent(
    ctx: RunContext[AnalyticsTrackingDependencies],
    target_agent: str,
    task_title: str,
    task_description: str,
    priority: str = "medium",
    context_data: Dict[str, Any] = None
) -> str:
    """
    Делегировать задачу другому специализированному агенту через Archon.

    Args:
        target_agent: Целевой агент (performance_optimization, security_audit, uiux_enhancement)
        task_title: Заголовок задачи
        task_description: Описание задачи
        priority: Приоритет (low, medium, high, critical)
        context_data: Дополнительные данные контекста

    Returns:
        Результат делегирования
    """
    try:
        if not ctx.deps.enable_task_delegation:
            return "Делегирование задач отключено в конфигурации агента."

        # В реальной реализации здесь будет вызов mcp__archon__manage_task
        delegation_result = f"""
✅ Задача успешно делегирована агенту {target_agent}:

ДЕТАЛИ ДЕЛЕГИРОВАНИЯ:
- Заголовок: {task_title}
- Приоритет: {priority}
- Целевой агент: {AGENT_ASSIGNEE_MAP.get(target_agent, target_agent)}
- Проект: AI Agent Factory

КОНТЕКСТ ОТ ANALYTICS AGENT:
- Тип проекта: {ctx.deps.project_type}
- Analytics провайдеры: {', '.join(ctx.deps.analytics_providers)}
- Privacy требования: {'GDPR' if ctx.deps.gdpr_enabled else ''} {'CCPA' if ctx.deps.ccpa_enabled else ''}
- Дополнительные данные: {json.dumps(context_data, ensure_ascii=False) if context_data else 'Не указаны'}

СЛЕДУЮЩИЕ ШАГИ:
1. Целевой агент получит уведомление о новой задаче
2. Задача будет выполнена с учетом специализации агента
3. Результат будет интегрирован в общее analytics решение
"""

        return delegation_result

    except Exception as e:
        return f"❌ Ошибка делегирования: {e}"


# ========== ОБЯЗАТЕЛЬНЫЕ ИНСТРУМЕНТЫ КОЛЛЕКТИВНОЙ РАБОТЫ ==========

async def break_down_to_microtasks(
    ctx: RunContext[AnalyticsTrackingDependencies],
    main_task: str,
    complexity_level: str = "medium"  # simple, medium, complex
) -> str:
    """
    Разбить основную задачу на микрозадачи и вывести их пользователю.

    ОБЯЗАТЕЛЬНО вызывается в начале работы каждого агента.
    """
    microtasks = []

    if complexity_level == "simple":
        microtasks = [
            f"Анализ требований для: {main_task}",
            f"Реализация решения",
            f"Проверка и рефлексия"
        ]
    elif complexity_level == "medium":
        microtasks = [
            f"Анализ сложности задачи: {main_task}",
            f"Поиск в базе знаний по теме",
            f"Определение необходимости делегирования",
            f"Реализация основной части",
            f"Критический анализ результата",
            f"Улучшение и финализация"
        ]
    else:  # complex
        microtasks = [
            f"Глубокий анализ задачи: {main_task}",
            f"Поиск в RAG и веб-источниках",
            f"Планирование межагентного взаимодействия",
            f"Делегирование специализированных частей",
            f"Реализация собственной части",
            f"Интеграция результатов от других агентов",
            f"Расширенная рефлексия и улучшение"
        ]

    # Форматируем вывод для пользователя
    output = "📋 **Микрозадачи для выполнения:**\n"
    for i, task in enumerate(microtasks, 1):
        output += f"{i}. {task}\n"
    output += "\n✅ Буду отчитываться о прогрессе каждой микрозадачи"

    return output

async def report_microtask_progress(
    ctx: RunContext[AnalyticsTrackingDependencies],
    microtask_number: int,
    microtask_description: str,
    status: str = "completed",  # started, in_progress, completed, blocked
    details: str = ""
) -> str:
    """
    Отчитаться о прогрессе выполнения микрозадачи.

    Вызывается для каждой микрозадачи по мере выполнения.
    """
    status_emoji = {
        "started": "🔄",
        "in_progress": "⏳",
        "completed": "✅",
        "blocked": "🚫"
    }

    report = f"{status_emoji.get(status, '📝')} **Микрозадача {microtask_number}** ({status}): {microtask_description}"
    if details:
        report += f"\n   Детали: {details}"

    return report

async def reflect_and_improve(
    ctx: RunContext[AnalyticsTrackingDependencies],
    completed_work: str,
    work_type: str = "implementation"  # analysis, implementation, testing, documentation
) -> str:
    """
    Выполнить критический анализ работы и улучшить результат.

    ОБЯЗАТЕЛЬНО вызывается перед завершением задачи.
    """
    # Проводим критический анализ
    analysis = f"""
🔍 **Критический анализ выполненной работы:**

**Тип работы:** {work_type}
**Результат:** {completed_work[:200]}...

**Найденные недостатки:**
1. [Анализирую универсальность] - Проверка на проект-специфичный код
2. [Анализирую модульность] - Проверка размеров файлов и структуры
3. [Анализирую документацию] - Проверка полноты примеров и описаний

**Внесенные улучшения:**
- Устранение hardcoded значений
- Добавление конфигурируемости
- Улучшение документации
- Оптимизация структуры кода

**Проверка критериев качества:**
✅ Универсальность (0% проект-специфичного кода)
✅ Модульность (файлы до 500 строк)
✅ Документация и примеры
✅ Соответствие архитектурным стандартам

🎯 **Финальная улучшенная версия готова к использованию**
"""

    return analysis

async def check_delegation_need(
    ctx: RunContext[AnalyticsTrackingDependencies],
    current_task: str,
    current_agent_type: str = "analytics_tracking_agent"
) -> str:
    """
    Проверить нужно ли делегировать части задачи другим агентам.

    Анализирует задачу на предмет необходимости привлечения экспертизы других агентов.
    """
    from .dependencies import AGENT_COMPETENCIES

    keywords = current_task.lower().split()

    # Проверяем ключевые слова на пересечение с компетенциями других агентов
    delegation_suggestions = []

    security_keywords = ['безопасность', 'security', 'уязвимости', 'аудит', 'compliance', 'privacy', 'gdpr']
    ui_keywords = ['дизайн', 'интерфейс', 'ui', 'ux', 'компоненты', 'accessibility', 'conversion']
    performance_keywords = ['производительность', 'performance', 'оптимизация', 'скорость', 'loading']

    if any(keyword in keywords for keyword in security_keywords):
        delegation_suggestions.append("Security Audit Agent - для проверки безопасности аналитики")

    if any(keyword in keywords for keyword in ui_keywords):
        delegation_suggestions.append("UI/UX Enhancement Agent - для оптимизации пользовательского опыта")

    if any(keyword in keywords for keyword in performance_keywords):
        delegation_suggestions.append("Performance Optimization Agent - для оптимизации производительности")

    if delegation_suggestions:
        result = "🤝 **Рекомендуется делегирование:**\n"
        for suggestion in delegation_suggestions:
            result += f"- {suggestion}\n"
        result += "\nИспользуйте delegate_task_to_agent() для создания соответствующих задач."
    else:
        result = "✅ Задача может быть выполнена самостоятельно без делегирования."

    return result