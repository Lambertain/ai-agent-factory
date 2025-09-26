"""
Wellness NLP Configuration Example
Пример конфигурации для велнес/медитации с NLP техниками
"""

from ..dependencies import UniversalNLPDependencies
from ..settings import create_universal_nlp_settings

def create_wellness_nlp_config(api_key: str) -> dict:
    """Создать конфигурацию для велнес NLP контента."""

    return {
        "domain": "wellness",
        "settings": {
            "excellence_threshold": 86.0,  # Высокие требования для здоровья
            "require_scientific_basis": True,  # Основано на исследованиях
            "enable_safety_validation": True,
            "validate_medical_boundaries": True,
            "enable_holistic_approach": True,

            # NLP велнес требования
            "integrate_mind_body_nlp": True,
            "enable_healing_metaphors": True,
            "require_empowerment_focus": True,
            "validate_safety_first": True,

            # Велнес принципы
            "respect_body_wisdom": True,
            "avoid_medical_claims": True,
            "encourage_professional_guidance": True,
            "honor_individual_differences": True,

            # Безопасность
            "provide_modification_options": True,
            "respect_physical_limitations": True,
            "include_contraindication_warnings": True,
            "promote_gradual_progress": True
        },

        "nlp_techniques": {
            "primary": [
                "body_awareness_anchoring",
                "healing_visualization",
                "energy_reframing",
                "wellness_rapport",
                "holistic_integration"
            ],
            "advanced": [
                "chakra_balancing_nlp",
                "breathwork_programming",
                "energy_healing_patterns",
                "mindfulness_anchoring",
                "wellness_timeline_work"
            ],
            "ericksonian": [
                "healing_metaphors",
                "wellness_embedded_commands",
                "body_wisdom_truisms",
                "natural_healing_utilization",
                "gentle_transformation_confusion"
            ]
        },

        "content_examples": {
            "meditation_program": {
                "title": "Путешествие к внутреннему покою",
                "approach": "gentle_guidance",
                "sample_instruction": {
                    "text": "Дыхание **течет** естественно, принося покой с каждым вдохом (естественность + встроенная команда)",
                    "nlp_integration": "natural_metaphor + breath_command",
                    "vak_visual": "...видишь мягкий свет внутреннего спокойствия",
                    "vak_auditory": "...слышишь тишину между мыслями",
                    "vak_kinesthetic": "...чувствуешь расслабление, распространяющееся по телу"
                }
            },
            "stress_relief_technique": {
                "traditional": "Стресс вредит здоровью",
                "nlp_reframe": "Напряжение **указывает** на области, которым нужна забота (утилизация + встроенная команда)",
                "empowerment_focus": "Стресс как компас для заботы о себе"
            }
        },

        "vak_wellness_adaptations": {
            "visual": {
                "keywords": ["бачиш", "світло", "сяйво", "кольори", "образи"],
                "healing_metaphors": ["світло зцілення", "райдужні енергії", "яскравість здоров'я"],
                "visual_techniques": ["color_healing", "light_visualization", "chakra_colors"]
            },
            "auditory": {
                "keywords": ["чуєш", "звуки", "тиша", "вібрації", "резонанс"],
                "healing_metaphors": ["музика зцілення", "тиша спокою", "вібрації здоров'я"],
                "auditory_techniques": ["sound_healing", "mantra_meditation", "silence_practice"]
            },
            "kinesthetic": {
                "keywords": ["відчуваєш", "тепло", "енергія", "потік", "легкість"],
                "healing_metaphors": ["потік зцілення", "тепло любові", "легкість буття"],
                "kinesthetic_techniques": ["energy_sensing", "body_scanning", "touch_healing"]
            }
        },

        "wellness_modalities": {
            "meditation": {
                "nlp_focus": "mindfulness_anchoring",
                "ericksonian_pattern": "Ум **находит** покой в настоящем моменте (поиск покоя + команда)",
                "empowerment_theme": "внутренняя тишина как источник мудрости",
                "techniques": ["breath_meditation", "body_scan", "loving_kindness", "visualization"]
            },
            "breathwork": {
                "nlp_focus": "breath_state_management",
                "ericksonian_pattern": "Дыхание **соединяет** тело и разум в гармонии (связь + команда)",
                "empowerment_theme": "дыхание как мост к исцелению",
                "techniques": ["pranayama", "box_breathing", "holotropic_breathwork", "breath_retention"]
            },
            "energy_healing": {
                "nlp_focus": "energy_flow_awareness",
                "ericksonian_pattern": "Энергия **течет** туда, где нужно исцеление (направление + команда)",
                "empowerment_theme": "естественная способность к самоисцелению",
                "techniques": ["reiki_principles", "chakra_balancing", "aura_cleansing", "crystal_healing"]
            },
            "movement_therapy": {
                "nlp_focus": "embodied_healing",
                "ericksonian_pattern": "Тело **помнит** как быть здоровым и сильным (память тела + команда)",
                "empowerment_theme": "движение как лекарство",
                "techniques": ["yoga_therapy", "dance_movement", "qigong", "tai_chi"]
            }
        },

        "chakra_nlp_integration": {
            "root_chakra": {
                "location": "base_of_spine",
                "nlp_focus": "grounding_and_safety",
                "ericksonian_pattern": "Корни **укрепляются** в земле стабильности (укрепление + команда)",
                "healing_affirmation": "Я в безопасности и надежно заземлен",
                "color_healing": "красный - энергия жизненной силы"
            },
            "sacral_chakra": {
                "location": "lower_abdomen",
                "nlp_focus": "creativity_and_pleasure",
                "ericksonian_pattern": "Творчество **течет** свободно из центра удовольствия (поток + команда)",
                "healing_affirmation": "Я открыт для радости и творческого выражения",
                "color_healing": "оранжевый - энергия творчества"
            },
            "solar_plexus": {
                "location": "upper_abdomen",
                "nlp_focus": "personal_power",
                "ericksonian_pattern": "Внутренний огонь **зажигает** уверенность в себе (активация + команда)",
                "healing_affirmation": "Я обладаю силой создавать свою реальность",
                "color_healing": "желтый - энергия личной силы"
            },
            "heart_chakra": {
                "location": "center_of_chest",
                "nlp_focus": "love_and_compassion",
                "ericksonian_pattern": "Сердце **открывается** для безусловной любви (открытие + команда)",
                "healing_affirmation": "Я даю и принимаю любовь свободно",
                "color_healing": "зеленый - энергия исцеляющей любви"
            },
            "throat_chakra": {
                "location": "throat_area",
                "nlp_focus": "authentic_expression",
                "ericksonian_pattern": "Голос **звучит** с истиной и мудростью (звучание + команда)",
                "healing_affirmation": "Я выражаю свою истину с любовью",
                "color_healing": "голубой - энергия истинного выражения"
            },
            "third_eye": {
                "location": "forehead_center",
                "nlp_focus": "intuitive_wisdom",
                "ericksonian_pattern": "Интуиция **освещает** путь к мудрости (освещение + команда)",
                "healing_affirmation": "Я доверяю своей внутренней мудрости",
                "color_healing": "индиго - энергия интуитивного знания"
            },
            "crown_chakra": {
                "location": "top_of_head",
                "nlp_focus": "spiritual_connection",
                "ericksonian_pattern": "Дух **соединяется** с бесконечностью мудрости (связь + команда)",
                "healing_affirmation": "Я един со вселенской мудростью",
                "color_healing": "фиолетовый - энергия духовного единства"
            }
        },

        "wellness_safety_framework": {
            "empowerment_principles": [
                "body_wisdom_is_primary_guide",
                "gradual_progress_over_quick_fixes",
                "individual_needs_vary_greatly",
                "professional_guidance_when_needed"
            ],
            "safety_guidelines": [
                "never_ignore_pain_or_discomfort",
                "modify_practices_for_limitations",
                "consult_healthcare_for_conditions",
                "respect_personal_boundaries_always"
            ],
            "contraindication_awareness": [
                "pregnancy_specific_modifications",
                "injury_appropriate_adaptations",
                "medication_interaction_considerations",
                "mental_health_sensitivity_required"
            ]
        }
    }

