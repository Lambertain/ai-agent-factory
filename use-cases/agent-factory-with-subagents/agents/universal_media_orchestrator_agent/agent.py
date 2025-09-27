# -*- coding: utf-8 -*-
"""
Universal Media Orchestrator Agent

Универсальный агент для управления, обработки и оптимизации медиа-контента:
изображения, видео, аудио, анимации, презентации и другие медиа-форматы.

Поддерживает оркестрацию медиа-процессов, оптимизацию для различных платформ,
автоматическую генерацию и адаптацию медиа-контента.
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import json

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model

from .dependencies import MediaOrchestratorDependencies, load_dependencies
from .settings import load_settings
from .providers import get_llm_model
from .tools import (
    orchestrate_media_pipeline,
    process_image_media,
    process_video_media,
    process_audio_media,
    generate_media_variations,
    optimize_media_for_platform,
    create_media_composition,
    extract_media_metadata,
    validate_media_quality,
    apply_media_effects
)
from .prompts import get_system_prompt


# Загрузка настроек и конфигурации
settings = load_settings()
dependencies = load_dependencies()

# Создание агента с оптимизированной моделью
media_orchestrator_agent = Agent(
    model=get_llm_model(),
    deps_type=MediaOrchestratorDependencies,
    system_prompt=get_system_prompt(dependencies.__dict__)
)

# Регистрация инструментов оркестрации медиа
media_orchestrator_agent.tool(orchestrate_media_pipeline)
media_orchestrator_agent.tool(process_image_media)
media_orchestrator_agent.tool(process_video_media)
media_orchestrator_agent.tool(process_audio_media)
media_orchestrator_agent.tool(generate_media_variations)
media_orchestrator_agent.tool(optimize_media_for_platform)
media_orchestrator_agent.tool(create_media_composition)
media_orchestrator_agent.tool(extract_media_metadata)
media_orchestrator_agent.tool(validate_media_quality)
media_orchestrator_agent.tool(apply_media_effects)


# === ОСНОВНЫЕ ТОЧКИ ВХОДА ===

async def run_media_orchestration_task(
    message: str,
    media_type: str = "image",
    processing_mode: str = "optimize",
    target_platform: str = "web",
    quality_level: str = "high",
    output_format: str = "auto",
    enable_ai_generation: bool = True,
    enable_effects: bool = True
) -> str:
    """
    Основная функция оркестрации медиа-контента.

    Args:
        message: Запрос на обработку медиа
        media_type: Тип медиа (image, video, audio, animation, presentation)
        processing_mode: Режим обработки (optimize, transform, generate, composite)
        target_platform: Целевая платформа (web, mobile, social, print, presentation)
        quality_level: Уровень качества (low, medium, high, premium)
        output_format: Формат вывода (auto или конкретный формат)
        enable_ai_generation: Включить AI генерацию
        enable_effects: Включить эффекты

    Returns:
        Результат обработки медиа
    """
    deps = MediaOrchestratorDependencies(
        api_key=settings.llm_api_key,
        project_path=settings.project_path,
        media_type=media_type,
        processing_mode=processing_mode,
        target_platform=target_platform,
        quality_level=quality_level,
        output_format=output_format,
        enable_ai_generation=enable_ai_generation,
        enable_effects=enable_effects,
        agent_name="universal_media_orchestrator",
        archon_project_id=settings.archon_project_id
    )

    try:
        result = await media_orchestrator_agent.run(message, deps=deps)
        return str(result.data)
    except Exception as e:
        return f"Ошибка оркестрации медиа: {str(e)}"


async def run_image_processing(
    image_path: str,
    operations: List[str] = None,
    target_size: Tuple[int, int] = None,
    target_format: str = "auto",
    quality: int = 85,
    platform_optimization: str = None
) -> Dict[str, Any]:
    """
    Специализированная функция для обработки изображений.

    Args:
        image_path: Путь к изображению
        operations: Список операций (resize, crop, filter, enhance, etc.)
        target_size: Целевой размер (ширина, высота)
        target_format: Формат вывода (jpeg, png, webp, avif)
        quality: Качество сжатия (1-100)
        platform_optimization: Оптимизация под платформу

    Returns:
        Результат обработки изображения
    """
    message = f"""
Обработай изображение: {image_path}

