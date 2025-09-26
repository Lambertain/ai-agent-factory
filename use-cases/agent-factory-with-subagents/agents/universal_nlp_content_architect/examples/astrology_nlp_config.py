"""
Astrology NLP Configuration Example
Пример конфигурации для астрологического домена с NLP техниками
"""

from ..dependencies import UniversalNLPDependencies
from ..settings import create_universal_nlp_settings

def create_astrology_nlp_config(api_key: str) -> dict:
    """Создать конфигурацию для астрологического NLP контента."""

    return {
        "domain": "astrology",
        "settings": {
            "excellence_threshold": 78.0,  # Умеренные требования для символических систем
            "require_scientific_basis": False,  # Астрология - символическая система
            "enable_cultural_validation": True,
            "validate_cultural_sensitivity": True,
            "enable_ethical_guidance": True,

            # NLP астрологические требования
            "integrate_cosmic_metaphors": True,
            "enable_archetypal_nlp": True,
            "require_empowerment_focus": True,
            "validate_symbolic_accuracy": True,

            # Астрологические принципы
            "respect_free_will": True,
            "avoid_fatalistic_predictions": True,
            "encourage_personal_growth": True,
            "honor_astrological_tradition": True,

            # Безопасность
            "avoid_medical_predictions": True,
            "avoid_financial_guarantees": True,
            "require_entertainment_disclaimers": True,
            "promote_self_responsibility": True
        },

        "nlp_techniques": {
            "primary": [
                "metaphorical_modeling",
                "temporal_anchoring",
                "archetypal_integration",
                "energy_reframing",
                "cosmic_rapport"
            ],
            "advanced": [
                "planetary_timeline_work",
                "astrological_parts_work",
                "karmic_reframing",
                "destiny_presuppositions",
                "cosmic_future_pacing"
            ],
            "ericksonian": [
                "cosmic_metaphors",
                "planetary_embedded_commands",
                "celestial_truisms",
                "karmic_utilization",
                "astrological_confusion"
            ]
        },

        "content_examples": {
            "natal_chart_analysis": {
                "title": "Твоя звездная карта возможностей",
                "approach": "empowerment_focused",
                "sample_interpretation": {
                    "text": "Как планеты движутся в своих орбитах (трюизм), так и твои таланты **раскрываются** в нужное время (презумпция + встроенная команда)",
                    "nlp_integration": "cosmic_metaphor + temporal_presupposition",
                    "vak_visual": "...видишь звездную карту своих возможностей",
                    "vak_auditory": "...слышишь зов своего предназначения",
                    "vak_kinesthetic": "...чувствуешь поток космической энергии"
                }
            },
            "mercury_retrograde_reframe": {
                "traditional": "Меркурий ретроградный - проблемы с коммуникацией",
                "nlp_reframe": "Меркурий дает возможность **пересмотреть** и **улучшить** твои способы общения (встроенные команды)",
                "empowerment_focus": "Период внутреннего диалога и мудрых решений"
            }
        },

        "vak_astrology_adaptations": {
            "visual": {
                "keywords": ["бачиш", "яскраво", "зірки", "світло", "кольори"],
                "cosmic_metaphors": ["зоряна карта можливостей", "яскравість планет", "кольори енергій"],
                "visual_techniques": ["chart_visualization", "color_astrology", "planetary_imagery"]
            },
            "auditory": {
                "keywords": ["чуєш", "музика", "резонанс", "вібрації", "заклик"],
                "cosmic_metaphors": ["музика сфер", "планетарні вібрації", "заклик долі"],
                "auditory_techniques": ["planetary_tones", "cosmic_affirmations", "astro_mantras"]
            },
            "kinesthetic": {
                "keywords": ["відчуваєш", "енергія", "потік", "вібрація", "притягання"],
                "cosmic_metaphors": ["потік планетарних енергій", "вібрації знаків", "притягання цілей"],
                "kinesthetic_techniques": ["energy_sensing", "planetary_breathing", "cosmic_movement"]
            }
        },

        "planetary_nlp_correspondences": {
            "sun": {
                "nlp_focus": "identity_anchoring",
                "ericksonian_pattern": "Солнце каждый день **восходит** заново (трюизм + встроенная команда)",
                "empowerment_theme": "личная сила и самовыражение"
            },
            "moon": {
                "nlp_focus": "emotional_integration",
                "ericksonian_pattern": "Как луна проходит свои фазы (метафора), так и эмоции **находят** баланс (утилизация)",
                "empowerment_theme": "интуиция и эмоциональная мудрость"
            },
            "mercury": {
                "nlp_focus": "communication_enhancement",
                "ericksonian_pattern": "Мысли текут как Меркурий (метафора), и **понимание** приходит легко (презумпция)",
                "empowerment_theme": "ясное мышление и общение"
            },
            "venus": {
                "nlp_focus": "relationship_harmony",
                "ericksonian_pattern": "Венера учит **ценить** красоту во всем (трюизм + встроенная команда)",
                "empowerment_theme": "любовь и гармония отношений"
            },
            "mars": {
                "nlp_focus": "action_motivation",
                "ericksonian_pattern": "Марс дает силу **действовать** смело (презумпция + команда)",
                "empowerment_theme": "мужество и инициатива"
            }
        },

        "astrological_safety_framework": {
            "empowerment_principles": [
                "focus_on_potentials_not_limitations",
                "emphasize_choice_and_free_will",
                "provide_constructive_guidance",
                "avoid_fear_based_interpretations"
            ],
            "ethical_guidelines": [
                "no_absolute_predictions",
                "respect_client_autonomy",
                "maintain_entertainment_context",
                "encourage_personal_responsibility"
            ],
            "disclaimer_requirements": [
                "for_entertainment_purposes",
                "not_substitute_for_professional_advice",
                "individual_choice_paramount",
                "symbolic_interpretation_only"
            ]
        }
    }

