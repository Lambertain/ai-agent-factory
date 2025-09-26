"""
Web Application Performance конфигурация для Performance Optimization Agent.

Этот файл демонстрирует настройку агента для оптимизации веб-приложений.
Включает frontend optimization, API performance, и full-stack optimization strategies.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from ..dependencies import PerformanceOptimizationDependencies


@dataclass
class WebAppPerformanceDependencies(PerformanceOptimizationDependencies):
    """Конфигурация для Web Application Performance Optimization."""

    # Основные настройки
    domain_type: str = "web_application"
    project_type: str = "full_stack"

    # Frontend optimization настройки
    enable_bundle_optimization: bool = True
    enable_lazy_loading: bool = True
    enable_image_optimization: bool = True
    enable_service_worker: bool = True
    enable_critical_css: bool = True

    # API optimization настройки
    enable_response_caching: bool = True
    enable_compression: bool = True
    enable_rate_limiting: bool = True
    enable_connection_pooling: bool = True

    # Database optimization
    enable_query_optimization: bool = True
    enable_database_indexing: bool = True
    enable_connection_caching: bool = True

    # Monitoring настройки
    enable_core_web_vitals: bool = True
    enable_real_user_monitoring: bool = True
    enable_synthetic_monitoring: bool = True

    # Performance targets
    target_fcp_ms: int = 1500  # First Contentful Paint
    target_lcp_ms: int = 2500  # Largest Contentful Paint
    target_cls_score: float = 0.1  # Cumulative Layout Shift
    target_fid_ms: int = 100  # First Input Delay
    target_api_response_ms: int = 200

    def get_frontend_optimization_config(self) -> Dict[str, Any]:
        """Конфигурация frontend optimization."""
        return {
            "webpack_optimization": {
                "split_chunks": self.enable_bundle_optimization,
                "tree_shaking": True,
                "code_splitting": self.enable_lazy_loading,
                "bundle_analyzer": True,
                "compression_plugin": self.enable_compression
            },
            "image_optimization": {
                "enabled": self.enable_image_optimization,
                "formats": ["avif", "webp", "jpg"],
                "lazy_loading": self.enable_lazy_loading,
                "responsive_images": True,
                "compression_quality": 80
            },
            "css_optimization": {
                "critical_css": self.enable_critical_css,
                "css_purging": True,
                "minification": True,
                "autoprefixer": True
            },
            "javascript_optimization": {
                "minification": True,
                "dead_code_elimination": True,
                "module_concatenation": True,
                "scope_hoisting": True
            },
            "service_worker": {
                "enabled": self.enable_service_worker,
                "caching_strategy": "cache_first",
                "runtime_caching": True,
                "offline_support": True
            }
        }

    def get_api_optimization_config(self) -> Dict[str, Any]:
        """Конфигурация API optimization."""
        return {
            "caching": {
                "enabled": self.enable_response_caching,
                "redis_config": {
                    "host": "localhost",
                    "port": 6379,
                    "db": 0,
                    "decode_responses": True
                },
                "cache_strategies": {
                    "api_responses": {"ttl": 300, "max_keys": 10000},
                    "user_sessions": {"ttl": 3600, "max_keys": 50000},
                    "static_data": {"ttl": 86400, "max_keys": 1000}
                }
            },
            "compression": {
                "enabled": self.enable_compression,
                "algorithms": ["gzip", "br"],
                "minimum_size": 1000,
                "compression_level": 6
            },
            "rate_limiting": {
                "enabled": self.enable_rate_limiting,
                "rules": [
                    {"endpoint": "/api/search", "limit": "100/minute"},
                    {"endpoint": "/api/upload", "limit": "10/minute"},
                    {"endpoint": "/api/auth", "limit": "5/minute"}
                ]
            },
            "connection_pooling": {
                "enabled": self.enable_connection_pooling,
                "database_pool_size": 20,
                "redis_pool_size": 10,
                "http_connection_pool": 100
            }
        }

    def get_database_optimization_config(self) -> Dict[str, Any]:
        """Конфигурация database optimization."""
        return {
            "query_optimization": {
                "enabled": self.enable_query_optimization,
                "slow_query_threshold_ms": 1000,
                "explain_plan_analysis": True,
                "query_caching": True
            },
            "indexing": {
                "enabled": self.enable_database_indexing,
                "auto_index_suggestions": True,
                "index_usage_monitoring": True,
                "composite_index_optimization": True
            },
            "connection_management": {
                "pool_size": 20,
                "max_overflow": 30,
                "pool_timeout": 30,
                "pool_recycle": 3600
            },
            "monitoring": {
                "slow_queries": True,
                "connection_stats": True,
                "query_performance": True
            }
        }

    def get_monitoring_config(self) -> Dict[str, Any]:
        """Конфигурация performance monitoring."""
        return {
            "core_web_vitals": {
                "enabled": self.enable_core_web_vitals,
                "thresholds": {
                    "fcp": self.target_fcp_ms,
                    "lcp": self.target_lcp_ms,
                    "cls": self.target_cls_score,
                    "fid": self.target_fid_ms
                }
            },
            "real_user_monitoring": {
                "enabled": self.enable_real_user_monitoring,
                "sample_rate": 0.1,
                "track_user_flows": True,
                "track_errors": True
            },
            "synthetic_monitoring": {
                "enabled": self.enable_synthetic_monitoring,
                "test_frequency": "5min",
                "locations": ["us-east", "eu-west", "asia-pacific"]
            },
            "api_monitoring": {
                "response_time_threshold": self.target_api_response_ms,
                "error_rate_threshold": 0.01,
                "availability_threshold": 0.999
            }
        }

    def get_performance_budget(self) -> Dict[str, Any]:
        """Performance budget для web application."""
        return {
            "bundle_sizes": {
                "javascript_main": "150kb",
                "javascript_vendor": "200kb",
                "css_main": "50kb",
                "total_page_size": "500kb"
            },
            "metrics": {
                "first_contentful_paint": f"{self.target_fcp_ms}ms",
                "largest_contentful_paint": f"{self.target_lcp_ms}ms",
                "cumulative_layout_shift": str(self.target_cls_score),
                "first_input_delay": f"{self.target_fid_ms}ms"
            },
            "api_performance": {
                "average_response_time": f"{self.target_api_response_ms}ms",
                "95th_percentile": f"{self.target_api_response_ms * 2}ms",
                "error_rate": "0.1%"
            }
        }


# Пример использования
def get_web_app_performance_dependencies() -> WebAppPerformanceDependencies:
    """Создать конфигурацию для Web Application Performance Optimization."""
    return WebAppPerformanceDependencies(
        api_key="your-api-key",
        domain_type="web_application",
        project_type="full_stack",
        enable_bundle_optimization=True,
        enable_lazy_loading=True,
        enable_response_caching=True,
        enable_core_web_vitals=True,
        target_fcp_ms=1500,
        target_api_response_ms=200
    )


# Примеры использования в коде
WEB_APP_PERFORMANCE_EXAMPLES = {
    "webpack_optimization": """
