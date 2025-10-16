# Module 05: Testing & Best Practices

## 🧪 Overview: Testing в PWA

Тестирование PWA - критически важный процесс для обеспечения качества и надежности приложения. PWA требуют специфического подхода к тестированию из-за offline capabilities, Service Workers и platform-specific features.

**Типы тестирования PWA:**
- **Manifest Validation** - проверка корректности manifest.json
- **Service Worker Testing** - тестирование offline scenarios
- **Performance Testing** - Core Web Vitals и load times
- **Cross-Platform Testing** - iOS, Android, Desktop
- **Accessibility Testing** - WCAG compliance

**Инструменты:**
- Lighthouse CI для automated audits
- Workbox для Service Worker testing
- Puppeteer/Playwright для E2E testing
- WebPageTest для performance analysis

---

## ✅ PWA Compliance Checker

**Описание:** Автоматический валидатор для проверки соответствия PWA стандартам и best practices.

**Что проверяется:**
- Наличие и корректность manifest.json
- Service Worker registration и статус
- HTTPS enforcement
- Icon sizes и форматы
- Display mode configuration

**Интеграция в CI/CD:**
Запускать валидатор в pre-deploy hooks для предотвращения deployment некорректных PWA.

### Базовая реализация

```javascript
class PWAValidator {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.passes = [];
  }

  /**
   * Валидировать manifest.json
   * @returns {Promise<boolean>} True если manifest корректен
   */
  async validateManifest() {
    const manifestLink = document.querySelector('link[rel="manifest"]');
    if (!manifestLink) {
      this.errors.push('No manifest link found');
      return false;
    }

    try {
      const response = await fetch(manifestLink.href);
      const manifest = await response.json();

      // Required fields
      const required = ['name', 'short_name', 'start_url', 'display', 'icons'];
      required.forEach(field => {
        if (!manifest[field]) {
          this.errors.push(`Missing required field: ${field}`);
        } else {
          this.passes.push(`✓ Has ${field}`);
        }
      });

      // Icon validation
      if (manifest.icons) {
        const sizes = manifest.icons.map(i => i.sizes);
        if (!sizes.includes('192x192')) {
          this.warnings.push('Missing 192x192 icon');
        }
        if (!sizes.includes('512x512')) {
          this.warnings.push('Missing 512x512 icon');
        }
      }

      // Display mode
      if (!['fullscreen', 'standalone', 'minimal-ui'].includes(manifest.display)) {
        this.warnings.push('Display mode not optimal for PWA');
      }

    } catch (err) {
      this.errors.push(`Failed to load manifest: ${err.message}`);
    }
  }

  /**
   * Валидировать Service Worker
   * @returns {Promise<boolean>} True если SW корректен
   */
  validateServiceWorker() {
    if (!('serviceWorker' in navigator)) {
      this.errors.push('Service Worker not supported');
      return false;
    }

    navigator.serviceWorker.getRegistration().then(registration => {
      if (registration) {
        this.passes.push('✓ Service Worker registered');

        if (registration.active) {
          this.passes.push('✓ Service Worker active');
        } else if (registration.installing) {
          this.warnings.push('Service Worker installing');
        } else if (registration.waiting) {
          this.warnings.push('Service Worker waiting');
        }
      } else {
        this.errors.push('No Service Worker registration found');
      }
    });
  }

  /**
   * Валидировать HTTPS
   * @returns {boolean} True если HTTPS
   */
  validateHTTPS() {
    if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
      this.errors.push('Not served over HTTPS');
    } else {
      this.passes.push('✓ Served over HTTPS');
    }
  }

  /**
   * Запустить полную валидацию PWA
   * @returns {Promise<Object>} Результаты валидации
   */
  async runFullValidation() {
    this.validateHTTPS();
    await this.validateManifest();
    this.validateServiceWorker();

    return {
      valid: this.errors.length === 0,
      errors: this.errors,
      warnings: this.warnings,
      passes: this.passes,
      score: (this.passes.length / (this.passes.length + this.errors.length)) * 100
    };
  }
}
```

### Интеграция в CI/CD Pipeline

