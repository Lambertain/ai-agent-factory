# Archon Implementation Engineer - Module Selection Logic

**Версия:** 1.0
**Дата:** 2025-10-20
**Автор:** Archon Implementation Engineer

---

## 📊 MODULE OVERVIEW

| # | Module | Priority | Lines | Domain | Load When |
|---|--------|----------|-------|--------|-----------|
| **01** | [Clean Architecture](modules/01_clean_architecture_design_patterns.md) | 🔴 CRITICAL | ~440 | Architecture & Patterns | Agent development, SOLID |
| **02** | [Performance](modules/02_performance_optimization.md) | 🔴 CRITICAL | ~530 | Optimization | High load, async, caching |
| **03** | [Database](modules/03_database_optimization.md) | 🟡 HIGH | ~590 | Data Layer | DB operations, vector search |
| **04** | [Testing](modules/04_testing_quality_assurance.md) | 🟡 HIGH | ~500 | Quality | Production code, testing |
| **05** | [Deployment](modules/05_deployment_devops.md) | 🟢 MEDIUM | ~650 | DevOps | Production deployment |
| **06** | [Monitoring](modules/06_monitoring_observability.md) | 🟢 MEDIUM | ~695 | Observability | Production monitoring |

**Total Knowledge:** ~3,400 lines in modules + ~500 tokens system prompt + ~1,500 common rules

**Priority Legend:**
- 🔴 **CRITICAL** - Load frequency: 70-80% of tasks
- 🟡 **HIGH** - Load frequency: 50-60% of tasks
- 🟢 **MEDIUM** - Load frequency: 30-40% of tasks

---

## 📦 Module 01: Clean Architecture & Design Patterns

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- Разработка AI агентов с бизнес-логикой
- Требуется высокая тестируемость
- Долгосрочная maintainability критична
- Реализация сложной бизнес-логики

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* чистая архитектура, SOLID, repository pattern, dependency injection, слои приложения, domain layer, бизнес-логика

*English:* clean architecture, SOLID, repository pattern, dependency injection, application layers, domain layer, business logic

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Создание Domain/Application/Infrastructure layers
- Реализация Repository Pattern с Generic типами
- Настройка Dependency Injection Container
- SOLID principles для AI agents
- Разделение concerns

**Примеры задач:**
- "Создать AI агента с clean architecture"
- "Реализовать repository pattern для данных"
- "Применить SOLID principles к коду"

---

## 📦 Module 02: Performance Optimization

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- Высокие нагрузки и масштабирование
- Оптимизация response time
- Работа с внешними API (rate limiting)
- Async/await patterns
- Caching strategies

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* производительность, async, батчинг, кэширование, connection pool, rate limiting, оптимизация

*English:* performance, async, batching, caching, connection pool, rate limiting, optimization

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Async/await patterns для parallel API calls
- Batching strategies для минимизации overhead
- Multi-level caching (Memory → Redis → DB)
- Token Bucket алгоритм для rate limiting
- Connection pooling

**Примеры задач:**
- "Оптимизировать производительность API"
- "Реализовать кэширование для агента"
- "Добавить async обработку запросов"

---

## 📦 Module 03: Database Optimization

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- Большие объемы данных
- Vector databases и similarity search
- Оптимизация медленных запросов
- Bulk operations
- Index optimization

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* база данных, индексы, vector search, FAISS, N+1 проблема, bulk операции, PostgreSQL

*English:* database, indexes, vector search, FAISS, N+1 problem, bulk operations, PostgreSQL

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- COPY для bulk inserts в PostgreSQL
- GIN/BRIN/Covering indexes
- FAISS IndexIVFFlat/HNSW для vector search
- N+1 query problem solutions
- Query optimization

**Примеры задач:**
- "Оптимизировать запросы к базе данных"
- "Реализовать vector search для RAG"
- "Исправить N+1 проблему"

---

