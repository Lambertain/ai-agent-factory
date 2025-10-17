# Module 01: Application & API Performance Optimization

## 📖 Overview

This module covers universal performance optimization patterns for application code and API endpoints. Focused on backend optimization, caching strategies, asynchronous processing, and API response optimization.

**Key Topics:**
- Python performance patterns (caching, async/await, generators)
- Memory-efficient code design
- API optimization (FastAPI, response caching, background tasks)
- Rate limiting and compression
- Database connection pooling

**Technologies Covered:** Python, FastAPI, Redis, asyncio, psutil, aiohttp

---

## 🐍 Python Application Performance Patterns

### 1. Caching Strategies

```python
# LRU Cache для дорогих вычислений
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_computation(n: int) -> int:
    """
    LRU cache для дорогих вычислений.

    Args:
        n: Параметр вычисления

    Returns:
        int: Результат вычисления

    Performance impact:
        - Первый вызов: O(n) время
        - Последующие вызовы: O(1) время
        - Memory overhead: хранит до 1000 результатов
    """
    return sum(i * i for i in range(n))

# Использование
result = expensive_computation(10000)  # Первый вызов - медленно
result = expensive_computation(10000)  # Из кэша - мгновенно
```

**Best Practices:**
- Используйте `maxsize` для ограничения memory usage
- Применяйте для pure functions (детерминированные функции)
- Мониторьте cache hit rate через `cache_info()`

---

### 2. Async/Await для I/O Bound Операций

```python
import asyncio
import aiohttp
from typing import List, Dict, Any

async def fetch_data(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """
    Асинхронная загрузка данных.

    Args:
        session: Aiohttp client session
        url: URL для загрузки

    Returns:
        Dict[str, Any]: Загруженные данные
    """
    async with session.get(url) as response:
        return await response.json()

async def batch_api_calls(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Параллельные HTTP запросы для улучшения throughput.

    Args:
        urls: Список URLs для загрузки

    Returns:
        List[Dict[str, Any]]: Результаты всех запросов

    Performance impact:
        - Sequential: N * 200ms = N * 200ms
        - Concurrent: ~200ms (все запросы параллельно)
        - Speedup: N times faster
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Использование
urls = ['https://api.example.com/data1', 'https://api.example.com/data2']
results = asyncio.run(batch_api_calls(urls))
```

**When to Use:**
- ✅ Multiple API calls
- ✅ Database queries (с asyncpg, motor)
- ✅ File I/O operations
- ❌ CPU-bound operations (используйте multiprocessing)

---

### 3. Memory-Efficient Generators

```python
def process_large_file(filename: str):
    """
    Generator для обработки больших файлов без загрузки в память.

    Args:
        filename: Путь к файлу

    Yields:
        Обработанные строки

    Memory impact:
        - Without generator: Весь файл в памяти (может быть GB)
        - With generator: Только текущая строка (~KB)
    """
    with open(filename, 'r') as f:
        for line in f:
            processed = process_line(line.strip())
            yield processed

def process_line(line: str) -> dict:
    """Обработка одной строки."""
    return {'data': line.upper(), 'length': len(line)}

# Использование - memory-efficient iteration
for result in process_large_file('large_data.txt'):
    save_to_database(result)
```

**Advantages:**
- Constant memory usage независимо от размера файла
- Lazy evaluation - обработка on-demand
- Композируемость - можно chain generators

---

### 4. Performance Monitoring Decorator

```python
import time
import psutil
from functools import wraps
from typing import Any, Callable

def performance_monitor(func: Callable) -> Callable:
    """
    Decorator для мониторинга производительности функций.

    Tracks:
        - Execution time
        - Memory usage delta
        - CPU usage

    Args:
        func: Функция для мониторинга

    Returns:
        Wrapped function с performance tracking
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Baseline measurements
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            # Final measurements
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss

            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory

            # Logging
            print(f"{func.__name__}:")
            print(f"  Time: {execution_time:.4f}s")
            print(f"  Memory: {memory_delta/1024/1024:.2f}MB")

    return wrapper

# Использование
@performance_monitor
def heavy_computation(n: int) -> int:
    return sum(i * i for i in range(n))

result = heavy_computation(1000000)
# Output:
# heavy_computation:
#   Time: 0.1234s
#   Memory: 45.23MB
```