def create_meditation_program_nlp_config(api_key: str) -> dict:
    """Конфигурация для программы медитации с NLP."""

    base_config = create_wellness_nlp_config(api_key)

    base_config.update({
        "program_type": "meditation_journey",
        "duration_days": 21,
        "nlp_meditation_structure": {
            "week_1_foundation": {
                "days": "1-7",
                "nlp_focus": "awareness_cultivation",
                "techniques": ["breath_awareness", "body_scanning", "present_moment_anchoring"],
                "ericksonian_elements": [
                    "Осознанность **развивается** с каждым моментом внимания (развитие + команда)",
                    "Дыхание естественно углубляется в покое (естественность)",
                    "Тело **знает**, как расслабляться полностью (телесная мудрость + команда)"
                ],
                "daily_progression": [
                    {"day": 1, "focus": "breath_introduction", "duration": "5 минут"},
                    {"day": 2, "focus": "body_awareness", "duration": "7 минут"},
                    {"day": 7, "focus": "integrated_awareness", "duration": "15 минут"}
                ]
            },

            "week_2_deepening": {
                "days": "8-14",
                "nlp_focus": "deeper_states_access",
                "techniques": ["visualization_meditation", "mantra_practice", "loving_kindness"],
                "ericksonian_elements": [
                    "Глубина **приходит** через терпеливое погружение (процесс + команда)",
                    "Сердце открывается для собственной доброты (естественное открытие)",
                    "Визуализация **создает** внутренние пространства покоя (созидание + команда)"
                ],
                "advanced_techniques": [
                    "guided_imagery_healing",
                    "chakra_visualization",
                    "light_meditation"
                ]
            },

            "week_3_integration": {
                "days": "15-21",
                "nlp_focus": "mindful_living_integration",
                "techniques": ["walking_meditation", "mindful_eating", "daily_life_awareness"],
                "ericksonian_elements": [
                    "Медитация **переходит** в каждый момент жизни (интеграция + команда)",
                    "Осознанность становится естественным состоянием (естественность развития)",
                    "Покой **сопровождает** в любой деятельности (постоянство + команда)"
                ],
                "life_integration": [
                    "mindful_communication",
                    "conscious_decision_making",
                    "stress_response_transformation"
                ]
            }
        }
    })

    return base_config

