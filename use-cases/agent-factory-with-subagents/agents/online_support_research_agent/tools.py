"""
Инструменты для Psychology Research Agent

Комплексный набор инструментов для валидации психологических исследований,
анализа методологии и поддержки научной деятельности.
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import json
import asyncio
from datetime import datetime
import re
import statistics

from pydantic_ai import RunContext
from pydantic import BaseModel, Field

from .dependencies import ResearchAgentDependencies


# ===== МОДЕЛИ ДАННЫХ =====

class StudyAnalysisRequest(BaseModel):
    """Запрос на анализ исследования."""
    study_data: Dict[str, Any] = Field(description="Данные исследования для анализа")
    analysis_type: str = Field(description="Тип анализа (methodology, statistics, ethics, quality)")
    validation_level: str = Field(default="standard", description="Уровень валидации")
    focus_areas: List[str] = Field(default_factory=list, description="Области фокуса анализа")


class LiteratureSearchRequest(BaseModel):
    """Запрос на поиск литературы."""
    query: str = Field(description="Поисковый запрос")
    research_domain: str = Field(default="general", description="Домен исследований")
    study_types: List[str] = Field(default_factory=list, description="Типы исследований")
    date_range: str = Field(default="last_5_years", description="Временной диапазон")
    max_results: int = Field(default=50, description="Максимальное количество результатов")


class StatisticalValidationRequest(BaseModel):
    """Запрос на статистическую валидацию."""
    study_design: str = Field(description="Дизайн исследования")
    sample_size: int = Field(description="Размер выборки")
    statistical_methods: List[str] = Field(description="Используемые статистические методы")
    effect_sizes: List[float] = Field(default_factory=list, description="Размеры эффектов")
    power_analysis: Optional[Dict[str, Any]] = Field(default=None, description="Анализ мощности")


class MethodologyAssessmentRequest(BaseModel):
    """Запрос на оценку методологии."""
    research_question: str = Field(description="Исследовательский вопрос")
    study_design: str = Field(description="Дизайн исследования")
    participants: Dict[str, Any] = Field(description="Информация об участниках")
    procedures: Dict[str, Any] = Field(description="Процедуры исследования")
    measures: List[Dict[str, Any]] = Field(description="Используемые методики")


# ===== ОСНОВНЫЕ ИНСТРУМЕНТЫ =====

async def search_research_knowledge(
    ctx: RunContext[ResearchAgentDependencies],
    query: str,
    research_domain: Optional[str] = None,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний исследовательской методологии.

    Args:
        query: Поисковый запрос
        research_domain: Домен исследований для фильтрации
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Используем MCP Archon для поиска в базе знаний
        from mcp__archon__rag_search_knowledge_base import rag_search_knowledge_base

        # Формируем расширенный запрос с тегами агента
        enhanced_query = f"{query} {' '.join(ctx.deps.knowledge_tags)}"

        result = await rag_search_knowledge_base(
            query=enhanced_query,
            source_domain=ctx.deps.knowledge_domain,
            match_count=match_count
        )

        if result.get("success") and result.get("results"):
            knowledge = "\n".join([
                f"**{r['metadata'].get('title', 'Документ')}:**\n{r['content']}"
                for r in result["results"]
            ])
            return f"📚 База знаний Psychology Research Agent:\n{knowledge}"
        else:
            # Fallback поиск по имени агента
            fallback_result = await rag_search_knowledge_base(
                query=f"psychology research agent methodology {query}",
                match_count=3
            )

            if fallback_result.get("success") and fallback_result.get("results"):
                knowledge = "\n".join([
                    f"**{r['metadata'].get('title', 'Документ')}:**\n{r['content']}"
                    for r in fallback_result["results"]
                ])
                return f"📚 База знаний (найдено через fallback):\n{knowledge}"

            return f"""⚠️ **Не удалось найти релевантную информацию в базе знаний**

🔍 **Запрос:** {query}
📋 **Теги поиска:** {', '.join(ctx.deps.knowledge_tags)}
🎯 **Домен:** {research_domain or ctx.deps.knowledge_domain}

