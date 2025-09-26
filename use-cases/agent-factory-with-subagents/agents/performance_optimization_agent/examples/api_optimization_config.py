"""
API Performance конфигурация для Performance Optimization Agent.

Этот файл демонстрирует настройку агента для оптимизации API производительности.
Включает настройки для REST API, GraphQL, и микросервисов.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from ..dependencies import PerformanceOptimizationDependencies


@dataclass
class APIPerformanceDependencies(PerformanceOptimizationDependencies):
    """Конфигурация для API оптимизации."""

    # Основные настройки
    domain_type: str = "api"
    project_type: str = "rest_api"
    framework: str = "fastapi"

    # Performance специфичные настройки
    performance_type: str = "api"
    optimization_strategy: str = "speed"

    # Целевые метрики для API
    target_metrics: Dict[str, Any] = field(default_factory=lambda: {
        "response_time_p50": 50,   # ms
        "response_time_p95": 200,  # ms
        "response_time_p99": 500,  # ms
        "throughput_rps": 5000,    # requests per second
        "error_rate": 0.001,       # 0.1%
        "cpu_usage": 0.6,          # 60%
        "memory_usage": 0.7,       # 70%
        "connection_pool_usage": 0.8,  # 80%
        "cache_hit_ratio": 0.85    # 85%
    })

    # API специфичные настройки
    enable_connection_pooling: bool = True
    enable_response_caching: bool = True
    enable_request_batching: bool = True
    enable_rate_limiting: bool = True
    enable_async_processing: bool = True

    # Database настройки
    enable_query_optimization: bool = True
    enable_database_indexing: bool = True
    enable_read_replicas: bool = True

    def __post_init__(self):
        super().__post_init__()

        # API performance knowledge tags
        self.knowledge_tags.extend([
            "api-performance", "rest-api", "graphql", "microservices",
            "caching", "connection-pooling", "async-processing"
        ])

    def get_api_performance_config(self) -> Dict[str, Any]:
        """Специфичная конфигурация для API производительности."""
        return {
            "request_handling": {
                "async_processing": self.enable_async_processing,
                "connection_pooling": self.enable_connection_pooling,
                "request_batching": self.enable_request_batching,
                "streaming_responses": True
            },
            "caching": {
                "response_caching": self.enable_response_caching,
                "redis_cache": True,
                "memory_cache": True,
                "cdn_caching": True,
                "cache_invalidation": True
            },
            "database": {
                "query_optimization": self.enable_query_optimization,
                "connection_pooling": True,
                "read_replicas": self.enable_read_replicas,
                "database_indexing": self.enable_database_indexing,
                "query_caching": True
            },
            "security": {
                "rate_limiting": self.enable_rate_limiting,
                "ddos_protection": True,
                "input_validation": True,
                "authentication_caching": True
            },
            "monitoring": {
                "apm_monitoring": True,
                "metrics_collection": True,
                "distributed_tracing": True,
                "health_checks": True
            }
        }

    def get_caching_strategy(self) -> Dict[str, Any]:
        """Стратегия кэширования для API."""
        return {
            "layers": {
                "application_cache": {
                    "enabled": True,
                    "ttl": 300,  # 5 minutes
                    "max_size": "100MB"
                },
                "redis_cache": {
                    "enabled": True,
                    "ttl": 3600,  # 1 hour
                    "max_memory": "1GB"
                },
                "cdn_cache": {
                    "enabled": True,
                    "ttl": 86400,  # 24 hours
                    "edge_locations": True
                }
            },
            "strategies": {
                "cache_aside": True,
                "write_through": False,
                "write_behind": True,
                "refresh_ahead": True
            },
            "invalidation": {
                "time_based": True,
                "event_based": True,
                "manual_purge": True,
                "smart_invalidation": True
            }
        }

    def get_database_optimization_config(self) -> Dict[str, Any]:
        """Конфигурация оптимизации базы данных."""
        return {
            "connection_management": {
                "pool_size": 20,
                "max_overflow": 10,
                "pool_timeout": 30,
                "pool_recycle": 3600
            },
            "query_optimization": {
                "explain_analyze": True,
                "slow_query_log": True,
                "query_plan_cache": True,
                "prepared_statements": True
            },
            "indexing": {
                "automatic_indexing": True,
                "composite_indexes": True,
                "partial_indexes": True,
                "covering_indexes": True
            },
            "replication": {
                "read_replicas": self.enable_read_replicas,
                "read_write_split": True,
                "failover_support": True,
                "lag_monitoring": True
            }
        }


# Пример использования
def get_api_performance_dependencies() -> APIPerformanceDependencies:
    """Создать конфигурацию для API оптимизации."""
    return APIPerformanceDependencies(
        project_path="/api/service",
        project_name="High Performance API",
        domain_type="api",
        project_type="rest_api",
        framework="fastapi",
        performance_type="api",
        optimization_strategy="speed",
        enable_connection_pooling=True,
        enable_response_caching=True,
        enable_async_processing=True
    )


# Примеры оптимизированного API кода
API_PERFORMANCE_EXAMPLES = {
    "fastapi_optimized": """
