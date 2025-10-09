# Production Deployment Guide
# AI Agent Factory - Универсальная фабрика агентов

**Версия:** 1.0.0
**Дата:** 2025-10-09
**Автор:** Archon Implementation Engineer

---

## Оглавление

1. [Введение](#введение)
2. [Требования к окружению](#требования-к-окружению)
3. [Подготовка к развертыванию](#подготовка-к-развертыванию)
4. [Docker развертывание](#docker-развертывание)
5. [Kubernetes развертывание](#kubernetes-развертывание)
6. [Конфигурация баз данных](#конфигурация-баз-данных)
7. [Настройка мониторинга](#настройка-мониторинга)
8. [Безопасность](#безопасность)
9. [Production Checklist](#production-checklist)
10. [Troubleshooting](#troubleshooting)

---

## Введение

Этот гайд описывает пошаговый процесс развертывания AI Agent Factory в production окружение. Система спроектирована для высоконагруженных AI-приложений с поддержкой:

- Множественных LLM провайдеров (OpenAI, Anthropic, Google Gemini, Ollama)
- Микросервисной архитектуры
- Горизонтального масштабирования
- Автоматического восстановления
- Мониторинга в реальном времени

**Целевая архитектура:**
```
┌─────────────────────────────────────────────────┐
│           Load Balancer (NGINX/ALB)             │
└────────────────┬────────────────────────────────┘
                 │
         ┌───────┴───────┐
         │               │
    ┌────▼────┐     ┌────▼────┐
    │ Agent   │     │ Agent   │
    │ Service │     │ Service │
    │ Pod 1   │     │ Pod 2   │
    └────┬────┘     └────┬────┘
         │               │
         └───────┬───────┘
                 │
         ┌───────▼──────────────────────────┐
         │                                   │
    ┌────▼────┐  ┌──────────┐  ┌──────────┐
    │  Redis  │  │PostgreSQL│  │ Vector   │
    │ (Cache) │  │   (DB)   │  │   DB     │
    └─────────┘  └──────────┘  └──────────┘
```

---

## Требования к окружению

### Минимальные требования

#### Серверное оборудование
- **CPU:** 4 cores (8 cores рекомендуется)
- **RAM:** 8 GB (16 GB рекомендуется)
- **Disk:** 100 GB SSD
- **Network:** 100 Mbps

#### Программное обеспечение
- **OS:** Ubuntu 22.04 LTS / Debian 11 / RHEL 8+
- **Docker:** 24.0+ или Docker Desktop
- **Docker Compose:** 2.20+
- **Kubernetes:** 1.28+ (для k8s развертывания)
- **Python:** 3.11+
- **Node.js:** 18+ (для TypeScript агентов)

#### Базы данных
- **PostgreSQL:** 15+ с расширением pgvector
- **Redis:** 7.0+
- **Vector DB:** Pinecone / Weaviate / pgvector (опционально)

### Рекомендуемая конфигурация для production

#### Высоконагруженное окружение
- **CPU:** 16+ cores
- **RAM:** 32+ GB
- **Disk:** 500+ GB NVMe SSD
- **Network:** 1 Gbps+
- **Database:** Managed service (AWS RDS, Google Cloud SQL)
- **Cache:** Managed Redis (AWS ElastiCache, Google Memorystore)

---

## Подготовка к развертыванию

### Шаг 1: Клонирование репозитория

```bash
# Клонировать репозиторий
git clone https://github.com/your-org/agent-factory.git
cd agent-factory/use-cases/agent-factory-with-subagents

# Проверить версию
git describe --tags
```

### Шаг 2: Настройка переменных окружения

```bash
# Скопировать production template
cp .env.production .env

# Отредактировать .env с вашими значениями
nano .env
```

**🚨 КРИТИЧЕСКИ ВАЖНО:** Замените все placeholder значения:

```bash
# Проверить наличие placeholder'ов
grep -E "your_.*_here|password|secret" .env

# Должно быть пусто!
```

#### Обязательные переменные для настройки:

1. **LLM API ключи:**
   ```bash
   OPENAI_API_KEY=sk-proj-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=AI...
   ```

2. **Database credentials:**
   ```bash
   DATABASE_URL=postgresql://prod_user:STRONG_PASSWORD@db.example.com:5432/agent_factory_prod
   REDIS_URL=redis://:STRONG_PASSWORD@redis.example.com:6379/0
   ```

3. **Security secrets:**
   ```bash
   JWT_SECRET_KEY=$(openssl rand -base64 32)
   ```

4. **API URLs:**
   ```bash
   API_BASE_URL=https://api.yourdomain.com
   API_CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
   ```

### Шаг 3: Создание SSL сертификатов

```bash
# Для Let's Encrypt (рекомендуется)
sudo apt install certbot
sudo certbot certonly --standalone -d api.yourdomain.com

# Сертификаты будут в:
# /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/api.yourdomain.com/privkey.pem

# Обновить .env
SSL_CERT_PATH=/etc/letsencrypt/live/api.yourdomain.com/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/api.yourdomain.com/privkey.pem
```

### Шаг 4: Настройка PostgreSQL

```bash
# Установить PostgreSQL 15+
sudo apt install postgresql-15 postgresql-contrib-15

# Создать production базу
sudo -u postgres psql << EOF
CREATE DATABASE agent_factory_prod;
CREATE USER prod_user WITH ENCRYPTED PASSWORD 'STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE agent_factory_prod TO prod_user;
\c agent_factory_prod
CREATE EXTENSION IF NOT EXISTS pgvector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- Для полнотекстового поиска
EOF
```

**Оптимизация PostgreSQL для production:**

```bash
# Редактировать postgresql.conf
sudo nano /etc/postgresql/15/main/postgresql.conf
```

Добавить:
```conf
# Производительность
shared_buffers = 4GB                    # 25% от RAM
effective_cache_size = 12GB             # 75% от RAM
work_mem = 16MB
maintenance_work_mem = 512MB
max_connections = 100

# WAL настройки
wal_buffers = 16MB
checkpoint_completion_target = 0.9
max_wal_size = 4GB
min_wal_size = 1GB

# Планировщик
random_page_cost = 1.1                  # Для SSD
effective_io_concurrency = 200

# Логирование
log_min_duration_statement = 1000       # Логировать медленные запросы (>1s)
log_line_prefix = '%t [%p]: user=%u,db=%d,app=%a,client=%h '
```

Перезапустить:
```bash
sudo systemctl restart postgresql
```

### Шаг 5: Настройка Redis

```bash
# Установить Redis 7+
sudo apt install redis-server

# Настроить redis.conf
sudo nano /etc/redis/redis.conf
```

Добавить:
```conf
# Безопасность
bind 127.0.0.1 ::1
requirepass STRONG_REDIS_PASSWORD
protected-mode yes

# Производительность
maxmemory 2gb
maxmemory-policy allkeys-lru

# Персистентность
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec

# Сеть
timeout 300
tcp-keepalive 60
```

Перезапустить:
```bash
sudo systemctl restart redis-server
```

### Шаг 6: Установка зависимостей

```bash
# Python зависимости
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# TypeScript агенты (если используются)
npm install --production
```

### Шаг 7: Миграции базы данных

```bash
# Применить миграции
alembic upgrade head

# Проверить статус
alembic current
```

---

## Docker развертывание

### Базовое Docker развертывание

#### Создание Dockerfile (если нет)

```dockerfile
# Использовать официальный Python образ
FROM python:3.11-slim

# Установить системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создать рабочую директорию
WORKDIR /app

# Копировать requirements
COPY requirements.txt .

# Установить Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копировать код приложения
COPY . .

# Создать non-root пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Запуск
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### Создание docker-compose.yml

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: agent_factory_prod
      POSTGRES_USER: prod_user
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U prod_user"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Agent Factory Application
  agent-factory:
    build:
      context: .
      dockerfile: Dockerfile
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./agents:/app/agents:ro
      - agent_logs:/var/log/agent-factory
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  # NGINX Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - agent-factory
    restart: unless-stopped

  # Prometheus Monitoring (опционально)
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    restart: unless-stopped

  # Grafana Dashboards (опционально)
  grafana:
    image: grafana/grafana:latest
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  agent_logs:
    driver: local
  prometheus_data:
    driver: local
  grafana_data:
    driver: local

networks:
  default:
    name: agent-factory-network
```

#### Создание nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream agent_factory {
        server agent-factory:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=60r/m;

    # HTTP to HTTPS redirect
    server {
        listen 80;
        server_name api.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name api.yourdomain.com;

        # SSL Configuration
        ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Logging
        access_log /var/log/nginx/agent_factory_access.log;
        error_log /var/log/nginx/agent_factory_error.log;

        # Proxy settings
        location / {
            limit_req zone=api_limit burst=100 nodelay;

            proxy_pass http://agent_factory;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 300s;

            # WebSocket support (если нужен)
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # Health check endpoint (без rate limiting)
        location /health {
            proxy_pass http://agent_factory/health;
            access_log off;
        }
    }
}
```

#### Запуск с Docker Compose

```bash
# Билд образов
docker-compose build

# Запуск в фоне
docker-compose up -d

# Проверить статус
docker-compose ps

# Логи
docker-compose logs -f agent-factory

# Остановка
docker-compose down
```

#### Обновление в production

```bash
# Пулл новых изменений
git pull origin main

# Билд новых образов
docker-compose build

# Обновление с zero-downtime (rolling update)
docker-compose up -d --no-deps --build agent-factory

# Проверить health
curl https://api.yourdomain.com/health
```

---

## Kubernetes развертывание

### Подготовка Kubernetes кластера

```bash
# Установить kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Проверить кластер
kubectl cluster-info
kubectl get nodes
```

### Создание Namespace

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: agent-factory
```

```bash
kubectl apply -f namespace.yaml
```

### Создание Secrets

```bash
# Создать secrets из .env файла
kubectl create secret generic agent-factory-secrets \
  --from-env-file=.env \
  --namespace=agent-factory

# Проверить
kubectl get secrets -n agent-factory
```

### ConfigMap для конфигурации

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agent-factory-config
  namespace: agent-factory
data:
  LOG_LEVEL: "INFO"
  WORKER_COUNT: "4"
  ENABLE_METRICS: "true"
```

```bash
kubectl apply -f configmap.yaml
```

### PersistentVolumeClaim для данных

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: agent-factory
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: fast-ssd

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
  namespace: agent-factory
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
  storageClassName: fast-ssd
```

```bash
kubectl apply -f pvc.yaml
```

### PostgreSQL Deployment

```yaml
# postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: agent-factory
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: pgvector/pgvector:pg15
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: agent_factory_prod
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: agent-factory-secrets
              key: DATABASE_USER
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: agent-factory-secrets
              key: DATABASE_PASSWORD
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: agent-factory
spec:
  selector:
    app: postgres
  ports:
  - protocol: TCP
    port: 5432
    targetPort: 5432
  type: ClusterIP
```

```bash
kubectl apply -f postgres-deployment.yaml
```

### Redis Deployment

```yaml
# redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: agent-factory
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        command: ["redis-server"]
        args: ["--requirepass", "$(REDIS_PASSWORD)"]
        ports:
        - containerPort: 6379
        env:
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: agent-factory-secrets
              key: REDIS_PASSWORD
        volumeMounts:
        - name: redis-storage
          mountPath: /data
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1"
      volumes:
      - name: redis-storage
        persistentVolumeClaim:
          claimName: redis-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: agent-factory
spec:
  selector:
    app: redis
  ports:
  - protocol: TCP
    port: 6379
    targetPort: 6379
  type: ClusterIP
```

```bash
kubectl apply -f redis-deployment.yaml
```

### Agent Factory Deployment

```yaml
# agent-factory-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-factory
  namespace: agent-factory
  labels:
    app: agent-factory
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: agent-factory
  template:
    metadata:
      labels:
        app: agent-factory
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: agent-factory
        image: your-registry/agent-factory:latest
        ports:
        - containerPort: 8000
          name: http
        - containerPort: 9090
          name: metrics
        envFrom:
        - secretRef:
            name: agent-factory-secrets
        - configMapRef:
            name: agent-factory-config
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1"
        volumeMounts:
        - name: agent-logs
          mountPath: /var/log/agent-factory
      volumes:
      - name: agent-logs
        emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
  name: agent-factory-service
  namespace: agent-factory
spec:
  selector:
    app: agent-factory
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: 8000
  - name: metrics
    protocol: TCP
    port: 9090
    targetPort: 9090
  type: LoadBalancer
```

```bash
kubectl apply -f agent-factory-deployment.yaml
```

### HorizontalPodAutoscaler

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: agent-factory-hpa
  namespace: agent-factory
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-factory
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
```

```bash
kubectl apply -f hpa.yaml
```

### Проверка развертывания

```bash
# Проверить pods
kubectl get pods -n agent-factory

# Логи
kubectl logs -f deployment/agent-factory -n agent-factory

# Проброс порта для тестирования
kubectl port-forward svc/agent-factory-service 8000:80 -n agent-factory

# Тест health endpoint
curl http://localhost:8000/health
```

---

## Конфигурация баз данных

### PostgreSQL Production Configuration

#### Индексы для производительности

```sql
-- Подключиться к production БД
psql -h your-db-host -U prod_user -d agent_factory_prod

-- Создать оптимизированные индексы
CREATE INDEX CONCURRENTLY idx_tasks_status_created
ON tasks (status, created_at DESC);

CREATE INDEX CONCURRENTLY idx_tasks_project_assignee
ON tasks (project_id, assignee)
WHERE archived = false;

CREATE INDEX CONCURRENTLY idx_documents_project_type
ON documents (project_id, document_type);

-- GIN индекс для полнотекстового поиска
CREATE INDEX CONCURRENTLY idx_documents_fulltext
ON documents USING gin(to_tsvector('english', title || ' ' || content));

-- Covering index для частых запросов
CREATE INDEX CONCURRENTLY idx_tasks_covering
ON tasks (id) INCLUDE (title, status, assignee, task_order)
WHERE archived = false;
```

#### Партиционирование для больших таблиц

```sql
-- Партиционирование логов по месяцам
CREATE TABLE audit_logs (
    id UUID DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL,
    user_id UUID,
    action TEXT,
    details JSONB
) PARTITION BY RANGE (created_at);

-- Создать партиции
CREATE TABLE audit_logs_2025_10 PARTITION OF audit_logs
FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

CREATE TABLE audit_logs_2025_11 PARTITION OF audit_logs
FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
```

#### Регулярное обслуживание

```bash
# Создать cronjob для vacuum
crontab -e
```

Добавить:
```cron
# Vacuum analyze каждую ночь в 2AM
0 2 * * * /usr/bin/vacuumdb -U prod_user -d agent_factory_prod --analyze --verbose

# Reindex каждое воскресенье в 3AM
0 3 * * 0 /usr/bin/reindexdb -U prod_user -d agent_factory_prod --verbose
```

### Redis Production Configuration

#### Настройка репликации (Master-Replica)

**Master Redis (redis-master.conf):**
```conf
bind 0.0.0.0
port 6379
requirepass MASTER_PASSWORD
masterauth MASTER_PASSWORD

# Персистентность
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec

# Репликация
min-replicas-to-write 1
min-replicas-max-lag 10

# Память
maxmemory 4gb
maxmemory-policy allkeys-lru
```

**Replica Redis (redis-replica.conf):**
```conf
bind 0.0.0.0
port 6379
requirepass REPLICA_PASSWORD
masterauth MASTER_PASSWORD

replicaof redis-master 6379
replica-read-only yes
```

#### Sentinel для автоматического failover

```conf
# sentinel.conf
port 26379
sentinel monitor mymaster redis-master 6379 2
sentinel auth-pass mymaster MASTER_PASSWORD
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 10000
```

---

## Настройка мониторинга

### Prometheus configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'agent-factory'
    static_configs:
      - targets: ['agent-factory:9090']
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - '/etc/prometheus/alerts.yml'
```

### Alerting rules

```yaml
# alerts.yml
groups:
  - name: agent_factory_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }}% over the last 5 minutes"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.9
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is above 90%"

      - alert: DatabaseConnectionPoolExhausted
        expr: pg_stat_database_numbackends / pg_settings_max_connections > 0.8
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool almost exhausted"
          description: "{{ $value }}% of connections are in use"

      - alert: LLMAPIHighLatency
        expr: histogram_quantile(0.95, llm_request_duration_seconds_bucket) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "LLM API high latency"
          description: "95th percentile latency is {{ $value }}s"

      - alert: HighCostAlert
        expr: llm_daily_cost_dollars > 80
        labels:
          severity: warning
        annotations:
          summary: "LLM daily cost approaching budget"
          description: "Current cost is ${{ $value }}, budget is $100"
```

### Grafana Dashboards

**Создать dashboard через API:**

```bash
# Import предустановленного dashboard
curl -X POST \
  http://grafana:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${GRAFANA_API_KEY}" \
  -d @grafana-dashboard.json
```

**Ключевые метрики для мониторинга:**

1. **Application metrics:**
   - Requests per second (RPS)
   - Response time (p50, p95, p99)
   - Error rate
   - Active connections

2. **LLM metrics:**
   - API latency
   - Token usage
   - Cost tracking
   - Model selection distribution

3. **Database metrics:**
   - Query latency
   - Connection pool usage
   - Cache hit rate
   - Slow queries count

4. **Infrastructure metrics:**
   - CPU usage
   - Memory usage
   - Disk I/O
   - Network throughput

---

## Безопасность

### 1. Network Security

#### Настройка Firewall (UFW)

```bash
# Включить UFW
sudo ufw enable

# Разрешить SSH
sudo ufw allow 22/tcp

# Разрешить HTTPS
sudo ufw allow 443/tcp

# Разрешить HTTP (для редиректа на HTTPS)
sudo ufw allow 80/tcp

# Запретить прямой доступ к базам данных (только internal)
sudo ufw deny 5432/tcp
sudo ufw deny 6379/tcp

# Проверить статус
sudo ufw status verbose
```

#### Security Groups (AWS/GCP)

**Входящие правила:**
- Port 443 (HTTPS): 0.0.0.0/0
- Port 80 (HTTP): 0.0.0.0/0
- Port 22 (SSH): YOUR_IP/32 (только ваш IP!)

**Исходящие правила:**
- All traffic: 0.0.0.0/0

### 2. API Security

#### Rate Limiting

```python
# В коде приложения (FastAPI example)
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/agents")
@limiter.limit("60/minute")
async def list_agents(request: Request):
    # Ваш код
    pass
```

#### JWT Authentication

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 3. Secrets Management

#### Использование AWS Secrets Manager

```python
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        raise e

# Использование
DATABASE_URL = get_secret('agent-factory/database-url')
LLM_API_KEY = get_secret('agent-factory/llm-api-key')
```

#### Rotation политика

```bash
# Создать Lambda для автоматической ротации
aws secretsmanager rotate-secret \
    --secret-id agent-factory/api-keys \
    --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789:function:rotate-api-keys \
    --rotation-rules AutomaticallyAfterDays=90
```

### 4. Data Encryption

#### Шифрование данных в PostgreSQL

```sql
-- Включить прозрачное шифрование (TDE) в managed databases
-- Для AWS RDS автоматически при создании с флагом --storage-encrypted

-- Шифрование чувствительных полей
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Пример таблицы с шифрованием
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    encrypted_api_key BYTEA,  -- Шифрованный API ключ
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Вставка с шифрованием
INSERT INTO users (email, encrypted_api_key)
VALUES (
    'user@example.com',
    pgp_sym_encrypt('secret_api_key', 'encryption_passphrase')
);

-- Чтение с дешифрованием
SELECT
    email,
    pgp_sym_decrypt(encrypted_api_key, 'encryption_passphrase') AS api_key
FROM users;
```

---

## Production Checklist

### Pre-Deployment Checklist

- [ ] **Environment Configuration**
  - [ ] Все переменные в `.env` заполнены
  - [ ] Нет placeholder значений (`your_*_here`)
  - [ ] SSL сертификаты настроены
  - [ ] Database credentials secure

- [ ] **Database Setup**
  - [ ] PostgreSQL 15+ установлен
  - [ ] pgvector расширение включено
  - [ ] Миграции применены (`alembic upgrade head`)
  - [ ] Индексы созданы
  - [ ] Backup настроен

- [ ] **Redis Setup**
  - [ ] Redis 7+ установлен
  - [ ] Password установлен
  - [ ] Персистентность настроена (AOF/RDB)

- [ ] **Security**
  - [ ] Firewall настроен
  - [ ] SSH ключи настроены (disable password auth)
  - [ ] SSL/TLS сертификаты валидны
  - [ ] Secrets в безопасном хранилище (не в .env!)
  - [ ] Rate limiting включен
  - [ ] CORS настроен правильно

- [ ] **Monitoring & Logging**
  - [ ] Prometheus установлен
  - [ ] Grafana dashboards настроены
  - [ ] Alerting rules сконфигурированы
  - [ ] Sentry DSN настроен
  - [ ] Log rotation настроен

- [ ] **Performance**
  - [ ] Database connection pool оптимизирован
  - [ ] Redis cache настроен
  - [ ] CDN настроен (для статики)
  - [ ] Load balancer настроен

- [ ] **Backup & Recovery**
  - [ ] Автоматические backups включены
  - [ ] Restore процедура протестирована
  - [ ] Disaster recovery план создан

### Post-Deployment Checklist

- [ ] **Health Checks**
  - [ ] `/health` endpoint отвечает 200 OK
  - [ ] Database connectivity проверена
  - [ ] Redis connectivity проверена
  - [ ] LLM API connectivity проверена

- [ ] **Smoke Tests**
  - [ ] Создать тестовый проект через API
  - [ ] Создать тестовую задачу
  - [ ] Выполнить тестовый LLM запрос
  - [ ] Проверить метрики в Prometheus

- [ ] **Performance Tests**
  - [ ] Load testing выполнен
  - [ ] Response times acceptable (<500ms p95)
  - [ ] Error rate <0.1%

- [ ] **Documentation**
  - [ ] API документация обновлена
  - [ ] Runbooks созданы для common issues
  - [ ] On-call procedures документированы

---

## Troubleshooting

### Общие проблемы

#### Проблема: Application не запускается

**Симптомы:**
```
Error: Failed to connect to database
```

**Диагностика:**
```bash
# Проверить database connectivity
psql -h your-db-host -U prod_user -d agent_factory_prod

# Проверить логи
docker-compose logs agent-factory

# Проверить переменные окружения
docker-compose exec agent-factory env | grep DATABASE
```

**Решение:**
1. Проверить `DATABASE_URL` в `.env`
2. Проверить firewall rules
3. Проверить database credentials
4. Проверить что database запущен: `docker-compose ps`

---

#### Проблема: High memory usage

**Симптомы:**
```
Application OOM killed
Memory usage >90%
```

**Диагностика:**
```bash
# Проверить memory usage
docker stats

# Kubernetes
kubectl top pods -n agent-factory
```

**Решение:**
1. Увеличить memory limits в docker-compose.yml или k8s deployment
2. Оптимизировать database connection pool:
   ```python
   DATABASE_POOL_SIZE=10  # Уменьшить
   ```
3. Включить Redis eviction:
   ```conf
   maxmemory 2gb
   maxmemory-policy allkeys-lru
   ```

---

#### Проблема: Slow API responses

**Симптомы:**
```
Response time >5s
Timeout errors
```

**Диагностика:**
```bash
# Проверить slow queries в PostgreSQL
psql -U prod_user -d agent_factory_prod << EOF
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
EOF

# Проверить Redis cache hit rate
redis-cli INFO stats | grep keyspace
```

**Решение:**
1. Добавить индексы для медленных запросов
2. Включить Redis caching:
   ```python
   ENABLE_QUERY_CACHE=true
   CACHE_TTL_MEDIUM=1800
   ```
3. Увеличить worker count:
   ```
   WORKER_COUNT=8
   ```

---

#### Проблема: LLM API rate limits

**Симптомы:**
```
Error: Rate limit exceeded (429)
```

**Решение:**
1. Включить retry с exponential backoff
2. Использовать fallback model:
   ```python
   # Если Anthropic rate limited, fallback на OpenAI
   if anthropic_rate_limited:
       use_openai_model()
   ```
3. Включить request queueing

---

### Kubernetes специфичные проблемы

#### Проблема: Pods в CrashLoopBackOff

**Диагностика:**
```bash
# Проверить статус
kubectl get pods -n agent-factory

# Логи
kubectl logs -f <pod-name> -n agent-factory

# Describe для деталей
kubectl describe pod <pod-name> -n agent-factory
```

**Решение:**
1. Проверить liveness/readiness probes
2. Увеличить `initialDelaySeconds` если приложение долго стартует
3. Проверить resource limits

---

#### Проблема: LoadBalancer не получает external IP

**Диагностика:**
```bash
kubectl get svc -n agent-factory
```

**Решение:**
1. Для облачных провайдеров - проверить квоты
2. Для on-premise - установить MetalLB:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.0/config/manifests/metallb-native.yaml
   ```

---

### Мониторинг и алерты

#### Настройка Slack уведомлений

```yaml
# alertmanager.yml
receivers:
  - name: 'slack'
    slack_configs:
      - api_url: 'YOUR_SLACK_WEBHOOK_URL'
        channel: '#agent-factory-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

route:
  receiver: 'slack'
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10m
  repeat_interval: 12h
```

---

## Заключение

Следуя этому гайду, вы развернете production-ready AI Agent Factory со всеми необходимыми компонентами:

✅ Масштабируемая архитектура
✅ Высокая доступность (HA)
✅ Автоматический мониторинг
✅ Безопасность enterprise-уровня
✅ Disaster recovery готовность

**Следующие шаги:**
1. Прочитать API документацию
2. Настроить CI/CD pipeline
3. Провести load testing
4. Создать runbooks для on-call

**Поддержка:**
- GitHub Issues: https://github.com/your-org/agent-factory/issues
- Slack: #agent-factory-support
- Email: support@yourdomain.com

---

**Версия гайда:** 1.0.0
**Последнее обновление:** 2025-10-09
**Автор:** Archon Implementation Engineer
**Лицензия:** MIT
