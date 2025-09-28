"""
Конфигурация Pattern Cultural Adaptation Expert Agent для образовательных проектов.

Специальная настройка для образовательных платформ,
онлайн-курсов и учебных материалов по психологии.
"""

from ..dependencies import CultureType, create_cultural_adaptation_dependencies


def create_education_config(api_key: str, target_culture: str = "universal"):
    """
    Создать конфигурацию для образовательных проектов.

    Args:
        api_key: API ключ для LLM провайдера
        target_culture: Целевая культура для адаптации

    Returns:
        Настроенные зависимости для образовательного домена
    """
    return create_cultural_adaptation_dependencies(
        api_key=api_key,
        target_culture=getattr(CultureType, target_culture.upper(), CultureType.UNIVERSAL),
        domain_type="education",
        project_type="e_learning",
        adaptation_depth="moderate",
        sensitivity_level="medium",
        cultural_validation_required=True,
        inclusive_content=True,
        academic_context=True,
        age_appropriate=True
    )


# Предустановленные конфигурации для образования
EDUCATION_UKRAINIAN_CONFIG = {
    "target_culture": CultureType.UKRAINIAN,
    "domain_type": "education",
    "project_type": "e_learning",
    "adaptation_depth": "moderate",
    "sensitivity_level": "medium",
    "cultural_focus": ["practical_application", "community_learning", "resilience_building"],
    "metaphor_themes": ["growth", "development", "overcoming"],
    "communication_style": "engaging_storytelling",
    "learning_style": "visual_narrative",
    "cultural_examples": True
}

EDUCATION_POLISH_CONFIG = {
    "target_culture": CultureType.POLISH,
    "domain_type": "education",
    "project_type": "e_learning",
    "adaptation_depth": "moderate",
    "sensitivity_level": "medium",
    "cultural_focus": ["structured_learning", "traditional_values", "moral_education"],
    "metaphor_themes": ["building", "foundation", "wisdom"],
    "communication_style": "formal_academic",
    "learning_style": "systematic_approach",
    "ethical_framework": True
}

EDUCATION_ENGLISH_CONFIG = {
    "target_culture": CultureType.ENGLISH,
    "domain_type": "education",
    "project_type": "e_learning",
    "adaptation_depth": "shallow",
    "sensitivity_level": "medium",
    "cultural_focus": ["evidence_based", "critical_thinking", "diversity"],
    "metaphor_themes": ["exploration", "discovery", "innovation"],
    "communication_style": "interactive_engaging",
    "learning_style": "self_directed",
    "research_based": True
}


def get_education_examples():
    """Получить примеры использования в образовательном контексте."""
    return {
        "psychology_course": {
            "ukrainian": "Курс практической психологии с акцентом на семейные ценности",
            "polish": "Академический курс с интеграцией этических принципов",
            "english": "Исследовательский курс с мультикультурной перспективой"
        },
        "stress_management": {
            "ukrainian": "Управление стрессом через природные техники и общинную поддержку",
            "polish": "Стресс-менеджмент с использованием традиционных практик",
            "english": "Научно-обоснованные техники управления стрессом"
        },
        "emotional_intelligence": {
            "ukrainian": "Эмоциональный интеллект в контексте коллективной культуры",
            "polish": "ЭИ с акцентом на социальную ответственность",
            "english": "ЭИ для личностного и профессионального развития"
        }
    }