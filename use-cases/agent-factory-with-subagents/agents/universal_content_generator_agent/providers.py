# -*- coding: utf-8 -*-
"""
Universal Content Generator Agent - Провайдеры LLM моделей

Оптимизированная система выбора и управления LLM моделями
для различных задач генерации контента.
"""

import os
from enum import Enum
from typing import Any, Dict, Optional
from dataclasses import dataclass

from pydantic_ai.models import Model
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class ContentComplexity(Enum):
    """Уровни сложности задач генерации контента."""
    SIMPLE = "simple"          # Простые посты, краткие описания
    MEDIUM = "medium"          # Блог-посты, статьи
    COMPLEX = "complex"        # Техническая документация, исследования
    CREATIVE = "creative"      # Креативный контент, storytelling


class ModelProvider(Enum):
    """Поддерживаемые провайдеры моделей."""
    QWEN = "qwen"
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"


@dataclass
class ModelConfig:
    """Конфигурация модели для конкретной задачи."""
    provider: ModelProvider
    model_name: str
    max_tokens: int
    temperature: float
    description: str
    cost_per_1k_tokens: float


class ContentGeneratorLLMProvider:
    """
    Провайдер LLM моделей для генерации контента.

    Автоматически выбирает оптимальную модель в зависимости от:
    - Типа контента
    - Сложности задачи
    - Требований к качеству
    - Ограничений по бюджету
    """

    def __init__(self):
        self.models = self._initialize_models()
        self.api_keys = self._load_api_keys()

    def _initialize_models(self) -> Dict[str, Dict[str, ModelConfig]]:
        """Инициализация доступных моделей по типам задач."""
        return {
            "blog_post": {
                "simple": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-coder-7b-instruct",
                    max_tokens=2048,
                    temperature=0.7,
                    description="Быстрая генерация простых блог-постов",
                    cost_per_1k_tokens=0.15
                ),
                "medium": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-32b-instruct",
                    max_tokens=4096,
                    temperature=0.6,
                    description="Качественные блог-посты среднего размера",
                    cost_per_1k_tokens=0.30
                ),
                "complex": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-72b-instruct",
                    max_tokens=8192,
                    temperature=0.5,
                    description="Глубокие аналитические статьи",
                    cost_per_1k_tokens=0.60
                ),
                "creative": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-32b-instruct",
                    max_tokens=4096,
                    temperature=0.8,
                    description="Креативные блог-посты с storytelling",
                    cost_per_1k_tokens=0.30
                )
            },

            "documentation": {
                "simple": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-coder-7b-instruct",
                    max_tokens=4096,
                    temperature=0.3,
                    description="Базовая техническая документация",
                    cost_per_1k_tokens=0.15
                ),
                "medium": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-coder-32b-instruct",
                    max_tokens=8192,
                    temperature=0.2,
                    description="Подробная API документация",
                    cost_per_1k_tokens=0.35
                ),
                "complex": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-72b-instruct",
                    max_tokens=16384,
                    temperature=0.1,
                    description="Комплексная техническая документация",
                    cost_per_1k_tokens=0.60
                )
            },

            "marketing": {
                "simple": ModelConfig(
                    provider=ModelProvider.GEMINI,
                    model_name="gemini-2.5-flash-lite",
                    max_tokens=1024,
                    temperature=0.8,
                    description="Быстрые маркетинговые тексты",
                    cost_per_1k_tokens=0.10
                ),
                "medium": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-32b-instruct",
                    max_tokens=2048,
                    temperature=0.7,
                    description="Убедительный маркетинговый контент",
                    cost_per_1k_tokens=0.30
                ),
                "creative": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-32b-instruct",
                    max_tokens=2048,
                    temperature=0.9,
                    description="Креативные рекламные кампании",
                    cost_per_1k_tokens=0.30
                )
            },

            "educational": {
                "simple": ModelConfig(
                    provider=ModelProvider.GEMINI,
                    model_name="gemini-2.5-flash-lite",
                    max_tokens=2048,
                    temperature=0.4,
                    description="Простые обучающие материалы",
                    cost_per_1k_tokens=0.10
                ),
                "medium": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-32b-instruct",
                    max_tokens=4096,
                    temperature=0.3,
                    description="Структурированные курсы и уроки",
                    cost_per_1k_tokens=0.30
                ),
                "complex": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-72b-instruct",
                    max_tokens=8192,
                    temperature=0.2,
                    description="Академический контент высокого уровня",
                    cost_per_1k_tokens=0.60
                )
            },

            "social_media": {
                "simple": ModelConfig(
                    provider=ModelProvider.GEMINI,
                    model_name="gemini-2.5-flash-lite",
                    max_tokens=512,
                    temperature=0.9,
                    description="Быстрые посты для соцсетей",
                    cost_per_1k_tokens=0.10
                ),
                "creative": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-32b-instruct",
                    max_tokens=1024,
                    temperature=0.8,
                    description="Вирусный контент для соцсетей",
                    cost_per_1k_tokens=0.30
                )
            },

            "email": {
                "simple": ModelConfig(
                    provider=ModelProvider.GEMINI,
                    model_name="gemini-2.5-flash-lite",
                    max_tokens=1024,
                    temperature=0.6,
                    description="Простые email newsletters",
                    cost_per_1k_tokens=0.10
                ),
                "medium": ModelConfig(
                    provider=ModelProvider.QWEN,
                    model_name="qwen2.5-32b-instruct",
                    max_tokens=2048,
                    temperature=0.5,
                    description="Персонализированные email кампании",
                    cost_per_1k_tokens=0.30
                )
            }
        }

    def _load_api_keys(self) -> Dict[str, str]:
        """Загрузка API ключей из переменных окружения."""
        return {
            "qwen": os.getenv("LLM_API_KEY", ""),
            "gemini": os.getenv("GEMINI_API_KEY", ""),
            "openai": os.getenv("OPENAI_API_KEY", ""),
            "claude": os.getenv("CLAUDE_API_KEY", "")
        }

    def get_model_for_task(
        self,
        content_type: str = "blog_post",
        complexity: str = "medium",
        quality_preference: str = "balanced",  # cost_optimized, balanced, quality_first
        custom_requirements: Dict[str, Any] = None
    ) -> Model:
        """
        Получить оптимальную модель для конкретной задачи.

        Args:
            content_type: Тип контента
            complexity: Уровень сложности
            quality_preference: Предпочтения по качеству vs стоимости
            custom_requirements: Дополнительные требования

        Returns:
            Настроенная модель для задачи
        """
        try:
            # Получение конфигурации модели
            model_config = self._get_model_config(
                content_type, complexity, quality_preference, custom_requirements
            )

            # Создание провайдера
            provider = self._create_provider(model_config)

            # Создание модели
            return self._create_model(provider, model_config)

        except Exception as e:
            # Fallback на базовую модель
            return self._get_fallback_model()

    def _get_model_config(
        self,
        content_type: str,
        complexity: str,
        quality_preference: str,
        custom_requirements: Dict[str, Any] = None
    ) -> ModelConfig:
        """Получить конфигурацию модели с учетом всех параметров."""
        custom_requirements = custom_requirements or {}

        # Базовая конфигурация по типу контента и сложности
        if content_type in self.models and complexity in self.models[content_type]:
            base_config = self.models[content_type][complexity]
        else:
            # Fallback конфигурация
            base_config = ModelConfig(
                provider=ModelProvider.QWEN,
                model_name="qwen2.5-32b-instruct",
                max_tokens=4096,
                temperature=0.6,
                description="Универсальная модель генерации контента",
                cost_per_1k_tokens=0.30
            )

        # Адаптация под предпочтения качества
        if quality_preference == "cost_optimized":
            # Выбираем более дешевую модель
            if base_config.provider == ModelProvider.QWEN and "72b" in base_config.model_name:
                base_config.model_name = "qwen2.5-32b-instruct"
                base_config.cost_per_1k_tokens = 0.30
            elif base_config.provider == ModelProvider.QWEN and "32b" in base_config.model_name:
                base_config.model_name = "qwen2.5-coder-7b-instruct"
                base_config.cost_per_1k_tokens = 0.15

        elif quality_preference == "quality_first":
            # Выбираем модель высшего качества
            if base_config.provider == ModelProvider.QWEN:
                base_config.model_name = "qwen2.5-72b-instruct"
                base_config.max_tokens = max(base_config.max_tokens, 8192)
                base_config.cost_per_1k_tokens = 0.60

        # Применение кастомных требований
        if "max_tokens" in custom_requirements:
            base_config.max_tokens = custom_requirements["max_tokens"]

        if "temperature" in custom_requirements:
            base_config.temperature = custom_requirements["temperature"]

        if "preferred_provider" in custom_requirements:
            preferred = custom_requirements["preferred_provider"]
            if preferred in [p.value for p in ModelProvider]:
                base_config.provider = ModelProvider(preferred)

        return base_config

    def _create_provider(self, config: ModelConfig) -> Any:
        """Создать провайдера для модели."""
        api_key = self.api_keys.get(config.provider.value, "")

        if not api_key:
            raise ValueError(f"API ключ не найден для провайдера {config.provider.value}")

        if config.provider == ModelProvider.QWEN:
            return OpenAIProvider(
                base_url=os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
                api_key=api_key
            )
        elif config.provider == ModelProvider.OPENAI:
            return OpenAIProvider(api_key=api_key)
        elif config.provider == ModelProvider.GEMINI:
            # Для Gemini используем OpenAI-совместимый API
            return OpenAIProvider(
                base_url=os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
                api_key=api_key
            )
        else:
            raise ValueError(f"Неподдерживаемый провайдер: {config.provider}")

    def _create_model(self, provider: Any, config: ModelConfig) -> Model:
        """Создать модель с конфигурацией."""
        return OpenAIModel(
            model_name=config.model_name,
            provider=provider
        )

    def _get_fallback_model(self) -> Model:
        """Получить fallback модель при ошибках."""
        api_key = self.api_keys.get("qwen", "") or os.getenv("LLM_API_KEY", "")

        provider = OpenAIProvider(
            base_url=os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
            api_key=api_key
        )

        return OpenAIModel("qwen2.5-32b-instruct", provider=provider)

    def estimate_cost(
        self,
        content_type: str,
        complexity: str,
        estimated_tokens: int
    ) -> Dict[str, float]:
        """
        Оценить стоимость генерации контента.

        Args:
            content_type: Тип контента
            complexity: Сложность
            estimated_tokens: Ожидаемое количество токенов

        Returns:
            Оценка стоимости в различных валютах
        """
        if content_type in self.models and complexity in self.models[content_type]:
            config = self.models[content_type][complexity]
            cost_usd = (estimated_tokens / 1000) * config.cost_per_1k_tokens

            return {
                "usd": round(cost_usd, 4),
                "uah": round(cost_usd * 41, 2),  # Примерный курс
                "eur": round(cost_usd * 0.92, 4),
                "tokens": estimated_tokens,
                "model": config.model_name
            }

        return {"error": "Не удалось оценить стоимость"}

    def get_available_models(self, content_type: str = None) -> Dict[str, Any]:
        """Получить список доступных моделей."""
        if content_type and content_type in self.models:
            return {
                "content_type": content_type,
                "models": {
                    complexity: {
                        "model_name": config.model_name,
                        "provider": config.provider.value,
                        "description": config.description,
                        "cost_per_1k_tokens": config.cost_per_1k_tokens
                    }
                    for complexity, config in self.models[content_type].items()
                }
            }
        else:
            return {
                "all_content_types": list(self.models.keys()),
                "total_models": sum(len(models) for models in self.models.values())
            }


