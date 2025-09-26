"""
Performance Optimization Agent для универсальной оптимизации производительности.

Этот агент специализируется на анализе и улучшении производительности различных типов проектов:
- Frontend приложения (React, Vue, Angular, Svelte)
- Backend API (FastAPI, Django, Express, Flask)
- Database optimization (PostgreSQL, MySQL, MongoDB)
- Full-stack web applications
- Mobile applications (React Native, Flutter)

Автоматически адаптируется под тип проекта, используемые технологии и домен применения.
"""

from .agent import (
    performance_agent,
    run_performance_optimization,
    run_performance_optimization_sync,
    analyze_project,
    optimize_project,
    monitor_project,
    create_project_report
)
from .dependencies import PerformanceOptimizationDependencies, load_performance_settings
from .settings import (
    PerformanceOptimizationSettings,
    load_performance_optimization_settings,
    get_llm_model,
    get_domain_defaults,
    get_framework_config,
    get_cost_optimization_config
)
from .tools import (
    analyze_performance,
    optimize_performance,
    monitor_performance,
    search_performance_knowledge,
    generate_performance_report
)

__version__ = "1.0.0"
__author__ = "Performance Optimization Agent"

__all__ = [
    # Основной агент
    "performance_agent",

    # Главные функции запуска
    "run_performance_optimization",
    "run_performance_optimization_sync",

    # Быстрые функции для специфичных задач
    "analyze_project",
    "optimize_project",
    "monitor_project",
    "create_project_report",

    # Конфигурация и зависимости
    "PerformanceOptimizationDependencies",
    "load_performance_settings",

    # Настройки (новый settings.py)
    "PerformanceOptimizationSettings",
    "load_performance_optimization_settings",
    "get_llm_model",
    "get_domain_defaults",
    "get_framework_config",
    "get_cost_optimization_config",

    # Инструменты (для расширения)
    "analyze_performance",
    "optimize_performance",
    "monitor_performance",
    "search_performance_knowledge",
    "generate_performance_report"
]