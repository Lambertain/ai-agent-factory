# Module 04: Security & Platform Optimization

## 🔒 Overview: Security в PWA

Безопасность - критический фактор успеха Progressive Web Apps. PWA должны обеспечивать уровень безопасности не ниже нативных приложений, защищая данные пользователей и предотвращая атаки.

**Ключевые аспекты безопасности:**
- **Content Security Policy (CSP)** - защита от XSS и injection атак
- **Secure Storage** - шифрование чувствительных данных
- **Platform Optimization** - адаптация под iOS и Android

**Compliance Requirements:**
- HTTPS везде (обязательно для PWA)
- CSP headers для защиты от XSS
- Secure cookies с SameSite
- Encryption для sensitive data

---

## 🛡️ Content Security Policy Generation

**Описание:** CSP (Content Security Policy) - это мощный механизм защиты от XSS, clickjacking и других code injection атак.

**Ключевые директивы CSP:**
- `default-src` - дефолтная политика для всех ресурсов
- `script-src` - откуда можно загружать JavaScript
- `style-src` - откуда можно загружать CSS
- `img-src` - откуда можно загружать изображения
- `connect-src` - куда можно делать fetch/XHR запросы

**Nonce-based CSP:**
Использование nonce (number used once) для разрешения inline скриптов без `unsafe-inline`.

### Базовая реализация

```javascript
class CSPGenerator {
  constructor(pwaType) {
    this.pwaType = pwaType;
    this.policies = this.getBasePolicy();
  }

  /**
   * Базовая CSP политика для PWA
   * @returns {Object} CSP директивы
   */
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

  /**
   * Добавить доверенный домен к директиве
   * @param {string} domain - Домен для добавления
   * @param {string} directive - CSP директива
   */
  addTrustedDomain(domain, directive = 'connect-src') {
    if (!this.policies[directive].includes(domain)) {
      this.policies[directive].push(domain);
    }
  }

  /**
   * Генерировать криптографически стойкий nonce
   * @returns {string} Base64-encoded nonce
   */
  generateNonce() {
    const array = new Uint8Array(16);
    crypto.getRandomValues(array);
    return btoa(String.fromCharCode.apply(null, array));
  }

  /**
   * Конвертировать политику в CSP header string
   * @returns {string} CSP header value
   */
  toHeaderString() {
    return Object.entries(this.policies)
      .map(([key, values]) => {
        if (values.length === 0) return key;
        return `${key} ${values.join(' ')}`;
      })
      .join('; ');
  }

  /**
   * Применить CSP и security headers к response
   * @param {Response} response - HTTP response
   * @returns {Object} Response с nonce для inline scripts
   */
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

### Интеграция в E-commerce PWA

```javascript
// Server-side CSP generation
const cspGenerator = new CSPGenerator('ecommerce');

// Добавить доверенные домены для payment providers
cspGenerator.addTrustedDomain('https://api.stripe.com', 'connect-src');
cspGenerator.addTrustedDomain('https://checkout.stripe.com', 'frame-src');
cspGenerator.addTrustedDomain('https://www.paypal.com', 'frame-src');

// Добавить CDN для изображений продуктов
cspGenerator.addTrustedDomain('https://cdn.shopify.com', 'img-src');

// Применить к response
app.use((req, res, next) => {
  const {response, nonce} = cspGenerator.applyToResponse(res);
  res.locals.cspNonce = nonce; // Для использования в шаблонах
  next();
});

// В HTML template - использовать nonce для inline scripts
// <script nonce="<%= cspNonce %>">
//   // Inline script разрешен с nonce
// </script>
```

---

## 🔐 Secure Storage with Web Crypto API

**Описание:** Web Crypto API предоставляет криптографические примитивы для шифрования данных в браузере без отправки на сервер.

**Ключевые возможности:**
- AES-GCM encryption для symmetric encryption
- RSA-OAEP для asymmetric encryption
- SHA-256/512 для hashing
- ECDSA для digital signatures

**Use Cases:**
- Хранение чувствительных данных (payment info, personal data)
- End-to-end encryption для messaging
- Secure session management

### Базовая реализация

```javascript
class SecureStorage {
  constructor() {
    this.dbName = 'secureStore';
    this.storeName = 'encrypted';
  }

