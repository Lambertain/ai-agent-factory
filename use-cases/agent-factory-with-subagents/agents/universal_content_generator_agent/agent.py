# -*- coding: utf-8 -*-
"""
Universal Content Generator Agent

Универсальный агент для генерации различных типов контента:
блоги, документация, маркетинговые материалы, образовательный контент,
социальные медиа, электронные письма и другие текстовые материалы.

Поддерживает адаптацию под различные домены, стили, аудитории и цели.
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model

from .dependencies import ContentGeneratorDependencies, load_dependencies
from .settings import load_settings
from .providers import get_llm_model
from .tools import (
    generate_content_outline,
    generate_content_sections,
    refine_content_style,
    optimize_content_seo,
    adapt_content_for_audience,
    validate_content_quality,
    generate_content_variations,
    extract_content_insights
)
from .prompts import get_system_prompt


# Загрузка настроек и конфигурации
settings = load_settings()
dependencies = load_dependencies()

# Создание агента с оптимизированной моделью
content_generator_agent = Agent(
    model=get_llm_model(),
    deps_type=ContentGeneratorDependencies,
    system_prompt=get_system_prompt(dependencies.__dict__)
)

# Регистрация инструментов генерации контента
content_generator_agent.tool(generate_content_outline)
content_generator_agent.tool(generate_content_sections)
content_generator_agent.tool(refine_content_style)
content_generator_agent.tool(optimize_content_seo)
content_generator_agent.tool(adapt_content_for_audience)
content_generator_agent.tool(validate_content_quality)
content_generator_agent.tool(generate_content_variations)
content_generator_agent.tool(extract_content_insights)


# === ОСНОВНЫЕ ТОЧКИ ВХОДА ===

async def run_content_generation_task(
    message: str,
    content_type: str = "blog_post",
    domain_type: str = "technology",
    target_audience: str = "professionals",
    content_style: str = "informative",
    content_length: str = "medium",
    language: str = "ukrainian",
    seo_focus: bool = True
) -> str:
    """
    Основная функция генерации контента.

    Args:
        message: Запрос на создание контента
        content_type: Тип контента (blog_post, documentation, marketing, etc.)
        domain_type: Домен контента (technology, business, health, etc.)
        target_audience: Целевая аудитория (professionals, beginners, experts, etc.)
        content_style: Стиль контента (informative, persuasive, educational, etc.)
        content_length: Длина контента (short, medium, long, comprehensive)
        language: Язык контента
        seo_focus: Фокус на SEO оптимизации

    Returns:
        Сгенерированный контент
    """
    deps = ContentGeneratorDependencies(
        api_key=settings.llm_api_key,
        project_path=settings.project_path,
        content_type=content_type,
        domain_type=domain_type,
        target_audience=target_audience,
        content_style=content_style,
        content_length=content_length,
        language=language,
        seo_optimization=seo_focus,
        agent_name="universal_content_generator",
        archon_project_id=settings.archon_project_id
    )

    try:
        result = await content_generator_agent.run(message, deps=deps)
        return str(result.data)
    except Exception as e:
        return f"Ошибка генерации контента: {str(e)}"


async def run_blog_post_generation(
    topic: str,
    keywords: List[str] = None,
    target_audience: str = "general",
    content_style: str = "engaging",
    word_count: int = 800,
    include_seo: bool = True
) -> str:
    """
    Специализированная функция для генерации блог-постов.

    Args:
        topic: Тема блог-поста
        keywords: Ключевые слова для SEO
        target_audience: Целевая аудитория
        content_style: Стиль написания
        word_count: Целевое количество слов
        include_seo: Включить SEO оптимизацию

    Returns:
        Готовый блог-пост
    """
    message = f"""
Создай блог-пост на тему: {topic}

Требования:
- Целевая аудитория: {target_audience}
- Стиль: {content_style}
- Примерное количество слов: {word_count}
- Ключевые слова: {', '.join(keywords) if keywords else 'автоматический подбор'}
- SEO оптимизация: {'включена' if include_seo else 'отключена'}
"""

    return await run_content_generation_task(
        message=message,
        content_type="blog_post",
        target_audience=target_audience,
        content_style=content_style,
        content_length="medium" if word_count <= 1000 else "long",
        seo_focus=include_seo
    )


async def run_documentation_generation(
    documentation_type: str,
    technical_level: str = "intermediate",
    framework: str = "general",
    include_examples: bool = True,
    format_style: str = "markdown"
) -> str:
    """
    Специализированная функция для генерации документации.

    Args:
        documentation_type: Тип документации (api, user_guide, technical_spec, etc.)
        technical_level: Технический уровень (beginner, intermediate, advanced)
        framework: Технологический стек
        include_examples: Включить примеры кода/использования
        format_style: Формат вывода (markdown, rst, html)

    Returns:
        Готовая документация
    """
    message = f"""
Создай {documentation_type} документацию:

Технические требования:
- Уровень сложности: {technical_level}
- Технологический стек: {framework}
- Примеры кода: {'включены' if include_examples else 'исключены'}
- Формат: {format_style}
"""

    return await run_content_generation_task(
        message=message,
        content_type="documentation",
        domain_type="technology",
        target_audience=technical_level,
        content_style="technical",
        seo_focus=False
    )


async def run_marketing_content_generation(
    campaign_type: str,
    product_category: str,
    marketing_goal: str = "awareness",
    tone: str = "professional",
    call_to_action: str = None
) -> str:
    """
    Специализированная функция для генерации маркетингового контента.

    Args:
        campaign_type: Тип кампании (email, social_media, landing_page, etc.)
        product_category: Категория продукта
        marketing_goal: Цель маркетинга (awareness, conversion, retention, etc.)
        tone: Тон коммуникации
        call_to_action: Призыв к действию

    Returns:
        Готовый маркетинговый контент
    """
    message = f"""
