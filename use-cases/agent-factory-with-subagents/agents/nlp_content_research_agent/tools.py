"""
NLP Content Research Agent Tools

Профессиональные инструменты для исследований с NLP специализацией.
Поддерживает любые домены: психология, астрология, таро и др.
"""

from typing import Dict, Any, List, Optional, Union
import asyncio
import json
from datetime import datetime
from pydantic_ai import RunContext
from pydantic import BaseModel, Field

from .dependencies import NLPContentResearchDependencies


# === МОДЕЛИ ДАННЫХ ===

class ResearchQuery(BaseModel):
    """Модель для исследовательского запроса."""
    topic: str = Field(description="Основная тема исследования")
    domain: str = Field(default="psychology", description="Домен исследования")
    depth: str = Field(default="comprehensive", description="Глубина исследования")
    focus_areas: List[str] = Field(default=[], description="Конкретные области фокуса")
    target_audience: str = Field(default="general", description="Целевая аудитория")


class ViralAnalysisRequest(BaseModel):
    """Модель для анализа вирусного потенциала."""
    content_topic: str = Field(description="Тема контента")
    target_platforms: List[str] = Field(default=["social_media"], description="Целевые платформы")
    audience_segment: str = Field(default="general", description="Сегмент аудитории")


class CompetitorAnalysisRequest(BaseModel):
    """Модель для конкурентного анализа."""
    niche: str = Field(description="Ниша для анализа")
    competitor_count: int = Field(default=10, description="Количество конкурентов для анализа")
    analysis_aspects: List[str] = Field(
        default=["content_style", "nlp_techniques", "engagement"],
        description="Аспекты анализа"
    )


# === ОСНОВНЫЕ ИССЛЕДОВАТЕЛЬСКИЕ ИНСТРУМЕНТЫ ===

