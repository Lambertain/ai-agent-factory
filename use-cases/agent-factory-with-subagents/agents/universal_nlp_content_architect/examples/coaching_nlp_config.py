"""
Coaching NLP Configuration Example
Пример конфигурации для коучинга с NLP техниками
"""

from ..dependencies import UniversalNLPDependencies
from ..settings import create_universal_nlp_settings

def create_coaching_nlp_config(api_key: str) -> dict:
    """Создать конфигурацию для коучингового NLP контента."""

    return {
        "domain": "coaching",
        "settings": {
            "excellence_threshold": 88.0,  # Высокие требования для коучинга
            "require_scientific_basis": True,  # Коучинг основан на психологии
            "enable_goal_validation": True,
            "validate_coaching_ethics": True,
            "enable_progress_tracking": True,

            # NLP коучинговые требования
            "integrate_advanced_nlp": True,
            "enable_outcome_orientation": True,
            "require_empowerment_focus": True,
            "validate_ecological_check": True,

            # Коучинговые принципы
            "respect_client_autonomy": True,
            "focus_on_solutions": True,
            "encourage_self_discovery": True,
            "maintain_professional_boundaries": True,

            # Безопасность
            "stay_within_coaching_scope": True,
            "provide_clear_agreements": True,
            "avoid_therapy_overlap": True,
            "focus_on_future_goals": True
        },

        "nlp_techniques": {
            "primary": [
                "outcome_specification",
                "resource_anchoring",
                "reframing_obstacles",
                "modeling_excellence",
                "future_pacing"
            ],
            "advanced": [
                "meta_programs_coaching",
                "logical_levels_alignment",
                "timeline_goal_setting",
                "parts_integration_coaching",
                "belief_change_coaching"
            ],
            "ericksonian": [
                "success_metaphors",
                "achievement_embedded_commands",
                "growth_truisms",
                "progress_utilization",
                "transformation_confusion"
            ]
        },

        "content_examples": {
            "goal_setting_session": {
                "title": "Дизайн твоего успешного будущего",
                "approach": "outcome_focused",
                "sample_process": {
                    "text": "Цели **становятся** реальными, когда мы их четко определяем (трюизм + встроенная команда)",
                    "nlp_integration": "outcome_metaphor + achievement_presupposition",
                    "vak_visual": "...видишь яркую картину своих достижений",
                    "vak_auditory": "...слышишь звуки успеха",
                    "vak_kinesthetic": "...чувствуешь энергию движения к цели"
                }
            },
            "obstacle_reframing": {
                "traditional": "У меня есть препятствия на пути к цели",
                "nlp_reframe": "Препятствия **показывают** путь к развитию новых навыков (утилизация + встроенная команда)",
                "empowerment_focus": "Каждый вызов - возможность стать сильнее"
            }
        },

        "vak_coaching_adaptations": {
            "visual": {
                "keywords": ["бачиш", "яскраво", "фокус", "перспектива", "картина"],
                "success_metaphors": ["яскраве майбутнє", "чітка мета", "широка перспектива"],
                "visual_techniques": ["goal_visualization", "success_imagery", "progress_charts"]
            },
            "auditory": {
                "keywords": ["чуєш", "звучить", "резонує", "відгук", "внутрішній голос"],
                "success_metaphors": ["голос успіху", "музика досягнень", "резонанс цілей"],
                "auditory_techniques": ["success_affirmations", "internal_dialogue", "goal_mantras"]
            },
            "kinesthetic": {
                "keywords": ["відчуваєш", "рух", "енергія", "імпульс", "сила"],
                "success_metaphors": ["енергія досягнень", "імпульс росту", "сила мотивації"],
                "kinesthetic_techniques": ["kinesthetic_anchoring", "energy_work", "movement_goals"]
            }
        },

        "coaching_methodologies": {
            "grow_model": {
                "goal": {
                    "nlp_focus": "outcome_specification",
                    "ericksonian_pattern": "Четкая цель **магнитом** притягивает возможности (метафора притяжения + команда)",
                    "empowerment_theme": "ясность намерения создает фокус"
                },
                "reality": {
                    "nlp_focus": "current_state_assessment",
                    "ericksonian_pattern": "Честность с собой **освобождает** энергию для изменений (трюизм + команда)",
                    "empowerment_theme": "принятие реальности - первый шаг к изменениям"
                },
                "options": {
                    "nlp_focus": "creative_problem_solving",
                    "ericksonian_pattern": "Разум **находит** решения, когда мы открыты возможностям (презумпция + команда)",
                    "empowerment_theme": "множество путей ведут к успеху"
                },
                "will": {
                    "nlp_focus": "commitment_anchoring",
                    "ericksonian_pattern": "Решимость **превращает** мечты в планы (трансформация + команда)",
                    "empowerment_theme": "воля к действию создает результаты"
                }
            }
        },

        "logical_levels_coaching": {
            "environment": {
                "coaching_focus": "context_optimization",
                "nlp_technique": "environmental_anchoring",
                "question_pattern": "Какая обстановка **поддерживает** твой успех? (пресуппозиция поддержки + команда)"
            },
            "behavior": {
                "coaching_focus": "action_planning",
                "nlp_technique": "behavior_modeling",
                "question_pattern": "Какие действия **приближают** тебя к цели? (движение + команда)"
            },
            "capabilities": {
                "coaching_focus": "skill_development",
                "nlp_technique": "competence_anchoring",
                "question_pattern": "Какие навыки **развиваются** в процессе достижения цели? (рост + презумпция)"
            },
            "beliefs": {
                "coaching_focus": "empowering_beliefs",
                "nlp_technique": "belief_installation",
                "question_pattern": "Во что ты **веришь** о своих возможностях? (вера + расширение)"
            },
            "identity": {
                "coaching_focus": "identity_evolution",
                "nlp_technique": "identity_anchoring",
                "question_pattern": "Кем ты **становишься**, достигая эту цель? (трансформация + команда)"
            },
            "purpose": {
                "coaching_focus": "meaning_connection",
                "nlp_technique": "purpose_anchoring",
                "question_pattern": "Как эта цель **служит** твоей высшей миссии? (служение + связь)"
            }
        },

        "coaching_safety_framework": {
            "empowerment_principles": [
                "client_is_naturally_creative_and_whole",
                "focus_on_client_agenda_not_coach_agenda",
                "trust_client_inner_wisdom",
                "support_self_directed_learning"
            ],
            "ethical_guidelines": [
                "maintain_professional_boundaries",
                "stay_within_coaching_competency",
                "respect_client_autonomy",
                "provide_clear_coaching_agreement"
            ],
            "referral_indicators": [
                "therapeutic_issues_emerge",
                "trauma_processing_needed",
                "mental_health_concerns",
                "addiction_recovery_issues"
            ]
        }
    }

