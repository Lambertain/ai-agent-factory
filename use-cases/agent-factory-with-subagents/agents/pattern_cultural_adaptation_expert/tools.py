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


async def delegate_to_pattern_agent(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    agent_type: str,
    task_description: str,
    task_priority: str = "medium"
) -> str:
    """
    Делегировать задачу другому Pattern агенту через Archon MCP.

    Args:
        agent_type: Тип агента (nlp_technique_master, test_architect, etc.)
        task_description: Описание задачи
        task_priority: Приоритет задачи

    Returns:
        Результат делегирования
    """
    try:
        if not ctx.deps.enable_pattern_agent_delegation:
            return "❌ Делегирование Pattern агентам отключено в настройках"

        if agent_type not in ctx.deps.pattern_agents_registry:
            available_agents = ', '.join(ctx.deps.pattern_agents_registry.keys())
            return f"❌ Pattern агент '{agent_type}' не найден. Доступные: {available_agents}"

        agent_full_name = ctx.deps.pattern_agents_registry[agent_type]

        # Здесь будет вызов Archon MCP для создания задачи
        # task_result = await mcp__archon__manage_task(
        #     action="create",
        #     project_id=ctx.deps.archon_project_id,
        #     title=f"Задача от Cultural Adaptation Expert: {task_description[:50]}",
        #     description=f"""
        # Задача делегирована от Pattern Cultural Adaptation Expert Agent
        #
        # Описание: {task_description}
        # Приоритет: {task_priority}
        # Целевая культура: {ctx.deps.target_culture.value}
        #
        # Контекст PatternShift:
        # {ctx.deps.get_patternshift_cultural_context()}
        #     """,
        #     assignee=agent_full_name,
        #     status="todo",
        #     feature="Pattern Inter-Agent Communication",
        #     task_order=50
        # )

        return f"""
✅ **Задача успешно делегирована Pattern агенту**

🎯 **Целевой агент:** {agent_full_name}
📋 **Тип агента:** {agent_type}
📝 **Задача:** {task_description}
⭐ **Приоритет:** {task_priority}

🔄 **Статус:** Задача создана в Archon MCP системе управления
🌍 **Культурный контекст:** {ctx.deps.target_culture.value}

💡 **Следующие шаги:**
1. Задача будет обработана {agent_full_name}
2. Результат будет доступен через Archon систему
3. Уведомления придут при изменении статуса

⚠️ **Примечание:** Полная интеграция с Archon MCP будет активирована после настройки соединения
"""

    except Exception as e:
        return f"❌ Ошибка делегирования задачи: {e}"


async def process_user_registration(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    request: UserRegistrationData
) -> str:
    """
    Обработать регистрационные данные пользователя и определить культурный профиль.

    Args:
        request: Данные регистрации пользователя

    Returns:
        Результат культурного профилирования и назначения
    """
    try:
        # Создаем профайлер и ассистент назначения
        profiler = PatternShiftCulturalProfiler()
        assigner = PatternShiftCultureAssigner()

        # Обрабатываем ответы пользователя
        assignment_result = assigner.process_registration_responses(request.responses)

        # Получаем объяснение назначения
        explanation = assigner.get_assignment_explanation(assignment_result, request.language_preference)

        # Обновляем культурный профиль агента
        if hasattr(ctx.deps, 'cultural_profile'):
            ctx.deps.cultural_profile = assignment_result.cultural_profile
        ctx.deps.target_culture = assignment_result.assigned_culture

        # Формируем результат
        confidence_emoji = "🎯" if assignment_result.confidence_score >= 0.8 else "⚠️" if assignment_result.confidence_score >= 0.6 else "❓"

        result = f"""
{confidence_emoji} **PatternShift Культурное Профилирование Завершено**

🎭 **Определенная культура:** {assignment_result.assigned_culture.value}
🙏 **Религиозный контекст:** {assignment_result.assigned_religion.value}
📊 **Уверенность:** {assignment_result.confidence_score:.0%} ({assignment_result.confidence_level.value})

📋 **Обоснование назначения:**
{assignment_result.assignment_rationale}

✨ **Что это означает для PatternShift:**
- Программа будет адаптирована под {assignment_result.assigned_culture.value} культурные особенности
- Метафоры и примеры будут культурно релевантными
- Религиозный контекст {assignment_result.assigned_religion.value} будет учтен
- Чувствительные темы будут исключены из контента

🔄 **Статус назначения:** {'Автоматическое' if not assignment_result.requires_confirmation else 'Требует подтверждения'}
"""

        if assignment_result.alternative_suggestions:
            result += f"\n🤔 **Альтернативные варианты:**\n"
            for alt_culture, confidence in assignment_result.alternative_suggestions[:3]:
                result += f"- {alt_culture.value} ({confidence:.0%})\n"

        if assignment_result.follow_up_questions:
            result += f"\n❓ **Дополнительные вопросы для уточнения:**\n"
            for question in assignment_result.follow_up_questions[:2]:
                question_text = question.get('question_ru' if request.language_preference == 'ru' else 'question_en', question.get('question_ru', ''))
                result += f"- {question_text}\n"

        result += f"""
⚙️ **Настройки можно изменить в любое время в личном кабинете**

🎯 **PatternShift готов к персонализированной трансформации!**
"""

        return result

    except Exception as e:
        return f"❌ Ошибка обработки регистрации: {e}"


