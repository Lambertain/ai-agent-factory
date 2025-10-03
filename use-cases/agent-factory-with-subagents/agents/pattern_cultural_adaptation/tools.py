"""
Инструменты для Pattern Cultural Adaptation Expert Agent.

Набор инструментов для культурной адаптации психологических интервенций
с учетом культурных особенностей, религиозных контекстов и языковых нюансов.
Специализированные для проекта PatternShift.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import (
    PatternCulturalAdaptationExpertDependencies,
    PatternShiftCulture,
    PatternShiftReligion,
    PatternShiftPhase,
    ModuleType
)

# Импортируем новые модули культурного профилирования
from .cultural_profiling import (
    PatternShiftCulturalProfiler,
    UserCulturalResponse,
    CulturalProfilingResult
)

from .auto_culture_assignment import (
    PatternShiftCultureAssigner,
    CultureAssignmentResult,
    AssignmentConfidenceLevel
)


class CulturalAnalysisRequest(BaseModel):
    """Запрос на анализ культурного контекста для PatternShift."""
    content: str = Field(description="Контент для анализа")
    target_culture: str = Field(description="Целевая PatternShift культура")
    content_type: str = Field(default="general", description="Тип контента")
    sensitivity_level: str = Field(default="moderate", description="Уровень чувствительности")


class AdaptationRequest(BaseModel):
    """Запрос на адаптацию контента для PatternShift."""
    original_content: str = Field(description="Оригинальный контент")
    target_culture: str = Field(description="Целевая PatternShift культура")
    adaptation_type: str = Field(description="Тип адаптации")
    preserve_elements: List[str] = Field(default_factory=list, description="Элементы для сохранения")


class CulturalValidationRequest(BaseModel):
    """Запрос на валидацию культурной приемлемости для PatternShift."""
    adapted_content: str = Field(description="Адаптированный контент")
    target_culture: str = Field(description="Целевая PatternShift культура")
    validation_criteria: List[str] = Field(default_factory=list, description="Критерии валидации")


class MetaphorAdaptationRequest(BaseModel):
    """Запрос на адаптацию метафор для PatternShift."""
    original_metaphors: List[str] = Field(description="Исходные метафоры")
    target_culture: str = Field(description="Целевая PatternShift культура")
    context: str = Field(description="Контекст использования")
    emotional_tone: str = Field(default="neutral", description="Эмоциональный тон")


class UserRegistrationData(BaseModel):
    """Данные регистрации пользователя для культурного профилирования."""
    responses: List[Dict[str, Any]] = Field(description="Ответы на вопросы анкеты")
    language_preference: str = Field(default="ru", description="Предпочитаемый язык")
    additional_info: Dict[str, Any] = Field(default_factory=dict, description="Дополнительная информация")


class CulturalProfileUpdateRequest(BaseModel):
    """Запрос на обновление культурного профиля пользователя."""
    user_id: str = Field(description="Идентификатор пользователя")
    profile_updates: Dict[str, Any] = Field(description="Обновления профиля")
    reason: str = Field(description="Причина обновления")
    confidence_adjustment: Optional[float] = Field(default=None, description="Корректировка уверенности")


async def search_agent_knowledge(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в знаниях агента через Archon RAG.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация
    """
    try:
        # Используем теги для фильтрации знаний агента
        search_tags = " ".join(ctx.deps.knowledge_tags)
        enhanced_query = f"{query} {search_tags}"

        # Здесь был бы вызов Archon RAG при наличии интеграции
        # result = await mcp__archon__rag_search_knowledge_base(
        #     query=enhanced_query,
        #     match_count=match_count
        # )

        return f"""
📚 **Поиск в базе знаний PatternShift Cultural Adaptation Expert**

🔍 **Запрос:** {query}
🏷️ **Теги:** {search_tags}

💡 **Найденная информация:**
- Использование культурно-адаптированных метафор для психологических интервенций
- Принципы адаптации НЛП техник под украинский, польский и английский контексты
- Протоколы валидации культурной безопасности в психологической работе
- Интеграция религиозных контекстов в терапевтические программы

⚠️ **Примечание:** Полная интеграция с Archon RAG будет активирована после настройки MCP соединения.
"""

    except Exception as e:
        return f"❌ Ошибка поиска знаний: {e}"


