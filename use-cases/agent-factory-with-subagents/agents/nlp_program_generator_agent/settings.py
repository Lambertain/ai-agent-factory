"""
NLP Program Generator Agent Settings

Cost-optimized настройки для генерации персонализированных программ трансформации.
Поддержка Qwen + Gemini моделей для минимизации затрат.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import Optional, List
import os


class NLPProgramGeneratorSettings(BaseSettings):
    """Настройки NLP Program Generator Agent."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Базовые LLM настройки
    llm_api_key: str = Field(..., description="API ключ для LLM")
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Cost-optimized модели
    # Генерация программ - Qwen Coder для структурированного контента
    llm_program_generation_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для генерации программ"
    )

    # Создание NLP техник - Premium Qwen для сложных паттернов
    llm_nlp_techniques_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для создания NLP техник"
    )

    # Эриксоновские паттерны - специализированная модель
    llm_hypnotic_patterns_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для гипнотических паттернов"
    )

    # Персонализация и адаптация - Gemini Flash для быстрых задач
    llm_personalization_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для персонализации"
    )

    # Валидация контента - экономичная Gemini
    llm_validation_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для валидации"
    )

    # Альтернативные API ключи
    gemini_api_key: Optional[str] = Field(None, description="Google Gemini API ключ")
    openai_api_key: Optional[str] = Field(None, description="OpenAI API ключ")

    # Настройки генерации программ
    program_domain: str = Field(default="psychology", description="Домен программ")
    default_severity_level: str = Field(default="moderate", description="Уровень по умолчанию")
    default_vak_type: str = Field(default="mixed", description="VAK тип по умолчанию")
    default_content_format: str = Field(default="both", description="Формат контента")

    # Персонализация
    enable_vak_adaptation: bool = Field(default=True, description="Включить VAK адаптацию")
    enable_pattern_shift: bool = Field(default=True, description="Использовать PatternShift")
    enable_hypnotic_language: bool = Field(default=True, description="Гипнотический язык")
    enable_nlp_techniques: bool = Field(default=True, description="NLP техники")

    # Технические ограничения
    max_program_duration: int = Field(default=21, description="Максимальная длительность программы")
    max_daily_time: int = Field(default=35, description="Максимальное время в день (минуты)")
    max_lines_per_module: int = Field(default=300, description="Максимум строк на модуль")
    enable_modular_structure: bool = Field(default=True, description="Модульная структура")

    # Cost optimization
    enable_smart_routing: bool = Field(default=True, description="Умная маршрутизация")
    gemini_use_batch_api: bool = Field(default=True, description="Batch API для Gemini")
    qwen_enable_context_cache: bool = Field(default=True, description="Кэш контекста Qwen")
    auto_compress_context: bool = Field(default=True, description="Сжатие контекста")

    # RAG и поиск
    enable_knowledge_search: bool = Field(default=True, description="Поиск в базе знаний")
    knowledge_match_count: int = Field(default=5, description="Количество результатов RAG")
    enable_web_research: bool = Field(default=False, description="Веб исследования")

    # Интеграция с Archon
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )
    enable_task_delegation: bool = Field(default=True, description="Делегирование задач")
    enable_progress_tracking: bool = Field(default=True, description="Отслеживание прогресса")

    # Безопасность и этика
    enable_safety_checks: bool = Field(default=True, description="Проверки безопасности")
    enable_ethics_validation: bool = Field(default=True, description="Этическая валидация")
    min_age_restriction: int = Field(default=16, description="Минимальный возраст")
    max_age_restriction: int = Field(default=80, description="Максимальный возраст")

    # Языковые настройки
    default_language: str = Field(default="ru", description="Язык по умолчанию")
    supported_languages: List[str] = Field(
        default=["ru", "en"],
        description="Поддерживаемые языки"
    )
    dual_language_mode: bool = Field(default=True, description="Двуязычный режим")

    # Логирование и мониторинг
    log_level: str = Field(default="INFO", description="Уровень логирования")
    enable_detailed_logging: bool = Field(default=True, description="Детальное логирование")
    track_generation_metrics: bool = Field(default=True, description="Метрики генерации")

    def get_model_for_task(self, task_type: str) -> str:
        """Получить оптимальную модель для типа задачи."""
        model_mapping = {
            "program_generation": self.llm_program_generation_model,
            "nlp_techniques": self.llm_nlp_techniques_model,
            "hypnotic_patterns": self.llm_hypnotic_patterns_model,
            "personalization": self.llm_personalization_model,
            "validation": self.llm_validation_model,
            "default": self.llm_program_generation_model
        }
        return model_mapping.get(task_type, model_mapping["default"])

    def get_api_key_for_model(self, model: str) -> str:
        """Получить API ключ для конкретной модели."""
        if "gemini" in model.lower():
            return self.gemini_api_key or self.llm_api_key
        elif "gpt" in model.lower() or "openai" in model.lower():
            return self.openai_api_key or self.llm_api_key
        else:
            # Qwen и другие модели через основной ключ
            return self.llm_api_key

    def get_program_parameters(self) -> dict:
        """Получить параметры для генерации программ."""
        return {
            "domain": self.program_domain,
            "severity_level": self.default_severity_level,
            "vak_type": self.default_vak_type,
            "content_format": self.default_content_format,
            "max_duration": self.max_program_duration,
            "max_daily_time": self.max_daily_time,
            "enable_pattern_shift": self.enable_pattern_shift,
            "enable_hypnotic_language": self.enable_hypnotic_language,
            "enable_nlp_techniques": self.enable_nlp_techniques,
            "modular_structure": self.enable_modular_structure,
            "max_lines_per_module": self.max_lines_per_module
        }

    def get_cost_optimization_settings(self) -> dict:
        """Получить настройки оптимизации затрат."""
        return {
            "smart_routing": self.enable_smart_routing,
            "batch_api": self.gemini_use_batch_api,
            "context_cache": self.qwen_enable_context_cache,
            "auto_compress": self.auto_compress_context,
            "model_mapping": {
                "heavy_tasks": self.llm_nlp_techniques_model,
                "medium_tasks": self.llm_program_generation_model,
                "light_tasks": self.llm_personalization_model
            }
        }

    def is_task_allowed(self, task_description: str, user_age: int = None) -> bool:
        """Проверить разрешена ли задача."""
        if not self.enable_safety_checks:
            return True

        # Возрастные ограничения
        if user_age and (user_age < self.min_age_restriction or user_age > self.max_age_restriction):
            return False

        # Проверка на запрещенные темы
        forbidden_keywords = [
            "suicide", "self-harm", "violence", "illegal",
            "drugs", "addiction" # без профессиональной поддержки
        ]

        task_lower = task_description.lower()
        return not any(keyword in task_lower for keyword in forbidden_keywords)


