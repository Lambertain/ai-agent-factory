"""
Web Application Performance конфигурация для Performance Optimization Agent.

Этот файл демонстрирует настройку агента для веб-приложений полного стека.
Включает оптимизацию frontend, backend и database слоев.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from ..dependencies import PerformanceOptimizationDependencies


@dataclass
class WebApplicationPerformanceDependencies(PerformanceOptimizationDependencies):
    """Конфигурация для веб-приложений полного стека."""

    # Основные настройки
    domain_type: str = "web_application"
    project_type: str = "full_stack"
    framework: str = "react"

    # Performance специфичные настройки
    performance_type: str = "web"
    optimization_strategy: str = "balanced"

    # Целевые метрики для веб-приложений
    target_metrics: Dict[str, Any] = field(default_factory=lambda: {
        "first_contentful_paint": 1500,  # ms
        "largest_contentful_paint": 2500,  # ms
        "cumulative_layout_shift": 0.1,
        "first_input_delay": 100,  # ms
        "total_blocking_time": 300,  # ms
        "bundle_size": 250,  # KB
        "page_load_time": 3000,  # ms
        "lighthouse_score": 90  # из 100
    })

    # Web-специфичные настройки
    enable_ssr: bool = True
    enable_code_splitting: bool = True
    enable_image_optimization: bool = True
    enable_cdn: bool = True
    enable_service_worker: bool = True

    def __post_init__(self):
        super().__post_init__()

        # Web application knowledge tags
        self.knowledge_tags.extend([
            "web-performance", "frontend", "backend", "full-stack",
            "lighthouse", "web-vitals", "bundle-optimization"
        ])

    def get_web_performance_config(self) -> Dict[str, Any]:
        """Специфичная конфигурация для веб-производительности."""
        return {
            "frontend": {
                "bundling": {
                    "code_splitting": self.enable_code_splitting,
                    "tree_shaking": True,
                    "dead_code_elimination": True,
                    "bundle_analysis": True
                },
                "assets": {
                    "image_optimization": self.enable_image_optimization,
                    "lazy_loading": True,
                    "critical_css": True,
                    "font_display_swap": True
                },
                "caching": {
                    "browser_cache": True,
                    "service_worker": self.enable_service_worker,
                    "cdn_integration": self.enable_cdn,
                    "static_asset_versioning": True
                }
            },
            "backend": {
                "rendering": {
                    "server_side_rendering": self.enable_ssr,
                    "static_generation": True,
                    "incremental_static_regeneration": True
                },
                "api": {
                    "response_compression": True,
                    "api_caching": True,
                    "database_optimization": True,
                    "connection_pooling": True
                }
            },
            "monitoring": {
                "real_user_monitoring": True,
                "synthetic_monitoring": True,
                "core_web_vitals": True,
                "lighthouse_ci": True
            }
        }

    def get_optimization_techniques(self) -> List[str]:
        """Список техник оптимизации для веб-приложений."""
        return [
            "code_splitting",
            "lazy_loading",
            "image_optimization",
            "critical_css_inlining",
            "font_optimization",
            "gzip_compression",
            "browser_caching",
            "cdn_delivery",
            "database_query_optimization",
            "api_response_caching",
            "static_asset_optimization",
            "lighthouse_optimization"
        ]

    def get_performance_budget(self) -> Dict[str, Dict[str, float]]:
        """Performance budget для веб-приложений."""
        return {
            "bundle_sizes": {
                "main_bundle": 150,  # KB
                "vendor_bundle": 200,  # KB
                "css_bundle": 50,  # KB
                "total_js": 350,  # KB
                "total_css": 100  # KB
            },
            "timing_metrics": {
                "ttfb": 200,  # ms - Time to First Byte
                "fcp": 1500,  # ms - First Contentful Paint
                "lcp": 2500,  # ms - Largest Contentful Paint
                "fid": 100,   # ms - First Input Delay
                "cls": 0.1,   # Cumulative Layout Shift
                "tbt": 300    # ms - Total Blocking Time
            },
            "resource_hints": {
                "preload_critical": 3,      # количество критических ресурсов
                "prefetch_next": 5,         # количество ресурсов для prefetch
                "preconnect_domains": 3     # количество доменов для preconnect
            }
        }


# Пример использования
def get_web_application_performance_dependencies() -> WebApplicationPerformanceDependencies:
    """Создать конфигурацию для веб-приложения."""
    return WebApplicationPerformanceDependencies(
        project_path="/web/application",
        project_name="Full Stack Web App",
        domain_type="web_application",
        project_type="full_stack",
        framework="react",
        performance_type="web",
        optimization_strategy="balanced",
        enable_ssr=True,
        enable_code_splitting=True,
        enable_image_optimization=True
    )


# Пример использования в React/Next.js приложении
WEB_PERFORMANCE_EXAMPLES = {
    "next_config": """
