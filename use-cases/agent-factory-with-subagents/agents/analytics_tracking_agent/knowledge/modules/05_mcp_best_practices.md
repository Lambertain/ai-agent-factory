# Module 05: MCP Integration & Best Practices

## MCP серверы и Best Practices для Analytics

Этот модуль содержит интеграцию с Model Context Protocol серверами для аналитики и сборник лучших практик для эффективного analytics tracking.

---

## MCP Servers для Analytics

### Google Analytics API MCP

```typescript
// Использование Google Analytics API через MCP
class GoogleAnalyticsMCP {
    private propertyId: string;

    constructor(propertyId: string) {
        this.propertyId = propertyId;
    }

    async fetchRealtimeUsers(): Promise<number> {
        const response = await fetch('/api/mcp/ga4/realtime-users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ propertyId: this.propertyId })
        });

        const data = await response.json();
        return data.activeUsers || 0;
    }

    async fetchTopPages(days: number = 7): Promise<Array<{ page: string; views: number }>> {
        const response = await fetch('/api/mcp/ga4/top-pages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                propertyId: this.propertyId,
                startDate: `${days}daysAgo`,
                endDate: 'today'
            })
        });

        const data = await response.json();
        return data.pages || [];
    }

    async fetchUserDemographics(): Promise<{
        ageGroups: Record<string, number>;
        genders: Record<string, number>;
        locations: Record<string, number>;
    }> {
        const response = await fetch('/api/mcp/ga4/demographics', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ propertyId: this.propertyId })
        });

        return await response.json();
    }

    async fetchConversionEvents(eventName: string, days: number = 30): Promise<Array<{
        date: string;
        count: number;
        value: number;
    }>> {
        const response = await fetch('/api/mcp/ga4/conversion-events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                propertyId: this.propertyId,
                eventName,
                startDate: `${days}daysAgo`,
                endDate: 'today'
            })
        });

        const data = await response.json();
        return data.events || [];
    }
}

// Использование
const gaMCP = new GoogleAnalyticsMCP('properties/123456789');

// Получить активных пользователей в реальном времени
const activeUsers = await gaMCP.fetchRealtimeUsers();
console.log(`Active users: ${activeUsers}`);

// Топ страниц за последние 7 дней
const topPages = await gaMCP.fetchTopPages(7);
topPages.forEach(page => {
    console.log(`${page.page}: ${page.views} views`);
});

// Демографические данные
const demographics = await gaMCP.fetchUserDemographics();
console.log('Age groups:', demographics.ageGroups);
console.log('Genders:', demographics.genders);
console.log('Top locations:', demographics.locations);

// Конверсионные события
const purchases = await gaMCP.fetchConversionEvents('purchase', 30);
purchases.forEach(event => {
    console.log(`${event.date}: ${event.count} purchases, $${event.value}`);
});
```

### Fetch MCP для External Analytics APIs

```typescript
// Использование Fetch MCP для интеграции с внешними analytics API
class ExternalAnalyticsMCP {
    async fetchMixpanelInsights(projectId: string, eventName: string): Promise<any> {
        const response = await fetch('/api/mcp/fetch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: `https://mixpanel.com/api/2.0/events/properties/`,
                method: 'GET',
                headers: {
                    'Authorization': `Basic ${btoa('YOUR_API_SECRET:')}`
                },
                params: {
                    event: eventName,
                    type: 'general',
                    unit: 'day'
                }
            })
        });

        return await response.json();
    }

    async fetchAmplitudeCharts(apiKey: string, chartId: string): Promise<any> {
        const response = await fetch('/api/mcp/fetch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: `https://amplitude.com/api/2/chart/${chartId}/query`,
                method: 'GET',
                headers: {
                    'Authorization': `Api-Key ${apiKey}`
                }
            })
        });

        return await response.json();
    }
}

const externalMCP = new ExternalAnalyticsMCP();

// Получить Mixpanel insights
const mixpanelData = await externalMCP.fetchMixpanelInsights('project_123', 'Button Clicked');

// Получить Amplitude chart data
const amplitudeData = await externalMCP.fetchAmplitudeCharts('api_key_123', 'chart_456');
```

---

## User Segmentation

### Advanced User Segmentation

```typescript
interface UserSegment {
    id: string;
    name: string;
    criteria: Array<{
        field: string;
        operator: 'equals' | 'not_equals' | 'greater_than' | 'less_than' | 'contains';
        value: any;
    }>;
}

class UserSegmentation {
    private segments: Map<string, UserSegment> = new Map();

    defineSegment(segment: UserSegment) {
        this.segments.set(segment.id, segment);
    }

