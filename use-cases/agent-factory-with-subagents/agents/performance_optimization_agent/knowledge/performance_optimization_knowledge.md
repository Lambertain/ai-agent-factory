# Performance Optimization Agent Knowledge Base

## Системный промпт

Ты - универсальный Performance Optimization Agent, эксперт по оптимизации производительности любых типов приложений и систем. Специализируешься на анализе bottlenecks, профилировании, мониторинге и предложении конкретных решений для улучшения performance.

**Твоя экспертиза:**
- Профилирование и анализ производительности для любых архитектур
- Оптимизация баз данных (SQL, NoSQL, кэширование)
- Frontend performance (bundle size, Core Web Vitals, lazy loading)
- Backend optimization (API performance, memory management, concurrency)
- Infrastructure optimization (CDN, caching, load balancing)
- Мониторинг и alerting систем в real-time

**Универсальная экспертиза:**
- Адаптация под любые технологические стеки
- Cross-platform optimization (web, mobile, desktop)
- Cloud и on-premise environments
- Microservices и monolithic architectures
- Multi-language performance analysis (Python, Node.js, Java, Go, .NET, etc.)

## Мультиагентные паттерны работы

### 🔄 Reflection Pattern
После каждой оптимизации:
1. Измеряю baseline метрики перед изменениями
2. Применяю оптимизации и измеряю impact
3. Анализирую trade-offs и побочные эффекты
4. Предлагаю дальнейшие улучшения на основе результатов
5. Документирую best practices для будущего использования

### 🛠️ Tool Use Pattern
- Performance profiling tools (cProfile, perf, Chrome DevTools)
- Monitoring systems (Prometheus, Grafana, DataDog, New Relic)
- Load testing tools (k6, Artillery, JMeter, locust)
- Database optimization tools (EXPLAIN PLAN, pg_stat_statements)
- Code analysis tools (SonarQube, CodeClimate)

### 📋 Planning Pattern
1. Baseline measurement и определение performance goals
2. Идентификация bottlenecks через профилирование
3. Приоритизация optimizations по impact/effort
4. Поэтапная реализация с continuous monitoring
5. A/B testing для validation результатов

### 👥 Multi-Agent Collaboration
- **С Database Agent**: SQL query optimization и индексирование
- **С Frontend Agent**: bundle optimization и Core Web Vitals
- **С DevOps Agent**: infrastructure tuning и scaling strategies
- **С Security Agent**: security-performance trade-offs анализ

## Универсальные Performance Optimization Patterns

### Application Performance Optimization

```python
# Python Performance Patterns
import asyncio
import cProfile
import psutil
from functools import lru_cache, wraps
from typing import Dict, Any, Optional
import time

# 1. Caching Strategies
@lru_cache(maxsize=1000)
def expensive_computation(n: int) -> int:
    """LRU cache для дорогих вычислений."""
    return sum(i * i for i in range(n))

# 2. Async/Await для I/O bound операций
async def batch_api_calls(urls: list[str]) -> list[Dict[str, Any]]:
    """Асинхронные HTTP запросы для улучшения throughput."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# 3. Memory-efficient generators
def process_large_file(filename: str):
    """Generator для обработки больших файлов без загрузки в память."""
    with open(filename, 'r') as f:
        for line in f:
            yield process_line(line.strip())

# 4. Performance monitoring decorator
def performance_monitor(func):
    """Decorator для мониторинга производительности функций."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss

            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory

            print(f"{func.__name__}: {execution_time:.4f}s, {memory_delta/1024/1024:.2f}MB")

    return wrapper

# 5. Database connection pooling
class DatabasePool:
    """Пул соединений для оптимизации DB access."""

    def __init__(self, connection_string: str, pool_size: int = 10):
        self.pool = asyncpg.create_pool(
            connection_string,
            min_size=pool_size//2,
            max_size=pool_size,
            command_timeout=30
        )

    async def execute_query(self, query: str, *params) -> list:
        """Выполнение запроса через pool."""
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *params)
```

### Database Performance Optimization

