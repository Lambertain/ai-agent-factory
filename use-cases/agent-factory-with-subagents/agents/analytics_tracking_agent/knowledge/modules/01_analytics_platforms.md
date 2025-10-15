# Module 01: Analytics Platforms Integration

## Интеграция основных аналитических платформ

Этот модуль содержит готовые паттерны интеграции с ведущими аналитическими платформами для веб-приложений: Google Analytics 4, Mixpanel и Amplitude.

---

## Google Analytics 4 (GA4)

### Базовая настройка

```javascript
// Инициализация Google Analytics 4
const GA_MEASUREMENT_ID = 'G-XXXXXXXXXX';

// Добавить gtag.js в HTML
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX', {
    page_title: document.title,
    page_path: window.location.pathname,
    send_page_view: true
  });
</script>
```

### Отслеживание событий

```javascript
// Базовое событие
gtag('event', 'button_click', {
    event_category: 'engagement',
    event_label: 'CTA Button',
    value: 1
});

// Enhanced E-commerce события
gtag('event', 'view_item', {
    items: [{
        item_id: 'sku123',
        item_name: 'Product Name',
        item_category: 'Electronics',
        price: 29.99,
        currency: 'USD'
    }]
});

gtag('event', 'add_to_cart', {
    items: [{
        item_id: 'sku123',
        item_name: 'Product Name',
        quantity: 1,
        price: 29.99
    }]
});

gtag('event', 'purchase', {
    transaction_id: '12345',
    value: 25.42,
    currency: 'USD',
    tax: 2.50,
    shipping: 5.00,
    items: [{
        item_id: 'sku123',
        item_name: 'Product Name',
        category: 'Electronics',
        quantity: 1,
        price: 25.42
    }]
});
```

### User Properties

```javascript
// Установить свойства пользователя
gtag('set', 'user_properties', {
    user_type: 'premium',
    account_age_days: 365,
    favorite_category: 'technology'
});

// User ID для кросс-платформенного отслеживания
gtag('config', 'G-XXXXXXXXXX', {
    user_id: 'unique_user_id_123'
});
```

### React Integration

```typescript
// useAnalytics.ts
import { useEffect } from 'react';

export function usePageView(path: string, title: string) {
    useEffect(() => {
        if (typeof window !== 'undefined' && window.gtag) {
            window.gtag('config', 'G-XXXXXXXXXX', {
                page_path: path,
                page_title: title
            });
        }
    }, [path, title]);
}

export function trackEvent(eventName: string, params: Record<string, any>) {
    if (typeof window !== 'undefined' && window.gtag) {
        window.gtag('event', eventName, params);
    }
}

// Использование в компоненте
import { usePageView, trackEvent } from '@/hooks/useAnalytics';

function ProductPage() {
    usePageView('/products', 'Products Page');

    const handleAddToCart = (product: Product) => {
        trackEvent('add_to_cart', {
            items: [{
                item_id: product.id,
                item_name: product.name,
                price: product.price
            }]
        });
    };

    return <div>...</div>;
}
```

---

## Mixpanel

### Базовая настройка

```javascript
// Инициализация Mixpanel
<script type="text/javascript">
(function(f,b){
    if(!b.__SV){
        var e,g,i,h;
        window.mixpanel=b;b._i=[];b.init=function(e,f,c){
            // Mixpanel initialization code
        };
        b._i.push([e,f,c])};
        b.__SV=1.2;e=f.createElement("script");
        e.type="text/javascript";
        e.async=!0;
        e.src="https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";
        f.getElementsByTagName("script")[0].parentNode.insertBefore(e,f.getElementsByTagName("script")[0])
    }
})(document,window.mixpanel||[]);
mixpanel.init("YOUR_TOKEN");
</script>
```

### Event Tracking

```javascript
// Простое событие
mixpanel.track('Button Clicked', {
    button_name: 'Sign Up',
    page: 'Homepage',
    section: 'Hero'
});

// E-commerce event
mixpanel.track('Product Purchased', {
    'Product Name': 'Premium Plan',
    'Revenue': 99.99,
    'Currency': 'USD',
    'Payment Method': 'Credit Card',
    'User Segment': 'Power User'
});

// Funnel tracking
mixpanel.track('Signup Started');
mixpanel.track('Signup Email Entered');
mixpanel.track('Signup Password Created');
mixpanel.track('Signup Completed');
```

### User Profiles

```javascript
// Идентификация пользователя
mixpanel.identify('unique_user_id_456');

// Установить профиль пользователя
mixpanel.people.set({
    '$email': 'user@example.com',
    '$name': 'John Doe',
    'Plan Type': 'Premium',
    'Account Created': new Date().toISOString()
});

// Инкрементальные свойства
mixpanel.people.increment('Logins Count');
mixpanel.people.increment('Total Revenue', 99.99);

// Append к массиву
mixpanel.people.append('Purchased Products', 'Product A');

// Set Once (не перезаписывается)
mixpanel.people.set_once({
    'First Purchase Date': new Date().toISOString()
});
```

### React Integration

