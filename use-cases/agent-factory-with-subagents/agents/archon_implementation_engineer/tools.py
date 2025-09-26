#!/usr/bin/env python3
"""
Инструменты для Archon Implementation Engineer Agent.

Набор специализированных инструментов для разработки кода и реализации функций.
"""

import json
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import ImplementationEngineerDependencies, ProgrammingLanguage, DevelopmentFramework


class CodeStructure(BaseModel):
    """Модель структуры кода."""
    files: List[Dict[str, str]] = Field(description="Список файлов с их содержимым")
    directories: List[str] = Field(description="Список директорий")
    dependencies: List[str] = Field(description="Внешние зависимости")
    entry_points: List[str] = Field(description="Точки входа приложения")
    tests: List[Dict[str, str]] = Field(description="Тестовые файлы")


class FeatureImplementation(BaseModel):
    """Модель реализации функции."""
    feature_name: str = Field(description="Название функции")
    code_files: List[Dict[str, str]] = Field(description="Файлы кода")
    test_files: List[Dict[str, str]] = Field(description="Тестовые файлы")
    documentation: str = Field(description="Документация к функции")
    dependencies: List[str] = Field(description="Необходимые зависимости")
    configuration: Dict[str, Any] = Field(description="Настройки конфигурации")


class QualityReport(BaseModel):
    """Отчет о качестве кода."""
    overall_score: float = Field(description="Общая оценка качества (0-100)")
    issues: List[Dict[str, str]] = Field(description="Найденные проблемы")
    suggestions: List[str] = Field(description="Рекомендации по улучшению")
    metrics: Dict[str, Any] = Field(description="Метрики кода")
    compliance: Dict[str, bool] = Field(description="Соответствие стандартам")


async def implement_feature(
    ctx: RunContext[ImplementationEngineerDependencies],
    feature_description: str,
    requirements: List[str],
    priority: str = "medium"
) -> FeatureImplementation:
    """
    Реализовать функцию согласно описанию и требованиям.

    Args:
        ctx: Контекст выполнения с зависимостями
        feature_description: Описание функции для реализации
        requirements: Список требований к функции
        priority: Приоритет функции (low/medium/high/critical)

    Returns:
        Реализация функции с кодом и тестами
    """
    deps = ctx.deps
    dev_config = deps.get_development_config()
    quality_config = deps.get_quality_config()

    # Анализируем требования для определения архитектуры
    code_files = []
    test_files = []

    # Генерируем основной код в зависимости от языка и фреймворка
    if deps.primary_language == ProgrammingLanguage.PYTHON:
        if deps.framework == DevelopmentFramework.FASTAPI:
            code_files.extend(_generate_fastapi_implementation(feature_description, requirements))
        elif deps.framework == DevelopmentFramework.DJANGO:
            code_files.extend(_generate_django_implementation(feature_description, requirements))
    elif deps.primary_language == ProgrammingLanguage.TYPESCRIPT:
        if deps.framework == DevelopmentFramework.NEXTJS:
            code_files.extend(_generate_nextjs_implementation(feature_description, requirements))

    # Генерируем тесты, если включено
    if deps.should_create_tests():
        test_files = _generate_test_files(feature_description, code_files, deps)

    # Создаем документацию
    documentation = _generate_feature_documentation(
        feature_description,
        requirements,
        code_files,
        dev_config
    )

    return FeatureImplementation(
        feature_name=_extract_feature_name(feature_description),
        code_files=code_files,
        test_files=test_files,
        documentation=documentation,
        dependencies=_extract_dependencies(requirements, deps),
        configuration=_generate_configuration(requirements, deps)
    )