# FastAPI with performance optimizations
from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
import asyncio
import aioredis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class APIPerformanceConfig:
    def __init__(self, config):
        self.config = config.get_api_performance_config()
        self.caching = config.get_caching_strategy()
        self.db_config = config.get_database_optimization_config()

# Async database setup with connection pooling
async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=False  # Disable in production
)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Redis connection pool
redis_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global redis_pool
    redis_pool = aioredis.ConnectionPool.from_url(
        "redis://localhost:6379",
        max_connections=20
    )

    # Initialize cache
    FastAPICache.init(RedisBackend(redis_pool), prefix="api-cache")

    yield

    # Shutdown
    await redis_pool.disconnect()

app = FastAPI(
    title="High Performance API",
    lifespan=lifespan
)

# Performance middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency with connection pooling
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/api/users/{user_id}")
@cache(expire=300)  # Cache for 5 minutes
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    # Optimized database query with eager loading
    result = await db.execute(
        select(User)
        .options(selectinload(User.profile))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Background task for analytics
    background_tasks.add_task(track_user_access, user_id)

    return user

@app.post("/api/users/batch")
async def create_users_batch(
    users: List[UserCreate],
    db: AsyncSession = Depends(get_db)
):
    # Batch processing for better performance
    db_users = [User(**user.dict()) for user in users]
    db.add_all(db_users)
    await db.commit()

    return {"created": len(db_users)}

# Async background task
async def track_user_access(user_id: int):
    # Non-blocking analytics tracking
    async with aioredis.Redis(connection_pool=redis_pool) as redis:
        await redis.incr(f"user_access:{user_id}")
""",

    "django_optimized": """
# Django with performance optimizations
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery import shared_task
import redis

class OptimizedUserAPIView(APIView):

    @method_decorator(cache_page(300))  # Cache for 5 minutes
    @method_decorator(vary_on_headers('Authorization'))
    def get(self, request, user_id):
        # Check cache first
        cache_key = f"user:{user_id}"
        user_data = cache.get(cache_key)

        if user_data is None:
            # Optimized query with select_related and prefetch_related
            try:
                user = User.objects.select_related('profile').prefetch_related(
                    'orders__items'
                ).get(id=user_id)

                user_data = {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'profile': {
                        'avatar': user.profile.avatar.url if user.profile.avatar else None,
                        'bio': user.profile.bio
                    },
                    'orders_count': user.orders.count()
                }

                # Cache for 5 minutes
                cache.set(cache_key, user_data, 300)

            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # Async background task for analytics
        track_user_access.delay(user_id)

        return Response(user_data)

    def post(self, request):
        # Batch processing with database transaction
        users_data = request.data.get('users', [])

        if not users_data:
            return Response(
                {'error': 'No users provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                # Bulk create for better performance
                users = [
                    User(
                        name=user_data['name'],
                        email=user_data['email']
                    )
                    for user_data in users_data
                ]
                User.objects.bulk_create(users, batch_size=100)

            return Response(
                {'created': len(users)},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@shared_task
def track_user_access(user_id):
    # Redis for high-performance analytics
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0
    )
    redis_client.incr(f"user_access:{user_id}")
    redis_client.expire(f"user_access:{user_id}", 86400)  # 24 hours
""",

    "node_express_optimized": """
// Express.js with performance optimizations
const express = require('express');
const compression = require('compression');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const redis = require('redis');
const { Pool } = require('pg');
const cluster = require('cluster');
const os = require('os');

// Redis connection pool
const redisClient = redis.createClient({
  socket: {
    host: 'localhost',
    port: 6379
  },
  maxRetriesPerRequest: 3
});

// PostgreSQL connection pool
const pgPool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'myapp',
  user: 'user',
  password: 'password',
  max: 20,  // Maximum connections in pool
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Cluster for multi-core utilization
if (cluster.isMaster) {
  const numCPUs = os.cpus().length;

  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    cluster.fork();
  });
} else {
  const app = express();

  // Performance middleware
  app.use(helmet());
  app.use(compression());

  // Rate limiting
  const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 1000, // limit each IP to 1000 requests per windowMs
    message: 'Too many requests from this IP'
  });
  app.use('/api/', limiter);

  app.use(express.json({ limit: '10mb' }));

  // Cache middleware
  const cache = (duration) => {
    return async (req, res, next) => {
      const key = req.originalUrl;

      try {
        const cached = await redisClient.get(key);
        if (cached) {
          return res.json(JSON.parse(cached));
        }

        res.sendResponse = res.json;
        res.json = (body) => {
          redisClient.setEx(key, duration, JSON.stringify(body));
          res.sendResponse(body);
        };

        next();
      } catch (error) {
        next();
      }
    };
  };

  // Optimized API endpoint
  app.get('/api/users/:id', cache(300), async (req, res) => {
    const { id } = req.params;

    try {
      // Optimized SQL query with joins
      const result = await pgPool.query(`
        SELECT
          u.id, u.name, u.email,
          p.avatar, p.bio,
          COUNT(o.id) as orders_count
        FROM users u
        LEFT JOIN profiles p ON u.id = p.user_id
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.id = $1
        GROUP BY u.id, p.avatar, p.bio
      `, [id]);

      if (result.rows.length === 0) {
        return res.status(404).json({ error: 'User not found' });
      }

      const user = result.rows[0];

      // Background analytics (non-blocking)
      setImmediate(() => {
        redisClient.incr(`user_access:${id}`);
      });

      res.json(user);

    } catch (error) {
      console.error('Database error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

  // Batch processing endpoint
  app.post('/api/users/batch', async (req, res) => {
    const { users } = req.body;

    if (!users || !Array.isArray(users)) {
      return res.status(400).json({ error: 'Invalid users data' });
    }

    const client = await pgPool.connect();

    try {
      await client.query('BEGIN');

      // Batch insert with prepared statement
      const values = users.map((user, index) =>
        `($${index * 2 + 1}, $${index * 2 + 2})`
      ).join(', ');

      const params = users.flatMap(user => [user.name, user.email]);

      const insertQuery = `
        INSERT INTO users (name, email)
        VALUES ${values}
        RETURNING id
      `;

      const result = await client.query(insertQuery, params);
      await client.query('COMMIT');

      res.status(201).json({ created: result.rowCount });

    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Batch insert error:', error);
      res.status(500).json({ error: 'Failed to create users' });
    } finally {
      client.release();
    }
  });

  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Worker ${process.pid} listening on port ${PORT}`);
  });
}
"""
}