# === ФУНКЦИИ УТИЛИТЫ ===

def get_llm_model(
    content_type: str = "blog_post",
    complexity: str = "medium",
    quality_preference: str = "balanced"
) -> Model:
    """
    Быстрый способ получения модели для задачи.

    Args:
        content_type: Тип контента
        complexity: Уровень сложности
        quality_preference: Предпочтения качества

    Returns:
        Настроенная модель
    """
    provider = ContentGeneratorLLMProvider()
    return provider.get_model_for_task(content_type, complexity, quality_preference)


def get_optimal_model_for_content(
    content_length: str,
    domain_type: str,
    quality_standard: str
) -> Model:
    """
    Получить оптимальную модель на основе характеристик контента.

    Args:
        content_length: Длина контента (short, medium, long, comprehensive)
        domain_type: Домен контента
        quality_standard: Стандарт качества

    Returns:
        Оптимальная модель
    """
    # Маппинг характеристик в параметры модели
    complexity_mapping = {
        "short": "simple",
        "medium": "medium",
        "long": "complex",
        "comprehensive": "complex"
    }

    quality_mapping = {
        "basic": "cost_optimized",
        "standard": "balanced",
        "high": "quality_first",
        "premium": "quality_first"
    }

    domain_type_mapping = {
        "technology": "documentation",
        "business": "marketing",
        "education": "educational",
        "health": "blog_post",
        "finance": "blog_post",
        "lifestyle": "social_media"
    }

    content_type = domain_type_mapping.get(domain_type, "blog_post")
    complexity = complexity_mapping.get(content_length, "medium")
    quality_preference = quality_mapping.get(quality_standard, "balanced")

    return get_llm_model(content_type, complexity, quality_preference)


# === ЭКСПОРТ ===

__all__ = [
    "ContentGeneratorLLMProvider",
    "ModelProvider",
    "ContentComplexity",
    "get_llm_model",
    "get_optimal_model_for_content"
]