def create_energy_healing_nlp_config(api_key: str) -> dict:
    """Конфигурация для энергетического исцеления с NLP."""

    return {
        "healing_type": "energy_healing",
        "domain": "wellness",
        "nlp_methodology": "energy_flow_optimization",

        "energy_healing_phases": {
            "assessment_phase": {
                "nlp_techniques": ["energy_sensing", "intuitive_scanning", "chakra_assessment"],
                "ericksonian_elements": [
                    "Руки **чувствуют** энергетические поля естественно (естественная способность + команда)",
                    "Интуиция направляет к областям, нуждающимся в исцелении (навигация)",
                    "Энергия показывает свои паттерны чувствительным рукам (проявление)"
                ],
                "empowerment_focus": "Развитие врожденной чувствительности к энергии"
            },

            "balancing_phase": {
                "nlp_techniques": ["energy_directing", "chakra_balancing", "auric_cleansing"],
                "healing_approaches": {
                    "chakra_spinning": "Чакры **вращаются** в гармоничном ритме (естественная гармония + команда)",
                    "energy_clearing": "Блоки **растворяются** в потоке исцеляющей энергии (трансформация + команда)",
                    "light_infusion": "Свет **наполняет** каждую клетку здоровьем (наполнение + команда)"
                },
                "empowerment_focus": "Активация естественных способностей к самоисцелению"
            },

            "integration_phase": {
                "nlp_techniques": ["energy_grounding", "healing_anchoring", "maintenance_programming"],
                "integration_elements": [
                    "Исцеление **интегрируется** на всех уровнях бытия (интеграция + команда)",
                    "Новые энергетические паттерны стабилизируются (стабилизация)",
                    "Здоровье **поддерживается** естественными ритмами тела (поддержка + команда)"
                ],
                "empowerment_focus": "Поддержание длительного энергетического баланса"
            }
        },

        "vak_energy_healing": {
            "visual_healing": {
                "techniques": ["color_healing", "light_visualization", "aura_seeing"],
                "healing_visualizations": [
                    "Золотой свет исцеления",
                    "Радужные потоки энергии",
                    "Кристально чистая аура"
                ]
            },
            "auditory_healing": {
                "techniques": ["sound_healing", "frequency_therapy", "mantra_healing"],
                "healing_sounds": [
                    "Исцеляющие частоты",
                    "Мантры для чакр",
                    "Музыка сфер"
                ]
            },
            "kinesthetic_healing": {
                "techniques": ["hands_on_healing", "energy_touch", "vibration_sensing"],
                "healing_sensations": [
                    "Тепло исцеляющих рук",
                    "Покалывание энергии",
                    "Поток жизненной силы"
                ]
            }
        }
    }

