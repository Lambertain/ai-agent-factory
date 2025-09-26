# Prisma Database Agent

**Универсальный агент для анализа и оптимизации баз данных с Prisma ORM**

Агент специализируется на проектировании схем, оптимизации запросов, управлении миграциями и анализе производительности для любых типов приложений. Полностью адаптируется под различные доменные области.

## 🎯 Основные возможности

### 🔍 Анализ и оптимизация схем
- **Универсальный анализ Prisma схем** для любых доменов
- **Оптимизация отношений** и нормализация данных
- **Индексирование** для максимальной производительности
- **Constraint validation** и data integrity

### 📊 Анализ производительности
- **Профилирование медленных запросов** с EXPLAIN планами
- **N+1 проблем detection** и решения
- **Connection pooling** оптимизация
- **Query optimization** для Prisma Client

### 🚀 Управление миграциями
- **Безопасное планирование миграций** с backward compatibility
- **Production-ready** стратегии развертывания
- **Rollback planning** для критических изменений
- **Zero-downtime** migration strategies

### 🎨 Доменная адаптация
Автоматически адаптируется под различные типы приложений:
- **E-commerce**: products, orders, customers, inventory
- **CRM**: contacts, deals, activities, pipelines
- **SaaS**: users, subscriptions, features, billing
- **Blog/CMS**: posts, authors, comments, media
- **Social**: users, posts, likes, follows
- **Custom**: любая доменная область

## 🚀 Быстрый старт

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Настройка переменных окружения

```bash
cp .env.example .env
```

Заполните обязательные переменные:
- `LLM_API_KEY` - API ключ для Qwen/Alibaba Cloud
- `GEMINI_API_KEY` - API ключ для Google Gemini

### Базовое использование

```python
from prisma_database_agent import run_prisma_analysis

# Анализ существующей схемы
result = await run_prisma_analysis(
    context="Optimize database schema for better performance",
    project_path="./my-project",
    analysis_type="performance"
)

print(result)
```

### Конфигурация под проект

```python
from prisma_database_agent.dependencies import PrismaDatabaseDependencies

# Настройка для E-commerce проекта
deps = PrismaDatabaseDependencies(
    project_name="MyStore",
    domain_type="e-commerce",
    analysis_mode="full",
    performance_threshold_ms=500.0,
    schema_config={
        "core_entities": ["Product", "Order", "Customer"],
        "critical_indexes": ["product_sku", "order_status"],
        "performance_focus": ["product_search", "order_processing"]
    }
)
```

## 🎨 Поддерживаемые домены

### E-commerce
```python
from examples.ecommerce_config import setup_ecommerce_agent

agent = setup_ecommerce_agent()
# Готов для анализа интернет-магазинов
```

### SaaS Platform
```python
from examples.saas_config import setup_saas_agent

agent = setup_saas_agent()
# Готов для анализа SaaS платформ
```

### CRM System
```python
from examples.crm_config import setup_crm_agent

agent = setup_crm_agent()
# Готов для анализа CRM систем
```

### Custom Domain
```python
deps = PrismaDatabaseDependencies(
    project_name="CustomApp",
    domain_type="custom",
    schema_config={
        "core_entities": ["YourEntity1", "YourEntity2"],
        "relations": ["YourEntity1-YourEntity2"],
        "indexes": ["your_critical_index"]
    }
)
```

## 🔧 Расширенная конфигурация

### Типы анализа

- **`full`** - Полный анализ схемы, запросов и производительности
- **`schema`** - Фокус на структуре и отношениях
- **`queries`** - Оптимизация запросов и производительности
- **`migrations`** - Планирование и валидация миграций
- **`performance`** - Глубокий анализ производительности

### Настройки производительности

```python
performance_config = {
    "performance_threshold_ms": 1000.0,  # Порог медленных запросов
    "target_query_performance": 300.0,   # Целевое время выполнения
    "max_connection_pool": 15,            # Размер пула соединений
    "enable_prepared_statements": True    # Подготовленные запросы
}
```

### RAG интеграция

Агент автоматически использует базу знаний для:
- Поиска best practices для Prisma
- Примеров оптимизации для PostgreSQL
- Доменных паттернов и архитектур
- Решения типичных проблем производительности

