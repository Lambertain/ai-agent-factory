# -*- coding: utf-8 -*-
"""
Universal Content Generator Agent - Инструменты

Набор инструментов для генерации, оптимизации и адаптации различных типов контента.
"""

import asyncio
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json

from pydantic_ai import RunContext
from .dependencies import ContentGeneratorDependencies


async def generate_content_outline(
    ctx: RunContext[ContentGeneratorDependencies],
    topic: str,
    content_type: str = None,
    target_length: str = None,
    include_seo_structure: bool = True
) -> str:
    """
    Создать структуру/план контента.

    Args:
        topic: Тема контента
        content_type: Тип контента (опционально, используется из deps)
        target_length: Целевая длина (опционально)
        include_seo_structure: Включить SEO-оптимизированную структуру

    Returns:
        Детальный план контента
    """
    content_type = content_type or ctx.deps.content_type
    target_length = target_length or ctx.deps.content_length

    try:
        outline_prompt = f"""
Создай детальную структуру контента:

Тема: {topic}
Тип контента: {content_type}
Целевая длина: {target_length}
Целевая аудитория: {ctx.deps.target_audience}
Домен: {ctx.deps.domain_type}
Стиль: {ctx.deps.content_style}

Требования к структуре:
{'- SEO-оптимизированные заголовки (H1, H2, H3)' if include_seo_structure else ''}
- Логический поток информации
- Четкие разделы и подразделы
- Ключевые моменты для каждого раздела
- Рекомендуемое количество слов для каждой секции

Дополнительные элементы:
{'- Введение с хуком' if ctx.deps.include_introduction else ''}
{'- Заключение с призывом к действию' if ctx.deps.include_conclusion else ''}
{'- SEO-элементы (мета-описание, ключевые слова)' if ctx.deps.seo_optimization else ''}

Пожалуйста, создай подробную структуру с описанием каждого раздела.
"""

        return outline_prompt

    except Exception as e:
        return f"Ошибка создания плана контента: {e}"


async def generate_content_sections(
    ctx: RunContext[ContentGeneratorDependencies],
    outline: str,
    section_name: str,
    section_requirements: Dict[str, Any] = None
) -> str:
    """
    Генерировать конкретную секцию контента на основе плана.

    Args:
        outline: Общий план контента
        section_name: Название секции для генерации
        section_requirements: Специфические требования к секции

    Returns:
        Готовая секция контента
    """
    try:
        requirements = section_requirements or {}
        word_count = requirements.get("word_count", "200-400 слов")
        key_points = requirements.get("key_points", [])
        style_notes = requirements.get("style_notes", "")

        section_prompt = f"""
Напиши секцию '{section_name}' на основе следующего плана:

ОБЩИЙ ПЛАН:
{outline}

ТРЕБОВАНИЯ К СЕКЦИИ:
- Объем: {word_count}
- Стиль: {ctx.deps.content_style}
- Тон: {ctx.deps.tone_formality}
- Аудитория: {ctx.deps.target_audience}
- Домен: {ctx.deps.domain_type}

{'КЛЮЧЕВЫЕ МОМЕНТЫ:' if key_points else ''}
{chr(10).join(f'- {point}' for point in key_points)}

{'СТИЛИСТИЧЕСКИЕ ЗАМЕЧАНИЯ:' if style_notes else ''}
{style_notes}

ДОПОЛНИТЕЛЬНЫЕ ТРЕБОВАНИЯ:
{'- Включить SEO-ключевые слова естественно' if ctx.deps.seo_optimization else ''}
{'- Адаптировать под культурный контекст: ' + ctx.deps.regional_preferences if ctx.deps.cultural_adaptation else ''}
{'- Использовать элементы storytelling' if ctx.deps.storytelling_elements else ''}
{'- Поддерживать читабельность: ' + ctx.deps.readability_level if ctx.deps.readability_level else ''}

Создай качественную, завершенную секцию контента.
"""

        return section_prompt

    except Exception as e:
        return f"Ошибка генерации секции контента: {e}"


