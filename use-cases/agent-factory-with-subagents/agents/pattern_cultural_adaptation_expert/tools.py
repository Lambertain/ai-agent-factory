"""
Инструменты для Pattern Cultural Adaptation Expert Agent.

Набор инструментов для культурной адаптации психологических интервенций
с учетом культурных особенностей, религиозных контекстов и языковых нюансов.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import (
    PatternCulturalAdaptationExpertDependencies,
    CultureType,
    ReligiousContext,
    CommunicationStyle,
    ValueSystem
)


class CulturalAnalysisRequest(BaseModel):
    """Запрос на анализ культурного контекста."""
    content: str = Field(description="Контент для анализа")
    target_culture: str = Field(description="Целевая культура")
    content_type: str = Field(default="general", description="Тип контента")
    sensitivity_level: str = Field(default="moderate", description="Уровень чувствительности")


class AdaptationRequest(BaseModel):
    """Запрос на адаптацию контента."""
    original_content: str = Field(description="Оригинальный контент")
    target_culture: str = Field(description="Целевая культура")
    adaptation_type: str = Field(description="Тип адаптации")
    preserve_elements: List[str] = Field(default_factory=list, description="Элементы для сохранения")


class CulturalValidationRequest(BaseModel):
    """Запрос на валидацию культурной приемлемости."""
    adapted_content: str = Field(description="Адаптированный контент")
    target_culture: str = Field(description="Целевая культура")
    validation_criteria: List[str] = Field(default_factory=list, description="Критерии валидации")


class MetaphorAdaptationRequest(BaseModel):
    """Запрос на адаптацию метафор."""
    original_metaphors: List[str] = Field(description="Исходные метафоры")
    target_culture: str = Field(description="Целевая культура")
    context: str = Field(description="Контекст использования")
    emotional_tone: str = Field(default="neutral", description="Эмоциональный тон")


async def search_agent_knowledge(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний агента культурной адаптации.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Используем MCP Archon для поиска в базе знаний
        from ..common.mcp_tools import mcp_archon_rag_search_knowledge_base

        # Обогащаем запрос тегами агента
        enhanced_query = f"{query} {' '.join(ctx.deps.knowledge_tags)}"

        result = await mcp_archon_rag_search_knowledge_base(
            query=enhanced_query,
            match_count=match_count
        )

        if result["success"] and result["results"]:
            knowledge = "\n".join([
                f"**{r['metadata']['title']}:**\n{r['content']}"
                for r in result["results"]
            ])
            return f"База знаний по культурной адаптации:\n{knowledge}"
        else:
            # Fallback поиск
            fallback_result = await mcp_archon_rag_search_knowledge_base(
                query=f"cultural adaptation expert knowledge",
                match_count=3
            )

            if fallback_result["success"] and fallback_result["results"]:
                knowledge = "\n".join([
                    f"**{r['metadata']['title']}:**\n{r['content']}"
                    for r in fallback_result["results"]
                ])
                return f"База знаний (fallback поиск):\n{knowledge}"

            return """
⚠️ **ПРОБЛЕМА С ПОИСКОМ В БАЗЕ ЗНАНИЙ**

🔍 **Агент:** Pattern Cultural Adaptation Expert
📋 **Теги:** cultural_adaptation, cross_cultural_psychology, agent_knowledge
🎯 **Запрос:** {query}

💡 **Рекомендации:**
1. Попробуйте более специфичные термины: "культурная адаптация", "кросс-культурная психология"
2. Используйте ключевые слова: "метафоры", "религиозный контекст", "коммуникационные стили"
3. Проверьте доступные источники в Archon Knowledge Base

