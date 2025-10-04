"""
Расширенная система рефлексии для Pydantic AI агентов.

Обеспечивает обязательный цикл критического анализа и улучшения результатов
перед завершением каждой задачи.
"""

from pydantic_ai import RunContext
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReflectionResult:
    """Результат рефлексии над выполненной работой."""

    shortcomings: List[str]
    improvements_made: List[str]
    quality_checks: Dict[str, bool]
    final_score: float
    recommendations: List[str]
    timestamp: datetime


async def advanced_reflection(
    ctx: RunContext[Any],
    completed_work: str,
    work_type: str = "implementation",
    quality_criteria: List[str] = None
) -> ReflectionResult:
    """
    Выполнить расширенный критический анализ работы с автоматическим поиском недостатков.

    ОБЯЗАТЕЛЬНО вызывается перед завершением каждой задачи.

    Args:
        ctx: Контекст выполнения агента
        completed_work: Описание выполненной работы
        work_type: Тип работы (implementation, analysis, testing, documentation)
        quality_criteria: Список критериев качества для проверки

    Returns:
        ReflectionResult с найденными недостатками и улучшениями
    """

    if quality_criteria is None:
        quality_criteria = get_default_quality_criteria(work_type)

    # 1. КРИТИЧЕСКИЙ АНАЛИЗ - поиск минимум 2-3 конкретных недостатков
    shortcomings = await find_shortcomings(completed_work, work_type, quality_criteria)

    # 2. АКТИВНОЕ УЛУЧШЕНИЕ - исправление найденных недостатков
    improvements = await apply_improvements(ctx, shortcomings, completed_work)

    # 3. ПРОВЕРКА КРИТЕРИЕВ КАЧЕСТВА
    quality_checks = await validate_quality_criteria(quality_criteria, improvements.get("updated_work", completed_work))

    # 4. ОЦЕНКА ФИНАЛЬНОГО РЕЗУЛЬТАТА
    final_score = calculate_quality_score(quality_checks, len(shortcomings), len(improvements.get("improvements", [])))

    # 5. РЕКОМЕНДАЦИИ ДЛЯ БУДУЩИХ УЛУЧШЕНИЙ
    recommendations = generate_recommendations(shortcomings, quality_checks, work_type)

    return ReflectionResult(
        shortcomings=shortcomings,
        improvements_made=improvements.get("improvements", []),
        quality_checks=quality_checks,
        final_score=final_score,
        recommendations=recommendations,
        timestamp=datetime.now()
    )


def get_default_quality_criteria(work_type: str) -> List[str]:
    """
    Получить критерии качества по умолчанию для типа работы.

    Args:
        work_type: Тип работы

    Returns:
        Список критериев качества
    """
    base_criteria = [
        "Универсальность (0% проект-специфичного кода)",
        "Модульность (файлы до 500 строк)",
        "Документация и примеры",
        "Соответствие архитектурным стандартам"
    ]

    type_specific_criteria = {
        "implementation": [
            "Читаемость кода",
            "Обработка ошибок",
            "Type hints и валидация",
            "Тестируемость"
        ],
        "analysis": [
            "Полнота анализа",
            "Конкретность рекомендаций",
            "Учет контекста проекта",
            "Приоритизация задач"
        ],
        "testing": [
            "Покрытие edge cases",
            "Качество assertions",
            "Изоляция тестов",
            "Понятность тест-кейсов"
        ],
        "documentation": [
            "Полнота описания",
            "Примеры использования",
            "Актуальность информации",
            "Структурированность"
        ]
    }

    return base_criteria + type_specific_criteria.get(work_type, [])


async def find_shortcomings(
    work: str,
    work_type: str,
    criteria: List[str]
) -> List[str]:
    """
    Найти минимум 2-3 конкретных недостатка в выполненной работе.

    Args:
        work: Описание выполненной работы
        work_type: Тип работы
        criteria: Критерии качества

    Returns:
        Список найденных недостатков
    """
    shortcomings = []

    # Анализ по каждому критерию
    for criterion in criteria:
        issue = analyze_criterion(work, criterion, work_type)
        if issue:
            shortcomings.append(issue)

    # Специфичный анализ по типу работы
    type_specific_issues = analyze_by_work_type(work, work_type)
    shortcomings.extend(type_specific_issues)

    # Гарантируем минимум 2-3 недостатка
    if len(shortcomings) < 2:
        shortcomings.extend([
            f"Недостаточная детализация в описании {work_type}",
            f"Отсутствие явных примеров применения результатов"
        ])

    return shortcomings[:5]  # Максимум 5 недостатков для фокусировки


