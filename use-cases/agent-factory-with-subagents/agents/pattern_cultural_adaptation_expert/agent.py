"""
Pattern Cultural Adaptation Expert Agent.

Агент для культурной адаптации психологических интервенций с учетом
культурных особенностей, религиозных контекстов и языковых нюансов.
"""

import asyncio
from typing import Dict, Any, Optional, Union
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

from .dependencies import (
    PatternCulturalAdaptationExpertDependencies,
    PatternShiftCulture,
    PatternShiftReligion,
    PatternShiftPhase,
    ModuleType,
    PATTERNSHIFT_UKRAINIAN_CONFIG,
    PATTERNSHIFT_POLISH_CONFIG,
    PATTERNSHIFT_ENGLISH_CONFIG
)
from .settings import load_settings, get_settings
from .prompts import get_system_prompt
from .tools import (
    search_agent_knowledge,
    analyze_cultural_context,
    adapt_content_culturally,
    validate_cultural_appropriateness,
    adapt_metaphors_culturally,
    generate_cultural_examples,
    delegate_to_pattern_agent,
    # Новые инструменты культурного профилирования
    process_user_registration,
    get_registration_questionnaire,
    update_user_cultural_profile,
    validate_cultural_assignment,
    # Модели данных
    CulturalAnalysisRequest,
    AdaptationRequest,
    CulturalValidationRequest,
    MetaphorAdaptationRequest,
    UserRegistrationData,
    CulturalProfileUpdateRequest
)


def get_llm_model():
    """Получить настроенную модель LLM."""
    settings = get_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)


# Создание агента
agent = Agent(
    get_llm_model(),
    deps_type=PatternCulturalAdaptationExpertDependencies,
    system_prompt=get_system_prompt()
)


# Регистрация инструментов
agent.tool(search_agent_knowledge)
agent.tool(analyze_cultural_context)
agent.tool(adapt_content_culturally)
agent.tool(validate_cultural_appropriateness)
agent.tool(adapt_metaphors_culturally)
agent.tool(generate_cultural_examples)
agent.tool(delegate_to_pattern_agent)

# Новые инструменты культурного профилирования
agent.tool(process_user_registration)
agent.tool(get_registration_questionnaire)
agent.tool(update_user_cultural_profile)
agent.tool(validate_cultural_assignment)


@agent.tool
async def set_target_patternshift_culture(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    culture: str,
    phase: str = "beginning",
    update_profile: bool = True
) -> str:
    """
    Установить целевую культуру PatternShift для адаптации.

    Args:
        culture: Код культуры PatternShift (ukrainian, polish, english)
        phase: Фаза программы (beginning, development, integration)
        update_profile: Обновить культурный профиль

    Returns:
        Подтверждение изменения
    """
    try:
        culture_type = PatternShiftCulture(culture.lower())
        phase_type = PatternShiftPhase(phase.lower())

        if culture_type not in ctx.deps.supported_cultures:
            return f"❌ Культура '{culture}' не поддерживается в PatternShift. Доступные: {[c.value for c in ctx.deps.supported_cultures]}"

        # Обновляем целевую культуру и фазу
        ctx.deps.target_culture = culture_type
        if update_profile and ctx.deps.cultural_profile:
            ctx.deps.cultural_profile.culture = culture_type
            ctx.deps.cultural_profile.phase = phase_type

        return f"""
✅ **PatternShift культура установлена: {culture_type.value}**
📅 **Фаза программы: {phase_type.value}**

📋 **PatternShift профиль:**
- Религиозный контекст: {ctx.deps.cultural_profile.religion.value if ctx.deps.cultural_profile else 'не определен'}
- Программа: 21-дневная трансформация
- Архитектура: Program→Phase→Day→Session→Activity→Module

⚠️ **Чувствительные темы:**
{chr(10).join(['- ' + topic for topic in ctx.deps.cultural_profile.sensitive_topics]) if ctx.deps.cultural_profile else '- не определены'}

🎯 **Культурные метафоры:**
{chr(10).join(['- ' + metaphor for metaphor in ctx.deps.cultural_profile.preferred_metaphors]) if ctx.deps.cultural_profile else '- не определены'}

✨ **Готов к культурной адаптации PatternShift модулей для {culture_type.value} аудитории!**
"""

    except ValueError as e:
        return f"❌ Неверный код культуры или фазы: {culture}/{phase}. Доступные культуры: ukrainian, polish, english. Фазы: beginning, development, integration"
    except Exception as e:
        return f"❌ Ошибка установки культуры: {e}"


