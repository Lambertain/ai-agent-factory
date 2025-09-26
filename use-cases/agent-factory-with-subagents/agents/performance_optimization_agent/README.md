# Universal Performance & Next.js Optimization Agent

**Универсальный агент для анализа и оптимизации производительности любых типов проектов с расширенной поддержкой Next.js**

Агент автоматически адаптируется под ваш технологический стек и тип проекта, предоставляя персонализированные рекомендации по улучшению производительности.

## 🎯 Универсальность 95%+

### ✅ Полная адаптация под проекты
- **0% упоминаний конкретных проектов** в коде и промптах
- **Конфигурируемые настройки** для любого типа проекта
- **Адаптивные промпты** под технологический стек
- **≥3 примера конфигураций** для разных доменов

### 🌐 Поддерживаемые типы проектов
- **Web Applications** - React, Vue, Angular full-stack приложения
- **Next.js Applications** - App Router, Server Components, Edge Runtime оптимизация
- **APIs** - REST/GraphQL сервисы, микросервисы
- **Mobile Apps** - React Native, Flutter, нативные iOS/Android
- **Database Systems** - PostgreSQL, MySQL, MongoDB оптимизация
- **Frontend** - SPA, статические сайты, PWA
- **Backend** - Node.js, Python, .NET серверные приложения

## ⚡ Ключевые возможности

### 📊 Комплексный анализ производительности
- **Core Web Vitals** - FCP, LCP, CLS, FID, TTFB мониторинг
- **Bundle Analysis** - размер сборки, dependency audit, tree shaking
- **Next.js Specific** - Server Components, App Router, Edge Runtime анализ
- **Database Profiling** - анализ запросов, индексирование
- **API Performance** - response time, throughput, error rate
- **Mobile Optimization** - startup time, memory, battery usage
- **Real-time Monitoring** - метрики в реальном времени

### 🚀 Адаптивные стратегии оптимизации
- **Speed** - минимальное время отклика (aggressive caching, precomputation)
- **Memory** - эффективное использование памяти (lazy loading, pooling)
- **CPU** - минимальная нагрузка процессора (algorithm optimization)
- **Network** - оптимизация сетевого трафика (compression, CDN)
- **Balanced** - сбалансированный подход для большинства случаев

### 🛠️ Универсальные инструменты
- `analyze_performance` - комплексный анализ проекта
- `optimize_performance` - применение конкретных оптимизаций
- `monitor_performance` - мониторинг метрик в реальном времени
- `search_performance_knowledge` - поиск best practices в RAG
- `generate_performance_report` - детальные отчеты с рекомендациями

## 🚀 Быстрый старт

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Настройка переменных окружения
Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

Заполните обязательные переменные:
- `LLM_API_KEY` - API ключ для Qwen/Alibaba Cloud
- `GEMINI_API_KEY` - API ключ для Google Gemini

### Базовое использование
```python
from performance_optimization_agent import run_performance_optimization_sync

# Анализ производительности веб-приложения
result = run_performance_optimization_sync(
    task="Проанализируй и оптимизируй производительность React приложения",
    project_path="/path/to/project",
    config={
        "domain_type": "web_application",
        "performance_type": "web",
        "optimization_strategy": "balanced",
        "framework": "react"
    }
)

print(result)
```

## 🎨 Примеры конфигураций

### Web Application (React/Next.js)
```python
from performance_optimization_agent.examples import get_web_application_performance_dependencies

config = get_web_application_performance_dependencies()
config.project_name = "My Web App"
config.framework = "react"
config.enable_ssr = True
config.enable_code_splitting = True
config.target_metrics = {
    "first_contentful_paint": 1500,
    "largest_contentful_paint": 2500,
    "bundle_size": 250  # KB
}
```

### High-Performance API
```python
from performance_optimization_agent.examples import get_api_performance_dependencies

config = get_api_performance_dependencies()
config.project_name = "My API Service"
config.framework = "fastapi"
config.optimization_strategy = "speed"
config.target_metrics = {
    "response_time_p95": 200,  # ms
    "throughput_rps": 5000,
    "error_rate": 0.001
}
```

### Mobile Application
```python
from performance_optimization_agent.examples import get_mobile_performance_dependencies

config = get_mobile_performance_dependencies()
config.project_name = "My Mobile App"
config.framework = "react_native"
config.optimization_strategy = "memory"
config.target_metrics = {
    "app_start_time": 2000,  # ms
    "memory_usage": 150,     # MB
    "battery_usage": 5       # % per hour
}
```

## 📋 Поддерживаемые технологии

### 🌐 Web Frameworks
- **React** - hooks optimization, memo, code splitting
- **Vue** - composition API, async components, tree shaking
- **Angular** - OnPush strategy, lazy loading, standalone components
- **Next.js** - SSR/SSG, image optimization, bundle analysis
- **Nuxt.js** - universal rendering, performance modules

