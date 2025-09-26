"""
Универсальные инструменты для PWA Mobile Agent.

Адаптируются под различные типы PWA приложений.
"""

import json
import os
from typing import Dict, Any, List
from pydantic_ai import RunContext
from .dependencies import PWAMobileAgentDependencies
from .prompts import (
    MANIFEST_GENERATION_PROMPT,
    SERVICE_WORKER_PROMPT,
    MOBILE_UX_PROMPT,
    OFFLINE_SYNC_PROMPT
)


async def generate_pwa_manifest(
    ctx: RunContext[PWAMobileAgentDependencies],
    app_name: str,
    description: str = ""
) -> str:
    """
    Генерирует оптимальный Web App Manifest для типа PWA приложения.

    Args:
        app_name: Название приложения
        description: Описание приложения

    Returns:
        JSON манифест, оптимизированный под тип PWA
    """
    deps = ctx.deps

    # Обновляем зависимости если переданы параметры
    if app_name:
        deps.app_name = app_name
    if description:
        deps.app_description = description

    # Базовый манифест
    manifest = {
        "name": deps.app_name,
        "short_name": deps.app_short_name or deps.app_name[:12],
        "description": deps.app_description,
        "start_url": deps.start_url,
        "display": deps.display_mode,
        "orientation": deps.orientation,
        "theme_color": deps.theme_color,
        "background_color": deps.background_color,
        "scope": "/",
        "lang": "en",
        "dir": "ltr",

        # Универсальные иконки
        "icons": _generate_icon_set(),

        # Категории на основе типа PWA
        "categories": deps._get_categories(),

        # Screenshots для store
        "screenshots": _generate_screenshots(deps.pwa_type),

        # Preferences
        "prefer_related_applications": False,
        "related_applications": []
    }

    # Добавляем специфичные для типа PWA настройки
    manifest.update(_get_type_specific_manifest_config(deps))

    return f"""
Web App Manifest для {deps.pwa_type} PWA приложения:

```json
{json.dumps(manifest, indent=2, ensure_ascii=False)}
```

**Ключевые особенности для {deps.pwa_type}:**
{_get_manifest_features_description(deps.pwa_type)}

**Инструкции по установке:**
1. Сохрани как `public/manifest.json`
2. Добавь в HTML: `<link rel="manifest" href="/manifest.json">`
3. Добавь meta теги для theme-color и viewport
4. Создай иконки в папке `public/icons/`
"""


async def create_service_worker(
    ctx: RunContext[PWAMobileAgentDependencies],
    cache_strategies: str = ""
) -> str:
    """
    Создает оптимальный Service Worker с стратегиями кэширования.

    Args:
        cache_strategies: Дополнительные требования к кэшированию

    Returns:
        Код Service Worker, адаптированный под тип PWA
    """
    deps = ctx.deps
    sw_config = deps.get_service_worker_config()

    # Генерируем Service Worker код
    service_worker_code = _generate_service_worker_code(deps, cache_strategies)

    return f"""
Service Worker для {deps.pwa_type} PWA приложения:

```javascript
{service_worker_code}
```

**Настроенные стратегии кэширования:**
{_get_caching_strategies_description(sw_config)}

**Настройка проекта:**
1. Сохрани как `public/sw.js`
2. Зарегистрируй в `app/layout.tsx` или `_app.tsx`
3. Настрой Workbox в `next.config.js` (если используешь)
4. Добавь offline страницу `public/offline.html`

**Дополнительные возможности:**
{_get_additional_features_description(deps)}
"""


async def optimize_mobile_ux(
    ctx: RunContext[PWAMobileAgentDependencies],
    component_type: str = "general"
) -> str:
    """
    Генерирует мобильные UX оптимизации для компонентов.

    Args:
        component_type: Тип компонента для оптимизации

    Returns:
        Рекомендации и код для мобильной UX оптимизации
    """
    deps = ctx.deps

    # Генерируем мобильные компоненты
    mobile_components = _generate_mobile_components(deps, component_type)

    return f"""
Мобильная UX оптимизация для {deps.pwa_type} приложения:

{mobile_components}

**Touch interaction guidelines:**
- Минимальный размер touch targets: 44x44px
- Spacing между кликабельными элементами: 8px
- Swipe gestures для навигации
- Pull-to-refresh для обновления данных

**Responsive breakpoints:**
- Mobile: 320px - 768px
- Tablet: 768px - 1024px
- Desktop: 1024px+

**Performance оптимизации:**
- Lazy loading для изображений
- Virtual scrolling для длинных списков
- Debounced search inputs
- Optimistic UI updates
"""


async def analyze_mobile_performance(
    ctx: RunContext[PWAMobileAgentDependencies],
    performance_focus: str = "general"
) -> str:
    """
    Анализирует мобильную производительность и предлагает оптимизации.

    Args:
        performance_focus: Фокус анализа (loading, runtime, offline)

    Returns:
        Анализ производительности и рекомендации
    """
    deps = ctx.deps

    performance_recommendations = _generate_performance_recommendations(deps, performance_focus)

    return f"""
Анализ мобильной производительности для {deps.pwa_type} PWA:

{performance_recommendations}

**Core Web Vitals цели:**
- LCP (Largest Contentful Paint): < 2.5s
- FID (First Input Delay): < 100ms
- CLS (Cumulative Layout Shift): < 0.1
- INP (Interaction to Next Paint): < 200ms

**Lighthouse PWA чеклист:**
- Installable: ✓ Manifest + Service Worker
- PWA-Optimized: ✓ Offline support
- Fast and reliable: ✓ Performance metrics
- Engaging: ✓ Добавление на домашний экран

**Рекомендуемые инструменты:**
- Chrome DevTools Lighthouse
- WebPageTest for field testing
- Workbox для Service Worker генерации
"""


async def setup_offline_sync(
    ctx: RunContext[PWAMobileAgentDependencies],
    data_type: str = "general"
) -> str:
    """
    Настраивает offline режим и синхронизацию данных.

    Args:
        data_type: Тип данных для синхронизации

    Returns:
        Код и стратегии для offline функциональности
    """
    deps = ctx.deps

    offline_code = _generate_offline_sync_code(deps, data_type)

    return f"""
Offline синхронизация для {deps.pwa_type} приложения:

{offline_code}

**Стратегия синхронизации:**
- Online: прямые API вызовы
- Offline: запись в IndexedDB
- Background sync: автоматическая синхронизация при восстановлении сети

**Conflict resolution:**
- Last-write-wins для простых случаев
- Operational transforms для коллаборативного редактирования
- User choice для критических конфликтов

**Storage limits:**
- Quota API для мониторинга доступного места
- Automatic cleanup старых данных
- User notification при нехватке места
"""


async def implement_file_system_access_api(
    ctx: RunContext[PWAMobileAgentDependencies],
    file_operations: str = "read,write"
) -> str:
    """
    Реализует File System Access API для productivity PWA.

    Args:
        file_operations: Тип операций (read, write, readwrite)

    Returns:
        Код для работы с File System Access API
    """
    deps = ctx.deps

    if deps.pwa_type not in ["productivity", "general"]:
        return f"⚠️ File System Access API рекомендуется для productivity приложений. Текущий тип: {deps.pwa_type}"

    return f"""
## File System Access API для {deps.pwa_type} PWA

### Проверка поддержки браузера
```typescript
function isFileSystemAccessSupported(): boolean {{
  return 'showOpenFilePicker' in window &&
         'showSaveFilePicker' in window &&
         'showDirectoryPicker' in window;
}}
```

### Чтение файлов
```typescript
export async function openFile(): Promise<File | null> {{
  try {{
    if (!isFileSystemAccessSupported()) {{
      // Fallback к input[type="file"]
      return await openFileWithInput();
    }}

    const [fileHandle] = await window.showOpenFilePicker({{
      types: [
        {{
          description: '{deps.pwa_type.title()} files',
          accept: {{
            'text/plain': ['.txt', '.md'],
            'application/json': ['.json'],
            'text/markdown': ['.md']
          }}
        }}
      ],
      excludeAcceptAllOption: true,
      multiple: false
    }});

    const file = await fileHandle.getFile();
    return file;
  }} catch (error) {{
    if (error.name !== 'AbortError') {{
      console.error('File open error:', error);
    }}
    return null;
  }}
}}
```

### Сохранение файлов
```typescript
export async function saveFile(content: string, filename: string = 'document.txt'): Promise<boolean> {{
  try {{
    if (!isFileSystemAccessSupported()) {{
      // Fallback к download link
      return downloadFile(content, filename);
    }}

    const fileHandle = await window.showSaveFilePicker({{
      suggestedName: filename,
      types: [
        {{
          description: '{deps.pwa_type.title()} files',
          accept: {{
            'text/plain': ['.txt'],
            'application/json': ['.json']
          }}
        }}
      ]
    }});

    const writable = await fileHandle.createWritable();
    await writable.write(content);
    await writable.close();

    return true;
  }} catch (error) {{
    if (error.name !== 'AbortError') {{
      console.error('File save error:', error);
    }}
    return false;
  }}
}}
```

### Работа с директориями
```typescript
export async function openDirectory(): Promise<FileSystemDirectoryHandle | null> {{
  try {{
    if (!('showDirectoryPicker' in window)) {{
      throw new Error('Directory picking not supported');
    }}

    const directoryHandle = await window.showDirectoryPicker({{
      mode: 'readwrite'
    }});

    return directoryHandle;
  }} catch (error) {{
    console.error('Directory open error:', error);
    return null;
  }}
}}

export async function listDirectoryFiles(directoryHandle: FileSystemDirectoryHandle): Promise<string[]> {{
  const files: string[] = [];

  for await (const [name, handle] of directoryHandle.entries()) {{
    if (handle.kind === 'file') {{
      files.push(name);
    }}
  }}

  return files;
}}
```

### Fallback реализация
```typescript
function openFileWithInput(): Promise<File | null> {{
  return new Promise((resolve) => {{
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.txt,.md,.json';

    input.onchange = (e) => {{
      const file = (e.target as HTMLInputElement).files?.[0];
      resolve(file || null);
    }};

    input.click();
  }});
}}

function downloadFile(content: string, filename: string): boolean {{
  try {{
    const blob = new Blob([content], {{ type: 'text/plain' }});
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();

    URL.revokeObjectURL(url);
    return true;
  }} catch (error) {{
    console.error('Download error:', error);
    return false;
  }}
}}
```

### React Hook для File System Access
```typescript
export function useFileSystemAccess() {{
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {{
    setIsSupported(isFileSystemAccessSupported());
  }}, []);

  return {{
    isSupported,
    openFile,
    saveFile,
    openDirectory
  }};
}}
```

**Преимущества для {deps.pwa_type} приложений:**
- Прямая интеграция с файловой системой
- Без ограничений на размер файлов
- Сохранение permissions между сессиями
- Нативный UX при работе с файлами

**Поддержка браузеров:**
- Chrome/Edge 86+
- Safari: частичная поддержка
- Firefox: в разработке

**Требования безопасности:**
- HTTPS обязателен
- User gesture required
- Secure context only
"""


async def implement_badging_api(
    ctx: RunContext[PWAMobileAgentDependencies],
    badge_type: str = "count"
) -> str:
    """
    Реализует Badging API для отображения уведомлений на иконке приложения.

    Args:
        badge_type: Тип badge (count, flag, custom)

    Returns:
        Код для работы с Badging API
    """
    deps = ctx.deps

    return f"""
## Badging API для {deps.pwa_type} PWA

### Проверка поддержки
```typescript
function isBadgingSupported(): boolean {{
  return 'setAppBadge' in navigator && 'clearAppBadge' in navigator;
}}
```

### Установка badge с числом
```typescript
export async function setAppBadge(count?: number): Promise<boolean> {{
  try {{
    if (!isBadgingSupported()) {{
      console.warn('Badging API not supported');
      return false;
    }}

    if (count === undefined || count === 0) {{
      // Показать флаг без числа
      await navigator.setAppBadge();
    }} else {{
      // Показать badge с числом
      await navigator.setAppBadge(count);
    }}

    return true;
  }} catch (error) {{
    console.error('Badge set error:', error);
    return false;
  }}
}}
```

### Очистка badge
```typescript
export async function clearAppBadge(): Promise<boolean> {{
  try {{
    if (!isBadgingSupported()) {{
      return false;
    }}

    await navigator.clearAppBadge();
    return true;
  }} catch (error) {{
    console.error('Badge clear error:', error);
    return false;
  }}
}}
```

### Badge Manager для {deps.pwa_type}
```typescript
class {deps.pwa_type.title()}BadgeManager {{
  private currentCount = 0;

  constructor() {{
    // Восстанавливаем счетчик из localStorage
    const stored = localStorage.getItem('{deps.pwa_type}-badge-count');
    this.currentCount = stored ? parseInt(stored, 10) : 0;
    this.updateBadge();
  }}

  async increment(): Promise<void> {{
    this.currentCount++;
    await this.updateBadge();
    this.persistCount();
  }}

  async decrement(): Promise<void> {{
    this.currentCount = Math.max(0, this.currentCount - 1);
    await this.updateBadge();
    this.persistCount();
  }}

  async reset(): Promise<void> {{
    this.currentCount = 0;
    await clearAppBadge();
    this.persistCount();
  }}

  async setCount(count: number): Promise<void> {{
    this.currentCount = Math.max(0, count);
    await this.updateBadge();
    this.persistCount();
  }}

  getCount(): number {{
    return this.currentCount;
  }}

  private async updateBadge(): Promise<void> {{
    if (this.currentCount > 0) {{
      await setAppBadge(this.currentCount);
    }} else {{
      await clearAppBadge();
    }}
  }}

  private persistCount(): void {{
    localStorage.setItem('{deps.pwa_type}-badge-count', this.currentCount.toString());
  }}
}}
```

### Специфичная реализация для {deps.pwa_type}
```typescript
{_get_badging_implementation_for_type(deps.pwa_type)}
```

### React Hook для Badging
```typescript
export function useAppBadge() {{
  const [badgeManager] = useState(() => new {deps.pwa_type.title()}BadgeManager());
  const [count, setCount] = useState(badgeManager.getCount());
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {{
    setIsSupported(isBadgingSupported());
  }}, []);

  const increment = useCallback(async () => {{
    await badgeManager.increment();
    setCount(badgeManager.getCount());
  }}, [badgeManager]);

  const decrement = useCallback(async () => {{
    await badgeManager.decrement();
    setCount(badgeManager.getCount());
  }}, [badgeManager]);

  const reset = useCallback(async () => {{
    await badgeManager.reset();
    setCount(0);
  }}, [badgeManager]);

  const setBadgeCount = useCallback(async (newCount: number) => {{
    await badgeManager.setCount(newCount);
    setCount(badgeManager.getCount());
  }}, [badgeManager]);

  return {{
    count,
    isSupported,
    increment,
    decrement,
    reset,
    setBadgeCount
  }};
}}
```

### Service Worker интеграция
```typescript
// В service worker
self.addEventListener('message', (event) => {{
  if (event.data && event.data.type === 'UPDATE_BADGE') {{
    const count = event.data.count;
    if (count > 0) {{
      self.registration.setAppBadge(count);
    }} else {{
      self.registration.clearAppBadge();
    }}
  }}
}});

// Push notification handler
self.addEventListener('push', (event) => {{
  // Обновляем badge при получении push уведомления
  const data = event.data?.json() ?? {{}};

  event.waitUntil(
    Promise.all([
      self.registration.showNotification(data.title, {{ /* options */ }}),
      self.registration.setAppBadge(data.badgeCount || 1)
    ])
  );
}});
```

**Применение для {deps.pwa_type}:**
{_get_badging_use_cases_for_type(deps.pwa_type)}

**Поддержка браузеров:**
- Chrome/Edge 81+
- Safari 16.4+
- Firefox: в планах

**Ограничения:**
- Работает только в installed PWA
- Требует HTTPS
- Platform-specific отображение
"""


async def implement_wake_lock_api(
    ctx: RunContext[PWAMobileAgentDependencies],
    lock_type: str = "screen"
) -> str:
    """
    Реализует Wake Lock API для предотвращения засыпания экрана.

    Args:
        lock_type: Тип блокировки (screen, system)

    Returns:
        Код для работы с Wake Lock API
    """
    deps = ctx.deps

    if deps.pwa_type not in ["gaming", "media", "general"]:
        return f"⚠️ Wake Lock API наиболее полезен для gaming и media приложений. Текущий тип: {deps.pwa_type}"

    return f"""
## Wake Lock API для {deps.pwa_type} PWA

### Проверка поддержки
```typescript
function isWakeLockSupported(): boolean {{
  return 'wakeLock' in navigator;
}}
```

### Wake Lock Manager
```typescript
class WakeLockManager {{
  private wakeLock: WakeLockSentinel | null = null;
  private isActive = false;

  async request(): Promise<boolean> {{
    try {{
      if (!isWakeLockSupported()) {{
        console.warn('Wake Lock API not supported');
        return false;
      }}

      if (this.wakeLock) {{
        console.log('Wake lock already active');
        return true;
      }}

      this.wakeLock = await navigator.wakeLock.request('screen');
      this.isActive = true;

      // Обработчик события release
      this.wakeLock.addEventListener('release', () => {{
        console.log('Wake lock was released');
        this.isActive = false;
        this.wakeLock = null;
      }});

      console.log('Wake lock activated');
      return true;
    }} catch (error) {{
      console.error('Wake lock request failed:', error);
      return false;
    }}
  }}

  async release(): Promise<boolean> {{
    try {{
      if (this.wakeLock) {{
        await this.wakeLock.release();
        this.wakeLock = null;
        this.isActive = false;
        console.log('Wake lock released manually');
        return true;
      }}
      return false;
    }} catch (error) {{
      console.error('Wake lock release failed:', error);
      return false;
    }}
  }}

  isLockActive(): boolean {{
    return this.isActive && this.wakeLock !== null;
  }}

  // Автоматический перезапрос после возврата в приложение
  async reacquire(): Promise<boolean> {{
    if (this.isActive && !this.wakeLock) {{
      return await this.request();
    }}
    return false;
  }}
}}
```

### Автоматическое управление для {deps.pwa_type}
```typescript
export class {deps.pwa_type.title()}WakeLockController {{
  private wakeLockManager = new WakeLockManager();
  private autoMode = false;

  constructor() {{
    this.setupEventListeners();
  }}

  private setupEventListeners(): void {{
    // Повторно запрашиваем wake lock при возврате в приложение
    document.addEventListener('visibilitychange', async () => {{
      if (!document.hidden && this.autoMode) {{
        await this.wakeLockManager.reacquire();
      }}
    }});

    // Освобождаем при переходе в background
    window.addEventListener('beforeunload', () => {{
      this.wakeLockManager.release();
    }});

    {_get_wake_lock_specific_listeners(deps.pwa_type)}
  }}

  async enableAutoMode(): Promise<boolean> {{
    this.autoMode = true;
    return await this.wakeLockManager.request();
  }}

  async disableAutoMode(): Promise<boolean> {{
    this.autoMode = false;
    return await this.wakeLockManager.release();
  }}

  async toggle(): Promise<boolean> {{
    if (this.wakeLockManager.isLockActive()) {{
      return await this.disableAutoMode();
    }} else {{
      return await this.enableAutoMode();
    }}
  }}

  isActive(): boolean {{
    return this.wakeLockManager.isLockActive();
  }}
}}
```

### React Hook для Wake Lock
```typescript
export function useWakeLock() {{
  const [controller] = useState(() => new {deps.pwa_type.title()}WakeLockController());
  const [isActive, setIsActive] = useState(false);
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {{
    setIsSupported(isWakeLockSupported());

    const checkStatus = () => {{
      setIsActive(controller.isActive());
    }};

    // Проверяем статус периодически
    const interval = setInterval(checkStatus, 1000);

    return () => {{
      clearInterval(interval);
      controller.disableAutoMode();
    }};
  }}, [controller]);

  const enable = useCallback(async () => {{
    const success = await controller.enableAutoMode();
    setIsActive(controller.isActive());
    return success;
  }}, [controller]);

  const disable = useCallback(async () => {{
    const success = await controller.disableAutoMode();
    setIsActive(controller.isActive());
    return success;
  }}, [controller]);

  const toggle = useCallback(async () => {{
    const success = await controller.toggle();
    setIsActive(controller.isActive());
    return success;
  }}, [controller]);

  return {{
    isActive,
    isSupported,
    enable,
    disable,
    toggle
  }};
}}
```

### UI компонент для управления
```typescript
export function WakeLockToggle() {{
  const {{ isActive, isSupported, toggle }} = useWakeLock();

  if (!isSupported) {{
    return null;
  }}

  return (
    <button
      onClick={{toggle}}
      className={{`px-4 py-2 rounded-lg transition-colors ${{
        isActive
          ? 'bg-green-600 text-white'
          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
      }}`}}
      aria-label={{isActive ? 'Отключить блокировку экрана' : 'Включить блокировку экрана'}}
    >
      {{isActive ? '🔒 Экран не засыпает' : '💤 Разрешить засыпание'}}
    </button>
  );
}}
```

**Применение для {deps.pwa_type}:**
{_get_wake_lock_use_cases_for_type(deps.pwa_type)}

**Поддержка браузеров:**
- Chrome/Edge 84+
- Safari: не поддерживается
- Firefox Android: частично

**Важные моменты:**
- Работает только при активном документе
- Автоматически освобождается при переходе в background
- Влияет на время работы батареи
- Требует HTTPS и user activation
"""


