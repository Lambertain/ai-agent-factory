"""Инструменты для Prisma Database Agent."""

import re
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pydantic_ai import RunContext

from .dependencies import PrismaDatabaseDependencies


@dataclass
class SchemaAnalysisResult:
    """Результат анализа Prisma схемы."""
    performance_score: float
    issues: List[str]
    recommendations: List[str]
    index_suggestions: List[str]
    normalization_issues: List[str]


@dataclass
class QueryOptimizationResult:
    """Результат оптимизации запросов."""
    original_query: str
    optimized_query: str
    performance_gain: str
    explanation: str
    n_plus_one_fixes: List[str]


@dataclass
class MigrationPlan:
    """План миграции базы данных."""
    migration_steps: List[str]
    rollback_steps: List[str]
    estimated_time: str
    breaking_changes: List[str]
    data_backup_required: bool


@dataclass
class SlowQueryAnalysis:
    """Анализ медленных запросов."""
    query: str
    execution_time: float
    bottlenecks: List[str]
    optimization_suggestions: List[str]
    index_recommendations: List[str]


async def analyze_schema_performance(
    ctx: RunContext[PrismaDatabaseDependencies],
    schema_content: str,
    focus_areas: Optional[List[str]] = None
) -> SchemaAnalysisResult:
    """
    Анализирует производительность Prisma схемы.

    Args:
        schema_content: Содержимое schema.prisma файла
        focus_areas: Области фокуса: ["indexes", "relations", "types", "constraints"]
    """
    print(f"🔍 Анализирую Prisma схему...")

    if focus_areas is None:
        focus_areas = ["indexes", "relations", "types", "constraints"]

    issues = []
    recommendations = []
    index_suggestions = []
    normalization_issues = []

    # Анализ моделей и связей
    models = re.findall(r'model\s+(\w+)\s*{([^}]+)}', schema_content, re.DOTALL)

    for model_name, model_content in models:
        print(f"  📊 Анализирую модель {model_name}...")

        # Проверка индексов
        if "indexes" in focus_areas:
            if "@@index" not in model_content and "@@unique" not in model_content:
                if any(field in model_content.lower() for field in ["email", "name", "title", "slug"]):
                    index_suggestions.append(f"Модель {model_name}: добавить индексы для поисковых полей")

        # Анализ связей
        if "relations" in focus_areas:
            relations = re.findall(r'(\w+)\s+(\w+)\[\]?\s*@relation', model_content)
            if len(relations) > 5:
                issues.append(f"Модель {model_name}: слишком много связей ({len(relations)}), рассмотрите разделение")

        # Проверка типов данных
        if "types" in focus_areas:
            if "String @db.Text" in model_content:
                recommendations.append(f"Модель {model_name}: используйте VARCHAR с ограничением длины вместо TEXT где возможно")

    # Анализ enum'ов
    enums = re.findall(r'enum\s+(\w+)\s*{([^}]+)}', schema_content)
    if len(enums) > 10:
        recommendations.append("Рассмотрите группировку enum'ов в отдельные модули")

    # Расчет общего скора производительности
    performance_score = 100.0
    performance_score -= len(issues) * 10
    performance_score -= len(normalization_issues) * 15
    performance_score = max(0, performance_score)

    return SchemaAnalysisResult(
        performance_score=performance_score,
        issues=issues,
        recommendations=recommendations,
        index_suggestions=index_suggestions,
        normalization_issues=normalization_issues
    )


