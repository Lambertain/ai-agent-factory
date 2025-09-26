"""
Frontend Performance конфигурация для Performance Optimization Agent.

Этот файл демонстрирует настройку агента для оптимизации производительности frontend приложений.
Включает bundle optimization, lazy loading, image optimization и Core Web Vitals.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from ..dependencies import PerformanceOptimizationDependencies


@dataclass
class FrontendPerformanceDependencies(PerformanceOptimizationDependencies):
    """Конфигурация для Frontend Performance Optimization."""

    # Основные настройки
    domain_type: str = "frontend"
    project_type: str = "react_spa"

    # Bundle optimization
    enable_code_splitting: bool = True
    enable_tree_shaking: bool = True
    enable_bundle_analysis: bool = True
    enable_compression: bool = True

    # Loading optimization
    enable_lazy_loading: bool = True
    enable_preloading: bool = True
    enable_prefetching: bool = True
    enable_service_worker: bool = True

    # Image optimization
    enable_image_optimization: bool = True
    enable_responsive_images: bool = True
    enable_modern_formats: bool = True
    image_quality: int = 80

    # Core Web Vitals targets
    target_fcp_ms: int = 1800  # First Contentful Paint
    target_lcp_ms: int = 2500  # Largest Contentful Paint
    target_fid_ms: int = 100   # First Input Delay
    target_cls_score: float = 0.1  # Cumulative Layout Shift

    def get_webpack_config(self) -> Dict[str, Any]:
        """Конфигурация Webpack optimization."""
        return {
            "optimization": {
                "splitChunks": {
                    "chunks": "all",
                    "cacheGroups": {
                        "vendor": {
                            "test": "/[\\\\/]node_modules[\\\\/]/",
                            "name": "vendors",
                            "chunks": "all",
                            "priority": 10
                        },
                        "common": {
                            "name": "common",
                            "minChunks": 2,
                            "priority": 5,
                            "chunks": "all",
                            "enforce": True
                        },
                        "react": {
                            "test": "/[\\\\/]node_modules[\\\\/](react|react-dom)[\\\\/]/",
                            "name": "react",
                            "chunks": "all",
                            "priority": 20
                        }
                    }
                },
                "usedExports": self.enable_tree_shaking,
                "sideEffects": False,
                "minimizer": [
                    {
                        "terser": {
                            "terserOptions": {
                                "compress": {
                                    "drop_console": True,
                                    "drop_debugger": True,
                                    "pure_funcs": ["console.log", "console.info"]
                                },
                                "mangle": True,
                                "format": {
                                    "comments": False
                                }
                            }
                        }
                    }
                ]
            },
            "plugins": [
                {
                    "compression": {
                        "enabled": self.enable_compression,
                        "algorithm": "gzip",
                        "test": "\\.(js|css|html|svg)$",
                        "threshold": 8192,
                        "minRatio": 0.8
                    }
                },
                {
                    "bundle_analyzer": {
                        "enabled": self.enable_bundle_analysis,
                        "analyzerMode": "static",
                        "generateStatsFile": True,
                        "openAnalyzer": False
                    }
                }
            ],
            "performance": {
                "hints": "error",
                "maxEntrypointSize": 250000,
                "maxAssetSize": 250000
            }
        }

    def get_vite_config(self) -> Dict[str, Any]:
        """Конфигурация Vite optimization."""
        return {
            "build": {
                "target": "es2015",
                "outDir": "dist",
                "assetsDir": "assets",
                "minify": "terser",
                "terserOptions": {
                    "compress": {
                        "drop_console": True,
                        "drop_debugger": True
                    }
                },
                "rollupOptions": {
                    "output": {
                        "manualChunks": {
                            "vendor": ["react", "react-dom"],
                            "ui": ["@mui/material", "@emotion/react"],
                            "utils": ["lodash", "date-fns", "axios"]
                        }
                    }
                },
                "chunkSizeWarningLimit": 500,
                "reportCompressedSize": False
            },
            "plugins": [
                "vite-plugin-pwa" if self.enable_service_worker else None,
                "vite-plugin-imagemin" if self.enable_image_optimization else None,
                "@vitejs/plugin-react"
            ],
            "server": {
                "hmr": True,
                "host": True
            }
        }

    def get_image_optimization_config(self) -> Dict[str, Any]:
        """Конфигурация image optimization."""
        return {
            "formats": {
                "avif": {
                    "enabled": self.enable_modern_formats,
                    "quality": self.image_quality,
                    "effort": 4
                },
                "webp": {
                    "enabled": self.enable_modern_formats,
                    "quality": self.image_quality,
                    "method": 4
                },
                "jpeg": {
                    "quality": self.image_quality,
                    "progressive": True
                },
                "png": {
                    "quality": [0.6, 0.8],
                    "compressionLevel": 9
                }
            },
            "responsive_images": {
                "enabled": self.enable_responsive_images,
                "breakpoints": [320, 640, 768, 1024, 1280, 1536],
                "formats": ["avif", "webp", "jpg"] if self.enable_modern_formats else ["jpg"],
                "loading": "lazy" if self.enable_lazy_loading else "eager"
            },
            "optimization": {
                "mozjpeg": True,
                "pngquant": True,
                "svgo": {
                    "plugins": [
                        {"removeViewBox": False},
                        {"removeDimensions": True}
                    ]
                }
            }
        }

    def get_loading_optimization_config(self) -> Dict[str, Any]:
        """Конфигурация loading optimization."""
        return {
            "code_splitting": {
                "enabled": self.enable_code_splitting,
                "strategies": [
                    "route_based",
                    "component_based",
                    "feature_based"
                ],
                "loading_states": True,
                "error_boundaries": True
            },
            "lazy_loading": {
                "enabled": self.enable_lazy_loading,
                "components": True,
                "images": True,
                "intersection_observer": True,
                "loading_placeholder": True
            },
            "preloading": {
                "enabled": self.enable_preloading,
                "critical_resources": [
                    {"type": "font", "as": "font", "crossorigin": "anonymous"},
                    {"type": "style", "as": "style"},
                    {"type": "script", "as": "script"}
                ],
                "prefetch_routes": self.enable_prefetching
            },
            "service_worker": {
                "enabled": self.enable_service_worker,
                "caching_strategy": "cache_first",
                "runtime_caching": [
                    {
                        "urlPattern": "/api/.*",
                        "handler": "network_first",
                        "options": {"cacheName": "api-cache", "expiration": {"maxEntries": 50}}
                    },
                    {
                        "urlPattern": ".*\\.(js|css)$",
                        "handler": "cache_first",
                        "options": {"cacheName": "static-resources"}
                    }
                ]
            }
        }

    def get_core_web_vitals_config(self) -> Dict[str, Any]:
        """Конфигурация Core Web Vitals monitoring."""
        return {
            "metrics": {
                "fcp": {
                    "target": self.target_fcp_ms,
                    "good": 1800,
                    "needs_improvement": 3000
                },
                "lcp": {
                    "target": self.target_lcp_ms,
                    "good": 2500,
                    "needs_improvement": 4000
                },
                "fid": {
                    "target": self.target_fid_ms,
                    "good": 100,
                    "needs_improvement": 300
                },
                "cls": {
                    "target": self.target_cls_score,
                    "good": 0.1,
                    "needs_improvement": 0.25
                },
                "ttfb": {
                    "target": 800,
                    "good": 800,
                    "needs_improvement": 1800
                }
            },
            "measurement": {
                "web_vitals_library": True,
                "performance_observer": True,
                "long_tasks_observer": True,
                "layout_shift_observer": True
            },
            "reporting": {
                "console_logging": True,
                "analytics_integration": True,
                "real_user_monitoring": True,
                "lab_testing": True
            }
        }

    def get_performance_budget(self) -> Dict[str, Any]:
        """Performance budget для frontend."""
        return {
            "bundle_sizes": {
                "javascript_main": "150KB",
                "javascript_vendor": "200KB",
                "css_main": "50KB",
                "images_total": "500KB",
                "fonts_total": "100KB"
            },
            "network": {
                "requests_total": 50,
                "requests_initial": 10,
                "transfer_size": "1MB",
                "resource_size": "2MB"
            },
            "runtime": {
                "main_thread_blocking": "200ms",
                "javascript_execution": "400ms",
                "rendering_tasks": "16ms"
            },
            "metrics": {
                "first_contentful_paint": f"{self.target_fcp_ms}ms",
                "largest_contentful_paint": f"{self.target_lcp_ms}ms",
                "first_input_delay": f"{self.target_fid_ms}ms",
                "cumulative_layout_shift": str(self.target_cls_score)
            }
        }


# Пример использования
def get_frontend_performance_dependencies() -> FrontendPerformanceDependencies:
    """Создать конфигурацию для Frontend Performance Optimization."""
    return FrontendPerformanceDependencies(
        api_key="your-api-key",
        domain_type="frontend",
        project_type="react_spa",
        enable_code_splitting=True,
        enable_lazy_loading=True,
        enable_image_optimization=True,
        target_fcp_ms=1800,
        target_lcp_ms=2500
    )


# Примеры оптимизации
FRONTEND_PERFORMANCE_EXAMPLES = {
    "react_optimization": """