async def implement_idle_detection_api(
    ctx: RunContext[PWAMobileAgentDependencies],
    threshold_minutes: int = 5
) -> str:
    """
    Реализует Idle Detection API для определения неактивности пользователя.

    Args:
        threshold_minutes: Порог неактивности в минутах

    Returns:
        Код для работы с Idle Detection API
    """
    deps = ctx.deps

    return f"""
## Idle Detection API для {deps.pwa_type} PWA

### Проверка поддержки
```typescript
function isIdleDetectionSupported(): boolean {{
  return 'IdleDetector' in window;
}}
```

### Idle Detection Manager
```typescript
class IdleDetectionManager {{
  private detector: IdleDetector | null = null;
  private isActive = false;
  private callbacks: {{
    onIdle: Array<() => void>;
    onActive: Array<() => void>;
  }} = {{
    onIdle: [],
    onActive: []
  }};

  constructor(private thresholdMs: number = {threshold_minutes * 60 * 1000}) {{}}

  async start(): Promise<boolean> {{
    try {{
      if (!isIdleDetectionSupported()) {{
        console.warn('Idle Detection API not supported, using fallback');
        return this.startFallbackDetection();
      }}

      // Запрашиваем разрешение
      const permission = await navigator.permissions.query({{
        name: 'idle-detection' as PermissionName
      }});

      if (permission.state !== 'granted') {{
        console.warn('Idle detection permission not granted');
        return this.startFallbackDetection();
      }}

      this.detector = new IdleDetector();

      this.detector.addEventListener('change', () => {{
        const userState = this.detector?.userState;
        const screenState = this.detector?.screenState;

        if (userState === 'idle' || screenState === 'locked') {{
          this.onIdleDetected();
        }} else if (userState === 'active' && screenState === 'unlocked') {{
          this.onActiveDetected();
        }}
      }});

      await this.detector.start({{
        threshold: this.thresholdMs,
        signal: new AbortController().signal
      }});

      this.isActive = true;
      console.log('Idle detection started');
      return true;
    }} catch (error) {{
      console.error('Idle detection start failed:', error);
      return this.startFallbackDetection();
    }}
  }}

  async stop(): Promise<void> {{
    if (this.detector) {{
      this.detector = null;
    }}
    this.isActive = false;
    this.stopFallbackDetection();
  }}

  onIdle(callback: () => void): void {{
    this.callbacks.onIdle.push(callback);
  }}

  onActive(callback: () => void): void {{
    this.callbacks.onActive.push(callback);
  }}

  private onIdleDetected(): void {{
    console.log('User is idle');
    this.callbacks.onIdle.forEach(cb => cb());
  }}

  private onActiveDetected(): void {{
    console.log('User is active');
    this.callbacks.onActive.forEach(cb => cb());
  }}

  // Fallback реализация для браузеров без поддержки
  private fallbackTimeout: NodeJS.Timeout | null = null;
  private fallbackIsIdle = false;

  private startFallbackDetection(): boolean {{
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];

    const resetTimer = () => {{
      if (this.fallbackTimeout) {{
        clearTimeout(this.fallbackTimeout);
      }}

      if (this.fallbackIsIdle) {{
        this.fallbackIsIdle = false;
        this.onActiveDetected();
      }}

      this.fallbackTimeout = setTimeout(() => {{
        this.fallbackIsIdle = true;
        this.onIdleDetected();
      }}, this.thresholdMs);
    }};

    events.forEach(event => {{
      document.addEventListener(event, resetTimer, true);
    }});

    resetTimer(); // Запускаем таймер
    this.isActive = true;

    return true;
  }}

  private stopFallbackDetection(): void {{
    if (this.fallbackTimeout) {{
      clearTimeout(this.fallbackTimeout);
      this.fallbackTimeout = null;
    }}
  }}
}}
```

### Специализированный контроллер для {deps.pwa_type}
```typescript
export class {deps.pwa_type.title()}IdleController {{
  private idleManager = new IdleDetectionManager({threshold_minutes * 60 * 1000});
  private isIdle = false;

  constructor() {{
    this.setupIdleHandlers();
  }}

  private setupIdleHandlers(): void {{
    this.idleManager.onIdle(() => {{
      this.isIdle = true;
      this.handleIdle();
    }});

    this.idleManager.onActive(() => {{
      this.isIdle = false;
      this.handleActive();
    }});
  }}

  private handleIdle(): void {{
    console.log('{deps.pwa_type} app detected idle state');

    {_get_idle_handling_for_type(deps.pwa_type)}
  }}

  private handleActive(): void {{
    console.log('{deps.pwa_type} app detected active state');

    {_get_active_handling_for_type(deps.pwa_type)}
  }}

  async start(): Promise<boolean> {{
    return await this.idleManager.start();
  }}

  async stop(): Promise<void> {{
    await this.idleManager.stop();
  }}

  getIdleState(): boolean {{
    return this.isIdle;
  }}
}}
```

### React Hook для Idle Detection
```typescript
export function useIdleDetection(thresholdMinutes: number = {threshold_minutes}) {{
  const [controller] = useState(() => new {deps.pwa_type.title()}IdleController());
  const [isIdle, setIsIdle] = useState(false);
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {{
    setIsSupported(isIdleDetectionSupported());

    const startDetection = async () => {{
      await controller.start();
    }};

    startDetection();

    const checkIdleState = () => {{
      setIsIdle(controller.getIdleState());
    }};

    const interval = setInterval(checkIdleState, 1000);

    return () => {{
      clearInterval(interval);
      controller.stop();
    }};
  }}, [controller]);

  return {{
    isIdle,
    isSupported
  }};
}}
```

### Battery Optimization Integration
```typescript
export class BatteryOptimizedIdleManager {{
  private idleController = new {deps.pwa_type.title()}IdleController();
  private batteryManager: any = null;

  async init(): Promise<void> {{
    // Получаем информацию о батарее
    if ('getBattery' in navigator) {{
      this.batteryManager = await (navigator as any).getBattery();
    }}

    await this.idleController.start();
  }}

  private shouldOptimizeForBattery(): boolean {{
    if (!this.batteryManager) return false;

    return (
      !this.batteryManager.charging &&
      this.batteryManager.level < 0.2 // Батарея меньше 20%
    );
  }}

  optimizeForLowBattery(): void {{
    if (this.shouldOptimizeForBattery()) {{
      // Уменьшаем активность фоновых процессов
      console.log('Optimizing for low battery during idle');

      // Останавливаем ненужные анимации
      document.body.classList.add('low-battery-mode');

      // Уменьшаем частоту синхронизации
      // ... дополнительные оптимизации
    }}
  }}
}}
```

**Применение для {deps.pwa_type}:**
{_get_idle_use_cases_for_type(deps.pwa_type)}

**Поддержка браузеров:**
- Chrome/Edge 94+ (за флагом)
- Safari: не поддерживается
- Firefox: в разработке

**Требования:**
- HTTPS обязателен
- Permissions API required
- User activation необходим
- Fallback реализация рекомендуется
"""


async def implement_web_locks_api(
    ctx: RunContext[PWAMobileAgentDependencies],
    lock_scope: str = "document"
) -> str:
    """
    Реализует Web Locks API для координации между tabs и workers.

    Args:
        lock_scope: Область действия блокировки

    Returns:
        Код для работы с Web Locks API
    """
    deps = ctx.deps

    if deps.pwa_type not in ["productivity", "general"]:
        return f"⚠️ Web Locks API наиболее полезен для productivity приложений. Текущий тип: {deps.pwa_type}"

    return f"""
## Web Locks API для {deps.pwa_type} PWA

### Проверка поддержки
```typescript
function isWebLocksSupported(): boolean {{
  return 'locks' in navigator;
}}
```

### Базовый Lock Manager
```typescript
class WebLockManager {{
  private activeLocks = new Set<string>();

  async acquireLock<T>(
    lockName: string,
    callback: () => Promise<T>,
    options?: LockOptions
  ): Promise<T | null> {{
    try {{
      if (!isWebLocksSupported()) {{
        console.warn('Web Locks API not supported, executing without lock');
        return await callback();
      }}

      return await navigator.locks.request(lockName, options, async (lock) => {{
        if (!lock) {{
          console.warn(`Failed to acquire lock: ${{lockName}}`);
          return null;
        }}

        this.activeLocks.add(lockName);
        console.log(`Lock acquired: ${{lockName}}`);

        try {{
          const result = await callback();
          return result;
        }} finally {{
          this.activeLocks.delete(lockName);
          console.log(`Lock released: ${{lockName}}`);
        }}
      }});
    }} catch (error) {{
      console.error(`Lock operation failed for ${{lockName}}:`, error);
      return null;
    }}
  }}

  async queryLocks(): Promise<LockManagerSnapshot | null> {{
    try {{
      if (!isWebLocksSupported()) {{
        return null;
      }}

      return await navigator.locks.query();
    }} catch (error) {{
      console.error('Lock query failed:', error);
      return null;
    }}
  }}

  getActiveLocks(): string[] {{
    return Array.from(this.activeLocks);
  }}
}}
```

### Document Lock Manager для {deps.pwa_type}
```typescript
export class {deps.pwa_type.title()}DocumentLockManager {{
  private lockManager = new WebLockManager();
  private readonly EDIT_LOCK_PREFIX = '{deps.pwa_type}-edit-';
  private readonly SYNC_LOCK_PREFIX = '{deps.pwa_type}-sync-';

  // Блокировка редактирования документа
  async withEditLock<T>(
    documentId: string,
    editCallback: () => Promise<T>
  ): Promise<T | null> {{
    const lockName = `${{this.EDIT_LOCK_PREFIX}}${{documentId}}`;

    return await this.lockManager.acquireLock(
      lockName,
      editCallback,
      {{
        mode: 'exclusive',
        ifAvailable: false // Ждем освобождения
      }}
    );
  }}

  // Блокировка синхронизации (может быть shared)
  async withSyncLock<T>(
    operation: () => Promise<T>,
    shared: boolean = false
  ): Promise<T | null> {{
    const lockName = `${{this.SYNC_LOCK_PREFIX}}general`;

    return await this.lockManager.acquireLock(
      lockName,
      operation,
      {{
        mode: shared ? 'shared' : 'exclusive',
        ifAvailable: false
      }}
    );
  }}

  // Попытка получить блокировку без ожидания
  async tryEditLock<T>(
    documentId: string,
    editCallback: () => Promise<T>
  ): Promise<T | null> {{
    const lockName = `${{this.EDIT_LOCK_PREFIX}}${{documentId}}`;

    return await this.lockManager.acquireLock(
      lockName,
      editCallback,
      {{
        mode: 'exclusive',
        ifAvailable: true // Не ждем, возвращаем null если занято
      }}
    );
  }}

  async getDocumentEditStatus(documentId: string): Promise<boolean> {{
    const snapshot = await this.lockManager.queryLocks();
    if (!snapshot) return false;

    const editLockName = `${{this.EDIT_LOCK_PREFIX}}${{documentId}}`;
    return snapshot.held.some(lock => lock.name === editLockName);
  }}

  async getAllActiveEdits(): Promise<string[]> {{
    const snapshot = await this.lockManager.queryLocks();
    if (!snapshot) return [];

    return snapshot.held
      .filter(lock => lock.name.startsWith(this.EDIT_LOCK_PREFIX))
      .map(lock => lock.name.replace(this.EDIT_LOCK_PREFIX, ''));
  }}
}}
```

### Concurrent Editing Protection
```typescript
export class ConcurrentEditingProtection {{
  private documentLockManager = new {deps.pwa_type.title()}DocumentLockManager();
  private editingSessions = new Map<string, Date>();

  async startEditing(documentId: string): Promise<boolean> {{
    try {{
      const result = await this.documentLockManager.tryEditLock(documentId, async () => {{
        // Проверяем не редактируется ли уже
        const isBeingEdited = await this.documentLockManager.getDocumentEditStatus(documentId);
        if (isBeingEdited) {{
          throw new Error('Document is being edited in another tab');
        }}

        this.editingSessions.set(documentId, new Date());
        return true;
      }});

      return result !== null;
    }} catch (error) {{
      console.error('Failed to start editing:', error);
      return false;
    }}
  }}

  async saveChanges(documentId: string, saveCallback: () => Promise<void>): Promise<boolean> {{
    try {{
      const result = await this.documentLockManager.withEditLock(documentId, async () => {{
        await saveCallback();

        // Обновляем timestamp последнего сохранения
        this.editingSessions.set(documentId, new Date());

        return true;
      }});

      return result !== null;
    }} catch (error) {{
      console.error('Failed to save changes:', error);
      return false;
    }}
  }}

  async finishEditing(documentId: string): Promise<void> {{
    this.editingSessions.delete(documentId);
    // Lock автоматически освобождается когда выходим из области видимости
  }}

  isCurrentlyEditing(documentId: string): boolean {{
    return this.editingSessions.has(documentId);
  }}

  getEditingStartTime(documentId: string): Date | null {{
    return this.editingSessions.get(documentId) || null;
  }}
}}
```

### React Hook для Document Locking
```typescript
export function useDocumentLock(documentId: string) {{
  const [protectionManager] = useState(() => new ConcurrentEditingProtection());
  const [isEditing, setIsEditing] = useState(false);
  const [isLocked, setIsLocked] = useState(false);
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {{
    setIsSupported(isWebLocksSupported());
  }}, []);

  const startEditing = useCallback(async () => {{
    const success = await protectionManager.startEditing(documentId);
    if (success) {{
      setIsEditing(true);
      setIsLocked(true);
    }}
    return success;
  }}, [protectionManager, documentId]);

  const saveChanges = useCallback(async (saveCallback: () => Promise<void>) => {{
    return await protectionManager.saveChanges(documentId, saveCallback);
  }}, [protectionManager, documentId]);

  const finishEditing = useCallback(async () => {{
    await protectionManager.finishEditing(documentId);
    setIsEditing(false);
    setIsLocked(false);
  }}, [protectionManager, documentId]);

  // Автоматически завершаем редактирование при unmount
  useEffect(() => {{
    return () => {{
      if (isEditing) {{
        protectionManager.finishEditing(documentId);
      }}
    }};
  }}, [isEditing, protectionManager, documentId]);

  return {{
    isEditing,
    isLocked,
    isSupported,
    startEditing,
    saveChanges,
    finishEditing
  }};
}}
```

### Multi-tab Coordination Example
```typescript
export class MultiTabCoordinator {{
  private lockManager = new {deps.pwa_type.title()}DocumentLockManager();

  async coordinatedDataSync(): Promise<void> {{
    await this.lockManager.withSyncLock(async () => {{
      console.log('Starting coordinated sync across tabs');

      // Только один tab будет выполнять синхронизацию
      const lastSync = localStorage.getItem('{deps.pwa_type}-last-sync');
      const now = Date.now();

      if (!lastSync || now - parseInt(lastSync) > 5 * 60 * 1000) {{ // 5 минут
        console.log('Performing actual sync');
        await this.performDataSync();
        localStorage.setItem('{deps.pwa_type}-last-sync', now.toString());
      }} else {{
        console.log('Sync recently performed by another tab');
      }}
    }}, false); // exclusive lock
  }}

  private async performDataSync(): Promise<void> {{
    // Реальная синхронизация данных
    // ...
  }}
}}
```

**Применение для {deps.pwa_type}:**
{_get_web_locks_use_cases_for_type(deps.pwa_type)}

**Поддержка браузеров:**
- Chrome/Edge 69+
- Safari 15.4+
- Firefox 96+

**Преимущества:**
- Предотвращение race conditions
- Координация между tabs/workers
- Atomic operations
- Deadlock detection встроен
"""


