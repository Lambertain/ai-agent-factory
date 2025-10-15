# Module 03: Privacy & Compliance

## Privacy-Compliant Analytics Tracking

Этот модуль содержит паттерны для соблюдения требований GDPR, CCPA и других privacy regulations при работе с аналитикой.

---

## Consent Management System

### ConsentManager Class

```typescript
type ConsentType = 'analytics' | 'marketing' | 'functional' | 'necessary';

interface ConsentPreferences {
    analytics: boolean;
    marketing: boolean;
    functional: boolean;
    necessary: boolean; // Всегда true, необходимые cookies
}

class ConsentManager {
    private preferences: ConsentPreferences;
    private consentGiven: boolean = false;
    private storageKey: string = 'user_consent_preferences';

    constructor() {
        this.preferences = this.loadPreferences();
    }

    private loadPreferences(): ConsentPreferences {
        const stored = localStorage.getItem(this.storageKey);
        if (stored) {
            try {
                const parsed = JSON.parse(stored);
                this.consentGiven = true;
                return parsed;
            } catch {
                return this.getDefaultPreferences();
            }
        }
        return this.getDefaultPreferences();
    }

    private getDefaultPreferences(): ConsentPreferences {
        return {
            analytics: false,
            marketing: false,
            functional: false,
            necessary: true
        };
    }

    updateConsent(preferences: Partial<ConsentPreferences>) {
        this.preferences = {
            ...this.preferences,
            ...preferences,
            necessary: true // Всегда true
        };
        this.consentGiven = true;

        localStorage.setItem(this.storageKey, JSON.stringify(this.preferences));
        this.updateAnalyticsPlatforms();
        this.trackConsentChange(preferences);
    }

    private updateAnalyticsPlatforms() {
        // Google Analytics 4
        if (this.preferences.analytics) {
            gtag('consent', 'update', {
                analytics_storage: 'granted',
                ad_storage: this.preferences.marketing ? 'granted' : 'denied'
            });
        } else {
            gtag('consent', 'update', {
                analytics_storage: 'denied',
                ad_storage: 'denied'
            });
        }

        // Mixpanel
        if (this.preferences.analytics) {
            mixpanel.opt_in_tracking();
        } else {
            mixpanel.opt_out_tracking();
        }

        // Amplitude
        if (this.preferences.analytics) {
            amplitude.getInstance().setOptOut(false);
        } else {
            amplitude.getInstance().setOptOut(true);
        }
    }

    private trackConsentChange(preferences: Partial<ConsentPreferences>) {
        // Отслеживаем изменение consent только если analytics разрешена
        if (this.preferences.analytics) {
            const event = {
                consent_analytics: this.preferences.analytics,
                consent_marketing: this.preferences.marketing,
                consent_functional: this.preferences.functional,
                changed_preferences: Object.keys(preferences)
            };

            gtag('event', 'consent_updated', event);
            mixpanel.track('Consent Updated', event);
            amplitude.getInstance().logEvent('Consent Updated', event);
        }
    }

    hasConsent(type: ConsentType): boolean {
        return this.preferences[type];
    }

    hasGivenConsent(): boolean {
        return this.consentGiven;
    }

    getPreferences(): ConsentPreferences {
        return { ...this.preferences };
    }

    revokeAllConsent() {
        this.updateConsent({
            analytics: false,
            marketing: false,
            functional: false
        });
    }

    // GDPR Right to be forgotten
    deleteUserData(userId: string) {
        // Удаляем локальные данные
        localStorage.removeItem(this.storageKey);
        this.preferences = this.getDefaultPreferences();

        // GA4 - удалить User ID
        gtag('config', 'G-XXXXXXXXXX', {
            user_id: undefined
        });

        // Mixpanel - удалить профиль
        mixpanel.people.delete_user();

        // Amplitude - удалить данные
        amplitude.getInstance().setUserId(null);
        amplitude.getInstance().regenerateDeviceId();

        // Отправить запрос на backend для полного удаления
        this.requestDataDeletion(userId);
    }

    private async requestDataDeletion(userId: string) {
        try {
            await fetch('/api/gdpr/delete-user-data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId })
            });
        } catch (error) {
            console.error('Failed to request data deletion:', error);
        }
    }
}

// Глобальный instance
export const consentManager = new ConsentManager();
```

