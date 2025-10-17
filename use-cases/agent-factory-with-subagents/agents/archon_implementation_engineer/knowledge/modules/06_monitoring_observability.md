# Module 06: Monitoring & Observability

**Версия:** 1.0
**Дата:** 2025-10-17
**Автор:** Archon Implementation Engineer

**Назад к:** [Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- Prometheus metrics implementation (RED method: Rate/Errors/Duration)
- Structured logging с structlog в JSON формате
- Health check system с timeout, critical severity, parallel checks
- OpenTelemetry distributed tracing для microservices
- Alert Manager integration с webhook notifications
- SLO/SLI monitoring (Service Level Objectives/Indicators)
- Performance monitoring decorator для автоматического трекинга
- Three pillars of Observability: Metrics, Logs, Traces

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** мониторинг, prometheus, логи, health check, трейсинг, алерты, SLO, observability, метрики, distributed tracing, structured logging, correlation ID, spans

**English:** monitoring, prometheus, logs, health check, tracing, alerts, SLO, observability, metrics, distributed tracing, structured logging, correlation ID, spans

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Production окружение (ВСЕГДА для production)
- Debugging performance issues и bottlenecks
- Distributed tracing для microservices архитектуры
- Настройка алертов и SLO/SLI targets
- Observability для complex systems
- Proactive monitoring и incident response
- Root cause analysis для production incidents
- System reliability engineering (SRE)

---

## Comprehensive Monitoring Setup

### Prometheus Metrics Integration

```python
import logging
import time
from functools import wraps
from typing import Any, Callable, Dict
import structlog
from prometheus_client import Counter, Histogram, Gauge, Summary
import asyncio

# ═══════════════════════════════════════════════════════
# Prometheus Metrics Definitions
# ═══════════════════════════════════════════════════════

# Counters - монотонно возрастающие значения
REQUEST_COUNT = Counter(
    'agent_requests_total',
    'Total agent requests',
    ['method', 'status', 'endpoint']
)

ERROR_COUNT = Counter(
    'agent_errors_total',
    'Total agent errors',
    ['error_type', 'method']
)

# Histograms - распределение значений
REQUEST_DURATION = Histogram(
    'agent_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

LLM_TOKEN_COUNT = Histogram(
    'llm_tokens_used',
    'Number of LLM tokens used',
    ['model', 'operation'],
    buckets=[100, 500, 1000, 2000, 5000, 10000, 20000]
)

# Gauges - текущие значения, которые могут расти и падать
ACTIVE_CONNECTIONS = Gauge(
    'agent_active_connections',
    'Active agent connections'
)

QUEUE_SIZE = Gauge(
    'agent_queue_size',
    'Current queue size',
    ['queue_name']
)

CACHE_SIZE = Gauge(
    'cache_entries_total',
    'Total number of cache entries'
)

# Summary - статистика с квантилями
RESPONSE_SIZE = Summary(
    'response_size_bytes',
    'Response size in bytes',
    ['endpoint']
)

# ═══════════════════════════════════════════════════════
# Structured Logging Configuration
# ═══════════════════════════════════════════════════════

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,  # Добавляем контекстные переменные
        structlog.processors.TimeStamper(fmt="iso"),  # ISO timestamp
        structlog.processors.add_log_level,  # Добавляем уровень
        structlog.processors.StackInfoRenderer(),  # Stack traces
        structlog.processors.format_exc_info,  # Exception formatting
        structlog.processors.UnicodeDecoder(),  # UTF-8 декодирование
        structlog.processors.JSONRenderer()  # JSON output
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# ═══════════════════════════════════════════════════════
# Performance Monitoring Decorator
# ═══════════════════════════════════════════════════════

def monitor_performance(
    method: str = "unknown",
    endpoint: str = "unknown",
    track_tokens: bool = False
):
    """
    Декоратор для мониторинга производительности функций.

    Args:
        method: Название метода для метрик
        endpoint: Endpoint для группировки
        track_tokens: Отслеживать использование токенов
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status = "success"

            # Увеличиваем счетчик активных соединений
            ACTIVE_CONNECTIONS.inc()

            try:
                result = await func(*args, **kwargs)

                # Отслеживание токенов если включено
                if track_tokens and hasattr(result, 'usage'):
                    LLM_TOKEN_COUNT.labels(
                        model=getattr(result, 'model', 'unknown'),
                        operation=method
                    ).observe(result.usage.total_tokens)

                # Размер ответа
                if hasattr(result, 'data'):
                    response_size = len(str(result.data).encode('utf-8'))
                    RESPONSE_SIZE.labels(endpoint=endpoint).observe(response_size)

                return result

            except Exception as e:
                status = "error"
                error_type = type(e).__name__

                # Логирование ошибки
                logger.error(
                    "Function execution failed",
                    function=func.__name__,
                    method=method,
                    endpoint=endpoint,
                    error=str(e),
                    error_type=error_type,
                    exc_info=True
                )

                # Метрика ошибок
                ERROR_COUNT.labels(
                    error_type=error_type,
                    method=method
                ).inc()

                raise

            finally:
                # Подсчет времени выполнения
                duration = time.time() - start_time

                # Метрики
                REQUEST_DURATION.labels(
                    method=method,
                    endpoint=endpoint
                ).observe(duration)

                REQUEST_COUNT.labels(
                    method=method,
                    status=status,
                    endpoint=endpoint
                ).inc()

                ACTIVE_CONNECTIONS.dec()

                # Structured logging
                logger.info(
                    "Function executed",
                    function=func.__name__,
                    method=method,
                    endpoint=endpoint,
                    duration=duration,
                    status=status
                )

        return wrapper
    return decorator

# Usage Example
class MonitoredAgent:
    """Агент с мониторингом производительности."""

    @monitor_performance(method="query", endpoint="/api/query", track_tokens=True)
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Обработка запроса с мониторингом."""
        # Бизнес-логика
        pass
```

---

## Health Check System

### Comprehensive Health Checker

```python
from typing import Dict, Any, Callable, Optional
from enum import Enum
import asyncio

class HealthStatus(Enum):
    """Статусы здоровья компонентов."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class HealthChecker:
    """Система проверки здоровья приложения."""

    def __init__(self):
        self.checks: Dict[str, Callable] = {}
        self.check_timeouts: Dict[str, int] = {}

    def register_check(
        self,
        name: str,
        check_func: Callable,
        timeout: int = 5,
        critical: bool = True
    ):
        """
        Регистрация проверки здоровья.

        Args:
            name: Название проверки
            check_func: Async функция проверки
            timeout: Timeout в секундах
            critical: Критична ли проверка для общего статуса
        """
        self.checks[name] = {
            'func': check_func,
            'timeout': timeout,
            'critical': critical
        }

    async def check_health(self) -> Dict[str, Any]:
        """Выполнение всех проверок здоровья."""
        results = {}
        overall_status = HealthStatus.HEALTHY
        start_time = time.time()

        # Выполняем все проверки параллельно
        check_tasks = []
        for name, check_config in self.checks.items():
            task = asyncio.create_task(
                self._execute_check(name, check_config)
            )
            check_tasks.append((name, task, check_config))

        # Ждем результаты всех проверок
        for name, task, config in check_tasks:
            try:
                result = await task
                results[name] = result

                # Определяем общий статус
                if result['status'] == HealthStatus.UNHEALTHY.value:
                    if config['critical']:
                        overall_status = HealthStatus.UNHEALTHY
                    elif overall_status == HealthStatus.HEALTHY:
                        overall_status = HealthStatus.DEGRADED

            except Exception as e:
                logger.error(f"Health check {name} failed critically", error=str(e))
                results[name] = {
                    'status': HealthStatus.UNHEALTHY.value,
                    'error': str(e)
                }
                if config['critical']:
                    overall_status = HealthStatus.UNHEALTHY

        total_duration = time.time() - start_time

        return {
            'status': overall_status.value,
            'checks': results,
            'timestamp': time.time(),
            'duration_ms': int(total_duration * 1000)
        }

    async def _execute_check(
        self,
        name: str,
        config: Dict
    ) -> Dict[str, Any]:
        """Выполнение одной проверки с timeout."""
        try:
            # Выполняем с timeout
            check_result = await asyncio.wait_for(
                config['func'](),
                timeout=config['timeout']
            )

            return {
                'status': HealthStatus.HEALTHY.value,
                'details': check_result
            }

        except asyncio.TimeoutError:
            logger.warning(f"Health check {name} timed out")
            return {
                'status': HealthStatus.UNHEALTHY.value,
                'error': f'Timeout after {config["timeout"]}s'
            }

        except Exception as e:
            logger.error(f"Health check {name} failed", error=str(e))
            return {
                'status': HealthStatus.UNHEALTHY.value,
                'error': str(e)
            }

# ═══════════════════════════════════════════════════════
# Example Health Checks
# ═══════════════════════════════════════════════════════

async def database_health_check() -> Dict[str, Any]:
    """Проверка здоровья базы данных."""
    start = time.time()

    try:
        async with get_db_connection() as conn:
            # Простой запрос
            await conn.fetchval("SELECT 1")

            # Проверка количества активных соединений
            active_conns = await conn.fetchval(
                "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"
            )

        latency = (time.time() - start) * 1000

        return {
            'latency_ms': round(latency, 2),
            'active_connections': active_conns,
            'status': 'ok'
        }

    except Exception as e:
        raise Exception(f"Database unavailable: {str(e)}")

async def redis_health_check() -> Dict[str, Any]:
    """Проверка здоровья Redis."""
    start = time.time()

    try:
        # Ping Redis
        pong = await redis_client.ping()

        # Получаем информацию
        info = await redis_client.info()

        latency = (time.time() - start) * 1000

        return {
            'latency_ms': round(latency, 2),
            'used_memory_mb': round(info['used_memory'] / 1024 / 1024, 2),
            'connected_clients': info['connected_clients'],
            'status': 'ok'
        }

    except Exception as e:
        raise Exception(f"Redis unavailable: {str(e)}")

async def llm_service_health_check() -> Dict[str, Any]:
    """Проверка здоровья LLM сервиса."""
    start = time.time()

    try:
        # Простой тестовый запрос
        response = await llm_client.simple_query("test")

        latency = (time.time() - start) * 1000

        return {
            'latency_ms': round(latency, 2),
            'model': response.model,
            'status': 'ok'
        }

    except Exception as e:
        raise Exception(f"LLM service unavailable: {str(e)}")

async def queue_health_check() -> Dict[str, Any]:
    """Проверка здоровья очередей."""
    try:
        # Проверяем размер очередей
        queue_sizes = {}
        for queue_name in ['high_priority', 'normal', 'low_priority']:
            size = await get_queue_size(queue_name)
            queue_sizes[queue_name] = size
            QUEUE_SIZE.labels(queue_name=queue_name).set(size)

        # Проверяем dead letter queue
        dlq_size = await get_queue_size('dead_letter')

        return {
            'queue_sizes': queue_sizes,
            'dead_letter_queue': dlq_size,
            'status': 'ok' if dlq_size < 100 else 'warning'
        }

    except Exception as e:
        raise Exception(f"Queue system unavailable: {str(e)}")

# Setup Health Checker
health_checker = HealthChecker()
health_checker.register_check('database', database_health_check, timeout=5, critical=True)
health_checker.register_check('redis', redis_health_check, timeout=3, critical=True)
health_checker.register_check('llm_service', llm_service_health_check, timeout=10, critical=False)
health_checker.register_check('queues', queue_health_check, timeout=5, critical=False)
```

---

## Distributed Tracing

### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

# ═══════════════════════════════════════════════════════
# OpenTelemetry Setup
# ═══════════════════════════════════════════════════════

def setup_tracing(service_name: str, otlp_endpoint: str):
    """Настройка distributed tracing с OpenTelemetry."""

    # Resource - описание сервиса
    resource = Resource.create({
        "service.name": service_name,
        "service.version": "1.0.0",
        "deployment.environment": os.getenv("ENVIRONMENT", "development")
    })

    # Tracer Provider
    provider = TracerProvider(resource=resource)

    # OTLP Exporter (для Jaeger, Tempo, или другого backend)
    otlp_exporter = OTLPSpanExporter(
        endpoint=otlp_endpoint,
        insecure=True  # Используйте TLS в production
    )

    # Batch processor для оптимизации
    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)

    # Устанавливаем глобальный provider
    trace.set_tracer_provider(provider)

    # Автоинструментация библиотек
    FastAPIInstrumentor.instrument()
    AsyncPGInstrumentor().instrument()
    RedisInstrumentor().instrument()

    return trace.get_tracer(__name__)

