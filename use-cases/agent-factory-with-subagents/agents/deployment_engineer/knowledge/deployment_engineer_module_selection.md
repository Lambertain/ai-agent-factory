# Module Selection Guide - Deployment Engineer

**Version:** 1.0
**Date:** 2025-10-20
**Purpose:** Вибір релевантних модулів на основі аналізу задачі

---

## 📊 Доступні модулі

### Module 01: Docker & Containerization (395 lines)
**Priority:** 🔴 CRITICAL (70% of tasks)

**Коли читати:**
- Створення або оптимізація Dockerfile
- Налаштування Docker Compose для multi-container додатків
- Оптимізація розміру Docker образів
- Вирішення проблем з контейнеризацією

**Ключові слова:**
- **Російські:** docker, dockerfile, контейнер, образ, сборка, контейнеризация, multi-stage, buildkit
- **English:** docker, dockerfile, container, image, build, containerization, multi-stage, buildkit

**Технічні тригери:**
- Multi-stage builds (base → builder → production)
- Docker BuildKit та caching strategies
- Docker Compose для orchestration
- .dockerignore та layer optimization
- Security context (non-root user, health checks)

**Приклади задач:**
- "Створити production-ready Dockerfile для Python додатку"
- "Оптимізувати Docker образ, зменшити розмір"
- "Налаштувати Docker Compose для development оточення"

**Файл:** [modules/01_docker_containerization.md](modules/01_docker_containerization.md)

---

### Module 02: Kubernetes Orchestration (547 lines)
**Priority:** 🔴 CRITICAL (65% of tasks)

**Коли читати:**
- Розгортання додатків в Kubernetes
- Налаштування Kubernetes маніфестів (Deployment, Service, Ingress)
- Автомасштабування (HPA, VPA)
- Налаштування RBAC та network policies

**Ключові слова:**
- **Російські:** kubernetes, k8s, deployment, pod, service, ingress, autoscaling, hpa, манифест, оркестрация
- **English:** kubernetes, k8s, deployment, pod, service, ingress, autoscaling, hpa, manifest, orchestration

**Технічні тригери:**
- Kubernetes Deployment з health probes (liveness, readiness)
- Resource requests and limits
- HorizontalPodAutoscaler (HPA) configuration
- Service types (ClusterIP, NodePort, LoadBalancer)
- Ingress controllers та routing
- Network Policies для security

**Приклади задач:**
- "Розгорнути додаток в Kubernetes з autoscaling"
- "Налаштувати Ingress для роутингу трафіку"
- "Додати health checks та resource limits"

**Файл:** [modules/02_kubernetes_orchestration.md](modules/02_kubernetes_orchestration.md)

---

### Module 03: CI/CD Pipelines (575 lines)
**Priority:** 🟡 HIGH (55% of tasks)

**Коли читати:**
- Налаштування CI/CD pipeline (GitHub Actions, GitLab CI)
- Автоматизація тестування та deployment
- Інтеграція security scanning в pipeline
- Налаштування automated rollback

**Ключові слова:**
- **Російські:** ci/cd, пайплайн, github actions, gitlab ci, автоматизация, тестирование, deployment, workflow
- **English:** ci/cd, pipeline, github actions, gitlab ci, automation, testing, deployment, workflow

**Технічні тригери:**
- 5-stage pipeline (Test → Security → Build → Deploy → Verify)
- GitHub Actions workflow syntax
- Docker Buildx в CI/CD
- Automated testing (linting, unit tests, coverage)
- Security scanning (Trivy, Bandit)
- Deployment strategies (rolling, blue-green)

**Приклади задач:**
- "Створити GitHub Actions workflow для автоматичного deploy"
- "Додати security scanning в CI/CD pipeline"
- "Налаштувати automated rollback при помилках"

**Файл:** [modules/03_cicd_pipelines.md](modules/03_cicd_pipelines.md)

---

### Module 04: Infrastructure as Code (831 lines)
**Priority:** 🟢 MEDIUM (35% of tasks)

**Коли читати:**
- Provisioning cloud infrastructure (AWS, GCP, Azure)
- Створення Terraform modules
- Налаштування VPC, EKS, RDS через IaC
- Управління remote state

**Ключові слова:**
- **Російські:** terraform, iac, инфраструктура, aws, gcp, azure, cloud, provisioning, vpc, eks
- **English:** terraform, iac, infrastructure, aws, gcp, azure, cloud, provisioning, vpc, eks

**Технічні тригери:**
- Terraform modules та resource organization
- Remote state в S3 + DynamoDB lock
- AWS resources (VPC, EKS, RDS, Redis, ALB)
- Version constraints та provider configuration
- Terratest для infrastructure testing

**Приклади задач:**
- "Створити Terraform module для VPC на AWS"
- "Налаштувати EKS cluster через Terraform"
- "Додати remote state в S3 для team collaboration"

**Файл:** [modules/04_infrastructure_as_code.md](modules/04_infrastructure_as_code.md)

---

### Module 05: Monitoring & Observability (649 lines)
**Priority:** 🟡 HIGH (50% of tasks)

**Коли читати:**
- Налаштування Prometheus для збору метрик
- Створення Grafana dashboards
- Налаштування alerting rules
- Instrumentation додатків (metrics, tracing)

