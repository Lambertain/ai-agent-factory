# ⚠️ КРИТИЧЕСКИ ВАЖНО: ОБЯЗАТЕЛЬНОЕ ПЕРЕКЛЮЧЕНИЕ В РОЛЬ

**🚨 ПЕРЕД НАЧАЛОМ ЛЮБОЙ РАБОТЫ ТЫ ДОЛЖЕН:**

## 📢 ШАГ 1: ОБЪЯВИТЬ ПЕРЕКЛЮЧЕНИЕ ПОЛЬЗОВАТЕЛЮ

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎭 ПЕРЕКЛЮЧАЮСЬ В РОЛЬ PWA MOBILE AGENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Моя экспертиза:
• Чтение/запись локальных файлов без ограничений
• Работа с директориями
• Сохранение permissions между сессиями
• Поддержка: Chrome 86+, Safari частично

🎯 Специализация:
• Разработка и реализация решений
• Техническая экспертиза

✅ Готов выполнить задачу в роли эксперта Pwa Mobile Agent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ЭТО СООБЩЕНИЕ ОБЯЗАТЕЛЬНО ДОЛЖНО БЫТЬ ПОКАЗАНО ПОЛЬЗОВАТЕЛЮ!**

## 🚫 ШАГ 2: СОЗДАТЬ МИКРОЗАДАЧИ ЧЕРЕЗ TodoWrite

**СРАЗУ ПОСЛЕ объявления переключения создать 3-7 микрозадач**

## ✅ ШАГ 3: ТОЛЬКО ПОТОМ НАЧИНАТЬ РАБОТУ

---

# 🚨 КРИТИЧЕСКИ ВАЖНО: ЗАПРЕТ ТОКЕН-ЭКОНОМИИ И МАССОВЫХ ОПЕРАЦИЙ

**НИКОГДА НЕ ДЕЛАЙ:**
- ❌ Сокращать файлы "для экономии токенов"
- ❌ Писать "... (остальной код без изменений)"
- ❌ Пропускать комментарии и документацию
- ❌ Обрабатывать файлы "массово" без тщательной проверки
- ❌ Делать задачи "быстро" за счет качества

**ОБЯЗАТЕЛЬНО ДЕЛАЙ:**
- ✅ Пиши ПОЛНЫЙ код с ВСЕМИ комментариями
- ✅ Если файл большой - пиши его ЧАСТЯМИ, но полностью
- ✅ Обрабатывай КАЖДЫЙ файл тщательно и индивидуально
- ✅ Проверяй КАЖДОЕ изменение перед следующим
- ✅ Документируй КАЖДУЮ функцию и класс

**ПРАВИЛО БОЛЬШИХ ФАЙЛОВ:**
Если файл превышает лимит токенов:
1. Разбей на логические секции
2. Пиши каждую секцию полностью
3. Не используй "..." или сокращения
4. Сохраняй ВСЕ комментарии

**КАЧЕСТВО > СКОРОСТЬ**

---

## 📋 ОБОВ'ЯЗКОВІ ФІНАЛЬНІ ПУНКТИ TodoWrite:

**🚨 КОЖНА ЗАДАЧА ПОВИННА ЗАВЕРШУВАТИСЯ ЧОТИРМА ОБОВ'ЯЗКОВИМИ ПУНКТАМИ:**

```
N-3. Застосувати обов'язкові інструменти колективної роботи через декоратори
N-2. Створити Git коміт зі змінами архітектури
N-1. Оновити статус задачі в Archon [TASK_ID: {task_id}]
N.   Виконати Post-Task Checklist (.claude/rules/10_post_task_checklist.md) [TASK_ID: {task_id}]
```

**🆔 ОБОВ'ЯЗКОВО ВКАЗУВАТИ TASK_ID:**

```python
# ПРИКЛАД ПРАВИЛЬНОГО TodoWrite з task_id:
task_id = "3a7f8b9c-1d2e-3f4g-5h6i-7j8k9l0m1n2o"  # Отримали з Archon

TodoWrite([
    {"content": "Проаналізувати вимоги", "status": "pending", "activeForm": "Аналізую вимоги"},
    {"content": "Реалізувати функціонал", "status": "pending", "activeForm": "Реалізую функціонал"},
    {"content": "Написати тести", "status": "pending", "activeForm": "Пишу тести"},
    {"content": "Рефлексія: знайти недоліки та покращити", "status": "pending", "activeForm": "Провожу рефлексію"},
    {"content": f"Оновити статус задачі в Archon [TASK_ID: {task_id}]", "status": "pending", "activeForm": "Оновлюю статус задачі"},
    {"content": f"Виконати Post-Task Checklist (.claude/rules/10_post_task_checklist.md) [TASK_ID: {task_id}]", "status": "pending", "activeForm": "Виконую Post-Task Checklist"}
])
```

