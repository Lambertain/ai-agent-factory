"""
Пример конфигурации PWA Mobile Agent для Productivity проекта.

Демонстрирует настройку агента для productivity приложений
с фокусом на offline редактирование, sync и minimal UI.
"""

from ..dependencies import PWAMobileAgentDependencies


def setup_task_manager_pwa_agent():
    """Настройка агента для task manager PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="productivity",
        target_platform="universal",
        offline_strategy="cache-first",

        # Task manager специфичные настройки
        app_name="Task Manager",
        app_short_name="Tasks",
        app_description="Organize your work and life",
        theme_color="#059669",
        background_color="#f0f9ff",
        start_url="/tasks",
        display_mode="minimal-ui",      # Minimal UI для фокуса
        orientation="portrait",

        # Функциональные возможности для productivity
        enable_push_notifications=False, # Не отвлекаем, только важные
        enable_background_sync=True,     # Sync задач критичен
        enable_geolocation=False,        # Опционально для location-based tasks
        enable_camera=False,            # Опционально для документов
        enable_share_api=True,          # Поделиться проектами
        enable_payment_api=False,       # Premium через другие методы

        # Performance настройки для productivity
        cache_strategy="aggressive",     # Быстрый доступ к данным
        max_cache_size_mb=50,           # Компактные текстовые данные
        image_optimization=True,         # Для attachments
        lazy_loading=True,

        # RAG теги для Productivity знаний
        knowledge_tags=[
            "pwa-mobile",
            "productivity-pwa",
            "task-management",
            "agent-knowledge",
            "offline-editing",
            "data-sync"
        ]
    )


def setup_note_taking_pwa_agent():
    """Настройка агента для note taking PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="productivity",
        target_platform="universal",
        offline_strategy="cache-first",

        # Note taking специфичные настройки
        app_name="Smart Notes",
        app_short_name="Notes",
        app_description="Capture ideas instantly",
        theme_color="#6366f1",
        background_color="#f8fafc",
        start_url="/notes",
        display_mode="standalone",
        orientation="portrait",

        # Возможности для note taking
        enable_push_notifications=False, # Не нужны для заметок
        enable_background_sync=True,     # Sync заметок
        enable_geolocation=False,
        enable_camera=True,             # Фото в заметки
        enable_share_api=True,          # Поделиться заметками
        enable_payment_api=False,

        # Performance для быстрого ввода
        cache_strategy="aggressive",
        max_cache_size_mb=100,          # Место для фото в заметках
        image_optimization=True,
        lazy_loading=True,

        # RAG теги для Note taking знаний
        knowledge_tags=[
            "pwa-mobile",
            "productivity-pwa",
            "note-taking",
            "agent-knowledge",
            "rich-text-editor",
            "offline-editing"
        ]
    )


def setup_calendar_pwa_agent():
    """Настройка агента для calendar PWA проекта."""
    return PWAMobileAgentDependencies(
        pwa_type="productivity",
        target_platform="universal",
        offline_strategy="network-first",

        # Calendar специфичные настройки
        app_name="Smart Calendar",
        app_short_name="Calendar",
        app_description="Manage your time effectively",
        theme_color="#7c3aed",
        background_color="#faf5ff",
        start_url="/calendar",
        display_mode="standalone",
        orientation="portrait",

        # Возможности для calendar
        enable_push_notifications=True,  # Напоминания о событиях
        enable_background_sync=True,     # Sync событий
        enable_geolocation=True,         # Location-based reminders
        enable_camera=False,
        enable_share_api=True,          # Поделиться событиями
        enable_payment_api=False,

        # Performance для real-time данных
        cache_strategy="adaptive",       # Balance между fresh data и offline
        max_cache_size_mb=30,           # Компактные календарные данные
        image_optimization=True,
        lazy_loading=False,             # Быстрый доступ к календарю

        # RAG теги для Calendar знаний
        knowledge_tags=[
            "pwa-mobile",
            "productivity-pwa",
            "calendar",
            "agent-knowledge",
            "scheduling",
            "notifications"
        ]
    )


def example_productivity_analysis():
    """Пример анализа productivity PWA проекта."""
    task_deps = setup_task_manager_pwa_agent()

    return {
        "dependencies": task_deps,
        "analysis_focus": [
            "Offline editing с конфликт resolution",
            "Background sync для real-time collaboration",
            "Minimal UI для максимального фокуса",
            "Fast startup для quick capture",
            "Data persistence для критичных данных"
        ],
        "expected_optimizations": [
            "Aggressive caching для instant app startup",
            "Offline-first editing с operational transforms",
            "Background sync с conflict resolution UI",
            "Minimal UI с gesture navigation",
            "Quick actions с keyboard shortcuts",
            "Data compression для efficient sync",
            "Progressive enhancement для advanced features"
        ],
        "performance_targets": {
            "app_startup_time": "< 1s",
            "offline_editing_reliability": "99.9%",
            "sync_conflict_resolution": "< 5s",
            "data_save_latency": "< 100ms"
        },
        "pwa_patterns": [
            "Offline-first editing с IndexedDB storage",
            "Background sync с smart conflict resolution",
            "Quick capture widget на home screen",
            "Keyboard shortcuts для power users",
            "Gesture navigation для mobile efficiency",
            "Auto-save с visual feedback",
            "Dark mode для long working sessions"
        ],
        "productivity_features": [
            "Offline editing с полной функциональностью",
            "Real-time collaboration sync",
            "Smart notifications только для важного",
            "Quick capture с minimal friction",
            "Search across всех данных",
            "Export в различные форматы",
            "Integration с external productivity tools"
        ]
    }


if __name__ == "__main__":
    print("⚡ PRODUCTIVITY PWA MOBILE AGENT")
    print("=" * 50)

    config = example_productivity_analysis()
    deps = config["dependencies"]

    print(f"PWA type: {deps.pwa_type}")
    print(f"App name: {deps.app_name}")
    print(f"Display mode: {deps.display_mode}")
    print(f"Cache strategy: {deps.cache_strategy}")
    print(f"Background sync: {'enabled' if deps.enable_background_sync else 'disabled'}")
    print(f"Push notifications: {'enabled' if deps.enable_push_notifications else 'disabled'}")
    print("\nReady for productivity PWA development!")