# Usage
tracer = setup_tracing("archon-agent", "http://localhost:4317")

# ═══════════════════════════════════════════════════════
# Custom Tracing
# ═══════════════════════════════════════════════════════

async def process_with_tracing(query: str) -> Dict[str, Any]:
    """Обработка запроса с трейсингом."""

    # Создаем span для всей операции
    with tracer.start_as_current_span("process_query") as span:
        # Добавляем атрибуты
        span.set_attribute("query.length", len(query))
        span.set_attribute("query.type", "user_question")

        try:
            # Шаг 1: Валидация
            with tracer.start_as_current_span("validate_query"):
                validated = await validate_query(query)
                span.set_attribute("validation.passed", True)

            # Шаг 2: Поиск в базе знаний
            with tracer.start_as_current_span("knowledge_search") as search_span:
                results = await search_knowledge(validated)
                search_span.set_attribute("results.count", len(results))

            # Шаг 3: Генерация ответа
            with tracer.start_as_current_span("generate_response") as gen_span:
                response = await generate_response(results)
                gen_span.set_attribute("response.length", len(response))

            span.set_attribute("status", "success")
            return {"response": response, "status": "success"}

        except Exception as e:
            # Записываем ошибку в span
            span.record_exception(e)
            span.set_attribute("status", "error")
            raise
