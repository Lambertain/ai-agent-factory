"""
Psychology NLP Configuration Example
Пример конфигурации для психологического домена с NLP техниками
"""

from ..dependencies import UniversalNLPDependencies
from ..settings import create_universal_nlp_settings

def create_psychology_nlp_config(api_key: str) -> dict:
    """Создать конфигурацию для психологического NLP контента."""

    return {
        "domain": "psychology",
        "settings": {
            "excellence_threshold": 85.0,  # Повышенные требования для психологии
            "require_scientific_basis": True,
            "enable_clinical_safety": True,
            "validate_therapeutic_ethics": True,
            "enable_age_validation": True,

            # NLP специфичные требования
            "integrate_ericksonian_patterns": True,
            "require_vak_adaptations": True,
            "enable_therapeutic_metaphors": True,
            "validate_rapport_building": True,

            # Психологические принципы
            "focus_on_resources": True,
            "avoid_pathologizing": True,
            "encourage_self_efficacy": True,
            "maintain_hope_orientation": True,

            # Безопасность
            "avoid_clinical_diagnoses": True,
            "provide_professional_referrals": True,
            "require_informed_consent": True,
            "maintain_ethical_boundaries": True
        },

        "nlp_techniques": {
            "primary": [
                "reframing_context",
                "reframing_content",
                "anchoring_resources",
                "rapport_building",
                "presuppositions_healing"
            ],
            "advanced": [
                "meta_programs_identification",
                "submodalities_work",
                "timeline_therapy",
                "parts_integration",
                "belief_change_work"
            ],
            "ericksonian": [
                "therapeutic_metaphors",
                "embedded_commands",
                "truisms_healing",
                "utilization_principle",
                "confusion_technique"
            ]
        },

        "content_examples": {
            "depression_test": {
                "title": "Чому мені все байдуже?",
                "approach": "resource_focused",
                "sample_question": {
                    "text": "Коли ви прокидаєтеся вранці, перша думка зазвичай (трюизм):",
                    "nlp_integration": "truism + embedded_command",
                    "vak_visual": "...бачите можливості дня",
                    "vak_auditory": "...чуєте внутрішню мудрість",
                    "vak_kinesthetic": "...відчуваєте силу нового початку"
                }
            },
            "anxiety_program": {
                "title": "Від тривоги до спокою",
                "duration": 21,
                "phases": [
                    {"name": "recognition", "days": 7, "nlp_focus": "awareness_anchoring"},
                    {"name": "reframing", "days": 7, "nlp_focus": "context_shifting"},
                    {"name": "integration", "days": 7, "nlp_focus": "future_pacing"}
                ]
            }
        },

        "vak_psychology_adaptations": {
            "visual": {
                "keywords": ["бачиш", "ясно", "світло", "образ", "картина"],
                "metaphors": ["світло розуміння", "ясність мислей", "яскраві рішення"],
                "therapeutic_images": ["сонячний промінь надії", "мостик до змін"]
            },
            "auditory": {
                "keywords": ["чуєш", "звучить", "голос", "резонує", "мелодія"],
                "metaphors": ["внутрішній голос мудрості", "гармонія душі", "мелодія змін"],
                "therapeutic_sounds": ["тиша спокою", "ритм серця"]
            },
            "kinesthetic": {
                "keywords": ["відчуваєш", "тепло", "легко", "рух", "потік"],
                "metaphors": ["тепло прийняття", "легкість буття", "потік змін"],
                "therapeutic_sensations": ["обійми підтримки", "сила землі"]
            }
        },

        "safety_framework": {
            "crisis_indicators": [
                "suicidal_ideation_markers",
                "severe_depression_signs",
                "psychotic_symptoms",
                "substance_abuse_indicators"
            ],
            "referral_triggers": [
                "beyond_self_help_scope",
                "requires_professional_intervention",
                "medication_may_be_needed",
                "crisis_situation_detected"
            ],
            "ethical_boundaries": [
                "no_diagnostic_claims",
                "no_therapeutic_guarantees",
                "maintain_realistic_expectations",
                "respect_professional_limitations"
            ]
        }
    }

