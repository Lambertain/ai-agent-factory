"""
Universal UI/UX Enhancement Agent для любых типов проектов.

Агент специализируется на улучшении пользовательского интерфейса,
оптимизации Tailwind CSS, работе с shadcn/ui компонентами и обеспечении accessibility.
Адаптируется под любые проекты: e-commerce, SaaS, блоги, социальные сети и другие.
"""

from .agent import uiux_agent, run_uiux_enhancement, run_uiux_enhancement_sync
from .dependencies import UIUXEnhancementDependencies
from .settings import load_settings, UIUXAgentSettings

__version__ = "1.0.0"
__author__ = "UI/UX Enhancement Agent"

__all__ = [
    "uiux_agent",
    "run_uiux_enhancement",
    "run_uiux_enhancement_sync",
    "UIUXEnhancementDependencies",
    "load_settings",
    "UIUXAgentSettings"
]