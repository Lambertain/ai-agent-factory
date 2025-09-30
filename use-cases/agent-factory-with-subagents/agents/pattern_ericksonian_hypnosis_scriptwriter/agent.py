"""
Pattern Ericksonian Hypnosis Scriptwriter Agent

Специализированный агент для создания гипнотических скриптов и паттернов
в рамках системы PatternShift с полной интеграцией коллективных инструментов.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Union
from pydantic_ai import Agent, RunContext

from .settings import get_llm_model
from .dependencies import PatternEricksonianHypnosisScriptwriterDependencies
from .prompts import get_system_prompt
from .models import (
    HypnoticScript,
    TranceDepth,
    HypnoticTechnique,
    TherapeuticGoal,
    ScriptComponent
)
from .tools import (
    create_hypnotic_script,
    generate_embedded_commands,
    create_therapeutic_metaphor,
    assess_script_safety,
    adapt_trance_depth,
    search_agent_knowledge
)

# Попытка импорта универсальных декораторов
try:
    from ..common.pydantic_ai_decorators import (
        create_universal_pydantic_agent,
        with_integrations,
        register_agent
    )
    HAS_DECORATORS = True
except ImportError:
    HAS_DECORATORS = False

# Импорт обязательных инструментов коллективной работы
try:
    from ..common.collective_work_tools import (
        break_down_to_microtasks,
        report_microtask_progress,
        reflect_and_improve,
        check_delegation_need,
        delegate_task_to_agent
    )
    HAS_COLLECTIVE_TOOLS = True
except ImportError:
    HAS_COLLECTIVE_TOOLS = False

logger = logging.getLogger(__name__)

# === СОЗДАНИЕ АГЕНТА С ПОЛНОЙ ИНТЕГРАЦИЕЙ ===

if HAS_DECORATORS:
    # Используем новую универсальную архитектуру с автоматическими интеграциями
    agent = create_universal_pydantic_agent(
        model=get_llm_model(),
        deps_type=PatternEricksonianHypnosisScriptwriterDependencies,
        system_prompt=lambda deps: get_system_prompt(deps),
        agent_type="pattern_ericksonian_hypnosis_scriptwriter",
        knowledge_tags=["pattern-ericksonian-hypnosis", "hypnosis", "milton-model", "patternshift"],
        knowledge_domain="patternshift.com",
        with_collective_tools=True,
        with_knowledge_tool=True
    )
    logger.info("Pattern Ericksonian Hypnosis Scriptwriter Agent создан с универсальными декораторами")
else:
    # Fallback для старой архитектуры
    agent = Agent(
        model=get_llm_model(),
        deps_type=PatternEricksonianHypnosisScriptwriterDependencies,
        system_prompt=lambda deps: get_system_prompt(deps)
    )

    # Добавляем инструменты вручную
    agent.tool(search_agent_knowledge)

    # Добавляем обязательные инструменты коллективной работы вручную
    if HAS_COLLECTIVE_TOOLS:
        agent.tool(break_down_to_microtasks)
        agent.tool(report_microtask_progress)
        agent.tool(reflect_and_improve)
        agent.tool(check_delegation_need)
        agent.tool(delegate_task_to_agent)
        logger.info("Добавлены обязательные инструменты коллективной работы")

    logger.info("Pattern Ericksonian Hypnosis Scriptwriter Agent создан с fallback архитектурой")

# === РЕГИСТРАЦИЯ СПЕЦИАЛИЗИРОВАННЫХ ИНСТРУМЕНТОВ ГИПНОТЕРАПИИ ===

@agent.tool
async def create_full_hypnotic_script(
    ctx: RunContext[PatternEricksonianHypnosisScriptwriterDependencies],
    script_title: str,
    therapeutic_goal: str,
    target_problem: str,
    trance_depth: str = "medium",
    duration_minutes: int = 20,
    include_metaphor: bool = True
) -> str:
    """
    Создание полного гипнотического скрипта на основе терапевтической цели.

    Args:
        ctx: Контекст выполнения с зависимостями
        script_title: Название скрипта
        therapeutic_goal: Терапевтическая цель (релаксация, преодоление страха, уверенность)
        target_problem: Конкретная проблема клиента
        trance_depth: Глубина транса ("light", "medium", "deep")
        duration_minutes: Длительность скрипта в минутах
        include_metaphor: Включать ли терапевтическую метафору

    Returns:
        JSON строка с готовым гипнотическим скриптом
    """
    try:
        from .models import TranceDepth, TherapeuticGoal

        # Преобразование строки в enum
        depth_map = {
            "light": TranceDepth.LIGHT,
            "medium": TranceDepth.MEDIUM,
            "deep": TranceDepth.DEEP
        }
        depth = depth_map.get(trance_depth.lower(), TranceDepth.MEDIUM)

        # Оценка безопасности темы
        safety_check = await assess_script_safety(target_problem, therapeutic_goal)

        if not safety_check["is_safe"]:
            return f"Предупреждение: {safety_check['warning']}. Рекомендуется консультация специалиста."

        # Создание основного скрипта
        script = await create_hypnotic_script(
            title=script_title,
            goal=therapeutic_goal,
            problem=target_problem,
            depth=depth,
            duration=duration_minutes
        )

        # Генерация встроенных команд
        commands = await generate_embedded_commands(
            therapeutic_goal=therapeutic_goal,
            target_context=target_problem
        )

        # Создание метафоры если нужно
        metaphor = None
        if include_metaphor:
            metaphor = await create_therapeutic_metaphor(
                problem=target_problem,
                desired_outcome=therapeutic_goal
            )

        # Адаптация глубины транса
        adapted_script = await adapt_trance_depth(
            script=script,
            target_depth=depth,
            client_context=target_problem
        )

        result = {
            "title": script_title,
            "therapeutic_goal": therapeutic_goal,
            "trance_depth": trance_depth,
            "duration_minutes": duration_minutes,
            "structure": {
                "induction": adapted_script["induction"],
                "deepening": adapted_script["deepening"],
                "therapeutic_work": adapted_script["therapeutic_work"],
                "posthypnotic_suggestions": adapted_script["posthypnotic_suggestions"],
                "emergence": adapted_script["emergence"]
            },
            "embedded_commands": commands,
            "metaphor": metaphor if metaphor else "Не включена",
            "safety_notes": safety_check.get("recommendations", []),
            "usage_instructions": [
                "Читать медленно, с паузами",
                "Выделять встроенные команды интонацией",
                "Адаптировать под личный темп",
                "Можно прервать в любой момент"
            ]
        }

        import json
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка создания скрипта: {str(e)}"


@agent.tool
async def create_milton_model_patterns(
    ctx: RunContext[PatternEricksonianHypnosisScriptwriterDependencies],
    therapeutic_message: str,
    pattern_types: List[str] = None
) -> str:
    """
    Создание языковых паттернов Милтон-модели для непрямого внушения.

    Args:
        ctx: Контекст выполнения
        therapeutic_message: Основное терапевтическое сообщение
        pattern_types: Типы паттернов (nominalizations, unspecified_verbs, double_binds и т.д.)

    Returns:
        Примеры паттернов для данного сообщения
    """
    try:
        if pattern_types is None:
            pattern_types = [
                "nominalizations",
                "unspecified_verbs",
                "double_binds",
                "embedded_commands",
                "presuppositions"
            ]

        patterns = {}

        for pattern_type in pattern_types:
            if pattern_type == "nominalizations":
                patterns["nominalizations"] = [
                    f"И по мере того как происходит осознание...",
                    f"Это понимание приходит само...",
                    f"Трансформация начинается сейчас..."
                ]
            elif pattern_type == "unspecified_verbs":
                patterns["unspecified_verbs"] = [
                    f"Ты можешь заметить изменения...",
                    f"Это происходит естественно...",
                    f"Подсознание работает..."
                ]
            elif pattern_type == "double_binds":
                patterns["double_binds"] = [
                    f"Неважно, быстро или медленно ты {therapeutic_message.lower()}...",
                    f"Ты можешь {therapeutic_message.lower()} сейчас или через минуту...",
                    f"Не знаю, что произойдёт сначала: {therapeutic_message.lower()} или..."
                ]
            elif pattern_type == "embedded_commands":
                patterns["embedded_commands"] = [
                    f"Я не знаю, как быстро ты можешь {therapeutic_message.upper()}, но...",
                    f"Интересно, когда именно ты {therapeutic_message.upper()}...",
                    f"Подсознание уже знает, как {therapeutic_message.upper()}..."
                ]
            elif pattern_type == "presuppositions":
                patterns["presuppositions"] = [
                    f"Когда ты {therapeutic_message.lower()}, заметь изменения...",
                    f"После того как ты {therapeutic_message.lower()}, станет легче...",
                    f"Пока ты {therapeutic_message.lower()}, всё остальное становится проще..."
                ]

        import json
        return json.dumps({
            "therapeutic_message": therapeutic_message,
            "milton_model_patterns": patterns,
            "usage_tips": [
                "Комбинируйте разные паттерны в одном предложении",
                "Используйте паузы перед встроенными командами",
                "Варьируйте интонацию для усиления эффекта"
            ]
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка генерации паттернов: {str(e)}"


# === ФУНКЦИЯ ЗАПУСКА АГЕНТА ===

async def run_pattern_ericksonian_hypnosis_scriptwriter(
    user_message: str,
    deps: Optional[PatternEricksonianHypnosisScriptwriterDependencies] = None
) -> str:
    """
    Основная функция запуска Pattern Ericksonian Hypnosis Scriptwriter Agent.

    Args:
        user_message: Сообщение пользователя с запросом
        deps: Зависимости агента (опционально)

    Returns:
        Ответ агента
    """
    if deps is None:
        from .settings import load_settings
        settings = load_settings()
        deps = PatternEricksonianHypnosisScriptwriterDependencies(
            api_key=settings.llm_api_key,
            patternshift_project_path=settings.patternshift_project_path if hasattr(settings, 'patternshift_project_path') else ""
        )

    try:
        result = await agent.run(user_message, deps=deps)
        return result.data if hasattr(result, 'data') else str(result)
    except Exception as e:
        logger.error(f"Ошибка выполнения агента: {e}")
        return f"Ошибка: {str(e)}"


# === РЕГИСТРАЦИЯ АГЕНТА В ГЛОБАЛЬНОМ РЕЕСТРЕ ===

if HAS_DECORATORS:
    try:
        register_agent(
            "pattern_ericksonian_hypnosis_scriptwriter",
            agent,
            agent_type="pattern_content_specialist"
        )
        logger.info("Pattern Ericksonian Hypnosis Scriptwriter Agent зарегистрирован в глобальном реестре")
    except Exception as e:
        logger.warning(f"Не удалось зарегистрировать агента: {e}")