"""
Зависимости для Pattern Progress Narrator Agent
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class StorytellingDatabase:
    """База данных сторителлинга и нарративных техник"""

    def __post_init__(self):
        # Hero's Journey stages (Joseph Campbell)
        self.heros_journey_stages = {
            "ordinary_world": "Обычный мир - начальная точка",
            "call_to_adventure": "Зов к приключению - появление проблемы/возможности",
            "refusal_of_call": "Отказ от зова - страхи и сомнения",
            "meeting_mentor": "Встреча с наставником - поддержка и руководство",
            "crossing_threshold": "Пересечение порога - commitment к изменениям",
            "tests_allies_enemies": "Испытания - развитие навыков",
            "approach_inmost_cave": "Приближение к сокровенной пещере - подготовка к главному испытанию",
            "ordeal": "Испытание - момент истины",
            "reward": "Награда - достижение цели",
            "road_back": "Дорога назад - интеграция изменений",
            "resurrection": "Воскрешение - финальная трансформация",
            "return_with_elixir": "Возвращение с эликсиром - новая жизнь"
        }

        # Narrative arcs
        self.narrative_arcs = {
            "transformation": "From problem → through journey → to solution",
            "overcoming": "Challenge → struggle → breakthrough → mastery",
            "discovery": "Ignorance → curiosity → learning → wisdom",
            "growth": "Limitation → effort → progress → expansion"
        }

        # Framing techniques
        self.framing_techniques = {
            "achievement": "Highlight what was accomplished",
            "progress": "Show movement from point A to point B",
            "effort": "Recognize the work invested",
            "learning": "Extract lessons from experience",
            "character": "Show personal qualities demonstrated"
        }


@dataclass
class MotivationalPsychologyDatabase:
    """База данных мотивационной психологии"""

    def __post_init__(self):
        # Self-Determination Theory (Deci & Ryan)
        self.intrinsic_motivators = {
            "autonomy": "Sense of choice and volition",
            "competence": "Feeling effective and capable",
            "relatedness": "Connection with others"
        }

        # Goal Progress Theory
        self.progress_principles = {
            "small_wins": "Celebrate incremental progress",
            "momentum": "Build on consecutive successes",
            "reframing": "Turn setbacks into learning",
            "anticipation": "Create excitement for next steps",
            "reflection": "Acknowledge distance traveled"
        }

        # Motivational messaging patterns
        self.messaging_patterns = {
            "encouraging": "You're making progress, keep going",
            "celebratory": "Amazing achievement, you did it!",
            "reflective": "Look how far you've come",
            "supportive": "It's okay to struggle, you're not alone",
            "inspiring": "Imagine what's possible ahead"
        }


@dataclass
class MetaphorLibrary:
    """Библиотека терапевтических метафор"""

    def __post_init__(self):
        # Journey metaphors
        self.journey_metaphors = {
            "mountain_climb": "Восхождение на гору - преодоление высот",
            "river_flow": "Течение реки - движение с препятствиями",
            "path_discovery": "Открытие пути - исследование",
            "bridge_building": "Строительство моста - соединение",
            "seed_growth": "Рост семени - развитие изнутри"
        }

        # Transformation metaphors
        self.transformation_metaphors = {
            "butterfly": "Гусеница → кокон → бабочка",
            "phoenix": "Возрождение из пепла",
            "seasons": "Смена сезонов - циклы изменений",
            "alchemy": "Превращение свинца в золото",
            "sculpture": "Создание формы из материала"
        }

        # Archetypal images (Jung)
        self.archetypal_images = {
            "hero": "Преодолевающий трудности",
            "explorer": "Исследующий неизвестное",
            "sage": "Обретающий мудрость",
            "creator": "Создающий новое",
            "caregiver": "Заботящийся о себе"
        }


@dataclass
class PatternProgressNarratorDependencies:
    """Зависимости для Pattern Progress Narrator Agent"""

    # Основные настройки
    api_key: str
    agent_name: str = "pattern_progress_narrator"  # For RAG protection
    patternshift_project_path: str = ""

    # Контекст пользователя
    user_id: str = ""
    user_name: str = ""
    day_number: int = 1
    program_name: str = ""

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "pattern-progress-narrator",
        "storytelling",
        "motivation",
        "hero-journey",
        "agent-knowledge",
        "patternshift"
    ])
    knowledge_domain: str | None = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Специализированные базы данных
    storytelling_db: StorytellingDatabase = field(default_factory=StorytellingDatabase)
    motivation_db: MotivationalPsychologyDatabase = field(default_factory=MotivationalPsychologyDatabase)
    metaphor_lib: MetaphorLibrary = field(default_factory=MetaphorLibrary)

    def __post_init__(self):
        """Инициализация специализированных баз данных"""
        if not isinstance(self.storytelling_db, StorytellingDatabase):
            self.storytelling_db = StorytellingDatabase()

        if not isinstance(self.motivation_db, MotivationalPsychologyDatabase):
            self.motivation_db = MotivationalPsychologyDatabase()

        if not isinstance(self.metaphor_lib, MetaphorLibrary):
            self.metaphor_lib = MetaphorLibrary()


__all__ = [
    "StorytellingDatabase",
    "MotivationalPsychologyDatabase",
    "MetaphorLibrary",
    "PatternProgressNarratorDependencies"
]
