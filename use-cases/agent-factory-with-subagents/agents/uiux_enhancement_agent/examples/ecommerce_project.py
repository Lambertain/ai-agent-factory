"""
Пример конфигурации UI/UX Enhancement Agent для e-commerce проекта.

Демонстрирует настройку агента для интернет-магазина
с фокусом на conversion optimization и accessibility.
"""

from uiux_enhancement_agent import run_uiux_enhancement_sync, AgentDependencies


def setup_ecommerce_agent():
    """Настройка агента для e-commerce проекта."""
    return AgentDependencies(
        project_name="ShopApp",
        design_system="shadcn/ui",
        css_framework="tailwind",

        # E-commerce специфичная цветовая схема
        project_specific_colors={
            "brand-primary": "#059669",    # Green - trust, money
            "brand-secondary": "#DC2626",  # Red - urgency, sale
            "brand-accent": "#F59E0B",     # Amber - warnings, promotions
            "conversion": "#10B981",       # Success green for CTA
            "trust": "#3B82F6"             # Blue - security, trust badges
        },

        # Специализированные теги знаний
        knowledge_tags=[
            "uiux-enhancement",
            "ecommerce",
            "conversion",
            "shadcn",
            "tailwind",
            "accessibility"
        ],

        # E-commerce специфичные настройки
        wcag_compliance_level="AA",  # Критично для доступности покупок

        # Performance бюджет для e-commerce
        performance_budget={
            "first_contentful_paint": 1200,  # Быстрая загрузка критична
            "cumulative_layout_shift": 0.05,  # Стабильность для checkout
            "total_blocking_time": 200,
            "bundle_size_limit": 80  # Мобильные пользователи
        }
    )


def analyze_product_card():
    """Анализ карточки товара для e-commerce."""
    product_card_html = '''
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <img src={product.image} alt={product.name} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h3 className="font-semibold text-lg mb-2">{product.name}</h3>
        <p className="text-gray-600 text-sm mb-3">{product.description}</p>
        <div className="flex justify-between items-center">
          <span className="text-2xl font-bold text-green-600">${product.price}</span>
          <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Add to Cart
          </button>
        </div>
      </div>
    </div>
    '''

    deps = setup_ecommerce_agent()

    result = run_uiux_enhancement_sync(
        task="""
        Проанализируй карточку товара для e-commerce сайта.
        Фокус на:
        1. Conversion optimization (CTA visibility, trust signals)
        2. Mobile-first дизайн
        3. Accessibility для людей с ограничениями
        4. Performance (loading speed, image optimization)
        """,
        component_code=product_card_html,
        requirements={
            "accessibility_level": "WCAG 2.1 AA",
            "conversion_focus": True,
            "mobile_first": True,
            "trust_signals": True
        }
    )

    return result


def analyze_checkout_form():
    """Анализ формы оформления заказа."""
    checkout_form_html = '''
    <form className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Email</label>
        <input type="email" className="w-full px-3 py-2 border rounded-md" />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Card Number</label>
        <input type="text" className="w-full px-3 py-2 border rounded-md" />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Expiry</label>
          <input type="text" placeholder="MM/YY" className="w-full px-3 py-2 border rounded-md" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">CVV</label>
          <input type="text" className="w-full px-3 py-2 border rounded-md" />
        </div>
      </div>
      <button type="submit" className="w-full bg-green-600 text-white py-3 rounded-md font-semibold">
        Complete Order
      </button>
    </form>
    '''

    deps = setup_ecommerce_agent()

    result = run_uiux_enhancement_sync(
        task="""
        Анализируй форму checkout для максимальной конверсии.
        Критические аспекты:
        1. Безопасность данных (visual security indicators)
        2. Минимизация abandonment (простота заполнения)
        3. Error handling и validation
        4. Trust elements (security badges, SSL indicators)
        5. Mobile experience
        """,
        component_code=checkout_form_html,
        requirements={
            "security_focus": True,
            "error_prevention": True,
            "conversion_optimization": True,
            "mobile_checkout": True
        }
    )

    return result


if __name__ == "__main__":
    print("🛒 E-COMMERCE UI/UX ANALYSIS")
    print("=" * 50)

    print("\n📦 PRODUCT CARD ANALYSIS:")
    product_result = analyze_product_card()
    print(product_result)

    print("\n" + "=" * 50)
    print("\n💳 CHECKOUT FORM ANALYSIS:")
    checkout_result = analyze_checkout_form()
    print(checkout_result)