// React Performance Optimization Best Practices
import React, {
    memo,
    useMemo,
    useCallback,
    lazy,
    Suspense,
    startTransition
} from 'react';
import { ErrorBoundary } from 'react-error-boundary';

// 1. КОМПОНЕНТНАЯ ОПТИМИЗАЦИЯ
// Мемоизированный компонент для предотвращения ненужных ре-рендеров
const ProductCard = memo(({ product, onAddToCart }) => {
    // Мемоизация вычислений
    const discountedPrice = useMemo(() => {
        return product.price * (1 - product.discount);
    }, [product.price, product.discount]);

    // Мемоизация колбэков
    const handleAddToCart = useCallback(() => {
        onAddToCart(product.id);
    }, [product.id, onAddToCart]);

    return (
        <div className="product-card">
            <img
                src={product.image}
                alt={product.name}
                loading="lazy"
                decoding="async"
            />
            <h3>{product.name}</h3>
            <p>${discountedPrice.toFixed(2)}</p>
            <button onClick={handleAddToCart}>
                Add to Cart
            </button>
        </div>
    );
});

// 2. CODE SPLITTING с React.lazy
const ProductDetails = lazy(() =>
    import('./ProductDetails').then(module => ({
        default: module.ProductDetails
    }))
);

const ShoppingCart = lazy(() => import('./ShoppingCart'));

