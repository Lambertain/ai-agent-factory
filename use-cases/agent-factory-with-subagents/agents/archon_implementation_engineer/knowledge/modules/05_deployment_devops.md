# Module 05: Deployment & DevOps

**Версия:** 1.0
**Дата:** 2025-10-17
**Автор:** Archon Implementation Engineer

**Назад к:** [Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- Multi-stage Docker builds для минимизации размера образа (builder + runtime)
- Kubernetes Deployment с Rolling Update стратегией (zero downtime)
- Horizontal Pod Autoscaler (HPA) настройка для автомасштабирования
- GitHub Actions CI/CD workflow: linting → testing → build → deploy
- Health/Readiness/Liveness/Startup probes для production readiness
- Zero downtime deployment с maxSurge/maxUnavailable
- Resource limits и requests для cost optimization
- Security hardening: non-root user, RBAC, secrets management

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** deployment, docker, kubernetes, ci/cd, github actions, автомасштабирование, devops, контейнеризация, rolling update, helm, terraform, production, infrastructure

**English:** deployment, docker, kubernetes, ci/cd, github actions, autoscaling, devops, containerization, rolling update, helm, terraform, production, infrastructure

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Production deployment подготовка
- Настройка CI/CD pipeline с автоматическими тестами
- Автомасштабирование и zero downtime deployments
- Контейнеризация AI агентов для production
- Security hardening и compliance требования
- Cost optimization через resource management
- Multi-environment setup (development/staging/production)
- Infrastructure as Code необходим (IaC)

---

## Docker Containerization

### Multi-stage Docker Build для оптимизации размера

```dockerfile
# Multi-stage build для минимизации размера финального образа
FROM python:3.11-slim as builder

# Метаданные образа
LABEL maintainer="Archon Team <team@archon.ai>"
LABEL description="AI Agent Production Build"

# Установка зависимостей сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry для управления зависимостями
RUN pip install --no-cache-dir poetry==1.7.1

# Копирование файлов зависимостей
WORKDIR /build
COPY pyproject.toml poetry.lock ./

# Установка зависимостей (без dev зависимостей)
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi --no-root

# Копирование исходного кода
COPY . .

# Установка самого пакета
RUN poetry install --no-dev --no-interaction --no-ansi

# ═══════════════════════════════════════════════════════
# Production stage - минимальный финальный образ
# ═══════════════════════════════════════════════════════
FROM python:3.11-slim

# Установка runtime зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя для безопасности (non-root)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Копирование установленных пакетов из builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Создание рабочей директории
WORKDIR /app

# Копирование кода приложения с правильными permissions
COPY --chown=appuser:appuser . .

# Создание директорий для логов и данных
RUN mkdir -p /app/logs /app/data \
    && chown -R appuser:appuser /app/logs /app/data

# Переключение на non-root пользователя
USER appuser

# Expose порты
EXPOSE 8000

# Health check для контейнера
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Команда запуска приложения
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Docker Compose для локальной разработки

```yaml
version: '3.8'

services:
  # AI Agent сервис
  agent:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: archon-agent
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/archon
      - REDIS_URL=redis://redis:6379/0
      - LLM_API_KEY=${LLM_API_KEY}
      - ENVIRONMENT=development
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    networks:
      - archon-network

  # PostgreSQL база данных
  postgres:
    image: postgres:15-alpine
    container_name: archon-postgres
    environment:
      - POSTGRES_DB=archon
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_INITDB_ARGS=-E UTF8 --locale=en_US.UTF-8
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - archon-network

  # Redis для кэширования
  redis:
    image: redis:7-alpine
    container_name: archon-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - archon-network

  # Nginx для reverse proxy
  nginx:
    image: nginx:alpine
    container_name: archon-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - agent
    networks:
      - archon-network

volumes:
  postgres_data:
  redis_data:

networks:
  archon-network:
    driver: bridge
```

---

## Kubernetes Deployment

### Production-ready Kubernetes Manifests

```yaml
# ═══════════════════════════════════════════════════════
# Deployment Configuration
# ═══════════════════════════════════════════════════════
apiVersion: apps/v1
kind: Deployment
metadata:
  name: archon-agent
  namespace: production
  labels:
    app: archon-agent
    version: v1.0.0
    tier: backend
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero downtime deployment
  selector:
    matchLabels:
      app: archon-agent
  template:
    metadata:
      labels:
        app: archon-agent
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      # Anti-affinity для распределения по узлам
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - archon-agent
              topologyKey: kubernetes.io/hostname

      # Init container для миграций БД
      initContainers:
      - name: db-migration
        image: archon-agent:latest
        command: ['python', 'manage.py', 'migrate']
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: archon-secrets
              key: database-url

      containers:
      - name: archon-agent
        image: archon-agent:latest
        imagePullPolicy: Always
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP

        # Resource limits и requests
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"

        # Environment variables из ConfigMap и Secrets
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: archon-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: archon-secrets
              key: redis-url
        - name: LLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: archon-secrets
              key: llm-api-key

        # Liveness probe - проверка что контейнер живой
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        # Readiness probe - готовность принимать трафик
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2

        # Startup probe для медленного старта
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 0
          periodSeconds: 10
          failureThreshold: 30  # 5 minutes to start

        # Volume mounts
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
        - name: logs
          mountPath: /app/logs

      # Volumes
      volumes:
      - name: config
        configMap:
          name: archon-config
      - name: logs
        emptyDir: {}

      # Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

---
# ═══════════════════════════════════════════════════════
# Service Configuration
# ═══════════════════════════════════════════════════════
apiVersion: v1
kind: Service
metadata:
  name: archon-agent-service
  namespace: production
  labels:
    app: archon-agent
spec:
  type: LoadBalancer
  selector:
    app: archon-agent
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: 8000
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3 hours

---
# ═══════════════════════════════════════════════════════
# Horizontal Pod Autoscaler
# ═══════════════════════════════════════════════════════
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: archon-agent-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: archon-agent
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # 5 minutes
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 2
        periodSeconds: 15
      selectPolicy: Max

---
# ═══════════════════════════════════════════════════════
# ConfigMap для конфигурации
# ═══════════════════════════════════════════════════════
apiVersion: v1
kind: ConfigMap
metadata:
  name: archon-config
  namespace: production
data:
  config.yaml: |
    log_level: INFO
    max_workers: 4
    timeout: 30
    retry_attempts: 3
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ═══════════════════════════════════════════════════════
  # Testing Job
  # ═══════════════════════════════════════════════════════
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Install dependencies
      run: |
        poetry install --with dev

    - name: Run linting
      run: |
        poetry run black --check .
        poetry run isort --check .
        poetry run pylint src/

    - name: Run type checking
      run: |
        poetry run mypy src/

    - name: Run unit tests
      run: |
        poetry run pytest tests/unit -v --cov=src --cov-report=xml

    - name: Run integration tests
      run: |
        poetry run pytest tests/integration -v
      env:
        TEST_DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
        fail_ci_if_error: true

  # ═══════════════════════════════════════════════════════
  # Build and Push Docker Image
  # ═══════════════════════════════════════════════════════
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'

    steps:
    - uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.DOCKER_REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=registry,ref=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache
        cache-to: type=registry,ref=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache,mode=max

  # ═══════════════════════════════════════════════════════
  # Deploy to Production
  # ═══════════════════════════════════════════════════════
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://agent.archon.ai

    steps:
    - uses: actions/checkout@v3

    - name: Configure kubectl
      uses: azure/setup-kubectl@v3

    - name: Set up kubeconfig
      run: |
        mkdir -p ~/.kube
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > ~/.kube/config

    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/archon-agent \
          archon-agent=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:main-${{ github.sha }} \
          -n production

    - name: Wait for rollout
      run: |
        kubectl rollout status deployment/archon-agent -n production --timeout=5m

    - name: Run smoke tests
      run: |
        kubectl run smoke-test --image=curlimages/curl --rm -i --restart=Never \
          -- curl -f http://archon-agent-service/health || exit 1

    - name: Notify deployment
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: 'Deployment to production completed'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
      if: always()
```

---

## Best Practices для Deployment

### 1. Security Best Practices

**Docker Security:**
- ✅ Всегда используй non-root пользователя
- ✅ Multi-stage builds для минимизации attack surface
- ✅ Сканируй образы на уязвимости (Trivy, Snyk)
- ✅ Не храни секреты в образах

**Kubernetes Security:**
- ✅ Network Policies для изоляции подов
- ✅ Pod Security Policies/Standards
- ✅ RBAC для контроля доступа
- ✅ Secrets management через External Secrets Operator

### 2. Zero Downtime Deployment

```yaml
# Rolling Update Strategy
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # Один дополнительный под
    maxUnavailable: 0  # Ноль недоступных подов
```

**Ключевые элементы:**
- Readiness probes - не принимать трафик до готовности
- PreStop hooks - graceful shutdown
- PodDisruptionBudget - минимум доступных подов

### 3. Monitoring и Observability

**Что мониторить:**
- Health endpoints: `/health`, `/ready`, `/live`
- Metrics: CPU, memory, request rate, latency
- Logs: structured JSON logs
- Traces: distributed tracing (Jaeger, Tempo)

### 4. Cost Optimization

**Resource Management:**
```yaml
resources:
  requests:    # Гарантированные ресурсы
    memory: "512Mi"
    cpu: "250m"
  limits:      # Максимальные ресурсы
    memory: "1Gi"
    cpu: "500m"
```

**HPA для auto-scaling:**
- Scale по CPU/Memory метрикам
- Custom metrics (request rate, queue length)
- Predictive autoscaling для известных паттернов

---

**Навигация:**
- [← Предыдущий модуль: Testing & Quality Assurance](04_testing_quality_assurance.md)
- [↑ Назад к Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)
- [→ Следующий модуль: Monitoring & Observability](06_monitoring_observability.md)