**ЧОМУ ЦЕ ВАЖЛИВО:**
- Агент пам'ятає task_id протягом всього виконання
- В кінці легко знайти task_id з останнього пункту TodoWrite
- Уникаємо проблеми "забув task_id, не можу оновити статус"

**Що включає Post-Task Checklist:**
1. Освіження пам'яті (якщо потрібно)
2. Перевірка Git операцій для production проектів
3. **АВТОМАТИЧНЕ ПЕРЕКЛЮЧЕННЯ НА PROJECT MANAGER** (найважливіше!)
4. Збереження контексту проекту
5. Вибір наступної задачі з найвищим пріоритетом серед УСІХ ролей
6. Переключення в роль для нової задачі

**Детальна інструкція:** `.claude/rules/10_post_task_checklist.md`

**НІКОЛИ НЕ ЗАВЕРШУЙТЕ ЗАДАЧУ БЕЗ ЦЬОГО ЦИКЛУ!**

---

## 🎯 ОБОВ'ЯЗКОВЕ ПРАВИЛО: НЕГАЙНЕ СТВОРЕННЯ ЗАДАЧІ В ARCHON

**🚨 КОЛИ КОРИСТУВАЧ ПРОСИТЬ ЩОСЬ ЗРОБИТИ:**

### Крок 1: НЕГАЙНО створити задачу в Archon
```python
# ПРИКЛАД: Користувач написав "додай валідацію email"
await mcp__archon__manage_task(
    action="create",
    project_id=current_project_id,  # Проект над яким працюєш ЗАРАЗ
    title="Додати валідацію email",
    description="Користувач запросив: додай валідацію email\n\nДата створення: 2025-10-10",
    assignee=my_role,  # Твоя поточна роль
    status="todo",
    task_order=50
)
```

### Крок 2: ВИЗНАЧИТИ дію
- ✅ **ЯКЩО вільний** → відразу починай виконувати нову задачу
- ✅ **ЯКЩО зайнятий** → продовж поточну задачу, повідом користувача:
  ```
  "✅ Задачу створено в Archon
  🔄 Зараз завершую: [поточна задача]
  📋 Потім виконаю: [нова задача]"
  ```

### Крок 3: НЕ ЗАБУВАТИ
- Задача збережена в Archon → НЕ загубиться
- Після завершення поточної → автоматично перейти до нової через Post-Task Checklist

**ЧОМУ ЦЕ КРИТИЧНО:**
- Запобігає "забуванню" запитів користувача
- Створює чіткий trace всіх завдань
- Дозволяє продовжувати поточну роботу без страху втратити новий запит
- Project Manager бачить всі задачі і може переприоритизувати

**НІКОЛИ НЕ:**
- ❌ Не говори "виконаю після того як закінчу" без створення задачі
- ❌ Не переключайся на нову задачу кинувши поточну
- ❌ Не створюй задачу в іншому проекті (тільки в поточному)

---

# PWA Mobile Agent Knowledge Base - Enhanced Edition

## 🆕 Modern Web APIs Integration

### 📁 File System Access API
Прямая интеграция с файловой системой для productivity PWA:
- Чтение/запись локальных файлов без ограничений
- Работа с директориями
- Сохранение permissions между сессиями
- Поддержка: Chrome 86+, Safari частично

**Use cases:**
- Text/code editors
- Document processors
- File managers
- Data import/export tools

### 🏷️ Badging API
Отображение badge counts на иконке приложения:
- Numeric badges для счетчиков
- Flag badges для статусов
- Service Worker интеграция
- Поддержка: Chrome 81+, Safari 16.4+

**Use cases:**
- Unread messages count
- Shopping cart items
- Pending notifications
- Task reminders

### 🔒 Wake Lock API
Предотвращение засыпания экрана:
- Screen wake lock для активного контента
- Автоматическое управление
- Интеграция с media events
- Поддержка: Chrome 84+

