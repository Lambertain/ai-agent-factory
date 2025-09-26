"""
Пример конфигурации PWA Mobile Agent для E-commerce проекта.

Демонстрирует настройку агента для интернет-магазинов
с фокусом на offline корзину, payment API и push-уведомления.
"""

from ..dependencies import PWAMobileAgentDependencies


def setup_ecommerce_pwa_agent():
    """Настройка агента для e-commerce PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="ecommerce",
        target_platform="universal",
        offline_strategy="cache-first",

        # E-commerce специфичные настройки
        app_name="Online Store",
        app_short_name="Store",
        app_description="Your favorite online shopping destination",
        theme_color="#4f46e5",
        background_color="#f8fafc",
        start_url="/catalog",
        display_mode="standalone",

        # Функциональные возможности для e-commerce
        enable_push_notifications=True,  # Уведомления о скидках, статусе заказа
        enable_background_sync=True,     # Синхронизация корзины, избранного
        enable_geolocation=True,         # Определение ближайших магазинов
        enable_camera=True,              # Сканирование QR-кодов, поиск по фото
        enable_share_api=True,           # Поделиться товарами
        enable_payment_api=True,         # Web Payment API для оплаты

        # Performance настройки для e-commerce
        cache_strategy="aggressive",     # Агрессивное кэширование каталога
        max_cache_size_mb=100,          # Больше места для товарных изображений
        image_optimization=True,         # Оптимизация товарных фото
        lazy_loading=True,               # Lazy loading в каталоге

        # RAG теги для E-commerce знаний
        knowledge_tags=[
            "pwa-mobile",
            "ecommerce-pwa",
            "agent-knowledge",
            "shopping-cart",
            "payment-api",
            "product-catalog"
        ]
    )


def setup_marketplace_pwa_agent():
    """Настройка агента для marketplace PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="ecommerce",
        target_platform="universal",
        offline_strategy="network-first",

        # Marketplace специфичные настройки
        app_name="Marketplace Hub",
        app_short_name="Market",
        app_description="Buy and sell anything",
        theme_color="#059669",
        background_color="#f0f9ff",
        start_url="/",
        display_mode="standalone",

        # Расширенные возможности для marketplace
        enable_push_notifications=True,
        enable_background_sync=True,
        enable_geolocation=True,
        enable_camera=True,              # Фото товаров для продажи
        enable_share_api=True,
        enable_payment_api=True,

        # Performance для большого каталога
        cache_strategy="adaptive",
        max_cache_size_mb=150,
        image_optimization=True,
        lazy_loading=True,

        # RAG теги для Marketplace знаний
        knowledge_tags=[
            "pwa-mobile",
            "ecommerce-pwa",
            "marketplace",
            "agent-knowledge",
            "multi-vendor",
            "peer-to-peer"
        ]
    )


def example_ecommerce_analysis():
    """Пример анализа e-commerce PWA проекта."""
    ecommerce_deps = setup_ecommerce_pwa_agent()

    return {
        "dependencies": ecommerce_deps,
        "analysis_focus": [
            "Offline корзина и избранное",
            "Payment API интеграция",
            "Push-уведомления о заказах",
            "Каталог товаров с быстрой загрузкой",
            "Geolocation для доставки"
        ],
        "expected_optimizations": [
            "Aggressive caching для товарных изображений",
            "Background sync корзины при offline",
            "Payment Request API для быстрой оплаты",
            "Push notifications для abandoned cart",
            "Camera API для поиска по фото товара",
            "Share API для рекомендаций товаров",
            "Offline режим просмотра каталога"
        ],
        "performance_targets": {
            "catalog_load_time": "< 2s",
            "image_cache_hit_rate": "> 80%",
            "offline_functionality": "100% for cart",
            "payment_flow_completion": "< 30s"
        },
        "pwa_patterns": [
            "Add to Cart offline с sync при восстановлении сети",
            "Product image lazy loading с placeholder",
            "Payment sheet integration с Payment Request API",
            "Push notifications для order status updates",
            "Camera barcode scanning для быстрого добавления",
            "Geolocation для store locator и delivery",
            "Share target для product recommendations"
        ],
        "monetization_features": [
            "Wishlist sync между устройствами",
            "Push notifications для personalized offers",
            "Offline browsing для retention",
            "One-click payments через Payment API",
            "Social sharing для viral growth"
        ]
    }


if __name__ == "__main__":
    print("🛒 E-COMMERCE PWA MOBILE AGENT")
    print("=" * 50)

    config = example_ecommerce_analysis()
    deps = config["dependencies"]

    print(f"PWA type: {deps.pwa_type}")
    print(f"App name: {deps.app_name}")
    print(f"Cache strategy: {deps.cache_strategy}")
    print(f"Theme color: {deps.theme_color}")
    print(f"Payment API: {'enabled' if deps.enable_payment_api else 'disabled'}")
    print("\nReady for e-commerce PWA development!")