💡 **Рекомендации:**
1. Попробуйте более специфичные термины из области психологических исследований
2. Используйте методологические термины: "RCT", "validity", "reliability", "effect size"
3. Попробуйте поиск по стандартам: "CONSORT", "APA guidelines", "statistical power"

🛠️ **Альтернативы:**
- Поиск литературы через search_literature()
- Валидация через validate_study_methodology()
- Статистический анализ через validate_statistical_analysis()
"""

    except Exception as e:
        return f"❌ Ошибка поиска в базе знаний: {e}"


async def analyze_study_methodology(
    ctx: RunContext[ResearchAgentDependencies],
    request: MethodologyAssessmentRequest
) -> str:
    """
    Анализ методологии исследования.

    Args:
        request: Запрос на оценку методологии

    Returns:
        Детальный анализ методологии
    """
    try:
        # Получаем модель для методологического анализа
        model = ctx.deps.get_model_for_task("methodology_analysis", "complex")

        # Получаем критерии валидации
        criteria = ctx.deps.get_validation_criteria()

        analysis_prompt = f"""
Проведи экспертный анализ методологии исследования по следующим критериям:

**ИССЛЕДОВАНИЕ:**
- Вопрос: {request.research_question}
- Дизайн: {request.study_design}
- Участники: {json.dumps(request.participants, ensure_ascii=False, indent=2)}
- Процедуры: {json.dumps(request.procedures, ensure_ascii=False, indent=2)}
- Методики: {json.dumps(request.measures, ensure_ascii=False, indent=2)}

**КРИТЕРИИ ВАЛИДАЦИИ:**
{json.dumps(criteria, ensure_ascii=False, indent=2)}

**ДОМЕН:** {ctx.deps.research_domain}
**УРОВЕНЬ ВАЛИДАЦИИ:** {ctx.deps.validation_level}

Проанализируй следующие аспекты:

1. **СООТВЕТСТВИЕ ДИЗАЙНА ИССЛЕДОВАТЕЛЬСКОМУ ВОПРОСУ**
   - Адекватность дизайна для ответа на вопрос
   - Внутренняя и внешняя валидность
   - Контроль мешающих переменных

2. **КАЧЕСТВО ВЫБОРКИ**
   - Размер выборки и статистическая мощность
   - Репрезентативность популяции
   - Критерии включения/исключения

3. **ВАЛИДНОСТЬ ИЗМЕРЕНИЙ**
   - Психометрические свойства методик
   - Надежность и валидность инструментов
   - Соответствие методик целевой популяции

4. **ПРОЦЕДУРНЫЕ АСПЕКТЫ**
   - Стандартизация процедур
   - Контроль систематических ошибок
   - Этические соображения

5. **СООТВЕТСТВИЕ СТАНДАРТАМ**
   - Следование отчетным стандартам ({', '.join(ctx.deps.reporting_standards)})
   - Этическое соответствие ({', '.join(ctx.deps.ethics_standards)})

Дай оценку по 10-балльной шкале для каждого аспекта и общую рекомендацию.
"""

        # Выполняем анализ через LLM
        from pydantic_ai import Agent

        analysis_agent = Agent(model)
        result = await analysis_agent.run(analysis_prompt)

        return f"""# Анализ методологии исследования

## Исследование
**Вопрос:** {request.research_question}
**Дизайн:** {request.study_design}
**Домен:** {ctx.deps.research_domain}

## Экспертная оценка
{result.data}

## Критерии соответствия
- **Домен:** {ctx.deps.research_domain}
- **Уровень валидации:** {ctx.deps.validation_level}
- **Минимальный размер выборки:** {criteria.get('sample_size', 'не указан')}
- **Стандарты отчетности:** {', '.join(ctx.deps.reporting_standards)}

*Анализ выполнен с использованием {model.__class__.__name__}*
"""

    except Exception as e:
        return f"❌ Ошибка анализа методологии: {e}"


async def validate_statistical_analysis(
    ctx: RunContext[ResearchAgentDependencies],
    request: StatisticalValidationRequest
) -> str:
    """
    Валидация статистического анализа исследования.

    Args:
        request: Запрос на статистическую валидацию

    Returns:
        Детальная оценка статистических методов
    """
    try:
        # Получаем модель для статистической валидации
        model = ctx.deps.get_model_for_task("statistical_validation", "complex")

        # Проводим базовые проверки
        basic_checks = _perform_basic_statistical_checks(request)

        validation_prompt = f"""
