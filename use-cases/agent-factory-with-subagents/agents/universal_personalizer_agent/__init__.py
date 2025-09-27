# -*- coding: utf-8 -*-
"""
Universal Personalizer Agent

Универсальный агент для персонализации контента и пользовательского опыта
в различных доменах: психология, астрология, нумерология, бизнес и другие области.

Основные возможности:
- Анализ профиля пользователя для персонализации
- Генерация персонализированного контента
- Создание правил персонализации
- Адаптация контента под конкретного пользователя
- Отслеживание эффективности персонализации
- Оптимизация пользовательского опыта
- Коллективная работа с другими агентами

Примеры использования:

```python
from universal_personalizer_agent import run_personalization_task

# Персонализация для психологической платформы
result = await run_personalization_task(
    message="Создай персонализированную терапевтическую программу для пользователя с тревожностью",
    domain_type="psychology",
    project_type="transformation_platform",
    personalization_mode="adaptive"
)

# Персонализация для астрологического сервиса
result = await run_personalization_task(
    message="Персонализируй астрологические интерпретации под культурный контекст пользователя",
    domain_type="astrology",
    project_type="consultation_platform",
    personalization_mode="hybrid"
)

# Персонализация для бизнес-платформы
result = await run_personalization_task(
    message="Адаптируй бизнес-рекомендации под роль и индустрию пользователя",
    domain_type="business",
    project_type="analytics_platform",
    personalization_mode="ml_driven"
)
```

Структура агента:
- agent.py - основной агент и точки входа
- dependencies.py - управление зависимостями и конфигурация домена
- tools.py - инструменты персонализации и анализа
- prompts.py - адаптивные промпты под разные домены
- providers.py - оптимизированная система выбора LLM моделей
- settings.py - конфигурируемые параметры через .env
"""

from .agent import (
    personalizer_agent,
    run_personalization_task,
    run_user_profile_analysis,
    run_content_personalization,
    run_ux_optimization
)

from .dependencies import (
    PersonalizerDependencies,
    load_dependencies,
    AGENT_COMPETENCIES,
    AGENT_ASSIGNEE_MAP
)

from .settings import (
    PersonalizerSettings,
    PersonalizationConfig,
    load_settings,
    create_personalization_config,
    get_universal_settings_template
)

from .providers import (
    PersonalizerLLMProvider,
    ModelProvider,
    PersonalizationComplexity,
    get_llm_model
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Universal Personalizer Agent для персонализации контента и UX в любых доменах"

__all__ = [
    # Основные функции
    "personalizer_agent",
    "run_personalization_task",
    "run_user_profile_analysis",
    "run_content_personalization",
    "run_ux_optimization",

    # Зависимости и конфигурация
    "PersonalizerDependencies",
    "load_dependencies",
    "AGENT_COMPETENCIES",
    "AGENT_ASSIGNEE_MAP",

    # Настройки
    "PersonalizerSettings",
    "PersonalizationConfig",
    "load_settings",
    "create_personalization_config",
    "get_universal_settings_template",

    # Провайдеры LLM
    "PersonalizerLLMProvider",
    "ModelProvider",
    "PersonalizationComplexity",
    "get_llm_model",

    # Метаданные
    "__version__",
    "__author__",
    "__description__"
]

# Информация для автоматического обнаружения агента
AGENT_INFO = {
    "name": "Universal Personalizer Agent",
    "type": "personalizer",
    "version": __version__,
    "description": __description__,
    "supported_domains": [
        "psychology",
        "astrology",
        "numerology",
        "business"
    ],
    "capabilities": [
        "user_profile_analysis",
        "personalized_content_generation",
        "personalization_rules_creation",
        "content_adaptation",
        "ux_optimization",
        "effectiveness_tracking",
        "quality_validation",
        "collective_problem_solving"
    ],
    "personalization_modes": [
        "adaptive",
        "rule_based",
        "ml_driven",
        "hybrid"
    ],
    "required_env_vars": [
        "LLM_API_KEY"
    ],
    "optional_env_vars": [
        "DOMAIN_TYPE",
        "PROJECT_TYPE",
        "FRAMEWORK",
        "PERSONALIZATION_MODE",
        "PERSONALIZATION_DEPTH",
        "ADAPTATION_STRATEGY",
        "LEARNING_APPROACH",
        "PRIMARY_LANGUAGE",
        "ARCHON_PROJECT_ID"
    ],
    "knowledge_base_tags": [
        "personalization",
        "user-experience",
        "agent-knowledge",
        "pydantic-ai"
    ],
    "delegation_targets": [
        "security_audit",
        "rag_agent",
        "uiux_enhancement",
        "performance_optimization"
    ],
    "algorithms": [
        "collaborative_filtering",
        "content_based_filtering",
        "hybrid_recommendations",
        "behavioral_analysis",
        "cultural_adaptation",
        "real_time_optimization"
    ]
}