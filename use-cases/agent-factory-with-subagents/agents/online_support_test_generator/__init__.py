"""
Psychology Test Generator Agent - универсальный агент для создания психологических тестов и диагностик

Этот агент специализируется на создании научно обоснованных психологических тестов,
опросников и диагностических инструментов с поддержкой психометрической валидации
и адаптации под различные популяции.

Основные возможности:
- Генерация психологических тестов для различных доменов
- Создание валидных психометрических инструментов
- Адаптация тестов под целевые популяции
- Психометрическая валидация и анализ
- Интеграция с мультиагентной системой психологических агентов

Автор: AI Agent Factory
Версия: 1.0.0
"""

from .agent import (
    psychology_test_generator_agent,
    create_psychological_test,
    create_test_battery,
    adapt_test_for_population,
    TestGenerationRequest,
    TestBatteryRequest,
    PopulationAdaptationRequest
)

from .dependencies import (
    TestGeneratorDependencies,
    get_test_generator_config
)

from .settings import (
    PsychologyTestGeneratorSettings,
    load_settings,
    get_llm_model,
    get_domain_specific_settings,
    get_population_specific_settings,
    DEFAULT_RESPONSE_FORMATS,
    PSYCHOMETRIC_STANDARDS
)

from .tools import (
    generate_test_questions,
    create_scoring_system,
    validate_test_content,
    analyze_psychometric_properties,
    adapt_for_population,
    create_test_battery,
    search_psychology_knowledge,
    delegate_to_research_agent,
    delegate_to_quality_guardian,
    generate_test_report
)

from .prompts import (
    get_system_prompt,
    get_domain_prompts,
    get_population_prompts,
    get_validation_prompts,
    DOMAIN_SPECIFIC_PROMPTS,
    POPULATION_ADAPTED_PROMPTS,
    ETHICAL_GUIDELINES_PROMPTS
)

# Версия агента
__version__ = "1.0.0"

# Информация об агенте
__agent_info__ = {
    "name": "Psychology Test Generator Agent",
    "description": "Универсальный агент для создания психологических тестов и диагностик",
    "version": __version__,
    "author": "AI Agent Factory",
    "capabilities": [
        "Генерация психологических тестов",
        "Психометрическая валидация",
        "Адаптация под популяции",
        "Создание тестовых батарей",
        "Научное обоснование методик",
        "Этическая оценка тестов"
    ],
    "supported_domains": [
        "anxiety", "depression", "trauma", "personality", "stress",
        "relationships", "cognitive", "behavioral", "general"
    ],
    "supported_populations": [
        "children", "adolescents", "adults", "elderly", "special_needs"
    ],
    "integration": {
        "archon_project_id": "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        "knowledge_tags": ["psychology-test-generation", "psychometrics", "test-validation"],
        "collaborates_with": [
            "Psychology Research Agent",
            "Psychology Content Architect",
            "Psychology Quality Guardian"
        ]
    }
}

# Экспорт основных компонентов
__all__ = [
    # Основной агент и функции
    "psychology_test_generator_agent",
    "create_psychological_test",
    "create_test_battery",
    "adapt_test_for_population",

    # Типы данных
    "TestGenerationRequest",
    "TestBatteryRequest",
    "PopulationAdaptationRequest",

    # Конфигурация и зависимости
    "TestGeneratorDependencies",
    "get_test_generator_config",
    "PsychologyTestGeneratorSettings",
    "load_settings",
    "get_llm_model",

    # Инструменты
    "generate_test_questions",
    "create_scoring_system",
    "validate_test_content",
    "analyze_psychometric_properties",
    "adapt_for_population",
    "search_psychology_knowledge",

    # Промпты
    "get_system_prompt",
    "get_domain_prompts",
    "get_population_prompts",
    "get_validation_prompts",

    # Константы
    "DEFAULT_RESPONSE_FORMATS",
    "PSYCHOMETRIC_STANDARDS",
    "DOMAIN_SPECIFIC_PROMPTS",
    "POPULATION_ADAPTED_PROMPTS",

    # Метаинформация
    "__version__",
    "__agent_info__"
]


def get_agent_info():
    """
    Получить информацию об агенте.

    Returns:
        dict: Подробная информация об агенте
    """
    return __agent_info__


def quick_start_example():
    """
    Пример быстрого запуска агента.

    Returns:
        str: Пример кода для использования агента
    """
    return '''
# Пример использования Psychology Test Generator Agent

from psychology_test_generator import (
    psychology_test_generator_agent,
    TestGenerationRequest,
    TestGeneratorDependencies,
    load_settings
)

# Загрузка настроек
settings = load_settings()

# Создание зависимостей
deps = TestGeneratorDependencies(
    api_key=settings.llm_api_key,
    psychological_domain="anxiety",
    target_population="adults",
    test_type="assessment"
)

# Создание запроса на генерацию теста
request = TestGenerationRequest(
    domain="anxiety",
    population="adults",
    purpose="screening",
    question_count=15,
    response_format="frequency"
)

# Генерация теста
async def generate_test():
    result = await psychology_test_generator_agent.run(
        user_prompt=f"Создай тест для скрининга тревожности: {request.model_dump_json()}",
        deps=deps
    )
    return result.data

# Запуск генерации
# test_result = asyncio.run(generate_test())
'''


def get_available_domains():
    """
    Получить список доступных психологических доменов.

    Returns:
        list: Список поддерживаемых доменов
    """
    return __agent_info__["supported_domains"]


def get_available_populations():
    """
    Получить список доступных целевых популяций.

    Returns:
        list: Список поддерживаемых популяций
    """
    return __agent_info__["supported_populations"]


def validate_domain(domain: str) -> bool:
    """
    Проверить поддержку психологического домена.

    Args:
        domain: Название домена

    Returns:
        bool: True если домен поддерживается
    """
    return domain in get_available_domains()


def validate_population(population: str) -> bool:
    """
    Проверить поддержку целевой популяции.

    Args:
        population: Название популяции

    Returns:
        bool: True если популяция поддерживается
    """
    return population in get_available_populations()


def get_integration_info():
    """
    Получить информацию об интеграции с другими агентами.

    Returns:
        dict: Информация об интеграции
    """
    return __agent_info__["integration"]


# Настройка логирования для агента
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Обработчик для консольного вывода
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Формат логов
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)

# Добавление обработчика
if not logger.handlers:
    logger.addHandler(console_handler)

logger.info(f"Psychology Test Generator Agent v{__version__} initialized")