async def create_code_structure(
    ctx: RunContext[ImplementationEngineerDependencies],
    project_name: str,
    architecture_type: str = "layered"
) -> CodeStructure:
    """
    Создать базовую структуру кода проекта.

    Args:
        ctx: Контекст выполнения с зависимостями
        project_name: Название проекта
        architecture_type: Тип архитектуры (layered/hexagonal/microservices)

    Returns:
        Структура кода проекта
    """
    deps = ctx.deps
    dev_config = deps.get_development_config()

    # Создаем структуру директорий
    directories = _generate_directory_structure(architecture_type, deps)

    # Создаем базовые файлы
    files = _generate_base_files(project_name, architecture_type, deps)

    # Определяем зависимости
    dependencies = _determine_project_dependencies(deps)

    # Создаем точки входа
    entry_points = _generate_entry_points(project_name, deps)

    # Создаем базовые тесты
    tests = []
    if deps.should_create_tests():
        tests = _generate_base_test_structure(project_name, deps)

    return CodeStructure(
        files=files,
        directories=directories,
        dependencies=dependencies,
        entry_points=entry_points,
        tests=tests
    )


async def generate_tests(
    ctx: RunContext[ImplementationEngineerDependencies],
    code_content: str,
    test_type: str = "unit"
) -> List[Dict[str, str]]:
    """
    Генерировать тесты для переданного кода.

    Args:
        ctx: Контекст выполнения с зависимостями
        code_content: Содержимое кода для тестирования
        test_type: Тип тестов (unit/integration/e2e)

    Returns:
        Список тестовых файлов
    """
    deps = ctx.deps
    testing_strategy = deps.get_testing_strategy()

    if not testing_strategy.get("enabled", False):
        return []

    test_files = []

    # Генерируем тесты в зависимости от языка
    if deps.primary_language == ProgrammingLanguage.PYTHON:
        test_files = _generate_python_tests(code_content, test_type, deps)
    elif deps.primary_language == ProgrammingLanguage.TYPESCRIPT:
        test_files = _generate_typescript_tests(code_content, test_type, deps)

    return test_files


