# -*- coding: utf-8 -*-
"""
Универсальные настройки для Universal Media Orchestrator Agent.

Конфигурация поддерживает различные домены применения,
типы проектов и требования к медиа-обработке.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict, validator
from dotenv import load_dotenv


class MediaOrchestratorSettings(BaseSettings):
    """
    Универсальные настройки Universal Media Orchestrator Agent.

    Поддерживает адаптацию под различные домены и типы проектов
    через переменные окружения и конфигурационные файлы.
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="MEDIA_ORCHESTRATOR_"
    )

    # === БАЗОВЫЕ НАСТРОЙКИ ===

    # Пути проекта
    project_path: str = Field(
        default="",
        description="Корневой путь проекта"
    )

    media_assets_path: str = Field(
        default="assets/media",
        description="Путь к медиа-ресурсам относительно project_path"
    )

    output_path: str = Field(
        default="output/media",
        description="Путь для сохранения обработанных медиа"
    )

    temp_path: str = Field(
        default="tmp/media_processing",
        description="Временная папка для обработки"
    )

    # === НАСТРОЙКИ LLM ===

    # Основные API ключи
    llm_api_key: str = Field(
        ...,
        description="API ключ для основной LLM (Qwen/OpenAI Compatible)"
    )

    gemini_api_key: str = Field(
        ...,
        description="Google Gemini API ключ для быстрой обработки"
    )

    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic Claude API ключ для визуального анализа"
    )

    # Конфигурация моделей
    llm_provider: str = Field(
        default="openai_compatible",
        description="Основной провайдер LLM"
    )

    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL для API"
    )

    # Модели для разных типов задач
    default_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Основная модель для медиа-оркестрации"
    )

    image_analysis_model: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="Модель для анализа изображений"
    )

    video_processing_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для обработки видео"
    )

    ai_generation_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для AI-генерации контента"
    )

    quick_processing_model: str = Field(
        default="gemini-2.0-flash-exp",
        description="Быстрая модель для простых задач"
    )

    # === МЕДИА-ОБРАБОТКА ===

    # Поддерживаемые форматы
    supported_image_formats: List[str] = Field(
        default_factory=lambda: ["jpg", "jpeg", "png", "webp", "avif", "svg", "heic", "bmp", "tiff"],
        description="Поддерживаемые форматы изображений"
    )

    supported_video_formats: List[str] = Field(
        default_factory=lambda: ["mp4", "avi", "mov", "mkv", "webm", "flv", "wmv", "m4v"],
        description="Поддерживаемые форматы видео"
    )

    supported_audio_formats: List[str] = Field(
        default_factory=lambda: ["mp3", "wav", "flac", "aac", "ogg", "m4a", "wma"],
        description="Поддерживаемые форматы аудио"
    )

    # Настройки качества по умолчанию
    default_image_quality: int = Field(
        default=85,
        ge=1, le=100,
        description="Качество изображений по умолчанию (1-100)"
    )

    default_video_bitrate: str = Field(
        default="2M",
        description="Битрейт видео по умолчанию"
    )

    default_audio_bitrate: str = Field(
        default="192k",
        description="Битрейт аудио по умолчанию"
    )

    # Максимальные размеры
    max_image_width: int = Field(
        default=4096,
        description="Максимальная ширина изображения"
    )

    max_image_height: int = Field(
        default=4096,
        description="Максимальная высота изображения"
    )

    max_video_resolution: str = Field(
        default="4K",
        description="Максимальное разрешение видео"
    )

    max_file_size_mb: int = Field(
        default=500,
        description="Максимальный размер файла в MB"
    )

    # === ПЛАТФОРМЕННЫЕ НАСТРОЙКИ ===

    # Оптимизация для веб
    web_image_formats: List[str] = Field(
        default_factory=lambda: ["webp", "avif", "jpeg"],
        description="Предпочтительные форматы для веба"
    )

    web_video_codec: str = Field(
        default="h264",
        description="Предпочтительный кодек для веб-видео"
    )

    # Мобильная оптимизация
    mobile_max_width: int = Field(
        default=1080,
        description="Максимальная ширина для мобильных устройств"
    )

    mobile_quality_reduction: int = Field(
        default=10,
        description="Снижение качества для мобильных устройств (%)"
    )

    # Социальные сети
    social_aspect_ratios: Dict[str, str] = Field(
        default_factory=lambda: {
            "instagram_post": "1:1",
            "instagram_story": "9:16",
            "youtube_thumbnail": "16:9",
            "facebook_cover": "851:315",
            "twitter_header": "3:1"
        },
        description="Соотношения сторон для социальных сетей"
    )

    # === ПРОИЗВОДИТЕЛЬНОСТЬ ===

    # Параллельная обработка
    max_parallel_tasks: int = Field(
        default=4,
        description="Максимальное количество параллельных задач"
    )

    batch_size: int = Field(
        default=10,
        description="Размер пакета для массовой обработки"
    )

    # Кэширование
    enable_caching: bool = Field(
        default=True,
        description="Включить кэширование результатов"
    )

    cache_duration_hours: int = Field(
        default=24,
        description="Время жизни кэша в часах"
    )

    # Оптимизация памяти
    memory_limit_mb: int = Field(
        default=2048,
        description="Лимит использования памяти в MB"
    )

    # === AI И ГЕНЕРАЦИЯ ===

    # AI-генерация
    enable_ai_generation: bool = Field(
        default=True,
        description="Включить AI-генерацию контента"
    )

    ai_generation_timeout: int = Field(
        default=60,
        description="Таймаут AI-генерации в секундах"
    )

    # Стили по умолчанию
    default_ai_style: str = Field(
        default="realistic",
        description="Стиль AI-генерации по умолчанию"
    )

    available_ai_styles: List[str] = Field(
        default_factory=lambda: [
            "realistic", "artistic", "cartoon", "sketch",
            "minimalist", "professional", "creative", "abstract"
        ],
        description="Доступные стили AI-генерации"
    )

    # === ДОМЕН-СПЕЦИФИЧНЫЕ НАСТРОЙКИ ===

    # Тип проекта (влияет на оптимизацию)
    project_type: str = Field(
        default="general",
        description="Тип проекта (ecommerce, blog, portfolio, corporate, creative, etc.)"
    )

    domain_type: str = Field(
        default="universal",
        description="Домен применения (web, mobile, print, social, broadcast, etc.)"
    )

    # Брендинг (настраивается под проект)
    brand_colors: List[str] = Field(
        default_factory=list,
        description="Основные цвета бренда в HEX формате"
    )

    brand_fonts: List[str] = Field(
        default_factory=list,
        description="Основные шрифты бренда"
    )

    watermark_enabled: bool = Field(
        default=False,
        description="Включить водяные знаки"
    )

    watermark_text: str = Field(
        default="",
        description="Текст водяного знака"
    )

    # === ИНТЕГРАЦИИ ===

    # Archon интеграция
    archon_project_id: Optional[str] = Field(
        default=None,
        description="ID проекта в Archon для интеграции"
    )

    archon_enabled: bool = Field(
        default=True,
        description="Включить интеграцию с Archon"
    )

    # Внешние сервисы
    cloud_storage_enabled: bool = Field(
        default=False,
        description="Включить облачное хранилище"
    )

    cdn_enabled: bool = Field(
        default=False,
        description="Включить CDN для оптимизации"
    )

    # === БЕЗОПАСНОСТЬ И КОНФИДЕНЦИАЛЬНОСТЬ ===

    # Очистка метаданных
    remove_exif_data: bool = Field(
        default=True,
        description="Удалять EXIF данные из изображений"
    )

    privacy_mode: bool = Field(
        default=False,
        description="Режим повышенной конфиденциальности"
    )

    # Резервное копирование
    backup_original_files: bool = Field(
        default=True,
        description="Создавать резервные копии оригинальных файлов"
    )

    # === ЛОГИРОВАНИЕ И ОТЧЕТНОСТЬ ===

    log_level: str = Field(
        default="INFO",
        description="Уровень логирования"
    )

    enable_detailed_logging: bool = Field(
        default=True,
        description="Включить подробное логирование операций"
    )

    generate_processing_reports: bool = Field(
        default=True,
        description="Генерировать отчеты о обработке"
    )

    # === ЭКСПЕРИМЕНТАЛЬНЫЕ ФУНКЦИИ ===

    experimental_features: bool = Field(
        default=False,
        description="Включить экспериментальные функции"
    )

    beta_ai_models: bool = Field(
        default=False,
        description="Использовать бета-версии AI моделей"
    )

    @validator('project_path')
    def validate_project_path(cls, v):
        """Валидация пути проекта."""
        if v and not Path(v).exists():
            # Если путь не существует, попробуем создать
            try:
                Path(v).mkdir(parents=True, exist_ok=True)
            except Exception:
                pass  # Игнорируем ошибки создания
        return v

    @validator('brand_colors')
    def validate_brand_colors(cls, v):
        """Валидация цветов бренда."""
        valid_colors = []
        for color in v:
            if isinstance(color, str) and (color.startswith('#') or len(color) == 6):
                valid_colors.append(color)
        return valid_colors

    def get_absolute_path(self, relative_path: str) -> str:
        """
        Получить абсолютный путь относительно проекта.

        Args:
            relative_path: Относительный путь

        Returns:
            Абсолютный путь
        """
        if self.project_path:
            return str(Path(self.project_path) / relative_path)
        return relative_path

    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """
        Получить конфигурацию для конкретной платформы.

        Args:
            platform: Название платформы

        Returns:
            Словарь с настройками платформы
        """
        platform_configs = {
            "web": {
                "formats": self.web_image_formats,
                "max_width": self.max_image_width,
                "quality": self.default_image_quality,
                "video_codec": self.web_video_codec
            },
            "mobile": {
                "max_width": self.mobile_max_width,
                "quality": max(1, self.default_image_quality - self.mobile_quality_reduction),
                "formats": ["webp", "jpeg"]
            },
            "social": {
                "aspect_ratios": self.social_aspect_ratios,
                "formats": ["jpeg", "png"],
                "quality": 90
            },
            "print": {
                "dpi": 300,
                "formats": ["tiff", "pdf"],
                "quality": 95,
                "color_mode": "CMYK"
            }
        }

        return platform_configs.get(platform, platform_configs["web"])

    def get_domain_config(self) -> Dict[str, Any]:
        """
        Получить конфигурацию для текущего домена.

        Returns:
            Словарь с настройками домена
        """
        domain_configs = {
            "ecommerce": {
                "image_variants": ["thumbnail", "medium", "large", "zoom"],
                "optimization_priority": "speed",
                "watermark": False,
                "background_removal": True
            },
            "portfolio": {
                "image_variants": ["thumbnail", "large", "fullsize"],
                "optimization_priority": "quality",
                "watermark": True,
                "artistic_effects": True
            },
            "blog": {
                "image_variants": ["thumbnail", "medium"],
                "optimization_priority": "balanced",
                "seo_optimization": True,
                "alt_text_generation": True
            },
            "corporate": {
                "image_variants": ["standard", "presentation"],
                "optimization_priority": "consistency",
                "brand_compliance": True,
                "professional_effects": True
            }
        }

        return domain_configs.get(self.domain_type, domain_configs["blog"])


