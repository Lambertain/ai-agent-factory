# Module 02: Modern Web APIs Integration

## 🆕 Overview: Modern Web APIs for PWA

Современные Web APIs расширяют возможности Progressive Web Apps, приближая их к native приложениям. Эти API предоставляют доступ к системным функциям, улучшают user experience и повышают engagement.

**Ключевые преимущества:**
- Native-like функциональность в браузере
- Улучшенная интеграция с ОС
- Повышенный user engagement
- Cross-platform совместимость

**Covered APIs:**
1. File System Access API - работа с локальными файлами
2. Badging API - счетчики на иконке приложения
3. Wake Lock API - предотвращение засыпания экрана
4. Idle Detection API - определение неактивности пользователя

---

## 📁 File System Access API

**Описание:** Прямой доступ к файловой системе устройства для чтения, записи и управления файлами без ограничений традиционных веб-приложений.

**Поддержка браузеров:**
- Chrome 86+ (полная поддержка)
- Edge 86+
- Safari (частичная поддержка)
- Firefox (в разработке)

**Use Cases:**
- Text/code editors (VS Code Web, Monaco Editor)
- Document processors (Google Docs offline)
- File managers (облачные хранилища)
- Data import/export tools (CSV editors, JSON validators)
- Image editors (Photopea, Figma)

### Базовая реализация

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

### Продвинутый File Manager

```javascript
class FileSystemManager {
  constructor() {
    this.currentHandle = null;
  }

  /**
   * Открыть файл с фильтрацией по типу
   * @param {Object} options - Опции открытия файла
   * @returns {Promise<{handle: FileSystemFileHandle, content: string}>}
   */
  async openFile(options = {}) {
    const pickerOpts = {
      types: options.types || [{
        description: 'All Files',
        accept: { '*/*': ['*'] }
      }],
      multiple: false,
      ...options
    };

    const [fileHandle] = await window.showOpenFilePicker(pickerOpts);
    this.currentHandle = fileHandle;

    const file = await fileHandle.getFile();
    const content = await file.text();

    return { handle: fileHandle, content };
  }

  /**
   * Сохранить файл
   * @param {string} content - Контент для сохранения
   * @param {FileSystemFileHandle} handle - Опциональный handle существующего файла
   */
  async saveFile(content, handle = null) {
    const fileHandle = handle || this.currentHandle;

    if (!fileHandle) {
      // Save As - новый файл
      return await this.saveFileAs(content);
    }

    const writable = await fileHandle.createWritable();
    await writable.write(content);
    await writable.close();

    return fileHandle;
  }

  /**
   * Save As - выбор нового местоположения
   */
  async saveFileAs(content, options = {}) {
    const saveOpts = {
      suggestedName: 'untitled.txt',
      types: [{
        description: 'Text Files',
        accept: { 'text/plain': ['.txt'] }
      }],
      ...options
    };

    const fileHandle = await window.showSaveFilePicker(saveOpts);
    this.currentHandle = fileHandle;

    await this.saveFile(content, fileHandle);
    return fileHandle;
  }

  /**
   * Работа с директориями
   */
  async openDirectory() {
    const dirHandle = await window.showDirectoryPicker();
    const files = [];

    for await (const entry of dirHandle.values()) {
      files.push({
        name: entry.name,
        kind: entry.kind,
        handle: entry
      });
    }

    return { handle: dirHandle, files };
  }
}
```

**Применение:**
```javascript
// Code Editor PWA
const fileManager = new FileSystemManager();

document.getElementById('openBtn').addEventListener('click', async () => {
  const { content } = await fileManager.openFile({
    types: [{
      description: 'JavaScript Files',
      accept: { 'text/javascript': ['.js', '.jsx'] }
    }]
  });
  editor.setValue(content);
});

document.getElementById('saveBtn').addEventListener('click', async () => {
  await fileManager.saveFile(editor.getValue());
  showNotification('File saved!');
});
```

---

## 🏷️ Badging API

**Описание:** Отображение числовых или flag badge на иконке приложения для показа уведомлений, непрочитанных сообщений или статусов.

**Поддержка браузеров:**
- Chrome 81+ (Android, Windows, macOS, ChromeOS)
- Edge 81+
- Safari 16.4+ (macOS, iOS)

**Use Cases:**
- Unread messages count (мессенджеры, почта)
- Shopping cart items (e-commerce)
- Pending notifications (социальные сети)
- Task reminders (productivity apps)
- Live order status (доставка, такси)

