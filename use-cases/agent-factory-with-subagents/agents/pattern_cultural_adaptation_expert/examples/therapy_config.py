"""
Конфигурация Pattern Cultural Adaptation Expert Agent для терапевтических проектов.

Специальная настройка для психотерапевтических приложений,
клинической практики и терапевтических интервенций.
"""

from ..dependencies import CultureType, create_cultural_adaptation_dependencies


def create_therapy_config(api_key: str, target_culture: str = "ukrainian"):
    """
    Создать конфигурацию для терапевтических проектов.

    Args:
        api_key: API ключ для LLM провайдера
        target_culture: Целевая культура для адаптации

    Returns:
        Настроенные зависимости для терапевтического домена
    """
    return create_cultural_adaptation_dependencies(
        api_key=api_key,
        target_culture=getattr(CultureType, target_culture.upper(), CultureType.UNIVERSAL),
        domain_type="therapy",
        project_type="clinical",
        adaptation_depth="deep",
        sensitivity_level="high",
        cultural_validation_required=True,
        religious_accommodation=True,
        trauma_informed=True,
        professional_context=True
    )


# Предустановленные конфигурации для терапии
THERAPY_UKRAINIAN_CONFIG = {
    "target_culture": CultureType.UKRAINIAN,
    "domain_type": "therapy",
    "project_type": "clinical",
    "adaptation_depth": "deep",
    "sensitivity_level": "high",
    "cultural_focus": ["family_systems", "collective_trauma", "orthodox_values"],
    "metaphor_themes": ["nature", "home", "resilience"],
    "communication_style": "high_context",
    "religious_accommodation": True,
    "trauma_informed": True
}

THERAPY_POLISH_CONFIG = {
    "target_culture": CultureType.POLISH,
    "domain_type": "therapy",
    "project_type": "clinical",
    "adaptation_depth": "deep",
    "sensitivity_level": "high",
    "cultural_focus": ["catholic_values", "family_tradition", "solidarity"],
    "metaphor_themes": ["faith", "community", "heritage"],
    "communication_style": "formal_respectful",
    "religious_accommodation": True,
    "traditional_values": True
}

THERAPY_ENGLISH_CONFIG = {
    "target_culture": CultureType.ENGLISH,
    "domain_type": "therapy",
    "project_type": "clinical",
    "adaptation_depth": "moderate",
    "sensitivity_level": "high",
    "cultural_focus": ["individual_autonomy", "diversity", "evidence_based"],
    "metaphor_themes": ["personal_growth", "achievement", "innovation"],
    "communication_style": "direct_professional",
    "secular_approach": True,
    "inclusive_language": True
}


def get_therapy_examples():
    """Получить примеры использования в терапевтическом контексте."""
    return {
        "anxiety_treatment": {
            "ukrainian": "Техники заземления через связь с природой и семейными корнями",
            "polish": "Молитвенные практики и общинная поддержка при тревоге",
            "english": "Когнитивно-поведенческие техники с фокусом на личную эффективность"
        },
        "trauma_therapy": {
            "ukrainian": "Нарративная терапия с интеграцией культурной стойкости",
            "polish": "Ритуалы исцеления с уважением к католическим традициям",
            "english": "ПТСР-протоколы с учетом индивидуальных потребностей"
        },
        "family_therapy": {
            "ukrainian": "Системная терапия с фокусом на расширенную семью",
            "polish": "Семейная терапия с интеграцией религиозных ценностей",
            "english": "Структурная семейная терапия с акцентом на коммуникации"
        }
    }