---

## GDPR Compliant Initialization

### Google Analytics 4 with Consent Mode

```javascript
// Инициализация GA4 с Consent Mode
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}

  // Установить default consent state (до получения пользовательского согласия)
  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    wait_for_update: 2000 // Ждать 2 секунды до загрузки consent
  });

  // Инициализация GA4
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX', {
    anonymize_ip: true, // IP anonymization
    allow_google_signals: false, // Отключить персонализацию по умолчанию
    allow_ad_personalization_signals: false
  });
</script>

<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>

<script>
  // После получения consent от пользователя
  function updateConsentState(analyticsAllowed, marketingAllowed) {
    gtag('consent', 'update', {
      analytics_storage: analyticsAllowed ? 'granted' : 'denied',
      ad_storage: marketingAllowed ? 'granted' : 'denied',
      ad_user_data: marketingAllowed ? 'granted' : 'denied',
      ad_personalization: marketingAllowed ? 'granted' : 'denied'
    });
  }
</script>
```

---

## Privacy-Safe Event Tracking

### Anonymized User Tracking

```typescript
class PrivacySafeTracker {
    private hashUserId(userId: string): string {
        // Простой hash для анонимизации (в production использовать crypto.subtle.digest)
        let hash = 0;
        for (let i = 0; i < userId.length; i++) {
            const char = userId.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        return 'user_' + Math.abs(hash).toString(36);
    }

    trackEventPrivate(eventName: string, params: Record<string, any>) {
        // Проверить consent перед отправкой
        if (!consentManager.hasConsent('analytics')) {
            console.log('Analytics consent not granted, skipping event:', eventName);
            return;
        }

        // Удалить потенциально чувствительные данные
        const sanitizedParams = this.sanitizeParams(params);

        // Отправить анонимизированное событие
        gtag('event', eventName, sanitizedParams);
        mixpanel.track(eventName, sanitizedParams);
        amplitude.getInstance().logEvent(eventName, sanitizedParams);
    }

    private sanitizeParams(params: Record<string, any>): Record<string, any> {
        const sensitiveKeys = ['email', 'phone', 'password', 'ssn', 'credit_card'];
        const sanitized: Record<string, any> = {};

        for (const [key, value] of Object.entries(params)) {
            // Пропустить чувствительные ключи
            if (sensitiveKeys.some(sensitive => key.toLowerCase().includes(sensitive))) {
                continue;
            }

            // Анонимизировать user_id
            if (key === 'user_id' && typeof value === 'string') {
                sanitized[key] = this.hashUserId(value);
            } else {
                sanitized[key] = value;
            }
        }

        return sanitized;
    }

    identifyUserPrivate(userId: string, traits: Record<string, any>) {
        if (!consentManager.hasConsent('analytics')) {
            return;
        }

        const hashedUserId = this.hashUserId(userId);
        const sanitizedTraits = this.sanitizeParams(traits);

        // GA4
        gtag('config', 'G-XXXXXXXXXX', {
            user_id: hashedUserId
        });

        // Mixpanel
        mixpanel.identify(hashedUserId);
        mixpanel.people.set(sanitizedTraits);

        // Amplitude
        amplitude.getInstance().setUserId(hashedUserId);
        amplitude.getInstance().setUserProperties(sanitizedTraits);
    }
}

export const privacyTracker = new PrivacySafeTracker();
```

---

## Cookie Consent Banner Integration

### React Cookie Consent Component

