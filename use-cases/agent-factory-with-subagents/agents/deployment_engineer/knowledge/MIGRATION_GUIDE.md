# Deployment Engineer - Module Index

**Version:** 1.0
**Date:** 2025-10-20
**Author:** Archon Implementation Engineer
**Purpose:** Intelligent module selection based on task keywords and context

---

## 📊 Module Overview

| # | Module | Priority | Lines | Domain | Load When |
|---|--------|----------|-------|--------|-----------|
| **01** | [Docker & Containerization](modules/01_docker_containerization.md) | 🔴 CRITICAL | 395 | Container builds & optimization | Docker, image, build tasks |
| **02** | [Kubernetes Orchestration](modules/02_kubernetes_orchestration.md) | 🔴 CRITICAL | 547 | K8s deployment & scaling | K8s deployment, orchestration |
| **03** | [CI/CD Pipelines](modules/03_cicd_pipelines.md) | 🟡 HIGH | 575 | Automation & testing | CI/CD setup, pipeline tasks |
| **04** | [Infrastructure as Code](modules/04_infrastructure_as_code.md) | 🟢 MEDIUM | 831 | Terraform & cloud infra | Infrastructure provisioning |
| **05** | [Monitoring & Observability](modules/05_monitoring_observability.md) | 🟡 HIGH | 649 | Metrics & alerts | Monitoring, observability |
| **06** | [Security Best Practices](modules/06_security_best_practices.md) | 🟢 MEDIUM | 659 | Security hardening | Security, compliance tasks |

**Total Knowledge:** 3,656 lines in modules + 53 lines system prompt

**Priority Legend:**
- 🔴 **CRITICAL** - Load frequency: 60-70% of tasks
- 🟡 **HIGH** - Load frequency: 50-55% of tasks
- 🟢 **MEDIUM** - Load frequency: 30-35% of tasks

---

## 📦 Module 01: Docker & Containerization

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- Создание или оптимизация Dockerfile
- Настройка Docker Compose для multi-container приложений
- Оптимизация размера Docker образов
- Решение проблем с containerization

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* docker, dockerfile, контейнер, образ, сборка, контейнеризация, multi-stage, buildkit

*English:* docker, dockerfile, container, image, build, containerization, multi-stage, buildkit

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Multi-stage builds (base → builder → production)
- Docker BuildKit и caching strategies
- Docker Compose для orchestration
- .dockerignore и layer optimization
- Security context (non-root user, health checks)

**Примеры задач:**
- "Создать production-ready Dockerfile для Python приложения"
- "Оптимизировать Docker образ, уменьшить размер"
- "Настроить Docker Compose для development окружения"

---

## 📦 Module 02: Kubernetes Orchestration

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- Развертывание приложений в Kubernetes
- Настройка Kubernetes манифестов (Deployment, Service, Ingress)
- Автомасштабирование (HPA, VPA)
- Настройка RBAC и network policies

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* kubernetes, k8s, deployment, pod, service, ingress, autoscaling, hpa, манифест, оркестрация

*English:* kubernetes, k8s, deployment, pod, service, ingress, autoscaling, hpa, manifest, orchestration

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Kubernetes Deployment с health probes (liveness, readiness)
- Resource requests and limits
- HorizontalPodAutoscaler (HPA) configuration
- Service types (ClusterIP, NodePort, LoadBalancer)
- Ingress controllers и routing
- Network Policies для security

**Примеры задач:**
- "Развернуть приложение в Kubernetes с autoscaling"
- "Настроить Ingress для роутинга трафика"
- "Добавить health checks и resource limits"

---

## 📦 Module 03: CI/CD Pipelines

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- Настройка CI/CD pipeline (GitHub Actions, GitLab CI)
- Автоматизация тестирования и deployment
- Интеграция security scanning в pipeline
- Настройка automated rollback

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* ci/cd, пайплайн, github actions, gitlab ci, автоматизация, тестирование, deployment, workflow

*English:* ci/cd, pipeline, github actions, gitlab ci, automation, testing, deployment, workflow

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- 5-stage pipeline (Test → Security → Build → Deploy → Verify)
- GitHub Actions workflow syntax
- Docker Buildx в CI/CD
- Automated testing (linting, unit tests, coverage)
- Security scanning (Trivy, Bandit)
- Deployment strategies (rolling, blue-green)

**Примеры задач:**
- "Создать GitHub Actions workflow для автоматического deploy"
- "Добавить security scanning в CI/CD pipeline"
- "Настроить automated rollback при ошибках"

---

## 📦 Module 04: Infrastructure as Code

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Provisioning cloud infrastructure (AWS, GCP, Azure)
- Создание Terraform modules
- Настройка VPC, EKS, RDS через IaC
- Управление remote state

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* terraform, iac, инфраструктура, aws, gcp, azure, cloud, provisioning, vpc, eks

