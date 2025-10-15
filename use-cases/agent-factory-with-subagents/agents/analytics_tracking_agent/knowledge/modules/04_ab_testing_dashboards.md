# Module 04: A/B Testing & Dashboards

## A/B Testing и Real-Time Analytics Dashboards

Этот модуль содержит паттерны для A/B тестирования и создания аналитических дашбордов для мониторинга метрик в реальном времени.

---

## A/B Testing Integration

### Optimizely Integration

```typescript
// Инициализация Optimizely
import { createInstance } from '@optimizely/optimizely-sdk';

const optimizely = createInstance({
    sdkKey: 'YOUR_SDK_KEY',
    datafileOptions: {
        autoUpdate: true,
        updateInterval: 300000 // 5 минут
    }
});

class OptimizelyTracker {
    private client: any;
    private userId: string;

    constructor(userId: string) {
        this.client = optimizely;
        this.userId = userId;
    }

    async getVariation(experimentKey: string): Promise<string | null> {
        const user = {
            id: this.userId,
            attributes: this.getUserAttributes()
        };

        const variation = this.client.activate(experimentKey, user.id, user.attributes);

        // Отслеживать exposure event
        this.trackExposure(experimentKey, variation);

        return variation;
    }

    private getUserAttributes(): Record<string, any> {
        return {
            device_type: this.getDeviceType(),
            browser: this.getBrowser(),
            geo_location: this.getGeoLocation()
        };
    }

    private getDeviceType(): string {
        const ua = navigator.userAgent;
        if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
            return 'tablet';
        }
        if (/Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) {
            return 'mobile';
        }
        return 'desktop';
    }

    private getBrowser(): string {
        const ua = navigator.userAgent;
        if (ua.includes('Chrome')) return 'chrome';
        if (ua.includes('Firefox')) return 'firefox';
        if (ua.includes('Safari')) return 'safari';
        if (ua.includes('Edge')) return 'edge';
        return 'other';
    }

    private getGeoLocation(): string {
        // Использовать IP-based геолокацию или browser API
        return 'US'; // Placeholder
    }

    private trackExposure(experimentKey: string, variation: string | null) {
        const event = {
            experiment_key: experimentKey,
            variation: variation || 'control',
            user_id: this.userId
        };

        // Отслеживать exposure во всех платформах
        gtag('event', 'ab_test_exposure', event);
        mixpanel.track('AB Test Exposure', event);
        amplitude.getInstance().logEvent('AB Test Exposure', event);
    }

    trackConversion(experimentKey: string, conversionGoal: string, value?: number) {
        const event = {
            experiment_key: experimentKey,
            conversion_goal: conversionGoal,
            value: value || 0,
            user_id: this.userId
        };

        // Optimizely conversion tracking
        this.client.track(conversionGoal, this.userId);

        // Analytics platforms
        gtag('event', 'ab_test_conversion', event);
        mixpanel.track('AB Test Conversion', event);
        amplitude.getInstance().logEvent('AB Test Conversion', event);
    }
}

// Использование
const abTest = new OptimizelyTracker('user_123');

// Получить вариант для эксперимента
const buttonColor = await abTest.getVariation('button_color_test');
// buttonColor = 'red' | 'blue' | 'green' | null

// Отследить конверсию
if (userClickedButton) {
    abTest.trackConversion('button_color_test', 'button_click');
}

if (userMadePurchase) {
    abTest.trackConversion('button_color_test', 'purchase', 99.99);
}
```

### Google Optimize Integration

```typescript
class GoogleOptimizeTracker {
    private optimizeId: string;

    constructor(optimizeId: string) {
        this.optimizeId = optimizeId;
    }

    async getVariant(experimentId: string): Promise<string> {
        return new Promise((resolve) => {
            // Подождать загрузки Optimize
            if (window.gtag) {
                window.gtag('event', 'optimize.callback', {
                    callback: (value: string) => {
                        resolve(value);
                    }
                });
            } else {
                resolve('0'); // Default variant
            }
        });
    }

    trackExperimentView(experimentId: string, variantId: string) {
        const event = {
            experiment_id: experimentId,
            variant_id: variantId
        };

        gtag('event', 'experiment_impression', event);
        mixpanel.track('Experiment Viewed', event);
        amplitude.getInstance().logEvent('Experiment Viewed', event);
    }

    trackGoalCompletion(experimentId: string, goalName: string, value?: number) {
        const event = {
            experiment_id: experimentId,
            goal_name: goalName,
            value: value || 0
        };

        // Google Optimize автоматически отслеживает через GA4
        gtag('event', goalName, event);

        // Дополнительно в Mixpanel/Amplitude
        mixpanel.track('Goal Completed', event);
        amplitude.getInstance().logEvent('Goal Completed', event);
    }
}

// Использование
const optimize = new GoogleOptimizeTracker('OPT-XXXXXXX');

// Получить вариант
const variant = await optimize.getVariant('experiment_1');
optimize.trackExperimentView('experiment_1', variant);

// Отследить цель
if (userSignedUp) {
    optimize.trackGoalCompletion('experiment_1', 'signup');
}
```

