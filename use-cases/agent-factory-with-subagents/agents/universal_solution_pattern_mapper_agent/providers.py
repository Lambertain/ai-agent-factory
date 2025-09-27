# -*- coding: utf-8 -*-
"""
LLM провайдеры для Universal Solution Pattern Mapper Agent
Оптимизированная система выбора моделей для задач маппинга решений
"""

import os
from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class ModelProvider(Enum):
    """Поддерживаемые провайдеры LLM моделей."""
    QWEN = "qwen"
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"

class TaskComplexity(Enum):
    """Уровни сложности задач маппинга решений."""
    SIMPLE = "simple"  # Базовое маппинг простых паттернов
    MEDIUM = "medium"  # Комплексный анализ решений
    COMPLEX = "complex"  # Глубокое архитектурное проектирование
    CRITICAL = "critical"  # Критические системные решения

@dataclass
class ModelConfig:
    """Конфигурация модели для конкретного типа задач."""
    provider: ModelProvider
    model_name: str
    max_tokens: int
    temperature: float
    cost_per_1k_tokens: float
    quality_score: float  # 1-10
    speed_score: float  # 1-10

class SolutionPatternMapperLLMProvider:
    """
    Провайдер LLM моделей для Universal Solution Pattern Mapper Agent.

    Автоматически выбирает оптимальную модель на основе:
    - Сложности задачи маппинга
    - Требований к качеству анализа
    - Ограничений по стоимости
    - Доступности провайдеров
    """

    def __init__(self, preferred_provider: Optional[str] = None, cost_optimization: bool = True):
        self.preferred_provider = preferred_provider
        self.cost_optimization = cost_optimization
        self.available_providers = self._check_available_providers()
        self.model_configs = self._get_model_configurations()

    def _check_available_providers(self) -> Dict[str, bool]:
        """Проверить доступность провайдеров LLM."""
        return {
            "qwen": os.getenv("QWEN_API_KEY") is not None,
            "gemini": os.getenv("GEMINI_API_KEY") is not None,
            "openai": OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY") is not None,
            "claude": os.getenv("ANTHROPIC_API_KEY") is not None
        }

    def _get_model_configurations(self) -> Dict[str, ModelConfig]:
        """Получить конфигурации моделей для разных задач маппинга."""
        return {
            # Быстрые и экономичные модели для простых задач
            "qwen_simple": ModelConfig(
                provider=ModelProvider.QWEN,
                model_name="qwen2.5:7b",
                max_tokens=2048,
                temperature=0.3,
                cost_per_1k_tokens=0.001,
                quality_score=7.0,
                speed_score=9.0
            ),

            # Средние модели для комплексного анализа
            "qwen_medium": ModelConfig(
                provider=ModelProvider.QWEN,
                model_name="qwen2.5:14b",
                max_tokens=4096,
                temperature=0.4,
                cost_per_1k_tokens=0.003,
                quality_score=8.0,
                speed_score=8.0
            ),

            # Мощные модели для сложного маппинга
            "gemini_complex": ModelConfig(
                provider=ModelProvider.GEMINI,
                model_name="gemini-1.5-pro",
                max_tokens=8192,
                temperature=0.5,
                cost_per_1k_tokens=0.01,
                quality_score=9.0,
                speed_score=7.0
            ),

            # Премиум модели для критических задач
            "openai_critical": ModelConfig(
                provider=ModelProvider.OPENAI,
                model_name="gpt-4o",
                max_tokens=16384,
                temperature=0.3,
                cost_per_1k_tokens=0.03,
                quality_score=9.5,
                speed_score=6.0
            ),

            "claude_critical": ModelConfig(
                provider=ModelProvider.CLAUDE,
                model_name="claude-3-5-sonnet-20241022",
                max_tokens=8192,
                temperature=0.4,
                cost_per_1k_tokens=0.015,
                quality_score=9.8,
                speed_score=7.5
            )
        }

    def get_model_for_task(self, task_type: str = "pattern_mapping",
                          complexity: str = "medium",
                          domain_type: str = "psychology") -> Any:
        """
        Получить оптимальную модель для задачи маппинга решений.

        Args:
            task_type: Тип задачи (pattern_mapping, solution_analysis, blueprint_generation)
            complexity: Сложность задачи (simple, medium, complex, critical)
            domain_type: Домен для маппинга (psychology, business, etc.)

        Returns:
            Настроенный объект модели LLM
        """
        model_strategy = self._get_model_strategy(task_type, complexity, domain_type)

        for config_name in model_strategy:
            config = self.model_configs.get(config_name)
            if not config:
                continue

            provider_name = config.provider.value
            if not self.available_providers.get(provider_name, False):
                continue

            try:
                return self._create_model_instance(config)
            except Exception as e:
                print(f"Ошибка создания модели {config_name}: {e}")
                continue

        # Fallback к базовой модели
        return self._get_fallback_model()

    def _get_model_strategy(self, task_type: str, complexity: str, domain_type: str) -> list:
        """Определить стратегию выбора модели на основе параметров задачи."""

        # Стратегии для разных типов задач маппинга
        task_strategies = {
            "pattern_mapping": {
                "simple": ["qwen_simple", "qwen_medium"],
                "medium": ["qwen_medium", "gemini_complex"],
                "complex": ["gemini_complex", "claude_critical"],
                "critical": ["claude_critical", "openai_critical", "gemini_complex"]
            },
            "solution_analysis": {
                "simple": ["qwen_medium", "qwen_simple"],
                "medium": ["gemini_complex", "qwen_medium"],
                "complex": ["claude_critical", "gemini_complex"],
                "critical": ["claude_critical", "openai_critical"]
            },
            "blueprint_generation": {
                "simple": ["qwen_medium", "gemini_complex"],
                "medium": ["gemini_complex", "claude_critical"],
                "complex": ["claude_critical", "openai_critical"],
                "critical": ["claude_critical", "openai_critical"]
            },
            "domain_adaptation": {
                "simple": ["qwen_simple", "qwen_medium"],
                "medium": ["qwen_medium", "gemini_complex"],
                "complex": ["gemini_complex", "claude_critical"],
                "critical": ["claude_critical", "openai_critical"]
            }
        }

        # Дополнительные приоритеты для специфичных доменов
        domain_adjustments = {
            "psychology": {
                "preference": ["claude_critical", "gemini_complex"],  # Высокие требования к этике
                "minimum_quality": 8.5
            },
            "business": {
                "preference": ["gemini_complex", "openai_critical"],  # Фокус на аналитику
                "minimum_quality": 8.0
            },
            "astrology": {
                "preference": ["qwen_medium", "gemini_complex"],  # Баланс качества и стоимости
                "minimum_quality": 7.5
            },
            "numerology": {
                "preference": ["qwen_medium", "qwen_simple"],  # Математическая точность
                "minimum_quality": 7.0
            }
        }

        base_strategy = task_strategies.get(task_type, {}).get(complexity, ["qwen_medium"])
        domain_prefs = domain_adjustments.get(domain_type, {}).get("preference", [])

        # Объединяем стратегии с учетом доменных предпочтений
        combined_strategy = []

        # Сначала доменные предпочтения
        for model in domain_prefs:
            if model in base_strategy:
                combined_strategy.append(model)

        # Затем остальные из базовой стратегии
        for model in base_strategy:
            if model not in combined_strategy:
                combined_strategy.append(model)

        return combined_strategy

    def _create_model_instance(self, config: ModelConfig) -> Any:
        """Создать экземпляр модели на основе конфигурации."""

        if config.provider == ModelProvider.QWEN:
            return self._create_qwen_model(config)
        elif config.provider == ModelProvider.GEMINI:
            return self._create_gemini_model(config)
        elif config.provider == ModelProvider.OPENAI:
            return self._create_openai_model(config)
        elif config.provider == ModelProvider.CLAUDE:
            return self._create_claude_model(config)
        else:
            raise ValueError(f"Неподдерживаемый провайдер: {config.provider}")

    def _create_qwen_model(self, config: ModelConfig) -> Any:
        """Создать модель Qwen."""
        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=os.getenv("QWEN_API_KEY"),
                base_url=os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            )

            # Возвращаем обертку для единообразного API
            class QwenModel:
                def __init__(self, client, model_name, max_tokens, temperature):
                    self.client = client
                    self.model_name = model_name
                    self.max_tokens = max_tokens
                    self.temperature = temperature

                def __call__(self, messages):
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature
                    )
                    return response.choices[0].message.content

            return QwenModel(client, config.model_name, config.max_tokens, config.temperature)

        except Exception as e:
            raise RuntimeError(f"Ошибка создания Qwen модели: {e}")

    def _create_gemini_model(self, config: ModelConfig) -> Any:
        """Создать модель Gemini."""
        try:
            import google.generativeai as genai

            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel(config.model_name)

            class GeminiModel:
                def __init__(self, model, max_tokens, temperature):
                    self.model = model
                    self.max_tokens = max_tokens
                    self.temperature = temperature

                def __call__(self, messages):
                    # Конвертируем формат сообщений для Gemini
                    prompt = self._convert_messages_to_prompt(messages)

                    generation_config = genai.types.GenerationConfig(
                        max_output_tokens=self.max_tokens,
                        temperature=self.temperature
                    )

                    response = self.model.generate_content(
                        prompt,
                        generation_config=generation_config
                    )
                    return response.text

                def _convert_messages_to_prompt(self, messages):
                    prompt_parts = []
                    for msg in messages:
                        role = msg.get("role", "user")
                        content = msg.get("content", "")
                        if role == "system":
                            prompt_parts.append(f"System: {content}")
                        elif role == "user":
                            prompt_parts.append(f"User: {content}")
                        elif role == "assistant":
                            prompt_parts.append(f"Assistant: {content}")
                    return "\n\n".join(prompt_parts)

            return GeminiModel(model, config.max_tokens, config.temperature)

        except Exception as e:
            raise RuntimeError(f"Ошибка создания Gemini модели: {e}")

    def _create_openai_model(self, config: ModelConfig) -> Any:
        """Создать модель OpenAI."""
        try:
            from openai import OpenAI

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            class OpenAIModel:
                def __init__(self, client, model_name, max_tokens, temperature):
                    self.client = client
                    self.model_name = model_name
                    self.max_tokens = max_tokens
                    self.temperature = temperature

                def __call__(self, messages):
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature
                    )
                    return response.choices[0].message.content

            return OpenAIModel(client, config.model_name, config.max_tokens, config.temperature)

        except Exception as e:
            raise RuntimeError(f"Ошибка создания OpenAI модели: {e}")

    def _create_claude_model(self, config: ModelConfig) -> Any:
        """Создать модель Claude."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            class ClaudeModel:
                def __init__(self, client, model_name, max_tokens, temperature):
                    self.client = client
                    self.model_name = model_name
                    self.max_tokens = max_tokens
                    self.temperature = temperature

                def __call__(self, messages):
                    # Разделяем системное сообщение от остальных
                    system_message = None
                    chat_messages = []

                    for msg in messages:
                        if msg.get("role") == "system":
                            system_message = msg.get("content", "")
                        else:
                            chat_messages.append(msg)

                    kwargs = {
                        "model": self.model_name,
                        "messages": chat_messages,
                        "max_tokens": self.max_tokens,
                        "temperature": self.temperature
                    }

                    if system_message:
                        kwargs["system"] = system_message

                    response = self.client.messages.create(**kwargs)
                    return response.content[0].text

            return ClaudeModel(client, config.model_name, config.max_tokens, config.temperature)

        except Exception as e:
            raise RuntimeError(f"Ошибка создания Claude модели: {e}")

    def _get_fallback_model(self) -> Any:
        """Получить резервную модель в случае недоступности основных."""

        # Пробуем создать простейшую доступную модель
        fallback_order = ["qwen_simple", "qwen_medium", "gemini_complex"]

        for config_name in fallback_order:
            config = self.model_configs.get(config_name)
            if not config:
                continue

            provider_name = config.provider.value
            if self.available_providers.get(provider_name, False):
                try:
                    return self._create_model_instance(config)
                except Exception:
                    continue

        # Последний резерв - заглушка
        class MockModel:
            def __call__(self, messages):
                return "Модель недоступна. Проверьте конфигурацию LLM провайдеров."

        return MockModel()

    def get_available_models(self) -> Dict[str, Dict]:
        """Получить список доступных моделей с их характеристиками."""
        available = {}

        for name, config in self.model_configs.items():
            provider_name = config.provider.value
            if self.available_providers.get(provider_name, False):
                available[name] = {
                    "provider": provider_name,
                    "model_name": config.model_name,
                    "quality_score": config.quality_score,
                    "speed_score": config.speed_score,
                    "cost_per_1k_tokens": config.cost_per_1k_tokens
                }

        return available

    def estimate_cost(self, task_type: str, complexity: str, estimated_tokens: int) -> float:
        """Оценить стоимость выполнения задачи."""
        model_strategy = self._get_model_strategy(task_type, complexity, "psychology")

        if not model_strategy:
            return 0.0

        # Берем первую доступную модель из стратегии
        for config_name in model_strategy:
            config = self.model_configs.get(config_name)
            if config and self.available_providers.get(config.provider.value, False):
                return (estimated_tokens / 1000) * config.cost_per_1k_tokens

        return 0.0

def get_llm_model(task_type: str = "pattern_mapping",
                  complexity: str = "medium",
                  domain_type: str = "psychology") -> Any:
    """
    Фабричная функция для получения оптимальной LLM модели.

    Args:
        task_type: Тип задачи маппинга решений
        complexity: Сложность задачи
        domain_type: Целевой домен

    Returns:
        Настроенная модель LLM
    """
    provider = SolutionPatternMapperLLMProvider()
    return provider.get_model_for_task(task_type, complexity, domain_type)