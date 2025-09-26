"""
NLP Content Research Agent Providers

Cost-optimized провайдеры моделей для исследовательских задач.
Поддержка Qwen + Gemini для минимизации затрат.
"""

from typing import Dict, Any, Optional, Union, List
from enum import Enum
from dataclasses import dataclass

from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

from .settings import NLPContentResearchSettings


class TaskType(str, Enum):
    """Типы задач для выбора оптимальной модели."""
    RESEARCH = "research"                    # Веб-поиск, RAG, общий анализ
    DEEP_ANALYSIS = "deep_analysis"         # Сложный анализ, синтез данных
    CONTENT_CREATION = "content_creation"   # Создание контента, brief'ов
    QUICK_LOOKUP = "quick_lookup"          # Быстрые запросы, проверки
    VIRAL_ANALYSIS = "viral_analysis"      # Анализ вирусного потенциала
    COMPETITIVE_ANALYSIS = "competitive_analysis"  # Конкурентный анализ
    NLP_OPTIMIZATION = "nlp_optimization" # NLP оптимизация текста


class ModelProvider(str, Enum):
    """Поддерживаемые провайдеры."""
    QWEN = "qwen"
    GEMINI = "gemini"
    OPENAI = "openai"


@dataclass
class ModelConfig:
    """Конфигурация модели."""
    name: str
    provider: ModelProvider
    cost_per_1m_tokens: float
    max_tokens: int
    supports_batch: bool = False
    best_for: List[TaskType] = None

    def __post_init__(self):
        if self.best_for is None:
            self.best_for = []


