# Performance Optimization Agent Knowledge Base

## Системный промпт

Performance Optimization Agent — это универсальный эксперт по оптимизации производительности любых типов приложений. Агент адаптируется под конкретный технологический стек и тип проекта, предоставляя персонализированные рекомендации по улучшению производительности.

## Ключевые компетенции

### 🎯 Универсальная адаптация
- **Domain Types**: web_application, api, database, frontend, backend, mobile
- **Performance Types**: web, api, database, frontend, backend, mobile
- **Optimization Strategies**: speed, memory, cpu, network, balanced
- **Frameworks**: React, Vue, Angular, FastAPI, Django, Express, React Native, Flutter

### 📊 Анализ производительности
- Профилирование узких мест и bottlenecks
- Мониторинг Core Web Vitals (FCP, LCP, CLS, FID, TTFB)
- Анализ bundle size и dependency audit
- Database query performance analysis
- API response time optimization
- Mobile app startup и battery optimization

### ⚡ Оптимизационные техники

#### Frontend Optimization
- **Bundle Optimization**: Code splitting, tree shaking, dead code elimination
- **Asset Optimization**: Image compression, lazy loading, modern formats (WebP, AVIF)
- **Caching Strategies**: Browser cache, service worker, CDN integration
- **Critical Path**: Critical CSS, resource hints, preloading
- **Runtime Performance**: Virtual scrolling, memoization, efficient re-renders

#### Backend/API Optimization
- **Response Optimization**: Compression (gzip/brotli), response caching
- **Database Optimization**: Query optimization, indexing, connection pooling
- **Async Processing**: Background jobs, async/await patterns, non-blocking I/O
- **Rate Limiting**: Throttling, circuit breakers, load balancing
- **Monitoring**: APM integration, distributed tracing, health checks

#### Mobile Optimization
- **Startup Performance**: Lazy initialization, splash screen optimization
- **Memory Management**: Image caching, garbage collection, memory warnings
- **Battery Optimization**: Background task limiting, location optimization
- **Network Efficiency**: Request batching, offline support, compression
- **Rendering**: Frame rate optimization, layout optimization

#### Database Optimization
- **Query Performance**: Query plan analysis, index optimization
- **Connection Management**: Connection pooling, read/write splitting
- **Caching**: Query result caching, materialized views
- **Scalability**: Partitioning, replication, sharding
- **Monitoring**: Slow query logs, performance schema analysis

## Инструменты и методы

### 🔍 Анализ производительности
```python
@agent.tool
async def analyze_performance(
    ctx: RunContext[PerformanceOptimizationDependencies],
    analysis_type: str = "full",  # full, quick, specific
    target_path: str = ""
) -> str:
    """Комплексный анализ производительности проекта"""
```

### ⚡ Применение оптимизаций
```python
@agent.tool
async def optimize_performance(
    ctx: RunContext[PerformanceOptimizationDependencies],
    optimization_type: str,  # bundle, caching, database, images, compression
    target_files: List[str] = []
) -> str:
    """Применение конкретных оптимизаций"""
```

### 📊 Мониторинг метрик
```python
@agent.tool
async def monitor_performance(
    ctx: RunContext[PerformanceOptimizationDependencies],
    duration_minutes: int = 5,
    metrics: List[str] = []
) -> str:
    """Мониторинг производительности в реальном времени"""
```

### 📚 Поиск в базе знаний
```python
@agent.tool
async def search_performance_knowledge(
    ctx: RunContext[PerformanceOptimizationDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """Поиск best practices в базе знаний"""
```

## Специализированные конфигурации

### Web Application Performance
```python
# Конфигурация для веб-приложений
config = WebApplicationPerformanceDependencies(
    domain_type="web_application",
    performance_type="web",
    optimization_strategy="balanced",
    target_metrics={
        "first_contentful_paint": 1500,
        "largest_contentful_paint": 2500,
        "cumulative_layout_shift": 0.1,
        "bundle_size": 250  # KB
    }
)
```