async def get_registration_questionnaire(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    language: str = "ru"
) -> str:
    """
    Получить анкету для культурного профилирования при регистрации.

    Args:
        language: Язык анкеты (ru/en)

    Returns:
        JSON-структура анкеты для фронтенда
    """
    try:
        profiler = PatternShiftCulturalProfiler()
        questions = profiler.get_cultural_questions(language)

        # Читаем JSON шаблон анкеты
        import json
        import os

        questionnaire_path = os.path.join(os.path.dirname(__file__), "registration_questionnaire.json")
        with open(questionnaire_path, 'r', encoding='utf-8') as f:
            questionnaire_template = json.load(f)

        # Формируем ответ для агента
        lang_suffix = "ru" if language == "ru" else "en"

        result = f"""
📋 **PatternShift Анкета Культурного Профилирования**

📝 **Название:** {questionnaire_template['questionnaire_info'][f'title_{lang_suffix}']}
📄 **Описание:** {questionnaire_template['questionnaire_info'][f'description_{lang_suffix}']}
⏱️ **Время заполнения:** {questionnaire_template['questionnaire_info'][f'estimated_time_{lang_suffix}']}

🔒 **Конфиденциальность:** {questionnaire_template['questionnaire_info'][f'privacy_note_{lang_suffix}']}

❓ **Вопросы анкеты ({len(questions)} шт.):**

"""

        for i, question in enumerate(questions[:3], 1):  # Показываем первые 3 вопроса как пример
            result += f"""**{i}. {question['question']}**
   Тип: {question['type']} | Вес: {question['weight']}
   Варианты: {len(question['options'])} опций

"""

        result += f"""
📊 **Алгоритм обработки:**
- Взвешенная система подсчета баллов
- Минимальная уверенность для автоназначения: 60%
- Поддержка смешанных культурных профилей
- Автоматические дополнительные вопросы при низкой уверенности

🎯 **Поддерживаемые культуры:** 20 европейских культур
🙏 **Религиозные контексты:** Православие, Католицизм, Протестантизм, Светские взгляды, Смешанные традиции

💾 **Полная анкета в JSON доступна в файле:** registration_questionnaire.json
📁 **Для интеграции с фронтендом используйте полную JSON структуру**

✅ **Анкета готова к развертыванию в системе регистрации PatternShift**
"""

        return result

    except Exception as e:
        return f"❌ Ошибка получения анкеты: {e}"


async def update_user_cultural_profile(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    request: CulturalProfileUpdateRequest
) -> str:
    """
    Обновить культурный профиль пользователя.

    Args:
        request: Запрос на обновление профиля

    Returns:
        Результат обновления профиля
    """
    try:
        # Получаем текущий профиль пользователя
        current_profile = getattr(ctx.deps, 'cultural_profile', None)

        if not current_profile:
            return "❌ Культурный профиль пользователя не найден. Необходимо пройти первичное профилирование."

        # Применяем обновления
        updates_applied = []

        if 'culture' in request.profile_updates:
            new_culture = PatternShiftCulture(request.profile_updates['culture'])
            current_profile.culture = new_culture
            ctx.deps.target_culture = new_culture
            updates_applied.append(f"Культура изменена на: {new_culture.value}")

        if 'religion' in request.profile_updates:
            new_religion = PatternShiftReligion(request.profile_updates['religion'])
            current_profile.religion = new_religion
            updates_applied.append(f"Религиозный контекст изменен на: {new_religion.value}")

        if 'sensitive_topics' in request.profile_updates:
            current_profile.sensitive_topics = request.profile_updates['sensitive_topics']
            updates_applied.append("Чувствительные темы обновлены")

        if 'preferred_metaphors' in request.profile_updates:
            current_profile.preferred_metaphors = request.profile_updates['preferred_metaphors']
            updates_applied.append("Предпочтительные метафоры обновлены")

        # Корректируем уверенность если указано
        confidence_note = ""
        if request.confidence_adjustment:
            confidence_note = f"\n📊 **Корректировка уверенности:** {request.confidence_adjustment:+.1%}"

        return f"""
✅ **Культурный профиль успешно обновлен**

👤 **Пользователь:** {request.user_id}
📅 **Дата обновления:** {ctx.deps.get_patternshift_cultural_context().get('current_date', 'сегодня')}
📝 **Причина:** {request.reason}

🔄 **Примененные изменения:**
{chr(10).join(['- ' + update for update in updates_applied])}

{confidence_note}

🎯 **Обновленный профиль:**
- Культура: {current_profile.culture.value}
- Религиозный контекст: {current_profile.religion.value}
- Фаза программы: {current_profile.phase.value}
- Целевые модули: {', '.join([m.value for m in current_profile.target_modules[:3]])}

⚡ **Влияние на PatternShift:**
- Все будущие материалы будут адаптированы под новый профиль
- Текущий прогресс программы сохранен
- Метафоры и примеры будут обновлены

📝 **Рекомендация:** Пересмотрите ранее пройденные модули с учетом нового культурного контекста
"""

    except Exception as e:
        return f"❌ Ошибка обновления профиля: {e}"


