"""
Psychology Domain Validation Configuration

Конфигурация для валидации психологического контента с повышенными требованиями безопасности.
"""

from ..dependencies import create_psychology_quality_guardian_dependencies
from ..settings import create_validation_settings_for_domain

def create_psychology_validation_config(api_key: str) -> dict:
    """Создать конфигурацию для валидации психологического контента."""

    return {
        "domain": "psychology",
        "settings": {
            "excellence_threshold": 85.0,  # Повышенные требования для психологии
            "strict_safety_mode": True,
            "require_scientific_basis": True,
            "enable_age_validation": True,
            "min_age_restriction": 16,
            "max_age_restriction": 80,

            # Специфичные требования для психологии
            "require_evidence_based_approaches": True,
            "require_clinical_safety_checks": True,
            "enable_trauma_sensitivity": True,
            "require_professional_ethics": True,

            # Валидация методологии
            "validate_cbt_compliance": True,
            "validate_dbt_elements": True,
            "validate_mindfulness_safety": True,

            # Контент-специфичные настройки
            "min_test_questions": 15,
            "require_life_situations": True,
            "avoid_clinical_terminology": True,
            "require_vak_adaptation": True,

            # Безопасность
            "auto_flag_manipulation": True,
            "auto_flag_pseudoscience": True,
            "require_informed_consent": True,
            "require_contraindications": True
        },

        "validation_criteria": {
            # Структурные требования для тестов
            "test_requirements": {
                "min_questions": 15,
                "life_situation_ratio": 0.8,  # 80% жизненных ситуаций
                "clinical_terms_allowed": False,
                "flexible_scoring": True
            },

            # Требования для программ трансформации
            "program_requirements": {
                "three_level_structure": True,
                "crisis_phase_days": 21,
                "stabilization_phase_days": 21,
                "development_phase_days": 14,
                "vak_personalization": True,
                "multiformat_content": True,
                "anti_repetition_system": True
            },

            # Требования для NLP техник
            "nlp_requirements": {
                "scientific_evidence": True,
                "ericksonian_compliance": True,
                "ethical_framework": True,
                "safety_warnings": True,
                "age_appropriate": True
            }
        }
    }


def create_therapy_content_config(api_key: str) -> dict:
    """Конфигурация для терапевтического контента."""

    base_config = create_psychology_validation_config(api_key)
    base_config["settings"].update({
        "excellence_threshold": 90.0,  # Максимальные требования для терапии
        "require_license_compliance": True,
        "enable_supervision_requirements": True,
        "validate_therapeutic_alliance": True,
        "require_crisis_protocols": True
    })

    return base_config


def create_self_help_config(api_key: str) -> dict:
    """Конфигурация для контента самопомощи."""

    base_config = create_psychology_validation_config(api_key)
    base_config["settings"].update({
        "excellence_threshold": 80.0,  # Стандартные требования для самопомощи
        "enable_self_application_safety": True,
        "require_professional_referral_guidance": True,
        "validate_diy_safety": True,
        "limit_intervention_complexity": True
    })

    return base_config


def create_educational_psychology_config(api_key: str) -> dict:
    """Конфигурация для образовательного психологического контента."""

    base_config = create_psychology_validation_config(api_key)
    base_config["settings"].update({
        "excellence_threshold": 75.0,
        "enable_educational_standards": True,
        "validate_pedagogical_approach": True,
        "require_learning_objectives": True,
        "enable_age_specific_adaptation": True
    })

    return base_config


# Примеры использования
if __name__ == "__main__":
    # Конфигурация для валидации терапевтического контента
    therapy_config = create_therapy_content_config("your-api-key")

    # Конфигурация для самопомощи
    self_help_config = create_self_help_config("your-api-key")

    # Конфигурация для образовательного контента
    educational_config = create_educational_psychology_config("your-api-key")