```javascript
// Node.js test script для CI/CD
const puppeteer = require('puppeteer');

async function runPWAValidation(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto(url);

  // Inject PWAValidator
  await page.addScriptTag({path: './pwa-validator.js'});

  // Run validation
  const results = await page.evaluate(async () => {
    const validator = new PWAValidator();
    return await validator.runFullValidation();
  });

  await browser.close();

  // Exit with error if validation failed
  if (!results.valid) {
    console.error('PWA Validation Failed:');
    results.errors.forEach(err => console.error(`  ❌ ${err}`));
    process.exit(1);
  }

  console.log(`✅ PWA Validation Passed (Score: ${results.score.toFixed(0)}%)`);
  results.passes.forEach(pass => console.log(`  ${pass}`));

  if (results.warnings.length > 0) {
    console.log('⚠️ Warnings:');
    results.warnings.forEach(warn => console.log(`  ${warn}`));
  }
}

// Usage
runPWAValidation('https://your-pwa.com');
```

---

## 🚀 Progressive Enhancement Strategy

**Описание:** Прогрессивное улучшение - это стратегия разработки, при которой базовая функциональность работает без JavaScript, а PWA фичи добавляются постепенно при их поддержке.

**Принципы Progressive Enhancement:**
1. Базовый функционал работает без JS (HTML + CSS)
2. JavaScript добавляет интерактивность
3. Service Worker добавляет offline capability
4. Modern APIs добавляют native-like features

**Feature Detection:**
Всегда использовать feature detection вместо browser detection.

### Базовая реализация

```javascript
class ProgressiveEnhancement {
  /**
   * Применить прогрессивное улучшение для PWA
   */
  static async enhance() {
    // Basic functionality works without JS
    this.ensureBasicFunctionality();

    // Enhance with PWA features if supported
    if ('serviceWorker' in navigator) {
      await this.registerServiceWorker();
    }

    if ('Notification' in window) {
      await this.setupNotifications();
    }

    if ('share' in navigator) {
      this.enhanceSharing();
    }

    if ('getBattery' in navigator) {
      await this.optimizeForBattery();
    }

    // Platform-specific enhancements
    if (iOSOptimizer.detectiOS()) {
      iOSOptimizer.applyOptimizations();
    } else if (AndroidOptimizer.detectAndroid()) {
      AndroidOptimizer.applyOptimizations();
    }
  }

  /**
   * Обеспечить базовую функциональность без JS
   */
  static ensureBasicFunctionality() {
    // Ensure forms work without JS
    document.querySelectorAll('form').forEach(form => {
      if (!form.action) {
        form.action = form.dataset.action || '/submit';
      }
    });

    // Ensure links work
    document.querySelectorAll('a[data-spa]').forEach(link => {
      link.href = link.dataset.href || '#';
    });
  }

  /**
   * Зарегистрировать Service Worker с обработкой обновлений
   */
  static async registerServiceWorker() {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/',
        updateViaCache: 'none'
      });

      // Check for updates
      setInterval(() => {
        registration.update();
      }, 60000); // Every minute

      // Handle updates
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'activated') {
            // New service worker activated
            if (confirm('New version available! Reload?')) {
              location.reload();
            }
          }
        });
      });
    } catch (err) {
      console.error('SW registration failed:', err);
    }
  }

  /**
   * Настроить push notifications если поддерживается
   */
  static async setupNotifications() {
    if (Notification.permission === 'default') {
      // Request permission on user action, not immediately
      document.querySelector('.enable-notifications-btn')?.addEventListener('click', async () => {
        const permission = await Notification.requestPermission();
        if (permission === 'granted') {
          new Notification('Notifications enabled!', {
            body: 'You will now receive updates',
            icon: '/icons/icon-192x192.png'
          });
        }
      });
    }
  }

  /**
   * Улучшить sharing capabilities если поддерживается
   */
  static enhanceSharing() {
    const shareButtons = document.querySelectorAll('[data-share]');
    shareButtons.forEach(button => {
      button.addEventListener('click', async () => {
        try {
          await navigator.share({
            title: document.title,
            text: button.dataset.shareText,
            url: button.dataset.shareUrl || window.location.href
          });
        } catch (err) {
          // Fallback to copy to clipboard
          navigator.clipboard.writeText(window.location.href);
        }
      });
    });
  }

  /**
   * Оптимизировать для battery level
   */
  static async optimizeForBattery() {
    try {
      const battery = await navigator.getBattery();

      const updateBatteryOptimization = () => {
        if (battery.level < 0.2 && !battery.charging) {
          // Low battery - reduce features
          document.body.classList.add('battery-saver');
          // Pause animations, reduce polling, etc.
        } else {
          document.body.classList.remove('battery-saver');
        }
      };

      battery.addEventListener('levelchange', updateBatteryOptimization);
      battery.addEventListener('chargingchange', updateBatteryOptimization);
      updateBatteryOptimization();

    } catch (err) {
      console.log('Battery API not supported');
    }
  }
}
```