Проведи экспертную валидацию статистического анализа исследования:

**СТАТИСТИЧЕСКИЕ ДАННЫЕ:**
- Дизайн: {request.study_design}
- Размер выборки: {request.sample_size}
- Методы: {', '.join(request.statistical_methods)}
- Размеры эффектов: {request.effect_sizes}
- Анализ мощности: {json.dumps(request.power_analysis, ensure_ascii=False) if request.power_analysis else 'не предоставлен'}

**КРИТЕРИИ ВАЛИДАЦИИ:**
- Минимальная мощность: {ctx.deps.min_power}
- Уровень альфа: {ctx.deps.alpha_level}
- Минимальный размер эффекта: {ctx.deps.min_effect_size}

**БАЗОВЫЕ ПРОВЕРКИ:**
{json.dumps(basic_checks, ensure_ascii=False, indent=2)}

Проанализируй:

1. **АДЕКВАТНОСТЬ СТАТИСТИЧЕСКИХ МЕТОДОВ**
   - Соответствие методов дизайну исследования
   - Выполнение предположений методов
   - Корректность выбора тестов

2. **МОЩНОСТЬ И РАЗМЕР ВЫБОРКИ**
   - Достаточность размера выборки
   - Статистическая мощность
   - Анализ чувствительности

3. **РАЗМЕРЫ ЭФФЕКТОВ**
   - Практическая значимость
   - Доверительные интервалы
   - Интерпретация размеров эффектов

4. **МНОЖЕСТВЕННЫЕ СРАВНЕНИЯ**
   - Контроль семейной ошибки I рода
   - Поправки на множественность
   - Планируемые vs. исследовательские анализы

5. **ОТЧЕТНОСТЬ**
   - Соответствие стандартам APA/CONSORT
   - Полнота статистической отчетности
   - Доступность данных для репликации

Дай рейтинг статистического качества (1-10) и конкретные рекомендации.
"""

        from pydantic_ai import Agent

        validation_agent = Agent(model)
        result = await validation_agent.run(validation_prompt)

        return f"""# Валидация статистического анализа

## Исходные данные
- **Дизайн исследования:** {request.study_design}
- **Размер выборки:** {request.sample_size}
- **Статистические методы:** {', '.join(request.statistical_methods)}

## Базовые проверки
{_format_basic_checks(basic_checks)}

## Экспертная валидация
{result.data}

## Рекомендации по улучшению
{_generate_statistical_recommendations(basic_checks, ctx.deps)}

*Валидация выполнена с использованием {model.__class__.__name__}*
"""

    except Exception as e:
        return f"❌ Ошибка валидации статистического анализа: {e}"


async def search_literature(
    ctx: RunContext[ResearchAgentDependencies],
    request: LiteratureSearchRequest
) -> str:
    """
    Поиск релевантной научной литературы.

    Args:
        request: Запрос на поиск литературы

    Returns:
        Результаты поиска литературы
    """
    try:
        # Получаем модель для литературного обзора
        model = ctx.deps.get_model_for_task("literature_review", "standard")

        # Формируем стратегию поиска
        search_strategy = ctx.deps.get_literature_search_strategy()

        search_prompt = f"""
Выполни систематический поиск научной литературы по следующим параметрам:

**ЗАПРОС:** {request.query}
**ДОМЕН:** {request.research_domain}
**ТИПЫ ИССЛЕДОВАНИЙ:** {', '.join(request.study_types) if request.study_types else 'все типы'}
**ВРЕМЕННОЙ ДИАПАЗОН:** {request.date_range}
**МАКСИМУМ РЕЗУЛЬТАТОВ:** {request.max_results}

**СТРАТЕГИЯ ПОИСКА:**
{json.dumps(search_strategy, ensure_ascii=False, indent=2)}

**БАЗЫ ДАННЫХ:** {', '.join(ctx.deps.literature_search_databases)}

Выполни следующие шаги:

