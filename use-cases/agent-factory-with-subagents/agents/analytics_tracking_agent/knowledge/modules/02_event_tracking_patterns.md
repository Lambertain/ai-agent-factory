# Module 02: Event Tracking Patterns

## Универсальные паттерны отслеживания событий

Этот модуль содержит проверенные паттерны отслеживания ключевых пользовательских событий для различных типов приложений.

---

## E-commerce Purchase Funnel

### Полный цикл покупки

```typescript
// Класс для отслеживания E-commerce воронки
class EcommerceTracker {
    private platform: 'ga4' | 'mixpanel' | 'amplitude';

    constructor(platform: 'ga4' | 'mixpanel' | 'amplitude') {
        this.platform = platform;
    }

    trackProductView(product: {
        id: string;
        name: string;
        category: string;
        price: number;
        currency: string;
    }) {
        const event = {
            product_id: product.id,
            product_name: product.name,
            product_category: product.category,
            price: product.price,
            currency: product.currency
        };

        switch (this.platform) {
            case 'ga4':
                gtag('event', 'view_item', {
                    items: [{
                        item_id: product.id,
                        item_name: product.name,
                        item_category: product.category,
                        price: product.price,
                        currency: product.currency
                    }]
                });
                break;
            case 'mixpanel':
                mixpanel.track('Product Viewed', event);
                break;
            case 'amplitude':
                amplitude.getInstance().logEvent('Product Viewed', event);
                break;
        }
    }

    trackAddToCart(product: {
        id: string;
        name: string;
        quantity: number;
        price: number;
        currency: string;
    }) {
        const event = {
            product_id: product.id,
            product_name: product.name,
            quantity: product.quantity,
            price: product.price,
            total_value: product.price * product.quantity,
            currency: product.currency
        };

        switch (this.platform) {
            case 'ga4':
                gtag('event', 'add_to_cart', {
                    items: [{
                        item_id: product.id,
                        item_name: product.name,
                        quantity: product.quantity,
                        price: product.price
                    }],
                    currency: product.currency,
                    value: product.price * product.quantity
                });
                break;
            case 'mixpanel':
                mixpanel.track('Product Added to Cart', event);
                break;
            case 'amplitude':
                amplitude.getInstance().logEvent('Product Added to Cart', event);
                break;
        }
    }

    trackCheckoutStart(cart: {
        items: Array<{ id: string; name: string; quantity: number; price: number }>;
        total: number;
        currency: string;
    }) {
        const event = {
            cart_size: cart.items.length,
            total_value: cart.total,
            currency: cart.currency,
            item_count: cart.items.reduce((sum, item) => sum + item.quantity, 0)
        };

        switch (this.platform) {
            case 'ga4':
                gtag('event', 'begin_checkout', {
                    items: cart.items.map(item => ({
                        item_id: item.id,
                        item_name: item.name,
                        quantity: item.quantity,
                        price: item.price
                    })),
                    currency: cart.currency,
                    value: cart.total
                });
                break;
            case 'mixpanel':
                mixpanel.track('Checkout Started', event);
                break;
            case 'amplitude':
                amplitude.getInstance().logEvent('Checkout Started', event);
                break;
        }
    }

    trackPurchase(order: {
        orderId: string;
        items: Array<{ id: string; name: string; quantity: number; price: number }>;
        total: number;
        tax: number;
        shipping: number;
        currency: string;
        paymentMethod: string;
    }) {
        const event = {
            order_id: order.orderId,
            total_value: order.total,
            tax: order.tax,
            shipping: order.shipping,
            currency: order.currency,
            payment_method: order.paymentMethod,
            item_count: order.items.reduce((sum, item) => sum + item.quantity, 0)
        };

        switch (this.platform) {
            case 'ga4':
                gtag('event', 'purchase', {
                    transaction_id: order.orderId,
                    value: order.total,
                    tax: order.tax,
                    shipping: order.shipping,
                    currency: order.currency,
                    items: order.items.map(item => ({
                        item_id: item.id,
                        item_name: item.name,
                        quantity: item.quantity,
                        price: item.price
                    }))
                });
                break;
            case 'mixpanel':
                mixpanel.track('Purchase Completed', event);
                mixpanel.people.increment('Total Purchases');
                mixpanel.people.increment('Lifetime Value', order.total);
                break;
            case 'amplitude':
                amplitude.getInstance().logEvent('Purchase Completed', event);
                const identify = new amplitude.Identify()
                    .add('Total Purchases', 1)
                    .add('Lifetime Value', order.total);
                amplitude.getInstance().identify(identify);
                break;
        }
    }
}

// Использование
const tracker = new EcommerceTracker('ga4');

// Пользователь просматривает продукт
tracker.trackProductView({
    id: 'sku123',
    name: 'Wireless Mouse',
    category: 'Electronics',
    price: 29.99,
    currency: 'USD'
});

// Добавляет в корзину
tracker.trackAddToCart({
    id: 'sku123',
    name: 'Wireless Mouse',
    quantity: 1,
    price: 29.99,
    currency: 'USD'
});

// Начинает checkout
tracker.trackCheckoutStart({
    items: [{ id: 'sku123', name: 'Wireless Mouse', quantity: 1, price: 29.99 }],
    total: 29.99,
    currency: 'USD'
});

// Завершает покупку
tracker.trackPurchase({
    orderId: 'order_12345',
    items: [{ id: 'sku123', name: 'Wireless Mouse', quantity: 1, price: 29.99 }],
    total: 34.99,
    tax: 2.50,
    shipping: 2.50,
    currency: 'USD',
    paymentMethod: 'Credit Card'
});
```

