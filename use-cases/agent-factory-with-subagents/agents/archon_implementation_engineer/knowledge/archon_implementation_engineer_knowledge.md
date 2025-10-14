# Archon Implementation Engineer Agent - Knowledge Base

## 📚 Общие правила для всех агентов

**ОБЯЗАТЕЛЬНО ПЕРЕД НАЧАЛОМ РАБОТЫ:** Прочитай [Общие правила агентов](../_shared/agent_common_rules.md)

Все агенты следуют единым правилам workflow, качества и взаимодействия. Общие правила содержат:
- ✅ Переключение в роль (обязательно)
- ✅ Workflow и приоритизация
- ✅ Управление задачами (Archon + TodoWrite)
- ✅ Git интеграция и стандарты кодирования
- ✅ Post-Task Checklist (последний пункт каждой задачи)
- ✅ Протоколы анализа проблем и эскалации
- ✅ Заборона ярликів та токен-економії

---

## 🎭 СИСТЕМНЫЙ ПРОМПТ РОЛИ: Archon Implementation Engineer Agent

**Ты - Archon Implementation Engineer Agent**, эксперт в [ОБЛАСТЬ ЭКСПЕРТИЗЫ].

### ⚠️ ОБЯЗАТЕЛЬНО ПЕРЕД НАЧАЛОМ РАБОТЫ:
**ПРОЧИТАЙ:** [`agent_common_rules.md`](../_shared/agent_common_rules.md) - содержит критически важные правила workflow, качества и эскалации.

## Системный промпт для Archon Implementation Engineer

```
Ты ведущий инженер-разработчик команды Archon - специалист по превращению технических спецификаций в высококачественный, производительный код. Твоя экспертиза охватывает весь стек современных технологий.

**Твоя экспертиза:**
- Pydantic AI и современные LLM фреймворки
- Python/TypeScript/Go разработка
- Микросервисная архитектура и API дизайн
- Database design и optimization (PostgreSQL, Redis, Vector DB)
- Cloud infrastructure (AWS, GCP, Azure)
- DevOps и CI/CD пайплайны
- Performance optimization и профилирование

**Ключевые области разработки:**

1. **AI Agent Development:**
   - Pydantic AI агенты с инструментами и валидацией
   - RAG системы и vector search
   - LLM интеграции и prompt engineering
   - Cost optimization и model selection

2. **Backend Development:**
   - FastAPI/Flask RESTful APIs
   - Асинхронное программирование
   - Database design и ORM (SQLAlchemy, Prisma)
   - Caching strategies (Redis, Memcached)

3. **Frontend Development:**
   - Next.js 14 App Router архитектура
   - TypeScript и type-safe development
   - React Server Components
   - Performance optimization

4. **Infrastructure & DevOps:**
   - Docker containerization
   - Kubernetes orchestration
   - CI/CD с GitHub Actions/GitLab CI
   - Monitoring и observability

**Подход к работе:**
1. Начинай с понимания технических требований
2. Выбирай оптимальные технологии для задачи
3. Пиши чистый, тестируемый, документированный код
4. Следуй принципам SOLID и clean architecture
5. Оптимизируй производительность с самого начала
```

## Архитектурные паттерны

### Clean Architecture for AI Agents
```python
# Структура Pydantic AI агента по Clean Architecture
from typing import Protocol, Dict, Any
from pydantic_ai import Agent, RunContext
from abc import ABC, abstractmethod

# Domain Layer - Business Logic
class AgentUseCase(ABC):
    """Абстрактный use case для агента."""

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнить бизнес-логику агента."""
        pass

class ProcessUserQueryUseCase(AgentUseCase):
    """Use case для обработки пользовательских запросов."""

    def __init__(self, knowledge_service, validation_service):
        self.knowledge_service = knowledge_service
        self.validation_service = validation_service

    async def execute(self, query: str) -> Dict[str, Any]:
        # Валидация входных данных
        validated_query = await self.validation_service.validate(query)

        # Поиск релевантной информации
        context = await self.knowledge_service.search(validated_query)

        # Формирование ответа
        return {
            "query": validated_query,
            "context": context,
            "status": "success"
        }

# Application Layer - Agent Implementation
@dataclass
class AgentDependencies:
    """Зависимости агента."""
    knowledge_service: 'KnowledgeService'
    validation_service: 'ValidationService'
    settings: 'AgentSettings'

def create_agent(deps: AgentDependencies) -> Agent:
    """Factory для создания агента."""

    agent = Agent(
        model=deps.settings.model,
        deps_type=AgentDependencies,
        system_prompt=deps.settings.system_prompt
    )

    @agent.tool
    async def search_knowledge(ctx: RunContext[AgentDependencies], query: str) -> str:
        """Поиск в базе знаний."""
        use_case = ProcessUserQueryUseCase(
            ctx.deps.knowledge_service,
            ctx.deps.validation_service
        )
        result = await use_case.execute(query)
        return result

    return agent

# Infrastructure Layer - External Services
class KnowledgeService:
    """Сервис для работы с базой знаний."""

    def __init__(self, vector_db, embedding_model):
        self.vector_db = vector_db
        self.embedding_model = embedding_model

    async def search(self, query: str) -> List[Dict]:
        embedding = await self.embedding_model.encode(query)
        results = await self.vector_db.similarity_search(embedding)
        return results
```

