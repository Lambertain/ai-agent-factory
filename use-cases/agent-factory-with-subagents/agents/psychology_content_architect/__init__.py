"""
Psychology Content Architect Agent
Агент для создания психологических тестов по методологии PatternShift

4-уровневая система создания тестов:
1. Research - Погружение в тему
2. Draft - Создание черновика
3. Analysis - Рефлексия и улучшение
4. Finalization - Итоговый тест
"""

from .agent import (
    psychology_content_architect,
    create_psychological_test,
    adapt_existing_test,
    validate_test_methodology
)
from .dependencies import ContentArchitectDependencies, get_content_config
from .settings import ContentArchitectSettings, load_content_settings
from .tools import (
    research_test_topic,
    create_test_draft,
    analyze_and_improve_test,
    finalize_test_content,
    adapt_test_for_vak,
    validate_test_structure
)

__all__ = [
    "psychology_content_architect",
    "create_psychological_test",
    "adapt_existing_test",
    "validate_test_methodology",
    "ContentArchitectDependencies",
    "get_content_config",
    "ContentArchitectSettings",
    "load_content_settings",
    "research_test_topic",
    "create_test_draft",
    "analyze_and_improve_test",
    "finalize_test_content",
    "adapt_test_for_vak",
    "validate_test_structure"
]

__version__ = "1.0.0"
__description__ = "Psychology Content Architect Agent для создания психологических тестов"