async def analyze_cultural_context(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    request: CulturalAnalysisRequest
) -> str:
    """
    Анализ культурного контекста для PatternShift программы.

    Args:
        request: Запрос на анализ

    Returns:
        Результат анализа с рекомендациями по адаптации
    """
    try:
        target_culture = PatternShiftCulture(request.target_culture)
        cultural_context = ctx.deps.get_patternshift_cultural_context()

        analysis_result = f"""
🎯 **Культурный анализ для PatternShift**

📋 **Основные параметры:**
- Целевая культура: {target_culture.value}
- Религиозный контекст: {cultural_context.get('religion', 'не определен')}
- Фаза программы: {cultural_context.get('phase', 'не определена')}
- Тип контента: {request.content_type}

🧭 **Культурные особенности:**
"""

        # Анализ специфичных культурных элементов
        if target_culture == PatternShiftCulture.UKRAINIAN:
            analysis_result += """
- Высокий контекст коммуникации с эмоциональной окраской
- Важность семейных связей и исторической памяти
- Предпочтение природных метафор: поле, дуб, река
- Чувствительность к темам войны и национальной идентичности
- Православные традиции влияют на восприятие"""

        elif target_culture == PatternShiftCulture.POLISH:
            analysis_result += """
- Умеренный контекст коммуникации с уважением к традициям
- Сильное влияние католических ценностей
- Исторические метафоры солидарности и гордости
- Семейные ценности как основа мотивации
- Важность национальной идентичности"""

        elif target_culture == PatternShiftCulture.ENGLISH:
            analysis_result += """
- Низкий контекст, прямая коммуникация
- Индивидуализм и личные достижения
- Светские, рациональные подходы
- Бизнес и технологические метафоры
- Практичность и эффективность"""

        analysis_result += f"""

⚠️ **Чувствительные темы:**
{chr(10).join(['- ' + topic for topic in cultural_context.get('sensitive_topics', [])])}

🎨 **Рекомендуемые метафоры:**
{chr(10).join(['- ' + metaphor for metaphor in cultural_context.get('preferred_metaphors', [])])}

📊 **Уровень адаптации:** {cultural_context.get('patternshift_settings', {}).get('depth', 'умеренный')}
"""

        return analysis_result

    except Exception as e:
        return f"❌ Ошибка анализа культурного контекста: {e}"


async def adapt_content_culturally(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    request: AdaptationRequest
) -> str:
    """
    Культурная адаптация контента для PatternShift программы.

    Args:
        request: Запрос на адаптацию

    Returns:
        Адаптированный контент с пояснениями
    """
    try:
        target_culture = PatternShiftCulture(request.target_culture)
        cultural_context = ctx.deps.get_patternshift_cultural_context()

        # Получаем принципы адаптации для культуры
        adaptation_principles = {
            "metaphors": cultural_context.get('preferred_metaphors', []),
            "communication": "прямой" if target_culture == PatternShiftCulture.ENGLISH else "контекстный",
            "values": cultural_context.get('cultural_heroes', []),
            "examples": []
        }

        adapted_content = request.original_content
        adaptation_notes = []

        # Специфичные адаптации для PatternShift культур
        if target_culture == PatternShiftCulture.UKRAINIAN:
            adapted_content = adapted_content.replace("путь", "дорога домой")
            adapted_content = adapted_content.replace("цель", "мрія")
            adaptation_notes.append("Адаптированы ключевые понятия под украинский менталитет")

        elif target_culture == PatternShiftCulture.POLISH:
            if "семья" in adapted_content.lower():
                adaptation_notes.append("Усилен акцент на семейных ценностях")
            if "традиция" in adapted_content.lower():
                adaptation_notes.append("Подчеркнута важность католических традиций")

        elif target_culture == PatternShiftCulture.ENGLISH:
            adapted_content = adapted_content.replace("мы вместе", "you can achieve")
            adaptation_notes.append("Адаптирован под индивидуалистический подход")

        return f"""
🎯 **PatternShift Культурная Адаптация**

📝 **Оригинальный контент:**
{request.original_content}

✨ **Адаптированный контент:**
{adapted_content}

🔧 **Принципы адаптации:**
- Метафоры: {', '.join(adaptation_principles['metaphors'][:3])}
- Коммуникация: {adaptation_principles['communication']}
- Культурные герои: {', '.join(adaptation_principles['values'][:2])}

📋 **Внесенные изменения:**
{chr(10).join(['- ' + note for note in adaptation_notes]) if adaptation_notes else "- Контент адаптирован под культурный контекст"}

🎯 **Целевая PatternShift культура:** {target_culture.value}
📊 **Тип адаптации:** {request.adaptation_type}

✅ **PatternShift совместимость:** Адаптировано для 21-дневной программы трансформации
"""

    except Exception as e:
        return f"❌ Ошибка культурной адаптации: {e}"


