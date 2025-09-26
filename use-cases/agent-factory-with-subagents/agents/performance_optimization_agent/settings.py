#!/usr/bin/env python3
"""
Настройки для Performance Optimization Agent.

Универсальные настройки для оптимизации производительности любых типов проектов.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv


class PerformanceOptimizationSettings(BaseSettings):
    """Настройки Performance Optimization Agent с поддержкой переменных окружения."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM настройки
    llm_api_key: str = Field(..., description="API ключ для LLM")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Основная модель для оптимизации производительности"
    )

    # Специализированные модели для разных типов оптимизации
    llm_analysis_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для глубокого анализа производительности"
    )
    llm_monitoring_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Экономичная модель для мониторинга"
    )
    llm_profiling_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для профилирования кода"
    )

    # Alternative API keys for multi-provider setup
    gemini_api_key: str = Field(..., description="Google Gemini API ключ")

    # Cost optimization flags
    gemini_use_batch_api: bool = Field(default=True, description="Использовать Batch API для 50% скидки")
    qwen_enable_context_cache: bool = Field(default=True, description="Включить кэш контекста для Qwen")
    enable_smart_routing: bool = Field(default=True, description="Умная маршрутизация по стоимости")

    # Универсальные настройки доменов
    domain_type: str = Field(
        default="web_application",
        description="Тип домена: web_application, api, database, frontend, mobile, desktop"
    )
    project_type: str = Field(
        default="full_stack",
        description="Тип проекта: full_stack, spa, rest_api, graphql_api, microservices, monolith"
    )
    framework: str = Field(
        default="react",
        description="Framework: react, vue, angular, svelte, nextjs, express, fastapi, django, laravel"
    )
    performance_focus: str = Field(
        default="balanced",
        description="Фокус оптимизации: speed, memory, cpu, network, database, balanced"
    )

    # Performance targets (универсальные для разных доменов)
    target_response_time_ms: int = Field(
        default=200,
        description="Целевое время ответа в миллисекундах"
    )
    target_throughput_rps: int = Field(
        default=1000,
        description="Целевая пропускная способность в запросах в секунду"
    )
    target_error_rate: float = Field(
        default=0.001,
        description="Целевой процент ошибок (0.001 = 0.1%)"
    )
    target_cpu_usage: float = Field(
        default=0.7,
        description="Целевое использование CPU (0.7 = 70%)"
    )
    target_memory_usage: float = Field(
        default=0.8,
        description="Целевое использование памяти (0.8 = 80%)"
    )

    # Optimization features (адаптивные под домен)
    enable_caching: bool = Field(default=True, description="Включить стратегии кэширования")
    enable_compression: bool = Field(default=True, description="Включить сжатие данных")
    enable_lazy_loading: bool = Field(default=True, description="Включить ленивую загрузку")
    enable_bundling: bool = Field(default=True, description="Включить оптимизацию сборки")
    enable_cdn: bool = Field(default=True, description="Включить рекомендации CDN")
    enable_database_optimization: bool = Field(default=True, description="Включить оптимизацию БД")

    # Monitoring and profiling
    enable_monitoring: bool = Field(
        default=True,
        description="Включить мониторинг производительности"
    )
    enable_real_time_profiling: bool = Field(
        default=True,
        description="Включить профилирование в реальном времени"
    )
    enable_alerting: bool = Field(
        default=True,
        description="Включить систему уведомлений"
    )
    alert_threshold_multiplier: float = Field(
        default=1.5,
        description="Множитель для порогов срабатывания уведомлений"
    )

    # RAG и Knowledge Base
    knowledge_base_enabled: bool = Field(
        default=True,
        description="Использование базы знаний для оптимизации"
    )
    rag_search_threshold: float = Field(
        default=0.75,
        description="Порог релевантности для RAG поиска"
    )

    # Archon интеграция
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )
    archon_enabled: bool = Field(
        default=True,
        description="Включена ли интеграция с Archon"
    )

    # Context7 MCP Integration (для больших проектов)
    enable_context7_mcp: bool = Field(
        default=True,
        description="Включить Context7 MCP для управления контекстом"
    )
    context7_max_context_size: int = Field(
        default=100000,
        description="Максимальный размер контекста для Context7"
    )

    # Универсальные цветовые настройки (адаптируемые)
    performance_color_scheme: str = Field(
        default="modern_blue",
        description="Цветовая схема: modern_blue, green_eco, purple_tech, orange_energy, custom"
    )
    primary_color: str = Field(default="#3B82F6", description="Основной цвет интерфейса")
    success_color: str = Field(default="#10B981", description="Цвет успешных операций")
    warning_color: str = Field(default="#F59E0B", description="Цвет предупреждений")
    error_color: str = Field(default="#EF4444", description="Цвет ошибок")
    accent_color: str = Field(default="#8B5CF6", description="Акцентный цвет")


def load_performance_optimization_settings() -> PerformanceOptimizationSettings:
    """Загрузить настройки Performance Optimization Agent."""
    load_dotenv()

    try:
        return PerformanceOptimizationSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Performance Optimization Agent: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        if "gemini_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что GEMINI_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