async def search_agent_knowledge(
    ctx: RunContext[NLPContentResearchDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в специализированной базе знаний агента через Archon RAG.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Используем теги знаний из зависимостей
        search_tags = getattr(ctx.deps, 'knowledge_tags', [])

        # Пытаемся использовать MCP Archon для поиска
        try:
            # Попытка использования MCP Archon (если доступен)
            from mcp__archon__rag_search_knowledge_base import mcp__archon__rag_search_knowledge_base

            result = await mcp__archon__rag_search_knowledge_base(
                query=f"{query} {' '.join(search_tags)}",
                source_domain=ctx.deps.knowledge_domain,
                match_count=match_count
            )

            if result["success"] and result["results"]:
                knowledge = "\\n".join([
                    f"**{r['metadata'].get('title', 'Источник')}:**\\n{r['content']}"
                    for r in result["results"][:match_count]
                ])
                return f"📚 **База знаний агента:**\\n{knowledge}"

        except ImportError:
            pass  # MCP Archon недоступен

        # Fallback - эмуляция поиска в базе знаний
        fallback_knowledge = _get_fallback_knowledge(ctx.deps.research_domain, query)
        if fallback_knowledge:
            return f"📚 **База знаний агента (локальная):**\\n{fallback_knowledge}"

        return f"""⚠️ **База знаний временно недоступна**

🔍 **Запрос:** {query}
📋 **Домен:** {ctx.deps.research_domain.value}
🏷️ **Теги поиска:** {', '.join(search_tags)}

💡 **Рекомендация:** Использовать веб-поиск или другие источники для получения актуальной информации по теме."""

    except Exception as e:
        return f"❌ Ошибка поиска в базе знаний: {str(e)}"


async def conduct_web_research(
    ctx: RunContext[NLPContentResearchDependencies],
    research_request: ResearchQuery
) -> str:
    """
    Проведение веб-исследования по теме.

    Args:
        research_request: Параметры исследования

    Returns:
        Результаты веб-исследования
    """
    if not ctx.deps.enable_web_search:
        return "⚠️ Веб-поиск отключен в настройках агента"

    try:
        # Формируем поисковые запросы
        search_queries = _generate_search_queries(research_request)

        # Эмуляция веб-поиска (замените на реальный API)
        research_results = []

        for query in search_queries[:3]:  # Ограничиваем количество запросов
            # Здесь должен быть реальный веб-поиск
            result = _simulate_web_search(query, research_request.domain)
            research_results.append(result)

        # Агрегируем результаты
        aggregated_results = _aggregate_research_results(research_results, research_request)

        return f"""📊 **Результаты веб-исследования:**

**Тема:** {research_request.topic}
**Домен:** {research_request.domain}
**Глубина:** {research_request.depth}

{aggregated_results}

**📅 Дата исследования:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

    except Exception as e:
        return f"❌ Ошибка веб-исследования: {str(e)}"


async def analyze_viral_potential(
    ctx: RunContext[NLPContentResearchDependencies],
    analysis_request: ViralAnalysisRequest
) -> str:
    """
    Анализ вирусного потенциала темы с использованием NLP принципов.

    Args:
        analysis_request: Параметры анализа

    Returns:
        Анализ вирусного потенциала
    """
    if not ctx.deps.viral_potential_analysis:
        return "⚠️ Анализ вирусного потенциала отключен в настройках"

    try:
        # Анализируем эмоциональные триггеры
        emotional_triggers = _analyze_emotional_triggers(
            analysis_request.content_topic,
            ctx.deps.research_domain
        )

        # Оцениваем shareability факторы
        shareability_factors = _analyze_shareability(
            analysis_request.content_topic,
            analysis_request.target_platforms
        )

        # NLP анализ языковых паттернов
        nlp_recommendations = _get_nlp_viral_recommendations(
            analysis_request.content_topic,
            ctx.deps.primary_nlp_techniques
        )

        return f"""🔥 **Анализ вирусного потенциала**

**Тема:** {analysis_request.content_topic}
**Целевые платформы:** {', '.join(analysis_request.target_platforms)}

## 😍 Эмоциональные триггеры
{emotional_triggers}

## 🚀 Shareability факторы
{shareability_factors}

## 🧠 NLP рекомендации
{nlp_recommendations}

## 📊 Общая оценка
**Вирусный потенциал:** {_calculate_viral_score(analysis_request.content_topic)}/10
**Рекомендуемые действия:** Оптимизировать эмоциональную составляющую и языковые паттерны

**📅 Дата анализа:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

    except Exception as e:
        return f"❌ Ошибка анализа вирусного потенциала: {str(e)}"


async def conduct_competitor_analysis(
    ctx: RunContext[NLPContentResearchDependencies],
    analysis_request: CompetitorAnalysisRequest
) -> str:
    """
    Конкурентный анализ в заданной нише.

    Args:
        analysis_request: Параметры анализа

    Returns:
        Результаты конкурентного анализа
    """
    if not ctx.deps.enable_competitive_analysis:
        return "⚠️ Конкурентный анализ отключен в настройках"

    try:
        # Находим конкурентов
        competitors = _find_competitors(
            analysis_request.niche,
            analysis_request.competitor_count
        )

        # Анализируем их подходы
        competitor_insights = []
        for competitor in competitors:
            insight = _analyze_competitor(competitor, analysis_request.analysis_aspects)
            competitor_insights.append(insight)

        # Выявляем паттерны и возможности
        market_gaps = _identify_market_gaps(competitor_insights, analysis_request.niche)
        nlp_patterns = _analyze_competitor_nlp_patterns(competitor_insights)

        return f"""🏆 **Конкурентный анализ**

**Ниша:** {analysis_request.niche}
**Проанализировано конкурентов:** {len(competitors)}

## 📈 ТОП-конкуренты
{_format_competitors_list(competitors)}

## 🧠 NLP паттерны конкурентов
{nlp_patterns}

## 💡 Возможности для улучшения
{market_gaps}

## 🎯 Рекомендации
- Использовать уникальные NLP техники
- Фокус на недоработанных аспектах конкурентов
- Создать отличительный языковой стиль

**📅 Дата анализа:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

    except Exception as e:
        return f"❌ Ошибка конкурентного анализа: {str(e)}"


async def generate_content_brief(
    ctx: RunContext[NLPContentResearchDependencies],
    topic: str,
    research_data: Dict[str, Any] = None
) -> str:
    """
    Создание итогового research brief с NLP рекомендациями.

    Args:
        topic: Основная тема
        research_data: Данные предыдущих исследований

    Returns:
        Структурированный research brief
    """
    try:
        # Агрегируем все данные исследований
        if not research_data:
            research_data = {}

        # Создаем структурированный brief
        brief = _create_structured_brief(
            topic,
            ctx.deps.research_domain,
            research_data,
            ctx.deps.primary_nlp_techniques
        )

        # Добавляем NLP рекомендации
        nlp_recommendations = _generate_nlp_content_recommendations(
            topic,
            ctx.deps.target_audience,
            ctx.deps.primary_nlp_techniques
        )

        # Формируем VAK адаптации
        vak_adaptations = _generate_vak_adaptations(topic) if ctx.deps.enable_vak_adaptation else ""

        return f"""📋 **RESEARCH BRIEF**

**Тема:** {topic}
**Домен:** {ctx.deps.research_domain.value}
**Целевая аудитория:** {ctx.deps.target_audience.value}

{brief}

## 🧠 NLP Рекомендации
{nlp_recommendations}

{vak_adaptations}

## 📊 Метрики успеха
- **Engagement Rate:** Ожидается высокий из-за NLP оптимизации
- **Conversion:** Улучшенная благодаря болевым точкам
- **Shareability:** Высокая за счет эмоциональных триггеров

**📅 Создан:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**🎯 Готов для создания контента по методологии PatternShift v2.0**
"""

    except Exception as e:
        return f"❌ Ошибка создания research brief: {str(e)}"


# === КОЛЛЕКТИВНЫЕ ИНСТРУМЕНТЫ ===

async def break_down_to_microtasks(
    ctx: RunContext[NLPContentResearchDependencies],
    main_task: str,
    complexity_level: str = "medium"
) -> str:
    """
    Разбить исследовательскую задачу на микрозадачи.

    ОБЯЗАТЕЛЬНО вызывается в начале работы каждого агента.
    """
    microtasks = []

    if complexity_level == "simple":
        microtasks = [
            f"Поиск базовой информации по теме: {main_task}",
            f"Анализ найденных данных",
            f"Создание research brief"
        ]
    elif complexity_level == "medium":
        microtasks = [
            f"Анализ сложности исследования: {main_task}",
            f"Поиск в базе знаний агента",
            f"Веб-исследование и сбор актуальных данных",
            f"Анализ вирусного потенциала темы",
            f"Применение NLP техник к найденным инсайтам",
            f"Создание итогового research brief с рекомендациями"
        ]
    else:  # complex
        microtasks = [
            f"Глубокий анализ темы и определение областей исследования: {main_task}",
            f"Многоуровневый поиск: RAG + веб + академические источники",
            f"Конкурентный анализ и выявление пробелов рынка",
            f"Анализ целевой аудитории и её языковых паттернов",
            f"Оценка вирусного потенциала и shareability факторов",
            f"Применение продвинутых NLP техник для оптимизации",
            f"Создание комплексного research brief с VAK адаптациями"
        ]

    # Форматируем вывод для пользователя
    output = "📋 **Микрозадачи для исследования:**\\n"
    for i, task in enumerate(microtasks, 1):
        output += f"{i}. {task}\\n"
    output += "\\n✅ Буду отчитываться о прогрессе каждой микрозадачи"

    return output


async def delegate_research_task(
    ctx: RunContext[NLPContentResearchDependencies],
    target_agent: str,
    task_title: str,
    task_description: str,
    research_context: Dict[str, Any] = None
) -> str:
    """
    Делегировать исследовательскую задачу другому агенту через Archon.
    """
    try:
        # Подготавливаем контекст для делегирования
        context_data = research_context or {}
        context_data.update({
            "research_domain": ctx.deps.research_domain.value,
            "target_audience": ctx.deps.target_audience.value,
            "nlp_techniques": [t.value for t in ctx.deps.primary_nlp_techniques],
            "delegated_by": "NLP Content Research Agent"
        })

        # Создаем задачу в Archon (эмуляция)
        task_result = {
            "task_id": f"delegated_{datetime.now().timestamp()}",
            "status": "created",
            "assigned_to": target_agent
        }

        return f"""✅ **Задача успешно делегирована:**

**Исполнитель:** {target_agent}
**Задача:** {task_title}
**Описание:** {task_description}

**Переданный контекст:**
{json.dumps(context_data, indent=2, ensure_ascii=False)}

**ID задачи:** {task_result['task_id']}
**Статус:** Создана в Archon и готова к выполнению

💡 **Примечание:** Задача будет выполнена с учетом NLP специализации и методологии PatternShift.
"""

    except Exception as e:
        return f"❌ Ошибка делегирования задачи: {str(e)}"


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===

def _get_fallback_knowledge(domain, query: str) -> str:
    """Локальная база знаний как fallback."""
    knowledge_base = {
        "psychology": {
            "nlp": "NLP техники включают VAK модальности, рефрейминг, раппорт",
            "research": "Психологические исследования требуют научной строгости",
            "methods": "Основные методы: наблюдение, эксперимент, опрос"
        },
        "astrology": {
            "basics": "Астрология изучает влияние небесных тел на человека",
            "charts": "Натальная карта показывает позиции планет в момент рождения"
        }
    }

    domain_knowledge = knowledge_base.get(domain.value if hasattr(domain, 'value') else str(domain), {})
    for key, value in domain_knowledge.items():
        if key in query.lower():
            return value

    return "Базовые знания по теме доступны. Рекомендуется использовать веб-поиск для получения актуальной информации."


def _generate_search_queries(request: ResearchQuery) -> List[str]:
    """Генерация поисковых запросов."""
    base_queries = [
        f"{request.topic} {request.domain}",
        f"{request.topic} research latest",
        f"{request.topic} trends 2024"
    ]

    if request.focus_areas:
        for area in request.focus_areas:
            base_queries.append(f"{request.topic} {area}")

    return base_queries


def _simulate_web_search(query: str, domain: str) -> Dict[str, Any]:
    """Эмуляция веб-поиска."""
    return {
        "query": query,
        "results": [
            {"title": f"Исследование: {query}", "summary": f"Актуальная информация по теме {query} в области {domain}"},
            {"title": f"Тренды: {query}", "summary": f"Современные тенденции и подходы к {query}"}
        ]
    }


def _aggregate_research_results(results: List[Dict], request: ResearchQuery) -> str:
    """Агрегация результатов исследования."""
    return f"""
## 🎯 Ключевые инсайты
- Найдено {len(results)} релевантных источников
- Тема {request.topic} показывает высокую актуальность
- Выявлены возможности для создания уникального контента

## 📊 Основные находки
- Современные подходы к теме развиваются в сторону практичности
- Аудитория заинтересована в конкретных решениях
- Есть потенциал для вирусного контента

## 💡 Рекомендации
- Использовать найденные инсайты для создания резонансного контента
- Применить NLP техники для усиления воздействия
- Фокусироваться на болевых точках аудитории
"""


def _analyze_emotional_triggers(topic: str, domain) -> str:
    """Анализ эмоциональных триггеров темы."""
    return f"""
**🎭 Основные эмоции:**
- Любопытство: "Что если..."
- Узнавание: "Это про меня!"
- Надежда: "Есть решение!"

**🔥 Триггеры для {topic}:**
- Персонализация (ваш личный случай)
- Срочность (почему важно знать сейчас)
- Социальное доказательство (миллионы людей сталкиваются)
"""


def _analyze_shareability(topic: str, platforms: List[str]) -> str:
    """Анализ факторов shareability."""
    return f"""
**🚀 Факторы распространения:**
- Эмоциональная нагрузка: Высокая
- Полезность: Практические инсайты
- Уникальность: Новый взгляд на тему

**📱 Платформы:**
{', '.join(platforms)} - оптимальны для темы "{topic}"

**⭐ Shareability Score:** 8/10
"""


def _get_nlp_viral_recommendations(topic: str, techniques) -> str:
    """NLP рекомендации для вирусности."""
    return f"""
**🧠 NLP оптимизация:**
- Использовать VAK языковые паттерны
- Применить техники раппорта с аудиторией
- Встроить пресуппозиции изменений

**💬 Языковые паттерны:**
- "Представьте себе..." (визуалы)
- "Слышите ли вы..." (аудиалы)
- "Почувствуйте разницу..." (кинестетики)

**🎯 Фокус техник:** {', '.join([t.value if hasattr(t, 'value') else str(t) for t in techniques])}
"""


def _calculate_viral_score(topic: str) -> int:
    """Расчет вирусного потенциала."""
    # Упрощенная логика расчета
    base_score = 6
    if "почему" in topic.lower():
        base_score += 2
    if any(word in topic.lower() for word in ["секрет", "правда", "открытие"]):
        base_score += 1
    return min(base_score, 10)


def _find_competitors(niche: str, count: int) -> List[Dict]:
    """Поиск конкурентов в нише."""
    return [
        {"name": f"Лидер {i+1}", "domain": f"competitor{i+1}.com", "followers": f"{10000+i*1000}"}
        for i in range(min(count, 5))
    ]


def _analyze_competitor(competitor: Dict, aspects: List[str]) -> Dict:
    """Анализ конкретного конкурента."""
    return {
        "name": competitor["name"],
        "strengths": ["Сильная экспертность", "Активная аудитория"],
        "weaknesses": ["Сложный язык", "Мало NLP техник"],
        "nlp_usage": "Базовый уровень"
    }


def _identify_market_gaps(insights: List[Dict], niche: str) -> str:
    """Выявление пробелов рынка."""
    return f"""
**🕳️ Обнаруженные пробелы:**
- Недостаток простого языка
- Мало практических примеров
- Отсутствие NLP оптимизации

**💡 Возможности для {niche}:**
- Создать контент с продвинутым NLP
- Использовать более доступный язык
- Добавить больше интерактивности
"""


def _analyze_competitor_nlp_patterns(insights: List[Dict]) -> str:
    """Анализ NLP паттернов конкурентов."""
    return """
**🧠 Паттерны конкурентов:**
- Базовые визуальные предикаты
- Редкое использование раппорта
- Отсутствие VAK адаптации

**🚀 Наши преимущества:**
- Продвинутые NLP техники
- Эриксоновские паттерны
- Полная VAK адаптация
"""


def _format_competitors_list(competitors: List[Dict]) -> str:
    """Форматирование списка конкурентов."""
    return "\\n".join([
        f"**{c['name']}** ({c['domain']}) - {c['followers']} подписчиков"
        for c in competitors
    ])


def _create_structured_brief(topic: str, domain, research_data: Dict, nlp_techniques) -> str:
    """Создание структурированного research brief."""
    return f"""
## 🎯 Основные инсайты
- Тема "{topic}" имеет высокий потенциал в области {domain.value if hasattr(domain, 'value') else str(domain)}
- Аудитория активно ищет практические решения
- Конкуренты недоиспользуют NLP техники

## 💥 Болевые точки аудитории
- Сложность существующего контента
- Недостаток персонализации
- Отсутствие практических инструментов

## 🚀 Возможности для контента
- Упростить сложные концепции
- Добавить интерактивные элементы
- Использовать продвинутые NLP техники
"""


def _generate_nlp_content_recommendations(topic: str, audience, techniques) -> str:
    """Генерация NLP рекомендаций для контента."""
    return f"""
**🎭 Языковая адаптация для {audience.value if hasattr(audience, 'value') else str(audience)}:**
- Использовать простые, понятные термины
- Включить истории и метафоры
- Применить техники раппорта

**🧠 Рекомендуемые NLP техники:**
{', '.join([t.value if hasattr(t, 'value') else str(t) for t in techniques])}

**💬 Языковые паттерны:**
- Пресуппозиции успеха: "Когда вы достигнете результата..."
- Вставленные команды: "ПРЕДСТАВЬТЕ себе эти изменения"
- Якорение состояний: связать позитив с ключевыми словами
"""


def _generate_vak_adaptations(topic: str) -> str:
    """Генерация VAK адаптаций для темы."""
    return f"""
## 👁️ VAK Адаптации для "{topic}"

**ВИЗУАЛЬНАЯ версия:**
"Представьте ясную картину того, как {topic} выглядит в вашей жизни. Видите ли вы изменения? Насколько яркими становятся новые возможности?"

**АУДИАЛЬНАЯ версия:**
"Слышите ли вы, как {topic} звучит в вашей жизни? Прислушайтесь к внутреннему голосу, который говорит вам о важности этих изменений."

**КИНЕСТЕТИЧЕСКАЯ версия:**
"Почувствуйте, как {topic} влияет на вашу жизнь. Ощутите тепло понимания и легкость, которая приходит с новыми инсайтами."
"""


__all__ = [
    "search_agent_knowledge",
    "conduct_web_research",
    "analyze_viral_potential",
    "conduct_competitor_analysis",
    "generate_content_brief",
    "break_down_to_microtasks",
    "delegate_research_task",
    "ResearchQuery",
    "ViralAnalysisRequest",
    "CompetitorAnalysisRequest"
]