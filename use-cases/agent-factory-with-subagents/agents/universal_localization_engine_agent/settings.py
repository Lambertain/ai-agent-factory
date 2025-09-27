"""
Конфигурационные настройки для Universal Localization Engine Agent.
Предоставляет гибкие параметры для локализации различных типов проектов.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import os


@dataclass
class LocalizationSettings:
    """Основные настройки локализации"""

    # Языковые настройки
    default_source_language: str = "en"
    supported_target_languages: List[str] = field(default_factory=lambda: [
        "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko", "ar",
        "hi", "nl", "sv", "da", "no", "fi", "pl", "tr", "he", "th"
    ])

    # Настройки качества перевода
    default_quality_level: str = "professional"  # basic, standard, professional, native
    enable_quality_validation: bool = True
    quality_threshold: float = 0.85

    # Культурная адаптация
    enable_cultural_adaptation: bool = True
    enable_regional_variants: bool = True
    enable_rtl_support: bool = True

    # Технические настройки
    max_concurrent_translations: int = 5
    translation_batch_size: int = 100
    enable_translation_memory: bool = True
    enable_terminology_management: bool = True

    # Файловые настройки
    output_format: str = "json"  # json, csv, xml, yaml, properties
    preserve_file_structure: bool = True
    create_backup_files: bool = True

    # Настройки валидации
    enable_ui_compatibility_check: bool = True
    enable_length_validation: bool = True
    enable_placeholder_validation: bool = True
    enable_encoding_validation: bool = True


@dataclass
class ProjectTypeSettings:
    """Настройки для различных типов проектов"""

    web: Dict[str, Any] = field(default_factory=lambda: {
        "file_patterns": ["*.html", "*.js", "*.ts", "*.jsx", "*.tsx", "*.vue", "*.svelte"],
        "extract_patterns": {
            "text_content": r'(?:>)([^<]+)(?:<)',
            "attributes": r'(?:title|alt|placeholder|aria-label)=["\']([^"\']+)["\']',
            "js_strings": r'(?:__|t|i18n)\(["\']([^"\']+)["\']'
        },
        "output_structure": "nested",
        "ui_length_limits": {"button": 20, "menu": 30, "title": 50, "description": 200}
    })

    mobile: Dict[str, Any] = field(default_factory=lambda: {
        "platforms": ["ios", "android", "react_native", "flutter", "xamarin"],
        "file_patterns": {
            "ios": ["*.strings", "*.stringsdict", "Localizable.strings"],
            "android": ["strings.xml", "arrays.xml", "plurals.xml"],
            "react_native": ["*.json", "*.js", "*.ts"],
            "flutter": ["*.arb", "*.json"],
            "xamarin": ["*.resx", "*.xml"]
        },
        "screen_size_considerations": True,
        "platform_specific_guidelines": True
    })

    desktop: Dict[str, Any] = field(default_factory=lambda: {
        "frameworks": ["electron", "wpf", "winforms", "qt", "gtk", "cocoa"],
        "file_patterns": ["*.po", "*.pot", "*.properties", "*.resx", "*.qm"],
        "menu_structure_preservation": True,
        "keyboard_shortcuts_localization": True
    })

    api: Dict[str, Any] = field(default_factory=lambda: {
        "documentation_formats": ["openapi", "swagger", "postman", "markdown"],
        "error_message_patterns": True,
        "response_localization": True,
        "api_endpoint_documentation": True
    })

    game: Dict[str, Any] = field(default_factory=lambda: {
        "engines": ["unity", "unreal", "godot", "custom"],
        "asset_localization": True,
        "audio_localization": True,
        "ui_asset_adaptation": True,
        "cultural_content_adaptation": True,
        "rating_compliance": True
    })

    documentation: Dict[str, Any] = field(default_factory=lambda: {
        "formats": ["markdown", "rst", "docx", "pdf", "wiki", "confluence"],
        "structure_preservation": True,
        "cross_reference_updates": True,
        "image_caption_localization": True,
        "code_comment_localization": True
    })


@dataclass
class QualitySettings:
    """Настройки контроля качества"""

    validation_rules: Dict[str, Any] = field(default_factory=lambda: {
        "length_variance_threshold": 0.3,  # Допустимое отклонение длины текста
        "placeholder_preservation": True,
        "html_tag_preservation": True,
        "number_format_localization": True,
        "date_format_localization": True,
        "currency_localization": True,
        "measurement_unit_conversion": True
    })

    linguistic_checks: Dict[str, Any] = field(default_factory=lambda: {
        "grammar_check": True,
        "spelling_check": True,
        "terminology_consistency": True,
        "style_guide_compliance": True,
        "tone_consistency": True
    })

    cultural_checks: Dict[str, Any] = field(default_factory=lambda: {
        "cultural_sensitivity": True,
        "local_regulation_compliance": True,
        "market_specific_adaptation": True,
        "color_symbolism_check": True,
        "imagery_appropriateness": True
    })


@dataclass
class WorkflowSettings:
    """Настройки рабочих процессов"""

    automation_level: str = "high"  # low, medium, high, full

    workflow_stages: List[str] = field(default_factory=lambda: [
        "extraction",
        "preparation",
        "translation",
        "review",
        "cultural_adaptation",
        "quality_validation",
        "ui_testing",
        "deployment"
    ])

    approval_required: Dict[str, bool] = field(default_factory=lambda: {
        "high_visibility_content": True,
        "legal_content": True,
        "marketing_content": True,
        "ui_critical_content": True,
        "brand_content": True
    })

    integration_settings: Dict[str, Any] = field(default_factory=lambda: {
        "version_control": True,
        "ci_cd_integration": True,
        "project_management_sync": True,
        "notification_channels": ["email", "slack", "teams"],
        "progress_tracking": True
    })


@dataclass
class CostOptimizationSettings:
    """Настройки оптимизации затрат"""

    cost_priority: str = "balanced"  # cost_first, quality_first, balanced, speed_first

    model_selection_strategy: Dict[str, Any] = field(default_factory=lambda: {
        "simple_content": "cost_optimized",
        "technical_content": "quality_optimized",
        "creative_content": "premium",
        "bulk_content": "batch_optimized"
    })

    caching_settings: Dict[str, Any] = field(default_factory=lambda: {
        "enable_translation_cache": True,
        "cache_duration_days": 30,
        "cache_similarity_threshold": 0.95,
        "enable_fuzzy_matching": True
    })

    batch_processing: Dict[str, Any] = field(default_factory=lambda: {
        "enable_batching": True,
        "optimal_batch_size": 100,
        "batch_timeout_minutes": 30,
        "parallel_processing": True
    })


class LocalizationEngineConfig:
    """Главный класс конфигурации для Universal Localization Engine Agent"""

    def __init__(self, config_path: Optional[str] = None):
        self.general = LocalizationSettings()
        self.project_types = ProjectTypeSettings()
        self.quality = QualitySettings()
        self.workflow = WorkflowSettings()
        self.cost_optimization = CostOptimizationSettings()

        if config_path and os.path.exists(config_path):
            self.load_from_file(config_path)

    def load_from_file(self, config_path: str):
        """Загрузка конфигурации из файла"""
        import json
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                self._update_from_dict(config_data)
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")

    def save_to_file(self, config_path: str):
        """Сохранение конфигурации в файл"""
        import json
        try:
            config_data = self._to_dict()
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")

    def get_project_config(self, project_type: str) -> Dict[str, Any]:
        """Получение конфигурации для конкретного типа проекта"""
        project_configs = {
            "web": self.project_types.web,
            "mobile": self.project_types.mobile,
            "desktop": self.project_types.desktop,
            "api": self.project_types.api,
            "game": self.project_types.game,
            "documentation": self.project_types.documentation
        }
        return project_configs.get(project_type, self.project_types.web)

    def get_quality_config(self, quality_level: str) -> Dict[str, Any]:
        """Получение конфигурации качества"""
        base_config = self.quality.validation_rules.copy()

        if quality_level == "native":
            base_config.update({
                "require_human_review": True,
                "cultural_expert_review": True,
                "market_testing": True
            })
        elif quality_level == "professional":
            base_config.update({
                "linguistic_review": True,
                "terminology_check": True,
                "style_guide_check": True
            })
        elif quality_level == "standard":
            base_config.update({
                "basic_validation": True,
                "automated_checks": True
            })

        return base_config

    def get_cost_config(self, cost_priority: str) -> Dict[str, Any]:
        """Получение конфигурации оптимизации затрат"""
        self.cost_optimization.cost_priority = cost_priority
        return self.cost_optimization.__dict__

    def _update_from_dict(self, config_dict: Dict[str, Any]):
        """Обновление конфигурации из словаря"""
        for section, values in config_dict.items():
            if hasattr(self, section):
                section_obj = getattr(self, section)
                for key, value in values.items():
                    if hasattr(section_obj, key):
                        setattr(section_obj, key, value)

    def _to_dict(self) -> Dict[str, Any]:
        """Преобразование конфигурации в словарь"""
        return {
            "general": self.general.__dict__,
            "project_types": self.project_types.__dict__,
            "quality": self.quality.__dict__,
            "workflow": self.workflow.__dict__,
            "cost_optimization": self.cost_optimization.__dict__
        }


# Глобальный экземпляр конфигурации
localization_config = LocalizationEngineConfig()

# Функции для быстрого доступа к настройкам
def get_supported_languages() -> List[str]:
    """Получение списка поддерживаемых языков"""
    return localization_config.general.supported_target_languages

def get_project_settings(project_type: str) -> Dict[str, Any]:
    """Получение настроек для типа проекта"""
    return localization_config.get_project_config(project_type)

def get_quality_settings(quality_level: str) -> Dict[str, Any]:
    """Получение настроек качества"""
    return localization_config.get_quality_config(quality_level)

def update_settings(section: str, settings: Dict[str, Any]):
    """Обновление настроек"""
    if hasattr(localization_config, section):
        section_obj = getattr(localization_config, section)
        for key, value in settings.items():
            if hasattr(section_obj, key):
                setattr(section_obj, key, value)