"""
PWA Mobile Agent - универсальный агент для Progressive Web Apps.

Предоставляет инструменты для создания мобильных веб-приложений
с поддержкой offline, push-уведомлений, и оптимизации под различные типы проектов.
"""

from .agent import agent, run_pwa_mobile_analysis
from .dependencies import PWAMobileAgentDependencies
from .settings import load_settings

__version__ = "1.0.0"
__author__ = "AI Agent Factory"

__all__ = [
    "agent",
    "run_pwa_mobile_analysis",
    "PWAMobileAgentDependencies",
    "load_settings"
]