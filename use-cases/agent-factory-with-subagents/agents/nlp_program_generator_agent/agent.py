"""
NLP Program Generator Agent

Универсальный агент для создания персонализированных программ трансформации
с использованием PatternShift 2.0, NLP техник и Эриксоновского гипноза.
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import asyncio
from datetime import datetime

from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel, Field

from .dependencies import (
from ..common import check_pm_switch
    NLPProgramGeneratorDependencies,
    create_program_generator_dependencies,
    create_psychology_program_dependencies,
    create_universal_program_dependencies,
    ProgramDomain,
    SeverityLevel,
    VAKType,
    ContentFormat,
    NLPTechnique,
    EricksonianPattern,
    ProgramType
)
from .settings import load_settings
from .prompts import create_adaptive_system_prompt
from .providers import create_model_manager, TaskType
from .tools import (
    search_program_knowledge,
    generate_program_specification,
    create_daily_program_module,
    adapt_content_for_vak,
    generate_nlp_technique,
    break_down_program_creation,
    delegate_program_task
)


# === МОДЕЛИ РЕЗУЛЬТАТОВ ===

class ProgramGenerationResult(BaseModel):
    """Результат генерации программы."""
    program_id: str = Field(..., description="Уникальный ID программы")
    title: str = Field(..., description="Название программы")
    domain: str = Field(..., description="Домен программы")
    severity_level: str = Field(..., description="Уровень сложности")
    duration_days: int = Field(..., description="Продолжительность")
    daily_modules: List[Dict[str, Any]] = Field(..., description="Ежедневные модули")
    nlp_techniques_used: List[str] = Field(..., description="Использованные NLP техники")
    personalization_applied: bool = Field(..., description="Применена персонализация")
    estimated_effectiveness: float = Field(..., description="Оценка эффективности")


# === ОСНОВНОЙ АГЕНТ ===

def create_nlp_program_generator_agent(
    dependencies: Optional[NLPProgramGeneratorDependencies] = None
) -> Agent[NLPProgramGeneratorDependencies, str]:
    """Создать агент генерации NLP программ."""

    if dependencies is None:
        settings = load_settings()
        dependencies = create_universal_program_dependencies(
            api_key=settings.llm_api_key
        )

    # Создание адаптивного промпта
    system_prompt = create_adaptive_system_prompt(
        domain=dependencies.domain,
        vak_type=dependencies.vak_type,
        severity=dependencies.severity_level,
        content_format=dependencies.content_format
    )

    # Менеджер моделей для оптимизации затрат
    model_manager = create_model_manager(load_settings())
    model = model_manager.get_optimal_model_for_task(TaskType.PROGRAM_GENERATION)

    # Создание агента
    agent = Agent(
        model=model,
        deps_type=NLPProgramGeneratorDependencies,
        system_prompt=system_prompt
    )

    # Добавление инструментов
    agent.tool(search_program_knowledge)
    agent.tool(generate_program_specification)
    agent.tool(create_daily_program_module)
    agent.tool(adapt_content_for_vak)
    agent.tool(generate_nlp_technique)
    agent.tool(break_down_program_creation)
    agent.tool(delegate_program_task)

    return agent


# === ОСНОВНЫЕ ФУНКЦИИ ===

async def generate_personalized_program(
    test_results: Dict[str, Any],
    user_preferences: Dict[str, Any] = None,
    domain: str = "psychology",
    **kwargs
) -> str:
    """
    Создать персонализированную программу трансформации.

    Args:
        test_results: Результаты психологического тестирования
        user_preferences: Предпочтения пользователя
        domain: Домен программы
        **kwargs: Дополнительные параметры

    Returns:
        JSON с полной программой трансформации
    """
    try:
        # Создание зависимостей на основе результатов
        settings = load_settings()
        dependencies = create_program_generator_dependencies(
            api_key=settings.llm_api_key,
            domain=domain,
            severity=test_results.get("severity_level", "moderate"),
            vak_type=test_results.get("vak_type", "mixed"),
            **kwargs
        )

        # Создание агента
        agent = create_nlp_program_generator_agent(dependencies)

        # Формирование запроса
        user_prefs = user_preferences or {}
        request = f"""
Создай персонализированную программу трансформации на основе следующих данных:

**Результаты тестирования:**
{_format_test_results(test_results)}

**Предпочтения пользователя:**
{_format_user_preferences(user_prefs)}

**Требования к программе:**
- Домен: {domain}
- Учесть VAK тип и уровень проблемы
- Создать полную структуру программы
- Включить NLP техники и Эриксоновские паттерны
- Адаптировать под личные особенности

Создай программу с ежедневными модулями, четкими инструкциями и измеримыми результатами.
"""

        # Генерация программы
        result = await agent.run(request, deps=dependencies)
        return result.data

    except Exception as e:
        return f"Ошибка создания программы: {e}"


async def create_nlp_technique_library(
    techniques: List[str],
    domain: str = "psychology",
    vak_type: str = "mixed"
) -> Dict[str, Any]:
    """
    Создать библиотеку NLP техник для программ.

    Args:
        techniques: Список техник для создания
        domain: Домен применения
        vak_type: Тип восприятия для адаптации

    Returns:
        Словарь с техниками
    """
    try:
        settings = load_settings()
        dependencies = create_program_generator_dependencies(
            api_key=settings.llm_api_key,
            domain=domain,
            vak_type=vak_type
        )

        agent = create_nlp_program_generator_agent(dependencies)
        techniques_library = {}

        for technique_name in techniques:
            try:
                request = f"""
