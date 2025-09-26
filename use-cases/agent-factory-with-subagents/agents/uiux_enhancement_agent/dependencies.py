"""
Зависимости UI/UX Enhancement Agent.

Конфигурация для работы с дизайн системами, компонентными библиотеками
и инструментами анализа UI/UX с интеграцией MCP серверов.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# Import base dependencies with MCP integration
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from base_agent_dependencies import UniversalAgentDependencies
from mcp_integration import MCPIntegration, MCPToolsMixin


@dataclass
class UIUXEnhancementDependencies(UniversalAgentDependencies):
    """
    Зависимости агента UI/UX Enhancement с поддержкой RAG и специализированных инструментов.

    Включает настройки для работы с:
    - shadcn/ui компонентами
    - Tailwind CSS оптимизацией
    - Accessibility анализом
    - Дизайн системами
    """

    # UI/UX Agent specific settings (inherits core settings from base class)
    session_id: Optional[str] = None

    # Override base class defaults for UI/UX agent
    agent_type: str = field(default="uiux_enhancement", init=False)
    domain_type: str = "ui"  # Override base class
    project_type: str = "web_application"  # ecommerce, saas, blog, social, enterprise, portfolio, crm

    # UI/UX specific MCP integration
    enable_ui_automation: bool = field(default=True, init=False)
    enable_performance_monitoring: bool = field(default=True, init=False)
    custom_mcp_servers: List[str] = field(default_factory=lambda: ["shadcn", "puppeteer", "context7"], init=False)

    # UI/UX specific knowledge tags (extend base class)
    ui_knowledge_tags: List[str] = field(default_factory=lambda: [
        "design-systems",
        "accessibility",
        "shadcn",
        "tailwind-css",
        "responsive-design"
    ])

    # Настройки дизайн системы (универсальные по умолчанию)
    design_system_type: str = "custom"  # material, tailwind, bootstrap, custom, shadcn, chakra, mantine
    css_framework: str = "tailwind"  # tailwind, emotion, styled-components, css-modules, scss
    component_library_version: str = "latest"

    # Стратегии дизайна
    responsive_strategy: str = "mobile-first"  # mobile-first, desktop-first, adaptive, progressive

    # Accessibility настройки
    accessibility_level: str = "wcag-aa"  # wcag-a, wcag-aa, wcag-aaa, section-508
    accessibility_tools: List[str] = field(default_factory=lambda: [
        "axe-core",
        "lighthouse",
        "wave",
        "pa11y"
    ])

    # Поддержка тем (универсальные настройки)
    theme_support: List[str] = field(default_factory=lambda: ["light", "dark"])
    color_palette: Dict[str, str] = field(default_factory=lambda: {
        "primary": "hsl(var(--primary))",
        "secondary": "hsl(var(--secondary))",
        "accent": "hsl(var(--accent))",
        "background": "hsl(var(--background))",
        "foreground": "hsl(var(--foreground))",
        "muted": "hsl(var(--muted))",
        "border": "hsl(var(--border))"
    })

    # Настройки под конкретный проект (заполняются при инициализации)
    project_specific_colors: Dict[str, str] = field(default_factory=dict)
    project_name: str = ""

    # Responsive breakpoints (Tailwind CSS)
    breakpoints: Dict[str, str] = field(default_factory=lambda: {
        "xs": "475px",
        "sm": "640px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1280px",
        "2xl": "1536px",
        "3xl": "1920px"
    })

    # Performance настройки
    optimize_bundle_size: bool = True
    lazy_load_components: bool = True
    tree_shake_css: bool = True

    # Animation preferences
    animation_duration_fast: str = "150ms"
    animation_duration_normal: str = "300ms"
    animation_duration_slow: str = "500ms"
    reduce_motion_support: bool = True

    # Component enhancement settings
    auto_focus_management: bool = True
    keyboard_navigation: bool = True
    screen_reader_support: bool = True
    high_contrast_support: bool = True

    # Framework integration (расширенная поддержка)
    ui_framework: str = "react"  # react, vue, angular, svelte, solid, lit
    framework_version: str = "18"  # версия фреймворка

    # Tools integration
    puppeteer_enabled: bool = True  # Для visual testing
    figma_integration: bool = False  # Опционально для синхронизации с дизайном
    storybook_integration: bool = True  # Для документации компонентов
    chromatic_enabled: bool = False  # Visual regression testing

    def __post_init__(self):
        """Инициализация дополнительных настроек."""

        # Call parent __post_init__ first
        super().__post_init__()

        # Extend knowledge_tags with UI/UX specific tags
        self.knowledge_tags.extend(self.ui_knowledge_tags)

        # Remove duplicates from knowledge_tags
        self.knowledge_tags = list(set(self.knowledge_tags))

        # Добавляем теги для конкретного проекта, если указано имя проекта
        if self.project_name and self.project_name.lower() not in self.knowledge_tags:
            self.knowledge_tags.append(self.project_name.lower())

        # Объединяем основную палитру с проектными цветами
        if self.project_specific_colors:
            self.color_palette.update(self.project_specific_colors)

        # Добавляем теги для используемых технологий
        if self.design_system_type != "custom" and self.design_system_type not in self.knowledge_tags:
            self.knowledge_tags.append(self.design_system_type.replace("/", "-"))

        if self.css_framework not in self.knowledge_tags:
            self.knowledge_tags.append(self.css_framework)

        if self.ui_framework not in self.knowledge_tags:
            self.knowledge_tags.append(self.ui_framework)

    def get_mcp_toolsets(self):
        """Get MCP toolsets specifically configured for UI/UX work."""
        integration = self.get_mcp_integration()
        return integration.get_server_toolsets() if integration else []

    def get_accessibility_config(self) -> Dict[str, Any]:
        """Получить конфигурацию accessibility проверок."""
        return {
            "accessibility_level": self.accessibility_level,
            "tools": self.accessibility_tools,
            "auto_focus": self.auto_focus_management,
            "keyboard_nav": self.keyboard_navigation,
            "screen_reader": self.screen_reader_support,
            "high_contrast": self.high_contrast_support,
            "reduce_motion": self.reduce_motion_support
        }

    def get_responsive_config(self) -> Dict[str, Any]:
        """Получить конфигурацию responsive дизайна."""
        return {
            "breakpoints": self.breakpoints,
            "strategy": self.responsive_strategy,
            "mobile_first": self.responsive_strategy == "mobile-first",
            "touch_friendly": True,
            "viewport_meta": True
        }

    def get_performance_config(self) -> Dict[str, Any]:
        """Получить настройки производительности."""
        return {
            "bundle_optimization": self.optimize_bundle_size,
            "lazy_loading": self.lazy_load_components,
            "css_tree_shaking": self.tree_shake_css,
            "code_splitting": True,
            "image_optimization": True
        }

    def get_animation_config(self) -> Dict[str, str]:
        """Получить настройки анимаций."""
        return {
            "fast": self.animation_duration_fast,
            "normal": self.animation_duration_normal,
            "slow": self.animation_duration_slow,
            "easing": "cubic-bezier(0.4, 0, 0.2, 1)",
            "respect_reduced_motion": str(self.reduce_motion_support).lower()
        }

    def get_design_system_config(self) -> Dict[str, Any]:
        """Получить конфигурацию дизайн системы."""
        return {
            "type": self.design_system_type,
            "css_framework": self.css_framework,
            "ui_framework": self.ui_framework,
            "framework_version": self.framework_version,
            "responsive_strategy": self.responsive_strategy,
            "accessibility_level": self.accessibility_level,
            "theme_support": self.theme_support,
            "color_palette": self.color_palette
        }

    def get_framework_config(self) -> Dict[str, Any]:
        """Получить конфигурацию для конкретного UI фреймворка."""
        base_config = {
            "framework": self.ui_framework,
            "version": self.framework_version,
            "design_system": self.design_system_type,
            "css_framework": self.css_framework
        }

        # Специфичные настройки для фреймворков
        if self.ui_framework == "react":
            base_config.update({
                "supports_jsx": True,
                "supports_hooks": True,
                "component_format": "functional" if int(self.framework_version) >= 16 else "class"
            })
        elif self.ui_framework == "vue":
            base_config.update({
                "supports_composition_api": int(self.framework_version) >= 3,
                "supports_script_setup": int(self.framework_version) >= 3,
                "component_format": "sfc"
            })
        elif self.ui_framework == "angular":
            base_config.update({
                "supports_standalone": int(self.framework_version) >= 14,
                "supports_signals": int(self.framework_version) >= 16,
                "component_format": "typescript"
            })

        return base_config