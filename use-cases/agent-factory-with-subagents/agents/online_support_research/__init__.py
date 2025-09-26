"""
Psychology Research Agent

Универсальный агент для научного обоснования психологических методик.
Специализируется на систематическом обзоре литературы, мета-анализе
и оценке доказательной базы психологических интервенций.
"""

from .agent import (
    psychology_researcher,
    conduct_evidence_review,
    quick_literature_search,
    determine_question_type,
    determine_evidence_level,
    determine_recommendation_grade
)
from .dependencies import (
    ResearchDependencies,
    get_research_config
)
from .tools import (
    search_literature,
    analyze_evidence_quality,
    synthesize_research_findings,
    assess_clinical_significance,
    evaluate_safety_profile,
    generate_recommendations
)
from .prompts import (
    get_research_prompt,
    get_domain_specific_prompt,
    get_evidence_standard_prompt,
    get_population_prompt,
    get_search_strategy_prompt,
    get_summary_prompt,
    get_crisis_safety_prompt
)
from .settings import (
    ResearchSettings,
    ResearchDomain,
    TargetPopulation,
    EvidenceStandard,
    ResearchQuestionType,
    StudyType,
    RESEARCH_PRESETS,
    get_research_preset,
    list_available_presets,
    get_preset_info,
    create_domain_specific_settings
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Universal Psychology Research Agent for Evidence-Based Practice"

# Основные функции для экспорта
__all__ = [
    # Главный агент и функции
    "psychology_researcher",
    "conduct_evidence_review",
    "quick_literature_search",
    "determine_question_type",
    "determine_evidence_level",
    "determine_recommendation_grade",

    # Зависимости и конфигурация
    "ResearchDependencies",
    "get_research_config",

    # Инструменты исследования
    "search_literature",
    "analyze_evidence_quality",
    "synthesize_research_findings",
    "assess_clinical_significance",
    "evaluate_safety_profile",
    "generate_recommendations",

    # Промпты и шаблоны
    "get_research_prompt",
    "get_domain_specific_prompt",
    "get_evidence_standard_prompt",
    "get_population_prompt",
    "get_search_strategy_prompt",
    "get_summary_prompt",
    "get_crisis_safety_prompt",

    # Настройки и енумы
    "ResearchSettings",
    "ResearchDomain",
    "TargetPopulation",
    "EvidenceStandard",
    "ResearchQuestionType",
    "StudyType",
    "RESEARCH_PRESETS",
    "get_research_preset",
    "list_available_presets",
    "get_preset_info",
    "create_domain_specific_settings"
]

# Метаинформация об агенте
AGENT_INFO = {
    "name": "Psychology Research Agent",
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "specialization": "Научное обоснование психологических методик",
    "evidence_standards": [
        "low", "moderate", "high", "expert"
    ],
    "supported_domains": [
        "anxiety", "depression", "trauma", "relationships",
        "addiction", "stress", "grief", "parenting", "general"
    ],
    "supported_populations": [
        "adults", "adolescents", "children", "elderly",
        "couples", "families", "groups"
    ],
    "research_capabilities": [
        "Систематический обзор литературы",
        "Мета-анализ эффективности",
        "Оценка качества исследований",
        "Анализ клинической значимости",
        "Профиль безопасности",
        "Градуированные рекомендации"
    ],
    "databases_supported": [
        "PubMed", "PsycINFO", "Cochrane Library",
        "EMBASE", "Web of Science"
    ],
    "quality_tools": [
        "Cochrane Risk of Bias",
        "JADAD Scale",
        "Newcastle-Ottawa Scale",
        "GRADE Assessment"
    ],
    "output_formats": [
        "Structured research reports",
        "Clinical recommendations",
        "Evidence summaries",
        "Safety profiles"
    ]
}

def get_agent_info() -> dict:
    """Получить информацию об агенте"""
    return AGENT_INFO.copy()

def get_quick_start_guide() -> str:
    """Получить краткое руководство по использованию"""
    return """
    Psychology Research Agent - Быстрый старт

    1. Базовое использование:
       ```python
       from psychology_research import conduct_evidence_review

       result = await conduct_evidence_review(
           research_question="Эффективность КПТ при генерализованной тревожности",
           research_domain="anxiety",
           target_population="adults",
           evidence_standard="high"
       )
       ```

    2. Быстрый поиск литературы:
       ```python
       from psychology_research import quick_literature_search

       result = await quick_literature_search(
           topic="mindfulness depression",
           domain="depression",
           max_studies=15
       )
       ```

    3. С предустановленной конфигурацией:
       ```python
       from psychology_research import get_research_preset

       settings = get_research_preset("anxiety_adults_high")
       # Использовать settings для кастомизации
       ```

    4. Кастомная настройка:
       ```python
       from psychology_research import create_domain_specific_settings

       settings = create_domain_specific_settings(
           domain="trauma",
           population="adults",
           evidence_level="expert"
       )
       ```

    5. Использование инструментов напрямую:
       ```python
       from psychology_research import search_literature, analyze_evidence_quality

       # Поиск литературы
       search_results = await search_literature(
           ctx, "CBT anxiety effectiveness", ["pubmed", "psycinfo"]
       )

       # Анализ качества
       quality_analysis = await analyze_evidence_quality(
           ctx, search_results["studies"]
       )
       ```

    Поддерживаемые домены:
    - anxiety (тревожные расстройства)
    - depression (депрессивные расстройства)
    - trauma (травма и ПТСР)
    - relationships (семейная и парная терапия)
    - addiction (зависимости)
    - stress (стрессовые расстройства)
    - grief (горе и утрата)
    - parenting (родительство)

    Популяции:
    - adults (взрослые 18-65)
    - adolescents (подростки 12-18)
    - children (дети 6-12)
    - elderly (пожилые 65+)
    - couples (пары)
    - families (семьи)

    Стандарты доказательности:
    - low: пилотные исследования, case studies
    - moderate: контролируемые исследования
    - high: только высококачественные РКИ
    - expert: мета-анализы и систематические обзоры
    """

def get_research_workflow() -> str:
    """Получить описание рабочего процесса исследования"""
    return """
    Рабочий процесс Psychology Research Agent:

    1. ПОИСК ЛИТЕРАТУРЫ
       - Систематический поиск в базах данных
       - Применение критериев включения/исключения
       - Извлечение библиографических данных

    2. ОЦЕНКА КАЧЕСТВА
       - Применение инструментов оценки качества
       - Градация исследований по уровню доказательности
       - Исключение низкокачественных исследований

    3. СИНТЕЗ ДОКАЗАТЕЛЬСТВ
       - Мета-анализ количественных данных
       - Оценка гетерогенности между исследованиями
       - Анализ систематических ошибок публикации

    4. КЛИНИЧЕСКАЯ ЗНАЧИМОСТЬ
       - Расчет размеров эффекта
       - Определение минимальной клинически важной разности
       - Оценка числа пациентов для лечения (NNT)

    5. ПРОФИЛЬ БЕЗОПАСНОСТИ
       - Анализ нежелательных явлений
       - Оценка переносимости и отсева
       - Идентификация противопоказаний

    6. РЕКОМЕНДАЦИИ
       - Градуированные рекомендации по силе доказательств
       - Практические рекомендации для клиницистов
       - Направления будущих исследований

    Результат: Комплексный научно-обоснованный отчет с рекомендациями
    """

# Проверка совместимости при импорте
def _check_dependencies():
    """Проверка необходимых зависимостей"""
    try:
        import pydantic_ai
        import dataclasses
        from typing import Dict, List, Optional
        return True
    except ImportError as e:
        print(f"Warning: Missing dependency - {e}")
        return False

# Автоматическая проверка при импорте
_dependencies_ok = _check_dependencies()

if not _dependencies_ok:
    print("Warning: Some dependencies are missing. Some features may not work correctly.")

# Примеры использования для документации
USAGE_EXAMPLES = {
    "anxiety_research": {
        "description": "Исследование эффективности КПТ при тревожности",
        "code": """
result = await conduct_evidence_review(
    research_question="Эффективность когнитивно-поведенческой терапии при генерализованном тревожном расстройстве",
    research_domain="anxiety",
    target_population="adults",
    evidence_standard="high",
    intervention_type="psychotherapy"
)
        """
    },
    "depression_meta_analysis": {
        "description": "Мета-анализ антидепрессантов и психотерапии",
        "code": """
settings = create_domain_specific_settings("depression", "adults", "expert")
result = await conduct_evidence_review(
    research_question="Сравнительная эффективность антидепрессантов и психотерапии",
    research_domain="depression",
    evidence_standard="expert",
    research_question_type="comparison"
)
        """
    },
    "trauma_safety": {
        "description": "Оценка безопасности EMDR терапии",
        "code": """
result = await conduct_evidence_review(
    research_question="Профиль безопасности EMDR терапии при ПТСР",
    research_domain="trauma",
    target_population="adults",
    evidence_standard="high",
    research_question_type="safety"
)
        """
    }
}

def get_usage_examples() -> dict:
    """Получить примеры использования агента"""
    return USAGE_EXAMPLES.copy()