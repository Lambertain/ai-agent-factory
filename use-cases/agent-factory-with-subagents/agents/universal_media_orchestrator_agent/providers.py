# -*- coding: utf-8 -*-
"""
Провайдеры моделей для Universal Media Orchestrator Agent.

Система автоматического выбора оптимальных моделей для различных
типов медиа-обработки с учетом стоимости и производительности.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

from pydantic_ai.models import Model
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class TaskComplexity(Enum):
    """Уровни сложности задач медиа-оркестрации."""
    SIMPLE = "simple"      # Базовая оптимизация, простые конверсии
    MEDIUM = "medium"      # Сложная обработка, множественные операции
    COMPLEX = "complex"    # AI-генерация, архитектурный анализ
    PREMIUM = "premium"    # Профессиональная обработка, критическое качество


class MediaType(Enum):
    """Типы медиа для оптимизации выбора модели."""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    ANIMATION = "animation"
    PRESENTATION = "presentation"
    COMPOSITE = "composite"


@dataclass
class ModelConfig:
    """Конфигурация модели для специфических задач."""
    model_name: str
    provider: str
    base_url: str
    api_key_var: str
    cost_per_1m_tokens: float
    max_tokens: int
    specializations: List[str]
    performance_score: int  # 1-10


class MediaModelProvider:
    """
    Провайдер моделей для медиа-оркестрации с автоматическим выбором
    оптимальной модели на основе типа задачи и требований к качеству.
    """

    def __init__(self, settings: Any):
        """
        Инициализация провайдера моделей.

        Args:
            settings: Настройки приложения с API ключами и конфигурацией
        """
        self.settings = settings
        self.model_configs = self._init_model_configs()
        self.current_model: Optional[Model] = None
        self.fallback_model: Optional[Model] = None

    def _init_model_configs(self) -> Dict[str, ModelConfig]:
        """Инициализация конфигураций доступных моделей."""

        configs = {
            # === СПЕЦИАЛИЗИРОВАННЫЕ МОДЕЛИ ДЛЯ МЕДИА ===

            # Визуальные задачи - Claude Opus для понимания изображений
            "claude_opus_vision": ModelConfig(
                model_name="claude-3-5-sonnet-20241022",
                provider="anthropic",
                base_url="https://api.anthropic.com",
                api_key_var="ANTHROPIC_API_KEY",
                cost_per_1m_tokens=15.0,  # Premium за качество визуального анализа
                max_tokens=8192,
                specializations=["image_analysis", "visual_content", "design_critique"],
                performance_score=10
            ),

            # AI генерация и креативные задачи - Qwen Coder для структурированности
            "qwen_creative": ModelConfig(
                model_name="qwen2.5-coder-32b-instruct",
                provider="openai_compatible",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key_var="LLM_API_KEY",
                cost_per_1m_tokens=3.0,
                max_tokens=32768,
                specializations=["ai_generation", "media_scripting", "automation"],
                performance_score=9
            ),

            # Техническая обработка - Qwen Coder оптимизированный
            "qwen_technical": ModelConfig(
                model_name="qwen2.5-coder-14b-instruct",
                provider="openai_compatible",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key_var="LLM_API_KEY",
                cost_per_1m_tokens=1.5,
                max_tokens=32768,
                specializations=["technical_processing", "optimization", "batch_operations"],
                performance_score=8
            ),

            # Быстрая обработка - Gemini Flash для скорости
            "gemini_fast": ModelConfig(
                model_name="gemini-2.0-flash-exp",
                provider="google",
                base_url="https://generativelanguage.googleapis.com",
                api_key_var="GEMINI_API_KEY",
                cost_per_1m_tokens=0.4,  # Очень дешево для быстрых задач
                max_tokens=8192,
                specializations=["quick_processing", "batch_optimization", "validation"],
                performance_score=7
            ),

            # Анализ и планирование - Gemini Pro
            "gemini_analysis": ModelConfig(
                model_name="gemini-2.0-flash-thinking-exp",
                provider="google",
                base_url="https://generativelanguage.googleapis.com",
                api_key_var="GEMINI_API_KEY",
                cost_per_1m_tokens=1.0,
                max_tokens=32768,
                specializations=["media_analysis", "pipeline_planning", "quality_assessment"],
                performance_score=8
            ),

            # Fallback модель - Стабильная и доступная
            "fallback": ModelConfig(
                model_name="qwen2.5-coder-7b-instruct",
                provider="openai_compatible",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key_var="LLM_API_KEY",
                cost_per_1m_tokens=0.5,
                max_tokens=32768,
                specializations=["general_purpose", "fallback"],
                performance_score=6
            )
        }

        return configs

    def get_optimal_model(
        self,
        media_type: MediaType,
        task_complexity: TaskComplexity,
        processing_mode: str = "optimize",
        quality_priority: bool = False,
        cost_priority: bool = False
    ) -> Model:
        """
        Автоматический выбор оптимальной модели для конкретной задачи.

        Args:
            media_type: Тип медиа для обработки
            task_complexity: Сложность задачи
            processing_mode: Режим обработки (optimize, generate, analyze, etc.)
            quality_priority: Приоритет качества над стоимостью
            cost_priority: Приоритет стоимости над качеством

        Returns:
            Оптимальная модель для задачи
        """

        # Определяем оптимальную модель по задаче
        model_key = self._select_model_key(
            media_type, task_complexity, processing_mode,
            quality_priority, cost_priority
        )

        # Создаем и возвращаем модель
        return self._create_model(model_key)

    def _select_model_key(
        self,
        media_type: MediaType,
        task_complexity: TaskComplexity,
        processing_mode: str,
        quality_priority: bool,
        cost_priority: bool
    ) -> str:
        """Логика выбора ключа модели на основе параметров."""

        # Приоритет стоимости - используем быстрые модели
        if cost_priority:
            if task_complexity in [TaskComplexity.SIMPLE, TaskComplexity.MEDIUM]:
                return "gemini_fast"
            else:
                return "qwen_technical"

        # Приоритет качества или сложные задачи
        if quality_priority or task_complexity == TaskComplexity.PREMIUM:
            # Для визуальных задач - Claude с vision
            if media_type in [MediaType.IMAGE, MediaType.ANIMATION] and processing_mode in ["analyze", "generate"]:
                return "claude_opus_vision"
            # Для остальных сложных задач - Qwen Creative
            else:
                return "qwen_creative"

        # Стандартная логика выбора по типу задачи
        if processing_mode == "generate" and task_complexity == TaskComplexity.COMPLEX:
            # AI генерация - креативная модель
            return "qwen_creative"

        elif processing_mode == "analyze":
            # Анализ медиа - аналитическая модель
            if media_type in [MediaType.IMAGE, MediaType.VIDEO]:
                return "claude_opus_vision"  # Лучше понимает визуальный контент
            else:
                return "gemini_analysis"

        elif task_complexity == TaskComplexity.SIMPLE:
            # Простые задачи - быстрая модель
            return "gemini_fast"

        else:
            # Техническая обработка средней сложности
            return "qwen_technical"

    def _create_model(self, model_key: str) -> Model:
        """
        Создание экземпляра модели по ключу конфигурации.

        Args:
            model_key: Ключ конфигурации модели

        Returns:
            Экземпляр модели
        """
        config = self.model_configs.get(model_key)
        if not config:
            # Fallback на стандартную модель
            config = self.model_configs["fallback"]

        try:
            # Получаем API ключ из настроек
            api_key = getattr(self.settings, config.api_key_var.lower(), None)
            if not api_key:
                raise ValueError(f"API ключ {config.api_key_var} не найден в настройках")

            # Создаем провайдера
            if config.provider in ["openai_compatible"]:
                provider = OpenAIProvider(
                    base_url=config.base_url,
                    api_key=api_key
                )
                model = OpenAIModel(config.model_name, provider=provider)

            else:
                # Для других провайдеров используем fallback
                fallback_config = self.model_configs["fallback"]
                fallback_api_key = getattr(self.settings, fallback_config.api_key_var.lower())

                provider = OpenAIProvider(
                    base_url=fallback_config.base_url,
                    api_key=fallback_api_key
                )
                model = OpenAIModel(fallback_config.model_name, provider=provider)

            return model

        except Exception as e:
            # В случае ошибки используем fallback модель
            return self._create_fallback_model()

    def _create_fallback_model(self) -> Model:
        """Создание fallback модели для критических ситуаций."""

        try:
            config = self.model_configs["fallback"]
            api_key = getattr(self.settings, config.api_key_var.lower())

            provider = OpenAIProvider(
                base_url=config.base_url,
                api_key=api_key
            )

            return OpenAIModel(config.model_name, provider=provider)

        except Exception as e:
            raise RuntimeError(f"Не удалось создать даже fallback модель: {e}")

    def get_model_for_task_type(self, task_type: str) -> Model:
        """
        Упрощенный метод получения модели по типу задачи.

        Args:
            task_type: Тип задачи (image_processing, video_editing, ai_generation, etc.)

        Returns:
            Подходящая модель для типа задачи
        """

        task_mapping = {
            # Обработка изображений
            "image_processing": ("qwen_technical", MediaType.IMAGE, TaskComplexity.MEDIUM),
            "image_optimization": ("gemini_fast", MediaType.IMAGE, TaskComplexity.SIMPLE),
            "image_analysis": ("claude_opus_vision", MediaType.IMAGE, TaskComplexity.COMPLEX),

            # Работа с видео
            "video_processing": ("qwen_technical", MediaType.VIDEO, TaskComplexity.MEDIUM),
            "video_optimization": ("qwen_technical", MediaType.VIDEO, TaskComplexity.MEDIUM),
            "video_analysis": ("gemini_analysis", MediaType.VIDEO, TaskComplexity.COMPLEX),

            # AI генерация
            "ai_generation": ("qwen_creative", MediaType.COMPOSITE, TaskComplexity.COMPLEX),
            "content_generation": ("qwen_creative", MediaType.COMPOSITE, TaskComplexity.COMPLEX),

            # Анализ и планирование
            "media_analysis": ("gemini_analysis", MediaType.COMPOSITE, TaskComplexity.MEDIUM),
            "pipeline_planning": ("gemini_analysis", MediaType.COMPOSITE, TaskComplexity.MEDIUM),

            # Быстрые операции
            "batch_processing": ("gemini_fast", MediaType.COMPOSITE, TaskComplexity.SIMPLE),
            "validation": ("gemini_fast", MediaType.COMPOSITE, TaskComplexity.SIMPLE),
        }

        if task_type in task_mapping:
            model_key, media_type, complexity = task_mapping[task_type]
            return self._create_model(model_key)
        else:
            # Для неизвестных задач используем техническую модель
            return self._create_model("qwen_technical")

    def get_cost_optimized_model(self) -> Model:
        """Получить наиболее экономичную модель."""
        return self._create_model("gemini_fast")

    def get_quality_optimized_model(self, media_type: MediaType = MediaType.COMPOSITE) -> Model:
        """Получить модель с наивысшим качеством."""
        if media_type in [MediaType.IMAGE, MediaType.ANIMATION]:
            return self._create_model("claude_opus_vision")
        else:
            return self._create_model("qwen_creative")

    def get_balanced_model(self) -> Model:
        """Получить сбалансированную модель (качество/стоимость)."""
        return self._create_model("qwen_technical")

    def estimate_cost(self, model_key: str, estimated_tokens: int) -> float:
        """
        Оценка стоимости выполнения задачи.

        Args:
            model_key: Ключ модели
            estimated_tokens: Примерное количество токенов

        Returns:
            Оценочная стоимость в USD
        """
        config = self.model_configs.get(model_key, self.model_configs["fallback"])
        cost_per_token = config.cost_per_1m_tokens / 1_000_000
        return cost_per_token * estimated_tokens

    def get_model_info(self, model_key: str) -> Dict[str, Any]:
        """
        Получить информацию о модели.

        Args:
            model_key: Ключ модели

        Returns:
            Словарь с информацией о модели
        """
        config = self.model_configs.get(model_key)
        if not config:
            return {"error": f"Модель {model_key} не найдена"}

        return {
            "model_name": config.model_name,
            "provider": config.provider,
            "cost_per_1m_tokens": config.cost_per_1m_tokens,
            "max_tokens": config.max_tokens,
            "specializations": config.specializations,
            "performance_score": config.performance_score
        }

    def list_available_models(self) -> List[Dict[str, Any]]:
        """Получить список всех доступных моделей с их характеристиками."""

        models_info = []
        for key, config in self.model_configs.items():
            models_info.append({
                "key": key,
                "model_name": config.model_name,
                "provider": config.provider,
                "cost_per_1m_tokens": config.cost_per_1m_tokens,
                "specializations": config.specializations,
                "performance_score": config.performance_score
            })

        # Сортируем по performance_score (по убыванию)
        models_info.sort(key=lambda x: x["performance_score"], reverse=True)

        return models_info


def get_llm_model(settings: Any = None, model_type: str = "balanced") -> Model:
    """
    Фабричная функция для создания модели по типу.

    Args:
        settings: Настройки приложения
        model_type: Тип модели (cost_optimized, quality_optimized, balanced)

    Returns:
        Экземпляр модели
    """
    if settings is None:
        from .settings import load_settings
        settings = load_settings()

    provider = MediaModelProvider(settings)

    if model_type == "cost_optimized":
        return provider.get_cost_optimized_model()
    elif model_type == "quality_optimized":
        return provider.get_quality_optimized_model()
    else:  # balanced или любой другой
        return provider.get_balanced_model()


def get_model_for_media_task(
    media_type: str,
    complexity: str = "medium",
    processing_mode: str = "optimize",
    settings: Any = None
) -> Model:
    """
    Упрощенная функция получения модели для медиа-задач.

    Args:
        media_type: Тип медиа (image, video, audio, etc.)
        complexity: Сложность (simple, medium, complex, premium)
        processing_mode: Режим обработки
        settings: Настройки приложения

    Returns:
        Оптимальная модель для задачи
    """
    if settings is None:
        from .settings import load_settings
        settings = load_settings()

    provider = MediaModelProvider(settings)

    # Конвертируем строки в enum-ы
    media_enum = MediaType(media_type) if media_type in [e.value for e in MediaType] else MediaType.COMPOSITE
    complexity_enum = TaskComplexity(complexity) if complexity in [e.value for e in TaskComplexity] else TaskComplexity.MEDIUM

    return provider.get_optimal_model(
        media_type=media_enum,
        task_complexity=complexity_enum,
        processing_mode=processing_mode
    )