async def search_agent_knowledge(
    ctx: RunContext[PWAMobileAgentDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в специализированной базе знаний PWA Mobile Agent через Archon RAG.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    # Используем теги для фильтрации по знаниям агента
    search_tags = ctx.deps.knowledge_tags
    knowledge_domain = ctx.deps.knowledge_domain

    try:
        # Формируем улучшенный запрос с тегами
        enhanced_query = f"{query} {' '.join(search_tags)}"

        # Реальный вызов Archon RAG через MCP
        from ..mcp_client import mcp_archon_rag_search_knowledge_base

        result = await mcp_archon_rag_search_knowledge_base(
            query=enhanced_query,
            source_domain=knowledge_domain if knowledge_domain else None,
            match_count=match_count
        )

        if result.get("success") and result.get("results"):
            # Форматируем результаты для агента
            knowledge_items = []
            for idx, item in enumerate(result["results"], 1):
                title = item.get("metadata", {}).get("title", "")
                content = item.get("content", "")
                relevance = item.get("metadata", {}).get("relevance", 0)

                knowledge_items.append(
                    f"**{idx}. {title}** (релевантность: {relevance:.0%})\n{content}"
                )

            return f"""
📚 **База знаний PWA Mobile Agent**

🔍 Запрос: "{query}"
🏷️ Теги: {', '.join(search_tags)}
📊 Найдено: {len(result['results'])} результатов

{chr(10).join(knowledge_items)}

💡 **Применение для {ctx.deps.pwa_type} PWA:**
{_get_knowledge_application_hints(ctx.deps.pwa_type, query)}
"""
        else:
            # Fallback если база знаний недоступна
            return f"""
⚠️ База знаний временно недоступна.

**Рекомендации для {ctx.deps.pwa_type} PWA:**
{_get_fallback_recommendations(ctx.deps.pwa_type, query)}

Попробуйте позже или используйте локальные паттерны.
"""

    except Exception as e:
        return f"""
❌ Ошибка доступа к базе знаний: {e}

**Локальные рекомендации для {ctx.deps.pwa_type}:**
{_get_fallback_recommendations(ctx.deps.pwa_type, query)}
"""


def _get_knowledge_application_hints(pwa_type: str, query: str) -> str:
    """Получить подсказки по применению знаний для типа PWA."""
    hints = {
        "ecommerce": "Фокус на быстрой загрузке каталога, offline корзине, payment API",
        "media": "Приоритет offline чтению, progressive loading, share capabilities",
        "productivity": "Важна синхронизация данных, conflict resolution, offline editing",
        "social": "Real-time updates, push notifications, media handling",
        "gaming": "Performance optimization, asset caching, offline gameplay"
    }
    return hints.get(pwa_type, "Универсальные PWA best practices")


def _get_fallback_recommendations(pwa_type: str, query: str) -> str:
    """Получить fallback рекомендации при недоступности RAG."""
    query_lower = query.lower()

    recommendations = []

    if "cache" in query_lower or "offline" in query_lower:
        recommendations.append("- Cache-first strategy для статического контента")
        recommendations.append("- Network-first для динамических данных")
        recommendations.append("- IndexedDB для structured offline storage")

    if "performance" in query_lower:
        recommendations.append("- Lazy loading для изображений и компонентов")
        recommendations.append("- Code splitting для оптимального bundle size")
        recommendations.append("- Service Worker precaching критических ресурсов")

    if "security" in query_lower:
        recommendations.append("- CSP headers для защиты от XSS")
        recommendations.append("- HTTPS обязателен для PWA")
        recommendations.append("- Secure contexts для sensitive APIs")

    return "\n".join(recommendations) if recommendations else "Используйте стандартные PWA паттерны"


# Helper функции для генерации кода

def _generate_icon_set() -> List[Dict[str, Any]]:
    """Генерирует универсальный набор иконок для PWA."""
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    icons = []

    for size in sizes:
        icon = {
            "src": f"/icons/icon-{size}x{size}.png",
            "sizes": f"{size}x{size}",
            "type": "image/png"
        }

        # Добавляем purpose для ключевых размеров
        if size == 192:
            icon["purpose"] = "maskable"
        elif size == 144:
            icon["purpose"] = "any"

        icons.append(icon)

    return icons


def _generate_screenshots(pwa_type: str) -> List[Dict[str, Any]]:
    """Генерирует screenshots для store listing."""
    screenshots = [
        {
            "src": "/screenshots/mobile-home.png",
            "sizes": "1080x1920",
            "type": "image/png",
            "platform": "narrow",
            "label": "Главный экран"
        }
    ]

    # Добавляем специфичные для типа screenshots
    type_specific = {
        "ecommerce": [
            {"label": "Каталог товаров", "src": "/screenshots/mobile-catalog.png"},
            {"label": "Корзина", "src": "/screenshots/mobile-cart.png"}
        ],
        "media": [
            {"label": "Список статей", "src": "/screenshots/mobile-articles.png"},
            {"label": "Читалка", "src": "/screenshots/mobile-reader.png"}
        ],
        "productivity": [
            {"label": "Рабочие задачи", "src": "/screenshots/mobile-tasks.png"},
            {"label": "Редактор", "src": "/screenshots/mobile-editor.png"}
        ]
    }

    if pwa_type in type_specific:
        for additional in type_specific[pwa_type]:
            screenshots.append({
                "src": additional["src"],
                "sizes": "1080x1920",
                "type": "image/png",
                "platform": "narrow",
                "label": additional["label"]
            })

    return screenshots


def _get_type_specific_manifest_config(deps: PWAMobileAgentDependencies) -> Dict[str, Any]:
    """Получает специфичные для типа PWA настройки манифеста."""
    config = {}

    # Share target для социальных и медиа приложений
    if deps.pwa_type in ["social", "media"] and deps.enable_share_api:
        config["share_target"] = {
            "action": "/share",
            "method": "POST",
            "enctype": "multipart/form-data",
            "params": {
                "title": "title",
                "text": "text",
                "url": "url"
            }
        }

    # Shortcuts для разных типов приложений
    shortcuts_map = {
        "ecommerce": [
            {"name": "Каталог", "url": "/catalog", "icons": [{"src": "/icons/catalog.png", "sizes": "96x96"}]},
            {"name": "Корзина", "url": "/cart", "icons": [{"src": "/icons/cart.png", "sizes": "96x96"}]}
        ],
        "productivity": [
            {"name": "Новая задача", "url": "/tasks/new", "icons": [{"src": "/icons/add.png", "sizes": "96x96"}]},
            {"name": "Календарь", "url": "/calendar", "icons": [{"src": "/icons/calendar.png", "sizes": "96x96"}]}
        ],
        "media": [
            {"name": "Читать", "url": "/articles", "icons": [{"src": "/icons/read.png", "sizes": "96x96"}]},
            {"name": "Избранное", "url": "/favorites", "icons": [{"src": "/icons/favorite.png", "sizes": "96x96"}]}
        ]
    }

    if deps.pwa_type in shortcuts_map:
        config["shortcuts"] = shortcuts_map[deps.pwa_type]

    return config


def _get_manifest_features_description(pwa_type: str) -> str:
    """Возвращает описание ключевых особенностей манифеста для типа PWA."""
    descriptions = {
        "ecommerce": "- Share target для товаров\n- Shortcuts для каталога и корзины\n- Shopping категория",
        "media": "- Share target для статей\n- Entertainment категория\n- Портретная ориентация",
        "productivity": "- Shortcuts для создания задач\n- Minimal UI для фокуса\n- Business категория",
        "social": "- Share target и camera API\n- Social категория\n- Portrait ориентация",
        "gaming": "- Fullscreen display mode\n- Landscape ориентация\n- Games категория"
    }
    return descriptions.get(pwa_type, "- Универсальные PWA настройки\n- Adaptive для любого контента")


def _generate_service_worker_code(deps: PWAMobileAgentDependencies, additional_strategies: str) -> str:
    """Генерирует код Service Worker для типа PWA."""
    return f"""
import {{ precacheAndRoute }} from 'workbox-precaching';
import {{ registerRoute }} from 'workbox-routing';
import {{ StaleWhileRevalidate, CacheFirst, NetworkFirst }} from 'workbox-strategies';
import {{ ExpirationPlugin }} from 'workbox-expiration';
import {{ CacheableResponsePlugin }} from 'workbox-cacheable-response';
import {{ BackgroundSyncPlugin }} from 'workbox-background-sync';

// Precache static assets
precacheAndRoute(self.__WB_MANIFEST);

// {deps.pwa_type.upper()} PWA specific caching strategies

// API calls - {deps.offline_strategy}
registerRoute(
  ({{ url }}) => url.pathname.startsWith('/api/'),
  new {_get_strategy_class(deps.offline_strategy)}({{
    cacheName: 'api-cache',
    networkTimeoutSeconds: 5,
    plugins: [
      new CacheableResponsePlugin({{
        statuses: [0, 200]
      }}),
      new ExpirationPlugin({{
        maxEntries: 50,
        maxAgeSeconds: {_get_cache_duration(deps.pwa_type)}
      }})
    ]
  }})
);

// Images - Cache First for {deps.pwa_type}
registerRoute(
  ({{ request }}) => request.destination === 'image',
  new CacheFirst({{
    cacheName: 'image-cache',
    plugins: [
      new ExpirationPlugin({{
        maxEntries: {_get_image_cache_size(deps.pwa_type)},
        maxAgeSeconds: {_get_image_cache_duration(deps.pwa_type)},
        purgeOnQuotaError: true
      }})
    ]
  }})
);

{_get_type_specific_caching(deps.pwa_type)}

{_get_background_sync_code(deps) if deps.enable_background_sync else ""}

{_get_push_notification_code(deps) if deps.enable_push_notifications else ""}
"""


def _get_strategy_class(strategy: str) -> str:
    """Возвращает класс стратегии Workbox."""
    strategy_map = {
        "network-first": "NetworkFirst",
        "cache-first": "CacheFirst",
        "stale-while-revalidate": "StaleWhileRevalidate"
    }
    return strategy_map.get(strategy, "NetworkFirst")


def _get_cache_duration(pwa_type: str) -> int:
    """Возвращает длительность кэширования в секундах для типа PWA."""
    durations = {
        "ecommerce": 60 * 60 * 2,  # 2 hours - быстро меняющиеся цены
        "media": 60 * 60 * 24,     # 24 hours - статьи обновляются реже
        "productivity": 60 * 60,    # 1 hour - часто меняющиеся данные
        "social": 60 * 30,          # 30 minutes - real-time контент
        "gaming": 60 * 60 * 24 * 7  # 1 week - игровой контент стабильный
    }
    return durations.get(pwa_type, 60 * 60 * 24)  # По умолчанию 24 часа


def _get_image_cache_size(pwa_type: str) -> int:
    """Возвращает размер кэша изображений для типа PWA."""
    sizes = {
        "ecommerce": 200,    # Много товарных фото
        "media": 300,        # Статьи с изображениями
        "productivity": 50,  # Минимум изображений
        "social": 500,       # Много пользовательского контента
        "gaming": 100        # Игровые ассеты
    }
    return sizes.get(pwa_type, 100)


def _get_image_cache_duration(pwa_type: str) -> int:
    """Возвращает длительность кэширования изображений."""
    return 60 * 60 * 24 * 30  # 30 дней для всех типов


def _get_type_specific_caching(pwa_type: str) -> str:
    """Возвращает специфичные для типа PWA стратегии кэширования."""
    strategies = {
        "ecommerce": """
// Product data - короткий кэш из-за изменений цен
registerRoute(
  /\\/api\\/products/,
  new NetworkFirst({
    cacheName: 'products-cache',
    networkTimeoutSeconds: 3,
    plugins: [
      new ExpirationPlugin({
        maxAgeSeconds: 60 * 60 * 2 // 2 hours
      })
    ]
  })
);""",
        "media": """
// Articles - длинный кэш, контент стабильный
registerRoute(
  /\\/api\\/articles/,
  new StaleWhileRevalidate({
    cacheName: 'articles-cache',
    plugins: [
      new ExpirationPlugin({
        maxAgeSeconds: 60 * 60 * 24 * 7 // 1 week
      })
    ]
  })
);""",
        "productivity": """
// User data - быстрая синхронизация
registerRoute(
  /\\/api\\/tasks|notes|calendar/,
  new NetworkFirst({
    cacheName: 'user-data-cache',
    networkTimeoutSeconds: 2,
    plugins: [
      new ExpirationPlugin({
        maxAgeSeconds: 60 * 60 // 1 hour
      })
    ]
  })
);"""
    }
    return strategies.get(pwa_type, "// Generic caching strategies")


def _get_background_sync_code(deps: PWAMobileAgentDependencies) -> str:
    """Генерирует код background sync для типа PWA."""
    return f"""
// Background Sync for {deps.pwa_type}
const bgSyncPlugin = new BackgroundSyncPlugin('{deps.pwa_type}-queue', {{
  maxRetentionTime: 24 * 60 // Retry for 24 hours
}});

registerRoute(
  /\\/api\\/(create|update|delete)/,
  new NetworkFirst({{
    plugins: [bgSyncPlugin]
  }}),
  'POST'
);
"""


def _get_push_notification_code(deps: PWAMobileAgentDependencies) -> str:
    """Генерирует код push notifications для типа PWA."""
    return f"""
// Push Notifications for {deps.pwa_type}
self.addEventListener('push', (event) => {{
  const data = event.data?.json() ?? {{}};
  const options = {{
    body: data.body,
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    vibrate: [200, 100, 200],
    data: {{ url: data.url, id: data.id }},
    actions: {_get_notification_actions(deps.pwa_type)}
  }};

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
}});

self.addEventListener('notificationclick', (event) => {{
  event.notification.close();

  if (event.action === 'view') {{
    event.waitUntil(clients.openWindow(event.notification.data.url));
  }}
}});
"""


def _get_notification_actions(pwa_type: str) -> str:
    """Возвращает действия для push notifications по типу PWA."""
    actions = {
        "ecommerce": '[{"action": "view", "title": "View Product"}, {"action": "cart", "title": "Add to Cart"}]',
        "media": '[{"action": "read", "title": "Read Article"}, {"action": "save", "title": "Save for Later"}]',
        "productivity": '[{"action": "open", "title": "Open Task"}, {"action": "complete", "title": "Mark Complete"}]',
        "social": '[{"action": "view", "title": "View Post"}, {"action": "reply", "title": "Reply"}]'
    }
    return actions.get(pwa_type, '[{"action": "view", "title": "View"}, {"action": "dismiss", "title": "Dismiss"}]')


def _get_caching_strategies_description(config: Dict[str, Any]) -> str:
    """Возвращает описание настроенных стратегий кэширования."""
    return f"""
- **Основная стратегия**: {config['offline_strategy']}
- **Размер кэша**: максимум {config['max_cache_size_mb']} MB
- **Push notifications**: {'включены' if config['enable_push'] else 'отключены'}
- **Background sync**: {'включен' if config['enable_background_sync'] else 'отключен'}
- **Оптимизировано для**: {config['pwa_type']} приложений
"""


def _get_additional_features_description(deps: PWAMobileAgentDependencies) -> str:
    """Возвращает описание дополнительных возможностей PWA."""
    features = []
    if deps.enable_push_notifications:
        features.append("🔔 Push notifications")
    if deps.enable_background_sync:
        features.append("🔄 Background sync")
    if deps.enable_geolocation:
        features.append("📍 Geolocation")
    if deps.enable_camera:
        features.append("📸 Camera API")
    if deps.enable_share_api:
        features.append("📤 Share API")
    if deps.enable_payment_api:
        features.append("💳 Payment API")

    return "\n".join(f"- {feature}" for feature in features) if features else "- Базовая PWA функциональность"


def _generate_mobile_components(deps: PWAMobileAgentDependencies, component_type: str) -> str:
    """Генерирует мобильные компоненты для типа PWA."""
    # Здесь будет генерация React компонентов для мобильных интерфейсов
    return f"""
## Мобильные компоненты для {deps.pwa_type}

### Touch-Optimized Button
```tsx
interface TouchButtonProps {{
  onTap: () => void;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
}}

export function TouchButton({{ onTap, children, variant = 'primary' }}: TouchButtonProps) {{
  return (
    <button
      className="min-h-[44px] min-w-[44px] px-4 py-2 rounded-lg font-medium
                 active:scale-95 transition-transform duration-100
                 {{variant === 'primary' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-900'}}"
      onTouchStart={{() => hapticFeedback()}}
      onClick={{onTap}}
    >
      {{children}}
    </button>
  );
}}
```

### Swipeable Cards (для {deps.pwa_type})
```tsx
import {{ useSwipeable }} from 'react-swipeable';

export function SwipeableCards({{ items, onSwipe }}) {{
  const handlers = useSwipeable({{
    onSwipedLeft: () => onSwipe('left'),
    onSwipedRight: () => onSwipe('right'),
    preventDefaultTouchmoveEvent: true,
    trackMouse: true
  }});

  return (
    <div {{...handlers}} className="overflow-hidden rounded-lg">
      {{/* {deps.pwa_type} specific content */}}
    </div>
  );
}}
```

### Pull to Refresh
```tsx
export function PullToRefresh({{ onRefresh, children }}) {{
  // Implementation specific to {deps.pwa_type} data refreshing
  return (
    <div className="relative">
      {{/* Pull to refresh implementation */}}
      {{children}}
    </div>
  );
}}
```
"""


def _generate_performance_recommendations(deps: PWAMobileAgentDependencies, focus: str) -> str:
    """Генерирует рекомендации по производительности."""
    return f"""
## Performance анализ для {deps.pwa_type} PWA

### Основные метрики
- **Загрузка**: оптимизировано для {deps.cache_strategy} кэширования
- **Интерактивность**: touch targets ≥ 44px
- **Визуальная стабильность**: lazy loading изображений

### Рекомендации для {deps.pwa_type}:

**Bundle optimization:**
- Tree shaking неиспользуемого кода
- Code splitting по роутам
- Dynamic imports для тяжелых библиотек

**Image optimization:**
- WebP/AVIF форматы с fallback
- Responsive images с srcset
- {'Aggressive' if deps.pwa_type in ['media', 'ecommerce'] else 'Conservative'} lazy loading

**Runtime performance:**
- Virtual scrolling для длинных списков
- Debounced search (300ms)
- Optimistic UI updates
- Background data fetching

**Network optimization:**
- Service Worker precaching
- HTTP/2 server push для критических ресурсов
- CDN для статических ассетов
- Compression (gzip/brotli)

### Mobile-specific optimizations:
- Reduced motion для accessibility
- Battery usage optimization
- Memory management для старых устройств
- Network-aware loading (2G/3G/4G)
"""


def _get_badging_implementation_for_type(pwa_type: str) -> str:
    """Возвращает специфичную реализацию badge для типа PWA."""
    implementations = {
        "ecommerce": """
// E-commerce specific badge management
export class EcommerceBadgeManager extends EcommerceBadgeManager {
  async updateCartBadge(cartItems: number): Promise<void> {
    await this.setCount(cartItems);
  }

  async updateOrdersBadge(pendingOrders: number): Promise<void> {
    await this.setCount(pendingOrders);
  }

  async updateWishlistBadge(wishlistItems: number): Promise<void> {
    // Используем флаг для wishlist
    if (wishlistItems > 0) {
      await setAppBadge();
    } else {
      await clearAppBadge();
    }
  }
}""",
        "social": """
// Social media specific badge management
export class SocialBadgeManager extends SocialBadgeManager {
  async updateNotificationsBadge(unreadCount: number): Promise<void> {
    await this.setCount(unreadCount);
  }

  async updateMessagesBadge(unreadMessages: number): Promise<void> {
    await this.setCount(unreadMessages);
  }

  async updateFriendRequestsBadge(pendingRequests: number): Promise<void> {
    await this.setCount(pendingRequests);
  }
}""",
        "productivity": """
// Productivity specific badge management
export class ProductivityBadgeManager extends ProductivityBadgeManager {
  async updateTasksBadge(overdueTasks: number): Promise<void> {
    await this.setCount(overdueTasks);
  }

  async updateMeetingsBadge(upcomingMeetings: number): Promise<void> {
    await this.setCount(upcomingMeetings);
  }

  async updateEmailBadge(unreadEmails: number): Promise<void> {
    await this.setCount(unreadEmails);
  }
}"""
    }
    return implementations.get(pwa_type, "// Generic badge implementation")


def _get_badging_use_cases_for_type(pwa_type: str) -> str:
    """Возвращает случаи использования Badging API для типа PWA."""
    use_cases = {
        "ecommerce": """
- Количество товаров в корзине
- Новые заказы для продавцов
- Wishlist updates
- Sales notifications
- Inventory alerts""",
        "social": """
- Непрочитанные сообщения
- Friend requests
- Новые лайки/комментарии
- Mentions и replies
- Live stream notifications""",
        "productivity": """
- Просроченные задачи
- Календарные напоминания
- Непрочитанные email
- Collaborative document updates
- Project deadlines""",
        "media": """
- Новые статьи
- Video upload progress
- Subscription updates
- Reading progress
- Download completions""",
        "gaming": """
- Achievement unlocks
- Tournament updates
- Friend invitations
- Daily rewards
- Leaderboard changes"""
    }
    return use_cases.get(pwa_type, "- General notification counts\n- Status updates\n- Activity indicators")


def _get_wake_lock_specific_listeners(pwa_type: str) -> str:
    """Возвращает специфичные слушатели для Wake Lock API."""
    listeners = {
        "gaming": """
    // Gaming-specific listeners
    document.addEventListener('fullscreenchange', async () => {
      if (document.fullscreenElement) {
        await this.wakeLockManager.request();
      } else {
        await this.wakeLockManager.release();
      }
    });

    // Game pause/resume
    window.addEventListener('blur', () => {
      this.wakeLockManager.release();
    });

    window.addEventListener('focus', async () => {
      if (this.autoMode) {
        await this.wakeLockManager.request();
      }
    });""",
        "media": """
    // Media-specific listeners
    document.addEventListener('play', async (e) => {
      if (e.target instanceof HTMLVideoElement && this.autoMode) {
        await this.wakeLockManager.request();
      }
    });

    document.addEventListener('pause', async (e) => {
      if (e.target instanceof HTMLVideoElement) {
        await this.wakeLockManager.release();
      }
    });

    // Reading mode detection
    let readingMode = false;
    document.addEventListener('scroll', () => {
      if (readingMode && this.autoMode) {
        this.wakeLockManager.reacquire();
      }
    });"""
    }
    return listeners.get(pwa_type, "// Generic event listeners")


def _get_wake_lock_use_cases_for_type(pwa_type: str) -> str:
    """Возвращает случаи использования Wake Lock API для типа PWA."""
    use_cases = {
        "gaming": """
- Preventing screen dimming during gameplay
- Fullscreen gaming sessions
- Turn-based games waiting for player input
- Video game streaming
- AR/VR experiences""",
        "media": """
- Video/audio playback
- Reading long articles
- Slideshow presentations
- Live streaming viewing
- Digital magazine reading""",
        "general": """
- Document reading
- Presentation mode
- Data visualization dashboards
- Live monitoring systems
- Tutorial walkthroughs"""
    }
    return use_cases.get(pwa_type, "- General screen-on requirements\n- Long-form content consumption")


def _get_idle_handling_for_type(pwa_type: str) -> str:
    """Возвращает обработку idle состояния для типа PWA."""
    handlers = {
        "ecommerce": """
    // E-commerce idle handling
    // Сохраняем корзину
    this.saveCartToLocalStorage();

    // Приостанавливаем real-time updates цен
    this.pausePriceUpdates();

    // Уменьшаем частоту inventory checks
    this.reduceInventoryPolling();""",
        "productivity": """
    // Productivity idle handling
    // Автосохранение документов
    this.autoSaveDocuments();

    // Приостанавливаем collaborative updates
    this.pauseCollaborationSync();

    // Backup текущего состояния
    this.backupWorkSession();""",
        "social": """
    // Social idle handling
    // Показываем как "away"
    this.updatePresenceStatus('away');

    // Приостанавливаем typing indicators
    this.pauseTypingIndicators();

    // Уменьшаем частоту получения updates
    this.reduceFeedPolling();""",
        "media": """
    // Media idle handling
    // Приостанавливаем autoplay
    this.pauseAutoplay();

    // Сохраняем reading progress
    this.saveReadingProgress();

    // Уменьшаем preloading контента
    this.reduceContentPreloading();"""
    }
    return handlers.get(pwa_type, "// Generic idle handling")


async def implement_web_vitals_monitoring(
    ctx: RunContext[PWAMobileAgentDependencies],
    vitals_config: str = "all"
) -> str:
    """
    Реализует comprehensive Web Vitals мониторинг с real-time analytics.

    Args:
        vitals_config: Конфигурация мониторинга (all, core, extended, custom)

    Returns:
        Полная реализация Web Vitals мониторинга
    """
    deps = ctx.deps

    return f"""
## 🚀 Web Vitals Monitoring для {deps.pwa_type} PWA

### 📊 Core Web Vitals Implementation

```typescript
// web-vitals-monitor.ts
import {{getCLS, getFID, getLCP, getFCP, getTTFB, onINP}} from 'web-vitals';

interface VitalsData {{
  name: string;
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
  delta: number;
  id: string;
  navigationType: string;
  timestamp: number;
}}

interface VitalsConfig {{
  enableAnalytics: boolean;
  enableReporting: boolean;
  enableAdaptiveOptimization: boolean;
  sampleRate: number;
  debug: boolean;
  thresholds: {{
    lcp: {{ good: number; poor: number }};
    fid: {{ good: number; poor: number }};
    cls: {{ good: number; poor: number }};
    inp: {{ good: number; poor: number }};
  }};
}}

class WebVitalsMonitor {{
  private config: VitalsConfig;
  private vitalsData: Map<string, VitalsData[]> = new Map();
  private performanceObserver: PerformanceObserver | null = null;

  constructor(config: Partial<VitalsConfig> = {{}}) {{
    this.config = {{
      enableAnalytics: true,
      enableReporting: true,
      enableAdaptiveOptimization: {str(deps.cache_strategy == "adaptive").lower()},
      sampleRate: 1.0,
      debug: false,
      thresholds: {{
        lcp: {{ good: 2500, poor: 4000 }},
        fid: {{ good: 100, poor: 300 }},
        cls: {{ good: 0.1, poor: 0.25 }},
        inp: {{ good: 200, poor: 500 }}
      }},
      ...config
    }};

    this.initializeMonitoring();
  }}

  private initializeMonitoring(): void {{
    // Core Web Vitals
    getCLS(this.handleVital.bind(this));
    getFID(this.handleVital.bind(this));
    getLCP(this.handleVital.bind(this));
    onINP(this.handleVital.bind(this));

    // Additional metrics
    getFCP(this.handleVital.bind(this));
    getTTFB(this.handleVital.bind(this));

    // Custom performance monitoring
    this.initializeCustomMetrics();
    this.setupPerformanceObserver();
  }}

  private handleVital(vital: VitalsData): void {{
    const timestamp = Date.now();
    const rating = this.getRating(vital.name, vital.value);

    const vitalsEntry: VitalsData = {{
      ...vital,
      rating,
      timestamp,
      navigationType: this.getNavigationType()
    }};

    this.storeVital(vitalsEntry);

    if (this.config.enableReporting) {{
      this.reportVital(vitalsEntry);
    }}

    if (this.config.enableAdaptiveOptimization) {{
      this.triggerAdaptiveOptimization(vitalsEntry);
    }}

    if (this.config.debug) {{
      console.log('Web Vital:', vitalsEntry);
    }}
  }}

  private getRating(name: string, value: number): 'good' | 'needs-improvement' | 'poor' {{
    const thresholds = this.config.thresholds[name as keyof typeof this.config.thresholds];
    if (!thresholds) return 'good';

    if (value <= thresholds.good) return 'good';
    if (value <= thresholds.poor) return 'needs-improvement';
    return 'poor';
  }}

  private setupPerformanceObserver(): void {{
    if (!('PerformanceObserver' in window)) return;

    this.performanceObserver = new PerformanceObserver((list) => {{
      for (const entry of list.getEntries()) {{
        this.handlePerformanceEntry(entry);
      }}
    }});

    // Наблюдаем за различными типами performance entries
    try {{
      this.performanceObserver.observe({{ entryTypes: ['navigation', 'resource', 'paint', 'largest-contentful-paint', 'first-input', 'layout-shift'] }});
    }} catch (e) {{
      // Fallback для старых браузеров
      try {{
        this.performanceObserver.observe({{ entryTypes: ['navigation', 'resource', 'paint'] }});
      }} catch (e) {{
        console.warn('Performance Observer not fully supported');
      }}
    }}
  }}

  private handlePerformanceEntry(entry: PerformanceEntry): void {{
    // Обработка различных типов performance entries
    switch (entry.entryType) {{
      case 'navigation':
        this.handleNavigationEntry(entry as PerformanceNavigationTiming);
        break;
      case 'resource':
        this.handleResourceEntry(entry as PerformanceResourceTiming);
        break;
      case 'paint':
        this.handlePaintEntry(entry);
        break;
    }}
  }}

  private initializeCustomMetrics(): void {{
    // {deps.pwa_type}-specific metrics
    {_get_pwa_specific_metrics(deps.pwa_type)}
  }}

  // Adaptive optimization based on vitals
  private triggerAdaptiveOptimization(vital: VitalsData): void {{
    switch (vital.name) {{
      case 'LCP':
        if (vital.rating === 'poor') {{
          this.optimizeLCP();
        }}
        break;
      case 'FID':
      case 'INP':
        if (vital.rating === 'poor') {{
          this.optimizeInteractivity();
        }}
        break;
      case 'CLS':
        if (vital.rating === 'poor') {{
          this.optimizeLayoutStability();
        }}
        break;
    }}
  }}

  private optimizeLCP(): void {{
    // Adaptive LCP optimization
    {_get_lcp_optimization_code(deps.pwa_type)}
  }}

  private optimizeInteractivity(): void {{
    // Adaptive interactivity optimization
    {_get_interactivity_optimization_code(deps.pwa_type)}
  }}

  private optimizeLayoutStability(): void {{
    // Adaptive CLS optimization
    {_get_cls_optimization_code(deps.pwa_type)}
  }}

  // Analytics & Reporting
  private reportVital(vital: VitalsData): void {{
    // Send to analytics service
    if (Math.random() < this.config.sampleRate) {{
      this.sendToAnalytics(vital);
    }}
  }}

  private sendToAnalytics(vital: VitalsData): void {{
    // Google Analytics 4 integration
    if (typeof gtag !== 'undefined') {{
      gtag('event', vital.name, {{
        event_category: 'Web Vitals',
        value: Math.round(vital.name === 'CLS' ? vital.value * 1000 : vital.value),
        custom_parameter_1: vital.rating,
        custom_parameter_2: vital.navigationType
      }});
    }}

    // Custom analytics endpoint
    fetch('/api/vitals', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(vital)
    }}).catch(console.error);
  }}

  // Public API
  public getVitalsData(): Map<string, VitalsData[]> {{
    return this.vitalsData;
  }}

  public getAverageVitals(): Record<string, number> {{
    const averages: Record<string, number> = {{}};

    for (const [name, entries] of this.vitalsData) {{
      if (entries.length > 0) {{
        averages[name] = entries.reduce((sum, entry) => sum + entry.value, 0) / entries.length;
      }}
    }}

    return averages;
  }}

  public generateReport(): string {{
    const averages = this.getAverageVitals();
    const report = [];

    report.push('=== Web Vitals Report ===');

    for (const [name, value] of Object.entries(averages)) {{
      const rating = this.getRating(name, value);
      const emoji = rating === 'good' ? '✅' : rating === 'needs-improvement' ? '⚠️' : '❌';
      report.push(`${{emoji}} ${{name}}: ${{value.toFixed(2)}} (${{rating}})`);
    }}

    return report.join('\\n');
  }}

  public destroy(): void {{
    if (this.performanceObserver) {{
      this.performanceObserver.disconnect();
      this.performanceObserver = null;
    }}
  }}
}}

// Initialize monitor
const vitalsMonitor = new WebVitalsMonitor({{
  enableAdaptiveOptimization: true,
  debug: {str(deps.pwa_type == "gaming").lower()}, // Enable debug for gaming PWAs
  sampleRate: {_get_sample_rate(deps.pwa_type)}
}});
```

### 🔄 Real-time Dashboard Component

```typescript
// VitalsDashboard.tsx
import React, {{ useState, useEffect }} from 'react';

interface VitalsDisplayProps {{
  vitalsMonitor: WebVitalsMonitor;
}}

export const VitalsDashboard: React.FC<VitalsDisplayProps> = ({{ vitalsMonitor }}) => {{
  const [vitals, setVitals] = useState<Record<string, number>>({{}});
  const [isRealTime, setIsRealTime] = useState(true);

  useEffect(() => {{
    if (!isRealTime) return;

    const interval = setInterval(() => {{
      setVitals(vitalsMonitor.getAverageVitals());
    }}, 1000);

    return () => clearInterval(interval);
  }}, [vitalsMonitor, isRealTime]);

  const getVitalColor = (name: string, value: number): string => {{
    const rating = vitalsMonitor.getRating(name, value);
    return rating === 'good' ? '#10b981' : rating === 'needs-improvement' ? '#f59e0b' : '#ef4444';
  }};

  return (
    <div className="vitals-dashboard">
      <div className="vitals-header">
        <h3>🚀 Web Vitals Monitor</h3>
        <button
          onClick={{() => setIsRealTime(!isRealTime)}}
          className={{`toggle-btn ${{isRealTime ? 'active' : ''}}`}}
        >
          {{isRealTime ? '⏸️ Pause' : '▶️ Resume'}}
        </button>
      </div>

      <div className="vitals-grid">
        {{Object.entries(vitals).map(([name, value]) => (
          <div key={{name}} className="vital-card">
            <div className="vital-name">{{name.toUpperCase()}}</div>
            <div
              className="vital-value"
              style={{{{ color: getVitalColor(name, value) }}}}
            >
              {{value.toFixed(2)}}
              {{name === 'CLS' ? '' : 'ms'}}
            </div>
            <div className="vital-rating">
              {{vitalsMonitor.getRating(name, value)}}
            </div>
          </div>
        ))}
      </div>

      <div className="vitals-actions">
        <button onClick={{() => console.log(vitalsMonitor.generateReport())}}>
          📊 Generate Report
        </button>
        <button onClick={{() => vitalsMonitor.getVitalsData()}}>
          📋 Export Data
        </button>
      </div>
    </div>
  );
}};
```

### 📈 Performance Budget Integration

```typescript
// performance-budget.ts
interface PerformanceBudget {{
  lcp: number;
  fid: number;
  cls: number;
  inp: number;
  fcp: number;
  ttfb: number;
}}

const BUDGETS: Record<string, PerformanceBudget> = {{
  ecommerce: {{
    lcp: 2500,  // Critical for conversion
    fid: 100,   // Smooth interactions
    cls: 0.1,   // Stable product displays
    inp: 200,   // Quick form responses
    fcp: 1800,  // Fast first impression
    ttfb: 600   // Quick server response
  }},
  gaming: {{
    lcp: 2000,  // Fast game start
    fid: 50,    // Ultra-responsive controls
    cls: 0.05,  // No layout shifts during gameplay
    inp: 100,   // Instant game interactions
    fcp: 1500,  // Quick splash screen
    ttfb: 400   // Fast asset loading
  }},
  media: {{
    lcp: 3000,  // Acceptable for content loading
    fid: 100,   // Smooth media controls
    cls: 0.1,   // Stable content layout
    inp: 200,   // Responsive playback controls
    fcp: 2000,  // Content preview
    ttfb: 800   // Content delivery
  }},
  productivity: {{
    lcp: 2500,  // Quick app loading
    fid: 100,   // Responsive tools
    cls: 0.1,   // Stable workspace
    inp: 200,   // Quick actions
    fcp: 1800,  // Fast interface
    ttfb: 600   // Quick data access
  }},
  social: {{
    lcp: 2500,  // Fast content loading
    fid: 100,   // Smooth interactions
    cls: 0.1,   // Stable feed
    inp: 200,   // Quick posting/liking
    fcp: 1800,  // Fast timeline
    ttfb: 600   // Quick updates
  }}
}};

export function getPerformanceBudget(pwaType: string): PerformanceBudget {{
  return BUDGETS[pwaType] || BUDGETS.ecommerce;
}}

export function checkBudgetCompliance(
  vitals: Record<string, number>,
  pwaType: string
): Record<string, boolean> {{
  const budget = getPerformanceBudget(pwaType);
  const compliance: Record<string, boolean> = {{}};

  for (const [metric, value] of Object.entries(vitals)) {{
    const budgetValue = budget[metric as keyof PerformanceBudget];
    if (budgetValue !== undefined) {{
      compliance[metric] = value <= budgetValue;
    }}
  }}

  return compliance;
}}
```

### 🎯 PWA-Specific Optimizations для {deps.pwa_type}

{_get_pwa_specific_optimizations(deps.pwa_type)}

### 📱 Mobile-Specific Enhancements

```typescript
// mobile-vitals-enhancements.ts
export class MobileVitalsEnhancer {{
  private connectionObserver: NetworkInformation | null = null;

  constructor() {{
    this.setupConnectionObserver();
    this.setupDeviceMemoryOptimization();
  }}

  private setupConnectionObserver(): void {{
    // @ts-ignore - experimental API
    if ('connection' in navigator) {{
      // @ts-ignore
      this.connectionObserver = navigator.connection;
      this.adjustForNetworkConditions();

      // @ts-ignore
      navigator.connection.addEventListener('change', () => {{
        this.adjustForNetworkConditions();
      }});
    }}
  }}

  private adjustForNetworkConditions(): void {{
    if (!this.connectionObserver) return;

    const connection = this.connectionObserver;
    const effectiveType = connection.effectiveType;

    switch (effectiveType) {{
      case 'slow-2g':
      case '2g':
        this.enableLowBandwidthMode();
        break;
      case '3g':
        this.enableMediumBandwidthMode();
        break;
      case '4g':
      default:
        this.enableHighBandwidthMode();
        break;
    }}
  }}

  private enableLowBandwidthMode(): void {{
    // Aggressive optimization for slow networks
    {_get_low_bandwidth_optimizations(deps.pwa_type)}
  }}
}}
```

### 📊 Integration Instructions

1. **Install Web Vitals Library:**
   ```bash
   npm install web-vitals
   ```

2. **Add to your PWA entry point:**
   ```typescript
   import './web-vitals-monitor';
   ```

3. **Service Worker Integration:**
   ```javascript
   // Add to your service worker
   {_get_service_worker_vitals_integration(deps.pwa_type)}
   ```

4. **Analytics Setup:**
   - Configure Google Analytics 4 events
   - Set up custom analytics endpoint `/api/vitals`
   - Enable Real User Monitoring (RUM)

### 🎯 Success Metrics for {deps.pwa_type} PWA

{_get_success_metrics(deps.pwa_type)}

**Next Steps:**
1. Implement monitoring dashboard
2. Set up alerts for budget violations
3. Configure automated optimization triggers
4. Integrate with CI/CD for performance regression detection
"""


async def implement_adaptive_caching_strategies(
    ctx: RunContext[PWAMobileAgentDependencies],
    optimization_focus: str = "automatic"
) -> str:
    """
    Реализует адаптивные стратегии кэширования на основе Web Vitals и условий сети.

    Args:
        optimization_focus: Фокус оптимизации (automatic, bandwidth, storage, performance)

    Returns:
        Реализация адаптивного кэширования
    """
    deps = ctx.deps

    return f"""
## 🧠 Adaptive Caching Strategies для {deps.pwa_type} PWA

### 📊 Network-Aware Cache Management

```typescript
// adaptive-cache-manager.ts
interface NetworkConditions {{
  effectiveType: '2g' | '3g' | '4g' | 'slow-2g';
  downlink: number;
  rtt: number;
  saveData: boolean;
}}

interface CacheMetrics {{
  hitRate: number;
  missRate: number;
  averageLoadTime: number;
  storageUsage: number;
  lastOptimized: number;
}}

interface AdaptiveCacheConfig {{
  maxCacheSize: number;
  adaptiveThresholds: {{
    lcp: number;
    fid: number;
    cls: number;
  }};
  networkBasedLimits: {{
    '2g': {{ maxSize: number; retention: number }};
    '3g': {{ maxSize: number; retention: number }};
    '4g': {{ maxSize: number; retention: number }};
  }};
  pwaaType: string;
}}

class AdaptiveCacheManager {{
  private config: AdaptiveCacheConfig;
  private cacheMetrics: CacheMetrics;
  private networkObserver: NetworkInformation | null = null;
  private vitalsData: Map<string, number> = new Map();

  constructor(config: Partial<AdaptiveCacheConfig> = {{}}) {{
    this.config = {{
      maxCacheSize: {deps.max_cache_size_mb} * 1024 * 1024, // Convert MB to bytes
      adaptiveThresholds: {{
        lcp: {_get_adaptive_threshold("lcp", deps.pwa_type)},
        fid: {_get_adaptive_threshold("fid", deps.pwa_type)},
        cls: {_get_adaptive_threshold("cls", deps.pwa_type)}
      }},
      networkBasedLimits: {{
        '2g': {{ maxSize: {int(deps.max_cache_size_mb * 0.3)} * 1024 * 1024, retention: 24 * 60 * 60 * 1000 }}, // 1 day
        '3g': {{ maxSize: {int(deps.max_cache_size_mb * 0.6)} * 1024 * 1024, retention: 7 * 24 * 60 * 60 * 1000 }}, // 7 days
        '4g': {{ maxSize: {deps.max_cache_size_mb} * 1024 * 1024, retention: 30 * 24 * 60 * 60 * 1000 }} // 30 days
      }},
      pwaType: '{deps.pwa_type}',
      ...config
    }};

    this.initializeMetrics();
    this.setupNetworkObserver();
    this.setupVitalsIntegration();
  }}

  private initializeMetrics(): void {{
    this.cacheMetrics = {{
      hitRate: 0,
      missRate: 0,
      averageLoadTime: 0,
      storageUsage: 0,
      lastOptimized: Date.now()
    }};
  }}

  private setupNetworkObserver(): void {{
    // @ts-ignore - experimental API
    if ('connection' in navigator) {{
      // @ts-ignore
      this.networkObserver = navigator.connection;
      this.adjustCacheForNetwork();

      // @ts-ignore
      navigator.connection.addEventListener('change', () => {{
        this.adjustCacheForNetwork();
      }});
    }}
  }}

  private setupVitalsIntegration(): void {{
    // Listen for Web Vitals updates
    window.addEventListener('web-vitals-update', (event: CustomEvent) => {{
      const {{ name, value }} = event.detail;
      this.vitalsData.set(name, value);
      this.evaluateCacheOptimization();
    }});
  }}

  private adjustCacheForNetwork(): void {{
    if (!this.networkObserver) return;

    const {{ effectiveType, saveData }} = this.networkObserver;
    const limits = this.config.networkBasedLimits[effectiveType];

    if (limits) {{
      this.optimizeCacheSize(limits.maxSize);
      this.adjustRetentionPolicy(limits.retention);
    }}

    if (saveData) {{
      this.enableDataSaverMode();
    }} else {{
      this.disableDataSaverMode();
    }}
  }}

  private async optimizeCacheSize(targetSize: number): Promise<void> {{
    const currentUsage = await this.calculateStorageUsage();

    if (currentUsage > targetSize) {{
      await this.performCacheEviction(currentUsage - targetSize);
    }}
  }}

  private async performCacheEviction(bytesToFree: number): Promise<void> {{
    const cacheNames = await caches.keys();
    let freedBytes = 0;

    // {deps.pwa_type}-specific eviction strategy
    {_get_eviction_strategy(deps.pwa_type)}

    // LRU eviction as fallback
    for (const cacheName of cacheNames) {{
      if (freedBytes >= bytesToFree) break;

      const cache = await caches.open(cacheName);
      const requests = await cache.keys();

      // Sort by last access time (if available) or by age
      const sortedRequests = await this.sortRequestsByPriority(requests, cacheName);

      for (const request of sortedRequests) {{
        if (freedBytes >= bytesToFree) break;

        const response = await cache.match(request);
        if (response) {{
          const size = this.estimateResponseSize(response);
          await cache.delete(request);
          freedBytes += size;
        }}
      }}
    }}
  }}

  private async sortRequestsByPriority(
    requests: readonly Request[],
    cacheName: string
  ): Promise<Request[]> {{
    // PWA-specific priority sorting
    {_get_priority_sorting(deps.pwa_type)}
  }}

  private evaluateCacheOptimization(): void {{
    const lcpValue = this.vitalsData.get('LCP') || 0;
    const fidValue = this.vitalsData.get('FID') || 0;
    const clsValue = this.vitalsData.get('CLS') || 0;

    // Trigger optimization if vitals are poor
    if (lcpValue > this.config.adaptiveThresholds.lcp) {{
      this.optimizeForLCP();
    }}

    if (fidValue > this.config.adaptiveThresholds.fid) {{
      this.optimizeForFID();
    }}

    if (clsValue > this.config.adaptiveThresholds.cls) {{
      this.optimizeForCLS();
    }}
  }}

  private async optimizeForLCP(): Promise<void> {{
    // LCP optimization through caching
    {_get_lcp_cache_optimization(deps.pwa_type)}
  }}

  private async optimizeForFID(): Promise<void> {{
    // FID optimization through cache strategy
    {_get_fid_cache_optimization(deps.pwa_type)}
  }}

  private async optimizeForCLS(): Promise<void> {{
    // CLS optimization through preloading
    {_get_cls_cache_optimization(deps.pwa_type)}
  }}

  // Metrics tracking
  public async trackCacheHit(request: Request): Promise<void> {{
    this.cacheMetrics.hitRate = this.calculateHitRate();
    await this.updateMetrics();
  }}

  public async trackCacheMiss(request: Request): Promise<void> {{
    this.cacheMetrics.missRate = this.calculateMissRate();
    await this.updateMetrics();
  }}

  private calculateHitRate(): number {{
    // Implementation for hit rate calculation
    return 0.85; // Placeholder
  }}

  private calculateMissRate(): number {{
    // Implementation for miss rate calculation
    return 0.15; // Placeholder
  }}

  // Public API
  public getCacheMetrics(): CacheMetrics {{
    return {{ ...this.cacheMetrics }};
  }}

  public async generateOptimizationReport(): Promise<string> {{
    const report = [];
    const metrics = this.getCacheMetrics();

    report.push('=== Adaptive Cache Report ===');
    report.push(`Hit Rate: ${{(metrics.hitRate * 100).toFixed(1)}}%`);
    report.push(`Storage Usage: ${{(metrics.storageUsage / 1024 / 1024).toFixed(1)}}MB`);

    const networkType = this.networkObserver?.effectiveType || 'unknown';
    report.push(`Network: ${{networkType}}`);

    // PWA-specific recommendations
    {_get_cache_recommendations(deps.pwa_type)}

    return report.join('\\n');
  }}
}}
```

### 🎯 PWA-Specific Cache Strategies

{_get_pwa_cache_strategies(deps.pwa_type)}

### 🔄 Dynamic Cache Strategy Selection

```typescript
// dynamic-strategy-selector.ts
export class DynamicCacheStrategy {{
  private currentStrategy: string = '{deps.offline_strategy}';
  private vitalsThresholds = {{
    good: {{ lcp: 2500, fid: 100, cls: 0.1 }},
    poor: {{ lcp: 4000, fid: 300, cls: 0.25 }}
  }};

  public selectOptimalStrategy(vitals: Record<string, number>): string {{
    const lcpRating = this.getRating('lcp', vitals.LCP || 0);
    const fidRating = this.getRating('fid', vitals.FID || 0);
    const clsRating = this.getRating('cls', vitals.CLS || 0);

    // Strategy selection logic
    if (lcpRating === 'poor') {{
      return 'cache-first'; // Prioritize speed
    }}

    if (fidRating === 'poor') {{
      return 'stale-while-revalidate'; // Reduce blocking
    }}

    if (clsRating === 'poor') {{
      return 'network-first'; // Ensure content stability
    }}

    return '{deps.offline_strategy}'; // Default strategy
  }}

  private getRating(metric: string, value: number): 'good' | 'poor' {{
    const thresholds = this.vitalsThresholds;
    if (value <= thresholds.good[metric as keyof typeof thresholds.good]) {{
      return 'good';
    }}
    return 'poor';
  }}
}}
```

### 📊 Cache Analytics Dashboard

```typescript
// cache-analytics.tsx
import React, {{ useState, useEffect }} from 'react';

interface CacheAnalyticsProps {{
  cacheManager: AdaptiveCacheManager;
}}

export const CacheAnalytics: React.FC<CacheAnalyticsProps> = ({{ cacheManager }}) => {{
  const [metrics, setMetrics] = useState<CacheMetrics>(cacheManager.getCacheMetrics());
  const [report, setReport] = useState<string>('');

  useEffect(() => {{
    const interval = setInterval(async () => {{
      setMetrics(cacheManager.getCacheMetrics());
      setReport(await cacheManager.generateOptimizationReport());
    }}, 5000);

    return () => clearInterval(interval);
  }}, [cacheManager]);

  return (
    <div className="cache-analytics">
      <div className="metrics-grid">
        <div className="metric-card">
          <h4>Hit Rate</h4>
          <div className="metric-value">{{(metrics.hitRate * 100).toFixed(1)}}%</div>
        </div>
        <div className="metric-card">
          <h4>Storage Usage</h4>
          <div className="metric-value">{{(metrics.storageUsage / 1024 / 1024).toFixed(1)}}MB</div>
        </div>
        <div className="metric-card">
          <h4>Avg Load Time</h4>
          <div className="metric-value">{{metrics.averageLoadTime.toFixed(0)}}ms</div>
        </div>
      </div>

      <div className="optimization-report">
        <h4>📊 Optimization Report</h4>
        <pre>{{report}}</pre>
      </div>
    </div>
  );
}};
```

### 🚀 Integration Instructions

1. **Initialize Adaptive Caching:**
   ```typescript
   import {{ AdaptiveCacheManager }} from './adaptive-cache-manager';

   const cacheManager = new AdaptiveCacheManager({{
     maxCacheSize: {deps.max_cache_size_mb} * 1024 * 1024,
     pwaType: '{deps.pwa_type}'
   }});
   ```

2. **Service Worker Integration:**
   ```javascript
   // Add to your service worker
   {_get_service_worker_adaptive_integration(deps.pwa_type)}
   ```

3. **Web Vitals Integration:**
   ```typescript
   // Connect with Web Vitals
   import {{ getCLS, getFID, getLCP }} from 'web-vitals';

   getCLS((metric) => {{
     window.dispatchEvent(new CustomEvent('web-vitals-update', {{
       detail: {{ name: metric.name, value: metric.value }}
     }}));
   }});
   ```

### 🎯 {deps.pwa_type.title()} PWA Optimization Targets

{_get_cache_optimization_targets(deps.pwa_type)}

**Benefits:**
- ⚡ **Automatic Optimization**: Self-tuning based on real performance
- 📱 **Network Adaptive**: Adjusts to connection quality
- 🧠 **Smart Eviction**: PWA-specific priority algorithms
- 📊 **Performance Driven**: Web Vitals integrated decisions
- 🔄 **Dynamic Strategies**: Real-time strategy switching
"""


async def implement_runtime_performance_monitoring(
    ctx: RunContext[PWAMobileAgentDependencies],
    monitoring_scope: str = "comprehensive"
) -> str:
    """
    Реализует runtime мониторинг производительности с real-time алертами.

    Args:
        monitoring_scope: Область мониторинга (comprehensive, memory, cpu, network, custom)

    Returns:
        Система runtime мониторинга производительности
    """
    deps = ctx.deps

    return f"""
## 🔬 Runtime Performance Monitoring для {deps.pwa_type} PWA

### 📊 Comprehensive Performance Monitor

```typescript
// runtime-performance-monitor.ts
interface PerformanceMetrics {{
  memory: {{
    used: number;
    limit: number;
    percentage: number;
  }};
  cpu: {{
    usage: number;
    idleTime: number;
  }};
  network: {{
    bandwidth: number;
    latency: number;
    effectiveType: string;
  }};
  fps: {{
    current: number;
    average: number;
    drops: number;
  }};
  battery: {{
    level: number;
    charging: boolean;
  }};
  storage: {{
    used: number;
    available: number;
    quota: number;
  }};
}}

interface PerformanceAlert {{
  type: 'warning' | 'critical' | 'info';
  metric: string;
  value: number;
  threshold: number;
  timestamp: number;
  action?: string;
}}

interface MonitoringConfig {{
  intervals: {{
    memory: number;
    cpu: number;
    network: number;
    fps: number;
    battery: number;
  }};
  thresholds: {{
    memoryWarning: number;
    memoryCritical: number;
    cpuWarning: number;
    cpuCritical: number;
    fpsWarning: number;
    fpsCritical: number;
  }};
  enableAlerts: boolean;
  enableAutoOptimization: boolean;
  pwaType: string;
}}

export class RuntimePerformanceMonitor {{
  private config: MonitoringConfig;
  private metrics: PerformanceMetrics;
  private alerts: PerformanceAlert[] = [];
  private observers: Map<string, any> = new Map();
  private intervals: Map<string, NodeJS.Timeout> = new Map();

  constructor(config: Partial<MonitoringConfig> = {{}}) {{
    this.config = {{
      intervals: {{
        memory: 5000,     // 5 seconds
        cpu: 2000,        // 2 seconds
        network: 10000,   // 10 seconds
        fps: 1000,        // 1 second
        battery: 30000    // 30 seconds
      }},
      thresholds: {{
        memoryWarning: {_get_memory_threshold("warning", deps.pwa_type)},
        memoryCritical: {_get_memory_threshold("critical", deps.pwa_type)},
        cpuWarning: {_get_cpu_threshold("warning", deps.pwa_type)},
        cpuCritical: {_get_cpu_threshold("critical", deps.pwa_type)},
        fpsWarning: {_get_fps_threshold("warning", deps.pwa_type)},
        fpsCritical: {_get_fps_threshold("critical", deps.pwa_type)}
      }},
      enableAlerts: true,
      enableAutoOptimization: {str(deps.cache_strategy == "adaptive").lower()},
      pwaType: '{deps.pwa_type}',
      ...config
    }};

    this.initializeMetrics();
    this.startMonitoring();
  }}

  private initializeMetrics(): void {{
    this.metrics = {{
      memory: {{ used: 0, limit: 0, percentage: 0 }},
      cpu: {{ usage: 0, idleTime: 0 }},
      network: {{ bandwidth: 0, latency: 0, effectiveType: 'unknown' }},
      fps: {{ current: 0, average: 0, drops: 0 }},
      battery: {{ level: 100, charging: false }},
      storage: {{ used: 0, available: 0, quota: 0 }}
    }};
  }}

  private startMonitoring(): void {{
    // Memory monitoring
    this.intervals.set('memory', setInterval(() => {{
      this.trackMemoryUsage();
    }}, this.config.intervals.memory));

    // CPU monitoring (approximation)
    this.intervals.set('cpu', setInterval(() => {{
      this.trackCPUUsage();
    }}, this.config.intervals.cpu));

    // Network monitoring
    this.intervals.set('network', setInterval(() => {{
      this.trackNetworkPerformance();
    }}, this.config.intervals.network));

    // FPS monitoring
    this.intervals.set('fps', setInterval(() => {{
      this.trackFrameRate();
    }}, this.config.intervals.fps));

    // Battery monitoring
    if ('getBattery' in navigator) {{
      this.intervals.set('battery', setInterval(() => {{
        this.trackBatteryStatus();
      }}, this.config.intervals.battery));
    }}

    // Storage monitoring
    this.trackStorageUsage();

    // Setup performance observers
    this.setupPerformanceObservers();
  }}

  private trackMemoryUsage(): void {{
    // @ts-ignore - experimental API
    if ('memory' in performance) {{
      // @ts-ignore
      const memory = performance.memory;
      const used = memory.usedJSHeapSize;
      const limit = memory.jsHeapSizeLimit;
      const percentage = (used / limit) * 100;

      this.metrics.memory = {{ used, limit, percentage }};

      // Check thresholds
      if (percentage > this.config.thresholds.memoryCritical) {{
        this.createAlert('critical', 'memory', percentage, this.config.thresholds.memoryCritical);
        if (this.config.enableAutoOptimization) {{
          this.optimizeMemoryUsage();
        }}
      }} else if (percentage > this.config.thresholds.memoryWarning) {{
        this.createAlert('warning', 'memory', percentage, this.config.thresholds.memoryWarning);
      }}
    }}
  }}

  private trackCPUUsage(): void {{
    // CPU approximation using frame timing
    const startTime = performance.now();

    requestIdleCallback((deadline) => {{
      const endTime = performance.now();
      const frameTime = endTime - startTime;
      const idealFrameTime = 16.67; // 60 FPS

      const cpuUsage = Math.min(100, (frameTime / idealFrameTime) * 100);
      this.metrics.cpu.usage = cpuUsage;
      this.metrics.cpu.idleTime = deadline.timeRemaining();

      if (cpuUsage > this.config.thresholds.cpuCritical) {{
        this.createAlert('critical', 'cpu', cpuUsage, this.config.thresholds.cpuCritical);
        if (this.config.enableAutoOptimization) {{
          this.optimizeCPUUsage();
        }}
      }} else if (cpuUsage > this.config.thresholds.cpuWarning) {{
        this.createAlert('warning', 'cpu', cpuUsage, this.config.thresholds.cpuWarning);
      }}
    }});
  }}

  private trackNetworkPerformance(): void {{
    // @ts-ignore - experimental API
    if ('connection' in navigator) {{
      // @ts-ignore
      const connection = navigator.connection;

      this.metrics.network = {{
        bandwidth: connection.downlink || 0,
        latency: connection.rtt || 0,
        effectiveType: connection.effectiveType || 'unknown'
      }};

      // Network quality assessment
      const isSlowNetwork = connection.effectiveType === '2g' || connection.effectiveType === 'slow-2g';
      if (isSlowNetwork) {{
        this.createAlert('warning', 'network', 0, 0, 'Slow network detected');
        if (this.config.enableAutoOptimization) {{
          this.optimizeForSlowNetwork();
        }}
      }}
    }}
  }}

  private trackFrameRate(): void {{
    let lastTime = performance.now();
    let frameCount = 0;
    let fpsSum = 0;

    const measureFPS = (currentTime: number) => {{
      frameCount++;
      const deltaTime = currentTime - lastTime;

      if (deltaTime >= 1000) {{ // Calculate FPS every second
        const fps = Math.round((frameCount * 1000) / deltaTime);
        this.metrics.fps.current = fps;

        fpsSum += fps;
        this.metrics.fps.average = Math.round(fpsSum / frameCount);

        if (fps < this.config.thresholds.fpsCritical) {{
          this.metrics.fps.drops++;
          this.createAlert('critical', 'fps', fps, this.config.thresholds.fpsCritical);
          if (this.config.enableAutoOptimization) {{
            this.optimizeFrameRate();
          }}
        }} else if (fps < this.config.thresholds.fpsWarning) {{
          this.createAlert('warning', 'fps', fps, this.config.thresholds.fpsWarning);
        }}

        frameCount = 0;
        lastTime = currentTime;
      }}

      requestAnimationFrame(measureFPS);
    }};

    requestAnimationFrame(measureFPS);
  }}

  private async trackBatteryStatus(): Promise<void> {{
    try {{
      // @ts-ignore
      const battery = await navigator.getBattery();

      this.metrics.battery = {{
        level: Math.round(battery.level * 100),
        charging: battery.charging
      }};

      // Battery optimization for low levels
      if (battery.level < 0.2 && !battery.charging) {{
        this.createAlert('warning', 'battery', battery.level * 100, 20);
        if (this.config.enableAutoOptimization) {{
          this.enableBatterySaver();
        }}
      }}
    }} catch (error) {{
      console.warn('Battery API not available');
    }}
  }}

  private async trackStorageUsage(): Promise<void> {{
    if ('storage' in navigator && 'estimate' in navigator.storage) {{
      try {{
        const estimate = await navigator.storage.estimate();

        this.metrics.storage = {{
          used: estimate.usage || 0,
          quota: estimate.quota || 0,
          available: (estimate.quota || 0) - (estimate.usage || 0)
        }};

        const usagePercentage = ((estimate.usage || 0) / (estimate.quota || 1)) * 100;
        if (usagePercentage > 80) {{
          this.createAlert('warning', 'storage', usagePercentage, 80);
          if (this.config.enableAutoOptimization) {{
            this.cleanupStorage();
          }}
        }}
      }} catch (error) {{
        console.warn('Storage API not available');
      }}
    }}
  }}

  private setupPerformanceObservers(): void {{
    // Long tasks observer
    if ('PerformanceObserver' in window) {{
      try {{
        const longTaskObserver = new PerformanceObserver((list) => {{
          for (const entry of list.getEntries()) {{
            if (entry.duration > 50) {{ // Tasks longer than 50ms
              this.createAlert('warning', 'long-task', entry.duration, 50);
            }}
          }}
        }});

        longTaskObserver.observe({{ entryTypes: ['longtask'] }});
        this.observers.set('longtask', longTaskObserver);
      }} catch (e) {{
        console.warn('Long task observer not supported');
      }}
    }}
  }}

  // Alert management
  private createAlert(
    type: 'warning' | 'critical' | 'info',
    metric: string,
    value: number,
    threshold: number,
    message?: string
  ): void {{
    const alert: PerformanceAlert = {{
      type,
      metric,
      value,
      threshold,
      timestamp: Date.now(),
      action: message
    }};

    this.alerts.push(alert);

    if (this.config.enableAlerts) {{
      this.displayAlert(alert);
    }}

    // Keep only last 100 alerts
    if (this.alerts.length > 100) {{
      this.alerts = this.alerts.slice(-100);
    }}
  }}

  private displayAlert(alert: PerformanceAlert): void {{
    const emoji = alert.type === 'critical' ? '🔴' : alert.type === 'warning' ? '⚠️' : 'ℹ️';
    console.warn(`${{emoji}} Performance Alert: ${{alert.metric}} = ${{alert.value}} (threshold: ${{alert.threshold}})`);

    // Show user notification for critical alerts
    if (alert.type === 'critical' && 'Notification' in window && Notification.permission === 'granted') {{
      new Notification(`Performance Alert: ${{alert.metric}}`, {{
        body: `Value ${{alert.value}} exceeded threshold ${{alert.threshold}}`,
        icon: '/icons/icon-192x192.png'
      }});
    }}
  }}

  // Optimization methods
  private optimizeMemoryUsage(): void {{
    // {deps.pwa_type}-specific memory optimization
    {_get_memory_optimization(deps.pwa_type)}
  }}

  private optimizeCPUUsage(): void {{
    // {deps.pwa_type}-specific CPU optimization
    {_get_cpu_optimization(deps.pwa_type)}
  }}

  private optimizeForSlowNetwork(): void {{
    // {deps.pwa_type}-specific network optimization
    {_get_network_optimization(deps.pwa_type)}
  }}

  private optimizeFrameRate(): void {{
    // {deps.pwa_type}-specific FPS optimization
    {_get_fps_optimization(deps.pwa_type)}
  }}

  private enableBatterySaver(): void {{
    // {deps.pwa_type}-specific battery optimization
    {_get_battery_optimization(deps.pwa_type)}
  }}

  private async cleanupStorage(): void {{
    // Storage cleanup strategy
    {_get_storage_cleanup(deps.pwa_type)}
  }}

  // Public API
  public getMetrics(): PerformanceMetrics {{
    return {{ ...this.metrics }};
  }}

  public getAlerts(type?: 'warning' | 'critical' | 'info'): PerformanceAlert[] {{
    if (type) {{
      return this.alerts.filter(alert => alert.type === type);
    }}
    return [...this.alerts];
  }}

  public clearAlerts(): void {{
    this.alerts = [];
  }}

  public generateReport(): string {{
    const report = [];
    const metrics = this.getMetrics();

    report.push('=== Runtime Performance Report ===');
    report.push(`Memory: ${{metrics.memory.percentage.toFixed(1)}}% (${{(metrics.memory.used / 1024 / 1024).toFixed(1)}}MB)`);
    report.push(`CPU: ${{metrics.cpu.usage.toFixed(1)}}%`);
    report.push(`FPS: ${{metrics.fps.current}} (avg: ${{metrics.fps.average}})`);
    report.push(`Network: ${{metrics.network.effectiveType}} (${{metrics.network.bandwidth}}Mbps)`);
    report.push(`Battery: ${{metrics.battery.level}}% (${{metrics.battery.charging ? 'charging' : 'not charging'}})`);
    report.push(`Storage: ${{(metrics.storage.used / 1024 / 1024).toFixed(1)}}MB used`);

    const criticalAlerts = this.getAlerts('critical');
    const warningAlerts = this.getAlerts('warning');

    if (criticalAlerts.length > 0) {{
      report.push(`\\n🔴 Critical Alerts: ${{criticalAlerts.length}}`);
    }}
    if (warningAlerts.length > 0) {{
      report.push(`⚠️ Warning Alerts: ${{warningAlerts.length}}`);
    }}

    return report.join('\\n');
  }}

  public destroy(): void {{
    // Clear all intervals
    for (const [name, interval] of this.intervals) {{
      clearInterval(interval);
    }}
    this.intervals.clear();

    // Disconnect observers
    for (const [name, observer] of this.observers) {{
      observer.disconnect();
    }}
    this.observers.clear();
  }}
}}
```

### 📱 Mobile-Optimized Performance Dashboard

```typescript
// performance-dashboard.tsx
import React, {{ useState, useEffect }} from 'react';

interface PerformanceDashboardProps {{
  monitor: RuntimePerformanceMonitor;
}}

export const PerformanceDashboard: React.FC<PerformanceDashboardProps> = ({{ monitor }}) => {{
  const [metrics, setMetrics] = useState(monitor.getMetrics());
  const [alerts, setAlerts] = useState(monitor.getAlerts());
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {{
    const interval = setInterval(() => {{
      setMetrics(monitor.getMetrics());
      setAlerts(monitor.getAlerts());
    }}, 1000);

    return () => clearInterval(interval);
  }}, [monitor]);

  const getStatusColor = (value: number, warning: number, critical: number): string => {{
    if (value >= critical) return '#ef4444';
    if (value >= warning) return '#f59e0b';
    return '#10b981';
  }};

  return (
    <div className="performance-dashboard">
      {{/* Compact View */}}
      <div className="compact-metrics" onClick={{() => setIsExpanded(!isExpanded)}}>
        <div className="metric-indicator">
          <span style={{{{ color: getStatusColor(metrics.memory.percentage, 70, 85) }}}}>
            MEM: {{metrics.memory.percentage.toFixed(0)}}%
          </span>
        </div>
        <div className="metric-indicator">
          <span style={{{{ color: getStatusColor(metrics.cpu.usage, 70, 85) }}}}>
            CPU: {{metrics.cpu.usage.toFixed(0)}}%
          </span>
        </div>
        <div className="metric-indicator">
          <span style={{{{ color: getStatusColor(60 - metrics.fps.current, 30, 45) }}}}>
            FPS: {{metrics.fps.current}}
          </span>
        </div>
        {{alerts.filter(a => a.type === 'critical').length > 0 && (
          <div className="alert-indicator critical">🔴</div>
        )}}
        {{alerts.filter(a => a.type === 'warning').length > 0 && (
          <div className="alert-indicator warning">⚠️</div>
        )}}
      </div>

      {{/* Expanded View */}}
      {{isExpanded && (
        <div className="expanded-metrics">
          <div className="metrics-grid">
            <div className="metric-card">
              <h4>Memory</h4>
              <div className="metric-value">{{metrics.memory.percentage.toFixed(1)}}%</div>
              <div className="metric-detail">{{(metrics.memory.used / 1024 / 1024).toFixed(1)}}MB used</div>
            </div>

            <div className="metric-card">
              <h4>CPU</h4>
              <div className="metric-value">{{metrics.cpu.usage.toFixed(1)}}%</div>
              <div className="metric-detail">{{metrics.cpu.idleTime.toFixed(1)}}ms idle</div>
            </div>

            <div className="metric-card">
              <h4>Frame Rate</h4>
              <div className="metric-value">{{metrics.fps.current}} FPS</div>
              <div className="metric-detail">{{metrics.fps.drops}} drops</div>
            </div>

            <div className="metric-card">
              <h4>Network</h4>
              <div className="metric-value">{{metrics.network.effectiveType}}</div>
              <div className="metric-detail">{{metrics.network.bandwidth}}Mbps</div>
            </div>

            <div className="metric-card">
              <h4>Battery</h4>
              <div className="metric-value">{{metrics.battery.level}}%</div>
              <div className="metric-detail">{{metrics.battery.charging ? '🔌' : '🔋'}}</div>
            </div>

            <div className="metric-card">
              <h4>Storage</h4>
              <div className="metric-value">{{(metrics.storage.used / 1024 / 1024).toFixed(1)}}MB</div>
              <div className="metric-detail">{{(metrics.storage.available / 1024 / 1024).toFixed(1)}}MB free</div>
            </div>
          </div>

          {{alerts.length > 0 && (
            <div className="alerts-section">
              <h4>Recent Alerts</h4>
              {{alerts.slice(-5).map((alert, index) => (
                <div key={{index}} className={{`alert alert-${{alert.type}}`}}>
                  <span>{{alert.metric}}: {{alert.value}} (threshold: {{alert.threshold}})</span>
                  <span className="alert-time">{{new Date(alert.timestamp).toLocaleTimeString()}}</span>
                </div>
              ))}
            </div>
          )}}

          <div className="dashboard-actions">
            <button onClick={{() => console.log(monitor.generateReport())}}>
              📊 Generate Report
            </button>
            <button onClick={{() => monitor.clearAlerts()}}>
              🗑️ Clear Alerts
            </button>
          </div>
        </div>
      )}}
    </div>
  );
}};
```

### 🎯 {deps.pwa_type.title()} PWA Specific Monitoring

{_get_pwa_specific_monitoring(deps.pwa_type)}

### 🚀 Integration Instructions

1. **Initialize Performance Monitoring:**
   ```typescript
   import {{ RuntimePerformanceMonitor }} from './runtime-performance-monitor';

   const performanceMonitor = new RuntimePerformanceMonitor({{
     enableAutoOptimization: true,
     pwaType: '{deps.pwa_type}',
     thresholds: {{
       memoryWarning: 70,
       memoryCritical: 85,
       cpuWarning: 70,
       cpuCritical: 85,
       fpsWarning: 45,
       fpsCritical: 30
     }}
   }});
   ```

2. **Service Worker Integration:**
   ```javascript
   // Send performance data to service worker
   setInterval(() => {{
     const metrics = performanceMonitor.getMetrics();
     navigator.serviceWorker.controller?.postMessage({{
       type: 'PERFORMANCE_UPDATE',
       metrics
     }});
   }}, 10000); // Every 10 seconds
   ```

3. **React Integration:**
   ```tsx
   import {{ PerformanceDashboard }} from './performance-dashboard';

   function App() {{
     return (
       <div>
         <PerformanceDashboard monitor={{performanceMonitor}} />
         {{/* Your app content */}}
       </div>
     );
   }}
   ```

### 📊 Monitoring Scope: {monitoring_scope}

{_get_monitoring_scope_config(monitoring_scope, deps.pwa_type)}

**Benefits:**
- 🔍 **Real-time Monitoring**: Continuous performance tracking
- ⚡ **Auto-optimization**: Automatic performance adjustments
- 🚨 **Smart Alerts**: Context-aware performance warnings
- 📱 **Mobile-optimized**: Battery and network aware
- 🎯 **PWA-specific**: Tailored for {deps.pwa_type} applications
"""


def _get_pwa_specific_metrics(pwa_type: str) -> str:
    """Возвращает специфичные для PWA метрики."""
    metrics_map = {
        "ecommerce": """
    // E-commerce specific metrics
    this.trackCheckoutFunnelMetrics();
    this.trackProductImageLoadTimes();
    this.trackCartInteractionLatency();""",
        "gaming": """
    // Gaming specific metrics
    this.trackFrameRate();
    this.trackInputLatency();
    this.trackAssetLoadingTimes();""",
        "media": """
    // Media specific metrics
    this.trackVideoLoadTime();
    this.trackContentSeekLatency();
    this.trackBufferingEvents();""",
        "productivity": """
    // Productivity specific metrics
    this.trackDocumentLoadTime();
    this.trackAutoSaveLatency();
    this.trackToolSwitchingTime();""",
        "social": """
    // Social specific metrics
    this.trackFeedLoadTime();
    this.trackPostInteractionLatency();
    this.trackNotificationDeliveryTime();"""
    }
    return metrics_map.get(pwa_type, "// General metrics")


def _get_lcp_optimization_code(pwa_type: str) -> str:
    """Возвращает код оптимизации LCP для типа PWA."""
    optimizations = {
        "ecommerce": """
    // E-commerce LCP optimization
    this.preloadProductImages();
    this.optimizeHeroBanner();
    this.prioritizeCriticalCSS();""",
        "gaming": """
    // Gaming LCP optimization
    this.preloadGameAssets();
    this.optimizeSplashScreen();
    this.prioritizeGameEngine();""",
        "media": """
    // Media LCP optimization
    this.preloadThumbnails();
    this.optimizeVideoPosters();
    this.prioritizeContentView();""",
        "productivity": """
    // Productivity LCP optimization
    this.preloadWorkspaceUI();
    this.optimizeToolbar();
    this.prioritizeDocumentView();""",
        "social": """
    // Social LCP optimization
    this.preloadFeedContent();
    this.optimizeProfileImages();
    this.prioritizeTimeline();"""
    }
    return optimizations.get(pwa_type, "// Generic LCP optimization")


def _get_interactivity_optimization_code(pwa_type: str) -> str:
    """Возвращает код оптимизации интерактивности для типа PWA."""
    optimizations = {
        "ecommerce": """
    // E-commerce interactivity optimization
    this.deferNonCriticalScripts();
    this.optimizeAddToCartButton();
    this.reduceMainThreadBlocking();""",
        "gaming": """
    // Gaming interactivity optimization
    this.prioritizeInputHandlers();
    this.optimizeGameLoop();
    this.reduceJSExecutionTime();""",
        "media": """
    // Media interactivity optimization
    this.optimizePlaybackControls();
    this.deferVideoProcessing();
    this.reduceUIBlocking();""",
        "productivity": """
    // Productivity interactivity optimization
    this.optimizeToolResponsiveness();
    this.deferBackgroundTasks();
    this.prioritizeUserActions();""",
        "social": """
    // Social interactivity optimization
    this.optimizeLikeButtons();
    this.deferFeedProcessing();
    this.prioritizeInteractions();"""
    }
    return optimizations.get(pwa_type, "// Generic interactivity optimization")


def _get_cls_optimization_code(pwa_type: str) -> str:
    """Возвращает код оптимизации CLS для типа PWA."""
    optimizations = {
        "ecommerce": """
    // E-commerce CLS optimization
    this.reserveProductImageSpace();
    this.stabilizeCartUpdates();
    this.preventAdLayoutShifts();""",
        "gaming": """
    // Gaming CLS optimization
    this.reserveGameCanvasSpace();
    this.stabilizeUIElements();
    this.preventAssetLoadShifts();""",
        "media": """
    // Media CLS optimization
    this.reserveVideoPlayerSpace();
    this.stabilizeContentLayout();
    this.preventThumbnailShifts();""",
        "productivity": """
    // Productivity CLS optimization
    this.reserveToolbarSpace();
    this.stabilizeDocumentLayout();
    this.preventPanelShifts();""",
        "social": """
    // Social CLS optimization
    this.reserveFeedSpace();
    this.stabilizePostLayout();
    this.preventImageShifts();"""
    }
    return optimizations.get(pwa_type, "// Generic CLS optimization")


def _get_sample_rate(pwa_type: str) -> float:
    """Возвращает sample rate для аналитики в зависимости от типа PWA."""
    rates = {
        "gaming": 1.0,  # Высокий sample rate для gaming
        "ecommerce": 0.8,  # Высокий для e-commerce
        "productivity": 0.6,  # Средний для productivity
        "media": 0.5,  # Средний для media
        "social": 0.3   # Низкий для social (много пользователей)
    }
    return rates.get(pwa_type, 0.5)


def _get_pwa_specific_optimizations(pwa_type: str) -> str:
    """Возвращает специфичные оптимизации для типа PWA."""
    optimizations = {
        "ecommerce": """
**E-commerce PWA Optimizations:**

```typescript
// Product image optimization
const imageOptimizer = {
  preloadCriticalImages: () => {
    const criticalImages = document.querySelectorAll('.hero-image, .product-image-primary');
    criticalImages.forEach(img => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.as = 'image';
      link.href = img.src || img.dataset.src;
      document.head.appendChild(link);
    });
  },

  lazyLoadProductImages: () => {
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            imageObserver.unobserve(img);
          }
        });
      });

      document.querySelectorAll('.product-image.lazy').forEach(img => {
        imageObserver.observe(img);
      });
    }
  }
};

// Cart interaction optimization
const cartOptimizer = {
  debounceQuantityUpdates: (callback, delay = 300) => {
    let timeoutId;
    return (...args) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => callback.apply(this, args), delay);
    };
  }
};
```""",
        "gaming": """
**Gaming PWA Optimizations:**

```typescript
// Frame rate monitoring
const gamePerformanceMonitor = {
  fpsCounter: 0,
  lastFrameTime: 0,

  trackFPS: () => {
    const now = performance.now();
    const fps = 1000 / (now - this.lastFrameTime);
    this.lastFrameTime = now;

    if (fps < 30) {
      this.optimizeForLowFPS();
    }

    this.fpsCounter = fps;
    requestAnimationFrame(() => this.trackFPS());
  },

  optimizeForLowFPS: () => {
    // Reduce visual effects
    document.body.classList.add('low-performance-mode');

    // Reduce asset quality
    this.reduceAssetQuality();
  }
};

// Input latency optimization
const inputOptimizer = {
  setupLowLatencyInput: () => {
    // Use passive listeners for better performance
    document.addEventListener('touchstart', this.handleTouch, { passive: false });
    document.addEventListener('touchmove', this.handleTouch, { passive: false });

    // Prevent context menu on long press
    document.addEventListener('contextmenu', e => e.preventDefault());
  }
};
```""",
        "media": """
**Media PWA Optimizations:**

```typescript
// Video performance optimization
const mediaOptimizer = {
  setupAdaptiveQuality: () => {
    const video = document.querySelector('video');
    if (!video) return;

    // Monitor connection speed
    if ('connection' in navigator) {
      const connection = navigator.connection;

      switch (connection.effectiveType) {
        case '2g':
          video.src = video.dataset.srcLow;
          break;
        case '3g':
          video.src = video.dataset.srcMed;
          break;
        default:
          video.src = video.dataset.srcHigh;
      }
    }
  },

  preloadVideoContent: () => {
    const videos = document.querySelectorAll('video[data-preload]');
    videos.forEach(video => {
      video.preload = 'metadata';
    });
  }
};
```""",
        "productivity": """
**Productivity PWA Optimizations:**

```typescript
// Document handling optimization
const productivityOptimizer = {
  setupVirtualScrolling: () => {
    // Implement virtual scrolling for large documents
    const container = document.querySelector('.document-container');
    if (!container) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.loadDocumentSection(entry.target);
        } else {
          this.unloadDocumentSection(entry.target);
        }
      });
    });

    document.querySelectorAll('.document-section').forEach(section => {
      observer.observe(section);
    });
  },

  optimizeAutoSave: () => {
    let saveTimeout;
    const debouncedSave = () => {
      clearTimeout(saveTimeout);
      saveTimeout = setTimeout(() => {
        this.saveDocument();
      }, 2000);
    };

    document.addEventListener('input', debouncedSave);
  }
};
```""",
        "social": """
**Social PWA Optimizations:**

```typescript
// Feed optimization
const socialOptimizer = {
  setupInfiniteFeed: () => {
    const feedContainer = document.querySelector('.feed');
    let loading = false;

    const loadMorePosts = async () => {
      if (loading) return;
      loading = true;

      try {
        const posts = await this.fetchMorePosts();
        this.appendPosts(posts);
      } finally {
        loading = false;
      }
    };

    // Intersection observer for infinite scroll
    const sentinel = document.querySelector('.feed-sentinel');
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        loadMorePosts();
      }
    });

    observer.observe(sentinel);
  },

  optimizeImageUploads: () => {
    const uploadInput = document.querySelector('input[type="file"]');
    uploadInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/')) {
        this.compressImage(file).then(compressedFile => {
          this.uploadImage(compressedFile);
        });
      }
    });
  }
};
```"""
    }
    return optimizations.get(pwa_type, "// Generic PWA optimizations")


def _get_low_bandwidth_optimizations(pwa_type: str) -> str:
    """Возвращает оптимизации для медленных сетей."""
    optimizations = {
        "ecommerce": """
    // Disable non-essential product recommendations
    this.disableRecommendations();
    // Use low-quality product images
    this.switchToLowQualityImages();
    // Reduce checkout form complexity
    this.simplifyCheckout();""",
        "gaming": """
    // Reduce game asset quality
    this.setLowQualityAssets();
    // Disable particle effects
    this.disableEffects();
    // Reduce frame rate target
    this.setTargetFPS(30);""",
        "media": """
    // Switch to audio-only mode
    this.enableAudioOnlyMode();
    // Reduce video quality
    this.setVideoQuality('240p');
    // Disable autoplay
    this.disableAutoplay();""",
        "productivity": """
    // Disable real-time collaboration
    this.disableRealTimeSync();
    // Reduce autosave frequency
    this.setAutosaveInterval(60000);
    // Disable rich text formatting
    this.setPlainTextMode();""",
        "social": """
    // Load text-only posts
    this.enableTextOnlyMode();
    // Disable video autoplay
    this.disableVideoAutoplay();
    // Reduce feed refresh rate
    this.setRefreshInterval(30000);"""
    }
    return optimizations.get(pwa_type, "// Generic low bandwidth optimizations")


def _get_service_worker_vitals_integration(pwa_type: str) -> str:
    """Возвращает интеграцию Web Vitals в Service Worker."""
    return f"""
// Service Worker Web Vitals integration for {pwa_type} PWA
self.addEventListener('message', (event) => {{
  if (event.data && event.data.type === 'WEB_VITALS') {{
    // Store vitals data in IndexedDB
    storeVitalsData(event.data.vitals);

    // Send to background sync if offline
    if (!navigator.onLine) {{
      event.waitUntil(
        self.registration.sync.register('vitals-sync')
      );
    }}
  }}
}});

self.addEventListener('sync', (event) => {{
  if (event.tag === 'vitals-sync') {{
    event.waitUntil(syncVitalsData());
  }}
}});

async function storeVitalsData(vitals) {{
  const db = await openVitalsDB();
  const tx = db.transaction('vitals', 'readwrite');
  const store = tx.objectStore('vitals');
  await store.add({{
    ...vitals,
    timestamp: Date.now(),
    synced: false
  }});
}}
"""


def _get_success_metrics(pwa_type: str) -> str:
    """Возвращает метрики успеха для типа PWA."""
    metrics = {
        "ecommerce": """
**E-commerce Success Metrics:**
- 🛒 **Conversion Rate**: +15% improvement target
- ⚡ **LCP < 2.0s**: Critical for product page performance
- 🎯 **INP < 150ms**: Smooth add-to-cart interactions
- 📱 **Mobile Performance Score**: 90+ on Lighthouse
- 💳 **Checkout Completion**: 95%+ success rate""",
        "gaming": """
**Gaming Success Metrics:**
- 🎮 **Input Latency**: < 50ms for controls
- 📈 **Frame Rate**: Stable 60 FPS target
- ⚡ **LCP < 1.5s**: Fast game loading
- 🚀 **Memory Usage**: < 256MB on mobile
- 🎯 **Engagement**: 80%+ session completion""",
        "media": """
**Media Success Metrics:**
- 📺 **Video Start Time**: < 2s playback initiation
- ⚡ **LCP < 2.5s**: Content preview loading
- 📱 **Buffer Rate**: < 5% buffering time
- 🎯 **Completion Rate**: 85%+ content consumption
- 📊 **Quality Adaptation**: Smooth quality transitions""",
        "productivity": """
**Productivity Success Metrics:**
- 📝 **Document Load**: < 2s for 10MB files
- ⚡ **LCP < 2.0s**: Fast workspace loading
- 💾 **Auto-save**: < 500ms save operations
- 🔄 **Sync Reliability**: 99.9% data consistency
- 🎯 **User Efficiency**: 25% faster task completion""",
        "social": """
**Social Success Metrics:**
- 📱 **Feed Load**: < 1.5s initial content
- ⚡ **LCP < 2.0s**: Fast timeline rendering
- 💬 **Post Interaction**: < 200ms response time
- 🔄 **Real-time Updates**: < 1s notification delivery
- 🎯 **Engagement**: 60%+ daily active users"""
    }
    return metrics.get(pwa_type, "// Generic success metrics")


def _get_adaptive_threshold(metric: str, pwa_type: str) -> int:
    """Возвращает адаптивные пороги для метрик Web Vitals."""
    thresholds = {
        "gaming": {"lcp": 2000, "fid": 50, "cls": 0.05},
        "ecommerce": {"lcp": 2500, "fid": 100, "cls": 0.1},
        "media": {"lcp": 3000, "fid": 100, "cls": 0.1},
        "productivity": {"lcp": 2500, "fid": 100, "cls": 0.1},
        "social": {"lcp": 2500, "fid": 100, "cls": 0.1}
    }
    return thresholds.get(pwa_type, thresholds["ecommerce"])[metric]


def _get_eviction_strategy(pwa_type: str) -> str:
    """Возвращает стратегию вытеснения кэша для типа PWA."""
    strategies = {
        "ecommerce": """
    // E-commerce: Prioritize product and checkout pages
    const priorityOrder = ['product-', 'checkout-', 'cart-', 'category-', 'static-'];
    for (const priority of priorityOrder) {
      for (const cacheName of cacheNames) {
        if (cacheName.includes(priority)) {
          // Keep high-priority caches longer
          continue;
        }
      }
    }""",
        "gaming": """
    // Gaming: Prioritize game assets and core engine
    const preservePatterns = ['/game-engine/', '/critical-assets/', '/ui-core/'];
    const evictPatterns = ['/optional-assets/', '/audio-effects/', '/textures-hd/'];""",
        "media": """
    // Media: Prioritize recently accessed content
    const mediaAssets = requests.filter(req =>
      req.url.includes('/media/') || req.url.includes('/images/')
    );
    // Evict oldest media first""",
        "productivity": """
    // Productivity: Prioritize documents and workspace
    const workspaceData = requests.filter(req =>
      req.url.includes('/documents/') || req.url.includes('/workspace/')
    );
    // Keep recent work, evict old temp files""",
        "social": """
    // Social: Prioritize user content and feeds
    const userContent = requests.filter(req =>
      req.url.includes('/profile/') || req.url.includes('/posts/')
    );
    // Evict old feed data first"""
    }
    return strategies.get(pwa_type, "// Generic LRU eviction")


def _get_priority_sorting(pwa_type: str) -> str:
    """Возвращает алгоритм сортировки по приоритету для типа PWA."""
    sorting = {
        "ecommerce": """
    return requests.sort((a, b) => {
      // Product pages have highest priority
      const aScore = this.getEcommercePriority(a.url);
      const bScore = this.getEcommercePriority(b.url);
      return bScore - aScore;
    });

    private getEcommercePriority(url: string): number {
      if (url.includes('/product/')) return 100;
      if (url.includes('/checkout/')) return 90;
      if (url.includes('/cart/')) return 80;
      if (url.includes('/category/')) return 70;
      return 10;
    }""",
        "gaming": """
    return requests.sort((a, b) => {
      const aScore = this.getGamingPriority(a.url);
      const bScore = this.getGamingPriority(b.url);
      return bScore - aScore;
    });

    private getGamingPriority(url: string): number {
      if (url.includes('/game-engine/')) return 100;
      if (url.includes('/critical-assets/')) return 90;
      if (url.includes('/ui-core/')) return 80;
      if (url.includes('/sounds/')) return 50;
      return 10;
    }""",
        "media": """
    return requests.sort((a, b) => {
      const aScore = this.getMediaPriority(a.url);
      const bScore = this.getMediaPriority(b.url);
      return bScore - aScore;
    });

    private getMediaPriority(url: string): number {
      if (url.includes('/video/') && url.includes('quality=hd')) return 100;
      if (url.includes('/images/') && url.includes('thumbnail')) return 90;
      if (url.includes('/audio/')) return 70;
      return 10;
    }""",
        "productivity": """
    return requests.sort((a, b) => {
      const aScore = this.getProductivityPriority(a.url);
      const bScore = this.getProductivityPriority(b.url);
      return bScore - aScore;
    });

    private getProductivityPriority(url: string): number {
      if (url.includes('/documents/recent/')) return 100;
      if (url.includes('/workspace/')) return 90;
      if (url.includes('/templates/')) return 70;
      if (url.includes('/temp/')) return 10;
      return 50;
    }""",
        "social": """
    return requests.sort((a, b) => {
      const aScore = this.getSocialPriority(a.url);
      const bScore = this.getSocialPriority(b.url);
      return bScore - aScore;
    });

    private getSocialPriority(url: string): number {
      if (url.includes('/profile/me/')) return 100;
      if (url.includes('/feed/recent/')) return 90;
      if (url.includes('/messages/')) return 80;
      if (url.includes('/feed/old/')) return 30;
      return 50;
    }"""
    }
    return sorting.get(pwa_type, "return requests; // No special sorting")


def _get_lcp_cache_optimization(pwa_type: str) -> str:
    """Возвращает оптимизацию кэша для LCP."""
    optimizations = {
        "ecommerce": """
    // Cache critical product images with high priority
    const criticalImages = ['/hero-images/', '/product-primary/'];
    await this.precacheResources(criticalImages, 'critical-images-v1');""",
        "gaming": """
    // Cache game loading screen and core assets
    const gameCore = ['/splash-screen/', '/game-engine/', '/ui-framework/'];
    await this.precacheResources(gameCore, 'game-core-v1');""",
        "media": """
    // Cache video thumbnails and preview images
    const mediaPreviews = ['/thumbnails/', '/preview-images/', '/poster-frames/'];
    await this.precacheResources(mediaPreviews, 'media-previews-v1');""",
        "productivity": """
    // Cache workspace UI and recent documents
    const workspaceAssets = ['/workspace-ui/', '/document-templates/', '/recent-docs/'];
    await this.precacheResources(workspaceAssets, 'workspace-v1');""",
        "social": """
    // Cache profile images and feed UI
    const socialAssets = ['/profile-images/', '/feed-ui/', '/avatar-cache/'];
    await this.precacheResources(socialAssets, 'social-ui-v1');"""
    }
    return optimizations.get(pwa_type, "// Generic LCP cache optimization")


def _get_fid_cache_optimization(pwa_type: str) -> str:
    """Возвращает оптимизацию кэша для FID."""
    optimizations = {
        "ecommerce": """
    // Cache JavaScript bundles for faster interactions
    await this.updateCacheStrategy('stale-while-revalidate', ['/js/cart.js', '/js/checkout.js']);""",
        "gaming": """
    // Cache game scripts with immediate availability
    await this.updateCacheStrategy('cache-first', ['/js/game-engine.js', '/js/input-handlers.js']);""",
        "media": """
    // Cache media controls and player scripts
    await this.updateCacheStrategy('stale-while-revalidate', ['/js/media-player.js', '/js/controls.js']);""",
        "productivity": """
    // Cache editor scripts and workspace tools
    await this.updateCacheStrategy('cache-first', ['/js/editor.js', '/js/workspace.js']);""",
        "social": """
    // Cache interaction scripts (like, share, comment)
    await this.updateCacheStrategy('stale-while-revalidate', ['/js/social-actions.js', '/js/feed.js']);"""
    }
    return optimizations.get(pwa_type, "// Generic FID cache optimization")


def _get_cls_cache_optimization(pwa_type: str) -> str:
    """Возвращает оптимизацию кэша для CLS."""
    optimizations = {
        "ecommerce": """
    // Preload critical CSS to prevent layout shifts
    await this.precacheResources(['/css/product-layout.css', '/css/cart-layout.css'], 'layout-css-v1');""",
        "gaming": """
    // Preload game UI CSS and ensure stable layouts
    await this.precacheResources(['/css/game-ui.css', '/css/hud-layout.css'], 'game-layout-v1');""",
        "media": """
    // Preload media player CSS and video container styles
    await this.precacheResources(['/css/media-player.css', '/css/video-layout.css'], 'media-layout-v1');""",
        "productivity": """
    // Preload workspace CSS and document styles
    await this.precacheResources(['/css/workspace.css', '/css/document-view.css'], 'workspace-layout-v1');""",
        "social": """
    // Preload feed CSS and post layout styles
    await this.precacheResources(['/css/feed-layout.css', '/css/post-styles.css'], 'social-layout-v1');"""
    }
    return optimizations.get(pwa_type, "// Generic CLS cache optimization")


def _get_cache_recommendations(pwa_type: str) -> str:
    """Возвращает рекомендации по кэшированию для типа PWA."""
    recommendations = {
        "ecommerce": """
    report.push('💡 E-commerce Recommendations:');
    report.push('- Cache product images aggressively');
    report.push('- Use stale-while-revalidate for cart data');
    report.push('- Preload checkout flow assets');""",
        "gaming": """
    report.push('💡 Gaming Recommendations:');
    report.push('- Cache game assets with cache-first');
    report.push('- Minimize cache eviction during gameplay');
    report.push('- Preload next level assets');""",
        "media": """
    report.push('💡 Media Recommendations:');
    report.push('- Cache video thumbnails aggressively');
    report.push('- Use adaptive bitrate caching');
    report.push('- Clean old media cache regularly');""",
        "productivity": """
    report.push('💡 Productivity Recommendations:');
    report.push('- Cache recent documents offline');
    report.push('- Sync workspace changes frequently');
    report.push('- Preload collaboration tools');""",
        "social": """
    report.push('💡 Social Recommendations:');
    report.push('- Cache user profiles and avatars');
    report.push('- Use background sync for posts');
    report.push('- Limit feed cache to recent content');"""
    }
    return recommendations.get(pwa_type, "report.push('💡 General cache recommendations');")


def _get_pwa_cache_strategies(pwa_type: str) -> str:
    """Возвращает специфичные стратегии кэширования для типа PWA."""
    strategies = {
        "ecommerce": """
**E-commerce Cache Strategy:**

```typescript
const ecommerceStrategy = {
  '/api/products/': 'stale-while-revalidate', // Product data freshness
  '/images/products/': 'cache-first',         // Product images
  '/api/cart/': 'network-first',              // Cart always fresh
  '/api/checkout/': 'network-only',           // Critical checkout data
  '/static/': 'cache-first',                  // Static assets
  '/api/inventory/': 'network-first'          // Inventory updates
};
```""",
        "gaming": """
**Gaming Cache Strategy:**

```typescript
const gamingStrategy = {
  '/game-assets/': 'cache-first',      // Game assets never change
  '/api/save-game/': 'network-first',  // Save data critical
  '/api/leaderboard/': 'stale-while-revalidate', // Leaderboard updates
  '/audio/': 'cache-first',            // Audio assets
  '/textures/': 'cache-first',         // Visual assets
  '/api/achievements/': 'network-first' // Achievement progress
};
```""",
        "media": """
**Media Cache Strategy:**

```typescript
const mediaStrategy = {
  '/videos/': 'cache-first',           // Video content
  '/api/playlist/': 'stale-while-revalidate', // Playlist updates
  '/thumbnails/': 'cache-first',       // Thumbnail images
  '/api/progress/': 'network-first',   // Viewing progress
  '/subtitles/': 'cache-first',        // Subtitle files
  '/api/recommendations/': 'network-first' // Fresh recommendations
};
```""",
        "productivity": """
**Productivity Cache Strategy:**

```typescript
const productivityStrategy = {
  '/documents/': 'network-first',      // Document freshness
  '/api/sync/': 'network-only',        // Real-time sync
  '/templates/': 'cache-first',        // Document templates
  '/api/collaborate/': 'network-first', // Collaboration data
  '/assets/icons/': 'cache-first',     // UI assets
  '/api/autosave/': 'network-first'    // Auto-save data
};
```""",
        "social": """
**Social Cache Strategy:**

```typescript
const socialStrategy = {
  '/api/feed/': 'network-first',       // Fresh feed content
  '/api/posts/': 'stale-while-revalidate', // Posts with updates
  '/images/avatars/': 'cache-first',   // Profile images
  '/api/messages/': 'network-first',   // Real-time messages
  '/api/notifications/': 'network-first', // Live notifications
  '/static/': 'cache-first'            // Static assets
};
```"""
    }
    return strategies.get(pwa_type, "// Generic cache strategy")


def _get_service_worker_adaptive_integration(pwa_type: str) -> str:
    """Возвращает интеграцию адаптивного кэширования в Service Worker."""
    return f"""
// Adaptive caching integration for {pwa_type} PWA
import {{ AdaptiveCacheManager }} from './adaptive-cache-manager';

const cacheManager = new AdaptiveCacheManager({{
  pwaType: '{pwa_type}',
  maxCacheSize: 50 * 1024 * 1024 // 50MB
}});

self.addEventListener('fetch', (event) => {{
  const {{ request }} = event;

  // Apply adaptive caching strategy
  event.respondWith(
    caches.match(request).then(async (cachedResponse) => {{
      if (cachedResponse) {{
        await cacheManager.trackCacheHit(request);
        return cachedResponse;
      }}

      await cacheManager.trackCacheMiss(request);

      const response = await fetch(request);

      // Store with adaptive strategy
      const strategy = await cacheManager.getOptimalStrategy(request);
      await cacheManager.store(request, response.clone(), strategy);

      return response;
    }})
  );
}});

// Periodic cache optimization
setInterval(async () => {{
  await cacheManager.performOptimization();
}}, 5 * 60 * 1000); // Every 5 minutes
"""


def _get_cache_optimization_targets(pwa_type: str) -> str:
    """Возвращает целевые показатели оптимизации кэша."""
    targets = {
        "ecommerce": """
**E-commerce Cache Targets:**
- 🎯 **Cache Hit Rate**: 85%+ for product pages
- ⚡ **Product Image Load**: < 500ms from cache
- 🛒 **Cart Response**: < 200ms for cached data
- 📊 **Conversion Optimization**: 15% improvement target
- 💾 **Storage Efficiency**: < 30MB for core assets""",
        "gaming": """
**Gaming Cache Targets:**
- 🎯 **Asset Hit Rate**: 95%+ for game resources
- ⚡ **Game Start Time**: < 3s from cache
- 🎮 **Level Load**: < 1s for cached levels
- 📊 **Memory Efficiency**: < 128MB cache usage
- 🚀 **Performance**: 60 FPS sustained""",
        "media": """
**Media Cache Targets:**
- 🎯 **Content Hit Rate**: 80%+ for thumbnails
- ⚡ **Video Start**: < 2s for cached content
- 📺 **Thumbnail Load**: < 300ms
- 📊 **Storage Management**: Adaptive quality caching
- 🎵 **Audio Streaming**: 99% cache availability""",
        "productivity": """
**Productivity Cache Targets:**
- 🎯 **Document Hit Rate**: 90%+ for recent files
- ⚡ **Workspace Load**: < 1.5s from cache
- 📝 **Auto-save**: < 500ms response time
- 📊 **Sync Efficiency**: 99.9% data consistency
- 💾 **Storage Optimization**: Smart document caching""",
        "social": """
**Social Cache Targets:**
- 🎯 **Feed Hit Rate**: 75%+ for recent content
- ⚡ **Profile Load**: < 1s for cached profiles
- 💬 **Message Response**: < 200ms
- 📊 **Engagement**: 40% faster interactions
- 🔄 **Real-time Sync**: < 1s notification delivery"""
    }
    return targets.get(pwa_type, "// Generic cache targets")


def _get_active_handling_for_type(pwa_type: str) -> str:
    """Возвращает обработку active состояния для типа PWA."""
    handlers = {
        "ecommerce": """
    // E-commerce active handling
    // Возобновляем price updates
    this.resumePriceUpdates();

    // Синхронизируем корзину с сервером
    this.syncCartWithServer();

    // Проверяем inventory changes
    this.checkInventoryUpdates();""",
        "productivity": """
    // Productivity active handling
    // Возобновляем collaboration sync
    this.resumeCollaborationSync();

    // Проверяем conflicts в документах
    this.checkDocumentConflicts();

    // Синхронизируем changes
    this.syncPendingChanges();""",
        "social": """
    // Social active handling
    // Обновляем статус на "online"
    this.updatePresenceStatus('online');

    // Возобновляем real-time updates
    this.resumeFeedPolling();

    // Синхронизируем missed messages
    this.syncMissedMessages();""",
        "media": """
    // Media active handling
    // Возобновляем autoplay если было
    this.resumeAutoplayIfNeeded();

    // Возобновляем content preloading
    this.resumeContentPreloading();

    // Синхронизируем reading progress
    this.syncReadingProgress();"""
    }
    return handlers.get(pwa_type, "// Generic active handling")


def _get_idle_use_cases_for_type(pwa_type: str) -> str:
    """Возвращает случаи использования Idle Detection API для типа PWA."""
    use_cases = {
        "ecommerce": """
- Auto-save shopping cart
- Pause real-time price updates
- Reduce inventory polling frequency
- Show "away" status for live chat
- Battery optimization for mobile shopping""",
        "productivity": """
- Auto-save documents and work state
- Pause collaborative real-time features
- Backup current session
- Reduce sync frequency
- Optimize for battery during breaks""",
        "social": """
- Update presence status to "away"
- Pause typing indicators
- Reduce feed polling
- Batch notification delivery
- Optimize battery for background mode""",
        "media": """
- Pause autoplay sequences
- Save reading/viewing progress
- Reduce content preloading
- Pause live stream buffering
- Battery optimization for long sessions"""
    }
    return use_cases.get(pwa_type, "- Battery optimization\n- Reduce background activity\n- Auto-save state")


def _get_web_locks_use_cases_for_type(pwa_type: str) -> str:
    """Возвращает случаи использования Web Locks API для типа PWA."""
    use_cases = {
        "productivity": """
- Prevent concurrent document editing
- Coordinate multi-tab data sync
- Ensure atomic save operations
- Manage shared resource access
- Prevent race conditions in collaborative features""",
        "general": """
- Coordinate between multiple tabs
- Prevent duplicate background sync
- Manage shared localStorage access
- Ensure data consistency
- Control resource-intensive operations"""
    }
    return use_cases.get(pwa_type, "- Basic multi-tab coordination\n- Prevent duplicate operations")


def _generate_offline_sync_code(deps: PWAMobileAgentDependencies, data_type: str) -> str:
    """Генерирует код для offline синхронизации."""
    return f"""
## Offline Storage для {deps.pwa_type}

### IndexedDB Schema
```typescript
interface {deps.pwa_type.title()}Data {{
  id: string;
  data: any;
  timestamp: number;
  syncStatus: 'synced' | 'pending' | 'failed';
  lastModified: number;
}}

class OfflineDatabase extends Dexie {{
  {data_type}!: Table<{deps.pwa_type.title()}Data>;

  constructor() {{
    super('{deps.pwa_type}OfflineDB');
    this.version(1).stores({{
      {data_type}: 'id, timestamp, syncStatus, lastModified'
    }});
  }}
}}
```

### Sync Manager
```typescript
export class {deps.pwa_type.title()}SyncManager {{
  private db = new OfflineDatabase();

  async sync{data_type.title()}() {{
    const pendingItems = await this.db.{data_type}
      .where('syncStatus').equals('pending')
      .toArray();

    for (const item of pendingItems) {{
      try {{
        const response = await fetch('/api/{data_type}', {{
          method: 'POST',
          body: JSON.stringify(item.data),
          headers: {{ 'Content-Type': 'application/json' }}
        }});

        if (response.ok) {{
          await this.db.{data_type}.update(item.id, {{
            syncStatus: 'synced',
            lastModified: Date.now()
          }});
        }}
      }} catch (error) {{
        await this.db.{data_type}.update(item.id, {{ syncStatus: 'failed' }});
      }}
    }}
  }}

  async cache{data_type.title()}(item: any) {{
    await this.db.{data_type}.put({{
      id: item.id,
      data: item,
      timestamp: Date.now(),
      syncStatus: navigator.onLine ? 'synced' : 'pending',
      lastModified: Date.now()
    }});
  }}

  async get{data_type.title()}() {{
    return await this.db.{data_type}
      .orderBy('lastModified')
      .reverse()
      .toArray();
  }}
}}
```

### Network Status Hook
```typescript
export function useNetworkStatus() {{
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const syncManager = new {deps.pwa_type.title()}SyncManager();

  useEffect(() => {{
    const handleOnline = () => {{
      setIsOnline(true);
      syncManager.sync{data_type.title()}(); // Auto-sync when back online
    }};

    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {{
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    }};
  }}, []);

  return {{ isOnline, syncManager }};
}}
```

### Conflict Resolution Strategy
```typescript
export async function resolveConflict(local: any, remote: any) {{
  // {deps.pwa_type} specific conflict resolution
  if (local.lastModified > remote.lastModified) {{
    return local; // Local wins (last-write-wins)
  }}

  // For {deps.pwa_type}, prefer server data
  return remote;
}}
```
"""


# ===== SECURITY ENHANCEMENTS =====

async def implement_csp_generation(
    ctx: RunContext[PWAMobileAgentDependencies],
    security_level: str = "strict"
) -> str:
    """
    Генерирует Content Security Policy для PWA приложения.

    Args:
        security_level: Уровень безопасности - strict, moderate, permissive

    Returns:
        CSP конфигурация с headers и meta tags
    """
    try:
        # Валидация входных параметров
        if not ctx or not hasattr(ctx, 'deps'):
            raise ValueError("Некорректный контекст: отсутствуют зависимости")

        deps = ctx.deps

        # Валидация security_level
        valid_levels = ["strict", "moderate", "permissive"]
        if security_level not in valid_levels:
            raise ValueError(f"Недопустимый уровень безопасности '{security_level}'. Доступные: {valid_levels}")

        # Валидация pwa_type
        if not hasattr(deps, 'pwa_type') or not deps.pwa_type:
            raise ValueError("Тип PWA не определен в зависимостях")

        # Базовые CSP директивы с обработкой ошибок
        try:
            csp_config = _generate_base_csp_config(deps, security_level)
        except Exception as e:
            raise RuntimeError(f"Ошибка генерации базовой CSP конфигурации: {e}")

        # Специфичные для типа PWA настройки с обработкой ошибок
        try:
            type_specific_csp = _get_type_specific_csp(deps.pwa_type, security_level)
            csp_config.update(type_specific_csp)
        except Exception as e:
            # Если type-specific CSP не удалось сгенерировать, продолжаем с базовой конфигурацией
            print(f"Предупреждение: не удалось загрузить type-specific CSP: {e}")

        # Nonce generation для inline scripts с обработкой ошибок
        try:
            nonce_config = _generate_nonce_configuration()
        except Exception as e:
            # Если nonce конфигурация не удалась, используем стандартную
            nonce_config = {"enabled": False, "fallback": True}
            print(f"Предупреждение: не удалось сгенерировать nonce конфигурацию: {e}")

    except Exception as e:
        # Критическая ошибка - возвращаем базовую безопасную CSP
        return f"""
# ОШИБКА CSP ГЕНЕРАЦИИ: {e}

## Fallback CSP Configuration

### Базовая безопасная CSP
```apache
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; media-src 'self'; frame-src 'none';
```

### Рекомендации
1. Проверьте корректность входных параметров
2. Убедитесь, что все зависимости инициализированы
3. Обратитесь к документации для настройки специфичных правил

### Устранение неисправностей
- Проверьте тип PWA: должен быть одним из допустимых значений
- Убедитесь, что уровень безопасности корректен: strict/moderate/permissive
- Проверьте наличие всех необходимых зависимостей в контексте
"""

    return f"""
# Content Security Policy для {deps.pwa_type} PWA

## CSP Header Configuration

### HTTP Headers
```apache
Content-Security-Policy: {_build_csp_header(csp_config)}
Content-Security-Policy-Report-Only: {_build_csp_header(csp_config, report_only=True)}
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### HTML Meta Tags
```html
<meta http-equiv="Content-Security-Policy" content="{_build_csp_header(csp_config)}">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="DENY">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
```

## CSP Configuration Details

### Security Level: {security_level.upper()}
{_get_security_level_description(security_level)}

### Type-Specific Rules for {deps.pwa_type}:
{_get_type_csp_description(deps.pwa_type)}

## Nonce Implementation

### Server-side (Node.js/Express)
```javascript
const crypto = require('crypto');

app.use((req, res, next) => {{
  res.locals.nonce = crypto.randomBytes(16).toString('base64');
  res.setHeader('Content-Security-Policy',
    `script-src 'self' 'nonce-${{res.locals.nonce}}'; object-src 'none';`);
  next();
}});
```

### Client-side Usage
```html
<script nonce="{{{{nonce}}}}">
  // Inline scripts with nonce
  console.log('Secure inline script');
</script>
```

## CSP Violation Reporting

### Report Endpoint Setup
```javascript
app.post('/csp-violation-report', (req, res) => {{
  console.log('CSP Violation:', req.body);
  // Log to security monitoring system
  res.status(204).end();
}});
```

### Report URI in CSP
```
report-uri /csp-violation-report;
report-to csp-endpoint;
```

## Testing & Deployment

### Development Mode
- Use `Content-Security-Policy-Report-Only` для тестирования
- Мониторьте violations в dev tools
- Постепенно ужесточайте политику

### Production Deployment
- Активируйте полную CSP защиту
- Настройте централизованный logging нарушений
- Регулярно анализируйте reports

### Security Audit Commands
```bash
# Тестирование CSP
curl -H "Content-Security-Policy-Report-Only: ..." https://yourapp.com

# Анализ security headers
curl -I https://yourapp.com | grep -i security
```
"""


async def implement_secure_storage(
    ctx: RunContext[PWAMobileAgentDependencies],
    storage_type: str = "sensitive"
) -> str:
    """
    Реализует secure storage patterns для PWA.

    Args:
        storage_type: Тип данных - sensitive, credentials, user_data

    Returns:
        Secure storage implementation с шифрованием
    """
    deps = ctx.deps

    return f"""
# Secure Storage для {deps.pwa_type} PWA

## Web Crypto API Implementation

### Encryption Service
```typescript
class SecureStorage {{
  private keyPromise: Promise<CryptoKey>;

  constructor() {{
    this.keyPromise = this.generateOrRetrieveKey();
  }}

  private async generateOrRetrieveKey(): Promise<CryptoKey> {{
    // Используем пароль пользователя или биометрию для ключа
    const password = await this.getUserCredentials();
    const encoder = new TextEncoder();
    const data = encoder.encode(password);

    const hash = await crypto.subtle.digest('SHA-256', data);

    return crypto.subtle.importKey(
      'raw',
      hash,
      {{ name: 'AES-GCM', length: 256 }},
      false,
      ['encrypt', 'decrypt']
    );
  }}

  async encrypt(data: any): Promise<string> {{
    const key = await this.keyPromise;
    const encoder = new TextEncoder();
    const encodedData = encoder.encode(JSON.stringify(data));

    const iv = crypto.getRandomValues(new Uint8Array(12));
    const encryptedData = await crypto.subtle.encrypt(
      {{ name: 'AES-GCM', iv }},
      key,
      encodedData
    );

    // Комбинируем IV и encrypted data
    const combined = new Uint8Array(iv.length + encryptedData.byteLength);
    combined.set(iv);
    combined.set(new Uint8Array(encryptedData), iv.length);

    return btoa(String.fromCharCode(...combined));
  }}

  async decrypt(encryptedString: string): Promise<any> {{
    const key = await this.keyPromise;
    const combined = new Uint8Array(
      atob(encryptedString).split('').map(c => c.charCodeAt(0))
    );

    const iv = combined.slice(0, 12);
    const data = combined.slice(12);

    const decryptedData = await crypto.subtle.decrypt(
      {{ name: 'AES-GCM', iv }},
      key,
      data
    );

    const decoder = new TextDecoder();
    return JSON.parse(decoder.decode(decryptedData));
  }}

  private async getUserCredentials(): Promise<string> {{
    // {deps.pwa_type}-specific credential strategy
    {_get_credential_strategy(deps.pwa_type)}
  }}
}}
```

### Secure localStorage Wrapper
```typescript
class SecureLocalStorage {{
  private storage: SecureStorage;

  constructor() {{
    this.storage = new SecureStorage();
  }}

  async setItem(key: string, value: any): Promise<void> {{
    const encrypted = await this.storage.encrypt(value);
    localStorage.setItem(`secure_${{key}}`, encrypted);
  }}

  async getItem(key: string): Promise<any> {{
    const encrypted = localStorage.getItem(`secure_${{key}}`);
    if (!encrypted) return null;

    try {{
      return await this.storage.decrypt(encrypted);
    }} catch (error) {{
      console.error('Decryption failed:', error);
      return null;
    }}
  }}

  removeItem(key: string): void {{
    localStorage.removeItem(`secure_${{key}}`);
  }}

  clear(): void {{
    Object.keys(localStorage)
      .filter(key => key.startsWith('secure_'))
      .forEach(key => localStorage.removeItem(key));
  }}
}}
```

## Biometric Authentication Integration

### WebAuthn Implementation
```typescript
class BiometricAuth {{
  async registerCredential(username: string): Promise<boolean> {{
    try {{
      const credential = await navigator.credentials.create({{
        publicKey: {{
          challenge: crypto.getRandomValues(new Uint8Array(32)),
          rp: {{
            name: "{deps.app_name}",
            id: window.location.hostname,
          }},
          user: {{
            id: new TextEncoder().encode(username),
            name: username,
            displayName: username,
          }},
          pubKeyCredParams: [{{alg: -7, type: "public-key"}}],
          authenticatorSelection: {{
            authenticatorAttachment: "platform",
            userVerification: "required"
          }},
          timeout: 60000,
          attestation: "direct"
        }}
      }});

      // Сохраняем credential ID
      await this.storeCredentialId(credential.id);
      return true;
    }} catch (error) {{
      console.error('Biometric registration failed:', error);
      return false;
    }}
  }}

  async authenticate(): Promise<boolean> {{
    try {{
      const credentialId = await this.getStoredCredentialId();
      if (!credentialId) return false;

      const assertion = await navigator.credentials.get({{
        publicKey: {{
          challenge: crypto.getRandomValues(new Uint8Array(32)),
          allowCredentials: [{{
            id: credentialId,
            type: 'public-key'
          }}],
          userVerification: 'required'
        }}
      }});

      return assertion !== null;
    }} catch (error) {{
      console.error('Biometric authentication failed:', error);
      return false;
    }}
  }}

  private async storeCredentialId(id: string): Promise<void> {{
    const secureStorage = new SecureLocalStorage();
    await secureStorage.setItem('biometric_credential_id', id);
  }}

  private async getStoredCredentialId(): Promise<ArrayBuffer | null> {{
    const secureStorage = new SecureLocalStorage();
    const stored = await secureStorage.getItem('biometric_credential_id');
    return stored ? new TextEncoder().encode(stored) : null;
  }}
}}
```

## Token Management System

### JWT Token Rotation
```typescript
class TokenManager {{
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  private tokenRefreshTimer: NodeJS.Timeout | null = null;

  constructor(private secureStorage: SecureLocalStorage) {{
    this.loadTokens();
  }}

  async setTokens(access: string, refresh: string): Promise<void> {{
    this.accessToken = access;
    this.refreshToken = refresh;

    await this.secureStorage.setItem('access_token', access);
    await this.secureStorage.setItem('refresh_token', refresh);

    this.scheduleTokenRefresh();
  }}

  async getAccessToken(): Promise<string | null> {{
    if (!this.accessToken) {{
      this.accessToken = await this.secureStorage.getItem('access_token');
    }}

    return this.accessToken;
  }}

  private async loadTokens(): Promise<void> {{
    this.accessToken = await this.secureStorage.getItem('access_token');
    this.refreshToken = await this.secureStorage.getItem('refresh_token');

    if (this.accessToken) {{
      this.scheduleTokenRefresh();
    }}
  }}

  private scheduleTokenRefresh(): void {{
    if (this.tokenRefreshTimer) {{
      clearTimeout(this.tokenRefreshTimer);
    }}

    // Обновляем токен за 5 минут до истечения
    const payload = JSON.parse(atob(this.accessToken!.split('.')[1]));
    const expiresIn = (payload.exp * 1000) - Date.now() - (5 * 60 * 1000);

    this.tokenRefreshTimer = setTimeout(async () => {{
      await this.refreshAccessToken();
    }}, Math.max(expiresIn, 0));
  }}

  private async refreshAccessToken(): Promise<void> {{
    try {{
      const response = await fetch('/api/auth/refresh', {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
        }},
        body: JSON.stringify({{ refreshToken: this.refreshToken }})
      }});

      if (response.ok) {{
        const {{ accessToken, refreshToken }} = await response.json();
        await this.setTokens(accessToken, refreshToken);
      }} else {{
        await this.logout();
      }}
    }} catch (error) {{
      console.error('Token refresh failed:', error);
      await this.logout();
    }}
  }}

  async logout(): Promise<void> {{
    this.accessToken = null;
    this.refreshToken = null;

    if (this.tokenRefreshTimer) {{
      clearTimeout(this.tokenRefreshTimer);
    }}

    await this.secureStorage.removeItem('access_token');
    await this.secureStorage.removeItem('refresh_token');
  }}
}}
```

## Privacy-First Analytics

### Anonymous Usage Tracking
```typescript
class PrivacyAnalytics {{
  private sessionId: string;

  constructor() {{
    this.sessionId = this.generateAnonymousId();
  }}

  private generateAnonymousId(): string {{
    return crypto.randomUUID();
  }}

  trackEvent(event: string, data?: Record<string, any>): void {{
    // Отправляем только анонимные метрики
    const anonymousData = {{
      sessionId: this.sessionId,
      event,
      timestamp: Date.now(),
      appType: "{deps.pwa_type}",
      data: this.sanitizeData(data)
    }};

    // Не сохраняем личные данные локально
    this.sendAnalytics(anonymousData);
  }}

  private sanitizeData(data?: Record<string, any>): Record<string, any> {{
    if (!data) return {{}};

    // Удаляем личную информацию
    const sanitized = {{ ...data }};
    delete sanitized.email;
    delete sanitized.phone;
    delete sanitized.userId;
    delete sanitized.personalInfo;

    return sanitized;
  }}

  private sendAnalytics(data: Record<string, any>): void {{
    // Отправляем через secure endpoint
    fetch('/api/analytics', {{
      method: 'POST',
      headers: {{
        'Content-Type': 'application/json',
      }},
      body: JSON.stringify(data)
    }}).catch(() => {{
      // Игнорируем ошибки аналитики
    }});
  }}
}}
```

## Security Best Practices для {deps.pwa_type}

### 1. Data Minimization
- Собирайте только необходимые данные
- Регулярно очищайте неиспользуемые данные
- Используйте data retention policies

### 2. Transport Security
- Всегда используйте HTTPS
- Применяйте certificate pinning
- Валидируйте SSL certificates

### 3. Input Validation
- Sanitize все пользовательские входы
- Используйте type-safe validation
- Применяйте rate limiting

### 4. Error Handling
- Не раскрывайте sensitive information в errors
- Логируйте security events
- Используйте generic error messages

### Implementation Checklist:
- [ ] CSP headers настроены
- [ ] Secure storage реализован
- [ ] Biometric auth интегрирован
- [ ] Token rotation работает
- [ ] Privacy analytics настроены
- [ ] Security headers добавлены
- [ ] Input validation реализована
"""


async def implement_privacy_compliance(
    ctx: RunContext[PWAMobileAgentDependencies],
    regulation: str = "gdpr"
) -> str:
    """
    Реализует privacy compliance для PWA.

    Args:
        regulation: Тип регулирования - gdpr, ccpa, privacy_first

    Returns:
        Privacy compliance implementation
    """
    deps = ctx.deps

    return f"""
# Privacy Compliance для {deps.pwa_type} PWA

## {regulation.upper()} Compliance Implementation

### Cookie & Storage Consent Management
```typescript
class ConsentManager {{
  private consentData: Record<string, boolean> = {{}};

  constructor() {{
    this.loadConsent();
  }}

  async requestConsent(): Promise<void> {{
    const consent = await this.showConsentDialog();
    this.consentData = consent;
    await this.saveConsent();
    this.applyConsentSettings();
  }}

  private async showConsentDialog(): Promise<Record<string, boolean>> {{
    return new Promise((resolve) => {{
      const dialog = document.createElement('div');
      dialog.innerHTML = `
        <div class="consent-dialog">
          <h3>Privacy Settings</h3>
          <label>
            <input type="checkbox" id="essential" checked disabled>
            Essential cookies (required)
          </label>
          <label>
            <input type="checkbox" id="analytics">
            Analytics & Performance
          </label>
          <label>
            <input type="checkbox" id="marketing">
            Marketing & Personalization
          </label>
          <button onclick="acceptConsent()">Save Preferences</button>
          <button onclick="acceptAll()">Accept All</button>
        </div>
      `;

      document.body.appendChild(dialog);

      window.acceptConsent = () => {{
        const essential = true;
        const analytics = (document.getElementById('analytics') as HTMLInputElement).checked;
        const marketing = (document.getElementById('marketing') as HTMLInputElement).checked;

        document.body.removeChild(dialog);
        resolve({{ essential, analytics, marketing }});
      }};

      window.acceptAll = () => {{
        document.body.removeChild(dialog);
        resolve({{ essential: true, analytics: true, marketing: true }});
      }};
    }});
  }}

  private async saveConsent(): Promise<void> {{
    const secureStorage = new SecureLocalStorage();
    await secureStorage.setItem('privacy_consent', {{
      ...this.consentData,
      timestamp: Date.now(),
      version: "1.0"
    }});
  }}

  private async loadConsent(): Promise<void> {{
    const secureStorage = new SecureLocalStorage();
    const saved = await secureStorage.getItem('privacy_consent');
    if (saved) {{
      this.consentData = saved;
      this.applyConsentSettings();
    }}
  }}

  private applyConsentSettings(): void {{
    // Применяем настройки приватности
    if (!this.consentData.analytics) {{
      this.disableAnalytics();
    }}

    if (!this.consentData.marketing) {{
      this.disableMarketing();
    }}
  }}

  hasConsent(type: string): boolean {{
    return this.consentData[type] === true;
  }}
}}
```

## Implementation Checklist для {regulation.upper()}:
- [ ] Consent management система
- [ ] Data subject rights API
- [ ] Privacy-by-design storage
- [ ] Data retention policies
- [ ] Breach detection система
- [ ] Privacy notice интеграция
- [ ] Regular compliance audits
- [ ] Staff privacy training
"""


def _generate_base_csp_config(deps: PWAMobileAgentDependencies, security_level: str) -> Dict[str, List[str]]:
    """Генерирует базовую CSP конфигурацию."""
    base_config = {
        "default-src": ["'self'"],
        "script-src": ["'self'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:", "https:"],
        "font-src": ["'self'", "https:"],
        "connect-src": ["'self'"],
        "manifest-src": ["'self'"],
        "worker-src": ["'self'"],
        "object-src": ["'none'"],
        "base-uri": ["'self'"],
        "form-action": ["'self'"],
        "frame-ancestors": ["'none'"],
        "upgrade-insecure-requests": []
    }

    if security_level == "strict":
        base_config["script-src"] = ["'self'", "'nonce-{nonce}'"]
        base_config["style-src"] = ["'self'", "'nonce-{nonce}'"]
    elif security_level == "moderate":
        base_config["script-src"].append("'unsafe-eval'")
    elif security_level == "permissive":
        base_config["script-src"].extend(["'unsafe-inline'", "'unsafe-eval'"])

    return base_config


def _get_type_specific_csp(pwa_type: str, security_level: str) -> Dict[str, List[str]]:
    """Возвращает CSP настройки специфичные для типа PWA."""
    type_configs = {
        "ecommerce": {
            "connect-src": ["'self'", "https://api.stripe.com", "https://checkout.paypal.com"],
            "frame-src": ["https://checkout.paypal.com", "https://js.stripe.com"],
            "img-src": ["'self'", "data:", "https:", "https://cdn.shopify.com"]
        },
        "media": {
            "media-src": ["'self'", "https:", "blob:"],
            "img-src": ["'self'", "data:", "https:", "blob:"],
            "connect-src": ["'self'", "https:"]
        },
        "social": {
            "connect-src": ["'self'", "https://api.twitter.com", "https://graph.facebook.com"],
            "frame-src": ["https://platform.twitter.com", "https://www.facebook.com"],
            "img-src": ["'self'", "data:", "https:", "https://pbs.twimg.com"]
        }
    }

    return type_configs.get(pwa_type, {})


def _build_csp_header(config: Dict[str, List[str]], report_only: bool = False) -> str:
    """Строит CSP header строку."""
    directives = []
    for directive, sources in config.items():
        if sources:
            directives.append(f"{directive} {' '.join(sources)}")
        else:
            directives.append(directive)

    csp_string = "; ".join(directives)

    if report_only:
        csp_string += "; report-uri /csp-violation-report"

    return csp_string


def _get_security_level_description(level: str) -> str:
    """Возвращает описание уровня безопасности."""
    descriptions = {
        "strict": "Максимальная безопасность с nonce для всех inline элементов",
        "moderate": "Сбалансированная безопасность с ограниченным eval",
        "permissive": "Базовая защита с поддержкой legacy кода"
    }
    return descriptions.get(level, "Стандартная защита")


def _get_type_csp_description(pwa_type: str) -> str:
    """Возвращает описание CSP правил для типа PWA."""
    descriptions = {
        "ecommerce": "Разрешены payment gateways (Stripe, PayPal), CDN для продуктов",
        "media": "Поддержка video/audio streaming, blob URLs для медиа",
        "social": "Интеграция с социальными платформами, внешние CDN"
    }
    return descriptions.get(pwa_type, "Стандартные правила безопасности")


def _get_credential_strategy(pwa_type: str) -> str:
    """Возвращает стратегию получения credentials для типа PWA."""
    strategies = {
        "ecommerce": """
    // E-commerce: биометрия + PIN
    if (await BiometricAuth.isAvailable()) {
      return await BiometricAuth.authenticate();
    }
    return await promptForPIN();""",
        "productivity": """
    // Productivity: master password + 2FA
    const masterPassword = await promptForMasterPassword();
    const totpCode = await promptForTOTP();
    return `${masterPassword}:${totpCode}`;""",
        "social": """
    // Social: OAuth + device binding
    const oauthToken = await getOAuthToken();
    const deviceId = await getDeviceFingerprint();
    return `${oauthToken}:${deviceId}`;"""
    }
    return strategies.get(pwa_type, "return await promptForPassword();")


# Помощники для генерации nonce
def _generate_nonce_configuration() -> Dict[str, str]:
    """Генерирует конфигурацию для nonce."""
    return {
        "algorithm": "crypto.randomBytes(16).toString('base64')",
        "usage": "Для inline scripts и styles",
        "rotation": "Каждый запрос"
    }