```sql
-- Universal Database Optimization Patterns

-- 1. Index Optimization
-- Composite indexes для multi-column queries
CREATE INDEX CONCURRENTLY idx_orders_user_status_date
ON orders (user_id, status, created_at DESC)
WHERE status IN ('pending', 'processing');

-- Partial indexes для filtered queries
CREATE INDEX CONCURRENTLY idx_active_users
ON users (last_login_at DESC)
WHERE is_active = true;

-- 2. Query Optimization
-- Избегание N+1 queries через JOINs
SELECT u.id, u.name, p.title, p.created_at
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
WHERE u.is_active = true
ORDER BY p.created_at DESC;

-- Pagination с cursor-based approach для больших datasets
SELECT id, name, created_at
FROM users
WHERE created_at < $1  -- cursor
ORDER BY created_at DESC
LIMIT 20;

-- 3. Materialized Views для complex aggregations
CREATE MATERIALIZED VIEW user_statistics AS
SELECT
    user_id,
    COUNT(*) as total_posts,
    AVG(view_count) as avg_views,
    MAX(created_at) as last_post_date
FROM posts
WHERE status = 'published'
GROUP BY user_id;

-- Refresh strategy
REFRESH MATERIALIZED VIEW CONCURRENTLY user_statistics;

-- 4. Partitioning для больших таблиц
CREATE TABLE events (
    id BIGSERIAL,
    user_id INTEGER,
    event_type VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE events_202501 PARTITION OF events
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- 5. Connection pooling configuration
-- PgBouncer configuration
[databases]
app_db = host=localhost port=5432 dbname=app_production

[pgbouncer]
pool_mode = transaction
default_pool_size = 25
max_client_conn = 100
server_idle_timeout = 600
```

### Frontend Performance Optimization

```javascript
// Modern Frontend Performance Patterns

// 1. Code Splitting и Lazy Loading
import { lazy, Suspense } from 'react';

const LazyComponent = lazy(() =>
  import('./HeavyComponent').then(module => ({
    default: module.HeavyComponent
  }))
);

function App() {
  return (
    <Suspense fallback={<LoadingSkeleton />}>
      <LazyComponent />
    </Suspense>
  );
}

// 2. Virtual Scrolling для больших списков
import { FixedSizeList as List } from 'react-window';

function VirtualizedList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      <ItemComponent item={items[index]} />
    </div>
  );

  return (
    <List
      height={600}
      itemCount={items.length}
      itemSize={80}
      width="100%"
    >
      {Row}
    </List>
  );
}

// 3. Image optimization с современными форматами
function OptimizedImage({ src, alt, ...props }) {
  return (
    <picture>
      <source srcSet={`${src}.avif`} type="image/avif" />
      <source srcSet={`${src}.webp`} type="image/webp" />
      <img src={`${src}.jpg`} alt={alt} loading="lazy" {...props} />
    </picture>
  );
}

// 4. Service Worker для caching
// sw.js
const CACHE_NAME = 'app-v1';
const urlsToCache = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});

// 5. Bundle optimization
// webpack.config.js optimization
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
        common: {
          minChunks: 2,
          chunks: 'all',
          enforce: true
        }
      }
    },
    usedExports: true,
    sideEffects: false
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  }
};
```

### API Performance Optimization

```python
# Universal API Performance Patterns
from fastapi import FastAPI, Depends, BackgroundTasks
from redis import Redis
import asyncio
from typing import List, Optional
import json

app = FastAPI()
redis_client = Redis(host='localhost', port=6379, decode_responses=True)

# 1. Response Caching
async def get_cached_response(cache_key: str) -> Optional[dict]:
    """Получение кэшированного ответа."""
    cached = await redis_client.get(cache_key)
    return json.loads(cached) if cached else None

async def set_cached_response(cache_key: str, data: dict, ttl: int = 3600):
    """Кэширование ответа с TTL."""
    await redis_client.setex(cache_key, ttl, json.dumps(data))

# 2. Database Query Optimization
async def get_user_posts_optimized(user_id: int) -> List[dict]:
    """Оптимизированный запрос с пагинацией и выборочными полями."""
    cache_key = f"user_posts:{user_id}"

    # Проверяем кэш
    cached_data = await get_cached_response(cache_key)
    if cached_data:
        return cached_data

    # Выборочные поля + JOIN одним запросом
    query = """
    SELECT p.id, p.title, p.created_at, u.name as author_name
    FROM posts p
    JOIN users u ON p.user_id = u.id
    WHERE p.user_id = $1 AND p.status = 'published'
    ORDER BY p.created_at DESC
    LIMIT 20
    """

    posts = await database.fetch_all(query, user_id)
    result = [dict(post) for post in posts]

    # Кэшируем результат
    await set_cached_response(cache_key, result, ttl=300)
    return result

# 3. Background Tasks для тяжелых операций
@app.post("/process-upload/")
async def process_upload(
    file_data: dict,
    background_tasks: BackgroundTasks
):
    """API endpoint с background обработкой."""
    # Быстрый ответ пользователю
    task_id = generate_task_id()

    # Тяжелая обработка в фоне
    background_tasks.add_task(process_file, file_data, task_id)

    return {"task_id": task_id, "status": "processing"}

async def process_file(file_data: dict, task_id: str):
    """Background task для обработки файла."""
    try:
        # Тяжелая обработка
        result = await heavy_file_processing(file_data)

        # Сохраняем результат
        await redis_client.setex(f"task:{task_id}", 3600, json.dumps({
            "status": "completed",
            "result": result
        }))
    except Exception as e:
        await redis_client.setex(f"task:{task_id}", 3600, json.dumps({
            "status": "failed",
            "error": str(e)
        }))

# 4. Rate Limiting для защиты от перегрузки
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/data")
@limiter.limit("100/minute")
async def get_data(request: Request):
    """Rate-limited API endpoint."""
    return await fetch_data()

# 5. Response Compression
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Infrastructure Performance Optimization

```yaml
# Docker Performance Optimization
# Dockerfile
FROM python:3.11-slim as builder

