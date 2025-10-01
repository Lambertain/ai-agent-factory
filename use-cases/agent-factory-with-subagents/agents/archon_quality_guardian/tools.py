# -*- coding: utf-8 -*-
"""
Инструменты для Archon Quality Guardian Agent
"""

import os
import subprocess
import json
from typing import List, Dict, Any, Optional
from pathlib import Path


async def run_command(command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
    """
    Выполнить команду и вернуть результат.

    Args:
        command: Команда для выполнения
        cwd: Рабочая директория

    Returns:
        Словарь с результатом выполнения
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timeout exceeded (60s)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def analyze_python_code(file_path: str, project_path: str) -> Dict[str, Any]:
    """
    Анализ Python кода с помощью статических анализаторов.

    Args:
        file_path: Путь к файлу
        project_path: Корень проекта

    Returns:
        Результаты анализа
    """
    results = {}

    # Pylint
    pylint_result = await run_command(
        f"pylint {file_path} --output-format=json",
        cwd=project_path
    )
    if pylint_result["success"]:
        try:
            results["pylint"] = json.loads(pylint_result["stdout"])
        except:
            results["pylint"] = {"issues": []}

    # Flake8
    flake8_result = await run_command(
        f"flake8 {file_path} --format=json",
        cwd=project_path
    )
    if flake8_result["success"]:
        try:
            results["flake8"] = json.loads(flake8_result["stdout"])
        except:
            results["flake8"] = {"issues": []}

    # MyPy
    mypy_result = await run_command(
        f"mypy {file_path} --json",
        cwd=project_path
    )
    if mypy_result["success"]:
        try:
            results["mypy"] = json.loads(mypy_result["stdout"])
        except:
            results["mypy"] = {"issues": []}

    # Bandit (security)
    bandit_result = await run_command(
        f"bandit {file_path} -f json",
        cwd=project_path
    )
    if bandit_result["success"]:
        try:
            results["bandit"] = json.loads(bandit_result["stdout"])
        except:
            results["bandit"] = {"issues": []}

    return results


async def analyze_typescript_code(file_path: str, project_path: str) -> Dict[str, Any]:
    """
    Анализ TypeScript кода с помощью статических анализаторов.

    Args:
        file_path: Путь к файлу
        project_path: Корень проекта

    Returns:
        Результаты анализа
    """
    results = {}

    # ESLint
    eslint_result = await run_command(
        f"eslint {file_path} --format=json",
        cwd=project_path
    )
    if eslint_result["success"]:
        try:
            results["eslint"] = json.loads(eslint_result["stdout"])
        except:
            results["eslint"] = {"issues": []}

    # TypeScript Compiler
    tsc_result = await run_command(
        "tsc --noEmit --pretty false",
        cwd=project_path
    )
    results["tsc"] = {
        "success": tsc_result["success"],
        "errors": tsc_result.get("stderr", "")
    }

    return results


async def calculate_code_metrics(file_path: str, language: str) -> Dict[str, Any]:
    """
    Рассчитать метрики кода (сложность, размер, и т.д.).

    Args:
        file_path: Путь к файлу
        language: Язык программирования

    Returns:
        Словарь с метриками
    """
    metrics = {
        "lines_of_code": 0,
        "complexity": 0,
        "functions": 0,
        "classes": 0
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

            # Подсчет строк кода (исключая пустые и комментарии)
            code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
            metrics["lines_of_code"] = len(code_lines)

            # Упрощенный подсчет функций и классов
            if language == "python":
                metrics["functions"] = content.count('def ')
                metrics["classes"] = content.count('class ')
            elif language == "typescript":
                metrics["functions"] = content.count('function ') + content.count('=>')
                metrics["classes"] = content.count('class ')

    except Exception as e:
        metrics["error"] = str(e)

    return metrics


async def get_test_coverage(project_path: str, language: str) -> Dict[str, Any]:
    """
    Получить test coverage для проекта.

    Args:
        project_path: Путь к проекту
        language: Язык программирования

    Returns:
        Информация о покрытии тестами
    """
    coverage_data = {
        "coverage_percentage": 0.0,
        "branch_coverage": 0.0,
        "files_covered": 0,
        "total_files": 0
    }

    try:
        if language == "python":
            # Запуск pytest с coverage
            result = await run_command(
                "pytest --cov=. --cov-report=json",
                cwd=project_path
            )

            if result["success"]:
                coverage_file = Path(project_path) / "coverage.json"
                if coverage_file.exists():
                    with open(coverage_file, 'r') as f:
                        coverage_json = json.load(f)
                        coverage_data["coverage_percentage"] = coverage_json.get("totals", {}).get("percent_covered", 0.0)

        elif language == "typescript":
            # Запуск Jest с coverage
            result = await run_command(
                "jest --coverage --coverageReporters=json",
                cwd=project_path
            )

            if result["success"]:
                coverage_file = Path(project_path) / "coverage" / "coverage-summary.json"
                if coverage_file.exists():
                    with open(coverage_file, 'r') as f:
                        coverage_json = json.load(f)
                        total = coverage_json.get("total", {})
                        coverage_data["coverage_percentage"] = total.get("lines", {}).get("pct", 0.0)

    except Exception as e:
        coverage_data["error"] = str(e)

    return coverage_data


async def detect_code_smells(code: str, language: str) -> List[Dict[str, Any]]:
    """
    Детектировать code smells в коде.

    Args:
        code: Код для анализа
        language: Язык программирования

    Returns:
        Список code smells
    """
    smells = []

    lines = code.split('\n')

    # Длинные методы
    if len(lines) > 50:
        smells.append({
            "type": "long_method",
            "severity": "major",
            "description": f"Метод содержит {len(lines)} строк (рекомендуется < 50)",
            "refactoring": "Разбейте метод на более мелкие функции"
        })

    # Много параметров
    for i, line in enumerate(lines):
        if language == "python" and "def " in line:
            # Простая эвристика для подсчета параметров
            params_count = line.count(',') + 1 if '(' in line and ')' in line else 0
            if params_count > 5:
                smells.append({
                    "type": "too_many_parameters",
                    "severity": "major",
                    "line": i + 1,
                    "description": f"Функция имеет {params_count} параметров (рекомендуется < 5)",
                    "refactoring": "Используйте объект конфигурации или паттерн Builder"
                })

    # Дублирование кода
    unique_lines = set(line.strip() for line in lines if line.strip())
    if len(unique_lines) < len(lines) * 0.7:  # Более 30% дубликатов
        smells.append({
            "type": "code_duplication",
            "severity": "minor",
            "description": "Обнаружено дублирование кода",
            "refactoring": "Вынесите повторяющийся код в отдельную функцию"
        })

    return smells


async def estimate_fix_time(issue: Dict[str, Any]) -> float:
    """
    Оценить время на исправление проблемы.

    Args:
        issue: Описание проблемы

    Returns:
        Оценка времени в часах
    """
    severity = issue.get("severity", "minor")

    # Базовая оценка времени по severity
    time_estimates = {
        "blocker": 4.0,
        "critical": 2.0,
        "major": 1.0,
        "minor": 0.5,
        "info": 0.25
    }

    return time_estimates.get(severity, 0.5)


async def find_project_files(project_path: str, extensions: List[str]) -> List[str]:
    """
    Найти все файлы проекта с указанными расширениями.

    Args:
        project_path: Путь к проекту
        extensions: Список расширений файлов

    Returns:
        Список путей к файлам
    """
    files = []

    for ext in extensions:
        pattern = f"**/*{ext}"
        for file_path in Path(project_path).glob(pattern):
            if file_path.is_file():
                # Исключаем node_modules, venv, __pycache__ и т.д.
                if not any(excl in str(file_path) for excl in ['node_modules', 'venv', '__pycache__', '.git']):
                    files.append(str(file_path))

    return files


def format_quality_report(metrics: Dict[str, Any], issues: List[Dict], smells: List[Dict]) -> str:
    """
    Форматировать отчет о качестве кода для пользователя.

    Args:
        metrics: Метрики качества
        issues: Найденные проблемы
        smells: Code smells

    Returns:
        Форматированный отчет
    """
    report = "# Quality Analysis Report\n\n"

    # Метрики
    report += "## Metrics\n"
    report += f"- Lines of Code: {metrics.get('lines_of_code', 'N/A')}\n"
    report += f"- Test Coverage: {metrics.get('coverage_percentage', 0):.1f}%\n"
    report += f"- Complexity Score: {metrics.get('complexity', 'N/A')}\n"
    report += f"- Maintainability Index: {metrics.get('maintainability_index', 'N/A')}\n\n"

    # Проблемы по severity
    if issues:
        report += "## Issues by Severity\n"
        by_severity = {}
        for issue in issues:
            severity = issue.get("severity", "unknown")
            by_severity[severity] = by_severity.get(severity, 0) + 1

        for severity, count in sorted(by_severity.items()):
            report += f"- {severity.capitalize()}: {count}\n"
        report += "\n"

    # Code Smells
    if smells:
        report += "## Code Smells\n"
        for smell in smells[:5]:  # Top 5
            report += f"- **{smell['type']}** (Line {smell.get('line', 'N/A')}): {smell['description']}\n"
            report += f"  *Refactoring:* {smell['refactoring']}\n"
        report += "\n"

    # Рекомендации
    report += "## Recommendations\n"
    if metrics.get('coverage_percentage', 0) < 80:
        report += "- Increase test coverage to at least 80%\n"
    if len(issues) > 10:
        report += "- Address critical and major issues first\n"
    if smells:
        report += "- Refactor code smells to improve maintainability\n"

    return report