```typescript
import React, { useState, useEffect } from 'react';
import { consentManager } from './ConsentManager';

export function CookieConsentBanner() {
    const [showBanner, setShowBanner] = useState(false);
    const [showDetails, setShowDetails] = useState(false);
    const [preferences, setPreferences] = useState(consentManager.getPreferences());

    useEffect(() => {
        if (!consentManager.hasGivenConsent()) {
            setShowBanner(true);
        }
    }, []);

    const handleAcceptAll = () => {
        consentManager.updateConsent({
            analytics: true,
            marketing: true,
            functional: true
        });
        setShowBanner(false);
    };

    const handleRejectAll = () => {
        consentManager.updateConsent({
            analytics: false,
            marketing: false,
            functional: false
        });
        setShowBanner(false);
    };

    const handleSavePreferences = () => {
        consentManager.updateConsent(preferences);
        setShowBanner(false);
    };

    const updatePreference = (key: keyof typeof preferences, value: boolean) => {
        setPreferences(prev => ({
            ...prev,
            [key]: value
        }));
    };

    if (!showBanner) return null;

    return (
        <div className="fixed bottom-0 left-0 right-0 bg-gray-900 text-white p-6 z-50">
            <div className="max-w-6xl mx-auto">
                <h2 className="text-xl font-bold mb-2">Cookie Consent</h2>
                <p className="mb-4">
                    We use cookies to enhance your browsing experience and analyze our traffic.
                    Please choose your preferences below.
                </p>

                {!showDetails ? (
                    <div className="flex gap-4">
                        <button
                            onClick={handleAcceptAll}
                            className="px-6 py-2 bg-blue-600 rounded hover:bg-blue-700"
                        >
                            Accept All
                        </button>
                        <button
                            onClick={handleRejectAll}
                            className="px-6 py-2 bg-gray-700 rounded hover:bg-gray-600"
                        >
                            Reject All
                        </button>
                        <button
                            onClick={() => setShowDetails(true)}
                            className="px-6 py-2 border border-gray-600 rounded hover:bg-gray-800"
                        >
                            Customize
                        </button>
                    </div>
                ) : (
                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <label>
                                <span className="font-semibold">Necessary Cookies</span>
                                <p className="text-sm text-gray-400">
                                    Required for the website to function properly
                                </p>
                            </label>
                            <input type="checkbox" checked disabled className="w-5 h-5" />
                        </div>

                        <div className="flex items-center justify-between">
                            <label>
                                <span className="font-semibold">Analytics Cookies</span>
                                <p className="text-sm text-gray-400">
                                    Help us understand how visitors use our website
                                </p>
                            </label>
                            <input
                                type="checkbox"
                                checked={preferences.analytics}
                                onChange={(e) => updatePreference('analytics', e.target.checked)}
                                className="w-5 h-5"
                            />
                        </div>

                        <div className="flex items-center justify-between">
                            <label>
                                <span className="font-semibold">Marketing Cookies</span>
                                <p className="text-sm text-gray-400">
                                    Used to deliver personalized advertisements
                                </p>
                            </label>
                            <input
                                type="checkbox"
                                checked={preferences.marketing}
                                onChange={(e) => updatePreference('marketing', e.target.checked)}
                                className="w-5 h-5"
                            />
                        </div>

                        <div className="flex items-center justify-between">
                            <label>
                                <span className="font-semibold">Functional Cookies</span>
                                <p className="text-sm text-gray-400">
                                    Enable enhanced functionality and personalization
                                </p>
                            </label>
                            <input
                                type="checkbox"
                                checked={preferences.functional}
                                onChange={(e) => updatePreference('functional', e.target.checked)}
                                className="w-5 h-5"
                            />
                        </div>

                        <div className="flex gap-4">
                            <button
                                onClick={handleSavePreferences}
                                className="px-6 py-2 bg-blue-600 rounded hover:bg-blue-700"
                            >
                                Save Preferences
                            </button>
                            <button
                                onClick={() => setShowDetails(false)}
                                className="px-6 py-2 border border-gray-600 rounded hover:bg-gray-800"
                            >
                                Back
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
```

