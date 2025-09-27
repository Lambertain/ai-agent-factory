# -*- coding: utf-8 -*-
"""
Universal Media Orchestrator Agent - Управление зависимостями

Конфигурация зависимостей для универсального агента оркестрации медиа
с поддержкой различных типов медиа, платформ и режимов обработки.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


@dataclass
class MediaOrchestratorDependencies:
    """
    Зависимости для Universal Media Orchestrator Agent.

    Поддерживает оркестрацию медиа-контента:
    - Обработка изображений, видео, аудио
    - AI генерация медиа-контента
    - Оптимизация под платформы
    - Создание композиций и анимаций
    - Управление медиа-пайплайнами
    """

    # === ОСНОВНЫЕ НАСТРОЙКИ ===
    api_key: str
    project_path: str = ""

    # === КОНФИГУРАЦИЯ МЕДИА ===
    media_type: str = "image"  # image, video, audio, animation, presentation, composite
    processing_mode: str = "optimize"  # optimize, transform, generate, composite, analyze
    target_platform: str = "web"  # web, mobile, social, print, presentation, broadcast
    quality_level: str = "high"  # low, medium, high, premium, lossless
    output_format: str = "auto"  # auto или конкретный формат

    # === ОБРАБОТКА ИЗОБРАЖЕНИЙ ===
    image_format: str = "auto"  # jpeg, png, webp, avif, svg, gif
    image_quality: int = 85  # 1-100
    image_max_width: int = 1920
    image_max_height: int = 1080
    image_compression_mode: str = "balanced"  # quality, balanced, size
    image_color_profile: str = "sRGB"  # sRGB, Adobe RGB, P3
    image_dpi: int = 72  # DPI для печати

    # === ОБРАБОТКА ВИДЕО ===
    video_codec: str = "h264"  # h264, h265, vp9, av1
    video_resolution: str = "1080p"  # 480p, 720p, 1080p, 1440p, 4k
    video_fps: int = 30  # 24, 30, 60
    video_bitrate: str = "auto"  # auto или конкретное значение
    video_container: str = "mp4"  # mp4, webm, mov, avi
    video_audio_codec: str = "aac"  # aac, mp3, opus

    # === ОБРАБОТКА АУДИО ===
    audio_format: str = "mp3"  # mp3, wav, flac, ogg, aac
    audio_bitrate: int = 192  # kbps
    audio_sample_rate: int = 44100  # Hz
    audio_channels: int = 2  # 1 (mono), 2 (stereo), 5.1, 7.1
    audio_normalize: bool = True

    # === AI ГЕНЕРАЦИЯ ===
    enable_ai_generation: bool = True
    ai_generation_model: str = "stable_diffusion"  # stable_diffusion, midjourney, dalle
    ai_generation_style: str = "realistic"  # realistic, artistic, cartoon, abstract
    ai_generation_quality: str = "high"  # low, medium, high, ultra
    ai_prompt_enhancement: bool = True

    # === ЭФФЕКТЫ И ФИЛЬТРЫ ===
    enable_effects: bool = True
    color_correction: bool = False
    noise_reduction: bool = False
    sharpening: bool = False
    blur_effect: str = "none"  # none, gaussian, motion, radial
    artistic_filters: List[str] = field(default_factory=list)

    # === ПЛАТФОРМЕННАЯ ОПТИМИЗАЦИЯ ===

    # Социальные сети
    instagram_optimization: bool = False
    instagram_aspect_ratios: List[str] = field(default_factory=lambda: ["1:1", "4:5", "9:16"])
    youtube_optimization: bool = False
    youtube_thumbnails: bool = False
    tiktok_optimization: bool = False
    facebook_optimization: bool = False
    linkedin_optimization: bool = False

    # Веб-платформы
    web_optimization: bool = True
    responsive_breakpoints: List[int] = field(default_factory=lambda: [320, 768, 1024, 1440])
    webp_support: bool = True
    avif_support: bool = False
    lazy_loading_optimization: bool = True

    # Мобильные платформы
    mobile_optimization: bool = True
    retina_support: bool = True
    mobile_first: bool = False

    # Печать
    print_optimization: bool = False
    print_dpi: int = 300
    cmyk_conversion: bool = False

    # === КОМПОЗИЦИИ И АНИМАЦИИ ===
    composition_type: str = "single"  # single, collage, slideshow, animation, interactive
    layout_style: str = "auto"  # auto, grid, masonry, freeform, template
    animation_type: str = "none"  # none, fade, slide, zoom, custom
    animation_duration: float = 1.0  # секунды
    transition_effects: List[str] = field(default_factory=list)

    # === БРЕНДИНГ И СТИЛЬ ===
    brand_colors: List[str] = field(default_factory=list)  # HEX цвета
    brand_fonts: List[str] = field(default_factory=list)
    watermark_enabled: bool = False
    watermark_position: str = "bottom_right"  # corners, center, custom
    watermark_opacity: float = 0.5

    # === МЕТАДАННЫЕ И SEO ===
    include_metadata: bool = True
    alt_text_generation: bool = True
    seo_optimization: bool = True
    structured_data: bool = False
    copyright_info: str = ""
    keywords: List[str] = field(default_factory=list)

    # === ПАКЕТНАЯ ОБРАБОТКА ===
    batch_processing: bool = False
    batch_size: int = 10
    parallel_processing: bool = True
    max_concurrent_tasks: int = 4
    progress_tracking: bool = True

    # === ОБЛАЧНЫЕ СЕРВИСЫ ===
    cloud_storage_enabled: bool = False
    cloud_provider: str = "none"  # aws, gcp, azure, cloudinary
    cdn_optimization: bool = False
    auto_backup: bool = False

    # === БЕЗОПАСНОСТЬ И КОНФИДЕНЦИАЛЬНОСТЬ ===
    privacy_mode: bool = False
    exif_data_removal: bool = True
    face_detection_blur: bool = False
    content_filtering: bool = False
    adult_content_detection: bool = False

    # === ПРОИЗВОДИТЕЛЬНОСТЬ ===
    caching_enabled: bool = True
    cache_duration: int = 3600  # секунды
    memory_limit: str = "2GB"
    disk_space_limit: str = "10GB"
    cleanup_temp_files: bool = True

    # === RAG И KNOWLEDGE BASE ===
    agent_name: str = "universal_media_orchestrator"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "media-orchestration", "image-processing", "video-editing", "audio-processing", "agent-knowledge", "pydantic-ai"
    ])
    knowledge_domain: str = ""
    archon_project_id: str = ""

    # === МЕЖАГЕНТНОЕ ВЗАИМОДЕЙСТВИЕ ===
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"  # low, medium, high
    max_delegation_depth: int = 3

    # === КОНТЕКСТНЫЕ ПАРАМЕТРЫ ===
    project_context: Dict[str, Any] = field(default_factory=dict)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    strategy_parameters: Dict[str, Any] = field(default_factory=dict)

    # === КАСТОМИЗАЦИЯ ПО ТИПАМ МЕДИА ===
    media_specific_config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Пост-инициализация с настройкой медиа-специфичных параметров."""
        self._setup_media_specific_config()
        self._setup_platform_optimizations()
        self._validate_configuration()

    def _setup_media_specific_config(self):
        """Настройка конфигурации в зависимости от типа медиа."""
        media_configs = {
            "image": {
                "preferred_formats": ["webp", "jpeg", "png"],
                "optimization_priority": "quality",
                "ai_enhancement": True,
                "batch_friendly": True,
                "seo_important": True
            },
            "video": {
                "preferred_codecs": ["h264", "h265"],
                "optimization_priority": "compression",
                "streaming_ready": True,
                "thumbnail_generation": True,
                "caption_support": True
            },
            "audio": {
                "preferred_formats": ["mp3", "aac"],
                "optimization_priority": "quality",
                "noise_reduction": True,
                "normalize_volume": True,
                "metadata_rich": True
            },
            "animation": {
                "preferred_formats": ["gif", "webp", "mp4"],
                "loop_support": True,
                "size_optimization": True,
                "interactive_elements": False
            },
            "presentation": {
                "slide_formats": ["pdf", "pptx", "html"],
                "interactive_elements": True,
                "export_formats": ["pdf", "images"],
                "template_based": True
            },
            "composite": {
                "layer_support": True,
                "blend_modes": True,
                "mask_support": True,
                "vector_support": True
            }
        }

        if self.media_type in media_configs:
            self.media_specific_config.update(media_configs[self.media_type])

    def _setup_platform_optimizations(self):
        """Настройка оптимизаций под целевые платформы."""
        platform_configs = {
            "instagram": {
                "aspect_ratios": ["1:1", "4:5", "9:16"],
                "max_size": (1080, 1350),
                "formats": ["jpeg", "mp4"],
                "file_size_limit": "30MB"
            },
            "youtube": {
                "aspect_ratios": ["16:9"],
                "resolutions": ["1080p", "1440p", "4k"],
                "thumbnail_size": (1280, 720),
                "max_file_size": "128GB"
            },
            "tiktok": {
                "aspect_ratios": ["9:16"],
                "duration_limits": (15, 60),
                "vertical_first": True,
                "mobile_optimized": True
            },
            "web": {
                "responsive": True,
                "lazy_loading": True,
                "format_fallbacks": True,
                "seo_optimized": True
            },
            "print": {
                "high_dpi": True,
                "cmyk_ready": True,
                "bleed_area": True,
                "color_accurate": True
            }
        }

        if self.target_platform in platform_configs:
            platform_config = platform_configs[self.target_platform]

            # Применяем настройки платформы
            if self.target_platform == "instagram":
                self.instagram_optimization = True
                self.instagram_aspect_ratios = platform_config["aspect_ratios"]
            elif self.target_platform == "youtube":
                self.youtube_optimization = True
                self.youtube_thumbnails = True
            elif self.target_platform == "print":
                self.print_optimization = True
                self.print_dpi = 300
                self.cmyk_conversion = True

    def _validate_configuration(self):
        """Валидация и коррекция конфигурации."""
        # Проверка совместимости настроек
        if self.media_type == "video" and self.quality_level == "lossless":
            # Для видео lossless может быть слишком тяжелым
            self.quality_level = "premium"

        if self.target_platform == "mobile" and self.image_max_width > 1080:
            # Для мобильных устройств ограничиваем размер
            self.image_max_width = 1080
            self.image_max_height = 1920

        if self.ai_generation_quality == "ultra" and self.processing_mode == "optimize":
            # Ultra качество для оптимизации избыточно
            self.ai_generation_quality = "high"

        # Автоматическая настройка форматов
        if self.output_format == "auto":
            format_mapping = {
                "image": "webp" if self.webp_support else "jpeg",
                "video": "mp4",
                "audio": "mp3",
                "animation": "gif"
            }
            self.output_format = format_mapping.get(self.media_type, "auto")

    def get_processing_parameters(self) -> Dict[str, Any]:
        """Получить все параметры обработки в виде словаря."""
        return {
            "media_type": self.media_type,
            "processing_mode": self.processing_mode,
            "target_platform": self.target_platform,
            "quality_level": self.quality_level,
            "output_format": self.output_format,
            "enable_ai_generation": self.enable_ai_generation,
            "enable_effects": self.enable_effects
        }

    def get_quality_settings(self) -> Dict[str, Any]:
        """Получить настройки качества."""
        quality_mapping = {
            "low": {"compression": 60, "resolution_scale": 0.7},
            "medium": {"compression": 75, "resolution_scale": 0.85},
            "high": {"compression": 85, "resolution_scale": 1.0},
            "premium": {"compression": 95, "resolution_scale": 1.0},
            "lossless": {"compression": 100, "resolution_scale": 1.0}
        }

        return quality_mapping.get(self.quality_level, quality_mapping["high"])

    def get_platform_constraints(self) -> Dict[str, Any]:
        """Получить ограничения целевой платформы."""
        constraints = {
            "max_file_size": None,
            "aspect_ratios": [],
            "resolution_limits": {},
            "format_restrictions": [],
            "duration_limits": None
        }

        platform_constraints = {
            "instagram": {
                "max_file_size": "30MB",
                "aspect_ratios": ["1:1", "4:5", "9:16"],
                "resolution_limits": {"max_width": 1080, "max_height": 1350}
            },
            "youtube": {
                "max_file_size": "128GB",
                "aspect_ratios": ["16:9"],
                "resolution_limits": {"max_width": 3840, "max_height": 2160}
            },
            "tiktok": {
                "max_file_size": "2GB",
                "aspect_ratios": ["9:16"],
                "duration_limits": {"min": 15, "max": 60}
            },
            "web": {
                "max_file_size": "10MB",
                "format_restrictions": ["webp", "jpeg", "png"]
            }
        }

        if self.target_platform in platform_constraints:
            constraints.update(platform_constraints[self.target_platform])

        return constraints


