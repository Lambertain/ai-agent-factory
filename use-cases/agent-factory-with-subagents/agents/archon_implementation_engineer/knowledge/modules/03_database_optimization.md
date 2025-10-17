# Module 03: Database Optimization

**Версия:** 1.0
**Дата:** 2025-10-17
**Автор:** Archon Implementation Engineer

**Назад к:** [Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- COPY для bulk inserts в PostgreSQL (fastest method)
- Создание GIN/BRIN/Covering indexes для оптимизации запросов
- FAISS IndexIVFFlat/HNSW для vector similarity search
- Решение N+1 query problem с JOIN или batch fetch
- Hybrid search implementation (vector + full-text PostgreSQL)
- EXPLAIN ANALYZE для анализа производительности запросов
- Batch upsert операции с ON CONFLICT UPDATE
- Vector database оптимизация по размеру данных (<10k, <100k, >100k)

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** база данных, индексы, vector search, FAISS, N+1 проблема, bulk операции, PostgreSQL, оптимизация, similarity search, embeddings, hybrid search, full-text search, query optimization, batch operations

**English:** database, indexes, vector search, FAISS, N+1 problem, bulk operations, PostgreSQL, optimization, similarity search, embeddings, hybrid search, full-text search, query optimization, batch operations

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Большие объемы данных для вставки (тысячи записей)
- Vector databases и semantic similarity search
- Оптимизация медленных database запросов
- Работа с embeddings и векторным поиском
- N+1 query problem обнаружен в логах
- Необходимость bulk inserts/updates с минимальным overhead
- Hybrid поиск (векторный + текстовый)
- Анализ и оптимизация query execution plans

---

## Efficient Database Operations

### Optimized Database Class

```python
import asyncpg
from typing import List, Dict, Any
from contextlib import asynccontextmanager

class OptimizedDatabase:
    """Оптимизированная работа с базой данных."""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def initialize(self):
        """Инициализация пула соединений с оптимальными настройками."""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=5,
            max_size=20,
            command_timeout=60,
            server_settings={
                'jit': 'off',  # Отключение JIT для стабильности
                'application_name': 'archon_agent',
                'work_mem': '64MB',  # Память для операций сортировки
                'effective_cache_size': '4GB'  # Размер кэша ОС
            }
        )

    @asynccontextmanager
    async def transaction(self):
        """Контекстный менеджер для транзакций."""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                yield conn

    async def bulk_insert(
        self,
        table: str,
        data: List[Dict[str, Any]]
    ) -> int:
        """Массовая вставка данных через COPY (fastest method)."""
        if not data:
            return 0

        columns = list(data[0].keys())
        values = [list(row.values()) for row in data]

        async with self.pool.acquire() as conn:
            # COPY - самый быстрый способ вставки
            result = await conn.copy_records_to_table(
                table,
                records=values,
                columns=columns
            )
            return len(values)

    async def execute_query_with_pagination(
        self,
        base_query: str,
        params: List[Any],
        page_size: int = 1000
    ) -> List[Dict]:
        """Выполнение запроса с пагинацией для больших результатов."""
        all_results = []
        offset = 0

        async with self.pool.acquire() as conn:
            while True:
                paginated_query = f"{base_query} LIMIT {page_size} OFFSET {offset}"
                rows = await conn.fetch(paginated_query, *params)

                if not rows:
                    break

                all_results.extend([dict(row) for row in rows])
                offset += page_size

                if len(rows) < page_size:
                    break

        return all_results

    async def explain_query(
        self,
        query: str,
        params: List[Any] = None
    ) -> Dict:
        """Анализ плана выполнения запроса (EXPLAIN ANALYZE)."""
        explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"

        async with self.pool.acquire() as conn:
            result = await conn.fetchval(explain_query, *(params or []))
            return result[0]  # JSON результат

    async def optimize_table(self, table: str):
        """Оптимизация таблицы (VACUUM ANALYZE)."""
        async with self.pool.acquire() as conn:
            await conn.execute(f"VACUUM ANALYZE {table}")
```

### Batch Operations для производительности

```python
class BatchOperations:
    """Batch операции для минимизации round-trips."""

    def __init__(self, db: OptimizedDatabase):
        self.db = db

    async def batch_upsert(
        self,
        table: str,
        data: List[Dict],
        conflict_columns: List[str],
        update_columns: List[str]
    ):
        """Batch upsert (INSERT ... ON CONFLICT UPDATE)."""
        if not data:
            return

        columns = list(data[0].keys())
        values_placeholder = ', '.join([
            f"({', '.join(['$' + str(i*len(columns) + j + 1) for j in range(len(columns))])})"
            for i in range(len(data))
        ])

        conflict_clause = ', '.join(conflict_columns)
        update_clause = ', '.join([
            f"{col} = EXCLUDED.{col}" for col in update_columns
        ])

        query = f"""
            INSERT INTO {table} ({', '.join(columns)})
            VALUES {values_placeholder}
            ON CONFLICT ({conflict_clause})
            DO UPDATE SET {update_clause}
        """

        # Flatten data для параметров
        flat_values = [
            value for row in data for value in row.values()
        ]

        async with self.db.pool.acquire() as conn:
            await conn.execute(query, *flat_values)

    async def batch_delete(
        self,
        table: str,
        ids: List[str]
    ) -> int:
        """Batch удаление по списку ID."""
        if not ids:
            return 0

        placeholders = ', '.join(f'${i+1}' for i in range(len(ids)))
        query = f"DELETE FROM {table} WHERE id IN ({placeholders})"

        async with self.db.pool.acquire() as conn:
            result = await conn.execute(query, *ids)
            # Извлекаем количество удаленных строк
            return int(result.split()[-1])
```

---

## Indexing Strategies

### Оптимальные индексы для разных сценариев

```sql
-- 1. Составной индекс для поиска по нескольким полям
CREATE INDEX CONCURRENTLY idx_users_name_email
ON users (name, email)
WHERE active = true;

-- 2. Частичный индекс для активных записей (экономия места)
CREATE INDEX CONCURRENTLY idx_users_active
ON users (created_at)
WHERE active = true;

-- 3. GIN индекс для полнотекстового поиска
CREATE INDEX CONCURRENTLY idx_documents_search
ON documents USING gin(to_tsvector('english', title || ' ' || content));

-- 4. Индекс для JSON полей
CREATE INDEX CONCURRENTLY idx_metadata_tags
ON documents USING gin((metadata->>'tags'));

-- 5. Covering index для избежания table lookup
CREATE INDEX CONCURRENTLY idx_users_covering
ON users (id) INCLUDE (name, email, created_at)
WHERE active = true;

-- 6. BRIN индекс для timestamp columns (экономия памяти)
CREATE INDEX CONCURRENTLY idx_logs_created_at
ON logs USING brin(created_at);

-- 7. Hash индекс для точных совпадений
CREATE INDEX CONCURRENTLY idx_sessions_token
ON sessions USING hash(session_token);
```

### Index Maintenance

```python
class IndexMaintenance:
    """Управление индексами для оптимальной производительности."""

    def __init__(self, db: OptimizedDatabase):
        self.db = db

    async def check_index_usage(self, table: str) -> List[Dict]:
        """Проверка использования индексов на таблице."""
        query = """
            SELECT
                schemaname,
                tablename,
                indexname,
                idx_scan,
                idx_tup_read,
                idx_tup_fetch,
                pg_size_pretty(pg_relation_size(indexrelid)) as index_size
            FROM pg_stat_user_indexes
            WHERE tablename = $1
            ORDER BY idx_scan ASC
        """

        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(query, table)
            return [dict(row) for row in rows]

    async def find_missing_indexes(self, table: str) -> List[Dict]:
        """Найти потенциально полезные индексы."""
        query = """
            SELECT
                schemaname,
                tablename,
                attname,
                n_distinct,
                correlation
            FROM pg_stats
            WHERE tablename = $1
            AND n_distinct > 100  -- Достаточно уникальных значений
            AND correlation < 0.8  -- Низкая корреляция с физическим порядком
        """

        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(query, table)
            return [dict(row) for row in rows]

    async def rebuild_index(self, index_name: str):
        """Перестроить индекс конкурентно (без блокировки)."""
        query = f"REINDEX INDEX CONCURRENTLY {index_name}"

        async with self.db.pool.acquire() as conn:
            await conn.execute(query)
```

---

## Vector Database Optimization

### Optimized Vector Store с FAISS

```python
import numpy as np
from typing import List, Tuple
import faiss
import pickle

class OptimizedVectorStore:
    """Оптимизированное хранилище векторов с FAISS."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = None
        self.metadata = []

    def build_index(
        self,
        vectors: np.ndarray,
        use_gpu: bool = False
    ):
        """Построение оптимизированного индекса в зависимости от размера."""
        n_vectors = vectors.shape[0]

        # Выбор оптимального типа индекса
        if n_vectors < 10000:
            # Для малых данных - простой L2 поиск
            self.index = faiss.IndexFlatL2(self.dimension)
            print(f"[OK] Using IndexFlatL2 for {n_vectors} vectors")

        elif n_vectors < 100000:
            # Средние данные - IVF с кластерами
            nlist = min(100, n_vectors // 100)
            quantizer = faiss.IndexFlatL2(self.dimension)
            self.index = faiss.IndexIVFFlat(
                quantizer,
                self.dimension,
                nlist
            )
            print(f"[OK] Using IndexIVFFlat with {nlist} clusters")

        else:
            # Большие данные - HNSW для быстрого поиска
            self.index = faiss.IndexHNSWFlat(self.dimension, 32)
            self.index.hnsw.efConstruction = 200
            self.index.hnsw.efSearch = 50
            print(f"[OK] Using IndexHNSWFlat for {n_vectors} vectors")

        # GPU acceleration если доступно
        if use_gpu and faiss.get_num_gpus() > 0:
            res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(res, 0, self.index)
            print("[OK] Moved index to GPU")

        # Обучение индекса (для IVF)
        if hasattr(self.index, 'train'):
            print("[OK] Training index...")
            self.index.train(vectors)

        # Добавление векторов
        print("[OK] Adding vectors to index...")
        self.index.add(vectors)

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> Tuple[List[float], List[int]]:
        """Поиск ближайших векторов."""
        query_vector = query_vector.reshape(1, -1).astype(np.float32)
        distances, indices = self.index.search(query_vector, k)
        return distances[0].tolist(), indices[0].tolist()

    def batch_search(
        self,
        query_vectors: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Пакетный поиск для множества запросов."""
        return self.index.search(query_vectors.astype(np.float32), k)

    def save_index(self, filepath: str):
        """Сохранение индекса на диск."""
        # Сохранение FAISS индекса
        faiss.write_index(self.index, f"{filepath}.faiss")

        # Сохранение метаданных
        with open(f"{filepath}.metadata", 'wb') as f:
            pickle.dump(self.metadata, f)

        print(f"[OK] Index saved to {filepath}")

    def load_index(self, filepath: str):
        """Загрузка индекса с диска."""
        # Загрузка FAISS индекса
        self.index = faiss.read_index(f"{filepath}.faiss")

        # Загрузка метаданных
        with open(f"{filepath}.metadata", 'rb') as f:
            self.metadata = pickle.load(f)

        print(f"[OK] Index loaded from {filepath}")

    def add_vectors_incremental(
        self,
        vectors: np.ndarray,
        metadata: List[Dict]
    ):
        """Инкрементальное добавление векторов."""
        self.index.add(vectors.astype(np.float32))
        self.metadata.extend(metadata)
```

### Hybrid Search: Vector + Full-Text

```python
from typing import List, Dict
import asyncpg

class HybridSearchEngine:
    """Hybrid search: vector similarity + full-text search."""

    def __init__(
        self,
        vector_store: OptimizedVectorStore,
        db: OptimizedDatabase
    ):
        self.vector_store = vector_store
        self.db = db

    async def hybrid_search(
        self,
        query_text: str,
        query_embedding: np.ndarray,
        k: int = 20,
        alpha: float = 0.5  # Вес vector search vs full-text
    ) -> List[Dict]:
        """
        Hybrid search с комбинацией vector similarity и full-text search.

        Args:
            query_text: Текстовый запрос
            query_embedding: Векторное представление запроса
            k: Количество результатов
            alpha: Вес vector search (0-1), (1-alpha) = вес full-text
        """
        # 1. Vector search
        vector_distances, vector_indices = self.vector_store.search(
            query_embedding, k=k*2
        )

        # 2. Full-text search
        fulltext_results = await self._fulltext_search(query_text, k=k*2)

        # 3. Объединение результатов с взвешиванием
        combined_scores = {}

        # Нормализация vector scores
        max_vector_dist = max(vector_distances) if vector_distances else 1
        for idx, distance in zip(vector_indices, vector_distances):
            # Конвертируем distance в similarity score (0-1)
            similarity = 1 - (distance / max_vector_dist)
            combined_scores[idx] = alpha * similarity

        # Добавление full-text scores
        for result in fulltext_results:
            doc_id = result['id']
            rank_score = result['rank']

            if doc_id in combined_scores:
                combined_scores[doc_id] += (1 - alpha) * rank_score
            else:
                combined_scores[doc_id] = (1 - alpha) * rank_score

        # Сортировка по итоговому score
        sorted_results = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]

        # Получение документов
        doc_ids = [doc_id for doc_id, _ in sorted_results]
        documents = await self._get_documents_by_ids(doc_ids)

        return documents

    async def _fulltext_search(
        self,
        query: str,
        k: int
    ) -> List[Dict]:
        """Full-text поиск в PostgreSQL."""
        sql = """
            SELECT
                id,
                title,
                content,
                ts_rank(
                    to_tsvector('english', title || ' ' || content),
                    plainto_tsquery('english', $1)
                ) as rank
            FROM documents
            WHERE to_tsvector('english', title || ' ' || content) @@
                  plainto_tsquery('english', $1)
            ORDER BY rank DESC
            LIMIT $2
        """

        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(sql, query, k)
            return [dict(row) for row in rows]

    async def _get_documents_by_ids(
        self,
        doc_ids: List[int]
    ) -> List[Dict]:
        """Получить документы по списку ID."""
        placeholders = ', '.join(f'${i+1}' for i in range(len(doc_ids)))
        sql = f"""
            SELECT id, title, content, metadata
            FROM documents
            WHERE id IN ({placeholders})
        """

        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(sql, *doc_ids)
            return [dict(row) for row in rows]
```

---

## Query Optimization Patterns

### N+1 Query Problem Solution

```python
class OptimizedQueries:
    """Решение проблемы N+1 запросов."""

    def __init__(self, db: OptimizedDatabase):
        self.db = db

    async def get_users_with_posts_bad(self) -> List[Dict]:
        """❌ Плохо: N+1 queries."""
        users = await self._get_all_users()

        for user in users:
            # N дополнительных запросов!
            user['posts'] = await self._get_user_posts(user['id'])

        return users

    async def get_users_with_posts_good(self) -> List[Dict]:
        """✅ Хорошо: 2 queries с JOIN или batch fetch."""
        # Вариант 1: JOIN в одном запросе
        query = """
            SELECT
                u.id as user_id,
                u.name as user_name,
                u.email as user_email,
                p.id as post_id,
                p.title as post_title,
                p.content as post_content
            FROM users u
            LEFT JOIN posts p ON u.id = p.user_id
        """

        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(query)

        # Группировка результатов
        users_dict = {}
        for row in rows:
            user_id = row['user_id']

            if user_id not in users_dict:
                users_dict[user_id] = {
                    'id': user_id,
                    'name': row['user_name'],
                    'email': row['user_email'],
                    'posts': []
                }

            if row['post_id']:
                users_dict[user_id]['posts'].append({
                    'id': row['post_id'],
                    'title': row['post_title'],
                    'content': row['post_content']
                })

        return list(users_dict.values())

    async def _get_all_users(self) -> List[Dict]:
        """Получить всех пользователей."""
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM users")
            return [dict(row) for row in rows]

    async def _get_user_posts(self, user_id: str) -> List[Dict]:
        """Получить посты пользователя."""
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM posts WHERE user_id = $1", user_id
            )
            return [dict(row) for row in rows]
```

---

**Навигация:**
- [← Предыдущий модуль: Performance Optimization](02_performance_optimization.md)
- [↑ Назад к Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)
- [→ Следующий модуль: Testing & Quality Assurance](04_testing_quality_assurance.md)