**Ключові слова:**
- **Російські:** мониторинг, prometheus, grafana, метрики, алерты, observability, логи, трейсинг
- **English:** monitoring, prometheus, grafana, metrics, alerts, observability, logs, tracing

**Технічні тригери:**
- Prometheus Golden Signals (Latency, Traffic, Errors, Saturation)
- Grafana dashboard creation
- AlertManager та notification channels
- Application instrumentation (prometheus_client)
- Distributed tracing (OpenTelemetry)
- Structured logging

**Приклади задач:**
- "Налаштувати Prometheus monitoring для K8s додатку"
- "Створити Grafana dashboard для business метрик"
- "Додати alerting для critical errors"

**Файл:** [modules/05_monitoring_observability.md](modules/05_monitoring_observability.md)

---

### Module 06: Security Best Practices (659 lines)
**Priority:** 🟢 MEDIUM (30% of tasks)

**Коли читати:**
- Security hardening інфраструктури
- Налаштування secrets management
- Compliance та vulnerability scanning
- Network security (policies, TLS)

**Ключові слова:**
- **Російські:** безопасность, security, уязвимости, секреты, tls, rbac, network policy, compliance
- **English:** security, vulnerability, secrets, tls, rbac, network policy, compliance

**Технічні тригери:**
- Kubernetes Network Policies
- Secrets management (Sealed Secrets, External Secrets Operator)
- TLS/SSL certificates та encryption
- RBAC configuration
- Vulnerability scanning (Trivy, Snyk)
- Security best practices (non-root, read-only filesystem)

**Приклади задач:**
- "Налаштувати Sealed Secrets для безпечного зберігання credentials"
- "Додати Network Policies для ізоляції pods"
- "Інтегрувати vulnerability scanning в CI/CD"

**Файл:** [modules/06_security_best_practices.md](modules/06_security_best_practices.md)

---

## 🎯 Алгоритм вибору модулів

### Крок 1: Проаналізуй опис задачі
Прочитай `task_title` та `task_description`, виділи ключові слова.

### Крок 2: Знайди відповідності з модулями
Порівняй ключові слова задачі з ключовими словами кожного модуля (російські + English).

### Крок 3: Вибери релевантні модулі
Додай модулі, які мають хоча б одне співпадіння ключових слів.

### Крок 4: Fallback для незрозумілих задач
Якщо жодний модуль не підійшов → завантажуй CRITICAL модулі (01_docker + 02_kubernetes).

---

## 📋 Приклади вибору

### Приклад 1: Simple Docker task
**Task:** "Оптимізувати Dockerfile для Python додатку"

**Аналіз:**
- Ключові слова: "dockerfile", "python", "оптимізувати"
- Співпадіння: Module 01 (docker, dockerfile)

**Вибрані модулі:**
- `modules/01_docker_containerization.md`

**Результат:** 1 module loaded

---

### Приклад 2: K8s + Monitoring
**Task:** "Deploy додаток в Kubernetes з Prometheus monitoring"

**Аналіз:**
- Ключові слова: "deploy", "kubernetes", "prometheus", "monitoring"
- Співпадіння:
  - Module 02 (kubernetes, deploy)
  - Module 05 (prometheus, monitoring)

**Вибрані модулі:**
- `modules/02_kubernetes_orchestration.md`
- `modules/05_monitoring_observability.md`

**Результат:** 2 modules loaded

---

### Приклад 3: Full CI/CD stack
**Task:** "Setup complete CI/CD: Docker build → K8s deploy → Security scan → Monitoring"

**Аналіз:**
- Ключові слова: "docker", "build", "kubernetes", "deploy", "security", "scan", "monitoring"
- Співпадіння:
  - Module 01 (docker, build)
  - Module 02 (kubernetes, deploy)
  - Module 03 (ci/cd, pipeline)
  - Module 05 (monitoring)

**Вибрані модулі:**
- `modules/01_docker_containerization.md`
- `modules/02_kubernetes_orchestration.md`
- `modules/03_cicd_pipelines.md`
- `modules/05_monitoring_observability.md`

**Результат:** 4 modules loaded

---

### Приклад 4: Infrastructure + Security
**Task:** "Terraform для AWS VPC + EKS + Security hardening"

**Аналіз:**
- Ключові слова: "terraform", "aws", "vpc", "eks", "security"
- Співпадіння:
  - Module 02 (kubernetes, eks)
  - Module 04 (terraform, aws, vpc, eks)
  - Module 06 (security)

**Вибрані модулі:**
- `modules/02_kubernetes_orchestration.md`
- `modules/04_infrastructure_as_code.md`
- `modules/06_security_best_practices.md`

**Результат:** 3 modules loaded

---

## 📊 Статистика завантаження

**За складністю задач:**
- Simple tasks (1 module): 75% token savings
- Medium tasks (2 modules): 55% token savings
- Complex tasks (3-4 modules): 30% token savings

**Середнє:** 2.3 modules per task (з 6 доступних)

**Частота завантаження модулів:**
- 🔴 01_docker: 70% of tasks
- 🔴 02_kubernetes: 65% of tasks
- 🟡 03_cicd: 55% of tasks
- 🟡 05_monitoring: 50% of tasks
- 🟢 04_infrastructure: 35% of tasks
- 🟢 06_security: 30% of tasks

---

**Version:** 1.0
**Date:** 2025-10-20
**Author:** Archon Implementation Engineer
**Status:** ✅ Ready for use
