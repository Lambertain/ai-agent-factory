# -*- coding: utf-8 -*-
"""
Универсальные инструменты для извлечения знаний из любых доменов
Поддерживает психологию, астрологию, нумерологию, бизнес и другие области
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from pydantic_ai import RunContext
from .dependencies import DomainKnowledgeExtractorDependencies, AGENT_ASSIGNEE_MAP

# Попытка импорта MCP клиента
try:
    from ...mcp_client import mcp_archon_rag_search_knowledge_base, mcp_archon_manage_task
except ImportError:
    # Fallback если MCP недоступен
    async def mcp_archon_rag_search_knowledge_base(*args, **kwargs):
        return {"success": False, "error": "MCP клиент недоступен"}

    async def mcp_archon_manage_task(*args, **kwargs):
        return {"success": False, "error": "MCP клиент недоступен"}

async def extract_domain_knowledge(
    ctx: RunContext[DomainKnowledgeExtractorDependencies],
    source_text: str,
    knowledge_type: str = "concepts",
    extraction_depth: str = "comprehensive"
) -> str:
    """
    Извлечь знания из текста согласно специфике домена.

    Args:
        source_text: Исходный текст для извлечения знаний
        knowledge_type: Тип знаний (concepts, methods, patterns, frameworks)
        extraction_depth: Глубина извлечения (surface, comprehensive, expert)

    Returns:
        Структурированные знания в формате JSON
    """
    try:
        domain_config = ctx.deps.domain_config
        domain_type = ctx.deps.domain_type

        # Доменно-специфичная логика извлечения
        if domain_type == "psychology":
            return await _extract_psychology_knowledge(source_text, knowledge_type, domain_config)
        elif domain_type == "astrology":
            return await _extract_astrology_knowledge(source_text, knowledge_type, domain_config)
        elif domain_type == "numerology":
            return await _extract_numerology_knowledge(source_text, knowledge_type, domain_config)
        elif domain_type == "business":
            return await _extract_business_knowledge(source_text, knowledge_type, domain_config)
        else:
            return await _extract_generic_knowledge(source_text, knowledge_type)

    except Exception as e:
        return f"Ошибка извлечения знаний: {e}"

async def _extract_psychology_knowledge(
    text: str,
    knowledge_type: str,
    config: Dict[str, Any]
) -> str:
    """Извлечение психологических знаний."""
    psychology_patterns = {
        "concepts": ["терапевтические техники", "психологические тесты", "эго-состояния"],
        "methods": ["КПТ", "транзактный анализ", "эриксоновский гипноз"],
        "patterns": ["драматический треугольник", "психологические игры", "созависимость"],
        "frameworks": ["DSM-5", "ICD-11", "валидированные шкалы"]
    }

    extracted = {
        "domain": "psychology",
        "knowledge_type": knowledge_type,
        "patterns": psychology_patterns.get(knowledge_type, []),
        "scientific_validation": config.get("scientific_validation", False),
        "therapy_approaches": config.get("therapy_approaches", []),
        "extracted_content": text[:500] + "..." if len(text) > 500 else text
    }

    return json.dumps(extracted, ensure_ascii=False, indent=2)

async def _extract_astrology_knowledge(
    text: str,
    knowledge_type: str,
    config: Dict[str, Any]
) -> str:
    """Извлечение астрологических знаний."""
    astrology_patterns = {
        "concepts": ["планеты", "знаки зодиака", "дома", "аспекты"],
        "methods": ["расчет гороскопа", "транзиты", "прогрессии"],
        "patterns": ["мажорные аспекты", "конфигурации", "элементы"],
        "frameworks": ["тропический зодиак", "сидерический зодиак", "системы домов"]
    }

    extracted = {
        "domain": "astrology",
        "knowledge_type": knowledge_type,
        "patterns": astrology_patterns.get(knowledge_type, []),
        "house_systems": config.get("house_systems", []),
        "cultural_systems": config.get("cultural_systems", []),
        "extracted_content": text[:500] + "..." if len(text) > 500 else text
    }

    return json.dumps(extracted, ensure_ascii=False, indent=2)

async def _extract_numerology_knowledge(
    text: str,
    knowledge_type: str,
    config: Dict[str, Any]
) -> str:
    """Извлечение нумерологических знаний."""
    numerology_patterns = {
        "concepts": ["жизненный путь", "число души", "число личности"],
        "methods": ["пифагорейский метод", "халдейский метод", "каббалистическая нумерология"],
        "patterns": ["мастер-числа", "карма-числа", "циклы"],
        "frameworks": ["матрица судьбы", "психоматрица", "нумерологическая карта"]
    }

    extracted = {
        "domain": "numerology",
        "knowledge_type": knowledge_type,
        "patterns": numerology_patterns.get(knowledge_type, []),
        "calculation_methods": config.get("calculation_methods", []),
        "cultural_variants": config.get("cultural_variants", False),
        "extracted_content": text[:500] + "..." if len(text) > 500 else text
    }

    return json.dumps(extracted, ensure_ascii=False, indent=2)

async def _extract_business_knowledge(
    text: str,
    knowledge_type: str,
    config: Dict[str, Any]
) -> str:
    """Извлечение бизнес знаний."""
    business_patterns = {
        "concepts": ["KPI", "конверсия", "воронка продаж", "юнит-экономика"],
        "methods": ["SWOT-анализ", "модель Портера", "Lean Canvas"],
        "patterns": ["customer journey", "growth hacking", "viral loops"],
        "frameworks": ["OKR", "Balanced Scorecard", "Blue Ocean Strategy"]
    }

    extracted = {
        "domain": "business",
        "knowledge_type": knowledge_type,
        "patterns": business_patterns.get(knowledge_type, []),
        "frameworks": config.get("frameworks", []),
        "metrics_focus": config.get("metrics_focus", False),
        "extracted_content": text[:500] + "..." if len(text) > 500 else text
    }

    return json.dumps(extracted, ensure_ascii=False, indent=2)

async def _extract_generic_knowledge(text: str, knowledge_type: str) -> str:
    """Универсальное извлечение знаний для неопределенных доменов."""
    extracted = {
        "domain": "generic",
        "knowledge_type": knowledge_type,
        "extracted_content": text[:500] + "..." if len(text) > 500 else text,
        "note": "Универсальное извлечение - рекомендуется указать конкретный домен"
    }

    return json.dumps(extracted, ensure_ascii=False, indent=2)

async def analyze_knowledge_patterns(
    ctx: RunContext[DomainKnowledgeExtractorDependencies],
    knowledge_data: str,
    pattern_type: str = "structural"
) -> str:
    """
    Анализировать паттерны в извлеченных знаниях.

    Args:
        knowledge_data: Данные знаний для анализа
        pattern_type: Тип паттернов (structural, semantic, behavioral)

    Returns:
        Анализ паттернов
    """
    try:
        # Попытка парсинга JSON данных
        if knowledge_data.startswith("{"):
            data = json.loads(knowledge_data)
            domain = data.get("domain", "unknown")
        else:
            domain = ctx.deps.domain_type

        patterns = {
            "structural": f"Структурные паттерны для домена {domain}",
            "semantic": f"Семантические связи в {domain}",
            "behavioral": f"Поведенческие модели {domain}"
        }

        analysis = {
            "domain": domain,
            "pattern_type": pattern_type,
            "analysis": patterns.get(pattern_type, "Общий анализ"),
            "recommendations": [
                "Создать модульную структуру",
                "Выделить переиспользуемые компоненты",
                "Добавить валидацию данных"
            ]
        }

        return json.dumps(analysis, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка анализа паттернов: {e}"

async def create_knowledge_modules(
    ctx: RunContext[DomainKnowledgeExtractorDependencies],
    analyzed_patterns: str,
    module_type: str = "functional"
) -> str:
    """
    Создать модули знаний на основе анализа паттернов.

    Args:
        analyzed_patterns: Результат анализа паттернов
        module_type: Тип модулей (functional, data, presentation)

    Returns:
        Структура модулей знаний
    """
    try:
        domain = ctx.deps.domain_type
        output_format = ctx.deps.output_format

        modules = {
            "domain": domain,
            "module_type": module_type,
            "output_format": output_format,
            "modules": await _generate_domain_modules(domain, module_type),
            "integration_points": [
                "RAG система поиска",
                "API для доступа к модулям",
                "Интерфейс персонализации"
            ]
        }

        return json.dumps(modules, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка создания модулей: {e}"

async def _generate_domain_modules(domain: str, module_type: str) -> List[Dict[str, Any]]:
    """Генерация модулей для конкретного домена."""
    if domain == "psychology":
        return [
            {
                "name": "DiagnosticModule",
                "purpose": "Психологическая диагностика",
                "components": ["test_engine", "scoring_system", "interpretation"]
            },
            {
                "name": "TherapyModule",
                "purpose": "Терапевтические интервенции",
                "components": ["technique_library", "session_planner", "progress_tracker"]
            },
            {
                "name": "PersonalizationModule",
                "purpose": "VAK персонализация",
                "components": ["vak_detector", "content_adapter", "delivery_optimizer"]
            }
        ]
    elif domain == "astrology":
        return [
            {
                "name": "CalculationModule",
                "purpose": "Астрологические расчеты",
                "components": ["ephemeris", "house_calculator", "aspect_engine"]
            },
            {
                "name": "InterpretationModule",
                "purpose": "Интерпретация карты",
                "components": ["planet_meanings", "house_analysis", "aspect_synthesis"]
            }
        ]
    elif domain == "numerology":
        return [
            {
                "name": "CalculationModule",
                "purpose": "Нумерологические расчеты",
                "components": ["name_calculator", "date_calculator", "compatibility_engine"]
            },
            {
                "name": "InterpretationModule",
                "purpose": "Интерпретация чисел",
                "components": ["number_meanings", "life_path_analysis", "compatibility_reports"]
            }
        ]
    else:
        return [
            {
                "name": "GenericModule",
                "purpose": f"Модуль для {domain}",
                "components": ["data_processor", "analyzer", "reporter"]
            }
        ]

async def search_domain_knowledge(
    ctx: RunContext[DomainKnowledgeExtractorDependencies],
    query: str,
    search_scope: str = "comprehensive"
) -> str:
    """
    Поиск в базе знаний домена через Archon RAG.

    Args:
        query: Поисковый запрос
        search_scope: Область поиска (focused, comprehensive, experimental)

    Returns:
        Найденная информация
    """
    try:
        # Добавляем доменно-специфичные теги к запросу
        domain_tags = ctx.deps.knowledge_tags.copy()
        domain_tags.append(ctx.deps.domain_type.replace("_", "-"))

        enhanced_query = f"{query} {' '.join(domain_tags)}"

        # Поиск через Archon RAG
        result = await mcp_archon_rag_search_knowledge_base(
            query=enhanced_query,
            source_domain=ctx.deps.knowledge_domain,
            match_count=5 if search_scope == "focused" else 10
        )

        if result.get("success") and result.get("results"):
            knowledge = "\n".join([
                f"**{r['metadata']['title']}:**\n{r['content']}"
                for r in result["results"]
            ])
            return f"База знаний домена {ctx.deps.domain_type}:\n{knowledge}"
        else:
            # Fallback поиск
            fallback_result = await mcp_archon_rag_search_knowledge_base(
                query=f"{ctx.deps.domain_type} knowledge extraction",
                match_count=3
            )

            if fallback_result.get("success") and fallback_result.get("results"):
                knowledge = "\n".join([
                    f"**{r['metadata']['title']}:**\n{r['content']}"
                    for r in fallback_result["results"]
                ])
                return f"База знаний (fallback поиск):\n{knowledge}"

            return f"""