*English:* terraform, iac, infrastructure, aws, gcp, azure, cloud, provisioning, vpc, eks

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Terraform modules и resource organization
- Remote state в S3 + DynamoDB lock
- AWS resources (VPC, EKS, RDS, Redis, ALB)
- Version constraints и provider configuration
- Terratest для infrastructure testing

**Примеры задач:**
- "Создать Terraform module для VPC на AWS"
- "Настроить EKS cluster через Terraform"
- "Добавить remote state в S3 для team collaboration"

---

## 📦 Module 05: Monitoring & Observability

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- Настройка Prometheus для сбора метрик
- Создание Grafana dashboards
- Настройка alerting rules
- Instrumentation приложений (metrics, tracing)

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* мониторинг, prometheus, grafana, метрики, алерты, observability, логи, трейсинг

*English:* monitoring, prometheus, grafana, metrics, alerts, observability, logs, tracing

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Prometheus Golden Signals (Latency, Traffic, Errors, Saturation)
- Grafana dashboard creation
- AlertManager и notification channels
- Application instrumentation (prometheus_client)
- Distributed tracing (OpenTelemetry)
- Structured logging

**Примеры задач:**
- "Настроить Prometheus monitoring для K8s приложения"
- "Создать Grafana dashboard для business метрик"
- "Добавить alerting для critical errors"

---

## 📦 Module 06: Security Best Practices

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Security hardening инфраструктуры
- Настройка secrets management
- Compliance и vulnerability scanning
- Network security (policies, TLS)

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* безопасность, security, уязвимости, секреты, tls, rbac, network policy, compliance

*English:* security, vulnerability, secrets, tls, rbac, network policy, compliance

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Kubernetes Network Policies
- Secrets management (Sealed Secrets, External Secrets Operator)
- TLS/SSL certificates и encryption
- RBAC configuration
- Vulnerability scanning (Trivy, Snyk)
- Security best practices (non-root, read-only filesystem)

**Примеры задач:**
- "Настроить Sealed Secrets для безопасного хранения credentials"
- "Добавить Network Policies для изоляции pods"
- "Интегрировать vulnerability scanning в CI/CD"

---

## 🤖 Module Selection Function

### select_modules_for_task()

Intelligent module selection based on task keywords and context.

```python
def select_modules_for_task(task_description: str, task_title: str = "") -> list[str]:
    """
    Выбирает релевантные модули на основе анализа задачи.

    Args:
        task_description: Полное описание задачи
        task_title: Название задачи (опционально)

    Returns:
        List of module file paths to load

    Example:
        >>> select_modules_for_task("Создать Dockerfile для Python приложения")
        ["modules/01_docker_containerization.md"]

        >>> select_modules_for_task("Deploy в K8s с monitoring")
        ["modules/02_kubernetes_orchestration.md",
         "modules/05_monitoring_observability.md"]
    """

    full_text = f"{task_title} {task_description}".lower()
    selected_modules = []

    # Module 01: Docker & Containerization
    docker_keywords = [
        "docker", "dockerfile", "контейнер", "container", "образ", "image",
        "build", "сборка", "multi-stage", "buildkit", "docker-compose",
        "контейнеризация", "containerization"
    ]
    if any(kw in full_text for kw in docker_keywords):
        selected_modules.append("modules/01_docker_containerization.md")

    # Module 02: Kubernetes Orchestration
    k8s_keywords = [
        "kubernetes", "k8s", "deployment", "pod", "service", "ingress",
        "autoscaling", "hpa", "vpa", "оркестрация", "orchestration",
        "манифест", "manifest", "helm", "kustomize", "rbac"
    ]
    if any(kw in full_text for kw in k8s_keywords):
        selected_modules.append("modules/02_kubernetes_orchestration.md")

    # Module 03: CI/CD Pipelines
    cicd_keywords = [
        "ci/cd", "cicd", "pipeline", "пайплайн", "github actions",
        "gitlab ci", "jenkins", "workflow", "автоматизация", "automation",
        "testing", "тестирование", "deploy", "rollback"
    ]
    if any(kw in full_text for kw in cicd_keywords):
        selected_modules.append("modules/03_cicd_pipelines.md")

    # Module 04: Infrastructure as Code
    iac_keywords = [
        "terraform", "iac", "infrastructure", "инфраструктура",
        "aws", "gcp", "azure", "cloud", "vpc", "eks", "rds",
        "provisioning", "state", "module"
    ]
    if any(kw in full_text for kw in iac_keywords):
        selected_modules.append("modules/04_infrastructure_as_code.md")

    # Module 05: Monitoring & Observability
    monitoring_keywords = [
        "monitoring", "мониторинг", "prometheus", "grafana",
        "metrics", "метрики", "alert", "алерт", "observability",
        "logs", "логи", "tracing", "трейсинг", "dashboard"
    ]
    if any(kw in full_text for kw in monitoring_keywords):
        selected_modules.append("modules/05_monitoring_observability.md")

    # Module 06: Security Best Practices
    security_keywords = [
        "security", "безопасность", "vulnerability", "уязвимость",
        "secret", "секрет", "tls", "ssl", "rbac", "network policy",
        "compliance", "scan", "hardening"
    ]
    if any(kw in full_text for kw in security_keywords):
        selected_modules.append("modules/06_security_best_practices.md")

    # Fallback: if no keywords matched, load CRITICAL modules
    if not selected_modules:
        selected_modules = [
            "modules/01_docker_containerization.md",
            "modules/02_kubernetes_orchestration.md"
        ]

    return selected_modules
```

