"""
NLP Program Generator Agent Dependencies

Универсальные зависимости для создания персонализированных программ трансформации
с поддержкой PatternShift методологии, NLP техник и Эриксоновского гипноза.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime


class ProgramDomain(str, Enum):
    """Домены для программ трансформации."""
    PSYCHOLOGY = "psychology"
    ASTROLOGY = "astrology"
    TAROT = "tarot"
    NUMEROLOGY = "numerology"
    WELLNESS = "wellness"
    BUSINESS = "business"
    RELATIONSHIPS = "relationships"


class SeverityLevel(str, Enum):
    """Уровни сложности проблем."""
    SEVERE = "severe"        # Кризис - 21 день
    MODERATE = "moderate"    # Стабилизация - 21 день
    MILD = "mild"           # Восстановление - 14 дней
    MINIMAL = "minimal"     # Профилактика - 7 дней


class VAKType(str, Enum):
    """Типы восприятия информации."""
    VISUAL = "visual"           # Образы, визуализации
    AUDITORY = "auditory"       # Звуки, диалоги
    KINESTHETIC = "kinesthetic" # Ощущения, движения
    MIXED = "mixed"            # Смешанный тип


class ContentFormat(str, Enum):
    """Форматы контента программы."""
    TEXT = "text"           # Текстовая версия
    AUDIO = "audio"         # Аудио версия
    BOTH = "both"          # Обе версии
    INTERACTIVE = "interactive"  # Интерактивная версия


class NLPTechnique(str, Enum):
    """NLP техники для программ."""
    ANCHORING = "anchoring"             # Анкоринг
    SUBMODALITIES = "submodalities"     # Субмодальности
    REFRAMING = "reframing"             # Рефрейминг
    TIMELINE = "timeline"               # Временные линии
    SWISH_PATTERN = "swish_pattern"     # Свиш паттерн
    PARTS_INTEGRATION = "parts_integration"  # Интеграция частей
    META_MODEL = "meta_model"           # Мета-модель
    MILTON_MODEL = "milton_model"       # Модель Милтона


class EricksonianPattern(str, Enum):
    """Эриксоновские паттерны воздействия."""
    TRUISMS = "truisms"                 # Трюизмы
    PRESUPPOSITIONS = "presuppositions" # Пресуппозиции
    EMBEDDED_COMMANDS = "embedded_commands"  # Встроенные команды
    DOUBLE_BINDS = "double_binds"       # Двойные связки
    ANALOGICAL_MARKING = "analogical_marking"  # Аналоговое маркирование
    CONFUSION_TECHNIQUE = "confusion_technique"  # Техника замешательства


class ProgramType(str, Enum):
    """Типы программ трансформации."""
    CRISIS_INTERVENTION = "crisis_intervention"     # Кризисное вмешательство
    EMOTIONAL_REGULATION = "emotional_regulation"   # Регуляция эмоций
    CONFIDENCE_BUILDING = "confidence_building"     # Повышение уверенности
    RELATIONSHIP_HEALING = "relationship_healing"   # Исцеление отношений
    GOAL_ACHIEVEMENT = "goal_achievement"          # Достижение целей
    STRESS_MANAGEMENT = "stress_management"        # Управление стрессом
    ADDICTION_RECOVERY = "addiction_recovery"      # Преодоление зависимостей
    TRAUMA_HEALING = "trauma_healing"              # Исцеление травм


@dataclass
class NLPProgramGeneratorDependencies:
    """Зависимости NLP Program Generator Agent."""

    # Основные настройки
    api_key: str
    project_path: str = ""
    domain: ProgramDomain = ProgramDomain.PSYCHOLOGY

    # Настройки программы
    severity_level: SeverityLevel = SeverityLevel.MODERATE
    vak_type: VAKType = VAKType.MIXED
    content_format: ContentFormat = ContentFormat.BOTH
    program_type: ProgramType = ProgramType.EMOTIONAL_REGULATION

    # NLP конфигурация
    nlp_techniques: List[NLPTechnique] = field(default_factory=lambda: [
        NLPTechnique.ANCHORING,
        NLPTechnique.REFRAMING,
        NLPTechnique.SUBMODALITIES
    ])
    ericksonian_patterns: List[EricksonianPattern] = field(default_factory=lambda: [
        EricksonianPattern.TRUISMS,
        EricksonianPattern.PRESUPPOSITIONS,
        EricksonianPattern.EMBEDDED_COMMANDS
    ])

    # Персонализация
    age_range: str = "25-45"
    gender: Optional[str] = None
    preferred_language: str = "ru"
    daily_time_limit: int = 30  # минут

    # Технические параметры
    enable_pattern_shift: bool = True
    use_hypnotic_language: bool = True
    include_audio_scripts: bool = True
    modular_structure: bool = True
    max_lines_per_module: int = 300

    # RAG и поиск
    agent_name: str = "nlp_program_generator"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "nlp-program-generator", "agent-knowledge", "pydantic-ai",
        "transformation-programs", "nlp-techniques", "ericksonian-hypnosis",
        "pattern-shift", "personalization", "vak-adaptation"
    ])
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Интеграция с другими агентами
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"
    research_agent_integration: bool = True
    quality_control_enabled: bool = True

    def __post_init__(self):
        """Инициализация после создания объекта."""
        if not self.knowledge_domain:
            self.knowledge_domain = f"docs.{self.domain.value}.programs"

        # Адаптация техник под домен
        if self.domain == ProgramDomain.ASTROLOGY:
            self.knowledge_tags.extend([
                "astrology-programs", "cosmic-healing", "planetary-influence"
            ])
        elif self.domain == ProgramDomain.TAROT:
            self.knowledge_tags.extend([
                "tarot-therapy", "archetypal-healing", "symbolic-transformation"
            ])
        elif self.domain == ProgramDomain.NUMEROLOGY:
            self.knowledge_tags.extend([
                "numerology-programs", "number-psychology", "vibration-healing"
            ])

    def get_program_duration(self) -> int:
        """Получить продолжительность программы в днях."""
        duration_map = {
            SeverityLevel.SEVERE: 21,
            SeverityLevel.MODERATE: 21,
            SeverityLevel.MILD: 14,
            SeverityLevel.MINIMAL: 7
        }
        return duration_map[self.severity_level]

    def get_daily_session_time(self) -> Dict[str, int]:
        """Получить время ежедневной сессии."""
        if self.content_format == ContentFormat.TEXT:
            base_time = 15
        elif self.content_format == ContentFormat.AUDIO:
            base_time = 20
        else:  # BOTH
            base_time = 25

        # Корректировка по уровню сложности
        multipliers = {
            SeverityLevel.SEVERE: 1.4,
            SeverityLevel.MODERATE: 1.2,
            SeverityLevel.MILD: 1.0,
            SeverityLevel.MINIMAL: 0.8
        }

        adjusted_time = int(base_time * multipliers[self.severity_level])

        return {
            "text_minutes": adjusted_time,
            "audio_minutes": adjusted_time + 5,
            "total_minutes": min(adjusted_time, self.daily_time_limit)
        }

    def get_techniques_for_vak(self) -> List[str]:
        """Получить техники, адаптированные под VAK тип."""
        vak_techniques = {
            VAKType.VISUAL: [
                "visualization", "color_therapy", "imagery_healing",
                "mental_movies", "symbolic_representation"
            ],
            VAKType.AUDITORY: [
                "affirmations", "inner_dialogue", "sound_healing",
                "verbal_reframing", "auditory_anchoring"
            ],
            VAKType.KINESTHETIC: [
                "breathing_techniques", "body_awareness", "movement_therapy",
                "tactile_anchoring", "somatic_experiencing"
            ],
            VAKType.MIXED: [
                "multi_sensory_integration", "cross_modal_anchoring",
                "synesthetic_techniques", "balanced_approach"
            ]
        }
        return vak_techniques.get(self.vak_type, vak_techniques[VAKType.MIXED])

    def should_delegate(self, task_keywords: List[str], current_agent_type: str) -> Optional[str]:
        """Определить нужно ли делегировать задачу."""
        # Делегирование исследовательских задач
        research_keywords = ['research', 'study', 'evidence', 'scientific', 'validation']
        if any(keyword in task_keywords for keyword in research_keywords):
            return "nlp_content_research_agent"

        # Делегирование контроля качества
        quality_keywords = ['quality', 'validation', 'ethics', 'safety', 'review']
        if any(keyword in task_keywords for keyword in quality_keywords):
            return "nlp_content_quality_guardian_agent"

        return None


def create_program_generator_dependencies(
    api_key: str,
    domain: str = "psychology",
    severity: str = "moderate",
    vak_type: str = "mixed",
    **kwargs
) -> NLPProgramGeneratorDependencies:
    """Создать зависимости для генератора программ."""
    return NLPProgramGeneratorDependencies(
        api_key=api_key,
        domain=ProgramDomain(domain),
        severity_level=SeverityLevel(severity),
        vak_type=VAKType(vak_type),
        **kwargs
    )


def create_psychology_program_dependencies(
    api_key: str,
    **kwargs
) -> NLPProgramGeneratorDependencies:
    """Создать зависимости для психологических программ."""
    return create_program_generator_dependencies(
        api_key=api_key,
        domain="psychology",
        program_type=ProgramType.EMOTIONAL_REGULATION,
        nlp_techniques=[
            NLPTechnique.ANCHORING,
            NLPTechnique.REFRAMING,
            NLPTechnique.TIMELINE
        ],
        **kwargs
    )


def create_astrology_program_dependencies(
    api_key: str,
    **kwargs
) -> NLPProgramGeneratorDependencies:
    """Создать зависимости для астрологических программ."""
    return create_program_generator_dependencies(
        api_key=api_key,
        domain="astrology",
        program_type=ProgramType.GOAL_ACHIEVEMENT,
        nlp_techniques=[
            NLPTechnique.TIMELINE,
            NLPTechnique.ANCHORING,
            NLPTechnique.SUBMODALITIES
        ],
        **kwargs
    )


def create_universal_program_dependencies(
    api_key: str,
    **kwargs
) -> NLPProgramGeneratorDependencies:
    """Создать универсальные зависимости программ."""
    return create_program_generator_dependencies(
        api_key=api_key,
        domain="psychology",  # По умолчанию
        severity="moderate",
        vak_type="mixed",
        content_format=ContentFormat.BOTH,
        enable_pattern_shift=True,
        use_hypnotic_language=True,
        modular_structure=True,
        **kwargs
    )