// 3. ВИРТУАЛИЗАЦИЯ для больших списков
import { FixedSizeList as List } from 'react-window';

function ProductList({ products }) {
    const Row = useCallback(({ index, style }) => (
        <div style={style}>
            <ProductCard product={products[index]} />
        </div>
    ), [products]);

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

// 4. CONCURRENT FEATURES
function App() {
    const [query, setQuery] = useState('');
    const [products, setProducts] = useState([]);
    const [isPending, startTransition] = useTransition();

    const handleSearch = useCallback((searchQuery) => {
        startTransition(() => {
            // Неблокирующий поиск
            searchProducts(searchQuery).then(setProducts);
        });
    }, []);

    const deferredQuery = useDeferredValue(query);

    return (
        <div className="app">
            <SearchInput
                value={query}
                onChange={setQuery}
                onSearch={handleSearch}
            />

            {isPending && <div>Searching...</div>}

            <ErrorBoundary fallback={<div>Something went wrong</div>}>
                <Suspense fallback={<div>Loading product details...</div>}>
                    <ProductDetails query={deferredQuery} />
                </Suspense>
            </ErrorBoundary>

            <ProductList products={products} />
        </div>
    );
}

// 5. PERFORMANCE MONITORING
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function measurePerformance() {
    getCLS(console.log);
    getFID(console.log);
    getFCP(console.log);
    getLCP(console.log);
    getTTFB(console.log);
}

// Запуск мониторинга
if (typeof window !== 'undefined') {
    measurePerformance();
}

export default App;
""",

    "image_optimization": """
// Современная оптимизация изображений

// 1. PICTURE ELEMENT с современными форматами
function OptimizedImage({ src, alt, sizes, className }) {
    const imageBase = src.replace(/\.[^/.]+$/, "");

    return (
        <picture className={className}>
            {/* AVIF - лучшее сжатие */}
            <source
                srcSet={`
                    ${imageBase}-320.avif 320w,
                    ${imageBase}-640.avif 640w,
                    ${imageBase}-1024.avif 1024w,
                    ${imageBase}-1280.avif 1280w
                `}
                sizes={sizes}
                type="image/avif"
            />

            {/* WebP - хорошая поддержка */}
            <source
                srcSet={`
                    ${imageBase}-320.webp 320w,
                    ${imageBase}-640.webp 640w,
                    ${imageBase}-1024.webp 1024w,
                    ${imageBase}-1280.webp 1280w
                `}
                sizes={sizes}
                type="image/webp"
            />

            {/* Fallback JPEG */}
            <img
                src={`${imageBase}-640.jpg`}
                srcSet={`
                    ${imageBase}-320.jpg 320w,
                    ${imageBase}-640.jpg 640w,
                    ${imageBase}-1024.jpg 1024w,
                    ${imageBase}-1280.jpg 1280w
                `}
                sizes={sizes}
                alt={alt}
                loading="lazy"
                decoding="async"
            />
        </picture>
    );
}

// 2. INTERSECTION OBSERVER для lazy loading
import { useEffect, useRef, useState } from 'react';

function useLazyImage(src) {
    const [imageSrc, setImageSrc] = useState(null);
    const [imageRef, setImageRef] = useState();

    useEffect(() => {
        let observer;

        if (imageRef && imageSrc !== src) {
            observer = new IntersectionObserver(
                entries => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            setImageSrc(src);
                            observer.unobserve(imageRef);
                        }
                    });
                },
                { threshold: 0.1, rootMargin: '50px' }
            );
            observer.observe(imageRef);
        }

        return () => {
            if (observer && observer.unobserve) {
                observer.unobserve(imageRef);
            }
        };
    }, [imageRef, imageSrc, src]);

    return [setImageRef, imageSrc];
}

