"""
Pattern Test Architect Agent - Эксперт по созданию психологических тестов

Этот агент специализируется на:
- Адаптации научно валидированных методик в доступные инструменты
- Создании вирусных тестов с сохранением диагностической ценности
- Трансформации сложных психологических конструктов в простые вопросы
- Написании расшифровок результатов для самопознания и изменений
"""

from .agent import agent, run_pattern_test_architect, create_psychological_test
from .models import (
    TestRequest,
    TestResponse,
    TestQuestion,
    TestResult,
    PsychometricValidation,
    ViralTestTransformation,
    InterpretationScale,
    EffectivenessAnalysis,
    PsychologicalConstruct,
    TargetAudience,
    DifficultyLevel,
    QuestionType
)
from .tools import (
    validate_psychometric_properties,
    transform_academic_to_viral,
    generate_test_questions,
    create_interpretation_scales,
    analyze_test_effectiveness
)
from .dependencies import PatternTestArchitectDependencies, dependencies
from .prompts import PatternTestArchitectPrompts
from .settings import PatternTestArchitectSettings, settings

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Pattern Test Architect Agent для создания психологических тестов"

# Экспорт основных компонентов
__all__ = [
    # Основной агент
    "agent",
    "run_pattern_test_architect",
    "create_psychological_test",

    # Модели данных
    "TestRequest",
    "TestResponse",
    "TestQuestion",
    "TestResult",
    "PsychometricValidation",
    "ViralTestTransformation",
    "InterpretationScale",
    "EffectivenessAnalysis",
    "PsychologicalConstruct",
    "TargetAudience",
    "DifficultyLevel",
    "QuestionType",

    # Инструменты
    "validate_psychometric_properties",
    "transform_academic_to_viral",
    "generate_test_questions",
    "create_interpretation_scales",
    "analyze_test_effectiveness",

    # Зависимости
    "PatternTestArchitectDependencies",
    "dependencies",

    # Промпты
    "PatternTestArchitectPrompts",

    # Настройки
    "PatternTestArchitectSettings",
    "settings"
]

# Метаданные агента
AGENT_METADATA = {
    "name": "Pattern Test Architect",
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "tags": [
        "psychology",
        "psychometrics",
        "test_creation",
        "viral_content",
        "assessment",
        "transformation"
    ],
    "capabilities": [
        "Создание психологических тестов",
        "Валидация психометрических свойств",
        "Вирусная трансформация названий",
        "Генерация вопросов для тестов",
        "Создание интерпретаций результатов",
        "Анализ эффективности тестов",
        "Этическая валидация контента",
        "Культурная адаптация тестов"
    ],
    "requirements": [
        "pydantic",
        "pydantic-ai",
        "typing_extensions"
    ],
    "supported_constructs": [
        "depression",
        "anxiety",
        "stress",
        "self_esteem",
        "personality_big5",
        "attachment_style",
        "communication_style",
        "love_languages",
        "ego_states",
        "codependency",
        "drama_triangle",
        "emotional_intelligence",
        "perfectionism",
        "procrastination",
        "assertiveness",
        "stress_management"
    ],
    "supported_audiences": [
        "general",
        "teens",
        "young_adults",
        "adults",
        "mature",
        "professionals",
        "students"
    ]
}