Операции: {', '.join(operations) if operations else 'оптимизация'}
{'Целевой размер: ' + str(target_size) if target_size else ''}
Формат вывода: {target_format}
Качество: {quality}
{'Платформа: ' + platform_optimization if platform_optimization else ''}
"""

    deps = MediaOrchestratorDependencies(
        api_key=settings.llm_api_key,
        media_type="image",
        processing_mode="transform",
        quality_level="high" if quality > 80 else "medium",
        output_format=target_format
    )

    try:
        result = await media_orchestrator_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка обработки изображения: {str(e)}"}


async def run_video_processing(
    video_path: str,
    editing_operations: Dict[str, Any] = None,
    target_resolution: str = "1080p",
    target_fps: int = 30,
    target_codec: str = "h264",
    platform_optimization: str = None
) -> Dict[str, Any]:
    """
    Специализированная функция для обработки видео.

    Args:
        video_path: Путь к видео
        editing_operations: Операции редактирования (trim, merge, effects, etc.)
        target_resolution: Целевое разрешение
        target_fps: Целевой FPS
        target_codec: Целевой кодек
        platform_optimization: Оптимизация под платформу

    Returns:
        Результат обработки видео
    """
    message = f"""
Обработай видео: {video_path}

{'Операции редактирования: ' + str(editing_operations) if editing_operations else ''}
Целевое разрешение: {target_resolution}
FPS: {target_fps}
Кодек: {target_codec}
{'Платформа: ' + platform_optimization if platform_optimization else ''}
"""

    deps = MediaOrchestratorDependencies(
        api_key=settings.llm_api_key,
        media_type="video",
        processing_mode="transform",
        video_resolution=target_resolution,
        video_fps=target_fps,
        video_codec=target_codec
    )

    try:
        result = await media_orchestrator_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка обработки видео: {str(e)}"}


async def run_audio_processing(
    audio_path: str,
    audio_operations: List[str] = None,
    target_format: str = "mp3",
    target_bitrate: int = 192,
    apply_effects: List[str] = None
) -> Dict[str, Any]:
    """
    Специализированная функция для обработки аудио.

    Args:
        audio_path: Путь к аудио файлу
        audio_operations: Операции (normalize, compress, denoise, etc.)
        target_format: Формат вывода
        target_bitrate: Битрейт (kbps)
        apply_effects: Список эффектов

    Returns:
        Результат обработки аудио
    """
    message = f"""
Обработай аудио: {audio_path}

{'Операции: ' + ', '.join(audio_operations) if audio_operations else ''}
Формат: {target_format}
Битрейт: {target_bitrate} kbps
{'Эффекты: ' + ', '.join(apply_effects) if apply_effects else ''}
"""

    deps = MediaOrchestratorDependencies(
        api_key=settings.llm_api_key,
        media_type="audio",
        processing_mode="transform",
        audio_format=target_format,
        audio_bitrate=target_bitrate
    )

    try:
        result = await media_orchestrator_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка обработки аудио: {str(e)}"}


async def run_media_generation(
    generation_type: str,
    prompt: str,
    style: str = "realistic",
    dimensions: Dict[str, int] = None,
    duration: int = None,
    quality_preset: str = "high"
) -> Dict[str, Any]:
    """
    Функция для генерации медиа-контента с помощью AI.

    Args:
        generation_type: Тип генерации (image, video, audio, animation)
        prompt: Промпт для генерации
        style: Стиль генерации
        dimensions: Размеры (для изображений/видео)
        duration: Длительность (для видео/аудио)
        quality_preset: Пресет качества

    Returns:
        Сгенерированный медиа-контент
    """
    message = f"""
Сгенерируй {generation_type}:

Промпт: {prompt}
Стиль: {style}
{'Размеры: ' + str(dimensions) if dimensions else ''}
{'Длительность: ' + str(duration) + ' сек' if duration else ''}
Качество: {quality_preset}
"""

    deps = MediaOrchestratorDependencies(
        api_key=settings.llm_api_key,
        media_type=generation_type,
        processing_mode="generate",
        enable_ai_generation=True,
        ai_generation_style=style,
        quality_level=quality_preset
    )

    try:
        result = await media_orchestrator_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка генерации медиа: {str(e)}"}


async def run_media_composition(
    media_assets: List[Dict[str, Any]],
    composition_type: str = "collage",
    layout_style: str = "grid",
    output_dimensions: Tuple[int, int] = (1920, 1080),
    transitions: List[str] = None
) -> Dict[str, Any]:
    """
    Создание композиции из множества медиа-элементов.

    Args:
        media_assets: Список медиа-ресурсов
        composition_type: Тип композиции (collage, slideshow, montage, etc.)
        layout_style: Стиль компоновки
        output_dimensions: Размеры вывода
        transitions: Переходы между элементами

    Returns:
        Готовая композиция
    """
    message = f"""
