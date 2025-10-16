# Module 03: Performance & Monitoring

## 📊 Overview: Performance в PWA

Performance - критический фактор успеха Progressive Web Apps. Медленные приложения теряют пользователей: 53% покидают сайт, который загружается более 3 секунд.

**Core Metrics:**
- **Core Web Vitals** - ключевые метрики UX от Google
- **Custom Metrics** - специфичные для приложения метрики
- **Privacy-First Analytics** - сбор данных без нарушения приватности

**Business Impact:**
- 1 секунда задержки = 7% снижение конверсии
- 0.1s улучшение = 8% рост engagement
- Good Core Web Vitals = SEO boost

---

## 🎯 Core Web Vitals Integration

**Core Web Vitals** - это набор метрик от Google, измеряющих real-world user experience.

**3 ключевые метрики:**
1. **LCP (Largest Contentful Paint)** - загрузка основного контента (<2.5s = good)
2. **FID (First Input Delay)** - отзывчивость на первый клик (<100ms = good)
3. **CLS (Cumulative Layout Shift)** - стабильность layout (<0.1 = good)

**Дополнительные метрики:**
- **TTFB (Time to First Byte)** - серверная производительность
- **FCP (First Contentful Paint)** - когда появляется первый контент

### Базовая реализация

```javascript
import {getCLS, getFID, getLCP, getTTFB, getFCP} from 'web-vitals';

class PerformanceMonitor {
  constructor() {
    this.metrics = {};
    this.initializeMonitoring();
  }

  initializeMonitoring() {
    // Core Web Vitals
    getCLS(metric => this.logMetric('CLS', metric));
    getFID(metric => this.logMetric('FID', metric));
    getLCP(metric => this.logMetric('LCP', metric));

    // Additional metrics
    getTTFB(metric => this.logMetric('TTFB', metric));
    getFCP(metric => this.logMetric('FCP', metric));

    // Custom metrics
    this.measureCustomMetrics();
  }

  logMetric(name, metric) {
    this.metrics[name] = metric.value;

    // Send to analytics
    if ('sendBeacon' in navigator) {
      navigator.sendBeacon('/analytics', JSON.stringify({
        metric: name,
        value: metric.value,
        rating: metric.rating // 'good', 'needs-improvement', 'poor'
      }));
    }

    // Adaptive optimization based on metrics
    this.optimizeBasedOnMetrics();
  }

  optimizeBasedOnMetrics() {
    if (this.metrics.LCP > 2500) {
      // Poor LCP - reduce image quality
      this.reduceImageQuality();
    }

    if (this.metrics.FID > 100) {
      // Poor interactivity - defer non-critical JS
      this.deferNonCriticalScripts();
    }

    if (this.metrics.CLS > 0.1) {
      // Layout shifts - add dimensions to images
      this.stabilizeLayout();
    }
  }

  measureCustomMetrics() {
    // Time to Interactive
    const observer = new PerformanceObserver(list => {
      for (const entry of list.getEntries()) {
        if (entry.name === 'first-contentful-paint') {
          this.metrics.TTI = entry.startTime;
        }
      }
    });
    observer.observe({entryTypes: ['paint']});
  }

  /**
   * Reduce image quality для улучшения LCP
   */
  reduceImageQuality() {
    const images = document.querySelectorAll('img[data-src]');
    images.forEach(img => {
      const src = img.dataset.src;
      img.src = src.replace(/quality=\d+/, 'quality=70');
    });
  }

  /**
   * Defer non-critical scripts для улучшения FID
   */
  deferNonCriticalScripts() {
    const scripts = document.querySelectorAll('script[data-defer]');
    scripts.forEach(script => {
      if (!script.hasAttribute('defer')) {
        script.setAttribute('defer', '');
      }
    });
  }

  /**
   * Stabilize layout для улучшения CLS
   */
  stabilizeLayout() {
    const images = document.querySelectorAll('img:not([width]):not([height])');
    images.forEach(img => {
      // Add explicit dimensions based on aspect ratio
      const aspectRatio = img.naturalWidth / img.naturalHeight;
      img.style.aspectRatio = aspectRatio;
    });
  }
}
```

### Интеграция в E-commerce PWA

