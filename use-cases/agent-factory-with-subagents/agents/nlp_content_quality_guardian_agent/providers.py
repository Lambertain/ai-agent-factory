"""
NLP Content Quality Guardian Agent Providers

Провайдеры моделей для оптимизации затрат на валидацию.
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import asyncio
from dataclasses import dataclass

from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

from .settings import NLPQualityGuardianSettings, load_settings


class ValidationTaskType(Enum):
    """Типы задач валидации для оптимизации моделей."""
    DEEP_ANALYSIS = "deep_analysis"          # Сложный анализ качества - Premium Qwen 72B
    SAFETY_CHECK = "safety_check"            # Проверка безопасности - Qwen Coder 32B
    STRUCTURE_VALIDATION = "structure_validation"  # Структурная валидация - Qwen Coder 32B
    NLP_TECHNIQUE_ANALYSIS = "nlp_technique_analysis"  # Анализ техник - Premium Qwen 72B
    REPORT_GENERATION = "report_generation"   # Генерация отчетов - Gemini Flash Lite
    KNOWLEDGE_SEARCH = "knowledge_search"     # Поиск знаний - Gemini Flash Lite
    PATTERN_MATCHING = "pattern_matching"     # Паттерн матчинг - Qwen Coder 7B
    CULTURAL_VALIDATION = "cultural_validation"  # Культурная валидация - Gemini Flash


@dataclass
class ModelCostInfo:
    """Информация о стоимости модели."""
    input_cost_per_1m: float  # Стоимость за 1M input токенов
    output_cost_per_1m: float  # Стоимость за 1M output токенов
    performance_score: float  # Оценка производительности (1-10)
    recommended_for: List[str]  # Рекомендуемые типы задач


class QualityGuardianModelManager:
    """Менеджер моделей для оптимизации затрат на валидацию."""

    def __init__(self, settings: NLPQualityGuardianSettings):
        self.settings = settings
        self.model_costs = self._initialize_model_costs()
        self.task_model_mapping = self._initialize_task_mapping()
        self._cached_providers = {}

    def _initialize_model_costs(self) -> Dict[str, ModelCostInfo]:
        """Инициализация информации о стоимости моделей."""
        return {
            # Premium models for complex analysis
            "qwen2.5-72b-instruct": ModelCostInfo(
                input_cost_per_1m=2.0,
                output_cost_per_1m=6.0,
                performance_score=9.5,
                recommended_for=["deep_analysis", "nlp_technique_analysis", "complex_validation"]
            ),

            # Coding models for structured tasks
            "qwen2.5-coder-32b-instruct": ModelCostInfo(
                input_cost_per_1m=1.0,
                output_cost_per_1m=3.0,
                performance_score=8.5,
                recommended_for=["safety_check", "structure_validation", "pattern_detection"]
            ),

            "qwen2.5-coder-7b-instruct": ModelCostInfo(
                input_cost_per_1m=0.3,
                output_cost_per_1m=0.9,
                performance_score=7.0,
                recommended_for=["pattern_matching", "basic_validation", "simple_checks"]
            ),

            # Ultra-cheap Gemini for text tasks
            "gemini-2.5-flash-lite": ModelCostInfo(
                input_cost_per_1m=0.10,
                output_cost_per_1m=0.40,
                performance_score=8.0,
                recommended_for=["report_generation", "knowledge_search", "cultural_validation"]
            ),

            # Standard Gemini
            "gemini-2.5-flash": ModelCostInfo(
                input_cost_per_1m=0.15,
                output_cost_per_1m=0.60,
                performance_score=8.5,
                recommended_for=["multilingual_validation", "semantic_analysis", "content_understanding"]
            )
        }

    def _initialize_task_mapping(self) -> Dict[ValidationTaskType, str]:
        """Инициализация маппинга задач на модели."""
        return {
            ValidationTaskType.DEEP_ANALYSIS: self.settings.llm_validation_model,
            ValidationTaskType.SAFETY_CHECK: self.settings.llm_safety_model,
            ValidationTaskType.STRUCTURE_VALIDATION: self.settings.llm_safety_model,
            ValidationTaskType.NLP_TECHNIQUE_ANALYSIS: self.settings.llm_validation_model,
            ValidationTaskType.REPORT_GENERATION: self.settings.llm_reporting_model,
            ValidationTaskType.KNOWLEDGE_SEARCH: self.settings.llm_knowledge_model,
            ValidationTaskType.PATTERN_MATCHING: "qwen2.5-coder-7b-instruct",
            ValidationTaskType.CULTURAL_VALIDATION: self.settings.llm_knowledge_model
        }

    def get_optimal_model_for_task(self, task_type: ValidationTaskType) -> OpenAIModel:
        """Получить оптимальную модель для типа задачи валидации."""
        model_name = self.task_model_mapping.get(task_type, self.settings.llm_validation_model)

        # Создаем провайдер если не кэширован
        if model_name not in self._cached_providers:
            # Выбираем API ключ на основе модели
            if model_name.startswith("gemini"):
                api_key = self.settings.gemini_api_key
                base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            else:
                api_key = self.settings.llm_api_key
                base_url = self.settings.llm_base_url

            provider = OpenAIProvider(
                base_url=base_url,
                api_key=api_key
            )
            self._cached_providers[model_name] = OpenAIModel(model_name, provider=provider)

        return self._cached_providers[model_name]

    def estimate_task_cost(
        self,
        task_type: ValidationTaskType,
        input_tokens: int,
        estimated_output_tokens: int = 500
    ) -> Dict[str, Any]:
        """Оценить стоимость выполнения задачи."""
        model_name = self.task_model_mapping.get(task_type, self.settings.llm_validation_model)
        cost_info = self.model_costs.get(model_name)

        if not cost_info:
            return {"error": f"Информация о стоимости модели {model_name} не найдена"}

        input_cost = (input_tokens / 1_000_000) * cost_info.input_cost_per_1m
        output_cost = (estimated_output_tokens / 1_000_000) * cost_info.output_cost_per_1m
        total_cost = input_cost + output_cost

        return {
            "model": model_name,
            "task_type": task_type.value,
            "input_tokens": input_tokens,
            "output_tokens": estimated_output_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost,
            "performance_score": cost_info.performance_score,
            "cost_per_performance": total_cost / cost_info.performance_score if cost_info.performance_score > 0 else float('inf')
        }

    def optimize_validation_pipeline(
        self,
        validation_tasks: List[ValidationTaskType],
        content_length: int
    ) -> Dict[str, Any]:
        """Оптимизировать пайплайн валидации по стоимости."""
        # Оценка количества токенов на основе длины контента
        estimated_tokens = max(content_length // 4, 100)  # Примерно 1 токен = 4 символа

        optimization_plan = {
            "total_estimated_cost": 0.0,
            "tasks": [],
            "recommendations": []
        }

        for task_type in validation_tasks:
            # Оценка выходных токенов в зависимости от типа задачи
            if task_type in [ValidationTaskType.REPORT_GENERATION]:
                output_tokens = 2000
            elif task_type in [ValidationTaskType.DEEP_ANALYSIS, ValidationTaskType.NLP_TECHNIQUE_ANALYSIS]:
                output_tokens = 1000
            else:
                output_tokens = 500

            cost_estimate = self.estimate_task_cost(task_type, estimated_tokens, output_tokens)
            optimization_plan["tasks"].append(cost_estimate)
            optimization_plan["total_estimated_cost"] += cost_estimate.get("total_cost", 0)

        # Рекомендации по оптимизации
        if optimization_plan["total_estimated_cost"] > 0.50:  # Дорого
            optimization_plan["recommendations"].extend([
                "Рассмотрите использование более дешевых моделей для простых задач",
                "Включите batch processing для Gemini (50% скидка)",
                "Используйте контекстное кэширование для Qwen"
            ])

        if content_length > 50000:  # Большой контент
            optimization_plan["recommendations"].extend([
                "Включите автоматическое сжатие контекста",
                "Разделите валидацию на несколько этапов",
                "Используйте предварительную фильтрацию контента"
            ])

        return optimization_plan

    def get_validation_model_for_content_type(self, content_type: str) -> OpenAIModel:
        """Получить модель валидации для типа контента."""
        content_task_mapping = {
            "test": ValidationTaskType.STRUCTURE_VALIDATION,
            "transformation_program": ValidationTaskType.DEEP_ANALYSIS,
            "nlp_technique": ValidationTaskType.NLP_TECHNIQUE_ANALYSIS,
            "ericksonian_pattern": ValidationTaskType.NLP_TECHNIQUE_ANALYSIS,
            "knowledge_base": ValidationTaskType.PATTERN_MATCHING,
            "mixed_content": ValidationTaskType.DEEP_ANALYSIS
        }

        task_type = content_task_mapping.get(content_type, ValidationTaskType.DEEP_ANALYSIS)
        return self.get_optimal_model_for_task(task_type)

    def create_batch_validation_plan(
        self,
        validation_requests: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Создать план батчевой валидации для оптимизации."""
        batch_plan = {
            "total_requests": len(validation_requests),
            "batches": [],
            "total_cost": 0.0,
            "optimization_applied": []
        }

        # Группируем запросы по типу модели
        model_groups = {}
        for request in validation_requests:
            content_type = request.get("content_type", "mixed_content")
            model = self.get_validation_model_for_content_type(content_type)
            model_name = model.model_name

            if model_name not in model_groups:
                model_groups[model_name] = []
            model_groups[model_name].append(request)

        # Создаем батчи для каждой модели
        for model_name, requests in model_groups.items():
            batch_info = {
                "model": model_name,
                "requests_count": len(requests),
                "requests": requests,
                "estimated_cost": 0.0,
                "batch_discount": 0.0
            }

            # Применяем Batch API для Gemini
            if model_name.startswith("gemini") and len(requests) > 1 and self.settings.gemini_use_batch_api:
                batch_info["batch_discount"] = 0.5  # 50% скидка
                batch_plan["optimization_applied"].append(f"Gemini Batch API для {len(requests)} запросов")

            # Оценка стоимости батча
            for request in requests:
                content_length = len(request.get("content", ""))
                tokens = max(content_length // 4, 100)
                task_type = ValidationTaskType.DEEP_ANALYSIS  # По умолчанию

                cost_estimate = self.estimate_task_cost(task_type, tokens)
                batch_info["estimated_cost"] += cost_estimate.get("total_cost", 0)

            # Применяем скидку
            batch_info["estimated_cost"] *= (1 - batch_info["batch_discount"])
            batch_plan["total_cost"] += batch_info["estimated_cost"]
            batch_plan["batches"].append(batch_info)

        # Общие оптимизации
        if self.settings.enable_smart_routing:
            batch_plan["optimization_applied"].append("Умная маршрутизация по стоимости")

        if self.settings.qwen_enable_context_cache:
            batch_plan["optimization_applied"].append("Кэширование контекста Qwen")

        return batch_plan

    def get_model_performance_stats(self) -> Dict[str, Any]:
        """Получить статистику производительности моделей."""
        stats = {
            "models": {},
            "cost_efficiency_ranking": [],
            "performance_ranking": []
        }

        for model_name, cost_info in self.model_costs.items():
            stats["models"][model_name] = {
                "cost_per_1m_input": cost_info.input_cost_per_1m,
                "cost_per_1m_output": cost_info.output_cost_per_1m,
                "performance_score": cost_info.performance_score,
                "recommended_for": cost_info.recommended_for,
                "cost_efficiency": cost_info.performance_score / (cost_info.input_cost_per_1m + cost_info.output_cost_per_1m)
            }

        # Ранжирование по эффективности затрат
        stats["cost_efficiency_ranking"] = sorted(
            self.model_costs.items(),
            key=lambda x: x[1].performance_score / (x[1].input_cost_per_1m + x[1].output_cost_per_1m),
            reverse=True
        )

        # Ранжирование по производительности
        stats["performance_ranking"] = sorted(
            self.model_costs.items(),
            key=lambda x: x[1].performance_score,
            reverse=True
        )

        return stats


def create_model_manager(settings: Optional[NLPQualityGuardianSettings] = None) -> QualityGuardianModelManager:
    """Создать менеджер моделей валидации качества."""
    if settings is None:
        settings = load_settings()
    return QualityGuardianModelManager(settings)


def get_validation_model(
    task_type: ValidationTaskType,
    settings: Optional[NLPQualityGuardianSettings] = None
) -> OpenAIModel:
    """Получить модель для конкретной задачи валидации."""
    manager = create_model_manager(settings)
    return manager.get_optimal_model_for_task(task_type)


# Функции-утилиты для быстрого доступа к моделям

def get_deep_analysis_model(settings: Optional[NLPQualityGuardianSettings] = None) -> OpenAIModel:
    """Получить модель для глубокого анализа качества."""
    return get_validation_model(ValidationTaskType.DEEP_ANALYSIS, settings)


def get_safety_check_model(settings: Optional[NLPQualityGuardianSettings] = None) -> OpenAIModel:
    """Получить модель для проверки безопасности."""
    return get_validation_model(ValidationTaskType.SAFETY_CHECK, settings)


def get_report_generation_model(settings: Optional[NLPQualityGuardianSettings] = None) -> OpenAIModel:
    """Получить модель для генерации отчетов."""
    return get_validation_model(ValidationTaskType.REPORT_GENERATION, settings)


def get_knowledge_search_model(settings: Optional[NLPQualityGuardianSettings] = None) -> OpenAIModel:
    """Получить модель для поиска в базе знаний."""
    return get_validation_model(ValidationTaskType.KNOWLEDGE_SEARCH, settings)