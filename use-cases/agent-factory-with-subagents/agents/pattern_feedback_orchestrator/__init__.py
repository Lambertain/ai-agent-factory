"""
Pattern Feedback Orchestrator Agent

Специализированный Pydantic AI агент для дизайна систем обратной связи
в рамках системы PatternShift.
"""

from .agent import agent, run_pattern_feedback_orchestrator
from .dependencies import PatternFeedbackOrchestratorDependencies
from .models import (
    FeedbackQuestion,
    FeedbackForm,
    TriggerRule,
    FeedbackResponse,
    FeedbackAnalytics,
    FeedbackModule,
    CrisisIndicator,
    QuestionType,
    ResponseScaleType,
    FeedbackPurpose,
    TriggerAction
)
from .tools import (
    design_feedback_form,
    create_trigger_rules,
    detect_crisis_patterns,
    generate_actionable_insights,
    search_agent_knowledge
)

__version__ = "1.0.0"

__all__ = [
    # Основной агент
    "agent",
    "run_pattern_feedback_orchestrator",

    # Зависимости
    "PatternFeedbackOrchestratorDependencies",

    # Модели данных
    "FeedbackQuestion",
    "FeedbackForm",
    "TriggerRule",
    "FeedbackResponse",
    "FeedbackAnalytics",
    "FeedbackModule",
    "CrisisIndicator",
    "QuestionType",
    "ResponseScaleType",
    "FeedbackPurpose",
    "TriggerAction",

    # Инструменты
    "design_feedback_form",
    "create_trigger_rules",
    "detect_crisis_patterns",
    "generate_actionable_insights",
    "search_agent_knowledge"
]