### Применение в Production

```javascript
// app.js - Entry point
document.addEventListener('DOMContentLoaded', async () => {
  // Apply progressive enhancement
  await ProgressiveEnhancement.enhance();

  // Feature flags based on support
  const features = {
    serviceWorker: 'serviceWorker' in navigator,
    pushNotifications: 'Notification' in window,
    webShare: 'share' in navigator,
    fileSystem: 'showOpenFilePicker' in window,
    badging: 'setAppBadge' in navigator,
    wakeLock: 'wakeLock' in navigator
  };

  // Log supported features
  console.log('Supported PWA features:', features);

  // Initialize only supported features
  if (features.serviceWorker) {
    // Service Worker is available
  }

  if (features.pushNotifications) {
    // Push notifications available
  }

  // Add feature detection classes to body
  Object.entries(features).forEach(([feature, supported]) => {
    document.body.classList.toggle(`supports-${feature}`, supported);
  });
});

// CSS - Progressive enhancement styles
/*
/* Base styles work everywhere */
.notification-btn {
  display: inline-block;
  padding: 10px 20px;
}

/* Enhanced styles for supported browsers */
.supports-pushNotifications .notification-btn {
  /* Add icon, animations */
}

/* Battery saver mode */
.battery-saver * {
  animation: none !important;
  transition: none !important;
}

.battery-saver img {
  /* Reduce image quality */
  filter: grayscale(50%);
}
*/
```

---

## 📊 Best Practices Summary

### Performance Checklist

**Обязательные метрики:**
- ✅ LCP (Largest Contentful Paint) < 2.5s
- ✅ FID (First Input Delay) < 100ms
- ✅ CLS (Cumulative Layout Shift) < 0.1
- ✅ TTFB (Time to First Byte) < 800ms
- ✅ FCP (First Contentful Paint) < 1.8s

**Оптимизации:**
- ✅ Implement adaptive loading based on network conditions
- ✅ Use intelligent cache management with automatic cleanup
- ✅ Monitor Core Web Vitals in production
- ✅ Implement progressive enhancement
- ✅ Optimize for battery usage
- ✅ Lazy load images and components
- ✅ Code splitting for large bundles
- ✅ Compress assets (gzip/brotli)

---

### Security Checklist

**Обязательные требования:**
- ✅ Serve over HTTPS everywhere
- ✅ Generate and apply strict CSP headers
- ✅ Use Web Crypto API for sensitive data
- ✅ Implement secure Service Worker communication
- ✅ Enable HSTS (HTTP Strict Transport Security)
- ✅ Regular security audits with automated tools

**Дополнительные меры:**
- ✅ Sanitize user inputs
- ✅ Implement rate limiting
- ✅ Use secure cookies (HttpOnly, Secure, SameSite)
- ✅ Regular dependency updates
- ✅ Implement proper CORS policies

---

### UX Checklist

**Обязательные требования:**
- ✅ Platform-specific optimizations (iOS/Android)
- ✅ Offline-first approach with graceful degradation
- ✅ Touch-optimized interfaces (44px minimum tap target)
- ✅ Responsive design with mobile-first approach
- ✅ Fast initial load (< 3s on 3G)
- ✅ Skeleton screens for loading states

**Дополнительные улучшения:**
- ✅ Haptic feedback для touch interactions
- ✅ Dark mode support
- ✅ Accessibility (WCAG 2.1 AA compliance)
- ✅ Pull-to-refresh pattern
- ✅ App-like navigation (bottom nav bar)
- ✅ Swipe gestures where appropriate

---

### Developer Experience Checklist

**Обязательные инструменты:**
- ✅ Automated testing with PWA validator
- ✅ Performance monitoring dashboard
- ✅ Build-time optimizations (webpack/vite)
- ✅ Hot reload for development
- ✅ Comprehensive documentation

**CI/CD Pipeline:**
- ✅ Lighthouse CI for automated audits
- ✅ Visual regression testing
- ✅ E2E testing (Playwright/Puppeteer)
- ✅ Automated manifest validation
- ✅ Service Worker testing

**Development Workflow:**
- ✅ Local HTTPS development server
- ✅ Service Worker debugging tools
- ✅ Network throttling for testing
- ✅ Device emulation for cross-platform testing

---

## 🔧 Testing Tools & Frameworks

### Lighthouse CI Integration

