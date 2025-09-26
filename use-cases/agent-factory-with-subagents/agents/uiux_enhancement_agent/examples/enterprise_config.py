"""
Enterprise UI/UX конфигурация для UI/UX Enhancement Agent.

Этот файл демонстрирует настройку агента для корпоративных enterprise проектов.
Включает настройки для высокого уровня безопасности, accessibility, и соответствия корпоративным стандартам.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from ..dependencies import UIUXEnhancementDependencies


@dataclass
class EnterpriseUIUXDependencies(UIUXEnhancementDependencies):
    """Конфигурация для Enterprise проектов."""

    # Основные настройки
    domain_type: str = "enterprise"
    project_type: str = "corporate_platform"

    # Enterprise специфичные настройки
    design_system_type: str = "custom"  # Корпоративная дизайн система
    css_framework: str = "scss"  # Часто используется в enterprise
    ui_framework: str = "angular"  # Популярен в enterprise
    framework_version: str = "17"
    accessibility_level: str = "wcag-aaa"  # Максимальный уровень
    responsive_strategy: str = "desktop-first"  # Enterprise часто desktop-first

    # Security и compliance
    enable_security_headers: bool = True
    enable_audit_logging: bool = True
    enable_user_session_management: bool = True
    compliance_standards: List[str] = field(default_factory=lambda: [
        "WCAG-AAA", "Section-508", "GDPR", "SOX", "HIPAA"
    ])

    # Enterprise UI features
    enable_role_based_ui: bool = True
    enable_multi_tenant: bool = True
    enable_white_labeling: bool = True
    enable_advanced_permissions: bool = True

    # Брендинг и кастомизация
    allow_custom_themes: bool = True
    enable_logo_customization: bool = True
    enable_color_scheme_override: bool = True

    def __post_init__(self):
        super().__post_init__()

        # Enterprise knowledge tags
        self.knowledge_tags.extend([
            "enterprise", "corporate", "security", "compliance", "angular"
        ])

    def get_security_config(self) -> Dict[str, Any]:
        """Конфигурация безопасности для Enterprise."""
        return {
            "content_security_policy": True,
            "xss_protection": True,
            "clickjacking_protection": True,
            "secure_headers": self.enable_security_headers,
            "session_management": self.enable_user_session_management,
            "audit_logging": self.enable_audit_logging,
            "input_sanitization": True,
            "csrf_protection": True
        }

    def get_compliance_config(self) -> Dict[str, Any]:
        """Конфигурация соответствия стандартам."""
        return {
            "standards": self.compliance_standards,
            "accessibility_level": self.accessibility_level,
            "data_privacy": "GDPR" in self.compliance_standards,
            "audit_trail": self.enable_audit_logging,
            "user_consent_management": True,
            "data_retention_policies": True
        }

    def get_enterprise_features_config(self) -> Dict[str, Any]:
        """Конфигурация enterprise функций."""
        return {
            "role_based_ui": self.enable_role_based_ui,
            "multi_tenant": self.enable_multi_tenant,
            "white_labeling": self.enable_white_labeling,
            "advanced_permissions": self.enable_advanced_permissions,
            "sso_integration": True,
            "ldap_integration": True,
            "api_rate_limiting": True,
            "bulk_operations": True
        }

    def get_color_scheme(self) -> Dict[str, str]:
        """Консервативная корпоративная цветовая схема."""
        return {
            # Основные корпоративные цвета
            "primary": "hsl(214, 84%, 56%)",      # Professional blue
            "secondary": "hsl(210, 16%, 82%)",    # Light gray
            "accent": "hsl(142, 71%, 45%)",       # Success green
            "background": "hsl(0, 0%, 100%)",     # Pure white
            "foreground": "hsl(222, 84%, 5%)",    # Dark text
            "muted": "hsl(210, 40%, 96%)",        # Very light gray
            "border": "hsl(214, 32%, 91%)",       # Light border

            # Enterprise status colors
            "success": "hsl(142, 71%, 45%)",      # Green
            "warning": "hsl(38, 92%, 50%)",       # Orange
            "error": "hsl(0, 72%, 51%)",          # Red
            "info": "hsl(199, 89%, 48%)",         # Blue

            # Role-based colors
            "admin": "hsl(0, 72%, 51%)",          # Red for admin
            "manager": "hsl(38, 92%, 50%)",       # Orange for manager
            "user": "hsl(214, 84%, 56%)",         # Blue for user
            "guest": "hsl(210, 16%, 82%)",        # Gray for guest

            # Compliance indicators
            "compliant": "hsl(142, 71%, 45%)",    # Green
            "non_compliant": "hsl(0, 72%, 51%)", # Red
            "pending_review": "hsl(38, 92%, 50%)" # Orange
        }

    def get_component_config(self) -> Dict[str, Any]:
        """Конфигурация компонентов для Enterprise."""
        return {
            "navigation": {
                "show_breadcrumbs": True,
                "show_user_menu": True,
                "show_notifications": True,
                "show_help_center": True,
                "collapsible_sidebar": True,
                "role_based_menus": self.enable_role_based_ui
            },
            "data_tables": {
                "pagination": True,
                "sorting": True,
                "filtering": True,
                "bulk_actions": True,
                "export_functionality": True,
                "column_customization": True,
                "row_selection": True
            },
            "forms": {
                "inline_validation": True,
                "progressive_disclosure": True,
                "auto_save": True,
                "field_help_text": True,
                "required_indicators": True,
                "character_counters": True
            },
            "security": {
                "password_strength_indicator": True,
                "two_factor_auth_ui": True,
                "session_timeout_warning": True,
                "secure_file_upload": True
            },
            "reporting": {
                "dashboard_widgets": True,
                "chart_types": ["bar", "line", "pie", "scatter", "heatmap"],
                "export_formats": ["PDF", "Excel", "CSV"],
                "scheduled_reports": True
            }
        }

    def get_layout_config(self) -> Dict[str, Any]:
        """Конфигурация layout для Enterprise."""
        return {
            "grid": {
                "dashboard_grid": {"desktop": 4, "tablet": 2, "mobile": 1},
                "content_grid": {"desktop": 3, "tablet": 2, "mobile": 1},
                "card_grid": {"desktop": 4, "tablet": 3, "mobile": 2}
            },
            "spacing": {
                "section_gap": "4rem",      # Больше пространства
                "component_gap": "2rem",
                "element_gap": "1rem"
            },
            "containers": {
                "header": "full",
                "sidebar": "fixed",          # Фиксированная боковая панель
                "main": "container",         # Контейнер с ограничением ширины
                "footer": "full"
            },
            "breakpoints": {
                "mobile": "768px",
                "tablet": "1024px",
                "desktop": "1280px",
                "wide": "1536px",
                "ultra_wide": "1920px"      # Для больших мониторов
            }
        }

    def get_accessibility_config(self) -> Dict[str, Any]:
        """Расширенная конфигурация accessibility для Enterprise."""
        base_config = super().get_accessibility_config()

        enterprise_config = {
            "high_contrast_mode": True,
            "keyboard_navigation": True,
            "screen_reader_optimized": True,
            "focus_indicators": True,
            "reduced_motion_support": True,
            "font_size_scaling": True,
            "color_blind_support": True,
            "voice_control_support": True,

            # Enterprise specific accessibility
            "section_508_compliance": True,
            "aria_live_regions": True,
            "landmark_navigation": True,
            "skip_links": [
                {"href": "#main", "label": "Skip to main content"},
                {"href": "#navigation", "label": "Skip to navigation"},
                {"href": "#sidebar", "label": "Skip to sidebar"},
                {"href": "#footer", "label": "Skip to footer"}
            ],

            # WCAG AAA specific requirements
            "color_contrast_ratio": 7.0,    # AAA требует 7:1
            "minimum_text_size": "14px",
            "maximum_line_length": "80ch",
            "content_language_attributes": True,
            "heading_structure_validation": True
        }

        return {**base_config, **enterprise_config}


# Пример использования
def get_enterprise_uiux_dependencies() -> EnterpriseUIUXDependencies:
    """Создать конфигурацию для Enterprise проекта."""
    return EnterpriseUIUXDependencies(
        project_path="/corporate/platform",
        project_name="Corporate Management Platform",
        domain_type="enterprise",
        project_type="corporate_platform",
        design_system_type="custom",
        accessibility_level="wcag-aaa",
        enable_role_based_ui=True,
        enable_multi_tenant=True,
        enable_audit_logging=True
    )


# Пример использования в Angular компоненте
ENTERPRISE_COMPONENT_EXAMPLES = {
    "role_based_navigation": """
