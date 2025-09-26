"""
Конфигурация Psychology Test Generator для научных исследований

Этот пример показывает как настроить агент для использования в:
- Академических исследованиях
- Психологических экспериментах
- Лонгитюдных исследованиях
- Кросс-культурных проектах
"""

from psychology_test_generator import TestGeneratorDependencies, get_test_generator_config


def get_research_config():
    """
    Конфигурация для научных исследований.

    Особенности:
    - Высокие стандарты валидности
    - Экспериментальные конструкты
    - Кросс-культурная адаптация
    - Лонгитюдное отслеживание
    """
    return get_test_generator_config(
        domain="experimental_psychology",
        population="adults",
        test_type="research",
        purpose="scientific_investigation",

        # Исследовательские стандарты
        test_specification={
            "construct": "experimental_construct",
            "subscales": ["primary_measure", "control_variables", "mediators", "moderators"],
            "question_count": 40,
            "response_format": "likert_7",
            "time_limit_minutes": 25,
            "difficulty_level": "moderate",
            "cultural_adaptation": True
        },

        # Высокие исследовательские стандарты
        psychometric_standards={
            "reliability_threshold": 0.85,  # Исследовательский стандарт
            "validity_requirements": ["content", "construct", "convergent", "discriminant"],
            "normative_sample_size": 500,
            "validation_type": "comprehensive",
            "statistical_power": 0.90,
            "effect_size_detection": 0.2
        },

        # Исследовательские адаптации
        population_adaptations={
            "language_level": "professional",
            "cultural_considerations": True,
            "accessibility_features": [],
            "administration_format": "digital",
            "support_required": "none"
        }
    )


def get_personality_research_config():
    """Конфигурация для исследования личности."""
    return TestGeneratorDependencies(
        psychological_domain="personality",
        target_population="adults",
        test_type="research",
        measurement_purpose="scientific_investigation",

        test_specification={
            "construct": "personality_dimensions",
            "subscales": ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"],
            "question_count": 60,  # Детальное измерение
            "response_format": "likert_7",
            "time_limit_minutes": 20,
            "difficulty_level": "moderate"
        },

        psychometric_standards={
            "reliability_threshold": 0.85,
            "validity_requirements": ["content", "construct", "convergent", "discriminant"],
            "validation_type": "comprehensive"
        },

        # Исследовательские настройки
        enable_validation_tools=True,
        enable_psychometric_analysis=True,
        enable_research_integration=True
    )


def get_social_psychology_config():
    """Конфигурация для социально-психологических исследований."""
    return TestGeneratorDependencies(
        psychological_domain="social",
        target_population="adults",
        test_type="research",
        measurement_purpose="experimental_study",

        test_specification={
            "construct": "social_psychological_constructs",
            "subscales": ["attitudes", "social_identity", "group_dynamics", "interpersonal_relations"],
            "question_count": 35,
            "response_format": "likert_7",
            "time_limit_minutes": 18
        },

        psychometric_standards={
            "reliability_threshold": 0.80,
            "validity_requirements": ["content", "construct", "criterion"],
            "validation_type": "comprehensive"
        }
    )


def get_cognitive_research_config():
    """Конфигурация для когнитивных исследований."""
    return TestGeneratorDependencies(
        psychological_domain="cognitive",
        target_population="adults",
        test_type="research",
        measurement_purpose="cognitive_assessment",

        test_specification={
            "construct": "cognitive_processes",
            "subscales": ["attention", "memory", "executive_function", "processing_speed"],
            "question_count": 30,
            "response_format": "multiple_choice",
            "time_limit_minutes": 25
        },

        psychometric_standards={
            "reliability_threshold": 0.88,
            "validity_requirements": ["content", "construct", "criterion"],
            "validation_type": "comprehensive"
        }
    )


def get_developmental_research_config():
    """Конфигурация для исследований развития."""
    return TestGeneratorDependencies(
        psychological_domain="developmental",
        target_population="children",
        test_type="research",
        measurement_purpose="developmental_study",

        test_specification={
            "construct": "developmental_milestones",
            "subscales": ["cognitive_development", "social_development", "emotional_development", "motor_skills"],
            "question_count": 20,
            "response_format": "frequency",
            "time_limit_minutes": 15
        },

        psychometric_standards={
            "reliability_threshold": 0.80,
            "validity_requirements": ["content", "construct"],
            "validation_type": "basic"
        },

        # Детские адаптации для исследований
        population_adaptations={
            "language_level": "grade_6",
            "cultural_considerations": True,
            "accessibility_features": ["visual_aids", "simplified_language"],
            "administration_format": "mixed",
            "support_required": "intensive"
        }
    )


def get_cross_cultural_config():
    """Конфигурация для кросс-культурных исследований."""
    return TestGeneratorDependencies(
        psychological_domain="cultural",
        target_population="adults",
        test_type="research",
        measurement_purpose="cross_cultural_study",

        test_specification={
            "construct": "cultural_psychological_constructs",
            "subscales": ["cultural_values", "identity", "acculturation", "worldview"],
            "question_count": 45,
            "response_format": "likert_7",
            "time_limit_minutes": 22
        },

        psychometric_standards={
            "reliability_threshold": 0.85,
            "validity_requirements": ["content", "construct", "measurement_invariance"],
            "validation_type": "comprehensive"
        },

        # Кросс-культурные адаптации
        population_adaptations={
            "cultural_considerations": True,
            "language_level": "grade_10",
            "administration_format": "digital",
            "support_required": "minimal"
        }
    )


