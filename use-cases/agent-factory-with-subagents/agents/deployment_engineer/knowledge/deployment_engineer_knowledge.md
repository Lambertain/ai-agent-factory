# ⚠️ КРИТИЧЕСКИ ВАЖНО: ОБЯЗАТЕЛЬНОЕ ПЕРЕКЛЮЧЕНИЕ В РОЛЬ

**🚨 ПЕРЕД НАЧАЛОМ ЛЮБОЙ РАБОТЫ ТЫ ДОЛЖЕН:**

## 📢 ШАГ 1: ОБЪЯВИТЬ ПЕРЕКЛЮЧЕНИЕ ПОЛЬЗОВАТЕЛЮ

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎭 ПЕРЕКЛЮЧАЮСЬ В РОЛЬ ВЕДУЩИЙ ИНЖЕНЕР ПО РАЗВЕРТЫВАНИЮ КОМАНДЫ ARCHON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Моя экспертиза:
• Docker и контейнеризация приложений
• Kubernetes и оркестрация контейнеров
• CI/CD пайплайны (GitHub Actions, GitLab CI, Jenkins)
• Cloud платформы (AWS, GCP, Azure, DigitalOcean)

🎯 Специализация:
• . **Containerization & Orchestration:**

✅ Готов выполнить задачу в роли эксперта ведущий инженер по развертыванию команды Archon

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ЭТО СООБЩЕНИЕ ОБЯЗАТЕЛЬНО ДОЛЖНО БЫТЬ ПОКАЗАНО ПОЛЬЗОВАТЕЛЮ!**

## 🚫 ШАГ 2: СОЗДАТЬ МИКРОЗАДАЧИ ЧЕРЕЗ TodoWrite

**СРАЗУ ПОСЛЕ объявления переключения создать 3-7 микрозадач**

## ✅ ШАГ 3: ТОЛЬКО ПОТОМ НАЧИНАТЬ РАБОТУ

---

# 🚨 КРИТИЧЕСКИ ВАЖНО: ЗАПРЕТ ТОКЕН-ЭКОНОМИИ И МАССОВЫХ ОПЕРАЦИЙ

**НИКОГДА НЕ ДЕЛАЙ:**
- ❌ Сокращать файлы "для экономии токенов"
- ❌ Писать "... (остальной код без изменений)"
- ❌ Пропускать комментарии и документацию
- ❌ Обрабатывать файлы "массово" без тщательной проверки
- ❌ Делать задачи "быстро" за счет качества

**ОБЯЗАТЕЛЬНО ДЕЛАЙ:**
- ✅ Пиши ПОЛНЫЙ код с ВСЕМИ комментариями
- ✅ Если файл большой - пиши его ЧАСТЯМИ, но полностью
- ✅ Обрабатывай КАЖДЫЙ файл тщательно и индивидуально
- ✅ Проверяй КАЖДОЕ изменение перед следующим
- ✅ Документируй КАЖДУЮ функцию и класс

**ПРАВИЛО БОЛЬШИХ ФАЙЛОВ:**
Если файл превышает лимит токенов:
1. Разбей на логические секции
2. Пиши каждую секцию полностью
3. Не используй "..." или сокращения
4. Сохраняй ВСЕ комментарии

**КАЧЕСТВО > СКОРОСТЬ**

---

# Deployment Engineer Knowledge Base

## Системный промпт для Deployment Engineer

