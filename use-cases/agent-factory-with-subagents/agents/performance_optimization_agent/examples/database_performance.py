"""
Database Performance конфигурация для Performance Optimization Agent.

Этот файл демонстрирует настройку агента для оптимизации производительности баз данных.
Включает query optimization, indexing strategies, connection pooling и monitoring.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from ..dependencies import PerformanceOptimizationDependencies


@dataclass
class DatabasePerformanceDependencies(PerformanceOptimizationDependencies):
    """Конфигурация для Database Performance Optimization."""

    # Основные настройки
    domain_type: str = "database"
    project_type: str = "postgresql"

    # Query optimization
    enable_query_optimization: bool = True
    enable_query_caching: bool = True
    enable_prepared_statements: bool = True
    slow_query_threshold_ms: int = 1000

    # Indexing strategies
    enable_auto_indexing: bool = True
    enable_index_monitoring: bool = True
    enable_partial_indexes: bool = True
    enable_covering_indexes: bool = True

    # Connection management
    enable_connection_pooling: bool = True
    min_pool_size: int = 5
    max_pool_size: int = 20
    connection_timeout: int = 30
    idle_timeout: int = 600

    # Performance targets
    target_query_time_ms: int = 100
    target_connection_usage: float = 0.8
    target_cache_hit_ratio: float = 0.95
    target_lock_wait_time_ms: int = 50

    def get_postgresql_config(self) -> Dict[str, Any]:
        """Конфигурация PostgreSQL optimization."""
        return {
            "postgresql_conf": {
                # Memory settings
                "shared_buffers": "256MB",
                "effective_cache_size": "1GB",
                "work_mem": "4MB",
                "maintenance_work_mem": "64MB",

                # Query planner
                "random_page_cost": 1.1,
                "effective_io_concurrency": 200,
                "default_statistics_target": 100,

                # Write-ahead logging
                "wal_buffers": "16MB",
                "checkpoint_completion_target": 0.7,
                "wal_writer_delay": "200ms",

                # Connection settings
                "max_connections": 200,
                "shared_preload_libraries": "pg_stat_statements",

                # Logging
                "log_min_duration_statement": self.slow_query_threshold_ms,
                "log_checkpoints": "on",
                "log_connections": "on",
                "log_disconnections": "on",
                "log_lock_waits": "on"
            },
            "extensions": [
                "pg_stat_statements",
                "pg_buffercache",
                "pg_stat_activity",
                "btree_gin",
                "btree_gist"
            ]
        }

    def get_query_optimization_config(self) -> Dict[str, Any]:
        """Конфигурация query optimization."""
        return {
            "analysis_tools": {
                "explain_analyze": True,
                "auto_explain": {
                    "enabled": True,
                    "log_min_duration": self.slow_query_threshold_ms,
                    "log_analyze": True,
                    "log_buffers": True,
                    "log_timing": True,
                    "log_verbose": True
                }
            },
            "optimization_strategies": {
                "query_rewriting": True,
                "subquery_to_join": True,
                "index_hints": True,
                "materialized_views": True,
                "partition_pruning": True
            },
            "caching": {
                "query_result_cache": {
                    "enabled": self.enable_query_caching,
                    "max_size": "128MB",
                    "ttl": 3600
                },
                "prepared_statement_cache": {
                    "enabled": self.enable_prepared_statements,
                    "max_statements": 1000
                }
            }
        }

    def get_indexing_strategy(self) -> Dict[str, Any]:
        """Стратегии индексирования."""
        return {
            "auto_indexing": {
                "enabled": self.enable_auto_indexing,
                "analyze_frequency": "daily",
                "unused_index_detection": True,
                "duplicate_index_detection": True
            },
            "index_types": {
                "btree": {
                    "use_cases": ["equality", "range", "ordering"],
                    "maintenance": "automatic"
                },
                "gin": {
                    "use_cases": ["full_text", "jsonb", "arrays"],
                    "maintenance": "low"
                },
                "gist": {
                    "use_cases": ["spatial", "ranges", "full_text"],
                    "maintenance": "medium"
                },
                "hash": {
                    "use_cases": ["equality_only"],
                    "maintenance": "automatic"
                }
            },
            "partial_indexes": {
                "enabled": self.enable_partial_indexes,
                "strategies": [
                    "WHERE status = 'active'",
                    "WHERE deleted_at IS NULL",
                    "WHERE created_at > NOW() - INTERVAL '1 year'"
                ]
            },
            "covering_indexes": {
                "enabled": self.enable_covering_indexes,
                "include_columns": True,
                "analyze_queries": True
            }
        }

    def get_connection_pooling_config(self) -> Dict[str, Any]:
        """Конфигурация connection pooling."""
        return {
            "pgbouncer": {
                "pool_mode": "transaction",
                "max_client_conn": 100,
                "default_pool_size": self.max_pool_size,
                "min_pool_size": self.min_pool_size,
                "reserve_pool_size": 3,
                "server_round_robin": 1,
                "server_idle_timeout": self.idle_timeout,
                "server_connect_timeout": self.connection_timeout
            },
            "application_pool": {
                "framework": "asyncpg",
                "min_size": self.min_pool_size,
                "max_size": self.max_pool_size,
                "max_queries": 50000,
                "max_inactive_connection_lifetime": 300,
                "setup_hooks": ["SET timezone = 'UTC'"]
            }
        }

    def get_monitoring_config(self) -> Dict[str, Any]:
        """Конфигурация database monitoring."""
        return {
            "performance_metrics": {
                "query_performance": {
                    "slow_queries": True,
                    "most_time_consuming": True,
                    "most_frequent": True,
                    "index_usage": True
                },
                "connection_stats": {
                    "active_connections": True,
                    "idle_connections": True,
                    "waiting_connections": True,
                    "pool_utilization": True
                },
                "cache_performance": {
                    "buffer_cache_hit_ratio": True,
                    "query_cache_hit_ratio": True,
                    "index_cache_hit_ratio": True
                }
            },
            "alerting": {
                "slow_query_threshold": f">{self.target_query_time_ms}ms",
                "connection_pool_usage": f">{self.target_connection_usage * 100}%",
                "cache_hit_ratio": f"<{self.target_cache_hit_ratio * 100}%",
                "lock_wait_time": f">{self.target_lock_wait_time_ms}ms",
                "deadlock_detection": True
            },
            "automated_maintenance": {
                "vacuum_analyze": {
                    "enabled": True,
                    "schedule": "0 2 * * *",  # Daily at 2 AM
                    "aggressive_threshold": 0.2
                },
                "reindex": {
                    "enabled": True,
                    "schedule": "0 3 * * 0",  # Weekly on Sunday at 3 AM
                    "bloat_threshold": 0.3
                },
                "statistics_update": {
                    "enabled": True,
                    "schedule": "0 1 * * *",  # Daily at 1 AM
                    "auto_analyze": True
                }
            }
        }

    def get_backup_performance_config(self) -> Dict[str, Any]:
        """Конфигурация backup performance."""
        return {
            "continuous_archiving": {
                "enabled": True,
                "wal_archive_timeout": "60s",
                "archive_compression": "gzip",
                "max_wal_senders": 3
            },
            "backup_strategies": {
                "hot_backup": {
                    "method": "pg_basebackup",
                    "compression": True,
                    "parallel_jobs": 4,
                    "exclude_tables": ["temp_*", "log_*"]
                },
                "logical_backup": {
                    "method": "pg_dump",
                    "custom_format": True,
                    "parallel_jobs": 2,
                    "exclude_schemas": ["information_schema"]
                }
            },
            "restore_optimization": {
                "parallel_restore": True,
                "disable_triggers": True,
                "increase_maintenance_work_mem": "1GB",
                "checkpoint_segments": 64
            }
        }


# Пример использования
def get_database_performance_dependencies() -> DatabasePerformanceDependencies:
    """Создать конфигурацию для Database Performance Optimization."""
    return DatabasePerformanceDependencies(
        api_key="your-api-key",
        domain_type="database",
        project_type="postgresql",
        enable_query_optimization=True,
        enable_auto_indexing=True,
        enable_connection_pooling=True,
        target_query_time_ms=100
    )


# Примеры SQL оптимизации
DATABASE_PERFORMANCE_EXAMPLES = {
    "query_optimization": """