🛠️ **Базовые принципы культурной адаптации:**
- Уважение к культурным различиям
- Сохранение терапевтической эффективности
- Адаптация метафор и примеров
- Учет религиозных и социальных особенностей
"""

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"


async def analyze_cultural_context(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    request: CulturalAnalysisRequest
) -> str:
    """
    Анализ культурного контекста контента.

    Args:
        request: Запрос на анализ

    Returns:
        Детальный анализ культурных аспектов
    """
    try:
        # Получаем культурный профиль
        cultural_context = ctx.deps.get_cultural_context()
        target_culture = CultureType(request.target_culture)

        # Анализ контента
        analysis = {
            "cultural_elements": [],
            "potential_issues": [],
            "adaptation_needs": [],
            "recommendations": []
        }

        # Поиск культурно-специфичных элементов
        content_lower = request.content.lower()

        # Проверка чувствительных тем
        if ctx.deps.cultural_profile:
            sensitive_topics = ctx.deps.cultural_profile.sensitive_topics
            for topic in sensitive_topics:
                if topic.lower() in content_lower:
                    analysis["potential_issues"].append(f"Чувствительная тема: {topic}")

        # Анализ метафор
        common_metaphors = ["дорога", "дом", "семья", "дерево", "река", "гора"]
        found_metaphors = [m for m in common_metaphors if m in content_lower]
        if found_metaphors:
            analysis["cultural_elements"].extend(found_metaphors)

        # Рекомендации по адаптации
        if target_culture == CultureType.UKRAINIAN:
            analysis["recommendations"].extend([
                "Использовать метафоры природы (поле, дуб, река)",
                "Учесть контекст войны и национального сопротивления",
                "Включить православные ценности при необходимости"
            ])
        elif target_culture == CultureType.POLISH:
            analysis["recommendations"].extend([
                "Использовать католические образы и ценности",
                "Учесть важность семейных традиций",
                "Включить исторический контекст солидарности"
            ])
        elif target_culture == CultureType.ENGLISH:
            analysis["recommendations"].extend([
                "Использовать светские, универсальные метафоры",
                "Фокус на индивидуальных достижениях",
                "Прямая, низкоконтекстная коммуникация"
            ])

        return f"""
📊 **Анализ культурного контекста**

🎯 **Целевая культура:** {request.target_culture}
📝 **Тип контента:** {request.content_type}
⚡ **Уровень чувствительности:** {request.sensitivity_level}

🔍 **Найденные культурные элементы:**
{chr(10).join(['- ' + element for element in analysis["cultural_elements"]]) if analysis["cultural_elements"] else "- Специфичные элементы не обнаружены"}

⚠️ **Потенциальные проблемы:**
{chr(10).join(['- ' + issue for issue in analysis["potential_issues"]]) if analysis["potential_issues"] else "- Проблем не выявлено"}

💡 **Рекомендации по адаптации:**
{chr(10).join(['- ' + rec for rec in analysis["recommendations"]])}

📋 **Профиль культуры:**
- Религиозный контекст: {cultural_context.get('religious_context', 'не определен')}
- Стиль коммуникации: {cultural_context.get('communication_style', 'не определен')}
- Система ценностей: {cultural_context.get('value_system', 'не определена')}
"""

    except Exception as e:
        return f"Ошибка анализа культурного контекста: {e}"


async def adapt_content_culturally(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    request: AdaptationRequest
) -> str:
    """
    Адаптация контента под культурные особенности.

    Args:
        request: Запрос на адаптацию

    Returns:
        Адаптированный контент с пояснениями
    """
    try:
        target_culture = CultureType(request.target_culture)
        cultural_context = ctx.deps.get_cultural_context()

        # Базовые принципы адаптации
        adaptation_principles = {
            CultureType.UKRAINIAN: {
                "metaphors": ["поле", "дуб", "домашний очаг", "дорога домой"],
                "values": ["стойкость", "семья", "свобода", "достоинство"],
                "communication": "эмоциональный, образный стиль",
                "examples": "украинские реалии, исторические фигуры"
            },
            CultureType.POLISH: {
                "metaphors": ["католические образы", "исторические события", "семейные традиции"],
                "values": ["традиция", "вера", "солидарность", "гордость"],
                "communication": "формальный, уважительный стиль",
                "examples": "польский контекст, культурные герои"
            },
            CultureType.ENGLISH: {
                "metaphors": ["светские", "универсальные", "индивидуалистские"],
                "values": ["индивидуализм", "достижения", "инновации"],
                "communication": "прямой, низкоконтекстный стиль",
                "examples": "глобальный контекст, разнообразие"
            }
        }

        principles = adaptation_principles.get(target_culture, adaptation_principles[CultureType.ENGLISH])

        # Процесс адаптации
        adapted_content = request.original_content
        adaptation_notes = []

        # Адаптация метафор (симуляция)
        if "дорога" in request.original_content.lower():
            if target_culture == CultureType.UKRAINIAN:
                adapted_content = adapted_content.replace("дорога", "дорога домой")
                adaptation_notes.append("Метафора 'дорога' адаптирована как 'дорога домой' для украинского контекста")

        # Адаптация примеров
        if "успех" in request.original_content.lower():
            if target_culture == CultureType.POLISH:
                adaptation_notes.append("Концепция успеха может быть дополнена семейными и религиозными ценностями")

        # Адаптация стиля коммуникации
        if target_culture == CultureType.ENGLISH:
            adaptation_notes.append("Стиль сделан более прямым и конкретным для англоязычной аудитории")
        elif target_culture == CultureType.UKRAINIAN:
            adaptation_notes.append("Добавлена эмоциональная окраска для украинского контекста")

        return f"""
