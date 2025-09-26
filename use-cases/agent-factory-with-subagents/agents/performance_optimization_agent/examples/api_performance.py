"""
API Performance конфигурация для Performance Optimization Agent.

Этот файл демонстрирует настройку агента для оптимизации API производительности.
Включает caching strategies, rate limiting, compression, и connection pooling.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from ..dependencies import PerformanceOptimizationDependencies


@dataclass
class APIPerformanceDependencies(PerformanceOptimizationDependencies):
    """Конфигурация для API Performance Optimization."""

    # Основные настройки
    domain_type: str = "api"
    project_type: str = "rest_api"

    # Caching настройки
    enable_response_caching: bool = True
    enable_query_caching: bool = True
    enable_memory_caching: bool = True
    cache_ttl_short: int = 300  # 5 minutes
    cache_ttl_medium: int = 3600  # 1 hour
    cache_ttl_long: int = 86400  # 24 hours

    # Rate limiting
    enable_rate_limiting: bool = True
    enable_adaptive_rate_limiting: bool = True
    enable_user_based_limits: bool = True

    # Compression
    enable_response_compression: bool = True
    compression_threshold: int = 1000  # bytes
    compression_algorithms: List[str] = field(default_factory=lambda: ["gzip", "br"])

    # Connection management
    enable_connection_pooling: bool = True
    max_pool_size: int = 20
    connection_timeout: int = 30

    # Performance targets
    target_response_time_ms: int = 100
    target_throughput_rps: int = 1000
    target_error_rate: float = 0.001  # 0.1%
    target_p95_response_time_ms: int = 500

    def get_caching_config(self) -> Dict[str, Any]:
        """Конфигурация caching strategies."""
        return {
            "redis_config": {
                "host": "localhost",
                "port": 6379,
                "db": 0,
                "decode_responses": True,
                "max_connections": 10,
                "retry_on_timeout": True
            },
            "cache_strategies": {
                "static_data": {
                    "ttl": self.cache_ttl_long,
                    "pattern": "/api/config/*",
                    "compression": True
                },
                "user_data": {
                    "ttl": self.cache_ttl_medium,
                    "pattern": "/api/users/*",
                    "per_user": True
                },
                "search_results": {
                    "ttl": self.cache_ttl_short,
                    "pattern": "/api/search/*",
                    "vary_by": ["query", "filters"]
                },
                "real_time_data": {
                    "ttl": 60,
                    "pattern": "/api/live/*",
                    "invalidation": "event_based"
                }
            },
            "cache_invalidation": {
                "patterns": [
                    {"pattern": "/api/users/*", "triggers": ["user_update", "user_delete"]},
                    {"pattern": "/api/products/*", "triggers": ["product_update", "inventory_change"]}
                ]
            }
        }

    def get_rate_limiting_config(self) -> Dict[str, Any]:
        """Конфигурация rate limiting."""
        return {
            "global_limits": {
                "requests_per_second": 100,
                "requests_per_minute": 5000,
                "requests_per_hour": 100000
            },
            "endpoint_limits": {
                "/api/auth/login": {"limit": "5/minute", "burst": 10},
                "/api/auth/register": {"limit": "3/minute", "burst": 5},
                "/api/search": {"limit": "100/minute", "burst": 20},
                "/api/upload": {"limit": "10/minute", "burst": 3},
                "/api/admin/*": {"limit": "1000/hour", "burst": 50}
            },
            "user_tier_limits": {
                "free": {"limit": "100/hour", "burst": 10},
                "premium": {"limit": "1000/hour", "burst": 50},
                "enterprise": {"limit": "10000/hour", "burst": 200}
            },
            "adaptive_limiting": {
                "enabled": self.enable_adaptive_rate_limiting,
                "cpu_threshold": 80,
                "memory_threshold": 85,
                "response_time_threshold": self.target_response_time_ms * 2
            }
        }

    def get_compression_config(self) -> Dict[str, Any]:
        """Конфигурация compression."""
        return {
            "algorithms": self.compression_algorithms,
            "compression_level": {
                "gzip": 6,
                "br": 4,
                "deflate": 6
            },
            "minimum_size": self.compression_threshold,
            "mime_types": [
                "application/json",
                "application/xml",
                "text/plain",
                "text/html",
                "text/css",
                "application/javascript"
            ],
            "exclude_patterns": [
                "/api/binary/*",
                "/api/images/*",
                "/api/download/*"
            ]
        }

    def get_connection_pooling_config(self) -> Dict[str, Any]:
        """Конфигурация connection pooling."""
        return {
            "database_pool": {
                "min_size": 5,
                "max_size": self.max_pool_size,
                "max_overflow": 10,
                "pool_timeout": self.connection_timeout,
                "pool_recycle": 3600,
                "pool_pre_ping": True
            },
            "redis_pool": {
                "max_connections": 10,
                "retry_on_timeout": True,
                "socket_keepalive": True,
                "socket_keepalive_options": {}
            },
            "http_client_pool": {
                "max_connections": 100,
                "max_keepalive_connections": 20,
                "keepalive_expiry": 30
            }
        }

    def get_monitoring_config(self) -> Dict[str, Any]:
        """Конфигурация performance monitoring."""
        return {
            "metrics": {
                "response_time": {
                    "enabled": True,
                    "percentiles": [50, 95, 99],
                    "alert_threshold": self.target_p95_response_time_ms
                },
                "throughput": {
                    "enabled": True,
                    "target_rps": self.target_throughput_rps,
                    "alert_threshold": self.target_throughput_rps * 0.8
                },
                "error_rate": {
                    "enabled": True,
                    "target_rate": self.target_error_rate,
                    "alert_threshold": self.target_error_rate * 2
                },
                "cache_hit_ratio": {
                    "enabled": True,
                    "target_ratio": 0.8,
                    "alert_threshold": 0.6
                }
            },
            "alerting": {
                "response_time_p95": f">{self.target_p95_response_time_ms}ms",
                "error_rate": f">{self.target_error_rate * 100}%",
                "throughput_drop": f"<{self.target_throughput_rps * 0.8}rps",
                "cache_miss_ratio": ">40%"
            },
            "health_checks": {
                "database": "/health/db",
                "cache": "/health/cache",
                "external_apis": "/health/external"
            }
        }

    def get_optimization_strategies(self) -> Dict[str, Any]:
        """API optimization strategies."""
        return {
            "query_optimization": {
                "enable_query_batching": True,
                "enable_dataloader_pattern": True,
                "enable_n_plus_one_detection": True,
                "enable_query_caching": True
            },
            "response_optimization": {
                "enable_field_selection": True,
                "enable_pagination": True,
                "default_page_size": 20,
                "max_page_size": 100,
                "enable_response_streaming": True
            },
            "async_processing": {
                "enable_background_tasks": True,
                "enable_task_queues": True,
                "queue_backend": "redis",
                "max_queue_size": 10000
            }
        }


# Пример использования
def get_api_performance_dependencies() -> APIPerformanceDependencies:
    """Создать конфигурацию для API Performance Optimization."""
    return APIPerformanceDependencies(
        api_key="your-api-key",
        domain_type="api",
        project_type="rest_api",
        enable_response_caching=True,
        enable_rate_limiting=True,
        enable_response_compression=True,
        target_response_time_ms=100,
        target_throughput_rps=1000
    )


# Примеры кода для API optimization
API_PERFORMANCE_EXAMPLES = {
    "fastapi_optimization": """
