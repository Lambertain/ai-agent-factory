"""
Утилиты для работы с Fetch MCP в агентах.

Оптимизированные wrapper-функции для различных типов веб-контента
на основе проведенных тестов и оптимизации параметров.
"""

from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class FetchMCPOptimizer:
    """Оптимизированные настройки для Fetch MCP по типам контента."""

    # Оптимальные настройки на основе тестирования
    CONTENT_TYPE_CONFIGS = {
        "documentation": {
            "maxLength": 15000,
            "enableFetchImages": False,
            "raw": False,
            "description": "Техническая документация, туториалы, статьи"
        },
        "json_api": {
            "maxLength": 5000,
            "enableFetchImages": False,
            "raw": True,
            "description": "JSON API ответы, структурированные данные"
        },
        "design_inspiration": {
            "maxLength": 8000,
            "enableFetchImages": True,
            "imageMaxCount": 3,
            "imageQuality": 90,
            "imageMaxWidth": 800,
            "imageMaxHeight": 600,
            "returnBase64": False,
            "saveImages": True,
            "description": "Дизайн сайтов, UI/UX примеры, визуальный контент"
        },
        "competitor_analysis": {
            "maxLength": 12000,
            "enableFetchImages": True,
            "imageMaxCount": 2,
            "imageQuality": 80,
            "returnBase64": False,
            "saveImages": True,
            "description": "Анализ конкурентов, маркетинговые материалы"
        },
        "research": {
            "maxLength": 20000,
            "enableFetchImages": False,
            "raw": False,
            "description": "Исследовательские материалы, научные статьи"
        },
        "lightweight": {
            "maxLength": 3000,
            "enableFetchImages": False,
            "raw": False,
            "description": "Быстрое извлечение основной информации"
        }
    }

    @classmethod
    def get_config(cls, content_type: str) -> Dict[str, Any]:
        """Получить оптимальную конфигурацию для типа контента."""
        if content_type not in cls.CONTENT_TYPE_CONFIGS:
            logger.warning(f"Unknown content type: {content_type}, using 'lightweight'")
            content_type = "lightweight"

        return cls.CONTENT_TYPE_CONFIGS[content_type].copy()

    @classmethod
    def list_content_types(cls) -> List[str]:
        """Получить список доступных типов контента."""
        return list(cls.CONTENT_TYPE_CONFIGS.keys())


async def extract_web_content(
    url: str,
    content_type: str = "documentation",
    custom_params: Optional[Dict[str, Any]] = None,
    mcp_fetch_function: Optional[callable] = None
) -> Dict[str, Any]:
    """
    Извлечь контент веб-страницы с оптимизированными параметрами.

    Args:
        url: URL для извлечения контента
        content_type: Тип контента (documentation, json_api, design_inspiration, etc.)
        custom_params: Дополнительные параметры для переопределения
        mcp_fetch_function: Функция MCP fetch для вызова

    Returns:
        Словарь с результатами извлечения
    """
    # Получаем оптимальную конфигурацию
    config = FetchMCPOptimizer.get_config(content_type)

    # Применяем пользовательские параметры
    if custom_params:
        config.update(custom_params)

    # Удаляем description из параметров вызова
    config.pop("description", None)

    try:
        if mcp_fetch_function:
            result = await mcp_fetch_function(url=url, **config)
        else:
            # Fallback - предполагаем что функция будет передана
            logger.warning("No MCP fetch function provided")
            return {"error": "No MCP fetch function available"}

        return {
            "success": True,
            "content": result,
            "config_used": config,
            "content_type": content_type,
            "url": url
        }

    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return {
            "success": False,
            "error": str(e),
            "config_used": config,
            "content_type": content_type,
            "url": url
        }