def create_life_coaching_nlp_config(api_key: str) -> dict:
    """Конфигурация для лайф-коучинга с NLP техниками."""

    base_config = create_coaching_nlp_config(api_key)

    base_config.update({
        "coaching_type": "life_coaching",
        "nlp_life_coaching_elements": {
            "life_wheel_assessment": {
                "nlp_approach": "holistic_balance",
                "ericksonian_frame": "Жизнь **стремится** к гармонии во всех сферах (естественность + команда)",
                "empowerment_message": "Баланс создает устойчивый успех"
            },
            "values_clarification": {
                "nlp_approach": "core_values_anchoring",
                "ericksonian_frame": "Ценности **направляют** к аутентичным решениям (навигация + команда)",
                "empowerment_message": "Жизнь по ценностям приносит глубокое удовлетворение"
            },
            "life_purpose_discovery": {
                "nlp_approach": "purpose_emergence",
                "ericksonian_frame": "Предназначение **раскрывается** через осознанность (процесс + команда)",
                "empowerment_message": "Твоя уникальная миссия ждет воплощения"
            }
        },

        "transformation_phases": {
            "awareness_phase": {
                "duration": "weeks 1-2",
                "nlp_focus": "current_state_mapping",
                "techniques": ["life_wheel", "values_assessment", "limiting_beliefs_identification"],
                "ericksonian_elements": [
                    "Осознанность **пробуждает** возможности изменений (пробуждение + команда)",
                    "Честность с собой открывает двери к росту (метафора открытия)",
                    "Каждое осознание приносит новую силу (трюизм о росте)"
                ]
            },
            "goal_setting_phase": {
                "duration": "weeks 3-4",
                "nlp_focus": "desired_state_creation",
                "techniques": ["smart_goals", "vision_boarding", "future_self_visualization"],
                "ericksonian_elements": [
                    "Ясные цели **магнитом** притягивают ресурсы (метафора притяжения + команда)",
                    "Видение будущего мотивирует настоящее (связь времен)",
                    "Мечты становятся планами, планы - реальностью (трансформационная цепочка)"
                ]
            },
            "action_phase": {
                "duration": "weeks 5-10",
                "nlp_focus": "behavioral_change",
                "techniques": ["habit_formation", "accountability_systems", "progress_tracking"],
                "ericksonian_elements": [
                    "Маленькие шаги **создают** большие изменения (накопление + команда)",
                    "Действие порождает уверенность (причинно-следственная связь)",
                    "Прогресс **ускоряется** с каждым достижением (прогрессия + команда)"
                ]
            },
            "integration_phase": {
                "duration": "weeks 11-12",
                "nlp_focus": "sustainable_change",
                "techniques": ["identity_integration", "maintenance_planning", "success_anchoring"],
                "ericksonian_elements": [
                    "Новые привычки **становятся** частью личности (интеграция + команда)",
                    "Успех создает устойчивость к вызовам (сила через достижения)",
                    "Рост **продолжается** за пределами коучинга (будущее + команда)"
                ]
            }
        }
    })

    return base_config