---

## Cart Abandonment Tracking

### Отслеживание брошенных корзин

```typescript
class CartAbandonmentTracker {
    private cartCheckInterval: number = 300000; // 5 минут
    private abandonmentThreshold: number = 1800000; // 30 минут
    private cartTimer: NodeJS.Timeout | null = null;

    startTracking(cart: {
        items: Array<any>;
        total: number;
        userId?: string;
    }) {
        // Очистить предыдущий таймер
        if (this.cartTimer) {
            clearTimeout(this.cartTimer);
        }

        // Установить таймер для отслеживания брошенной корзины
        this.cartTimer = setTimeout(() => {
            this.trackCartAbandonment(cart);
        }, this.abandonmentThreshold);
    }

    stopTracking() {
        if (this.cartTimer) {
            clearTimeout(this.cartTimer);
            this.cartTimer = null;
        }
    }

    private trackCartAbandonment(cart: {
        items: Array<any>;
        total: number;
        userId?: string;
    }) {
        const event = {
            cart_size: cart.items.length,
            cart_value: cart.total,
            user_id: cart.userId,
            abandoned_at: new Date().toISOString(),
            items: cart.items.map(item => ({
                product_id: item.id,
                product_name: item.name,
                quantity: item.quantity,
                price: item.price
            }))
        };

        // GA4
        gtag('event', 'cart_abandoned', event);

        // Mixpanel
        mixpanel.track('Cart Abandoned', event);

        // Amplitude
        amplitude.getInstance().logEvent('Cart Abandoned', event);

        // Отправить данные на бэкенд для email reminder
        this.sendAbandonmentEmail(cart);
    }

    private async sendAbandonmentEmail(cart: any) {
        try {
            await fetch('/api/cart-abandonment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userId: cart.userId,
                    items: cart.items,
                    total: cart.total,
                    abandonedAt: new Date().toISOString()
                })
            });
        } catch (error) {
            console.error('Failed to send cart abandonment email:', error);
        }
    }
}

// Использование в React
import { useEffect, useState } from 'react';

function ShoppingCart() {
    const [cart, setCart] = useState({ items: [], total: 0 });
    const tracker = new CartAbandonmentTracker();

    useEffect(() => {
        if (cart.items.length > 0) {
            tracker.startTracking(cart);
        }

        return () => {
            tracker.stopTracking();
        };
    }, [cart]);

    const handleCheckout = () => {
        tracker.stopTracking(); // Остановить отслеживание при начале checkout
        // Продолжить с checkout
    };

    return <div>...</div>;
}
```

---

## Conversion Funnel Tracking

### Отслеживание конверсионных воронок