### Custom A/B Testing Implementation

```typescript
class CustomABTest {
    private experimentName: string;
    private variants: string[];
    private userId: string;
    private assignedVariant: string;

    constructor(experimentName: string, variants: string[], userId: string) {
        this.experimentName = experimentName;
        this.variants = variants;
        this.userId = userId;
        this.assignedVariant = this.getAssignedVariant();
        this.trackAssignment();
    }

    private getAssignedVariant(): string {
        // Проверить localStorage для consistency
        const storageKey = `ab_test_${this.experimentName}`;
        const stored = localStorage.getItem(storageKey);

        if (stored && this.variants.includes(stored)) {
            return stored;
        }

        // Случайное назначение с равномерным распределением
        const hash = this.hashUserId(this.userId + this.experimentName);
        const variantIndex = hash % this.variants.length;
        const assigned = this.variants[variantIndex];

        localStorage.setItem(storageKey, assigned);
        return assigned;
    }

    private hashUserId(str: string): number {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash);
    }

    private trackAssignment() {
        const event = {
            experiment_name: this.experimentName,
            variant: this.assignedVariant,
            user_id: this.userId,
            assigned_at: new Date().toISOString()
        };

        gtag('event', 'custom_ab_test_assigned', event);
        mixpanel.track('Custom AB Test Assigned', event);
        amplitude.getInstance().logEvent('Custom AB Test Assigned', event);
    }

    getVariant(): string {
        return this.assignedVariant;
    }

    isVariant(variantName: string): boolean {
        return this.assignedVariant === variantName;
    }

    trackConversion(conversionType: string, value?: number) {
        const event = {
            experiment_name: this.experimentName,
            variant: this.assignedVariant,
            conversion_type: conversionType,
            value: value || 0,
            user_id: this.userId
        };

        gtag('event', 'custom_ab_test_conversion', event);
        mixpanel.track('Custom AB Test Conversion', event);
        amplitude.getInstance().logEvent('Custom AB Test Conversion', event);
    }
}

// Использование
const pricingTest = new CustomABTest(
    'pricing_page_layout',
    ['original', 'variant_a', 'variant_b'],
    'user_456'
);

// Показать соответствующий вариант
if (pricingTest.isVariant('variant_a')) {
    // Показать вариант A
} else if (pricingTest.isVariant('variant_b')) {
    // Показать вариант B
} else {
    // Показать оригинал
}

// Отследить конверсию
if (userSubscribed) {
    pricingTest.trackConversion('subscription', 29.99);
}
```

---

## Analytics Dashboard Implementation

### Real-Time Metrics Dashboard