async def refine_content_style(
    ctx: RunContext[ContentGeneratorDependencies],
    content: str,
    target_style: str = None,
    style_adjustments: Dict[str, Any] = None
) -> str:
    """
    Адаптировать стиль контента под требования.

    Args:
        content: Исходный контент
        target_style: Желаемый стиль (опционально)
        style_adjustments: Конкретные стилистические изменения

    Returns:
        Контент с адаптированным стилем
    """
    try:
        target_style = target_style or ctx.deps.content_style
        adjustments = style_adjustments or {}

        style_prompt = f"""
Адаптируй следующий контент под требуемый стиль:

ИСХОДНЫЙ КОНТЕНТ:
{content}

ЦЕЛЕВОЙ СТИЛЬ: {target_style}
ФОРМАЛЬНОСТЬ: {ctx.deps.tone_formality}
КРЕАТИВНОСТЬ: {ctx.deps.creativity_level}
АУДИТОРИЯ: {ctx.deps.target_audience}

СТИЛИСТИЧЕСКИЕ КОРРЕКТИРОВКИ:
{'- Уровень юмора: ' + ctx.deps.humor_usage if ctx.deps.humor_usage != 'none' else ''}
{'- Личные анекдоты: включены' if ctx.deps.personal_anecdotes else ''}
{'- Storytelling элементы: включены' if ctx.deps.storytelling_elements else ''}

СПЕЦИФИЧЕСКИЕ ИЗМЕНЕНИЯ:
{chr(10).join(f'- {key}: {value}' for key, value in adjustments.items())}

КАЧЕСТВЕННЫЕ ТРЕБОВАНИЯ:
- Сохранить основное сообщение и информацию
- Адаптировать тон и манеру изложения
- Улучшить читабельность и вовлечение
- Поддержать единообразие стиля по всему тексту

Перепиши контент с учетом всех требований.
"""

        return style_prompt

    except Exception as e:
        return f"Ошибка адаптации стиля: {e}"


async def optimize_content_seo(
    ctx: RunContext[ContentGeneratorDependencies],
    content: str,
    primary_keyword: str = None,
    secondary_keywords: List[str] = None,
    meta_requirements: Dict[str, Any] = None
) -> str:
    """
    Оптимизировать контент для поисковых систем.

    Args:
        content: Исходный контент
        primary_keyword: Основное ключевое слово
        secondary_keywords: Дополнительные ключевые слова
        meta_requirements: Требования к мета-элементам

    Returns:
        SEO-оптимизированный контент с мета-данными
    """
    if not ctx.deps.seo_optimization:
        return content

    try:
        primary_keyword = primary_keyword or ctx.deps.seo_primary_keyword
        secondary_keywords = secondary_keywords or ctx.deps.seo_secondary_keywords
        meta_reqs = meta_requirements or {}

        seo_prompt = f"""
Оптимизируй следующий контент для SEO:

ИСХОДНЫЙ КОНТЕНТ:
{content}

SEO ПАРАМЕТРЫ:
- Основное ключевое слово: {primary_keyword}
- Дополнительные ключевые слова: {', '.join(secondary_keywords) if secondary_keywords else 'автоподбор'}
- Язык: {ctx.deps.language}
- Целевая аудитория: {ctx.deps.target_audience}

ТРЕБОВАНИЯ К ОПТИМИЗАЦИИ:
1. Заголовки (H1, H2, H3):
   - H1 должен содержать основное ключевое слово
   - H2/H3 должны включать связанные термины
   - Логическая иерархия заголовков

2. Распределение ключевых слов:
   - Плотность основного КС: 1-2%
   - Естественное включение в текст
   - Использование синонимов и вариаций

3. Мета-элементы:
   {'- Мета-описание (150-160 символов)' if ctx.deps.seo_meta_description else ''}
   - Title tag (оптимальная длина)
   - Alt-тексты для изображений (если упоминаются)

4. Структурные элементы:
   - Списки и подзаголовки
   - Внутренние ссылки (предложения)
   - FAQ секция (если применимо)

5. Читабельность:
   - Короткие предложения и абзацы
   - Использование переходных слов
   - Четкая структура

ДОПОЛНИТЕЛЬНЫЕ ТРЕБОВАНИЯ:
{chr(10).join(f'- {key}: {value}' for key, value in meta_reqs.items())}

Создай SEO-оптимизированную версию контента с сохранением качества и естественности.
"""

        return seo_prompt

    except Exception as e:
        return f"Ошибка SEO оптимизации: {e}"


