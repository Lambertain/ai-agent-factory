"""
Зависимости для Pattern Safety Protocol Agent
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class CrisisResourceDatabase:
    """База данных кризисных ресурсов и линий помощи."""

    def __post_init__(self):
        self.crisis_hotlines = {
            "russia": [
                {
                    "name": "Телефон доверия экстренной психологической помощи МЧС",
                    "phone": "8-495-989-50-50",
                    "available": "24/7",
                    "description": "Круглосуточная психологическая помощь в кризисных ситуациях"
                },
                {
                    "name": "Линия помощи «Дети онлайн»",
                    "phone": "8-800-25-000-15",
                    "available": "9:00-18:00 (пн-пт)",
                    "description": "Психологическая помощь детям и подросткам"
                },
                {
                    "name": "Телефон доверия для детей, подростков и родителей",
                    "phone": "8-800-2000-122",
                    "available": "24/7",
                    "description": "Анонимная бесплатная психологическая помощь"
                }
            ],
            "international": [
                {
                    "name": "International Association for Suicide Prevention",
                    "website": "https://www.iasp.info/resources/Crisis_Centres/",
                    "description": "Глобальный каталог кризисных центров"
                }
            ]
        }

        self.emergency_services = {
            "medical_emergency": "103 (скорая помощь)",
            "police": "102",
            "general_emergency": "112"
        }

        self.online_resources = [
            {
                "name": "Ясно",
                "url": "https://yasno.live/",
                "description": "Онлайн-сервис психологической помощи"
            },
            {
                "name": "Помощь рядом",
                "url": "https://pomoschryadom.ru/",
                "description": "Список организаций психологической помощи в России"
            }
        ]


@dataclass
class ContraindicationsDatabase:
    """База данных противопоказаний для психологических техник."""

    def __post_init__(self):
        # Абсолютные противопоказания
        self.absolute_contraindications = {
            "hypnosis": [
                "Активный психоз",
                "Эпилепсия (без разрешения врача)",
                "Тяжелые диссоциативные расстройства",
                "Острые психотические эпизоды"
            ],
            "breathwork": [
                "Сердечно-сосудистые заболевания",
                "Беременность (первый триместр)",
                "Эпилепсия",
                "Недавние операции",
                "Тяжелая астма"
            ],
            "deep_trauma_work": [
                "Острый суицидальный риск",
                "Активная ПТСР без терапевтической поддержки",
                "Недавняя травма (< 6 месяцев без терапии)",
                "Психотические расстройства"
            ]
        }

        # Относительные противопоказания (требуют адаптации)
        self.relative_contraindications = {
            "visualization": [
                "Афантазия (невозможность визуализации)",
                "Тревожные расстройства (адаптировать интенсивность)"
            ],
            "body_scanning": [
                "Соматоформные расстройства",
                "История физического насилия"
            ],
            "mindfulness": [
                "Депрессивные руминации (риск усиления)",
                "Деперсонализация/дереализация"
            ]
        }

        # Временные противопоказания
        self.temporary_contraindications = [
            "Острая фаза горя",
            "Интоксикация",
            "Тяжелая физическая болезнь",
            "Экстремальный стресс (травматическое событие < 72 часов)"
        ]


@dataclass
class RiskIndicatorsDatabase:
    """База данных индикаторов риска."""

    def __post_init__(self):
        # Суицидальные индикаторы
        self.suicidal_indicators = [
            "Прямые высказывания о желании умереть",
            "Разговоры о самоубийстве",
            "Поиск способов самоубийства",
            "Прощание с близкими",
            "Раздача ценных вещей",
            "Внезапное спокойствие после депрессии",
            "Составление завещания или прощальных писем"
        ]

        # Признаки кризиса
        self.crisis_indicators = [
            "Неспособность справляться с повседневными задачами",
            "Интенсивная тревога или паника",
            "Потеря контакта с реальностью",
            "Галлюцинации или бред",
            "Экстремальные перепады настроения",
            "Недавняя серьезная травма или потеря"
        ]

        # Индикаторы самоповреждения
        self.self_harm_indicators = [
            "Следы порезов или ожогов",
            "Упоминания о самоповреждении",
            "Паттерн саморазрушительного поведения",
            "Импульсивность и рискованное поведение"
        ]

        # Триггеры травмы
        self.trauma_triggers = [
            "Флешбэки",
            "Диссоциация",
            "Интенсивные эмоциональные реакции",
            "Избегающее поведение",
            "Гипервозбуждение"
        ]


@dataclass
class PharmacologicalInteractionsDatabase:
    """База данных фармакологических взаимодействий."""

    def __post_init__(self):
        self.medication_interactions = {
            "antidepressants": {
                "ssri": {
                    "medications": ["Прозак", "Золофт", "Ципралекс"],
                    "interactions": [
                        {
                            "technique": "Дыхательные практики",
                            "risk": "moderate",
                            "description": "Может усилить побочные эффекты (головокружение)",
                            "recommendation": "Начинать осторожно, короткие сессии"
                        }
                    ]
                },
                "maoi": {
                    "medications": ["Нардил", "Парнат"],
                    "interactions": [
                        {
                            "technique": "Техники активации",
                            "risk": "high",
                            "description": "Риск гипертонического криза при активации",
                            "recommendation": "Консультация с психиатром обязательна"
                        }
                    ]
                }
            },
            "anxiolytics": {
                "benzodiazepines": {
                    "medications": ["Ксанакс", "Феназепам", "Диазепам"],
                    "interactions": [
                        {
                            "technique": "Гипноз",
                            "risk": "moderate",
                            "description": "Усиление седативного эффекта",
                            "recommendation": "Снизить глубину транса, избегать после приема"
                        },
                        {
                            "technique": "Релаксационные техники",
                            "risk": "low",
                            "description": "Синергичный эффект релаксации",
                            "recommendation": "Обычно безопасно, контролировать состояние"
                        }
                    ]
                }
            },
            "mood_stabilizers": {
                "lithium": {
                    "medications": ["Литий"],
                    "interactions": [
                        {
                            "technique": "Дыхательные практики",
                            "risk": "high",
                            "description": "Дегидратация может повысить токсичность лития",
                            "recommendation": "Обильное питье, медицинское наблюдение"
                        }
                    ]
                }
            },
            "antipsychotics": {
                "typical": {
                    "medications": ["Галоперидол", "Аминазин"],
                    "interactions": [
                        {
                            "technique": "Активирующие техники",
                            "risk": "moderate",
                            "description": "Может снижаться эффективность седации",
                            "recommendation": "Консультация с психиатром перед программой"
                        }
                    ]
                }
            }
        }


@dataclass
class VulnerableGroupsDatabase:
    """База данных уязвимых групп пользователей."""

    def __post_init__(self):
        self.vulnerable_groups = {
            "children_adolescents": {
                "age_range": "< 18 лет",
                "vulnerabilities": [
                    "Развивающийся мозг и эмоциональная регуляция",
                    "Повышенная внушаемость",
                    "Ограниченная способность к самостоятельной оценке рисков"
                ],
                "modifications": [
                    "Обязательное согласие родителей",
                    "Адаптированный язык и примеры",
                    "Укороченные сессии (10-15 минут)",
                    "Игровые элементы для вовлечения"
                ],
                "red_flags": [
                    "Признаки буллинга",
                    "Проблемы в школе",
                    "Социальная изоляция",
                    "Изменения в поведении"
                ]
            },
            "elderly": {
                "age_range": "> 65 лет",
                "vulnerabilities": [
                    "Когнитивные изменения",
                    "Социальная изоляция",
                    "Хронические заболевания"
                ],
                "modifications": [
                    "Упрощенные инструкции",
                    "Больше времени на освоение",
                    "Адаптация для физических ограничений",
                    "Увеличенный текст и аудио-поддержка"
                ],
                "red_flags": [
                    "Признаки деменции",
                    "Потеря партнера",
                    "Депрессия или апатия"
                ]
            },
            "pregnancy_postpartum": {
                "age_range": "Беременные и послеродовой период (до 1 года)",
                "vulnerabilities": [
                    "Гормональные изменения",
                    "Риск послеродовой депрессии",
                    "Физиологический стресс"
                ],
                "modifications": [
                    "Исключить breathwork в первом триместре",
                    "Адаптировать физические упражнения",
                    "Скрининг послеродовой депрессии",
                    "Фокус на self-compassion"
                ],
                "red_flags": [
                    "Послеродовая депрессия",
                    "Тревога о ребенке",
                    "Проблемы привязанности",
                    "Мысли о вреде себе или ребенку"
                ]
            },
            "trauma_survivors": {
                "age_range": "Любой возраст",
                "vulnerabilities": [
                    "ПТСР или комплексное ПТСР",
                    "Триггеры и флешбэки",
                    "Диссоциация",
                    "Доверие к программе/терапевту"
                ],
                "modifications": [
                    "Trauma-informed подход",
                    "Контроль и выбор пользователя",
                    "Grounding техники в начале",
                    "Постепенное увеличение интенсивности"
                ],
                "red_flags": [
                    "Диссоциативные эпизоды",
                    "Флешбэки",
                    "Повторная травматизация",
                    "Эмоциональная дисрегуляция"
                ]
            }
        }


@dataclass
class PatternSafetyProtocolDependencies:
    """Зависимости для Pattern Safety Protocol Agent."""

    # Основные настройки
    api_key: str
    agent_name: str = "pattern_safety_protocol"  # For RAG protection
    patternshift_project_path: str = ""
    user_id: Optional[str] = None

    # Базы данных безопасности
    crisis_resources: CrisisResourceDatabase = field(default_factory=CrisisResourceDatabase)
    contraindications_db: ContraindicationsDatabase = field(default_factory=ContraindicationsDatabase)
    risk_indicators_db: RiskIndicatorsDatabase = field(default_factory=RiskIndicatorsDatabase)
    pharmacological_interactions_db: PharmacologicalInteractionsDatabase = field(default_factory=PharmacologicalInteractionsDatabase)
    vulnerable_groups_db: VulnerableGroupsDatabase = field(default_factory=VulnerableGroupsDatabase)

    # Настройки мониторинга
    enable_continuous_monitoring: bool = True
    monitoring_frequency: str = "daily"  # daily, per_module, continuous

    # Настройки эскалации
    escalation_threshold: str = "moderate"  # low, moderate, high
    auto_escalate_critical: bool = True
    notify_admin_on_risk: bool = True

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "pattern-safety-protocol",
        "crisis-intervention",
        "risk-assessment",
        "agent-knowledge",
        "patternshift"
    ])
    knowledge_domain: Optional[str] = None
    archon_project_id: Optional[str] = None

    # Настройки безопасности
    require_informed_consent: bool = True
    allow_self_assessment: bool = True
    duty_of_care_enabled: bool = True


__all__ = [
    "CrisisResourceDatabase",
    "ContraindicationsDatabase",
    "RiskIndicatorsDatabase",
    "PharmacologicalInteractionsDatabase",
    "VulnerableGroupsDatabase",
    "PatternSafetyProtocolDependencies"
]
