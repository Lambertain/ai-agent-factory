"""
Пример конфигурации UI/UX Enhancement Agent для SaaS dashboard проекта.

Демонстрирует настройку агента для B2B SaaS платформы
с фокусом на productivity и data visualization.
"""

from uiux_enhancement_agent import run_uiux_enhancement_sync, AgentDependencies


def setup_saas_agent():
    """Настройка агента для SaaS dashboard проекта."""
    return AgentDependencies(
        project_name="DataPlatform",
        design_system="custom",  # Часто SaaS имеют кастомные дизайн системы
        css_framework="emotion",  # CSS-in-JS популярен в enterprise

        # SaaS специфичная цветовая схема (professional)
        project_specific_colors={
            "brand-primary": "#1E40AF",    # Professional blue
            "brand-secondary": "#6366F1",  # Accent purple
            "data-positive": "#059669",    # Green for positive metrics
            "data-negative": "#DC2626",    # Red for negative metrics
            "data-neutral": "#6B7280",     # Gray for neutral data
            "warning": "#F59E0B",          # Amber for warnings
            "info": "#3B82F6"              # Blue for info
        },

        # SaaS специфичные теги знаний
        knowledge_tags=[
            "uiux-enhancement",
            "saas",
            "dashboard",
            "data-visualization",
            "b2b",
            "enterprise",
            "accessibility"
        ],

        # Enterprise требования к accessibility
        wcag_compliance_level="AA",
        accessibility_tools=["axe-core", "lighthouse", "wave", "pa11y"],

        # Performance для data-heavy приложений
        performance_budget={
            "first_contentful_paint": 2000,  # Сложные dashboard могут быть медленнее
            "cumulative_layout_shift": 0.1,
            "total_blocking_time": 500,  # Больше tolerance для rich apps
            "bundle_size_limit": 200  # Enterprise apps часто больше
        },

        # SaaS специфичные настройки
        theme_support=["light", "dark", "auto"],  # Важно для long work sessions
        high_contrast_support=True,  # Enterprise accessibility
        reduce_motion_support=True   # Для пользователей с чувствительностью
    )


def analyze_metrics_widget():
    """Анализ виджета метрик для dashboard."""
    metrics_widget_html = '''
    <div className="bg-white p-6 rounded-lg shadow-sm border">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Revenue</h3>
        <div className="flex items-center text-green-600">
          <span className="text-sm font-medium">+12.5%</span>
          <svg className="w-4 h-4 ml-1" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" />
          </svg>
        </div>
      </div>
      <div className="text-3xl font-bold text-gray-900 mb-2">$124,563</div>
      <div className="text-sm text-gray-500">vs last month</div>
    </div>
    '''

    deps = setup_saas_agent()

    result = run_uiux_enhancement_sync(
        task="""
        Анализируй виджет метрик для B2B SaaS dashboard.
        Ключевые аспекты:
        1. Data clarity и readability (числа должны быть легко читаемы)
        2. Color coding для positive/negative metrics
        3. Context и reference points (vs last month)
        4. Accessibility для screen readers (ARIA labels для data)
        5. Responsive design для разных экранов
        6. Dark theme support
        """,
        component_code=metrics_widget_html,
        requirements={
            "data_visualization": True,
            "accessibility_level": "WCAG 2.1 AA",
            "theme_support": ["light", "dark"],
            "screen_reader_friendly": True,
            "responsive": True
        }
    )

    return result


def analyze_data_table():
    """Анализ таблицы данных для enterprise dashboard."""
    data_table_html = '''
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Customer
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Revenue
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          <tr>
            <td className="px-6 py-4 whitespace-nowrap">
              <div className="text-sm font-medium text-gray-900">Acme Corp</div>
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              $45,000
            </td>
            <td className="px-6 py-4 whitespace-nowrap">
              <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                Active
              </span>
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button className="text-blue-600 hover:text-blue-900">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    '''

    deps = setup_saas_agent()

    result = run_uiux_enhancement_sync(
        task="""
        Анализируй таблицу данных для enterprise SaaS platform.
        Enterprise требования:
        1. Accessibility для больших таблиц (keyboard navigation, screen readers)
        2. Sorting и filtering indicators
        3. Pagination или virtualization для performance
        4. Consistent data formatting (numbers, dates, currency)
        5. Bulk actions support
        6. Export functionality UX
        7. Mobile responsive или dedicated mobile view
        """,
        component_code=data_table_html,
        requirements={
            "enterprise_grade": True,
            "large_dataset_support": True,
            "keyboard_navigation": True,
            "bulk_operations": True,
            "accessibility_level": "WCAG 2.1 AA"
        }
    )

    return result


def analyze_navigation_sidebar():
    """Анализ боковой навигации для SaaS dashboard."""
    sidebar_html = '''
    <div className="w-64 bg-gray-900 h-screen flex flex-col">
      <div className="p-4">
        <div className="text-white text-xl font-bold">DataPlatform</div>
      </div>
      <nav className="flex-1 px-2 py-4 space-y-2">
        <a href="#" className="bg-gray-800 text-white group flex items-center px-2 py-2 text-sm font-medium rounded-md">
          <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
          </svg>
          Dashboard
        </a>
        <a href="#" className="text-gray-300 hover:bg-gray-700 group flex items-center px-2 py-2 text-sm font-medium rounded-md">
          <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" />
          </svg>
          Customers
        </a>
        <a href="#" className="text-gray-300 hover:bg-gray-700 group flex items-center px-2 py-2 text-sm font-medium rounded-md">
          <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Reports
        </a>
      </nav>
    </div>
    '''

    deps = setup_saas_agent()

    result = run_uiux_enhancement_sync(
        task="""
        Анализируй боковую навигацию для SaaS dashboard.
        Требования для enterprise UX:
        1. Collapsible sidebar для screen real estate
        2. Clear visual hierarchy и grouping
        3. Active state indicators
        4. Keyboard navigation support
        5. Search/filter для большого количества пунктов
        6. Breadcrumbs integration
        7. Mobile responsive behavior
        8. User role-based visibility
        """,
        component_code=sidebar_html,
        requirements={
            "enterprise_navigation": True,
            "collapsible": True,
            "keyboard_support": True,
            "role_based_access": True,
            "mobile_responsive": True
        }
    )

    return result


if __name__ == "__main__":
    print("📊 SAAS DASHBOARD UI/UX ANALYSIS")
    print("=" * 50)

    print("\n📈 METRICS WIDGET ANALYSIS:")
    metrics_result = analyze_metrics_widget()
    print(metrics_result)

    print("\n" + "=" * 50)
    print("\n📋 DATA TABLE ANALYSIS:")
    table_result = analyze_data_table()
    print(table_result)

    print("\n" + "=" * 50)
    print("\n🧭 NAVIGATION SIDEBAR ANALYSIS:")
    sidebar_result = analyze_navigation_sidebar()
    print(sidebar_result)