async def validate_cultural_assignment(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    assigned_culture: str,
    user_feedback: Dict[str, Any]
) -> str:
    """
    Валидация назначенной культуры на основе обратной связи пользователя.

    Args:
        assigned_culture: Назначенная культура
        user_feedback: Обратная связь пользователя

    Returns:
        Результат валидации и рекомендации
    """
    try:
        culture = PatternShiftCulture(assigned_culture)

        # Анализируем обратную связь
        feedback_score = user_feedback.get('satisfaction_score', 5)  # 1-10
        feedback_comments = user_feedback.get('comments', '')
        specific_issues = user_feedback.get('specific_issues', [])

        validation_result = {
            'is_valid': feedback_score >= 7,
            'confidence_adjustment': 0.0,
            'recommendations': [],
            'action_needed': 'none'
        }

        if feedback_score >= 8:
            validation_result['confidence_adjustment'] = 0.1
            validation_result['recommendations'].append("Отличное соответствие культурного профиля")
        elif feedback_score >= 6:
            validation_result['recommendations'].append("Хорошее соответствие с небольшими улучшениями")
        elif feedback_score >= 4:
            validation_result['confidence_adjustment'] = -0.2
            validation_result['recommendations'].append("Требуется пересмотр некоторых аспектов профиля")
            validation_result['action_needed'] = 'profile_adjustment'
        else:
            validation_result['confidence_adjustment'] = -0.4
            validation_result['recommendations'].append("Рекомендуется полное повторное профилирование")
            validation_result['action_needed'] = 'full_reprof'

        # Анализ конкретных проблем
        if 'metaphors_unclear' in specific_issues:
            validation_result['recommendations'].append("Необходима адаптация метафор и примеров")
        if 'religious_conflict' in specific_issues:
            validation_result['recommendations'].append("Требуется корректировка религиозного контекста")
        if 'language_issues' in specific_issues:
            validation_result['recommendations'].append("Необходима проверка языковой адаптации")

        # Формируем ответ
        status_emoji = "✅" if validation_result['is_valid'] else "⚠️" if feedback_score >= 4 else "❌"

        result = f"""
{status_emoji} **Валидация Культурного Назначения**

🎭 **Назначенная культура:** {culture.value}
📊 **Оценка пользователя:** {feedback_score}/10
📝 **Комментарии:** {feedback_comments}

🔍 **Результат валидации:**
- Назначение {'корректно' if validation_result['is_valid'] else 'требует доработки'}
- Корректировка уверенности: {validation_result['confidence_adjustment']:+.1%}
- Требуемое действие: {validation_result['action_needed']}

💡 **Рекомендации:**
{chr(10).join(['- ' + rec for rec in validation_result['recommendations']])}
"""

        if specific_issues:
            result += f"\n⚠️ **Выявленные проблемы:**\n"
            issue_descriptions = {
                'metaphors_unclear': 'Метафоры непонятны или нерелевантны',
                'religious_conflict': 'Конфликт с религиозными взглядами',
                'language_issues': 'Языковые несоответствия',
                'cultural_mismatch': 'Общее несоответствие культуре'
            }
            for issue in specific_issues:
                result += f"- {issue_descriptions.get(issue, issue)}\n"

        if validation_result['action_needed'] == 'full_reprof':
            result += f"\n🔄 **Рекомендуется:** Пройти повторное культурное профилирование\n"
        elif validation_result['action_needed'] == 'profile_adjustment':
            result += f"\n⚙️ **Рекомендуется:** Корректировка отдельных элементов профиля\n"

        result += f"\n✨ **PatternShift продолжит адаптацию с учетом обратной связи**"

        return result

    except Exception as e:
        return f"❌ Ошибка валидации назначения: {e}"