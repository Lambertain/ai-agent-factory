# -*- coding: utf-8 -*-
"""
Universal Localization Engine Agent

Универсальный агент для локализации и интернационализации проектов.
Поддерживает полный цикл локализации: от извлечения текста до
культурной адаптации и качественного контроля переводов.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model

from .dependencies import LocalizationEngineDependencies, load_dependencies
from .settings import load_settings
from .providers import get_llm_model
from .tools import (
    extract_translatable_content,
    translate_content_batch,
    validate_translation_quality,
    generate_locale_files,
    analyze_localization_coverage,
    optimize_translation_workflow,
    create_translation_memory,
    validate_ui_compatibility,
    generate_cultural_adaptation,
    manage_translation_projects
)
from .prompts import get_system_prompt


# Загрузка настроек и конфигурации
settings = load_settings()
dependencies = load_dependencies()

# Создание агента с оптимизированной моделью
localization_engine_agent = Agent(
    model=get_llm_model(),
    deps_type=LocalizationEngineDependencies,
    system_prompt=get_system_prompt(dependencies.__dict__)
)

# Регистрация инструментов локализации
localization_engine_agent.tool(extract_translatable_content)
localization_engine_agent.tool(translate_content_batch)
localization_engine_agent.tool(validate_translation_quality)
localization_engine_agent.tool(generate_locale_files)
localization_engine_agent.tool(analyze_localization_coverage)
localization_engine_agent.tool(optimize_translation_workflow)
localization_engine_agent.tool(create_translation_memory)
localization_engine_agent.tool(validate_ui_compatibility)
localization_engine_agent.tool(generate_cultural_adaptation)
localization_engine_agent.tool(manage_translation_projects)


# === ОСНОВНЫЕ ТОЧКИ ВХОДА ===

async def run_localization_task(
    message: str,
    source_language: str = "en",
    target_languages: List[str] = None,
    project_type: str = "web",
    translation_quality: str = "professional",
    enable_cultural_adaptation: bool = True,
    enable_ui_validation: bool = True
) -> str:
    """
    Основная функция для полной локализации проекта.

    Args:
        message: Описание задачи локализации
        source_language: Исходный язык (по умолчанию английский)
        target_languages: Список целевых языков
        project_type: Тип проекта (web, mobile, desktop, game, etc.)
        translation_quality: Уровень качества (basic, standard, professional, native)
        enable_cultural_adaptation: Включить культурную адаптацию
        enable_ui_validation: Включить валидацию UI совместимости

    Returns:
        Результат локализации проекта
    """
    if target_languages is None:
        target_languages = ["es", "fr", "de", "ru", "zh"]

    deps = LocalizationEngineDependencies(
        api_key=settings.llm_api_key,
        project_path=settings.project_path,
        source_language=source_language,
        target_languages=target_languages,
        project_type=project_type,
        translation_quality=translation_quality,
        enable_cultural_adaptation=enable_cultural_adaptation,
        ui_validation_checks={"text_overflow": enable_ui_validation},
        agent_name="universal_localization_engine",
        archon_project_id=settings.archon_project_id
    )

    try:
        result = await localization_engine_agent.run(message, deps=deps)
        return str(result.data)
    except Exception as e:
        return f"Ошибка локализации: {str(e)}"


async def run_content_extraction(
    project_path: str,
    file_patterns: List[str] = None,
    extraction_rules: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Извлечение переводимого контента из проекта.

    Args:
        project_path: Путь к проекту
        file_patterns: Паттерны файлов для сканирования
        extraction_rules: Правила извлечения контента

    Returns:
        Извлеченный контент для перевода
    """
    if file_patterns is None:
        file_patterns = ["**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx", "**/*.vue", "**/*.html"]

    if extraction_rules is None:
        extraction_rules = {
            "include_attributes": ["title", "alt", "placeholder", "aria-label"],
            "include_functions": ["t", "i18n", "translate", "$t"],
            "exclude_patterns": ["test", "node_modules", ".git"],
            "extract_comments": True
        }

    deps = LocalizationEngineDependencies(
        api_key=settings.llm_api_key,
        project_path=project_path,
        auto_text_extraction=True,
        scan_file_types=[p.replace("**/", "").replace("*", "") for p in file_patterns]
    )

    message = f"""
Извлеки весь переводимый контент из проекта: {project_path}

Паттерны файлов: {', '.join(file_patterns)}
Правила извлечения: {json.dumps(extraction_rules, indent=2)}

Создай структурированный отчет с:
1. Найденными текстовыми строками
2. Контекстом использования
3. Приоритетами перевода
4. Рекомендациями по организации
"""

    try:
        result = await localization_engine_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка извлечения контента: {str(e)}"}