```yaml
# .github/workflows/lighthouse-ci.yml
name: Lighthouse CI
on: [push]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun
```

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000'],
      numberOfRuns: 3
    },
    assert: {
      assertions: {
        'categories:performance': ['error', {minScore: 0.9}],
        'categories:accessibility': ['error', {minScore: 0.9}],
        'categories:best-practices': ['error', {minScore: 0.9}],
        'categories:seo': ['error', {minScore: 0.9}],
        'categories:pwa': ['error', {minScore: 0.9}]
      }
    },
    upload: {
      target: 'temporary-public-storage'
    }
  }
};
```

### Playwright E2E Testing

```javascript
// tests/pwa.spec.js
const { test, expect } = require('@playwright/test');

test.describe('PWA Functionality', () => {
  test('should register service worker', async ({ page }) => {
    await page.goto('https://your-pwa.com');

    const swRegistered = await page.evaluate(async () => {
      const registration = await navigator.serviceWorker.getRegistration();
      return registration !== undefined;
    });

    expect(swRegistered).toBe(true);
  });

  test('should work offline', async ({ page, context }) => {
    await page.goto('https://your-pwa.com');

    // Wait for service worker activation
    await page.waitForTimeout(2000);

    // Go offline
    await context.setOffline(true);

    // Navigate to cached page
    await page.goto('https://your-pwa.com/products');

    // Should still render
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should have valid manifest', async ({ page }) => {
    await page.goto('https://your-pwa.com');

    const manifestLink = await page.locator('link[rel="manifest"]');
    const manifestHref = await manifestLink.getAttribute('href');

    expect(manifestHref).toBeTruthy();

    // Fetch and validate manifest
    const manifest = await page.evaluate(async (href) => {
      const response = await fetch(href);
      return await response.json();
    }, manifestHref);

    expect(manifest.name).toBeDefined();
    expect(manifest.short_name).toBeDefined();
    expect(manifest.icons).toBeDefined();
    expect(manifest.icons.length).toBeGreaterThan(0);
  });
});
```

---

## 🎯 Performance Budget Configuration

```javascript
// performance-budget.config.js
module.exports = {
  budgets: {
    // Core Web Vitals
    LCP: 2500,  // ms
    FID: 100,   // ms
    CLS: 0.1,   // score

    // Additional metrics
    TTFB: 800,  // ms
    FCP: 1800,  // ms
    TTI: 3800,  // ms

    // Resource budgets
    totalJavaScript: 200 * 1024, // 200KB
    totalCSS: 50 * 1024,         // 50KB
    totalImages: 500 * 1024,     // 500KB
    totalFonts: 100 * 1024,      // 100KB

    // Request budgets
    totalRequests: 50,
    thirdPartyRequests: 10
  },

  checkBudgets(metrics) {
    const violations = [];

    Object.entries(this.budgets).forEach(([key, budget]) => {
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
};
```

---

## 📈 Monitoring & Analytics Strategy

```javascript
// monitoring.js
class PWAMonitoring {
  static setupMonitoring() {
    // Monitor Service Worker lifecycle
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      console.log('New Service Worker activated');
      this.trackEvent('sw_updated');
    });

    // Monitor install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.trackEvent('install_prompt_shown');
    });

    // Monitor app installed
    window.addEventListener('appinstalled', () => {
      this.trackEvent('pwa_installed');
    });

    // Monitor standalone mode
    if (window.matchMedia('(display-mode: standalone)').matches) {
      this.trackEvent('launched_standalone');
    }

    // Monitor errors
    window.addEventListener('error', (e) => {
      this.trackError(e.error);
    });

    // Monitor unhandled promise rejections
    window.addEventListener('unhandledrejection', (e) => {
      this.trackError(e.reason);
    });
  }

  static trackEvent(eventName, properties = {}) {
    // Send to analytics
    if ('sendBeacon' in navigator) {
      navigator.sendBeacon('/analytics/event', JSON.stringify({
        event: eventName,
        properties,
        timestamp: Date.now()
      }));
    }
  }

  static trackError(error) {
    console.error('PWA Error:', error);
    this.trackEvent('pwa_error', {
      message: error.message,
      stack: error.stack
    });
  }
}

// Initialize monitoring
PWAMonitoring.setupMonitoring();
```

---

**Версия модуля:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
**Проект:** AI Agent Factory - PWA Mobile Agent Modularization (5/7)

**Навигация:**
- [← Module 04: Security & Platform Optimization](04_security_platform_optimization.md)
- [↑ Назад к главной](../pwa_mobile_agent_knowledge.md)

**Tags:** testing, validation, progressive-enhancement, best-practices, lighthouse, playwright, monitoring, performance-budgets
