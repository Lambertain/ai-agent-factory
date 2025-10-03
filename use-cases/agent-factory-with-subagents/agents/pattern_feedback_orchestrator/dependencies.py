"""
Зависимости для Pattern Feedback Orchestrator Agent
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import os


@dataclass
class PsychometricDatabase:
    """База данных психометрических принципов"""

    def __post_init__(self):
        self.scale_types = {
            "likert": "Шкала Лайкерта - ordinal scale для измерения отношений",
            "semantic_differential": "Семантический дифференциал - биполярные шкалы",
            "thurstone": "Шкала Терстоуна - equal-appearing intervals",
            "guttman": "Шкала Гуттмана - cumulative scale"
        }

        self.response_biases = {
            "social_desirability": "Социальная желательность - стремление выглядеть лучше",
            "acquiescence": "Согласие - тенденция соглашаться с утверждениями",
            "extreme_response": "Экстремальный ответ - выбор крайних значений",
            "central_tendency": "Центральная тенденция - избегание крайних значений",
            "recency_effect": "Эффект недавности - влияние последних событий"
        }

        self.question_design_principles = {
            "clarity": "Четкость и однозначность формулировки",
            "brevity": "Краткость - короткие вопросы лучше",
            "relevance": "Релевантность целям сбора данных",
            "neutrality": "Нейтральность - избегание leading questions",
            "single_concept": "Один концепт на вопрос"
        }


@dataclass
class UXResearchDatabase:
    """База данных принципов UX research"""

    def __post_init__(self):
        self.feedback_timing = {
            "immediate": "Сразу после опыта - высокая точность, свежие эмоции",
            "delayed": "Отложенная - меньше эмоций, больше рефлексии",
            "periodic": "Периодическая - отслеживание динамики"
        }

        self.form_design_principles = {
            "progressive_disclosure": "Постепенное раскрытие - показывать по одному вопросу",
            "progress_indicators": "Индикаторы прогресса - мотивируют завершение",
            "clear_labels": "Четкие подписи - пользователь всегда знает что делать",
            "error_prevention": "Предотвращение ошибок - валидация в реальном времени",
            "mobile_first": "Mobile-first - оптимизация для мобильных устройств"
        }

        self.completion_tactics = {
            "short_forms": "Короткие формы (<3 минут) - completion rate >80%",
            "optional_questions": "Опциональные вопросы - снижают barrier to entry",
            "save_progress": "Сохранение прогресса - можно вернуться позже",
            "incentives": "Стимулы - повышают мотивацию заполнения"
        }


@dataclass
class BehavioralAnalyticsDatabase:
    """База данных поведенческой аналитики"""

    def __post_init__(self):
        self.crisis_detection_patterns = {
            "extreme_negative": "Экстремально негативные ответы на multiple вопросов",
            "rapid_decline": "Резкое снижение показателей за короткий период",
            "hopelessness_indicators": "Индикаторы безнадежности в открытых ответах",
            "isolation_signals": "Сигналы изоляции и отстранения",
            "risk_keywords": "Ключевые слова риска в текстовых ответах"
        }

        self.engagement_metrics = {
            "completion_rate": "Процент завершения форм",
            "response_quality": "Качество ответов (не rushed, thoughtful)",
            "open_text_length": "Длина текстовых ответов",
            "time_spent": "Время заполнения",
            "consistency": "Консистентность ответов"
        }

        self.actionable_insights_criteria = {
            "specificity": "Конкретность - четкие рекомендации",
            "feasibility": "Выполнимость - можно реализовать",
            "measurability": "Измеримость - можно отследить изменения",
            "relevance": "Релевантность - важно для пользователя"
        }


@dataclass
class PatternFeedbackOrchestratorDependencies:
    """
    Зависимости для Pattern Feedback Orchestrator Agent

    Интеграции:
    - RAG через knowledge_tags и knowledge_domain
    - Archon через archon_project_id
    - PatternShift через patternshift_project_path
    """

    # Основные параметры
    api_key: str
    patternshift_project_path: str = ""
    agent_name: str = "pattern_feedback_orchestrator"

    # RAG интеграция
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "pattern-feedback",
        "psychometrics",
        "ux-research",
        "behavioral-analytics",
        "crisis-detection",
        "agent-knowledge",
        "patternshift"
    ])
    knowledge_domain: Optional[str] = None

    # Archon интеграция - проект PatternShift
    archon_project_id: str = "d5c0bd7d-8856-4ed3-98b1-561f80f7a299"

    # Специализированные базы данных
    psychometric_db: PsychometricDatabase = field(default_factory=PsychometricDatabase)
    ux_research_db: UXResearchDatabase = field(default_factory=UXResearchDatabase)
    behavioral_analytics_db: BehavioralAnalyticsDatabase = field(default_factory=BehavioralAnalyticsDatabase)

    def __post_init__(self):
        """Валидация зависимостей"""
        if not self.api_key:
            raise ValueError("API key обязателен для работы агента")

        # Валидация пути к PatternShift проекту если указан
        if self.patternshift_project_path and not os.path.exists(self.patternshift_project_path):
            raise ValueError(f"PatternShift проект не найден: {self.patternshift_project_path}")

    def get_scale_type_info(self, scale_type: str) -> str:
        """Получить информацию о типе шкалы"""
        return self.psychometric_db.scale_types.get(scale_type, "")

    def get_response_bias_info(self, bias_type: str) -> str:
        """Получить информацию о типе предвзятости ответов"""
        return self.psychometric_db.response_biases.get(bias_type, "")

    def get_feedback_timing_strategy(self, timing: str) -> str:
        """Получить стратегию тайминга обратной связи"""
        return self.ux_research_db.feedback_timing.get(timing, "")

    def get_crisis_detection_pattern(self, pattern: str) -> str:
        """Получить паттерн детекции кризиса"""
        return self.behavioral_analytics_db.crisis_detection_patterns.get(pattern, "")

    def get_form_design_principle(self, principle: str) -> str:
        """Получить принцип дизайна форм"""
        return self.ux_research_db.form_design_principles.get(principle, "")


__all__ = [
    "PatternFeedbackOrchestratorDependencies",
    "PsychometricDatabase",
    "UXResearchDatabase",
    "BehavioralAnalyticsDatabase"
]