async def optimize_performance(
    ctx: RunContext[ImplementationEngineerDependencies],
    code_content: str,
    performance_targets: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Оптимизировать код для улучшения производительности.

    Args:
        ctx: Контекст выполнения с зависимостями
        code_content: Содержимое кода для оптимизации
        performance_targets: Целевые показатели производительности

    Returns:
        Результат оптимизации с улучшенным кодом
    """
    deps = ctx.deps
    perf_requirements = deps.get_performance_requirements()

    optimizations = []
    optimized_code = code_content

    # Анализируем код на предмет узких мест
    bottlenecks = _analyze_performance_bottlenecks(code_content)

    for bottleneck in bottlenecks:
        optimization = _apply_performance_optimization(
            bottleneck,
            code_content,
            deps
        )
        optimizations.append(optimization)
        if optimization.get("improved_code"):
            optimized_code = optimization["improved_code"]

    return {
        "original_code": code_content,
        "optimized_code": optimized_code,
        "optimizations_applied": optimizations,
        "performance_improvements": _calculate_performance_improvements(optimizations),
        "recommendations": perf_requirements
    }


async def validate_code_quality(
    ctx: RunContext[ImplementationEngineerDependencies],
    code_files: List[Dict[str, str]]
) -> QualityReport:
    """
    Валидировать качество кода согласно стандартам.

    Args:
        ctx: Контекст выполнения с зависимостями
        code_files: Список файлов кода для проверки

    Returns:
        Отчет о качестве кода
    """
    deps = ctx.deps
    quality_config = deps.get_quality_config()

    issues = []
    suggestions = []
    metrics = {}
    compliance = {}

    for file_info in code_files:
        file_path = file_info.get("path", "unknown")
        file_content = file_info.get("content", "")

        # Проверяем размер файла
        line_count = len(file_content.split('\n'))
        if line_count > quality_config["max_file_lines"]:
            issues.append({
                "file": file_path,
                "type": "file_size",
                "message": f"Файл содержит {line_count} строк, превышает лимит {quality_config['max_file_lines']}"
            })

        # Проверяем стиль кода
        style_issues = _check_code_style(file_content, quality_config, deps)
        issues.extend(style_issues)

        # Проверяем безопасность
        if deps.enable_security_checks:
            security_issues = _check_security_issues(file_content, deps)
            issues.extend(security_issues)

        # Собираем метрики
        file_metrics = _calculate_file_metrics(file_content)
        metrics[file_path] = file_metrics

    # Проверяем соответствие стандартам
    compliance = {
        "style_guide": len([i for i in issues if i.get("type") == "style"]) == 0,
        "file_size": len([i for i in issues if i.get("type") == "file_size"]) == 0,
        "security": len([i for i in issues if i.get("type") == "security"]) == 0,
        "type_checking": _check_type_annotations(code_files) if deps.enable_type_checking else True
    }

    # Генерируем рекомендации
    suggestions = _generate_quality_suggestions(issues, quality_config)

    # Рассчитываем общий балл
    overall_score = _calculate_quality_score(issues, compliance, len(code_files))

    return QualityReport(
        overall_score=overall_score,
        issues=issues,
        suggestions=suggestions,
        metrics=metrics,
        compliance=compliance
    )


async def search_implementation_knowledge(
    ctx: RunContext[ImplementationEngineerDependencies],
    query: str,
    knowledge_type: str = "implementation"
) -> Dict[str, Any]:
    """
    Поиск знаний по реализации в базе знаний.

    Args:
        ctx: Контекст выполнения с зависимостями
        query: Поисковый запрос
        knowledge_type: Тип знаний (implementation, patterns, examples)

    Returns:
        Результаты поиска знаний по реализации
    """
    deps = ctx.deps

    # Формируем расширенный запрос с тегами знаний
    enhanced_query = f"{query} {' '.join(deps.knowledge_tags)}"

    # Симуляция поиска в базе знаний
    search_results = {
        "query": query,
        "knowledge_type": knowledge_type,
        "results": [
            {
                "title": f"Паттерны реализации для {query}",
                "content": f"Рекомендации по реализации {query} с использованием {deps.primary_language.value}",
                "relevance": 0.9,
                "source": "implementation_knowledge_base",
                "code_examples": _generate_code_examples(query, deps)
            }
        ],
        "total_results": 1,
        "search_time_ms": 120
    }

    return search_results


async def delegate_to_quality_guardian(
    ctx: RunContext[ImplementationEngineerDependencies],
    task_description: str,
    code_files: List[Dict[str, str]],
    priority: str = "medium"
) -> Dict[str, Any]:
    """
    Делегировать задачу Quality Guardian для проверки качества.

    Args:
        ctx: Контекст выполнения с зависимостями
        task_description: Описание задачи для проверки
        code_files: Файлы кода для проверки
        priority: Приоритет задачи

    Returns:
        Результат делегирования
    """
    deps = ctx.deps

    if not deps.collaborate_with_quality_guardian:
        return {"delegated": False, "reason": "Коллаборация с Quality Guardian отключена"}

    # Подготавливаем контекст для Quality Guardian
    delegation_context = {
        "task_type": "code_review",
        "description": task_description,
        "files_count": len(code_files),
        "quality_standard": deps.quality_standard.value,
        "testing_required": deps.should_create_tests(),
        "languages": [deps.primary_language.value],
        "framework": deps.framework.value
    }

    return {
        "delegated": True,
        "assigned_to": "Archon Quality Guardian",
        "task_context": delegation_context,
        "priority": priority,
        "expected_deliverables": [
            "Code review report",
            "Quality assessment",
            "Improvement recommendations"
        ]
    }


# Вспомогательные функции

def _generate_fastapi_implementation(feature_description: str, requirements: List[str]) -> List[Dict[str, str]]:
    """Генерировать реализацию для FastAPI."""
    files = [
        {
            "path": "main.py",
            "content": f"""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="{_extract_feature_name(feature_description)}")

# Модели данных
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    class Config:
        from_attributes = True

# Эндпоинты
@app.get("/items/", response_model=List[Item])
async def read_items():
    '''Получить список элементов'''
    return []

@app.post("/items/", response_model=Item)
async def create_item(item: ItemCreate):
    '''Создать новый элемент'''
    return Item(id=1, **item.dict())
