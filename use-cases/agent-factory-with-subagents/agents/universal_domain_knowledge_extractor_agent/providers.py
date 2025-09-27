# -*- coding: utf-8 -*-
"""
Провайдеры LLM для Universal Domain Knowledge Extractor Agent
Поддерживает различные модели с оптимизацией под задачи извлечения знаний
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Загружаем переменные окружения
load_dotenv()

class KnowledgeExtractionModelProvider:
    """Провайдер моделей для задач извлечения знаний."""

    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

        if not self.api_key:
            raise ValueError("LLM_API_KEY не найден в переменных окружения")

    def get_extraction_model(self, task_complexity: str = "medium") -> OpenAIModel:
        """
        Получить модель для извлечения знаний в зависимости от сложности задачи.

        Args:
            task_complexity: Сложность задачи (simple, medium, complex)

        Returns:
            Настроенная модель для извлечения знаний
        """
        # Выбор модели в зависимости от сложности
        model_mapping = {
            "simple": os.getenv("LLM_DOCS_MODEL", "gemini-2.5-flash-lite"),  # Простые задачи
            "medium": os.getenv("LLM_CODING_MODEL", "qwen2.5-coder-32b-instruct"),  # Средние задачи
            "complex": os.getenv("LLM_ARCHITECTURE_MODEL", "qwen2.5-72b-instruct")  # Сложные задачи
        }

        model_name = model_mapping.get(task_complexity, "qwen2.5-coder-32b-instruct")

        # Создаем провайдера
        provider = OpenAIProvider(
            base_url=self.base_url,
            api_key=self.api_key
        )

        # Возвращаем настроенную модель
        return OpenAIModel(
            model_name=model_name,
            provider=provider
        )

    def get_domain_optimized_model(self, domain_type: str) -> OpenAIModel:
        """
        Получить модель, оптимизированную для конкретного домена.

        Args:
            domain_type: Тип домена (psychology, astrology, numerology, business)

        Returns:
            Оптимизированная модель для домена
        """
        # Доменно-специфичная оптимизация моделей
        domain_model_mapping = {
            "psychology": "qwen2.5-coder-32b-instruct",  # Для научной валидации
            "astrology": "qwen2.5-72b-instruct",  # Для сложных расчетов
            "numerology": "qwen2.5-coder-32b-instruct",  # Для математических вычислений
            "business": "gemini-2.5-flash-lite",  # Для быстрого анализа
            "generic": "qwen2.5-coder-32b-instruct"  # Универсальная модель
        }

        model_name = domain_model_mapping.get(domain_type, "qwen2.5-coder-32b-instruct")

        provider = OpenAIProvider(
            base_url=self.base_url,
            api_key=self.api_key
        )

        return OpenAIModel(
            model_name=model_name,
            provider=provider
        )

    def get_multilingual_model(self, target_language: str = "ukrainian") -> OpenAIModel:
        """
        Получить модель для многоязычной обработки знаний.

        Args:
            target_language: Целевой язык (ukrainian, polish, english)

        Returns:
            Модель с поддержкой многоязычности
        """
        # Для многоязычных задач используем более мощные модели
        multilingual_models = {
            "ukrainian": "qwen2.5-72b-instruct",  # Лучшая поддержка украинского
            "polish": "qwen2.5-coder-32b-instruct",  # Хорошая поддержка польского
            "english": "gemini-2.5-flash-lite",  # Быстрая для английского
            "mixed": "qwen2.5-72b-instruct"  # Для смешанных языков
        }

        model_name = multilingual_models.get(target_language, "qwen2.5-coder-32b-instruct")

        provider = OpenAIProvider(
            base_url=self.base_url,
            api_key=self.api_key
        )

        return OpenAIModel(
            model_name=model_name,
            provider=provider
        )

# Глобальный экземпляр провайдера
_model_provider = None

def get_model_provider() -> KnowledgeExtractionModelProvider:
    """Получить глобальный экземпляр провайдера моделей."""
    global _model_provider
    if _model_provider is None:
        _model_provider = KnowledgeExtractionModelProvider()
    return _model_provider

def get_llm_model(
    task_complexity: str = "medium",
    domain_type: Optional[str] = None,
    target_language: Optional[str] = None
) -> OpenAIModel:
    """
    Получить LLM модель для извлечения знаний.

    Args:
        task_complexity: Сложность задачи (simple, medium, complex)
        domain_type: Тип домена для оптимизации (optional)
        target_language: Целевой язык (optional)

    Returns:
        Настроенная модель LLM
    """
    provider = get_model_provider()

    # Приоритизация: если указан домен, используем доменную оптимизацию
    if domain_type:
        return provider.get_domain_optimized_model(domain_type)

    # Если указан язык, используем многоязычную модель
    if target_language:
        return provider.get_multilingual_model(target_language)

    # По умолчанию используем модель по сложности
    return provider.get_extraction_model(task_complexity)

def get_cost_optimized_model(operation_type: str = "extraction") -> OpenAIModel:
    """
    Получить модель с оптимизацией по стоимости.

    Args:
        operation_type: Тип операции (extraction, analysis, validation)

    Returns:
        Cost-оптимизированная модель
    """
    provider = get_model_provider()

    # Оптимизация по стоимости для разных типов операций
    cost_optimized_mapping = {
        "extraction": "gemini-2.5-flash-lite",  # Дешевая для извлечения
        "analysis": "qwen2.5-coder-32b-instruct",  # Средняя для анализа
        "validation": "gemini-2.5-flash-lite",  # Дешевая для валидации
        "complex_analysis": "qwen2.5-72b-instruct"  # Дорогая только для сложного анализа
    }

    model_name = cost_optimized_mapping.get(operation_type, "qwen2.5-coder-32b-instruct")

    provider_instance = OpenAIProvider(
        base_url=provider.base_url,
        api_key=provider.api_key
    )

    return OpenAIModel(
        model_name=model_name,
        provider=provider_instance
    )