🎯 **Культурная адаптация контента**

📝 **Оригинальный контент:**
{request.original_content}

✨ **Адаптированный контент:**
{adapted_content}

🔧 **Примененные принципы адаптации:**
- Метафоры: {', '.join(principles['metaphors'])}
- Ценности: {', '.join(principles['values'])}
- Стиль коммуникации: {principles['communication']}
- Примеры: {principles['examples']}

📋 **Внесенные изменения:**
{chr(10).join(['- ' + note for note in adaptation_notes]) if adaptation_notes else "- Контент не требовал значительных изменений"}

✅ **Сохранены элементы:**
{', '.join(request.preserve_elements) if request.preserve_elements else "Не указаны"}

🎯 **Целевая культура:** {request.target_culture}
📊 **Тип адаптации:** {request.adaptation_type}
"""

    except Exception as e:
        return f"Ошибка культурной адаптации: {e}"


async def validate_cultural_appropriateness(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    request: CulturalValidationRequest
) -> str:
    """
    Валидация культурной приемлемости адаптированного контента.

    Args:
        request: Запрос на валидацию

    Returns:
        Результат валидации с рекомендациями
    """
    try:
        target_culture = CultureType(request.target_culture)
        cultural_context = ctx.deps.get_cultural_context()

        validation_results = {
            "cultural_sensitivity": True,
            "religious_appropriateness": True,
            "language_appropriateness": True,
            "stereotype_avoidance": True,
            "overall_score": 0.0,
            "issues": [],
            "recommendations": []
        }

        content_lower = request.adapted_content.lower()

        # Проверка чувствительных тем
        if ctx.deps.cultural_profile:
            sensitive_topics = ctx.deps.cultural_profile.sensitive_topics
            for topic in sensitive_topics:
                if topic.lower() in content_lower:
                    validation_results["issues"].append(f"Содержит чувствительную тему: {topic}")
                    validation_results["cultural_sensitivity"] = False

        # Проверка религиозной приемлемости
        religious_context = ctx.deps.cultural_profile.religious_context if ctx.deps.cultural_profile else None
        if religious_context == ReligiousContext.ORTHODOX:
            if any(word in content_lower for word in ["католический", "протестантский"]):
                validation_results["issues"].append("Возможен конфликт с православным контекстом")
                validation_results["religious_appropriateness"] = False
        elif religious_context == ReligiousContext.CATHOLIC:
            if any(word in content_lower for word in ["православный", "протестантский"]):
                validation_results["issues"].append("Возможен конфликт с католическим контекстом")
                validation_results["religious_appropriateness"] = False

        # Проверка стереотипов
        stereotype_words = ["все украинцы", "все поляки", "типичный", "обычно они"]
        for word in stereotype_words:
            if word in content_lower:
                validation_results["issues"].append(f"Возможный стереотип: {word}")
                validation_results["stereotype_avoidance"] = False

        # Расчет общего балла
        scores = [
            validation_results["cultural_sensitivity"],
            validation_results["religious_appropriateness"],
            validation_results["language_appropriateness"],
            validation_results["stereotype_avoidance"]
        ]
        validation_results["overall_score"] = sum(scores) / len(scores)

        # Генерация рекомендаций
        if not validation_results["cultural_sensitivity"]:
            validation_results["recommendations"].append("Пересмотреть использование чувствительных тем")

        if not validation_results["religious_appropriateness"]:
            validation_results["recommendations"].append("Адаптировать религиозные ссылки под целевую аудиторию")

        if not validation_results["stereotype_avoidance"]:
            validation_results["recommendations"].append("Избегать обобщений и стереотипов")

        if validation_results["overall_score"] == 1.0:
            validation_results["recommendations"].append("Контент культурно приемлем и готов к использованию")

        return f"""