@dataclass
class ProcessingProfile:
    """Профиль обработки для конкретного типа задач."""

    name: str
    description: str
    target_platforms: List[str] = field(default_factory=list)
    quality_level: str = "high"
    optimization_focus: str = "balanced"  # speed, quality, size, balanced
    ai_enhancement: bool = True
    batch_processing: bool = False
    custom_settings: Dict[str, Any] = field(default_factory=dict)


# Предустановленные профили обработки
PROCESSING_PROFILES = {
    "web_optimization": ProcessingProfile(
        name="Веб-оптимизация",
        description="Оптимизация изображений и видео для веб-сайтов",
        target_platforms=["web", "mobile"],
        quality_level="high",
        optimization_focus="speed",
        ai_enhancement=True,
        batch_processing=True,
        custom_settings={
            "formats": ["webp", "avif", "jpeg"],
            "lazy_loading": True,
            "responsive_variants": True
        }
    ),

    "social_media": ProcessingProfile(
        name="Социальные сети",
        description="Подготовка контента для социальных платформ",
        target_platforms=["social"],
        quality_level="high",
        optimization_focus="balanced",
        ai_enhancement=True,
        batch_processing=True,
        custom_settings={
            "aspect_ratios": True,
            "platform_specific": True,
            "engaging_thumbnails": True
        }
    ),

    "professional_print": ProcessingProfile(
        name="Профессиональная печать",
        description="Подготовка изображений для высококачественной печати",
        target_platforms=["print"],
        quality_level="premium",
        optimization_focus="quality",
        ai_enhancement=False,
        batch_processing=False,
        custom_settings={
            "dpi": 300,
            "color_profile": "CMYK",
            "bleed_margins": True
        }
    ),

    "quick_preview": ProcessingProfile(
        name="Быстрый просмотр",
        description="Быстрая обработка для предварительного просмотра",
        target_platforms=["web"],
        quality_level="medium",
        optimization_focus="speed",
        ai_enhancement=False,
        batch_processing=True,
        custom_settings={
            "low_resolution": True,
            "minimal_processing": True,
            "fast_algorithms": True
        }
    )
}