```typescript
class FunnelTracker {
    private funnelSteps: string[] = [];
    private currentStep: number = 0;
    private funnelStartTime: number = Date.now();

    constructor(funnelName: string, steps: string[]) {
        this.funnelSteps = steps;
        this.trackFunnelStart(funnelName);
    }

    private trackFunnelStart(funnelName: string) {
        const event = {
            funnel_name: funnelName,
            total_steps: this.funnelSteps.length,
            started_at: new Date().toISOString()
        };

        gtag('event', 'funnel_started', event);
        mixpanel.track('Funnel Started', event);
        amplitude.getInstance().logEvent('Funnel Started', event);
    }

    nextStep(additionalData?: Record<string, any>) {
        if (this.currentStep < this.funnelSteps.length) {
            const stepName = this.funnelSteps[this.currentStep];
            const timeInFunnel = Date.now() - this.funnelStartTime;

            const event = {
                step_name: stepName,
                step_number: this.currentStep + 1,
                total_steps: this.funnelSteps.length,
                time_in_funnel_seconds: Math.round(timeInFunnel / 1000),
                ...additionalData
            };

            gtag('event', 'funnel_step_completed', event);
            mixpanel.track('Funnel Step Completed', event);
            amplitude.getInstance().logEvent('Funnel Step Completed', event);

            this.currentStep++;
        }
    }

    trackDropOff(reason?: string) {
        const stepName = this.funnelSteps[this.currentStep];
        const timeInFunnel = Date.now() - this.funnelStartTime;

        const event = {
            dropped_at_step: stepName,
            step_number: this.currentStep + 1,
            total_steps: this.funnelSteps.length,
            time_in_funnel_seconds: Math.round(timeInFunnel / 1000),
            drop_reason: reason
        };

        gtag('event', 'funnel_drop_off', event);
        mixpanel.track('Funnel Drop Off', event);
        amplitude.getInstance().logEvent('Funnel Drop Off', event);
    }

    complete(additionalData?: Record<string, any>) {
        const timeInFunnel = Date.now() - this.funnelStartTime;

        const event = {
            funnel_completed: true,
            total_steps: this.funnelSteps.length,
            completion_time_seconds: Math.round(timeInFunnel / 1000),
            ...additionalData
        };

        gtag('event', 'funnel_completed', event);
        mixpanel.track('Funnel Completed', event);
        amplitude.getInstance().logEvent('Funnel Completed', event);
    }
}

// Использование - Signup Funnel
const signupFunnel = new FunnelTracker('User Signup', [
    'Landing Page Visit',
    'Email Entered',
    'Password Created',
    'Profile Information',
    'Email Verified',
    'Account Created'
]);

// Пользователь заходит на страницу
signupFunnel.nextStep({ utm_source: 'google', utm_medium: 'cpc' });

// Вводит email
signupFunnel.nextStep({ email_domain: 'gmail.com' });

// Создает пароль
signupFunnel.nextStep({ password_strength: 'strong' });

// Уходит со страницы
signupFunnel.trackDropOff('Page closed before completion');

// ИЛИ завершает регистрацию
signupFunnel.complete({ user_type: 'free', referral_code: 'FRIEND123' });
```

---

## Custom Event Patterns

### Видео контент

```typescript
class VideoTracker {
    private videoId: string;
    private videoDuration: number;
    private milestones: number[] = [0.25, 0.5, 0.75, 1.0];
    private trackedMilestones: Set<number> = new Set();

    constructor(videoId: string, videoDuration: number) {
        this.videoId = videoId;
        this.videoDuration = videoDuration;
        this.trackVideoStart();
    }

    private trackVideoStart() {
        const event = {
            video_id: this.videoId,
            video_duration: this.videoDuration
        };

        gtag('event', 'video_start', event);
        mixpanel.track('Video Started', event);
        amplitude.getInstance().logEvent('Video Started', event);
    }

    updateProgress(currentTime: number) {
        const progress = currentTime / this.videoDuration;

        this.milestones.forEach(milestone => {
            if (progress >= milestone && !this.trackedMilestones.has(milestone)) {
                this.trackMilestone(milestone, currentTime);
                this.trackedMilestones.add(milestone);
            }
        });
    }

    private trackMilestone(milestone: number, currentTime: number) {
        const event = {
            video_id: this.videoId,
            milestone_percent: milestone * 100,
            current_time: currentTime,
            video_duration: this.videoDuration
        };

        const eventName = milestone === 1.0 ? 'video_complete' : `video_progress_${milestone * 100}`;

        gtag('event', eventName, event);
        mixpanel.track(`Video ${milestone === 1.0 ? 'Completed' : 'Progress ' + (milestone * 100) + '%'}`, event);
        amplitude.getInstance().logEvent(`Video ${milestone === 1.0 ? 'Completed' : 'Progress'}`, event);
    }

    trackPause(currentTime: number) {
        const event = {
            video_id: this.videoId,
            paused_at: currentTime,
            progress_percent: (currentTime / this.videoDuration) * 100
        };

        gtag('event', 'video_pause', event);
        mixpanel.track('Video Paused', event);
        amplitude.getInstance().logEvent('Video Paused', event);
    }
}
```