1. **ФОРМИРОВАНИЕ ПОИСКОВОГО ЗАПРОСА**
   - Ключевые термины и синонимы
   - Булевы операторы
   - MeSH термины (для PubMed)
   - Ограничения поиска

2. **КРИТЕРИИ ОТБОРА**
   - Критерии включения
   - Критерии исключения
   - Фильтры качества

3. **АНАЛИЗ ЛИТЕРАТУРЫ**
   - Релевантные исследования
   - Качество доказательств
   - Пробелы в исследованиях
   - Методологические ограничения

4. **СИНТЕЗ РЕЗУЛЬТАТОВ**
   - Основные находки
   - Консенсус и противоречия
   - Практические применения
   - Направления будущих исследований

Представь результаты в структурированном виде с оценкой качества источников.
"""

        from pydantic_ai import Agent

        search_agent = Agent(model)
        result = await search_agent.run(search_prompt)

        return f"""# Результаты поиска литературы

## Параметры поиска
- **Запрос:** {request.query}
- **Домен:** {request.research_domain}
- **Базы данных:** {', '.join(ctx.deps.literature_search_databases)}
- **Диапазон:** {request.date_range}

## Стратегия поиска
{_format_search_strategy(search_strategy)}

## Результаты анализа
{result.data}

## Рекомендации для практики
{_generate_literature_recommendations(request, ctx.deps)}

*Поиск выполнен с использованием {model.__class__.__name__}*
"""

    except Exception as e:
        return f"❌ Ошибка поиска литературы: {e}"


async def evaluate_study_quality(
    ctx: RunContext[ResearchAgentDependencies],
    study_data: Dict[str, Any],
    assessment_framework: str = "custom"
) -> str:
    """
    Оценка качества исследования по стандартизированным критериям.

    Args:
        study_data: Данные исследования
        assessment_framework: Используемый фреймворк оценки

    Returns:
        Комплексная оценка качества исследования
    """
    try:
        # Получаем модель для анализа качества
        model = ctx.deps.get_model_for_task("methodology_analysis", "complex")

        # Определяем фреймворк оценки
        framework_criteria = _get_quality_assessment_framework(
            assessment_framework,
            ctx.deps.research_domain
        )

        quality_prompt = f"""
Проведи комплексную оценку качества исследования используя {assessment_framework} критерии:

**ДАННЫЕ ИССЛЕДОВАНИЯ:**
{json.dumps(study_data, ensure_ascii=False, indent=2)}

**КРИТЕРИИ ОЦЕНКИ:**
{json.dumps(framework_criteria, ensure_ascii=False, indent=2)}

**ДОМЕН:** {ctx.deps.research_domain}
**УРОВЕНЬ ВАЛИДАЦИИ:** {ctx.deps.validation_level}

Оцени по следующим компонентам:

1. **ДИЗАЙН ИССЛЕДОВАНИЯ** (0-10 баллов)
   - Соответствие дизайна исследовательским целям
   - Контроль систематических ошибок
   - Внутренняя валидность

2. **УЧАСТНИКИ** (0-10 баллов)
   - Адекватность размера выборки
   - Репрезентативность
   - Характеристики выборки

3. **ИЗМЕРЕНИЯ** (0-10 баллов)
   - Валидность инструментов
   - Надежность измерений
   - Соответствие популяции

4. **СТАТИСТИЧЕСКИЙ АНАЛИЗ** (0-10 баллов)
   - Корректность методов
   - Контроль ошибок
   - Интерпретация результатов

5. **ЭТИЧЕСКИЕ АСПЕКТЫ** (0-10 баллов)
   - Одобрение этических комитетов
   - Информированное согласие
   - Минимизация рисков

6. **ОТЧЕТНОСТЬ** (0-10 баллов)
   - Соответствие стандартам
   - Полнота информации
   - Воспроизводимость

Дай общий рейтинг качества, выдели сильные стороны и области для улучшения.
"""

        from pydantic_ai import Agent

        quality_agent = Agent(model)
        result = await quality_agent.run(quality_prompt)

        return f"""# Оценка качества исследования

## Методология оценки
**Фреймворк:** {assessment_framework}
**Домен:** {ctx.deps.research_domain}
**Критерии:** {len(framework_criteria)} компонентов

## Результаты оценки
{result.data}

