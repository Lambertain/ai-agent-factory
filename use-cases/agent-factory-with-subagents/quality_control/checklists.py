# -*- coding: utf-8 -*-
"""
Чеклисты для проверки качества при работе в роли Quality Guardian.

Это ДАННЫЕ для проверок, которые я (Claude) использую когда переключаюсь в роль Quality Guardian.
"""

# ============================================================================
# КРИТИЧЕСКИ ВАЖНО: Проверка переключения в роли
# ============================================================================

ROLE_SWITCHING_CHECKLIST = {
    "name": "Проверка переключения в роли",
    "priority": "BLOCKER",
    "items": [
        {
            "id": "role_announcement",
            "check": "Агент объявляет переключение в роль пользователю",
            "what_to_find": "━━━ ПЕРЕКЛЮЧАЮСЬ В РОЛЬ",
            "where": "В начале работы агента",
            "severity": "BLOCKER"
        },
        {
            "id": "expertise_shown",
            "check": "Показана экспертиза роли",
            "what_to_find": "📋 Моя экспертиза:",
            "where": "В объявлении переключения",
            "severity": "BLOCKER"
        },
        {
            "id": "todowrite_after_switch",
            "check": "TodoWrite СРАЗУ после переключения",
            "what_to_find": "TodoWrite вызов после объявления роли",
            "where": "Сразу после переключения в роль",
            "severity": "CRITICAL"
        },
        {
            "id": "microtasks_shown",
            "check": "Микрозадачи показаны пользователю",
            "what_to_find": "3-7 микрозадач в списке",
            "where": "После TodoWrite",
            "severity": "CRITICAL"
        }
    ]
}

# ============================================================================
# Проверка универсальности агентов
# ============================================================================

UNIVERSALITY_CHECKLIST = {
    "name": "Проверка универсальности",
    "priority": "BLOCKER",
    "forbidden_terms": [
        "unipark", "UniPark", "UNIPARK",
        "PatternShift", "patternshift",
        # Добавьте другие проект-специфичные термины
    ],
    "items": [
        {
            "id": "no_hardcoded_projects",
            "check": "0% упоминаний конкретных проектов",
            "what_to_find": "Hardcoded названия проектов",
            "where": "Весь код агента",
            "severity": "BLOCKER"
        },
        {
            "id": "examples_directory",
            "check": "Наличие examples/ с конфигурациями для разных доменов",
            "what_to_find": "examples/ директория с минимум 3 примерами",
            "where": "agents/[agent_name]/examples/",
            "severity": "MAJOR"
        },
        {
            "id": "configurable_dependencies",
            "check": "Зависимости конфигурируемы",
            "what_to_find": "domain_type, project_type в dependencies",
            "where": "dependencies.py",
            "severity": "MAJOR"
        }
    ]
}

# ============================================================================
# Проверка качества кода
# ============================================================================

CODE_QUALITY_CHECKLIST = {
    "name": "Проверка качества кода",
    "priority": "MAJOR",
    "items": [
        {
            "id": "file_size_limit",
            "check": "Файлы НЕ превышают 500 строк",
            "what_to_find": "Файлы > 500 строк",
            "where": "Все .py файлы",
            "severity": "MAJOR"
        },
        {
            "id": "docstrings",
            "check": "Все функции имеют docstrings",
            "what_to_find": 'def/async def без """',
            "where": "Все функции",
            "severity": "MINOR"
        },
        {
            "id": "type_hints",
            "check": "Использование type hints",
            "what_to_find": "Функции с параметрами без типов",
            "where": "Все функции",
            "severity": "MINOR"
        },
        {
            "id": "no_emojis_in_code",
            "check": "Нет эмодзи в Python коде",
            "what_to_find": "Unicode эмодзи в .py файлах",
            "where": "Весь Python код",
            "severity": "MINOR"
        }
    ]
}

# ============================================================================
# Проверка архитектуры
# ============================================================================

ARCHITECTURE_CHECKLIST = {
    "name": "Проверка архитектуры",
    "priority": "CRITICAL",
    "required_files": [
        "agent.py",
        "tools.py",
        "prompts.py",
        "dependencies.py",
        "__init__.py"
    ],
    "items": [
        {
            "id": "required_files_exist",
            "check": "Все обязательные файлы присутствуют",
            "what_to_find": "Отсутствующие файлы из required_files",
            "where": "agents/[agent_name]/",
            "severity": "CRITICAL"
        },
        {
            "id": "knowledge_directory",
            "check": "Наличие knowledge/ директории",
            "what_to_find": "knowledge/ директория",
            "where": "agents/[agent_name]/knowledge/",
            "severity": "MAJOR"
        },
        {
            "id": "pydantic_ai_structure",
            "check": "Структура соответствует Pydantic AI",
            "what_to_find": "Agent, RunContext, tools decorators",
            "where": "agent.py",
            "severity": "CRITICAL"
        }
    ]
}

# ============================================================================
# Проверка документации
# ============================================================================

DOCUMENTATION_CHECKLIST = {
    "name": "Проверка документации",
    "priority": "MAJOR",
    "items": [
        {
            "id": "readme_exists",
            "check": "Наличие README.md",
            "what_to_find": "README.md",
            "where": "agents/[agent_name]/",
            "severity": "MAJOR"
        },
        {
            "id": "usage_examples",
            "check": "Примеры использования в README",
            "what_to_find": "Секция с примерами кода",
            "where": "README.md",
            "severity": "MINOR"
        },
        {
            "id": "knowledge_base",
            "check": "База знаний агента",
            "what_to_find": "[agent_name]_knowledge.md",
            "where": "agents/[agent_name]/knowledge/",
            "severity": "MAJOR"
        }
    ]
}

# ============================================================================
# Проверка тестирования
# ============================================================================

TESTING_CHECKLIST = {
    "name": "Проверка тестирования",
    "priority": "MAJOR",
    "items": [
        {
            "id": "tests_directory",
            "check": "Наличие tests/ директории",
            "what_to_find": "tests/",
            "where": "agents/[agent_name]/tests/",
            "severity": "MAJOR"
        },
        {
            "id": "test_files",
            "check": "Тестовые файлы присутствуют",
            "what_to_find": "test_agent.py, test_tools.py",
            "where": "agents/[agent_name]/tests/",
            "severity": "MAJOR"
        }
    ]
}

# ============================================================================
# Полный чеклист для Quality Guardian
# ============================================================================

FULL_QUALITY_CHECKLIST = [
    ROLE_SWITCHING_CHECKLIST,
    UNIVERSALITY_CHECKLIST,
    CODE_QUALITY_CHECKLIST,
    ARCHITECTURE_CHECKLIST,
    DOCUMENTATION_CHECKLIST,
    TESTING_CHECKLIST
]
