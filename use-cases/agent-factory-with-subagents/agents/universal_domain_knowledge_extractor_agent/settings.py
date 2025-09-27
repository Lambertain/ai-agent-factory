# -*- coding: utf-8 -*-
"""
Настройки для Universal Domain Knowledge Extractor Agent
Универсальная конфигурация для работы с различными доменами знаний
"""

import os
from typing import List, Dict, Any, Optional
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

class UniversalKnowledgeExtractionSettings(BaseSettings):
    """
    Универсальные настройки для извлечения знаний из любых доменов.

    Поддерживает психологию, астрологию, нумерологию, бизнес и другие области.
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # === ОСНОВНЫЕ НАСТРОЙКИ ===
    agent_name: str = Field(
        default="universal_domain_knowledge_extractor",
        description="Имя агента"
    )

    # === LLM КОНФИГУРАЦИЯ ===
    llm_api_key: str = Field(..., description="API-ключ для LLM")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL для LLM API"
    )

    # Модели для разных типов задач извлечения знаний
    llm_extraction_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для извлечения знаний"
    )
    llm_analysis_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Модель для анализа паттернов"
    )
    llm_validation_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Модель для валидации знаний"
    )

    # === ДОМЕННАЯ КОНФИГУРАЦИЯ ===
    default_domain_type: str = Field(
        default="psychology",
        description="Домен по умолчанию (psychology, astrology, numerology, business)"
    )
    default_project_type: str = Field(
        default="transformation_platform",
        description="Тип проекта по умолчанию"
    )
    default_framework: str = Field(
        default="pydantic_ai",
        description="Технологический фреймворк"
    )

    # === НАСТРОЙКИ ИЗВЛЕЧЕНИЯ ЗНАНИЙ ===
    default_extraction_depth: str = Field(
        default="comprehensive",
        description="Глубина извлечения (surface, comprehensive, expert)"
    )
    default_output_format: str = Field(
        default="modular",
        description="Формат вывода (modular, structured, narrative)"
    )
    default_validation_level: str = Field(
        default="scientific",
        description="Уровень валидации (basic, scientific, expert)"
    )

    # === ЛОКАЛИЗАЦИЯ ===
    primary_language: str = Field(
        default="ukrainian",
        description="Основной язык для извлечения знаний"
    )
    supported_languages: List[str] = Field(
        default=["ukrainian", "polish", "english"],
        description="Поддерживаемые языки"
    )

    # === RAG И KNOWLEDGE BASE ===
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )
    knowledge_base_url: str = Field(
        default="http://localhost:3737",
        description="URL Archon Knowledge Base"
    )
    default_knowledge_tags: List[str] = Field(
        default=["domain-knowledge", "knowledge-extraction", "agent-knowledge", "pydantic-ai"],
        description="Теги знаний по умолчанию"
    )

    # === ДОМЕННО-СПЕЦИФИЧНЫЕ НАСТРОЙКИ ===

    # Психология
    psychology_validation_enabled: bool = Field(
        default=True,
        description="Включить научную валидацию для психологии"
    )
    psychology_therapy_approaches: List[str] = Field(
        default=["CBT", "TA", "Ericksonian", "NLP"],
        description="Поддерживаемые терапевтические подходы"
    )
    psychology_test_types: List[str] = Field(
        default=["personality", "clinical", "behavioral"],
        description="Типы психологических тестов"
    )

    # Астрология
    astrology_house_systems: List[str] = Field(
        default=["Placidus", "Koch", "Equal"],
        description="Поддерживаемые системы домов"
    )
    astrology_cultural_systems: List[str] = Field(
        default=["Western", "Vedic", "Chinese"],
        description="Культурные астрологические системы"
    )
    astrology_calculation_precision: str = Field(
        default="high",
        description="Точность астрологических расчетов"
    )

    # Нумерология
    numerology_calculation_methods: List[str] = Field(
        default=["Pythagorean", "Chaldean", "Kabbalah"],
        description="Методы нумерологических расчетов"
    )
    numerology_analysis_types: List[str] = Field(
        default=["name_analysis", "birth_date_analysis", "compatibility_analysis"],
        description="Типы нумерологического анализа"
    )

    # Бизнес
    business_frameworks: List[str] = Field(
        default=["SWOT", "Porter", "Lean", "Agile"],
        description="Бизнес-фреймворки для анализа"
    )
    business_metrics_focus: bool = Field(
        default=True,
        description="Фокус на метриках в бизнес-анализе"
    )

    # === ПРОИЗВОДИТЕЛЬНОСТЬ И ОПТИМИЗАЦИЯ ===
    enable_caching: bool = Field(
        default=True,
        description="Включить кэширование результатов"
    )
    cache_ttl_seconds: int = Field(
        default=3600,
        description="Время жизни кэша в секундах"
    )
    max_concurrent_extractions: int = Field(
        default=5,
        description="Максимальное количество одновременных извлечений"
    )
    extraction_timeout_seconds: int = Field(
        default=300,
        description="Таймаут для операций извлечения"
    )

    # === МЕЖАГЕНТНОЕ ВЗАИМОДЕЙСТВИЕ ===
    enable_task_delegation: bool = Field(
        default=True,
        description="Включить делегирование задач другим агентам"
    )
    delegation_threshold: str = Field(
        default="medium",
        description="Порог сложности для делегирования"
    )
    auto_delegate_security_tasks: bool = Field(
        default=True,
        description="Автоматически делегировать задачи безопасности"
    )

    # === КАЧЕСТВО И ВАЛИДАЦИЯ ===
    enable_quality_checks: bool = Field(
        default=True,
        description="Включить проверки качества"
    )
    require_scientific_validation: bool = Field(
        default=True,
        description="Требовать научную валидацию"
    )
    enable_cultural_adaptation: bool = Field(
        default=True,
        description="Включить культурную адаптацию"
    )

    # === ОТЛАДКА И ЛОГИРОВАНИЕ ===
    debug_mode: bool = Field(
        default=False,
        description="Режим отладки"
    )
    log_level: str = Field(
        default="INFO",
        description="Уровень логирования"
    )
    save_extraction_logs: bool = Field(
        default=True,
        description="Сохранять логи извлечения"
    )

    def get_domain_config(self, domain_type: str) -> Dict[str, Any]:
        """Получить конфигурацию для конкретного домена."""
        domain_configs = {
            "psychology": {
                "validation_enabled": self.psychology_validation_enabled,
                "therapy_approaches": self.psychology_therapy_approaches,
                "test_types": self.psychology_test_types,
                "scientific_validation": self.require_scientific_validation
            },
            "astrology": {
                "house_systems": self.astrology_house_systems,
                "cultural_systems": self.astrology_cultural_systems,
                "calculation_precision": self.astrology_calculation_precision
            },
            "numerology": {
                "calculation_methods": self.numerology_calculation_methods,
                "analysis_types": self.numerology_analysis_types
            },
            "business": {
                "frameworks": self.business_frameworks,
                "metrics_focus": self.business_metrics_focus
            }
        }

        return domain_configs.get(domain_type, {})

    def get_model_for_task(self, task_type: str) -> str:
        """Получить модель для конкретного типа задачи."""
        task_model_mapping = {
            "extraction": self.llm_extraction_model,
            "analysis": self.llm_analysis_model,
            "validation": self.llm_validation_model,
            "complex_analysis": self.llm_analysis_model
        }

        return task_model_mapping.get(task_type, self.llm_extraction_model)

    def is_language_supported(self, language: str) -> bool:
        """Проверить поддерживается ли язык."""
        return language.lower() in [lang.lower() for lang in self.supported_languages]

def load_settings() -> UniversalKnowledgeExtractionSettings:
    """
    Загрузить настройки с проверкой обязательных параметров.

    Returns:
        Настройки агента

    Raises:
        ValueError: Если не указаны обязательные параметры
    """
    load_dotenv()

    try:
        settings = UniversalKnowledgeExtractionSettings()

        # Проверяем критически важные настройки
        if not settings.llm_api_key:
            raise ValueError("LLM_API_KEY не указан в переменных окружения")

        return settings

    except Exception as e:
        error_msg = f"Ошибка загрузки настроек: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\n\nДобавьте в файл .env:\nLLM_API_KEY=your_api_key_here"
        raise ValueError(error_msg) from e

# Глобальный экземпляр настроек
_settings_instance: Optional[UniversalKnowledgeExtractionSettings] = None

def get_settings() -> UniversalKnowledgeExtractionSettings:
    """Получить глобальный экземпляр настроек."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = load_settings()
    return _settings_instance

def reload_settings() -> UniversalKnowledgeExtractionSettings:
    """Перезагрузить настройки (полезно для тестов)."""
    global _settings_instance
    _settings_instance = None
    return get_settings()