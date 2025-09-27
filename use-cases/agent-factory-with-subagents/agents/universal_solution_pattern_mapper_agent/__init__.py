# -*- coding: utf-8 -*-
"""
Universal Solution Pattern Mapper Agent

Универсальный агент для маппинга решений и паттернов в различных доменах.
Поддерживает психологию, астрологию, нумерологию, бизнес и другие области.

Основные возможности:
- Маппинг решений для проблем в любых доменах
- Анализ соответствия проблемы и решения
- Генерация детальных чертежей решений
- Поиск и адаптация паттернов через RAG
- Валидация предложенных решений
- Коллективная работа с другими агентами

Примеры использования:

```python
from universal_solution_pattern_mapper_agent import run_solution_pattern_mapping

# Анализ решений для психологической платформы
result = await run_solution_pattern_mapping(
    message="Проанализируй архитектурные паттерны для платформы онлайн-терапии",
    domain_type="psychology",
    project_type="transformation_platform"
)

# Маппинг решений для астрологического сервиса
result = await run_solution_pattern_mapping(
    message="Создай архитектуру системы астрологических расчетов",
    domain_type="astrology",
    project_type="consultation_platform"
)

# Бизнес-решения для автоматизации
result = await run_solution_pattern_mapping(
    message="Спроектируй решения для автоматизации бизнес-процессов",
    domain_type="business",
    project_type="automation_platform"
)
```

Структура агента:
- agent.py - основной агент и точка входа
- dependencies.py - управление зависимостями и конфигурация домена
- tools.py - инструменты маппинга и анализа решений
- prompts.py - адаптивные промпты под разные домены
- providers.py - оптимизированная система выбора LLM моделей
- settings.py - конфигурируемые параметры через .env
"""

from .agent import (
    solution_pattern_mapper_agent,
    run_solution_pattern_mapping
)

from .dependencies import (
    SolutionPatternMapperDependencies,
    load_dependencies,
    AGENT_COMPETENCIES,
    AGENT_ASSIGNEE_MAP
)

from .settings import (
    SolutionPatternMapperSettings,
    DomainConfig,
    load_settings,
    create_domain_config,
    get_universal_settings_template
)

from .providers import (
    SolutionPatternMapperLLMProvider,
    ModelProvider,
    TaskComplexity,
    get_llm_model
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Universal Solution Pattern Mapper Agent для маппинга решений в любых доменах"

__all__ = [
    # Основные функции
    "solution_pattern_mapper_agent",
    "run_solution_pattern_mapping",

    # Зависимости и конфигурация
    "SolutionPatternMapperDependencies",
    "load_dependencies",
    "AGENT_COMPETENCIES",
    "AGENT_ASSIGNEE_MAP",

    # Настройки
    "SolutionPatternMapperSettings",
    "DomainConfig",
    "load_settings",
    "create_domain_config",
    "get_universal_settings_template",

    # Провайдеры LLM
    "SolutionPatternMapperLLMProvider",
    "ModelProvider",
    "TaskComplexity",
    "get_llm_model",

    # Метаданные
    "__version__",
    "__author__",
    "__description__"
]

# Информация для автоматического обнаружения агента
AGENT_INFO = {
    "name": "Universal Solution Pattern Mapper Agent",
    "type": "solution_pattern_mapper",
    "version": __version__,
    "description": __description__,
    "supported_domains": [
        "psychology",
        "astrology",
        "numerology",
        "business"
    ],
    "capabilities": [
        "solution_pattern_mapping",
        "problem_solution_analysis",
        "blueprint_generation",
        "pattern_knowledge_search",
        "solution_validation",
        "domain_adaptation",
        "collective_problem_solving"
    ],
    "required_env_vars": [
        "LLM_API_KEY"
    ],
    "optional_env_vars": [
        "DOMAIN_TYPE",
        "PROJECT_TYPE",
        "FRAMEWORK",
        "PATTERN_COMPLEXITY",
        "SOLUTION_SCOPE",
        "VALIDATION_LEVEL",
        "PRIMARY_LANGUAGE",
        "ARCHON_PROJECT_ID"
    ],
    "knowledge_base_tags": [
        "solution-patterns",
        "pattern-mapping",
        "agent-knowledge",
        "pydantic-ai"
    ],
    "delegation_targets": [
        "security_audit",
        "rag_agent",
        "uiux_enhancement",
        "performance_optimization"
    ]
}