### Базовая реализация

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

### Интеграция с различными типами приложений

```javascript
// E-commerce - Shopping Cart Badge
class CartBadgeManager extends BadgeManager {
  constructor() {
    super();
    this.cartItems = [];
  }

  addItem(item) {
    this.cartItems.push(item);
    this.updateBadge();
  }

  removeItem(itemId) {
    this.cartItems = this.cartItems.filter(item => item.id !== itemId);
    this.updateBadge();
  }

  async updateBadge() {
    await BadgeManager.setBadge(this.cartItems.length);
  }

  async clearCart() {
    this.cartItems = [];
    await BadgeManager.clearBadge();
  }
}

// Messaging App - Unread Messages Badge
class MessageBadgeManager extends BadgeManager {
  constructor() {
    super();
    this.unreadCount = 0;
  }

  async incrementUnread() {
    this.unreadCount++;
    await BadgeManager.setBadge(this.unreadCount);
  }

  async markAllRead() {
    this.unreadCount = 0;
    await BadgeManager.clearBadge();
  }

  async setUnreadCount(count) {
    this.unreadCount = count;
    await BadgeManager.setBadge(count);
  }
}

// Service Worker integration - показывать badge при push уведомлении
self.addEventListener('push', event => {
  const data = event.data.json();

  // Показать notification
  self.registration.showNotification(data.title, {
    body: data.body,
    badge: '/images/badge.png'
  });

  // Обновить badge count
  event.waitUntil(
    navigator.setAppBadge(data.unreadCount)
  );
});
```

---

## 🔒 Wake Lock API

**Описание:** Предотвращение автоматического выключения экрана или перехода устройства в спящий режим во время важных операций.

**Поддержка браузеров:**
- Chrome 84+
- Edge 84+
- Safari 16.4+ (iOS, macOS)

**Use Cases:**
- Video/audio playback (YouTube, Spotify)
- Gaming sessions (браузерные игры)
- Presentation mode (Google Slides)
- Reading long content (e-books, articles)
- Cooking recipes (пошаговые инструкции)
- Fitness tracking (таймеры тренировок)

### Базовая реализация

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

### Интеграция в Video Player

```javascript
class VideoPlayerWithWakeLock {
  constructor(videoElement) {
    this.video = videoElement;
    this.wakeLockManager = new WakeLockManager();
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Запросить Wake Lock при воспроизведении
    this.video.addEventListener('play', async () => {
      await this.wakeLockManager.requestWakeLock();
      console.log('Wake Lock активирован - экран не будет выключаться');
    });

    // Освободить Wake Lock при паузе
    this.video.addEventListener('pause', async () => {
      await this.wakeLockManager.releaseWakeLock();
      console.log('Wake Lock деактивирован');
    });

    // Освободить Wake Lock при окончании видео
    this.video.addEventListener('ended', async () => {
      await this.wakeLockManager.releaseWakeLock();
    });
  }
}

// Использование
const video = document.querySelector('video');
const player = new VideoPlayerWithWakeLock(video);
```

### Интеграция в Gaming PWA

```javascript
class GameWakeLockManager extends WakeLockManager {
  constructor() {
    super();
    this.isGameActive = false;
  }

  async startGame() {
    this.isGameActive = true;
    await this.requestWakeLock();
    console.log('Игра начата - экран защищен от засыпания');
  }

  async pauseGame() {
    this.isGameActive = false;
    await this.releaseWakeLock();
    console.log('Игра на паузе - Wake Lock освобожден');
  }

  async endGame() {
    this.isGameActive = false;
    await this.releaseWakeLock();
    console.log('Игра завершена');
  }

  // Автоматическое восстановление при возврате в приложение
  async handleVisibilityChange() {
    if (document.visibilityState === 'visible' && this.isGameActive) {
      await this.requestWakeLock();
    }
  }
}
```

---

## 😴 Idle Detection API

**Описание:** Определение периодов неактивности пользователя для оптимизации ресурсов, автосохранения данных и улучшения battery life.

**Поддержка браузеров:**
- Chrome 94+ (experimental flag)
- Edge 94+ (experimental flag)

**Use Cases:**
- Auto-save state (текстовые редакторы)
- Pause background tasks (экономия ресурсов)
- Update presence status (чаты, видеоконференции)
- Battery optimization (мобильные PWA)
- Session timeout warnings (банкинг, админ панели)

### Базовая реализация

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

### Интеграция в Productivity App