## 📊 Доступные инструменты

### `analyze_schema_performance`
Анализ структуры и производительности Prisma схемы.

```python
result = await analyze_schema_performance(
    ctx,
    schema_content="model User { ... }",
    focus_areas=["relations", "indexes"]
)
```

### `optimize_queries`
Оптимизация Prisma запросов и устранение N+1 проблем.

```python
result = await optimize_queries(
    ctx,
    queries=["prisma.user.findMany({ include: { posts: true } })"],
    optimization_level="aggressive"
)
```

### `create_migration_plan`
Планирование безопасных миграций схемы.

```python
result = await create_migration_plan(
    ctx,
    current_schema="...",
    target_schema="...",
    include_rollback=True
)
```

### `search_agent_knowledge`
Поиск в базе знаний агента через Archon RAG.

```python
result = await search_agent_knowledge(
    ctx,
    query="prisma transaction optimization patterns",
    match_count=5
)
```

## 🎯 Примеры использования

### Анализ E-commerce схемы

```python
from examples.ecommerce_config import example_ecommerce_analysis

analysis = example_ecommerce_analysis()
deps = analysis["dependencies"]

result = await run_prisma_analysis(
    context="Optimize e-commerce database for high traffic",
    project_path="./ecommerce-app",
    analysis_type="performance"
)
```

### SaaS Multi-tenant оптимизация

```python
from examples.saas_config import setup_saas_agent

deps = setup_saas_agent()
# Фокус на Row Level Security и tenant isolation

result = await run_prisma_analysis(
    context="Implement secure multi-tenancy with optimal performance",
    project_path="./saas-platform",
    analysis_type="schema"
)
```

### CRM Analytics оптимизация

```python
from examples.crm_config import setup_crm_agent

deps = setup_crm_agent()
# Фокус на sales analytics и reporting queries

result = await run_prisma_analysis(
    context="Optimize CRM for fast analytics and reporting",
    project_path="./crm-system",
    analysis_type="queries"
)
```

## 🛡️ Best Practices

### Схемы баз данных
- Используйте правильные типы данных для домена
- Применяйте индексы для часто запрашиваемых полей
- Планируйте отношения с учетом производительности
- Обеспечивайте data integrity через constraints

### Запросы и производительность
- Избегайте N+1 проблем с помощью include/select
- Используйте pagination для больших datasets
- Применяйте aggregate функции для аналитики
- Оптимизируйте connection pooling

### Миграции
- Всегда тестируйте миграции на копии production данных
- Планируйте rollback стратегии
- Используйте транзакции для критических изменений
- Мониторьте производительность после миграций

## 📋 Мультиагентные паттерны

Агент реализует 4 ключевых паттерна:

### 1. **Reflection (Рефлексия)**
- Критический анализ созданных схем
- Выявление проблем производительности
- Предложение улучшенных вариантов

### 2. **Tool Use (Использование инструментов)**
- Автоматический анализ схем и запросов
- RAG поиск в базе знаний Prisma
- Интеграция с PostgreSQL EXPLAIN

### 3. **Planning (Планирование)**
- Поэтапное планирование миграций
- Анализ влияния изменений
- Стратегии развертывания

### 4. **Multi-Agent Collaboration**
- Интеграция с TypeScript Agent для типов
- Сотрудничество с Frontend Agents
- Координация с DevOps агентами

## 🔗 Интеграции

### Archon RAG
Автоматический поиск в базе знаний для:
- Примеров оптимизации Prisma
- PostgreSQL best practices
- Доменных архитектурных паттернов

### TypeScript Integration
Синхронизация с TypeScript Agent для:
- Генерации типов из схемы
- Type-safe query builders
- Validation схем

### DevOps Integration
Координация с DevOps агентами для:
- CI/CD pipeline настройки
- Database deployment стратегий
- Monitoring и alerting

## 📚 Дополнительные ресурсы

- [Prisma Documentation](https://www.prisma.io/docs/)
- [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [Database Design Best Practices](https://www.prisma.io/dataguide/datamodeling)

---

**Prisma Database Agent** - универсальное решение для любых задач работы с базами данных! 🗄️✨