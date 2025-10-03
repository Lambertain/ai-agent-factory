"""
Универсальные зависимости для PWA Mobile Agent.

Поддерживает различные типы PWA приложений через конфигурируемые настройки.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import os


@dataclass
class PWAMobileAgentDependencies:
    """Зависимости PWA Mobile Agent с поддержкой различных типов проектов."""

    # Основные настройки
    agent_name: str = "pwa_mobile"  # For RAG protection
    project_path: str = ""

    # Универсальная конфигурация PWA
    pwa_type: str = "general"  # general, ecommerce, media, productivity, social, gaming
    target_platform: str = "universal"  # universal, ios, android, windows
    offline_strategy: str = "network-first"  # network-first, cache-first, stale-while-revalidate

    # Настройки манифеста
    app_name: str = ""
    app_short_name: str = ""
    app_description: str = ""
    theme_color: str = "#000000"
    background_color: str = "#ffffff"
    start_url: str = "/"
    display_mode: str = "standalone"  # standalone, fullscreen, minimal-ui, browser
    orientation: str = "any"  # any, portrait, landscape

    # Функциональные возможности
    enable_push_notifications: bool = True
    enable_background_sync: bool = True
    enable_geolocation: bool = False
    enable_camera: bool = False
    enable_share_api: bool = True
    enable_payment_api: bool = False

    # Performance настройки
    cache_strategy: str = "adaptive"  # adaptive, aggressive, conservative
    max_cache_size_mb: int = 50
    image_optimization: bool = True
    lazy_loading: bool = True

    # Modern Web APIs настройки
    enable_file_system_access: bool = False
    enable_badging_api: bool = True
    enable_wake_lock: bool = False
    enable_idle_detection: bool = True
    enable_web_locks: bool = False

    # Настройки для Web APIs
    idle_detection_threshold_minutes: int = 5
    wake_lock_auto_mode: bool = False
    file_system_allowed_types: List[str] = field(default_factory=lambda: [".txt", ".md", ".json"])
    web_locks_scope: str = "document"

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=list)
    knowledge_domain: str = ""
    archon_project_id: str = ""
    enable_rag_search: bool = True
    rag_confidence_threshold: float = 0.7

    def __post_init__(self):
        """Инициализация конфигурации PWA на основе типа проекта."""
        if not self.knowledge_tags:
            # Базовые теги для PWA агента
            self.knowledge_tags = ["pwa-mobile", "agent-knowledge", "pydantic-ai"]

            # Добавляем специфичные теги для типа PWA
            type_specific_tags = {
                "ecommerce": ["ecommerce-pwa", "payment-api", "offline-cart"],
                "media": ["media-pwa", "offline-reading", "content-cache"],
                "productivity": ["productivity-pwa", "offline-sync", "data-conflict"],
                "social": ["social-pwa", "real-time", "push-notifications"],
                "gaming": ["gaming-pwa", "performance", "asset-caching"]
            }

            if self.pwa_type in type_specific_tags:
                self.knowledge_tags.extend(type_specific_tags[self.pwa_type])

        # Настройки по типу PWA
        self._setup_pwa_defaults()

        # Настройка environment variables
        self._load_env_settings()

        # Настройка RAG domain если не задан
        if not self.knowledge_domain:
            self._setup_knowledge_domain()

    def _setup_pwa_defaults(self):
        """Настройка значений по умолчанию для разных типов PWA."""
        pwa_defaults = {
            "ecommerce": {
                "enable_payment_api": True,
                "enable_push_notifications": True,
                "enable_share_api": True,
                "cache_strategy": "aggressive",
                "theme_color": "#4f46e5",
                "background_color": "#f8fafc",
                "offline_strategy": "cache-first",
                "knowledge_tags": ["pwa-mobile", "ecommerce-pwa", "agent-knowledge"]
            },
            "media": {
                "enable_share_api": True,
                "enable_push_notifications": True,
                "cache_strategy": "conservative",
                "max_cache_size_mb": 100,
                "theme_color": "#dc2626",
                "background_color": "#000000",
                "offline_strategy": "cache-first",
                "knowledge_tags": ["pwa-mobile", "media-pwa", "agent-knowledge"],
                # Modern Web APIs для media
                "enable_wake_lock": True,
                "enable_idle_detection": True,
                "idle_detection_threshold_minutes": 3
            },
            "productivity": {
                "enable_background_sync": True,
                "enable_push_notifications": False,
                "cache_strategy": "aggressive",
                "theme_color": "#059669",
                "background_color": "#f0f9ff",
                "offline_strategy": "cache-first",
                "knowledge_tags": ["pwa-mobile", "productivity-pwa", "agent-knowledge"],
                # Modern Web APIs для productivity
                "enable_file_system_access": True,
                "enable_web_locks": True,
                "enable_idle_detection": True
            },
            "social": {
                "enable_push_notifications": True,
                "enable_share_api": True,
                "enable_camera": True,
                "enable_geolocation": True,
                "theme_color": "#7c3aed",
                "background_color": "#faf5ff",
                "offline_strategy": "network-first",
                "knowledge_tags": ["pwa-mobile", "social-pwa", "agent-knowledge"]
            },
            "gaming": {
                "display_mode": "fullscreen",
                "orientation": "landscape",
                "enable_push_notifications": True,
                "cache_strategy": "aggressive",
                "max_cache_size_mb": 200,
                "theme_color": "#ea580c",
                "background_color": "#000000",
                "offline_strategy": "cache-first",
                "knowledge_tags": ["pwa-mobile", "gaming-pwa", "agent-knowledge"],
                # Modern Web APIs для gaming
                "enable_wake_lock": True,
                "wake_lock_auto_mode": True,
                "enable_idle_detection": True,
                "idle_detection_threshold_minutes": 10
            }
        }

        if self.pwa_type in pwa_defaults:
            defaults = pwa_defaults[self.pwa_type]
            for key, value in defaults.items():
                if hasattr(self, key) and getattr(self, key) in ["", [], False, 0]:
                    setattr(self, key, value)

    def _load_env_settings(self):
        """Загрузка настроек из environment variables."""
        # PWA настройки из .env
        self.app_name = os.getenv("PWA_APP_NAME", self.app_name)
        self.app_short_name = os.getenv("PWA_SHORT_NAME", self.app_short_name)
        self.app_description = os.getenv("PWA_DESCRIPTION", self.app_description)
        self.theme_color = os.getenv("PWA_THEME_COLOR", self.theme_color)
        self.background_color = os.getenv("PWA_BACKGROUND_COLOR", self.background_color)

        # Performance настройки
        if os.getenv("PWA_MAX_CACHE_SIZE"):
            self.max_cache_size_mb = int(os.getenv("PWA_MAX_CACHE_SIZE", self.max_cache_size_mb))

        # Archon интеграция
        self.archon_project_id = os.getenv("ARCHON_PROJECT_ID", self.archon_project_id)

    def get_manifest_config(self) -> Dict[str, Any]:
        """Получить конфигурацию для PWA манифеста."""
        return {
            "name": self.app_name,
            "short_name": self.app_short_name,
            "description": self.app_description,
            "start_url": self.start_url,
            "display": self.display_mode,
            "orientation": self.orientation,
            "theme_color": self.theme_color,
            "background_color": self.background_color,
            "categories": self._get_categories(),
            "features": self._get_enabled_features()
        }

    def get_service_worker_config(self) -> Dict[str, Any]:
        """Получить конфигурацию для Service Worker."""
        return {
            "cache_strategy": self.cache_strategy,
            "offline_strategy": self.offline_strategy,
            "max_cache_size_mb": self.max_cache_size_mb,
            "enable_push": self.enable_push_notifications,
            "enable_background_sync": self.enable_background_sync,
            "pwa_type": self.pwa_type
        }

    def _get_categories(self) -> List[str]:
        """Получить категории для PWA манифеста на основе типа."""
        category_map = {
            "ecommerce": ["shopping", "business", "lifestyle"],
            "media": ["entertainment", "photo", "video"],
            "productivity": ["productivity", "business", "utilities"],
            "social": ["social", "communication", "entertainment"],
            "gaming": ["games", "entertainment"],
            "general": ["utilities", "lifestyle"]
        }
        return category_map.get(self.pwa_type, ["utilities"])

    def _get_enabled_features(self) -> List[str]:
        """Получить список включенных функций."""
        features = []
        if self.enable_push_notifications:
            features.append("push_notifications")
        if self.enable_background_sync:
            features.append("background_sync")
        if self.enable_geolocation:
            features.append("geolocation")
        if self.enable_camera:
            features.append("camera")
        if self.enable_share_api:
            features.append("share_api")
        if self.enable_payment_api:
            features.append("payment_api")
        return features

    def _setup_knowledge_domain(self):
        """Настроить knowledge domain для RAG поиска."""
        domain_map = {
            "ecommerce": "ecommerce.pwa.docs",
            "media": "media.pwa.docs",
            "productivity": "productivity.pwa.docs",
            "social": "social.pwa.docs",
            "gaming": "gaming.pwa.docs",
            "general": "pwa.docs"
        }
        self.knowledge_domain = domain_map.get(self.pwa_type, "pwa.docs")

    def get_web_apis_config(self) -> Dict[str, Any]:
        """Получить конфигурацию современных Web APIs."""
        return {
            "file_system_access": {
                "enabled": self.enable_file_system_access,
                "allowed_types": self.file_system_allowed_types,
                "recommended_for": ["productivity", "general"]
            },
            "badging_api": {
                "enabled": self.enable_badging_api,
                "recommended_for": ["ecommerce", "social", "productivity", "media", "gaming"]
            },
            "wake_lock": {
                "enabled": self.enable_wake_lock,
                "auto_mode": self.wake_lock_auto_mode,
                "recommended_for": ["gaming", "media"]
            },
            "idle_detection": {
                "enabled": self.enable_idle_detection,
                "threshold_minutes": self.idle_detection_threshold_minutes,
                "recommended_for": ["ecommerce", "productivity", "social", "media"]
            },
            "web_locks": {
                "enabled": self.enable_web_locks,
                "scope": self.web_locks_scope,
                "recommended_for": ["productivity"]
            }
        }

    def get_enabled_web_apis(self) -> List[str]:
        """Получить список включенных Web APIs."""
        enabled_apis = []

        if self.enable_file_system_access:
            enabled_apis.append("File System Access API")
        if self.enable_badging_api:
            enabled_apis.append("Badging API")
        if self.enable_wake_lock:
            enabled_apis.append("Wake Lock API")
        if self.enable_idle_detection:
            enabled_apis.append("Idle Detection API")
        if self.enable_web_locks:
            enabled_apis.append("Web Locks API")

        return enabled_apis