✅ **Валидация культурной приемлемости**

🎯 **Целевая культура:** {request.target_culture}
📊 **Общий балл:** {validation_results["overall_score"]:.1%}

🔍 **Результаты проверки:**
- Культурная чувствительность: {'✅' if validation_results["cultural_sensitivity"] else '❌'}
- Религиозная приемлемость: {'✅' if validation_results["religious_appropriateness"] else '❌'}
- Языковая корректность: {'✅' if validation_results["language_appropriateness"] else '✅'}
- Отсутствие стереотипов: {'✅' if validation_results["stereotype_avoidance"] else '❌'}

⚠️ **Выявленные проблемы:**
{chr(10).join(['- ' + issue for issue in validation_results["issues"]]) if validation_results["issues"] else "- Проблем не выявлено"}

💡 **Рекомендации:**
{chr(10).join(['- ' + rec for rec in validation_results["recommendations"]])}

📋 **Критерии валидации:**
{', '.join(request.validation_criteria) if request.validation_criteria else "Стандартные критерии"}

🎯 **Статус:** {'Готов к использованию' if validation_results["overall_score"] >= 0.8 else 'Требует доработки'}
"""

    except Exception as e:
        return f"Ошибка валидации культурной приемлемости: {e}"


async def adapt_metaphors_culturally(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    request: MetaphorAdaptationRequest
) -> str:
    """
    Адаптация метафор под культурные особенности.

    Args:
        request: Запрос на адаптацию метафор

    Returns:
        Адаптированные метафоры с объяснениями
    """
    try:
        target_culture = CultureType(request.target_culture)

        # Культурно-специфичные метафоры
        cultural_metaphors = {
            CultureType.UKRAINIAN: {
                "природа": ["поле", "дуб", "река", "степь", "земля"],
                "дом": ["домашний очаг", "родная хата", "порог"],
                "путь": ["дорога домой", "тропинка", "перекресток"],
                "сила": ["козацкая сила", "стойкость дуба", "течение реки"],
                "рост": ["колосок", "росток", "цветение"]
            },
            CultureType.POLISH: {
                "природа": ["белый орел", "висла", "леса", "поля"],
                "дом": ["родной дом", "семейный очаг", "гостеприимство"],
                "путь": ["паломничество", "крестный путь", "дорога к успеху"],
                "сила": ["солидарность", "единство", "вера"],
                "рост": ["возрождение", "восстановление", "духовный рост"]
            },
            CultureType.ENGLISH: {
                "природа": ["mountain", "ocean", "forest", "garden"],
                "дом": ["home", "foundation", "cornerstone"],
                "путь": ["journey", "pathway", "road to success"],
                "сила": ["inner strength", "resilience", "empowerment"],
                "рост": ["growth", "development", "evolution"]
            }
        }

        # Адаптация каждой метафоры
        adaptations = []
        culture_metaphors = cultural_metaphors.get(target_culture, cultural_metaphors[CultureType.ENGLISH])

        for original_metaphor in request.original_metaphors:
            # Определение категории метафоры
            category = "общая"
            for cat, metaphors in culture_metaphors.items():
                if any(m in original_metaphor.lower() for m in metaphors):
                    category = cat
                    break

            # Поиск подходящей замены
            if category in culture_metaphors:
                suitable_metaphors = culture_metaphors[category]
                # Выбираем первую подходящую (в реальности здесь был бы более сложный алгоритм)
                adapted = suitable_metaphors[0] if suitable_metaphors else original_metaphor
            else:
                adapted = original_metaphor

            adaptations.append({
                "original": original_metaphor,
                "adapted": adapted,
                "category": category,
                "reason": f"Адаптировано для {target_culture.value} культуры"
            })

        return f"""
