# Module 05: Monitoring & Observability

**Назад к:** [Deployment Engineer Knowledge Base](../deployment_engineer_knowledge.md)

---

## 🎯 ТРИГГЕРНАЯ СИСТЕМА - Когда читать этот модуль

### Тип 1: Ключевые слова (Keywords Triggers)
**Читай этот модуль ЕСЛИ задача содержит:**
- `prometheus`, `grafana`, `monitoring`, `observability`
- `metrics`, `alerts`, `alerting`, `alert rules`
- `tracing`, `distributed tracing`, `opentelemetry`, `jaeger`
- `histogram`, `gauge`, `counter`, `prometheus_client`
- `golden signals`, `sli`, `slo`, `service level`
- `dashboard`, `visualization`, `grafana dashboard`

### Тип 2: Сценарии использования (Scenario Triggers)
**Читай этот модуль КОГДА нужно:**
- Настроить Prometheus для сбора метрик
- Создать alert rules для приложения
- Настроить Grafana dashboard для визуализации
- Инструментировать приложение метриками (FastAPI)
- Настроить distributed tracing (OpenTelemetry + Jaeger)
- Создать SLI/SLO для сервиса
- Настроить Golden Signals monitoring
- Создать алерты для infrastructure и application
- Настроить Prometheus middleware для автоматического сбора метрик
- Интегрировать мониторинг в CI/CD pipeline

### Тип 3: Технические термины (Technical Terms Triggers)
**Читай этот модуль ЕСЛИ встречаешь:**
- Golden Signals (Latency, Traffic, Errors, Saturation)
- SLI/SLO (Service Level Indicators/Objectives)
- Prometheus exporters и scrape_configs
- histogram_quantile для расчета percentiles
- OpenTelemetry spans и трейсинг
- Jaeger distributed tracing
- Alert rules (rate, for, labels, annotations)
- Prometheus middleware для FastAPI
- Grafana datasources и provisioning
- Counter, Histogram, Gauge метрики
- Alert fatigue prevention
- Node exporter и Kubernetes service discovery

---

## 📋 СОДЕРЖАНИЕ МОДУЛЯ

**Основные темы:**
1. ✅ Prometheus Configuration (complete setup с Kubernetes service discovery)
2. ✅ Alert Rules (application + infrastructure alerts с правильными порогами)
3. ✅ Grafana Dashboards (JSON конфигурация для визуализации метрик)
4. ✅ Application Instrumentation (FastAPI metrics - Counter, Histogram, Gauge)
5. ✅ Distributed Tracing (OpenTelemetry + Jaeger интеграция)
6. ✅ Best Practices (Golden Signals, SLI/SLO, Alert Fatigue Prevention)

**Конфигурации:**
- Complete Prometheus configuration (global, alerting, scrape_configs)
- Production alert rules (HighErrorRate, HighResponseTime, ApplicationDown, HighMemoryUsage)
- Infrastructure alerts (NodeHighCPU, NodeHighMemory, DiskSpaceLow, PodCrashLooping)
- Grafana dashboard JSON (Request Rate, Response Time, Error Rate, Memory, DB Connections)
- FastAPI Prometheus middleware (automatic metrics collection)

**Инструменты:**
- Prometheus (metrics collection, alerting)
- Grafana (visualization, dashboards)
- OpenTelemetry (distributed tracing)
- Jaeger (trace visualization)
- prometheus_client (Python library)

---

## Prometheus Configuration

### Complete Prometheus Setup

```yaml
# ========================================
# prometheus.yml - Main Configuration
# ========================================
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'archon-prod'
    environment: 'production'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

# Load rules once and periodically evaluate them
rule_files:
  - "alerts/*.yml"

# Scrape configurations
scrape_configs:
  # ========================================
  # Prometheus self-monitoring
  # ========================================
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # ========================================
  # Kubernetes API server
  # ========================================
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
      - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https

  # ========================================
  # Kubernetes nodes
  # ========================================
  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)

  # ========================================
  # Kubernetes pods
  # ========================================
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name

  # ========================================
  # Application metrics
  # ========================================
  - job_name: 'archon-agent'
    static_configs:
      - targets: ['archon-agent-service:8000']
    metrics_path: /metrics
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        replacement: 'archon-agent'
```