```typescript
interface DashboardMetric {
    name: string;
    value: number;
    change: number;
    changeType: 'increase' | 'decrease';
    unit: 'number' | 'currency' | 'percentage';
}

class AnalyticsDashboard {
    private metrics: Map<string, DashboardMetric> = new Map();
    private updateInterval: NodeJS.Timeout | null = null;

    async initialize() {
        await this.fetchAllMetrics();
        this.startAutoUpdate(60000); // Обновлять каждую минуту
    }

    private async fetchAllMetrics() {
        const [users, revenue, conversions, engagement] = await Promise.all([
            this.fetchActiveUsers(),
            this.fetchRevenue(),
            this.fetchConversionRate(),
            this.fetchEngagementScore()
        ]);

        this.metrics.set('active_users', users);
        this.metrics.set('revenue', revenue);
        this.metrics.set('conversion_rate', conversions);
        this.metrics.set('engagement_score', engagement);
    }

    private async fetchActiveUsers(): Promise<DashboardMetric> {
        // Получить активных пользователей из GA4
        const response = await fetch('/api/analytics/active-users');
        const data = await response.json();

        return {
            name: 'Active Users',
            value: data.current,
            change: ((data.current - data.previous) / data.previous) * 100,
            changeType: data.current > data.previous ? 'increase' : 'decrease',
            unit: 'number'
        };
    }

    private async fetchRevenue(): Promise<DashboardMetric> {
        const response = await fetch('/api/analytics/revenue');
        const data = await response.json();

        return {
            name: 'Revenue',
            value: data.current,
            change: ((data.current - data.previous) / data.previous) * 100,
            changeType: data.current > data.previous ? 'increase' : 'decrease',
            unit: 'currency'
        };
    }

    private async fetchConversionRate(): Promise<DashboardMetric> {
        const response = await fetch('/api/analytics/conversion-rate');
        const data = await response.json();

        return {
            name: 'Conversion Rate',
            value: data.current,
            change: data.current - data.previous,
            changeType: data.current > data.previous ? 'increase' : 'decrease',
            unit: 'percentage'
        };
    }

    private async fetchEngagementScore(): Promise<DashboardMetric> {
        const response = await fetch('/api/analytics/engagement');
        const data = await response.json();

        return {
            name: 'Engagement Score',
            value: data.current,
            change: ((data.current - data.previous) / data.previous) * 100,
            changeType: data.current > data.previous ? 'increase' : 'decrease',
            unit: 'number'
        };
    }

    private startAutoUpdate(intervalMs: number) {
        this.updateInterval = setInterval(() => {
            this.fetchAllMetrics();
        }, intervalMs);
    }

    stopAutoUpdate() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    getMetrics(): DashboardMetric[] {
        return Array.from(this.metrics.values());
    }

    getMetric(name: string): DashboardMetric | undefined {
        return this.metrics.get(name);
    }
}

// React Component для Dashboard
import React, { useEffect, useState } from 'react';

export function AnalyticsDashboardComponent() {
    const [metrics, setMetrics] = useState<DashboardMetric[]>([]);
    const dashboard = new AnalyticsDashboard();

    useEffect(() => {
        dashboard.initialize().then(() => {
            setMetrics(dashboard.getMetrics());
        });

        const interval = setInterval(() => {
            setMetrics(dashboard.getMetrics());
        }, 60000);

        return () => {
            clearInterval(interval);
            dashboard.stopAutoUpdate();
        };
    }, []);

    const formatValue = (metric: DashboardMetric) => {
        switch (metric.unit) {
            case 'currency':
                return `$${metric.value.toLocaleString()}`;
            case 'percentage':
                return `${metric.value.toFixed(2)}%`;
            default:
                return metric.value.toLocaleString();
        }
    };

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {metrics.map((metric) => (
                <div key={metric.name} className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-sm font-medium text-gray-500">{metric.name}</h3>
                    <p className="text-3xl font-bold mt-2">{formatValue(metric)}</p>
                    <div className={`flex items-center mt-2 ${metric.changeType === 'increase' ? 'text-green-600' : 'text-red-600'}`}>
                        <span className="text-sm font-medium">
                            {metric.changeType === 'increase' ? '↗' : '↘'} {Math.abs(metric.change).toFixed(2)}%
                        </span>
                        <span className="text-xs text-gray-500 ml-2">vs last period</span>
                    </div>
                </div>
            ))}
        </div>
    );
}
```

---

## Mobile App Analytics

### React Native Analytics Integration