    getUserSegments(user: Record<string, any>): string[] {
        const matchedSegments: string[] = [];

        for (const [id, segment] of this.segments) {
            if (this.matchesSegment(user, segment)) {
                matchedSegments.push(id);
            }
        }

        return matchedSegments;
    }

    private matchesSegment(user: Record<string, any>, segment: UserSegment): boolean {
        return segment.criteria.every(criterion => {
            const userValue = user[criterion.field];

            switch (criterion.operator) {
                case 'equals':
                    return userValue === criterion.value;
                case 'not_equals':
                    return userValue !== criterion.value;
                case 'greater_than':
                    return userValue > criterion.value;
                case 'less_than':
                    return userValue < criterion.value;
                case 'contains':
                    return String(userValue).includes(String(criterion.value));
                default:
                    return false;
            }
        });
    }

    trackSegmentEvent(userId: string, eventName: string, segments: string[]) {
        const event = {
            user_id: userId,
            event_name: eventName,
            user_segments: segments
        };

        // Отслеживать с метаданными сегментов
        gtag('event', eventName, event);
        mixpanel.track(eventName, event);
        amplitude.getInstance().logEvent(eventName, event);
    }
}

// Определение сегментов
const segmentation = new UserSegmentation();

segmentation.defineSegment({
    id: 'power_users',
    name: 'Power Users',
    criteria: [
        { field: 'total_purchases', operator: 'greater_than', value: 10 },
        { field: 'lifetime_value', operator: 'greater_than', value: 1000 }
    ]
});

segmentation.defineSegment({
    id: 'at_risk_churn',
    name: 'At Risk of Churn',
    criteria: [
        { field: 'days_since_last_login', operator: 'greater_than', value: 30 },
        { field: 'total_purchases', operator: 'greater_than', value: 0 }
    ]
});

segmentation.defineSegment({
    id: 'new_users',
    name: 'New Users',
    criteria: [
        { field: 'account_age_days', operator: 'less_than', value: 7 }
    ]
});

// Использование
const user = {
    user_id: 'user_789',
    total_purchases: 15,
    lifetime_value: 1500,
    days_since_last_login: 2,
    account_age_days: 365
};

const userSegments = segmentation.getUserSegments(user);
console.log('User segments:', userSegments); // ['power_users']

// Отслеживать событие с сегментами
segmentation.trackSegmentEvent(user.user_id, 'Product Viewed', userSegments);
```

---

## Analytics Best Practices

### 1. Event Naming Convention

```typescript
// ПРАВИЛЬНО - понятная иерархия и консистентность
const EVENT_NAMES = {
    // E-commerce
    PRODUCT_VIEWED: 'Product Viewed',
    PRODUCT_ADDED_TO_CART: 'Product Added to Cart',
    CHECKOUT_STARTED: 'Checkout Started',
    PURCHASE_COMPLETED: 'Purchase Completed',

    // User engagement
    VIDEO_PLAYED: 'Video Played',
    VIDEO_PAUSED: 'Video Paused',
    VIDEO_COMPLETED: 'Video Completed',

    // Forms
    FORM_STARTED: 'Form Started',
    FORM_FIELD_FILLED: 'Form Field Filled',
    FORM_SUBMITTED: 'Form Submitted',

    // Navigation
    PAGE_VIEWED: 'Page Viewed',
    LINK_CLICKED: 'Link Clicked',
    BUTTON_CLICKED: 'Button Clicked'
};

// НЕПРАВИЛЬНО - непоследовательные названия
const BAD_EVENTS = {
    view_prod: 'view_prod',
    add_cart: 'add_cart',
    start_checkout: 'CheckoutStart',
    purchase: 'PURCHASE_COMPLETE'
};
```

### 2. Property Standardization

```typescript
// Стандартизированные свойства для всех событий
interface BaseEventProperties {
    timestamp: string;
    user_id?: string;
    session_id: string;
    page_url: string;
    page_title: string;
    referrer?: string;
    device_type: 'mobile' | 'tablet' | 'desktop';
    browser: string;
    os: string;
}

interface ProductEvent extends BaseEventProperties {
    product_id: string;
    product_name: string;
    product_category: string;
    product_price: number;
    currency: string;
}

