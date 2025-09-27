# -*- coding: utf-8 -*-
"""
Universal Media Orchestrator Agent

Универсальный агент для оркестрации, обработки и оптимизации
медиа-контента всех типов с поддержкой множественных платформ.

Основные возможности:
- Мультиформатная обработка (изображения, видео, аудио, анимации)
- Платформенная адаптация (веб, мобильные, социальные сети, печать)
- AI-powered генерация и улучшение контента
- Автоматическая оркестрация медиа-пайплайнов
- Интеграция с Archon Knowledge Base
"""

from .agent import (
    media_orchestrator_agent,
    run_media_orchestration_task,
    run_image_processing,
    run_video_processing,
    run_audio_processing,
    run_media_generation,
    run_media_composition,
    run_platform_optimization,
    analyze_media_requirements,
    create_media_strategy
)

from .dependencies import (
    MediaOrchestratorDependencies,
    load_dependencies
)

from .settings import (
    MediaOrchestratorSettings,
    load_settings,
    get_processing_profile,
    list_processing_profiles,
    create_custom_profile,
    ProcessingProfile,
    PROCESSING_PROFILES
)

from .providers import (
    MediaModelProvider,
    get_llm_model,
    get_model_for_media_task,
    TaskComplexity,
    MediaType
)

from .prompts import (
    get_system_prompt,
    get_preset_prompt,
    MediaPromptConfig,
    PRESET_CONFIGURATIONS
)

# Версия агента
__version__ = "1.0.0"

# Метаинформация
__author__ = "AI Agent Factory"
__description__ = "Universal Media Orchestrator Agent for comprehensive media processing"
__license__ = "MIT"

# Основные экспорты
__all__ = [
    # Основной агент и функции
    "media_orchestrator_agent",
    "run_media_orchestration_task",
    "run_image_processing",
    "run_video_processing",
    "run_audio_processing",
    "run_media_generation",
    "run_media_composition",
    "run_platform_optimization",
    "analyze_media_requirements",
    "create_media_strategy",

    # Конфигурация и зависимости
    "MediaOrchestratorDependencies",
    "load_dependencies",
    "MediaOrchestratorSettings",
    "load_settings",

    # Профили обработки
    "get_processing_profile",
    "list_processing_profiles",
    "create_custom_profile",
    "ProcessingProfile",
    "PROCESSING_PROFILES",

    # Системы моделей
    "MediaModelProvider",
    "get_llm_model",
    "get_model_for_media_task",
    "TaskComplexity",
    "MediaType",

    # Промпты и конфигурации
    "get_system_prompt",
    "get_preset_prompt",
    "MediaPromptConfig",
    "PRESET_CONFIGURATIONS",

    # Метаинформация
    "__version__",
    "__author__",
    "__description__",
    "__license__"
]

# Информация о поддерживаемых функциях
SUPPORTED_FEATURES = {
    "media_types": [
        "image", "video", "audio", "animation",
        "presentation", "composite"
    ],
    "image_formats": [
        "jpg", "jpeg", "png", "webp", "avif",
        "svg", "heic", "bmp", "tiff"
    ],
    "video_formats": [
        "mp4", "avi", "mov", "mkv", "webm",
        "flv", "wmv", "m4v"
    ],
    "audio_formats": [
        "mp3", "wav", "flac", "aac", "ogg",
        "m4a", "wma"
    ],
    "processing_modes": [
        "optimize", "transform", "generate",
        "composite", "analyze"
    ],
    "target_platforms": [
        "web", "mobile", "social", "print",
        "presentation", "broadcast"
    ],
    "quality_levels": [
        "low", "medium", "high", "premium", "lossless"
    ],
    "ai_capabilities": [
        "generation", "enhancement", "style_transfer",
        "background_removal", "upscaling", "restoration"
    ]
}

# Информация о интеграциях
INTEGRATIONS = {
    "archon_knowledge_base": {
        "enabled": True,
        "features": ["rag_search", "task_delegation", "progress_tracking"]
    },
    "collective_problem_solving": {
        "enabled": True,
        "features": ["microtask_breakdown", "agent_delegation", "reflection"]
    },
    "model_optimization": {
        "enabled": True,
        "features": ["cost_optimization", "quality_optimization", "auto_selection"]
    }
}

def get_agent_info() -> dict:
    """
    Получить информацию об агенте и его возможностях.

    Returns:
        Словарь с подробной информацией об агенте
    """
    return {
        "name": "Universal Media Orchestrator Agent",
        "version": __version__,
        "description": __description__,
        "author": __author__,
        "license": __license__,
        "supported_features": SUPPORTED_FEATURES,
        "integrations": INTEGRATIONS,
        "knowledge_base": "universal_media_orchestrator_knowledge.md",
        "tags": [
            "media-processing", "image-optimization", "video-editing",
            "audio-processing", "ai-generation", "platform-optimization",
            "universal-agent", "pydantic-ai", "archon-integration"
        ]
    }

def get_quick_start_example() -> str:
    """
    Получить пример быстрого старта для агента.

    Returns:
        Строка с примером кода
    """
    return '''
# Быстрый старт Universal Media Orchestrator Agent

from universal_media_orchestrator_agent import run_media_orchestration_task

# Базовая оркестрация медиа
result = await run_media_orchestration_task(
    message="Оптимизируй изображения для веб-сайта электронной коммерции",
    media_type="image",
    processing_mode="optimize",
    target_platform="web",
    quality_level="high"
)

# Специализированная обработка
from universal_media_orchestrator_agent import run_image_processing

image_result = await run_image_processing(
    image_path="product_photo.jpg",
    operations=["resize", "enhance", "watermark"],
    target_size=(800, 800),
    platform_optimization="ecommerce"
)

print("Медиа-обработка завершена!")
'''

# Автоматическая проверка зависимостей при импорте
try:
    from .settings import load_settings

    # Пробуем загрузить настройки для валидации
    _settings = load_settings()

    # Проверяем наличие критических API ключей
    if not _settings.llm_api_key:
        import warnings
        warnings.warn(
            "LLM API ключ не найден. Убедитесь, что MEDIA_ORCHESTRATOR_LLM_API_KEY "
            "или LLM_API_KEY указан в переменных окружения.",
            UserWarning
        )

    if not _settings.gemini_api_key:
        import warnings
        warnings.warn(
            "Gemini API ключ не найден. Некоторые функции могут быть недоступны. "
            "Установите MEDIA_ORCHESTRATOR_GEMINI_API_KEY для полной функциональности.",
            UserWarning
        )

except Exception as e:
    import warnings
    warnings.warn(
        f"Проблема при инициализации агента: {e}. "
        "Проверьте конфигурацию в файле .env",
        UserWarning
    )

# Сообщение об успешной инициализации (только в debug режиме)
import os
if os.getenv("DEBUG", "").lower() in ("true", "1", "yes"):
    print(f"✅ Universal Media Orchestrator Agent v{__version__} загружен успешно")
    print(f"📁 Поддерживаемые типы медиа: {', '.join(SUPPORTED_FEATURES['media_types'])}")
    print(f"🔧 Режимы обработки: {', '.join(SUPPORTED_FEATURES['processing_modes'])}")
    print(f"🌐 Целевые платформы: {', '.join(SUPPORTED_FEATURES['target_platforms'])}")