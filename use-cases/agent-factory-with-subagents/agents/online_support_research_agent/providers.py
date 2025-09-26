"""
Провайдеры моделей для Psychology Research Agent

Интеллектуальная система управления LLM провайдерами с оптимизацией
под различные типы исследовательских задач.
"""

from typing import Optional, Dict, Any
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.gemini import GeminiProvider
from pydantic_ai.models.gemini import GeminiModel

from .settings import PsychologyResearchAgentSettings, load_settings


class ResearchModelProvider:
    """
    Провайдер моделей для Psychology Research Agent.

    Обеспечивает оптимальную маршрутизацию запросов к наиболее подходящим
    моделям в зависимости от типа исследовательской задачи.
    """

    def __init__(self, settings: Optional[PsychologyResearchAgentSettings] = None):
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
        """Инициализация моделей для различных исследовательских задач."""

        # Модели для основного Qwen провайдера
        if "qwen" in self._providers:
            qwen_provider = self._providers["qwen"]

            # Основная модель для общего анализа исследований
            self._models["general"] = OpenAIModel(
                self.settings.llm_model,
                provider=qwen_provider
            )

            # Мощная модель для методологического анализа
            self._models["methodology_analysis"] = OpenAIModel(
                self.settings.methodology_analysis_model,
                provider=qwen_provider
            )

            # Специализированная модель для статистической валидации
            self._models["statistical_validation"] = OpenAIModel(
                self.settings.statistical_validation_model,
                provider=qwen_provider
            )

            # Быстрая модель для литературного обзора
            self._models["literature_review"] = OpenAIModel(
                self.settings.literature_review_model,
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
                self.settings.literature_review_model,  # Используем быструю модель для отчетов
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

    def get_model_for_task(
        self,
        task_type: str,
        research_domain: str = "general",
        complexity: str = "standard"
    ) -> Any:
        """
        Получить оптимальную модель для конкретной исследовательской задачи.

        Args:
            task_type: Тип задачи (methodology_analysis, statistical_validation,
                      literature_review, reporting, meta_analysis)
            research_domain: Домен исследований (clinical, cognitive, social, developmental)
            complexity: Сложность задачи (simple, standard, complex, critical)

        Returns:
            Модель LLM оптимальная для задачи
        """

        # Логика выбора модели в зависимости от задачи и контекста
        model_key = self._determine_optimal_model(task_type, research_domain, complexity)

        if model_key in self._models:
            return self._models[model_key]

        # Fallback на основную модель
        return self._models.get("general") or self._get_fallback_model()

    def _determine_optimal_model(self, task_type: str, research_domain: str, complexity: str) -> str:
        """Определить оптимальную модель на основе параметров."""

        # Критические задачи требуют лучших моделей
        if complexity == "critical" or research_domain in ["clinical", "developmental"]:
            if task_type == "methodology_analysis":
                return "methodology_analysis"
            elif task_type == "statistical_validation":
                return "statistical_validation"
            elif task_type in ["meta_analysis", "systematic_review"]:
                return "methodology_analysis"  # Требует высокой точности

        # Специфичная логика по типам задач
        if task_type == "methodology_analysis":
            if complexity in ["complex", "critical"]:
                return "methodology_analysis"
            else:
                return "general"

        elif task_type == "statistical_validation":
            if complexity in ["standard", "complex", "critical"]:
                return "statistical_validation"
            else:
                return "general"

        elif task_type == "literature_review":
            # Литературный обзор может использовать более экономичную модель
            return "literature_review"

        elif task_type in ["reporting", "documentation", "summary"]:
            return "reporting"

        elif task_type in ["meta_analysis", "systematic_review"]:
            # Мета-анализ требует высокой точности
            return "methodology_analysis"

        # Домен-специфичная логика
        if research_domain == "clinical":
            return "methodology_analysis"  # Клиника требует особой точности
        elif research_domain == "developmental":
            return "methodology_analysis"  # Детские исследования требуют осторожности
        elif research_domain == "cognitive":
            return "statistical_validation"  # Когнитивные исследования очень статистичны
        elif research_domain == "social":
            return "general"  # Социальные исследования более гибкие

        return "general"

    def get_model_for_validation_level(
        self,
        validation_level: str,
        research_type: str = "empirical"
    ) -> Any:
        """
        Получить модель в зависимости от требуемого уровня валидации.

        Args:
            validation_level: Уровень валидации (basic, standard, rigorous, publication_grade)
            research_type: Тип исследования (empirical, theoretical, meta_analysis)

        Returns:
            Подходящая модель LLM
        """

        if validation_level in ["rigorous", "publication_grade"]:
            # Самые строгие требования
            if research_type == "meta_analysis":
                return self.get_model_for_task("methodology_analysis", complexity="critical")
            else:
                return self.get_model_for_task("methodology_analysis", complexity="complex")

        elif validation_level == "standard":
            # Стандартные требования
            if research_type in ["meta_analysis", "systematic_review"]:
                return self.get_model_for_task("methodology_analysis", complexity="standard")
            else:
                return self.get_model_for_task("statistical_validation", complexity="standard")

        else:  # basic
            # Базовая валидация
            return self.get_model_for_task("general", complexity="simple")

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
            if task_type in ["reporting", "documentation", "literature_search"]:
                return self._models.get("reporting") or self._models.get("literature_review")
            else:
                return self._models.get("literature_review") or self._models.get("general")

        elif priority == "quality":
            # Максимальное качество
            if task_type in ["methodology_analysis", "systematic_review"]:
                return self._models.get("methodology_analysis") or self._models.get("general")
            elif task_type == "statistical_validation":
                return self._models.get("statistical_validation") or self._models.get("general")
            else:
                return self._models.get("general")

        else:  # balanced
            # Сбалансированный подход
            return self.get_model_for_task(task_type)

    def get_batch_processing_model(
        self,
        batch_size: int,
        task_complexity: str = "standard"
    ) -> Any:
        """
        Получить модель для пакетной обработки исследований.

        Args:
            batch_size: Размер пакета
            task_complexity: Сложность задач

        Returns:
            Оптимальная модель для пакетной обработки
        """

        # Для больших пакетов используем экономичные модели
        if batch_size > 20:
            if task_complexity == "simple":
                return self._models.get("reporting") or self._models.get("literature_review")
            else:
                return self._models.get("literature_review") or self._models.get("general")

        # Для средних пакетов - стандартные модели
        elif batch_size > 5:
            return self._models.get("general")

        # Для малых пакетов можем позволить лучшие модели
        else:
            if task_complexity == "complex":
                return self._models.get("methodology_analysis") or self._models.get("general")
            else:
                return self._models.get("general")

    def get_model_for_research_phase(self, research_phase: str, domain: str = "general") -> Any:
        """
        Получить модель для определенной фазы исследования.

        Args:
            research_phase: Фаза исследования (planning, data_collection, analysis, reporting)
            domain: Домен исследования

        Returns:
            Подходящая модель для фазы исследования
        """

        if research_phase == "planning":
            # Планирование требует методологической экспертизы
            return self.get_model_for_task("methodology_analysis", domain, "standard")

        elif research_phase == "data_collection":
            # Сбор данных требует понимания протоколов
            return self.get_model_for_task("general", domain, "standard")

        elif research_phase == "analysis":
            # Анализ требует статистической экспертизы
            return self.get_model_for_task("statistical_validation", domain, "complex")

        elif research_phase == "reporting":
            # Отчетность может использовать экономичную модель
            return self.get_model_for_task("reporting", domain, "standard")

        else:
            return self.get_model_for_task("general", domain, "standard")

    def _get_fallback_model(self) -> Any:
        """Получить fallback модель если основные недоступны."""
        # Приоритет fallback моделей
        fallback_priority = [
            "general", "statistical_validation", "literature_review",
            "reporting", "openai_general"
        ]

        for model_key in fallback_priority:
            if model_key in self._models:
                return self._models[model_key]

        raise RuntimeError(
            "Ни одна модель LLM не доступна. Проверьте настройки API ключей."
        )

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

    def estimate_cost(
        self,
        task_type: str,
        content_length: int,
        research_domain: str = "general",
        complexity: str = "standard"
    ) -> Dict[str, Any]:
        """
        Оценить стоимость выполнения исследовательской задачи.

        Args:
            task_type: Тип задачи
            content_length: Длина контента (примерное количество токенов)
            research_domain: Домен исследования
            complexity: Сложность задачи

        Returns:
            Оценка стоимости и рекомендации
        """

        # Примерные коэффициенты стоимости (relative costs)
        model_costs = {
            "methodology_analysis": 1.0,  # Qwen 72B - самая дорогая
            "statistical_validation": 0.6,  # Qwen 32B Coder - средняя
            "general": 0.6,  # Qwen 32B Coder - средняя
            "literature_review": 0.3,  # Qwen 7B Coder - дешевая
            "reporting": 0.05,  # Gemini Flash Lite - очень дешевая
        }

        selected_model_key = self._determine_optimal_model(task_type, research_domain, complexity)
        base_cost = model_costs.get(selected_model_key, 0.6)

        # Дополнительные множители для исследовательских задач
        domain_multiplier = {
            "clinical": 1.2,  # Повышенные требования к точности
            "developmental": 1.2,  # Особая осторожность с детьми
            "cognitive": 1.0,
            "social": 0.9,
            "educational": 0.9,
            "general": 1.0
        }.get(research_domain, 1.0)

        complexity_multiplier = {
            "simple": 0.8,
            "standard": 1.0,
            "complex": 1.3,
            "critical": 1.6
        }.get(complexity, 1.0)

        # Оценка относительной стоимости
        estimated_tokens = content_length * 1.4  # Учитываем промпт и развернутый ответ
        relative_cost = base_cost * domain_multiplier * complexity_multiplier * (estimated_tokens / 1000)

        return {
            "selected_model": selected_model_key,
            "relative_cost": relative_cost,
            "estimated_tokens": estimated_tokens,
            "domain_multiplier": domain_multiplier,
            "complexity_multiplier": complexity_multiplier,
            "cost_level": (
                "low" if relative_cost < 0.5 else
                "medium" if relative_cost < 2.0 else
                "high" if relative_cost < 5.0 else
                "very_high"
            ),
            "optimization_suggestions": self._get_cost_optimization_suggestions(
                task_type, relative_cost, research_domain
            )
        }

    def _get_cost_optimization_suggestions(
        self,
        task_type: str,
        relative_cost: float,
        research_domain: str
    ) -> list:
        """Получить предложения по оптимизации стоимости."""
        suggestions = []

        if relative_cost > 3.0:
            suggestions.append("Рассмотрите разбивку на более мелкие задачи")
            if task_type == "methodology_analysis":
                suggestions.append("Для предварительного анализа можно использовать более экономичную модель")

        if relative_cost > 2.0:
            suggestions.append("Можно использовать пакетную обработку для экономии")
            if research_domain in ["social", "educational"]:
                suggestions.append("Для данного домена допустимы менее строгие требования к модели")

        if task_type == "reporting" and relative_cost > 1.0:
            suggestions.append("Для отчетов рекомендуется использовать Gemini Flash Lite")

        if not suggestions:
            suggestions.append("Текущая конфигурация оптимальна по стоимости")

        return suggestions


# Глобальный экземпляр провайдера
_provider_instance: Optional[ResearchModelProvider] = None


def get_model_provider(
    settings: Optional[PsychologyResearchAgentSettings] = None
) -> ResearchModelProvider:
    """
    Получить глобальный экземпляр провайдера моделей.

    Args:
        settings: Настройки (опционально, для переинициализации)

    Returns:
        Экземпляр провайдера моделей
    """
    global _provider_instance

    if _provider_instance is None or settings is not None:
        _provider_instance = ResearchModelProvider(settings)

    return _provider_instance


def get_llm_model(
    task_type: str = "general",
    research_domain: str = "general",
    complexity: str = "standard"
) -> Any:
    """
    Быстрый доступ к модели для исследовательской задачи.

    Args:
        task_type: Тип задачи
        research_domain: Домен исследования
        complexity: Сложность

    Returns:
        Модель LLM
    """
    provider = get_model_provider()
    return provider.get_model_for_task(task_type, research_domain, complexity)


def get_default_model() -> Any:
    """Получить модель по умолчанию для агента."""
    return get_llm_model("general", "general", "standard")


# Экспорт
__all__ = [
    "ResearchModelProvider",
    "get_model_provider",
    "get_llm_model",
    "get_default_model"
]