# Multi-stage build для уменьшения image size
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim

# Установка только runtime dependencies
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Оптимизация для production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

USER 1000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]

---
# Kubernetes Performance Configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: app:latest
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: WORKERS
          value: "2"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20

---
# Nginx Performance Configuration
server {
    listen 80;
    server_name app.example.com;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Caching static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Connection pooling
    upstream backend {
        least_conn;
        server app1:8000 max_fails=3 fail_timeout=30s;
        server app2:8000 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }
}
```

## Domain-Specific Performance Patterns

### E-commerce Performance Optimization

```python
# E-commerce специфичные оптимизации
class EcommercePerformanceOptimizer:
    """Performance optimization для e-commerce платформ."""

    async def optimize_product_search(self, query: str, filters: dict) -> dict:
        """Оптимизированный поиск продуктов с кэшированием."""
        cache_key = f"search:{hash(query + str(sorted(filters.items())))}"

        # Проверяем кэш популярных запросов
        cached_result = await self.redis.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        # Elasticsearch query с optimized aggregations
        search_body = {
            "query": {
                "bool": {
                    "must": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["title^3", "description", "category"],
                            "type": "best_fields"
                        }}
                    ],
                    "filter": self._build_filters(filters)
                }
            },
            "aggs": {
                "categories": {"terms": {"field": "category.keyword", "size": 10}},
                "price_ranges": {"range": {"field": "price", "ranges": [
                    {"to": 50}, {"from": 50, "to": 100}, {"from": 100}
                ]}}
            },
            "size": 20,
            "_source": ["id", "title", "price", "image_url", "rating"]
        }

        result = await self.elasticsearch.search(index="products", body=search_body)

        # Кэшируем популярные запросы на 5 минут
        await self.redis.setex(cache_key, 300, json.dumps(result))
        return result

    async def optimize_cart_operations(self, user_id: str, item_id: str, quantity: int):
        """Оптимизированные операции с корзиной через Redis."""
        cart_key = f"cart:{user_id}"

        # Атомарные операции через Redis pipeline
        pipe = self.redis.pipeline()
        pipe.hset(cart_key, item_id, quantity)
        pipe.expire(cart_key, 86400 * 7)  # 7 дней TTL

        # Пересчёт общей стоимости в background
        pipe.sadd(f"cart_updates:{int(time.time()) // 60}", user_id)
        await pipe.execute()
```

### SaaS Performance Optimization

```python
# SaaS платформы оптимизации
class SaaSPerformanceOptimizer:
    """Performance optimization для SaaS приложений."""

    async def optimize_dashboard_data(self, user_id: str, org_id: str) -> dict:
        """Оптимизация загрузки dashboard data."""
        # Parallel loading различных dashboard sections
        dashboard_tasks = [
            self._get_analytics_data(org_id),
            self._get_recent_activities(user_id),
            self._get_usage_metrics(org_id),
            self._get_notifications(user_id)
        ]

        analytics, activities, metrics, notifications = await asyncio.gather(
            *dashboard_tasks, return_exceptions=True
        )

        return {
            "analytics": analytics if not isinstance(analytics, Exception) else {},
            "activities": activities if not isinstance(activities, Exception) else [],
            "metrics": metrics if not isinstance(metrics, Exception) else {},
            "notifications": notifications if not isinstance(notifications, Exception) else []
        }

    async def optimize_multi_tenant_queries(self, tenant_id: str, query: str) -> list:
        """Tenant-aware query optimization."""
        # Row-level security через prepared statements
        tenant_aware_query = f"""
        SET row_security = on;
        SET app.tenant_id = '{tenant_id}';
        {query}
        """

        return await self.database.fetch_all(tenant_aware_query)
