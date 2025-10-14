# Module 03: CI/CD Pipelines

**Назад к:** [Deployment Engineer Knowledge Base](../deployment_engineer_knowledge.md)

---

## GitHub Actions CI/CD Pipeline

### Complete Multi-Stage Workflow

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

**Ключевые стадии:**
1. ✅ Test - lint, type check, unit tests
2. ✅ Security - Trivy, Bandit scanning
3. ✅ Build - Docker image build and push
4. ✅ Deploy - Kubernetes deployment
5. ✅ Smoke Test - post-deployment verification

---

## GitLab CI Pipeline

### Alternative Pipeline Configuration

```yaml
# .gitlab-ci.yml
stages:
  - test
  - security
  - build
  - deploy
  - verify

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

# ========================================
# Test Stage
# ========================================
test:
  stage: test
  image: python:3.11
  before_script:
    - pip install poetry
    - poetry install
  script:
    - poetry run flake8 .
    - poetry run mypy .
    - poetry run pytest --cov=. --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

# ========================================
# Security Stage
# ========================================
security:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy fs --exit-code 0 --severity HIGH,CRITICAL .
  allow_failure: true

# ========================================
# Build Stage
# ========================================
build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
    - docker tag $IMAGE_TAG $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main

# ========================================
# Deploy Stage
# ========================================
deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  before_script:
    - mkdir -p $HOME/.kube
    - echo "$KUBE_CONFIG" | base64 -d > $HOME/.kube/config
  script:
    - kubectl set image deployment/archon-agent archon-agent=$IMAGE_TAG -n archon-agent
    - kubectl rollout status deployment/archon-agent -n archon-agent --timeout=5m
  only:
    - main
  environment:
    name: production
    url: https://agent.example.com

# ========================================
# Verify Stage
# ========================================
verify:
  stage: verify
  script:
    - curl -f https://agent.example.com/health || exit 1
  only:
    - main
```

---

## Best Practices для CI/CD

### 1. Automated Testing

**Всегда запускай тесты перед деплоем:**
```yaml
# Обязательные проверки
- Linting (flake8, mypy)
- Unit tests (pytest)
- Integration tests
- Code coverage check
```

**Пример pytest конфигурации:**
```ini
# pytest.ini
[pytest]
minversion = 7.0
addopts =
    --cov=.
    --cov-report=term-missing
    --cov-report=html
    --cov-report=xml
    --cov-fail-under=80
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### 2. Security Scanning

**Multi-layer security:**
```yaml
# 1. Dependency scanning
- name: Dependency check
  run: |
    pip install safety
    safety check

# 2. SAST scanning
- name: Bandit scan
  run: bandit -r . -ll

# 3. Container scanning
- name: Trivy scan
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'image'
    image-ref: ${{ env.IMAGE_NAME }}
```

### 3. Rollback Strategies

**Automated rollback on failure:**
```yaml
- name: Deploy with rollback
  run: |
    kubectl apply -f k8s/
    kubectl rollout status deployment/archon-agent -n archon-agent || \
    kubectl rollout undo deployment/archon-agent -n archon-agent
```

**Blue/Green Deployment:**
```yaml
# Deploy to green environment
kubectl apply -f k8s/green/

# Wait for green to be ready
kubectl wait --for=condition=available deployment/archon-agent-green

# Switch traffic to green
kubectl patch service archon-agent -p '{"spec":{"selector":{"version":"green"}}}'

# Monitor and rollback if needed
if ! smoke_test; then
  kubectl patch service archon-agent -p '{"spec":{"selector":{"version":"blue"}}}'
fi
```

### 4. Environment Management

**Environment-specific configurations:**
```yaml
# Development
deploy-dev:
  environment: development
  variables:
    REPLICAS: 1
    RESOURCES_LIMITS_CPU: "500m"
    RESOURCES_LIMITS_MEMORY: "256Mi"

# Staging
deploy-staging:
  environment: staging
  variables:
    REPLICAS: 2
    RESOURCES_LIMITS_CPU: "1000m"
    RESOURCES_LIMITS_MEMORY: "512Mi"

# Production
deploy-prod:
  environment: production
  variables:
    REPLICAS: 3
    RESOURCES_LIMITS_CPU: "2000m"
    RESOURCES_LIMITS_MEMORY: "1Gi"
```

### 5. Caching and Optimization

**Docker layer caching:**
```yaml
- name: Build with cache
  uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Dependency caching:**
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/poetry.lock') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

---

## Monitoring CI/CD Pipeline

### Metrics to Track

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PipelineMetrics:
    """Метрики CI/CD пайплайна."""

    pipeline_id: str
    duration_seconds: float
    status: str  # success, failed, cancelled

    test_duration: float
    build_duration: float
    deploy_duration: float

    tests_passed: int
    tests_failed: int

    security_issues_found: int
    code_coverage_percent: float

    deployed_version: str
    deployment_timestamp: datetime

    def calculate_success_rate(self) -> float:
        """Рассчитать success rate тестов."""
        total_tests = self.tests_passed + self.tests_failed
        if total_tests == 0:
            return 100.0
        return (self.tests_passed / total_tests) * 100
```

### Pipeline Monitoring Dashboard

```yaml
# Prometheus metrics для GitHub Actions
- name: Export metrics
  run: |
    echo "pipeline_duration_seconds{job=\"${{ github.job }}\"} $DURATION" | \
    curl --data-binary @- http://pushgateway:9091/metrics/job/github_actions
```

---

**Навигация:**
- [← Предыдущий модуль: Kubernetes Orchestration](02_kubernetes_orchestration.md)
- [↑ Назад к Deployment Engineer Knowledge Base](../deployment_engineer_knowledge.md)
- [→ Следующий модуль: Infrastructure as Code](04_infrastructure_as_code.md)