// next.config.js - Web Performance Optimization
const nextConfig = {
  // Bundle optimization
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // Image optimization
  images: {
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  // Bundle analysis
  ...(process.env.ANALYZE === 'true' && {
    webpack: (config) => {
      config.plugins.push(
        new (require('@next/bundle-analyzer'))({
          enabled: true,
          openAnalyzer: true,
        })
      );
      return config;
    },
  }),

  // Performance optimizations
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
  },

  // Compression
  compress: true,

  // Static optimization
  trailingSlash: false,

  // Headers for caching
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
""",

    "performance_component": """
// Performance-optimized React component
import { memo, lazy, Suspense } from 'react';
import Image from 'next/image';
import dynamic from 'next/dynamic';

// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));
const DynamicModal = dynamic(() => import('./Modal'), {
  ssr: false,
  loading: () => <div>Loading...</div>
});

// Memoized component for performance
const OptimizedProductCard = memo(({ product, config }) => {
  const performanceConfig = config.get_web_performance_config();

  return (
    <article className="product-card">
      {/* Optimized image loading */}
      {performanceConfig.frontend.assets.image_optimization && (
        <Image
          src={product.image}
          alt={product.name}
          width={300}
          height={200}
          priority={product.featured}
          placeholder="blur"
          blurDataURL="data:image/jpeg;base64,..."
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
      )}

      <div className="product-info">
        <h3>{product.name}</h3>
        <p>{product.description}</p>
        <span className="price">{product.price}</span>

        {/* Lazy load complex components */}
        {performanceConfig.frontend.assets.lazy_loading && (
          <Suspense fallback={<div>Loading chart...</div>}>
            <HeavyChart data={product.analytics} />
          </Suspense>
        )}
      </div>
    </article>
  );
});

OptimizedProductCard.displayName = 'OptimizedProductCard';

export default OptimizedProductCard;
""",

    "lighthouse_config": """
// lighthouse.config.js - Performance monitoring
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000'],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['error', {minScore: 0.9}],
        'categories:accessibility': ['error', {minScore: 0.9}],
        'categories:best-practices': ['error', {minScore: 0.9}],
        'categories:seo': ['error', {minScore: 0.9}],

        // Core Web Vitals
        'first-contentful-paint': ['error', {maxNumericValue: 1500}],
        'largest-contentful-paint': ['error', {maxNumericValue: 2500}],
        'cumulative-layout-shift': ['error', {maxNumericValue: 0.1}],
        'total-blocking-time': ['error', {maxNumericValue: 300}],

        // Bundle size limits
        'unused-javascript': ['error', {maxNumericValue: 50000}],
        'unminified-javascript': 'error',
        'unused-css-rules': ['error', {maxNumericValue: 20000}],
      },
    },
    upload: {
      target: 'lhci',
      serverBaseUrl: 'https://lighthouse-ci.example.com',
    },
  },
};
""",

    "web_vitals_tracking": """
// Web Vitals tracking for performance monitoring
import {getCLS, getFID, getFCP, getLCP, getTTFB} from 'web-vitals';

function sendToAnalytics(metric) {
  // Send to your analytics service
  if (typeof gtag !== 'undefined') {
    gtag('event', metric.name, {
      event_category: 'Web Vitals',
      event_label: metric.id,
      value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
      non_interaction: true,
    });
  }

  // Send to custom analytics endpoint
  fetch('/api/analytics/web-vitals', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: metric.name,
      value: metric.value,
      id: metric.id,
      url: location.href,
      timestamp: Date.now(),
    }),
  });
}

// Track all Core Web Vitals
getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);

// Performance observer for custom metrics
const performanceObserver = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    if (entry.entryType === 'navigation') {
      // Track page load performance
      const metrics = {
        dns_lookup: entry.domainLookupEnd - entry.domainLookupStart,
        tcp_connection: entry.connectEnd - entry.connectStart,
        request_response: entry.responseEnd - entry.requestStart,
        dom_processing: entry.domContentLoadedEventEnd - entry.responseEnd,
        load_complete: entry.loadEventEnd - entry.loadEventStart,
      };

      sendToAnalytics({
        name: 'navigation_timing',
        value: metrics,
        id: 'nav-timing',
      });
    }
  });
});

performanceObserver.observe({entryTypes: ['navigation', 'paint']});

export { sendToAnalytics };
"""
}