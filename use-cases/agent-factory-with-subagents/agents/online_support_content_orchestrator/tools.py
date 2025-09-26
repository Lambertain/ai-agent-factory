"""
Tools для Psychology Content Orchestrator Agent
"""

from typing import List, Dict, Any, Optional
from .dependencies import search_psychology_knowledge, ContentCreationRequest

async def search_agent_knowledge(query: str, domain: str = "general") -> str:
    """
    Поиск знаний по психологии и терапии

    Args:
        query: Поисковый запрос
        domain: Психологический домен (anxiety, depression, relationships, etc.)

    Returns:
        Найденные знания в текстовом формате
    """
    knowledge_results = await search_psychology_knowledge(
        query=query,
        domain=domain,
        tags=["psychology", "therapy", domain],
        match_count=5
    )

    if not knowledge_results:
        return f"Знания по запросу '{query}' в домене '{domain}' не найдены."

    formatted_results = []
    for i, knowledge in enumerate(knowledge_results, 1):
        formatted_results.append(
            f"Результат {i}:\n"
            f"Домен: {knowledge.domain}\n"
            f"Подход: {knowledge.therapeutic_approach}\n"
            f"Содержание: {knowledge.content}\n"
        )

    return "\n".join(formatted_results)

async def coordinate_content_creation(
    content_type: str,
    target_audience: str,
    psychological_domain: str,
    objectives: List[str],
    constraints: Optional[List[str]] = None,
    cultural_context: Optional[str] = None
) -> str:
    """
    Координация создания психологического контента

    Args:
        content_type: Тип контента (therapeutic, educational, assessment)
        target_audience: Целевая аудитория (teenagers, adults, seniors)
        psychological_domain: Психологический домен
        objectives: Цели контента
        constraints: Ограничения при создании
        cultural_context: Культурный контекст

    Returns:
        План координации создания контента
    """
    # Поиск релевантных знаний
    knowledge_query = f"{content_type} {psychological_domain} {target_audience}"
    relevant_knowledge = await search_agent_knowledge(knowledge_query, psychological_domain)

    # Создание плана координации
    plan = f"""
ПЛАН КООРДИНАЦИИ ПСИХОЛОГИЧЕСКОГО КОНТЕНТА

1. БАЗОВЫЕ ПАРАМЕТРЫ:
   - Тип контента: {content_type}
   - Целевая аудитория: {target_audience}
   - Психологический домен: {psychological_domain}
   - Культурный контекст: {cultural_context or 'универсальный'}

2. ЦЕЛИ КОНТЕНТА:
   {chr(10).join(f"   - {obj}" for obj in objectives)}

3. ОГРАНИЧЕНИЯ:
   {chr(10).join(f"   - {const}" for const in (constraints or ['Нет специальных ограничений']))}

4. НАЙДЕННЫЕ ЗНАНИЯ:
   {relevant_knowledge}

5. РЕКОМЕНДУЕМАЯ СТРУКТУРА:
   - Введение и контекст проблемы
   - Теоретические основы
   - Практические техники и упражнения
   - Примеры и кейсы
   - Заключение и следующие шаги

6. КООРДИНАЦИЯ СОЗДАНИЯ:
   - Этап 1: Исследование и анализ целевой аудитории
   - Этап 2: Создание основного контента
   - Этап 3: Адаптация под культурный контекст
   - Этап 4: Проверка на соответствие этическим стандартам
   - Этап 5: Финальная редактура и оформление
"""

    return plan

async def analyze_target_audience(
    audience_type: str,
    age_range: str,
    cultural_background: str = "mixed",
    psychological_needs: List[str] = None
) -> str:
    """
    Анализ целевой аудитории для психологического контента

    Args:
        audience_type: Тип аудитории (clients, professionals, general_public)
        age_range: Возрастной диапазон
        cultural_background: Культурный фон
        psychological_needs: Психологические потребности

    Returns:
        Анализ целевой аудитории
    """
    # Поиск знаний об особенностях аудитории
    audience_query = f"psychological needs {audience_type} {age_range} {cultural_background}"
    audience_knowledge = await search_agent_knowledge(audience_query, "developmental")

    analysis = f"""
АНАЛИЗ ЦЕЛЕВОЙ АУДИТОРИИ

1. ХАРАКТЕРИСТИКИ АУДИТОРИИ:
   - Тип: {audience_type}
   - Возрастной диапазон: {age_range}
   - Культурный фон: {cultural_background}

2. ПСИХОЛОГИЧЕСКИЕ ПОТРЕБНОСТИ:
   {chr(10).join(f"   - {need}" for need in (psychological_needs or ['Не указаны']))}

3. ЗНАНИЯ ОБ АУДИТОРИИ:
   {audience_knowledge}

4. РЕКОМЕНДАЦИИ ПО АДАПТАЦИИ КОНТЕНТА:
   - Учесть возрастные особенности восприятия
   - Адаптировать язык и примеры под аудиторию
   - Включить культурно-специфичные элементы
   - Предусмотреть индивидуальные различия

5. ПРЕДПОЧТИТЕЛЬНЫЕ ФОРМАТЫ:
   - Для подростков: интерактивные элементы, мультимедиа
   - Для взрослых: структурированная информация, кейсы
   - Для профессионалов: научные данные, методологии
"""

    return analysis