### 🔌 Backend Frameworks
- **FastAPI** - async optimization, dependency injection, response models
- **Django** - query optimization, template caching, static files
- **Express.js** - clustering, middleware optimization, compression
- **NestJS** - microservices, caching, performance monitoring
- **ASP.NET Core** - async patterns, memory pooling, caching

### 📱 Mobile Frameworks
- **React Native** - bundle optimization, memory management, performance
- **Flutter** - widget optimization, build optimization, performance tools
- **Xamarin** - platform-specific optimizations, memory management
- **Ionic** - hybrid app optimization, native performance

### 🗄️ Databases
- **PostgreSQL** - query optimization, indexing, connection pooling
- **MySQL** - query analysis, InnoDB optimization, replication
- **MongoDB** - aggregation pipeline, indexing strategies
- **Redis** - caching strategies, memory optimization
- **Elasticsearch** - search optimization, cluster performance

## 🔧 Расширенная конфигурация

### Performance Profiles
```python
# Получение профиля производительности для типа приложения
profile = config.get_performance_profile()
print(profile["priority_metrics"])  # Приоритетные метрики
print(profile["tools"])             # Рекомендуемые инструменты
print(profile["strategies"])        # Стратегии оптимизации
```

### Adaptive Thresholds
```python
# Адаптивные пороги под тип приложения
thresholds = config.get_adaptive_thresholds()
print(thresholds["response_time"])  # Пороги времени отклика
print(thresholds["memory_usage"])   # Пороги использования памяти
```

### Framework-Specific Configuration
```python
# Конфигурация для конкретного фреймворка
framework_config = config.get_framework_specific_config()
print(framework_config)  # React: code_splitting, memo_optimization, etc.
```

## 📊 Доступные инструменты

### `analyze_performance`
Комплексный анализ производительности проекта.
```python
result = await analyze_performance(
    ctx,
    analysis_type="full",  # full, quick, specific
    target_path="/src"
)
```

### `optimize_performance`
Применение конкретных оптимизаций.
```python
result = await optimize_performance(
    ctx,
    optimization_type="bundle",  # bundle, caching, database, images
    target_files=["src/App.js", "src/utils.js"]
)
```

### `monitor_performance`
Мониторинг метрик в реальном времени.
```python
result = await monitor_performance(
    ctx,
    duration_minutes=5,
    metrics=["response_time", "cpu_usage", "memory_usage"]
)
```

### `generate_performance_report`
Создание детального отчета с рекомендациями.
```python
result = await generate_performance_report(
    ctx,
    include_charts=True,
    format="markdown"  # markdown, json, html
)
```

## 🎯 Стратегии оптимизации

### ⚡ Speed Strategy
- **Цель**: Минимальное время отклика
- **Техники**: Aggressive caching, precomputation, parallelization
- **Подходит для**: API сервисы, real-time приложения
- **Trade-offs**: Повышенное использование памяти

### 💾 Memory Strategy
- **Цель**: Эффективное использование памяти
- **Техники**: Lazy loading, object pooling, compression
- **Подходит для**: Мобильные приложения, embedded systems
- **Trade-offs**: Возможное увеличение времени отклика

### 🖥️ CPU Strategy
- **Цель**: Минимальная нагрузка на процессор
- **Техники**: Algorithm optimization, batch processing, async operations
- **Подходит для**: High-load системы, serverless функции
- **Trade-offs**: Использование памяти, время отклика

### 🌐 Network Strategy
- **Цель**: Минимальное использование сети
- **Техники**: Compression, CDN, connection reuse, batching
- **Подходит для**: Мобильные приложения, slow connection users
- **Trade-offs**: Локальное хранилище, сложность

### ⚖️ Balanced Strategy
- **Цель**: Сбалансированная производительность
- **Техники**: Комбинация всех подходов
- **Подходит для**: Большинство web приложений
- **Trade-offs**: Отсутствуют экстремальные оптимизации

## 📈 Мониторинг и метрики

### Core Web Vitals
- **First Contentful Paint (FCP)** - время первого контента
- **Largest Contentful Paint (LCP)** - время загрузки основного контента
- **Cumulative Layout Shift (CLS)** - стабильность layout
- **First Input Delay (FID)** - отзывчивость интерфейса
- **Time to First Byte (TTFB)** - время ответа сервера

### API Performance
- **Response Time** - P50, P95, P99 percentiles
- **Throughput** - requests per second (RPS)
- **Error Rate** - процент неуспешных запросов
- **Availability** - uptime и SLA метрики

### Mobile Metrics
- **App Start Time** - cold/warm start performance
- **Memory Usage** - heap size, memory leaks
- **Battery Usage** - энергопотребление приложения
- **Frame Rate** - плавность анимаций (60 FPS target)
- **Network Efficiency** - data usage optimization

### Database Performance
- **Query Performance** - execution time, plan analysis
- **Index Efficiency** - index usage statistics
- **Connection Pool** - utilization, wait times
- **Cache Hit Ratio** - query result caching efficiency

## 🔍 Performance Analysis Patterns