function LazyImage({ src, alt, placeholder, ...props }) {
    const [imageRef, imageSrc] = useLazyImage(src);

    return (
        <img
            ref={imageRef}
            src={imageSrc || placeholder}
            alt={alt}
            {...props}
        />
    );
}

// 3. RESPONSIVE IMAGES HOOK
function useResponsiveImage(baseSrc, breakpoints = [320, 640, 768, 1024, 1280]) {
    const [currentSrc, setCurrentSrc] = useState(baseSrc);

    useEffect(() => {
        function updateImage() {
            const width = window.innerWidth;
            const devicePixelRatio = window.devicePixelRatio || 1;
            const targetWidth = width * devicePixelRatio;

            // Найти ближайший размер
            const closestBreakpoint = breakpoints.reduce((prev, curr) =>
                Math.abs(curr - targetWidth) < Math.abs(prev - targetWidth) ? curr : prev
            );

            const extension = baseSrc.split('.').pop();
            const baseWithoutExt = baseSrc.replace(/\.[^/.]+$/, "");
            setCurrentSrc(`${baseWithoutExt}-${closestBreakpoint}.${extension}`);
        }

        updateImage();
        window.addEventListener('resize', updateImage);

        return () => window.removeEventListener('resize', updateImage);
    }, [baseSrc, breakpoints]);

    return currentSrc;
}
""",

    "service_worker": """
// Service Worker для кэширования и offline поддержки

// sw.js - Service Worker
const CACHE_NAME = 'app-cache-v1';
const STATIC_CACHE = 'static-cache-v1';
const API_CACHE = 'api-cache-v1';

// Ресурсы для предварительного кэширования
const PRECACHE_URLS = [
    '/',
    '/static/js/main.js',
    '/static/css/main.css',
    '/static/fonts/Inter-Regular.woff2',
    '/manifest.json'
];

// Установка Service Worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => cache.addAll(PRECACHE_URLS))
            .then(() => self.skipWaiting())
    );
});