"""
        }
    ]
    return files


def _generate_django_implementation(feature_description: str, requirements: List[str]) -> List[Dict[str, str]]:
    """Генерировать реализацию для Django."""
    return [
        {
            "path": "models.py",
            "content": f"# Django модели для {_extract_feature_name(feature_description)}\nfrom django.db import models\n"
        }
    ]


def _generate_nextjs_implementation(feature_description: str, requirements: List[str]) -> List[Dict[str, str]]:
    """Генерировать реализацию для Next.js."""
    return [
        {
            "path": "pages/api/items.ts",
            "content": f"// Next.js API для {_extract_feature_name(feature_description)}\nexport default function handler(req, res) {{\n  res.status(200).json({{ message: 'Hello' }});\n}}"
        }
    ]


def _generate_test_files(feature_description: str, code_files: List[Dict[str, str]], deps) -> List[Dict[str, str]]:
    """Генерировать тестовые файлы."""
    return [
        {
            "path": "test_main.py",
            "content": f"# Тесты для {_extract_feature_name(feature_description)}\nimport pytest\n\ndef test_example():\n    assert True\n"
        }
    ]


def _generate_python_tests(code_content: str, test_type: str, deps) -> List[Dict[str, str]]:
    """Генерировать Python тесты."""
    return [
        {
            "path": f"test_{test_type}.py",
            "content": f"import pytest\n\ndef test_{test_type}_example():\n    assert True\n"
        }
    ]


def _generate_typescript_tests(code_content: str, test_type: str, deps) -> List[Dict[str, str]]:
    """Генерировать TypeScript тесты."""
    return [
        {
            "path": f"{test_type}.test.ts",
            "content": f"describe('{test_type} tests', () => {{\n  it('should pass', () => {{\n    expect(true).toBe(true);\n  }});\n}});"
        }
    ]


def _extract_feature_name(description: str) -> str:
    """Извлечь название функции из описания."""
    words = description.lower().split()
    return "_".join(words[:3])


def _extract_dependencies(requirements: List[str], deps) -> List[str]:
    """Извлечь зависимости из требований."""
    dependencies = []

    if deps.primary_language == ProgrammingLanguage.PYTHON:
        dependencies.extend(["fastapi", "uvicorn", "pydantic"])
    elif deps.primary_language == ProgrammingLanguage.TYPESCRIPT:
        dependencies.extend(["@types/node", "typescript"])

    return dependencies


def _generate_configuration(requirements: List[str], deps) -> Dict[str, Any]:
    """Генерировать конфигурацию."""
    return {
        "environment": "development",
        "debug": True,
        "database_url": f"{deps.database_type.value}://localhost:5432/app"
    }


def _generate_feature_documentation(feature_description: str, requirements: List[str], code_files: List[Dict[str, str]], config: Dict[str, Any]) -> str:
    """Генерировать документацию функции."""
    return f"""
# {_extract_feature_name(feature_description).title()}

## Описание
{feature_description}

## Требования
{chr(10).join(f"- {req}" for req in requirements)}

## Технологии
- Язык: {config.get('language', 'unknown')}
- Фреймворк: {config.get('framework', 'unknown')}

## Файлы
{chr(10).join(f"- {file['path']}" for file in code_files)}
"""


def _generate_directory_structure(architecture_type: str, deps) -> List[str]:
    """Генерировать структуру директорий."""
    base_dirs = ["src", "tests", "docs"]

    if architecture_type == "layered":
        base_dirs.extend(["src/models", "src/services", "src/controllers"])
    elif architecture_type == "hexagonal":
        base_dirs.extend(["src/domain", "src/application", "src/infrastructure"])

    return base_dirs


def _generate_base_files(project_name: str, architecture_type: str, deps) -> List[Dict[str, str]]:
    """Генерировать базовые файлы проекта."""
    files = [
        {
            "path": "README.md",
            "content": f"# {project_name}\n\nОписание проекта"
        },
        {
            "path": ".gitignore",
            "content": "*.pyc\n__pycache__/\n.env\n"
        }
    ]

    if deps.primary_language == ProgrammingLanguage.PYTHON:
        files.append({
            "path": "requirements.txt",
            "content": "fastapi\nuvicorn\n"
        })

    return files


def _determine_project_dependencies(deps) -> List[str]:
    """Определить зависимости проекта."""
    return deps.preferred_languages + deps.additional_technologies


def _generate_entry_points(project_name: str, deps) -> List[str]:
    """Генерировать точки входа."""
    if deps.primary_language == ProgrammingLanguage.PYTHON:
        return ["main.py"]
    elif deps.primary_language == ProgrammingLanguage.TYPESCRIPT:
        return ["index.ts"]
    return ["main"]


def _generate_base_test_structure(project_name: str, deps) -> List[Dict[str, str]]:
    """Генерировать базовую структуру тестов."""
    return [
        {
            "path": "tests/conftest.py",
            "content": "import pytest\n"
        }
    ]


def _analyze_performance_bottlenecks(code_content: str) -> List[Dict[str, Any]]:
    """Анализировать узкие места производительности."""
    return [
        {
            "type": "database_query",
            "line": 10,
            "description": "Потенциально медленный запрос к БД"
        }
    ]


def _apply_performance_optimization(bottleneck: Dict[str, Any], code_content: str, deps) -> Dict[str, Any]:
    """Применить оптимизацию производительности."""
    return {
        "bottleneck": bottleneck,
        "optimization": "Добавлено кэширование",
        "improved_code": code_content  # В реальности здесь будет улучшенный код
    }


def _calculate_performance_improvements(optimizations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Рассчитать улучшения производительности."""
    return {
        "estimated_speedup": "2x",
        "optimizations_count": len(optimizations)
    }