  /**
   * Генерировать AES-256 ключ для шифрования
   * @returns {Promise<CryptoKey>} Encryption key
   */
  async generateKey() {
    return await crypto.subtle.generateKey(
      {name: 'AES-GCM', length: 256},
      true,
      ['encrypt', 'decrypt']
    );
  }

  /**
   * Зашифровать данные с помощью AES-GCM
   * @param {any} data - Данные для шифрования
   * @param {CryptoKey} key - Encryption key
   * @returns {Promise<Object>} Зашифрованные данные с IV
   */
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

  /**
   * Расшифровать данные
   * @param {Object} encryptedData - Зашифрованные данные с IV
   * @param {CryptoKey} key - Decryption key
   * @returns {Promise<any>} Расшифрованные данные
   */
  async decrypt(encryptedData, key) {
    const decryptedData = await crypto.subtle.decrypt(
      {name: 'AES-GCM', iv: new Uint8Array(encryptedData.iv)},
      key,
      new Uint8Array(encryptedData.data)
    );

    const decoder = new TextDecoder();
    return JSON.parse(decoder.decode(decryptedData));
  }

  /**
   * Сохранить зашифрованные данные в IndexedDB
   * @param {string} key - Storage key
   * @param {any} value - Value to store
   * @param {CryptoKey} encryptionKey - Encryption key
   */
  async store(key, value, encryptionKey) {
    const encrypted = await this.encrypt(value, encryptionKey);

    // Store in IndexedDB
    const db = await this.openDB();
    const tx = db.transaction([this.storeName], 'readwrite');
    await tx.objectStore(this.storeName).put({key, value: encrypted});
  }

  /**
   * Извлечь и расшифровать данные из IndexedDB
   * @param {string} key - Storage key
   * @param {CryptoKey} encryptionKey - Decryption key
   * @returns {Promise<any>} Расшифрованные данные
   */
  async retrieve(key, encryptionKey) {
    const db = await this.openDB();
    const tx = db.transaction([this.storeName], 'readonly');
    const result = await tx.objectStore(this.storeName).get(key);

    if (result) {
      return await this.decrypt(result.value, encryptionKey);
    }
    return null;
  }

