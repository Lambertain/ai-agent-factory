# Analytics Tracking Agent Knowledge Base

> Универсальный агент для интеграции и управления аналитикой веб-приложений

---

## Общие правила всех агентов

**ОБЯЗАТЕЛЬНО ПРОЧИТАЙ ПЕРЕД НАЧАЛОМ РАБОТЫ:**

📖 [Общие правила для всех агентов](../_shared/agent_common_rules.md)

**Этот документ содержит:**
- Универсальные стандарты кодирования
- Правила работы с проектами
- Структуру ответов
- Best practices для всех агентов

---

## Системный промпт Analytics Tracking Agent

```
Вы - Analytics Tracking Agent, эксперт по интеграции и управлению аналитикой в веб-приложениях.

ВАША ЭКСПЕРТИЗА:
- Интеграция Google Analytics 4, Mixpanel, Amplitude
- Разработка event tracking паттернов для различных user flows
- Реализация GDPR/CCPA compliant аналитических решений
- Настройка A/B тестирования и экспериментов
- Построение real-time analytics dashboards
- Оптимизация производительности аналитических скриптов
- Работа с MCP серверами для доступа к аналитическим API

ТЕХНОЛОГИЧЕСКИЙ СТЕК:
- Analytics Platforms: GA4, Mixpanel, Amplitude
- A/B Testing: Optimizely, Google Optimize, custom solutions
- Privacy: GDPR Consent Mode, cookie management
- Frontend: React hooks, TypeScript, Context API
- Performance: Event batching, lazy loading
- MCP Integration: Google Analytics API, Fetch MCP

КЛЮЧЕВЫЕ КОМПЕТЕНЦИИ:
1. Мультиплатформенная интеграция (GA4 + Mixpanel + Amplitude)
2. Privacy-first подход с granular consent management
3. Production-ready tracking patterns для E-commerce, Forms, Video, Funnels
4. Real-time dashboard с auto-refresh и WebSocket поддержкой
5. Custom A/B testing с hash-based assignment
6. Web Vitals monitoring (CLS, FID, FCP, LCP, TTFB)
7. User segmentation с criteria-based matching
8. Session management с timeout handling
9. Data quality assurance с event validation

ПРИНЦИПЫ РАБОТЫ:
✅ Consent checking перед любым tracking
✅ Type-safe event properties через TypeScript interfaces
✅ Error handling для всех аналитических вызовов
✅ Event batching для оптимизации производительности
✅ Lazy loading аналитических скриптов
✅ User ID hashing для анонимизации
✅ Consistent event naming conventions
✅ Multi-platform property mapping

ПОДХОД К РЕШЕНИЮ ЗАДАЧ:
1. Определить платформы аналитики (GA4/Mixpanel/Amplitude)
2. Разработать event schema с typed properties
3. Реализовать consent management перед tracking
4. Создать tracker classes с multi-platform support
5. Добавить error handling и validation
6. Оптимизировать производительность (batching/lazy loading)
7. Интегрировать с React через hooks/providers
8. Настроить MCP integration для API доступа
```

---

## Модули знаний

База знаний разделена на 5 специализированных модулей для быстрого доступа к нужной информации:

### 📊 [Module 01: Analytics Platforms Integration](./modules/01_analytics_platforms.md)
**Размер:** 506 строк
**Когда использовать:** Начальная настройка аналитики, интеграция платформ

**Содержит:**
- Google Analytics 4 setup и event tracking
- Mixpanel integration с user profiles
- Amplitude session tracking
- React integration patterns (hooks, providers)
- Best practices (naming, error handling, user identification)

**Ключевые классы:**
- Нет классов (базовые паттерны и утилиты)

**Пример использования:**
```typescript
// GA4 Enhanced E-commerce
gtag('event', 'purchase', {
    transaction_id: '12345',
    value: 25.42,
    currency: 'USD',
    items: [...]
});

// React hook
function usePageView(path: string, title: string) {
    useEffect(() => {
        gtag('config', 'G-XXXXXXXXXX', {
            page_path: path,
            page_title: title
        });
    }, [path, title]);
}
```

---

### 🎯 [Module 02: Event Tracking Patterns](./modules/02_event_tracking_patterns.md)
**Размер:** 514 строк
**Когда использовать:** Разработка tracking логики для user flows

**Содержит:**
- E-commerce purchase funnel tracking
- Cart abandonment detection (30-min timeout)
- Conversion funnel с drop-off analysis
- Video progress tracking (milestone-based)
- Form interaction tracking

**Ключевые классы:**
- `EcommerceTracker` - полный цикл покупки
- `CartAbandonmentTracker` - отслеживание брошенных корзин
- `FunnelTracker` - многошаговые воронки
- `VideoTracker` - прогресс видео (25%/50%/75%/100%)
- `FormTracker` - взаимодействие с формами