```

### Blog/CMS Performance Optimization

```python
# Blog/CMS оптимизации
class BlogPerformanceOptimizer:
    """Performance optimization для blog/CMS систем."""

    async def optimize_content_delivery(self, slug: str) -> dict:
        """Оптимизированная доставка контента блога."""
        cache_key = f"post:{slug}"

        # Многоуровневое кэширование
        # L1: In-memory cache (Redis)
        cached_post = await self.redis.get(cache_key)
        if cached_post:
            return json.loads(cached_post)

        # L2: Database с optimized query
        post_query = """
        SELECT
            p.id, p.title, p.content, p.published_at,
            u.name as author_name, u.avatar_url,
            array_agg(t.name) as tags,
            c.name as category_name
        FROM posts p
        JOIN users u ON p.author_id = u.id
        LEFT JOIN post_tags pt ON p.id = pt.post_id
        LEFT JOIN tags t ON pt.tag_id = t.id
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.slug = $1 AND p.status = 'published'
        GROUP BY p.id, u.id, c.id
        """

        post_data = await self.database.fetch_one(post_query, slug)

        if post_data:
            result = dict(post_data)

            # Кэшируем на 1 час
            await self.redis.setex(cache_key, 3600, json.dumps(result, default=str))

            # Increment view count асинхронно
            asyncio.create_task(self._increment_view_count(result['id']))

            return result

        return None

    async def optimize_sitemap_generation(self) -> str:
        """Оптимизированная генерация sitemap."""
        cache_key = "sitemap:xml"

        cached_sitemap = await self.redis.get(cache_key)
        if cached_sitemap:
            return cached_sitemap

        # Bulk query для всех published posts
        posts = await self.database.fetch_all("""
        SELECT slug, updated_at
        FROM posts
        WHERE status = 'published'
        ORDER BY updated_at DESC
        """)

        sitemap_xml = self._generate_sitemap_xml(posts)

        # Кэшируем sitemap на 24 часа
        await self.redis.setex(cache_key, 86400, sitemap_xml)

        return sitemap_xml
```

## Performance Monitoring и Alerting

### Universal Monitoring Setup

```python
# Universal Performance Monitoring
import time
import psutil
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import logging

# Prometheus metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('app_request_duration_seconds', 'Request duration')
MEMORY_USAGE = Gauge('app_memory_usage_bytes', 'Memory usage')
CPU_USAGE = Gauge('app_cpu_usage_percent', 'CPU usage')

class PerformanceMonitor:
    """Универсальный monitoring класс."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def track_request(self, method: str, endpoint: str):
        """Decorator для трекинга requests."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()

                try:
                    result = func(*args, **kwargs)
                    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
                    return result
                finally:
                    REQUEST_DURATION.observe(time.time() - start_time)
            return wrapper
        return decorator

    async def collect_system_metrics(self):
        """Сбор системных метрик."""
        while True:
            # Memory usage
            memory = psutil.virtual_memory()
            MEMORY_USAGE.set(memory.used)

            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            CPU_USAGE.set(cpu_percent)

            # Log критичные значения
            if memory.percent > 85:
                self.logger.warning(f"High memory usage: {memory.percent}%")

            if cpu_percent > 80:
                self.logger.warning(f"High CPU usage: {cpu_percent}%")

            await asyncio.sleep(30)

    def setup_alerting(self):
        """Настройка alerting rules."""
        alerting_rules = {
            "high_memory": {
                "condition": "memory_usage > 0.85",
                "action": self._send_alert,
                "message": "Memory usage exceeded 85%"
            },
            "slow_requests": {
                "condition": "request_duration_p95 > 2.0",
                "action": self._send_alert,
                "message": "95th percentile response time > 2s"
            }
        }
        return alerting_rules

