# -*- coding: utf-8 -*-
"""
Обязательные инструменты коллективной работы для всех Pydantic AI агентов

Этот модуль содержит стандартные инструменты, которые должны быть
добавлены ко всем агентам для поддержки коллективного решения задач.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from pydantic_ai import RunContext

logger = logging.getLogger(__name__)

# Матрица компетенций агентов для делегирования
AGENT_COMPETENCIES = {
    "security_audit": [
        "безопасность", "уязвимости", "compliance", "аудит безопасности",
        "secrets detection", "penetration testing", "OWASP", "CVE"
    ],
    "rag_agent": [
        "поиск информации", "семантический анализ", "knowledge base",
        "document retrieval", "информационный поиск", "текстовый анализ"
    ],
    "uiux_enhancement": [
        "дизайн", "пользовательский интерфейс", "accessibility", "UX/UI",
        "компонентные библиотеки", "дизайн системы", "пользовательский опыт"
    ],
    "performance_optimization": [
        "производительность", "оптимизация", "скорость", "memory usage",
        "cpu optimization", "caching", "load testing", "профилирование"
    ],
    "typescript_architecture": [
        "типизация", "архитектура", "TypeScript", "type safety",
        "код структура", "рефакторинг", "architectural patterns"
    ],
    "prisma_database": [
        "база данных", "SQL", "Prisma", "схемы данных",
        "migrations", "query optimization", "database design"
    ],
    "pwa_mobile": [
        "PWA", "мобильная разработка", "service workers", "offline",
        "mobile UX", "app manifest", "мобильная адаптация"
    ],
    "analytics_tracking": [
        "аналитика", "трекинг", "метрики", "конверсия",
        "Google Analytics", "события", "отслеживание пользователей"
    ],
    "mcp_configuration": [
        "MCP", "конфигурация", "Claude Desktop", "серверы",
        "интеграция", "настройка", "MCP protocol"
    ]
}

AGENT_ASSIGNEE_MAP = {
    "security_audit": "Security Audit Agent",
    "rag_agent": "Archon Analysis Lead",
    "uiux_enhancement": "Archon UI/UX Designer",
    "performance_optimization": "Performance Optimization Agent",
    "typescript_architecture": "Archon Blueprint Architect",
    "prisma_database": "Archon Implementation Engineer",
    "pwa_mobile": "Archon Implementation Engineer",
    "analytics_tracking": "Analytics Tracking Agent",
    "mcp_configuration": "Mcp Configuration Agent"
}

async def break_down_to_microtasks(
    ctx: RunContext,
    main_task: str,
    complexity_level: str = "medium"
) -> str:
    """
    Разбить основную задачу на микрозадачи и вывести их пользователю.

    ОБЯЗАТЕЛЬНО вызывается в начале работы каждого агента.

    Args:
        ctx: Контекст выполнения
        main_task: Основная задача для разбивки
        complexity_level: Уровень сложности (simple, medium, complex)

    Returns:
        Форматированный список микрозадач для пользователя
    """
    try:
        microtasks = []

        if complexity_level == "simple":
            microtasks = [
                f"Анализ требований для: {main_task}",
                f"Реализация решения",
                f"Проверка и рефлексия"
            ]
        elif complexity_level == "medium":
            microtasks = [
                f"Анализ сложности задачи: {main_task}",
                f"Поиск в базе знаний по теме",
                f"Определение необходимости делегирования",
                f"Реализация основной части",
                f"Критический анализ результата",
                f"Улучшение и финализация"
            ]
        else:  # complex
            microtasks = [
                f"Глубокий анализ задачи: {main_task}",
                f"Поиск в RAG и веб-источниках",
                f"Планирование межагентного взаимодействия",
                f"Делегирование специализированных частей",
                f"Реализация собственной части",
                f"Интеграция результатов от других агентов",
                f"Расширенная рефлексия и улучшение"
            ]

        # Форматируем вывод для пользователя
        output = "📋 **Микрозадачи для выполнения:**\n"
        for i, task in enumerate(microtasks, 1):
            output += f"{i}. {task}\n"
        output += "\n✅ Буду отчитываться о прогрессе каждой микрозадачи"

        logger.info(f"Создан план из {len(microtasks)} микрозадач для: {main_task}")
        return output

    except Exception as e:
        logger.error(f"Ошибка создания микрозадач: {e}")
        return f"Ошибка создания плана микрозадач: {e}"

async def report_microtask_progress(
    ctx: RunContext,
    microtask_number: int,
    microtask_description: str,
    status: str = "completed",
    details: str = ""
) -> str:
    """
    Отчитаться о прогрессе выполнения микрозадачи.

    Вызывается для каждой микрозадачи по мере выполнения.

    Args:
        ctx: Контекст выполнения
        microtask_number: Номер микрозадачи
        microtask_description: Описание микрозадачи
        status: Статус (started, in_progress, completed, blocked)
        details: Дополнительные детали

    Returns:
        Форматированный отчет о прогрессе
    """
    try:
        status_emoji = {
            "started": "🔄",
            "in_progress": "⏳",
            "completed": "✅",
            "blocked": "🚫"
        }

        report = f"{status_emoji.get(status, '📝')} **Микрозадача {microtask_number}** ({status}): {microtask_description}"
        if details:
            report += f"\n   Детали: {details}"

        logger.info(f"Отчет о микрозадаче {microtask_number}: {status}")
        return report

    except Exception as e:
        logger.error(f"Ошибка отчета о микрозадаче: {e}")
        return f"Ошибка отчета: {e}"

async def reflect_and_improve(
    ctx: RunContext,
    completed_work: str,
    work_type: str = "implementation",
    quality_criteria: List[str] = None
) -> str:
    """
    Выполнить расширенный критический анализ работы и улучшить результат.

    ОБЯЗАТЕЛЬНО вызывается перед завершением задачи.
    Использует продвинутую систему рефлексии с автоматическим поиском недостатков.

    Args:
        ctx: Контекст выполнения
        completed_work: Описание выполненной работы
        work_type: Тип работы (analysis, implementation, testing, documentation)
        quality_criteria: Опциональный список критериев качества

    Returns:
        Детальный анализ с улучшениями
    """
    try:
        # Используем продвинутую систему рефлексии
        from .reflection_system import advanced_reflection, format_reflection_report

        logger.info(f"Запуск расширенной рефлексии для работы типа: {work_type}")

        # Выполняем расширенный анализ
        reflection_result = await advanced_reflection(
            ctx=ctx,
            completed_work=completed_work,
            work_type=work_type,
            quality_criteria=quality_criteria
        )

        # Форматируем результат для пользователя
        formatted_report = format_reflection_report(reflection_result)

        logger.info(f"Рефлексия завершена. Балл качества: {reflection_result.final_score}/10.0")

        return formatted_report

    except Exception as e:
        logger.error(f"Ошибка расширенной рефлексии: {e}")
        # Fallback на базовый анализ
        return f"""