### Repository Pattern для Data Access
```python
from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar
import asyncpg
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class Repository(ABC, Generic[T]):
    """Абстрактный репозиторий."""

    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

class PostgreSQLRepository(Repository[T]):
    """Реализация репозитория для PostgreSQL."""

    def __init__(self, pool: asyncpg.Pool, table_name: str, model_class):
        self.pool = pool
        self.table_name = table_name
        self.model_class = model_class

    async def create(self, entity: T) -> T:
        async with self.pool.acquire() as conn:
            data = entity.model_dump()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(f'${i+1}' for i in range(len(data)))

            query = f"""
                INSERT INTO {self.table_name} ({columns})
                VALUES ({placeholders})
                RETURNING *
            """

            row = await conn.fetchrow(query, *data.values())
            return self.model_class(**dict(row))

    async def get_by_id(self, id: str) -> Optional[T]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                f"SELECT * FROM {self.table_name} WHERE id = $1", id
            )
            return self.model_class(**dict(row)) if row else None

# Usage Example
class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str

class UserRepository(PostgreSQLRepository[User]):
    def __init__(self, pool: asyncpg.Pool):
        super().__init__(pool, "users", User)

# Service Layer
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        return await self.user_repo.create(user)
```

## Performance Optimization Patterns

### Async Programming Best Practices
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
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        self.executor.shutdown()

    async def parallel_api_calls(self, urls: List[str]) -> List[Dict]:
        """Параллельные вызовы API."""
        tasks = [self.fetch_data(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Фильтрация успешных результатов
        return [r for r in results if not isinstance(r, Exception)]

    async def fetch_data(self, url: str) -> Dict:
        """Получение данных с retry логикой."""
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
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

    async def cpu_intensive_task(self, data: List[Dict]) -> List[Dict]:
        """CPU-интенсивная задача в thread pool."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.process_data_sync,
            data
        )

    def process_data_sync(self, data: List[Dict]) -> List[Dict]:
        """Синхронная обработка данных."""
        # Сложные вычисления
        return [self.transform_item(item) for item in data]

    def transform_item(self, item: Dict) -> Dict:
        # Тяжелые вычисления
        time.sleep(0.01)  # Имитация работы
        return {"processed": True, **item}

# Usage with context manager
async def main():
    async with PerformanceOptimizedAgent() as agent:
        urls = ["http://api1.com", "http://api2.com", "http://api3.com"]
        results = await agent.parallel_api_calls(urls)
        processed = await agent.cpu_intensive_task(results)
        return processed
```

### Caching Strategies
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
        """Сохранить значение в кэш."""
        await self.redis.setex(key, ttl, pickle.dumps(value))

    async def delete(self, key: str):
        """Удалить значение из кэша."""
        await self.redis.delete(key)

    async def clear_pattern(self, pattern: str):
        """Очистить кэш по паттерну."""
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)

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
    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager

    @cached(ttl=1800, key_prefix="data_service")
    async def expensive_computation(self, param1: str, param2: int, cache_manager=None) -> Dict:
        """Дорогая операция с кэшированием."""
        # Симуляция тяжелых вычислений
        await asyncio.sleep(2)
        return {"result": f"processed_{param1}_{param2}"}
```

## Database Optimization

### Efficient Database Operations
```python
import asyncpg
from typing import List, Dict, Any
from contextlib import asynccontextmanager

class OptimizedDatabase:
    """Оптимизированная работа с базой данных."""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def initialize(self):
        """Инициализация пула соединений."""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=5,
            max_size=20,
            command_timeout=60,
            server_settings={
                'jit': 'off',  # Отключение JIT для стабильности
                'application_name': 'archon_agent'
            }
        )

    @asynccontextmanager
    async def transaction(self):
        """Контекстный менеджер для транзакций."""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                yield conn

    async def bulk_insert(self, table: str, data: List[Dict[str, Any]]) -> int:
        """Массовая вставка данных."""
        if not data:
            return 0

        columns = list(data[0].keys())
        values = [list(row.values()) for row in data]

        async with self.pool.acquire() as conn:
            result = await conn.copy_records_to_table(
                table,
                records=values,
                columns=columns
            )
            return len(values)

    async def execute_query_with_pagination(
        self,
        base_query: str,
        params: List[Any],
        page_size: int = 1000
    ) -> List[Dict]:
        """Выполнение запроса с пагинацией."""
        all_results = []
        offset = 0

        async with self.pool.acquire() as conn:
            while True:
                paginated_query = f"{base_query} LIMIT {page_size} OFFSET {offset}"
                rows = await conn.fetch(paginated_query, *params)

                if not rows:
                    break

                all_results.extend([dict(row) for row in rows])
                offset += page_size

                if len(rows) < page_size:
                    break

        return all_results

    async def explain_query(self, query: str, params: List[Any] = None) -> Dict:
        """Анализ плана выполнения запроса."""
        explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"

        async with self.pool.acquire() as conn:
            result = await conn.fetchval(explain_query, *(params or []))
            return result[0]  # JSON результат

# Indexing Strategies
OPTIMIZED_INDEXES = """
-- Индексы для производительности

-- Составной индекс для поиска по нескольким полям
CREATE INDEX CONCURRENTLY idx_users_name_email
ON users (name, email)
WHERE active = true;

-- Частичный индекс для активных записей
CREATE INDEX CONCURRENTLY idx_users_active
ON users (created_at)
WHERE active = true;

-- GIN индекс для полнотекстового поиска
CREATE INDEX CONCURRENTLY idx_documents_search
ON documents USING gin(to_tsvector('english', title || ' ' || content));

-- Индекс для JSON полей
CREATE INDEX CONCURRENTLY idx_metadata_tags
ON documents USING gin((metadata->>'tags'));

-- Covering index для избежания table lookup
CREATE INDEX CONCURRENTLY idx_users_covering
ON users (id) INCLUDE (name, email, created_at)
WHERE active = true;
"""
```

### Vector Database Optimization
```python
import numpy as np
from typing import List, Tuple
import faiss
import pickle

class OptimizedVectorStore:
    """Оптимизированное хранилище векторов."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = None
        self.metadata = []

    def build_index(self, vectors: np.ndarray, use_gpu: bool = False):
        """Построение оптимизированного индекса."""
        n_vectors = vectors.shape[0]

        if n_vectors < 10000:
            # Для малых данных - простой L2 поиск
            self.index = faiss.IndexFlatL2(self.dimension)
        elif n_vectors < 100000:
            # Средние данные - IVF с 100 кластерами
            nlist = min(100, n_vectors // 100)
            self.index = faiss.IndexIVFFlat(
                faiss.IndexFlatL2(self.dimension),
                self.dimension,
                nlist
            )
        else:
            # Большие данные - HNSW для быстрого поиска
            self.index = faiss.IndexHNSWFlat(self.dimension, 32)
            self.index.hnsw.efConstruction = 200
            self.index.hnsw.efSearch = 50

        if use_gpu and faiss.get_num_gpus() > 0:
            self.index = faiss.index_cpu_to_gpu(
                faiss.StandardGpuResources(), 0, self.index
            )

        # Обучение индекса (для IVF)
        if hasattr(self.index, 'train'):
            self.index.train(vectors)

        # Добавление векторов
        self.index.add(vectors)

    def search(self, query_vector: np.ndarray, k: int = 10) -> Tuple[List[float], List[int]]:
        """Поиск ближайших векторов."""
        query_vector = query_vector.reshape(1, -1).astype(np.float32)
        distances, indices = self.index.search(query_vector, k)
        return distances[0].tolist(), indices[0].tolist()

    def batch_search(self, query_vectors: np.ndarray, k: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """Пакетный поиск для множества запросов."""
        return self.index.search(query_vectors.astype(np.float32), k)

    def save_index(self, filepath: str):
        """Сохранение индекса на диск."""
        faiss.write_index(self.index, f"{filepath}.faiss")
        with open(f"{filepath}.metadata", 'wb') as f:
            pickle.dump(self.metadata, f)

    def load_index(self, filepath: str):
        """Загрузка индекса с диска."""
        self.index = faiss.read_index(f"{filepath}.faiss")
        with open(f"{filepath}.metadata", 'rb') as f:
            self.metadata = pickle.load(f)
```

## Testing Strategies

### Comprehensive Testing Framework
```python
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from pydantic_ai.models.test import TestModel
from pydantic_ai import Agent

class TestAgentFramework:
    """Фреймворк для тестирования AI агентов."""

    @pytest.fixture
    async def test_agent(self):
        """Создание тестового агента."""
        # Мокаем внешние зависимости
        mock_dependencies = MagicMock()
        mock_dependencies.knowledge_service = AsyncMock()
        mock_dependencies.validation_service = AsyncMock()

        # Создаем агента с тестовой моделью
        agent = Agent(
            model=TestModel(),
            deps_type=type(mock_dependencies)
        )

        @agent.tool
        async def mock_search(ctx, query: str) -> str:
            return f"Mock result for: {query}"

        return agent, mock_dependencies

    @pytest.mark.asyncio
    async def test_agent_basic_functionality(self, test_agent):
        """Тест базовой функциональности агента."""
        agent, deps = test_agent

        result = await agent.run("Test query", deps=deps)

        assert result.data is not None
        assert isinstance(result.data, str)

    @pytest.mark.asyncio
    async def test_agent_tool_usage(self, test_agent):
        """Тест использования инструментов агентом."""
        agent, deps = test_agent

        # Настраиваем TestModel для использования инструментов
        result = await agent.run(
            "Use the search tool to find information",
            deps=deps
        )

        assert "Mock result" in str(result.data)

    @pytest.mark.asyncio
    async def test_error_handling(self, test_agent):
        """Тест обработки ошибок."""
        agent, deps = test_agent

        # Мокаем ошибку в зависимости
        deps.knowledge_service.search.side_effect = Exception("Test error")

        # Агент должен gracefully обработать ошибку
        result = await agent.run("Query that causes error", deps=deps)

        # Проверяем, что агент обработал ошибку
        assert result.data is not None

# Performance Testing
class PerformanceTestSuite:
    """Набор тестов производительности."""

    @pytest.mark.performance
    async def test_concurrent_requests(self, test_agent):
        """Тест производительности при конкурентных запросах."""
        agent, deps = test_agent

        # Создаем множественные конкурентные запросы
        tasks = [
            agent.run(f"Query {i}", deps=deps)
            for i in range(100)
        ]

        start_time = asyncio.get_event_loop().time()
        results = await asyncio.gather(*tasks)
        end_time = asyncio.get_event_loop().time()

        # Проверяем производительность
        total_time = end_time - start_time
        assert total_time < 10.0  # Все запросы за 10 секунд
        assert len(results) == 100
        assert all(r.data is not None for r in results)

    @pytest.mark.performance
    async def test_memory_usage(self, test_agent):
        """Тест использования памяти."""
        import psutil
        import os

        agent, deps = test_agent

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Выполняем множество операций
        for i in range(1000):
            await agent.run(f"Query {i}", deps=deps)

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Проверяем, что память не утекает
        assert memory_increase < 100 * 1024 * 1024  # Менее 100MB увеличения

# Integration Testing
@pytest.mark.integration
class IntegrationTestSuite:
    """Интеграционные тесты."""

    async def test_full_pipeline(self):
        """Тест полного пайплайна агента."""
        # Настройка реальных зависимостей
        from your_app.dependencies import RealDependencies
        from your_app.agent import create_agent

        deps = RealDependencies()
        await deps.initialize()

        try:
            agent = create_agent(deps)
            result = await agent.run("Real query", deps=deps)

            assert result.data is not None
            # Дополнительные проверки для интеграционного теста

        finally:
            await deps.cleanup()
```

## Deployment & DevOps

### Docker Optimization
```dockerfile
# Multi-stage build для оптимизации размера
FROM python:3.11-slim as builder

# Установка зависимостей сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Production stage
FROM python:3.11-slim

# Создание пользователя для безопасности
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование установленных пакетов
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Создание рабочей директории
WORKDIR /app

# Копирование кода приложения
COPY --chown=appuser:appuser . .

# Переключение на пользователя
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Команда запуска
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: archon-agent
  labels:
    app: archon-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: archon-agent
  template:
    metadata:
      labels:
        app: archon-agent
    spec:
      containers:
      - name: archon-agent
        image: archon-agent:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: archon-secrets
              key: database-url
        - name: LLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: archon-secrets
              key: llm-api-key
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: archon-agent-service
spec:
  selector:
    app: archon-agent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## Monitoring & Observability

### Comprehensive Monitoring Setup
```python
import logging
import time
from functools import wraps
from typing import Any, Callable
import structlog
from prometheus_client import Counter, Histogram, Gauge
import asyncio

# Metrics
REQUEST_COUNT = Counter('agent_requests_total', 'Total agent requests', ['method', 'status'])
REQUEST_DURATION = Histogram('agent_request_duration_seconds', 'Request duration')
ACTIVE_CONNECTIONS = Gauge('agent_active_connections', 'Active connections')

# Structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

def monitor_performance(func: Callable) -> Callable:
    """Декоратор для мониторинга производительности."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        status = "success"

        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            status = "error"
            logger.error("Function execution failed",
                        function=func.__name__,
                        error=str(e))
            raise
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.observe(duration)
            REQUEST_COUNT.labels(method=func.__name__, status=status).inc()

            logger.info("Function executed",
                       function=func.__name__,
                       duration=duration,
                       status=status)

    return wrapper

class HealthChecker:
    """Система проверки здоровья приложения."""

    def __init__(self):
        self.checks = {}

    def register_check(self, name: str, check_func: Callable):
        """Регистрация проверки здоровья."""
        self.checks[name] = check_func

    async def check_health(self) -> Dict[str, Any]:
        """Выполнение всех проверок здоровья."""
        results = {}
        overall_status = "healthy"

        for name, check_func in self.checks.items():
            try:
                result = await check_func()
                results[name] = {"status": "healthy", "details": result}
            except Exception as e:
                results[name] = {"status": "unhealthy", "error": str(e)}
                overall_status = "unhealthy"

                logger.error("Health check failed",
                           check_name=name,
                           error=str(e))

        return {
            "status": overall_status,
            "checks": results,
            "timestamp": time.time()
        }

# Example health checks
async def database_health_check():
    """Проверка здоровья базы данных."""
    # Попытка выполнить простой запрос
    async with get_db_connection() as conn:
        await conn.fetchval("SELECT 1")
    return {"latency": "< 10ms"}

async def llm_service_health_check():
    """Проверка здоровья LLM сервиса."""
    # Тестовый запрос к LLM
    try:
        response = await llm_client.simple_query("test")
        return {"status": "responsive", "model": response.model}
    except Exception:
        raise Exception("LLM service unavailable")
```

## Best Practices для Implementation Engineer

### 1. Code Quality Guidelines
- **Type Hints**: Всегда используй типизацию
- **Documentation**: Docstrings для всех публичных функций
- **Error Handling**: Explicit exception handling
- **Testing**: Минимум 80% покрытие тестами

### 2. Performance Optimization
- **Async/Await**: Для I/O операций
- **Caching**: Redis/Memcached для частых запросов
- **Database**: Оптимизированные запросы и индексы
- **Monitoring**: Постоянный мониторинг метрик

### 3. Security Implementation
- **Input Validation**: Pydantic модели для валидации
- **Authentication**: JWT tokens, OAuth 2.0
- **Secrets Management**: Environment variables, HashiCorp Vault
- **SQL Injection**: Parameterized queries only

### 4. Deployment Strategy
- **Containerization**: Docker для консистентности
- **Health Checks**: Liveness и readiness probes
- **Scaling**: Horizontal автомасштабирование
- **CI/CD**: Автоматизированное тестирование и деплой

---

## 🔍 ДОМЕННЫЕ ЗНАНИЯ: [ОБЛАСТЬ]

```python
```python
```python
```python
```python
```python
```python
```python
### 1. Code Quality Guidelines
### 2. Performance Optimization
### 3. Security Implementation

---

**Версия:** 2.0 (Модульная архитектура)
**Дата рефакторинга:** 2025-10-14
**Автор рефакторинга:** Archon Blueprint Architect
