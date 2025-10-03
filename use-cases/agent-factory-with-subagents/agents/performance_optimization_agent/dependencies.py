"""
Зависимости Performance Optimization Agent.

Универсальные зависимости для оптимизации производительности любых типов проектов.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv


class PerformanceAgentSettings(BaseSettings):
    """Настройки Performance Optimization Agent с поддержкой переменных окружения."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # API ключи
    llm_api_key: str = Field(..., description="API-ключ LLM провайдера")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для оптимизации"
    )

    # Archon RAG интеграция
    archon_api_url: str = Field(
        default="http://localhost:3737",
        description="URL Archon API"
    )
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )

    # Performance настройки
    performance_domain_type: str = Field(
        default="web_application",
        description="Тип домена: web_application, api, database, frontend"
    )
    performance_project_type: str = Field(
        default="full_stack",
        description="Тип проекта: full_stack, spa, rest_api, postgresql, etc."
    )
    performance_framework: str = Field(
        default="react",
        description="Framework: react, vue, fastapi, django, express, etc."
    )

    # Оптимизация настройки
    enable_caching: bool = Field(default=True, description="Включить кэширование")
    enable_compression: bool = Field(default=True, description="Включить сжатие")
    enable_monitoring: bool = Field(default=True, description="Включить мониторинг")
    enable_lazy_loading: bool = Field(default=True, description="Включить lazy loading")

    # Performance targets
    target_response_time_ms: int = Field(default=200, description="Целевое время ответа в мс")
    target_throughput_rps: int = Field(default=1000, description="Целевая пропускная способность RPS")
    target_error_rate: float = Field(default=0.001, description="Целевой процент ошибок")

    # Цветовая палитра (универсальная)
    primary_color: str = Field(default="#3B82F6", description="Основной цвет")
    secondary_color: str = Field(default="#10B981", description="Вторичный цвет")
    accent_color: str = Field(default="#8B5CF6", description="Акцентный цвет")
    warning_color: str = Field(default="#F59E0B", description="Цвет предупреждений")
    error_color: str = Field(default="#EF4444", description="Цвет ошибок")


def load_performance_settings() -> PerformanceAgentSettings:
    """Загрузить настройки агента производительности."""
    load_dotenv()

    try:
        return PerformanceAgentSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Performance Agent: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедись, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e