**Пример использования:**
```typescript
const tracker = new EcommerceTracker('ga4');

tracker.trackProductView(product);
tracker.trackAddToCart(product, 1);
tracker.trackCheckoutStarted(cart);
tracker.trackPurchase(order);
```

---

### 🔒 [Module 03: Privacy & Compliance](./modules/03_privacy_compliance.md)
**Размер:** 492 строки
**Когда использовать:** Реализация GDPR/CCPA compliance, consent management

**Содержит:**
- GDPR Consent Mode для GA4
- ConsentManager с granular permissions
- Privacy-safe tracking (user ID hashing)
- Cookie consent banner (React component)
- Right to access / Right to be forgotten

**Ключевые классы:**
- `ConsentManager` - управление согласиями (analytics/marketing/functional/necessary)
- `PrivacySafeTracker` - анонимизированное отслеживание
- `PrivacyCompliance` - GDPR right to access/forgotten
- `CookieConsentBanner` (React) - баннер согласия

**Пример использования:**
```typescript
const consentManager = new ConsentManager();

// Проверка перед tracking
if (consentManager.canTrack('analytics')) {
    gtag('event', 'page_view');
}

// Обновление согласий
consentManager.updateConsent({
    analytics: true,
    marketing: false
});
```

---

### 🧪 [Module 04: A/B Testing & Dashboards](./modules/04_ab_testing_dashboards.md)
**Размер:** 525 строк
**Когда использовать:** Настройка экспериментов, real-time monitoring

**Содержит:**
- Optimizely SDK integration
- Google Optimize с GA4
- Custom A/B testing (hash-based assignment)
- Real-time analytics dashboard
- React Native mobile analytics
- Web Vitals performance monitoring

**Ключевые классы:**
- `OptimizelyTracker` - эксперименты и конверсии
- `GoogleOptimizeTracker` - GA4 integration
- `CustomABTest` - hash-based variant assignment
- `AnalyticsDashboard` - real-time метрики
- `MobileAnalyticsTracker` - React Native Firebase
- `PerformanceMonitor` - Web Vitals (CLS, FID, FCP, LCP, TTFB)

**Пример использования:**
```typescript
const abTest = new CustomABTest('checkout_flow', ['control', 'variant_a'], userId);

if (abTest.isVariant('variant_a')) {
    // Показать новый checkout
}

abTest.trackConversion('purchase', 99.99);
```

---

### ⚙️ [Module 05: MCP Integration & Best Practices](./modules/05_mcp_best_practices.md)
**Когда использовать:** Подключение к API аналитики, advanced patterns

**Содержит:**
- Google Analytics API MCP integration
- Fetch MCP для Mixpanel/Amplitude
- User segmentation с criteria matching
- Analytics best practices (naming, properties, errors)
- Session management (30-min timeout)
- Data quality assurance (validation)
- Performance optimization (batching, lazy loading)

**Ключевые классы:**
- `GoogleAnalyticsMCP` - realtime users, top pages, demographics, conversions
- `ExternalAnalyticsMCP` - Mixpanel/Amplitude API
- `UserSegmentation` - criteria-based segments
- `AnalyticsErrorTracker` - JS errors, API errors, form validation
- `SessionManager` - timeout handling
- `AnalyticsQA` - event validation
- `EventBatcher` - batch size 10, 5-sec flush
- `LazyAnalyticsLoader` - on-scroll loading

**Пример использования:**
```typescript
const gaMcp = new GoogleAnalyticsMCP('GA_PROPERTY_ID');

const activeUsers = await gaMcp.fetchRealtimeUsers();
const conversions = await gaMcp.fetchConversionEvents('purchase', 30);

// Segmentation
const segmentation = new UserSegmentation();
segmentation.defineSegment({
    id: 'high_value',
    name: 'High Value Users',
    criteria: [
        { field: 'lifetime_value', operator: 'greater_than', value: 1000 }
    ]
});

const segments = segmentation.getUserSegments(user);
```

---

## Навигация по задачам

### Выбор модуля по типу задачи:

**Начальная интеграция платформ:**
→ Module 01 (Analytics Platforms Integration)

**Разработка tracking логики:**
→ Module 02 (Event Tracking Patterns)

**GDPR/CCPA compliance:**
→ Module 03 (Privacy & Compliance)

**A/B тестирование, dashboards:**
→ Module 04 (A/B Testing & Dashboards)

**MCP integration, optimization:**
→ Module 05 (MCP Integration & Best Practices)

---

## Best Practices Checklist

### Перед началом разработки:

- [ ] Определить нужные платформы (GA4/Mixpanel/Amplitude)
- [ ] Разработать event naming convention
- [ ] Создать TypeScript interfaces для event properties
- [ ] Спланировать consent management стратегию
- [ ] Выбрать паттерн React integration (hooks/providers)

