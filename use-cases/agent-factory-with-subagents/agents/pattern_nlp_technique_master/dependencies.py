"""
Pattern NLP Technique Master Agent Dependencies

Зависимости для создания модульных НЛП-техник трансформации.
Поддерживает CBT, DBT, ACT и классические НЛП паттерны.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from .settings import load_settings


class NLPTechniqueType(str, Enum):
    """Типы НЛП техник."""
    ANCHORING = "anchoring"
    REFRAMING = "reframing"
    SWISH_PATTERN = "swish_pattern"
    TIMELINE_THERAPY = "timeline_therapy"
    SIX_STEP_REFRAMING = "six_step_reframing"
    PHOBIA_CURE = "phobia_cure"
    CHANGE_PERSONAL_HISTORY = "change_personal_history"
    DIGITAL_ANCHORING = "digital_anchoring"
    VIRTUAL_SWISH = "virtual_swish"


class TherapyModality(str, Enum):
    """Модальности терапии."""
    CBT = "cbt"  # Cognitive Behavioral Therapy
    DBT = "dbt"  # Dialectical Behavior Therapy
    ACT = "act"  # Acceptance and Commitment Therapy
    MINDFULNESS = "mindfulness"
    NLP_CLASSIC = "nlp_classic"


class ProblemArea(str, Enum):
    """Области психологических проблем."""
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    PHOBIAS = "phobias"
    TRAUMA = "trauma"
    RELATIONSHIPS = "relationships"
    SELF_ESTEEM = "self_esteem"
    ADDICTION = "addiction"
    EMOTIONAL_REGULATION = "emotional_regulation"
    LIMITING_BELIEFS = "limiting_beliefs"
    STRESS_MANAGEMENT = "stress_management"


class RepresentationalSystem(str, Enum):
    """Репрезентативные системы VAK."""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    MULTIMODAL = "multimodal"


class DifficultyLevel(str, Enum):
    """Уровни сложности техник."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class TechniqueFormat(str, Enum):
    """Форматы техник."""
    GUIDED_AUDIO = "guided_audio"
    TEXT_INSTRUCTIONS = "text_instructions"
    INTERACTIVE_SCRIPT = "interactive_script"
    VIDEO_DEMO = "video_demo"
    MIXED_MEDIA = "mixed_media"


@dataclass
class PatternNLPTechniqueMasterDependencies:
    """Зависимости для Pattern NLP Technique Master Agent."""

    # Основные настройки
    api_key: str
    project_path: str = ""

    # Агент информация
    agent_name: str = "pattern_nlp_technique_master"

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "pattern-nlp-technique-master", "agent-knowledge", "pydantic-ai",
        "nlp", "therapy", "psychology", "techniques"
    ])
    knowledge_domain: str | None = "patternshift.com"
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Конфигурация техник
    default_technique_type: NLPTechniqueType = NLPTechniqueType.REFRAMING
    default_therapy_modality: TherapyModality = TherapyModality.CBT
    default_problem_area: ProblemArea = ProblemArea.ANXIETY
    default_rep_system: RepresentationalSystem = RepresentationalSystem.MULTIMODAL
    default_difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    default_format: TechniqueFormat = TechniqueFormat.TEXT_INSTRUCTIONS

    # Персонализация
    user_profile: Dict[str, Any] = field(default_factory=dict)
    session_context: Dict[str, Any] = field(default_factory=dict)

    # Безопасность
    enable_safety_checks: bool = True
    contraindications_check: bool = True
    crisis_detection: bool = True

    # Настройки генерации
    technique_duration_minutes: int = 15
    include_preparation_steps: bool = True
    include_integration_steps: bool = True
    include_homework: bool = True

    # Научная валидация
    require_evidence_base: bool = True
    include_research_references: bool = True

    def __post_init__(self):
        """Инициализация после создания."""
        # Загружаем настройки
        settings = load_settings()

        # Обновляем путь проекта если не указан
        if not self.project_path:
            self.project_path = getattr(settings, 'project_path', '')


def create_technique_dependencies(
    technique_type: NLPTechniqueType,
    therapy_modality: TherapyModality,
    problem_area: ProblemArea,
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER,
    rep_system: RepresentationalSystem = RepresentationalSystem.MULTIMODAL,
    format_type: TechniqueFormat = TechniqueFormat.TEXT_INSTRUCTIONS,
    **kwargs
) -> PatternNLPTechniqueMasterDependencies:
    """
    Создать зависимости для конкретного типа техники.

    Args:
        technique_type: Тип НЛП техники
        therapy_modality: Модальность терапии
        problem_area: Область проблемы
        difficulty: Уровень сложности
        rep_system: Репрезентативная система
        format_type: Формат техники
        **kwargs: Дополнительные параметры

    Returns:
        Настроенные зависимости для агента
    """
    settings = load_settings()

    return PatternNLPTechniqueMasterDependencies(
        api_key=settings.llm_api_key,
        project_path=getattr(settings, 'project_path', ''),
        default_technique_type=technique_type,
        default_therapy_modality=therapy_modality,
        default_problem_area=problem_area,
        default_difficulty=difficulty,
        default_rep_system=rep_system,
        default_format=format_type,
        **kwargs
    )


def create_cbt_dependencies(**kwargs) -> PatternNLPTechniqueMasterDependencies:
    """Создать зависимости для CBT техник."""
    return create_technique_dependencies(
        technique_type=NLPTechniqueType.REFRAMING,
        therapy_modality=TherapyModality.CBT,
        problem_area=ProblemArea.ANXIETY,
        **kwargs
    )


def create_dbt_dependencies(**kwargs) -> PatternNLPTechniqueMasterDependencies:
    """Создать зависимости для DBT техник."""
    return create_technique_dependencies(
        technique_type=NLPTechniqueType.ANCHORING,
        therapy_modality=TherapyModality.DBT,
        problem_area=ProblemArea.EMOTIONAL_REGULATION,
        **kwargs
    )


def create_act_dependencies(**kwargs) -> PatternNLPTechniqueMasterDependencies:
    """Создать зависимости для ACT техник."""
    return create_technique_dependencies(
        technique_type=NLPTechniqueType.REFRAMING,
        therapy_modality=TherapyModality.ACT,
        problem_area=ProblemArea.LIMITING_BELIEFS,
        **kwargs
    )


def create_classic_nlp_dependencies(**kwargs) -> PatternNLPTechniqueMasterDependencies:
    """Создать зависимости для классических НЛП техник."""
    return create_technique_dependencies(
        technique_type=NLPTechniqueType.SWISH_PATTERN,
        therapy_modality=TherapyModality.NLP_CLASSIC,
        problem_area=ProblemArea.PHOBIAS,
        **kwargs
    )


def create_mindfulness_dependencies(**kwargs) -> PatternNLPTechniqueMasterDependencies:
    """Создать зависимости для майндфулнесс техник."""
    return create_technique_dependencies(
        technique_type=NLPTechniqueType.ANCHORING,
        therapy_modality=TherapyModality.MINDFULNESS,
        problem_area=ProblemArea.STRESS_MANAGEMENT,
        **kwargs
    )