def load_dependencies() -> MediaOrchestratorDependencies:
    """
    Загрузить зависимости из переменных окружения.

    Returns:
        Настроенный экземпляр MediaOrchestratorDependencies
    """
    return MediaOrchestratorDependencies(
        api_key=os.getenv("LLM_API_KEY", ""),
        project_path=os.getenv("PROJECT_PATH", ""),

        # Конфигурация медиа
        media_type=os.getenv("MEDIA_TYPE", "image"),
        processing_mode=os.getenv("PROCESSING_MODE", "optimize"),
        target_platform=os.getenv("TARGET_PLATFORM", "web"),
        quality_level=os.getenv("QUALITY_LEVEL", "high"),
        output_format=os.getenv("OUTPUT_FORMAT", "auto"),

        # AI генерация
        enable_ai_generation=os.getenv("ENABLE_AI_GENERATION", "true").lower() == "true",
        ai_generation_model=os.getenv("AI_GENERATION_MODEL", "stable_diffusion"),
        ai_generation_style=os.getenv("AI_GENERATION_STYLE", "realistic"),

        # Эффекты
        enable_effects=os.getenv("ENABLE_EFFECTS", "true").lower() == "true",
        color_correction=os.getenv("COLOR_CORRECTION", "false").lower() == "true",

        # Платформенная оптимизация
        web_optimization=os.getenv("WEB_OPTIMIZATION", "true").lower() == "true",
        mobile_optimization=os.getenv("MOBILE_OPTIMIZATION", "true").lower() == "true",
        webp_support=os.getenv("WEBP_SUPPORT", "true").lower() == "true",

        # Безопасность
        privacy_mode=os.getenv("PRIVACY_MODE", "false").lower() == "true",
        exif_data_removal=os.getenv("EXIF_DATA_REMOVAL", "true").lower() == "true",

        # RAG и Knowledge Base
        agent_name="universal_media_orchestrator",
        knowledge_tags=os.getenv("KNOWLEDGE_TAGS", "media-orchestration,image-processing,video-editing,audio-processing,agent-knowledge,pydantic-ai").split(","),
        archon_project_id=os.getenv("ARCHON_PROJECT_ID", ""),

        # Межагентное взаимодействие
        enable_task_delegation=os.getenv("ENABLE_TASK_DELEGATION", "true").lower() == "true",
        delegation_threshold=os.getenv("DELEGATION_THRESHOLD", "medium")
    )