async def adapt_content_for_audience(
    ctx: RunContext[ContentGeneratorDependencies],
    content: str,
    target_audience: str = None,
    audience_characteristics: Dict[str, Any] = None
) -> str:
    """
    Адаптировать контент под конкретную аудиторию.

    Args:
        content: Исходный контент
        target_audience: Целевая аудитория
        audience_characteristics: Характеристики аудитории

    Returns:
        Адаптированный контент
    """
    try:
        target_audience = target_audience or ctx.deps.target_audience
        characteristics = audience_characteristics or {}

        adaptation_prompt = f"""
Адаптируй контент под целевую аудиторию:

ИСХОДНЫЙ КОНТЕНТ:
{content}

ЦЕЛЕВАЯ АУДИТОРИЯ: {target_audience}

ХАРАКТЕРИСТИКИ АУДИТОРИИ:
- Уровень экспертизы: {ctx.deps.readability_level}
- Домен интересов: {ctx.deps.domain_type}
- Предпочитаемый стиль: {ctx.deps.content_style}
- Культурный контекст: {ctx.deps.regional_preferences if ctx.deps.cultural_adaptation else 'универсальный'}

ДОПОЛНИТЕЛЬНЫЕ ХАРАКТЕРИСТИКИ:
{chr(10).join(f'- {key}: {value}' for key, value in characteristics.items())}

АДАПТАЦИОННЫЕ ТРЕБОВАНИЯ:

1. Языковая адаптация:
   - Уровень сложности терминологии
   - Использование жаргона и профессиональных терминов
   - Длина предложений и структура

2. Контентная адаптация:
   - Примеры и кейсы, релевантные аудитории
   - Уровень детализации объяснений
   - Фокус на интересах и проблемах аудитории

3. Культурная адаптация:
   {'- Местные ссылки и контекст' if ctx.deps.cultural_adaptation else ''}
   {'- Региональные особенности: ' + ctx.deps.regional_preferences if ctx.deps.cultural_adaptation else ''}
   {'- Локальные примеры и валюта' if ctx.deps.local_references else ''}

4. Стилистическая адаптация:
   - Тон коммуникации
   - Формальность обращения
   - Эмоциональная окраска

Создай версию контента, максимально релевантную целевой аудитории.
"""

        return adaptation_prompt

    except Exception as e:
        return f"Ошибка адаптации для аудитории: {e}"