<!-- Enterprise Role-Based Navigation Component -->
<nav class="enterprise-nav" [attr.aria-label]="'Main navigation for ' + userRole">
  <div class="nav-header">
    <img [src]="tenantLogo" [alt]="tenantName + ' logo'" class="tenant-logo">
    <h1 class="sr-only">{{tenantName}} Platform</h1>
  </div>

  <ul class="nav-menu" role="menubar">
    <li *ngFor="let item of getMenuItems()"
        role="none"
        [class.nav-item]="true"
        [class.nav-item--active]="isActive(item.path)">

      <a [routerLink]="item.path"
         role="menuitem"
         [attr.aria-current]="isActive(item.path) ? 'page' : null"
         [attr.aria-label]="item.label + (item.badge ? ' (' + item.badge + ' notifications)' : '')"
         class="nav-link">

        <mat-icon [attr.aria-hidden]="true">{{item.icon}}</mat-icon>
        <span class="nav-text">{{item.label}}</span>

        <span *ngIf="item.badge"
              class="nav-badge"
              [attr.aria-label]="item.badge + ' notifications'">
          {{item.badge}}
        </span>
      </a>

      <!-- Submenu для сложной навигации -->
      <ul *ngIf="item.children && isExpanded(item.path)"
          class="nav-submenu"
          role="menu"
          [attr.aria-label]="item.label + ' submenu'">
        <li *ngFor="let child of item.children" role="none">
          <a [routerLink]="child.path"
             role="menuitem"
             class="nav-sublink">
            {{child.label}}
          </a>
        </li>
      </ul>
    </li>
  </ul>

  <div class="nav-footer">
    <button class="nav-user-menu"
            [attr.aria-expanded]="isUserMenuOpen"
            [attr.aria-label]="'User menu for ' + currentUser.name"
            (click)="toggleUserMenu()">
      <mat-icon aria-hidden="true">account_circle</mat-icon>
      <span class="user-name">{{currentUser.name}}</span>
      <span class="user-role">{{currentUser.role}}</span>
    </button>
  </div>