-- Оптимизация медленных запросов PostgreSQL

-- 1. АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ
-- Включить pg_stat_statements для сбора статистики
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Найти самые медленные запросы
SELECT
    query,
    calls,
    total_time,
    mean_time,
    stddev_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- 2. ОПТИМИЗАЦИЯ ИНДЕКСОВ
-- Найти неиспользуемые индексы
SELECT
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_tup_read = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Создание составного индекса с включенными колонками
CREATE INDEX CONCURRENTLY idx_orders_user_status_include
ON orders (user_id, status)
INCLUDE (created_at, total_amount);

-- Частичный индекс для активных записей
CREATE INDEX CONCURRENTLY idx_users_active
ON users (email)
WHERE status = 'active' AND deleted_at IS NULL;

-- 3. МАТЕРИАЛИЗОВАННЫЕ ПРЕДСТАВЛЕНИЯ
-- Для агрегированных данных
CREATE MATERIALIZED VIEW sales_summary AS
SELECT
    DATE_TRUNC('day', created_at) as date,
    COUNT(*) as orders_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value
FROM orders
WHERE status = 'completed'
GROUP BY DATE_TRUNC('day', created_at);

-- Автоматическое обновление через триггер
CREATE OR REPLACE FUNCTION refresh_sales_summary()
RETURNS trigger AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY sales_summary;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- 4. ПАРТИЦИОНИРОВАНИЕ ТАБЛИЦ
-- Партиционирование по дате
CREATE TABLE orders_partitioned (
    id SERIAL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    total_amount DECIMAL(10,2),
    status VARCHAR(20)
) PARTITION BY RANGE (created_at);