async def validate_content_quality(
    ctx: RunContext[ContentGeneratorDependencies],
    content: str,
    quality_criteria: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Валидировать качество контента по различным критериям.

    Args:
        content: Контент для проверки
        quality_criteria: Дополнительные критерии качества

    Returns:
        Результаты валидации и рекомендации
    """
    try:
        criteria = quality_criteria or {}
        validation_results = {}

        # Основные метрики
        word_count = len(content.split())
        char_count = len(content)
        paragraph_count = len([p for p in content.split('\n\n') if p.strip()])
        sentence_count = len([s for s in re.split(r'[.!?]+', content) if s.strip()])

        # Базовые проверки
        validation_results.update({
            "word_count": word_count,
            "character_count": char_count,
            "paragraph_count": paragraph_count,
            "sentence_count": sentence_count,
            "avg_words_per_sentence": round(word_count / max(sentence_count, 1), 1),
            "avg_sentences_per_paragraph": round(sentence_count / max(paragraph_count, 1), 1)
        })

        # Проверка структуры
        has_headings = bool(re.search(r'^#+\s', content, re.MULTILINE))
        has_lists = bool(re.search(r'^\s*[-*+]\s', content, re.MULTILINE))
        has_numbered_lists = bool(re.search(r'^\s*\d+\.\s', content, re.MULTILINE))

        validation_results.update({
            "has_headings": has_headings,
            "has_lists": has_lists,
            "has_numbered_lists": has_numbered_lists,
            "well_structured": has_headings and (has_lists or has_numbered_lists)
        })

        # SEO проверки (если включено)
        if ctx.deps.seo_optimization:
            primary_keyword = ctx.deps.seo_primary_keyword
            if primary_keyword:
                keyword_count = content.lower().count(primary_keyword.lower())
                keyword_density = (keyword_count / word_count) * 100 if word_count > 0 else 0

                validation_results.update({
                    "primary_keyword_count": keyword_count,
                    "keyword_density": round(keyword_density, 2),
                    "optimal_keyword_density": 1.0 <= keyword_density <= 2.5
                })

        # Проверка читабельности
        long_sentences = len([s for s in re.split(r'[.!?]+', content)
                             if len(s.split()) > 20])

        validation_results.update({
            "long_sentences_count": long_sentences,
            "readability_good": validation_results["avg_words_per_sentence"] <= 20
        })

        # Проверка соответствия требованиям длины
        length_targets = {
            "short": (100, 500),
            "medium": (500, 1500),
            "long": (1500, 3000),
            "comprehensive": (3000, 10000)
        }

        if ctx.deps.content_length in length_targets:
            min_words, max_words = length_targets[ctx.deps.content_length]
            validation_results.update({
                "length_appropriate": min_words <= word_count <= max_words,
                "length_target": f"{min_words}-{max_words} слов",
                "length_status": "соответствует" if min_words <= word_count <= max_words else "не соответствует"
            })

        # Общая оценка качества
        quality_score = 0
        max_score = 0

        # Критерии оценки
        quality_checks = [
            ("well_structured", 25),
            ("readability_good", 20),
            ("length_appropriate", 15),
            ("has_headings", 10),
            ("has_lists", 10)
        ]

        if ctx.deps.seo_optimization and "optimal_keyword_density" in validation_results:
            quality_checks.append(("optimal_keyword_density", 20))

        for check, points in quality_checks:
            max_score += points
            if validation_results.get(check, False):
                quality_score += points

        validation_results.update({
            "quality_score": quality_score,
            "max_possible_score": max_score,
            "quality_percentage": round((quality_score / max_score) * 100, 1) if max_score > 0 else 0
        })

        # Рекомендации по улучшению
        recommendations = []

        if not validation_results.get("well_structured", False):
            recommendations.append("Добавить заголовки и списки для улучшения структуры")

        if not validation_results.get("readability_good", False):
            recommendations.append("Сократить длину предложений для лучшей читабельности")

        if not validation_results.get("length_appropriate", False):
            recommendations.append(f"Скорректировать длину контента до {validation_results.get('length_target', 'целевого диапазона')}")

        if ctx.deps.seo_optimization and not validation_results.get("optimal_keyword_density", False):
            recommendations.append("Оптимизировать плотность ключевых слов (1-2.5%)")

        validation_results["recommendations"] = recommendations

        return validation_results

    except Exception as e:
        return {
            "error": f"Ошибка валидации контента: {e}",
            "quality_score": 0,
            "recommendations": ["Необходимо исправить ошибки валидации"]
        }


async def generate_content_variations(
    ctx: RunContext[ContentGeneratorDependencies],
    base_content: str,
    variation_types: List[str] = None,
    variation_count: int = 3
) -> Dict[str, str]:
    """
    Создать вариации контента для A/B тестирования или разных каналов.

    Args:
        base_content: Базовый контент
        variation_types: Типы вариаций (tone, length, style, format)
        variation_count: Количество вариаций

    Returns:
        Словарь с различными вариациями контента
    """
    try:
        variation_types = variation_types or ["tone", "style", "format"]
        variations = {}

        variation_configs = {
            "tone": [
                {"name": "формальный", "description": "более официальный и профессиональный тон"},
                {"name": "дружелюбный", "description": "теплый и приветливый тон"},
                {"name": "авторитетный", "description": "экспертный и уверенный тон"}
            ],
            "style": [
                {"name": "краткий", "description": "сжатый и лаконичный стиль"},
                {"name": "детальный", "description": "подробный с множеством примеров"},
                {"name": "повествовательный", "description": "сторителлинг подход"}
            ],
            "format": [
                {"name": "списочный", "description": "структурирован в виде списков и пунктов"},
                {"name": "вопрос-ответ", "description": "формат FAQ или диалога"},
                {"name": "пошаговый", "description": "четкий алгоритм действий"}
            ],
            "length": [
                {"name": "краткая_версия", "description": "сокращенная версия (50% от оригинала)"},
                {"name": "расширенная_версия", "description": "расширенная версия (+50% контента)"},
                {"name": "ультра_краткая", "description": "основные тезисы (25% от оригинала)"}
            ]
        }

        for variation_type in variation_types[:variation_count]:
            if variation_type in variation_configs:
                configs = variation_configs[variation_type]
                for i, config in enumerate(configs[:variation_count]):
                    variation_key = f"{variation_type}_{config['name']}"

                    variation_prompt = f"""
Создай вариацию контента с фокусом на: {config['description']}

ИСХОДНЫЙ КОНТЕНТ:
{base_content}

ТРЕБОВАНИЯ К ВАРИАЦИИ:
- Тип изменения: {variation_type} - {config['description']}
- Сохранить основное сообщение
- Адаптировать под {ctx.deps.target_audience}
- Поддержать стиль: {ctx.deps.content_style}
- Качество: {ctx.deps.quality_standard}

КОНКРЕТНЫЕ ИЗМЕНЕНИЯ:
{config['description']}

Создай качественную вариацию контента.
"""

                    variations[variation_key] = variation_prompt

        return variations

    except Exception as e:
        return {"error": f"Ошибка создания вариаций: {e}"}


async def extract_content_insights(
    ctx: RunContext[ContentGeneratorDependencies],
    content: str,
    insight_types: List[str] = None
) -> Dict[str, Any]:
    """
    Извлечь инсайты и аналитику из контента.

    Args:
        content: Контент для анализа
        insight_types: Типы анализа (readability, seo, engagement, structure)

    Returns:
        Детальные инсайты и рекомендации
    """
    try:
        insight_types = insight_types or ["readability", "seo", "engagement", "structure"]
        insights = {}

        # Базовая аналитика
        word_count = len(content.split())
        char_count = len(content)
        reading_time = max(1, round(word_count / 200))  # 200 слов в минуту

        insights["basic_metrics"] = {
            "word_count": word_count,
            "character_count": char_count,
            "estimated_reading_time": f"{reading_time} мин",
            "paragraphs": len([p for p in content.split('\n\n') if p.strip()])
        }

        # Анализ читабельности
        if "readability" in insight_types:
            sentences = [s for s in re.split(r'[.!?]+', content) if s.strip()]
            avg_sentence_length = word_count / len(sentences) if sentences else 0

            # Простой индекс читабельности
            readability_score = max(0, min(100, 100 - (avg_sentence_length * 2)))

            insights["readability"] = {
                "average_sentence_length": round(avg_sentence_length, 1),
                "readability_score": round(readability_score, 1),
                "readability_level": "легко" if readability_score > 70 else "средне" if readability_score > 40 else "сложно",
                "sentences_count": len(sentences)
            }

        # SEO анализ
        if "seo" in insight_types and ctx.deps.seo_optimization:
            # Анализ заголовков
            h1_count = len(re.findall(r'^#\s', content, re.MULTILINE))
            h2_count = len(re.findall(r'^##\s', content, re.MULTILINE))
            h3_count = len(re.findall(r'^###\s', content, re.MULTILINE))

            # Анализ ключевых слов
            keyword_analysis = {}
            if ctx.deps.seo_primary_keyword:
                keyword = ctx.deps.seo_primary_keyword.lower()
                keyword_count = content.lower().count(keyword)
                keyword_density = (keyword_count / word_count) * 100 if word_count > 0 else 0

                keyword_analysis = {
                    "primary_keyword": ctx.deps.seo_primary_keyword,
                    "keyword_count": keyword_count,
                    "keyword_density": round(keyword_density, 2),
                    "density_status": "оптимально" if 1.0 <= keyword_density <= 2.5 else "требует корректировки"
                }

            insights["seo"] = {
                "heading_structure": {
                    "h1_count": h1_count,
                    "h2_count": h2_count,
                    "h3_count": h3_count,
                    "good_hierarchy": h1_count == 1 and h2_count > 0
                },
                "keyword_analysis": keyword_analysis,
                "internal_links": len(re.findall(r'\[.*?\]\((?!http)', content)),
                "external_links": len(re.findall(r'\[.*?\]\(http', content))
            }

        # Анализ вовлечения
        if "engagement" in insight_types:
            # Элементы, повышающие вовлечение
            questions = len(re.findall(r'\?', content))
            exclamations = len(re.findall(r'!', content))
            lists = len(re.findall(r'^\s*[-*+]\s', content, re.MULTILINE))
            numbered_lists = len(re.findall(r'^\s*\d+\.\s', content, re.MULTILINE))

            # Эмоциональные слова (упрощенный анализ)
            emotional_words = ['отлично', 'замечательно', 'удивительно', 'важно', 'критично', 'необходимо']
            emotion_count = sum(content.lower().count(word) for word in emotional_words)

            insights["engagement"] = {
                "interactive_elements": {
                    "questions": questions,
                    "exclamations": exclamations,
                    "lists": lists + numbered_lists
                },
                "emotional_appeal": {
                    "emotional_words_count": emotion_count,
                    "emotional_density": round((emotion_count / word_count) * 100, 2) if word_count > 0 else 0
                },
                "engagement_score": min(100, (questions * 5) + (lists * 3) + (emotion_count * 2))
            }

        # Структурный анализ
        if "structure" in insight_types:
            # Анализ структуры документа
            has_intro = bool(re.search(r'(введение|introduction|вступление)', content.lower()[:500]))
            has_conclusion = bool(re.search(r'(заключение|выводы|conclusion|итог)', content.lower()[-500:]))
            has_cta = bool(re.search(r'(свяжитесь|подпишитесь|купите|узнайте больше|действуйте)', content.lower()))

            insights["structure"] = {
                "document_flow": {
                    "has_introduction": has_intro,
                    "has_conclusion": has_conclusion,
                    "has_call_to_action": has_cta
                },
                "content_balance": {
                    "intro_percentage": round((len(content[:500]) / len(content)) * 100, 1),
                    "conclusion_percentage": round((len(content[-500:]) / len(content)) * 100, 1)
                },
                "structure_score": sum([has_intro, has_conclusion, has_cta]) * 25
            }

        # Общие рекомендации
        recommendations = []

        if insights.get("readability", {}).get("readability_score", 100) < 60:
            recommendations.append("Упростить предложения для лучшей читабельности")

        if insights.get("seo", {}).get("heading_structure", {}).get("good_hierarchy", True) == False:
            recommendations.append("Улучшить структуру заголовков (H1, H2, H3)")

        if insights.get("engagement", {}).get("engagement_score", 100) < 30:
            recommendations.append("Добавить интерактивные элементы (вопросы, списки)")

        if insights.get("structure", {}).get("structure_score", 100) < 50:
            recommendations.append("Улучшить структуру документа (введение, заключение, CTA)")

        insights["recommendations"] = recommendations
        insights["analysis_timestamp"] = datetime.now().isoformat()

        return insights

    except Exception as e:
        return {
            "error": f"Ошибка анализа контента: {e}",
            "analysis_timestamp": datetime.now().isoformat()
        }


# === ПОИСК В БАЗЕ ЗНАНИЙ ===

async def search_content_knowledge(
    ctx: RunContext[ContentGeneratorDependencies],
    query: str,
    content_category: str = None,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний агента для получения экспертной информации.

    Args:
        query: Поисковый запрос
        content_category: Категория контента для фильтрации
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Формируем поисковый запрос с учетом контекста агента
        search_query = f"{query} content generation"
        if content_category:
            search_query += f" {content_category}"

        # Добавляем теги агента для фильтрации
        agent_tags = " ".join(ctx.deps.knowledge_tags)
        search_query += f" {agent_tags}"

        # Здесь должен быть вызов к Archon RAG API
        # Временная заглушка для демонстрации
        knowledge_response = f"""
Поиск знаний по запросу: {query}

Релевантная информация из базы знаний:
- Лучшие практики для типа контента: {ctx.deps.content_type}
- Рекомендации для домена: {ctx.deps.domain_type}
- Стратегии для аудитории: {ctx.deps.target_audience}

[В реальной реализации здесь будет вызов mcp__archon__rag_search_knowledge_base]
"""

        return knowledge_response

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"


# === ЭКСПОРТ ===

__all__ = [
    "generate_content_outline",
    "generate_content_sections",
    "refine_content_style",
    "optimize_content_seo",
    "adapt_content_for_audience",
    "validate_content_quality",
    "generate_content_variations",
    "extract_content_insights",
    "search_content_knowledge"
]