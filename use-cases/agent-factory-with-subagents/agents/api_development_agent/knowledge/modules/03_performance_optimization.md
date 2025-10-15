# Module 03: Performance Optimization

## Паттерны оптимизации производительности API

Этот модуль содержит проверенные паттерны для повышения производительности API: кэширование, оптимизация базы данных, и другие best practices.

---

## Caching Strategies

### Multi-Level Caching with Redis

```python
import redis
import json
from functools import wraps
from typing import Any, Callable

# Initialize Redis client
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

def cache_result(
    expiry: int = 3600,
    cache_key_prefix: str = "api"
) -> Callable:
    """
    Decorator для кэширования результатов функций.

    Args:
        expiry: Время жизни кэша в секундах (default: 1 hour)
        cache_key_prefix: Префикс для ключей кэша

    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate unique cache key
            cache_key = f"{cache_key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)

            # Execute function if not cached
            result = await func(*args, **kwargs)

            # Cache result
            redis_client.setex(
                cache_key,
                expiry,
                json.dumps(result, default=str)
            )

            return result
        return wrapper
    return decorator

# Usage example
@cache_result(expiry=1800)  # Cache for 30 minutes
async def get_user_profile(user_id: int):
    """Expensive database operation."""
    return await db.fetch_user_with_details(user_id)

@cache_result(expiry=3600, cache_key_prefix="products")
async def get_product_catalog(category: str, page: int):
    """Cache product listings."""
    return await db.fetch_products_by_category(category, page)
```

### Cache Invalidation Patterns

```python
class CacheManager:
    """Управление кэшем с инвалидацией."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def invalidate_user_cache(self, user_id: int):
        """Invalidate all cache entries for a user."""
        pattern = f"api:*:user:{user_id}*"
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)

    def invalidate_by_pattern(self, pattern: str):
        """Invalidate cache by pattern."""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)

    def set_with_tags(self, key: str, value: Any, tags: list, expiry: int = 3600):
        """Set cache value with tags for easier invalidation."""
        # Store value
        self.redis.setex(key, expiry, json.dumps(value))

        # Store tags
        for tag in tags:
            self.redis.sadd(f"tag:{tag}", key)
            self.redis.expire(f"tag:{tag}", expiry)

    def invalidate_by_tag(self, tag: str):
        """Invalidate all cache entries with a specific tag."""
        tag_key = f"tag:{tag}"
        keys = self.redis.smembers(tag_key)

        if keys:
            self.redis.delete(*keys)
            self.redis.delete(tag_key)

# Usage
cache_manager = CacheManager(redis_client)

# Cache with tags
cache_manager.set_with_tags(
    key="user:profile:123",
    value=user_data,
    tags=["user:123", "profiles"],
    expiry=1800
)

# Invalidate by tag
cache_manager.invalidate_by_tag("user:123")  # Invalidates all user's cache
```

---

## Database Query Optimization

### N+1 Query Prevention with Eager Loading

```python
from sqlalchemy.orm import selectinload, joinedload, Session

def get_users_with_posts(db: Session):
    """
    Fetch users with their posts using eager loading.
    Prevents N+1 queries.
    """
    return db.query(User).options(
        selectinload(User.posts).selectinload(Post.comments)
    ).all()

def get_user_with_relations(db: Session, user_id: int):
    """
    Fetch user with all related data using joinedload.
    Single query instead of multiple.
    """
    return db.query(User).options(
        joinedload(User.profile),
        joinedload(User.settings),
        selectinload(User.posts).selectinload(Post.tags)
    ).filter(User.id == user_id).first()
```

### Cursor-Based Pagination

