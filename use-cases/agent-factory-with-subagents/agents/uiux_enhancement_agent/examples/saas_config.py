"""
SaaS UI/UX конфигурация для UI/UX Enhancement Agent.

Этот файл демонстрирует настройку агента для SaaS проектов.
Включает дашборды, аналитику, и специфичные UI компоненты для SaaS приложений.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from ..dependencies import UIUXEnhancementDependencies


@dataclass
class SaaSUIUXDependencies(UIUXEnhancementDependencies):
    """Конфигурация для SaaS проектов."""

    # Основные настройки
    domain_type: str = "saas"
    project_type: str = "web_application"

    # SaaS специфичные настройки
    enable_dashboard: bool = True
    enable_analytics: bool = True
    enable_user_management: bool = True
    enable_billing: bool = True
    enable_api_docs: bool = True

    # Dashboard настройки
    dashboard_layout: str = "sidebar"  # sidebar, topbar, hybrid
    enable_widgets: bool = True
    enable_custom_dashboards: bool = True
    enable_data_export: bool = True

    # Navigation настройки
    sidebar_collapsed_by_default: bool = False
    enable_breadcrumbs: bool = True
    enable_command_palette: bool = True

    # Feature flags
    enable_dark_mode: bool = True
    enable_multiple_workspaces: bool = True
    enable_real_time_updates: bool = True

    def get_color_scheme(self) -> Dict[str, Any]:
        """Цветовая схема для SaaS."""
        return {
            "primary": "hsl(221, 83%, 53%)",   # Professional blue
            "secondary": "hsl(210, 11%, 15%)", # Dark gray
            "success": "hsl(142, 76%, 36%)",   # Success green
            "warning": "hsl(38, 92%, 50%)",    # Warning amber
            "destructive": "hsl(0, 84%, 60%)", # Error red
            "accent": "hsl(262, 83%, 58%)",    # Accent purple

            # SaaS specific colors
            "dashboard": "hsl(220, 14%, 96%)", # Light background
            "sidebar": "hsl(220, 13%, 18%)",   # Dark sidebar
            "card": "hsl(0, 0%, 100%)",        # White cards
            "border": "hsl(214, 32%, 91%)",    # Light borders

            # Status colors
            "active": "hsl(142, 76%, 36%)",    # Active status
            "inactive": "hsl(0, 0%, 63%)",     # Inactive status
            "pending": "hsl(38, 92%, 50%)",    # Pending status
            "error": "hsl(0, 84%, 60%)",       # Error status

            # Chart colors
            "chart_1": "hsl(221, 83%, 53%)",
            "chart_2": "hsl(262, 83%, 58%)",
            "chart_3": "hsl(142, 76%, 36%)",
            "chart_4": "hsl(38, 92%, 50%)",
            "chart_5": "hsl(0, 84%, 60%)",
        }

    def get_component_config(self) -> Dict[str, Any]:
        """Конфигурация компонентов для SaaS."""
        return {
            "sidebar": {
                "width": "280px",
                "collapsed_width": "80px",
                "collapsible": True,
                "show_logo": True,
                "show_user_info": True,
                "navigation_groups": True
            },
            "dashboard": {
                "grid_columns": {"mobile": 1, "tablet": 2, "desktop": 3, "wide": 4},
                "widget_spacing": "1.5rem",
                "enable_drag_drop": self.enable_custom_dashboards,
                "auto_refresh": self.enable_real_time_updates
            },
            "data_table": {
                "pagination": True,
                "sorting": True,
                "filtering": True,
                "search": True,
                "bulk_actions": True,
                "export": self.enable_data_export
            },
            "forms": {
                "validation": "real_time",
                "auto_save": True,
                "field_groups": True,
                "progress_indicator": True
            },
            "modals": {
                "backdrop_dismiss": True,
                "escape_key": True,
                "focus_trap": True,
                "max_width": "600px"
            }
        }

    def get_layout_config(self) -> Dict[str, Any]:
        """Конфигурация layout для SaaS."""
        return {
            "dashboard_layout": self.dashboard_layout,
            "spacing": {
                "page_padding": "2rem",
                "section_gap": "3rem",
                "component_gap": "1.5rem",
                "element_gap": "0.75rem"
            },
            "containers": {
                "header": "full",
                "sidebar": "fixed" if self.dashboard_layout == "sidebar" else "none",
                "main": "full",
                "footer": "full"
            },
            "breakpoints": {
                "sidebar_collapse": "768px",
                "mobile_navigation": "640px"
            }
        }

    def get_animation_config(self) -> Dict[str, Any]:
        """Конфигурация анимаций для SaaS."""
        return {
            "sidebar_toggle": {
                "duration": "300ms",
                "easing": "cubic-bezier(0.4, 0, 0.2, 1)"
            },
            "modal_transitions": {
                "duration": "200ms",
                "easing": "ease-out"
            },
            "data_updates": {
                "type": "fade",
                "duration": "300ms"
            },
            "loading_states": {
                "skeleton": True,
                "spinner": True,
                "progress_bars": True
            },
            "micro_interactions": {
                "button_hover": "scale(1.02)",
                "card_hover": "translateY(-2px)",
                "focus_ring": True
            }
        }

    def get_accessibility_config(self) -> Dict[str, Any]:
        """Конфигурация accessibility для SaaS."""
        return {
            "high_contrast_mode": True,
            "keyboard_navigation": True,
            "screen_reader_optimized": True,
            "focus_indicators": True,
            "reduced_motion": True,
            "aria_labels": {
                "sidebar_toggle": "Toggle sidebar navigation",
                "user_menu": "User account menu",
                "notifications": "Notifications",
                "dashboard_widget": "Dashboard widget: {title}",
                "data_table": "Data table: {rows} rows"
            },
            "skip_links": [
                {"href": "#main", "label": "Skip to main content"},
                {"href": "#navigation", "label": "Skip to navigation"},
                {"href": "#dashboard", "label": "Skip to dashboard"}
            ],
            "landmarks": {
                "navigation": "main navigation",
                "search": "site search",
                "main": "main content"
            }
        }

    def get_widget_config(self) -> Dict[str, Any]:
        """Конфигурация виджетов для SaaS дашборда."""
        return {
            "metrics": {
                "size": {"width": 1, "height": 1},
                "chart_type": "number",
                "show_trend": True,
                "show_comparison": True
            },
            "chart": {
                "size": {"width": 2, "height": 1},
                "chart_types": ["line", "bar", "pie", "area"],
                "interactive": True,
                "export": self.enable_data_export
            },
            "table": {
                "size": {"width": 2, "height": 2},
                "pagination": True,
                "search": True,
                "actions": True
            },
            "activity_feed": {
                "size": {"width": 1, "height": 2},
                "real_time": self.enable_real_time_updates,
                "filters": True,
                "timestamps": True
            }
        }


# Пример использования
def get_saas_uiux_dependencies() -> SaaSUIUXDependencies:
    """Создать конфигурацию для SaaS проекта."""
    return SaaSUIUXDependencies(
        api_key="your-api-key",
        domain_type="saas",
        project_type="web_application",
        enable_dashboard=True,
        enable_analytics=True,
        enable_user_management=True,
        dashboard_layout="sidebar",
        enable_custom_dashboards=True
    )


# Пример использования в React компоненте
SAAS_COMPONENT_EXAMPLES = {
    "dashboard_widget": """
