# Archon Blueprint Architect - Module Selection Logic

## 🎯 Коли читати цей файл:

**ЗАВЖДИ після прочитання системного промпту та задачі з Archon MCP.**

Цей файл містить логіку вибору модулів для контекстно-залежного читання.

## 📊 MODULE OVERVIEW

| # | Module | Priority | Lines | Domain | Load When |
|---|--------|----------|-------|--------|-----------|
| **01** | [SOLID & Clean Architecture](modules/01_solid_clean_architecture.md) | 🔴 CRITICAL | ~350 | Architecture Principles | Agent development, DDD, SOLID |
| **02** | [Microservices Patterns](modules/02_microservices_patterns.md) | 🟡 HIGH | ~305 | Distributed Systems | Microservices, Service Discovery |
| **03** | [Event-Driven & CQRS](modules/03_event_driven_cqrs.md) | 🟡 HIGH | ~513 | Event Architecture | Event Sourcing, CQRS, Message Bus |
| **04** | [Cloud & Serverless](modules/04_cloud_serverless_architecture.md) | 🟢 MEDIUM | ~355 | Cloud Architecture | Serverless, IaC, Kubernetes |
| **05** | [AI Agent Architecture](modules/05_ai_agent_architecture.md) | 🔴 CRITICAL | ~770 | AI Agent Design | AI agent development |

**Общее количество строк в модулях:** ~2,293 строк

**Стратегия чтения:** 2-3 модуля на задачу (~900-1,400 токенов)

## 📦 Module 01: SOLID Principles & Clean Architecture

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- Создание любых AI агентов
- Проектирование систем с чистой архитектурой
- Рефакторинг монолита на DDD
- Разделение на Domain/Application/Infrastructure слои
- Внедрение Dependency Injection

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* чистый код, SOLID принципы, чистая архитектура, dependency injection, разделение ответственностей, DDD, слои архитектуры, доменная модель, repository pattern, domain service, application service

*English:* clean code, SOLID principles, clean architecture, dependency injection, separation of concerns, DDD, layered architecture, domain model, repository pattern, domain service, application service

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Domain-Driven Design (Entity, Value Object, Aggregate Root, Domain Event)
- Clean Architecture Layers (Domain, Application, Infrastructure, Interface)
- SOLID Principles (SRP, OCP, LSP, ISP, DIP)
- Repository Pattern, Unit of Work, Specification Pattern
- Dependency Injection (IoC Container, Constructor Injection)

**Примеры задач:**
- "Создать AI агента с clean architecture"
- "Спроектировать систему с DDD"
- "Разделить код на domain/application/infrastructure слои"
- "Реализовать repository pattern для агента"
- "Применить SOLID принципы к архитектуре"

## 📦 Module 02: Microservices Architecture Patterns

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- Декомпозиция монолита на микросервисы
- Проектирование распределенных систем
- Повышение resilience и fault tolerance
- Внедрение Service Discovery и Load Balancing
- Saga pattern для распределенных транзакций

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* микросервисы, service discovery, load balancer, circuit breaker, API gateway, распределенная система, saga pattern, resilience, отказоустойчивость, балансировка нагрузки, service mesh

*English:* microservices, service discovery, load balancer, circuit breaker, API gateway, distributed system, saga pattern, resilience, fault tolerance, load balancing, service mesh

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Service Discovery & Registry (Consul, Eureka, etcd, ZooKeeper)
- Load Balancing (Round Robin, Least Connections, Sticky Sessions)
- Resilience Patterns (Circuit Breaker, Retry, Bulkhead, Rate Limiting)
- API Gateway (Request Routing, Authentication, Rate Limiting)
- Distributed Transactions (Saga Pattern, Two-Phase Commit)
- Communication (REST, gRPC, GraphQL, Message Queue)
- Observability (Distributed Tracing, Centralized Logging, Metrics)

**Примеры задач:**
- "Спроектировать микросервисную архитектуру"
- "Реализовать service discovery для агентов"
- "Добавить circuit breaker для resilience"
- "Создать API gateway для агентов"
- "Внедрить saga pattern для распределенных транзакций"

## 📦 Module 03: Event-Driven Architecture & CQRS

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- Системы с audit trail требованиями
- High-throughput приложения
- Eventual consistency архитектуры
- Event-driven системы интеграции
- Системы с разделением чтения/записи

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* event sourcing, CQRS, событийная архитектура, aggregate root, event store, message bus, eventual consistency, проекция, event handler, command handler, query handler