### Usage Examples

**Example 1: Simple Docker task**
```python
Task: "Создать optimized Dockerfile для FastAPI приложения"
Selected: ["modules/01_docker_containerization.md"]
Result: 1 module loaded (CRITICAL priority)
```

**Example 2: K8s deployment with monitoring**
```python
Task: "Deploy приложение в Kubernetes с Prometheus monitoring"
Selected: ["modules/02_kubernetes_orchestration.md",
           "modules/05_monitoring_observability.md"]
Result: 2 modules loaded (CRITICAL + HIGH priorities)
```

**Example 3: Full CI/CD stack**
```python
Task: "Setup complete CI/CD: Docker build → K8s deploy → Monitoring"
Selected: ["modules/01_docker_containerization.md",
           "modules/02_kubernetes_orchestration.md",
           "modules/03_cicd_pipelines.md",
           "modules/05_monitoring_observability.md"]
Result: 4 modules loaded (complex multi-domain task)
```

**Example 4: Production infrastructure**
```python
Task: "Terraform для AWS VPC + EKS + Security hardening"
Selected: ["modules/02_kubernetes_orchestration.md",
           "modules/04_infrastructure_as_code.md",
           "modules/06_security_best_practices.md"]
Result: 3 modules loaded (infrastructure + security focus)
```

---

## 🔄 Workflow Integration

### 7-Stage Process

```
STAGE 1: Read deployment_engineer_system_prompt.md (~500 tokens)
   ↓ File: knowledge/deployment_engineer_system_prompt.md
   ↓ Contains: Role identity + 5 Core Principles

STAGE 2: Read task from Archon MCP
   ↓ mcp__archon__find_tasks(task_id="...")

STAGE 3: Read deployment_engineer_module_selection.md + select modules
   ↓ File: knowledge/deployment_engineer_module_selection.md
   ↓ Select 2-3 relevant modules из 6

STAGE 4: Read ONLY SELECTED modules
   ↓ Files: knowledge/modules/01-06_*.md
   ↓ Load only relevant knowledge

STAGE 5: Git Log First
   ↓ git log --oneline -10
   ↓ Project context from recent changes

STAGE 6: Read existing code (MANDATORY!)
   ↓ Grep/Glob for existing implementation
   ↓ Read for code analysis

STAGE 7: Execute task with minimal context
```

---

## 📈 Expected Performance

### Module Loading Distribution

**By Task Complexity:**
- Simple tasks (1 module): Docker-only, K8s-only, CI/CD-only
- Medium tasks (2 modules): Docker + K8s, K8s + Monitoring, IaC + Security
- Complex tasks (3-4 modules): Full stack, Production deployment

**Average:** 2.3 modules per task (из 6 available)

### Priority Validation

**Module Load Frequency (predicted):**
- 🔴 01_docker: 70% of tasks
- 🔴 02_kubernetes: 65% of tasks
- 🟡 03_cicd: 55% of tasks
- 🟡 05_monitoring: 50% of tasks
- 🟢 04_infrastructure: 35% of tasks
- 🟢 06_security: 30% of tasks

---

## ✅ Best Practices

### DO:
1. **ALWAYS read system_prompt.md first** - this is role identity
2. **Use MODULE_INDEX.md for selection** - don't guess which modules to load
3. **Load ONLY relevant modules** - not all 6 modules
4. **Check existing code (STAGE 6)** - mandatory before changes
5. **Use Git context (STAGE 5)** - for project history understanding

### DON'T:
1. **DON'T load all 6 modules** - only relevant 2-3
2. **DON'T skip MODULE_INDEX.md** - critical for module selection
3. **DON'T guess which modules needed** - use select_modules_for_task()
4. **DON'T ignore STAGE 6** - code reading is mandatory
5. **DON'T skip Git context** - history matters

---

**Version:** 1.0
**Date:** 2025-10-20
**Author:** Archon Implementation Engineer
**Status:** Ready for production use
