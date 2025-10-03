"""
Зависимости для Pattern Exercise Architect Agent
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import os


@dataclass
class ExerciseDesignDatabase:
    """База данных принципов дизайна упражнений"""

    def __post_init__(self):
        self.exercise_principles = {
            "embodiment": "Воплощение опыта через телесные практики",
            "integration": "Интеграция изменений в повседневную жизнь",
            "progression": "Прогрессивное усложнение от простого к сложному",
            "multi_channel": "Задействование множественных каналов научения",
            "self_check": "Механизмы самопроверки и рефлексии",
            "nlp_integration": "Интеграция НЛП техник в упражнения"
        }

        self.learning_channels = {
            "cognitive": ["анализ", "планирование", "рефлексия", "метапознание"],
            "emotional": ["эмоциональный резонанс", "эмпатия", "катарсис"],
            "somatic": ["телесные практики", "дыхание", "движение", "осознанность тела"],
            "social": ["групповые практики", "обратная связь", "моделирование"]
        }

        self.nlp_techniques = [
            "рефрейминг",
            "якорение",
            "метафоры",
            "визуализация",
            "субмодальности",
            "позиции восприятия",
            "временная линия",
            "стратегии моделирования"
        ]


@dataclass
class CompletionCriteriaDatabase:
    """База данных критериев выполнения упражнений"""

    def __post_init__(self):
        self.criteria_types = {
            "behavioral": "Наблюдаемое поведение",
            "emotional": "Эмоциональное состояние",
            "cognitive": "Когнитивные изменения",
            "somatic": "Телесные ощущения"
        }

        self.self_check_questions = {
            "awareness": "Что я сейчас осознаю?",
            "change": "Что изменилось?",
            "integration": "Как я могу применить это в жизни?",
            "learning": "Чему я научился?"
        }


@dataclass
class ExerciseVariantsDatabase:
    """База данных вариантов упражнений"""

    def __post_init__(self):
        self.vak_adaptations = {
            "visual": "Визуальные образы, схемы, метафоры",
            "auditory": "Звуки, ритмы, вербализация",
            "kinesthetic": "Движение, ощущения, действия"
        }

        self.age_adaptations = {
            "young_adults": "18-30: Цифровые форматы, геймификация",
            "adults": "30-50: Практичность, карьера, семья",
            "mature": "50+: Мудрость, наследие, смыслы"
        }

        self.difficulty_levels = {
            "beginner": "Простые, короткие, с детальными инструкциями",
            "intermediate": "Умеренные, требуют некоторой практики",
            "advanced": "Сложные, требуют опыта и углубленной работы",
            "expert": "Мастер-уровень, тонкая настройка"
        }


@dataclass
class PatternExerciseArchitectDependencies:
    """
    Зависимости для Pattern Exercise Architect Agent

    Интеграции:
    - RAG через knowledge_tags и knowledge_domain
    - Archon через archon_project_id
    - PatternShift через patternshift_project_path
    """

    # Основные параметры
    api_key: str
    patternshift_project_path: str = ""
    agent_name: str = "pattern_exercise_architect"

    # RAG интеграция
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "pattern-exercise",
        "transformational-exercises",
        "nlp-techniques",
        "embodiment",
        "agent-knowledge",
        "patternshift"
    ])
    knowledge_domain: Optional[str] = None

    # Archon интеграция - проект PatternShift
    archon_project_id: str = "d5c0bd7d-8856-4ed3-98b1-561f80f7a299"

    # Специализированные базы данных
    exercise_design_db: ExerciseDesignDatabase = field(default_factory=ExerciseDesignDatabase)
    completion_criteria_db: CompletionCriteriaDatabase = field(default_factory=CompletionCriteriaDatabase)
    variants_db: ExerciseVariantsDatabase = field(default_factory=ExerciseVariantsDatabase)

    def __post_init__(self):
        """Валидация зависимостей"""
        if not self.api_key:
            raise ValueError("API key обязателен для работы агента")

        # Валидация пути к PatternShift проекту если указан
        if self.patternshift_project_path and not os.path.exists(self.patternshift_project_path):
            raise ValueError(f"PatternShift проект не найден: {self.patternshift_project_path}")

    def get_exercise_principle(self, principle_key: str) -> str:
        """Получить принцип дизайна упражнения"""
        return self.exercise_design_db.exercise_principles.get(principle_key, "")

    def get_learning_channel_techniques(self, channel: str) -> List[str]:
        """Получить техники для канала научения"""
        return self.exercise_design_db.learning_channels.get(channel, [])

    def get_nlp_techniques(self) -> List[str]:
        """Получить список НЛП техник"""
        return self.exercise_design_db.nlp_techniques

    def get_self_check_questions(self) -> Dict[str, str]:
        """Получить вопросы для самопроверки"""
        return self.completion_criteria_db.self_check_questions

    def get_vak_adaptation(self, vak_type: str) -> str:
        """Получить адаптацию под VAK тип"""
        return self.variants_db.vak_adaptations.get(vak_type, "")

    def get_age_adaptation(self, age_group: str) -> str:
        """Получить адаптацию под возрастную группу"""
        return self.variants_db.age_adaptations.get(age_group, "")


__all__ = [
    "PatternExerciseArchitectDependencies",
    "ExerciseDesignDatabase",
    "CompletionCriteriaDatabase",
    "ExerciseVariantsDatabase"
]