class ModelManager:
    """Менеджер моделей с cost-optimization."""

    def __init__(self, settings: NLPContentResearchSettings):
        self.settings = settings
        self._models_registry = self._initialize_models_registry()
        self._providers_cache = {}

    def _initialize_models_registry(self) -> Dict[str, ModelConfig]:
        """Инициализация реестра доступных моделей."""
        return {
            # === QWEN MODELS (Alibaba) ===
            "qwen2.5-72b-instruct": ModelConfig(
                name="qwen2.5-72b-instruct",
                provider=ModelProvider.QWEN,
                cost_per_1m_tokens=2.00,  # Высокая стоимость, но максимальное качество
                max_tokens=32768,
                best_for=[TaskType.DEEP_ANALYSIS, TaskType.COMPETITIVE_ANALYSIS]
            ),
            "qwen2.5-coder-32b-instruct": ModelConfig(
                name="qwen2.5-coder-32b-instruct",
                provider=ModelProvider.QWEN,
                cost_per_1m_tokens=1.20,  # Средняя стоимость, хорошо для контента
                max_tokens=32768,
                best_for=[TaskType.CONTENT_CREATION, TaskType.NLP_OPTIMIZATION]
            ),
            "qwen2.5-coder-7b-instruct": ModelConfig(
                name="qwen2.5-coder-7b-instruct",
                provider=ModelProvider.QWEN,
                cost_per_1m_tokens=0.60,  # Бюджетная опция
                max_tokens=32768,
                best_for=[TaskType.QUICK_LOOKUP]
            ),

            # === GEMINI MODELS (Google) ===
            "gemini-2.0-flash-exp": ModelConfig(
                name="gemini-2.0-flash-exp",
                provider=ModelProvider.GEMINI,
                cost_per_1m_tokens=0.10,  # ОЧЕНЬ дешево!
                max_tokens=1000000,  # Огромный контекст
                supports_batch=True,
                best_for=[TaskType.RESEARCH, TaskType.VIRAL_ANALYSIS]
            ),
            "gemini-2.0-flash-thinking-exp": ModelConfig(
                name="gemini-2.0-flash-thinking-exp",
                provider=ModelProvider.GEMINI,
                cost_per_1m_tokens=0.15,  # Дешево + thinking
                max_tokens=32768,
                best_for=[TaskType.DEEP_ANALYSIS, TaskType.CONTENT_CREATION]
            ),

            # === FALLBACK MODELS ===
            "gpt-4o-mini": ModelConfig(
                name="gpt-4o-mini",
                provider=ModelProvider.OPENAI,
                cost_per_1m_tokens=0.40,
                max_tokens=128000,
                best_for=[TaskType.QUICK_LOOKUP, TaskType.NLP_OPTIMIZATION]
            )
        }

    def get_optimal_model_for_task(
        self,
        task_type: TaskType,
        budget_limit: Optional[float] = None,
        context_size_needed: int = 4000
    ) -> str:
        """
        Получить оптимальную модель для задачи с учетом стоимости.

        Args:
            task_type: Тип задачи
            budget_limit: Лимит стоимости за 1M токенов
            context_size_needed: Необходимый размер контекста

        Returns:
            Имя оптимальной модели
        """
        # Получаем подходящие модели
        suitable_models = [
            model for model in self._models_registry.values()
            if (task_type in model.best_for and
                model.max_tokens >= context_size_needed and
                (budget_limit is None or model.cost_per_1m_tokens <= budget_limit))
        ]

        if not suitable_models:
            # Fallback: ищем любую подходящую по контексту
            suitable_models = [
                model for model in self._models_registry.values()
                if model.max_tokens >= context_size_needed
            ]

        if not suitable_models:
            # Ultimate fallback
            return self.settings.llm_model

        # Сортируем по стоимости (дешевле = лучше)
        suitable_models.sort(key=lambda m: m.cost_per_1m_tokens)

        return suitable_models[0].name

    def get_model_instance(
        self,
        model_name: str,
        task_context: Optional[Dict[str, Any]] = None
    ) -> OpenAIModel:
        """
        Создать экземпляр модели.

        Args:
            model_name: Имя модели
            task_context: Контекст задачи для оптимизации

        Returns:
            Экземпляр модели
        """
        model_config = self._models_registry.get(model_name)

        if not model_config:
            # Fallback на основную модель
            return self._create_default_model()

        try:
            if model_config.provider == ModelProvider.GEMINI:
                return self._create_gemini_model(model_config, task_context)
            elif model_config.provider == ModelProvider.QWEN:
                return self._create_qwen_model(model_config, task_context)
            else:
                return self._create_openai_model(model_config, task_context)

        except Exception as e:
            print(f"⚠️ Ошибка создания модели {model_name}: {e}")
            return self._create_default_model()

    def _create_gemini_model(
        self,
        config: ModelConfig,
        context: Optional[Dict[str, Any]] = None
    ) -> OpenAIModel:
        """Создать Gemini модель."""
        if not hasattr(self.settings, 'gemini_api_key') or not self.settings.gemini_api_key:
            raise ValueError("Gemini API ключ не настроен")

        provider_key = f"gemini_{config.name}"
        if provider_key not in self._providers_cache:
            self._providers_cache[provider_key] = GeminiProvider(
                api_key=self.settings.gemini_api_key
            )

        return OpenAIModel(
            config.name,
            provider=self._providers_cache[provider_key]
        )

    def _create_qwen_model(
        self,
        config: ModelConfig,
        context: Optional[Dict[str, Any]] = None
    ) -> OpenAIModel:
        """Создать Qwen модель через OpenAI-совместимый API."""
        provider_key = f"qwen_{config.name}"
        if provider_key not in self._providers_cache:
            self._providers_cache[provider_key] = OpenAIProvider(
                base_url=self.settings.llm_base_url,
                api_key=self.settings.llm_api_key
            )

        return OpenAIModel(
            config.name,
            provider=self._providers_cache[provider_key]
        )

    def _create_openai_model(
        self,
        config: ModelConfig,
        context: Optional[Dict[str, Any]] = None
    ) -> OpenAIModel:
        """Создать OpenAI модель."""
        provider_key = f"openai_{config.name}"
        if provider_key not in self._providers_cache:
            self._providers_cache[provider_key] = OpenAIProvider(
                api_key=self.settings.llm_api_key  # Предполагаем совместимость
            )

        return OpenAIModel(
            config.name,
            provider=self._providers_cache[provider_key]
        )

    def _create_default_model(self) -> OpenAIModel:
        """Создать модель по умолчанию."""
        if "default" not in self._providers_cache:
            self._providers_cache["default"] = OpenAIProvider(
                base_url=self.settings.llm_base_url,
                api_key=self.settings.llm_api_key
            )

        return OpenAIModel(
            self.settings.llm_model,
            provider=self._providers_cache["default"]
        )

    def get_cost_estimate(
        self,
        model_name: str,
        estimated_tokens: int
    ) -> Dict[str, Any]:
        """
        Получить оценку стоимости запроса.

        Args:
            model_name: Имя модели
            estimated_tokens: Оценочное количество токенов

        Returns:
            Информация о стоимости
        """
        model_config = self._models_registry.get(model_name)

        if not model_config:
            return {"error": "Модель не найдена"}

        cost_estimate = (estimated_tokens / 1_000_000) * model_config.cost_per_1m_tokens

        return {
            "model": model_name,
            "provider": model_config.provider.value,
            "estimated_tokens": estimated_tokens,
            "cost_per_1m_tokens": model_config.cost_per_1m_tokens,
            "estimated_cost_usd": round(cost_estimate, 4),
            "supports_batch": model_config.supports_batch,
            "max_tokens": model_config.max_tokens
        }

    def get_batch_processing_model(
        self,
        batch_size: int,
        task_complexity: str = "standard"
    ) -> OpenAIModel:
        """
        Получить модель для пакетной обработки.

        Args:
            batch_size: Размер пакета
            task_complexity: Сложность задач

        Returns:
            Оптимальная модель для пакетной обработки
        """
        # Для больших пакетов предпочитаем дешевые модели
        if batch_size > 10:
            # Gemini 2.0 Flash очень дешевый для больших объемов
            if hasattr(self.settings, 'gemini_api_key') and self.settings.gemini_api_key:
                return self.get_model_instance("gemini-2.0-flash-exp")

        # Для средних пакетов используем баланс цены и качества
        if task_complexity == "complex":
            return self.get_model_instance("qwen2.5-72b-instruct")
        elif task_complexity == "standard":
            return self.get_model_instance("qwen2.5-coder-32b-instruct")
        else:
            return self.get_model_instance("qwen2.5-coder-7b-instruct")

    def optimize_model_selection(
        self,
        research_context: Dict[str, Any]
    ) -> str:
        """
        Оптимальный выбор модели на основе контекста исследования.

        Args:
            research_context: Контекст исследования

        Returns:
            Имя оптимальной модели
        """
        domain = research_context.get("domain", "general")
        complexity = research_context.get("research_depth", "standard")
        audience = research_context.get("target_audience", "general")
        enable_viral_analysis = research_context.get("enable_viral_analysis", False)

        # Логика выбора модели
        if complexity == "exhaustive" or domain == "psychology":
            # Сложные исследования требуют лучшие модели
            return self.get_optimal_model_for_task(TaskType.DEEP_ANALYSIS)

        elif enable_viral_analysis:
            # Для вирусного анализа отлично подходит дешевый Gemini
            return self.get_optimal_model_for_task(TaskType.VIRAL_ANALYSIS)

        elif complexity == "quick":
            # Быстрые задачи - дешевые модели
            return self.get_optimal_model_for_task(TaskType.QUICK_LOOKUP)

        else:
            # Стандартные исследования - баланс цены и качества
            return self.get_optimal_model_for_task(TaskType.RESEARCH)


