# 📱 PWA & Cross-Platform Mobile Agent

**Универсальный агент для создания и оптимизации Progressive Web Apps (PWA) и кроссплатформенных мобильных приложений.**

Агент объединил возможности PWA и нативной мобильной разработки, адаптируясь под любой тип проекта. Поддерживает React Native, Flutter, Capacitor, Cordova и другие фреймворки.

## 🌟 Возможности

### 🎯 Универсальная поддержка проектов
- **E-commerce**: offline корзина, Payment API, push-уведомления о скидках
- **Media/News**: offline чтение, background sync, share API
- **Productivity**: offline редактирование, minimal UI, sync данных
- **Social**: camera API, geolocation, real-time sync
- **Gaming**: fullscreen mode, performance optimization, achievement system

### 🛠️ Инструменты разработки
- **PWA Manifest**: автоматическая генерация с адаптацией под тип проекта
- **Service Worker**: создание с оптимальными стратегиями кэширования
- **Mobile UX**: оптимизация интерфейса для мобильных устройств
- **Performance**: анализ и улучшение производительности
- **Offline Sync**: настройка синхронизации данных

### 🔧 Кроссплатформенная разработка
- **React Native**: настройка проектов и оптимизация для iOS/Android
- **Flutter**: создание универсальных приложений
- **Capacitor**: интеграция PWA с нативными возможностями
- **Cordova/PhoneGap**: поддержка legacy проектов
- **Electron**: desktop приложения из web технологий
- **Tauri**: современные desktop приложения на Rust
- **Ionic**: hybrid мобильные приложения

### 📱 Мобильные Web API
- **Push Notifications**: уведомления с rich content
- **Background Sync**: синхронизация в фоновом режиме
- **Camera API**: работа с камерой устройства
- **Geolocation**: определение местоположения
- **Share API**: нативный sharing
- **Payment API**: Web Payments для покупок
- **Storage**: IndexedDB, localStorage для offline работы

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
cp .env.example .env
# Отредактируйте .env с вашими настройками
```

### 3. Базовое использование

```python
from pwa_mobile_agent import run_pwa_mobile_analysis
from pwa_mobile_agent.examples.ecommerce_config import setup_ecommerce_pwa_agent

# Настройка для e-commerce проекта
deps = setup_ecommerce_pwa_agent()

# Анализ и оптимизация PWA
result = await run_pwa_mobile_analysis(
    context="Анализируй PWA для интернет-магазина",
    project_path="/path/to/project",
    pwa_type="ecommerce"
)
```

## 📋 Конфигурация

### Основные настройки (.env)

```env
# LLM Configuration
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen2.5-coder-32b-instruct

# PWA Application Settings
PWA_APP_NAME=My PWA Application
PWA_SHORT_NAME=MyPWA
PWA_DESCRIPTION=Progressive Web Application
PWA_THEME_COLOR=#000000
PWA_BACKGROUND_COLOR=#ffffff

# Performance Settings
PWA_MAX_CACHE_SIZE=50
PWA_CACHE_STRATEGY=adaptive

# Feature Flags
PWA_ENABLE_PUSH=true
PWA_ENABLE_BACKGROUND_SYNC=true
PWA_ENABLE_GEOLOCATION=false
PWA_ENABLE_CAMERA=false
PWA_ENABLE_SHARE=true
PWA_ENABLE_PAYMENT=false

# Archon Integration
ARCHON_URL=http://localhost:3737
ARCHON_PROJECT_ID=c75ef8e3-6f4d-4da2-9e81-8d38d04a341a
```

### Зависимости агента

```python
@dataclass
class PWAMobileAgentDependencies:
    # Основные настройки
    pwa_type: str = "general"  # general, ecommerce, media, productivity, social, gaming
    target_platform: str = "universal"  # universal, ios, android
    offline_strategy: str = "network-first"  # cache-first, network-first, stale-while-revalidate

    # PWA манифест
    app_name: str = "PWA Application"
    app_short_name: str = "PWA"
    app_description: str = "Progressive Web Application"
    theme_color: str = "#000000"
    background_color: str = "#ffffff"
    start_url: str = "/"
    display_mode: str = "standalone"  # fullscreen, standalone, minimal-ui, browser
    orientation: str = "portrait"  # portrait, landscape, any

    # Функциональность
    enable_push_notifications: bool = True
    enable_background_sync: bool = True
    enable_geolocation: bool = False
    enable_camera: bool = False
    enable_share_api: bool = True
    enable_payment_api: bool = False

    # Производительность
    cache_strategy: str = "adaptive"  # aggressive, conservative, adaptive
    max_cache_size_mb: int = 50
    image_optimization: bool = True
    lazy_loading: bool = True

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: ["pwa-mobile", "agent-knowledge"])
```

## 📚 Примеры конфигураций

### E-commerce PWA

```python
from pwa_mobile_agent.examples.ecommerce_config import setup_ecommerce_pwa_agent