### Во время разработки:

- [ ] Проверять consent перед каждым tracking вызовом
- [ ] Использовать try-catch для всех аналитических вызовов
- [ ] Применять event batching для оптимизации
- [ ] Добавлять type hints для всех event properties
- [ ] Хешировать user IDs для анонимизации
- [ ] Валидировать события перед отправкой

### После разработки:

- [ ] Тестировать tracking в режиме debug
- [ ] Проверить consent flow на всех платформах
- [ ] Убедиться в корректности event properties
- [ ] Проверить производительность (Network tab)
- [ ] Задокументировать custom events
- [ ] Настроить GA4 DebugView / Mixpanel Live View

---

## Быстрые ссылки

### Модули по размеру (для быстрого поиска):

1. **Module 03** - Privacy & Compliance (492 строки) - самый компактный
2. **Module 01** - Analytics Platforms (506 строк)
3. **Module 02** - Event Tracking Patterns (514 строк)
4. **Module 04** - A/B Testing & Dashboards (525 строк)
5. **Module 05** - MCP Integration & Best Practices

### Модули по частоте использования:

**Ежедневно:**
- Module 02 (Event Tracking Patterns)
- Module 03 (Privacy & Compliance)

**При настройке:**
- Module 01 (Analytics Platforms Integration)
- Module 04 (A/B Testing & Dashboards)

**Advanced cases:**
- Module 05 (MCP Integration & Best Practices)

---

## Архитектурные принципы

### Multi-platform Architecture

Все tracker классы поддерживают 3 платформы одновременно:

```typescript
class Tracker {
    private platform: 'ga4' | 'mixpanel' | 'amplitude';

    track(event: string, properties: any) {
        switch (this.platform) {
            case 'ga4':
                gtag('event', event, properties);
                break;
            case 'mixpanel':
                mixpanel.track(event, properties);
                break;
            case 'amplitude':
                amplitude.getInstance().logEvent(event, properties);
                break;
        }
    }
}
```

### Privacy-First Design

Каждый tracking вызов проверяет consent:

```typescript
if (consentManager.canTrack('analytics')) {
    tracker.track('event_name', properties);
}
```

### Type-Safe Events

Использование TypeScript для гарантии корректности:

```typescript
interface ProductEvent extends BaseEventProperties {
    product_id: string;
    product_name: string;
    price: number;
    currency: string;
}

function trackProductView(product: ProductEvent) {
    // TypeScript гарантирует наличие всех полей
}
```

### Performance Optimization

```typescript
// Batching
const batcher = new EventBatcher();
batcher.addEvent('event1', props1);
batcher.addEvent('event2', props2);
// Отправка batch каждые 5 секунд или при достижении 10 событий

// Lazy Loading
const loader = new LazyAnalyticsLoader();
loader.loadOnScroll('https://cdn.analytics.com/script.js');
```

---

## Версионная информация

**Версия базы знаний:** 2.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
**Последнее обновление:** 2025-10-15

**Changelog:**
- **v2.0** (2025-10-15) - Модуляризация: 631 строка → 5 модулей
  - Module 01: Analytics Platforms (506 строк)
  - Module 02: Event Tracking Patterns (514 строк)
  - Module 03: Privacy & Compliance (492 строки)
  - Module 04: A/B Testing & Dashboards (525 строк)
  - Module 05: MCP Integration & Best Practices
- **v1.0** - Монолитный файл (631 строка) - архивирован

**Метрики модуляризации:**
- Уменьшение главного файла: 631 → ~350 строк (45% reduction)
- Количество модулей: 5 (оптимально для данной области)
- Средний размер модуля: ~510 строк
- Полнота кода: 100% (нет placeholder '...')
- React integration: hooks, providers, components
- Multi-platform support: GA4 + Mixpanel + Amplitude

---

## Связанные ресурсы

### Внутренние агенты:
- **UI/UX Enhancement Agent** - дизайн analytics dashboards
- **Performance Optimization Agent** - оптимизация скриптов аналитики
- **Privacy/Security Agent** - аудит GDPR/CCPA compliance
- **API Development Agent** - backend интеграция для MCP серверов

### Внешние ресурсы:
- [Google Analytics 4 Documentation](https://developers.google.com/analytics/devguides/collection/ga4)
- [Mixpanel Developer Docs](https://developer.mixpanel.com/)
- [Amplitude Developer Center](https://www.docs.developers.amplitude.com/)
- [Web Vitals Library](https://github.com/GoogleChrome/web-vitals)
- [GDPR Consent Mode](https://support.google.com/analytics/answer/9976101)

---

**🎯 ПОМНИ:** Качество аналитики = качество данных для принятия решений!
