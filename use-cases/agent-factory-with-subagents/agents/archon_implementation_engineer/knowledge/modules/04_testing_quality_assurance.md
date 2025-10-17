# Module 04: Testing & Quality Assurance

**Версия:** 1.0
**Дата:** 2025-10-17
**Автор:** Archon Implementation Engineer

**Назад к:** [Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- TestModel vs Real Model для unit/integration тестирования
- Performance testing: concurrent requests, memory leaks, percentiles
- Error recovery и retry logic testing
- Tool calls validation и sequence testing
- Integration testing с реальными зависимостями (PostgreSQL, Redis, Vector DB)
- Memory leak detection с psutil и gc
- Response time SLA проверки (P50, P95, P99)
- 70/20/10 coverage strategy implementation (Unit/Integration/E2E)

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** тестирование, pytest, TestModel, integration tests, performance tests, покрытие кода, unit tests, мокирование, assertions, retry logic, error handling, percentiles, CI/CD testing, regression tests

**English:** testing, pytest, TestModel, integration tests, performance tests, code coverage, unit tests, mocking, assertions, retry logic, error handling, percentiles, CI/CD testing, regression tests

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Разработка production кода для AI агентов
- Обеспечение надежности и качества агентов
- Performance regression testing необходим
- CI/CD pipeline setup и автоматизация тестов
- Написание новых features с тестами
- Проверка error recovery механизмов
- Валидация SLA требований (latency, throughput)
- Необходимость 80%+ test coverage

---

## Comprehensive Testing Framework для AI Agents

### Базовая структура тестирования

```python
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from pydantic_ai.models.test import TestModel
from pydantic_ai import Agent, RunContext
from typing import Dict, Any, List

class TestAgentFramework:
    """Фреймворк для тестирования AI агентов."""

    @pytest.fixture
    async def test_agent(self):
        """Создание тестового агента с моками."""
        # Мокаем внешние зависимости
        mock_dependencies = MagicMock()
        mock_dependencies.knowledge_service = AsyncMock()
        mock_dependencies.validation_service = AsyncMock()
        mock_dependencies.cache_manager = AsyncMock()

        # Настройка моков
        mock_dependencies.knowledge_service.search.return_value = [
            {"title": "Test Result", "content": "Test Content"}
        ]
        mock_dependencies.validation_service.validate.return_value = True

        # Создаем агента с тестовой моделью
        agent = Agent(
            model=TestModel(),
            deps_type=type(mock_dependencies),
            system_prompt="Test agent for unit testing"
        )

        @agent.tool
        async def mock_search(ctx: RunContext, query: str) -> str:
            """Mock инструмент поиска."""
            return f"Mock result for: {query}"

        @agent.tool
        async def mock_validate(ctx: RunContext, data: Dict) -> bool:
            """Mock инструмент валидации."""
            return True

        return agent, mock_dependencies

    @pytest.mark.asyncio
    async def test_agent_basic_functionality(self, test_agent):
        """Тест базовой функциональности агента."""
        agent, deps = test_agent

        result = await agent.run("Test query", deps=deps)

        assert result.data is not None
        assert isinstance(result.data, str)
        assert len(result.data) > 0

    @pytest.mark.asyncio
    async def test_agent_tool_usage(self, test_agent):
        """Тест использования инструментов агентом."""
        agent, deps = test_agent

        # Настраиваем TestModel для использования инструментов
        result = await agent.run(
            "Use the search tool to find information about Python",
            deps=deps
        )

        assert result.data is not None
        assert "Mock result" in str(result.data)

    @pytest.mark.asyncio
    async def test_agent_error_handling(self, test_agent):
        """Тест обработки ошибок."""
        agent, deps = test_agent

        # Мокаем ошибку в зависимости
        deps.knowledge_service.search.side_effect = Exception("Database connection failed")

        # Агент должен gracefully обработать ошибку
        result = await agent.run("Query that causes error", deps=deps)

        # Проверяем, что агент обработал ошибку и вернул результат
        assert result.data is not None
        # В реальном агенте должна быть логика fallback

    @pytest.mark.asyncio
    async def test_agent_multiple_tools(self, test_agent):
        """Тест последовательного вызова нескольких инструментов."""
        agent, deps = test_agent

        result = await agent.run(
            "Search for Python and then validate the results",
            deps=deps
        )

        assert result.data is not None
        # Проверяем, что оба инструмента были задействованы
```

### Тестирование с реальной моделью

```python
@pytest.mark.integration
class TestRealModelIntegration:
    """Тесты с реальной LLM моделью (integration tests)."""

    @pytest.fixture
    async def real_agent(self):
        """Создание агента с реальной моделью."""
        # Используем OpenAI или Anthropic модель
        agent = Agent(
            model='openai:gpt-4',  # Или 'anthropic:claude-3-5-sonnet-20241022'
            system_prompt="Production-ready agent"
        )

        @agent.tool
        async def real_search(ctx: RunContext, query: str) -> Dict:
            """Реальный инструмент поиска."""
            # Реальная реализация
            pass

        return agent

    @pytest.mark.asyncio
    async def test_real_model_response(self, real_agent):
        """Тест с реальной моделью (требует API ключ)."""
        # Skip если нет API ключа
        import os
        if not os.getenv('OPENAI_API_KEY'):
            pytest.skip("OPENAI_API_KEY not set")

        result = await real_agent.run("What is Python?")

        assert result.data is not None
        assert len(result.data) > 50  # Проверяем достаточность ответа
        assert "python" in result.data.lower()
```

---

## Performance Testing

### Тесты производительности

```python
import time
import psutil
import os
from statistics import mean, stdev

class PerformanceTestSuite:
    """Набор тестов производительности."""

    @pytest.mark.performance
    async def test_concurrent_requests(self, test_agent):
        """Тест производительности при конкурентных запросах."""
        agent, deps = test_agent

        # Создаем множественные конкурентные запросы
        num_requests = 100
        tasks = [
            agent.run(f"Query number {i}", deps=deps)
            for i in range(num_requests)
        ]

        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # Проверяем производительность
        total_time = end_time - start_time
        avg_time_per_request = total_time / num_requests

        assert total_time < 10.0  # Все запросы за 10 секунд
        assert len(results) == num_requests
        assert all(r.data is not None for r in results)

        print(f"\n[OK] Performance metrics:")
        print(f"    Total time: {total_time:.2f}s")
        print(f"    Avg per request: {avg_time_per_request:.3f}s")
        print(f"    Requests per second: {num_requests/total_time:.2f}")

    @pytest.mark.performance
    async def test_memory_usage(self, test_agent):
        """Тест использования памяти (проверка memory leaks)."""
        agent, deps = test_agent

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Выполняем множество операций
        for i in range(1000):
            await agent.run(f"Query {i}", deps=deps)

            # Принудительная сборка мусора каждые 100 запросов
            if i % 100 == 0:
                import gc
                gc.collect()

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        print(f"\n[OK] Memory usage:")
        print(f"    Initial: {initial_memory:.2f} MB")
        print(f"    Final: {final_memory:.2f} MB")
        print(f"    Increase: {memory_increase:.2f} MB")

        # Проверяем, что память не утекает
        assert memory_increase < 100  # Менее 100MB увеличения

    @pytest.mark.performance
    async def test_response_time_percentiles(self, test_agent):
        """Тест перцентилей времени ответа."""
        agent, deps = test_agent

        response_times = []

        # Выполняем серию запросов
        for i in range(100):
            start = time.time()
            await agent.run(f"Query {i}", deps=deps)
            response_times.append(time.time() - start)

        # Вычисляем статистику
        sorted_times = sorted(response_times)
        p50 = sorted_times[49]  # Медиана
        p95 = sorted_times[94]
        p99 = sorted_times[98]

        print(f"\n[OK] Response time percentiles:")
        print(f"    P50 (median): {p50:.3f}s")
        print(f"    P95: {p95:.3f}s")
        print(f"    P99: {p99:.3f}s")
        print(f"    Mean: {mean(response_times):.3f}s")
        print(f"    StdDev: {stdev(response_times):.3f}s")

        # SLA проверки
        assert p50 < 0.5  # 50% запросов быстрее 0.5s
        assert p95 < 2.0  # 95% запросов быстрее 2s
        assert p99 < 5.0  # 99% запросов быстрее 5s
```

---

## Integration Testing

### Интеграционные тесты с реальными зависимостями

```python
@pytest.mark.integration
class IntegrationTestSuite:
    """Интеграционные тесты с реальными сервисами."""

    @pytest.fixture(scope="class")
    async def real_dependencies(self):
        """Инициализация реальных зависимостей для интеграционных тестов."""
        from your_app.dependencies import RealDependencies

        deps = RealDependencies(
            database_url=os.getenv('TEST_DATABASE_URL'),
            redis_url=os.getenv('TEST_REDIS_URL'),
            llm_api_key=os.getenv('OPENAI_API_KEY')
        )

        # Инициализация
        await deps.initialize()

        yield deps

        # Cleanup после всех тестов
        await deps.cleanup()

    async def test_full_pipeline(self, real_dependencies):
        """Тест полного пайплайна агента с реальными сервисами."""
        from your_app.agent import create_agent

        agent = create_agent(real_dependencies)

        # Реальный запрос
        result = await agent.run(
            "Search for information about Python programming",
            deps=real_dependencies
        )

        assert result.data is not None
        assert len(result.data) > 0

        # Проверяем, что данные были записаны в БД
        async with real_dependencies.db_pool.acquire() as conn:
            query_log = await conn.fetchrow(
                "SELECT * FROM query_logs ORDER BY created_at DESC LIMIT 1"
            )
            assert query_log is not None
            assert "Python" in query_log['query']

    async def test_database_integration(self, real_dependencies):
        """Тест интеграции с базой данных."""
        async with real_dependencies.db_pool.acquire() as conn:
            # Тестовая запись
            test_user = await conn.fetchrow("""
                INSERT INTO users (name, email)
                VALUES ($1, $2)
                RETURNING *
            """, "Test User", "test@example.com")

            assert test_user is not None
            assert test_user['name'] == "Test User"

            # Очистка после теста
            await conn.execute("DELETE FROM users WHERE email = $1", "test@example.com")

    async def test_redis_integration(self, real_dependencies):
        """Тест интеграции с Redis."""
        cache = real_dependencies.cache_manager

        # Тестируем set/get
        await cache.set("test_key", {"data": "test_value"}, ttl=60)
        result = await cache.get("test_key")

        assert result is not None
        assert result['data'] == "test_value"

        # Cleanup
        await cache.delete("test_key")

    async def test_vector_db_integration(self, real_dependencies):
        """Тест интеграции с vector database."""
        vector_service = real_dependencies.vector_service

        # Тестовый embedding
        test_text = "This is a test document for vector search"
        embedding = await vector_service.embed_text(test_text)

        assert len(embedding) > 0
        assert isinstance(embedding[0], float)

        # Поиск похожих
        similar = await vector_service.search_similar(embedding, k=5)
        assert len(similar) <= 5
```

---

## Тестирование специфичных сценариев

### Retry логика и error recovery

```python
class TestErrorRecovery:
    """Тесты обработки ошибок и retry логики."""

    @pytest.mark.asyncio
    async def test_retry_on_transient_error(self, test_agent):
        """Тест retry при временных ошибках."""
        agent, deps = test_agent

        call_count = 0

        async def failing_then_success(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Temporary network error")
            return [{"title": "Success", "content": "Data"}]

        deps.knowledge_service.search = AsyncMock(side_effect=failing_then_success)

        # Агент должен успешно выполнить запрос после ретраев
        with patch('asyncio.sleep'):  # Ускоряем тест
            result = await agent.run("Test query with retries", deps=deps)

        assert result.data is not None
        assert call_count == 3  # Провалились 2 раза, успех на 3-й

    @pytest.mark.asyncio
    async def test_fallback_on_critical_error(self, test_agent):
        """Тест fallback механизма при критических ошибках."""
        agent, deps = test_agent

        # Мокаем критическую ошибку
        deps.knowledge_service.search.side_effect = Exception("Database is down")

        # Агент должен использовать fallback
        result = await agent.run("Query during outage", deps=deps)

        assert result.data is not None
        # Проверяем, что используется кэшированный или default ответ
```

### Тестирование tool calls

```python
class TestToolCalls:
    """Тесты вызовов инструментов агентом."""

    @pytest.mark.asyncio
    async def test_tool_call_sequence(self, test_agent):
        """Тест последовательности вызовов инструментов."""
        agent, deps = test_agent

        tool_calls = []

        # Трекаем вызовы инструментов
        original_search = deps.knowledge_service.search

        async def tracked_search(*args, **kwargs):
            tool_calls.append(('search', args, kwargs))
            return await original_search(*args, **kwargs)

        deps.knowledge_service.search = AsyncMock(side_effect=tracked_search)

        result = await agent.run(
            "Search for Python, then search for Django",
            deps=deps
        )

        assert len(tool_calls) >= 1  # Минимум 1 вызов search
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_tool_validation(self, test_agent):
        """Тест валидации параметров инструментов."""
        agent, deps = test_agent

        # Инструмент с валидацией
        @agent.tool
        async def validated_tool(ctx: RunContext, number: int) -> str:
            """Инструмент с валидацией входных данных."""
            if number < 0:
                raise ValueError("Number must be positive")
            return f"Result: {number * 2}"

        # Тест с корректными данными
        result = await agent.run("Use the tool with number 5", deps=deps)
        assert result.data is not None

        # Тест с некорректными данными
        # TestModel может не вызвать инструмент с негативным числом
```

---

## Best Practices для тестирования AI агентов

### Когда использовать TestModel vs Real Model:

**TestModel (Unit Tests):**
- ✅ Быстрые тесты логики
- ✅ Тестирование edge cases
- ✅ CI/CD пайплайн
- ✅ Не требует API ключей
- ✅ Детерминированные результаты

**Real Model (Integration Tests):**
- ✅ Тестирование качества ответов
- ✅ End-to-end сценарии
- ✅ Pre-production тестирование
- ⚠️ Требует API ключи
- ⚠️ Медленнее
- ⚠️ Стоимость API вызовов

### Структура тестового покрытия:

```python
# Рекомендуемое распределение тестов:
# - 70% Unit tests (TestModel)
# - 20% Integration tests (Real Model + Real Dependencies)
# - 10% E2E tests (Full Production Stack)

# Пример pytest.ini:
"""
[pytest]
markers =
    unit: Unit tests (fast, no external dependencies)
    integration: Integration tests (slow, require external services)
    e2e: End-to-end tests (slowest, full stack)
    performance: Performance and load tests
"""

# Команды для запуска:
# pytest -m unit                 # Только unit tests
# pytest -m "unit or integration"  # Unit + integration
# pytest -m performance          # Только performance tests
```

---

**Навигация:**
- [← Предыдущий модуль: Database Optimization](03_database_optimization.md)
- [↑ Назад к Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)
- [→ Следующий модуль: Deployment & DevOps](05_deployment_devops.md)