Создай маркетинговый контент для {campaign_type}:

Параметры кампании:
- Категория продукта: {product_category}
- Цель: {marketing_goal}
- Тон: {tone}
- Call-to-action: {call_to_action or 'подобрать автоматически'}
"""

    return await run_content_generation_task(
        message=message,
        content_type="marketing",
        domain_type="business",
        target_audience="customers",
        content_style="persuasive",
        seo_focus=True
    )


async def run_educational_content_generation(
    subject: str,
    education_level: str = "intermediate",
    learning_style: str = "visual",
    content_format: str = "structured",
    include_assessments: bool = True
) -> str:
    """
    Специализированная функция для генерации образовательного контента.

    Args:
        subject: Предмет/тема обучения
        education_level: Уровень образования (beginner, intermediate, advanced)
        learning_style: Стиль обучения (visual, auditory, kinesthetic, reading)
        content_format: Формат контента (structured, narrative, interactive)
        include_assessments: Включить задания/тесты

    Returns:
        Готовый образовательный контент
    """
    message = f"""
Создай образовательный контент по теме: {subject}

Образовательные параметры:
- Уровень: {education_level}
- Стиль обучения: {learning_style}
- Формат: {content_format}
- Задания/тесты: {'включены' if include_assessments else 'исключены'}
"""

    return await run_content_generation_task(
        message=message,
        content_type="educational",
        domain_type="education",
        target_audience=education_level,
        content_style="educational",
        seo_focus=False
    )


async def run_social_media_generation(
    platform: str,
    content_theme: str,
    post_type: str = "standard",
    engagement_goal: str = "likes",
    hashtag_strategy: str = "moderate"
) -> str:
    """
    Специализированная функция для генерации контента социальных сетей.

    Args:
        platform: Социальная платформа (facebook, instagram, linkedin, twitter, etc.)
        content_theme: Тема контента
        post_type: Тип поста (standard, story, reel, carousel, etc.)
        engagement_goal: Цель вовлечения (likes, shares, comments, saves)
        hashtag_strategy: Стратегия хештегов (minimal, moderate, extensive)

    Returns:
        Готовый контент для социальных сетей
    """
    message = f"""
Создай контент для {platform}:

Параметры поста:
- Тема: {content_theme}
- Тип поста: {post_type}
- Цель вовлечения: {engagement_goal}
- Стратегия хештегов: {hashtag_strategy}
"""

    return await run_content_generation_task(
        message=message,
        content_type="social_media",
        domain_type="marketing",
        target_audience="social_users",
        content_style="engaging",
        seo_focus=True
    )


# === УТИЛИТЫ ===

async def get_content_suggestions(
    content_type: str,
    domain: str,
    audience: str
) -> Dict[str, List[str]]:
    """
    Получить предложения по контенту для указанных параметров.

    Args:
        content_type: Тип контента
        domain: Домен
        audience: Аудитория

    Returns:
        Словарь с предложениями тем, стилей, форматов
    """
    deps = ContentGeneratorDependencies(
        api_key=settings.llm_api_key,
        content_type=content_type,
        domain_type=domain,
        target_audience=audience
    )

    suggestions_prompt = f"""
Предложи варианты контента для:
- Тип: {content_type}
- Домен: {domain}
- Аудитория: {audience}

Нужны предложения:
1. 5 актуальных тем
2. 3 подходящих стиля написания
3. 3 эффективных формата контента
"""

    try:
        result = await content_generator_agent.run(suggestions_prompt, deps=deps)
        # Парсинг результата в структурированный формат
        suggestions = {
            "topics": [],
            "styles": [],
            "formats": []
        }

        content = str(result.data)
        # Простой парсинг - в реальной реализации можно использовать более сложную логику
        lines = content.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if 'темы' in line.lower() or 'topics' in line.lower():
                current_section = "topics"
            elif 'стиль' in line.lower() or 'style' in line.lower():
                current_section = "styles"
            elif 'формат' in line.lower() or 'format' in line.lower():
                current_section = "formats"
            elif line.startswith(('-', '•', '*')) and current_section:
                suggestions[current_section].append(line[1:].strip())

        return suggestions
    except Exception as e:
        return {
            "topics": [f"Ошибка получения предложений: {e}"],
            "styles": [],
            "formats": []
        }


async def validate_content_requirements(
    content: str,
    requirements: Dict[str, Any]
) -> Dict[str, bool]:
    """
    Валидировать контент на соответствие требованиям.

    Args:
        content: Контент для проверки
        requirements: Требования к контенту

    Returns:
        Результаты валидации
    """
    validation_results = {}

    # Проверка длины
    if "min_words" in requirements:
        word_count = len(content.split())
        validation_results["min_words"] = word_count >= requirements["min_words"]

    if "max_words" in requirements:
        word_count = len(content.split())
        validation_results["max_words"] = word_count <= requirements["max_words"]

    # Проверка ключевых слов
    if "keywords" in requirements:
        content_lower = content.lower()
        keyword_found = any(keyword.lower() in content_lower for keyword in requirements["keywords"])
        validation_results["keywords"] = keyword_found

    # Проверка структуры
    if "required_sections" in requirements:
        sections_found = all(section.lower() in content.lower() for section in requirements["required_sections"])
        validation_results["required_sections"] = sections_found

    return validation_results


# === ЭКСПОРТ ===

__all__ = [
    "content_generator_agent",
    "run_content_generation_task",
    "run_blog_post_generation",
    "run_documentation_generation",
    "run_marketing_content_generation",
    "run_educational_content_generation",
    "run_social_media_generation",
    "get_content_suggestions",
    "validate_content_requirements"
]