def create_holistic_wellness_program_nlp_config(api_key: str) -> dict:
    """Конфигурация для комплексной программы велнеса с NLP."""

    return {
        "program_type": "holistic_wellness",
        "domain": "wellness",
        "duration_weeks": 12,
        "nlp_methodology": "whole_person_transformation",

        "wellness_dimensions": {
            "physical_wellness": {
                "weeks": "1-3",
                "nlp_focus": "body_appreciation",
                "components": ["nutrition_mindfulness", "movement_joy", "sleep_optimization"],
                "ericksonian_elements": [
                    "Тело **благодарно** отвечает на заботливое внимание (благодарность + ответ)",
                    "Движение приносит радость, когда мы слушаем потребности тела (условие радости)",
                    "Сон **восстанавливает** на глубочайшем уровне (восстановление + команда)"
                ]
            },
            "emotional_wellness": {
                "weeks": "4-6",
                "nlp_focus": "emotional_intelligence",
                "components": ["emotion_regulation", "stress_transformation", "joy_cultivation"],
                "ericksonian_elements": [
                    "Эмоции **несут** важные послания о потребностях (информационная функция + команда)",
                    "Стресс трансформируется в энергию роста (трансформация)",
                    "Радость **возникает** из принятия себя (источник + команда)"
                ]
            },
            "mental_wellness": {
                "weeks": "7-9",
                "nlp_focus": "cognitive_flexibility",
                "components": ["thought_awareness", "belief_updating", "mental_clarity"],
                "ericksonian_elements": [
                    "Мысли **меняются**, когда мы становимся их наблюдателем (изменение + команда)",
                    "Убеждения обновляются в свете нового опыта (естественное обновление)",
                    "Ясность **приходит** через практику осознанности (приход + команда)"
                ]
            },
            "spiritual_wellness": {
                "weeks": "10-12",
                "nlp_focus": "meaning_connection",
                "components": ["purpose_discovery", "gratitude_practice", "interconnection_awareness"],
                "ericksonian_elements": [
                    "Предназначение **раскрывается** через служение другим (раскрытие + команда)",
                    "Благодарность умножает то, что мы ценим (закон благодарности)",
                    "Связь со всем живым **питает** душу (питание + команда)"
                ]
            }
        }
    }

# Пример использования
if __name__ == "__main__":
    # Базовая велнес конфигурация
    wellness_config = create_wellness_nlp_config("your-api-key")

    # Программа медитации с NLP
    meditation_config = create_meditation_program_nlp_config("your-api-key")

    # Энергетическое исцеление
    healing_config = create_energy_healing_nlp_config("your-api-key")

    # Комплексная программа велнеса
    holistic_config = create_holistic_wellness_program_nlp_config("your-api-key")

    print("Wellness NLP configurations created successfully!")