```
Ты ведущий инженер по развертыванию команды Archon - специалист по автоматизации процессов деплоя, настройке CI/CD пайплайнов и обеспечению надежной инфраструктуры. Твоя экспертиза критична для бесперебойной работы систем.

**Твоя экспертиза:**
- Docker и контейнеризация приложений
- Kubernetes и оркестрация контейнеров
- CI/CD пайплайны (GitHub Actions, GitLab CI, Jenkins)
- Cloud платформы (AWS, GCP, Azure, DigitalOcean)
- Infrastructure as Code (Terraform, Ansible, Pulumi)
- Monitoring и Observability (Prometheus, Grafana, DataDog)
- Automated testing в пайплайнах
- Security scanning и compliance

**Ключевые области ответственности:**

1. **Containerization & Orchestration:**
   - Создание оптимизированных Dockerfile
   - Multi-stage builds для минимизации размера образов
   - Kubernetes манифесты и Helm charts
   - Service mesh настройка (Istio, Linkerd)

2. **CI/CD Automation:**
   - GitHub Actions workflows для автоматических деплоев
   - GitLab CI pipelines с multi-stage deployment
   - Jenkins pipelines для сложных enterprise сценариев
   - Automated rollback стратегии

3. **Cloud Infrastructure:**
   - Terraform модули для управления инфраструктурой
   - Kubernetes clusters на различных облаках
   - Load balancing и auto-scaling настройка
   - Cost optimization стратегии

4. **Monitoring & Alerting:**
   - Prometheus metrics сбор
   - Grafana dashboards для визуализации
   - Alert rules для проактивного реагирования
   - Distributed tracing (Jaeger, Zipkin)

**Подход к работе:**
1. Автоматизируй все повторяющиеся процессы
2. Применяй Infrastructure as Code принципы
3. Обеспечивай observability на всех уровнях
4. Внедряй security scanning в CI/CD
5. Оптимизируй затраты на инфраструктуру
```

## Docker Best Practices

### Оптимизированный Multi-Stage Build
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

### Docker Compose для локальной разработки
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

## Kubernetes Deployment

### Complete Kubernetes Manifests
```yaml
# ========================================
# Namespace
# ========================================
apiVersion: v1
kind: Namespace
metadata:
  name: archon-agent
  labels:
    name: archon-agent

---
# ========================================
# ConfigMap - Конфигурация приложения
# ========================================
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: archon-agent
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  PORT: "8000"

---
# ========================================
# Secret - Секретные данные
# ========================================
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: archon-agent
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:password@postgres:5432/mydb"
  LLM_API_KEY: "your-llm-api-key"
  REDIS_URL: "redis://redis:6379/0"

---
# ========================================
# Deployment - Основное приложение
# ========================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: archon-agent
  namespace: archon-agent
  labels:
    app: archon-agent
    version: v1
spec:
  replicas: 3
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: archon-agent
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: archon-agent
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: archon-agent-sa
      securityContext:
        fsGroup: 1000
        runAsNonRoot: true
        runAsUser: 1000

      containers:
      - name: archon-agent
        image: archon-agent:latest
        imagePullPolicy: Always

        ports:
        - name: http
          containerPort: 8000
          protocol: TCP

        env:
        - name: PORT
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: PORT
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: LOG_LEVEL
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_URL
        - name: LLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: LLM_API_KEY

        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3

        volumeMounts:
        - name: logs
          mountPath: /app/logs
        - name: tmp
          mountPath: /tmp

      volumes:
      - name: logs
        emptyDir: {}
      - name: tmp
        emptyDir: {}

---
# ========================================
# Service - Expose приложения
# ========================================
apiVersion: v1
kind: Service
metadata:
  name: archon-agent-service
  namespace: archon-agent
  labels:
    app: archon-agent
spec:
  type: ClusterIP
  selector:
    app: archon-agent
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: http
  sessionAffinity: None

---
# ========================================
# Ingress - Внешний доступ
# ========================================
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: archon-agent-ingress
  namespace: archon-agent
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - agent.example.com
    secretName: archon-agent-tls
  rules:
  - host: agent.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: archon-agent-service
            port:
              number: 80

---
# ========================================
# HorizontalPodAutoscaler - Auto-scaling
# ========================================
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: archon-agent-hpa
  namespace: archon-agent
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
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 4
        periodSeconds: 30
      selectPolicy: Max

---
# ========================================
# ServiceAccount
# ========================================
apiVersion: v1
kind: ServiceAccount
metadata:
  name: archon-agent-sa
  namespace: archon-agent
```

## GitHub Actions CI/CD Pipeline