def create_business_coaching_nlp_config(api_key: str) -> dict:
    """Конфигурация для бизнес-коучинга с NLP."""

    return {
        "coaching_type": "business_coaching",
        "domain": "coaching",
        "nlp_methodology": "business_excellence",

        "business_coaching_areas": {
            "leadership_development": {
                "nlp_techniques": ["leadership_modeling", "influence_patterns", "team_rapport"],
                "ericksonian_elements": [
                    "Лидеры **вдохновляют** других на достижения (естественность лидерства + команда)",
                    "Влияние растет через служение команде (парадокс влияния)",
                    "Лучшие решения **рождаются** в атмосфере доверия (создание + команда)"
                ],
                "empowerment_focus": "Развитие аутентичного лидерского стиля"
            },

            "performance_optimization": {
                "nlp_techniques": ["excellence_modeling", "peak_state_anchoring", "outcome_focus"],
                "performance_areas": {
                    "productivity_enhancement": "Эффективность **возрастает** при ясности приоритетов (рост + команда)",
                    "decision_making": "Лучшие решения **приходят** из интуиции и анализа (баланс + процесс)",
                    "stress_management": "Спокойствие **создает** пространство для мудрых действий (созидание + команда)"
                },
                "empowerment_focus": "Достижение устойчиво высокой производительности"
            },

            "strategic_planning": {
                "nlp_techniques": ["strategic_thinking", "systems_modeling", "future_pacing"],
                "planning_elements": [
                    "Стратегия **объединяет** видение с действием (интеграция + команда)",
                    "Гибкость планов обеспечивает устойчивость к изменениям (адаптивность)",
                    "Успех **достигается** через последовательные шаги (процесс + команда)"
                ],
                "empowerment_focus": "Создание адаптивных стратегий роста"
            }
        },

        "vak_business_coaching": {
            "visual_business": {
                "techniques": ["strategic_visualization", "process_mapping", "dashboard_creation"],
                "business_metaphors": [
                    "Ясная картина бизнес-целей",
                    "Визуальный контроль показателей",
                    "Схема оптимальных процессов"
                ]
            },
            "auditory_business": {
                "techniques": ["feedback_systems", "communication_optimization", "team_dialogue"],
                "business_metaphors": [
                    "Музыка слаженной команды",
                    "Резонанс корпоративных ценностей",
                    "Диалог с рынком и клиентами"
                ]
            },
            "kinesthetic_business": {
                "techniques": ["hands_on_learning", "experiential_exercises", "action_planning"],
                "business_metaphors": [
                    "Ощущение пульса рынка",
                    "Энергия команды в действии",
                    "Движение к бизнес-целям"
                ]
            }
        }
    }

def create_wellness_coaching_nlp_config(api_key: str) -> dict:
    """Конфигурация для велнес-коучинга с NLP."""

    return {
        "coaching_type": "wellness_coaching",
        "domain": "coaching",
        "nlp_methodology": "holistic_wellness",

        "wellness_dimensions": {
            "physical_wellness": {
                "nlp_approach": "body_wisdom_connection",
                "ericksonian_frame": "Тело **знает**, что ему нужно для здоровья (телесная мудрость + команда)",
                "empowerment_theme": "доверие естественным потребностям тела"
            },
            "mental_wellness": {
                "nlp_approach": "mindful_thinking",
                "ericksonian_frame": "Разум **находит** покой в осознанности (поиск покоя + команда)",
                "empowerment_theme": "культивирование ментальной ясности"
            },
            "emotional_wellness": {
                "nlp_approach": "emotional_intelligence",
                "ericksonian_frame": "Эмоции **направляют** к важным потребностям (навигация + команда)",
                "empowerment_theme": "эмоциональная мудрость и интеграция"
            },
            "spiritual_wellness": {
                "nlp_approach": "meaning_connection",
                "ericksonian_frame": "Дух **стремится** к связи с большим (естественное стремление + команда)",
                "empowerment_theme": "поиск смысла и духовного роста"
            }
        },

        "wellness_coaching_tools": {
            "habit_formation": {
                "nlp_techniques": ["anchoring_healthy_habits", "environmental_design", "identity_based_change"],
                "wellness_applications": [
                    "Здоровые привычки **формируются** через постоянство и радость (процесс + команда)",
                    "Окружение поддерживает или препятствует изменениям (экологический фактор)",
                    "Изменение идентичности создает устойчивые результаты (глубинное изменение)"
                ]
            },
            "stress_management": {
                "nlp_techniques": ["state_management", "reframing_stressors", "resource_anchoring"],
                "stress_reframes": [
                    "Стресс **сигнализирует** о необходимости заботы о себе (переосмысление + команда)",
                    "Напряжение показывает области для развития устойчивости (рост через вызовы)",
                    "Расслабление **восстанавливает** естественный баланс (восстановление + команда)"
                ]
            }
        }
    }

# Пример использования
if __name__ == "__main__":
    # Базовая коучинговая конфигурация
    coaching_config = create_coaching_nlp_config("your-api-key")

    # Лайф-коучинг с NLP
    life_coaching_config = create_life_coaching_nlp_config("your-api-key")

    # Бизнес-коучинг
    business_config = create_business_coaching_nlp_config("your-api-key")

    # Велнес-коучинг
    wellness_config = create_wellness_coaching_nlp_config("your-api-key")

    print("Coaching NLP configurations created successfully!")