### Form Interaction Tracking

```typescript
class FormTracker {
    private formId: string;
    private formStartTime: number | null = null;
    private fieldInteractions: Map<string, number> = new Map();

    constructor(formId: string) {
        this.formId = formId;
    }

    trackFormStart() {
        this.formStartTime = Date.now();

        const event = {
            form_id: this.formId,
            started_at: new Date().toISOString()
        };

        gtag('event', 'form_start', event);
        mixpanel.track('Form Started', event);
        amplitude.getInstance().logEvent('Form Started', event);
    }

    trackFieldInteraction(fieldName: string) {
        const interactionCount = (this.fieldInteractions.get(fieldName) || 0) + 1;
        this.fieldInteractions.set(fieldName, interactionCount);

        if (interactionCount === 1) {
            const event = {
                form_id: this.formId,
                field_name: fieldName
            };

            gtag('event', 'form_field_interaction', event);
            mixpanel.track('Form Field Interacted', event);
            amplitude.getInstance().logEvent('Form Field Interacted', event);
        }
    }

    trackFormSubmission(success: boolean, errorFields?: string[]) {
        const timeToComplete = this.formStartTime ? Date.now() - this.formStartTime : 0;

        const event = {
            form_id: this.formId,
            success,
            time_to_complete_seconds: Math.round(timeToComplete / 1000),
            field_interaction_count: this.fieldInteractions.size,
            error_fields: errorFields || []
        };

        const eventName = success ? 'form_submit_success' : 'form_submit_error';

        gtag('event', eventName, event);
        mixpanel.track(success ? 'Form Submitted' : 'Form Submission Failed', event);
        amplitude.getInstance().logEvent(success ? 'Form Submitted' : 'Form Submission Failed', event);
    }
}

// Использование в React
function ContactForm() {
    const formTracker = new FormTracker('contact_form');

    const handleFocus = (fieldName: string) => {
        if (!formTracker.formStartTime) {
            formTracker.trackFormStart();
        }
        formTracker.trackFieldInteraction(fieldName);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await submitForm();
            formTracker.trackFormSubmission(true);
        } catch (error) {
            formTracker.trackFormSubmission(false, ['email', 'phone']);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input onFocus={() => handleFocus('name')} />
            <input onFocus={() => handleFocus('email')} />
            <button type="submit">Submit</button>
        </form>
    );
}
```

---

## Best Practices

### 1. Consistent Event Naming
```typescript
// ПРАВИЛЬНО - понятная иерархия
'Product Viewed'
'Product Added to Cart'
'Product Removed from Cart'

// НЕПРАВИЛЬНО - несогласованные названия
'view_product'
'added_to_cart'
'cart_item_remove'
```

### 2. Include Context in Events
```typescript
// ПРАВИЛЬНО - полный контекст
trackEvent('Button Clicked', {
    button_name: 'Sign Up',
    button_location: 'Header',
    page: 'Homepage',
    device_type: 'Mobile'
});

// НЕПРАВИЛЬНО - недостаточно контекста
trackEvent('Button Clicked', { button: 'signup' });
```

### 3. Track Both Success and Failure
```typescript
// Отслеживать успешные и неуспешные действия
trackFormSubmission(true); // Success
trackFormSubmission(false, ['email_invalid', 'phone_required']); // Failure with reasons
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