# FastAPI с полной performance optimization
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import asyncio
import asyncpg
import redis.asyncio as redis
import time

app = FastAPI(title="Optimized API")

# Compression middleware
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
    compresslevel=6
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Database connection pool
class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=5,
            max_size=20,
            max_queries=50000,
            max_inactive_connection_lifetime=300,
            command_timeout=60
        )

    async def get_connection(self):
        return self.pool.acquire()

db_manager = DatabaseManager()

# Redis cache setup
@app.on_event("startup")
async def startup():
    redis_client = redis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis_client), prefix="api-cache")
    await db_manager.create_pool()

# Adaptive caching decorator
from functools import wraps

def cache_with_ttl(ttl: int, vary_by: list = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key from function name and parameters
            cache_key = f"{func.__name__}:"
            if vary_by:
                cache_key += ":".join([str(kwargs.get(param, '')) for param in vary_by])

            # Try cache first
            cached = await FastAPICache.get(cache_key)
            if cached:
                return cached

            # Execute function and cache result
            result = await func(*args, **kwargs)
            await FastAPICache.set(cache_key, result, expire=ttl)
            return result
        return wrapper
    return decorator

# Optimized endpoint with caching, rate limiting, and batching
@app.get("/api/products")
@limiter.limit("100/minute")
@cache_with_ttl(ttl=300, vary_by=['category', 'limit', 'offset'])
async def get_products(
    category: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    start_time = time.time()

    async with db_manager.get_connection() as conn:
        # Optimized query with proper indexing
        query = '''
        SELECT p.id, p.name, p.price, p.category, p.image_url,
               c.name as category_name,
               COALESCE(AVG(r.rating), 0) as avg_rating,
               COUNT(r.id) as review_count
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN reviews r ON p.id = r.product_id
        WHERE ($1::text IS NULL OR p.category = $1)
        GROUP BY p.id, c.name
        ORDER BY p.created_at DESC
        LIMIT $2 OFFSET $3
        '''

        products = await conn.fetch(query, category, limit, offset)

        # Convert to dict for JSON serialization
        result = [dict(product) for product in products]

    # Background task for analytics
    background_tasks.add_task(track_api_usage, "products", len(result))

    # Performance metrics
    response_time = time.time() - start_time

    return {
        "products": result,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "total": len(result)
        },
        "meta": {
            "response_time_ms": round(response_time * 1000, 2),
            "cached": False
        }
    }

# Batch processing for multiple requests
@app.post("/api/products/batch")
@limiter.limit("10/minute")
async def get_products_batch(product_ids: List[int]):
    if len(product_ids) > 50:  # Limit batch size
        raise HTTPException(status_code=400, detail="Too many IDs in batch")

    async with db_manager.get_connection() as conn:
        # Single query for all products
        query = '''
        SELECT id, name, price, category, image_url
        FROM products
        WHERE id = ANY($1::int[])
        '''

        products = await conn.fetch(query, product_ids)
        return {"products": [dict(p) for p in products]}

# Health check endpoint
@app.get("/health")
async def health_check():
    checks = {}

    # Database health
    try:
        async with db_manager.get_connection() as conn:
            await conn.fetchval("SELECT 1")
        checks["database"] = "healthy"
    except:
        checks["database"] = "unhealthy"

    # Cache health
    try:
        await FastAPICache.get("health_check")
        checks["cache"] = "healthy"
    except:
        checks["cache"] = "unhealthy"

    status = "healthy" if all(v == "healthy" for v in checks.values()) else "unhealthy"

    return {"status": status, "checks": checks}

async def track_api_usage(endpoint: str, result_count: int):
    # Background analytics tracking
    pass
""",

    "graphql_optimization": """
# GraphQL с DataLoader pattern для N+1 problem решения
from graphene import ObjectType, String, List, Field, Schema
import asyncio
from aiodataloader import DataLoader

class UserLoader(DataLoader):
    async def batch_load_fn(self, user_ids):
        # Batch load users instead of individual queries
        async with get_db_connection() as conn:
            users = await conn.fetch(
                "SELECT * FROM users WHERE id = ANY($1::int[])",
                user_ids
            )
            # Return in same order as requested
            user_dict = {user['id']: user for user in users}
            return [user_dict.get(user_id) for user_id in user_ids]

class ProductLoader(DataLoader):
    async def batch_load_fn(self, product_ids):
        async with get_db_connection() as conn:
            products = await conn.fetch(
                "SELECT * FROM products WHERE id = ANY($1::int[])",
                product_ids
            )
            product_dict = {product['id']: product for product in products}
            return [product_dict.get(product_id) for product_id in product_ids]

class User(ObjectType):
    id = String()
    name = String()
    email = String()
    orders = List(lambda: Order)

    async def resolve_orders(self, info):
        # Use DataLoader to batch order queries
        return await info.context['order_loader'].load(self.id)

class Product(ObjectType):
    id = String()
    name = String()
    price = String()
    user = Field(User)

    async def resolve_user(self, info):
        # Batch user loading
        return await info.context['user_loader'].load(self.user_id)

class Query(ObjectType):
    products = List(Product)

    async def resolve_products(self, info):
        # Single query with proper indexing
        async with get_db_connection() as conn:
            return await conn.fetch(
                "SELECT * FROM products ORDER BY created_at DESC LIMIT 100"
            )

# Schema with DataLoader context
schema = Schema(query=Query)

async def graphql_handler(request):
    # Create DataLoader instances per request
    context = {
        'user_loader': UserLoader(),
        'product_loader': ProductLoader(),
        'order_loader': OrderLoader()
    }

    result = await schema.execute_async(
        request.json['query'],
        context_value=context
    )

    return result
""",

    "caching_strategies": """
# Advanced caching strategies
import redis.asyncio as redis
import json
import hashlib
from typing import Any, Optional
from functools import wraps

class SmartCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600):
        await self.redis.setex(
            key,
            ttl,
            json.dumps(value, default=str)
        )

    async def invalidate_pattern(self, pattern: str):
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)

    def cache_key(self, *args, **kwargs) -> str:
        # Generate deterministic cache key
        key_data = f"{args}-{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()