def get_llm_model(optimization_type: str = "general"):
    """
    Получить сконфигурированную LLM модель для конкретного типа оптимизации.

    Args:
        optimization_type: Тип оптимизации (general, analysis, monitoring, profiling)

    Returns:
        Сконфигурированная модель
    """
    settings = load_performance_optimization_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    # Выбираем модель в зависимости от типа оптимизации
    model_mapping = {
        "general": settings.llm_model,
        "analysis": settings.llm_analysis_model,
        "monitoring": settings.llm_monitoring_model,
        "profiling": settings.llm_profiling_model
    }

    selected_model = model_mapping.get(optimization_type, settings.llm_model)
    return OpenAIModel(selected_model, provider=provider)


def get_domain_defaults(domain_type: str = None):
    """Получить настройки по умолчанию для конкретного домена."""
    settings = load_performance_optimization_settings()
    current_domain = domain_type or settings.domain_type

    domain_configs = {
        "web_application": {
            "target_response_time_ms": 200,
            "target_throughput_rps": 1000,
            "focus_areas": ["frontend", "backend", "database"],
            "key_metrics": ["TTFB", "FCP", "LCP", "CLS", "FID"],
            "optimization_strategies": ["caching", "compression", "lazy_loading", "cdn"]
        },
        "api": {
            "target_response_time_ms": 100,
            "target_throughput_rps": 5000,
            "focus_areas": ["latency", "throughput", "scalability"],
            "key_metrics": ["response_time", "throughput", "error_rate", "availability"],
            "optimization_strategies": ["connection_pooling", "caching", "pagination", "rate_limiting"]
        },
        "database": {
            "target_response_time_ms": 50,
            "target_throughput_rps": 10000,
            "focus_areas": ["query_optimization", "indexing", "caching"],
            "key_metrics": ["query_time", "connections", "cache_hit_ratio", "disk_io"],
            "optimization_strategies": ["indexing", "query_optimization", "connection_pooling", "partitioning"]
        },
        "frontend": {
            "target_response_time_ms": 300,
            "target_throughput_rps": 500,
            "focus_areas": ["user_experience", "loading_speed", "interactivity"],
            "key_metrics": ["FCP", "LCP", "CLS", "FID", "TTI", "Bundle Size"],
            "optimization_strategies": ["code_splitting", "lazy_loading", "asset_optimization", "service_worker"]
        },
        "mobile": {
            "target_response_time_ms": 500,
            "target_throughput_rps": 200,
            "focus_areas": ["battery_usage", "memory", "network_usage"],
            "key_metrics": ["startup_time", "memory_usage", "battery_drain", "network_requests"],
            "optimization_strategies": ["offline_support", "image_optimization", "data_compression", "background_sync"]
        }
    }

    return domain_configs.get(current_domain, domain_configs["web_application"])


def get_framework_config(framework: str = None):
    """Получить специфичную конфигурацию для framework."""
    settings = load_performance_optimization_settings()
    current_framework = framework or settings.framework

    framework_configs = {
        "react": {
            "bundle_analyzer": "webpack-bundle-analyzer",
            "performance_tools": ["React DevTools Profiler", "Lighthouse", "Web Vitals"],
            "optimization_patterns": ["React.memo", "useMemo", "useCallback", "lazy loading"],
            "build_optimizations": ["tree shaking", "code splitting", "chunk optimization"]
        },
        "nextjs": {
            "bundle_analyzer": "@next/bundle-analyzer",
            "performance_tools": ["Next.js Speed Insights", "Lighthouse", "Core Web Vitals"],
            "optimization_patterns": ["SSG/SSR optimization", "Image optimization", "Font optimization"],
            "build_optimizations": ["automatic code splitting", "tree shaking", "dynamic imports"]
        },
        "vue": {
            "bundle_analyzer": "webpack-bundle-analyzer",
            "performance_tools": ["Vue DevTools", "Lighthouse", "Web Vitals"],
            "optimization_patterns": ["v-once", "v-memo", "async components", "keep-alive"],
            "build_optimizations": ["tree shaking", "code splitting", "chunk optimization"]
        },
        "fastapi": {
            "performance_tools": ["uvicorn", "gunicorn", "async profiling"],
            "optimization_patterns": ["async/await", "database connection pooling", "caching"],
            "build_optimizations": ["Docker optimization", "dependency injection", "background tasks"]
        },
        "django": {
            "performance_tools": ["django-debug-toolbar", "django-silk", "APM tools"],
            "optimization_patterns": ["select_related", "prefetch_related", "database indexing"],
            "build_optimizations": ["static file optimization", "template caching", "database optimization"]
        }
    }

    return framework_configs.get(current_framework, framework_configs.get("react", {}))


def get_cost_optimization_config():
    """Получить конфигурацию оптимизации стоимости моделей."""
    settings = load_performance_optimization_settings()

    return {
        "smart_routing_enabled": settings.enable_smart_routing,
        "batch_api_enabled": settings.gemini_use_batch_api,
        "context_cache_enabled": settings.qwen_enable_context_cache,
        "model_costs": {
            "qwen2.5-72b-instruct": {"input": 2.0, "output": 3.0},  # $/1M tokens
            "qwen2.5-coder-32b-instruct": {"input": 1.0, "output": 2.0},
            "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40}
        },
        "optimization_strategies": {
            "use_lite_models_for_monitoring": True,
            "use_coder_models_for_code_analysis": True,
            "use_premium_models_for_architecture": True,
            "enable_context_compression": True
        }
    }