deps = setup_ecommerce_pwa_agent()
# Настройки: offline корзина, Payment API, push для акций
```

### Media/News PWA

```python
from pwa_mobile_agent.examples.media_config import setup_news_pwa_agent

deps = setup_news_pwa_agent()
# Настройки: offline чтение, background sync новостей, share API
```

### Productivity PWA

```python
from pwa_mobile_agent.examples.productivity_config import setup_task_manager_pwa_agent

deps = setup_task_manager_pwa_agent()
# Настройки: offline редактирование, minimal UI, sync задач
```

### Social PWA

```python
from pwa_mobile_agent.examples.social_config import setup_social_network_pwa_agent

deps = setup_social_network_pwa_agent()
# Настройки: camera API, geolocation, real-time sync
```

### Gaming PWA

```python
from pwa_mobile_agent.examples.gaming_config import setup_casual_game_pwa_agent

deps = setup_casual_game_pwa_agent()
# Настройки: fullscreen mode, performance optimization, payments
```

## 🔧 Инструменты агента

### generate_pwa_manifest
Генерация PWA манифеста с адаптацией под тип проекта.

```python
manifest = await generate_pwa_manifest(
    ctx,
    app_name="My Store",
    description="Best online shopping experience"
)
```

### create_service_worker
Создание Service Worker с оптимальными стратегиями кэширования.

```python
service_worker = await create_service_worker(
    ctx,
    strategy="cache-first",
    cache_patterns=["/api/products/*", "/images/*"]
)
```

### optimize_mobile_ux
Оптимизация пользовательского интерфейса для мобильных устройств.

```python
optimizations = await optimize_mobile_ux(
    ctx,
    target_platform="universal",
    focus_areas=["touch_targets", "gestures", "responsive"]
)
```

### analyze_mobile_performance
Анализ производительности мобильной версии.

```python
performance_report = await analyze_mobile_performance(
    ctx,
    metrics=["core_web_vitals", "loading_speed", "interactivity"]
)
```

### setup_offline_sync
Настройка синхронизации данных для offline работы.

```python
sync_config = await setup_offline_sync(
    ctx,
    data_types=["user_data", "app_state", "offline_actions"],
    conflict_resolution="last_write_wins"
)
```

## 🎯 Стратегии кэширования

### Cache-first
Идеально для статичного контента и e-commerce каталогов.

```javascript
// Сначала проверяется кэш, затем сеть
cache-first: assets, product images, static resources
```

### Network-first
Подходит для динамического контента и real-time данных.

```javascript
// Сначала сеть, кэш как fallback
network-first: user data, news feeds, multiplayer games
```

### Stale-while-revalidate
Баланс между свежестью данных и производительностью.

```javascript
// Отдает из кэша, обновляет в фоне
stale-while-revalidate: API responses, content updates
```

## 📱 Мобильная оптимизация

### Touch Targets
- Минимальный размер: 44x44px
- Расстояние между элементами: 8px
- Области для жестов: swipe, pinch, rotate

### Responsive Design
- Mobile-first подход
- Breakpoints: 320px, 768px, 1024px
- Flexible layouts с CSS Grid/Flexbox

### Performance
- Core Web Vitals оптимизация
- Image optimization и lazy loading
- Code splitting для быстрой загрузки

## 🔄 Интеграция с Archon

Агент интегрирован с Archon Knowledge Base для:

- **Поиск лучших практик**: `search_agent_knowledge("PWA optimization")`
- **Архитектурные паттерны**: документированные решения для PWA
- **Code examples**: готовые примеры Service Workers и манифестов

### Настройка RAG

```python
# В dependencies.py указаны теги для поиска
knowledge_tags = ["pwa-mobile", "progressive-web-app", "mobile-optimization"]

# Поиск в базе знаний
result = await search_agent_knowledge(ctx, "service worker strategies")
```

## 🧪 Тестирование

### Запуск тестов

```bash
pytest tests/ -v
```

### Структура тестов

```
tests/
├── test_agent.py           # Основная функциональность
├── test_tools.py          # Тестирование инструментов
├── test_mobile_ux.py      # UX оптимизации
├── test_performance.py    # Performance анализ
└── conftest.py           # Общие фикстуры
```

## 📈 Метрики производительности

### Core Web Vitals
- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1

### PWA специфичные метрики
- **Time to Interactive**: < 3s
- **Cache hit ratio**: > 80%
- **Offline functionality**: 100% for core features
- **Installation rate**: > 20%

## 🔗 Полезные ресурсы

- [PWA Developer Guide](https://web.dev/progressive-web-apps/)
- [Workbox Documentation](https://developers.google.com/web/tools/workbox)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Mobile Web Best Practices](https://developers.google.com/web/fundamentals)

## 🤝 Поддержка

Для вопросов и предложений:
- Создайте задачу в Archon Project: `c75ef8e3-6f4d-4da2-9e81-8d38d04a341a`
- Используйте RAG для поиска документации
- Проверьте examples/ для готовых конфигураций

## 📄 Лицензия

Универсальный PWA Mobile Agent разработан для AI Agent Factory проекта и доступен для использования в любых PWA проектах.