"""
Провайдеры моделей для Universal Quality Validator Agent.
Оптимизированная система выбора моделей под различные задачи валидации.
"""

from typing import Dict, Any, Optional, List
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.gemini import GeminiProvider
from dataclasses import dataclass
from enum import Enum

from .dependencies import QualityStandard, ValidationLevel, ProjectDomain
from .settings import load_settings


class TaskComplexity(Enum):
    """Сложность задачи для выбора оптимальной модели."""
    SIMPLE = "simple"        # Простые проверки, binary decisions
    STANDARD = "standard"    # Стандартная валидация и анализ
    COMPLEX = "complex"      # Сложный архитектурный анализ
    CRITICAL = "critical"    # Критичные security/compliance задачи


class ModelPurpose(Enum):
    """Назначение модели для оптимизации."""
    CODE_ANALYSIS = "code_analysis"
    SECURITY_AUDIT = "security_audit"
    PERFORMANCE_REVIEW = "performance_review"
    DOCUMENTATION = "documentation"
    GENERAL_VALIDATION = "general_validation"


@dataclass
class ModelConfig:
    """Конфигурация модели."""
    model_name: str
    provider: str
    base_url: Optional[str] = None
    api_key_env: str = "LLM_API_KEY"
    cost_per_1k_tokens: float = 0.0
    max_tokens: int = 8000
    temperature: float = 0.1
    suitable_for: List[ModelPurpose] = None

    def __post_init__(self):
        if self.suitable_for is None:
            self.suitable_for = [ModelPurpose.GENERAL_VALIDATION]