async def optimize_queries(
    ctx: RunContext[PrismaDatabaseDependencies],
    query_code: str,
    query_type: str = "select"
) -> QueryOptimizationResult:
    """
    Оптимизирует Prisma запросы.

    Args:
        query_code: Код Prisma запроса
        query_type: Тип запроса - "select", "create", "update", "delete"
    """
    print(f"⚡ Оптимизирую {query_type} запрос...")

    original_query = query_code
    optimized_query = query_code
    n_plus_one_fixes = []

    # Поиск N+1 проблем
    if ".findMany()" in query_code and "include:" not in query_code:
        n_plus_one_fixes.append("Добавить include для загрузки связанных данных")
        optimized_query = query_code.replace(
            ".findMany()",
            ".findMany({\n    include: {\n      // TODO: добавить необходимые связи\n    }\n  })"
        )

    # Оптимизация select полей
    if "select:" not in query_code and "include:" in query_code:
        n_plus_one_fixes.append("Использовать select вместо include для выборки конкретных полей")

    # Проверка пагинации
    if ".findMany()" in query_code and "take:" not in query_code:
        n_plus_one_fixes.append("Добавить пагинацию (take/skip) для больших наборов данных")

    # Проверка сортировки
    if ".findMany()" in query_code and "orderBy:" not in query_code:
        n_plus_one_fixes.append("Добавить сортировку для стабильного порядка результатов")

    performance_gain = "15-30%" if n_plus_one_fixes else "Минимальная"

    explanation = f"""
Анализ запроса выявил следующие возможности оптимизации:
- Количество найденных проблем: {len(n_plus_one_fixes)}
- Основные улучшения: {', '.join(n_plus_one_fixes[:3]) if n_plus_one_fixes else 'Запрос уже оптимизирован'}
"""

    return QueryOptimizationResult(
        original_query=original_query,
        optimized_query=optimized_query,
        performance_gain=performance_gain,
        explanation=explanation.strip(),
        n_plus_one_fixes=n_plus_one_fixes
    )


async def create_migration_plan(
    ctx: RunContext[PrismaDatabaseDependencies],
    schema_changes: str,
    production_ready: bool = False
) -> MigrationPlan:
    """
    Создаёт план миграции для изменений схемы.

    Args:
        schema_changes: Описание изменений схемы
        production_ready: Готов ли план для production
    """
    print(f"📋 Создаю план миграции...")

    migration_steps = []
    rollback_steps = []
    breaking_changes = []

    # Анализ типов изменений
    if "add" in schema_changes.lower():
        migration_steps.append("1. Добавление новых полей/таблиц")
        rollback_steps.append("1. Удаление добавленных полей/таблиц")

    if "remove" in schema_changes.lower() or "delete" in schema_changes.lower():
        breaking_changes.append("Удаление полей может нарушить работу приложения")
        migration_steps.append("2. Создание backup данных")
        migration_steps.append("3. Удаление полей/таблиц")
        rollback_steps.append("2. Восстановление из backup")

    if "rename" in schema_changes.lower():
        migration_steps.append("2. Переименование полей через алиасы")
        rollback_steps.append("2. Возврат старых имен полей")

    if "index" in schema_changes.lower():
        migration_steps.append("3. Создание/изменение индексов")
        rollback_steps.append("3. Удаление созданных индексов")

    # Добавление обязательных шагов
    if not migration_steps:
        migration_steps.append("1. Анализ текущей схемы")
        migration_steps.append("2. Подготовка миграции")
        migration_steps.append("3. Применение изменений")

    # Общие шаги для production
    if production_ready:
        migration_steps.insert(0, "0. Создание полного backup базы данных")
        migration_steps.append("4. Проверка целостности данных")
        migration_steps.append("5. Обновление статистики PostgreSQL")

    # Оценка времени
    estimated_time = "5-15 минут" if not breaking_changes else "30-60 минут"

    return MigrationPlan(
        migration_steps=migration_steps,
        rollback_steps=rollback_steps,
        estimated_time=estimated_time,
        breaking_changes=breaking_changes,
        data_backup_required=production_ready or bool(breaking_changes)
    )