```typescript
// MixpanelProvider.tsx
import React, { createContext, useContext } from 'react';
import mixpanel from 'mixpanel-browser';

const MixpanelContext = createContext(mixpanel);

export function MixpanelProvider({ children, token }: { children: React.ReactNode; token: string }) {
    React.useEffect(() => {
        mixpanel.init(token);
    }, [token]);

    return <MixpanelContext.Provider value={mixpanel}>{children}</MixpanelContext.Provider>;
}

export function useMixpanel() {
    return useContext(MixpanelContext);
}

// Использование
function App() {
    const mixpanel = useMixpanel();

    const handleSignup = (email: string) => {
        mixpanel.track('Signup Completed', {
            email,
            source: 'homepage'
        });
        mixpanel.people.set({ '$email': email });
    };

    return <div>...</div>;
}
```

---

## Amplitude

### Базовая настройка

```javascript
// Инициализация Amplitude
<script src="https://cdn.amplitude.com/libs/amplitude-8.5.0-min.gz.js"></script>
<script>
  amplitude.getInstance().init("YOUR_API_KEY", null, {
    includeReferrer: true,
    includeUtm: true,
    saveEvents: true
  });
</script>
```

### Event Tracking

```javascript
// Простое событие
amplitude.getInstance().logEvent('Button Clicked', {
    buttonName: 'Get Started',
    location: 'Header'
});

// E-commerce event
amplitude.getInstance().logEvent('Product Viewed', {
    productId: 'sku789',
    productName: 'Wireless Headphones',
    price: 149.99,
    category: 'Electronics'
});

amplitude.getInstance().logEvent('Purchase Completed', {
    orderId: 'order_12345',
    totalAmount: 299.99,
    itemCount: 2,
    paymentMethod: 'PayPal'
});
```

### User Properties

```javascript
// Установить User ID
amplitude.getInstance().setUserId('user_123456');

// User Properties
amplitude.getInstance().setUserProperties({
    'User Type': 'Premium',
    'Subscription Plan': 'Annual',
    'Account Age': 90
});

// Identify для создания/обновления профиля
const identify = new amplitude.Identify()
    .set('Plan', 'Premium')
    .add('Total Purchases', 1)
    .append('Interests', 'Technology');

amplitude.getInstance().identify(identify);
```

### Session Tracking

```javascript
// Начать новую сессию
amplitude.getInstance().setSessionId(Date.now());

// Отслеживание длительности сессии автоматическое, но можно настроить
amplitude.getInstance().init("YOUR_API_KEY", null, {
    sessionTimeout: 1800000 // 30 минут в миллисекундах
});
```

### React Integration

```typescript
// AmplitudeProvider.tsx
import React, { createContext, useContext, useEffect } from 'react';
import amplitude from 'amplitude-js';

const AmplitudeContext = createContext(amplitude.getInstance());

export function AmplitudeProvider({ children, apiKey }: { children: React.ReactNode; apiKey: string }) {
    useEffect(() => {
        amplitude.getInstance().init(apiKey);
    }, [apiKey]);

    return <AmplitudeContext.Provider value={amplitude.getInstance()}>{children}</AmplitudeContext.Provider>;
}

export function useAmplitude() {
    return useContext(AmplitudeContext);
}

// Использование
function FeaturePage() {
    const amp = useAmplitude();

    useEffect(() => {
        amp.logEvent('Feature Page Viewed', {
            featureName: 'Advanced Analytics'
        });
    }, []);

    const handleFeatureUsed = (featureName: string) => {
        amp.logEvent('Feature Used', { featureName });
    };

    return <div>...</div>;
}
```

---

## Best Practices для всех платформ

### 1. Event Naming Conventions
```javascript
// ПРАВИЛЬНО - понятные, последовательные имена
'Product Purchased'
'Signup Completed'
'Video Played'

// НЕПРАВИЛЬНО - непонятные, несогласованные
'buy_prod'
'user_signup'
'play'
```

### 2. Event Properties Structure
```javascript
// ПРАВИЛЬНО - структурированные properties
{
    product_id: 'sku123',
    product_name: 'Wireless Mouse',
    product_category: 'Electronics',
    price: 29.99,
    currency: 'USD'
}

// НЕПРАВИЛЬНО - неструктурированные
{
    info: 'Mouse Electronics 29.99 USD'
}
```

### 3. User Identification Timing
```javascript
// Идентифицировать пользователя как можно раньше
// GA4
gtag('config', 'G-XXXXXXXXXX', { user_id: userId });

// Mixpanel
mixpanel.identify(userId);

// Amplitude
amplitude.getInstance().setUserId(userId);
```

### 4. Error Handling
```javascript
// Обработка ошибок аналитики
function safeTrackEvent(platform: 'ga4' | 'mixpanel' | 'amplitude', eventName: string, params: any) {
    try {
        switch (platform) {
            case 'ga4':
                if (window.gtag) {
                    window.gtag('event', eventName, params);
                }
                break;
            case 'mixpanel':
                if (window.mixpanel) {
                    window.mixpanel.track(eventName, params);
                }
                break;
            case 'amplitude':
                if (window.amplitude) {
                    window.amplitude.getInstance().logEvent(eventName, params);
                }
                break;
        }
    } catch (error) {
        console.error(`Analytics error (${platform}):`, error);
    }
}
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