// SaaS Dashboard Widget Component
export function SaaSDashboardWidget({
  widget,
  config
}: {
  widget: DashboardWidget;
  config: SaaSUIUXDependencies;
}) {
  const colorScheme = config.get_color_scheme();
  const dashboardConfig = config.get_component_config().dashboard;

  return (
    <Card
      className="p-6 hover:shadow-lg transition-shadow"
      style={{ backgroundColor: colorScheme.card }}
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">{widget.title}</h3>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem>Refresh</DropdownMenuItem>
            <DropdownMenuItem>Configure</DropdownMenuItem>
            {config.enable_data_export && (
              <DropdownMenuItem>Export</DropdownMenuItem>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <div className="space-y-4">
        {widget.type === 'metric' && (
          <div>
            <div className="text-3xl font-bold" style={{ color: colorScheme.primary }}>
              {widget.value}
            </div>
            <div className="flex items-center gap-2 text-sm">
              <span className="text-muted-foreground">{widget.label}</span>
              {widget.trend && (
                <span className={cn(
                  "flex items-center gap-1",
                  widget.trend > 0 ? "text-green-600" : "text-red-600"
                )}>
                  {widget.trend > 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                  {Math.abs(widget.trend)}%
                </span>
              )}
            </div>
          </div>
        )}

        {widget.type === 'chart' && (
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={widget.data}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke={colorScheme.primary}
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {widget.type === 'list' && (
          <div className="space-y-2">
            {widget.items.slice(0, 5).map((item, index) => (
              <div key={index} className="flex items-center justify-between p-2 rounded hover:bg-muted/50">
                <span className="text-sm">{item.name}</span>
                <span className="text-sm font-medium" style={{ color: colorScheme.primary }}>
                  {item.value}
                </span>
              </div>
            ))}
            {widget.items.length > 5 && (
              <Button variant="ghost" size="sm" className="w-full">
                View all {widget.items.length} items
              </Button>
            )}
          </div>
        )}
      </div>

      {dashboardConfig.auto_refresh && (
        <div className="mt-4 pt-4 border-t">
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>Last updated: {widget.lastUpdated}</span>
            <span>Auto-refresh: 30s</span>
          </div>
        </div>
      )}
    </Card>
  );
}
""",

    "sidebar_navigation": """
// SaaS Sidebar Navigation Component
export function SaaSSidebarNavigation({
  config,
  isCollapsed,
  onToggle
}: {
  config: SaaSUIUXDependencies;
  isCollapsed: boolean;
  onToggle: () => void;
}) {
  const colorScheme = config.get_color_scheme();
  const sidebarConfig = config.get_component_config().sidebar;

  const navigationItems = [
    { icon: Home, label: "Dashboard", href: "/dashboard" },
    { icon: BarChart3, label: "Analytics", href: "/analytics", enabled: config.enable_analytics },
    { icon: Users, label: "Users", href: "/users", enabled: config.enable_user_management },
    { icon: CreditCard, label: "Billing", href: "/billing", enabled: config.enable_billing },
    { icon: Settings, label: "Settings", href: "/settings" },
  ].filter(item => item.enabled !== false);

  return (
    <div
      className={cn(
        "flex flex-col h-screen border-r transition-all duration-300",
        isCollapsed ? "w-20" : "w-72"
      )}
      style={{
        backgroundColor: colorScheme.sidebar,
        borderColor: colorScheme.border
      }}
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b" style={{ borderColor: colorScheme.border }}>
        {!isCollapsed && (
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded flex items-center justify-center">
              <span className="text-white font-bold text-sm">S</span>
            </div>
            <span className="text-white font-semibold">SaaS App</span>
          </div>
        )}
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggle}
          className="text-white hover:bg-white/10"
          aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {isCollapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-2">
        <div className="space-y-1">
          {navigationItems.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors",
                isCollapsed && "justify-center"
              )}
            >
              <item.icon className="h-5 w-5 flex-shrink-0" />
              {!isCollapsed && (
                <span className="text-sm font-medium">{item.label}</span>
              )}
            </a>
          ))}
        </div>

        {config.enable_command_palette && !isCollapsed && (
          <div className="mt-6 px-3">
            <Button
              variant="ghost"
              className="w-full justify-start text-white/80 hover:text-white hover:bg-white/10"
            >
              <Search className="h-4 w-4 mr-2" />
              <span className="text-sm">Search...</span>
              <kbd className="ml-auto pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
                ⌘K
              </kbd>
            </Button>
          </div>
        )}
      </nav>

      {/* User Info */}
      {sidebarConfig.show_user_info && (
        <div className="p-4 border-t" style={{ borderColor: colorScheme.border }}>
          {!isCollapsed ? (
            <div className="flex items-center gap-3">
              <Avatar className="h-8 w-8">
                <AvatarImage src="/user.jpg" />
                <AvatarFallback>JD</AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">John Doe</p>
                <p className="text-xs text-white/60 truncate">john@example.com</p>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon" className="text-white/80 hover:text-white">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem>Profile</DropdownMenuItem>
                  <DropdownMenuItem>Settings</DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>Sign out</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          ) : (
            <div className="flex justify-center">
              <Avatar className="h-8 w-8">
                <AvatarImage src="/user.jpg" />
                <AvatarFallback>JD</AvatarFallback>
              </Avatar>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
"""
}