### API Performance
```python
# Конфигурация для API
config = APIPerformanceDependencies(
    domain_type="api",
    performance_type="api",
    optimization_strategy="speed",
    target_metrics={
        "response_time_p95": 200,
        "throughput_rps": 5000,
        "error_rate": 0.001
    }
)
```

### Mobile Performance
```python
# Конфигурация для мобильных приложений
config = MobilePerformanceDependencies(
    domain_type="mobile",
    performance_type="mobile",
    optimization_strategy="memory",
    target_metrics={
        "app_start_time": 2000,
        "memory_usage": 150,  # MB
        "battery_usage": 5    # % per hour
    }
)
```

## Лучшие практики по доменам

### 🌐 Web Applications
- **Core Web Vitals**: FCP < 1.5s, LCP < 2.5s, CLS < 0.1, FID < 100ms
- **Bundle Size**: Main bundle < 150KB, total JS < 350KB
- **Image Optimization**: WebP/AVIF formats, responsive images, lazy loading
- **Caching Strategy**: Service Worker + CDN + browser cache
- **Critical Resources**: Inline critical CSS, preload fonts, defer non-critical JS

### 🔌 APIs
- **Response Times**: P50 < 50ms, P95 < 200ms, P99 < 500ms
- **Throughput**: > 1000 RPS for standard APIs, > 5000 RPS for high-performance
- **Database**: Connection pooling, query optimization, read replicas
- **Caching**: Redis/Memcached, response caching, CDN for static content
- **Monitoring**: APM tools, distributed tracing, SLA monitoring

### 📱 Mobile Apps
- **Startup Time**: Cold start < 2s, warm start < 500ms
- **Memory Usage**: < 150MB for React Native, < 100MB for Flutter
- **Battery Life**: < 5% drain per hour active use
- **Network**: Request batching, offline support, compression
- **Rendering**: 60 FPS target, efficient list rendering

### 🗄️ Databases
- **Query Performance**: < 50ms for simple queries, < 200ms for complex
- **Index Efficiency**: Index hit ratio > 95%
- **Connection Management**: Pool utilization < 80%
- **Cache Hit Ratio**: > 85% for query result cache
- **Backup Performance**: Non-blocking, incremental backups

## Стратегии оптимизации

### ⚡ Speed Strategy
- **Приоритет**: Минимальное время отклика
- **Техники**: Aggressive caching, precomputation, parallelization
- **Trade-offs**: Повышенное использование памяти, сложность кода
- **Метрики**: Response time (50%), Throughput (30%), CPU (20%)

### 💾 Memory Strategy
- **Приоритет**: Эффективное использование памяти
- **Техники**: Lazy loading, object pooling, compression
- **Trade-offs**: Возможное увеличение времени отклика
- **Метрики**: Memory usage (50%), Response time (30%), Throughput (20%)

### 🖥️ CPU Strategy
- **Приоритет**: Минимальная нагрузка на процессор
- **Техники**: Algorithm optimization, batch processing, async operations
- **Trade-offs**: Использование памяти, время отклика
- **Метрики**: CPU usage (50%), Throughput (30%), Memory (20%)

### 🌐 Network Strategy
- **Приоритет**: Минимальное использование сети
- **Техники**: Compression, CDN, connection reuse, batching
- **Trade-offs**: Локальное хранилище, сложность
- **Метрики**: Network latency (40%), Bandwidth (30%), Response time (30%)

### ⚖️ Balanced Strategy
- **Приоритет**: Сбалансированная производительность
- **Техники**: Комбинация всех подходов
- **Trade-offs**: Отсутствуют экстремальные оптимизации
- **Метрики**: Равномерное распределение весов (25% каждая)

## Мониторинг и метрики

### 📊 Core Metrics
- **Response Time**: P50, P95, P99 percentiles
- **Throughput**: Requests per second (RPS)
- **Error Rate**: Percentage of failed requests
- **Resource Usage**: CPU, Memory, Disk I/O
- **User Experience**: Core Web Vitals, conversion rates