async def run_batch_translation(
    content_data: Dict[str, Any],
    target_languages: List[str],
    translation_config: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Массовый перевод контента на множество языков.

    Args:
        content_data: Данные для перевода
        target_languages: Целевые языки
        translation_config: Конфигурация перевода

    Returns:
        Переведенный контент по языкам
    """
    if translation_config is None:
        translation_config = {
            "quality": "professional",
            "preserve_formatting": True,
            "context_aware": True,
            "brand_consistent": True,
            "cultural_adaptation": True
        }

    deps = LocalizationEngineDependencies(
        api_key=settings.llm_api_key,
        target_languages=target_languages,
        translation_quality=translation_config.get("quality", "professional"),
        enable_context_awareness=translation_config.get("context_aware", True),
        enable_brand_consistency=translation_config.get("brand_consistent", True),
        enable_cultural_adaptation=translation_config.get("cultural_adaptation", True)
    )

    message = f"""
Выполни массовый перевод контента на языки: {', '.join(target_languages)}

Исходные данные: {json.dumps(content_data, indent=2, ensure_ascii=False)}
Конфигурация: {json.dumps(translation_config, indent=2)}

Требования:
1. Высокое качество перевода
2. Сохранение контекста и форматирования
3. Культурная адаптация
4. Консистентность терминологии
5. Валидация результатов
"""

    try:
        result = await localization_engine_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка пакетного перевода: {str(e)}"}


async def run_quality_validation(
    translated_content: Dict[str, Any],
    validation_rules: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Валидация качества переводов.

    Args:
        translated_content: Переведенный контент
        validation_rules: Правила валидации

    Returns:
        Отчет о качестве переводов
    """
    if validation_rules is None:
        validation_rules = {
            "check_completeness": True,
            "check_consistency": True,
            "check_formatting": True,
            "check_length": True,
            "check_grammar": True,
            "check_cultural_appropriateness": True
        }

    deps = LocalizationEngineDependencies(
        api_key=settings.llm_api_key,
        quality_checks=validation_rules,
        enable_quality_checks=True
    )

    message = f"""
Проведи комплексную валидацию качества переводов.

Переведенный контент: {json.dumps(translated_content, indent=2, ensure_ascii=False)}
Правила валидации: {json.dumps(validation_rules, indent=2)}

Создай детальный отчет о:
1. Полноте переводов
2. Качестве языка
3. Консистентности терминологии
4. Культурной адекватности
5. Технических проблемах
6. Рекомендациях по улучшению
"""

    try:
        result = await localization_engine_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка валидации качества: {str(e)}"}


async def run_ui_compatibility_check(
    translated_content: Dict[str, Any],
    ui_constraints: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Проверка совместимости переводов с UI.

    Args:
        translated_content: Переведенный контент
        ui_constraints: Ограничения UI

    Returns:
        Отчет о совместимости с UI
    """
    if ui_constraints is None:
        ui_constraints = {
            "max_button_length": 20,
            "max_menu_length": 25,
            "max_tooltip_length": 100,
            "max_title_length": 50,
            "check_text_overflow": True,
            "check_rtl_support": True
        }

    deps = LocalizationEngineDependencies(
        api_key=settings.llm_api_key,
        ui_validation_checks={
            "text_overflow": ui_constraints.get("check_text_overflow", True),
            "rtl_support": ui_constraints.get("check_rtl_support", True),
            "layout_breaking": True,
            "font_support": True
        }
    )

    message = f"""
Проверь совместимость переводов с пользовательским интерфейсом.

Переведенный контент: {json.dumps(translated_content, indent=2, ensure_ascii=False)}
Ограничения UI: {json.dumps(ui_constraints, indent=2)}

Анализируй:
1. Длину текстов в различных элементах UI
2. Возможность переполнения текста
3. Поддержку RTL языков
4. Совместимость с шрифтами
5. Влияние на макет
6. Предложения по оптимизации
"""

    try:
        result = await localization_engine_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка проверки UI совместимости: {str(e)}"}


async def run_cultural_adaptation(
    content_data: Dict[str, Any],
    target_locales: List[str],
    adaptation_level: str = "standard"
) -> Dict[str, Any]:
    """
    Культурная адаптация контента для целевых локалей.

    Args:
        content_data: Исходный контент
        target_locales: Целевые локали
        adaptation_level: Уровень адаптации (basic, standard, deep)

    Returns:
        Культурно адаптированный контент
    """
    deps = LocalizationEngineDependencies(
        api_key=settings.llm_api_key,
        supported_locales={locale: {"name": locale} for locale in target_locales},
        enable_cultural_adaptation=True,
        cultural_adaptation_level=adaptation_level
    )

    message = f"""
Выполни культурную адаптацию контента для локалей: {', '.join(target_locales)}

Исходный контент: {json.dumps(content_data, indent=2, ensure_ascii=False)}
Уровень адаптации: {adaptation_level}

Адаптируй:
1. Цвета и визуальные элементы
2. Даты, числа, валюты
3. Культурные референсы
4. Социальные нормы
5. Бизнес-практики
6. Правовые требования
"""

    try:
        result = await localization_engine_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка культурной адаптации: {str(e)}"}


async def run_localization_workflow_optimization(
    project_config: Dict[str, Any],
    team_size: int = 3,
    timeline: str = "standard"
) -> Dict[str, Any]:
    """
    Оптимизация workflow локализации для команды.

    Args:
        project_config: Конфигурация проекта
        team_size: Размер команды локализации
        timeline: Временные рамки (rush, standard, extended)

    Returns:
        Оптимизированный workflow локализации
    """
    deps = LocalizationEngineDependencies(
        api_key=settings.llm_api_key,
        project_type=project_config.get("type", "web"),
        target_languages=project_config.get("languages", ["es", "fr", "de"]),
        enable_translator_workflow=True,
        enable_reviewer_workflow=True,
        version_control_integration=True,
        ci_cd_integration=True
    )

    message = f"""
Создай оптимизированный workflow локализации для проекта.

Конфигурация проекта: {json.dumps(project_config, indent=2)}
Размер команды: {team_size} человек
Временные рамки: {timeline}

Спланируй:
1. Этапы локализации
2. Распределение ролей
3. Процессы валидации
4. Инструменты и интеграции
5. Контроль качества
6. Временной план
"""

    try:
        result = await localization_engine_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка оптимизации workflow: {str(e)}"}


async def run_translation_memory_creation(
    historical_translations: Dict[str, Any],
    domain_glossaries: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Создание и оптимизация памяти переводов.

    Args:
        historical_translations: Исторические переводы
        domain_glossaries: Доменные глоссарии

    Returns:
        Оптимизированная память переводов
    """
    if domain_glossaries is None:
        domain_glossaries = {}

    deps = LocalizationEngineDependencies(
        api_key=settings.llm_api_key,
        enable_translation_memory=True,
        enable_terminology_extraction=True,
        custom_terminology=domain_glossaries
    )

    message = f"""
Создай оптимизированную память переводов на основе исторических данных.

Исторические переводы: {json.dumps(historical_translations, indent=2, ensure_ascii=False)}
Доменные глоссарии: {json.dumps(domain_glossaries, indent=2, ensure_ascii=False)}

Создай:
1. Структурированную память переводов
2. Терминологические базы
3. Правила автоматического сопоставления
4. Метрики качества совпадений
5. Рекомендации по использованию
"""

    try:
        result = await localization_engine_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка создания памяти переводов: {str(e)}"}


# === АНАЛИТИЧЕСКИЕ ФУНКЦИИ ===

async def analyze_localization_requirements(
    project_path: str,
    target_markets: List[str],
    business_goals: List[str] = None
) -> Dict[str, Any]:
    """
    Анализ требований к локализации проекта.

    Args:
        project_path: Путь к проекту
        target_markets: Целевые рынки
        business_goals: Бизнес-цели локализации

    Returns:
        Анализ требований к локализации
    """
    if business_goals is None:
        business_goals = ["market_expansion", "user_engagement", "revenue_growth"]

    deps = LocalizationEngineDependencies(
        api_key=settings.llm_api_key,
        project_path=project_path,
        target_languages=[market.split('-')[0] for market in target_markets]
    )

    message = f"""
Проанализируй требования к локализации для проекта: {project_path}

Целевые рынки: {', '.join(target_markets)}
Бизнес-цели: {', '.join(business_goals)}

Определи:
1. Объем контента для локализации
2. Приоритеты по языкам и регионам
3. Технические требования
4. Ресурсы и временные рамки
5. Бюджетные оценки
6. Риски и ограничения
"""

    try:
        result = await localization_engine_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка анализа требований: {str(e)}"}


async def create_localization_strategy(
    requirements: Dict[str, Any],
    constraints: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Создание стратегии локализации.

    Args:
        requirements: Требования к локализации
        constraints: Ограничения (бюджет, время, ресурсы)

    Returns:
        Стратегия локализации
    """
    if constraints is None:
        constraints = {
            "budget": "medium",
            "timeline": "standard",
            "team_size": "small"
        }

    deps = LocalizationEngineDependencies(
        api_key=settings.llm_api_key,
        project_type=requirements.get("project_type", "web"),
        domain_type=requirements.get("domain_type", "general")
    )

    message = f"""
Создай стратегию локализации на основе требований и ограничений.

Требования: {json.dumps(requirements, indent=2, ensure_ascii=False)}
Ограничения: {json.dumps(constraints, indent=2)}

Включи:
1. Поэтапный план локализации
2. Приоритизацию языков и контента
3. Выбор инструментов и технологий
4. Организацию команды и процессов
5. Контроль качества
6. Метрики успеха
"""

    try:
        result = await localization_engine_agent.run(message, deps=deps)
        return json.loads(str(result.data))
    except Exception as e:
        return {"error": f"Ошибка создания стратегии: {str(e)}"}


# === ЭКСПОРТ ===

__all__ = [
    "localization_engine_agent",
    "run_localization_task",
    "run_content_extraction",
    "run_batch_translation",
    "run_quality_validation",
    "run_ui_compatibility_check",
    "run_cultural_adaptation",
    "run_localization_workflow_optimization",
    "run_translation_memory_creation",
    "analyze_localization_requirements",
    "create_localization_strategy"
]