# Module 01: Docker & Containerization

**Назад к:** [Deployment Engineer Knowledge Base](../deployment_engineer_knowledge.md)

---

## 🎯 ТРИГГЕРНАЯ СИСТЕМА - Когда читать этот модуль

### Тип 1: Ключевые слова (Keywords Triggers)
**Читай этот модуль ЕСЛИ задача содержит:**
- `docker`, `dockerfile`, `docker-compose`
- `container`, `containerization`, `image`
- `build`, `multi-stage build`, `buildkit`
- `dockerignore`, `docker build`
- `alpine`, `slim`, `base image`

### Тип 2: Сценарии использования (Scenario Triggers)
**Читай этот модуль КОГДА нужно:**
- Создать Dockerfile для нового приложения
- Оптимизировать существующий Docker образ
- Настроить Docker Compose для локальной разработки
- Уменьшить размер Docker образа
- Добавить security scanning в Docker workflow
- Настроить multi-stage build
- Создать health check для контейнера

### Тип 3: Технические термины (Technical Terms Triggers)
**Читай этот модуль ЕСЛИ встречаешь:**
- Multi-stage builds
- Layer caching
- BuildKit
- Security context (Docker)
- Health checks
- Non-root user
- Image optimization
- Docker registry
- Container orchestration basics

---

## 📋 СОДЕРЖАНИЕ МОДУЛЯ

**Основные темы:**
1. ✅ Оптимизированный Multi-Stage Build (production-ready Dockerfile)
2. ✅ Docker Compose для локальной разработки (complete stack с monitoring)
3. ✅ Best Practices для Docker (optimization, security, caching)
4. ✅ Docker Build Strategies (multi-architecture, caching)

**Конфигурации:**
- Production Dockerfile (3 stages: base → builder → production)
- Docker Compose с PostgreSQL, Redis, Prometheus, Grafana
- .dockerignore для оптимизации
- Health check примеры

**Команды и скрипты:**
- BuildKit для параллельной сборки
- Multi-architecture builds
- Security scanning (Trivy, Snyk)
- Cache optimization

---

## Оптимизированный Multi-Stage Build

### Production-Ready Dockerfile

```dockerfile
# ========================================
# Stage 1: Base image с системными зависимостями
# ========================================
FROM python:3.11-slim AS base

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ========================================
# Stage 2: Builder - установка Python зависимостей
# ========================================
FROM base AS builder

# Установка Poetry для управления зависимостями
RUN pip install --no-cache-dir poetry

# Копирование файлов зависимостей
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Установка зависимостей (без dev-пакетов)
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi --no-root

# Копирование исходного кода
COPY . .

# Установка приложения
RUN poetry install --no-dev --no-interaction --no-ansi

# ========================================
# Stage 3: Production runtime
# ========================================
FROM python:3.11-slim AS production

# Создание непривилегированного пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Установка только runtime зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование установленных пакетов из builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Создание рабочей директории
WORKDIR /app

# Копирование только необходимых файлов приложения
COPY --from=builder --chown=appuser:appuser /app /app

# Переключение на непривилегированного пользователя
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Expose порт
EXPOSE 8000

# Запуск приложения
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Ключевые преимущества:**
- ✅ Multi-stage build минимизирует размер финального образа
- ✅ Непривилегированный пользователь для безопасности
- ✅ Health check для мониторинга
- ✅ Кэширование слоев для быстрой сборки

---

## Docker Compose для локальной разработки

### Complete Stack with Monitoring

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
      - LLM_API_KEY=${LLM_API_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
    networks:
      - app-network
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - app-network

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
    depends_on:
      - prometheus
    networks:
      - app-network

volumes:
  postgres-data:
  redis-data:
  prometheus-data:
  grafana-data:

networks:
  app-network:
    driver: bridge
```

**Ключевые компоненты:**
- ✅ Приложение с health checks
- ✅ PostgreSQL с persistent storage
- ✅ Redis для кэширования
- ✅ Prometheus для метрик
- ✅ Grafana для визуализации

---

## Best Practices для Docker

### 1. Container Optimization

**Минимизация размера образа:**
```dockerfile
# ❌ ПЛОХО - большой образ
FROM python:3.11

# ✅ ХОРОШО - slim образ
FROM python:3.11-slim
```

**Использование .dockerignore:**
```
# .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.log
.git
.pytest_cache
.mypy_cache
venv/
*.egg-info
```

### 2. Security Best Practices

**Непривилегированные пользователи:**
```dockerfile
# Создание пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Переключение
USER appuser
```

**Security scanning:**
```bash
# Trivy scanning
trivy image archon-agent:latest

# Snyk scanning
snyk container test archon-agent:latest
```

### 3. Build Optimization

**Эффективное кэширование:**
```dockerfile
# ✅ ПРАВИЛЬНЫЙ порядок - зависимости сначала
COPY pyproject.toml poetry.lock ./
RUN poetry install

# Код копируем после - чаще меняется
COPY . .
```

**BuildKit для параллельной сборки:**
```bash
# Включение BuildKit
export DOCKER_BUILDKIT=1
docker build -t archon-agent:latest .
```

### 4. Health Checks

**Правильный health check:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1
```

**Health endpoint в приложении:**
```python
@app.get("/health")
async def health_check():
    """Health check endpoint для Docker и K8s."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": VERSION
    }
```

### 5. Resource Limits

**Docker Compose limits:**
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

---

## Docker Build Strategies

### Multi-Architecture Builds

```bash
# Создание buildx builder
docker buildx create --name multiarch --use

# Build для multiple architectures
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t archon-agent:latest \
  --push .
```

### Caching Strategies

```bash
# Использование cache mount
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# External cache
docker build \
  --cache-from=type=registry,ref=archon-agent:cache \
  --cache-to=type=registry,ref=archon-agent:cache,mode=max \
  -t archon-agent:latest .
```

---

**Навигация:**
- [← Назад к Deployment Engineer Knowledge Base](../deployment_engineer_knowledge.md)
- [→ Следующий модуль: Kubernetes Orchestration](02_kubernetes_orchestration.md)