  /**
   * Открыть или создать IndexedDB
   * @returns {Promise<IDBDatabase>} Database instance
   */
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

### Real-World Usage Example

```javascript
// Initialize secure storage
const secureStorage = new SecureStorage();

// Generate encryption key (store this securely!)
const encryptionKey = await secureStorage.generateKey();

// Store sensitive user data
const userData = {
  creditCard: '4242-4242-4242-4242',
  cvv: '123',
  expiryDate: '12/25'
};

await secureStorage.store('paymentInfo', userData, encryptionKey);

// Retrieve and decrypt when needed
const decryptedData = await secureStorage.retrieve('paymentInfo', encryptionKey);
console.log(decryptedData); // Original data

// Key Management Best Practices:
// 1. Generate key on first use
// 2. Store key in secure location (not in localStorage!)
// 3. Consider using user password to derive encryption key (PBKDF2)
// 4. Rotate keys periodically

// Example: Derive key from user password
async function deriveKeyFromPassword(password, salt) {
  const encoder = new TextEncoder();
  const passwordKey = await crypto.subtle.importKey(
    'raw',
    encoder.encode(password),
    {name: 'PBKDF2'},
    false,
    ['deriveBits', 'deriveKey']
  );

  return await crypto.subtle.deriveKey(
    {
      name: 'PBKDF2',
      salt: encoder.encode(salt),
      iterations: 100000,
      hash: 'SHA-256'
    },
    passwordKey,
    {name: 'AES-GCM', length: 256},
    true,
    ['encrypt', 'decrypt']
  );
}
```

---

## 📱 iOS Safari PWA Optimizations

**Описание:** iOS Safari имеет специфические требования и ограничения для PWA. Правильная оптимизация критична для native-like опыта.

**Ключевые особенности iOS PWA:**
- Отдельный engine для standalone mode (webkit, не Safari)
- Ограниченная поддержка Service Workers
- Специфические meta tags для status bar, splash screens
- Safe area insets для notch devices

**iOS PWA Checklist:**
- ✅ apple-mobile-web-app-capable meta tag
- ✅ apple-mobile-web-app-status-bar-style для status bar
- ✅ apple-touch-icon для home screen icon
- ✅ apple-touch-startup-image для splash screens
- ✅ viewport-fit=cover для notch support

### Базовая реализация

```javascript
class iOSOptimizer {
  /**
   * Определить iOS устройство (включая iPad на iPadOS 13+)
   * @returns {boolean} True если iOS
   */
  static detectiOS() {
    return /iPad|iPhone|iPod/.test(navigator.userAgent) ||
           (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  }

  /**
   * Применить все iOS-специфичные оптимизации
   */
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

  /**
   * Добавить splash screens для всех размеров iOS устройств
   */
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

### Интеграция в PWA

```javascript
// app.js - инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
  if (iOSOptimizer.detectiOS()) {
    iOSOptimizer.applyOptimizations();

    // iOS-specific fixes
    // Fix для 100vh на iOS Safari (notch compatibility)
    const updateVH = () => {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', `${vh}px`);
    };
    updateVH();
    window.addEventListener('resize', updateVH);

    // Prevent double-tap zoom
    let lastTouchEnd = 0;
    document.addEventListener('touchend', (event) => {
      const now = Date.now();
      if (now - lastTouchEnd <= 300) {
        event.preventDefault();
      }
      lastTouchEnd = now;
    }, false);
  }
});

// CSS - использование safe area insets
/*
.app-header {
  padding-top: var(--sat);
  padding-left: var(--sal);
  padding-right: var(--sar);
}

.app-footer {
  padding-bottom: var(--sab);
}

/* Использование --vh вместо vh для корректной высоты */
.full-height {
  height: 100vh; /* Fallback */
  height: calc(var(--vh, 1vh) * 100);
}
*/
```

---

## 🤖 Android TWA Configuration

**Описание:** Trusted Web Activities (TWA) позволяют запускать PWA как нативное Android приложение через Chrome Custom Tabs.

**Ключевые возможности TWA:**
- Полноэкранный режим без browser UI
- Digital Asset Links для верификации ownership
- Share Target API для sharing из других apps
- App Shortcuts для quick actions

**TWA Requirements:**
- HTTPS и valid SSL certificate
- Digital Asset Links JSON на сервере
- Signed APK с matching certificate fingerprint
- Service Worker для offline support

### Базовая реализация

```javascript
class AndroidOptimizer {
  /**
   * Определить Android устройство
   * @returns {boolean} True если Android
   */
  static detectAndroid() {
    return /Android/.test(navigator.userAgent);
  }

  /**
   * Генерировать Digital Asset Links для TWA
   * @returns {Array} Asset links configuration
   */
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

  /**
   * Применить Android-специфичные оптимизации
   */
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

