# -*- coding: utf-8 -*-
"""
Инструменты для роли Quality Guardian.

Эти функции помогают МНЕ (Claude) когда я переключаюсь в роль Quality Guardian.
Я использую их для проверки качества кода и создания задач исправления.
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple

from .checklists import (
    ROLE_SWITCHING_CHECKLIST,
    UNIVERSALITY_CHECKLIST,
    CODE_QUALITY_CHECKLIST,
    ARCHITECTURE_CHECKLIST,
    DOCUMENTATION_CHECKLIST,
    TESTING_CHECKLIST
)


def run_quality_audit(project_path: str) -> str:
    """
    Запустить полный аудит качества проекта.

    Я использую этот инструмент когда нужно проверить весь проект.

    Args:
        project_path: Путь к проекту для проверки

    Returns:
        Отчет с найденными проблемами
    """
    project_path = Path(project_path)
    problems = []

    print("🔍 Начинаю аудит качества...")

    # Проверка переключения в роли (КРИТИЧЕСКИ ВАЖНО!)
    role_problems = check_role_switching(project_path)
    problems.extend(role_problems)

    # Проверка универсальности
    univ_problems = check_universality(project_path)
    problems.extend(univ_problems)

    # Проверка качества кода
    code_problems = check_code_quality(project_path)
    problems.extend(code_problems)

    # Проверка архитектуры
    arch_problems = check_architecture(project_path)
    problems.extend(arch_problems)

    # Проверка документации
    doc_problems = check_documentation(project_path)
    problems.extend(doc_problems)

    # Проверка тестов
    test_problems = check_testing(project_path)
    problems.extend(test_problems)

    # Формируем отчет
    report = format_audit_report(problems)

    print(f"✅ Аудит завершен. Найдено проблем: {len(problems)}")

    return report


def check_role_switching(project_path: Path) -> List[Dict]:
    """
    🚨 КРИТИЧЕСКИ ВАЖНО: Проверить переключение агентов в роли.

    Args:
        project_path: Путь к проекту

    Returns:
        Список найденных проблем
    """
    problems = []
    checklist = ROLE_SWITCHING_CHECKLIST

    print(f"🎭 Проверка: {checklist['name']}...")

    # Находим все файлы агентов
    agent_files = list(project_path.glob("agents/*/agent.py"))

    for agent_file in agent_files:
        agent_name = agent_file.parent.name

        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Проверяем каждый пункт чеклиста
        for item in checklist['items']:
            if not re.search(item['what_to_find'], content, re.IGNORECASE):
                problems.append({
                    "file": str(agent_file),
                    "agent": agent_name,
                    "severity": item['severity'],
                    "check_id": item['id'],
                    "problem": f"{item['check']} - НЕ НАЙДЕНО",
                    "where": item['where']
                })

    return problems


def check_universality(project_path: Path) -> List[Dict]:
    """
    Проверить универсальность агентов (0% проект-специфичного кода).

    Args:
        project_path: Путь к проекту

    Returns:
        Список найденных проблем
    """
    problems = []
    checklist = UNIVERSALITY_CHECKLIST

    print(f"🌐 Проверка: {checklist['name']}...")

    # Находим все Python файлы агентов
    python_files = list(project_path.glob("agents/**/*.py"))

    for py_file in python_files:
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Проверяем запрещенные термины
        for line_num, line in enumerate(lines, 1):
            for forbidden_term in checklist['forbidden_terms']:
                if forbidden_term in line:
                    # Исключаем комментарии с примерами
                    if '# Пример:' not in line and '# Example:' not in line:
                        problems.append({
                            "file": str(py_file),
                            "line": line_num,
                            "severity": "BLOCKER",
                            "check_id": "no_hardcoded_projects",
                            "problem": f"Найден проект-специфичный термин: {forbidden_term}",
                            "where": f"Строка {line_num}"
                        })

    # Проверяем наличие examples/
    agents_dirs = [d for d in project_path.glob("agents/*") if d.is_dir()]
    for agent_dir in agents_dirs:
        examples_dir = agent_dir / "examples"
        if not examples_dir.exists():
            problems.append({
                "file": str(agent_dir),
                "severity": "MAJOR",
                "check_id": "examples_directory",
                "problem": "Отсутствует examples/ директория",
                "where": "agents/{}/examples/".format(agent_dir.name)
            })

    return problems


def check_code_quality(project_path: Path) -> List[Dict]:
    """
    Проверить качество кода.

    Args:
        project_path: Путь к проекту

    Returns:
        Список найденных проблем
    """
    problems = []

    print("📝 Проверка: качество кода...")

    python_files = list(project_path.glob("agents/**/*.py"))

    for py_file in python_files:
        with open(py_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            line_count = len(lines)
            content = ''.join(lines)

        # Проверка размера файла (max 500 строк)
        if line_count > 500:
            problems.append({
                "file": str(py_file),
                "severity": "MAJOR",
                "check_id": "file_size_limit",
                "problem": f"Файл слишком большой: {line_count} строк (max 500)",
                "where": "Весь файл"
            })

        # Проверка docstrings
        functions = re.findall(r'^(async )?def (\w+)\(', content, re.MULTILINE)
        for is_async, func_name in functions:
            func_pattern = f"(async )?def {func_name}\\([^)]*\\):[\\s\\n]*\"\"\""
            if not re.search(func_pattern, content):
                problems.append({
                    "file": str(py_file),
                    "severity": "MINOR",
                    "check_id": "docstrings",
                    "problem": f"Отсутствует docstring для функции {func_name}",
                    "where": f"Функция {func_name}"
                })

    return problems


def check_architecture(project_path: Path) -> List[Dict]:
    """
    Проверить архитектуру агентов.

    Args:
        project_path: Путь к проекту

    Returns:
        Список найденных проблем
    """
    problems = []
    checklist = ARCHITECTURE_CHECKLIST

    print("🏗️ Проверка: архитектура...")

    agents_dirs = [d for d in project_path.glob("agents/*") if d.is_dir()]

    for agent_dir in agents_dirs:
        # Проверяем обязательные файлы
        for required_file in checklist['required_files']:
            file_path = agent_dir / required_file
            if not file_path.exists():
                problems.append({
                    "file": str(agent_dir),
                    "severity": "CRITICAL",
                    "check_id": "required_files_exist",
                    "problem": f"Отсутствует обязательный файл: {required_file}",
                    "where": f"agents/{agent_dir.name}/{required_file}"
                })

    return problems


def check_documentation(project_path: Path) -> List[Dict]:
    """
    Проверить документацию.

    Args:
        project_path: Путь к проекту

    Returns:
        Список найденных проблем
    """
    problems = []

    print("📚 Проверка: документация...")

    agents_dirs = [d for d in project_path.glob("agents/*") if d.is_dir()]

    for agent_dir in agents_dirs:
        # Проверяем README.md
        readme = agent_dir / "README.md"
        if not readme.exists():
            problems.append({
                "file": str(agent_dir),
                "severity": "MAJOR",
                "check_id": "readme_exists",
                "problem": "Отсутствует README.md",
                "where": f"agents/{agent_dir.name}/README.md"
            })

        # Проверяем базу знаний
        knowledge_dir = agent_dir / "knowledge"
        if not knowledge_dir.exists():
            problems.append({
                "file": str(agent_dir),
                "severity": "MAJOR",
                "check_id": "knowledge_base",
                "problem": "Отсутствует knowledge/ директория",
                "where": f"agents/{agent_dir.name}/knowledge/"
            })

    return problems


def check_testing(project_path: Path) -> List[Dict]:
    """
    Проверить тестирование.

    Args:
        project_path: Путь к проекту

    Returns:
        Список найденных проблем
    """
    problems = []

    print("🧪 Проверка: тестирование...")

    agents_dirs = [d for d in project_path.glob("agents/*") if d.is_dir()]

    for agent_dir in agents_dirs:
        tests_dir = agent_dir / "tests"
        if not tests_dir.exists():
            problems.append({
                "file": str(agent_dir),
                "severity": "MAJOR",
                "check_id": "tests_directory",
                "problem": "Отсутствует tests/ директория",
                "where": f"agents/{agent_dir.name}/tests/"
            })

    return problems


def format_audit_report(problems: List[Dict]) -> str:
    """
    Отформатировать отчет аудита для вывода.

    Args:
        problems: Список найденных проблем

    Returns:
        Форматированный отчет
    """
    if not problems:
        return "✅ Проблем не найдено! Отличная работа!"

    # Группируем по серьезности
    by_severity = {}
    for problem in problems:
        severity = problem.get('severity', 'INFO')
        if severity not in by_severity:
            by_severity[severity] = []
        by_severity[severity].append(problem)

    # Формируем отчет
    report = "📊 ОТЧЕТ АУДИТА КАЧЕСТВА\n"
    report += "=" * 80 + "\n\n"

    report += f"🔍 Всего проблем найдено: {len(problems)}\n\n"

    # Проблемы по серьезности
    severity_order = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]

    for severity in severity_order:
        if severity in by_severity:
            count = len(by_severity[severity])
            report += f"\n{'🚨' if severity == 'BLOCKER' else '❌' if severity == 'CRITICAL' else '⚠️'} {severity}: {count} проблем\n"
            report += "-" * 80 + "\n"

            for i, problem in enumerate(by_severity[severity][:10], 1):  # Показываем первые 10
                report += f"\n{i}. {problem.get('problem', 'Неизвестная проблема')}\n"
                report += f"   📁 Файл: {problem.get('file', 'N/A')}\n"
                if 'line' in problem:
                    report += f"   📍 Строка: {problem.get('line')}\n"
                report += f"   📍 Где: {problem.get('where', 'N/A')}\n"

            if count > 10:
                report += f"\n... и еще {count - 10} проблем\n"

    return report


def create_archon_tasks_for_problems(problems: List[Dict], project_id: str) -> str:
    """
    Создать задачи в Archon для найденных проблем.

    Я использую этот инструмент после аудита, чтобы создать задачи исправления.

    Args:
        problems: Список найденных проблем
        project_id: ID проекта в Archon

    Returns:
        Отчет о созданных задачах
    """
    print(f"📋 Создаю задачи в Archon для {len(problems)} проблем...")

    tasks_by_severity = {}
    for problem in problems:
        severity = problem.get('severity', 'INFO')
        if severity not in tasks_by_severity:
            tasks_by_severity[severity] = []
        tasks_by_severity[severity].append(problem)

    # Формируем отчет
    report = f"📋 ЗАДАЧИ ДЛЯ СОЗДАНИЯ В ARCHON\n"
    report += "=" * 80 + "\n\n"

    severity_order = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR"]
    task_count = 0

    for severity in severity_order:
        if severity not in tasks_by_severity:
            continue

        problems_list = tasks_by_severity[severity]
        report += f"\n{severity}: {len(problems_list)} задач\n"
        report += "-" * 80 + "\n"

        for problem in problems_list:
            task_count += 1
            report += f"\nЗадача {task_count}:\n"
            report += f"Название: {problem.get('problem')}\n"
            report += f"Файл: {problem.get('file')}\n"
            report += f"Приоритет: {severity}\n"
            report += f"Назначить на: Implementation Engineer\n"

    report += f"\n\n✅ Всего задач для создания: {task_count}\n"
    report += "\n💡 СЛЕДУЮЩИЙ ШАГ: Используй mcp__archon__manage_task для создания этих задач в Archon\n"

    return report