```python
from typing import Optional, List
from datetime import datetime

def paginate_posts(
    db: Session,
    cursor: Optional[datetime] = None,
    limit: int = 20
) -> dict:
    """
    Cursor-based pagination for better performance on large datasets.

    Args:
        db: Database session
        cursor: Timestamp cursor for pagination
        limit: Number of items per page

    Returns:
        Dict with data and pagination info
    """
    query = db.query(Post).order_by(Post.created_at.desc())

    if cursor:
        query = query.filter(Post.created_at < cursor)

    # Fetch limit + 1 to check if there are more results
    posts = query.limit(limit + 1).all()

    has_next = len(posts) > limit
    if has_next:
        posts = posts[:-1]  # Remove extra item

    next_cursor = posts[-1].created_at if posts and has_next else None

    return {
        "data": [post.to_dict() for post in posts],
        "pagination": {
            "next_cursor": next_cursor.isoformat() if next_cursor else None,
            "has_next": has_next,
            "limit": limit
        }
    }

# FastAPI endpoint
@app.get("/posts")
async def list_posts(
    cursor: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List posts with cursor-based pagination."""
    cursor_date = None
    if cursor:
        cursor_date = datetime.fromisoformat(cursor)

    return paginate_posts(db, cursor_date, limit)
```

### Database Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# Configure connection pool
engine = create_engine(
    "postgresql://user:password@localhost/dbname",
    poolclass=QueuePool,
    pool_size=20,  # Maximum number of connections in the pool
    max_overflow=10,  # Maximum overflow connections
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=False  # Set to True for debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Response Compression

### Gzip Compression Middleware

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Add gzip compression middleware
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,  # Only compress responses larger than 1KB
    compresslevel=6  # Compression level (1-9, higher = better compression but slower)
)
```

### Selective Compression

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import gzip

class SmartCompressionMiddleware(BaseHTTPMiddleware):
    """Smart compression - только для подходящих content types."""

    COMPRESSIBLE_TYPES = [
        "application/json",
        "application/xml",
        "text/html",
        "text/plain",
        "text/css",
        "text/javascript"
    ]

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Check if client accepts gzip
        accept_encoding = request.headers.get("accept-encoding", "")
        if "gzip" not in accept_encoding:
            return response

        # Check content type
        content_type = response.headers.get("content-type", "")
        if not any(ct in content_type for ct in self.COMPRESSIBLE_TYPES):
            return response

        # Compress response
        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        if len(body) < 1000:  # Don't compress small responses
            return response

        compressed_body = gzip.compress(body, compresslevel=6)

        return Response(
            content=compressed_body,
            status_code=response.status_code,
            headers={
                **response.headers,
                "Content-Encoding": "gzip",
                "Content-Length": str(len(compressed_body))
            },
            media_type=content_type
        )

app.add_middleware(SmartCompressionMiddleware)
```

---

## Query Result Streaming

### Streaming Large Datasets

```python
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import json

async def stream_large_dataset(db: Session) -> AsyncGenerator[str, None]:
    """
    Stream large dataset instead of loading all into memory.
    """
    yield "["

    first = True
    async for record in db.stream(query):
        if not first:
            yield ","
        yield json.dumps(record.to_dict())
        first = False

    yield "]"

@app.get("/export/users")
async def export_users(db: Session = Depends(get_db)):
    """Export all users as streaming JSON."""
    return StreamingResponse(
        stream_large_dataset(db),
        media_type="application/json"
    )
```

---

## Background Task Processing

### Celery Integration

```python
from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

@celery_app.task
def send_email_task(email: str, subject: str, body: str):
    """Background task для отправки email."""
    send_email(email, subject, body)

@celery_app.task
def process_large_file(file_path: str):
    """Background task для обработки файлов."""
    process_file(file_path)

# FastAPI endpoint
@app.post("/users/")
async def create_user(user: UserCreate):
    """Create user and send welcome email asynchronously."""
    new_user = db_create_user(user)

    # Schedule background task
    send_email_task.delay(
        new_user.email,
        "Welcome!",
        f"Welcome to our platform, {new_user.full_name}!"
    )

    return new_user
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
