"""
Конфигурация Pattern Cultural Adaptation Expert Agent для корпоративных проектов.

Специальная настройка для корпоративного обучения,
HR-программ и организационного развития.
"""

from ..dependencies import CultureType, create_cultural_adaptation_dependencies


def create_corporate_config(api_key: str, target_culture: str = "english"):
    """
    Создать конфигурацию для корпоративных проектов.

    Args:
        api_key: API ключ для LLM провайдера
        target_culture: Целевая культура для адаптации

    Returns:
        Настроенные зависимости для корпоративного домена
    """
    return create_cultural_adaptation_dependencies(
        api_key=api_key,
        target_culture=getattr(CultureType, target_culture.upper(), CultureType.ENGLISH),
        domain_type="corporate",
        project_type="training",
        adaptation_depth="moderate",
        sensitivity_level="medium",
        cultural_validation_required=True,
        professional_context=True,
        business_appropriate=True,
        performance_focused=True
    )


# Предустановленные конфигурации для корпораций
CORPORATE_UKRAINIAN_CONFIG = {
    "target_culture": CultureType.UKRAINIAN,
    "domain_type": "corporate",
    "project_type": "training",
    "adaptation_depth": "moderate",
    "sensitivity_level": "medium",
    "cultural_focus": ["team_solidarity", "adaptability", "resourcefulness"],
    "metaphor_themes": ["building_together", "overcoming_challenges", "unity"],
    "communication_style": "collaborative_warm",
    "leadership_style": "supportive_democratic",
    "crisis_resilience": True
}

CORPORATE_POLISH_CONFIG = {
    "target_culture": CultureType.POLISH,
    "domain_type": "corporate",
    "project_type": "training",
    "adaptation_depth": "moderate",
    "sensitivity_level": "medium",
    "cultural_focus": ["quality_excellence", "tradition_innovation", "responsibility"],
    "metaphor_themes": ["craftsmanship", "legacy", "reliability"],
    "communication_style": "formal_structured",
    "leadership_style": "hierarchical_respectful",
    "work_ethic": True
}

CORPORATE_ENGLISH_CONFIG = {
    "target_culture": CultureType.ENGLISH,
    "domain_type": "corporate",
    "project_type": "training",
    "adaptation_depth": "shallow",
    "sensitivity_level": "low",
    "cultural_focus": ["performance_metrics", "innovation", "individual_development"],
    "metaphor_themes": ["achievement", "growth", "optimization"],
    "communication_style": "direct_efficient",
    "leadership_style": "results_oriented",
    "data_driven": True
}


def get_corporate_examples():
    """Получить примеры использования в корпоративном контексте."""
    return {
        "leadership_development": {
            "ukrainian": "Развитие лидерства через поддержку команды в сложных условиях",
            "polish": "Лидерские навыки с акцентом на ответственность и качество",
            "english": "Performance-driven leadership development program"
        },
        "stress_workplace": {
            "ukrainian": "Управление рабочим стрессом через коллективную поддержку",
            "polish": "Профилактика выгорания с уважением к work-life balance",
            "english": "Evidence-based stress management for high-performance teams"
        },
        "team_building": {
            "ukrainian": "Тимбилдинг через совместное преодоление вызовов",
            "polish": "Командная работа с акцентом на взаимное уважение",
            "english": "Results-oriented team collaboration and communication"
        },
        "change_management": {
            "ukrainian": "Адаптация к изменениям через культурную гибкость",
            "polish": "Управление изменениями с сохранением стабильности",
            "english": "Agile change management and organizational transformation"
        }
    }