def create_depression_nlp_test_config(api_key: str) -> dict:
    """Конфигурация для теста депрессии с NLP элементами."""

    base_config = create_psychology_nlp_config(api_key)

    base_config.update({
        "specific_focus": "depression",
        "test_structure": {
            "question_count": 16,
            "answer_format": "3_point_scale",
            "severity_levels": [
                {"level": "minimal", "range": "0-7", "nlp_response": "anchoring_hope"},
                {"level": "mild", "range": "8-15", "nlp_response": "gentle_reframing"},
                {"level": "moderate", "range": "16-25", "nlp_response": "resource_activation"},
                {"level": "severe", "range": "26+", "nlp_response": "professional_referral"}
            ]
        },

        "nlp_question_examples": [
            {
                "id": 1,
                "base_text": "Коли ви думаєте про майбутнє",
                "nlp_techniques": ["presupposition", "embedded_command"],
                "ericksonian_version": "Коли ви думаєте про майбутнє (презумпція), що першого **відчуваєте** щодо можливостей (встроена команда)?",
                "vak_adaptations": {
                    "visual": "...які образи приходять на думку?",
                    "auditory": "...що говорить внутрішній голос?",
                    "kinesthetic": "...які відчуття з'являються?"
                }
            },
            {
                "id": 2,
                "base_text": "Ваш настрій протягом дня",
                "nlp_techniques": ["utilization", "reframing"],
                "ericksonian_version": "Настрій природно змінюється (трюізм), і ви можете **помітити** моменти легкості (утилізація + встроена команда)",
                "therapeutic_reframe": "Коливання настрою = здатність до змін"
            }
        ]
    })

    return base_config

def create_anxiety_nlp_program_config(api_key: str) -> dict:
    """Конфигурация для программы работы с тревогой через NLP."""

    return {
        "program_type": "anxiety_transformation",
        "duration": 21,
        "domain": "psychology",

        "nlp_program_structure": {
            "phase_1_destabilization": {
                "days": "1-7",
                "nlp_focus": "anxiety_reframing",
                "techniques": ["context_reframing", "anxiety_anchoring", "breathing_patterns"],
                "ericksonian_elements": [
                    "Тревога - это сигнал (трюизм)",
                    "Тело знает, как успокоиться (презумпция)",
                    "Дыхание может стать **якорем** спокойствия (встроенная команда)"
                ]
            },

            "phase_2_transformation": {
                "days": "8-14",
                "nlp_focus": "resource_installation",
                "techniques": ["resource_anchoring", "future_pacing", "confidence_modeling"],
                "daily_exercises": [
                    {"name": "Morning Resource Anchor", "nlp_technique": "kinesthetic_anchoring"},
                    {"name": "Confidence Visualization", "nlp_technique": "visual_rehearsal"},
                    {"name": "Evening Integration", "nlp_technique": "auditory_affirmations"}
                ]
            },

            "phase_3_integration": {
                "days": "15-21",
                "nlp_focus": "future_pacing",
                "techniques": ["ecological_check", "maintenance_anchors", "success_programming"],
                "integration_elements": [
                    "Спокій стає частиною вас (презумпція интеграції)",
                    "Навички автоматично **активуються** (встроенная команда)",
                    "Уверенность растет с каждым днем (прогрессивная презумпція)"
                ]
            }
        },

        "vak_program_adaptations": {
            "visual_track": {
                "exercises": ["guided_imagery", "color_therapy", "visual_anchors"],
                "metaphors": ["светлое будущее", "ясная перспектива", "радужный спектр эмоций"]
            },
            "auditory_track": {
                "exercises": ["self_talk_reframing", "sound_anchoring", "rhythmic_breathing"],
                "metaphors": ["внутренняя мелодия покоя", "голос уверенности", "ритм спокойствия"]
            },
            "kinesthetic_track": {
                "exercises": ["body_awareness", "movement_therapy", "touch_anchoring"],
                "metaphors": ["поток спокойствия", "сила земли", "тепло уверенности"]
            }
        }
    }

# Пример использования
if __name__ == "__main__":
    # Базовая психологическая конфигурация
    psychology_config = create_psychology_nlp_config("your-api-key")

    # Специализированная конфигурация для депрессии
    depression_config = create_depression_nlp_test_config("your-api-key")

    # Программа трансформации тревоги
    anxiety_program_config = create_anxiety_nlp_program_config("your-api-key")

    print("Psychology NLP configurations created successfully!")