-- Создание партиций
CREATE TABLE orders_2024_q1 PARTITION OF orders_partitioned
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders_partitioned
FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- 5. ОПТИМИЗАЦИЯ ЗАПРОСОВ
-- До оптимизации (N+1 проблема)
SELECT * FROM users WHERE id IN (
    SELECT DISTINCT user_id FROM orders WHERE created_at > NOW() - INTERVAL '30 days'
);

-- После оптимизации (JOIN)
SELECT DISTINCT u.*
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.created_at > NOW() - INTERVAL '30 days';

-- Использование CTE для сложных запросов
WITH recent_orders AS (
    SELECT user_id, COUNT(*) as order_count, SUM(total_amount) as total_spent
    FROM orders
    WHERE created_at > NOW() - INTERVAL '90 days'
    GROUP BY user_id
    HAVING COUNT(*) >= 3
),
user_segments AS (
    SELECT
        user_id,
        CASE
            WHEN total_spent > 1000 THEN 'high_value'
            WHEN total_spent > 300 THEN 'medium_value'
            ELSE 'low_value'
        END as segment
    FROM recent_orders
)
SELECT u.email, us.segment, ro.order_count, ro.total_spent
FROM users u
JOIN user_segments us ON u.id = us.user_id
JOIN recent_orders ro ON u.id = ro.user_id
ORDER BY ro.total_spent DESC;
""",

    "connection_pooling": """
# Оптимизация подключений с asyncpg и PgBouncer

import asyncpg
import asyncio
from contextlib import asynccontextmanager
from typing import Optional
import logging