## Рекомендации по улучшению
{_generate_quality_improvement_recommendations(study_data, ctx.deps)}

## Соответствие стандартам
{_check_standards_compliance(study_data, ctx.deps)}

*Оценка выполнена с использованием {model.__class__.__name__}*
"""

    except Exception as e:
        return f"❌ Ошибка оценки качества исследования: {e}"


async def perform_meta_analysis_planning(
    ctx: RunContext[ResearchAgentDependencies],
    research_question: str,
    inclusion_criteria: List[str],
    databases: List[str] = None
) -> str:
    """
    Планирование мета-анализа или систематического обзора.

    Args:
        research_question: Исследовательский вопрос
        inclusion_criteria: Критерии включения исследований
        databases: Базы данных для поиска

    Returns:
        План мета-анализа
    """
    try:
        # Получаем модель для методологического анализа
        model = ctx.deps.get_model_for_task("methodology_analysis", "critical")

        databases = databases or ctx.deps.literature_search_databases

        planning_prompt = f"""
Разработай детальный план мета-анализа/систематического обзора:

**ИССЛЕДОВАТЕЛЬСКИЙ ВОПРОС:** {research_question}
**КРИТЕРИИ ВКЛЮЧЕНИЯ:** {', '.join(inclusion_criteria)}
**БАЗЫ ДАННЫХ:** {', '.join(databases)}
**ДОМЕН:** {ctx.deps.research_domain}

Создай план по следующей структуре:

1. **ПРОТОКОЛ ИССЛЕДОВАНИЯ**
   - Формализация исследовательского вопроса (PICOS)
   - Первичные и вторичные исходы
   - Критерии включения и исключения
   - Стратегия поиска

2. **МЕТОДОЛОГИЯ ПОИСКА**
   - Ключевые термины и синонимы
   - Стратегия для каждой базы данных
   - Дополнительные источники
   - Временные рамки

3. **ОТБОР ИССЛЕДОВАНИЙ**
   - Процедура скрининга
   - Критерии принятия решений
   - Разрешение разногласий
   - Документирование процесса

4. **ИЗВЛЕЧЕНИЕ ДАННЫХ**
   - Формы извлечения данных
   - Необходимые переменные
   - Контакт с авторами
   - Проверка точности

5. **ОЦЕНКА КАЧЕСТВА**
   - Инструменты оценки риска систематических ошибок
   - Критерии качества доказательств
   - Независимые оценщики
   - Консенсус-процедуры

6. **СТАТИСТИЧЕСКИЙ АНАЛИЗ**
   - Меры эффекта
   - Модели анализа (фиксированные/случайные эффекты)
   - Анализ гетерогенности
   - Анализ подгрупп

7. **ИНТЕРПРЕТАЦИЯ РЕЗУЛЬТАТОВ**
   - Клиническая значимость
   - Доверие к доказательствам (GRADE)
   - Ограничения
   - Практические рекомендации

Включи временные рамки и ресурсы для каждого этапа.
"""

        from pydantic_ai import Agent

        planning_agent = Agent(model)
        result = await planning_agent.run(planning_prompt)

        return f"""# План мета-анализа / систематического обзора

## Исследовательский вопрос
{research_question}

## Детальный план выполнения
{result.data}

## Контрольные точки качества
{_generate_meta_analysis_checkpoints(ctx.deps)}

## Ресурсы и инструменты
{_list_meta_analysis_resources()}