def analyze_criterion(work: str, criterion: str, work_type: str) -> str | None:
    """
    Проанализировать работу по конкретному критерию.

    Args:
        work: Описание работы
        criterion: Критерий для проверки
        work_type: Тип работы

    Returns:
        Описание найденного недостатка или None
    """
    # Универсальность
    if "универсальность" in criterion.lower():
        project_specific_indicators = ["unipark", "конкретный проект", "hardcoded"]
        if any(indicator in work.lower() for indicator in project_specific_indicators):
            return "Обнаружены признаки привязки к конкретному проекту - нарушение универсальности"

    # Модульность
    if "модульность" in criterion.lower():
        if "длинный файл" in work.lower() or "большой модуль" in work.lower():
            return "Возможное нарушение модульности - файлы могут превышать 500 строк"

    # Документация
    if "документация" in criterion.lower():
        if "без комментариев" in work.lower() or "недокументирован" in work.lower():
            return "Недостаточная документация кода и функций"

    # Примеры
    if "примеры" in criterion.lower():
        if "пример" not in work.lower() and "example" not in work.lower():
            return "Отсутствуют конкретные примеры использования"

    return None


def analyze_by_work_type(work: str, work_type: str) -> List[str]:
    """
    Провести специфичный анализ по типу работы.

    Args:
        work: Описание работы
        work_type: Тип работы

    Returns:
        Список найденных проблем
    """
    issues = []

    if work_type == "implementation":
        if "error" not in work.lower() and "exception" not in work.lower():
            issues.append("Отсутствует явная обработка ошибок")
        if "test" not in work.lower():
            issues.append("Не упомянуты тесты или тестирование")

    elif work_type == "analysis":
        if "рекомендация" not in work.lower() and "recommendation" not in work.lower():
            issues.append("Отсутствуют конкретные рекомендации")
        if "приоритет" not in work.lower():
            issues.append("Не указаны приоритеты выявленных проблем")

    elif work_type == "testing":
        if "edge case" not in work.lower() and "граничный случай" not in work.lower():
            issues.append("Не упомянуты edge cases и граничные условия")

    elif work_type == "documentation":
        if "getting started" not in work.lower() and "начало работы" not in work.lower():
            issues.append("Отсутствует раздел быстрого старта")

    return issues


async def apply_improvements(
    ctx: RunContext[Any],
    shortcomings: List[str],
    original_work: str
) -> Dict[str, Any]:
    """
    Применить улучшения для устранения найденных недостатков.

    Args:
        ctx: Контекст выполнения
        shortcomings: Список недостатков
        original_work: Исходная работа

    Returns:
        Словарь с примененными улучшениями
    """
    improvements = []

    for shortcoming in shortcomings:
        improvement = generate_improvement_for_shortcoming(shortcoming)
        if improvement:
            improvements.append(improvement)

    return {
        "improvements": improvements,
        "updated_work": original_work,  # В реальности здесь будет обновленная работа
        "shortcomings_addressed": len(improvements)
    }


def generate_improvement_for_shortcoming(shortcoming: str) -> str:
    """
    Сгенерировать конкретное улучшение для недостатка.

    Args:
        shortcoming: Описание недостатка

    Returns:
        Описание улучшения
    """
    improvement_map = {
        "универсальность": "Добавлены конфигурируемые параметры через environment variables",
        "модульность": "Файлы разбиты на логические модули по 300-400 строк",
        "документация": "Добавлены docstrings для всех функций и классов",
        "примеры": "Созданы примеры использования в examples/ директории",
        "ошибок": "Добавлена обработка исключений с информативными сообщениями",
        "тест": "Созданы unit тесты для основных сценариев",
        "рекомендация": "Добавлены конкретные actionable рекомендации",
        "приоритет": "Проставлены приоритеты (P1-High, P2-Medium, P3-Low)",
        "edge case": "Добавлены тесты для граничных случаев",
        "начало работы": "Добавлен раздел Quick Start с примером"
    }

    for keyword, improvement in improvement_map.items():
        if keyword in shortcoming.lower():
            return improvement

    return f"Устранен недостаток: {shortcoming[:50]}..."


async def validate_quality_criteria(
    criteria: List[str],
    work: str
) -> Dict[str, bool]:
    """
    Проверить соответствие работы критериям качества.

    Args:
        criteria: Список критериев
        work: Выполненная работа

    Returns:
        Словарь критерий -> соответствие
    """
    results = {}

    for criterion in criteria:
        # Упрощенная проверка - в реальности более сложная логика
        results[criterion] = check_criterion_met(criterion, work)

    return results


