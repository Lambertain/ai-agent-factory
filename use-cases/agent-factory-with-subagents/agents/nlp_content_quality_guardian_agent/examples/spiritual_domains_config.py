"""
Spiritual Domains Validation Configuration

Конфигурации для валидации контента в духовных доменах: астрология, таро, нумерология.
"""

from ..dependencies import ValidationDomain
from ..settings import create_validation_settings_for_domain


def create_astrology_validation_config(api_key: str) -> dict:
    """Создать конфигурацию для валидации астрологического контента."""

    return {
        "domain": "astrology",
        "settings": {
            "excellence_threshold": 75.0,  # Умеренные требования для символических систем
            "require_scientific_basis": False,  # Астрология - символическая система
            "enable_cultural_validation": True,
            "validate_cultural_sensitivity": True,
            "enable_ethical_guidance": True,

            # Специфичные требования для астрологии
            "validate_symbolic_accuracy": True,
            "require_cultural_respect": True,
            "avoid_deterministic_claims": True,
            "require_empowering_language": True,

            # Этические принципы
            "avoid_fatalistic_predictions": True,
            "encourage_free_will": True,
            "respect_client_autonomy": True,
            "provide_constructive_guidance": True,

            # Безопасность
            "avoid_medical_predictions": True,
            "avoid_financial_advice": True,
            "require_entertainment_disclaimers": True,
            "encourage_personal_responsibility": True
        },

        "validation_criteria": {
            "symbolic_integrity": {
                "accurate_interpretations": True,
                "consistent_symbolism": True,
                "respectful_approach": True,
                "cultural_awareness": True
            },

            "ethical_guidance": {
                "empowering_messages": True,
                "avoid_fear_based_content": True,
                "encourage_growth": True,
                "respect_diversity": True
            },

            "safety_standards": {
                "no_medical_claims": True,
                "no_financial_guarantees": True,
                "no_relationship_manipulation": True,
                "encourage_professional_help": True
            }
        }
    }


def create_tarot_validation_config(api_key: str) -> dict:
    """Конфигурация для валидации таро контента."""

    base_config = create_astrology_validation_config(api_key)
    base_config["domain"] = "tarot"

    base_config["settings"].update({
        "validate_card_symbolism": True,
        "require_interpretive_flexibility": True,
        "enable_intuitive_guidance": True,
        "respect_traditional_meanings": True,
        "allow_personal_interpretations": True
    })

    base_config["tarot_specific"] = {
        "card_accuracy": {
            "correct_traditional_meanings": True,
            "respect_deck_variations": True,
            "acknowledge_personal_intuition": True,
            "provide_multiple_interpretations": True
        },

        "reading_ethics": {
            "client_confidentiality": True,
            "non_judgmental_approach": True,
            "encourage_self_reflection": True,
            "avoid_dependency_creation": True
        },

        "safety_guidelines": {
            "no_absolute_predictions": True,
            "encourage_personal_agency": True,
            "respect_client_boundaries": True,
            "provide_supportive_guidance": True
        }
    }

    return base_config


def create_numerology_validation_config(api_key: str) -> dict:
    """Конфигурация для валидации нумерологического контента."""

    base_config = create_astrology_validation_config(api_key)
    base_config["domain"] = "numerology"

    base_config["settings"].update({
        "validate_mathematical_accuracy": True,
        "require_calculation_transparency": True,
        "respect_cultural_number_meanings": True,
        "provide_balanced_interpretations": True
    })

    base_config["numerology_specific"] = {
        "calculation_accuracy": {
            "correct_reduction_methods": True,
            "transparent_calculations": True,
            "explain_methodology": True,
            "acknowledge_system_variations": True
        },

        "interpretation_quality": {
            "balanced_perspectives": True,
            "positive_and_challenging_aspects": True,
            "growth_oriented_guidance": True,
            "cultural_sensitivity": True
        },

        "ethical_application": {
            "avoid_limiting_beliefs": True,
            "encourage_personal_development": True,
            "respect_individual_uniqueness": True,
            "promote_self_awareness": True
        }
    }

    return base_config