*План разработан с использованием {model.__class__.__name__}*
"""

    except Exception as e:
        return f"❌ Ошибка планирования мета-анализа: {e}"


# ===== КОЛЛЕКТИВНЫЕ ИНСТРУМЕНТЫ =====

async def break_down_to_microtasks(
    ctx: RunContext[ResearchAgentDependencies],
    main_task: str,
    complexity_level: str = "medium"
) -> str:
    """
    Разбить исследовательскую задачу на микрозадачи.

    Args:
        main_task: Основная задача
        complexity_level: Уровень сложности

    Returns:
        Список микрозадач для выполнения
    """
    if complexity_level == "simple":
        microtasks = [
            f"Поиск в базе знаний по теме: {main_task}",
            f"Анализ методологических требований",
            f"Выполнение основной валидации",
            f"Подготовка отчета с рекомендациями"
        ]
    elif complexity_level == "medium":
        microtasks = [
            f"Анализ сложности задачи: {main_task}",
            f"Поиск релевантной литературы и стандартов",
            f"Определение критериев валидации для домена {ctx.deps.research_domain}",
            f"Выполнение экспертного анализа",
            f"Статистическая валидация (если применимо)",
            f"Проверка этического соответствия",
            f"Критический анализ результатов",
            f"Подготовка итогового отчета с улучшениями"
        ]
    else:  # complex
        microtasks = [
            f"Глубокий анализ исследовательской задачи: {main_task}",
            f"Систематический поиск литературы и мета-анализов",
            f"Анализ применимых методологических стандартов",
            f"Консультация с экспертами других доменов",
            f"Детальная валидация статистических методов",
            f"Комплексная этическая экспертиза",
            f"Оценка воспроизводимости и репликации",
            f"Анализ практической значимости",
            f"Расширенная рефлексия и peer review",
            f"Финализация с рекомендациями для улучшения"
        ]

    output = "📋 **Микрозадачи для Psychology Research Agent:**\n"
    for i, task in enumerate(microtasks, 1):
        output += f"{i}. {task}\n"
    output += f"\n🎯 **Домен:** {ctx.deps.research_domain}\n"
    output += f"📊 **Уровень валидации:** {ctx.deps.validation_level}\n"
    output += "\n✅ Буду отчитываться о прогрессе каждой микрозадачи"

    return output


async def delegate_task_to_agent(
    ctx: RunContext[ResearchAgentDependencies],
    target_agent: str,
    task_title: str,
    task_description: str,
    priority: str = "medium",
    context_data: Dict[str, Any] = None
) -> str:
    """
    Делегировать задачу другому специализированному агенту.

    Args:
        target_agent: Целевой агент
        task_title: Название задачи
        task_description: Описание задачи
        priority: Приоритет задачи
        context_data: Контекстные данные

    Returns:
        Результат делегирования
    """
    try:
        # Карта агентов
        agent_map = {
            "quality_guardian": "Psychology Quality Guardian Agent",
            "security_audit": "Security Audit Agent",
            "uiux_enhancement": "Archon UI/UX Designer",
            "performance_optimization": "Performance Optimization Agent"
        }

        assignee = agent_map.get(target_agent, "Archon Analysis Lead")

        # Создаем задачу в Archon
        from mcp__archon__manage_task import manage_task

        result = await manage_task(
            action="create",
            project_id=ctx.deps.archon_project_id,
            title=task_title,
            description=f"{task_description}\n\n**Контекст от Psychology Research Agent:**\n{json.dumps(context_data, ensure_ascii=False, indent=2) if context_data else 'Нет дополнительного контекста'}",
            assignee=assignee,
            status="todo",
            feature=f"Делегирование от research_agent",
            task_order=50
        )

        return f"""✅ **Задача успешно делегирована агенту {target_agent}**

📋 **Детали делегирования:**
- **Задача ID:** {result.get('task', {}).get('id', 'не указан')}
- **Назначен:** {assignee}
- **Приоритет:** {priority}
- **Статус:** создана в Archon