</nav>
""",

    "enterprise_data_table": """
<!-- Enterprise Data Table Component -->
<div class="enterprise-table-container">
  <div class="table-header">
    <div class="table-title">
      <h2 id="table-title">{{tableTitle}}</h2>
      <span class="table-count" aria-live="polite">
        {{filteredData.length}} of {{totalData.length}} records
      </span>
    </div>

    <div class="table-actions">
      <mat-form-field appearance="outline" class="search-field">
        <mat-label>Search</mat-label>
        <input matInput
               [(ngModel)]="searchTerm"
               [attr.aria-label]="'Search in ' + tableTitle"
               (input)="onSearch($event)">
        <mat-icon matSuffix aria-hidden="true">search</mat-icon>
      </mat-form-field>

      <button mat-raised-button
              color="primary"
              [disabled]="selectedRows.length === 0"
              [attr.aria-label]="'Export ' + selectedRows.length + ' selected items'"
              (click)="exportSelected()">
        <mat-icon aria-hidden="true">download</mat-icon>
        Export ({{selectedRows.length}})
      </button>
    </div>
  </div>

  <div class="table-wrapper" role="region" [attr.aria-labelledby]="'table-title'">
    <table mat-table
           [dataSource]="filteredData"
           [attr.aria-label]="tableTitle + ' data table'"
           multiTemplateDataRows
           class="enterprise-table">

      <!-- Selection Column -->
      <ng-container matColumnDef="select">
        <th mat-header-cell *matHeaderCellDef>
          <mat-checkbox (change)="$event ? masterToggle() : null"
                        [checked]="selection.hasValue() && isAllSelected()"
                        [indeterminate]="selection.hasValue() && !isAllSelected()"
                        [attr.aria-label]="'Select all ' + tableTitle">
          </mat-checkbox>
        </th>
        <td mat-cell *matCellDef="let row">
          <mat-checkbox (click)="$event.stopPropagation()"
                        (change)="$event ? selection.toggle(row) : null"
                        [checked]="selection.isSelected(row)"
                        [attr.aria-label]="'Select ' + row.name">
          </mat-checkbox>
        </td>
      </ng-container>

      <!-- Data Columns -->
      <ng-container *ngFor="let column of displayedColumns" [matColumnDef]="column.key">
        <th mat-header-cell *matHeaderCellDef mat-sort-header>
          {{column.label}}
          <span class="sr-only" *ngIf="column.sortable">
            , sortable column
          </span>
        </th>
        <td mat-cell *matCellDef="let row">
          <span [attr.aria-label]="column.label + ': ' + getCellValue(row, column.key)">
            {{getCellValue(row, column.key)}}
          </span>
        </td>
      </ng-container>

      <!-- Actions Column -->
      <ng-container matColumnDef="actions">
        <th mat-header-cell *matHeaderCellDef>Actions</th>
        <td mat-cell *matCellDef="let row">
          <button mat-icon-button
                  [matMenuTriggerFor]="actionMenu"
                  [attr.aria-label]="'Actions for ' + row.name">
            <mat-icon aria-hidden="true">more_vert</mat-icon>
          </button>

          <mat-menu #actionMenu="matMenu">
            <button mat-menu-item
                    *ngFor="let action of getAvailableActions(row)"
                    (click)="executeAction(action, row)"
                    [disabled]="!canExecuteAction(action, row)">
              <mat-icon aria-hidden="true">{{action.icon}}</mat-icon>
              <span>{{action.label}}</span>
            </button>
          </mat-menu>
        </td>
      </ng-container>

      <tr mat-header-row *matHeaderRowDef="allColumns; sticky: true"></tr>
      <tr mat-row *matRowDef="let row; columns: allColumns;"
          [class.selected-row]="selection.isSelected(row)"
          (click)="onRowClick(row)"
          [attr.aria-selected]="selection.isSelected(row)">
      </tr>
    </table>
  </div>

  <mat-paginator [pageSizeOptions]="[10, 25, 50, 100]"
                 [attr.aria-label]="'Pagination for ' + tableTitle"
                 showFirstLastButtons>
  </mat-paginator>
</div>
"""
}