function trackStandardizedEvent(eventName: string, properties: BaseEventProperties) {
    const enrichedProperties = {
        ...properties,
        timestamp: new Date().toISOString(),
        session_id: getOrCreateSessionId(),
        page_url: window.location.href,
        page_title: document.title,
        device_type: getDeviceType(),
        browser: getBrowser(),
        os: getOS()
    };

    gtag('event', eventName, enrichedProperties);
    mixpanel.track(eventName, enrichedProperties);
    amplitude.getInstance().logEvent(eventName, enrichedProperties);
}
```

### 3. Error Tracking in Analytics

```typescript
class AnalyticsErrorTracker {
    trackJavaScriptError(error: Error, context: string) {
        const event = {
            error_message: error.message,
            error_stack: error.stack,
            error_context: context,
            page: window.location.pathname,
            timestamp: new Date().toISOString()
        };

        gtag('event', 'javascript_error', event);
        mixpanel.track('JavaScript Error', event);
        amplitude.getInstance().logEvent('JavaScript Error', event);
    }

    trackAPIError(endpoint: string, statusCode: number, errorMessage: string) {
        const event = {
            api_endpoint: endpoint,
            status_code: statusCode,
            error_message: errorMessage,
            page: window.location.pathname
        };

        gtag('event', 'api_error', event);
        mixpanel.track('API Error', event);
        amplitude.getInstance().logEvent('API Error', event);
    }

    trackFormValidationError(formName: string, fieldName: string, errorType: string) {
        const event = {
            form_name: formName,
            field_name: fieldName,
            error_type: errorType
        };

        gtag('event', 'form_validation_error', event);
        mixpanel.track('Form Validation Error', event);
        amplitude.getInstance().logEvent('Form Validation Error', event);
    }
}

const errorTracker = new AnalyticsErrorTracker();

// Глобальный обработчик ошибок
window.addEventListener('error', (event) => {
    errorTracker.trackJavaScriptError(event.error, 'window_error_handler');
});

// API error tracking
fetch('/api/users')
    .catch(error => {
        errorTracker.trackAPIError('/api/users', 500, error.message);
    });

// Form validation error
if (emailInvalid) {
    errorTracker.trackFormValidationError('signup_form', 'email', 'invalid_format');
}
```

### 4. Session Management

```typescript
class SessionManager {
    private sessionId: string;
    private sessionStartTime: number;
    private sessionTimeout: number = 1800000; // 30 минут
    private lastActivityTime: number;

    constructor() {
        this.sessionId = this.getOrCreateSessionId();
        this.sessionStartTime = Date.now();
        this.lastActivityTime = Date.now();
        this.trackSessionStart();
        this.setupActivityTracking();
    }

    private getOrCreateSessionId(): string {
        const stored = sessionStorage.getItem('session_id');
        if (stored) {
            return stored;
        }

        const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        sessionStorage.setItem('session_id', newSessionId);
        return newSessionId;
    }

    private trackSessionStart() {
        const event = {
            session_id: this.sessionId,
            started_at: new Date(this.sessionStartTime).toISOString()
        };

        gtag('event', 'session_start', event);
        mixpanel.track('Session Started', event);
        amplitude.getInstance().logEvent('Session Started', event);
    }

    private setupActivityTracking() {
        const events = ['click', 'scroll', 'keypress', 'mousemove'];

        events.forEach(eventType => {
            window.addEventListener(eventType, () => {
                this.updateActivity();
            });
        });

        setInterval(() => {
            this.checkSessionTimeout();
        }, 60000); // Проверять каждую минуту
    }

    private updateActivity() {
        this.lastActivityTime = Date.now();
    }

    private checkSessionTimeout() {
        const timeSinceActivity = Date.now() - this.lastActivityTime;

        if (timeSinceActivity > this.sessionTimeout) {
            this.endSession();
            this.startNewSession();
        }
    }

    private endSession() {
        const sessionDuration = Date.now() - this.sessionStartTime;

        const event = {
            session_id: this.sessionId,
            duration_seconds: Math.round(sessionDuration / 1000),
            ended_at: new Date().toISOString()
        };

        gtag('event', 'session_end', event);
        mixpanel.track('Session Ended', event);
        amplitude.getInstance().logEvent('Session Ended', event);
    }

    private startNewSession() {
        sessionStorage.removeItem('session_id');
        this.sessionId = this.getOrCreateSessionId();
        this.sessionStartTime = Date.now();
        this.trackSessionStart();
    }

    getSessionId(): string {
        return this.sessionId;
    }
}