---

### 5. Database Connection Pooling

```python
import asyncpg
from typing import List, Any

class DatabasePool:
    """
    Пул соединений для оптимизации DB access.

    Benefits:
        - Reuse connections вместо создания новых
        - Connection limit control
        - Automatic connection health checks
    """

    def __init__(self, connection_string: str, pool_size: int = 10):
        """
        Initialize database pool.

        Args:
            connection_string: PostgreSQL connection string
            pool_size: Maximum pool size
        """
        self.connection_string = connection_string
        self.pool_size = pool_size
        self.pool = None

    async def initialize(self):
        """Create connection pool."""
        self.pool = await asyncpg.create_pool(
            self.connection_string,
            min_size=self.pool_size // 2,  # Минимум соединений
            max_size=self.pool_size,       # Максимум соединений
            command_timeout=30,            # Timeout для запросов
            max_queries=50000,             # Max queries per connection
            max_inactive_connection_lifetime=300  # Recycle old connections
        )

    async def execute_query(self, query: str, *params: Any) -> List[Any]:
        """
        Выполнение запроса через pool.

        Args:
            query: SQL query
            *params: Query parameters

        Returns:
            List[Any]: Query results

        Performance:
            - Without pooling: ~50ms per query (connection overhead)
            - With pooling: ~2ms per query
        """
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *params)

    async def close(self):
        """Close pool and all connections."""
        if self.pool:
            await self.pool.close()

# Использование
async def main():
    db = DatabasePool('postgresql://user:pass@localhost/dbname')
    await db.initialize()

    # Efficient query execution
    users = await db.execute_query("SELECT * FROM users WHERE active = $1", True)

    await db.close()
```

---

## 🚀 API Performance Optimization

### 1. Response Caching

```python
from fastapi import FastAPI, Depends
from redis import Redis
import json
from typing import Optional, Dict, Any

app = FastAPI()
redis_client = Redis(host='localhost', port=6379, decode_responses=True)

async def get_cached_response(cache_key: str) -> Optional[Dict[str, Any]]:
    """
    Получение кэшированного ответа.

    Args:
        cache_key: Ключ кэша

    Returns:
        Optional[Dict]: Кэшированные данные или None
    """
    cached = redis_client.get(cache_key)
    return json.loads(cached) if cached else None

async def set_cached_response(cache_key: str, data: Dict[str, Any], ttl: int = 3600):
    """
    Кэширование ответа с TTL.

    Args:
        cache_key: Ключ кэша
        data: Данные для кэширования
        ttl: Time to live в секундах (default: 1 hour)
    """
    redis_client.setex(cache_key, ttl, json.dumps(data))

@app.get("/api/user/{user_id}")
async def get_user_data(user_id: int) -> Dict[str, Any]:
    """
    API endpoint с кэшированием.

    Performance impact:
        - Cache HIT: ~1ms (Redis lookup)
        - Cache MISS: ~50ms (database query)
        - Cache hit ratio: >80% after warmup
    """
    cache_key = f"user:{user_id}"

    # Проверяем кэш
    cached_data = await get_cached_response(cache_key)
    if cached_data:
        return cached_data

    # Database query
    user_data = await database.fetch_one(
        "SELECT * FROM users WHERE id = $1", user_id
    )

    # Кэшируем результат
    await set_cached_response(cache_key, dict(user_data), ttl=300)

    return dict(user_data)
```

---

### 2. Database Query Optimization

```python
from typing import List

async def get_user_posts_optimized(user_id: int) -> List[Dict[str, Any]]:
    """
    Оптимизированный запрос с пагинацией и выборочными полями.

    Optimizations:
        - JOIN вместо N+1 queries
        - Выборочные поля (SELECT specific columns)
        - Index hint (WHERE на indexed column)
        - LIMIT для pagination

    Performance:
        - N+1 queries: 1 + N * 50ms = 1000ms для 20 постов
        - Optimized JOIN: 1 * 50ms = 50ms (20x faster!)
    """
    cache_key = f"user_posts:{user_id}"

    # Проверяем кэш
    cached_data = await get_cached_response(cache_key)
    if cached_data:
        return cached_data

    # Optimized query - JOIN вместо N+1
    query = """
    SELECT
        p.id,
        p.title,
        p.created_at,
        u.name as author_name
    FROM posts p
    JOIN users u ON p.user_id = u.id
    WHERE p.user_id = $1 AND p.status = 'published'
    ORDER BY p.created_at DESC
    LIMIT 20
    """

    posts = await database.fetch_all(query, user_id)
    result = [dict(post) for post in posts]

    # Кэшируем результат на 5 минут
    await set_cached_response(cache_key, result, ttl=300)

    return result
```