// Активация Service Worker
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME &&
                        cacheName !== STATIC_CACHE &&
                        cacheName !== API_CACHE) {
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch обработчик с разными стратегиями кэширования
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    // API запросы - Network First
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(networkFirst(request, API_CACHE));
    }
    // Статические ресурсы - Cache First
    else if (request.destination === 'script' ||
             request.destination === 'style' ||
             request.destination === 'font') {
        event.respondWith(cacheFirst(request, STATIC_CACHE));
    }
    // Изображения - Cache First с fallback
    else if (request.destination === 'image') {
        event.respondWith(cacheFirst(request, CACHE_NAME));
    }
    // HTML страницы - Network First с fallback
    else if (request.destination === 'document') {
        event.respondWith(networkFirst(request, CACHE_NAME));
    }
    // Остальное - Network First
    else {
        event.respondWith(fetch(request));
    }
});

// Network First стратегия
async function networkFirst(request, cacheName) {
    try {
        const networkResponse = await fetch(request);

        if (networkResponse.ok) {
            const cache = await caches.open(cacheName);
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        const cachedResponse = await caches.match(request);
        return cachedResponse || new Response('Offline', { status: 503 });
    }
}

// Cache First стратегия
async function cacheFirst(request, cacheName) {
    const cachedResponse = await caches.match(request);

    if (cachedResponse) {
        return cachedResponse;
    }

    try {
        const networkResponse = await fetch(request);

        if (networkResponse.ok) {
            const cache = await caches.open(cacheName);
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        return new Response('Resource not available', { status: 404 });
    }
}

// Регистрация Service Worker в приложении
// register-sw.js
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);

                // Проверка обновлений каждые 5 минут
                setInterval(() => {
                    registration.update();
                }, 5 * 60 * 1000);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });

    // Обработка обновлений Service Worker
    navigator.serviceWorker.addEventListener('controllerchange', () => {
        window.location.reload();
    });
}