```typescript
// React Native Analytics Tracker
import { Platform } from 'react-native';
import analytics from '@react-native-firebase/analytics';

class MobileAnalyticsTracker {
    private platform: string;
    private appVersion: string;

    constructor(appVersion: string) {
        this.platform = Platform.OS;
        this.appVersion = appVersion;
    }

    async logScreenView(screenName: string, screenClass: string) {
        await analytics().logScreenView({
            screen_name: screenName,
            screen_class: screenClass
        });

        // Также в Mixpanel/Amplitude
        mixpanel.track('Screen Viewed', {
            screen_name: screenName,
            screen_class: screenClass,
            platform: this.platform,
            app_version: this.appVersion
        });

        amplitude.getInstance().logEvent('Screen Viewed', {
            screen_name: screenName,
            screen_class: screenClass,
            platform: this.platform,
            app_version: this.appVersion
        });
    }

    async logAppOpen(source?: string) {
        await analytics().logAppOpen();

        mixpanel.track('App Opened', {
            source: source || 'direct',
            platform: this.platform,
            app_version: this.appVersion
        });

        amplitude.getInstance().logEvent('App Opened', {
            source: source || 'direct',
            platform: this.platform,
            app_version: this.appVersion
        });
    }

    async logPushNotificationReceived(notificationId: string, title: string) {
        await analytics().logEvent('notification_received', {
            notification_id: notificationId,
            notification_title: title
        });

        mixpanel.track('Push Notification Received', {
            notification_id: notificationId,
            notification_title: title,
            platform: this.platform
        });

        amplitude.getInstance().logEvent('Push Notification Received', {
            notification_id: notificationId,
            notification_title: title,
            platform: this.platform
        });
    }

    async logInAppPurchase(productId: string, price: number, currency: string) {
        await analytics().logPurchase({
            value: price,
            currency: currency,
            items: [{ item_id: productId }]
        });

        mixpanel.track('In-App Purchase', {
            product_id: productId,
            price: price,
            currency: currency,
            platform: this.platform
        });

        mixpanel.people.increment('Total Purchases');
        mixpanel.people.increment('Lifetime Value', price);

        amplitude.getInstance().logEvent('In-App Purchase', {
            product_id: productId,
            price: price,
            currency: currency,
            platform: this.platform
        });

        const identify = new amplitude.Identify()
            .add('Total Purchases', 1)
            .add('Lifetime Value', price);
        amplitude.getInstance().identify(identify);
    }
}

// Использование в React Native App
const mobileTracker = new MobileAnalyticsTracker('1.2.3');

// Screen navigation
mobileTracker.logScreenView('ProductDetails', 'ProductDetailsScreen');

// App opened
mobileTracker.logAppOpen('push_notification');

// Push notification
mobileTracker.logPushNotificationReceived('notif_123', 'Special Offer');

// In-app purchase
mobileTracker.logInAppPurchase('premium_monthly', 9.99, 'USD');
```

---

## Performance Monitoring

### Web Vitals Tracking

```typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

class PerformanceMonitor {
    constructor() {
        this.initWebVitals();
    }

    private initWebVitals() {
        getCLS(this.sendToAnalytics);
        getFID(this.sendToAnalytics);
        getFCP(this.sendToAnalytics);
        getLCP(this.sendToAnalytics);
        getTTFB(this.sendToAnalytics);
    }

    private sendToAnalytics(metric: any) {
        const event = {
            metric_name: metric.name,
            metric_value: Math.round(metric.value),
            metric_rating: metric.rating,
            page: window.location.pathname
        };

        // GA4
        gtag('event', 'web_vitals', event);

        // Mixpanel
        mixpanel.track('Web Vitals', event);

        // Amplitude
        amplitude.getInstance().logEvent('Web Vitals', event);
    }

    trackPageLoadTime() {
        window.addEventListener('load', () => {
            const perfData = window.performance.timing;
            const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;

            const event = {
                page_load_time_ms: pageLoadTime,
                page: window.location.pathname
            };

            gtag('event', 'page_load_time', event);
            mixpanel.track('Page Load Time', event);
            amplitude.getInstance().logEvent('Page Load Time', event);
        });
    }
}

const perfMonitor = new PerformanceMonitor();
perfMonitor.trackPageLoadTime();
```

---

## Best Practices

### 1. Statistical Significance
```typescript
// Не делать выводы до достижения статистической значимости
const MINIMUM_SAMPLE_SIZE = 1000;
const MINIMUM_RUNTIME_DAYS = 7;

function isTestReady(participants: number, runtimeDays: number): boolean {
    return participants >= MINIMUM_SAMPLE_SIZE && runtimeDays >= MINIMUM_RUNTIME_DAYS;
}
```

### 2. Consistent User Experience
```typescript
// Сохранять пользователя в одном варианте на протяжении всего теста
localStorage.setItem(`ab_test_${experimentName}`, assignedVariant);
```

### 3. Track Everything
```typescript
// Отслеживать и exposure, и conversions
abTest.trackExposure(); // Когда пользователь видит вариант
abTest.trackConversion(); // Когда достигает цели
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