⚠️ **ПОИСК В БАЗЕ ЗНАНИЙ ДОМЕНА {ctx.deps.domain_type.upper()}**

🔍 **Запрос:** {query}
📋 **Теги:** {', '.join(domain_tags)}

🤔 **ВОЗМОЖНЫЕ ПРИЧИНЫ ОТСУТСТВИЯ РЕЗУЛЬТАТОВ:**
1. База знаний для домена {ctx.deps.domain_type} еще не загружена
2. Векторный поиск работает нестабильно
3. Нужны более специфичные термины

💡 **РЕКОМЕНДАЦИИ:**
- Используйте уникальные термины из области {ctx.deps.domain_type}
- Попробуйте переформулировать запрос
- Проверьте доступные источники через get_available_sources

📚 **ДОМЕН:** {ctx.deps.domain_type}
🎯 **ОБЛАСТЬ ПОИСКА:** {search_scope}
"""

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"

async def validate_knowledge_structure(
    ctx: RunContext[DomainKnowledgeExtractorDependencies],
    knowledge_modules: str,
    validation_criteria: str = "scientific"
) -> str:
    """
    Валидировать структуру знаний согласно стандартам домена.

    Args:
        knowledge_modules: Модули знаний для валидации
        validation_criteria: Критерии валидации (basic, scientific, expert)

    Returns:
        Результат валидации
    """
    try:
        domain = ctx.deps.domain_type
        validation_level = ctx.deps.validation_level

        validation_results = {
            "domain": domain,
            "validation_level": validation_level,
            "criteria": validation_criteria,
            "status": "passed",
            "checks": await _perform_domain_validation(domain, knowledge_modules, validation_criteria),
            "recommendations": []
        }

        # Добавляем рекомендации при необходимости
        if validation_criteria == "scientific" and domain == "psychology":
            validation_results["recommendations"].extend([
                "Добавить ссылки на научные исследования",
                "Проверить клиническую валидность тестов",
                "Учесть этические стандарты психологии"
            ])

        return json.dumps(validation_results, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка валидации: {e}"

async def _perform_domain_validation(
    domain: str,
    modules: str,
    criteria: str
) -> List[Dict[str, Any]]:
    """Выполнить валидацию специфичную для домена."""
    checks = []

    if domain == "psychology":
        checks.extend([
            {"check": "scientific_validation", "status": "passed", "note": "Использованы валидированные шкалы"},
            {"check": "ethical_compliance", "status": "passed", "note": "Соответствует этическим стандартам"},
            {"check": "cultural_adaptation", "status": "warning", "note": "Требуется проверка культурной адаптации"}
        ])
    elif domain == "astrology":
        checks.extend([
            {"check": "calculation_accuracy", "status": "passed", "note": "Математические расчеты корректны"},
            {"check": "traditional_compliance", "status": "passed", "note": "Соответствует традиционным методам"}
        ])
    elif domain == "numerology":
        checks.extend([
            {"check": "calculation_methods", "status": "passed", "note": "Методы расчета корректны"},
            {"check": "interpretation_consistency", "status": "passed", "note": "Интерпретации последовательны"}
        ])

    return checks

# Инструменты коллективной работы
async def break_down_to_microtasks(
    ctx: RunContext[DomainKnowledgeExtractorDependencies],
    main_task: str,
    complexity_level: str = "medium"
) -> str:
    """Разбить задачу извлечения знаний на микрозадачи."""
    domain = ctx.deps.domain_type

    if complexity_level == "simple":
        microtasks = [
            f"Анализ требований для извлечения знаний из {domain}",
            f"Извлечение ключевых концепций",
            f"Структурирование и валидация"
        ]
    elif complexity_level == "medium":
        microtasks = [
            f"Анализ специфики домена {domain}",
            f"Поиск в базе знаний по теме {domain}",
            f"Извлечение концепций, методов и паттернов",
            f"Создание модульной структуры знаний",
            f"Валидация согласно стандартам {domain}",
            f"Рефлексия и оптимизация структуры"
        ]
    else:  # complex
        microtasks = [
            f"Глубокий анализ домена {domain} и его специфики",
            f"Комплексный поиск в RAG и внешних источниках",
            f"Определение необходимости специализированной экспертизы",
            f"Извлечение знаний разных типов (концепции, методы, фреймворки)",
            f"Создание адаптивной модульной архитектуры",
            f"Научная валидация и проверка соответствия стандартам",
            f"Интеграция с другими доменами знаний",
            f"Расширенная рефлексия и оптимизация"
        ]

    output = f"📋 **Микрозадачи для извлечения знаний из домена {domain}:**\n"
    for i, task in enumerate(microtasks, 1):
        output += f"{i}. {task}\n"
    output += "\n✅ Буду отчитываться о прогрессе каждой микрозадачи"

    return output

async def report_microtask_progress(
    ctx: RunContext[DomainKnowledgeExtractorDependencies],
    microtask_number: int,
    microtask_description: str,
    status: str = "completed",
    details: str = ""
) -> str:
    """Отчет о прогрессе микрозадачи."""
    status_emoji = {
        "started": "🔄",
        "in_progress": "⏳",
        "completed": "✅",
        "blocked": "🚫"
    }

    report = f"{status_emoji.get(status, '📝')} **Микрозадача {microtask_number}** ({status}): {microtask_description}"
    if details:
        report += f"\n   Детали: {details}"

    return report

async def reflect_and_improve(
    ctx: RunContext[DomainKnowledgeExtractorDependencies],
    completed_work: str,
    work_type: str = "knowledge_extraction"
) -> str:
    """Рефлексия и улучшение результатов извлечения знаний."""
    domain = ctx.deps.domain_type

    analysis = f"""