🔍 **Критический анализ выполненной работы:**

**Тип работы:** {work_type}
**Результат:** {completed_work[:200]}...

⚠️ **Ошибка расширенной рефлексии:** {e}

**Базовый анализ:**
- Проверка универсальности
- Проверка модульности
- Проверка документации

🎯 **Рекомендуется повторить анализ с исправлением ошибки**
"""

async def check_delegation_need(
    ctx: RunContext,
    current_task: str,
    current_agent_type: str
) -> str:
    """
    Проверить нужно ли делегировать части задачи другим агентам.

    Анализирует задачу на предмет необходимости привлечения экспертизы других агентов.

    Args:
        ctx: Контекст выполнения
        current_task: Текущая задача
        current_agent_type: Тип текущего агента

    Returns:
        Рекомендации по делегированию
    """
    try:
        keywords = current_task.lower().split()

        # Проверяем ключевые слова на пересечение с компетенциями других агентов
        delegation_suggestions = []

        for agent_type, competencies in AGENT_COMPETENCIES.items():
            if agent_type != current_agent_type:
                # Проверяем пересечение ключевых слов с компетенциями
                matching_keywords = []
                for keyword in keywords:
                    for competency in competencies:
                        if keyword in competency.lower() or competency.lower() in keyword:
                            matching_keywords.append(competency)

                if matching_keywords:
                    assignee = AGENT_ASSIGNEE_MAP.get(agent_type, "Archon Analysis Lead")
                    delegation_suggestions.append(
                        f"{assignee} - для работы с: {', '.join(set(matching_keywords))}"
                    )

        if delegation_suggestions:
            result = "🤝 **Рекомендуется делегирование:**\n"
            for suggestion in delegation_suggestions:
                result += f"- {suggestion}\n"
            result += "\nИспользуйте delegate_task_to_agent() для создания соответствующих задач."
        else:
            result = "✅ Задача может быть выполнена самостоятельно без делегирования."

        logger.info(f"Проверка делегирования: найдено {len(delegation_suggestions)} предложений")
        return result

    except Exception as e:
        logger.error(f"Ошибка проверки делегирования: {e}")
        return f"Ошибка анализа делегирования: {e}"

async def delegate_task_to_agent(
    ctx: RunContext,
    target_agent: str,
    task_title: str,
    task_description: str,
    priority: str = "medium",
    context_data: Dict[str, Any] = None
) -> str:
    """
    Делегировать задачу другому специализированному агенту через Archon.

    Используется когда текущая задача требует экспертизы другого агента.

    Args:
        ctx: Контекст выполнения
        target_agent: Целевой агент (security_audit, rag_agent, etc.)
        task_title: Название задачи
        task_description: Описание задачи
        priority: Приоритет (low, medium, high, critical)
        context_data: Дополнительные данные контекста

    Returns:
        Результат делегирования
    """
    try:
        # Импортируем здесь чтобы избежать циклических импортов
        try:
            from ...common.archon_integrations import create_archon_task
        except ImportError:
            # Fallback для случаев когда archon_integrations недоступен
            logger.warning("Модуль archon_integrations недоступен, используем заглушку")
            return f"⚠️ Делегирование задачи '{task_title}' агенту {target_agent} запланировано, но Archon недоступен"

        # Определяем assignee по целевому агенту
        assignee = AGENT_ASSIGNEE_MAP.get(target_agent, "Archon Analysis Lead")

        # Формируем полное описание с контекстом
        full_description = task_description
        if context_data:
            full_description += f"\n\n**Контекст от агента:**\n{context_data}"

        # Создаем задачу в Archon
        task_result = await create_archon_task(
            title=task_title,
            description=full_description,
            assignee=assignee,
            priority=priority,
            feature=f"Делегирование от {target_agent}"
        )

        result = f"✅ Задача успешно делегирована агенту {target_agent}:\n"
        result += f"- Assignee: {assignee}\n"
        result += f"- Приоритет: {priority}\n"
        result += f"- Статус: создана в Archon"

        if "task_id" in task_result:
            result += f"\n- Задача ID: {task_result['task_id']}"

        logger.info(f"Делегирована задача '{task_title}' агенту {target_agent}")
        return result

    except Exception as e:
        logger.error(f"Ошибка делегирования: {e}")
        return f"❌ Ошибка делегирования: {e}"

# Дополнительные утилиты для коллективной работы

def get_agent_competencies(agent_type: str) -> List[str]:
    """Получить список компетенций для указанного типа агента."""
    return AGENT_COMPETENCIES.get(agent_type, [])

def find_best_agent_for_task(task_keywords: List[str], exclude_agent: str = None) -> Optional[str]:
    """
    Найти лучшего агента для задачи на основе ключевых слов.

    Args:
        task_keywords: Ключевые слова задачи
        exclude_agent: Агент для исключения из поиска

    Returns:
        Тип лучшего агента или None
    """
    best_match = None
    best_score = 0

    for agent_type, competencies in AGENT_COMPETENCIES.items():
        if exclude_agent and agent_type == exclude_agent:
            continue

        # Подсчитываем совпадения
        score = 0
        for keyword in task_keywords:
            for competency in competencies:
                if keyword.lower() in competency.lower():
                    score += 1

        if score > best_score:
            best_score = score
            best_match = agent_type

    return best_match

def should_delegate_task(task_description: str, current_agent_type: str, threshold: int = 2) -> bool:
    """
    Определить следует ли делегировать задачу другому агенту.

    Args:
        task_description: Описание задачи
        current_agent_type: Тип текущего агента
        threshold: Минимальное количество совпадений для делегирования

    Returns:
        True если следует делегировать
    """
    keywords = task_description.lower().split()
    current_competencies = get_agent_competencies(current_agent_type)

    # Проверяем есть ли совпадения с компетенциями текущего агента
    current_matches = 0
    for keyword in keywords:
        for competency in current_competencies:
            if keyword in competency.lower():
                current_matches += 1

    # Если у текущего агента мало совпадений, стоит рассмотреть делегирование
    return current_matches < threshold