```javascript
class EcommercePerformanceMonitor extends PerformanceMonitor {
  constructor() {
    super();
    this.businessMetrics = {};
  }

  measureCustomMetrics() {
    super.measureCustomMetrics();

    // E-commerce specific metrics
    this.measureTimeToProductCard();
    this.measureTimeToCheckout();
    this.measureImageLoadTime();
  }

  measureTimeToProductCard() {
    const observer = new PerformanceObserver(list => {
      for (const entry of list.getEntries()) {
        if (entry.name.includes('product-card')) {
          this.businessMetrics.productCardLoad = entry.duration;
          console.log(`Product card loaded in ${entry.duration}ms`);
        }
      }
    });
    observer.observe({entryTypes: ['measure']});
  }

  measureTimeToCheckout() {
    // Measure time from "Add to Cart" to Checkout page
    performance.mark('checkout-start');

    document.querySelector('.checkout-btn')?.addEventListener('click', () => {
      performance.mark('checkout-complete');
      performance.measure('checkout-flow', 'checkout-start', 'checkout-complete');

      const measure = performance.getEntriesByName('checkout-flow')[0];
      this.businessMetrics.checkoutTime = measure.duration;
      console.log(`Checkout flow: ${measure.duration}ms`);
    });
  }

  measureImageLoadTime() {
    const productImages = document.querySelectorAll('.product-image');

    productImages.forEach((img, index) => {
      img.addEventListener('load', () => {
        performance.mark(`image-${index}-loaded`);
      });
    });
  }

  optimizeBasedOnMetrics() {
    super.optimizeBasedOnMetrics();

    // E-commerce specific optimizations
    if (this.businessMetrics.productCardLoad > 1000) {
      this.enableLazyLoadingForProducts();
    }

    if (this.metrics.LCP > 3000) {
      this.prioritizeHeroImageLoading();
    }
  }

  enableLazyLoadingForProducts() {
    const productCards = document.querySelectorAll('.product-card');

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('loaded');
          observer.unobserve(entry.target);
        }
      });
    });

    productCards.forEach(card => observer.observe(card));
  }

  prioritizeHeroImageLoading() {
    const heroImage = document.querySelector('.hero-image');
    if (heroImage) {
      heroImage.loading = 'eager';
      heroImage.fetchPriority = 'high';
    }
  }
}
```

---

## 🔒 Privacy-Preserving Analytics

**Описание:** Сбор аналитических данных с соблюдением приватности пользователей - без cookies, IP-адресов и device fingerprinting.

**Принципы:**
- Анонимизация данных на клиенте
- Batch отправка для минимизации запросов
- Session-based IDs вместо постоянных
- Удаление PII (Personally Identifiable Information)

**Compliance:**
- ✅ GDPR compatible
- ✅ CCPA compatible
- ✅ Не требует cookie consent banner
- ✅ Respects "Do Not Track"

### Базовая реализация

```javascript
class PrivacyAnalytics {
  constructor() {
    this.queue = [];
    this.batchSize = 10;
    this.batchTimeout = 5000;
  }

  track(event, properties = {}) {
    // Anonymize data
    const anonymized = {
      event,
      properties: this.anonymizeProperties(properties),
      timestamp: Date.now(),
      session: this.getAnonymousSession(),
      // No user ID, IP, or device fingerprinting
    };

    this.queue.push(anonymized);

    if (this.queue.length >= this.batchSize) {
      this.flush();
    } else {
      this.scheduleFlush();
    }
  }

  anonymizeProperties(properties) {
    const anonymized = {...properties};

    // Remove sensitive fields
    delete anonymized.email;
    delete anonymized.name;
    delete anonymized.phone;
    delete anonymized.address;

    // Hash any IDs
    if (anonymized.userId) {
      anonymized.userId = this.hash(anonymized.userId);
    }

    return anonymized;
  }

  hash(str) {
    // Simple hash for demo - use proper hashing in production
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString(36);
  }

  getAnonymousSession() {
    // Session ID that resets on browser close
    if (!sessionStorage.getItem('anonSession')) {
      sessionStorage.setItem('anonSession', Math.random().toString(36).substr(2, 9));
    }
    return sessionStorage.getItem('anonSession');
  }

  scheduleFlush() {
    if (this.flushTimeout) return;

    this.flushTimeout = setTimeout(() => {
      this.flush();
      this.flushTimeout = null;
    }, this.batchTimeout);
  }

  async flush() {
    if (this.queue.length === 0) return;

    const events = [...this.queue];
    this.queue = [];

    try {
      if ('sendBeacon' in navigator) {
        navigator.sendBeacon('/analytics', JSON.stringify(events));
      } else {
        await fetch('/analytics', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(events)
        });
      }
    } catch (err) {
      // Re-queue events on failure
      this.queue.unshift(...events);
    }
  }
}
```

### Интеграция с Performance Monitoring

```javascript
class PrivacyAwarePerformanceMonitor extends PerformanceMonitor {
  constructor() {
    super();
    this.analytics = new PrivacyAnalytics();
  }

  logMetric(name, metric) {
    super.logMetric(name, metric);

    // Track to privacy-first analytics
    this.analytics.track('performance_metric', {
      metric_name: name,
      value: Math.round(metric.value),
      rating: metric.rating,
      page: this.getAnonymousPageIdentifier()
    });
  }

  getAnonymousPageIdentifier() {
    // Anonymize URL - remove query params and hash
    const url = new URL(window.location.href);
    return url.pathname;
  }

  trackUserJourney() {
    // Track navigation without storing personal data
    window.addEventListener('popstate', () => {
      this.analytics.track('page_view', {
        page: this.getAnonymousPageIdentifier(),
        referrer: document.referrer ? 'external' : 'internal'
      });
    });
  }

  trackConversion(event) {
    // Track business events anonymously
    this.analytics.track('conversion', {
      event_type: event.type,
      value: event.value,
      // No user identification
    });
  }
}
```