---

## Alert Rules

### Production Alert Rules

```yaml
# ========================================
# alerts/application.yml
# ========================================
groups:
  - name: application_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
          component: application
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"

      # High response time
      - alert: HighResponseTime
        expr: |
          histogram_quantile(0.95,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1
        for: 5m
        labels:
          severity: warning
          component: application
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }}s"

      # Application down
      - alert: ApplicationDown
        expr: up{job="archon-agent"} == 0
        for: 2m
        labels:
          severity: critical
          component: application
        annotations:
          summary: "Application is down"
          description: "{{ $labels.instance }} has been down for more than 2 minutes"

      # High memory usage
      - alert: HighMemoryUsage
        expr: |
          (process_resident_memory_bytes / 1024 / 1024 / 1024) > 0.8
        for: 5m
        labels:
          severity: warning
          component: application
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value | humanize }}GB (threshold: 800MB)"

      # Database connection pool exhausted
      - alert: DatabasePoolExhausted
        expr: |
          db_pool_connections_active / db_pool_connections_max > 0.9
        for: 5m
        labels:
          severity: warning
          component: database
        annotations:
          summary: "Database connection pool nearly exhausted"
          description: "{{ $value | humanizePercentage }} of connections in use"

# ========================================
# alerts/infrastructure.yml
# ========================================
groups:
  - name: infrastructure_alerts
    interval: 30s
    rules:
      # Node high CPU
      - alert: NodeHighCPU
        expr: |
          100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 10m
        labels:
          severity: warning
          component: infrastructure
        annotations:
          summary: "High CPU usage on node"
          description: "CPU usage on {{ $labels.instance }} is {{ $value | humanize }}%"

      # Node high memory
      - alert: NodeHighMemory
        expr: |
          (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
        for: 10m
        labels:
          severity: warning
          component: infrastructure
        annotations:
          summary: "High memory usage on node"
          description: "Memory usage on {{ $labels.instance }} is {{ $value | humanize }}%"

      # Disk space low
      - alert: DiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 15
        for: 5m
        labels:
          severity: warning
          component: infrastructure
        annotations:
          summary: "Low disk space"
          description: "{{ $labels.instance }}:{{ $labels.mountpoint }} has {{ $value | humanize }}% free"

      # Pod crash looping
      - alert: PodCrashLooping
        expr: |
          rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: critical
          component: kubernetes
        annotations:
          summary: "Pod is crash looping"
          description: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
```

---

## Grafana Dashboards

### Application Dashboard JSON

```json
{
  "dashboard": {
    "title": "Archon Agent Monitoring",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{ method }} {{ status }}"
          }
        ]
      },
      {
        "id": 2,
        "title": "Response Time (95th percentile)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{ path }}"
          }
        ]
      },
      {
        "id": 3,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m])",
            "legendFormat": "Error Rate"
          }
        ]
      },
      {
        "id": 4,
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "process_resident_memory_bytes / 1024 / 1024",
            "legendFormat": "Memory (MB)"
          }
        ]
      },
      {
        "id": 5,
        "title": "Active Database Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "db_pool_connections_active",
            "legendFormat": "Active Connections"
          }
        ]
      }
    ]
  }
}
```

---

## Application Instrumentation

### FastAPI Metrics Example

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Request, Response
import time

# ========================================
# Metrics Definitions
# ========================================
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP requests',
    ['method', 'endpoint']
)

DB_CONNECTION_POOL = Gauge(
    'db_pool_connections_active',
    'Active database connections'
)

DB_CONNECTION_POOL_MAX = Gauge(
    'db_pool_connections_max',
    'Maximum database connections'
)

# ========================================
# Middleware для автоматического сбора метрик
# ========================================
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    """Middleware для сбора метрик по HTTP запросам."""
    method = request.method
    endpoint = request.url.path

    # Увеличить счетчик активных запросов
    ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).inc()

    # Начать отсчет времени
    start_time = time.time()

    try:
        # Выполнить запрос
        response = await call_next(request)
        status = response.status_code
    except Exception as e:
        status = 500
        raise
    finally:
        # Уменьшить счетчик активных запросов
        ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).dec()

        # Записать метрики
        duration = time.time() - start_time
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()
        REQUEST_DURATION.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    return response

