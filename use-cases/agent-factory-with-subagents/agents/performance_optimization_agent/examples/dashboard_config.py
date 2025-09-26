"""
Пример конфигурации Performance Optimization Agent для dashboard проектов.

Этот пример демонстрирует оптимизацию производительности для дашбордов,
аналитических панелей и админ-интерфейсов с акцентом на:
- Оптимизацию больших таблиц и списков
- Эффективную работу с графиками и визуализациями
- Управление большими объемами данных
- Оптимизацию обновлений в реальном времени
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum

from ..dependencies import PerformanceOptimizationDependencies
from ..settings import PerformanceOptimizationSettings


class DashboardOptimizationType(Enum):
    """Типы оптимизации для дашбордов"""
    DATA_TABLES = "data_tables"
    CHARTS_GRAPHS = "charts_graphs"
    REAL_TIME_UPDATES = "real_time_updates"
    INFINITE_SCROLL = "infinite_scroll"
    LAZY_LOADING = "lazy_loading"
    VIRTUALIZATION = "virtualization"


@dataclass
class DashboardPerformanceDependencies(PerformanceOptimizationDependencies):
    """Зависимости для оптимизации дашбордов"""

    # Тип проекта
    domain_type: str = "dashboard"
    project_type: str = "analytics"

    # Специфичные для дашбордов настройки
    enable_data_virtualization: bool = True
    enable_chart_optimization: bool = True
    enable_real_time_optimization: bool = True

    # Конфигурация таблиц
    max_table_rows_per_page: int = 100
    enable_table_virtualization: bool = True
    table_row_height: int = 50

    # Конфигурация графиков
    chart_animation_duration: int = 300
    enable_chart_lazy_loading: bool = True
    max_data_points_per_chart: int = 1000

    # Real-time updates
    websocket_debounce_ms: int = 250
    max_concurrent_updates: int = 5
    update_batch_size: int = 20


@dataclass
class DashboardPerformanceSettings(PerformanceOptimizationSettings):
    """Настройки производительности для дашбордов"""

    # Performance budgets для дашбордов
    target_fcp_ms: int = 1500  # First Contentful Paint
    target_lcp_ms: int = 2500  # Largest Contentful Paint
    target_fid_ms: int = 100   # First Input Delay
    target_cls_score: float = 0.1  # Cumulative Layout Shift

    # Memory budgets
    max_memory_usage_mb: int = 512
    max_dom_nodes: int = 5000
    max_event_listeners: int = 1000

    # Data loading budgets
    max_initial_data_size_mb: int = 2
    max_chart_rendering_time_ms: int = 500
    max_table_rendering_time_ms: int = 300


class DashboardOptimizationPatterns:
    """Паттерны оптимизации для дашбордов"""

    @staticmethod
    def get_table_virtualization_config() -> Dict[str, Any]:
        """Конфигурация виртуализации таблиц"""
        return {
            "react_window": {
                "itemSize": 50,
                "height": 400,
                "overscanCount": 5,
                "useIsScrolling": True
            },
            "react_virtualized": {
                "rowHeight": 50,
                "headerHeight": 40,
                "noRowsRenderer": "() => <div>No data</div>",
                "overscanRowCount": 10
            },
            "tanstack_virtual": {
                "size": 50,
                "paddingStart": 0,
                "paddingEnd": 0,
                "scrollMargin": 0
            }
        }

    @staticmethod
    def get_chart_optimization_config() -> Dict[str, Any]:
        """Конфигурация оптимизации графиков"""
        return {
            "chart_js": {
                "animation": {"duration": 300},
                "responsive": True,
                "maintainAspectRatio": False,
                "datasets": {
                    "parsing": False,
                    "normalized": True
                },
                "scales": {
                    "x": {"type": "time", "time": {"parser": "YYYY-MM-DD"}},
                    "y": {"beginAtZero": True}
                }
            },
            "recharts": {
                "syncId": "dashboard",
                "margin": {"top": 10, "right": 30, "left": 0, "bottom": 0},
                "animationDuration": 300
            },
            "d3": {
                "transition_duration": 300,
                "ease": "easeLinear",
                "interpolate": "interpolateNumber"
            }
        }

    @staticmethod
    def get_real_time_optimization_config() -> Dict[str, Any]:
        """Конфигурация оптимизации real-time обновлений"""
        return {
            "websocket": {
                "reconnect": True,
                "reconnectInterval": 5000,
                "maxReconnectAttempts": 10,
                "timeout": 30000
            },
            "debouncing": {
                "updateDebounceMs": 250,
                "renderDebounceMs": 16,  # 60 FPS
                "batchUpdates": True
            },
            "throttling": {
                "maxUpdatesPerSecond": 10,
                "maxConcurrentRequests": 5,
                "queueSize": 100
            }
        }


class DashboardPerformanceMetrics:
    """Метрики производительности для дашбордов"""

    @staticmethod
    def get_core_web_vitals() -> Dict[str, Dict[str, float]]:
        """Core Web Vitals для дашбордов"""
        return {
            "lcp": {"good": 2.5, "needs_improvement": 4.0, "poor": float("inf")},
            "fid": {"good": 0.1, "needs_improvement": 0.3, "poor": float("inf")},
            "cls": {"good": 0.1, "needs_improvement": 0.25, "poor": float("inf")},
            "fcp": {"good": 1.8, "needs_improvement": 3.0, "poor": float("inf")},
            "ttfb": {"good": 0.8, "needs_improvement": 1.8, "poor": float("inf")}
        }

    @staticmethod
    def get_dashboard_specific_metrics() -> Dict[str, Dict[str, Any]]:
        """Специфичные для дашбордов метрики"""
        return {
            "table_rendering": {
                "target_ms": 300,
                "max_acceptable_ms": 500,
                "measurement": "time_to_visible_rows"
            },
            "chart_rendering": {
                "target_ms": 500,
                "max_acceptable_ms": 1000,
                "measurement": "time_to_interactive_chart"
            },
            "data_loading": {
                "target_ms": 1000,
                "max_acceptable_ms": 2000,
                "measurement": "time_to_data_display"
            },
            "real_time_updates": {
                "target_latency_ms": 100,
                "max_acceptable_latency_ms": 250,
                "measurement": "update_to_ui_delay"
            }
        }


def create_dashboard_performance_config(
    dashboard_type: str = "analytics",
    data_volume: str = "medium",
    real_time_enabled: bool = True
) -> Dict[str, Any]:
    """
    Создает конфигурацию оптимизации производительности для дашборда.

    Args:
        dashboard_type: Тип дашборда (analytics, admin, monitoring)
        data_volume: Объем данных (small, medium, large, enterprise)
        real_time_enabled: Включены ли real-time обновления

    Returns:
        Полная конфигурация оптимизации дашборда
    """

    # Базовая конфигурация в зависимости от типа
    base_configs = {
        "analytics": {
            "focus": ["charts", "data_tables", "filtering"],
            "chart_types": ["line", "bar", "pie", "area"],
            "table_features": ["sorting", "filtering", "pagination"]
        },
        "admin": {
            "focus": ["data_tables", "forms", "navigation"],
            "chart_types": ["bar", "line"],
            "table_features": ["crud", "bulk_actions", "search"]
        },
        "monitoring": {
            "focus": ["real_time", "charts", "alerts"],
            "chart_types": ["line", "gauge", "heatmap"],
            "table_features": ["live_updates", "filtering"]
        }
    }

    # Настройки в зависимости от объема данных
    volume_configs = {
        "small": {"max_rows": 1000, "virtualization": False, "lazy_loading": False},
        "medium": {"max_rows": 10000, "virtualization": True, "lazy_loading": True},
        "large": {"max_rows": 100000, "virtualization": True, "lazy_loading": True},
        "enterprise": {"max_rows": 1000000, "virtualization": True, "lazy_loading": True}
    }

    config = base_configs.get(dashboard_type, base_configs["analytics"])
    volume_config = volume_configs.get(data_volume, volume_configs["medium"])

    return {
        "dependencies": {
            "domain_type": "dashboard",
            "project_type": dashboard_type,
            "enable_data_virtualization": volume_config["virtualization"],
            "enable_chart_optimization": True,
            "enable_real_time_optimization": real_time_enabled,
            "max_table_rows_per_page": min(100, volume_config["max_rows"] // 10)
        },
        "settings": {
            "target_fcp_ms": 1500,
            "target_lcp_ms": 2500,
            "max_memory_usage_mb": 512 if data_volume != "enterprise" else 1024,
            "max_dom_nodes": volume_config["max_rows"] // 2
        },
        "optimizations": {
            "table_virtualization": DashboardOptimizationPatterns.get_table_virtualization_config(),
            "chart_optimization": DashboardOptimizationPatterns.get_chart_optimization_config(),
            "real_time": DashboardOptimizationPatterns.get_real_time_optimization_config() if real_time_enabled else {}
        },
        "metrics": {
            "core_web_vitals": DashboardPerformanceMetrics.get_core_web_vitals(),
            "dashboard_metrics": DashboardPerformanceMetrics.get_dashboard_specific_metrics()
        }
    }


# Примеры использования
if __name__ == "__main__":
    # Пример 1: Аналитический дашборд
    analytics_config = create_dashboard_performance_config(
        dashboard_type="analytics",
        data_volume="large",
        real_time_enabled=True
    )

    print("Analytics Dashboard Configuration:")
    print(f"- Domain: {analytics_config['dependencies']['domain_type']}")
    print(f"- Virtualization: {analytics_config['dependencies']['enable_data_virtualization']}")
    print(f"- Real-time: {analytics_config['dependencies']['enable_real_time_optimization']}")
    print(f"- Max memory: {analytics_config['settings']['max_memory_usage_mb']}MB")

    # Пример 2: Админ панель
    admin_config = create_dashboard_performance_config(
        dashboard_type="admin",
        data_volume="medium",
        real_time_enabled=False
    )

    print("\nAdmin Dashboard Configuration:")
    print(f"- Domain: {admin_config['dependencies']['domain_type']}")
    print(f"- Target LCP: {admin_config['settings']['target_lcp_ms']}ms")
    print(f"- Max DOM nodes: {admin_config['settings']['max_dom_nodes']}")

    # Пример 3: Мониторинг дашборд
    monitoring_config = create_dashboard_performance_config(
        dashboard_type="monitoring",
        data_volume="enterprise",
        real_time_enabled=True
    )

    print("\nMonitoring Dashboard Configuration:")
    print(f"- Memory limit: {monitoring_config['settings']['max_memory_usage_mb']}MB")
    print(f"- Real-time enabled: {monitoring_config['dependencies']['enable_real_time_optimization']}")
    print(f"- Rows per page: {monitoring_config['dependencies']['max_table_rows_per_page']}")