### Real-World Usage Example

```javascript
// Initialize monitoring
const monitor = new PrivacyAwarePerformanceMonitor();

// Track e-commerce events without PII
document.querySelector('.add-to-cart-btn').addEventListener('click', event => {
  monitor.trackConversion({
    type: 'add_to_cart',
    value: event.target.dataset.price
  });
});

document.querySelector('.checkout-btn').addEventListener('click', () => {
  monitor.trackConversion({
    type: 'checkout_start',
    value: cart.total
  });
});

// Track custom performance marks
performance.mark('product-gallery-loaded');
monitor.analytics.track('custom_metric', {
  metric: 'product_gallery',
  load_time: performance.getEntriesByName('product-gallery-loaded')[0].startTime
});
```

---

## 📈 Real User Monitoring (RUM)

**Описание:** Сбор метрик от реальных пользователей в production для понимания actual performance.

```javascript
class RealUserMonitoring {
  constructor() {
    this.performanceMonitor = new PrivacyAwarePerformanceMonitor();
    this.setupMonitoring();
  }

  setupMonitoring() {
    // Monitor Long Tasks (>50ms)
    this.monitorLongTasks();

    // Monitor Resource Loading
    this.monitorResources();

    // Monitor User Interactions
    this.monitorInteractions();

    // Monitor Errors
    this.monitorErrors();
  }

  monitorLongTasks() {
    const observer = new PerformanceObserver(list => {
      for (const entry of list.getEntries()) {
        this.performanceMonitor.analytics.track('long_task', {
          duration: Math.round(entry.duration),
          start_time: Math.round(entry.startTime)
        });
      }
    });
    observer.observe({entryTypes: ['longtask']});
  }

  monitorResources() {
    const observer = new PerformanceObserver(list => {
      for (const entry of list.getEntries()) {
        if (entry.duration > 1000) { // Slow resources > 1s
          this.performanceMonitor.analytics.track('slow_resource', {
            type: entry.initiatorType,
            duration: Math.round(entry.duration),
            size: Math.round(entry.transferSize / 1024) // KB
          });
        }
      }
    });
    observer.observe({entryTypes: ['resource']});
  }

  monitorInteractions() {
    const interactionObserver = new PerformanceObserver(list => {
      for (const entry of list.getEntries()) {
        this.performanceMonitor.analytics.track('user_interaction', {
          type: entry.name,
          duration: Math.round(entry.duration)
        });
      }
    });
    interactionObserver.observe({entryTypes: ['event']});
  }

  monitorErrors() {
    window.addEventListener('error', event => {
      this.performanceMonitor.analytics.track('error', {
        message: event.message,
        file: this.anonymizeUrl(event.filename),
        line: event.lineno
      });
    });
  }

  anonymizeUrl(url) {
    return url.replace(/https?:\/\/[^\/]+/, '');
  }
}
```

---

## 🎯 Best Practices: Performance Monitoring

### 1. Synthetic vs Real User Monitoring

**Synthetic Monitoring:**
- Lighthouse CI
- WebPageTest
- Chrome DevTools Performance
- Predictable, reproducible results

**Real User Monitoring:**
- web-vitals library
- PerformanceObserver API
- Real-world data
- Captures edge cases

**Recommended:** Используйте оба подхода

### 2. Performance Budgets

```javascript
const PERFORMANCE_BUDGETS = {
  LCP: 2500,  // ms
  FID: 100,   // ms
  CLS: 0.1,   // score
  TTFB: 800,  // ms
  FCP: 1800,  // ms
  bundle_size: 200 * 1024, // 200KB
  image_size: 100 * 1024   // 100KB
};

function checkBudgets(metrics) {
  const violations = [];

  Object.entries(PERFORMANCE_BUDGETS).forEach(([key, budget]) => {
    if (metrics[key] > budget) {
      violations.push({
        metric: key,
        actual: metrics[key],
        budget: budget,
        overage: ((metrics[key] - budget) / budget * 100).toFixed(2) + '%'
      });
    }
  });

  return violations;
}
```

### 3. Sampling для снижения нагрузки

```javascript
class SampledPerformanceMonitor extends PerformanceMonitor {
  constructor(samplingRate = 0.1) { // 10% by default
    super();
    this.samplingRate = samplingRate;
  }

  logMetric(name, metric) {
    // Only log for sampled users
    if (Math.random() < this.samplingRate) {
      super.logMetric(name, metric);
    }
  }
}
```

---

**Версия модуля:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
**Проект:** AI Agent Factory - PWA Mobile Agent Modularization (5/7)

**Навигация:**
- [← Module 02: Modern Web APIs Integration](02_modern_web_apis_integration.md)
- [→ Module 04: Security & Platform Optimization](04_security_platform_optimization.md)
- [↑ Назад к главной](../pwa_mobile_agent_knowledge.md)

**Tags:** core-web-vitals, performance-monitoring, privacy-analytics, rum, performance-budgets, web-vitals