**Use cases:**
- Video/audio playbook
- Gaming sessions
- Presentation mode
- Reading long content

### 😴 Idle Detection API
Определение неактивности пользователя:
- Настраиваемые пороги timeout
- Battery optimization
- Fallback для несовместимых браузеров
- Поддержка: Chrome 94+ (experimental)

**Use cases:**
- Auto-save state
- Pause background tasks
- Update presence status
- Battery optimization

### 🔐 Web Locks API
Координация между tabs и workers:
- Exclusive/shared locks
- Document editing protection
- Multi-tab synchronization
- Поддержка: Chrome 69+, Safari 15.4+, Firefox 96+

**Use cases:**
- Prevent concurrent editing
- Coordinate data sync
- Ensure atomic operations
- Resource management

## 📱 Системный промпт агента

Я - универсальный PWA Mobile Agent, эксперт по Progressive Web Apps и мобильной веб-разработке. Моя специализация включает создание быстрых, надежных и engaging мобильных веб-приложений с native-like опытом для любых типов проектов.

## 🏗️ Архитектурные паттерны PWA

### Service Worker Strategies

#### Cache-First Strategy
```javascript
// Идеально для статичного контента
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request).then(fetchResponse => {
        return caches.open('v1').then(cache => {
          cache.put(event.request, fetchResponse.clone());
          return fetchResponse;
        });
      });
    })
  );
});
```
**Применение**: E-commerce product images, Gaming assets, Media thumbnails

#### Network-First Strategy
```javascript
// Для динамического контента
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request);
    })
  );
});
```
**Применение**: User data, Real-time updates, API calls

#### Stale-While-Revalidate
```javascript
// Баланс между скоростью и актуальностью
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.open('v1').then(cache => {
      return cache.match(event.request).then(cachedResponse => {
        const fetchPromise = fetch(event.request).then(networkResponse => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
        return cachedResponse || fetchPromise;
      });
    })
  );
});
```
**Применение**: News articles, Social feeds, Product catalogs

### Advanced Caching Patterns

#### Adaptive Loading Based on Network
```javascript
async function getNetworkSpeed() {
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  if (connection) {
    const effectiveType = connection.effectiveType;
    return {
      is2G: effectiveType === '2g',
      is3G: effectiveType === '3g',
      is4G: effectiveType === '4g',
      saveData: connection.saveData
    };
  }
  return { is4G: true }; // Default to best quality
}

// Adaptive image loading
async function loadImage(imagePath) {
  const network = await getNetworkSpeed();
  if (network.is2G || network.saveData) {
    return `${imagePath}?quality=low`;
  } else if (network.is3G) {
    return `${imagePath}?quality=medium`;
  }
  return `${imagePath}?quality=high`;
}
```

#### Intelligent Cache Management
```javascript
class CacheManager {
  constructor(maxSize = 50 * 1024 * 1024) { // 50MB default
    this.maxSize = maxSize;
  }

  async cleanOldCaches() {
    const cacheNames = await caches.keys();
    const currentCaches = ['v1', 'api-cache', 'image-cache'];

    await Promise.all(
      cacheNames.map(cacheName => {
        if (!currentCaches.includes(cacheName)) {
          return caches.delete(cacheName);
        }
      })
    );
  }

  async checkStorageQuota() {
    if ('storage' in navigator && 'estimate' in navigator.storage) {
      const {usage, quota} = await navigator.storage.estimate();
      const percentUsed = (usage / quota) * 100;

      if (percentUsed > 90) {
        await this.performCleanup();
      }

      return {usage, quota, percentUsed};
    }
  }

  async performCleanup() {
    // Remove least recently used items
    const cache = await caches.open('v1');
    const requests = await cache.keys();
    const itemsWithTimestamp = [];

    for (const request of requests) {
      const response = await cache.match(request);
      const timestamp = response.headers.get('sw-cache-timestamp');
      itemsWithTimestamp.push({request, timestamp});
    }

    // Sort by timestamp and remove oldest
    itemsWithTimestamp.sort((a, b) => a.timestamp - b.timestamp);
    const itemsToRemove = itemsWithTimestamp.slice(0, Math.floor(itemsWithTimestamp.length * 0.3));

    for (const item of itemsToRemove) {
      await cache.delete(item.request);
    }
  }
}
```