# Grafana Dashboard Configuration
GRAFANA_DASHBOARD = {
    "dashboard": {
        "title": "Application Performance",
        "panels": [
            {
                "title": "Request Rate",
                "type": "graph",
                "targets": [{"expr": "rate(app_requests_total[5m])"}]
            },
            {
                "title": "Response Time",
                "type": "graph",
                "targets": [{"expr": "histogram_quantile(0.95, app_request_duration_seconds)"}]
            },
            {
                "title": "Memory Usage",
                "type": "singlestat",
                "targets": [{"expr": "app_memory_usage_bytes"}]
            }
        ]
    }
}
```

## Performance Testing Strategies

```python
# Performance Testing Framework
import asyncio
import aiohttp
import time
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class LoadTestResult:
    """Результаты нагрузочного тестирования."""
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    p95_response_time: float
    requests_per_second: float
    errors: List[str]

class UniversalLoadTester:
    """Универсальный load tester."""

    async def run_load_test(
        self,
        url: str,
        concurrent_users: int = 10,
        duration_seconds: int = 60,
        headers: Dict[str, str] = None
    ) -> LoadTestResult:
        """Запуск нагрузочного теста."""

        results = []
        errors = []
        start_time = time.time()

        async def worker():
            """Worker для выполнения requests."""
            async with aiohttp.ClientSession(headers=headers) as session:
                while time.time() - start_time < duration_seconds:
                    request_start = time.time()
                    try:
                        async with session.get(url) as response:
                            await response.text()
                            request_time = time.time() - request_start
                            results.append({
                                'success': response.status == 200,
                                'response_time': request_time,
                                'status_code': response.status
                            })
                    except Exception as e:
                        errors.append(str(e))
                        results.append({
                            'success': False,
                            'response_time': time.time() - request_start,
                            'status_code': 0
                        })

        # Запуск concurrent workers
        workers = [asyncio.create_task(worker()) for _ in range(concurrent_users)]
        await asyncio.gather(*workers)

        # Анализ результатов
        successful = [r for r in results if r['success']]
        response_times = [r['response_time'] for r in results]

        return LoadTestResult(
            total_requests=len(results),
            successful_requests=len(successful),
            failed_requests=len(results) - len(successful),
            average_response_time=sum(response_times) / len(response_times),
            p95_response_time=sorted(response_times)[int(len(response_times) * 0.95)],
            requests_per_second=len(results) / duration_seconds,
            errors=errors
        )
```

## Рефлексия и Performance Analysis

После каждой оптимизации выполняй комплексный анализ:

### 1. Performance Metrics Checklist
- ✅ Response time improved (target: <200ms for API, <2s for pages)
- ✅ Throughput increased (requests per second)
- ✅ Memory usage optimized (no memory leaks)
- ✅ CPU utilization efficient
- ✅ Database query performance improved
- ✅ Cache hit ratio optimized (>80% for hot data)

### 2. Scalability Validation
- ✅ Load testing под increased traffic
- ✅ Horizontal scaling возможности
- ✅ Database scaling strategies
- ✅ CDN и caching effectiveness
- ✅ Auto-scaling configuration

### 3. Trade-offs Analysis
- ✅ Performance vs Security balance
- ✅ Speed vs Reliability trade-offs
- ✅ Memory vs CPU optimization choices
- ✅ Cost vs Performance optimization
- ✅ Complexity vs Maintainability

### 4. Monitoring Setup
- ✅ Real-time performance monitoring
- ✅ Alerting для performance regressions
- ✅ SLA compliance tracking
- ✅ Business metrics correlation
- ✅ Capacity planning data

### 5. Documentation и Knowledge Sharing
- ✅ Performance optimization decisions documented
- ✅ Before/after metrics comparison
- ✅ Best practices для team sharing
- ✅ Performance testing automation
- ✅ Monitoring playbooks создание

## MCP серверы для Performance Optimization

### Рекомендуемые MCP серверы:
- **prometheus** - metrics collection и alerting
- **grafana** - performance dashboards и visualization
- **database** - direct database performance analysis
- **docker** - container performance monitoring
- **aws/gcp/azure** - cloud infrastructure monitoring

### Интеграция с performance stack:
- Автоматический сбор performance metrics
- Real-time alerting при performance issues
- Database query analysis и optimization suggestions
- Infrastructure scaling recommendations
- Cost optimization через performance improvements

Этот агент должен работать как универсальный performance эксперт для любых типов систем - от мобильных приложений до enterprise платформ, адаптируясь под специфические требования каждой архитектуры через конфигурацию и monitoring setup.