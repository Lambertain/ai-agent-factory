"""
NLP Program Generator Agent - Universal Transformation Program Creator

Мощный агент для создания персонализированных программ трансформации с использованием
PatternShift v2.0 методологии, интегрированной с NLP техниками и Эриксоновским гипнозом.
Поддерживает работу в любых доменах: психология, астрология, таро, нумерология.

Author: Implementation Engineer
Version: 1.0.0
"""

from .agent import (
    get_nlp_program_generator_agent,
    generate_personalized_program,
    create_nlp_technique_library,
    adapt_program_for_vak,
    generate_program_batch
)
from .dependencies import (
    NLPProgramGeneratorDependencies,
    ProgramDomain,
    SeverityLevel,
    VAKType,
    ContentFormat,
    NLPTechnique,
    EricksonianPattern,
    ProgramType
)
from .settings import load_settings
from .providers import ModelManager, TaskType

__version__ = "1.0.0"
__author__ = "Implementation Engineer"

__all__ = [
    "get_nlp_program_generator_agent",
    "generate_personalized_program",
    "create_nlp_technique_library",
    "adapt_program_for_vak",
    "generate_program_batch",
    "NLPProgramGeneratorDependencies",
    "ProgramDomain",
    "SeverityLevel",
    "VAKType",
    "ContentFormat",
    "NLPTechnique",
    "EricksonianPattern",
    "ProgramType",
    "load_settings",
    "ModelManager",
    "TaskType"
]