// Webpack configuration для performance optimization
const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  mode: 'production',

  // Entry points для code splitting
  entry: {
    main: './src/index.js',
    vendor: ['react', 'react-dom', 'lodash']
  },

  optimization: {
    // Advanced code splitting
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
        common: {
          name: 'common',
          minChunks: 2,
          priority: 5,
          chunks: 'all',
          enforce: true
        }
      }
    },

    // Tree shaking и dead code elimination
    usedExports: true,
    sideEffects: false,

    // Minification
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true,
            drop_debugger: true
          }
        }
      })
    ]
  },

  plugins: [
    // Gzip compression
    new CompressionPlugin({
      algorithm: 'gzip',
      test: /\\.(js|css|html|svg)$/,
      threshold: 8192,
      minRatio: 0.8
    }),

    // Bundle analysis
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      generateStatsFile: true
    })
  ],

  // Performance budget enforcement
  performance: {
    hints: 'error',
    maxEntrypointSize: 250000,
    maxAssetSize: 250000
  }
};
""",

    "api_optimization": """
// FastAPI с performance optimization
from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import redis
import asyncio

app = FastAPI()

# Compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Redis для caching
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Connection pooling
class DatabasePool:
    def __init__(self):
        self.pool = None

    async def get_pool(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=10,
                max_size=20,
                command_timeout=60
            )
        return self.pool