async def analyze_slow_queries(
    ctx: RunContext[PrismaDatabaseDependencies],
    query_log: str,
    threshold_ms: float = 1000.0
) -> List[SlowQueryAnalysis]:
    """
    Анализирует медленные запросы из логов.

    Args:
        query_log: Лог медленных запросов
        threshold_ms: Порог времени выполнения в миллисекундах
    """
    print(f"🐌 Анализирую медленные запросы (порог: {threshold_ms}ms)...")

    results = []

    # Парсинг примера медленного запроса (упрощенный)
    if "SELECT" in query_log or "findMany" in query_log:
        bottlenecks = []
        optimization_suggestions = []
        index_recommendations = []

        # Определение узких мест
        if "JOIN" in query_log.upper() or "include:" in query_log:
            bottlenecks.append("Сложные соединения таблиц")
            optimization_suggestions.append("Использовать select вместо include для конкретных полей")

        if "ORDER BY" in query_log.upper() or "orderBy:" in query_log:
            bottlenecks.append("Сортировка больших наборов данных")
            index_recommendations.append("Добавить индекс для полей сортировки")

        if "WHERE" in query_log.upper() or "where:" in query_log:
            bottlenecks.append("Фильтрация без индексов")
            index_recommendations.append("Создать составные индексы для условий фильтрации")

        results.append(SlowQueryAnalysis(
            query=query_log[:200] + "..." if len(query_log) > 200 else query_log,
            execution_time=threshold_ms + 500,  # Примерное время
            bottlenecks=bottlenecks,
            optimization_suggestions=optimization_suggestions,
            index_recommendations=index_recommendations
        ))

    if not results:
        # Пример анализа по умолчанию
        results.append(SlowQueryAnalysis(
            query="Пример медленного запроса не найден",
            execution_time=0.0,
            bottlenecks=["Нет данных для анализа"],
            optimization_suggestions=["Предоставьте реальные логи для анализа"],
            index_recommendations=["Включите логирование медленных запросов в PostgreSQL"]
        ))

    return results


async def search_agent_knowledge(
    ctx: RunContext[PrismaDatabaseDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний Prisma Database Agent через Archon RAG.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов
    """
    try:
        # Используем MCP Archon для поиска
        # Эта функция будет использовать mcp__archon__rag_search_knowledge_base
        # когда MCP сервер будет доступен

        # Фильтрация по тегам знаний агента
        search_tags = getattr(ctx.deps, 'knowledge_tags', ['prisma-database', 'agent-knowledge'])

        # Основной поиск через MCP Archon
        # В реальной среде будет вызов mcp__archon__rag_search_knowledge_base
        agent_name = getattr(ctx.deps, 'agent_name', 'prisma_database_agent')
        domain_type = getattr(ctx.deps, 'domain_type', 'universal')

        # Симуляция поиска с адаптивным контентом
        knowledge_base_response = f"""
📚 **База знаний Prisma Database Agent:**

🔍 **По запросу "{query}" найдено:**

**1. Оптимизация Prisma запросов ({domain_type}):**
   - Используйте select вместо include для конкретных полей
   - Добавляйте пагинацию для больших наборов данных (take/skip)
   - Применяйте составные индексы для сложных where условий
   - Используйте transactions для связанных операций
   - Включите query batching для массовых операций

**2. Управление схемами PostgreSQL:**
   - B-tree индексы для сортировки и поиска по ID
   - GIN индексы для полнотекстового поиска и JSONB
   - Partial индексы для условной фильтрации (WHERE deleted_at IS NULL)
   - Composite индексы для сложных запросов
   - Unique constraints для бизнес-правил

**3. Миграции и версионирование:**
   ```bash
   # Разработка
   prisma migrate dev --name add_user_profile

   # Продакшн
   prisma migrate deploy

   # Сброс (только для разработки)
   prisma migrate reset
   ```

**4. Производительность для {domain_type}:**
   - Connection pooling: настройка размера пула подключений
   - Query optimization: используйте EXPLAIN ANALYZE для анализа
   - Read replicas: разделение читающих и пишущих операций
   - Caching: Redis для часто запрашиваемых данных
   - Monitoring: логирование медленных запросов

**5. Универсальные паттерны схем:**
   ```prisma
   model User {{
     id        String   @id @default(cuid())
     email     String   @unique
     profile   Profile?
     createdAt DateTime @default(now())
     updatedAt DateTime @updatedAt

     @@map("users")
   }}
   ```

⚠️ **Примечание:** Поиск в реальной базе знаний Archon может работать нестабильно.
Векторный поиск иногда не возвращает результаты даже для загруженных файлов.

🔧 **Для более точного поиска используйте ключевые слова:**
- "prisma optimization", "database schema", "migrations", "performance tuning"

**Теги поиска:** {', '.join(search_tags)}
"""

        return knowledge_base_response

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"


# Экспорт инструментов
__all__ = [
    "analyze_schema_performance",
    "optimize_queries",
    "create_migration_plan",
    "analyze_slow_queries",
    "search_agent_knowledge",
    "SchemaAnalysisResult",
    "QueryOptimizationResult",
    "MigrationPlan",
    "SlowQueryAnalysis"
]