## 📦 Module 04: Testing & Quality Assurance

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- Разработка production кода
- Обеспечение надежности агентов
- Performance regression testing
- Test coverage requirements

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* тестирование, pytest, TestModel, integration tests, performance tests, покрытие кода

*English:* testing, pytest, TestModel, integration tests, performance tests, code coverage

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- TestModel vs Real Model для unit/integration тестов
- Performance testing (concurrent requests, percentiles)
- Error recovery и retry logic testing
- 80%+ код coverage requirement

**Примеры задач:**
- "Написать unit тесты для агента"
- "Добавить integration тесты"
- "Проверить код coverage"

---

## 📦 Module 05: Deployment & DevOps

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Production deployment подготовка
- Настройка CI/CD pipeline
- Автомасштабирование и zero downtime
- Docker containerization

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* deployment, docker, kubernetes, ci/cd, github actions, автомасштабирование

*English:* deployment, docker, kubernetes, ci/cd, github actions, autoscaling

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Multi-stage Docker builds
- Kubernetes HPA (Horizontal Pod Autoscaler)
- GitHub Actions workflow для тестирования и deploy
- Rolling updates для zero downtime

**Примеры задач:**
- "Создать Dockerfile для агента"
- "Настроить CI/CD pipeline"
- "Развернуть в Kubernetes"

---

## 📦 Module 06: Monitoring & Observability

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Production окружение (всегда)
- Debugging performance issues
- Distributed tracing необходим
- Health checks setup

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* мониторинг, prometheus, логи, health check, трейсинг, алерты, SLO

*English:* monitoring, prometheus, logs, health check, tracing, alerts, SLO

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Prometheus metrics (RED method: Rate/Errors/Duration)
- Structured logging с structlog
- Health check system с timeout
- OpenTelemetry distributed tracing

**Примеры задач:**
- "Добавить мониторинг для агента"
- "Настроить health checks"
- "Реализовать structured logging"

---

## 🎯 USAGE EXAMPLES

### Example 1: Agent Development Task
**Task:** "Создать Payment Integration Agent с clean architecture"

**Modules to load:**
1. Module 01 (Clean Architecture) - 🔴 CRITICAL match
2. Module 04 (Testing) - 🟡 HIGH (production code)

**Total:** ~940 lines (~2,500 tokens)

---

### Example 2: Performance Optimization Task
**Task:** "Оптимизировать производительность API агента"

**Modules to load:**
1. Module 02 (Performance) - 🔴 CRITICAL match
2. Module 03 (Database) - 🟡 HIGH (likely DB queries involved)

**Total:** ~1,120 lines (~3,000 tokens)

---

### Example 3: Production Deployment Task
**Task:** "Развернуть агента в production с мониторингом"

**Modules to load:**
1. Module 05 (Deployment) - 🟢 MEDIUM match
2. Module 06 (Monitoring) - 🟢 MEDIUM match

**Total:** ~1,345 lines (~3,500 tokens)

---

## 📈 TOKEN OPTIMIZATION

**OLD Approach (reading ALL modules):**
- System prompt: ~500 tokens
- ALL 6 modules: ~3,400 lines (~9,000 tokens)
- **Total:** ~9,500 tokens per task

**NEW Approach (context-dependent):**
- System prompt: ~500 tokens
- Common rules: ~1,500 tokens
- 2-3 relevant modules: ~1,200-1,800 tokens
- **Total:** ~3,200-3,800 tokens per task

**Savings:** ~60-66% token reduction (9,500 → 3,200-3,800)

---

**Navigation:**
- [System Prompt](archon_implementation_engineer_system_prompt.md)
- [Common Agent Rules](../common_agent_rules.md)
- [Module 01: Clean Architecture](modules/01_clean_architecture_design_patterns.md)
- [Module 02: Performance](modules/02_performance_optimization.md)
- [Module 03: Database](modules/03_database_optimization.md)
- [Module 04: Testing](modules/04_testing_quality_assurance.md)
- [Module 05: Deployment](modules/05_deployment_devops.md)
- [Module 06: Monitoring](modules/06_monitoring_observability.md)
