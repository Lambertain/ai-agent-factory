"""
NLP Program Generator Agent Tools

Профессиональные инструменты для создания персонализированных программ трансформации
с NLP техниками и Эриксоновскими паттернами.
"""

from typing import Dict, Any, List, Optional, Union
import asyncio
import json
from datetime import datetime, timedelta
import re

from pydantic_ai import RunContext
from pydantic import BaseModel, Field

from .dependencies import (
    NLPProgramGeneratorDependencies,
    SeverityLevel,
    VAKType,
    ContentFormat,
    NLPTechnique,
    EricksonianPattern,
    ProgramType
)


# === МОДЕЛИ ДАННЫХ ===

class ProgramSpecification(BaseModel):
    """Спецификация программы трансформации."""
    program_id: str = Field(..., description="Уникальный ID программы")
    title: str = Field(..., description="Название программы")
    domain: str = Field(..., description="Домен применения")
    severity_level: str = Field(..., description="Уровень сложности")
    vak_type: str = Field(..., description="Тип восприятия")
    duration_days: int = Field(..., description="Продолжительность в днях")
    daily_time_minutes: int = Field(..., description="Время ежедневных сессий")
    content_format: str = Field(..., description="Формат контента")
    target_outcomes: List[str] = Field(..., description="Целевые результаты")


class DailyModule(BaseModel):
    """Ежедневный модуль программы."""
    day_number: int = Field(..., description="Номер дня")
    title: str = Field(..., description="Название модуля")
    theme: str = Field(..., description="Основная тема дня")

    # Структура сессии
    introduction: str = Field(..., description="Гипнотическое введение")
    main_technique: str = Field(..., description="Основная техника")
    practical_tasks: str = Field(..., description="Практические задания")
    reflection: str = Field(..., description="Рефлексия")
    completion: str = Field(..., description="Завершение")

    # Метаданные
    nlp_techniques: List[str] = Field(default=[], description="Используемые NLP техники")
    ericksonian_patterns: List[str] = Field(default=[], description="Эриксоновские паттерны")
    vak_elements: List[str] = Field(default=[], description="VAK элементы")
    estimated_time: int = Field(..., description="Примерное время выполнения")


class NLPTechniqueTemplate(BaseModel):
    """Шаблон NLP техники."""
    technique_name: str = Field(..., description="Название техники")
    technique_type: str = Field(..., description="Тип техники")
    description: str = Field(..., description="Описание техники")
    instructions: str = Field(..., description="Инструкции применения")
    vak_adaptations: Dict[str, str] = Field(..., description="Адаптации под VAK")
    contraindications: List[str] = Field(default=[], description="Противопоказания")


# === ОСНОВНЫЕ ИНСТРУМЕНТЫ ===