db_pool = DatabasePool()

@app.get("/api/products")
@limiter.limit("100/minute")
async def get_products(
    category: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    # Cache key generation
    cache_key = f"products:{category}:{limit}:{offset}"

    # Check cache first
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    # Database query с connection pooling
    pool = await db_pool.get_pool()
    async with pool.acquire() as connection:
        query = '''
        SELECT id, name, price, category, image_url
        FROM products
        WHERE ($1::text IS NULL OR category = $1)
        ORDER BY created_at DESC
        LIMIT $2 OFFSET $3
        '''

        products = await connection.fetch(query, category, limit, offset)
        result = [dict(product) for product in products]

    # Cache result for 5 minutes
    redis_client.setex(cache_key, 300, json.dumps(result, default=str))

    return {"products": result, "total": len(result)}

@app.middleware("http")
async def add_performance_headers(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response
""",

    "frontend_performance": """
// React Performance Optimization
import React, { lazy, Suspense, memo, useMemo, useCallback } from 'react';
import { Helmet } from 'react-helmet';

// Code splitting с lazy loading
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Memoized component для предотвращения re-renders
const ProductCard = memo(({ product, onAddToCart }) => {
  const handleAddToCart = useCallback(() => {
    onAddToCart(product.id);
  }, [product.id, onAddToCart]);

  const discountedPrice = useMemo(() => {
    return product.price * (1 - product.discount);
  }, [product.price, product.discount]);

  return (
    <div className="product-card">
      {/* Critical CSS inline */}
      <style>{`
        .product-card {
          transform: translateZ(0); /* GPU acceleration */
          will-change: transform;
        }
      `}</style>

      {/* Optimized image loading */}
      <picture>
        <source srcSet={`${product.image}.avif`} type="image/avif" />
        <source srcSet={`${product.image}.webp`} type="image/webp" />
        <img
          src={`${product.image}.jpg`}
          alt={product.name}
          loading="lazy"
          decoding="async"
        />
      </picture>

      <h3>{product.name}</h3>
      <p>${discountedPrice.toFixed(2)}</p>

      <button onClick={handleAddToCart}>
        Add to Cart
      </button>
    </div>
  );
});

// Virtual scrolling для больших списков
import { FixedSizeList as List } from 'react-window';

function ProductList({ products }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      <ProductCard product={products[index]} />
    </div>
  );

  return (
    <List
      height={600}
      itemCount={products.length}
      itemSize={250}
      itemData={products}
    >
      {Row}
    </List>
  );
}

// Performance monitoring
function PerformanceTracker() {
  useEffect(() => {
    // Core Web Vitals measurement
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.entryType === 'largest-contentful-paint') {
          console.log('LCP:', entry.startTime);
        }
        if (entry.entryType === 'layout-shift') {
          console.log('CLS:', entry.value);
        }
      }
    });

    observer.observe({ entryTypes: ['largest-contentful-paint', 'layout-shift'] });

    return () => observer.disconnect();
  }, []);

  return null;
}

export default function App() {
  return (
    <>
      <Helmet>
        {/* Resource hints для performance */}
        <link rel="preconnect" href="https://api.example.com" />
        <link rel="dns-prefetch" href="https://cdn.example.com" />
        <link rel="preload" href="/critical.css" as="style" />
      </Helmet>

      <PerformanceTracker />

      <Suspense fallback={<div>Loading...</div>}>
        <HeavyComponent />
      </Suspense>
    </>
  );
}
"""
}