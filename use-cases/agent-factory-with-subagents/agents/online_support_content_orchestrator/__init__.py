"""
Psychology Content Orchestrator Agent
Универсальный агент для координации создания психологического контента
"""

from .agent import psychology_orchestrator, coordinate_psychology_content
from .settings import (
    PsychologyContentSettings,
    ContentType,
    PsychologicalDomain,
    ExpertiseLevel,
    PRESET_CONFIGS,
    get_preset_config
)
from .dependencies import RAGConfig, PsychologyKnowledge, ContentCreationRequest

__all__ = [
    'psychology_orchestrator',
    'coordinate_psychology_content',
    'PsychologyContentSettings',
    'ContentType',
    'PsychologicalDomain',
    'ExpertiseLevel',
    'PRESET_CONFIGS',
    'get_preset_config',
    'RAGConfig',
    'PsychologyKnowledge',
    'ContentCreationRequest'
]

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__description__ = "Универсальный агент для координации создания психологического контента"