Создай композицию из медиа-элементов:

Количество элементов: {len(media_assets)}
Тип композиции: {composition_type}
Стиль компоновки: {layout_style}
Размеры: {output_dimensions}
{'Переходы: ' + ', '.join(transitions) if transitions else ''}
"""

    deps = MediaOrchestratorDependencies(
        api_key=settings.llm_api_key,
        media_type="composite",
        processing_mode="composite",
        composition_type=composition_type,
        layout_style=layout_style
    )

    try:
        result = await media_orchestrator_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка создания композиции: {str(e)}"}


async def run_platform_optimization(
    media_path: str,
    target_platforms: List[str],
    optimization_goals: List[str] = None,
    maintain_quality: bool = True
) -> Dict[str, Dict[str, Any]]:
    """
    Оптимизация медиа для различных платформ.

    Args:
        media_path: Путь к медиа файлу
        target_platforms: Целевые платформы (instagram, youtube, tiktok, web, etc.)
        optimization_goals: Цели оптимизации (size, quality, compatibility)
        maintain_quality: Сохранять качество

    Returns:
        Оптимизированные версии для каждой платформы
    """
    message = f"""
Оптимизируй медиа для платформ: {media_path}

Платформы: {', '.join(target_platforms)}
{'Цели: ' + ', '.join(optimization_goals) if optimization_goals else 'баланс'}
Сохранение качества: {'да' if maintain_quality else 'нет'}
"""

    results = {}

    for platform in target_platforms:
        deps = MediaOrchestratorDependencies(
            api_key=settings.llm_api_key,
            target_platform=platform,
            processing_mode="optimize",
            maintain_quality=maintain_quality
        )

        try:
            result = await media_orchestrator_agent.run(message, deps=deps)
            results[platform] = json.loads(str(result.data))
        except Exception as e:
            results[platform] = {"error": str(e)}

    return results


# === УТИЛИТЫ ===

async def analyze_media_requirements(
    project_type: str,
    target_audience: str,
    platforms: List[str]
) -> Dict[str, Any]:
    """
    Анализ требований к медиа для проекта.

    Args:
        project_type: Тип проекта
        target_audience: Целевая аудитория
        platforms: Целевые платформы

    Returns:
        Рекомендации по медиа-контенту
    """
    deps = MediaOrchestratorDependencies(
        api_key=settings.llm_api_key,
        project_context={
            "type": project_type,
            "audience": target_audience,
            "platforms": platforms
        }
    )

    analysis_prompt = f"""
Проанализируй требования к медиа для проекта:

Тип проекта: {project_type}
Аудитория: {target_audience}
Платформы: {', '.join(platforms)}

Определи:
1. Рекомендуемые типы медиа
2. Оптимальные форматы и размеры
3. Стилистические рекомендации
4. Технические требования
"""

    try:
        result = await media_orchestrator_agent.run(analysis_prompt, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка анализа требований: {str(e)}"}


async def create_media_strategy(
    content_goals: List[str],
    budget_level: str = "medium",
    timeline: str = "standard"
) -> Dict[str, Any]:
    """
    Создание стратегии медиа-контента.

    Args:
        content_goals: Цели контента
        budget_level: Уровень бюджета
        timeline: Временные рамки

    Returns:
        Стратегия медиа-контента
    """
    deps = MediaOrchestratorDependencies(
        api_key=settings.llm_api_key,
        strategy_parameters={
            "goals": content_goals,
            "budget": budget_level,
            "timeline": timeline
        }
    )

    strategy_prompt = f"""
Создай стратегию медиа-контента:

Цели: {', '.join(content_goals)}
Бюджет: {budget_level}
Сроки: {timeline}

Включи:
1. Приоритеты медиа-форматов
2. Каналы распространения
3. График производства
4. Метрики успеха
"""

    try:
        result = await media_orchestrator_agent.run(strategy_prompt, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка создания стратегии: {str(e)}"}


# === ЭКСПОРТ ===

__all__ = [
    "media_orchestrator_agent",
    "run_media_orchestration_task",
    "run_image_processing",
    "run_video_processing",
    "run_audio_processing",
    "run_media_generation",
    "run_media_composition",
    "run_platform_optimization",
    "analyze_media_requirements",
    "create_media_strategy"
]