---

## Privacy Policy Integration

### User Data Access (GDPR Right to Access)

```typescript
class PrivacyCompliance {
    async exportUserData(userId: string): Promise<UserDataExport> {
        // Собрать данные из всех источников
        const gaData = await this.fetchGAData(userId);
        const mixpanelData = await this.fetchMixpanelData(userId);
        const amplitudeData = await this.fetchAmplitudeData(userId);
        const localData = this.fetchLocalStorageData(userId);

        return {
            userId,
            exportDate: new Date().toISOString(),
            analytics: {
                googleAnalytics: gaData,
                mixpanel: mixpanelData,
                amplitude: amplitudeData
            },
            localStorage: localData,
            cookies: this.getCookiesList()
        };
    }

    private async fetchGAData(userId: string) {
        // Использовать GA4 Reporting API
        try {
            const response = await fetch('/api/analytics/ga4-export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId })
            });
            return await response.json();
        } catch {
            return null;
        }
    }

    private async fetchMixpanelData(userId: string) {
        // Mixpanel Data Export API
        try {
            const response = await fetch('/api/analytics/mixpanel-export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId })
            });
            return await response.json();
        } catch {
            return null;
        }
    }

    private async fetchAmplitudeData(userId: string) {
        // Amplitude Export API
        try {
            const response = await fetch('/api/analytics/amplitude-export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId })
            });
            return await response.json();
        } catch {
            return null;
        }
    }

    private fetchLocalStorageData(userId: string) {
        const relevantKeys = Object.keys(localStorage).filter(key =>
            key.includes('user') || key.includes('consent') || key.includes('preferences')
        );

        const data: Record<string, any> = {};
        relevantKeys.forEach(key => {
            try {
                data[key] = JSON.parse(localStorage.getItem(key) || '');
            } catch {
                data[key] = localStorage.getItem(key);
            }
        });

        return data;
    }

    private getCookiesList(): Array<{ name: string; value: string; expires?: string }> {
        return document.cookie.split(';').map(cookie => {
            const [name, value] = cookie.trim().split('=');
            return { name, value };
        });
    }

    async downloadUserDataExport(userId: string) {
        const data = await this.exportUserData(userId);
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `user-data-export-${userId}-${Date.now()}.json`;
        a.click();

        URL.revokeObjectURL(url);
    }
}

export const privacyCompliance = new PrivacyCompliance();
```

---

## Best Practices

### 1. Default Deny
```typescript
// ПРАВИЛЬНО - отказывать по умолчанию
gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied'
});

// НЕПРАВИЛЬНО - разрешать по умолчанию
gtag('consent', 'default', {
    analytics_storage: 'granted'
});
```

### 2. Granular Consent
```typescript
// ПРАВИЛЬНО - детальный выбор
{
    analytics: boolean;
    marketing: boolean;
    functional: boolean;
}

// НЕПРАВИЛЬНО - всё или ничего
{
    allCookies: boolean;
}
```

### 3. Consent Persistence
```typescript
// Сохранять consent на 12 месяцев (GDPR requirement)
const CONSENT_EXPIRY_MONTHS = 12;

function saveConsent(preferences: ConsentPreferences) {
    const expiry = new Date();
    expiry.setMonth(expiry.getMonth() + CONSENT_EXPIRY_MONTHS);

    localStorage.setItem('consent_preferences', JSON.stringify({
        preferences,
        expiresAt: expiry.toISOString()
    }));
}
```

### 4. Privacy by Design
```typescript
// Всегда проверять consent перед tracking
function trackEvent(eventName: string, params: any) {
    if (!consentManager.hasConsent('analytics')) {
        return; // Не отслеживать без согласия
    }
    // Продолжить отслеживание
}
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