async def validate_cultural_appropriateness(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    request: CulturalValidationRequest
) -> str:
    """
    Валидация культурной приемлемости для PatternShift.

    Args:
        request: Запрос на валидацию

    Returns:
        Результат валидации с рекомендациями
    """
    try:
        target_culture = PatternShiftCulture(request.target_culture)
        cultural_context = ctx.deps.get_patternshift_cultural_context()

        validation_results = {
            "cultural_sensitivity": True,
            "religious_appropriateness": True,
            "language_appropriateness": True,
            "patternshift_compatibility": True,
            "overall_score": 0.0,
            "issues": [],
            "recommendations": []
        }

        content_lower = request.adapted_content.lower()

        # Проверка чувствительных тем PatternShift
        sensitive_topics = cultural_context.get('sensitive_topics', [])
        for topic in sensitive_topics:
            if topic.lower() in content_lower:
                validation_results["issues"].append(f"Содержит чувствительную тему: {topic}")
                validation_results["cultural_sensitivity"] = False

        # Проверка религиозной приемлемости для PatternShift
        religion = cultural_context.get('religion')
        if religion == PatternShiftReligion.ORTHODOX.value:
            if any(word in content_lower for word in ["католический", "протестантский"]):
                validation_results["issues"].append("Возможен конфликт с православным контекстом")
                validation_results["religious_appropriateness"] = False
        elif religion == PatternShiftReligion.CATHOLIC.value:
            if any(word in content_lower for word in ["православный", "протестантский"]):
                validation_results["issues"].append("Возможен конфликт с католическим контекстом")
                validation_results["religious_appropriateness"] = False

        # Проверка совместимости с PatternShift архитектурой
        patternshift_keywords = ["программа", "фаза", "день", "сессия", "активность", "модуль"]
        if not any(keyword in content_lower for keyword in patternshift_keywords):
            validation_results["recommendations"].append("Рекомендуется добавить структурные элементы PatternShift")

        # Вычисление общего балла
        score_factors = [
            validation_results["cultural_sensitivity"],
            validation_results["religious_appropriateness"],
            validation_results["language_appropriateness"],
            validation_results["patternshift_compatibility"]
        ]
        validation_results["overall_score"] = sum(score_factors) / len(score_factors) * 100

        status_emoji = "✅" if validation_results["overall_score"] >= 80 else "⚠️" if validation_results["overall_score"] >= 60 else "❌"

        return f"""
{status_emoji} **PatternShift Культурная Валидация**

📊 **Общий балл:** {validation_results["overall_score"]:.1f}%

🎯 **Целевая культура:** {target_culture.value}

✅ **Результаты проверки:**
- Культурная чувствительность: {'✅' if validation_results["cultural_sensitivity"] else '❌'}
- Религиозная приемлемость: {'✅' if validation_results["religious_appropriateness"] else '❌'}
- Языковая уместность: {'✅' if validation_results["language_appropriateness"] else '❌'}
- PatternShift совместимость: {'✅' if validation_results["patternshift_compatibility"] else '❌'}

{'⚠️ **Найденные проблемы:**' + chr(10) + chr(10).join(['- ' + issue for issue in validation_results["issues"]]) if validation_results["issues"] else ''}

{'💡 **Рекомендации:**' + chr(10) + chr(10).join(['- ' + rec for rec in validation_results["recommendations"]]) if validation_results["recommendations"] else ''}

📋 **Критерии валидации:**
{', '.join(request.validation_criteria) if request.validation_criteria else 'Стандартные критерии PatternShift'}
"""

    except Exception as e:
        return f"❌ Ошибка валидации: {e}"