## 🆕 Modern Web APIs Integration

### File System Access API
```javascript
// For productivity PWAs - local file editing
async function openAndEditFile() {
  try {
    const [fileHandle] = await window.showOpenFilePicker({
      types: [{
        description: 'Text Files',
        accept: { 'text/plain': ['.txt', '.md'] }
      }],
      multiple: false
    });

    const file = await fileHandle.getFile();
    const contents = await file.text();

    // Edit contents...
    const newContents = contents + '\n// Edited by PWA';

    // Write back
    const writable = await fileHandle.createWritable();
    await writable.write(newContents);
    await writable.close();
  } catch (err) {
    console.error('File operation cancelled or failed:', err);
  }
}
```

### Badging API
```javascript
// Show notification badge on app icon
class BadgeManager {
  static async setBadge(count) {
    if ('setAppBadge' in navigator) {
      try {
        await navigator.setAppBadge(count);
      } catch (err) {
        console.error('Badge API not supported:', err);
      }
    }
  }

  static async clearBadge() {
    if ('clearAppBadge' in navigator) {
      await navigator.clearAppBadge();
    }
  }

  // For e-commerce cart count
  static async updateCartBadge(cartItems) {
    await this.setBadge(cartItems.length);
  }

  // For social notifications
  static async updateNotificationBadge(unreadCount) {
    await this.setBadge(unreadCount);
  }
}
```

### Wake Lock API
```javascript
// Prevent screen from sleeping during important operations
class WakeLockManager {
  constructor() {
    this.wakeLock = null;
  }

  async requestWakeLock() {
    try {
      this.wakeLock = await navigator.wakeLock.request('screen');

      this.wakeLock.addEventListener('release', () => {
        console.log('Wake Lock released');
      });

      // Re-acquire on visibility change
      document.addEventListener('visibilitychange', async () => {
        if (this.wakeLock !== null && document.visibilityState === 'visible') {
          await this.requestWakeLock();
        }
      });
    } catch (err) {
      console.error('Wake Lock failed:', err);
    }
  }

  async releaseWakeLock() {
    if (this.wakeLock) {
      await this.wakeLock.release();
      this.wakeLock = null;
    }
  }
}

// Usage for video/gaming PWAs
const wakeLockManager = new WakeLockManager();
// During video playback or gaming session
await wakeLockManager.requestWakeLock();
// When done
await wakeLockManager.releaseWakeLock();
```

### Idle Detection API
```javascript
// Optimize resources when user is idle
class IdleManager {
  constructor(threshold = 60000) { // 1 minute default
    this.threshold = threshold;
    this.detector = null;
  }

  async startMonitoring() {
    if ('IdleDetector' in window) {
      try {
        await IdleDetector.requestPermission();

        this.detector = new IdleDetector();
        this.detector.addEventListener('change', () => {
          const {userState, screenState} = this.detector;

          if (userState === 'idle' && screenState === 'locked') {
            this.onUserIdle();
          } else if (userState === 'active') {
            this.onUserActive();
          }
        });

        await this.detector.start({
          threshold: this.threshold,
          signal: new AbortController().signal
        });
      } catch (err) {
        console.error('Idle detection failed:', err);
      }
    }
  }

  onUserIdle() {
    // Pause background operations
    // Stop real-time updates
    // Reduce resource usage
    console.log('User is idle - optimizing resources');
  }

  onUserActive() {
    // Resume operations
    // Sync pending data
    // Refresh content
    console.log('User is active - resuming operations');
  }
}
```

## 📊 Performance Monitoring & Web Vitals

### Core Web Vitals Integration
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
      this.reducImageQuality();
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
}
```

## 🔒 Security & Privacy Enhancements

### Content Security Policy Generation
```javascript
class CSPGenerator {
  constructor(pwaType) {
    this.pwaType = pwaType;
    this.policies = this.getBasePolicy();
  }

  getBasePolicy() {
    return {
      'default-src': ["'self'"],
      'script-src': ["'self'", "'strict-dynamic'"],
      'style-src': ["'self'", "'unsafe-inline'"], // For dynamic styles
      'img-src': ["'self'", 'data:', 'https:'],
      'font-src': ["'self'", 'data:'],
      'connect-src': ["'self'"],
      'media-src': ["'self'"],
      'object-src': ["'none'"],
      'frame-ancestors': ["'none'"],
      'base-uri': ["'self'"],
      'form-action': ["'self'"],
      'upgrade-insecure-requests': []
    };
  }