---

### 3. Background Tasks

```python
from fastapi import BackgroundTasks
import uuid

def generate_task_id() -> str:
    """Generate unique task ID."""
    return str(uuid.uuid4())

@app.post("/process-upload/")
async def process_upload(
    file_data: Dict[str, Any],
    background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """
    API endpoint с background обработкой.

    Benefits:
        - Быстрый ответ пользователю (<100ms)
        - Тяжелая обработка в фоне
        - User experience improvement

    Response time:
        - Without background: 5000ms (ждём обработки)
        - With background: 50ms (возвращаем task_id)
        - User satisfaction: 100x better!
    """
    # Быстрый ответ пользователю
    task_id = generate_task_id()

    # Тяжелая обработка в фоне
    background_tasks.add_task(process_file, file_data, task_id)

    return {
        "task_id": task_id,
        "status": "processing",
        "message": "File processing started"
    }

async def process_file(file_data: Dict[str, Any], task_id: str):
    """
    Background task для обработки файла.

    Args:
        file_data: Данные файла
        task_id: ID задачи для tracking
    """
    try:
        # Тяжелая обработка (5+ секунд)
        result = await heavy_file_processing(file_data)

        # Сохраняем результат в Redis
        await redis_client.setex(f"task:{task_id}", 3600, json.dumps({
            "status": "completed",
            "result": result
        }))
    except Exception as e:
        # Сохраняем ошибку
        await redis_client.setex(f"task:{task_id}", 3600, json.dumps({
            "status": "failed",
            "error": str(e)
        }))

async def heavy_file_processing(file_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate heavy processing."""
    await asyncio.sleep(5)  # Имитация тяжелой работы
    return {"processed": True, "rows": 1000}
```

---

### 4. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/data")
@limiter.limit("100/minute")
async def get_data(request: Request) -> Dict[str, Any]:
    """
    Rate-limited API endpoint.

    Limits:
        - 100 requests per minute per IP
        - Automatic 429 response при превышении

    Protection:
        - Prevents API abuse
        - Protects infrastructure from overload
        - Fair usage enforcement
    """
    return await fetch_data()
```

---

### 5. Response Compression

```python
from fastapi.middleware.gzip import GZipMiddleware

# Add compression middleware
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,  # Compress responses > 1KB
    compresslevel=6     # Balance between speed and compression (1-9)
)

# Benefits:
# - Reduces bandwidth by 70-90% for text responses
# - Faster transfer over slow connections
# - Lower cloud egress costs
```

---

## 📊 Best Practices

### Application Performance

✅ **Caching Strategy:**
- Use LRU cache для pure functions
- Monitor cache hit ratio (target: >80%)
- Set appropriate TTL values

✅ **Async/Await:**
- Use для I/O-bound operations
- Avoid для CPU-bound tasks (use multiprocessing)
- Always handle exceptions в async code

✅ **Memory Management:**
- Use generators для больших datasets
- Profile memory usage regularly
- Avoid global state accumulation

### API Performance

✅ **Response Time Targets:**
- < 100ms для simple GET requests
- < 200ms для database queries
- < 50ms для cached responses

✅ **Database Optimization:**
- Use connection pooling
- Implement response caching
- Optimize N+1 queries

✅ **Background Processing:**
- Offload heavy tasks to background
- Provide task status endpoints
- Set appropriate timeouts

---

**Версия модуля:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
**Проект:** AI Agent Factory - Performance Optimization Agent Modularization (6/7)

**Навигация:**
- [→ Module 02: Database Performance](02_database_performance.md)
- [↑ Назад к главной](../performance_optimization_agent_knowledge.md)

**Tags:** application-performance, api-optimization, python, fastapi, caching, async-await, background-tasks, rate-limiting
