"""
Зависимости для Pattern Scientific Validator Agent.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class EvidenceBasedResearchDatabase:
    """База данных исследований эффективности психологических интервенций."""

    def __post_init__(self):
        """Инициализация базы данных исследований."""

        # Cognitive Behavioral Therapy (CBT) Evidence
        self.cbt_research = {
            "meta_analyses": [
                {
                    "title": "Efficacy of CBT: A meta-analytic review",
                    "authors": ["Hofmann et al."],
                    "year": 2012,
                    "journal": "Cognitive Therapy and Research",
                    "sample_size": 16000,
                    "effect_size": 0.75,  # Large effect
                    "findings": "CBT показывает большой эффект для тревожных расстройств, депрессии",
                    "self_help_efficacy": 0.60  # Эффект ниже но значимый
                },
                {
                    "title": "The efficacy of cognitive behavioral therapy: A review",
                    "authors": ["Butler et al."],
                    "year": 2006,
                    "journal": "Clinical Psychology Review",
                    "sample_size": 9138,
                    "effect_size": 0.80,
                    "findings": "CBT эффективен для широкого спектра психологических проблем"
                }
            ],
            "techniques": {
                "cognitive_restructuring": {
                    "evidence_level": "meta_analysis",
                    "effect_size": "large (d=0.80)",
                    "validated_for": ["depression", "anxiety", "negative_thinking"],
                    "self_help_adaptation": "effective"
                },
                "behavioral_activation": {
                    "evidence_level": "rct",
                    "effect_size": "large (d=0.78)",
                    "validated_for": ["depression", "low_motivation"],
                    "self_help_adaptation": "highly_effective"
                }
            }
        }

        # NLP Techniques Evidence
        self.nlp_research = {
            "status": "limited_evidence",
            "meta_analyses": [],
            "concerns": [
                "Недостаточно RCT",
                "Малые размеры выборок",
                "Lack of standardization"
            ],
            "techniques": {
                "reframing": {
                    "evidence_level": "expert_opinion",
                    "related_to": "cognitive_restructuring (CBT)",
                    "theoretical_foundation": "Sound - similar to CBT",
                    "safety": "safe",
                    "validation_note": "Механизм overlap с CBT техниками"
                },
                "anchoring": {
                    "evidence_level": "case_studies",
                    "concerns": ["Не валидирован в RCT"],
                    "safety": "safe",
                    "validation_note": "Похож на классическое обусловливание"
                },
                "submodalities": {
                    "evidence_level": "not_validated",
                    "concerns": ["Отсутствие эмпирической поддержки"],
                    "safety": "safe_but_unproven"
                }
            }
        }

        # Mindfulness-Based Interventions
        self.mindfulness_research = {
            "meta_analyses": [
                {
                    "title": "Mindfulness-based therapy: A comprehensive meta-analysis",
                    "authors": ["Khoury et al."],
                    "year": 2013,
                    "journal": "Clinical Psychology Review",
                    "sample_size": 12145,
                    "effect_size": 0.55,  # Medium effect
                    "findings": "Mindfulness эффективен для тревоги, депрессии, stress"
                }
            ],
            "techniques": {
                "mindfulness_meditation": {
                    "evidence_level": "meta_analysis",
                    "effect_size": "medium (d=0.55)",
                    "validated_for": ["anxiety", "depression", "stress", "chronic_pain"],
                    "self_help_adaptation": "effective"
                },
                "body_scan": {
                    "evidence_level": "rct",
                    "effect_size": "medium (d=0.50)",
                    "validated_for": ["stress", "body_awareness"],
                    "safety": "safe"
                }
            }
        }

        # Acceptance and Commitment Therapy (ACT)
        self.act_research = {
            "meta_analyses": [
                {
                    "title": "A meta-analytic review of ACT",
                    "authors": ["A-Tjak et al."],
                    "year": 2015,
                    "journal": "Journal of Consulting and Clinical Psychology",
                    "sample_size": 4000,
                    "effect_size": 0.42,  # Medium effect
                    "findings": "ACT эффективен для широкого спектра состояний"
                }
            ]
        }


@dataclass
class SafetyProtocolsDatabase:
    """База данных протоколов безопасности."""

    def __post_init__(self):
        """Инициализация протоколов безопасности."""

        self.contraindications = {
            "active_psychosis": {
                "techniques_contraindicated": [
                    "deep_regression",
                    "intensive_emotional_work",
                    "unsupervised_mindfulness"
                ],
                "rationale": "Риск ухудшения симптомов"
            },
            "severe_trauma": {
                "techniques_contraindicated": [
                    "exposure_without_support",
                    "traumatic_memory_work"
                ],
                "requires": "professional_supervision"
            },
            "suicidal_ideation": {
                "techniques_contraindicated": ["all_self_help"],
                "requires": "immediate_professional_help",
                "emergency_resources": "Crisis hotline, ER"
            },
            "active_substance_abuse": {
                "techniques_caution": [
                    "emotional_regulation_work"
                ],
                "note": "Может потребовать сначала стабилизацию"
            }
        }

        self.warning_signs = [
            "Усиление суицидальных мыслей",
            "Появление психотических симптомов",
            "Значительное ухудшение функционирования",
            "Неконтролируемые панические атаки",
            "Диссоциативные эпизоды",
            "Саморазрушительное поведение"
        ]

        self.safe_practices = [
            "Всегда информировать о пределах самопомощи",
            "Давать ресурсы профессиональной помощи",
            "Мониторить прогресс и ухудшения",
            "Рекомендовать профессионала при стагнации",
            "Избегать pathologizing нормального опыта"
        ]


@dataclass
class EthicalGuidelinesDatabase:
    """База данных этических руководств."""

    def __post_init__(self):
        """Инициализация этических руководств."""

        self.informed_consent_elements = [
            "Объяснение природы интервенции",
            "Описание потенциальных рисков",
            "Описание потенциальных преимуществ",
            "Альтернативы (включая профессиональную помощь)",
            "Право отказаться или прекратить",
            "Пределы конфиденциальности",
            "Контакты для вопросов"
        ]

        self.ethical_principles = {
            "autonomy": {
                "description": "Уважение права на самоопределение",
                "implementation": [
                    "Предоставление выбора",
                    "Информированное согласие",
                    "Право отказаться"
                ]
            },
            "beneficence": {
                "description": "Действовать в интересах пользователя",
                "implementation": [
                    "Evidence-based подходы",
                    "Максимизация пользы",
                    "Компетентная практика"
                ]
            },
            "non_maleficence": {
                "description": "Не навреди",
                "implementation": [
                    "Минимизация рисков",
                    "Мониторинг безопасности",
                    "Contraindications"
                ]
            },
            "justice": {
                "description": "Справедливое распределение",
                "implementation": [
                    "Доступность",
                    "Культурная адаптация",
                    "Отсутствие дискриминации"
                ]
            }
        }


@dataclass
class AdaptationStandardsDatabase:
    """База данных стандартов адаптации техник для самопомощи."""

    def __post_init__(self):
        """Инициализация стандартов адаптации."""

        self.adaptation_principles = {
            "fidelity": {
                "description": "Сохранение ключевых элементов",
                "requirements": [
                    "Идентифицировать active ingredients",
                    "Сохранить механизм действия",
                    "Не упрощать до потери эффективности"
                ]
            },
            "safety": {
                "description": "Адаптация с учетом безопасности",
                "requirements": [
                    "Удалить элементы требующие supervision",
                    "Добавить safeguards",
                    "Ясные инструкции когда остановиться"
                ]
            },
            "accessibility": {
                "description": "Доступность для самостоятельного использования",
                "requirements": [
                    "Понятные инструкции",
                    "Пошаговость",
                    "Примеры применения"
                ]
            }
        }

        self.acceptable_modifications = [
            "Упрощение языка",
            "Добавление примеров",
            "Разбивка на меньшие шаги",
            "Добавление визуальных aids",
            "Создание worksheets",
            "Адаптация под онлайн формат"
        ]

        self.unacceptable_modifications = [
            "Удаление ключевых компонентов",
            "Изменение механизма действия",
            "Добавление непроверенных элементов",
            "Overclaiming эффективности",
            "Игнорирование contraindications"
        ]


@dataclass
class EffectivenessMetricsDatabase:
    """База данных метрик эффективности."""

    def __post_init__(self):
        """Инициализация метрик эффективности."""

        self.validated_outcome_measures = {
            "depression": [
                {
                    "name": "PHQ-9",
                    "description": "Patient Health Questionnaire-9",
                    "validated": True,
                    "self_report": True,
                    "sensitivity": "high"
                },
                {
                    "name": "BDI-II",
                    "description": "Beck Depression Inventory",
                    "validated": True,
                    "self_report": True
                }
            ],
            "anxiety": [
                {
                    "name": "GAD-7",
                    "description": "Generalized Anxiety Disorder-7",
                    "validated": True,
                    "self_report": True,
                    "sensitivity": "high"
                }
            ],
            "wellbeing": [
                {
                    "name": "WEMWBS",
                    "description": "Warwick-Edinburgh Mental Wellbeing Scale",
                    "validated": True
                }
            ]
        }

        self.effect_size_interpretation = {
            "small": {"cohens_d": "0.20-0.49", "meaning": "Заметный но небольшой эффект"},
            "medium": {"cohens_d": "0.50-0.79", "meaning": "Умеренный эффект"},
            "large": {"cohens_d": "0.80+", "meaning": "Большой эффект"}
        }


@dataclass
class PatternScientificValidatorDependencies:
    """Зависимости агента."""

    api_key: str
    patternshift_project_path: str = ""

    # Базы данных
    research_database: EvidenceBasedResearchDatabase = field(
        default_factory=EvidenceBasedResearchDatabase
    )
    safety_protocols: SafetyProtocolsDatabase = field(
        default_factory=SafetyProtocolsDatabase
    )
    ethical_guidelines: EthicalGuidelinesDatabase = field(
        default_factory=EthicalGuidelinesDatabase
    )
    adaptation_standards: AdaptationStandardsDatabase = field(
        default_factory=AdaptationStandardsDatabase
    )
    effectiveness_metrics: EffectivenessMetricsDatabase = field(
        default_factory=EffectivenessMetricsDatabase
    )

    # RAG конфигурация
    agent_name: str = "pattern_scientific_validator"
    knowledge_tags: List[str] = field(
        default_factory=lambda: [
            "pattern-scientific-validator",
            "evidence-based",
            "research",
            "agent-knowledge",
            "patternshift"
        ]
    )
    knowledge_domain: str | None = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"


__all__ = [
    "EvidenceBasedResearchDatabase",
    "SafetyProtocolsDatabase",
    "EthicalGuidelinesDatabase",
    "AdaptationStandardsDatabase",
    "EffectivenessMetricsDatabase",
    "PatternScientificValidatorDependencies"
]