```

---

## Alerting System

### Alert Manager Integration

```python
from typing import List, Dict
import aiohttp
from enum import Enum

class AlertSeverity(Enum):
    """Уровни важности алертов."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertManager:
    """Менеджер алертов для уведомлений о проблемах."""

    def __init__(self, webhook_url: str, service_name: str):
        self.webhook_url = webhook_url
        self.service_name = service_name
        self.alert_history: List[Dict] = []

    async def send_alert(
        self,
        title: str,
        message: str,
        severity: AlertSeverity = AlertSeverity.WARNING,
        metadata: Dict = None
    ):
        """Отправка алерта в систему мониторинга."""

        alert = {
            'service': self.service_name,
            'title': title,
            'message': message,
            'severity': severity.value,
            'timestamp': time.time(),
            'metadata': metadata or {}
        }

        # Сохраняем в историю
        self.alert_history.append(alert)
        if len(self.alert_history) > 1000:
            self.alert_history.pop(0)

        # Отправляем webhook
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=alert,
                    timeout=5
                ) as response:
                    if response.status != 200:
                        logger.error(
                            "Failed to send alert",
                            status=response.status,
                            alert=title
                        )
        except Exception as e:
            logger.error("Alert delivery failed", error=str(e))

    async def check_and_alert_on_metrics(self):
        """Проверка метрик и отправка алертов при превышении порогов."""

        # Проверка error rate
        error_rate = await self._get_error_rate()
        if error_rate > 0.05:  # 5% errors
            await self.send_alert(
                "High Error Rate Detected",
                f"Error rate is {error_rate*100:.2f}%",
                severity=AlertSeverity.ERROR,
                metadata={'error_rate': error_rate}
            )

        # Проверка latency
        p95_latency = await self._get_p95_latency()
        if p95_latency > 2.0:  # 2 seconds
            await self.send_alert(
                "High Latency Detected",
                f"P95 latency is {p95_latency:.2f}s",
                severity=AlertSeverity.WARNING,
                metadata={'p95_latency': p95_latency}
            )

        # Проверка queue size
        queue_size = await self._get_queue_size()
        if queue_size > 10000:
            await self.send_alert(
                "Queue Backlog",
                f"Queue size is {queue_size}",
                severity=AlertSeverity.WARNING,
                metadata={'queue_size': queue_size}
            )
```

---

## Best Practices для Monitoring & Observability

### 1. Три столпа Observability

**Metrics (Метрики):**
- ✅ Используй RED method: Rate, Errors, Duration
- ✅ Golden signals: Latency, Traffic, Errors, Saturation
- ✅ Business metrics: пользовательская активность, конверсии

**Logs (Логи):**
- ✅ Structured logging (JSON)
- ✅ Correlation IDs для трейсинга запросов
- ✅ Правильные уровни: DEBUG, INFO, WARNING, ERROR, CRITICAL

**Traces (Трейсы):**
- ✅ Distributed tracing для microservices
- ✅ Spans для каждой важной операции
- ✅ Attributes и events для контекста

### 2. Alerting Best Practices

```python
# ✅ ПРАВИЛЬНО - конкретный, actionable alert
alert_manager.send_alert(
    "Database connection pool exhausted",
    "All 20 connections in use for 5+ minutes. "
    "Consider scaling up or investigating slow queries.",
    severity=AlertSeverity.CRITICAL,
    metadata={
        'active_connections': 20,
        'max_connections': 20,
        'slow_queries_count': 15
    }
)

# ❌ НЕПРАВИЛЬНО - неконкретный alert
alert_manager.send_alert(
    "Something wrong",
    "Check the system",
    severity=AlertSeverity.ERROR
)
```

### 3. SLO/SLI Monitoring

```python
# Service Level Indicators (SLI)
availability_sli = successful_requests / total_requests
latency_sli = requests_under_100ms / total_requests

# Service Level Objectives (SLO)
AVAILABILITY_SLO = 0.999  # 99.9% uptime
LATENCY_SLO = 0.95  # 95% requests under 100ms

# Проверка SLO
if availability_sli < AVAILABILITY_SLO:
    alert_manager.send_alert(
        "SLO Breach: Availability",
        f"Current: {availability_sli*100:.2f}%, Target: {AVAILABILITY_SLO*100}%",
        severity=AlertSeverity.CRITICAL
    )
```

---

**Навигация:**
- [← Предыдущий модуль: Deployment & DevOps](05_deployment_devops.md)
- [↑ Назад к Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)