  addTrustedDomain(domain, directive = 'connect-src') {
    if (!this.policies[directive].includes(domain)) {
      this.policies[directive].push(domain);
    }
  }

  generateNonce() {
    const array = new Uint8Array(16);
    crypto.getRandomValues(array);
    return btoa(String.fromCharCode.apply(null, array));
  }

  toHeaderString() {
    return Object.entries(this.policies)
      .map(([key, values]) => {
        if (values.length === 0) return key;
        return `${key} ${values.join(' ')}`;
      })
      .join('; ');
  }

  applyToResponse(response) {
    const nonce = this.generateNonce();
    let cspHeader = this.toHeaderString();
    cspHeader = cspHeader.replace("'strict-dynamic'", `'nonce-${nonce}' 'strict-dynamic'`);

    response.headers.set('Content-Security-Policy', cspHeader);
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('X-Frame-Options', 'DENY');
    response.headers.set('X-XSS-Protection', '1; mode=block');

    return {response, nonce};
  }
}
```

### Secure Storage with Web Crypto API
```javascript
class SecureStorage {
  constructor() {
    this.dbName = 'secureStore';
    this.storeName = 'encrypted';
  }

  async generateKey() {
    return await crypto.subtle.generateKey(
      {name: 'AES-GCM', length: 256},
      true,
      ['encrypt', 'decrypt']
    );
  }

  async encrypt(data, key) {
    const encoder = new TextEncoder();
    const encodedData = encoder.encode(JSON.stringify(data));

    const iv = crypto.getRandomValues(new Uint8Array(12));
    const encryptedData = await crypto.subtle.encrypt(
      {name: 'AES-GCM', iv},
      key,
      encodedData
    );

    return {
      iv: Array.from(iv),
      data: Array.from(new Uint8Array(encryptedData))
    };
  }

  async decrypt(encryptedData, key) {
    const decryptedData = await crypto.subtle.decrypt(
      {name: 'AES-GCM', iv: new Uint8Array(encryptedData.iv)},
      key,
      new Uint8Array(encryptedData.data)
    );

    const decoder = new TextDecoder();
    return JSON.parse(decoder.decode(decryptedData));
  }

  async store(key, value, encryptionKey) {
    const encrypted = await this.encrypt(value, encryptionKey);

    // Store in IndexedDB
    const db = await this.openDB();
    const tx = db.transaction([this.storeName], 'readwrite');
    await tx.objectStore(this.storeName).put({key, value: encrypted});
  }

  async retrieve(key, encryptionKey) {
    const db = await this.openDB();
    const tx = db.transaction([this.storeName], 'readonly');
    const result = await tx.objectStore(this.storeName).get(key);

    if (result) {
      return await this.decrypt(result.value, encryptionKey);
    }
    return null;
  }

  async openDB() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);

      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, {keyPath: 'key'});
        }
      };
    });
  }
}
```

## 📱 Platform-Specific Optimizations

### iOS Safari PWA Optimizations
```javascript
class iOSOptimizer {
  static detectiOS() {
    return /iPad|iPhone|iPod/.test(navigator.userAgent) ||
           (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  }

  static applyOptimizations() {
    if (!this.detectiOS()) return;

    // iOS status bar styling
    const meta = document.createElement('meta');
    meta.name = 'apple-mobile-web-app-status-bar-style';
    meta.content = 'black-translucent';
    document.head.appendChild(meta);

    // iOS splash screens
    this.addSplashScreens();

    // iOS specific viewport
    const viewport = document.querySelector('meta[name="viewport"]');
    if (viewport) {
      viewport.content = 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover';
    }

    // Disable bounce scroll
    document.body.style.overscrollBehavior = 'none';

    // Handle safe area insets
    document.documentElement.style.setProperty('--sat', 'env(safe-area-inset-top)');
    document.documentElement.style.setProperty('--sar', 'env(safe-area-inset-right)');
    document.documentElement.style.setProperty('--sab', 'env(safe-area-inset-bottom)');
    document.documentElement.style.setProperty('--sal', 'env(safe-area-inset-left)');
  }

  static addSplashScreens() {
    const splashScreens = [
      {sizes: '640x1136', href: '/splash/splash-640x1136.png', media: '(device-width: 320px) and (device-height: 568px)'},
      {sizes: '750x1334', href: '/splash/splash-750x1334.png', media: '(device-width: 375px) and (device-height: 667px)'},
      {sizes: '1242x2208', href: '/splash/splash-1242x2208.png', media: '(device-width: 414px) and (device-height: 736px)'},
      {sizes: '1125x2436', href: '/splash/splash-1125x2436.png', media: '(device-width: 375px) and (device-height: 812px)'},
      {sizes: '1284x2778', href: '/splash/splash-1284x2778.png', media: '(device-width: 428px) and (device-height: 926px)'}
    ];

    splashScreens.forEach(screen => {
      const link = document.createElement('link');
      link.rel = 'apple-touch-startup-image';
      link.href = screen.href;
      link.media = screen.media;
      document.head.appendChild(link);
    });
  }
}
```

### Android TWA Configuration
```javascript
class AndroidOptimizer {
  static detectAndroid() {
    return /Android/.test(navigator.userAgent);
  }

