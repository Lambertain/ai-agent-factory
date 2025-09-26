"""
Провайдеры моделей для Psychology Quality Guardian Agent

Универсальная система управления LLM провайдерами с оптимизацией
под различные задачи контроля качества.
"""

from typing import Optional, Dict, Any
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.gemini import GeminiProvider
from pydantic_ai.models.gemini import GeminiModel

from .settings import PsychologyQualityGuardianSettings, load_settings


class QualityGuardianModelProvider:
    """
    Провайдер моделей для Psychology Quality Guardian Agent.

    Обеспечивает интеллектуальную маршрутизацию запросов к оптимальным
    моделям в зависимости от типа задачи и требований качества.
    """

    def __init__(self, settings: Optional[PsychologyQualityGuardianSettings] = None):
        """
        Инициализация провайдера моделей.

        Args:
            settings: Настройки агента (загружаются автоматически если не указаны)
        """
        self.settings = settings or load_settings()
        self._providers: Dict[str, Any] = {}
        self._models: Dict[str, Any] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Инициализация доступных провайдеров."""

        # Основной провайдер (Qwen через Dashscope)
        if self.settings.llm_api_key:
            self._providers["qwen"] = OpenAIProvider(
                base_url=self.settings.llm_base_url,
                api_key=self.settings.llm_api_key
            )

        # OpenAI провайдер (если настроен)
        if self.settings.openai_api_key:
            self._providers["openai"] = OpenAIProvider(
                api_key=self.settings.openai_api_key
            )

        # Gemini провайдер (если настроен)
        if self.settings.gemini_api_key:
            self._providers["gemini"] = GeminiProvider(
                api_key=self.settings.gemini_api_key
            )

        self._initialize_models()

    def _initialize_models(self):
        """Инициализация моделей для различных задач."""

        # Модели для основного Qwen провайдера
        if "qwen" in self._providers:
            qwen_provider = self._providers["qwen"]

            # Основная модель для общего анализа
            self._models["general"] = OpenAIModel(
                self.settings.llm_model,
                provider=qwen_provider
            )

            # Мощная модель для этического анализа
            self._models["ethical_analysis"] = OpenAIModel(
                self.settings.ethical_analysis_model,
                provider=qwen_provider
            )

            # Специализированная модель для научной валидации
            self._models["scientific_validation"] = OpenAIModel(
                self.settings.scientific_validation_model,
                provider=qwen_provider
            )

            # Быстрая модель для анализа безопасности
            self._models["safety_analysis"] = OpenAIModel(
                self.settings.safety_analysis_model,
                provider=qwen_provider
            )

        # Экономичная модель для отчетов (Gemini если доступен)
        if "gemini" in self._providers:
            self._models["reporting"] = GeminiModel(
                self.settings.reporting_model,
                provider=self._providers["gemini"]
            )
        elif "qwen" in self._providers:
            # Fallback на Qwen если Gemini недоступен
            self._models["reporting"] = OpenAIModel(
                self.settings.safety_analysis_model,  # Используем быструю модель для отчетов
                provider=self._providers["qwen"]
            )

        # OpenAI модели (если доступны)
        if "openai" in self._providers:
            openai_provider = self._providers["openai"]
            self._models["openai_general"] = OpenAIModel(
                "gpt-4o-mini",  # Экономичная модель OpenAI
                provider=openai_provider
            )
            self._models["openai_advanced"] = OpenAIModel(
                "gpt-4o",  # Мощная модель OpenAI
                provider=openai_provider
            )

    def get_model_for_task(self, task_type: str, domain: str = "general", complexity: str = "standard") -> Any:
        """
        Получить оптимальную модель для конкретной задачи.

        Args:
            task_type: Тип задачи (ethical_analysis, scientific_validation, safety_analysis, reporting)
            domain: Домен применения (clinical, research, educational, wellness, organizational)
            complexity: Сложность задачи (simple, standard, complex, critical)

        Returns:
            Модель LLM оптимальная для задачи
        """

        # Логика выбора модели в зависимости от задачи и контекста
        model_key = self._determine_optimal_model(task_type, domain, complexity)

        if model_key in self._models:
            return self._models[model_key]

        # Fallback на основную модель
        return self._models.get("general") or self._get_fallback_model()

    def _determine_optimal_model(self, task_type: str, domain: str, complexity: str) -> str:
        """Определить оптимальную модель на основе параметров."""

        # Критические задачи требуют лучших моделей
        if complexity == "critical" or domain in ["clinical", "research"]:
            if task_type == "ethical_analysis":
                return "ethical_analysis"
            elif task_type == "scientific_validation":
                return "scientific_validation"
            elif task_type in ["safety_analysis", "content_analysis"]:
                return "safety_analysis"

        # Стандартные задачи
        if task_type == "ethical_analysis":
            return "ethical_analysis" if complexity in ["standard", "complex"] else "general"
        elif task_type == "scientific_validation":
            return "scientific_validation" if complexity in ["standard", "complex"] else "general"
        elif task_type in ["safety_analysis", "content_analysis"]:
            return "safety_analysis"
        elif task_type in ["reporting", "documentation"]:
            return "reporting"

        # Домен-специфичная логика
        if domain == "clinical":
            return "ethical_analysis"  # Клиника требует особой осторожности
        elif domain == "research":
            return "scientific_validation"  # Исследования требуют научной строгости
        elif domain == "wellness":
            return "safety_analysis"  # Wellness требует быстрого анализа безопасности

        return "general"

    def get_model_for_evaluation_type(self, evaluation_scope: list, domain_type: str = "general") -> Any:
        """
        Получить модель для конкретного типа оценки.

        Args:
            evaluation_scope: Список областей оценки
            domain_type: Тип домена

        Returns:
            Подходящая модель LLM
        """

        # Если оценка включает этические аспекты - используем мощную модель
        if "ethical" in evaluation_scope:
            return self.get_model_for_task("ethical_analysis", domain_type, "complex")

        # Если оценка включает научную валидацию - используем специализированную модель
        if "scientific" in evaluation_scope or "psychometric" in evaluation_scope:
            return self.get_model_for_task("scientific_validation", domain_type, "complex")

        # Если только безопасность - можно использовать быструю модель
        if evaluation_scope == ["safety"]:
            return self.get_model_for_task("safety_analysis", domain_type, "standard")

        # Для комплексной оценки используем основную модель
        return self.get_model_for_task("general", domain_type, "standard")

    def get_cost_optimized_model(self, task_type: str, priority: str = "balanced") -> Any:
        """
        Получить модель с оптимизацией по стоимости.

        Args:
            task_type: Тип задачи
            priority: Приоритет (cost, quality, balanced)

        Returns:
            Модель с учетом соотношения цена/качество
        """

        if priority == "cost":
            # Максимальная экономия
            if task_type in ["reporting", "documentation", "simple_analysis"]:
                return self._models.get("reporting") or self._models.get("safety_analysis")
            else:
                return self._models.get("safety_analysis") or self._models.get("general")

        elif priority == "quality":
            # Максимальное качество
            if task_type == "ethical_analysis":
                return self._models.get("ethical_analysis") or self._models.get("general")
            elif task_type == "scientific_validation":
                return self._models.get("scientific_validation") or self._models.get("general")
            else:
                return self._models.get("general")

        else:  # balanced
            # Сбалансированный подход
            return self.get_model_for_task(task_type)

    def get_batch_processing_model(self, batch_size: int, task_complexity: str = "standard") -> Any:
        """
        Получить модель для пакетной обработки.

        Args:
            batch_size: Размер пакета
            task_complexity: Сложность задач

        Returns:
            Оптимальная модель для пакетной обработки
        """

        # Для больших пакетов используем экономичные модели
        if batch_size > 20:
            if task_complexity == "simple":
                return self._models.get("reporting") or self._models.get("safety_analysis")
            else:
                return self._models.get("safety_analysis") or self._models.get("general")

        # Для средних пакетов - стандартные модели
        elif batch_size > 5:
            return self._models.get("general")

        # Для малых пакетов можем позволить лучшие модели
        else:
            if task_complexity == "complex":
                return self._models.get("ethical_analysis") or self._models.get("general")
            else:
                return self._models.get("general")

    def _get_fallback_model(self) -> Any:
        """Получить fallback модель если основные недоступны."""
        # Приоритет fallback моделей
        fallback_priority = ["general", "safety_analysis", "reporting", "openai_general"]

        for model_key in fallback_priority:
            if model_key in self._models:
                return self._models[model_key]

        raise RuntimeError("Ни одна модель LLM не доступна. Проверьте настройки API ключей.")

    def get_available_models(self) -> Dict[str, str]:
        """Получить список доступных моделей."""
        available = {}
        for key, model in self._models.items():
            model_name = getattr(model, 'model_name', str(model))
            available[key] = model_name
        return available

    def get_provider_status(self) -> Dict[str, bool]:
        """Получить статус доступности провайдеров."""
        return {
            "qwen": "qwen" in self._providers,
            "openai": "openai" in self._providers,
            "gemini": "gemini" in self._providers
        }

    def estimate_cost(self, task_type: str, content_length: int, domain: str = "general") -> Dict[str, Any]:
        """
        Оценить стоимость выполнения задачи.

        Args:
            task_type: Тип задачи
            content_length: Длина контента (примерное количество токенов)
            domain: Домен применения

        Returns:
            Оценка стоимости и рекомендации
        """

        # Примерные коэффициенты стоимости (relative costs)
        model_costs = {
            "ethical_analysis": 1.0,  # Qwen 72B - дорогая модель
            "scientific_validation": 0.6,  # Qwen 32B Coder - средняя
            "safety_analysis": 0.3,  # Qwen 7B Coder - дешевая
            "general": 0.6,  # Qwen 32B Coder - средняя
            "reporting": 0.1,  # Gemini Flash Lite - очень дешевая
        }

        selected_model_key = self._determine_optimal_model(task_type, domain, "standard")
        base_cost = model_costs.get(selected_model_key, 0.6)

        # Оценка относительной стоимости
        estimated_tokens = content_length * 1.3  # Учитываем системный промпт и ответ
        relative_cost = base_cost * (estimated_tokens / 1000)

        return {
            "selected_model": selected_model_key,
            "relative_cost": relative_cost,
            "estimated_tokens": estimated_tokens,
            "cost_level": "low" if relative_cost < 0.5 else "medium" if relative_cost < 2.0 else "high",
            "optimization_suggestions": self._get_cost_optimization_suggestions(task_type, relative_cost)
        }

    def _get_cost_optimization_suggestions(self, task_type: str, relative_cost: float) -> list:
        """Получить предложения по оптимизации стоимости."""
        suggestions = []

        if relative_cost > 2.0:
            suggestions.append("Рассмотрите использование более экономичной модели для данной задачи")
            if task_type == "reporting":
                suggestions.append("Для отчетов можно использовать Gemini Flash Lite")

        if relative_cost > 1.0:
            suggestions.append("Можно разбить задачу на более мелкие части")
            suggestions.append("Рассмотрите пакетную обработку для экономии")

        if not suggestions:
            suggestions.append("Текущая конфигурация оптимальна по стоимости")

        return suggestions


# Глобальный экземпляр провайдера
_provider_instance: Optional[QualityGuardianModelProvider] = None


def get_model_provider(settings: Optional[PsychologyQualityGuardianSettings] = None) -> QualityGuardianModelProvider:
    """
    Получить глобальный экземпляр провайдера моделей.

    Args:
        settings: Настройки (опционально, для переинициализации)

    Returns:
        Экземпляр провайдера моделей
    """
    global _provider_instance

    if _provider_instance is None or settings is not None:
        _provider_instance = QualityGuardianModelProvider(settings)

    return _provider_instance


def get_llm_model(
    task_type: str = "general",
    domain: str = "general",
    complexity: str = "standard"
) -> Any:
    """
    Быстрый доступ к модели для задачи.

    Args:
        task_type: Тип задачи
        domain: Домен
        complexity: Сложность

    Returns:
        Модель LLM
    """
    provider = get_model_provider()
    return provider.get_model_for_task(task_type, domain, complexity)


def get_default_model() -> Any:
    """Получить модель по умолчанию для агента."""
    return get_llm_model("general", "general", "standard")


# Экспорт
__all__ = [
    "QualityGuardianModelProvider",
    "get_model_provider",
    "get_llm_model",
    "get_default_model"
]