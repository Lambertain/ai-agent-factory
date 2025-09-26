"""
NLP Content Research Agent - Universal Professional Researcher with NLP Specialization

A powerful agent that combines professional research capabilities with NLP expertise
to create viral content using PatternShift v2.0 methodology. Works universally across
domains including psychology, astrology, tarot, numerology and others.

Author: Implementation Engineer
Version: 1.0.0
"""

from .agent import get_nlp_content_research_agent
from .dependencies import (
    NLPContentResearchDependencies,
    ResearchDomain,
    NLPTechnique,
    AudienceType
)
from .settings import load_settings
from .providers import ModelManager, TaskType

__version__ = "1.0.0"
__author__ = "Implementation Engineer"

__all__ = [
    "get_nlp_content_research_agent",
    "NLPContentResearchDependencies",
    "ResearchDomain",
    "NLPTechnique",
    "AudienceType",
    "load_settings",
    "ModelManager",
    "TaskType"
]