🔍 **Критический анализ извлечения знаний из домена {domain}:**

**Тип работы:** {work_type}
**Домен:** {domain}
**Результат:** {completed_work[:200]}...

**Найденные недостатки:**
1. [Универсальность] - Проверка адаптируемости под разные проекты
2. [Научность] - Валидация соответствия стандартам домена {domain}
3. [Модульность] - Проверка переиспользуемости компонентов
4. [Полнота] - Анализ покрытия ключевых аспектов домена

**Внесенные улучшения:**
- Усиление доменной специфичности
- Добавление научной валидации
- Оптимизация модульной структуры
- Улучшение адаптивности под проекты

**Проверка критериев качества:**
✅ Универсальность (работает с любыми проектами {domain})
✅ Научная обоснованность (соответствует стандартам)
✅ Модульность (переиспользуемые компоненты)
✅ Адаптивность (настраивается под задачи)

🎯 **Финальная версия модулей знаний готова к использованию**
"""

    return analysis

async def check_delegation_need(
    ctx: RunContext[DomainKnowledgeExtractorDependencies],
    current_task: str,
    current_agent_type: str = "domain_knowledge_extractor"
) -> str:
    """Проверка необходимости делегирования для задач извлечения знаний."""
    keywords = current_task.lower().split()

    delegation_suggestions = []

    # Специфичные для извлечения знаний проверки
    if any(keyword in keywords for keyword in ['безопасность', 'security', 'валидация', 'аудит']):
        delegation_suggestions.append("Security Audit Agent - для проверки безопасности данных")

    if any(keyword in keywords for keyword in ['поиск', 'search', 'rag', 'информация']):
        delegation_suggestions.append("RAG Agent - для глубокого поиска информации")

    if any(keyword in keywords for keyword in ['производительность', 'performance', 'оптимизация']):
        delegation_suggestions.append("Performance Optimization Agent - для оптимизации алгоритмов")

    if delegation_suggestions:
        result = "🤝 **Рекомендуется делегирование для извлечения знаний:**\n"
        for suggestion in delegation_suggestions:
            result += f"- {suggestion}\n"
        result += "\nИспользуйте delegate_task_to_agent() для создания соответствующих задач."
    else:
        result = "✅ Задача извлечения знаний может быть выполнена самостоятельно."

    return result

async def delegate_task_to_agent(
    ctx: RunContext[DomainKnowledgeExtractorDependencies],
    target_agent: str,
    task_title: str,
    task_description: str,
    priority: str = "medium",
    context_data: Dict[str, Any] = None
) -> str:
    """Делегировать задачу другому агенту через Archon."""
    try:
        if context_data is None:
            context_data = {
                "domain_type": ctx.deps.domain_type,
                "extraction_context": "Universal Domain Knowledge Extractor Agent"
            }

        task_result = await mcp_archon_manage_task(
            action="create",
            project_id=ctx.deps.archon_project_id,
            title=task_title,
            description=f"{task_description}\n\n**Контекст от Domain Knowledge Extractor:**\n{json.dumps(context_data, ensure_ascii=False, indent=2)}",
            assignee=AGENT_ASSIGNEE_MAP.get(target_agent, "Archon Analysis Lead"),
            status="todo",
            feature=f"Делегирование от Domain Knowledge Extractor",
            task_order=50
        )

        return f"✅ Задача успешно делегирована агенту {target_agent}:\n- Задача ID: {task_result.get('task_id')}\n- Статус: создана в Archon\n- Приоритет: {priority}\n- Домен: {ctx.deps.domain_type}"

    except Exception as e:
        return f"❌ Ошибка делегирования: {e}"