### Complete Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ========================================
  # Job 1: Lint and Test
  # ========================================
  test:
    name: Lint and Test
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'

    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Install dependencies
      run: |
        poetry install --no-interaction

    - name: Run linters
      run: |
        poetry run flake8 .
        poetry run mypy .
        poetry run black --check .

    - name: Run tests
      run: |
        poetry run pytest --cov=. --cov-report=xml --cov-report=html

    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  # ========================================
  # Job 2: Security Scanning
  # ========================================
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: test

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

    - name: Run Bandit security linter
      run: |
        pip install bandit
        bandit -r . -f json -o bandit-report.json || true

    - name: Upload Bandit results
      uses: actions/upload-artifact@v3
      with:
        name: bandit-security-report
        path: bandit-report.json

  # ========================================
  # Job 3: Build Docker Image
  # ========================================
  build:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
        build-args: |
          VERSION=${{ github.sha }}

  # ========================================
  # Job 4: Deploy to Kubernetes
  # ========================================
  deploy:
    name: Deploy to Kubernetes
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Configure kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'

    - name: Set up kubeconfig
      run: |
        mkdir -p $HOME/.kube
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
        chmod 600 $HOME/.kube/config

    - name: Update image in deployment
      run: |
        kubectl set image deployment/archon-agent \
          archon-agent=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n archon-agent

    - name: Wait for rollout to complete
      run: |
        kubectl rollout status deployment/archon-agent -n archon-agent --timeout=5m

    - name: Verify deployment
      run: |
        kubectl get pods -n archon-agent -l app=archon-agent
        kubectl get services -n archon-agent

  # ========================================
  # Job 5: Smoke Tests
  # ========================================
  smoke-test:
    name: Run Smoke Tests
    runs-on: ubuntu-latest
    needs: deploy

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Run smoke tests
      run: |
        curl -f https://agent.example.com/health || exit 1
        curl -f https://agent.example.com/ready || exit 1

    - name: Notify on failure
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: 'Deployment smoke tests failed!'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Terraform Infrastructure as Code

### AWS Infrastructure Module
```hcl
# ========================================
# main.tf - Primary infrastructure
# ========================================
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "archon-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = "archon-agent"
      ManagedBy   = "terraform"
    }
  }
}

# ========================================
# VPC Configuration
# ========================================
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "archon-vpc-${var.environment}"
  cidr = var.vpc_cidr

  azs             = data.aws_availability_zones.available.names
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway   = true
  single_nat_gateway   = var.environment != "production"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Environment = var.environment
  }
}

# ========================================
# EKS Cluster
# ========================================
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "archon-cluster-${var.environment}"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    general = {
      desired_size = var.node_desired_size
      min_size     = var.node_min_size
      max_size     = var.node_max_size

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"

      labels = {
        role = "general"
      }

      tags = {
        NodeGroup = "general"
      }
    }
  }

  tags = {
    Environment = var.environment
  }
}

# ========================================
# RDS PostgreSQL Database
# ========================================
module "db" {
  source = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "archon-db-${var.environment}"

  engine               = "postgres"
  engine_version       = "15.4"
  family               = "postgres15"
  major_engine_version = "15"
  instance_class       = var.db_instance_class

  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  port     = 5432

  multi_az               = var.environment == "production"
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [module.db_security_group.security_group_id]

  backup_retention_period = 7
  skip_final_snapshot     = var.environment != "production"
  deletion_protection     = var.environment == "production"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = {
    Environment = var.environment
  }
}

# ========================================
# ElastiCache Redis
# ========================================
module "redis" {
  source = "terraform-aws-modules/elasticache/aws"
  version = "~> 1.0"

  cluster_id           = "archon-redis-${var.environment}"
  engine               = "redis"
  engine_version       = "7.0"
  parameter_group_name = "default.redis7"

  node_type            = var.redis_node_type
  num_cache_nodes      = var.environment == "production" ? 3 : 1
  port                 = 6379

  subnet_ids          = module.vpc.private_subnets
  security_group_ids  = [module.redis_security_group.security_group_id]

  snapshot_retention_limit = 5
  automatic_failover_enabled = var.environment == "production"

  tags = {
    Environment = var.environment
  }
}

# ========================================
# Application Load Balancer
# ========================================
module "alb" {
  source = "terraform-aws-modules/alb/aws"
  version = "~> 9.0"

  name = "archon-alb-${var.environment}"

  load_balancer_type = "application"
  vpc_id             = module.vpc.vpc_id
  subnets            = module.vpc.public_subnets
  security_groups    = [module.alb_security_group.security_group_id]

  enable_deletion_protection = var.environment == "production"

  target_groups = [
    {
      name             = "archon-tg-${var.environment}"
      backend_protocol = "HTTP"
      backend_port     = 8000
      target_type      = "ip"

      health_check = {
        enabled             = true
        interval            = 30
        path                = "/health"
        port                = "traffic-port"
        healthy_threshold   = 3
        unhealthy_threshold = 3
        timeout             = 6
        protocol            = "HTTP"
        matcher             = "200"
      }
    }
  ]

  tags = {
    Environment = var.environment
  }
}

# ========================================
# variables.tf
# ========================================
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "node_desired_size" {
  description = "Desired number of EKS nodes"
  type        = number
  default     = 3
}

variable "node_min_size" {
  description = "Minimum number of EKS nodes"
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum number of EKS nodes"
  type        = number
  default     = 10
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "archon"
}

variable "db_username" {
  description = "Database username"
  type        = string
  sensitive   = true
}

variable "redis_node_type" {
  description = "Redis node type"
  type        = string
  default     = "cache.t3.micro"
}
```

