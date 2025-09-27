# -*- coding: utf-8 -*-
"""
Зависимости для Universal Localization Engine Agent.

Универсальная система локализации и интернационализации
для проектов любого типа и масштаба.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from pathlib import Path


@dataclass
class LocalizationEngineDependencies:
    """
    Универсальные зависимости для системы локализации.

    Поддерживает адаптацию под различные типы проектов,
    технологические стеки и требования к локализации.
    """

    # === БАЗОВЫЕ НАСТРОЙКИ ===

    api_key: str
    project_path: str = ""
    agent_name: str = "universal_localization_engine"

    # === КОНФИГУРАЦИЯ ЛОКАЛИЗАЦИИ ===

    # Языки и регионы
    source_language: str = "en"  # Исходный язык проекта
    target_languages: List[str] = field(default_factory=lambda: ["es", "fr", "de", "ru", "zh", "ja"])
    default_locale: str = "en-US"

    # Поддерживаемые локали с расширенной информацией
    supported_locales: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "en-US": {"name": "English (US)", "rtl": False, "currency": "USD", "date_format": "MM/dd/yyyy"},
        "en-GB": {"name": "English (UK)", "rtl": False, "currency": "GBP", "date_format": "dd/MM/yyyy"},
        "es-ES": {"name": "Español (España)", "rtl": False, "currency": "EUR", "date_format": "dd/MM/yyyy"},
        "es-MX": {"name": "Español (México)", "rtl": False, "currency": "MXN", "date_format": "dd/MM/yyyy"},
        "fr-FR": {"name": "Français (France)", "rtl": False, "currency": "EUR", "date_format": "dd/MM/yyyy"},
        "de-DE": {"name": "Deutsch (Deutschland)", "rtl": False, "currency": "EUR", "date_format": "dd.MM.yyyy"},
        "ru-RU": {"name": "Русский (Россия)", "rtl": False, "currency": "RUB", "date_format": "dd.MM.yyyy"},
        "zh-CN": {"name": "中文 (简体)", "rtl": False, "currency": "CNY", "date_format": "yyyy/MM/dd"},
        "zh-TW": {"name": "中文 (繁體)", "rtl": False, "currency": "TWD", "date_format": "yyyy/MM/dd"},
        "ja-JP": {"name": "日本語", "rtl": False, "currency": "JPY", "date_format": "yyyy/MM/dd"},
        "ko-KR": {"name": "한국어", "rtl": False, "currency": "KRW", "date_format": "yyyy.MM.dd"},
        "ar-SA": {"name": "العربية", "rtl": True, "currency": "SAR", "date_format": "dd/MM/yyyy"},
        "he-IL": {"name": "עברית", "rtl": True, "currency": "ILS", "date_format": "dd/MM/yyyy"},
        "hi-IN": {"name": "हिन्दी", "rtl": False, "currency": "INR", "date_format": "dd/MM/yyyy"},
        "th-TH": {"name": "ไทย", "rtl": False, "currency": "THB", "date_format": "dd/MM/yyyy"},
        "vi-VN": {"name": "Tiếng Việt", "rtl": False, "currency": "VND", "date_format": "dd/MM/yyyy"},
        "pt-BR": {"name": "Português (Brasil)", "rtl": False, "currency": "BRL", "date_format": "dd/MM/yyyy"},
        "it-IT": {"name": "Italiano", "rtl": False, "currency": "EUR", "date_format": "dd/MM/yyyy"},
        "nl-NL": {"name": "Nederlands", "rtl": False, "currency": "EUR", "date_format": "dd-MM-yyyy"},
        "sv-SE": {"name": "Svenska", "rtl": False, "currency": "SEK", "date_format": "yyyy-MM-dd"},
        "pl-PL": {"name": "Polski", "rtl": False, "currency": "PLN", "date_format": "dd.MM.yyyy"}
    })

    # === ТЕХНОЛОГИЧЕСКИЙ СТЕК ===

    # Тип проекта (влияет на стратегию локализации)
    project_type: str = "web"  # web, mobile, desktop, api, game, documentation

    # Фреймворк проекта
    framework: str = "universal"  # react, vue, angular, nextjs, flutter, unity, etc.

    # Система управления переводами
    translation_system: str = "json"  # json, yaml, gettext, icu, xliff, properties

    # Архитектура файлов локализации
    localization_structure: str = "namespace"  # flat, namespace, nested, feature-based

    # === НАСТРОЙКИ ПЕРЕВОДА ===

    # Качество перевода
    translation_quality: str = "professional"  # basic, standard, professional, native

    # Режим перевода
    translation_mode: str = "ai_assisted"  # manual, ai_assisted, fully_automated

    # Контекстуальный перевод
    enable_context_awareness: bool = True
    enable_brand_consistency: bool = True
    enable_cultural_adaptation: bool = True

    # AI модели для перевода
    primary_translation_model: str = "gpt-4"
    fallback_translation_model: str = "gemini-pro"
    specialized_models: Dict[str, str] = field(default_factory=lambda: {
        "technical": "claude-3-sonnet",
        "marketing": "gpt-4",
        "legal": "claude-3-opus",
        "creative": "gpt-4-turbo"
    })

    # === КОНТЕНТ И ФОРМАТЫ ===

    # Типы контента для локализации
    content_types: List[str] = field(default_factory=lambda: [
        "ui_text", "marketing_copy", "documentation", "legal_text",
        "emails", "notifications", "error_messages", "help_content"
    ])

    # Форматы файлов
    supported_file_formats: List[str] = field(default_factory=lambda: [
        "json", "yaml", "po", "xliff", "csv", "xlsx", "properties", "xml"
    ])

    # Типы переводимого контента
    translatable_content: Dict[str, bool] = field(default_factory=lambda: {
        "static_text": True,
        "dynamic_content": True,
        "images_with_text": True,
        "video_subtitles": True,
        "audio_transcripts": True,
        "metadata": True,
        "alt_text": True,
        "seo_content": True
    })

    # === ДОМЕН-СПЕЦИФИЧНЫЕ НАСТРОЙКИ ===

    # Тип домена (влияет на терминологию и подход)
    domain_type: str = "general"  # ecommerce, saas, education, healthcare, finance, gaming

    # Специализированные словари
    use_domain_dictionaries: bool = True
    custom_terminology: Dict[str, Dict[str, str]] = field(default_factory=dict)

    # Регулятивные требования
    compliance_requirements: List[str] = field(default_factory=list)  # gdpr, ccpa, hipaa, etc.

    # === АВТОМАТИЗАЦИЯ И WORKFLOW ===

    # Автоматическое обнаружение текста
    auto_text_extraction: bool = True
    scan_file_types: List[str] = field(default_factory=lambda: [
        ".js", ".jsx", ".ts", ".tsx", ".vue", ".html", ".php", ".py", ".java", ".cs"
    ])

    # Workflow автоматизации
    enable_auto_translation: bool = True
    enable_quality_checks: bool = True
    enable_consistency_validation: bool = True
    enable_context_validation: bool = True

    # Интеграции
    translation_services: List[str] = field(default_factory=lambda: [
        "google_translate", "azure_translator", "aws_translate", "deepl"
    ])

    version_control_integration: bool = True
    ci_cd_integration: bool = True

    # === КАЧЕСТВО И ВАЛИДАЦИЯ ===

    # Проверки качества
    quality_checks: Dict[str, bool] = field(default_factory=lambda: {
        "missing_translations": True,
        "placeholder_consistency": True,
        "length_validation": True,
        "format_validation": True,
        "encoding_validation": True,
        "grammar_check": True,
        "terminology_consistency": True,
        "cultural_appropriateness": True
    })

    # Валидация UI
    ui_validation_checks: Dict[str, bool] = field(default_factory=lambda: {
        "text_overflow": True,
        "layout_breaking": True,
        "rtl_support": True,
        "font_support": True,
        "character_encoding": True
    })

    # === ПРОИЗВОДИТЕЛЬНОСТЬ ===

    # Оптимизация загрузки
    enable_lazy_loading: bool = True
    enable_translation_caching: bool = True
    enable_compression: bool = True

    # Fallback стратегии
    fallback_strategy: str = "source_language"  # source_language, default_locale, show_key
    partial_translation_handling: str = "mixed"  # all_or_nothing, mixed, progressive

    # === ИНТЕРНАЦИОНАЛИЗАЦИЯ (I18N) ===

    # Форматирование
    number_formatting: Dict[str, str] = field(default_factory=lambda: {
        "decimal_separator": "auto",  # auto, dot, comma
        "thousands_separator": "auto",  # auto, comma, space, none
        "currency_symbol_position": "auto"  # auto, before, after
    })

    date_time_formatting: Dict[str, str] = field(default_factory=lambda: {
        "date_format": "locale_default",
        "time_format": "locale_default",
        "timezone_handling": "user_timezone"
    })

    # RTL поддержка
    rtl_support_level: str = "full"  # none, basic, full
    bidirectional_text_support: bool = True

    # === ИНТЕГРАЦИЯ С АРХИТЕКТУРОЙ ===

    # Archon интеграция
    archon_project_id: Optional[str] = None
    enable_progress_tracking: bool = True

    # RAG и знания
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "localization", "i18n", "l10n", "translation", "universal-agent"
    ])
    knowledge_domain: Optional[str] = "localization.docs"

    # === РАСШИРЕННЫЕ ВОЗМОЖНОСТИ ===

    # Машинное обучение
    enable_translation_memory: bool = True
    enable_terminology_extraction: bool = True
    enable_quality_prediction: bool = True

    # Аналитика и метрики
    enable_analytics: bool = True
    track_translation_metrics: bool = True
    monitor_user_engagement: bool = True

    # Коллаборация
    enable_translator_workflow: bool = True
    enable_reviewer_workflow: bool = True
    enable_community_contributions: bool = False

    # === БЕЗОПАСНОСТЬ ===

    # Защита данных
    encrypt_translations: bool = False
    sanitize_content: bool = True
    validate_input_security: bool = True

    # Аудит
    enable_change_tracking: bool = True
    enable_approval_workflow: bool = False

    def __post_init__(self):
        """Пост-инициализация с валидацией и автонастройкой."""

        # Валидация языков
        if self.source_language not in [lang.split('-')[0] for lang in self.supported_locales.keys()]:
            # Добавляем поддержку исходного языка если его нет
            self.supported_locales[f"{self.source_language}-XX"] = {
                "name": f"{self.source_language.upper()} (Generic)",
                "rtl": False,
                "currency": "USD",
                "date_format": "MM/dd/yyyy"
            }

        # Автонастройка под тип проекта
        if self.project_type == "mobile":
            # Мобильные приложения требуют более компактных переводов
            self.quality_checks["length_validation"] = True
            self.ui_validation_checks["text_overflow"] = True

        elif self.project_type == "game":
            # Игры требуют креативного подхода и больше контекста
            self.enable_cultural_adaptation = True
            self.specialized_models["creative"] = self.specialized_models.get("creative", "gpt-4-turbo")

        elif self.project_type == "api":
            # API документация требует технической точности
            self.translation_quality = "professional"
            self.content_types = ["documentation", "error_messages", "api_descriptions"]

        # Автонастройка под домен
        if self.domain_type == "ecommerce":
            self.content_types.extend(["product_descriptions", "checkout_flow", "customer_support"])
            self.quality_checks["terminology_consistency"] = True

        elif self.domain_type == "healthcare":
            self.compliance_requirements.extend(["hipaa", "medical_terminology"])
            self.translation_quality = "professional"

        elif self.domain_type == "finance":
            self.compliance_requirements.extend(["financial_regulations", "legal_accuracy"])
            self.specialized_models["legal"] = "claude-3-opus"

        # Настройка файловой структуры
        if not self.project_path:
            self.project_path = str(Path.cwd())

    def get_locale_info(self, locale: str) -> Dict[str, Any]:
        """
        Получить информацию о локали.

        Args:
            locale: Код локали (например, 'en-US')

        Returns:
            Словарь с информацией о локали
        """
        return self.supported_locales.get(locale, self.supported_locales[self.default_locale])

    def is_rtl_locale(self, locale: str) -> bool:
        """
        Проверить, является ли локаль RTL (right-to-left).

        Args:
            locale: Код локали

        Returns:
            True если локаль RTL
        """
        locale_info = self.get_locale_info(locale)
        return locale_info.get("rtl", False)

    def get_currency_for_locale(self, locale: str) -> str:
        """
        Получить валюту для локали.

        Args:
            locale: Код локали

        Returns:
            Код валюты
        """
        locale_info = self.get_locale_info(locale)
        return locale_info.get("currency", "USD")

    def get_supported_languages(self) -> List[str]:
        """
        Получить список поддерживаемых языков.

        Returns:
            Список языковых кодов
        """
        languages = set()
        for locale in self.supported_locales.keys():
            lang = locale.split('-')[0]
            languages.add(lang)
        return sorted(list(languages))

    def get_workflow_config(self) -> Dict[str, Any]:
        """
        Получить конфигурацию workflow для данного проекта.

        Returns:
            Конфигурация workflow
        """
        return {
            "auto_extraction": self.auto_text_extraction,
            "auto_translation": self.enable_auto_translation,
            "quality_checks": self.enable_quality_checks,
            "human_review": self.translation_mode != "fully_automated",
            "approval_workflow": self.enable_approval_workflow,
            "version_control": self.version_control_integration
        }

    def get_quality_config(self) -> Dict[str, Any]:
        """
        Получить конфигурацию проверок качества.

        Returns:
            Конфигурация качества
        """
        return {
            "content_checks": self.quality_checks,
            "ui_checks": self.ui_validation_checks,
            "translation_quality": self.translation_quality,
            "context_awareness": self.enable_context_awareness,
            "brand_consistency": self.enable_brand_consistency
        }


def load_dependencies(
    project_type: str = "web",
    domain_type: str = "general",
    **kwargs
) -> LocalizationEngineDependencies:
    """
    Фабричная функция для создания зависимостей локализации.

    Args:
        project_type: Тип проекта
        domain_type: Домен применения
        **kwargs: Дополнительные параметры

    Returns:
        Настроенные зависимости локализации
    """
    # Базовые настройки из переменных окружения
    import os
    from dotenv import load_dotenv

    load_dotenv()

    base_config = {
        "api_key": os.getenv("LLM_API_KEY", ""),
        "project_path": os.getenv("PROJECT_PATH", ""),
        "project_type": project_type,
        "domain_type": domain_type,
        "archon_project_id": os.getenv("ARCHON_PROJECT_ID")
    }

    # Объединяем с переданными параметрами
    config = {**base_config, **kwargs}

    return LocalizationEngineDependencies(**config)


# Предустановленные конфигурации для различных типов проектов
PRESET_CONFIGURATIONS = {
    "ecommerce_web": {
        "project_type": "web",
        "domain_type": "ecommerce",
        "target_languages": ["es", "fr", "de", "zh", "ja"],
        "content_types": ["ui_text", "product_descriptions", "checkout_flow", "customer_support"],
        "translation_quality": "professional",
        "enable_cultural_adaptation": True
    },

    "saas_platform": {
        "project_type": "web",
        "domain_type": "saas",
        "target_languages": ["es", "fr", "de", "pt", "ja"],
        "content_types": ["ui_text", "documentation", "help_content", "notifications"],
        "translation_quality": "professional",
        "enable_context_awareness": True
    },

    "mobile_app": {
        "project_type": "mobile",
        "domain_type": "general",
        "target_languages": ["es", "fr", "de", "zh", "ar"],
        "content_types": ["ui_text", "notifications", "help_content"],
        "translation_quality": "standard",
        "quality_checks": {"length_validation": True, "text_overflow": True}
    },

    "documentation_site": {
        "project_type": "documentation",
        "domain_type": "technical",
        "target_languages": ["es", "fr", "de", "zh", "ja", "ko"],
        "content_types": ["documentation", "help_content", "api_descriptions"],
        "translation_quality": "professional",
        "specialized_models": {"technical": "claude-3-sonnet"}
    },

    "gaming_platform": {
        "project_type": "game",
        "domain_type": "entertainment",
        "target_languages": ["es", "fr", "de", "ru", "zh", "ja", "ko"],
        "content_types": ["ui_text", "story_content", "character_dialogue"],
        "translation_quality": "native",
        "enable_cultural_adaptation": True,
        "specialized_models": {"creative": "gpt-4-turbo"}
    }
}