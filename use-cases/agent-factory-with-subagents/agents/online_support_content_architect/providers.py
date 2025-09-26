"""
Psychology Content Architect Agent - Model Providers

Интеллектуальная система выбора и управления LLM моделями
с оптимизацией стоимости для задач архитектуры психологических программ.
"""

from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime, timedelta

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.gemini import GeminiProvider

from .settings import load_settings


class TaskType(str, Enum):
    """Типы задач для оптимального выбора модели."""
    ARCHITECTURE_DESIGN = "architecture_design"  # Сложное архитектурное планирование
    STRUCTURE_ANALYSIS = "structure_analysis"    # Анализ структуры программ
    MODULE_PLANNING = "module_planning"          # Планирование модулей
    CONTENT_ORGANIZATION = "content_organization" # Организация контента
    DOCUMENTATION = "documentation"              # Документация
    VALIDATION = "validation"                    # Валидация архитектуры
    SIMPLE_QUERIES = "simple_queries"           # Простые запросы


class ModelCapability(str, Enum):
    """Возможности моделей."""
    COMPLEX_REASONING = "complex_reasoning"
    STRUCTURED_OUTPUT = "structured_output"
    CREATIVE_DESIGN = "creative_design"
    FAST_RESPONSE = "fast_response"
    COST_EFFECTIVE = "cost_effective"
    LARGE_CONTEXT = "large_context"


@dataclass
class ModelSpecs:
    """Спецификации модели."""
    name: str
    provider: str
    cost_per_1k_tokens: float
    context_window: int
    capabilities: List[ModelCapability]
    performance_score: float
    recommended_for: List[TaskType]


@dataclass
class TaskRequirements:
    """Требования к задаче."""
    complexity: str  # low, medium, high, expert
    context_size: int
    creativity_required: bool
    speed_priority: bool
    cost_priority: bool
    accuracy_priority: bool