export const sessionManager = new SessionManager();
```

### 5. Data Quality Assurance

```typescript
class AnalyticsQA {
    validateEvent(eventName: string, properties: Record<string, any>): boolean {
        const errors: string[] = [];

        // Проверка имени события
        if (!eventName || typeof eventName !== 'string') {
            errors.push('Event name must be a non-empty string');
        }

        // Проверка обязательных свойств
        const requiredProperties = ['timestamp', 'session_id', 'page_url'];
        requiredProperties.forEach(prop => {
            if (!(prop in properties)) {
                errors.push(`Missing required property: ${prop}`);
            }
        });

        // Проверка типов значений
        if (properties.user_id && typeof properties.user_id !== 'string') {
            errors.push('user_id must be a string');
        }

        if (properties.value && typeof properties.value !== 'number') {
            errors.push('value must be a number');
        }

        // Проверка на недопустимые значения
        if (properties.price && properties.price < 0) {
            errors.push('price cannot be negative');
        }

        if (errors.length > 0) {
            console.error('Event validation failed:', errors);
            this.reportValidationError(eventName, errors);
            return false;
        }

        return true;
    }

    private reportValidationError(eventName: string, errors: string[]) {
        // Отслеживать validation errors для monitoring
        gtag('event', 'analytics_validation_error', {
            event_name: eventName,
            errors: errors.join(', ')
        });
    }

    sanitizeProperties(properties: Record<string, any>): Record<string, any> {
        const sanitized: Record<string, any> = {};

        for (const [key, value] of Object.entries(properties)) {
            // Удалить null и undefined
            if (value === null || value === undefined) {
                continue;
            }

            // Обрезать длинные строки
            if (typeof value === 'string' && value.length > 500) {
                sanitized[key] = value.substring(0, 500) + '...';
            } else {
                sanitized[key] = value;
            }
        }

        return sanitized;
    }
}

export const analyticsQA = new AnalyticsQA();

// Использование
function safeTrackEvent(eventName: string, properties: Record<string, any>) {
    const sanitizedProps = analyticsQA.sanitizeProperties(properties);

    if (analyticsQA.validateEvent(eventName, sanitizedProps)) {
        gtag('event', eventName, sanitizedProps);
        mixpanel.track(eventName, sanitizedProps);
        amplitude.getInstance().logEvent(eventName, sanitizedProps);
    }
}
```

---

## Performance Optimization

### 1. Event Batching

```typescript
class EventBatcher {
    private batch: Array<{ eventName: string; properties: any }> = [];
    private batchSize: number = 10;
    private flushInterval: number = 5000; // 5 секунд
    private timer: NodeJS.Timeout | null = null;

    constructor() {
        this.startAutoFlush();
    }

    addEvent(eventName: string, properties: any) {
        this.batch.push({ eventName, properties });

        if (this.batch.length >= this.batchSize) {
            this.flush();
        }
    }

    private startAutoFlush() {
        this.timer = setInterval(() => {
            if (this.batch.length > 0) {
                this.flush();
            }
        }, this.flushInterval);
    }

    private flush() {
        if (this.batch.length === 0) return;

        const eventsToSend = [...this.batch];
        this.batch = [];

        // Отправить batch всех событий
        eventsToSend.forEach(({ eventName, properties }) => {
            gtag('event', eventName, properties);
            mixpanel.track(eventName, properties);
            amplitude.getInstance().logEvent(eventName, properties);
        });
    }

    destroy() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        this.flush(); // Отправить оставшиеся события
    }
}

export const eventBatcher = new EventBatcher();
```

### 2. Lazy Loading Analytics Scripts

```typescript
class LazyAnalyticsLoader {
    private loaded: Set<string> = new Set();

    async loadGoogleAnalytics(measurementId: string) {
        if (this.loaded.has('ga4')) return;

        const script = document.createElement('script');
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;

        document.head.appendChild(script);

        await this.waitForScript(script);

        window.dataLayer = window.dataLayer || [];
        function gtag(){window.dataLayer.push(arguments);}
        window.gtag = gtag;
        gtag('js', new Date());
        gtag('config', measurementId);

        this.loaded.add('ga4');
    }

    async loadMixpanel(token: string) {
        if (this.loaded.has('mixpanel')) return;

        const script = document.createElement('script');
        script.src = 'https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js';

        document.head.appendChild(script);

        await this.waitForScript(script);

        mixpanel.init(token);

        this.loaded.add('mixpanel');
    }

    private waitForScript(script: HTMLScriptElement): Promise<void> {
        return new Promise((resolve, reject) => {
            script.onload = () => resolve();
            script.onerror = () => reject(new Error('Script load failed'));
        });
    }
}

// Ленивая загрузка только после взаимодействия пользователя
const loader = new LazyAnalyticsLoader();

window.addEventListener('scroll', () => {
    loader.loadGoogleAnalytics('G-XXXXXXXXXX');
    loader.loadMixpanel('YOUR_TOKEN');
}, { once: true });
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