@dataclass
class PerformanceOptimizationDependencies:
    """Универсальные зависимости для Performance Optimization Agent."""

    # Основные настройки
    api_key: str
    agent_name: str = "performance_optimization"  # For RAG protection
    project_path: str = ""

    # Универсальные типы проектов
    domain_type: str = "web_application"  # web_application, api, database, frontend, mobile
    project_type: str = "full_stack"     # full_stack, spa, rest_api, postgresql, react_native
    framework: str = "react"             # react, vue, fastapi, django, express, laravel

    # Специализированные настройки производительности
    performance_type: str = "web"        # web, api, database, frontend, backend, mobile
    optimization_strategy: str = "balanced"  # speed, memory, cpu, network, balanced
    target_metrics: Dict[str, Any] = field(default_factory=dict)

    # RAG и Knowledge Base
    knowledge_tags: List[str] = field(
        default_factory=lambda: ["performance-optimization", "agent-knowledge", "pydantic-ai"]
    )
    knowledge_domain: str | None = None
    archon_project_id: str | None = None

    # Context7 MCP Integration
    enable_context7_mcp: bool = True
    context7_library_cache: Dict[str, str] = field(default_factory=dict)
    context7_docs_cache: Dict[str, Dict] = field(default_factory=dict)

    # Performance оптимизация настройки
    enable_caching: bool = True
    enable_compression: bool = True
    enable_monitoring: bool = True
    enable_lazy_loading: bool = True
    enable_bundling: bool = True

    # Performance targets (универсальные)
    target_response_time_ms: int = 200
    target_throughput_rps: int = 1000
    target_error_rate: float = 0.001
    target_cpu_usage: float = 0.7
    target_memory_usage: float = 0.8

    # Мониторинг настройки
    enable_real_time_monitoring: bool = True
    enable_alerting: bool = True
    alert_threshold_multiplier: float = 1.5

    # Настройки для различных доменов
    frontend_settings: Dict[str, Any] = field(default_factory=dict)
    backend_settings: Dict[str, Any] = field(default_factory=dict)
    database_settings: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация конфигурации после создания."""
        if not self.knowledge_tags:
            self.knowledge_tags = [
                "performance-optimization",
                "agent-knowledge",
                "pydantic-ai",
                self.domain_type,
                self.framework
            ]

        # Настройки по умолчанию для разных доменов
        if not self.frontend_settings and self.domain_type in ["frontend", "web_application"]:
            self.frontend_settings = {
                "bundle_optimization": self.enable_bundling,
                "lazy_loading": self.enable_lazy_loading,
                "image_optimization": True,
                "css_optimization": True,
                "js_minification": True
            }

        if not self.backend_settings and self.domain_type in ["api", "backend", "web_application"]:
            self.backend_settings = {
                "response_caching": self.enable_caching,
                "compression": self.enable_compression,
                "connection_pooling": True,
                "query_optimization": True
            }

        if not self.database_settings and self.domain_type in ["database", "web_application"]:
            self.database_settings = {
                "query_optimization": True,
                "indexing": True,
                "connection_pooling": True,
                "query_caching": self.enable_caching
            }

    def get_domain_config(self) -> Dict[str, Any]:
        """Получить конфигурацию для текущего домена."""
        configs = {
            "frontend": self.frontend_settings,
            "backend": self.backend_settings,
            "database": self.database_settings,
            "web_application": {
                **self.frontend_settings,
                **self.backend_settings,
                **self.database_settings
            }
        }
        return configs.get(self.domain_type, {})

    def get_framework_specific_config(self) -> Dict[str, Any]:
        """Получить конфигурацию для конкретного фреймворка."""
        framework_configs = {
            "react": {
                "code_splitting": True,
                "memo_optimization": True,
                "bundle_analysis": True,
                "dev_tools": "React DevTools"
            },
            "vue": {
                "tree_shaking": True,
                "async_components": True,
                "performance_devtools": True,
                "dev_tools": "Vue DevTools"
            },
            "fastapi": {
                "async_optimization": True,
                "dependency_injection": True,
                "response_models": True,
                "docs_optimization": True
            },
            "django": {
                "query_optimization": True,
                "template_caching": True,
                "static_files_optimization": True,
                "db_optimization": True
            },
            "express": {
                "middleware_optimization": True,
                "async_handlers": True,
                "clustering": True,
                "compression_middleware": True
            }
        }
        return framework_configs.get(self.framework, {})

    def get_monitoring_config(self) -> Dict[str, Any]:
        """Получить конфигурацию мониторинга."""
        return {
            "enabled": self.enable_monitoring,
            "real_time": self.enable_real_time_monitoring,
            "alerting": self.enable_alerting,
            "metrics": {
                "response_time": {
                    "target": self.target_response_time_ms,
                    "alert_threshold": self.target_response_time_ms * self.alert_threshold_multiplier
                },
                "throughput": {
                    "target": self.target_throughput_rps,
                    "alert_threshold": self.target_throughput_rps * 0.8
                },
                "error_rate": {
                    "target": self.target_error_rate,
                    "alert_threshold": self.target_error_rate * 2
                },
                "cpu_usage": {
                    "target": self.target_cpu_usage,
                    "alert_threshold": self.target_cpu_usage * self.alert_threshold_multiplier
                },
                "memory_usage": {
                    "target": self.target_memory_usage,
                    "alert_threshold": self.target_memory_usage * self.alert_threshold_multiplier
                }
            }
        }

    def get_optimization_strategies(self) -> List[str]:
        """Получить список стратегий оптимизации для текущего домена."""
        strategies = []

        if self.domain_type in ["frontend", "web_application"]:
            strategies.extend([
                "bundle_optimization",
                "code_splitting",
                "lazy_loading",
                "image_optimization",
                "css_optimization"
            ])

        if self.domain_type in ["api", "backend", "web_application"]:
            strategies.extend([
                "response_caching",
                "compression",
                "connection_pooling",
                "rate_limiting",
                "async_processing"
            ])

        if self.domain_type in ["database", "web_application"]:
            strategies.extend([
                "query_optimization",
                "indexing",
                "connection_pooling",
                "query_caching",
                "partition_strategies"
            ])

        return list(set(strategies))  # Убираем дубликаты

    def get_performance_profile(self) -> Dict[str, Any]:
        """Получить профиль производительности для текущего типа приложения."""
        profiles = {
            "web": {
                "priority_metrics": ["response_time", "throughput", "page_load_time"],
                "optimization_focus": ["frontend", "backend", "caching"],
                "tools": ["lighthouse", "webpack_bundle_analyzer", "web_vitals"],
                "strategies": ["code_splitting", "lazy_loading", "compression"]
            },
            "api": {
                "priority_metrics": ["response_time", "throughput", "error_rate"],
                "optimization_focus": ["response_time", "concurrency", "caching"],
                "tools": ["ab", "wrk", "jmeter", "locust"],
                "strategies": ["connection_pooling", "response_caching", "async_processing"]
            },
            "database": {
                "priority_metrics": ["query_time", "connection_count", "cpu_usage"],
                "optimization_focus": ["queries", "indexes", "connections"],
                "tools": ["explain_plan", "pg_stat", "slow_query_log"],
                "strategies": ["query_optimization", "indexing", "connection_pooling"]
            },
            "frontend": {
                "priority_metrics": ["fcp", "lcp", "cls", "bundle_size"],
                "optimization_focus": ["rendering", "bundle_size", "assets"],
                "tools": ["lighthouse", "web_vitals", "bundle_analyzer"],
                "strategies": ["code_splitting", "image_optimization", "css_optimization"]
            },
            "backend": {
                "priority_metrics": ["cpu_usage", "memory_usage", "response_time"],
                "optimization_focus": ["algorithms", "memory", "concurrency"],
                "tools": ["profiler", "memory_profiler", "async_profiler"],
                "strategies": ["algorithm_optimization", "memory_optimization", "async_processing"]
            },
            "mobile": {
                "priority_metrics": ["app_start_time", "battery_usage", "memory_usage"],
                "optimization_focus": ["startup", "battery", "memory"],
                "tools": ["instruments", "android_profiler", "flipper"],
                "strategies": ["lazy_initialization", "battery_optimization", "memory_management"]
            }
        }
        return profiles.get(self.performance_type, profiles["web"])

    def get_optimization_strategy_config(self) -> Dict[str, Any]:
        """Получить конфигурацию для выбранной стратегии оптимизации."""
        strategy_configs = {
            "speed": {
                "priority": "response_time",
                "trade_offs": ["memory_usage", "complexity"],
                "techniques": ["caching", "precomputation", "parallelization"],
                "metrics_weight": {"response_time": 0.5, "throughput": 0.3, "cpu_usage": 0.2}
            },
            "memory": {
                "priority": "memory_efficiency",
                "trade_offs": ["response_time", "cpu_usage"],
                "techniques": ["lazy_loading", "object_pooling", "compression"],
                "metrics_weight": {"memory_usage": 0.5, "response_time": 0.3, "throughput": 0.2}
            },
            "cpu": {
                "priority": "cpu_efficiency",
                "trade_offs": ["memory_usage", "response_time"],
                "techniques": ["algorithm_optimization", "batch_processing", "async_processing"],
                "metrics_weight": {"cpu_usage": 0.5, "throughput": 0.3, "memory_usage": 0.2}
            },
            "network": {
                "priority": "network_efficiency",
                "trade_offs": ["local_storage", "complexity"],
                "techniques": ["compression", "cdn", "connection_reuse"],
                "metrics_weight": {"network_latency": 0.4, "bandwidth_usage": 0.3, "response_time": 0.3}
            },
            "balanced": {
                "priority": "overall_performance",
                "trade_offs": [],
                "techniques": ["caching", "compression", "optimization"],
                "metrics_weight": {"response_time": 0.25, "throughput": 0.25, "cpu_usage": 0.25, "memory_usage": 0.25}
            }
        }
        return strategy_configs.get(self.optimization_strategy, strategy_configs["balanced"])

    def get_adaptive_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Получить адаптивные пороги для различных типов приложений."""
        performance_profile = self.get_performance_profile()
        base_thresholds = {
            "response_time": {"good": 200, "acceptable": 500, "poor": 1000},
            "throughput": {"good": 1000, "acceptable": 500, "poor": 100},
            "cpu_usage": {"good": 0.5, "acceptable": 0.7, "poor": 0.9},
            "memory_usage": {"good": 0.6, "acceptable": 0.8, "poor": 0.95},
            "error_rate": {"good": 0.001, "acceptable": 0.01, "poor": 0.05}
        }

        # Адаптируем пороги под тип приложения
        if self.performance_type == "api":
            base_thresholds["response_time"]["good"] = 100
            base_thresholds["throughput"]["good"] = 2000
        elif self.performance_type == "database":
            base_thresholds["response_time"]["good"] = 50
            base_thresholds["cpu_usage"]["good"] = 0.6
        elif self.performance_type == "frontend":
            base_thresholds["response_time"]["good"] = 300  # Page load time
            base_thresholds["bundle_size"] = {"good": 100, "acceptable": 250, "poor": 500}  # KB
        elif self.performance_type == "mobile":
            base_thresholds["response_time"]["good"] = 400
            base_thresholds["battery_usage"] = {"good": 0.1, "acceptable": 0.2, "poor": 0.4}  # %/hour

        return base_thresholds