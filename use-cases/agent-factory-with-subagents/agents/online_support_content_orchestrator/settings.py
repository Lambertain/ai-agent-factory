"""
Settings для Psychology Content Orchestrator Agent
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class ContentType(str, Enum):
    """Типы психологического контента"""
    THERAPEUTIC = "therapeutic"
    EDUCATIONAL = "educational"
    ASSESSMENT = "assessment"
    PREVENTIVE = "preventive"
    SUPPORT = "support"

class PsychologicalDomain(str, Enum):
    """Психологические домены"""
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    RELATIONSHIPS = "relationships"
    TRAUMA = "trauma"
    ADDICTION = "addiction"
    CHILD = "child"
    ADOLESCENT = "adolescent"
    FAMILY = "family"
    GENERAL = "general"

class ExpertiseLevel(str, Enum):
    """Уровни экспертизы"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    PROFESSIONAL = "professional"
    EXPERT = "expert"

class PsychologyContentSettings(BaseModel):
    """Настройки для создания психологического контента"""
    content_type: ContentType = ContentType.THERAPEUTIC
    target_domain: PsychologicalDomain = PsychologicalDomain.GENERAL
    expertise_level: ExpertiseLevel = ExpertiseLevel.PROFESSIONAL

    # Настройки аудитории
    target_age_range: Optional[str] = None
    cultural_context: Optional[str] = None
    language_preference: str = "russian"

    # Качественные параметры
    evidence_based: bool = True
    culturally_sensitive: bool = True
    safety_checked: bool = True

    # RAG настройки
    rag_match_count: int = Field(default=5, ge=1, le=20)
    search_domains: List[str] = Field(default_factory=lambda: ["psychology", "therapy"])

    class Config:
        use_enum_values = True

class ContentStructure(BaseModel):
    """Структура создаваемого контента"""
    title: str
    introduction: str
    main_sections: List[Dict[str, Any]]
    practical_exercises: List[str]
    resources: List[str]
    safety_notes: List[str]
    cultural_adaptations: Optional[Dict[str, Any]] = None

class QualityChecklist(BaseModel):
    """Чеклист для проверки качества контента"""
    scientific_validity: bool = False
    ethical_compliance: bool = False
    cultural_sensitivity: bool = False
    practical_applicability: bool = False
    safety_assessment: bool = False

    notes: Optional[str] = None
    recommendations: List[str] = Field(default_factory=list)

# Предустановленные конфигурации
PRESET_CONFIGS = {
    "anxiety_therapy": PsychologyContentSettings(
        content_type=ContentType.THERAPEUTIC,
        target_domain=PsychologicalDomain.ANXIETY,
        expertise_level=ExpertiseLevel.PROFESSIONAL,
        search_domains=["anxiety", "CBT", "mindfulness", "therapy"]
    ),

    "depression_education": PsychologyContentSettings(
        content_type=ContentType.EDUCATIONAL,
        target_domain=PsychologicalDomain.DEPRESSION,
        expertise_level=ExpertiseLevel.INTERMEDIATE,
        search_domains=["depression", "behavioral_activation", "psychoeducation"]
    ),

    "child_assessment": PsychologyContentSettings(
        content_type=ContentType.ASSESSMENT,
        target_domain=PsychologicalDomain.CHILD,
        expertise_level=ExpertiseLevel.PROFESSIONAL,
        target_age_range="6-12",
        search_domains=["child_psychology", "assessment", "development"]
    ),

    "family_support": PsychologyContentSettings(
        content_type=ContentType.SUPPORT,
        target_domain=PsychologicalDomain.FAMILY,
        expertise_level=ExpertiseLevel.BEGINNER,
        search_domains=["family_therapy", "support", "communication"]
    )
}

def get_preset_config(preset_name: str) -> Optional[PsychologyContentSettings]:
    """Получить предустановленную конфигурацию"""
    return PRESET_CONFIGS.get(preset_name)