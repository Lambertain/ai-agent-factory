"""
Deployment Engineer Tools - инструменты для DevOps, CI/CD и автоматизации развертывания.
"""

from pydantic_ai import Agent, RunContext
from .dependencies import DeploymentEngineerDependencies
from typing import Dict, Any, List
import asyncio


def register_tools(agent: Agent):
    """Регистрация всех инструментов для Deployment Engineer."""

    @agent.tool
    async def check_docker_health(
        ctx: RunContext[DeploymentEngineerDependencies],
        container_name: str
    ) -> str:
        """
        Проверить здоровье Docker контейнера.

        Args:
            container_name: Название контейнера

        Returns:
            Статус контейнера и health check результаты
        """
        try:
            # Симуляция проверки Docker контейнера
            result = {
                "container": container_name,
                "status": "running",
                "health": "healthy",
                "uptime": "2d 5h 34m",
                "memory_usage": "256MB / 512MB",
                "cpu_usage": "12%"
            }

            return f"""
Статус Docker контейнера:
- Контейнер: {result['container']}
- Статус: {result['status']}
- Здоровье: {result['health']}
- Uptime: {result['uptime']}
- Память: {result['memory_usage']}
- CPU: {result['cpu_usage']}
"""
        except Exception as e:
            return f"Ошибка проверки контейнера: {str(e)}"

    @agent.tool
    async def check_kubernetes_pods(
        ctx: RunContext[DeploymentEngineerDependencies],
        namespace: str = "default"
    ) -> str:
        """
        Проверить статус подов в Kubernetes namespace.

        Args:
            namespace: Kubernetes namespace

        Returns:
            Список подов и их статусы
        """
        try:
            # Симуляция получения подов Kubernetes
            pods = [
                {"name": "app-deployment-abc123", "status": "Running", "restarts": 0, "age": "5d"},
                {"name": "app-deployment-def456", "status": "Running", "restarts": 0, "age": "5d"},
                {"name": "app-deployment-ghi789", "status": "Running", "restarts": 1, "age": "3d"}
            ]

            result = f"Поды в namespace '{namespace}':\n\n"
            for pod in pods:
                result += f"- {pod['name']}: {pod['status']} (рестарты: {pod['restarts']}, возраст: {pod['age']})\n"

            return result
        except Exception as e:
            return f"Ошибка получения подов: {str(e)}"

    @agent.tool
    async def generate_dockerfile(
        ctx: RunContext[DeploymentEngineerDependencies],
        language: str,
        project_type: str
    ) -> str:
        """
        Сгенерировать оптимизированный Dockerfile для проекта.

        Args:
            language: Язык программирования (python, node, go, etc.)
            project_type: Тип проекта (api, web, worker, etc.)

        Returns:
            Содержимое Dockerfile
        """
        dockerfiles = {
            "python_api": """# Multi-stage build для Python API
FROM python:3.11-slim AS base

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Builder stage
FROM base AS builder
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \\
    && poetry install --no-dev --no-interaction --no-ansi

# Production stage
FROM base AS production
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
            "node_web": """# Multi-stage build для Node.js приложения
FROM node:18-alpine AS base
RUN apk add --no-cache libc6-compat

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS production
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
"""
        }

        key = f"{language}_{project_type}"
        if key in dockerfiles:
            return f"Сгенерирован Dockerfile для {language} {project_type}:\n\n{dockerfiles[key]}"
        else:
            return f"Dockerfile для комбинации {language}/{project_type} не найден. Доступные: {list(dockerfiles.keys())}"

    @agent.tool
    async def generate_github_actions_workflow(
        ctx: RunContext[DeploymentEngineerDependencies],
        workflow_type: str
    ) -> str:
        """
        Сгенерировать GitHub Actions workflow для CI/CD.

        Args:
            workflow_type: Тип workflow (test, deploy, full)

        Returns:
            YAML конфигурация GitHub Actions
        """
        workflows = {
            "test": """name: Test Pipeline

on:
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - run: pip install poetry && poetry install
    - run: poetry run pytest --cov
""",
            "deploy": """name: Deploy Pipeline

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: docker/setup-buildx-action@v3
    - uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    - uses: docker/build-push-action@v5
      with:
        push: true
        tags: ghcr.io/${{ github.repository }}:latest
""",
            "full": """name: Full CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    - run: pip install poetry && poetry install
    - run: poetry run pytest --cov --cov-report=xml
    - uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    needs: test
    steps:
    - uses: actions/checkout@v4
    - uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        format: 'sarif'
        output: 'trivy-results.sarif'
    - uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  build:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v4
    - uses: docker/setup-buildx-action@v3
    - uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    - uses: docker/build-push-action@v5
      with:
        push: true
        tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
    - uses: actions/checkout@v4
    - uses: azure/setup-kubectl@v3
    - run: |
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
        kubectl set image deployment/app app=ghcr.io/${{ github.repository }}:${{ github.sha }}
        kubectl rollout status deployment/app --timeout=5m
"""
        }

        if workflow_type in workflows:
            return f"GitHub Actions workflow '{workflow_type}':\n\n{workflows[workflow_type]}"
        else:
            return f"Workflow тип '{workflow_type}' не найден. Доступные: {list(workflows.keys())}"

    @agent.tool
    async def generate_kubernetes_manifests(
        ctx: RunContext[DeploymentEngineerDependencies],
        app_name: str,
        replicas: int = 3
    ) -> str:
        """
        Сгенерировать Kubernetes манифесты для приложения.

        Args:
            app_name: Название приложения
            replicas: Количество реплик

        Returns:
            Kubernetes YAML манифесты
        """
        manifests = f"""---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  labels:
    app: {app_name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {app_name}:latest
        ports:
        - containerPort: 8000
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
  name: {app_name}-service
spec:
  selector:
    app: {app_name}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {app_name}-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {app_name}
  minReplicas: {replicas}
  maxReplicas: {replicas * 3}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
"""
        return f"Kubernetes манифесты для {app_name}:\n\n{manifests}"

    @agent.tool
    async def check_deployment_health(
        ctx: RunContext[DeploymentEngineerDependencies],
        deployment_url: str
    ) -> str:
        """
        Проверить здоровье развернутого приложения.

        Args:
            deployment_url: URL развернутого приложения

        Returns:
            Результаты health check
        """
        try:
            # Симуляция health check
            health_status = {
                "url": deployment_url,
                "status": "healthy",
                "response_time": "45ms",
                "checks": {
                    "database": "connected",
                    "redis": "connected",
                    "external_api": "available"
                }
            }

            result = f"""
Health Check для {health_status['url']}:
- Общий статус: {health_status['status']}
- Время ответа: {health_status['response_time']}
- База данных: {health_status['checks']['database']}
- Redis: {health_status['checks']['redis']}
- Внешние API: {health_status['checks']['external_api']}
"""
            return result
        except Exception as e:
            return f"Ошибка health check: {str(e)}"

    @agent.tool
    async def estimate_infrastructure_cost(
        ctx: RunContext[DeploymentEngineerDependencies],
        cloud_provider: str,
        resources: Dict[str, Any]
    ) -> str:
        """
        Оценить стоимость инфраструктуры.

        Args:
            cloud_provider: Облачный провайдер (aws, gcp, azure)
            resources: Словарь с ресурсами

        Returns:
            Оценка стоимости
        """
        # Примерные расчеты стоимости
        base_costs = {
            "aws": {
                "compute": 0.10,  # per hour per instance
                "database": 0.20,  # per hour
                "load_balancer": 0.025  # per hour
            },
            "gcp": {
                "compute": 0.095,
                "database": 0.19,
                "load_balancer": 0.023
            },
            "azure": {
                "compute": 0.098,
                "database": 0.195,
                "load_balancer": 0.024
            }
        }

        if cloud_provider not in base_costs:
            return f"Провайдер {cloud_provider} не поддерживается. Доступные: aws, gcp, azure"

        costs = base_costs[cloud_provider]
        instances = resources.get("instances", 3)
        has_db = resources.get("database", True)
        has_lb = resources.get("load_balancer", True)

        monthly_cost = 0
        monthly_cost += costs["compute"] * instances * 24 * 30
        if has_db:
            monthly_cost += costs["database"] * 24 * 30
        if has_lb:
            monthly_cost += costs["load_balancer"] * 24 * 30

        return f"""
Оценка стоимости инфраструктуры на {cloud_provider}:
- Compute ({instances} инстансов): ${costs['compute'] * instances * 24 * 30:.2f}/мес
- Database: ${costs['database'] * 24 * 30:.2f}/мес
- Load Balancer: ${costs['load_balancer'] * 24 * 30:.2f}/мес

Итого: ${monthly_cost:.2f}/мес (приблизительно)
"""