class ArchitectModelProvider:
    """Провайдер моделей для Psychology Content Architect Agent."""

    def __init__(self):
        self.settings = load_settings()
        self._models_cache: Dict[str, Any] = {}
        self._performance_stats: Dict[str, Dict] = {}
        self._initialize_model_specs()

    def _initialize_model_specs(self):
        """Инициализация спецификаций моделей."""
        self.model_specs = {
            # Премиальные модели для сложного архитектурного анализа
            "qwen2.5-72b-instruct": ModelSpecs(
                name="qwen2.5-72b-instruct",
                provider="openai",
                cost_per_1k_tokens=2.0,  # Примерная стоимость
                context_window=32768,
                capabilities=[
                    ModelCapability.COMPLEX_REASONING,
                    ModelCapability.STRUCTURED_OUTPUT,
                    ModelCapability.CREATIVE_DESIGN,
                    ModelCapability.LARGE_CONTEXT
                ],
                performance_score=0.95,
                recommended_for=[TaskType.ARCHITECTURE_DESIGN, TaskType.STRUCTURE_ANALYSIS]
            ),

            # Средние модели для кодирования и структурирования
            "qwen2.5-coder-32b-instruct": ModelSpecs(
                name="qwen2.5-coder-32b-instruct",
                provider="openai",
                cost_per_1k_tokens=1.0,
                context_window=32768,
                capabilities=[
                    ModelCapability.STRUCTURED_OUTPUT,
                    ModelCapability.COMPLEX_REASONING,
                    ModelCapability.LARGE_CONTEXT
                ],
                performance_score=0.88,
                recommended_for=[TaskType.MODULE_PLANNING, TaskType.CONTENT_ORGANIZATION]
            ),

            # Экономичные модели для планирования и документации
            "gemini-2.5-flash-lite": ModelSpecs(
                name="gemini-2.5-flash-lite",
                provider="gemini",
                cost_per_1k_tokens=0.1,  # Очень дешевая
                context_window=32768,
                capabilities=[
                    ModelCapability.FAST_RESPONSE,
                    ModelCapability.COST_EFFECTIVE,
                    ModelCapability.STRUCTURED_OUTPUT
                ],
                performance_score=0.78,
                recommended_for=[TaskType.DOCUMENTATION, TaskType.VALIDATION, TaskType.SIMPLE_QUERIES]
            ),

            # Альтернативные модели
            "qwen2.5-coder-7b-instruct": ModelSpecs(
                name="qwen2.5-coder-7b-instruct",
                provider="openai",
                cost_per_1k_tokens=0.3,
                context_window=32768,
                capabilities=[
                    ModelCapability.FAST_RESPONSE,
                    ModelCapability.COST_EFFECTIVE,
                    ModelCapability.STRUCTURED_OUTPUT
                ],
                performance_score=0.75,
                recommended_for=[TaskType.SIMPLE_QUERIES, TaskType.VALIDATION]
            )
        }

    def select_optimal_model(
        self,
        task_type: TaskType,
        requirements: Optional[TaskRequirements] = None
    ) -> Tuple[str, float]:
        """
        Выбрать оптимальную модель для задачи.

        Returns:
            Tuple[model_name, estimated_cost]
        """
        if requirements is None:
            requirements = self._get_default_requirements(task_type)

        # Фильтрация подходящих моделей
        suitable_models = []
        for model_name, specs in self.model_specs.items():
            if self._is_model_suitable(specs, task_type, requirements):
                suitability_score = self._calculate_suitability_score(specs, requirements)
                suitable_models.append((model_name, specs, suitability_score))

        if not suitable_models:
            # Fallback на базовую модель
            return self.settings.llm_model, 1.0

        # Сортировка по пригодности
        suitable_models.sort(key=lambda x: x[2], reverse=True)
        best_model_name = suitable_models[0][0]
        estimated_cost = self._estimate_cost(suitable_models[0][1], requirements)

        return best_model_name, estimated_cost

    def _get_default_requirements(self, task_type: TaskType) -> TaskRequirements:
        """Получить требования по умолчанию для типа задачи."""
        defaults = {
            TaskType.ARCHITECTURE_DESIGN: TaskRequirements(
                complexity="high",
                context_size=8000,
                creativity_required=True,
                speed_priority=False,
                cost_priority=False,
                accuracy_priority=True
            ),
            TaskType.STRUCTURE_ANALYSIS: TaskRequirements(
                complexity="medium",
                context_size=6000,
                creativity_required=True,
                speed_priority=False,
                cost_priority=False,
                accuracy_priority=True
            ),
            TaskType.MODULE_PLANNING: TaskRequirements(
                complexity="medium",
                context_size=4000,
                creativity_required=False,
                speed_priority=False,
                cost_priority=True,
                accuracy_priority=True
            ),
            TaskType.CONTENT_ORGANIZATION: TaskRequirements(
                complexity="medium",
                context_size=4000,
                creativity_required=False,
                speed_priority=True,
                cost_priority=True,
                accuracy_priority=False
            ),
            TaskType.DOCUMENTATION: TaskRequirements(
                complexity="low",
                context_size=2000,
                creativity_required=False,
                speed_priority=True,
                cost_priority=True,
                accuracy_priority=False
            ),
            TaskType.VALIDATION: TaskRequirements(
                complexity="low",
                context_size=3000,
                creativity_required=False,
                speed_priority=True,
                cost_priority=True,
                accuracy_priority=True
            ),
            TaskType.SIMPLE_QUERIES: TaskRequirements(
                complexity="low",
                context_size=1000,
                creativity_required=False,
                speed_priority=True,
                cost_priority=True,
                accuracy_priority=False
            )
        }
        return defaults.get(task_type, defaults[TaskType.SIMPLE_QUERIES])

    def _is_model_suitable(
        self,
        specs: ModelSpecs,
        task_type: TaskType,
        requirements: TaskRequirements
    ) -> bool:
        """Проверить подходит ли модель для задачи."""
        # Проверка по типу задачи
        if task_type not in specs.recommended_for:
            # Проверяем совместимость capabilities
            required_capabilities = self._get_required_capabilities(task_type, requirements)
            if not any(cap in specs.capabilities for cap in required_capabilities):
                return False

        # Проверка context window
        if specs.context_window < requirements.context_size:
            return False

        # Проверка сложности
        if requirements.complexity == "expert" and specs.performance_score < 0.9:
            return False

        return True

    def _get_required_capabilities(
        self,
        task_type: TaskType,
        requirements: TaskRequirements
    ) -> List[ModelCapability]:
        """Получить необходимые capabilities для задачи."""
        capabilities = []

        if requirements.complexity in ["high", "expert"]:
            capabilities.append(ModelCapability.COMPLEX_REASONING)

        if requirements.creativity_required:
            capabilities.append(ModelCapability.CREATIVE_DESIGN)

        if requirements.speed_priority:
            capabilities.append(ModelCapability.FAST_RESPONSE)

        if requirements.cost_priority:
            capabilities.append(ModelCapability.COST_EFFECTIVE)

        if requirements.context_size > 16000:
            capabilities.append(ModelCapability.LARGE_CONTEXT)

        # По умолчанию требуем структурированный вывод
        capabilities.append(ModelCapability.STRUCTURED_OUTPUT)

        return capabilities

    def _calculate_suitability_score(
        self,
        specs: ModelSpecs,
        requirements: TaskRequirements
    ) -> float:
        """Рассчитать оценку пригодности модели."""
        score = 0.0

        # Базовая оценка производительности (40%)
        score += specs.performance_score * 0.4

        # Соответствие capabilities (30%)
        required_caps = self._get_required_capabilities(
            TaskType.ARCHITECTURE_DESIGN,  # Placeholder
            requirements
        )
        matching_caps = len(set(required_caps) & set(specs.capabilities))
        total_caps = len(required_caps)
        if total_caps > 0:
            score += (matching_caps / total_caps) * 0.3

        # Стоимость (20%)
        if requirements.cost_priority:
            # Чем дешевле, тем лучше
            cost_score = max(0, 1 - (specs.cost_per_1k_tokens / 3.0))
            score += cost_score * 0.2
        else:
            score += 0.1  # Neutral score if cost is not priority

        # Скорость (10%)
        if requirements.speed_priority:
            if ModelCapability.FAST_RESPONSE in specs.capabilities:
                score += 0.1

        return min(score, 1.0)

    def _estimate_cost(self, specs: ModelSpecs, requirements: TaskRequirements) -> float:
        """Оценить стоимость выполнения задачи."""
        # Примерная оценка количества токенов
        estimated_tokens = requirements.context_size + 1000  # input + output
        return (estimated_tokens / 1000) * specs.cost_per_1k_tokens

    def get_model_for_task(self, task_type: TaskType) -> Any:
        """Получить модель для конкретного типа задачи."""
        model_name, _ = self.select_optimal_model(task_type)

        if model_name in self._models_cache:
            return self._models_cache[model_name]

        # Создаем модель
        specs = self.model_specs.get(model_name)
        if not specs:
            # Fallback
            return self._create_default_model()

        model = self._create_model(model_name, specs)
        self._models_cache[model_name] = model
        return model

    def _create_model(self, model_name: str, specs: ModelSpecs) -> Any:
        """Создать модель по спецификации."""
        if specs.provider == "openai":
            provider = OpenAIProvider(
                base_url=self.settings.llm_base_url,
                api_key=self.settings.llm_api_key
            )
            return OpenAIModel(model_name, provider=provider)

        elif specs.provider == "gemini":
            provider = GeminiProvider(api_key=self.settings.gemini_api_key)
            return GeminiModel(model_name, provider=provider)

        else:
            return self._create_default_model()

    def _create_default_model(self) -> Any:
        """Создать модель по умолчанию."""
        provider = OpenAIProvider(
            base_url=self.settings.llm_base_url,
            api_key=self.settings.llm_api_key
        )
        return OpenAIModel(self.settings.llm_model, provider=provider)

    async def get_cost_estimate(
        self,
        task_type: TaskType,
        estimated_context_size: int = 4000
    ) -> Dict[str, Any]:
        """Получить оценку стоимости для задачи."""
        requirements = TaskRequirements(
            complexity="medium",
            context_size=estimated_context_size,
            creativity_required=False,
            speed_priority=False,
            cost_priority=False,
            accuracy_priority=True
        )

        model_name, estimated_cost = self.select_optimal_model(task_type, requirements)
        specs = self.model_specs.get(model_name)

        return {
            "task_type": task_type,
            "recommended_model": model_name,
            "estimated_cost_usd": estimated_cost,
            "context_size": estimated_context_size,
            "model_specs": {
                "provider": specs.provider if specs else "unknown",
                "performance_score": specs.performance_score if specs else 0.0,
                "cost_per_1k_tokens": specs.cost_per_1k_tokens if specs else 1.0
            }
        }

    def get_performance_stats(self) -> Dict[str, Any]:
        """Получить статистику производительности моделей."""
        return {
            "models_available": len(self.model_specs),
            "models_cached": len(self._models_cache),
            "performance_data": self._performance_stats,
            "cost_optimization_enabled": self.settings.enable_smart_routing
        }

    def update_performance_stats(
        self,
        model_name: str,
        task_type: TaskType,
        execution_time: float,
        success: bool,
        cost: float
    ):
        """Обновить статистику производительности."""
        if model_name not in self._performance_stats:
            self._performance_stats[model_name] = {
                "total_requests": 0,
                "successful_requests": 0,
                "total_time": 0.0,
                "total_cost": 0.0,
                "task_performance": {}
            }

        stats = self._performance_stats[model_name]
        stats["total_requests"] += 1
        stats["total_time"] += execution_time
        stats["total_cost"] += cost

        if success:
            stats["successful_requests"] += 1

        # Статистика по типам задач
        task_key = task_type.value
        if task_key not in stats["task_performance"]:
            stats["task_performance"][task_key] = {
                "count": 0,
                "avg_time": 0.0,
                "success_rate": 0.0
            }

        task_stats = stats["task_performance"][task_key]
        task_stats["count"] += 1
        task_stats["avg_time"] = (task_stats["avg_time"] * (task_stats["count"] - 1) + execution_time) / task_stats["count"]
        task_stats["success_rate"] = (task_stats["success_rate"] * (task_stats["count"] - 1) + (1 if success else 0)) / task_stats["count"]