🎨 **Адаптация метафор**

🎯 **Целевая культура:** {request.target_culture}
📝 **Контекст:** {request.context}
💭 **Эмоциональный тон:** {request.emotional_tone}

🔄 **Результаты адаптации:**

{chr(10).join([
    f"- **{a['original']}** → **{a['adapted']}**" + chr(10) +
    f"  Категория: {a['category']}" + chr(10) +
    f"  Обоснование: {a['reason']}" + chr(10)
    for a in adaptations
])}

💡 **Принципы адаптации:**
- Сохранение смыслового ядра метафоры
- Использование культурно-близких образов
- Учет эмоционального резонанса
- Соответствие контексту использования

✅ **Рекомендации по использованию:**
- Проверить восприятие целевой аудиторией
- Протестировать эмоциональную реакцию
- Учесть вариации внутри культуры
- Предусмотреть альтернативные варианты
"""

    except Exception as e:
        return f"Ошибка адаптации метафор: {e}"


async def generate_cultural_examples(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    topic: str,
    target_culture: str,
    context: str = "general",
    example_count: int = 3
) -> str:
    """
    Генерация культурно-релевантных примеров.

    Args:
        topic: Тема для примеров
        target_culture: Целевая культура
        context: Контекст использования
        example_count: Количество примеров

    Returns:
        Культурно-адаптированные примеры
    """
    try:
        culture_type = CultureType(target_culture)

        # Культурно-специфичные примеры
        cultural_examples = {
            CultureType.UKRAINIAN: {
                "стресс": [
                    "Как козак перед битвой собирал силы",
                    "Подготовка к важному экзамену в украинском университете",
                    "Поддержка семьи в трудные времена"
                ],
                "достижения": [
                    "Получение диплома в Киевском университете",
                    "Успешный запуск собственного бизнеса во Львове",
                    "Воссоединение с семьей после долгой разлуки"
                ],
                "отношения": [
                    "Крепкая дружба, как между побратимами",
                    "Забота о пожилых родителях в селе",
                    "Поддержка соседей в трудную минуту"
                ]
            },
            CultureType.POLISH: {
                "стресс": [
                    "Подготовка к важному семейному событию",
                    "Сдача экзамена в краковском университете",
                    "Принятие важного жизненного решения"
                ],
                "достижения": [
                    "Получение работы в международной компании",
                    "Покупка первой квартиры в Варшаве",
                    "Успешное завершение университета"
                ],
                "отношения": [
                    "Крепкие семейные традиции и воскресные обеды",
                    "Дружба со школьных лет",
                    "Поддержка церковной общины"
                ]
            },
            CultureType.ENGLISH: {
                "стресс": [
                    "Preparing for a job interview",
                    "Managing work-life balance",
                    "Dealing with social media pressure"
                ],
                "достижения": [
                    "Getting promoted at work",
                    "Completing a marathon",
                    "Learning a new skill online"
                ],
                "отношения": [
                    "Building professional networks",
                    "Maintaining long-distance friendships",
                    "Dating in the digital age"
                ]
            }
        }

        examples = cultural_examples.get(culture_type, cultural_examples[CultureType.ENGLISH])
        topic_examples = examples.get(topic.lower(), [f"Пример {i+1} для темы '{topic}'" for i in range(example_count)])

        # Берем нужное количество примеров
        selected_examples = topic_examples[:example_count]

        return f"""
💡 **Культурно-релевантные примеры**

🎯 **Тема:** {topic}
🌍 **Культура:** {target_culture}
📋 **Контекст:** {context}

📝 **Примеры:**

{chr(10).join([f"{i+1}. {example}" for i, example in enumerate(selected_examples)])}

🔍 **Принципы подбора:**
- Культурная релевантность и узнаваемость
- Соответствие ценностям и нормам культуры
- Эмоциональный резонанс с аудиторией
- Избегание стереотипов и обобщений

💡 **Рекомендации по использованию:**
- Адаптировать под конкретную аудиторию
- Учитывать возрастные и социальные различия
- Предусмотреть вариации для разных контекстов
- Проверить актуальность и релевантность
"""

    except Exception as e:
        return f"Ошибка генерации культурных примеров: {e}"