@agent.tool
async def get_adaptation_recommendations(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    content_type: str,
    target_audience: str = "general",
    sensitivity_level: str = "moderate"
) -> str:
    """
    Получить рекомендации по адаптации для типа контента.

    Args:
        content_type: Тип контента (therapy, education, self_help, training)
        target_audience: Целевая аудитория (adults, teens, elderly, professionals)
        sensitivity_level: Уровень чувствительности (low, moderate, high)

    Returns:
        Детальные рекомендации по адаптации
    """
    try:
        cultural_context = ctx.deps.get_patternshift_cultural_context()
        target_culture = ctx.deps.target_culture

        recommendations = {
            "metaphor_guidelines": [],
            "communication_style": [],
            "content_adjustments": [],
            "cultural_elements": [],
            "avoidance_list": []
        }

        # Рекомендации по метафорам
        if target_culture == PatternShiftCulture.UKRAINIAN:
            recommendations["metaphor_guidelines"].extend([
                "Используйте природные метафоры: поле, дуб, река",
                "Включайте образы дома и семейного очага",
                "Применяйте метафоры пути и дороги домой",
                "Используйте образы стойкости и выносливости"
            ])
        elif target_culture == PatternShiftCulture.POLISH:
            recommendations["metaphor_guidelines"].extend([
                "Используйте католические образы и символы",
                "Включайте семейные и традиционные метафоры",
                "Применяйте исторические аналогии",
                "Используйте образы солидарности и единства"
            ])
        elif target_culture == PatternShiftCulture.ENGLISH:
            recommendations["metaphor_guidelines"].extend([
                "Используйте светские, универсальные метафоры",
                "Включайте образы индивидуального роста",
                "Применяйте бизнес и спортивные аналогии",
                "Используйте технологические метафоры"
            ])

        # Рекомендации по стилю коммуникации
        if cultural_context.get('communication_style') == 'high_context':
            recommendations["communication_style"].extend([
                "Используйте непрямую коммуникацию",
                "Включайте контекстуальные подсказки",
                "Применяйте эмоциональную окраску",
                "Используйте истории и притчи"
            ])
        elif cultural_context.get('communication_style') == 'low_context':
            recommendations["communication_style"].extend([
                "Используйте прямую коммуникацию",
                "Будьте конкретны и точны",
                "Избегайте двусмысленности",
                "Структурируйте информацию логично"
            ])

        # Настройки под аудиторию
        if target_audience == "elderly":
            recommendations["content_adjustments"].extend([
                "Используйте традиционные ценности и образы",
                "Включайте исторические референсы",
                "Избегайте современного сленга",
                "Уважайте жизненный опыт"
            ])
        elif target_audience == "teens":
            recommendations["content_adjustments"].extend([
                "Используйте современные примеры",
                "Включайте технологические аналогии",
                "Применяйте актуальные культурные референсы",
                "Учитывайте межпоколенческие различия"
            ])

        # Чувствительные темы для избегания
        sensitive_topics = cultural_context.get('sensitive_topics', [])
        if sensitive_topics:
            recommendations["avoidance_list"].extend([
                f"Избегайте прямых упоминаний: {', '.join(sensitive_topics)}",
                "Будьте осторожны с политическими референсами",
                "Учитывайте религиозную чувствительность",
                "Избегайте культурных стереотипов"
            ])

        return f"""
🎯 **Рекомендации по адаптации**

📋 **Параметры:**
- Тип контента: {content_type}
- Целевая аудитория: {target_audience}
- Уровень чувствительности: {sensitivity_level}
- Целевая культура: {target_culture.value}

🎨 **Рекомендации по метафорам:**
{chr(10).join(['- ' + rec for rec in recommendations["metaphor_guidelines"]])}

💬 **Стиль коммуникации:**
{chr(10).join(['- ' + rec for rec in recommendations["communication_style"]])}

📝 **Настройки контента:**
{chr(10).join(['- ' + rec for rec in recommendations["content_adjustments"]])}

⚠️ **Что избегать:**
{chr(10).join(['- ' + rec for rec in recommendations["avoidance_list"]])}

✅ **Следующие шаги:**
1. Применить рекомендации к вашему контенту
2. Провести анализ культурного контекста
3. Выполнить адаптацию с учетом рекомендаций
4. Провести валидацию результата
"""

    except Exception as e:
        return f"❌ Ошибка получения рекомендаций: {e}"


@agent.tool
async def comprehensive_cultural_analysis(
    ctx: RunContext[PatternCulturalAdaptationExpertDependencies],
    content: str,
    target_culture: str,
    include_suggestions: bool = True
) -> str:
    """
    Комплексный анализ контента с рекомендациями по адаптации.

    Args:
        content: Контент для анализа
        target_culture: Целевая культура
        include_suggestions: Включить предложения по улучшению

    Returns:
        Полный анализ с рекомендациями
    """
    try:
        # Анализ культурного контекста
        analysis_request = CulturalAnalysisRequest(
            content=content,
            target_culture=target_culture,
            content_type="comprehensive",
            sensitivity_level="high"
        )

        analysis_result = await analyze_cultural_context(ctx, analysis_request)

        result = f"🔍 **Комплексный культурный анализ**\n\n{analysis_result}"

        if include_suggestions:
            # Получение рекомендаций по адаптации
            adaptation_recs = await get_adaptation_recommendations(
                ctx,
                content_type="comprehensive",
                target_audience="general",
                sensitivity_level="high"
            )

            result += f"\n\n{adaptation_recs}"

            # Генерация примеров адаптации
            if "стресс" in content.lower() or "тревога" in content.lower():
                examples = await generate_cultural_examples(
                    ctx,
                    topic="стресс",
                    target_culture=target_culture,
                    context="therapy"
                )
                result += f"\n\n📚 **Примеры для темы стресса:**\n{examples}"

        return result

    except Exception as e:
        return f"❌ Ошибка комплексного анализа: {e}"