# === ФАБРИЧНЫЕ ФУНКЦИИ ===

def get_model_manager(settings: Optional[NLPContentResearchSettings] = None) -> ModelManager:
    """Получить менеджер моделей."""
    if settings is None:
        from .settings import load_settings
        settings = load_settings()

    return ModelManager(settings)


def get_research_model(
    task_type: str = "research",
    settings: Optional[NLPContentResearchSettings] = None
) -> OpenAIModel:
    """
    Получить модель для исследовательской задачи.

    Args:
        task_type: Тип исследовательской задачи
        settings: Настройки агента

    Returns:
        Экземпляр модели
    """
    manager = get_model_manager(settings)

    try:
        task_enum = TaskType(task_type)
        model_name = manager.get_optimal_model_for_task(task_enum)
        return manager.get_model_instance(model_name)
    except ValueError:
        # Неизвестный тип задачи - используем research по умолчанию
        return manager.get_model_instance(manager.get_optimal_model_for_task(TaskType.RESEARCH))


def get_cost_optimized_model(
    estimated_tokens: int = 4000,
    max_budget_per_1m: float = 1.0,
    settings: Optional[NLPContentResearchSettings] = None
) -> OpenAIModel:
    """
    Получить самую дешевую подходящую модель.

    Args:
        estimated_tokens: Ожидаемое количество токенов
        max_budget_per_1m: Максимальный бюджет за 1M токенов
        settings: Настройки агента

    Returns:
        Cost-optimized модель
    """
    manager = get_model_manager(settings)

    # Ищем самую дешевую модель в рамках бюджета
    model_name = manager.get_optimal_model_for_task(
        TaskType.RESEARCH,
        budget_limit=max_budget_per_1m,
        context_size_needed=estimated_tokens
    )

    return manager.get_model_instance(model_name)