# Multi-level caching
class MultiLevelCache:
    def __init__(self):
        self.memory_cache = {}  # L1 cache
        self.redis_cache = SmartCache("redis://localhost:6379")  # L2 cache

    async def get(self, key: str) -> Optional[Any]:
        # Try L1 first (memory)
        if key in self.memory_cache:
            return self.memory_cache[key]

        # Try L2 (Redis)
        value = await self.redis_cache.get(key)
        if value:
            # Populate L1 cache
            self.memory_cache[key] = value

        return value

    async def set(self, key: str, value: Any, ttl: int = 3600):
        # Set in both levels
        self.memory_cache[key] = value
        await self.redis_cache.set(key, value, ttl)

    async def invalidate(self, key: str):
        # Invalidate from both levels
        self.memory_cache.pop(key, None)
        await self.redis_cache.redis.delete(key)

# Cache-aside pattern with automatic refresh
def cache_aside(ttl: int = 3600, refresh_threshold: float = 0.8):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = kwargs.pop('cache', None)
            if not cache:
                return await func(*args, **kwargs)

            key = cache.cache_key(*args, **kwargs)

            # Try cache first
            cached = await cache.get(key)
            if cached:
                # Check if we need background refresh
                age = cached.get('_cache_age', 0)
                if age > ttl * refresh_threshold:
                    # Trigger background refresh
                    asyncio.create_task(
                        refresh_cache(func, cache, key, args, kwargs, ttl)
                    )
                return cached['data']

            # Cache miss - get from source
            result = await func(*args, **kwargs)
            await cache.set(key, {
                'data': result,
                '_cache_age': 0
            }, ttl)

            return result
        return wrapper
    return decorator

async def refresh_cache(func, cache, key, args, kwargs, ttl):
    try:
        result = await func(*args, **kwargs)
        await cache.set(key, {
            'data': result,
            '_cache_age': 0
        }, ttl)
    except Exception:
        # Silent fail for background refresh
        pass
"""
}