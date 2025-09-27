# -*- coding: utf-8 -*-
"""
LLM провайдеры для Universal Opportunity Analyzer Agent
Поддержка multiple провайдеров с оптимизацией стоимости анализа
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Попытка импорта провайдеров (graceful fallback)
try:
    from pydantic_ai.models.openai import OpenAIModel
    from pydantic_ai.providers.openai import OpenAIProvider
except ImportError:
    OpenAIModel = None
    OpenAIProvider = None

try:
    from pydantic_ai.models.gemini import GeminiModel
    from pydantic_ai.providers.gemini import GeminiProvider
except ImportError:
    GeminiModel = None
    GeminiProvider = None

logger = logging.getLogger(__name__)

class OpportunityAnalyzerLLMProvider:
    """
    Универсальный провайдер LLM для анализа возможностей с оптимизацией стоимости.

    Поддерживает различные модели в зависимости от типа задач анализа:
    - Qwen Coder для технического анализа
    - Gemini Flash для текстового анализа (экономия до 90%)
    - OpenAI для сложных аналитических задач
    """

    def __init__(self, domain_type: str = "psychology", analysis_type: str = "comprehensive"):
        self.domain_type = domain_type
        self.analysis_type = analysis_type

        # Загружаем environment variables
        load_dotenv()

        # Конфигурируем провайдеры
        self._setup_providers()

    def _setup_providers(self):
        """Настроить доступные провайдеры LLM."""
        self.providers = {}

        # Qwen провайдер (основной для анализа)
        qwen_api_key = os.getenv("LLM_API_KEY")
        qwen_base_url = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

        if qwen_api_key and OpenAIProvider:
            try:
                self.providers["qwen"] = OpenAIProvider(
                    base_url=qwen_base_url,
                    api_key=qwen_api_key
                )
                logger.info("Qwen провайдер настроен успешно")
            except Exception as e:
                logger.warning(f"Не удалось настроить Qwen провайдер: {e}")

        # Gemini провайдер (для экономии на текстовых задачах)
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key and GeminiProvider:
            try:
                self.providers["gemini"] = GeminiProvider(api_key=gemini_api_key)
                logger.info("Gemini провайдер настроен успешно")
            except Exception as e:
                logger.warning(f"Не удалось настроить Gemini провайдер: {e}")

        # OpenAI провайдер (запасной)
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key and OpenAIProvider:
            try:
                self.providers["openai"] = OpenAIProvider(api_key=openai_api_key)
                logger.info("OpenAI провайдер настроен успешно")
            except Exception as e:
                logger.warning(f"Не удалось настроить OpenAI провайдер: {e}")

    def get_model_for_task(self, task_type: str = "analysis") -> Any:
        """
        Получить оптимальную модель для конкретного типа задачи анализа.

        Args:
            task_type: Тип задачи (analysis, research, scoring, documentation)

        Returns:
            Настроенная модель LLM
        """
        # Стратегия выбора модели с оптимизацией стоимости
        model_strategy = self._get_model_strategy(task_type)

        # Пытаемся получить модель согласно стратегии
        for provider_name, model_name in model_strategy:
            provider = self.providers.get(provider_name)
            if provider:
                try:
                    if provider_name == "qwen":
                        return OpenAIModel(model_name, provider=provider)
                    elif provider_name == "gemini":
                        return GeminiModel(model_name, provider=provider)
                    elif provider_name == "openai":
                        return OpenAIModel(model_name, provider=provider)
                except Exception as e:
                    logger.warning(f"Ошибка создания модели {model_name}: {e}")
                    continue

        # Fallback на первый доступный провайдер
        return self._get_fallback_model()

    def _get_model_strategy(self, task_type: str) -> list:
        """
        Получить стратегию выбора модели для типа задачи.

        Returns:
            Список кортежей (provider, model) в порядке приоритета
        """
        strategies = {
            "analysis": [
                ("qwen", "qwen2.5-coder-32b-instruct"),  # Лучше для структурированного анализа
                ("qwen", "qwen2.5-72b-instruct"),        # Для сложного анализа
                ("gemini", "gemini-2.5-flash"),          # Экономичная альтернатива
                ("openai", "gpt-4o-mini")                # Fallback
            ],
            "research": [
                ("gemini", "gemini-2.5-flash-lite"),     # Очень дешево для research
                ("qwen", "qwen2.5-7b-instruct"),         # Быстро и экономично
                ("openai", "gpt-4o-mini")                # Fallback
            ],
            "scoring": [
                ("qwen", "qwen2.5-coder-7b-instruct"),   # Хорошо для структурированных расчетов
                ("gemini", "gemini-2.5-flash"),          # Дешево для численных задач
                ("openai", "gpt-4o-mini")                # Fallback
            ],
            "documentation": [
                ("gemini", "gemini-2.5-flash-lite"),     # Самый дешевый для текста
                ("qwen", "qwen2.5-7b-instruct"),         # Альтернатива
                ("openai", "gpt-4o-mini")                # Fallback
            ],
            "complex_analysis": [
                ("qwen", "qwen2.5-72b-instruct"),        # Для самых сложных задач
                ("qwen", "qwen2.5-coder-32b-instruct"),  # Альтернатива
                ("openai", "gpt-4o"),                    # Премиум fallback
                ("gemini", "gemini-2.5-flash")           # Экономичный fallback
            ]
        }

        return strategies.get(task_type, strategies["analysis"])

    def _get_fallback_model(self) -> Any:
        """Получить fallback модель если основные недоступны."""
        # Пытаемся использовать любой доступный провайдер
        fallback_configs = [
            ("qwen", "qwen2.5-coder-7b-instruct"),
            ("gemini", "gemini-2.5-flash-lite"),
            ("openai", "gpt-4o-mini")
        ]

        for provider_name, model_name in fallback_configs:
            provider = self.providers.get(provider_name)
            if provider:
                try:
                    if provider_name == "qwen":
                        return OpenAIModel(model_name, provider=provider)
                    elif provider_name == "gemini":
                        return GeminiModel(model_name, provider=provider)
                    elif provider_name == "openai":
                        return OpenAIModel(model_name, provider=provider)
                except Exception as e:
                    logger.warning(f"Fallback модель {model_name} недоступна: {e}")
                    continue

        # Если ничего не работает - ошибка
        raise RuntimeError(
            "Не удалось настроить ни одного LLM провайдера. "
            "Проверьте переменные окружения: LLM_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY"
        )

    def get_cost_estimate(self, task_type: str, input_tokens: int, output_tokens: int) -> Dict[str, Any]:
        """
        Получить оценку стоимости для задачи анализа.

        Args:
            task_type: Тип задачи
            input_tokens: Количество входных токенов
            output_tokens: Количество выходных токенов

        Returns:
            Информация о стоимости
        """
        # Примерные цены за 1M токенов (USD)
        pricing = {
            "qwen": {
                "qwen2.5-72b-instruct": {"input": 0.80, "output": 3.20},
                "qwen2.5-coder-32b-instruct": {"input": 0.25, "output": 1.00},
                "qwen2.5-coder-7b-instruct": {"input": 0.10, "output": 0.40},
                "qwen2.5-7b-instruct": {"input": 0.10, "output": 0.40}
            },
            "gemini": {
                "gemini-2.5-flash": {"input": 0.15, "output": 0.60},
                "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40}
            },
            "openai": {
                "gpt-4o": {"input": 2.50, "output": 10.00},
                "gpt-4o-mini": {"input": 0.15, "output": 0.60}
            }
        }

        strategy = self._get_model_strategy(task_type)
        if strategy:
            provider_name, model_name = strategy[0]
            model_pricing = pricing.get(provider_name, {}).get(model_name, {"input": 0.15, "output": 0.60})

            cost = (input_tokens * model_pricing["input"] + output_tokens * model_pricing["output"]) / 1_000_000

            return {
                "provider": provider_name,
                "model": model_name,
                "estimated_cost_usd": round(cost, 6),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "task_type": task_type
            }

        return {"error": "Не удалось рассчитать стоимость"}

def get_llm_model(domain_type: str = "psychology", task_type: str = "analysis") -> Any:
    """
    Фабричная функция для получения оптимальной LLM модели.

    Args:
        domain_type: Тип домена анализа
        task_type: Тип аналитической задачи

    Returns:
        Настроенная модель LLM
    """
    try:
        provider_manager = OpportunityAnalyzerLLMProvider(domain_type)
        return provider_manager.get_model_for_task(task_type)
    except Exception as e:
        logger.error(f"Ошибка настройки LLM модели: {e}")
        raise

def get_cost_optimized_model(estimated_tokens: int = 5000, task_complexity: str = "medium") -> Any:
    """
    Получить модель с оптимизацией по стоимости.

    Args:
        estimated_tokens: Примерное количество токенов
        task_complexity: Сложность задачи (simple, medium, complex)

    Returns:
        Оптимальная по стоимости модель
    """
    # Выбираем тип задачи на основе сложности
    task_mapping = {
        "simple": "documentation",     # Самые дешевые модели
        "medium": "analysis",          # Баланс цена/качество
        "complex": "complex_analysis"  # Качество важнее цены
    }

    task_type = task_mapping.get(task_complexity, "analysis")

    # Дополнительная оптимизация для больших объемов
    if estimated_tokens > 10000 and task_complexity != "complex":
        task_type = "research"  # Используем более дешевые модели

    return get_llm_model(task_type=task_type)