# ===== УДОБНЫЕ ФУНКЦИИ =====

def get_model_provider() -> ArchitectModelProvider:
    """Получить провайдер моделей."""
    return ArchitectModelProvider()


def get_architecture_model() -> Any:
    """Получить модель для архитектурных задач."""
    provider = get_model_provider()
    return provider.get_model_for_task(TaskType.ARCHITECTURE_DESIGN)


def get_planning_model() -> Any:
    """Получить модель для планирования."""
    provider = get_model_provider()
    return provider.get_model_for_task(TaskType.MODULE_PLANNING)


def get_documentation_model() -> Any:
    """Получить модель для документации."""
    provider = get_model_provider()
    return provider.get_model_for_task(TaskType.DOCUMENTATION)


def get_default_model() -> Any:
    """Получить модель по умолчанию."""
    provider = get_model_provider()
    return provider._create_default_model()


async def estimate_task_cost(
    task_type: TaskType,
    context_size: int = 4000
) -> Dict[str, Any]:
    """Оценить стоимость выполнения задачи."""
    provider = get_model_provider()
    return await provider.get_cost_estimate(task_type, context_size)


# ===== СПЕЦИАЛИЗИРОВАННЫЕ ПРОВАЙДЕРЫ =====

class ArchitectureModelRouter:
    """Маршрутизатор моделей для архитектурных задач."""

    def __init__(self):
        self.provider = get_model_provider()

    def route_task(self, task_description: str, complexity_hint: str = "medium") -> Any:
        """Маршрутизировать задачу к подходящей модели."""
        # Простая эвристика определения типа задачи
        task_type = self._classify_task(task_description)

        # Настройка требований на основе подсказки сложности
        requirements = self.provider._get_default_requirements(task_type)
        requirements.complexity = complexity_hint

        model_name, _ = self.provider.select_optimal_model(task_type, requirements)
        return self.provider._models_cache.get(model_name) or self.provider._create_model(
            model_name,
            self.provider.model_specs[model_name]
        )

    def _classify_task(self, description: str) -> TaskType:
        """Классифицировать задачу по описанию."""
        description_lower = description.lower()

        if any(word in description_lower for word in ["архитектура", "дизайн", "проект", "структура программы"]):
            return TaskType.ARCHITECTURE_DESIGN
        elif any(word in description_lower for word in ["анализ", "структура", "компоненты"]):
            return TaskType.STRUCTURE_ANALYSIS
        elif any(word in description_lower for word in ["модуль", "план", "этап"]):
            return TaskType.MODULE_PLANNING
        elif any(word in description_lower for word in ["организация", "контент", "материалы"]):
            return TaskType.CONTENT_ORGANIZATION
        elif any(word in description_lower for word in ["документация", "описание", "руководство"]):
            return TaskType.DOCUMENTATION
        elif any(word in description_lower for word in ["проверка", "валидация", "оценка"]):
            return TaskType.VALIDATION
        else:
            return TaskType.SIMPLE_QUERIES


def get_smart_model_router() -> ArchitectureModelRouter:
    """Получить умный маршрутизатор моделей."""
    return ArchitectureModelRouter()


# ===== ЭКСПОРТ =====
__all__ = [
    "ArchitectModelProvider",
    "TaskType",
    "ModelCapability",
    "TaskRequirements",
    "ArchitectureModelRouter",
    "get_model_provider",
    "get_architecture_model",
    "get_planning_model",
    "get_documentation_model",
    "get_default_model",
    "get_smart_model_router",
    "estimate_task_cost"
]