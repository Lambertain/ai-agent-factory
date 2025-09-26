"""
Пример конфигурации PWA Mobile Agent для Media/News проекта.

Демонстрирует настройку агента для медиа приложений
с фокусом на offline чтение, share API и push-уведомления.
"""

from ..dependencies import PWAMobileAgentDependencies


def setup_news_pwa_agent():
    """Настройка агента для news PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="media",
        target_platform="universal",
        offline_strategy="cache-first",

        # News специфичные настройки
        app_name="Daily News",
        app_short_name="News",
        app_description="Stay informed with latest news",
        theme_color="#dc2626",
        background_color="#fef2f2",
        start_url="/",
        display_mode="standalone",
        orientation="portrait",

        # Функциональные возможности для news
        enable_push_notifications=True,  # Breaking news notifications
        enable_background_sync=True,     # Sync новых статей
        enable_geolocation=False,        # Локальные новости (опционально)
        enable_camera=False,            # Не нужна для чтения
        enable_share_api=True,          # Поделиться статьями
        enable_payment_api=False,       # Подписка через другие методы

        # Performance настройки для media
        cache_strategy="aggressive",     # Агрессивное кэширование статей
        max_cache_size_mb=200,          # Много контента для offline
        image_optimization=True,         # Оптимизация фото в статьях
        lazy_loading=True,              # Lazy loading изображений

        # RAG теги для Media знаний
        knowledge_tags=[
            "pwa-mobile",
            "media-pwa",
            "news-app",
            "agent-knowledge",
            "offline-reading",
            "content-sync"
        ]
    )


def setup_magazine_pwa_agent():
    """Настройка агента для magazine PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="media",
        target_platform="universal",
        offline_strategy="stale-while-revalidate",

        # Magazine специфичные настройки
        app_name="Digital Magazine",
        app_short_name="Magazine",
        app_description="Premium digital magazine experience",
        theme_color="#7c3aed",
        background_color="#faf5ff",
        start_url="/issues",
        display_mode="standalone",
        orientation="any",

        # Возможности для magazine
        enable_push_notifications=True,
        enable_background_sync=True,
        enable_geolocation=False,
        enable_camera=False,
        enable_share_api=True,
        enable_payment_api=True,        # Подписка на журнал

        # Performance для качественного контента
        cache_strategy="conservative",   # Качество важнее размера кэша
        max_cache_size_mb=300,          # Высококачественные изображения
        image_optimization=True,
        lazy_loading=True,

        # RAG теги для Magazine знаний
        knowledge_tags=[
            "pwa-mobile",
            "media-pwa",
            "magazine",
            "agent-knowledge",
            "premium-content",
            "subscription"
        ]
    )


def setup_podcast_pwa_agent():
    """Настройка агента для podcast PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="media",
        target_platform="universal",
        offline_strategy="network-first",

        # Podcast специфичные настройки
        app_name="Podcast Player",
        app_short_name="Podcasts",
        app_description="Your favorite podcasts, anywhere",
        theme_color="#ea580c",
        background_color="#fff7ed",
        start_url="/podcasts",
        display_mode="standalone",
        orientation="portrait",

        # Возможности для podcast
        enable_push_notifications=True,  # Новые эпизоды
        enable_background_sync=True,     # Download эпизодов
        enable_geolocation=False,
        enable_camera=False,
        enable_share_api=True,          # Поделиться эпизодом
        enable_payment_api=True,        # Premium подписки

        # Performance для audio контента
        cache_strategy="adaptive",       # Адаптивно под размер эпизодов
        max_cache_size_mb=500,          # Много аудио файлов
        image_optimization=True,         # Обложки подкастов
        lazy_loading=True,

        # RAG теги для Podcast знаний
        knowledge_tags=[
            "pwa-mobile",
            "media-pwa",
            "podcast",
            "agent-knowledge",
            "audio-streaming",
            "offline-playback"
        ]
    )


def example_media_analysis():
    """Пример анализа media PWA проекта."""
    news_deps = setup_news_pwa_agent()

    return {
        "dependencies": news_deps,
        "analysis_focus": [
            "Offline чтение статей",
            "Background sync новых материалов",
            "Push notifications для breaking news",
            "Share API для социального распространения",
            "Image optimization для быстрой загрузки"
        ],
        "expected_optimizations": [
            "Aggressive caching статей для offline чтения",
            "Background sync новых материалов каждые 30 минут",
            "Push notifications с rich content preview",
            "Share API с native sharing UI",
            "Image lazy loading с progressive enhancement",
            "Reading progress sync между устройствами",
            "Dark mode для комфортного чтения"
        ],
        "performance_targets": {
            "article_load_time": "< 1.5s",
            "offline_content_availability": "> 90%",
            "image_optimization_savings": "> 60%",
            "push_notification_open_rate": "> 15%"
        },
        "pwa_patterns": [
            "Article prefetching на основе reading habits",
            "Offline reading queue с sync статуса прочитанного",
            "Push notifications для trending topics",
            "Share target для получения ссылок из других приложений",
            "Background periodic sync для fresh content",
            "Reading progress indicator с cloud sync",
            "Dark/light theme с system preference detection"
        ],
        "content_features": [
            "Offline reading с full text search",
            "Save for later с categorization",
            "Reading time estimation",
            "Font size и reading preferences",
            "Related articles recommendation",
            "Comment system с offline support"
        ]
    }


if __name__ == "__main__":
    print("📰 MEDIA PWA MOBILE AGENT")
    print("=" * 50)

    config = example_media_analysis()
    deps = config["dependencies"]

    print(f"PWA type: {deps.pwa_type}")
    print(f"App name: {deps.app_name}")
    print(f"Cache strategy: {deps.cache_strategy}")
    print(f"Theme color: {deps.theme_color}")
    print(f"Cache size: {deps.max_cache_size_mb}MB")
    print(f"Share API: {'enabled' if deps.enable_share_api else 'disabled'}")
    print("\nReady for media PWA development!")