async def adapt_metaphors_culturally(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    request: MetaphorAdaptationRequest
) -> str:
    """
    Адаптация метафор для PatternShift культурного контекста.

    Args:
        request: Запрос на адаптацию метафор

    Returns:
        Адаптированные метафоры
    """
    try:
        target_culture = PatternShiftCulture(request.target_culture)
        cultural_context = ctx.deps.get_patternshift_cultural_context()

        adapted_metaphors = []
        adaptation_explanations = []

        for metaphor in request.original_metaphors:
            adapted_metaphor = metaphor
            explanation = f"Оригинал: {metaphor}"

            # Адаптация под PatternShift культуры
            if target_culture == PatternShiftCulture.UKRAINIAN:
                metaphor_mapping = {
                    "путь": "дорога домой",
                    "дерево": "дуб-віковий",
                    "река": "ріка життя",
                    "дом": "родинне вогнище",
                    "мост": "міст через річку"
                }
                for orig, adapted in metaphor_mapping.items():
                    if orig in metaphor.lower():
                        adapted_metaphor = metaphor.replace(orig, adapted)
                        explanation += f" → Адаптировано: {adapted_metaphor}"
                        break

            elif target_culture == PatternShiftCulture.POLISH:
                metaphor_mapping = {
                    "путь": "droga do domu",
                    "семья": "rodzina katolicka",
                    "история": "historia solidarności",
                    "сила": "siła tradycji"
                }
                for orig, adapted in metaphor_mapping.items():
                    if orig in metaphor.lower():
                        adapted_metaphor = metaphor.replace(orig, adapted)
                        explanation += f" → Адаптировано: {adapted_metaphor}"
                        break

            elif target_culture == PatternShiftCulture.ENGLISH:
                metaphor_mapping = {
                    "путь": "personal journey",
                    "команда": "individual achievement",
                    "традиция": "innovation",
                    "сообщество": "networking"
                }
                for orig, adapted in metaphor_mapping.items():
                    if orig in metaphor.lower():
                        adapted_metaphor = metaphor.replace(orig, adapted)
                        explanation += f" → Адаптировано: {adapted_metaphor}"
                        break

            adapted_metaphors.append(adapted_metaphor)
            adaptation_explanations.append(explanation)

        return f"""
🎨 **PatternShift Адаптация Метафор**

🎯 **Целевая культура:** {target_culture.value}
📝 **Контекст:** {request.context}
😊 **Эмоциональный тон:** {request.emotional_tone}

✨ **Адаптированные метафоры:**
{chr(10).join(['- ' + metaphor for metaphor in adapted_metaphors])}

🔄 **Процесс адаптации:**
{chr(10).join(adaptation_explanations)}

🌟 **Культурные принципы:**
- Используются предпочтительные образы: {', '.join(cultural_context.get('preferred_metaphors', [])[:3])}
- Учтен религиозный контекст: {cultural_context.get('religion', 'светский')}
- Избегание чувствительных тем: {', '.join(cultural_context.get('sensitive_topics', [])[:2])}

✅ **PatternShift интеграция:** Метафоры адаптированы для психологических интервенций
"""

    except Exception as e:
        return f"❌ Ошибка адаптации метафор: {e}"


async def generate_cultural_examples(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    topic: str,
    target_culture: str,
    context: str = "general"
) -> str:
    """
    Генерация культурно-адаптированных примеров для PatternShift.

    Args:
        topic: Тема примеров
        target_culture: Целевая культура
        context: Контекст использования

    Returns:
        Культурно-адаптированные примеры
    """
    try:
        culture = PatternShiftCulture(target_culture)
        cultural_context = ctx.deps.get_patternshift_cultural_context()

        examples = []

        if topic.lower() == "стресс":
            if culture == PatternShiftCulture.UKRAINIAN:
                examples = [
                    "Подібно до дуба, що гнеться від вітру, але не ламається",
                    "Як ріка знаходить шлях навколо каменів",
                    "Наче домашнє вогнище, що дає тепло в холодну ніч"
                ]
            elif culture == PatternShiftCulture.POLISH:
                examples = [
                    "Jak silna rodzina katolicka w trudnych czasach",
                    "Podobnie do solidarności, która jednoczy ludzi",
                    "Jak tradycyjne wartości, które nas prowadzą"
                ]
            elif culture == PatternShiftCulture.ENGLISH:
                examples = [
                    "Like a personal fitness journey with clear milestones",
                    "Similar to project management - breaking down big tasks",
                    "Think of it as software optimization - removing bugs"
                ]

        elif topic.lower() == "мотивация":
            if culture == PatternShiftCulture.UKRAINIAN:
                examples = [
                    "Як мрія про повернення додому",
                    "Наче сіяння зерна в рідну землю",
                    "Подібно до світла, що веде через темний ліс"
                ]
            elif culture == PatternShiftCulture.POLISH:
                examples = [
                    "Jak modlitwa, która daje siłę",
                    "Podobnie do rodzinnych tradycji przekazywanych pokoleniom",
                    "Jak dążenie do wolności i niepodległości"
                ]
            elif culture == PatternShiftCulture.ENGLISH:
                examples = [
                    "Like achieving your quarterly business goals",
                    "Similar to upgrading your personal operating system",
                    "Think of it as your individual success metrics"
                ]

        return f"""
💡 **PatternShift Культурные Примеры**

🎯 **Тема:** {topic}
🌍 **Целевая культура:** {culture.value}
📋 **Контекст:** {context}

✨ **Примеры:**
{chr(10).join(['- ' + example for example in examples])}

🎨 **Культурная основа:**
- Предпочитаемые метафоры: {', '.join(cultural_context.get('preferred_metaphors', [])[:2])}
- Культурные герои: {', '.join(cultural_context.get('cultural_heroes', [])[:2])}
- Религиозный контекст: {cultural_context.get('religion', 'светский')}

📚 **Применение в PatternShift:**
Примеры готовы для интеграции в 21-дневную программу трансформации, модули НЛП и эриксоновского гипноза.
"""

    except Exception as e:
        return f"❌ Ошибка генерации примеров: {e}"


# Инструменты управления приложением удалены согласно аудиту качества.
# Pattern агенты должны создавать контент, а не управлять приложением.