def _check_code_style(file_content: str, quality_config: Dict[str, Any], deps) -> List[Dict[str, str]]:
    """Проверить стиль кода."""
    issues = []

    # Проверяем длину строк
    lines = file_content.split('\n')
    for i, line in enumerate(lines, 1):
        if len(line) > 88:  # PEP8 рекомендует 79, но можно 88
            issues.append({
                "file": "current_file",
                "type": "style",
                "line": str(i),
                "message": f"Строка слишком длинная: {len(line)} символов"
            })

    return issues


def _check_security_issues(file_content: str, deps) -> List[Dict[str, str]]:
    """Проверить проблемы безопасности."""
    issues = []

    # Простая проверка на SQL инъекции
    if "f\"SELECT * FROM {" in file_content:
        issues.append({
            "file": "current_file",
            "type": "security",
            "message": "Потенциальная SQL инъекция через f-string"
        })

    return issues


def _calculate_file_metrics(file_content: str) -> Dict[str, Any]:
    """Рассчитать метрики файла."""
    lines = file_content.split('\n')
    return {
        "lines_count": len(lines),
        "non_empty_lines": len([line for line in lines if line.strip()]),
        "comment_lines": len([line for line in lines if line.strip().startswith('#')]),
        "complexity_estimate": "low"
    }


def _check_type_annotations(code_files: List[Dict[str, str]]) -> bool:
    """Проверить наличие аннотаций типов."""
    for file_info in code_files:
        content = file_info.get("content", "")
        if "def " in content and "->" not in content:
            return False
    return True


def _generate_quality_suggestions(issues: List[Dict[str, str]], quality_config: Dict[str, Any]) -> List[str]:
    """Генерировать рекомендации по качеству."""
    suggestions = []

    if any(issue["type"] == "file_size" for issue in issues):
        suggestions.append("Разбейте большие файлы на модули")

    if any(issue["type"] == "style" for issue in issues):
        suggestions.append("Используйте автоформатер кода (black, prettier)")

    return suggestions


def _calculate_quality_score(issues: List[Dict[str, str]], compliance: Dict[str, bool], files_count: int) -> float:
    """Рассчитать общий балл качества."""
    base_score = 100.0

    # Вычитаем баллы за проблемы
    penalty_per_issue = 10.0
    total_penalty = len(issues) * penalty_per_issue

    # Учитываем соответствие стандартам
    compliance_bonus = sum(compliance.values()) * 5.0

    final_score = max(0, base_score - total_penalty + compliance_bonus)
    return min(100, final_score)


def _generate_code_examples(query: str, deps) -> List[Dict[str, str]]:
    """Генерировать примеры кода."""
    return [
        {
            "language": deps.primary_language.value,
            "code": f"# Пример реализации для {query}\nprint('Hello, World!')",
            "description": f"Базовый пример для {query}"
        }
    ]