def create_spiritual_coaching_config(api_key: str) -> dict:
    """Конфигурация для духовного коучинга."""

    return {
        "domain": "spiritual_coaching",
        "settings": {
            "excellence_threshold": 80.0,  # Повышенные требования для коучинга
            "enable_ethical_coaching_standards": True,
            "require_professional_boundaries": True,
            "validate_spiritual_safety": True,
            "enable_trauma_awareness": True,

            # Коучинг этика
            "require_informed_consent": True,
            "maintain_professional_boundaries": True,
            "respect_client_beliefs": True,
            "avoid_religious_imposition": True,

            # Безопасность
            "recognize_mental_health_issues": True,
            "provide_referral_resources": True,
            "avoid_therapeutic_claims": True,
            "maintain_coaching_scope": True
        },

        "coaching_standards": {
            "professional_ethics": {
                "client_confidentiality": True,
                "informed_consent": True,
                "clear_agreements": True,
                "professional_boundaries": True
            },

            "spiritual_safety": {
                "respect_beliefs": True,
                "avoid_spiritual_bypassing": True,
                "ground_practices": True,
                "trauma_informed_approach": True
            },

            "competency_requirements": {
                "stay_within_scope": True,
                "ongoing_education": True,
                "supervision_when_needed": True,
                "referral_network": True
            }
        }
    }


def create_meditation_wellness_config(api_key: str) -> dict:
    """Конфигурация для медитации и велнеса."""

    return {
        "domain": "meditation_wellness",
        "settings": {
            "excellence_threshold": 78.0,
            "validate_practice_safety": True,
            "require_beginner_modifications": True,
            "enable_contraindication_warnings": True,
            "validate_evidence_based_benefits": True,

            # Практическая безопасность
            "provide_beginner_guidance": True,
            "warn_about_intense_practices": True,
            "offer_modifications": True,
            "respect_physical_limitations": True,

            # Научная честность
            "avoid_exaggerated_claims": True,
            "acknowledge_research_limitations": True,
            "provide_realistic_expectations": True,
            "cite_credible_sources": True
        },

        "wellness_standards": {
            "practice_safety": {
                "clear_instructions": True,
                "safety_warnings": True,
                "modification_options": True,
                "professional_guidance_recommendations": True
            },

            "evidence_based_approach": {
                "research_backed_claims": True,
                "honest_limitations": True,
                "realistic_timelines": True,
                "individual_variation_acknowledgment": True
            },

            "inclusivity": {
                "accessible_practices": True,
                "cultural_sensitivity": True,
                "physical_accommodation": True,
                "diverse_needs_consideration": True
            }
        }
    }


# Мапинг духовных доменов
SPIRITUAL_DOMAIN_MAPPING = {
    "astrology": create_astrology_validation_config,
    "tarot": create_tarot_validation_config,
    "numerology": create_numerology_validation_config,
    "spiritual_coaching": create_spiritual_coaching_config,
    "meditation": create_meditation_wellness_config,
    "wellness": create_meditation_wellness_config
}


def get_spiritual_validation_config(domain: str, api_key: str) -> dict:
    """Получить конфигурацию для духовного домена."""

    config_creator = SPIRITUAL_DOMAIN_MAPPING.get(domain)
    if not config_creator:
        # Возвращаем базовую астрологическую конфигурацию как fallback
        config_creator = create_astrology_validation_config

    return config_creator(api_key)


def create_holistic_wellness_config(api_key: str) -> dict:
    """Комбинированная конфигурация для холистического велнеса."""

    base_config = create_meditation_wellness_config(api_key)
    base_config["domain"] = "holistic_wellness"

    # Объединяем элементы всех духовных практик
    base_config["holistic_elements"] = {
        "astrology_integration": True,
        "numerology_insights": True,
        "tarot_reflection": True,
        "meditation_practices": True,
        "spiritual_coaching": True
    }

    base_config["settings"].update({
        "cross_discipline_validation": True,
        "integrated_approach_safety": True,
        "respect_all_traditions": True,
        "avoid_spiritual_materialism": True
    })

    return base_config


# Примеры использования
if __name__ == "__main__":
    # Конфигурации для разных духовных доменов
    astrology_config = create_astrology_validation_config("your-api-key")
    tarot_config = create_tarot_validation_config("your-api-key")
    numerology_config = create_numerology_validation_config("your-api-key")

    # Холистический подход
    holistic_config = create_holistic_wellness_config("your-api-key")

    # Получение конфигурации по домену
    config = get_spiritual_validation_config("tarot", "your-api-key")