class DatabasePool:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.logger = logging.getLogger(__name__)

    async def create_pool(
        self,
        database_url: str,
        min_size: int = 5,
        max_size: int = 20,
        max_queries: int = 50000,
        max_inactive_connection_lifetime: float = 300.0,
        command_timeout: float = 60.0
    ):
        """Создать пул подключений с оптимальными настройками."""

        self.pool = await asyncpg.create_pool(
            database_url,
            min_size=min_size,
            max_size=max_size,
            max_queries=max_queries,
            max_inactive_connection_lifetime=max_inactive_connection_lifetime,
            command_timeout=command_timeout,
            setup=self._setup_connection
        )
        self.logger.info(f"Database pool created: {min_size}-{max_size} connections")

    async def _setup_connection(self, connection):
        """Настройка каждого подключения."""
        # Установить часовой пояс
        await connection.execute("SET timezone = 'UTC'")

        # Оптимизация для конкретного приложения
        await connection.execute("SET statement_timeout = '30s'")
        await connection.execute("SET lock_timeout = '10s'")

        # Включить JIT для сложных запросов
        await connection.execute("SET jit = on")

    @asynccontextmanager
    async def acquire(self):
        """Контекстный менеджер для получения подключения."""
        async with self.pool.acquire() as connection:
            yield connection

    async def execute_query(self, query: str, *args):
        """Выполнить запрос с обработкой ошибок."""
        async with self.acquire() as conn:
            try:
                return await conn.fetch(query, *args)
            except asyncpg.exceptions.PostgresError as e:
                self.logger.error(f"Database error: {e}")
                raise
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                raise

    async def execute_transaction(self, queries: list):
        """Выполнить несколько запросов в транзакции."""
        async with self.acquire() as conn:
            async with conn.transaction():
                results = []
                for query, args in queries:
                    result = await conn.fetch(query, *args)
                    results.append(result)
                return results

    async def close(self):
        """Закрыть пул подключений."""
        if self.pool:
            await self.pool.close()

# PgBouncer конфигурация для production
PGBOUNCER_CONFIG = '''
[databases]
myapp = host=localhost port=5432 dbname=myapp

[pgbouncer]
pool_mode = transaction
listen_port = 6432
listen_addr = 0.0.0.0
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

# Connection limits
max_client_conn = 100
default_pool_size = 20
min_pool_size = 5
reserve_pool_size = 3

# Timeouts
server_round_robin = 1
query_timeout = 0
query_wait_timeout = 120
client_idle_timeout = 0
server_idle_timeout = 600
server_connect_timeout = 15
server_login_retry = 15

# Performance
ignore_startup_parameters = extra_float_digits

# Logging
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1

# Stats
stats_period = 60
'''

# Мониторинг пула подключений
class PoolMonitor:
    def __init__(self, pool: DatabasePool):
        self.pool = pool
        self.logger = logging.getLogger(__name__)

    async def get_pool_stats(self):
        """Получить статистику пула."""
        if not self.pool.pool:
            return None

        return {
            "size": self.pool.pool.get_size(),
            "min_size": self.pool.pool.get_min_size(),
            "max_size": self.pool.pool.get_max_size(),
            "idle_size": self.pool.pool.get_idle_size(),
            "query_count": getattr(self.pool.pool, '_queue', {}).qsize() if hasattr(self.pool.pool, '_queue') else 0
        }

    async def monitor_connections(self):
        """Мониторинг подключений каждые 30 секунд."""
        while True:
            stats = await self.get_pool_stats()
            if stats:
                utilization = (stats["size"] - stats["idle_size"]) / stats["max_size"]

                self.logger.info(
                    f"Pool stats: {stats['size']}/{stats['max_size']} connections, "
                    f"{stats['idle_size']} idle, {utilization:.1%} utilization"
                )

                # Предупреждение при высокой утилизации
                if utilization > 0.8:
                    self.logger.warning(f"High pool utilization: {utilization:.1%}")

            await asyncio.sleep(30)