# === КОНСТАНТЫ КОМПЕТЕНЦИЙ ===

AGENT_COMPETENCIES = {
    "media_types": [
        "image", "video", "audio", "animation", "presentation", "composite",
        "infographic", "social_post", "thumbnail", "banner", "logo"
    ],
    "processing_modes": [
        "optimize", "transform", "generate", "composite", "analyze",
        "enhance", "repair", "convert", "resize", "compress"
    ],
    "platforms": [
        "web", "mobile", "social", "print", "presentation", "broadcast",
        "instagram", "youtube", "tiktok", "facebook", "linkedin", "twitter"
    ],
    "formats": {
        "image": ["jpeg", "png", "webp", "avif", "svg", "gif", "bmp", "tiff"],
        "video": ["mp4", "webm", "mov", "avi", "mkv", "flv"],
        "audio": ["mp3", "wav", "flac", "aac", "ogg", "m4a"]
    },
    "ai_capabilities": [
        "image_generation", "video_generation", "audio_synthesis",
        "style_transfer", "upscaling", "colorization", "restoration"
    ],
    "specializations": [
        "image_optimization", "video_editing", "audio_processing",
        "animation_creation", "brand_consistency", "platform_adaptation"
    ]
}

AGENT_ASSIGNEE_MAP = {
    "image_optimization": "Performance Optimization Agent",
    "video_editing": "Media Specialist Agent",
    "audio_processing": "Audio Engineer Agent",
    "ui_design": "UI/UX Enhancement Agent",
    "content_creation": "Content Generator Agent",
    "quality_assurance": "Quality Guardian Agent",
    "seo_optimization": "SEO Specialist Agent",
    "brand_guidelines": "Brand Consistency Agent"
}

# Экспорт
__all__ = [
    "MediaOrchestratorDependencies",
    "load_dependencies",
    "AGENT_COMPETENCIES",
    "AGENT_ASSIGNEE_MAP"
]