def create_natal_chart_nlp_analysis_config(api_key: str) -> dict:
    """Конфигурация для NLP анализа натальной карты."""

    base_config = create_astrology_nlp_config(api_key)

    base_config.update({
        "analysis_type": "natal_chart",
        "nlp_chart_elements": {
            "sun_sign": {
                "nlp_approach": "identity_enhancement",
                "ericksonian_frame": "Солнце в твоей карте **освещает** путь к самовыражению",
                "empowerment_message": "Твоя уникальность - это дар миру"
            },
            "moon_sign": {
                "nlp_approach": "emotional_wisdom",
                "ericksonian_frame": "Луна показывает, как сердце **находит** покой",
                "empowerment_message": "Твои эмоции - источник внутренней мудрости"
            },
            "ascendant": {
                "nlp_approach": "presentation_confidence",
                "ericksonian_frame": "Восходящий знак **открывает** двери к новым возможностям",
                "empowerment_message": "Ты естественно привлекаешь подходящие ситуации"
            }
        },

        "aspect_nlp_interpretations": {
            "conjunction": {
                "traditional": "Планеты соединены",
                "nlp_reframe": "Энергии **объединяются** для усиления твоих способностей",
                "empowerment": "Мощная концентрация талантов"
            },
            "opposition": {
                "traditional": "Напряжение между планетами",
                "nlp_reframe": "Создается продуктивная полярность, которая **мотивирует** рост",
                "empowerment": "Баланс противоположностей = мудрость"
            },
            "trine": {
                "traditional": "Гармоничный аспект",
                "nlp_reframe": "Таланты **текут** естественно и легко",
                "empowerment": "Естественные способности и удача"
            }
        }
    })

    return base_config

def create_astrological_coaching_nlp_config(api_key: str) -> dict:
    """Конфигурация для астрологического коучинга с NLP."""

    return {
        "coaching_type": "astrological_empowerment",
        "domain": "astrology",
        "nlp_methodology": "cosmic_transformation",

        "coaching_phases": {
            "chart_exploration": {
                "nlp_techniques": ["cosmic_rapport", "archetypal_anchoring"],
                "ericksonian_elements": [
                    "Твоя карта **рассказывает** историю возможностей (встроенная команда)",
                    "Планеты показывают ресурсы, которые у тебя есть (презумпция)",
                    "Каждый аспект несет подарок (трюизм)"
                ],
                "empowerment_focus": "Обнаружение скрытых талантов"
            },

            "challenge_reframing": {
                "nlp_techniques": ["astrological_reframing", "planetary_utilization"],
                "challenge_transformations": {
                    "saturn_aspects": "Сатурн учит **строить** прочный фундамент успеха",
                    "pluto_transits": "Плутон **трансформирует** то, что больше не служит",
                    "mars_squares": "Марс дает энергию **преодолевать** препятствия"
                },
                "empowerment_focus": "Трансформация препятствий в возможности"
            },

            "future_visioning": {
                "nlp_techniques": ["cosmic_future_pacing", "planetary_goal_setting"],
                "visioning_elements": [
                    "Звезды **направляют** к твоей высшей версии (метафора + команда)",
                    "Транзиты открывают **идеальные** окна возможностей (презумпция)",
                    "Ты **становишься** тем, кем рожден быть (трансформационная команда)"
                ],
                "empowerment_focus": "Создание вдохновляющего будущего"
            }
        },

        "vak_astrological_coaching": {
            "visual_coaching": {
                "techniques": ["chart_visualization", "planetary_imagery", "future_sight"],
                "cosmic_visualizations": [
                    "Твоя звездная карта успеха",
                    "Планетарный путь к целям",
                    "Космическое видение будущего"
                ]
            },
            "auditory_coaching": {
                "techniques": ["planetary_affirmations", "cosmic_dialogue", "astro_mantras"],
                "cosmic_sounds": [
                    "Голос твоего Солнца",
                    "Мелодия планетарной гармонии",
                    "Космический призыв к действию"
                ]
            },
            "kinesthetic_coaching": {
                "techniques": ["planetary_embodiment", "energy_work", "cosmic_movement"],
                "cosmic_sensations": [
                    "Поток солнечной энергии",
                    "Заземляющая сила Сатурна",
                    "Трансформирующий огонь Плутона"
                ]
            }
        }
    }

# Пример использования
if __name__ == "__main__":
    # Базовая астрологическая конфигурация
    astrology_config = create_astrology_nlp_config("your-api-key")

    # Анализ натальной карты с NLP
    natal_chart_config = create_natal_chart_nlp_analysis_config("your-api-key")

    # Астрологический коучинг
    coaching_config = create_astrological_coaching_nlp_config("your-api-key")

    print("Astrology NLP configurations created successfully!")