  /**
   * Улучшить manifest.json для Android
   */
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

### TWA Integration Example

```javascript
// Server-side: Serve Digital Asset Links
// GET /.well-known/assetlinks.json
app.get('/.well-known/assetlinks.json', (req, res) => {
  res.json(AndroidOptimizer.generateAssetLinks());
});

// Client-side: Android optimizations
document.addEventListener('DOMContentLoaded', () => {
  if (AndroidOptimizer.detectAndroid()) {
    AndroidOptimizer.applyOptimizations();

    // Handle Share Target API
    if ('share' in navigator) {
      document.querySelector('.share-btn').addEventListener('click', async () => {
        try {
          await navigator.share({
            title: 'Check out this product',
            text: 'Amazing product from our PWA',
            url: window.location.href
          });
        } catch (err) {
          console.log('Share failed:', err);
        }
      });
    }

    // Handle App Shortcuts
    if ('getInstalledRelatedApps' in navigator) {
      navigator.getInstalledRelatedApps().then(relatedApps => {
        if (relatedApps.length > 0) {
          console.log('TWA installed:', relatedApps);
        }
      });
    }
  }
});

// manifest.json - Android shortcuts
/*
{
  "name": "My PWA",
  "short_name": "PWA",
  "shortcuts": [
    {
      "name": "View Cart",
      "short_name": "Cart",
      "description": "View your shopping cart",
      "url": "/cart",
      "icons": [{"src": "/icons/cart.png", "sizes": "192x192"}]
    },
    {
      "name": "Search Products",
      "short_name": "Search",
      "description": "Search for products",
      "url": "/search",
      "icons": [{"src": "/icons/search.png", "sizes": "192x192"}]
    }
  ]
}
*/
```

---

## 🎯 Best Practices: Security & Platform Optimization

### 1. Security Headers Setup

**Рекомендуемые заголовки:**
```javascript
// Express.js middleware
app.use((req, res, next) => {
  // CSP
  res.setHeader('Content-Security-Policy', cspGenerator.toHeaderString());

  // HTTPS enforcement
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');

  // Prevent MIME sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');

  // XSS protection
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // Referrer policy
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

  // Permissions policy
  res.setHeader('Permissions-Policy', 'geolocation=(), camera=(), microphone=()');

  next();
});
```

### 2. Platform Detection Strategy

```javascript
class PlatformDetector {
  static getPlatform() {
    if (iOSOptimizer.detectiOS()) return 'ios';
    if (AndroidOptimizer.detectAndroid()) return 'android';
    return 'desktop';
  }

  static applyPlatformOptimizations() {
    const platform = this.getPlatform();

    switch (platform) {
      case 'ios':
        iOSOptimizer.applyOptimizations();
        break;
      case 'android':
        AndroidOptimizer.applyOptimizations();
        break;
      default:
        // Desktop optimizations
        break;
    }
  }

  static isStandalone() {
    // Check if PWA is running in standalone mode
    return window.matchMedia('(display-mode: standalone)').matches ||
           window.navigator.standalone === true;
  }
}
```

### 3. Key Rotation Strategy

```javascript
class KeyRotationManager {
  constructor(rotationInterval = 30 * 24 * 60 * 60 * 1000) { // 30 days
    this.rotationInterval = rotationInterval;
  }

  async shouldRotateKey(keyMetadata) {
    const now = Date.now();
    const keyAge = now - keyMetadata.createdAt;
    return keyAge > this.rotationInterval;
  }

  async rotateKey(oldKey, secureStorage) {
    // Generate new key
    const newKey = await secureStorage.generateKey();

    // Re-encrypt all data with new key
    const allKeys = await this.getAllStorageKeys();

    for (const key of allKeys) {
      const data = await secureStorage.retrieve(key, oldKey);
      await secureStorage.store(key, data, newKey);
    }

    return newKey;
  }
}
```

---

**Версия модуля:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
**Проект:** AI Agent Factory - PWA Mobile Agent Modularization (5/7)

**Навигация:**
- [← Module 03: Performance & Monitoring](03_performance_monitoring.md)
- [→ Module 05: Testing & Best Practices](05_testing_best_practices.md)
- [↑ Назад к главной](../pwa_mobile_agent_knowledge.md)

**Tags:** security, csp, web-crypto-api, ios-optimization, android-twa, platform-specific, secure-storage