🔄 **Следующие шаги:**
- Агент {target_agent} получит задачу в Archon
- Результат будет доступен через систему Archon
- Интеграция результатов в основной анализ
"""

    except Exception as e:
        return f"❌ Ошибка делегирования: {e}"


async def check_delegation_need(
    ctx: RunContext[ResearchAgentDependencies],
    current_task: str,
    current_agent_type: str = "research_agent"
) -> str:
    """
    Проверить необходимость делегирования задачи.

    Args:
        current_task: Описание текущей задачи
        current_agent_type: Тип текущего агента

    Returns:
        Рекомендации по делегированию
    """
    keywords = current_task.lower().split()
    suggestions = []

    # Определяем ключевые слова для других агентов
    quality_keywords = ['качество', 'quality', 'валидация', 'compliance', 'стандарты']
    security_keywords = ['безопасность', 'security', 'privacy', 'data protection', 'gdpr']
    ui_keywords = ['интерфейс', 'ui', 'ux', 'дизайн', 'пользователь']
    performance_keywords = ['производительность', 'performance', 'optimization']

    if any(kw in keywords for kw in quality_keywords) and 'research' not in keywords:
        suggestions.append("Psychology Quality Guardian Agent - для дополнительной валидации качества")

    if any(kw in keywords for kw in security_keywords):
        suggestions.append("Security Audit Agent - для проверки безопасности данных")

    if any(kw in keywords for kw in ui_keywords):
        suggestions.append("UI/UX Enhancement Agent - для работы с интерфейсами")

    if any(kw in keywords for kw in performance_keywords):
        suggestions.append("Performance Optimization Agent - для оптимизации производительности")

    if suggestions:
        result = "🤝 **Рекомендуется делегирование:**\n"
        for suggestion in suggestions:
            result += f"- {suggestion}\n"
        result += "\n💡 Используйте delegate_task_to_agent() для создания соответствующих задач."
    else:
        result = "✅ Задача может быть выполнена самостоятельно в рамках исследовательской экспертизы."

    return result


# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====

def _perform_basic_statistical_checks(request: StatisticalValidationRequest) -> Dict[str, Any]:
    """Выполнить базовые статистические проверки."""
    checks = {
        "sample_size_adequate": request.sample_size >= 30,
        "effect_sizes_provided": len(request.effect_sizes) > 0,
        "power_analysis_provided": request.power_analysis is not None,
        "multiple_methods": len(request.statistical_methods) > 1,
        "effect_size_magnitude": "not_assessed"
    }

    if request.effect_sizes:
        avg_effect = statistics.mean(request.effect_sizes)
        if avg_effect >= 0.8:
            checks["effect_size_magnitude"] = "large"
        elif avg_effect >= 0.5:
            checks["effect_size_magnitude"] = "medium"
        elif avg_effect >= 0.2:
            checks["effect_size_magnitude"] = "small"
        else:
            checks["effect_size_magnitude"] = "trivial"

    return checks


def _format_basic_checks(checks: Dict[str, Any]) -> str:
    """Форматировать результаты базовых проверок."""
    status_map = {True: "✅", False: "❌"}

    formatted = []
    for key, value in checks.items():
        if isinstance(value, bool):
            formatted.append(f"{status_map[value]} {key.replace('_', ' ').title()}")
        else:
            formatted.append(f"📊 {key.replace('_', ' ').title()}: {value}")

    return "\n".join(formatted)


def _generate_statistical_recommendations(
    checks: Dict[str, Any],
    deps: ResearchAgentDependencies
) -> str:
    """Сгенерировать рекомендации по статистическому анализу."""
    recommendations = []

    if not checks.get("sample_size_adequate"):
        recommendations.append("🔢 Рассмотрите увеличение размера выборки для достижения адекватной статистической мощности")

    if not checks.get("effect_sizes_provided"):
        recommendations.append("📊 Добавьте расчет и отчетность размеров эффектов с доверительными интервалами")

    if not checks.get("power_analysis_provided"):
        recommendations.append("⚡ Проведите анализ статистической мощности a priori или post hoc")

    if checks.get("effect_size_magnitude") == "trivial":
        recommendations.append("⚠️ Размеры эффектов малы - рассмотрите практическую значимость результатов")

    return "\n".join(recommendations) if recommendations else "✅ Статистический анализ соответствует базовым требованиям"


def _format_search_strategy(strategy: Dict[str, Any]) -> str:
    """Форматировать стратегию поиска литературы."""
    formatted = []
    for key, value in strategy.items():
        if isinstance(value, list):
            formatted.append(f"**{key.replace('_', ' ').title()}:** {', '.join(value)}")
        elif isinstance(value, dict):
            formatted.append(f"**{key.replace('_', ' ').title()}:** {json.dumps(value, ensure_ascii=False)}")
        else:
            formatted.append(f"**{key.replace('_', ' ').title()}:** {value}")

    return "\n".join(formatted)


def _generate_literature_recommendations(
    request: LiteratureSearchRequest,
    deps: ResearchAgentDependencies
) -> str:
    """Сгенерировать рекомендации по литературному поиску."""
    recommendations = [
        f"🔍 Расширьте поиск включением {', '.join(deps.literature_search_databases)}",
        f"📅 Рассмотрите расширение временного диапазона для полноты обзора",
        f"🌐 Включите международные источники для культурной валидности",
        f"📊 Фокусируйтесь на {deps.methodology_focus} исследованиях для {deps.research_domain} домена"
    ]

    return "\n".join(recommendations)


def _get_quality_assessment_framework(framework: str, domain: str) -> Dict[str, Any]:
    """Получить критерии фреймворка оценки качества."""
    frameworks = {
        "custom": {
            "design_quality": ["randomization", "blinding", "control_group"],
            "sample_quality": ["size", "representativeness", "attrition"],
            "measurement_quality": ["validity", "reliability", "standardization"],
            "analysis_quality": ["appropriate_methods", "effect_sizes", "confidence_intervals"],
            "reporting_quality": ["transparency", "completeness", "reproducibility"]
        },
        "cochrane": {
            "selection_bias": ["randomization", "allocation_concealment"],
            "performance_bias": ["blinding_participants", "blinding_personnel"],
            "detection_bias": ["blinding_outcomes"],
            "attrition_bias": ["incomplete_data"],
            "reporting_bias": ["selective_reporting"],
            "other_bias": ["other_sources"]
        }
    }

    return frameworks.get(framework, frameworks["custom"])


def _generate_quality_improvement_recommendations(
    study_data: Dict[str, Any],
    deps: ResearchAgentDependencies
) -> str:
    """Сгенерировать рекомендации по улучшению качества."""
    recommendations = [
        f"📋 Следуйте стандартам отчетности: {', '.join(deps.reporting_standards)}",
        f"🔢 Обеспечьте минимальный размер выборки: {deps.min_sample_size}",
        f"📊 Включите анализ размеров эффектов (минимум {deps.min_effect_size})",
        f"⚡ Проведите анализ статистической мощности (минимум {deps.min_power})",
        f"🔒 Обеспечьте соблюдение этических стандартов: {', '.join(deps.ethics_standards)}"
    ]

    return "\n".join(recommendations)


def _check_standards_compliance(
    study_data: Dict[str, Any],
    deps: ResearchAgentDependencies
) -> str:
    """Проверить соответствие стандартам."""
    compliance_check = []

    for standard in deps.reporting_standards:
        compliance_check.append(f"📋 {standard}: требует проверки соответствия чек-листу")

    for standard in deps.ethics_standards:
        compliance_check.append(f"🔒 {standard}: требует этической экспертизы")

    return "\n".join(compliance_check)


def _generate_meta_analysis_checkpoints(deps: ResearchAgentDependencies) -> str:
    """Сгенерировать контрольные точки для мета-анализа."""
    checkpoints = [
        "📋 Регистрация протокола в PROSPERO или аналогичном реестре",
        "🔍 Независимый скрининг минимум двумя исследователями",
        "📊 Оценка качества с использованием валидированных инструментов",
        "📈 Анализ гетерогенности и источников вариации",
        "🎯 Анализ чувствительности и подгрупп",
        "📝 Соблюдение стандартов отчетности PRISMA"
    ]

    return "\n".join(checkpoints)


def _list_meta_analysis_resources() -> str:
    """Список ресурсов для мета-анализа."""
    resources = [
        "🛠️ **Программное обеспечение:** RevMan, R (metafor), Comprehensive Meta-Analysis",
        "📚 **Базы данных:** Cochrane Library, PubMed, PsycINFO, Embase",
        "📋 **Инструменты оценки:** RoB 2.0, ROBINS-I, AMSTAR 2",
        "📊 **Стандарты отчетности:** PRISMA, PRISMA-P, PRISMA-ScR",
        "🔍 **Реестры протоколов:** PROSPERO, OSF Registries"
    ]

    return "\n".join(resources)


# Экспорт основных инструментов
__all__ = [
    "search_research_knowledge",
    "analyze_study_methodology",
    "validate_statistical_analysis",
    "search_literature",
    "evaluate_study_quality",
    "perform_meta_analysis_planning",
    "break_down_to_microtasks",
    "delegate_task_to_agent",
    "check_delegation_need"
]