  static generateAssetLinks() {
    return [{
      "relation": ["delegate_permission/common.handle_all_urls"],
      "target": {
        "namespace": "android_app",
        "package_name": "com.example.pwa",
        "sha256_cert_fingerprints": [
          "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00"
        ]
      }
    }];
  }

  static applyOptimizations() {
    if (!this.detectAndroid()) return;

    // Android theme color for browser UI
    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) {
      // Dynamic theme color based on scroll
      window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
          themeColor.content = '#000000';
        } else {
          themeColor.content = '#ffffff';
        }
      });
    }

    // Android specific manifest additions
    this.enhanceManifest();
  }

  static enhanceManifest() {
    // Add Android-specific features to manifest
    const manifestLink = document.querySelector('link[rel="manifest"]');
    if (manifestLink) {
      fetch(manifestLink.href)
        .then(r => r.json())
        .then(manifest => {
          manifest.shortcuts = manifest.shortcuts || [];
          manifest.share_target = {
            action: "/share",
            method: "POST",
            enctype: "multipart/form-data",
            params: {
              title: "title",
              text: "text",
              url: "url",
              files: [{
                name: "media",
                accept: ["image/*", "video/*"]
              }]
            }
          };

          // Create new manifest blob
          const blob = new Blob([JSON.stringify(manifest)], {type: 'application/manifest+json'});
          const url = URL.createObjectURL(blob);
          manifestLink.href = url;
        });
    }
  }
}
```

## 🧪 Testing & Validation Patterns

### PWA Compliance Checker
```javascript
class PWAValidator {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.passes = [];
  }

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

  validateHTTPS() {
    if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
      this.errors.push('Not served over HTTPS');
    } else {
      this.passes.push('✓ Served over HTTPS');
    }
  }

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

## 🚀 Deployment & Production Patterns

### Progressive Enhancement Strategy
```javascript
class ProgressiveEnhancement {
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
}
```

## 📊 Analytics & Monitoring

### Privacy-Preserving Analytics
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

## 🎯 Best Practices Summary

### Performance Checklist
- [ ] Implement adaptive loading based on network conditions
- [ ] Use intelligent cache management with automatic cleanup
- [ ] Monitor Core Web Vitals in production
- [ ] Implement progressive enhancement
- [ ] Optimize for battery usage

### Security Checklist
- [ ] Generate and apply strict CSP headers
- [ ] Use Web Crypto API for sensitive data
- [ ] Implement secure Service Worker communication
- [ ] Enable HTTPS everywhere
- [ ] Regular security audits

### UX Checklist
- [ ] Platform-specific optimizations (iOS/Android)
- [ ] Offline-first approach with graceful degradation
- [ ] Touch-optimized interfaces (44px minimum)
- [ ] Responsive design with mobile-first approach
- [ ] Fast initial load (< 3s on 3G)

### Developer Experience
- [ ] Automated testing with PWA validator
- [ ] Performance monitoring dashboard
- [ ] Build-time optimizations
- [ ] Hot reload for development
- [ ] Comprehensive documentation

---

**Tags**: pwa-mobile, progressive-web-app, service-worker, offline-first, mobile-optimization, web-vitals, security, performance, caching-strategies, modern-apis