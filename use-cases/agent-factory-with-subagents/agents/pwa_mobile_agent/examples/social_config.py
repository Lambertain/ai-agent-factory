"""
Пример конфигурации PWA Mobile Agent для Social проекта.

Демонстрирует настройку агента для социальных приложений
с фокусом на camera API, geolocation, real-time sync и share API.
"""

from ..dependencies import PWAMobileAgentDependencies


def setup_social_network_pwa_agent():
    """Настройка агента для social network PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="social",
        target_platform="universal",
        offline_strategy="network-first",

        # Social network специфичные настройки
        app_name="Social Hub",
        app_short_name="Social",
        app_description="Connect with friends and share moments",
        theme_color="#7c3aed",
        background_color="#faf5ff",
        start_url="/feed",
        display_mode="standalone",
        orientation="portrait",

        # Функциональные возможности для social
        enable_push_notifications=True,  # Уведомления о лайках, комментариях
        enable_background_sync=True,     # Sync постов, сообщений
        enable_geolocation=True,         # Location tagging, nearby friends
        enable_camera=True,              # Фото/видео контент
        enable_share_api=True,          # Native sharing
        enable_payment_api=False,       # Monetization через другие методы

        # Performance настройки для social
        cache_strategy="adaptive",       # Balance fresh content и offline
        max_cache_size_mb=300,          # Много медиа контента
        image_optimization=True,         # Оптимизация фото пользователей
        lazy_loading=True,              # Infinite scroll feed

        # RAG теги для Social знаний
        knowledge_tags=[
            "pwa-mobile",
            "social-pwa",
            "social-network",
            "agent-knowledge",
            "real-time-sync",
            "media-sharing"
        ]
    )


def setup_messaging_pwa_agent():
    """Настройка агента для messaging PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="social",
        target_platform="universal",
        offline_strategy="cache-first",

        # Messaging специфичные настройки
        app_name="Quick Chat",
        app_short_name="Chat",
        app_description="Instant messaging made simple",
        theme_color="#059669",
        background_color="#f0f9ff",
        start_url="/chats",
        display_mode="standalone",
        orientation="portrait",

        # Возможности для messaging
        enable_push_notifications=True,  # Новые сообщения
        enable_background_sync=True,     # Sync сообщений
        enable_geolocation=True,         # Location sharing
        enable_camera=True,              # Photo/video messages
        enable_share_api=True,          # Share content to chat
        enable_payment_api=False,

        # Performance для real-time messaging
        cache_strategy="adaptive",
        max_cache_size_mb=200,          # История сообщений + медиа
        image_optimization=True,
        lazy_loading=True,

        # RAG теги для Messaging знаний
        knowledge_tags=[
            "pwa-mobile",
            "social-pwa",
            "messaging",
            "agent-knowledge",
            "real-time-chat",
            "push-notifications"
        ]
    )


def setup_photo_sharing_pwa_agent():
    """Настройка агента для photo sharing PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="social",
        target_platform="universal",
        offline_strategy="cache-first",

        # Photo sharing специфичные настройки
        app_name="Photo Stories",
        app_short_name="Photos",
        app_description="Share your moments beautifully",
        theme_color="#dc2626",
        background_color="#fef2f2",
        start_url="/photos",
        display_mode="standalone",
        orientation="portrait",

        # Возможности для photo sharing
        enable_push_notifications=True,  # Новые фото друзей
        enable_background_sync=True,     # Upload фото в фоне
        enable_geolocation=True,         # Photo location tagging
        enable_camera=True,              # Main feature - camera
        enable_share_api=True,          # Share photos externally
        enable_payment_api=False,

        # Performance для photo-heavy app
        cache_strategy="aggressive",     # Cache много фото
        max_cache_size_mb=500,          # Большой кэш для фото
        image_optimization=True,         # Critical для фото
        lazy_loading=True,              # Lazy load в галерее

        # RAG теги для Photo sharing знаний
        knowledge_tags=[
            "pwa-mobile",
            "social-pwa",
            "photo-sharing",
            "agent-knowledge",
            "camera-api",
            "image-optimization"
        ]
    )


def example_social_analysis():
    """Пример анализа social PWA проекта."""
    social_deps = setup_social_network_pwa_agent()

    return {
        "dependencies": social_deps,
        "analysis_focus": [
            "Real-time sync для социального контента",
            "Camera API для создания контента",
            "Push notifications для engagement",
            "Geolocation для location-based features",
            "Share API для viral распространения"
        ],
        "expected_optimizations": [
            "Network-first strategy для fresh social content",
            "Camera API с filters и editing",
            "Push notifications с rich media preview",
            "Geolocation для check-ins и nearby friends",
            "Share API с native OS integration",
            "Background sync для offline posting",
            "Adaptive image loading по network quality"
        ],
        "performance_targets": {
            "feed_load_time": "< 2s",
            "camera_open_time": "< 1s",
            "photo_upload_success_rate": "> 95%",
            "push_notification_delivery": "> 90%"
        },
        "pwa_patterns": [
            "Infinite scroll feed с virtual scrolling",
            "Camera capture с instant preview",
            "Push notifications для social engagement",
            "Background upload с retry logic",
            "Share target для receiving content",
            "Geolocation check-ins с privacy controls",
            "Real-time chat с offline message queue"
        ],
        "social_features": [
            "Real-time notifications для social interactions",
            "Camera с built-in filters и editing",
            "Location sharing с privacy controls",
            "Content sharing через native Share API",
            "Offline posting с background sync",
            "Stories/ephemeral content support",
            "Social login с WebAuthn"
        ]
    }


if __name__ == "__main__":
    print("👥 SOCIAL PWA MOBILE AGENT")
    print("=" * 50)

    config = example_social_analysis()
    deps = config["dependencies"]

    print(f"PWA type: {deps.pwa_type}")
    print(f"App name: {deps.app_name}")
    print(f"Theme color: {deps.theme_color}")
    print(f"Camera API: {'enabled' if deps.enable_camera else 'disabled'}")
    print(f"Geolocation: {'enabled' if deps.enable_geolocation else 'disabled'}")
    print(f"Push notifications: {'enabled' if deps.enable_push_notifications else 'disabled'}")
    print(f"Share API: {'enabled' if deps.enable_share_api else 'disabled'}")
    print("\nReady for social PWA development!")