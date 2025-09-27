# -*- coding: utf-8 -*-
"""
Провайдеры моделей для Universal Localization Engine Agent.

Оптимизированная система выбора моделей для различных задач локализации
с учетом языков, качества перевода и стоимости.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

from pydantic_ai.models import Model
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class LocalizationTask(Enum):
    """Типы задач локализации."""
    EXTRACTION = "extraction"        # Извлечение переводимого контента
    TRANSLATION = "translation"      # Перевод текста
    VALIDATION = "validation"        # Валидация качества
    CULTURAL_ADAPTATION = "cultural" # Культурная адаптация
    WORKFLOW_OPTIMIZATION = "workflow" # Оптимизация процессов
    PROJECT_MANAGEMENT = "management" # Управление проектами


class LanguageComplexity(Enum):
    """Сложность языка для перевода."""
    SIMPLE = "simple"      # Европейские языки (ES, FR, DE, IT)
    MEDIUM = "medium"      # Славянские, скандинавские (RU, PL, SV)
    COMPLEX = "complex"    # Азиатские без иероглифов (HI, TH, AR, HE)
    ADVANCED = "advanced"  # Иероглифические (ZH, JA, KO)


@dataclass
class LocalizationModelConfig:
    """Конфигурация модели для задач локализации."""
    model_name: str
    provider: str
    base_url: str
    api_key_var: str
    cost_per_1m_tokens: float
    max_tokens: int
    specializations: List[str]
    language_support: List[str]  # Поддерживаемые языки
    quality_score: int  # 1-10
    cultural_awareness: int  # 1-10


class LocalizationModelProvider:
    """
    Провайдер моделей для локализации с автоматическим выбором
    оптимальной модели на основе задачи, языков и требований качества.
    """

    def __init__(self, settings: Any):
        """
        Инициализация провайдера моделей локализации.

        Args:
            settings: Настройки приложения с API ключами
        """
        self.settings = settings
        self.model_configs = self._init_model_configs()
        self.language_complexity_map = self._init_language_complexity()

    def _init_model_configs(self) -> Dict[str, LocalizationModelConfig]:
        """Инициализация конфигураций моделей для локализации."""

        configs = {
            # === СПЕЦИАЛИЗИРОВАННЫЕ МОДЕЛИ ДЛЯ ПЕРЕВОДА ===

            # Премиум перевод - Claude Opus для сложных языков и культурной адаптации
            "claude_translation_premium": LocalizationModelConfig(
                model_name="claude-3-5-sonnet-20241022",
                provider="anthropic",
                base_url="https://api.anthropic.com",
                api_key_var="ANTHROPIC_API_KEY",
                cost_per_1m_tokens=15.0,
                max_tokens=8192,
                specializations=["premium_translation", "cultural_adaptation", "creative_content"],
                language_support=["zh", "ja", "ko", "ar", "he", "th", "hi", "ru"],
                quality_score=10,
                cultural_awareness=10
            ),

            # Профессиональный перевод - Qwen для технического контента
            "qwen_translation_pro": LocalizationModelConfig(
                model_name="qwen2.5-coder-32b-instruct",
                provider="openai_compatible",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key_var="LLM_API_KEY",
                cost_per_1m_tokens=3.0,
                max_tokens=32768,
                specializations=["technical_translation", "software_localization", "batch_processing"],
                language_support=["en", "zh", "ja", "ko", "es", "fr", "de", "ru", "pt", "it"],
                quality_score=9,
                cultural_awareness=7
            ),

            # Быстрый перевод - Gemini Flash для массовой обработки
            "gemini_translation_fast": LocalizationModelConfig(
                model_name="gemini-2.0-flash-exp",
                provider="google",
                base_url="https://generativelanguage.googleapis.com",
                api_key_var="GEMINI_API_KEY",
                cost_per_1m_tokens=0.4,
                max_tokens=8192,
                specializations=["fast_translation", "batch_processing", "basic_localization"],
                language_support=["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"],
                quality_score=7,
                cultural_awareness=6
            ),

            # Культурная адаптация - Claude для глубокого понимания культур
            "claude_cultural_expert": LocalizationModelConfig(
                model_name="claude-3-5-sonnet-20241022",
                provider="anthropic",
                base_url="https://api.anthropic.com",
                api_key_var="ANTHROPIC_API_KEY",
                cost_per_1m_tokens=15.0,
                max_tokens=8192,
                specializations=["cultural_adaptation", "market_research", "brand_localization"],
                language_support=["all"],  # Универсальные культурные знания
                quality_score=10,
                cultural_awareness=10
            ),

            # Техническая валидация - Qwen Coder для точности
            "qwen_validation": LocalizationModelConfig(
                model_name="qwen2.5-coder-14b-instruct",
                provider="openai_compatible",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key_var="LLM_API_KEY",
                cost_per_1m_tokens=1.5,
                max_tokens=32768,
                specializations=["quality_validation", "technical_review", "consistency_check"],
                language_support=["all"],
                quality_score=8,
                cultural_awareness=5
            ),

            # Workflow оптимизация - Gemini Pro для планирования
            "gemini_workflow": LocalizationModelConfig(
                model_name="gemini-2.0-flash-thinking-exp",
                provider="google",
                base_url="https://generativelanguage.googleapis.com",
                api_key_var="GEMINI_API_KEY",
                cost_per_1m_tokens=1.0,
                max_tokens=32768,
                specializations=["workflow_optimization", "project_planning", "process_automation"],
                language_support=["en"],  # Планирование в основном на английском
                quality_score=8,
                cultural_awareness=6
            ),

            # Извлечение контента - экономичная модель для анализа кода
            "qwen_extraction": LocalizationModelConfig(
                model_name="qwen2.5-coder-7b-instruct",
                provider="openai_compatible",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key_var="LLM_API_KEY",
                cost_per_1m_tokens=0.5,
                max_tokens=32768,
                specializations=["content_extraction", "code_analysis", "text_mining"],
                language_support=["en"],  # Извлечение обычно из английского кода
                quality_score=7,
                cultural_awareness=3
            ),

            # Fallback модель - надежная и доступная
            "fallback_localization": LocalizationModelConfig(
                model_name="qwen2.5-coder-7b-instruct",
                provider="openai_compatible",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key_var="LLM_API_KEY",
                cost_per_1m_tokens=0.5,
                max_tokens=32768,
                specializations=["general_purpose", "fallback"],
                language_support=["all"],
                quality_score=6,
                cultural_awareness=5
            )
        }

        return configs

    def _init_language_complexity(self) -> Dict[str, LanguageComplexity]:
        """Инициализация карты сложности языков."""

        return {
            # Простые (европейские латинские)
            "es": LanguageComplexity.SIMPLE,  # Испанский
            "fr": LanguageComplexity.SIMPLE,  # Французский
            "de": LanguageComplexity.SIMPLE,  # Немецкий
            "it": LanguageComplexity.SIMPLE,  # Итальянский
            "pt": LanguageComplexity.SIMPLE,  # Португальский
            "nl": LanguageComplexity.SIMPLE,  # Голландский

            # Средние (славянские, скандинавские)
            "ru": LanguageComplexity.MEDIUM,  # Русский
            "pl": LanguageComplexity.MEDIUM,  # Польский
            "cs": LanguageComplexity.MEDIUM,  # Чешский
            "sv": LanguageComplexity.MEDIUM,  # Шведский
            "no": LanguageComplexity.MEDIUM,  # Норвежский
            "da": LanguageComplexity.MEDIUM,  # Датский

            # Сложные (без иероглифов)
            "ar": LanguageComplexity.COMPLEX,  # Арабский (RTL)
            "he": LanguageComplexity.COMPLEX,  # Иврит (RTL)
            "hi": LanguageComplexity.COMPLEX,  # Хинди
            "th": LanguageComplexity.COMPLEX,  # Тайский
            "vi": LanguageComplexity.COMPLEX,  # Вьетнамский
            "tr": LanguageComplexity.COMPLEX,  # Турецкий

            # Продвинутые (иероглифические)
            "zh": LanguageComplexity.ADVANCED,  # Китайский
            "ja": LanguageComplexity.ADVANCED,  # Японский
            "ko": LanguageComplexity.ADVANCED,  # Корейский
        }

    def get_optimal_model(
        self,
        task: LocalizationTask,
        target_languages: List[str],
        quality_level: str = "professional",
        cost_priority: bool = False,
        cultural_adaptation: bool = True
    ) -> Model:
        """
        Автоматический выбор оптимальной модели для задачи локализации.

        Args:
            task: Тип задачи локализации
            target_languages: Целевые языки
            quality_level: Уровень качества (basic, standard, professional, native)
            cost_priority: Приоритет стоимости над качеством
            cultural_adaptation: Требуется ли культурная адаптация

        Returns:
            Оптимальная модель для задачи
        """

        # Определяем сложность языков
        max_complexity = self._get_max_language_complexity(target_languages)

        # Выбираем ключ модели
        model_key = self._select_model_key(
            task, max_complexity, quality_level, cost_priority, cultural_adaptation
        )

        # Создаем и возвращаем модель
        return self._create_model(model_key)

    def _get_max_language_complexity(self, languages: List[str]) -> LanguageComplexity:
        """Определяет максимальную сложность среди языков."""

        if not languages:
            return LanguageComplexity.SIMPLE

        complexities = []
        for lang in languages:
            # Берем код языка без региона (en-US -> en)
            lang_code = lang.split('-')[0].lower()
            complexity = self.language_complexity_map.get(lang_code, LanguageComplexity.MEDIUM)
            complexities.append(complexity)

        # Возвращаем максимальную сложность
        complexity_order = [
            LanguageComplexity.SIMPLE,
            LanguageComplexity.MEDIUM,
            LanguageComplexity.COMPLEX,
            LanguageComplexity.ADVANCED
        ]

        max_complexity = LanguageComplexity.SIMPLE
        for complexity in complexities:
            if complexity_order.index(complexity) > complexity_order.index(max_complexity):
                max_complexity = complexity

        return max_complexity

    def _select_model_key(
        self,
        task: LocalizationTask,
        language_complexity: LanguageComplexity,
        quality_level: str,
        cost_priority: bool,
        cultural_adaptation: bool
    ) -> str:
        """Логика выбора ключа модели."""

        # Приоритет стоимости - используем экономичные модели
        if cost_priority:
            if task == LocalizationTask.TRANSLATION:
                return "gemini_translation_fast"
            elif task == LocalizationTask.EXTRACTION:
                return "qwen_extraction"
            else:
                return "qwen_validation"

        # Выбор по типу задачи
        if task == LocalizationTask.EXTRACTION:
            return "qwen_extraction"

        elif task == LocalizationTask.TRANSLATION:
            # Выбор модели для перевода на основе языковой сложности и качества
            if quality_level == "native" or language_complexity == LanguageComplexity.ADVANCED:
                return "claude_translation_premium"
            elif quality_level == "professional" and language_complexity in [LanguageComplexity.COMPLEX, LanguageComplexity.MEDIUM]:
                return "qwen_translation_pro"
            else:
                return "gemini_translation_fast"

        elif task == LocalizationTask.CULTURAL_ADAPTATION:
            # Культурная адаптация всегда требует премиум модель
            return "claude_cultural_expert"

        elif task == LocalizationTask.VALIDATION:
            # Валидация - техническая точность
            return "qwen_validation"

        elif task == LocalizationTask.WORKFLOW_OPTIMIZATION:
            # Оптимизация процессов
            return "gemini_workflow"

        elif task == LocalizationTask.PROJECT_MANAGEMENT:
            # Управление проектами
            return "gemini_workflow"

        else:
            # По умолчанию
            return "qwen_translation_pro"

    def _create_model(self, model_key: str) -> Model:
        """Создание экземпляра модели по ключу."""

        config = self.model_configs.get(model_key)
        if not config:
            config = self.model_configs["fallback_localization"]

        try:
            # Получаем API ключ
            api_key = getattr(self.settings, config.api_key_var.lower(), None)
            if not api_key:
                raise ValueError(f"API ключ {config.api_key_var} не найден")

            # Создаем провайдера (пока только OpenAI Compatible)
            if config.provider in ["openai_compatible", "anthropic", "google"]:
                provider = OpenAIProvider(
                    base_url=config.base_url,
                    api_key=api_key
                )
                model = OpenAIModel(config.model_name, provider=provider)
            else:
                # Fallback
                fallback_config = self.model_configs["fallback_localization"]
                fallback_api_key = getattr(self.settings, fallback_config.api_key_var.lower())
                provider = OpenAIProvider(
                    base_url=fallback_config.base_url,
                    api_key=fallback_api_key
                )
                model = OpenAIModel(fallback_config.model_name, provider=provider)

            return model

        except Exception as e:
            return self._create_fallback_model()

    def _create_fallback_model(self) -> Model:
        """Создание fallback модели."""

        try:
            config = self.model_configs["fallback_localization"]
            api_key = getattr(self.settings, config.api_key_var.lower())

            provider = OpenAIProvider(
                base_url=config.base_url,
                api_key=api_key
            )

            return OpenAIModel(config.model_name, provider=provider)

        except Exception as e:
            raise RuntimeError(f"Не удалось создать даже fallback модель: {e}")

    def get_model_for_language_pair(
        self,
        source_lang: str,
        target_lang: str,
        quality: str = "professional"
    ) -> Model:
        """
        Получить модель для конкретной языковой пары.

        Args:
            source_lang: Исходный язык
            target_lang: Целевой язык
            quality: Уровень качества

        Returns:
            Оптимальная модель для языковой пары
        """

        # Определяем сложность целевого языка
        target_complexity = self.language_complexity_map.get(
            target_lang.split('-')[0].lower(),
            LanguageComplexity.MEDIUM
        )

        # Особые случаи для языковых пар
        special_pairs = {
            ("en", "zh"): "claude_translation_premium",  # EN->CN сложный
            ("en", "ja"): "claude_translation_premium",  # EN->JP сложный
            ("en", "ar"): "claude_translation_premium",  # EN->AR (RTL)
            ("zh", "en"): "qwen_translation_pro",        # CN->EN (Qwen хорош с китайским)
        }

        pair_key = (source_lang.split('-')[0], target_lang.split('-')[0])
        if pair_key in special_pairs:
            return self._create_model(special_pairs[pair_key])

        # Общая логика на основе сложности
        if target_complexity == LanguageComplexity.ADVANCED and quality in ["professional", "native"]:
            return self._create_model("claude_translation_premium")
        elif target_complexity in [LanguageComplexity.COMPLEX, LanguageComplexity.MEDIUM]:
            return self._create_model("qwen_translation_pro")
        else:
            return self._create_model("gemini_translation_fast")

    def get_cultural_adaptation_model(
        self,
        target_markets: List[str]
    ) -> Model:
        """
        Получить модель для культурной адаптации.

        Args:
            target_markets: Целевые рынки (локали)

        Returns:
            Модель для культурной адаптации
        """
        # Культурная адаптация всегда требует премиум модель
        return self._create_model("claude_cultural_expert")

    def get_batch_translation_model(
        self,
        volume: int,
        languages: List[str],
        budget_conscious: bool = False
    ) -> Model:
        """
        Получить модель для массового перевода.

        Args:
            volume: Объем текста (количество строк)
            languages: Языки перевода
            budget_conscious: Экономия бюджета

        Returns:
            Оптимальная модель для batch перевода
        """

        max_complexity = self._get_max_language_complexity(languages)

        # Для больших объемов и бюджетных проектов
        if volume > 1000 and budget_conscious:
            return self._create_model("gemini_translation_fast")

        # Для сложных языков независимо от объема
        elif max_complexity == LanguageComplexity.ADVANCED:
            return self._create_model("claude_translation_premium")

        # Баланс качества и стоимости
        else:
            return self._create_model("qwen_translation_pro")

    def estimate_translation_cost(
        self,
        word_count: int,
        target_languages: List[str],
        quality_level: str = "professional"
    ) -> Dict[str, Any]:
        """
        Оценка стоимости перевода проекта.

        Args:
            word_count: Количество слов для перевода
            target_languages: Целевые языки
            quality_level: Уровень качества

        Returns:
            Оценка стоимости по языкам и общая
        """

        # Примерная конверсия слов в токены (1 слово ≈ 1.3 токена)
        estimated_tokens = word_count * 1.3

        cost_breakdown = {}
        total_cost = 0

        for lang in target_languages:
            # Получаем оптимальную модель для языка
            model = self.get_model_for_language_pair("en", lang, quality_level)

            # Находим конфигурацию модели (упрощенно)
            model_cost = 3.0  # Средняя стоимость за 1M токенов

            # Определяем множитель сложности
            complexity = self.language_complexity_map.get(
                lang.split('-')[0].lower(),
                LanguageComplexity.MEDIUM
            )

            complexity_multiplier = {
                LanguageComplexity.SIMPLE: 1.0,
                LanguageComplexity.MEDIUM: 1.2,
                LanguageComplexity.COMPLEX: 1.5,
                LanguageComplexity.ADVANCED: 2.0
            }

            multiplier = complexity_multiplier[complexity]
            lang_cost = (estimated_tokens * model_cost * multiplier) / 1_000_000

            cost_breakdown[lang] = {
                "estimated_cost_usd": round(lang_cost, 3),
                "complexity": complexity.value,
                "multiplier": multiplier,
                "tokens": int(estimated_tokens)
            }

            total_cost += lang_cost

        return {
            "total_cost_usd": round(total_cost, 2),
            "cost_per_language": cost_breakdown,
            "source_words": word_count,
            "estimated_tokens": int(estimated_tokens),
            "quality_level": quality_level
        }

    def get_model_info(self, model_key: str) -> Dict[str, Any]:
        """Получить информацию о модели."""

        config = self.model_configs.get(model_key)
        if not config:
            return {"error": f"Модель {model_key} не найдена"}

        return {
            "model_name": config.model_name,
            "provider": config.provider,
            "cost_per_1m_tokens": config.cost_per_1m_tokens,
            "specializations": config.specializations,
            "language_support": config.language_support,
            "quality_score": config.quality_score,
            "cultural_awareness": config.cultural_awareness
        }

    def list_available_models(self) -> List[Dict[str, Any]]:
        """Список всех доступных моделей локализации."""

        models_info = []
        for key, config in self.model_configs.items():
            models_info.append({
                "key": key,
                "model_name": config.model_name,
                "provider": config.provider,
                "cost_per_1m_tokens": config.cost_per_1m_tokens,
                "specializations": config.specializations,
                "language_support": config.language_support,
                "quality_score": config.quality_score,
                "cultural_awareness": config.cultural_awareness
            })

        # Сортируем по качеству
        models_info.sort(key=lambda x: x["quality_score"], reverse=True)
        return models_info


def get_llm_model(settings: Any = None, model_type: str = "balanced") -> Model:
    """
    Фабричная функция для создания модели локализации.

    Args:
        settings: Настройки приложения
        model_type: Тип модели (cost_optimized, quality_optimized, balanced)

    Returns:
        Экземпляр модели
    """
    if settings is None:
        from .settings import load_settings
        settings = load_settings()

    provider = LocalizationModelProvider(settings)

    if model_type == "cost_optimized":
        return provider._create_model("gemini_translation_fast")
    elif model_type == "quality_optimized":
        return provider._create_model("claude_translation_premium")
    else:  # balanced
        return provider._create_model("qwen_translation_pro")


def get_model_for_localization_task(
    task: str,
    target_languages: List[str],
    quality: str = "professional",
    settings: Any = None
) -> Model:
    """
    Упрощенная функция получения модели для задач локализации.

    Args:
        task: Тип задачи
        target_languages: Целевые языки
        quality: Уровень качества
        settings: Настройки приложения

    Returns:
        Оптимальная модель для задачи
    """
    if settings is None:
        from .settings import load_settings
        settings = load_settings()

    provider = LocalizationModelProvider(settings)

    # Конвертируем строку в enum
    task_enum = LocalizationTask(task) if task in [e.value for e in LocalizationTask] else LocalizationTask.TRANSLATION

    return provider.get_optimal_model(
        task=task_enum,
        target_languages=target_languages,
        quality_level=quality
    )