```javascript
class ProductivityIdleManager extends IdleManager {
  constructor(autoSaveCallback, threshold = 30000) { // 30 seconds
    super(threshold);
    this.autoSaveCallback = autoSaveCallback;
    this.idleStartTime = null;
  }

  onUserIdle() {
    super.onUserIdle();

    // Автосохранение при переходе в idle
    if (this.autoSaveCallback) {
      this.autoSaveCallback();
      console.log('Auto-saved due to inactivity');
    }

    // Pause real-time collaboration sync
    this.pauseCollaborationSync();

    // Reduce polling frequency
    this.slowDownPolling();

    this.idleStartTime = Date.now();
  }

  onUserActive() {
    super.onUserActive();

    // Resume collaboration sync
    this.resumeCollaborationSync();

    // Restore normal polling
    this.restoreNormalPolling();

    // Sync changes made during idle time
    this.syncPendingChanges();

    if (this.idleStartTime) {
      const idleDuration = Date.now() - this.idleStartTime;
      console.log(`User was idle for ${idleDuration / 1000} seconds`);
      this.idleStartTime = null;
    }
  }

  pauseCollaborationSync() {
    // Implementation
  }

  resumeCollaborationSync() {
    // Implementation
  }

  slowDownPolling() {
    // Reduce API calls from 5s to 60s intervals
  }

  restoreNormalPolling() {
    // Restore 5s polling
  }

  syncPendingChanges() {
    // Sync any changes made while user was idle
  }
}

// Usage
const autoSave = () => {
  const content = editor.getValue();
  localStorage.setItem('draft', content);
};

const idleManager = new ProductivityIdleManager(autoSave, 30000);
await idleManager.startMonitoring();
```

### Интеграция в Chat/Video Conference App

```javascript
class PresenceIdleManager extends IdleManager {
  constructor(updatePresenceCallback, threshold = 60000) {
    super(threshold);
    this.updatePresence = updatePresenceCallback;
    this.currentStatus = 'active';
  }

  onUserIdle() {
    super.onUserIdle();

    // Update presence to "away"
    this.currentStatus = 'away';
    this.updatePresence('away');

    // Pause camera/microphone in video call
    this.pauseMediaDevices();

    // Reduce bandwidth usage
    this.optimizeBandwidth();
  }

  onUserActive() {
    super.onUserActive();

    // Update presence to "active"
    this.currentStatus = 'active';
    this.updatePresence('active');

    // Resume media devices if was in call
    this.resumeMediaDevices();

    // Restore full quality
    this.restoreQuality();
  }

  pauseMediaDevices() {
    // Pause camera feed, mute microphone
  }

  resumeMediaDevices() {
    // Resume if user was in active call
  }

  optimizeBandwidth() {
    // Lower video quality, reduce frame rate
  }

  restoreQuality() {
    // Restore original settings
  }
}
```

---

## 🎯 Best Practices: Modern Web APIs

### 1. Feature Detection
```javascript
function checkAPISupport() {
  return {
    fileSystem: 'showOpenFilePicker' in window,
    badging: 'setAppBadge' in navigator,
    wakeLock: 'wakeLock' in navigator,
    idleDetection: 'IdleDetector' in window
  };
}

const support = checkAPISupport();
if (support.fileSystem) {
  enableFileSystemFeatures();
}
```

### 2. Graceful Degradation
```javascript
async function requestWakeLockWithFallback() {
  if ('wakeLock' in navigator) {
    return await navigator.wakeLock.request('screen');
  } else {
    // Fallback: показать инструкцию пользователю
    showManualWakeLockInstructions();
    return null;
  }
}
```

### 3. Permission Handling
```javascript
async function requestIdleDetectionWithPermission() {
  try {
    const permission = await IdleDetector.requestPermission();
    if (permission === 'granted') {
      return new IdleDetector();
    }
  } catch (err) {
    console.error('Permission denied:', err);
    return null;
  }
}
```

---

**Версия модуля:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
**Проект:** AI Agent Factory - PWA Mobile Agent Modularization (5/7)

**Навигация:**
- [← Module 01: PWA Fundamentals & Service Workers](01_pwa_fundamentals_service_workers.md)
- [→ Module 03: Performance & Monitoring](03_performance_monitoring.md)
- [↑ Назад к главной](../pwa_mobile_agent_knowledge.md)

**Tags:** file-system-api, badging-api, wake-lock-api, idle-detection-api, modern-web-apis, pwa-capabilities