## Monitoring and Observability

### Prometheus Configuration
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'archon-production'
    environment: 'production'

alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - 'alertmanager:9093'

rule_files:
  - '/etc/prometheus/rules/*.yml'

scrape_configs:
  # Scrape Prometheus itself
  - job_name: 'prometheus'
    static_configs:
    - targets: ['localhost:9090']

  # Scrape application metrics
  - job_name: 'archon-agent'
    kubernetes_sd_configs:
    - role: pod
      namespaces:
        names:
        - archon-agent
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

  # Scrape Kubernetes components
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
```

### Alert Rules
```yaml
# monitoring/prometheus/rules/alerts.yml
groups:
- name: archon_alerts
  interval: 30s
  rules:
  # High error rate
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value }} for {{ $labels.instance }}"

  # High latency
  - alert: HighLatency
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High latency detected"
      description: "95th percentile latency is {{ $value }}s for {{ $labels.instance }}"

  # Pod down
  - alert: PodDown
    expr: kube_pod_status_phase{phase!="Running",namespace="archon-agent"} > 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Pod is not running"
      description: "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is {{ $labels.phase }}"

  # High CPU usage
  - alert: HighCPUUsage
    expr: rate(container_cpu_usage_seconds_total{namespace="archon-agent"}[5m]) > 0.8
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage"
      description: "CPU usage is {{ $value }} for {{ $labels.pod }}"

  # High memory usage
  - alert: HighMemoryUsage
    expr: container_memory_usage_bytes{namespace="archon-agent"} / container_spec_memory_limit_bytes{namespace="archon-agent"} > 0.9
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "High memory usage"
      description: "Memory usage is {{ $value }} for {{ $labels.pod }}"
```

### Grafana Dashboard (JSON)
```json
{
  "dashboard": {
    "title": "Archon Agent Monitoring",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "id": 2,
        "title": "Latency (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "id": 3,
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      }
    ]
  }
}
```

## Best Practices для Deployment Engineer

### 1. Container Optimization
- Multi-stage builds для минимизации размера
- Непривилегированные пользователи в контейнерах
- Health checks для всех сервисов
- Security scanning образов

### 2. CI/CD Pipeline
- Automated testing на всех стадиях
- Security scanning перед деплоем
- Rollback стратегии
- Blue/Green или Canary deployments

### 3. Infrastructure as Code
- Terraform для всей инфраструктуры
- Версионирование конфигурации
- Environment-specific конфигурации
- Cost optimization через tagging

### 4. Monitoring & Alerting
- Prometheus для метрик
- Grafana для визуализации
- Alert rules для критичных метрик
- Distributed tracing для debugging

### 5. Security
- TLS/SSL для всех коммуникаций
- Secrets management (Vault, AWS Secrets Manager)
- Network policies в Kubernetes
- Regular security audits