*English:* event sourcing, CQRS, event-driven architecture, aggregate root, event store, message bus, eventual consistency, projection, event handler, command handler, query handler

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Event Sourcing (Event Store, Event Stream, Event Replay, Snapshot)
- CQRS (Command Handler, Query Handler, Write Model, Read Model)
- Event Handlers & Projections (Read Model Projection, Catch-up Subscription)
- Message Bus (RabbitMQ, Kafka, AWS SNS/SQS, Publish-Subscribe)
- Eventual Consistency (Asynchronous Processing, Compensating Actions, Outbox Pattern)

**Примеры задач:**
- "Реализовать event sourcing для агента"
- "Создать CQRS архитектуру"
- "Разделить чтение и запись в разные модели"
- "Внедрить event store для audit trail"
- "Создать event-driven интеграцию между агентами"

## 📦 Module 04: Cloud & Serverless Architecture

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Cloud-native приложения
- Auto-scaling архитектуры
- Pay-per-use модели
- Event-driven serverless workflows
- Миграция в облако
- Контейнеризация приложений

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* облачная архитектура, serverless, lambda, multi-cloud, IaC, terraform, контейнеризация, kubernetes, автоскейлинг, docker, helm, AWS, GCP, Azure

*English:* cloud architecture, serverless, lambda, multi-cloud, IaC, terraform, containerization, kubernetes, auto-scaling, docker, helm, AWS, GCP, Azure

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Serverless Computing (AWS Lambda, Google Cloud Functions, Azure Functions)
- Infrastructure as Code (Terraform, CloudFormation, Pulumi, AWS CDK)
- Container Orchestration (Kubernetes, Docker Swarm, Helm, Istio)
- Cloud Services (S3, DynamoDB, RDS, ElastiCache, CloudFront)
- Auto-scaling & Elasticity (HPA, VPA, KEDA, Auto Scaling Groups)
- Multi-Cloud & Hybrid (Multi-cloud deployment, Cloud migration patterns)

**Примеры задач:**
- "Создать serverless функцию для агента"
- "Настроить auto-scaling для high load"
- "Написать Terraform конфигурацию"
- "Спроектировать multi-cloud архитектуру"
- "Контейнеризировать агента с Docker"

## 📦 Module 05: AI Agent Architecture Design

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- Создание новых AI агентов
- Проектирование Pydantic AI агентов
- Архитектура agent.py / tools.py / prompts.py
- Интеграция MCP серверов
- Разработка инструментов (tools) для агентов
- Тестирование AI агентов

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* AI агент, Pydantic AI, agent architecture, tools интеграция, промпт инжиниринг, модульный агент, dependency injection, system prompt, testing, MCP server

*English:* AI agent, Pydantic AI, agent architecture, tools integration, prompt engineering, modular agent, dependency injection, system prompt, testing, MCP server

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Pydantic AI Core (Agent class, RunContext, ModelRetry, result_type, deps_type)
- Agent File Structure (agent.py, tools.py, prompts.py, dependencies.py, settings.py)
- Tool Design (@agent.tool decorator, Tool composition, Async implementation)
- Dependency Injection (BaseModel container, Dependency lifecycle, Shared resources)
- Structured Outputs (Pydantic BaseModel, Field validation, Type hints)
- Prompt Engineering (system_prompt, Dynamic prompts, Prompt templates)
- Testing Patterns (pytest, AsyncMock, Tool unit tests, Integration tests)
- MCP Integration (MCP server connection, Context passing)

**Примеры задач:**
- "Создать новый AI агент с Pydantic AI"
- "Реализовать tool функцию для агента"
- "Написать system prompt для роли"
- "Настроить dependency injection контейнер"
- "Интегрировать MCP server в агента"
- "Написать тесты для AI агента"

---

## 🎯 PRIORITY CASCADE (как часто читается каждый модуль)

### 🔴 CRITICAL Priority (читаются 70-80% задач)
- **Module 01:** SOLID & Clean Architecture - база для всех агентов
- **Module 05:** AI Agent Architecture - специфика Pydantic AI

### 🟡 HIGH Priority (читаются 50-60% задач)
- **Module 02:** Microservices Patterns - распределенные системы
- **Module 03:** Event-Driven & CQRS - асинхронные архитектуры

### 🟢 MEDIUM Priority (читаются 30-40% задач)
- **Module 04:** Cloud & Serverless - cloud-native решения

---

## 📝 ПРИМЕРЫ КОМБИНАЦИЙ МОДУЛЕЙ ДЛЯ ТИПОВЫХ ЗАДАЧ

### Задача: "Создать AI агента с чистой архитектурой"
**Читать:**
- ✅ Module 01 (SOLID & Clean Architecture) - CRITICAL
- ✅ Module 05 (AI Agent Architecture) - CRITICAL

**Токены:** ~1,120 (350 + 770)