def load_settings() -> MediaOrchestratorSettings:
    """
    Загрузить настройки из переменных окружения и файлов конфигурации.

    Returns:
        Экземпляр настроек
    """
    # Загружаем переменные окружения
    load_dotenv()

    try:
        settings = MediaOrchestratorSettings()

        # Автоматически определяем project_path если не указан
        if not settings.project_path:
            # Пытаемся определить из переменных окружения или текущей директории
            settings.project_path = os.getenv("PROJECT_PATH", str(Path.cwd()))

        return settings

    except Exception as e:
        error_msg = f"Не удалось загрузить настройки Media Orchestrator Agent: {e}"

        # Специальные сообщения для частых ошибок
        if "llm_api_key" in str(e).lower():
            error_msg += "\n🔑 Убедитесь, что MEDIA_ORCHESTRATOR_LLM_API_KEY или LLM_API_KEY указан в .env файле"

        if "gemini_api_key" in str(e).lower():
            error_msg += "\n🔑 Убедитесь, что MEDIA_ORCHESTRATOR_GEMINI_API_KEY или GEMINI_API_KEY указан в .env файле"

        raise ValueError(error_msg) from e


def get_processing_profile(profile_name: str) -> ProcessingProfile:
    """
    Получить профиль обработки по имени.

    Args:
        profile_name: Название профиля

    Returns:
        Профиль обработки
    """
    return PROCESSING_PROFILES.get(profile_name, PROCESSING_PROFILES["web_optimization"])


def list_processing_profiles() -> List[str]:
    """
    Получить список доступных профилей обработки.

    Returns:
        Список названий профилей
    """
    return list(PROCESSING_PROFILES.keys())


def create_custom_profile(
    name: str,
    description: str,
    target_platforms: List[str],
    **kwargs
) -> ProcessingProfile:
    """
    Создать пользовательский профиль обработки.

    Args:
        name: Название профиля
        description: Описание профиля
        target_platforms: Целевые платформы
        **kwargs: Дополнительные параметры

    Returns:
        Новый профиль обработки
    """
    return ProcessingProfile(
        name=name,
        description=description,
        target_platforms=target_platforms,
        **kwargs
    )