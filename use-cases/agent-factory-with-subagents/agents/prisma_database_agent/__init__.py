"""Prisma Database Agent для универсальной оптимизации баз данных."""

from .agent import prisma_agent, run_prisma_analysis, run_sync
from .tools import (
    analyze_schema_performance,
    optimize_queries,
    create_migration_plan,
    analyze_slow_queries,
    search_agent_knowledge
)
from .dependencies import PrismaDatabaseDependencies
from .settings import load_settings

__version__ = "1.0.0"
__all__ = [
    "prisma_agent",
    "run_prisma_analysis",
    "run_sync",
    "analyze_schema_performance",
    "optimize_queries",
    "create_migration_plan",
    "analyze_slow_queries",
    "search_agent_knowledge",
    "PrismaDatabaseDependencies",
    "load_settings"
]