async def run_pattern_cultural_adaptation_expert(
    user_message: str,
    target_culture: str = "universal",
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    """
    Запустить агента культурной адаптации.

    Args:
        user_message: Сообщение пользователя
        target_culture: Целевая культура
        api_key: API ключ (если не в переменных окружения)
        **kwargs: Дополнительные параметры

    Returns:
        Ответ агента
    """
    try:
        # Загрузка настроек
        if api_key:
            deps = create_pattern_cultural_adaptation_dependencies(
                api_key=api_key,
                target_culture=PatternShiftCulture(target_culture),
                **kwargs
            )
        else:
            settings = get_settings()
            deps = create_pattern_cultural_adaptation_dependencies(
                api_key=settings.llm_api_key,
                target_culture=PatternShiftCulture(target_culture),
                **kwargs
            )

        # Обновление системного промпта под культуру
        culture_type = PatternShiftCulture(target_culture)
        system_prompt = get_system_prompt()

        # Создание агента с обновленным промптом
        cultural_agent = Agent(
            get_llm_model(),
            deps_type=PatternCulturalAdaptationExpertDependencies,
            system_prompt=system_prompt
        )

        # Регистрация инструментов
        cultural_agent.tool(search_agent_knowledge)
        cultural_agent.tool(analyze_cultural_context)
        cultural_agent.tool(adapt_content_culturally)
        cultural_agent.tool(validate_cultural_appropriateness)
        cultural_agent.tool(adapt_metaphors_culturally)
        cultural_agent.tool(generate_cultural_examples)
        cultural_agent.tool(set_target_patternshift_culture)
        cultural_agent.tool(get_adaptation_recommendations)
        cultural_agent.tool(comprehensive_cultural_analysis)
        cultural_agent.tool(delegate_to_pattern_agent)

        # Запуск агента
        result = await cultural_agent.run(user_message, deps=deps)
        return result.data

    except Exception as e:
        return f"❌ Ошибка выполнения агента культурной адаптации: {e}"


# Convenience функции для быстрого использования
async def analyze_content_for_culture(
    content: str,
    target_culture: str = "universal",
    api_key: Optional[str] = None
) -> str:
    """
    Быстрый анализ контента для культуры.

    Args:
        content: Контент для анализа
        target_culture: Целевая культура
        api_key: API ключ

    Returns:
        Результат анализа
    """
    message = f"Проанализируй следующий контент для {target_culture} культуры:\n\n{content}"
    return await run_pattern_cultural_adaptation_expert(
        message,
        target_culture=target_culture,
        api_key=api_key
    )


async def adapt_content_for_culture(
    content: str,
    target_culture: str = "universal",
    adaptation_type: str = "moderate",
    api_key: Optional[str] = None
) -> str:
    """
    Быстрая адаптация контента под культуру.

    Args:
        content: Контент для адаптации
        target_culture: Целевая культура
        adaptation_type: Тип адаптации
        api_key: API ключ

    Returns:
        Адаптированный контент
    """
    message = f"Адаптируй следующий контент для {target_culture} культуры (уровень: {adaptation_type}):\n\n{content}"
    return await run_pattern_cultural_adaptation_expert(
        message,
        target_culture=target_culture,
        api_key=api_key
    )


async def validate_cultural_content(
    content: str,
    target_culture: str = "universal",
    api_key: Optional[str] = None
) -> str:
    """
    Быстрая валидация культурной приемлемости.

    Args:
        content: Контент для валидации
        target_culture: Целевая культура
        api_key: API ключ

    Returns:
        Результат валидации
    """
    message = f"Проведи валидацию культурной приемлемости для {target_culture} культуры:\n\n{content}"
    return await run_pattern_cultural_adaptation_expert(
        message,
        target_culture=target_culture,
        api_key=api_key
    )


# Экспорт основных функций
__all__ = [
    "agent",
    "run_pattern_cultural_adaptation_expert",
    "analyze_content_for_culture",
    "adapt_content_for_culture",
    "validate_cultural_content",
    "PatternCulturalAdaptationExpertDependencies",
    "CultureType",
    "CulturalAnalysisRequest",
    "AdaptationRequest",
    "CulturalValidationRequest",
    "MetaphorAdaptationRequest"
]