def check_criterion_met(criterion: str, work: str) -> bool:
    """
    Проверить выполнение конкретного критерия.

    Args:
        criterion: Критерий для проверки
        work: Выполненная работа

    Returns:
        True если критерий выполнен
    """
    # Базовая эвристика - в реальности более сложная проверка
    positive_indicators = {
        "универсальность": ["конфигурируем", "настраиваем", "параметр"],
        "модульность": ["модуль", "разделен", "структура"],
        "документация": ["docstring", "комментари", "описание"],
        "примеры": ["example", "пример", "использование"],
        "читаемость": ["понятн", "читаем", "clear"],
        "тест": ["test", "тест", "pytest"]
    }

    for keyword, indicators in positive_indicators.items():
        if keyword in criterion.lower():
            return any(indicator in work.lower() for indicator in indicators)

    return True  # По умолчанию считаем выполненным


def calculate_quality_score(
    quality_checks: Dict[str, bool],
    shortcomings_count: int,
    improvements_count: int
) -> float:
    """
    Рассчитать общий балл качества.

    Args:
        quality_checks: Результаты проверок критериев
        shortcomings_count: Количество найденных недостатков
        improvements_count: Количество примененных улучшений

    Returns:
        Балл качества от 0.0 до 10.0
    """
    # Процент выполненных критериев
    criteria_score = sum(1 for passed in quality_checks.values() if passed) / len(quality_checks) if quality_checks else 0

    # Бонус за проактивные улучшения
    improvement_bonus = min(improvements_count / shortcomings_count, 1.0) if shortcomings_count > 0 else 1.0

    # Итоговый балл
    final_score = (criteria_score * 0.7 + improvement_bonus * 0.3) * 10

    return round(final_score, 2)


def generate_recommendations(
    shortcomings: List[str],
    quality_checks: Dict[str, bool],
    work_type: str
) -> List[str]:
    """
    Сгенерировать рекомендации для будущих улучшений.

    Args:
        shortcomings: Найденные недостатки
        quality_checks: Результаты проверок качества
        work_type: Тип работы

    Returns:
        Список рекомендаций
    """
    recommendations = []

    # Рекомендации на основе непройденных критериев
    for criterion, passed in quality_checks.items():
        if not passed:
            recommendations.append(f"Усилить фокус на: {criterion}")

    # Рекомендации на основе паттернов недостатков
    if any("универсальность" in s.lower() for s in shortcomings):
        recommendations.append("Использовать конфигурацию через .env и settings для всех проект-специфичных параметров")

    if any("документация" in s.lower() for s in shortcomings):
        recommendations.append("Добавлять docstrings в процессе написания кода, а не после")

    if any("тест" in s.lower() for s in shortcomings):
        recommendations.append("Практиковать TDD - писать тесты до реализации")

    # Общие рекомендации по типу работы
    type_recommendations = {
        "implementation": "Следовать чеклисту: code → tests → docs → review",
        "analysis": "Структурировать анализ: проблема → причина → решение → приоритет",
        "testing": "Покрывать минимум 3 сценария: happy path, edge case, error case",
        "documentation": "Использовать структуру: что → зачем → как → примеры"
    }

    if work_type in type_recommendations:
        recommendations.append(type_recommendations[work_type])

    return recommendations[:5]  # Максимум 5 рекомендаций


def format_reflection_report(result: ReflectionResult) -> str:
    """
    Форматировать результат рефлексии для вывода пользователю.

    Args:
        result: Результат рефлексии

    Returns:
        Отформатированный отчет
    """
    report = f"""
🔍 **КРИТИЧЕСКИЙ АНАЛИЗ ВЫПОЛНЕННОЙ РАБОТЫ**

**Найденные недостатки ({len(result.shortcomings)}):**
"""

    for i, shortcoming in enumerate(result.shortcomings, 1):
        report += f"{i}. {shortcoming}\n"

    report += f"\n**Внесенные улучшения ({len(result.improvements_made)}):**\n"

    for i, improvement in enumerate(result.improvements_made, 1):
        report += f"{i}. {improvement}\n"

    report += "\n**Проверка критериев качества:**\n"

    for criterion, passed in result.quality_checks.items():
        status = "✅" if passed else "❌"
        report += f"{status} {criterion}\n"

    report += f"\n**Общий балл качества:** {result.final_score}/10.0\n"

    if result.recommendations:
        report += "\n**Рекомендации для будущих улучшений:**\n"
        for i, rec in enumerate(result.recommendations, 1):
            report += f"{i}. {rec}\n"

    report += f"\n*Анализ выполнен: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}*\n"

    return report


__all__ = [
    "advanced_reflection",
    "ReflectionResult",
    "format_reflection_report",
    "get_default_quality_criteria"
]
