# Module 02: Performance Optimization

**Версия:** 1.0
**Дата:** 2025-10-17
**Автор:** Archon Implementation Engineer

**Назад к:** [Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- Async/await patterns для parallel API calls
- Batching strategies для минимизации overhead (embeddings, API requests)
- Multi-level caching implementation (Memory → Redis → Database)
- Token Bucket алгоритм для rate limiting внешних API
- Connection pooling для PostgreSQL и Redis
- Performance profiling и bottleneck analysis
- CPU-intensive операции в thread pool (избежание блокировки event loop)

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** производительность, async, батчинг, кэширование, connection pool, rate limiting, оптимизация, параллелизм, thread pool, exponential backoff, throughput, latency

**English:** performance, async, batching, caching, connection pool, rate limiting, optimization, parallelism, thread pool, exponential backoff, throughput, latency

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Высокие нагрузки и необходимость масштабирования
- Оптимизация response time критична
- Работа с внешними API с rate limits
- Агент делает множество parallel операций
- CPU-intensive обработка данных
- Необходимость минимизировать latency
- Throughput агента недостаточен

---

## Async Programming Best Practices

### Performance Optimized Agent

```python
import asyncio
import aiohttp
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import time

class PerformanceOptimizedAgent:
    """Агент с оптимизацией производительности."""

    def __init__(self):
        self.session = None
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def __aenter__(self):
        """Context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.session.close()
        self.executor.shutdown()

    async def parallel_api_calls(self, urls: List[str]) -> List[Dict]:
        """Параллельные вызовы API с обработкой ошибок."""
        tasks = [self.fetch_data(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Фильтрация успешных результатов
        successful = [r for r in results if not isinstance(r, Exception)]

        # Логирование ошибок
        errors = [r for r in results if isinstance(r, Exception)]
        if errors:
            print(f"[WARNING] {len(errors)} requests failed")

        return successful

    async def fetch_data(self, url: str) -> Dict:
        """Получение данных с retry логикой и exponential backoff."""
        for attempt in range(3):
            try:
                async with self.session.get(url, timeout=5) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status
                        )
            except Exception as e:
                if attempt == 2:  # Последняя попытка
                    raise e
                # Exponential backoff: 1s, 2s, 4s
                await asyncio.sleep(2 ** attempt)

    async def cpu_intensive_task(self, data: List[Dict]) -> List[Dict]:
        """CPU-интенсивная задача в thread pool для избежания блокировки event loop."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.process_data_sync,
            data
        )

    def process_data_sync(self, data: List[Dict]) -> List[Dict]:
        """Синхронная обработка данных в отдельном потоке."""
        # Сложные вычисления, которые блокируют CPU
        return [self.transform_item(item) for item in data]

    def transform_item(self, item: Dict) -> Dict:
        """Трансформация одного элемента."""
        # Имитация тяжелых вычислений
        time.sleep(0.01)
        return {"processed": True, **item}

# Usage with context manager
async def main():
    async with PerformanceOptimizedAgent() as agent:
        # Параллельные API вызовы
        urls = ["http://api1.com", "http://api2.com", "http://api3.com"]
        results = await agent.parallel_api_calls(urls)

        # CPU-интенсивная обработка в thread pool
        processed = await agent.cpu_intensive_task(results)

        return processed
```

### Batching для оптимизации запросов

```python
import asyncio
from typing import List, Dict, Callable, Any
from collections import defaultdict
import time

class BatchProcessor:
    """Batch обработка запросов для минимизации overhead."""

    def __init__(self, batch_size: int = 10, max_wait_ms: int = 100):
        self.batch_size = batch_size
        self.max_wait_ms = max_wait_ms
        self.pending_requests: List[Dict] = []
        self.batch_lock = asyncio.Lock()

    async def add_to_batch(
        self,
        request_data: Any,
        processor: Callable
    ) -> Any:
        """Добавить запрос в batch и дождаться результата."""
        future = asyncio.Future()

        async with self.batch_lock:
            self.pending_requests.append({
                "data": request_data,
                "future": future
            })

            # Запустить обработку, если batch полный
            if len(self.pending_requests) >= self.batch_size:
                await self._process_batch(processor)

        # Если batch не полный, запустить таймер
        if not future.done():
            asyncio.create_task(
                self._wait_and_process(processor)
            )

        return await future

    async def _wait_and_process(self, processor: Callable):
        """Подождать таймаут и обработать partial batch."""
        await asyncio.sleep(self.max_wait_ms / 1000)

        async with self.batch_lock:
            if self.pending_requests:
                await self._process_batch(processor)

    async def _process_batch(self, processor: Callable):
        """Обработать batch запросов."""
        if not self.pending_requests:
            return

        # Извлекаем текущий batch
        batch = self.pending_requests[:]
        self.pending_requests.clear()

        # Обработка batch
        try:
            batch_data = [req["data"] for req in batch]
            results = await processor(batch_data)

            # Распределение результатов
            for req, result in zip(batch, results):
                req["future"].set_result(result)

        except Exception as e:
            # При ошибке - propagate ко всем futures
            for req in batch:
                req["future"].set_exception(e)

# Usage Example
class EmbeddingService:
    """Сервис для генерации embeddings с batching."""

    def __init__(self):
        self.batch_processor = BatchProcessor(batch_size=32, max_wait_ms=50)

    async def get_embedding(self, text: str) -> List[float]:
        """Получить embedding для одного текста."""
        return await self.batch_processor.add_to_batch(
            text,
            self._batch_embed
        )

    async def _batch_embed(self, texts: List[str]) -> List[List[float]]:
        """Batch генерация embeddings."""
        # Один API вызов для всех текстов
        # Вместо N вызовов - только 1
        print(f"[OK] Batch embedding {len(texts)} texts")

        # Реальный вызов к embedding API
        # response = await embedding_api.embed(texts)
        # return response.embeddings

        # Mock для примера
        return [[0.1, 0.2, 0.3] for _ in texts]

# Usage
async def process_documents(docs: List[str]):
    service = EmbeddingService()

    # Все запросы будут автоматически batch'иться
    embeddings = await asyncio.gather(*[
        service.get_embedding(doc) for doc in docs
    ])

    return embeddings
```

---

## Caching Strategies

### Redis Cache Manager

```python
import redis.asyncio as redis
import json
import hashlib
from functools import wraps
from typing import Optional, Any, Callable
import pickle

class CacheManager:
    """Менеджер кэширования с Redis."""

    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def get(self, key: str) -> Optional[Any]:
        """Получить значение из кэша."""
        value = await self.redis.get(key)
        if value:
            return pickle.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Сохранить значение в кэш с TTL."""
        await self.redis.setex(key, ttl, pickle.dumps(value))

    async def delete(self, key: str):
        """Удалить значение из кэша."""
        await self.redis.delete(key)

    async def clear_pattern(self, pattern: str):
        """Очистить кэш по паттерну (например: "user:*")."""
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)

    async def get_or_set(
        self,
        key: str,
        factory: Callable,
        ttl: int = 3600
    ) -> Any:
        """Получить из кэша или создать и закэшировать."""
        # Попытка получить из кэша
        cached = await self.get(key)
        if cached is not None:
            return cached

        # Создание значения
        value = await factory()

        # Кэширование
        await self.set(key, value, ttl)

        return value

def cached(ttl: int = 3600, key_prefix: str = ""):
    """Декоратор для кэширования результатов функций."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Генерация ключа кэша
            cache_key = f"{key_prefix}:{func.__name__}:{_generate_cache_key(args, kwargs)}"

            # Попытка получить из кэша
            cache_manager = kwargs.get('cache_manager')
            if cache_manager:
                cached_result = await cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            # Выполнение функции
            result = await func(*args, **kwargs)

            # Сохранение в кэш
            if cache_manager:
                await cache_manager.set(cache_key, result, ttl)

            return result
        return wrapper
    return decorator

def _generate_cache_key(args, kwargs) -> str:
    """Генерация ключа кэша на основе аргументов."""
    key_data = f"{args}:{sorted(kwargs.items())}"
    return hashlib.md5(key_data.encode()).hexdigest()

# Usage Example
class DataService:
    """Сервис с кэшированием."""

    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager

    @cached(ttl=1800, key_prefix="data_service")
    async def expensive_computation(
        self,
        param1: str,
        param2: int,
        cache_manager=None
    ) -> Dict:
        """Дорогая операция с кэшированием."""
        # Симуляция тяжелых вычислений
        await asyncio.sleep(2)
        return {"result": f"processed_{param1}_{param2}"}

    async def get_user_data(self, user_id: str) -> Dict:
        """Получить данные пользователя с кэшированием."""
        return await self.cache_manager.get_or_set(
            f"user:{user_id}",
            lambda: self._fetch_user_from_db(user_id),
            ttl=3600
        )

    async def _fetch_user_from_db(self, user_id: str) -> Dict:
        """Получить пользователя из БД."""
        # Реальный запрос к БД
        return {"id": user_id, "name": "User"}
```

### Multi-level Caching Strategy

```python
from typing import Optional
import asyncio

class MultiLevelCache:
    """Многоуровневое кэширование (Memory -> Redis -> DB)."""

    def __init__(self, redis_cache: CacheManager):
        self.memory_cache: Dict[str, Any] = {}
        self.redis_cache = redis_cache
        self.memory_ttl = 60  # 1 минута в памяти
        self.redis_ttl = 3600  # 1 час в Redis

    async def get(self, key: str) -> Optional[Any]:
        """Получить значение из многоуровневого кэша."""
        # L1: Memory cache
        if key in self.memory_cache:
            print(f"[OK] Cache hit: Memory - {key}")
            return self.memory_cache[key]

        # L2: Redis cache
        redis_value = await self.redis_cache.get(key)
        if redis_value:
            print(f"[OK] Cache hit: Redis - {key}")
            # Promote to memory cache
            self.memory_cache[key] = redis_value
            asyncio.create_task(self._expire_memory(key))
            return redis_value

        print(f"[WARNING] Cache miss - {key}")
        return None

    async def set(self, key: str, value: Any):
        """Установить значение во все уровни кэша."""
        # L1: Memory
        self.memory_cache[key] = value
        asyncio.create_task(self._expire_memory(key))

        # L2: Redis
        await self.redis_cache.set(key, value, self.redis_ttl)

    async def _expire_memory(self, key: str):
        """Expire memory cache entry."""
        await asyncio.sleep(self.memory_ttl)
        self.memory_cache.pop(key, None)

    async def invalidate(self, key: str):
        """Инвалидировать кэш на всех уровнях."""
        self.memory_cache.pop(key, None)
        await self.redis_cache.delete(key)
```

---

## Connection Pooling

### Database Connection Pool Management

```python
import asyncpg
from contextlib import asynccontextmanager

class PoolManager:
    """Менеджер пула соединений с базой данных."""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def initialize(self):
        """Инициализация пула соединений."""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=5,        # Минимум соединений
            max_size=20,       # Максимум соединений
            max_queries=50000, # Максимум запросов на соединение
            max_inactive_connection_lifetime=300,  # 5 минут
            command_timeout=60,
            server_settings={
                'jit': 'off',  # Отключение JIT для стабильности
                'application_name': 'archon_agent'
            }
        )

    @asynccontextmanager
    async def acquire(self):
        """Получить соединение из пула."""
        async with self.pool.acquire() as conn:
            yield conn

    async def close(self):
        """Закрыть пул соединений."""
        await self.pool.close()

# Usage
async def main():
    pool_manager = PoolManager("postgresql://...")
    await pool_manager.initialize()

    try:
        # Использование пула
        async with pool_manager.acquire() as conn:
            result = await conn.fetchval("SELECT version()")
            print(result)
    finally:
        await pool_manager.close()
```

---

## Rate Limiting

### Token Bucket Rate Limiter

```python
import time
import asyncio
from typing import Optional

class TokenBucket:
    """Rate limiter с алгоритмом Token Bucket."""

    def __init__(self, rate: float, capacity: int):
        """
        Args:
            rate: Количество токенов в секунду
            capacity: Максимальная вместимость bucket
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> bool:
        """Попытка получить токены."""
        async with self.lock:
            # Обновление количества токенов
            now = time.time()
            elapsed = now - self.last_update
            self.tokens = min(
                self.capacity,
                self.tokens + elapsed * self.rate
            )
            self.last_update = now

            # Проверка доступности токенов
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            return False

    async def wait_and_acquire(self, tokens: int = 1):
        """Подождать и получить токены."""
        while True:
            if await self.acquire(tokens):
                return

            # Подождать время до следующего токена
            wait_time = tokens / self.rate
            await asyncio.sleep(wait_time)

# Usage
class RateLimitedAPI:
    """API с rate limiting."""

    def __init__(self, rate_limit: int = 100):
        # 100 запросов в секунду
        self.limiter = TokenBucket(rate=rate_limit, capacity=rate_limit)

    async def make_request(self, url: str) -> Dict:
        """Выполнить запрос с rate limiting."""
        await self.limiter.wait_and_acquire()

        # Выполнение реального запроса
        print(f"[OK] Making request to {url}")
        # response = await http_client.get(url)
        # return response.json()
```

---

**Навигация:**
- [← Предыдущий модуль: Clean Architecture](01_clean_architecture_design_patterns.md)
- [↑ Назад к Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)
- [→ Следующий модуль: Database Optimization](03_database_optimization.md)
