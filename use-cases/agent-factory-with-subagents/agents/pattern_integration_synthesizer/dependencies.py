"""
Dependencies для Pattern Integration Synthesizer Agent с базами знаний.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


# ===== БАЗЫ ДАННЫХ ЗНАНИЙ =====

@dataclass
class OrchestrationPatternsDatabase:
    """База паттернов оркестрации модулей."""

    patterns: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "progressive_intensity": {
            "description": "Постепенное увеличение интенсивности",
            "sequence": ["light", "medium", "deep"],
            "rationale": "Предотвращение overwhelm, постепенная адаптация",
            "best_for": ["beginning_phase", "trauma_work", "sensitive_topics"]
        },
        "technique_sandwich": {
            "description": "Чередование активных техник и интеграции",
            "sequence": ["technique", "integration", "technique", "integration"],
            "rationale": "Время на закрепление изменений",
            "best_for": ["nlp_work", "hypnosis", "behavioral_change"]
        },
        "energy_wave": {
            "description": "Волнообразное управление энергией",
            "sequence": ["high_energy", "rest", "high_energy", "reflection"],
            "rationale": "Предотвращение выгорания, устойчивый momentum",
            "best_for": ["long_programs", "daily_sessions", "intensive_work"]
        },
        "spiral_deepening": {
            "description": "Спиральное углубление темы",
            "sequence": ["intro", "practice", "return_deeper", "practice", "mastery"],
            "rationale": "Постепенное раскрытие сложности без overwhelm",
            "best_for": ["complex_topics", "skill_building", "transformation"]
        }
    })

    synergy_rules: Dict[str, List[str]] = field(default_factory=lambda: {
        "high_synergy_pairs": [
            "cognitive_restructuring + behavioral_activation",
            "mindfulness + cognitive_defusion",
            "values_clarification + committed_action",
            "self_compassion + emotional_regulation",
            "body_awareness + emotional_processing"
        ],
        "sequential_dependencies": [
            "awareness_building → problem_identification → solution_development",
            "psychoeducation → skill_acquisition → real_world_application",
            "safety_establishment → trauma_processing → integration"
        ],
        "avoid_combinations": [
            "intensive_emotional_work + intensive_cognitive_work (same_day)",
            "multiple_hypnosis_sessions (same_day)",
            "conflicting_theoretical_frameworks (same_phase)"
        ]
    })


@dataclass
class EmotionalCurveDatabase:
    """База знаний об эмоциональной кривой трансформации."""

    curve_stages: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "days_1_3_excitement": {
            "stage": "excitement",
            "energy": "high",
            "motivation": "high",
            "characteristics": [
                "Энтузиазм и надежда",
                "Открытость к новому",
                "Высокая мотивация"
            ],
            "optimal_activities": [
                "Психообразование",
                "Легкие упражнения",
                "Мотивирующий контент"
            ],
            "avoid": ["Слишком интенсивная работа", "Сложные техники"]
        },
        "days_4_7_resistance": {
            "stage": "resistance",
            "energy": "medium",
            "motivation": "declining",
            "characteristics": [
                "Появление сомнений",
                "Первые трудности",
                "Снижение новизны"
            ],
            "optimal_activities": [
                "Поддерживающий контент",
                "Quick wins упражнения",
                "Напоминание о целях"
            ],
            "critical": "Основная точка dropout - нужна активная поддержка"
        },
        "days_8_12_breakthrough": {
            "stage": "breakthrough",
            "energy": "variable",
            "motivation": "renewed",
            "characteristics": [
                "Первые значимые изменения",
                "Renewed commitment",
                "Deeper insights"
            ],
            "optimal_activities": [
                "Углубленные техники",
                "Consolidation упражнения",
                "Celebrating progress"
            ],
            "opportunity": "Момент для более глубокой работы"
        },
        "days_13_18_integration": {
            "stage": "integration",
            "energy": "stable",
            "motivation": "high",
            "characteristics": [
                "Интеграция изменений",
                "Формирование новых паттернов",
                "Устойчивый прогресс"
            ],
            "optimal_activities": [
                "Real-world application",
                "Habit formation",
                "Advanced techniques"
            ],
            "focus": "Перенос в реальную жизнь"
        },
        "days_19_21_mastery": {
            "stage": "mastery",
            "energy": "high",
            "motivation": "intrinsic",
            "characteristics": [
                "Ownership изменений",
                "Внутренняя мотивация",
                "Планирование будущего"
            ],
            "optimal_activities": [
                "Consolidation",
                "Future planning",
                "Maintenance strategies"
            ],
            "goal": "Подготовка к самостоятельному продолжению"
        }
    })

    resistance_points: List[Dict[str, Any]] = field(default_factory=lambda: [
        {
            "day_range": "4-7",
            "type": "novelty_wearoff",
            "severity": "high",
            "mitigation": [
                "Вводить новые форматы",
                "Давать quick wins",
                "Усилить социальную поддержку"
            ]
        },
        {
            "day_range": "10-12",
            "type": "plateau_perception",
            "severity": "medium",
            "mitigation": [
                "Показывать прогресс визуально",
                "Вводить challenge tasks",
                "Reframe expectations"
            ]
        },
        {
            "day_range": "16-17",
            "type": "anticipatory_ending",
            "severity": "low",
            "mitigation": [
                "Фокус на продолжении после программы",
                "Maintenance planning",
                "Celebrating journey"
            ]
        }
    ])


@dataclass
class ModuleLoadDatabase:
    """База знаний о когнитивной и эмоциональной нагрузке."""

    load_guidelines: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "daily_limits": {
            "total_minutes": {"min": 15, "max": 60, "optimal_range": (30, 45)},
            "sessions_per_day": {"min": 1, "max": 3, "optimal": 2},
            "intensive_modules": {"max_per_day": 1}
        },
        "module_intensity": {
            "light": {
                "duration": "5-10 min",
                "examples": ["psychoeducation", "journaling", "light_exercise"],
                "can_combine_with": ["any"]
            },
            "medium": {
                "duration": "15-20 min",
                "examples": ["cognitive_techniques", "behavioral_activation", "mindfulness"],
                "can_combine_with": ["light", "medium"]
            },
            "intensive": {
                "duration": "30-45 min",
                "examples": ["deep_emotional_work", "hypnosis", "trauma_processing"],
                "can_combine_with": ["light"],
                "max_per_day": 1
            }
        },
        "recovery_time": {
            "after_light": "0-5 min",
            "after_medium": "5-10 min",
            "after_intensive": "several_hours_or_next_day"
        }
    })

    fatigue_indicators: List[str] = field(default_factory=lambda: [
        "Снижение completion rate",
        "Увеличение времени выполнения",
        "Negative feedback scores",
        "Skipping optional activities"
    ])


@dataclass
class TransitionPatternsDatabase:
    """База знаний о переходах между модулями."""

    transition_types: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "bridge": {
            "purpose": "Связать два модуля логически",
            "duration": "30-60 seconds",
            "elements": ["Recap previous", "Preview next", "Show connection"]
        },
        "energizer": {
            "purpose": "Повысить энергию перед активностью",
            "duration": "1-2 minutes",
            "elements": ["Physical movement", "Breath work", "Activation"]
        },
        "grounding": {
            "purpose": "Успокоить после интенсивной работы",
            "duration": "2-3 minutes",
            "elements": ["Breathing", "Body scan", "Safe space"]
        },
        "reflection": {
            "purpose": "Интегрировать опыт",
            "duration": "2-5 minutes",
            "elements": ["Key takeaways", "Personal insights", "Action items"]
        }
    })


# ===== ОСНОВНОЙ DEPENDENCY CLASS =====

@dataclass
class PatternIntegrationSynthesizerDependencies:
    """Зависимости агента Pattern Integration Synthesizer."""

    # Основные настройки
    api_key: str
    patternshift_project_path: str = ""

    # Имя агента для защиты от проблем RAG
    agent_name: str = "pattern_integration_synthesizer"

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "pattern-integration-synthesizer",
        "orchestration",
        "synergy",
        "agent-knowledge",
        "patternshift"
    ])
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Базы знаний
    orchestration_patterns_db: OrchestrationPatternsDatabase = field(
        default_factory=OrchestrationPatternsDatabase
    )
    emotional_curve_db: EmotionalCurveDatabase = field(
        default_factory=EmotionalCurveDatabase
    )
    module_load_db: ModuleLoadDatabase = field(
        default_factory=ModuleLoadDatabase
    )
    transition_patterns_db: TransitionPatternsDatabase = field(
        default_factory=TransitionPatternsDatabase
    )

    def __post_init__(self):
        """Инициализация конфигурации."""
        if not self.knowledge_tags:
            self.knowledge_tags = [
                "pattern-integration-synthesizer",
                "orchestration",
                "synergy",
                "agent-knowledge",
                "patternshift"
            ]


__all__ = [
    "OrchestrationPatternsDatabase",
    "EmotionalCurveDatabase",
    "ModuleLoadDatabase",
    "TransitionPatternsDatabase",
    "PatternIntegrationSynthesizerDependencies"
]
