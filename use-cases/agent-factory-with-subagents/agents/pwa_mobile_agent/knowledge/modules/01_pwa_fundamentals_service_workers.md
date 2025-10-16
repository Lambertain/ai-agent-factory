# Module 01: PWA Fundamentals & Service Workers

## 📚 Service Worker Strategies

Service Workers - это мощная технология, позволяющая создавать offline-first Progressive Web Apps с native-like опытом. Правильный выбор стратегии кэширования критически важен для производительности и пользовательского опыта.

### Cache-First Strategy

**Описание:** Приоритет отдается кэшу. Сначала проверяется наличие ресурса в кэше, и только при его отсутствии делается запрос к сети.

**Когда использовать:**
- Статический контент (CSS, JS, шрифты)
- Изображения продуктов в e-commerce
- Игровые ассеты
- Media thumbnails

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

**Преимущества:**
- Мгновенная загрузка кэшированных ресурсов
- Работает offline
- Снижение нагрузки на сеть

**Недостатки:**
- Может показывать устаревший контент
- Требует стратегии инвалидации кэша

---

### Network-First Strategy

**Описание:** Приоритет отдается сети. Сначала пытаемся получить свежие данные из сети, и только при неудаче используем кэш.

**Когда использовать:**
- Пользовательские данные (профили, настройки)
- Real-time updates (новости, котировки)
- API calls для динамического контента

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

**Преимущества:**
- Всегда свежие данные при наличии сети
- Graceful degradation при отсутствии сети

**Недостатки:**
- Медленнее при плохом соединении
- Не работает offline без предварительного кэширования

---

### Stale-While-Revalidate

**Описание:** Баланс между скоростью и актуальностью. Показываем кэшированные данные немедленно, но параллельно обновляем кэш из сети для следующего запроса.

**Когда использовать:**
- Новостные статьи
- Социальные ленты
- Каталоги продуктов
- Контент, где допустима некоторая задержка обновления

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

**Преимущества:**
- Мгновенная загрузка + автообновление
- Отличный UX баланс
- Работает offline

**Недостатки:**
- Пользователь может видеть устаревшие данные до следующего визита
- Дополнительные сетевые запросы

---

## 🚀 Advanced Caching Patterns

### Adaptive Loading Based on Network

**Описание:** Интеллектуальная адаптация качества контента в зависимости от скорости сети и экономии трафика.

**Use Cases:**
- Responsive Images (разное качество для 2G/3G/4G)
- Video quality adaptation
- Lazy loading with network awareness
- Data saver mode

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

**Интеграция в приложение:**
```javascript
// E-commerce product gallery
const productImages = document.querySelectorAll('.product-img');
productImages.forEach(async img => {
  const optimizedSrc = await loadImage(img.dataset.src);
  img.src = optimizedSrc;
});

// Видео-плеер
const videoPlayer = document.querySelector('video');
const network = await getNetworkSpeed();
if (network.is2G) {
  videoPlayer.src = 'video-360p.mp4';
} else if (network.is3G) {
  videoPlayer.src = 'video-720p.mp4';
} else {
  videoPlayer.src = 'video-1080p.mp4';
}
```

---

### Intelligent Cache Management

**Описание:** Автоматическое управление размером кэша, очистка старых данных и мониторинг квоты storage.

**Ключевые возможности:**
- Автоочистка устаревших кэшей
- LRU (Least Recently Used) eviction
- Storage quota monitoring
- Предотвращение переполнения

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

**Использование в Service Worker:**
```javascript
// sw.js
const cacheManager = new CacheManager(100 * 1024 * 1024); // 100MB

self.addEventListener('activate', event => {
  event.waitUntil(
    cacheManager.cleanOldCaches()
  );
});

// Периодическая проверка квоты
setInterval(async () => {
  const quota = await cacheManager.checkStorageQuota();
  console.log(`Cache usage: ${quota.percentUsed.toFixed(2)}%`);
}, 60000); // Каждую минуту
```

---

## 🏗️ Progressive Enhancement Strategy

**Описание:** Прогрессивное улучшение - это подход к разработке, при котором базовая функциональность работает без JavaScript, а дополнительные фичи добавляются при их поддержке.

**Принципы:**
1. Базовый функционал работает без JS
2. PWA фичи добавляются постепенно
3. Feature detection вместо browser detection
4. Graceful degradation

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

**Инициализация PWA:**
```javascript
// app.js - Entry point
document.addEventListener('DOMContentLoaded', () => {
  ProgressiveEnhancement.enhance();
});
```

---

## 📊 Best Practices: Service Workers

### 1. Versioning Strategy
```javascript
const CACHE_VERSION = 'v2';
const CACHE_NAME = `my-pwa-${CACHE_VERSION}`;

// При обновлении версии старые кэши удаляются
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
```

### 2. Precaching Critical Resources
```javascript
const PRECACHE_URLS = [
  '/',
  '/styles/main.css',
  '/scripts/app.js',
  '/offline.html'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(PRECACHE_URLS);
    })
  );
});
```

### 3. Skip Waiting для быстрых обновлений
```javascript
self.addEventListener('install', event => {
  // Активировать новый SW немедленно
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  // Захватить всех клиентов немедленно
  event.waitUntil(clients.claim());
});
```

---

## 🎯 Применение по типам приложений

### E-commerce PWA
```javascript
// Комбинированная стратегия
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Product images - Cache First
  if (url.pathname.startsWith('/images/products/')) {
    event.respondWith(cacheFirstStrategy(event.request));
  }
  // API calls - Network First
  else if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirstStrategy(event.request));
  }
  // Static assets - Cache First
  else if (url.pathname.match(/\.(css|js|woff2)$/)) {
    event.respondWith(cacheFirstStrategy(event.request));
  }
  // HTML pages - Stale While Revalidate
  else {
    event.respondWith(staleWhileRevalidateStrategy(event.request));
  }
});
```

### News/Media PWA
```javascript
// Оптимизация для контента
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Articles - Stale While Revalidate
  if (url.pathname.startsWith('/articles/')) {
    event.respondWith(staleWhileRevalidateStrategy(event.request));
  }
  // Breaking news - Network First
  else if (url.pathname === '/breaking') {
    event.respondWith(networkFirstStrategy(event.request));
  }
  // Images/Videos - Cache First + Adaptive
  else if (url.pathname.match(/\.(jpg|mp4|webm)$/)) {
    event.respondWith(adaptiveCacheStrategy(event.request));
  }
});
```

---

**Версия модуля:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
**Проект:** AI Agent Factory - PWA Mobile Agent Modularization (5/7)

**Навигация:**
- [← Назад к главной](../pwa_mobile_agent_knowledge.md)
- [→ Module 02: Modern Web APIs Integration](02_modern_web_apis_integration.md)

**Tags:** service-workers, caching-strategies, progressive-enhancement, offline-first, cache-management
