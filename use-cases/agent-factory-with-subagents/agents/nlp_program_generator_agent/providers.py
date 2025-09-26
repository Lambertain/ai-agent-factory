"""
NLP Program Generator Agent Providers

Cost-optimized провайдеры моделей для создания программ трансформации.
Поддержка Qwen + Gemini для минимизации затрат при максимальной эффективности.
"""

from typing import Dict, Any, Optional, Union, List
from enum import Enum
from dataclasses import dataclass

from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

from .settings import NLPProgramGeneratorSettings


class TaskType(str, Enum):
    """Типы задач для выбора оптимальной модели."""
    PROGRAM_GENERATION = "program_generation"      # Создание структуры программы
    NLP_TECHNIQUES = "nlp_techniques"             # Разработка NLP техник
    HYPNOTIC_PATTERNS = "hypnotic_patterns"      # Эриксоновские паттерны
    PERSONALIZATION = "personalization"          # VAK адаптация
    CONTENT_VALIDATION = "content_validation"    # Проверка контента
    QUICK_TASKS = "quick_tasks"                  # Быстрые задачи
    RESEARCH = "research"                        # Исследовательские задачи


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
    context_window: int = 32000

    def __post_init__(self):
        if self.best_for is None:
            self.best_for = []


class ModelManager:
    """Менеджер моделей с оптимизацией затрат."""

    def __init__(self, settings: NLPProgramGeneratorSettings):
        self.settings = settings
        self.models = self._initialize_models()
        self.cost_tracker = {}

    def _initialize_models(self) -> Dict[str, ModelConfig]:
        """Инициализация доступных моделей."""
        return {
            # Premium Qwen для сложных техник
            "qwen2.5-72b-instruct": ModelConfig(
                name="qwen2.5-72b-instruct",
                provider=ModelProvider.QWEN,
                cost_per_1m_tokens=2.0,
                max_tokens=8000,
                context_window=32768,
                best_for=[TaskType.NLP_TECHNIQUES, TaskType.HYPNOTIC_PATTERNS]
            ),

            # Balanced Qwen для программ
            "qwen2.5-coder-32b-instruct": ModelConfig(
                name="qwen2.5-coder-32b-instruct",
                provider=ModelProvider.QWEN,
                cost_per_1m_tokens=1.0,
                max_tokens=8000,
                context_window=32768,
                best_for=[TaskType.PROGRAM_GENERATION, TaskType.RESEARCH]
            ),

            # Economical Qwen для простых задач
            "qwen2.5-coder-7b-instruct": ModelConfig(
                name="qwen2.5-coder-7b-instruct",
                provider=ModelProvider.QWEN,
                cost_per_1m_tokens=0.3,
                max_tokens=4000,
                context_window=32768,
                best_for=[TaskType.CONTENT_VALIDATION, TaskType.QUICK_TASKS]
            ),

            # Ultra-cheap Gemini для персонализации
            "gemini-2.5-flash-lite": ModelConfig(
                name="gemini-2.5-flash-lite",
                provider=ModelProvider.GEMINI,
                cost_per_1m_tokens=0.10,
                max_tokens=4000,
                supports_batch=True,
                context_window=32768,
                best_for=[TaskType.PERSONALIZATION, TaskType.QUICK_TASKS]
            )
        }

    def get_optimal_model_for_task(
        self,
        task_type: TaskType,
        context_size: int = 0,
        quality_priority: bool = False
    ) -> OpenAIModel:
        """Получить оптимальную модель для типа задачи."""

        # Выбор модели по типу задачи
        if quality_priority:
            # Для критически важных задач - лучшая модель
            model_name = "qwen2.5-72b-instruct"
        else:
            model_preferences = {
                TaskType.PROGRAM_GENERATION: "qwen2.5-coder-32b-instruct",
                TaskType.NLP_TECHNIQUES: "qwen2.5-72b-instruct",
                TaskType.HYPNOTIC_PATTERNS: "qwen2.5-72b-instruct",
                TaskType.PERSONALIZATION: "gemini-2.5-flash-lite",
                TaskType.CONTENT_VALIDATION: "gemini-2.5-flash-lite",
                TaskType.QUICK_TASKS: "gemini-2.5-flash-lite",
                TaskType.RESEARCH: "qwen2.5-coder-32b-instruct"
            }
            model_name = model_preferences.get(task_type, "qwen2.5-coder-32b-instruct")

        # Проверка доступности модели
        model_config = self.models.get(model_name)
        if not model_config:
            model_name = "qwen2.5-coder-32b-instruct"  # Fallback
            model_config = self.models[model_name]

        # Проверка размера контекста
        if context_size > model_config.context_window:
            # Нужна модель с большим контекстом
            large_context_models = [
                "qwen2.5-72b-instruct",
                "qwen2.5-coder-32b-instruct"
            ]
            model_name = large_context_models[0]
            model_config = self.models[model_name]

        return self._create_model_instance(model_name, model_config)

    def _create_model_instance(self, model_name: str, config: ModelConfig) -> OpenAIModel:
        """Создать экземпляр модели."""
        api_key = self.settings.get_api_key_for_model(model_name)

        if config.provider == ModelProvider.GEMINI:
            # Gemini через OpenAI-compatible API (если поддерживается)
            provider = OpenAIProvider(
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                api_key=api_key
            )
        else:
            # Qwen и другие через основной endpoint
            provider = OpenAIProvider(
                base_url=self.settings.llm_base_url,
                api_key=api_key
            )

        return OpenAIModel(model_name, provider=provider)

    def estimate_cost(
        self,
        task_type: TaskType,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Оценить стоимость задачи."""
        model_name = self.get_model_name_for_task(task_type)
        model_config = self.models[model_name]

        total_tokens = input_tokens + output_tokens
        cost = (total_tokens / 1_000_000) * model_config.cost_per_1m_tokens

        # Учет batch скидки для Gemini
        if model_config.provider == ModelProvider.GEMINI and model_config.supports_batch:
            if self.settings.gemini_use_batch_api:
                cost *= 0.5  # 50% скидка за batch

        return cost

    def get_model_name_for_task(self, task_type: TaskType) -> str:
        """Получить имя модели для типа задачи."""
        return self.settings.get_model_for_task(task_type.value)

    def track_usage(self, task_type: TaskType, tokens_used: int, cost: float):
        """Отследить использование модели."""
        if task_type.value not in self.cost_tracker:
            self.cost_tracker[task_type.value] = {
                "total_tokens": 0,
                "total_cost": 0.0,
                "request_count": 0
            }

        tracker = self.cost_tracker[task_type.value]
        tracker["total_tokens"] += tokens_used
        tracker["total_cost"] += cost
        tracker["request_count"] += 1

    def get_usage_stats(self) -> Dict[str, Any]:
        """Получить статистику использования."""
        total_cost = sum(
            tracker["total_cost"]
            for tracker in self.cost_tracker.values()
        )
        total_tokens = sum(
            tracker["total_tokens"]
            for tracker in self.cost_tracker.values()
        )

        return {
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "by_task": self.cost_tracker.copy(),
            "average_cost_per_request": total_cost / max(sum(
                tracker["request_count"]
                for tracker in self.cost_tracker.values()
            ), 1)
        }

    def get_recommended_model_for_complexity(
        self,
        program_complexity: str,
        domain: str = "psychology"
    ) -> str:
        """Получить рекомендуемую модель по сложности программы."""
        complexity_mapping = {
            "simple": "gemini-2.5-flash-lite",      # Простые программы
            "medium": "qwen2.5-coder-32b-instruct", # Стандартные программы
            "complex": "qwen2.5-72b-instruct"       # Сложные программы
        }

        # Специфика домена
        if domain in ["astrology", "tarot"]:
            # Символические системы требуют более мощных моделей
            complexity_mapping["simple"] = "qwen2.5-coder-32b-instruct"
            complexity_mapping["medium"] = "qwen2.5-72b-instruct"

        return complexity_mapping.get(program_complexity, "qwen2.5-coder-32b-instruct")

    def optimize_batch_requests(
        self,
        requests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Оптимизировать пакетные запросы для экономии."""
        if not self.settings.enable_smart_routing:
            return requests

        # Группировка по типам задач
        grouped_requests = {}
        for req in requests:
            task_type = req.get("task_type", TaskType.QUICK_TASKS)
            if task_type not in grouped_requests:
                grouped_requests[task_type] = []
            grouped_requests[task_type].append(req)

        optimized_requests = []

        # Оптимизация для каждой группы
        for task_type, group_requests in grouped_requests.items():
            if len(group_requests) > 1:
                # Можно объединить похожие запросы
                if task_type == TaskType.PERSONALIZATION:
                    # VAK адаптации можно делать батчами
                    combined_request = self._combine_personalization_requests(group_requests)
                    if combined_request:
                        optimized_requests.append(combined_request)
                        continue

            optimized_requests.extend(group_requests)

        return optimized_requests

    def _combine_personalization_requests(
        self,
        requests: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Объединить запросы персонализации в один."""
        if len(requests) < 2:
            return None

        # Объединяем VAK адаптации
        combined_content = []
        vak_types = []

        for req in requests:
            combined_content.append(req.get("content", ""))
            vak_types.append(req.get("vak_type", "mixed"))

        return {
            "task_type": TaskType.PERSONALIZATION,
            "content": "\n---\n".join(combined_content),
            "vak_types": vak_types,
            "combined": True,
            "original_count": len(requests)
        }

    def get_cost_report(self, period: str = "total") -> Dict[str, Any]:
        """Получить отчет о затратах."""
        stats = self.get_usage_stats()

        # Анализ эффективности
        efficiency_score = 0
        if stats["total_tokens"] > 0:
            cost_per_token = stats["total_cost"] / stats["total_tokens"]
            # Нормализация: чем меньше cost_per_token, тем выше эффективность
            efficiency_score = max(0, min(100, (0.002 - cost_per_token) * 50000))

        # Рекомендации по оптимизации
        recommendations = []
        if stats["total_cost"] > 10.0:  # Если затраты высокие
            recommendations.append("Рассмотреть использование более экономичных моделей для простых задач")
        if not self.settings.enable_smart_routing:
            recommendations.append("Включить умную маршрутизацию для оптимизации")
        if not self.settings.gemini_use_batch_api:
            recommendations.append("Включить Batch API для Gemini для получения скидок")

        return {
            "period": period,
            "usage_stats": stats,
            "efficiency_score": round(efficiency_score, 2),
            "recommendations": recommendations,
            "model_distribution": self._get_model_distribution()
        }

    def _get_model_distribution(self) -> Dict[str, int]:
        """Получить распределение использования моделей."""
        distribution = {}
        for task_type, stats in self.cost_tracker.items():
            model_name = self.get_model_name_for_task(TaskType(task_type))
            if model_name not in distribution:
                distribution[model_name] = 0
            distribution[model_name] += stats["request_count"]
        return distribution


# === ФАБРИЧНЫЕ ФУНКЦИИ ===

def create_model_manager(settings: NLPProgramGeneratorSettings) -> ModelManager:
    """Создать менеджер моделей."""
    return ModelManager(settings)


def get_model_for_program_generation(settings: NLPProgramGeneratorSettings) -> OpenAIModel:
    """Получить модель для генерации программ."""
    manager = create_model_manager(settings)
    return manager.get_optimal_model_for_task(TaskType.PROGRAM_GENERATION)


def get_model_for_nlp_techniques(settings: NLPProgramGeneratorSettings) -> OpenAIModel:
    """Получить модель для создания NLP техник."""
    manager = create_model_manager(settings)
    return manager.get_optimal_model_for_task(
        TaskType.NLP_TECHNIQUES,
        quality_priority=True
    )


def get_model_for_personalization(settings: NLPProgramGeneratorSettings) -> OpenAIModel:
    """Получить модель для персонализации контента."""
    manager = create_model_manager(settings)
    return manager.get_optimal_model_for_task(TaskType.PERSONALIZATION)