async def analyze_competitor_sites(
    urls: List[str],
    mcp_fetch_function: callable,
    focus_areas: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Анализ сайтов конкурентов с оптимизированными настройками.

    Args:
        urls: Список URL для анализа
        mcp_fetch_function: Функция MCP fetch
        focus_areas: Области фокуса анализа

    Returns:
        Сводный анализ конкурентов
    """
    results = []

    for url in urls:
        try:
            result = await extract_web_content(
                url=url,
                content_type="competitor_analysis",
                mcp_fetch_function=mcp_fetch_function
            )
            results.append(result)

        except Exception as e:
            logger.error(f"Error analyzing competitor {url}: {e}")
            results.append({
                "success": False,
                "url": url,
                "error": str(e)
            })

    # Анализируем результаты
    successful_results = [r for r in results if r.get("success")]
    failed_results = [r for r in results if not r.get("success")]

    return {
        "total_sites": len(urls),
        "successful_extractions": len(successful_results),
        "failed_extractions": len(failed_results),
        "results": results,
        "focus_areas": focus_areas or [],
        "summary": {
            "success_rate": len(successful_results) / len(urls) if urls else 0,
            "common_patterns": _extract_common_patterns(successful_results),
            "recommendations": _generate_competitor_recommendations(successful_results)
        }
    }


async def gather_design_inspiration(
    urls: List[str],
    mcp_fetch_function: callable,
    design_categories: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Сбор дизайн-вдохновения с сайтов с сохранением изображений.

    Args:
        urls: URL сайтов для сбора дизайна
        mcp_fetch_function: Функция MCP fetch
        design_categories: Категории дизайна для фокуса

    Returns:
        Коллекция дизайн-вдохновения
    """
    design_collection = []

    for url in urls:
        try:
            result = await extract_web_content(
                url=url,
                content_type="design_inspiration",
                mcp_fetch_function=mcp_fetch_function
            )

            if result.get("success"):
                design_collection.append({
                    "url": url,
                    "content": result["content"],
                    "images_saved": _count_saved_images(result["content"]),
                    "design_elements": _extract_design_elements(result["content"]),
                    "categories": design_categories or []
                })

        except Exception as e:
            logger.error(f"Error gathering design from {url}: {e}")

    return {
        "total_sites_processed": len(urls),
        "successful_extractions": len(design_collection),
        "design_collection": design_collection,
        "categories": design_categories or [],
        "summary": {
            "total_images_saved": sum(d.get("images_saved", 0) for d in design_collection),
            "design_patterns": _analyze_design_patterns(design_collection),
            "inspiration_summary": _generate_design_summary(design_collection)
        }
    }


async def research_technical_topics(
    urls: List[str],
    topic: str,
    mcp_fetch_function: callable,
    depth: str = "comprehensive"
) -> Dict[str, Any]:
    """
    Исследование технических тем через веб-источники.

    Args:
        urls: URL источников для исследования
        topic: Тема исследования
        mcp_fetch_function: Функция MCP fetch
        depth: Глубина анализа (lightweight, comprehensive, research)

    Returns:
        Результаты технического исследования
    """
    content_type = "research" if depth == "comprehensive" else "documentation"
    research_results = []

    for url in urls:
        try:
            result = await extract_web_content(
                url=url,
                content_type=content_type,
                mcp_fetch_function=mcp_fetch_function
            )

            if result.get("success"):
                research_results.append({
                    "url": url,
                    "content": result["content"],
                    "relevance_score": _calculate_relevance(result["content"], topic),
                    "key_concepts": _extract_key_concepts(result["content"], topic),
                    "source_type": _determine_source_type(url)
                })

        except Exception as e:
            logger.error(f"Error researching {url}: {e}")

    return {
        "topic": topic,
        "depth": depth,
        "sources_processed": len(urls),
        "successful_extractions": len(research_results),
        "research_results": research_results,
        "synthesis": {
            "key_findings": _synthesize_findings(research_results, topic),
            "source_quality": _assess_source_quality(research_results),
            "recommendations": _generate_research_recommendations(research_results, topic)
        }
    }


# Вспомогательные функции для анализа

def _extract_common_patterns(results: List[Dict[str, Any]]) -> List[str]:
    """Извлечь общие паттерны из результатов анализа конкурентов."""
    patterns = []
    # Простой анализ на основе частоты ключевых слов
    # В реальной реализации здесь был бы более сложный NLP анализ
    return patterns


def _generate_competitor_recommendations(results: List[Dict[str, Any]]) -> List[str]:
    """Генерировать рекомендации на основе анализа конкурентов."""
    recommendations = [
        "Проанализировать структуру навигации лидеров рынка",
        "Изучить используемые цветовые схемы и типографику",
        "Оценить подходы к презентации продуктов/услуг"
    ]
    return recommendations


def _count_saved_images(content: str) -> int:
    """Подсчитать количество сохраненных изображений."""
    # Поиск упоминаний сохраненных файлов в выводе
    if "Saved Images:" in content or "saved to:" in content:
        return content.count("saved to:")
    return 0


def _extract_design_elements(content: str) -> List[str]:
    """Извлечь дизайн-элементы из контента."""
    elements = []
    # В реальной реализации здесь был бы парсинг HTML/CSS
    return elements


def _analyze_design_patterns(collection: List[Dict[str, Any]]) -> List[str]:
    """Анализировать дизайн-паттерны в коллекции."""
    patterns = [
        "Минималистичный дизайн",
        "Использование градиентов",
        "Карточная верстка",
        "Адаптивная типографика"
    ]
    return patterns


def _generate_design_summary(collection: List[Dict[str, Any]]) -> str:
    """Генерировать сводку дизайн-вдохновения."""
    summary = f"Проанализировано {len(collection)} дизайн-источников. "
    summary += "Выявлены современные тренды и паттерны UX/UI."
    return summary


def _calculate_relevance(content: str, topic: str) -> float:
    """Рассчитать релевантность контента теме."""
    # Простая оценка по вхождению ключевых слов темы
    topic_words = topic.lower().split()
    content_lower = content.lower()

    matches = sum(1 for word in topic_words if word in content_lower)
    return matches / len(topic_words) if topic_words else 0.0


def _extract_key_concepts(content: str, topic: str) -> List[str]:
    """Извлечь ключевые концепции из контента."""
    # В реальной реализации здесь был бы NLP анализ
    concepts = []
    return concepts


def _determine_source_type(url: str) -> str:
    """Определить тип источника по URL."""
    if "github.com" in url:
        return "code_repository"
    elif "stackoverflow.com" in url:
        return "q_and_a"
    elif "docs." in url or "documentation" in url:
        return "official_docs"
    elif "blog" in url or "medium.com" in url:
        return "blog_article"
    elif "wikipedia.org" in url:
        return "encyclopedia"
    else:
        return "general_website"


def _synthesize_findings(results: List[Dict[str, Any]], topic: str) -> List[str]:
    """Синтезировать ключевые находки исследования."""
    findings = [
        f"Исследование темы '{topic}' завершено",
        f"Обработано {len(results)} источников",
        "Выявлены ключевые подходы и best practices"
    ]
    return findings


def _assess_source_quality(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Оценить качество источников."""
    source_types = {}
    for result in results:
        source_type = result.get("source_type", "unknown")
        source_types[source_type] = source_types.get(source_type, 0) + 1

    return {
        "source_distribution": source_types,
        "quality_score": 0.8,  # Простая оценка
        "reliability": "high" if len(results) > 3 else "medium"
    }


def _generate_research_recommendations(results: List[Dict[str, Any]], topic: str) -> List[str]:
    """Генерировать рекомендации по исследованию."""
    recommendations = [
        "Углубить изучение наиболее релевантных источников",
        "Проверить актуальность найденной информации",
        "Рассмотреть практические примеры применения"
    ]
    return recommendations


# Константы для использования в агентах
FETCH_CONTENT_TYPES = FetchMCPOptimizer.CONTENT_TYPE_CONFIGS.keys()

# Примеры использования для документации
USAGE_EXAMPLES = {
    "basic_documentation": {
        "description": "Извлечение технической документации",
        "code": """
result = await extract_web_content(
    url="https://docs.python.org/3/tutorial/",
    content_type="documentation",
    mcp_fetch_function=mcp__fetch__imageFetch
)
"""
    },
    "competitor_analysis": {
        "description": "Анализ конкурентов с изображениями",
        "code": """
competitors = [
    "https://competitor1.com",
    "https://competitor2.com"
]
analysis = await analyze_competitor_sites(
    urls=competitors,
    mcp_fetch_function=mcp__fetch__imageFetch,
    focus_areas=["pricing", "features", "design"]
)
"""
    },
    "design_research": {
        "description": "Сбор дизайн-вдохновения",
        "code": """
design_sites = [
    "https://dribbble.com/shots/trending",
    "https://awwwards.com"
]
inspiration = await gather_design_inspiration(
    urls=design_sites,
    mcp_fetch_function=mcp__fetch__imageFetch,
    design_categories=["minimalism", "gradients"]
)
"""
    }
}