def load_settings() -> NLPProgramGeneratorSettings:
    """Загрузить настройки с валидацией."""
    load_dotenv()

    try:
        settings = NLPProgramGeneratorSettings()

        # Проверка критичных настроек
        if not settings.llm_api_key:
            raise ValueError("LLM_API_KEY is required")

        return settings

    except Exception as e:
        error_msg = f"Ошибка загрузки настроек: {e}"

        if "llm_api_key" in str(e).lower():
            error_msg += """

Создайте файл .env со следующими переменными:

# Основные LLM настройки
LLM_API_KEY=your_api_key_here
LLM_PROVIDER=openai
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# Дополнительно: Gemini для экономии
GEMINI_API_KEY=your_gemini_key_here

# Настройки программ
PROGRAM_DOMAIN=psychology
DEFAULT_SEVERITY_LEVEL=moderate
DEFAULT_VAK_TYPE=mixed

# Персонализация
ENABLE_VAK_ADAPTATION=true
ENABLE_PATTERN_SHIFT=true
ENABLE_HYPNOTIC_LANGUAGE=true
"""

        raise ValueError(error_msg) from e


def get_model_for_domain(domain: str) -> str:
    """Получить оптимальную модель для домена."""
    domain_models = {
        "psychology": "qwen2.5-coder-32b-instruct",
        "astrology": "qwen2.5-72b-instruct",  # Сложные символические системы
        "tarot": "qwen2.5-72b-instruct",      # Архетипическая работа
        "numerology": "qwen2.5-coder-32b-instruct",
        "wellness": "gemini-2.5-flash-lite",   # Простые программы
        "business": "qwen2.5-coder-32b-instruct"
    }
    return domain_models.get(domain, "qwen2.5-coder-32b-instruct")


def get_vak_optimization_model(vak_type: str) -> str:
    """Получить модель, оптимизированную под VAK тип."""
    vak_models = {
        "visual": "qwen2.5-72b-instruct",      # Сложные визуализации
        "auditory": "qwen2.5-coder-32b-instruct",  # Структурированные диалоги
        "kinesthetic": "qwen2.5-coder-32b-instruct",  # Практические техники
        "mixed": "qwen2.5-coder-32b-instruct"     # Универсальный подход
    }
    return vak_models.get(vak_type, "qwen2.5-coder-32b-instruct")