Создай детальное описание NLP техники "{technique_name}" для программ трансформации:

- Домен: {domain}
- VAK адаптация: {vak_type}
- Включи теоретическое обоснование
- Добавь пошаговые инструкции
- Укажи противопоказания
- Создай примеры применения

Техника должна быть безопасной для самостоятельного использования.
"""

                result = await agent.run(request, deps=dependencies)
                techniques_library[technique_name] = result.data

            except Exception as e:
                techniques_library[technique_name] = f"Ошибка создания техники: {e}"

        return {
            "domain": domain,
            "vak_type": vak_type,
            "techniques_count": len(techniques_library),
            "techniques": techniques_library,
            "created_at": datetime.now().isoformat()
        }

    except Exception as e:
        return {"error": f"Ошибка создания библиотеки: {e}"}


async def adapt_program_for_vak(
    program_content: str,
    target_vak: str
) -> str:
    """
    Адаптировать существующую программу под конкретный VAK тип.

    Args:
        program_content: Исходное содержимое программы
        target_vak: Целевой VAK тип

    Returns:
        Адаптированная программа
    """
    try:
        settings = load_settings()
        dependencies = create_universal_program_dependencies(
            api_key=settings.llm_api_key,
            vak_type=target_vak
        )

        agent = create_nlp_program_generator_agent(dependencies)

        request = f"""
Адаптируй следующую программу под {target_vak.upper()} тип восприятия:

{program_content}

Требования:
- Полная адаптация языка и метафор
- Изменение инструкций под доминирующий канал
- Сохранение эффективности техник
- Адаптация временных рамок если нужно
- Добавление VAK-специфичных элементов

Создай версию, максимально эффективную для {target_vak} типа.
"""

        result = await agent.run(request, deps=dependencies)
        return result.data

    except Exception as e:
        return f"Ошибка адаптации программы: {e}"


async def generate_program_batch(
    batch_requests: List[Dict[str, Any]],
    optimize_costs: bool = True
) -> List[Dict[str, Any]]:
    """
    Создать несколько программ в пакетном режиме.

    Args:
        batch_requests: Список запросов на создание программ
        optimize_costs: Оптимизировать затраты

    Returns:
        Список результатов
    """
    try:
        results = []
        settings = load_settings()

        # Оптимизация батча если включена
        if optimize_costs:
            model_manager = create_model_manager(settings)
            batch_requests = model_manager.optimize_batch_requests(batch_requests)

        for i, request in enumerate(batch_requests):
            try:
                print(f"Обработка запроса {i+1}/{len(batch_requests)}")

                test_results = request.get("test_results", {})
                user_preferences = request.get("user_preferences", {})
                domain = request.get("domain", "psychology")

                result = await generate_personalized_program(
                    test_results=test_results,
                    user_preferences=user_preferences,
                    domain=domain
                )

                results.append({
                    "request_id": request.get("id", f"batch_{i}"),
                    "status": "success",
                    "result": result
                })

            except Exception as e:
                results.append({
                    "request_id": request.get("id", f"batch_{i}"),
                    "status": "error",
                    "error": str(e)
                })

        return results

    except Exception as e:
        return [{"error": f"Ошибка батч-обработки: {e}"}]


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===

def _format_test_results(test_results: Dict[str, Any]) -> str:
    """Форматировать результаты тестирования."""
    formatted = []
    for key, value in test_results.items():
        formatted.append(f"- {key}: {value}")
    return "\n".join(formatted)


def _format_user_preferences(preferences: Dict[str, Any]) -> str:
    """Форматировать предпочтения пользователя."""
    if not preferences:
        return "Не указаны"

    formatted = []
    for key, value in preferences.items():
        formatted.append(f"- {key}: {value}")
    return "\n".join(formatted)


def get_nlp_program_generator_agent():
    """Получить экземпляр агента генерации программ."""
    return create_nlp_program_generator_agent()


# === ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===

async def create_psychology_program_example():
    """Пример создания психологической программы."""
    test_results = {
        "severity_level": "moderate",
        "vak_type": "kinesthetic",
        "problem_areas": ["anxiety", "self_esteem"],
        "age": 30,
        "duration_preference": "21_days"
    }

    user_preferences = {
        "content_format": "both",
        "daily_time": 25,
        "language": "ru",
        "include_audio": True
    }

    return await generate_personalized_program(
        test_results=test_results,
        user_preferences=user_preferences,
        domain="psychology"
    )


async def create_astrology_program_example():
    """Пример создания астрологической программы."""
    test_results = {
        "severity_level": "mild",
        "vak_type": "visual",
        "sun_sign": "leo",
        "moon_sign": "cancer",
        "rising_sign": "scorpio",
        "current_transits": ["saturn_return", "jupiter_conjunction"]
    }

    return await generate_personalized_program(
        test_results=test_results,
        domain="astrology"
    )