// PWA Manifest
const manifest = {
    "name": "Performance Optimized App",
    "short_name": "PerfApp",
    "description": "High-performance web application",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#000000",
    "icons": [
        {
            "src": "/icons/icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "/icons/icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
};
""",

    "performance_monitoring": """
// Comprehensive Performance Monitoring

import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

class PerformanceMonitor {
    constructor() {
        this.metrics = {};
        this.observers = new Map();
        this.init();
    }

    init() {
        // Core Web Vitals
        this.measureCoreWebVitals();

        // Custom metrics
        this.measureResourceTiming();
        this.measureLongTasks();
        this.measureLayoutShifts();
        this.measureMemoryUsage();

        // Navigation timing
        this.measureNavigationTiming();
    }

    measureCoreWebVitals() {
        getCLS(this.handleMetric.bind(this, 'CLS'));
        getFID(this.handleMetric.bind(this, 'FID'));
        getFCP(this.handleMetric.bind(this, 'FCP'));
        getLCP(this.handleMetric.bind(this, 'LCP'));
        getTTFB(this.handleMetric.bind(this, 'TTFB'));
    }

    measureResourceTiming() {
        const observer = new PerformanceObserver((list) => {
            list.getEntries().forEach(entry => {
                if (entry.entryType === 'resource') {
                    this.handleResourceTiming(entry);
                }
            });
        });

        observer.observe({ entryTypes: ['resource'] });
        this.observers.set('resource', observer);
    }

    measureLongTasks() {
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                list.getEntries().forEach(entry => {
                    this.handleMetric('LONG_TASK', {
                        duration: entry.duration,
                        startTime: entry.startTime,
                        attribution: entry.attribution
                    });
                });
            });

            observer.observe({ entryTypes: ['longtask'] });
            this.observers.set('longtask', observer);
        }
    }

    measureLayoutShifts() {
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                list.getEntries().forEach(entry => {
                    if (entry.entryType === 'layout-shift' && !entry.hadRecentInput) {
                        this.handleMetric('LAYOUT_SHIFT', {
                            value: entry.value,
                            sources: entry.sources
                        });
                    }
                });
            });

            observer.observe({ entryTypes: ['layout-shift'] });
            this.observers.set('layout-shift', observer);
        }
    }

    measureMemoryUsage() {
        if ('memory' in performance) {
            setInterval(() => {
                const memory = performance.memory;
                this.handleMetric('MEMORY', {
                    usedJSHeapSize: memory.usedJSHeapSize,
                    totalJSHeapSize: memory.totalJSHeapSize,
                    jsHeapSizeLimit: memory.jsHeapSizeLimit
                });
            }, 10000); // Каждые 10 секунд
        }
    }

    measureNavigationTiming() {
        window.addEventListener('load', () => {
            const navigation = performance.getEntriesByType('navigation')[0];

            this.handleMetric('NAVIGATION', {
                domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                domComplete: navigation.domComplete - navigation.navigationStart,
                loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
                firstByte: navigation.responseStart - navigation.requestStart,
                dnsLookup: navigation.domainLookupEnd - navigation.domainLookupStart,
                tcpConnect: navigation.connectEnd - navigation.connectStart,
                sslConnect: navigation.secureConnectionStart > 0 ?
                    navigation.connectEnd - navigation.secureConnectionStart : 0
            });
        });
    }

    handleResourceTiming(entry) {
        const resourceType = this.getResourceType(entry.name);

        this.handleMetric('RESOURCE_TIMING', {
            name: entry.name,
            type: resourceType,
            duration: entry.duration,
            transferSize: entry.transferSize,
            encodedBodySize: entry.encodedBodySize,
            decodedBodySize: entry.decodedBodySize,
            initiatorType: entry.initiatorType
        });
    }

    getResourceType(url) {
        if (url.includes('.js')) return 'script';
        if (url.includes('.css')) return 'style';
        if (url.match(/\.(jpg|jpeg|png|gif|webp|avif)$/)) return 'image';
        if (url.includes('.woff')) return 'font';
        if (url.includes('/api/')) return 'api';
        return 'other';
    }

    handleMetric(name, metric) {
        this.metrics[name] = metric;

        // Логирование в консоль
        console.log(`${name}:`, metric);

        // Отправка в аналитику
        this.sendToAnalytics(name, metric);

        // Проверка пороговых значений
        this.checkThresholds(name, metric);
    }

    sendToAnalytics(name, metric) {
        // Отправка в Google Analytics 4
        if (typeof gtag !== 'undefined') {
            gtag('event', 'web_vitals', {
                metric_name: name,
                metric_value: metric.value || metric.duration || metric,
                custom_parameter: JSON.stringify(metric)
            });
        }

        // Отправка в собственную аналитику
        fetch('/api/analytics/performance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                metric: name,
                value: metric,
                timestamp: Date.now(),
                userAgent: navigator.userAgent,
                url: window.location.href
            })
        }).catch(console.error);
    }

    checkThresholds(name, metric) {
        const thresholds = {
            CLS: { good: 0.1, poor: 0.25 },
            FID: { good: 100, poor: 300 },
            FCP: { good: 1800, poor: 3000 },
            LCP: { good: 2500, poor: 4000 },
            TTFB: { good: 800, poor: 1800 }
        };

        const threshold = thresholds[name];
        if (!threshold) return;

        const value = metric.value || metric.duration || metric;

        if (value > threshold.poor) {
            console.warn(`${name} is poor: ${value}`);
            this.triggerAlert(name, value, 'poor');
        } else if (value > threshold.good) {
            console.info(`${name} needs improvement: ${value}`);
        }
    }

    triggerAlert(metric, value, level) {
        // Уведомление команды разработки
        if (level === 'poor' && window.location.hostname !== 'localhost') {
            fetch('/api/alerts/performance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    metric,
                    value,
                    level,
                    url: window.location.href,
                    userAgent: navigator.userAgent,
                    timestamp: Date.now()
                })
            });
        }
    }

    getReport() {
        return {
            metrics: this.metrics,
            timestamp: Date.now(),
            url: window.location.href
        };
    }

    destroy() {
        this.observers.forEach(observer => observer.disconnect());
        this.observers.clear();
    }
}

// Инициализация мониторинга
const performanceMonitor = new PerformanceMonitor();

// Экспорт для использования в других модулях
export default performanceMonitor;
"""
}