### Web Application Analysis
```python
# Комплексный анализ веб-приложения
analysis_result = await analyze_performance(ctx, analysis_type="full")

# Фокус на Core Web Vitals
web_vitals = analysis_result["core_web_vitals"]
print(f"FCP: {web_vitals['fcp']}ms")
print(f"LCP: {web_vitals['lcp']}ms")
print(f"CLS: {web_vitals['cls']}")

# Bundle analysis
bundle_info = analysis_result["bundle_analysis"]
print(f"Main bundle: {bundle_info['main_size']}KB")
print(f"Vendor bundle: {bundle_info['vendor_size']}KB")
```

### API Performance Analysis
```python
# Анализ производительности API
api_analysis = await analyze_performance(ctx, analysis_type="api")

# Response time analysis
response_times = api_analysis["response_times"]
print(f"P50: {response_times['p50']}ms")
print(f"P95: {response_times['p95']}ms")
print(f"P99: {response_times['p99']}ms")

# Throughput analysis
print(f"Current RPS: {api_analysis['throughput']['current']}")
print(f"Peak RPS: {api_analysis['throughput']['peak']}")
```

### Database Optimization
```python
# Анализ производительности базы данных
db_analysis = await analyze_performance(ctx, analysis_type="database")

# Slow queries identification
slow_queries = db_analysis["slow_queries"]
for query in slow_queries:
    print(f"Query: {query['sql']}")
    print(f"Average time: {query['avg_time']}ms")
    print(f"Calls: {query['calls']}")

# Index recommendations
index_suggestions = db_analysis["index_suggestions"]
for suggestion in index_suggestions:
    print(f"Table: {suggestion['table']}")
    print(f"Suggested index: {suggestion['columns']}")
```

## 🛡️ Best Practices

### ✅ Анализ перед оптимизацией
- Всегда измеряй текущую производительность
- Профилируй реальные пользовательские сценарии
- Определи самые критичные bottlenecks
- Устанавливай конкретные цели улучшения

### 📊 Мониторинг и алертинг
- Настраивай continuous monitoring
- Устанавливай алерты на критичные метрики
- Отслеживай performance regressions
- Документируй все изменения

### 🔄 Итеративный подход
- Применяй оптимизации поэтапно
- Измеряй эффект каждого изменения
- Откатывай неэффективные оптимизации
- Непрерывно улучшай performance

## 🚀 Performance Budget

### Frontend Budget
```python
performance_budget = {
    "bundle_sizes": {
        "main_bundle": 150,    # KB
        "vendor_bundle": 200,  # KB
        "total_js": 350,       # KB
        "total_css": 100       # KB
    },
    "timing_metrics": {
        "fcp": 1500,          # ms
        "lcp": 2500,          # ms
        "fid": 100,           # ms
        "cls": 0.1            # score
    }
}
```

### API Budget
```python
api_budget = {
    "response_times": {
        "p50": 50,            # ms
        "p95": 200,           # ms
        "p99": 500            # ms
    },
    "throughput": {
        "target_rps": 1000,   # requests per second
        "peak_rps": 5000      # peak capacity
    },
    "availability": {
        "uptime": 99.9,       # percentage
        "error_rate": 0.1     # percentage
    }
}
```

## 💡 Advanced Features

### 🔍 Custom Analysis
```python
# Кастомный анализ для специфичных потребностей
custom_analysis = await analyze_performance(
    ctx,
    analysis_type="custom",
    custom_metrics=["bundle_size", "lighthouse_score", "memory_leaks"]
)
```

### 🎯 Targeted Optimization
```python
# Целевая оптимизация конкретных областей
targeted_optimization = await optimize_performance(
    ctx,
    optimization_type="targeted",
    focus_areas=["critical_path", "image_optimization", "caching"]
)
```

### 📊 Performance Dashboards
```python
# Генерация performance dashboard
dashboard = await generate_performance_report(
    ctx,
    format="dashboard",
    include_real_time=True,
    include_history=True
)
```

## 🔗 Интеграция

### 📚 Archon RAG Integration
```python
# Поиск в базе знаний
knowledge_result = await search_performance_knowledge(
    ctx,
    query="React performance optimization patterns",
    match_count=5
)
```

### 🔧 CI/CD Integration
- Lighthouse CI для автоматических performance audits
- Bundle size monitoring в CI pipeline
- Performance regression detection
- Automated performance testing

### 📊 Monitoring Integration
- Integration с APM tools (New Relic, DataDog)
- Custom metrics в Prometheus/Grafana
- Real-time alerting через Slack/Teams
- Performance analytics в Google Analytics

## 🤝 Участие в разработке

Агент постоянно развивается и улучшается. Предложения и баг-репорты приветствуются!

### 📋 Feature Requests
- Поддержка новых frameworks
- Дополнительные метрики мониторинга
- Интеграция с новыми инструментами
- Улучшение алгоритмов анализа

## 📄 Лицензия

MIT License - используйте в любых проектах.

---

**Performance Optimization Agent** - делаем ваши приложения быстрее, эффективнее и надежнее! ⚡📊🚀