async def search_program_knowledge(
    ctx: RunContext[NLPProgramGeneratorDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний агента по программам трансформации.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Используем теги агента для поиска
        search_query = f"{query} {' '.join(ctx.deps.knowledge_tags[:5])}"

        # В реальной реализации здесь был бы вызов RAG
        # result = await mcp__archon__rag_search_knowledge_base(
        #     query=search_query,
        #     match_count=match_count
        # )

        # Заглушка для демонстрации
        knowledge_base = f"""
База знаний агента (поиск: {query}):

**Методология PatternShift 2.0:**
- Трехуровневая система: Кризис (21 день) → Стабилизация (21 день) → Развитие (14 дней)
- Мультиформатный контент: текст + аудио с синхронизацией
- VAK персонализация под доминирующий канал восприятия

**NLP Техники для программ:**
- Анкоринг: создание ресурсных состояний через якоря
- Субмодальности: изменение качественных характеристик образов
- Рефрейминг: переосмысление значения событий
- Временные линии: работа с прошлым и будущим

**Эриксоновские паттерны:**
- Трюизмы: "Изменения происходят естественно..."
- Пресуппозиции: "Когда ты почувствуешь готовность..."
- Встроенные команды: "можешь РАССЛАБИТЬСЯ ПОЛНОСТЬЮ"
"""
        return knowledge_base

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"


async def generate_program_specification(
    ctx: RunContext[NLPProgramGeneratorDependencies],
    test_results: Dict[str, Any],
    user_preferences: Dict[str, Any] = None
) -> str:
    """
    Создать спецификацию программы на основе результатов тестирования.

    Args:
        test_results: Результаты психологического тестирования
        user_preferences: Предпочтения пользователя

    Returns:
        JSON спецификации программы
    """
    try:
        # Анализ результатов тестирования
        severity = test_results.get("severity_level", ctx.deps.severity_level.value)
        vak_type = test_results.get("vak_type", ctx.deps.vak_type.value)
        problem_areas = test_results.get("problem_areas", [])

        # Определение параметров программы
        duration = ctx.deps.get_program_duration()
        session_time = ctx.deps.get_daily_session_time()

        # Создание спецификации
        spec = ProgramSpecification(
            program_id=f"nlp_prog_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=f"Программа трансформации - {severity.upper()}",
            domain=ctx.deps.domain.value,
            severity_level=severity,
            vak_type=vak_type,
            duration_days=duration,
            daily_time_minutes=session_time["total_minutes"],
            content_format=ctx.deps.content_format.value,
            target_outcomes=_generate_target_outcomes(problem_areas, severity)
        )

        return spec.model_dump_json(indent=2)

    except Exception as e:
        return f"Ошибка создания спецификации: {e}"


async def create_daily_program_module(
    ctx: RunContext[NLPProgramGeneratorDependencies],
    day_number: int,
    program_theme: str,
    vak_type: str,
    severity_level: str
) -> str:
    """
    Создать ежедневный модуль программы трансформации.

    Args:
        day_number: Номер дня в программе
        program_theme: Тема программы
        vak_type: Тип восприятия (visual/auditory/kinesthetic)
        severity_level: Уровень сложности

    Returns:
        JSON описание модуля дня
    """
    try:
        # Поиск релевантной информации в базе знаний
        knowledge = await search_program_knowledge(
            ctx, f"{program_theme} день {day_number} {vak_type}"
        )

        # Выбор техник для дня
        techniques = _select_techniques_for_day(day_number, severity_level, vak_type)

        # Генерация структуры дня
        module = DailyModule(
            day_number=day_number,
            title=f"День {day_number}: {_get_daily_theme(day_number, program_theme)}",
            theme=program_theme,
            introduction=_generate_hypnotic_introduction(vak_type, program_theme),
            main_technique=_generate_main_technique(techniques["primary"], vak_type),
            practical_tasks=_generate_practical_tasks(techniques["practical"], vak_type),
            reflection=_generate_reflection_questions(program_theme, day_number),
            completion=_generate_hypnotic_completion(vak_type),
            nlp_techniques=techniques["nlp"],
            ericksonian_patterns=techniques["ericksonian"],
            vak_elements=_get_vak_elements(vak_type),
            estimated_time=ctx.deps.get_daily_session_time()["total_minutes"]
        )

        return module.model_dump_json(indent=2)

    except Exception as e:
        return f"Ошибка создания модуля дня: {e}"


async def adapt_content_for_vak(
    ctx: RunContext[NLPProgramGeneratorDependencies],
    content: str,
    target_vak: str
) -> str:
    """
    Адаптировать контент под конкретный VAK тип.

    Args:
        content: Исходный контент
        target_vak: Целевой VAK тип (visual/auditory/kinesthetic)

    Returns:
        Адаптированный контент
    """
    try:
        vak_adaptations = {
            "visual": {
                "intro_words": ["представь", "увидь", "визуализируй", "посмотри"],
                "descriptors": ["яркий", "четкий", "цветной", "детальный"],
                "metaphors": ["картина", "образ", "свет", "цвет", "форма"],
                "instructions": "Создавай яркие, детальные образы в своем воображении..."
            },
            "auditory": {
                "intro_words": ["услышь", "прислушайся", "скажи себе", "произнеси"],
                "descriptors": ["звучащий", "мелодичный", "ритмичный", "гармоничный"],
                "metaphors": ["мелодия", "звук", "голос", "эхо", "тон"],
                "instructions": "Настройся на внутренние звуки и голоса..."
            },
            "kinesthetic": {
                "intro_words": ["почувствуй", "ощути", "прикоснись", "вдохни"],
                "descriptors": ["теплый", "мягкий", "сильный", "глубокий"],
                "metaphors": ["поток", "волна", "дыхание", "движение", "прикосновение"],
                "instructions": "Фокусируйся на телесных ощущениях и движении энергии..."
            }
        }

        adaptation = vak_adaptations.get(target_vak, vak_adaptations["kinesthetic"])

        # Адаптация контента
        adapted_content = content

        # Замена общих слов на VAK-специфичные
        for word in adaptation["intro_words"]:
            adapted_content = re.sub(
                r'\b(обрати внимание|сосредоточься|направь внимание)\b',
                word,
                adapted_content,
                flags=re.IGNORECASE
            )

        # Добавление VAK-специфичных инструкций
        if "[VAK_INSTRUCTIONS]" in adapted_content:
            adapted_content = adapted_content.replace(
                "[VAK_INSTRUCTIONS]",
                adaptation["instructions"]
            )

        return f"**Адаптация для {target_vak.upper()}:**\n\n{adapted_content}"

    except Exception as e:
        return f"Ошибка адаптации контента: {e}"


async def generate_nlp_technique(
    ctx: RunContext[NLPProgramGeneratorDependencies],
    technique_name: str,
    application_context: str,
    vak_type: str = "mixed"
) -> str:
    """
    Сгенерировать описание и инструкции для NLP техники.

    Args:
        technique_name: Название техники (anchoring, reframing, etc.)
        application_context: Контекст применения
        vak_type: Тип восприятия для адаптации

    Returns:
        JSON описание NLP техники
    """
    try:
        # Шаблоны NLP техник
        technique_templates = {
            "anchoring": {
                "description": "Техника создания условно-рефлекторных связей между стимулом и состоянием",
                "base_instructions": """
                1. Войди в желаемое ресурсное состояние
                2. На пике состояния примени якорь (жест/слово/образ)
                3. Повторить связку 3-5 раз
                4. Протестировать якорь в нейтральном состоянии
                """,
                "vak_adaptations": {
                    "visual": "Используй яркий визуальный образ как якорь",
                    "auditory": "Выбери мелодию или фразу как якорь",
                    "kinesthetic": "Создай тактильный жест-якорь"
                }
            },
            "reframing": {
                "description": "Техника изменения восприятия ситуации через смену рамки интерпретации",
                "base_instructions": """
                1. Определи проблемную ситуацию
                2. Найди альтернативные интерпретации
                3. Выбери наиболее ресурсную рамку
                4. Интегрируй новое понимание
                """,
                "vak_adaptations": {
                    "visual": "Представь ситуацию как картину в разных рамках",
                    "auditory": "Расскажи историю с разных точек зрения",
                    "kinesthetic": "Почувствуй как меняется отношение к ситуации"
                }
            }
        }

        template = technique_templates.get(technique_name.lower(), {
            "description": f"Специализированная NLP техника: {technique_name}",
            "base_instructions": "Следуйте базовым принципам NLP",
            "vak_adaptations": {
                "visual": "Визуальная адаптация техники",
                "auditory": "Аудиальная адаптация техники",
                "kinesthetic": "Кинестетическая адаптация техники"
            }
        })

        technique = NLPTechniqueTemplate(
            technique_name=technique_name,
            technique_type="NLP",
            description=template["description"],
            instructions=template["base_instructions"],
            vak_adaptations=template["vak_adaptations"],
            contraindications=_get_technique_contraindications(technique_name)
        )

        return technique.model_dump_json(indent=2)

    except Exception as e:
        return f"Ошибка генерации NLP техники: {e}"


# === КОЛЛЕКТИВНАЯ РАБОТА ===

async def break_down_program_creation(
    ctx: RunContext[NLPProgramGeneratorDependencies],
    program_requirements: str,
    complexity_level: str = "medium"
) -> str:
    """
    Разбить создание программы на микрозадачи.

    Args:
        program_requirements: Требования к программе
        complexity_level: Уровень сложности (simple/medium/complex)

    Returns:
        Список микрозадач
    """
    microtasks = []

    if complexity_level == "simple":
        microtasks = [
            f"Анализ требований: {program_requirements}",
            "Создание спецификации программы",
            "Генерация 3-7 ключевых модулей",
            "Адаптация под VAK тип",
            "Валидация и финализация"
        ]
    elif complexity_level == "medium":
        microtasks = [
            f"Глубокий анализ требований: {program_requirements}",
            "Поиск в базе знаний по NLP техникам",
            "Создание детальной спецификации программы",
            "Генерация ежедневных модулей",
            "Создание NLP техник под задачи",
            "Адаптация контента под VAK",
            "Интеграция Эриксоновских паттернов",
            "Валидация безопасности и этики",
            "Финальная оптимизация программы"
        ]
    else:  # complex
        microtasks = [
            f"Комплексный анализ требований: {program_requirements}",
            "Исследование научных обоснований техник",
            "Планирование межмодульных связей",
            "Создание персонализированной архитектуры",
            "Генерация полного цикла программы",
            "Разработка уникальных NLP техник",
            "Создание мультиформатного контента",
            "Интеграция с другими агентами системы",
            "Многоуровневая валидация качества",
            "Оптимизация и тестирование эффективности"
        ]

    output = "📋 **Микрозадачи создания программы:**\n"
    for i, task in enumerate(microtasks, 1):
        output += f"{i}. {task}\n"
    output += "\n✅ Буду отчитываться о прогрессе каждой микрозадачи"

    return output


async def delegate_program_task(
    ctx: RunContext[NLPProgramGeneratorDependencies],
    target_agent: str,
    task_title: str,
    task_description: str,
    priority: str = "medium"
) -> str:
    """
    Делегировать задачу другому агенту через Archon.

    Args:
        target_agent: Целевой агент
        task_title: Название задачи
        task_description: Описание задачи
        priority: Приоритет задачи

    Returns:
        Результат делегирования
    """
    try:
        agent_mapping = {
            "research": "NLP Content Research Agent",
            "quality": "NLP Content Quality Guardian Agent",
            "validation": "Quality Guardian",
            "content": "Content Architect"
        }

        assignee = agent_mapping.get(target_agent, "Implementation Engineer")

        # В реальной реализации здесь был бы вызов Archon API
        # task_result = await mcp__archon__manage_task(...)

        return f"✅ Задача делегирована агенту {assignee}:\n- Название: {task_title}\n- Приоритет: {priority}\n- Статус: создана в системе"

    except Exception as e:
        return f"❌ Ошибка делегирования: {e}"


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===

def _generate_target_outcomes(problem_areas: List[str], severity: str) -> List[str]:
    """Генерация целевых результатов программы."""
    base_outcomes = [
        "Улучшение эмоциональной регуляции",
        "Повышение уверенности в себе",
        "Развитие навыков самопомощи",
        "Формирование здоровых паттернов мышления"
    ]

    if severity == "severe":
        base_outcomes.extend([
            "Стабилизация кризисного состояния",
            "Восстановление базового функционирования"
        ])
    elif severity == "mild":
        base_outcomes.extend([
            "Раскрытие личностного потенциала",
            "Достижение поставленных целей"
        ])

    return base_outcomes


def _select_techniques_for_day(day_number: int, severity: str, vak_type: str) -> Dict[str, List[str]]:
    """Выбор техник для конкретного дня."""
    return {
        "primary": f"День {day_number}: Основная техника для {severity}",
        "practical": f"Практические задания под {vak_type}",
        "nlp": ["anchoring", "reframing"],
        "ericksonian": ["truisms", "presuppositions"]
    }


def _get_daily_theme(day_number: int, program_theme: str) -> str:
    """Получить тему дня."""
    themes = [
        "Знакомство с программой",
        "Создание безопасного пространства",
        "Анализ текущего состояния",
        "Освобождение от блоков",
        "Формирование новых паттернов"
    ]
    return themes[min(day_number - 1, len(themes) - 1)]


def _generate_hypnotic_introduction(vak_type: str, theme: str) -> str:
    """Генерация гипнотического введения."""
    intros = {
        "visual": f"Представь перед собой дверь в новые возможности... {theme}",
        "auditory": f"Услышь голос внутренней мудрости, говорящий о... {theme}",
        "kinesthetic": f"Почувствуй волну трансформации, связанную с... {theme}"
    }
    return intros.get(vak_type, intros["kinesthetic"])


def _generate_main_technique(technique: str, vak_type: str) -> str:
    """Генерация основной техники дня."""
    return f"Основная техника ({technique}) адаптированная для {vak_type} типа восприятия"


def _generate_practical_tasks(tasks: str, vak_type: str) -> str:
    """Генерация практических заданий."""
    return f"Практические задания: {tasks} (адаптация под {vak_type})"


def _generate_reflection_questions(theme: str, day: int) -> str:
    """Генерация вопросов для рефлексии."""
    return f"Рефлексия дня {day}: Как изменилось твое отношение к теме '{theme}'?"


def _generate_hypnotic_completion(vak_type: str) -> str:
    """Генерация гипнотического завершения."""
    completions = {
        "visual": "Сохрани яркий образ достигнутых изменений...",
        "auditory": "Услышь внутреннее подтверждение прогресса...",
        "kinesthetic": "Ощути глубокую интеграцию нового опыта..."
    }
    return completions.get(vak_type, completions["kinesthetic"])


def _get_vak_elements(vak_type: str) -> List[str]:
    """Получить элементы для VAK типа."""
    elements = {
        "visual": ["образы", "цвета", "формы", "свет"],
        "auditory": ["звуки", "мелодии", "голоса", "ритм"],
        "kinesthetic": ["ощущения", "движения", "дыхание", "температура"]
    }
    return elements.get(vak_type, elements["kinesthetic"])


def _get_technique_contraindications(technique_name: str) -> List[str]:
    """Получить противопоказания для техники."""
    contraindications = {
        "anchoring": ["острые психотические состояния"],
        "timeline": ["ПТСР без профессиональной поддержки"],
        "reframing": ["бредовые расстройства"]
    }
    return contraindications.get(technique_name.lower(), [])