class QualityValidatorModelProvider:
    """Провайдер моделей для Quality Validator с оптимизацией по стоимости и качеству."""

    def __init__(self):
        self.settings = load_settings()
        self._model_configs = self._get_model_configurations()
        self._providers_cache = {}

    def _get_model_configurations(self) -> Dict[str, ModelConfig]:
        """Получить конфигурации всех доступных моделей."""
        return {
            # === CODING & TECHNICAL ANALYSIS ===
            "qwen2.5-coder-32b": ModelConfig(
                model_name="qwen2.5-coder-32b-instruct",
                provider="openai",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key_env="LLM_API_KEY",
                cost_per_1k_tokens=0.5,
                temperature=0.0,  # Строгий анализ кода
                suitable_for=[
                    ModelPurpose.CODE_ANALYSIS,
                    ModelPurpose.PERFORMANCE_REVIEW
                ]
            ),

            "qwen2.5-coder-7b": ModelConfig(
                model_name="qwen2.5-coder-7b-instruct",
                provider="openai",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key_env="LLM_API_KEY",
                cost_per_1k_tokens=0.1,
                temperature=0.0,
                suitable_for=[ModelPurpose.CODE_ANALYSIS]
            ),

            # === SECURITY & COMPLIANCE ===
            "qwen2.5-72b": ModelConfig(
                model_name="qwen2.5-72b-instruct",
                provider="openai",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key_env="LLM_API_KEY",
                cost_per_1k_tokens=2.0,
                temperature=0.0,  # Максимальная точность для security
                suitable_for=[
                    ModelPurpose.SECURITY_AUDIT,
                    ModelPurpose.GENERAL_VALIDATION
                ]
            ),

            # === COST-OPTIMIZED DOCUMENTATION & SIMPLE TASKS ===
            "gemini-2.5-flash": ModelConfig(
                model_name="gemini-2.5-flash",
                provider="gemini",
                api_key_env="GEMINI_API_KEY",
                cost_per_1k_tokens=0.075,  # Крайне дешево
                temperature=0.2,
                suitable_for=[
                    ModelPurpose.DOCUMENTATION,
                    ModelPurpose.GENERAL_VALIDATION
                ]
            ),

            # === BALANCED GENERAL PURPOSE ===
            "gpt-4o-mini": ModelConfig(
                model_name="gpt-4o-mini",
                provider="openai",
                api_key_env="OPENAI_API_KEY",
                cost_per_1k_tokens=0.15,
                temperature=0.1,
                suitable_for=[
                    ModelPurpose.GENERAL_VALIDATION,
                    ModelPurpose.DOCUMENTATION
                ]
            )
        }

    def _get_provider(self, model_config: ModelConfig):
        """Получить или создать провайдера для модели."""
        cache_key = f"{model_config.provider}_{model_config.base_url or 'default'}"

        if cache_key in self._providers_cache:
            return self._providers_cache[cache_key]

        if model_config.provider == "openai":
            import os
            api_key = os.getenv(model_config.api_key_env)
            if not api_key:
                raise ValueError(f"API key not found in environment: {model_config.api_key_env}")

            provider = OpenAIProvider(
                base_url=model_config.base_url,
                api_key=api_key
            )
        elif model_config.provider == "gemini":
            import os
            api_key = os.getenv(model_config.api_key_env)
            if not api_key:
                raise ValueError(f"API key not found in environment: {model_config.api_key_env}")

            provider = GeminiProvider(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {model_config.provider}")

        self._providers_cache[cache_key] = provider
        return provider

    def _determine_complexity(
        self,
        validation_type: str,
        project_domain: ProjectDomain,
        validation_level: ValidationLevel
    ) -> TaskComplexity:
        """Определить сложность задачи для выбора модели."""

        # Security всегда critical
        if validation_type == "security":
            return TaskComplexity.CRITICAL

        # Compliance для финтеха и healthcare - critical
        if validation_type == "compliance" and project_domain in [
            ProjectDomain.FINTECH, ProjectDomain.HEALTHCARE
        ]:
            return TaskComplexity.CRITICAL

        # Enterprise уровень всегда complex
        if validation_level == ValidationLevel.ENTERPRISE:
            return TaskComplexity.COMPLEX

        # Архитектурный анализ - complex
        if validation_type in ["architecture", "performance"] and validation_level in [
            ValidationLevel.COMPREHENSIVE, ValidationLevel.ENTERPRISE
        ]:
            return TaskComplexity.COMPLEX

        # Basic уровень - simple
        if validation_level == ValidationLevel.BASIC:
            return TaskComplexity.SIMPLE

        return TaskComplexity.STANDARD

    def _select_optimal_model(
        self,
        purpose: ModelPurpose,
        complexity: TaskComplexity,
        budget_conscious: bool = True
    ) -> str:
        """Выбрать оптимальную модель по назначению и сложности."""

        # Критичные задачи безопасности - только лучшие модели
        if complexity == TaskComplexity.CRITICAL:
            if purpose == ModelPurpose.SECURITY_AUDIT:
                return "qwen2.5-72b"  # Максимальная точность
            elif purpose == ModelPurpose.CODE_ANALYSIS:
                return "qwen2.5-coder-32b"  # Лучший для кода

        # Сложные архитектурные задачи
        elif complexity == TaskComplexity.COMPLEX:
            if purpose in [ModelPurpose.CODE_ANALYSIS, ModelPurpose.PERFORMANCE_REVIEW]:
                return "qwen2.5-coder-32b"
            else:
                return "qwen2.5-72b"

        # Стандартные задачи - баланс цена/качество
        elif complexity == TaskComplexity.STANDARD:
            if purpose == ModelPurpose.CODE_ANALYSIS:
                return "qwen2.5-coder-7b" if budget_conscious else "qwen2.5-coder-32b"
            elif purpose == ModelPurpose.DOCUMENTATION:
                return "gemini-2.5-flash"  # Очень дешево
            else:
                return "gpt-4o-mini"  # Универсальный баланс

        # Простые задачи - максимально дешево
        else:  # TaskComplexity.SIMPLE
            if purpose == ModelPurpose.DOCUMENTATION:
                return "gemini-2.5-flash"
            else:
                return "qwen2.5-coder-7b" if purpose == ModelPurpose.CODE_ANALYSIS else "gpt-4o-mini"

    def get_optimal_model(
        self,
        validation_type: str = "general",
        project_domain: ProjectDomain = ProjectDomain.WEB_DEVELOPMENT,
        validation_level: ValidationLevel = ValidationLevel.STANDARD,
        priority: str = "quality"  # quality, speed, cost
    ):
        """
        Получить оптимальную модель для конкретной задачи валидации.

        Args:
            validation_type: Тип валидации (code, security, performance, etc.)
            project_domain: Домен проекта
            validation_level: Уровень детализации валидации
            priority: Приоритет (quality, speed, cost)
        """

        # Определяем назначение модели
        purpose_mapping = {
            "code": ModelPurpose.CODE_ANALYSIS,
            "security": ModelPurpose.SECURITY_AUDIT,
            "performance": ModelPurpose.PERFORMANCE_REVIEW,
            "documentation": ModelPurpose.DOCUMENTATION,
            "compliance": ModelPurpose.SECURITY_AUDIT,  # Требует высокой точности
            "general": ModelPurpose.GENERAL_VALIDATION
        }

        purpose = purpose_mapping.get(validation_type, ModelPurpose.GENERAL_VALIDATION)
        complexity = self._determine_complexity(validation_type, project_domain, validation_level)
        budget_conscious = (priority == "cost")

        # Выбираем модель
        selected_model_key = self._select_optimal_model(purpose, complexity, budget_conscious)
        model_config = self._model_configs[selected_model_key]

        # Создаем и возвращаем модель
        provider = self._get_provider(model_config)

        if model_config.provider == "openai":
            return OpenAIModel(
                model_config.model_name,
                provider=provider,
                temperature=model_config.temperature
            )
        elif model_config.provider == "gemini":
            return GeminiModel(
                model_config.model_name,
                provider=provider,
                temperature=model_config.temperature
            )

    def get_cost_estimate(
        self,
        model_name: str,
        estimated_tokens: int = 4000
    ) -> Dict[str, Any]:
        """Получить оценку стоимости для модели."""

        model_config = self._model_configs.get(model_name)
        if not model_config:
            return {"error": f"Model {model_name} not found"}

        cost = (estimated_tokens / 1000) * model_config.cost_per_1k_tokens

        return {
            "model": model_name,
            "estimated_tokens": estimated_tokens,
            "cost_per_1k_tokens": model_config.cost_per_1k_tokens,
            "estimated_cost_usd": round(cost, 4),
            "provider": model_config.provider
        }

    def get_all_models_info(self) -> Dict[str, Dict[str, Any]]:
        """Получить информацию о всех доступных моделях."""
        return {
            name: {
                "model_name": config.model_name,
                "provider": config.provider,
                "cost_per_1k_tokens": config.cost_per_1k_tokens,
                "suitable_for": [purpose.value for purpose in config.suitable_for],
                "temperature": config.temperature
            }
            for name, config in self._model_configs.items()
        }

    def recommend_model_for_task(
        self,
        task_description: str,
        domain: ProjectDomain,
        budget_limit: Optional[float] = None
    ) -> Dict[str, Any]:
        """Рекомендовать модель на основе описания задачи."""

        # Простая эвристика для определения типа задачи
        task_lower = task_description.lower()

        if any(word in task_lower for word in ["security", "vulnerability", "compliance"]):
            validation_type = "security"
        elif any(word in task_lower for word in ["performance", "speed", "optimization"]):
            validation_type = "performance"
        elif any(word in task_lower for word in ["code", "refactor", "quality"]):
            validation_type = "code"
        elif any(word in task_lower for word in ["document", "readme", "docs"]):
            validation_type = "documentation"
        else:
            validation_type = "general"

        # Определяем уровень валидации по ключевым словам
        if any(word in task_lower for word in ["enterprise", "comprehensive", "detailed"]):
            level = ValidationLevel.COMPREHENSIVE
        elif any(word in task_lower for word in ["basic", "simple", "quick"]):
            level = ValidationLevel.BASIC
        else:
            level = ValidationLevel.STANDARD

        priority = "cost" if budget_limit and budget_limit < 0.01 else "quality"

        model = self.get_optimal_model(validation_type, domain, level, priority)

        return {
            "recommended_model": model.model_name,
            "reasoning": f"Оптимальная модель для '{validation_type}' задач в домене {domain.value}",
            "validation_type": validation_type,
            "validation_level": level.value,
            "priority": priority
        }