### 🚨 Alerting Thresholds
- **Good**: Зеленая зона, оптимальная производительность
- **Acceptable**: Желтая зона, приемлемая производительность
- **Poor**: Красная зона, требует немедленного внимания

### 📈 Adaptive Thresholds
Пороги автоматически адаптируются под тип приложения:
- **API**: Более строгие требования к response time
- **Frontend**: Фокус на Core Web Vitals
- **Mobile**: Акцент на battery и memory usage
- **Database**: Приоритет query performance

## Инструменты и технологии

### 🔧 Performance Tools
- **Web**: Lighthouse, Web Vitals, Bundle Analyzer
- **API**: Apache Bench, wrk, JMeter, Locust
- **Database**: EXPLAIN ANALYZE, pg_stat, slow query log
- **Mobile**: Instruments (iOS), Android Profiler, Flipper
- **Monitoring**: New Relic, DataDog, Grafana, Prometheus

### 📚 Frameworks Expertise
- **React**: Memo, useMemo, Code splitting, React DevTools
- **Vue**: Vue DevTools, async components, tree shaking
- **Angular**: OnPush strategy, lazy loading, bundle optimization
- **FastAPI**: Async endpoints, dependency injection, response models
- **Django**: Query optimization, template caching, static files
- **Express**: Clustering, middleware optimization, compression

## Паттерны оптимизации

### 🎯 Frontend Patterns
```javascript
// React optimization patterns
const OptimizedComponent = memo(({ data }) => {
  const expensiveValue = useMemo(() =>
    computeExpensiveValue(data), [data]
  );

  return <div>{expensiveValue}</div>;
});

// Code splitting
const LazyComponent = lazy(() => import('./HeavyComponent'));
```

### 🔌 Backend Patterns
```python
# FastAPI optimization patterns
@app.get("/users/{user_id}")
@cache(expire=300)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.profile))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

### 📱 Mobile Patterns
```javascript
// React Native optimization
const OptimizedList = memo(({ data }) => (
  <FlatList
    data={data}
    renderItem={renderItem}
    initialNumToRender={10}
    maxToRenderPerBatch={5}
    windowSize={10}
    removeClippedSubviews={true}
    getItemLayout={(data, index) => ({
      length: ITEM_HEIGHT,
      offset: ITEM_HEIGHT * index,
      index,
    })}
  />
));
```

## Интеграция с проектами

### 🔄 Workflow Integration
1. **Анализ**: Комплексное профилирование текущего состояния
2. **Планирование**: Приоритизация оптимизаций по impact/effort
3. **Реализация**: Поэтапное применение оптимизаций
4. **Мониторинг**: Отслеживание эффективности изменений
5. **Итерация**: Непрерывное улучшение на основе метрик

### 📋 Performance Budget
Установка и контроль performance budget:
- Bundle size limits
- Response time targets
- Resource usage thresholds
- Core Web Vitals targets
- Error rate limits

### 🚀 CI/CD Integration
- Lighthouse CI для автоматических performance audits
- Bundle size monitoring в CI pipeline
- Performance regression detection
- Automated performance testing
- Performance metrics в PR checks

## Best practices

### ✅ Общие принципы
1. **Measure First**: Всегда измеряй перед оптимизацией
2. **Focus on Bottlenecks**: Оптимизируй самые критичные проблемы
3. **Monitor Continuously**: Постоянный мониторинг производительности
4. **Test Thoroughly**: Проверяй каждую оптимизацию
5. **Document Changes**: Документируй все изменения и их эффект

### 🚫 Антипаттерны
- Преждевременная оптимизация без измерений
- Микрооптимизации вместо решения реальных проблем
- Игнорирование пользовательского опыта ради метрик
- Оптимизация без учета trade-offs
- Отсутствие мониторинга после внедрения

### 🎯 Performance-First Mindset
- Рассматривай производительность как функциональность
- Устанавливай performance budget на старте проекта
- Автоматизируй performance testing
- Обучай команду performance best practices
- Делай performance частью definition of done