# Использование
async def main():
    db_pool = DatabasePool()
    await db_pool.create_pool(
        "postgresql://user:password@localhost:5432/myapp",
        min_size=5,
        max_size=20
    )

    # Запуск мониторинга
    monitor = PoolMonitor(db_pool)
    monitor_task = asyncio.create_task(monitor.monitor_connections())

    try:
        # Выполнение запросов
        users = await db_pool.execute_query(
            "SELECT * FROM users WHERE created_at > $1",
            datetime.now() - timedelta(days=30)
        )

        # Транзакция
        transaction_queries = [
            ("INSERT INTO orders (user_id, total) VALUES ($1, $2)", [1, 100.0]),
            ("UPDATE users SET last_order_at = NOW() WHERE id = $1", [1])
        ]
        await db_pool.execute_transaction(transaction_queries)

    finally:
        monitor_task.cancel()
        await db_pool.close()
""",

    "monitoring_queries": """
-- Мониторинг производительности PostgreSQL

-- 1. АКТИВНЫЕ ПОДКЛЮЧЕНИЯ
SELECT
    datname,
    state,
    COUNT(*) as connections,
    MAX(now() - state_change) as max_duration
FROM pg_stat_activity
WHERE state IS NOT NULL
GROUP BY datname, state
ORDER BY datname, state;

-- 2. БЛОКИРОВКИ И ОЖИДАНИЯ
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement,
    blocked_activity.application_name AS blocked_application,
    blocking_activity.application_name AS blocking_application,
    blocked_locks.mode AS blocked_mode,
    blocking_locks.mode AS blocking_mode,
    now() - blocked_activity.query_start AS blocked_duration
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity
    ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.DATABASE IS NOT DISTINCT FROM blocked_locks.DATABASE
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity
    ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.GRANTED;

-- 3. РАЗМЕРЫ ТАБЛИЦ И ИНДЕКСОВ
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) -
                   pg_relation_size(schemaname||'.'||tablename)) as index_size,
    pg_stat_get_live_tuples(c.oid) as live_tuples,
    pg_stat_get_dead_tuples(c.oid) as dead_tuples
FROM pg_tables pt
JOIN pg_class c ON c.relname = pt.tablename
JOIN pg_namespace n ON n.oid = c.relnamespace AND n.nspname = pt.schemaname
WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 4. ЭФФЕКТИВНОСТЬ КЭША
SELECT
    'buffer_cache' as cache_type,
    ROUND(
        100.0 * sum(blks_hit) / NULLIF(sum(blks_hit) + sum(blks_read), 0), 2
    ) as hit_ratio_percent
FROM pg_stat_database
UNION ALL
SELECT
    'index_cache' as cache_type,
    ROUND(
        100.0 * sum(idx_blks_hit) / NULLIF(sum(idx_blks_hit) + sum(idx_blks_read), 0), 2
    ) as hit_ratio_percent
FROM pg_statio_user_indexes;

-- 5. VACUUM И ANALYZE СТАТИСТИКА
SELECT
    schemaname,
    tablename,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze,
    vacuum_count,
    autovacuum_count,
    analyze_count,
    autoanalyze_count,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows,
    ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_ratio_percent
FROM pg_stat_user_tables
ORDER BY dead_ratio_percent DESC NULLS LAST;

-- 6. CHECKPOINT И WAL СТАТИСТИКА
SELECT
    checkpoints_timed,
    checkpoints_req,
    checkpoint_write_time,
    checkpoint_sync_time,
    buffers_checkpoint,
    buffers_clean,
    maxwritten_clean,
    buffers_backend,
    buffers_backend_fsync,
    buffers_alloc,
    stats_reset
FROM pg_stat_bgwriter;

-- 7. РЕПЛИКАЦИЯ (если настроена)
SELECT
    client_addr,
    client_hostname,
    client_port,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag,
    sync_priority,
    sync_state
FROM pg_stat_replication;
"""
}