# Пример использования в исследовательском проекте
RESEARCH_USAGE_EXAMPLE = """
# Пример исследовательского проекта

from psychology_test_generator import psychology_test_generator_agent
from examples.research_config import get_personality_research_config

async def conduct_personality_study(study_id: str, sample_size: int, conditions: list):
    # Загрузка исследовательской конфигурации
    deps = get_personality_research_config()

    # Создание исследовательского инструмента
    result = await psychology_test_generator_agent.run(
        user_prompt=f\"\"\"
        Создай исследовательский инструмент для изучения личности:
        - Исследование ID: {study_id}
        - Размер выборки: {sample_size}
        - Экспериментальные условия: {conditions}
        - Требования: высокая валидность, психометрическая надежность
        - Формат: подходящий для онлайн-администрирования
        \"\"\",
        deps=deps
    )

    return {
        "research_instrument": result.data,
        "study_metadata": {
            "study_id": study_id,
            "target_sample_size": sample_size,
            "conditions": conditions,
            "expected_reliability": deps.psychometric_standards["reliability_threshold"],
            "administration_time": f"{deps.test_specification['time_limit_minutes']} minutes"
        }
    }

# Лонгитюдное исследование
async def setup_longitudinal_study():
    # Базовые измерения
    baseline_configs = [
        ("Personality", get_personality_research_config()),
        ("Social Psychology", get_social_psychology_config()),
        ("Cognitive", get_cognitive_research_config())
    ]

    study_battery = {}
    for name, config in baseline_configs:
        instrument = await psychology_test_generator_agent.run(
            user_prompt=f"Создай {name.lower()} инструмент для лонгитюдного исследования",
            deps=config
        )
        study_battery[f"{name.lower()}_baseline"] = instrument.data

    return {
        "longitudinal_battery": study_battery,
        "measurement_points": ["baseline", "6_months", "12_months", "24_months"],
        "retention_strategies": ["incentives", "regular_contact", "progress_feedback"],
        "data_analysis_plan": "mixed_effects_modeling"
    }
"""


# Исследовательские стандарты и протоколы
RESEARCH_PROTOCOLS = {
    "ethical_standards": {
        "irb_approval": "Required for human subjects research",
        "informed_consent": "Detailed consent with study procedures",
        "debriefing": "Post-study explanation of hypotheses",
        "data_anonymization": "Remove all identifying information"
    },

    "methodological_standards": {
        "sample_size_calculation": "Power analysis required",
        "randomization": "Proper randomization procedures",
        "control_groups": "Appropriate control conditions",
        "blinding": "Double-blind when possible"
    },

    "data_quality": {
        "reliability_minimum": 0.80,
        "validity_evidence": ["content", "construct", "criterion"],
        "factor_structure": "Confirmatory factor analysis",
        "measurement_invariance": "Multi-group testing"
    },

    "reporting_standards": {
        "consort": "For randomized trials",
        "strobe": "For observational studies",
        "prisma": "For systematic reviews",
        "pre_registration": "Study protocol registration"
    }
}


# Специализированные исследовательские конструкты
RESEARCH_CONSTRUCTS = {
    "experimental_psychology": {
        "cognitive_load": "Working memory demands during tasks",
        "attention_bias": "Selective attention toward specific stimuli",
        "implicit_attitudes": "Automatic evaluative responses",
        "decision_making": "Choice processes under uncertainty"
    },

    "social_psychology": {
        "social_identity": "Group membership and identification",
        "intergroup_contact": "Quality of contact between groups",
        "stereotype_threat": "Performance anxiety due to stereotypes",
        "prosocial_behavior": "Helping and cooperation"
    },

    "developmental_psychology": {
        "theory_of_mind": "Understanding others' mental states",
        "attachment_styles": "Relationship patterns with caregivers",
        "executive_function": "Self-regulation and cognitive control",
        "moral_reasoning": "Ethical decision-making development"
    },

    "clinical_psychology": {
        "emotion_regulation": "Management of emotional responses",
        "cognitive_biases": "Systematic thinking errors",
        "coping_strategies": "Responses to stress and adversity",
        "therapeutic_alliance": "Relationship quality in therapy"
    }
}


# Статистические методы для анализа
RESEARCH_STATISTICS = {
    "descriptive": ["means", "standard_deviations", "correlations", "effect_sizes"],
    "inferential": ["t_tests", "anova", "regression", "structural_equation_modeling"],
    "advanced": ["multilevel_modeling", "machine_learning", "network_analysis", "meta_analysis"],
    "psychometric": ["factor_analysis", "irt_models", "reliability_analysis", "validity_studies"]
}


if __name__ == "__main__":
    # Демонстрация исследовательских конфигураций
    print("=== Research Psychology Test Generator Configurations ===")

    configs = [
        ("Personality Research", get_personality_research_config()),
        ("Social Psychology", get_social_psychology_config()),
        ("Cognitive Research", get_cognitive_research_config()),
        ("Developmental Research", get_developmental_research_config()),
        ("Cross-Cultural", get_cross_cultural_config())
    ]

    for name, config in configs:
        print(f"\n{name}:")
        print(f"  Domain: {config.psychological_domain}")
        print(f"  Population: {config.target_population}")
        print(f"  Questions: {config.test_specification['question_count']}")
        print(f"  Reliability: {config.psychometric_standards['reliability_threshold']}")
        print(f"  Validation: {', '.join(config.psychometric_standards['validity_requirements'])}")

    print(f"\n=== Available Research Constructs ===")
    for domain, constructs in RESEARCH_CONSTRUCTS.items():
        print(f"\n{domain.replace('_', ' ').title()}:")
        for construct, description in constructs.items():
            print(f"  • {construct.replace('_', ' ').title()}: {description}")