# === ИНФОРМАЦИОННЫЕ ФУНКЦИИ ===

def get_available_models() -> Dict[str, Dict[str, Any]]:
    """Получить список доступных моделей."""
    from .settings import load_settings
    settings = load_settings()
    manager = ModelManager(settings)

    return {
        name: {
            "provider": config.provider.value,
            "cost_per_1m_tokens": config.cost_per_1m_tokens,
            "max_tokens": config.max_tokens,
            "supports_batch": config.supports_batch,
            "best_for": [task.value for task in config.best_for]
        }
        for name, config in manager._models_registry.items()
    }


def estimate_research_cost(
    research_type: str,
    estimated_complexity: str = "medium"
) -> Dict[str, Any]:
    """
    Оценить стоимость исследования.

    Args:
        research_type: Тип исследования
        estimated_complexity: Оценочная сложность

    Returns:
        Оценка стоимости
    """
    token_estimates = {
        "quick": 2000,
        "standard": 8000,
        "comprehensive": 20000,
        "exhaustive": 50000
    }

    complexity_multipliers = {
        "simple": 0.7,
        "medium": 1.0,
        "complex": 1.5,
        "very_complex": 2.0
    }

    base_tokens = token_estimates.get(research_type, 8000)
    multiplier = complexity_multipliers.get(estimated_complexity, 1.0)
    total_tokens = int(base_tokens * multiplier)

    manager = get_model_manager()

    # Получаем оценки для разных моделей
    models_to_check = ["gemini-2.0-flash-exp", "qwen2.5-coder-32b-instruct", "qwen2.5-72b-instruct"]

    estimates = {}
    for model_name in models_to_check:
        estimates[model_name] = manager.get_cost_estimate(model_name, total_tokens)

    return {
        "research_type": research_type,
        "estimated_complexity": estimated_complexity,
        "estimated_tokens": total_tokens,
        "model_estimates": estimates,
        "recommended_model": min(estimates.items(), key=lambda x: x[1].get("estimated_cost_usd", float('inf')))[0]
    }


__all__ = [
    "ModelManager",
    "TaskType",
    "ModelProvider",
    "get_model_manager",
    "get_research_model",
    "get_cost_optimized_model",
    "get_available_models",
    "estimate_research_cost"
]