### Задача: "Спроектировать микросервисную систему агентов"
**Читать:**
- ✅ Module 01 (SOLID & Clean Architecture) - CRITICAL
- ✅ Module 02 (Microservices Patterns) - HIGH
- ✅ Module 05 (AI Agent Architecture) - CRITICAL

**Токены:** ~1,425 (350 + 305 + 770)

### Задача: "Создать event-driven архитектуру для агентов"
**Читать:**
- ✅ Module 01 (SOLID & Clean Architecture) - CRITICAL
- ✅ Module 03 (Event-Driven & CQRS) - HIGH
- ✅ Module 05 (AI Agent Architecture) - CRITICAL

**Токены:** ~1,633 (350 + 513 + 770)

### Задача: "Развернуть агента в serverless среде"
**Читать:**
- ✅ Module 04 (Cloud & Serverless) - MEDIUM
- ✅ Module 05 (AI Agent Architecture) - CRITICAL

**Токены:** ~1,125 (355 + 770)

---

## 🔍 KEYWORD-BASED MODULE SELECTION FUNCTION

```python
def select_modules_for_task(task_description: str) -> list[str]:
    """
    Выбрать модули для чтения на основе описания задачи.

    Args:
        task_description: Описание задачи от пользователя или из Archon

    Returns:
        list[str]: Список путей к модулям для чтения
    """
    task_lower = task_description.lower()
    modules = []

    # Module 01: SOLID & Clean Architecture (CRITICAL - читается почти всегда для агентов)
    if any(keyword in task_lower for keyword in [
        "агент", "agent", "архитектура", "architecture", "solid", "ddd",
        "clean", "чистая", "repository", "domain", "слои", "layers"
    ]):
        modules.append("modules/01_solid_clean_architecture.md")

    # Module 02: Microservices Patterns (HIGH)
    if any(keyword in task_lower for keyword in [
        "микросервис", "microservice", "service discovery", "load balancer",
        "circuit breaker", "api gateway", "saga", "resilience", "распределенн"
    ]):
        modules.append("modules/02_microservices_patterns.md")

    # Module 03: Event-Driven & CQRS (HIGH)
    if any(keyword in task_lower for keyword in [
        "event", "событ", "cqrs", "event sourcing", "aggregate", "projection",
        "message bus", "kafka", "rabbitmq", "eventual consistency"
    ]):
        modules.append("modules/03_event_driven_cqrs.md")

    # Module 04: Cloud & Serverless (MEDIUM)
    if any(keyword in task_lower for keyword in [
        "serverless", "lambda", "cloud", "облак", "terraform", "kubernetes",
        "docker", "k8s", "aws", "gcp", "azure", "iac", "helm"
    ]):
        modules.append("modules/04_cloud_serverless_architecture.md")

    # Module 05: AI Agent Architecture (CRITICAL - читается всегда для AI задач)
    if any(keyword in task_lower for keyword in [
        "ai агент", "ai agent", "pydantic ai", "tool", "инструмент", "prompt",
        "промпт", "mcp", "testing", "тестирование", "agent.py", "tools.py"
    ]):
        modules.append("modules/05_ai_agent_architecture.md")

    # FALLBACK: если ключевых слов не найдено, читать CRITICAL модули
    if not modules:
        modules = [
            "modules/01_solid_clean_architecture.md",  # CRITICAL
            "modules/05_ai_agent_architecture.md"      # CRITICAL
        ]

    return modules
```

---

## 📊 МЕТРИКИ ОПТИМИЗАЦИИ ТОКЕНОВ (OLD vs NEW)

### OLD Workflow (читать ВСЕ модули):
- Модулей: 5
- Строк: ~2,293
- Токенов: ~3,400-3,600

### NEW Workflow (контекстное чтение):
- Модулей за задачу: 2-3
- Строк за задачу: ~900-1,400
- Токенов за задачу: ~1,350-2,100

### Экономия токенов:
- **Минимум:** 38% (3,600 → 2,100)
- **Максимум:** 63% (3,600 → 1,350)
- **Среднее:** 57% (3,600 → 1,550)

---

**Версия:** 1.0
**Дата создания:** 2025-10-20
**Автор:** Archon Implementation Engineer
**Проект:** AI Agent Factory - Blueprint Architect Refactoring (NEW workflow)

**Изменения:**
- ✅ Создана модульная навигация с приоритетами (CRITICAL/HIGH/MEDIUM)
- ✅ Добавлены Russian + English keywords для каждого модуля
- ✅ Добавлены технические триггеры для точного выбора
- ✅ Примеры типовых задач и комбинаций модулей
- ✅ Функция select_modules_for_task() с keyword mapping
- ✅ Метрики оптимизации токенов (OLD vs NEW)