# ========================================
# Endpoint для экспорта метрик
# ========================================
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    # Обновить метрики пула соединений
    pool = app.state.db_pool
    DB_CONNECTION_POOL.set(pool.get_active_connections())
    DB_CONNECTION_POOL_MAX.set(pool.max_connections)

    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

# ========================================
# Custom бизнес-метрики
# ========================================
AGENT_TASKS_COMPLETED = Counter(
    'agent_tasks_completed_total',
    'Total completed agent tasks',
    ['agent_type', 'status']
)

AGENT_TASK_DURATION = Histogram(
    'agent_task_duration_seconds',
    'Agent task execution duration',
    ['agent_type']
)

# Использование в коде
@app.post("/tasks")
async def execute_task(task: Task):
    start_time = time.time()
    try:
        result = await agent.execute(task)
        AGENT_TASKS_COMPLETED.labels(
            agent_type=task.agent_type,
            status="success"
        ).inc()
        return result
    except Exception as e:
        AGENT_TASKS_COMPLETED.labels(
            agent_type=task.agent_type,
            status="error"
        ).inc()
        raise
    finally:
        duration = time.time() - start_time
        AGENT_TASK_DURATION.labels(
            agent_type=task.agent_type
        ).observe(duration)
```

---

## Distributed Tracing

### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# ========================================
# Setup OpenTelemetry
# ========================================
def setup_tracing(app: FastAPI):
    """Настройка распределенного трейсинга."""
    # Создать провайдер трейсов
    trace.set_tracer_provider(TracerProvider())

    # Создать Jaeger экспортер
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",
        agent_port=6831,
    )

    # Добавить экспортер
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )

    # Автоматически инструментировать FastAPI
    FastAPIInstrumentor.instrument_app(app)

# ========================================
# Использование в коде
# ========================================
tracer = trace.get_tracer(__name__)

async def process_with_tracing(data: dict):
    """Функция с трейсингом."""
    with tracer.start_as_current_span("process_data") as span:
        # Добавить атрибуты
        span.set_attribute("data.size", len(data))
        span.set_attribute("data.type", type(data).__name__)

        # Вложенный span для подоперации
        with tracer.start_as_current_span("validate_data"):
            validated = validate(data)

        # Еще один вложенный span
        with tracer.start_as_current_span("transform_data"):
            result = transform(validated)

        return result
```

---

## Best Practices для Monitoring

### 1. Golden Signals

**Четыре ключевые метрики:**
```python
# Latency - время отклика
REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency',
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 2, 5]
)

# Traffic - количество запросов
REQUEST_RATE = Counter(
    'requests_total',
    'Total requests'
)

# Errors - ошибки
ERROR_RATE = Counter(
    'errors_total',
    'Total errors',
    ['type']
)

# Saturation - использование ресурсов
RESOURCE_USAGE = Gauge(
    'resource_usage_percent',
    'Resource usage percentage',
    ['resource_type']
)
```

### 2. SLI/SLO Monitoring

**Service Level Indicators:**
```yaml
# SLI: 95% запросов должны выполняться < 500ms
- record: sli:request_latency:ratio
  expr: |
    histogram_quantile(0.95,
      rate(http_request_duration_seconds_bucket[5m])
    ) < 0.5

# SLO: 99.9% uptime
- record: slo:availability:ratio
  expr: |
    sum(rate(up[30d])) / count(up) >= 0.999
```

### 3. Alert Fatigue Prevention

**Правильные пороги:**
```yaml
# ❌ ПЛОХО - слишком чувствительный
- alert: HighCPU
  expr: cpu_usage > 50
  for: 1m

# ✅ ХОРОШО - учитывает паттерны
- alert: HighCPU
  expr: cpu_usage > 80
  for: 10m
```

---

**Навигация:**
- [← Предыдущий модуль: Infrastructure as Code](04_infrastructure_as_code.md)
- [↑ Назад к Deployment Engineer Knowledge Base](../deployment_engineer_knowledge.md)
- [→ Следующий модуль: Security & Best Practices](06_security_best_practices.md)
