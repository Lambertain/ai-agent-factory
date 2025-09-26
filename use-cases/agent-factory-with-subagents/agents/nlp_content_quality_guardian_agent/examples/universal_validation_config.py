"""
Universal Domain Validation Configuration

Универсальные конфигурации для валидации контента в любых доменах.
"""

from ..dependencies import create_universal_quality_guardian_dependencies
from ..settings import create_validation_settings_for_domain

def create_universal_validation_config(api_key: str) -> dict:
    """Создать универсальную конфигурацию валидации."""

    return {
        "domain": "universal",
        "settings": {
            "excellence_threshold": 80.0,  # Сбалансированные требования
            "enable_cross_domain_validation": True,
            "enable_cultural_adaptation": True,
            "support_multiple_methodologies": True,

            # Универсальные требования безопасности
            "enable_safety_scanning": True,
            "enable_ethics_validation": True,
            "auto_flag_manipulation": True,
            "auto_flag_pseudoscience": True,

            # Гибкие настройки
            "adaptive_quality_thresholds": True,
            "configurable_validation_aspects": True,
            "domain_agnostic_checks": True,

            # Мультиязычность и культура
            "multilingual_validation": True,
            "cultural_sensitivity_checks": True,
            "cross_cultural_adaptation": True
        },

        "validation_aspects": {
            "structure_validation": {
                "adaptive_requirements": True,
                "content_type_specific": True,
                "flexible_thresholds": True
            },

            "safety_validation": {
                "universal_safety_principles": True,
                "cultural_context_awareness": True,
                "age_appropriate_guidelines": True
            },

            "quality_validation": {
                "evidence_based_when_applicable": True,
                "ethical_framework_required": True,
                "transparency_principles": True
            }
        }
    }


def create_ecommerce_validation_config(api_key: str) -> dict:
    """Конфигурация для e-commerce контента."""

    base_config = create_universal_validation_config(api_key)
    base_config["settings"].update({
        "validate_commercial_ethics": True,
        "require_transparency_in_marketing": True,
        "enable_consumer_protection": True,
        "validate_pricing_fairness": True,
        "require_clear_terms": True
    })

    base_config["ecommerce_specific"] = {
        "product_description_accuracy": True,
        "pricing_transparency": True,
        "return_policy_clarity": True,
        "customer_data_protection": True,
        "advertising_standards": True
    }

    return base_config


def create_saas_validation_config(api_key: str) -> dict:
    """Конфигурация для SaaS платформ."""

    base_config = create_universal_validation_config(api_key)
    base_config["settings"].update({
        "validate_technical_accuracy": True,
        "require_api_documentation_quality": True,
        "enable_security_best_practices": True,
        "validate_user_onboarding": True,
        "require_accessibility_compliance": True
    })

    base_config["saas_specific"] = {
        "api_documentation": True,
        "security_practices": True,
        "user_experience": True,
        "technical_support_quality": True,
        "scalability_considerations": True
    }

    return base_config


def create_blog_cms_validation_config(api_key: str) -> dict:
    """Конфигурация для блогов и CMS."""

    base_config = create_universal_validation_config(api_key)
    base_config["settings"].update({
        "validate_content_accuracy": True,
        "require_source_attribution": True,
        "enable_plagiarism_detection": True,
        "validate_seo_best_practices": True,
        "require_readability_standards": True
    })

    base_config["content_specific"] = {
        "editorial_standards": True,
        "fact_checking": True,
        "copyright_compliance": True,
        "seo_optimization": True,
        "reader_engagement": True
    }

    return base_config


def create_crm_validation_config(api_key: str) -> dict:
    """Конфигурация для CRM систем."""

    base_config = create_universal_validation_config(api_key)
    base_config["settings"].update({
        "validate_data_privacy_compliance": True,
        "require_gdpr_compliance": True,
        "enable_customer_consent_validation": True,
        "validate_communication_ethics": True,
        "require_opt_out_mechanisms": True
    })

    base_config["crm_specific"] = {
        "data_privacy": True,
        "communication_ethics": True,
        "customer_consent": True,
        "automation_ethics": True,
        "reporting_accuracy": True
    }

    return base_config


def create_educational_platform_config(api_key: str) -> dict:
    """Конфигурация для образовательных платформ."""

    base_config = create_universal_validation_config(api_key)
    base_config["settings"].update({
        "validate_educational_standards": True,
        "require_age_appropriate_content": True,
        "enable_learning_objective_validation": True,
        "validate_assessment_fairness": True,
        "require_accessibility_standards": True
    })

    base_config["educational_specific"] = {
        "learning_objectives": True,
        "assessment_validity": True,
        "age_appropriateness": True,
        "accessibility": True,
        "engagement_quality": True
    }

    return base_config


def create_healthcare_adjacent_config(api_key: str) -> dict:
    """Конфигурация для контента, смежного с здравоохранением."""

    base_config = create_universal_validation_config(api_key)
    base_config["settings"].update({
        "strict_medical_claims_validation": True,
        "require_professional_disclaimers": True,
        "enable_evidence_based_validation": True,
        "validate_safety_warnings": True,
        "require_professional_referral_guidance": True,
        "excellence_threshold": 85.0  # Повышенные требования
    })

    base_config["healthcare_adjacent"] = {
        "medical_disclaimers": True,
        "evidence_based_claims": True,
        "safety_warnings": True,
        "professional_referrals": True,
        "regulatory_compliance": True
    }

    return base_config


# Мапинг доменов к конфигурациям
DOMAIN_CONFIG_MAPPING = {
    "universal": create_universal_validation_config,
    "ecommerce": create_ecommerce_validation_config,
    "saas": create_saas_validation_config,
    "blog": create_blog_cms_validation_config,
    "cms": create_blog_cms_validation_config,
    "crm": create_crm_validation_config,
    "education": create_educational_platform_config,
    "healthcare_adjacent": create_healthcare_adjacent_config
}


def get_validation_config_for_domain(domain: str, api_key: str) -> dict:
    """Получить конфигурацию валидации для конкретного домена."""

    config_creator = DOMAIN_CONFIG_MAPPING.get(domain, create_universal_validation_config)
    return config_creator(api_key)


# Примеры использования
if __name__ == "__main__":
    # Универсальная конфигурация
    universal_config = create_universal_validation_config("your-api-key")

    # E-commerce конфигурация
    ecommerce_config = create_ecommerce_validation_config("your-api-key")

    # SaaS конфигурация
    saas_config = create_saas_validation_config("your-api-key")

    # Получение конфигурации по имени домена
    config = get_validation_config_for_domain("ecommerce", "your-api-key")