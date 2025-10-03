"""
Pydantic модели для Pattern Metaphor Weaver Agent.

Модели для создания терапевтических метафор в программах трансформации.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class MetaphorType(str, Enum):
    """Типы терапевтических метафор."""
    JOURNEY = "journey"  # Метафора пути/путешествия
    NATURE = "nature"  # Природные метафоры (река, дерево, etc.)
    ARCHITECTURE = "architecture"  # Архитектурные метафоры (строительство, дом)
    TRANSFORMATION = "transformation"  # Метафоры трансформации (бабочка, феникс)
    HEALING = "healing"  # Целительные метафоры
    GROWTH = "growth"  # Метафоры роста и развития
    LIBERATION = "liberation"  # Освобождение и раскрепощение
    INTEGRATION = "integration"  # Интеграция частей личности
    REBIRTH = "rebirth"  # Перерождение и новое начало


class ArchetypeType(str, Enum):
    """Юнгианские архетипы."""
    HERO = "hero"  # Герой
    SHADOW = "shadow"  # Тень
    ANIMA_ANIMUS = "anima_animus"  # Анима/Анимус
    WISE_OLD_MAN = "wise_old_man"  # Мудрый старец
    GREAT_MOTHER = "great_mother"  # Великая мать
    CHILD = "child"  # Ребенок (внутренний ребенок)
    TRICKSTER = "trickster"  # Трикстер
    SELF = "self"  # Самость
    PERSONA = "persona"  # Персона


class MetaphorLevel(str, Enum):
    """Уровни понимания метафоры."""
    SURFACE = "surface"  # Поверхностный уровень
    SYMBOLIC = "symbolic"  # Символический уровень
    ARCHETYPAL = "archetypal"  # Архетипический уровень
    TRANSFORMATIONAL = "transformational"  # Трансформационный уровень


class IsomorphismType(str, Enum):
    """Типы изоморфизма метафор."""
    STRUCTURAL = "structural"  # Структурный изоморфизм
    PROCESS = "process"  # Процессуальный изоморфизм
    EMOTIONAL = "emotional"  # Эмоциональный изоморфизм
    RELATIONAL = "relational"  # Реляционный изоморфизм


class TherapeuticMessage(BaseModel):
    """Терапевтическое послание встроенное в метафору."""
    message_id: str
    core_message: str
    level: MetaphorLevel
    embedded_suggestion: Optional[str] = None
    target_belief: Optional[str] = None  # Какое убеждение меняем


class TherapeuticMetaphor(BaseModel):
    """Терапевтическая метафора."""
    metaphor_id: str
    title: str
    metaphor_type: MetaphorType
    archetype: Optional[ArchetypeType] = None

    # Содержание
    narrative: str  # Основное повествование
    imagery: List[str] = Field(default_factory=list)  # Образы
    symbols: Dict[str, str] = Field(default_factory=dict)  # Символы и их значения

    # Терапевтические слои
    therapeutic_messages: List[TherapeuticMessage] = Field(default_factory=list)
    levels: List[MetaphorLevel] = Field(default_factory=list)

    # Изоморфизм
    isomorphism_type: Optional[IsomorphismType] = None
    maps_to_problem: str  # На какую проблему/паттерн накладывается

    # Культурная адаптация
    cultural_context: Optional[str] = None
    adapted_for_age: Optional[str] = None  # children, adolescents, adults, elderly

    # Метаданные
    intended_effect: str
    timing_suggestion: str  # Когда использовать
    created_at: datetime = Field(default_factory=datetime.now)


class MetaphorSeed(BaseModel):
    """Семя метафоры - краткая отсылка для активации."""
    seed_id: str
    original_metaphor_id: str
    seed_phrase: str  # Краткая фраза для напоминания
    activation_context: str  # В каком контексте активировать
    expected_effect: str


class ArchetypalImage(BaseModel):
    """Архетипический образ."""
    image_id: str
    archetype: ArchetypeType
    cultural_manifestation: str
    symbolic_meaning: str
    therapeutic_application: str
    examples: List[str] = Field(default_factory=list)


class StoryStructure(BaseModel):
    """Структура терапевтической истории."""
    story_id: str
    title: str

    # Структура
    beginning: str  # Начало (установка ситуации)
    middle: str  # Середина (конфликт/трансформация)
    end: str  # Конец (resolution/новое состояние)

    # Встроенные элементы
    embedded_metaphors: List[str] = Field(default_factory=list)  # ID метафор
    therapeutic_messages: List[str] = Field(default_factory=list)

    # Характеристики
    emotional_arc: str
    transformation_point: str  # Ключевой момент трансформации
    resolution_type: str  # Как разрешается


class IsomorphicMapping(BaseModel):
    """Изоморфное отображение между проблемой и метафорой."""
    mapping_id: str
    problem_structure: Dict[str, Any]
    metaphor_structure: Dict[str, Any]
    correspondence: Dict[str, str]  # Элемент проблемы -> элемент метафоры
    isomorphism_type: IsomorphismType


class MetaphorLibrary(BaseModel):
    """Библиотека метафор."""
    library_id: str
    name: str
    description: str

    # Категории
    by_type: Dict[MetaphorType, List[str]] = Field(default_factory=dict)
    by_archetype: Dict[ArchetypeType, List[str]] = Field(default_factory=dict)
    by_problem: Dict[str, List[str]] = Field(default_factory=dict)

    # Готовые метафоры
    metaphors: List[TherapeuticMetaphor] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class MetaphorEffectiveness(BaseModel):
    """Оценка эффективности метафоры."""
    evaluation_id: str
    metaphor_id: str

    # Метрики
    resonance_score: float = Field(ge=0.0, le=1.0)  # Насколько резонирует
    comprehension_score: float = Field(ge=0.0, le=1.0)  # Насколько понятна
    transformation_potential: float = Field(ge=0.0, le=1.0)  # Потенциал изменений

    # Обратная связь
    user_feedback: Optional[str] = None
    insights_generated: List[str] = Field(default_factory=list)

    evaluated_at: datetime = Field(default_factory=datetime.now)


class CulturalAdaptation(BaseModel):
    """Культурная адаптация метафоры."""
    adaptation_id: str
    original_metaphor_id: str
    target_culture: str

    # Адаптация
    adapted_narrative: str
    replaced_symbols: Dict[str, str] = Field(default_factory=dict)  # Старый -> новый
    cultural_considerations: List[str] = Field(default_factory=list)

    # Сохранение сути
    preserved_core_message: str
    preserved_isomorphism: bool = Field(default=True)


class MetaphorChain(BaseModel):
    """Цепочка метафор в программе."""
    chain_id: str
    program_id: str

    # Последовательность
    metaphor_sequence: List[str] = Field(default_factory=list)  # ID метафор
    thematic_thread: str  # Общая нить

    # Развитие
    progression: str  # Как развивается метафора
    cumulative_effect: str  # Кумулятивный эффект

    # Якорение
    recurring_symbols: List[str] = Field(default_factory=list)
    callbacks: Dict[str, str] = Field(default_factory=dict)  # Отсылки назад


__all__ = [
    "MetaphorType",
    "ArchetypeType",
    "MetaphorLevel",
    "IsomorphismType",
    "TherapeuticMessage",
    "TherapeuticMetaphor",
    "MetaphorSeed",
    "ArchetypalImage",
    "StoryStructure",
    "IsomorphicMapping",
    "MetaphorLibrary",
    "MetaphorEffectiveness",
    "CulturalAdaptation",
    "MetaphorChain"
]
