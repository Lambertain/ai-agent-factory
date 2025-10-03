"""
Зависимости для Pattern Transition Craftsman Agent.

Специализированные базы данных для создания переходов между модулями.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class TransitionTemplatesDatabase:
    """База данных шаблонов переходов."""

    def __post_init__(self):
        self.templates_by_type = {
            "intro_to_main": [
                {
                    "id": "itm_001",
                    "template": "Отлично! Теперь, когда мы с вами [краткое резюме введения], давайте перейдем к практической части...",
                    "energy": "building",
                    "duration": 30
                },
                {
                    "id": "itm_002",
                    "template": "Вы готовы? То, что мы сейчас сделаем, опирается на понимание, которое вы получили выше...",
                    "energy": "activating",
                    "duration": 25
                }
            ],
            "main_to_reflection": [
                {
                    "id": "mtr_001",
                    "template": "Давайте сделаем паузу и осознаем, что только что произошло. Какие изменения вы заметили?...",
                    "energy": "calm",
                    "duration": 40
                },
                {
                    "id": "mtr_002",
                    "template": "Замечательно! Теперь важный момент - интегрировать этот опыт. Что вы чувствуете сейчас?...",
                    "energy": "neutral",
                    "duration": 35
                }
            ],
            "day_to_day": [
                {
                    "id": "dtd_001",
                    "template": "Вчера вы [достижение предыдущего дня]. Сегодня мы продолжим этот путь и углубим ваше понимание...",
                    "energy": "building",
                    "duration": 45
                },
                {
                    "id": "dtd_002",
                    "template": "Новый день, новые возможности. Помните, как вчера вы [якорь]? Это станет фундаментом для сегодняшней работы...",
                    "energy": "activating",
                    "duration": 50
                }
            ],
            "technique_to_exercise": [
                {
                    "id": "tte_001",
                    "template": "Теперь, когда вы освоили технику, давайте закрепим её на практике. Это упражнение поможет вам...",
                    "energy": "sustaining",
                    "duration": 30
                },
                {
                    "id": "tte_002",
                    "template": "Отлично! Вы понимаете механизм. Время применить это в реальной ситуации...",
                    "energy": "activating",
                    "duration": 25
                }
            ]
        }

        self.micro_interventions = {
            "reframe": [
                "Это не неудача, это ценная информация о том, как работает ваша психика.",
                "Сопротивление - это нормально. Оно показывает, что мы касаемся чего-то важного.",
                "Каждый маленький шаг имеет значение, даже если результат не сразу заметен."
            ],
            "anchor": [
                "Помните то чувство легкости, которое возникло в прошлый раз? Давайте вернемся к нему.",
                "Как и тогда, когда вы [предыдущее достижение], сейчас вы готовы к следующему шагу.",
                "Это та же самая сила, которую вы использовали вчера. Она с вами."
            ],
            "motivate": [
                "Вы уже прошли больше половины пути. Представьте, что будет через неделю!",
                "Каждый модуль делает вас сильнее. Вы это уже чувствуете?",
                "То, что вы делаете сейчас, изменит вашу жизнь. Это не преувеличение."
            ],
            "validate": [
                "То, что вы чувствуете - абсолютно нормально на этом этапе.",
                "Ваш опыт уникален, и это именно то, что нужно.",
                "Вы движетесь в правильном направлении, даже если это не всегда очевидно."
            ]
        }

    def get_template(self, transition_type: str, energy_level: str = None) -> Optional[Dict[str, Any]]:
        """Получить шаблон перехода по типу и энергетике."""
        templates = self.templates_by_type.get(transition_type, [])
        if not templates:
            return None

        if energy_level:
            filtered = [t for t in templates if t["energy"] == energy_level]
            return filtered[0] if filtered else templates[0]

        return templates[0]

    def get_micro_intervention(self, intervention_type: str) -> str:
        """Получить микро-интервенцию по типу."""
        interventions = self.micro_interventions.get(intervention_type, [])
        return interventions[0] if interventions else ""


@dataclass
class EnergyTransitionsDatabase:
    """База данных энергетических переходов."""

    def __post_init__(self):
        self.transitions = {
            ("calm", "activating"): {
                "technique": "progressive_energization",
                "text": "Сделайте глубокий вдох... и на выдохе почувствуйте, как энергия начинает циркулировать в вашем теле. С каждым вдохом - больше энергии, больше готовности действовать.",
                "duration": 45,
                "breath_work": True,
                "movement": False
            },
            ("activating", "calm"): {
                "technique": "gentle_grounding",
                "text": "Теперь давайте плавно замедлимся. Почувствуйте землю под ногами. Выдох длиннее вдоха. Всё хорошо. Вы в безопасности.",
                "duration": 50,
                "breath_work": True,
                "grounding": True
            },
            ("neutral", "building"): {
                "technique": "momentum_builder",
                "text": "Вы чувствуете, как что-то начинает происходить? Это momentum. Давайте аккуратно усилим его, не форсируя, просто следуя естественному потоку.",
                "duration": 40,
                "visualization": True
            },
            ("building", "sustaining"): {
                "technique": "plateau_stabilization",
                "text": "Отлично! Теперь важно удержать эту энергию. Не нужно больше усилий - просто позвольте ей быть.",
                "duration": 35,
                "breath_work": True
            }
        }

    def get_transition(self, from_energy: str, to_energy: str) -> Optional[Dict[str, Any]]:
        """Получить энергетический переход."""
        return self.transitions.get((from_energy, to_energy))


@dataclass
class AnchorPatternsDatabase:
    """База данных паттернов якорей для преемственности."""

    def __post_init__(self):
        self.anchor_patterns = {
            "metaphor": {
                "pattern": "Помните метафору [X]? Сейчас мы используем её следующий уровень...",
                "examples": [
                    "Помните метафору реки? Сейчас мы учимся не просто плыть, но управлять течением.",
                    "Как та лестница, которую мы представляли. Вы поднялись ещё на одну ступень."
                ]
            },
            "achievement": {
                "pattern": "Вчера вы смогли [достижение]. Сегодня мы опираемся на эту силу...",
                "examples": [
                    "Вчера вы смогли отследить свои мысли. Сегодня мы научимся их менять.",
                    "Помните, как легко получилась техника вчера? Эта же лёгкость с вами сейчас."
                ]
            },
            "insight": {
                "pattern": "То понимание, что пришло к вам [когда] - '[инсайт]'. Давайте углубим его...",
                "examples": [
                    "То понимание, что пришло к вам вчера - 'я сам создаю свои ограничения'. Давайте увидим, как их убрать.",
                    "Ваш инсайт о связи эмоций и мыслей - сейчас мы будем работать именно с этим."
                ]
            },
            "emotion": {
                "pattern": "Помните то чувство [эмоция], которое вы испытали? Это ваш ресурс...",
                "examples": [
                    "Помните то чувство лёгкости, когда получилась техника? Вызовите его снова.",
                    "Та спокойная уверенность, которую вы почувствовали - она всё ещё с вами."
                ]
            }
        }

    def get_anchor_pattern(self, anchor_type: str) -> Dict[str, Any]:
        """Получить паттерн якоря."""
        return self.anchor_patterns.get(anchor_type, {})


@dataclass
class ModalityBridgesDatabase:
    """База данных мостов между модальностями."""

    def __post_init__(self):
        self.modality_bridges = {
            "visual_to_auditory": {
                "bridge": "Теперь закройте глаза и просто слушайте. Позвольте образам раствориться, остаются только звуки и слова...",
                "duration": 30
            },
            "auditory_to_kinesthetic": {
                "bridge": "Слышите это? А теперь почувствуйте, как эти слова отзываются в вашем теле. Где вы ощущаете резонанс?...",
                "duration": 35
            },
            "kinesthetic_to_visual": {
                "bridge": "Сохраняя это телесное ощущение, откройте глаза. Если бы это ощущение было цветом, каким оно было бы?...",
                "duration": 30
            },
            "single_to_multi": {
                "bridge": "Отлично! Теперь давайте задействуем все ваши чувства. Видьте, слышьте, ощущайте одновременно...",
                "duration": 40
            }
        }

    def get_bridge(self, modality_shift: str) -> Optional[Dict[str, Any]]:
        """Получить мост между модальностями."""
        return self.modality_bridges.get(modality_shift)


@dataclass
class FlowOptimizationDatabase:
    """База данных для оптимизации потока программы."""

    def __post_init__(self):
        self.flow_principles = {
            "coherence": {
                "description": "Связность и последовательность модулей",
                "checklist": [
                    "Каждый модуль логически следует из предыдущего",
                    "Используются якоря из предыдущих модулей",
                    "Нет резких скачков в сложности",
                    "Терминология консистентна"
                ]
            },
            "emotional_continuity": {
                "description": "Непрерывность эмоционального опыта",
                "checklist": [
                    "Переходы учитывают эмоциональное состояние",
                    "Нет резких сбросов энергии без причины",
                    "Эмоциональные пики и спады запланированы",
                    "Есть время на интеграцию интенсивных опытов"
                ]
            },
            "attention_management": {
                "description": "Управление фокусом внимания",
                "checklist": [
                    "Переходы не отвлекают от основной темы",
                    "Фокус внимания явно перенаправляется",
                    "Нет информационной перегрузки",
                    "Ключевые идеи повторяются в разных формах"
                ]
            }
        }

    def get_principle(self, principle_name: str) -> Dict[str, Any]:
        """Получить принцип оптимизации flow."""
        return self.flow_principles.get(principle_name, {})


@dataclass
class PatternTransitionCraftsmanDependencies:
    """Зависимости для Pattern Transition Craftsman Agent."""

    api_key: str
    patternshift_project_path: str = ""
    user_id: Optional[str] = None
    program_id: Optional[str] = None

    # Базы данных
    templates_db: TransitionTemplatesDatabase = field(default_factory=TransitionTemplatesDatabase)
    energy_transitions_db: EnergyTransitionsDatabase = field(default_factory=EnergyTransitionsDatabase)
    anchor_patterns_db: AnchorPatternsDatabase = field(default_factory=AnchorPatternsDatabase)
    modality_bridges_db: ModalityBridgesDatabase = field(default_factory=ModalityBridgesDatabase)
    flow_optimization_db: FlowOptimizationDatabase = field(default_factory=FlowOptimizationDatabase)

    # Контекст программы
    program_context: Dict[str, Any] = field(default_factory=dict)
    module_history: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        """Инициализация зависимостей."""
        # Инициализация баз данных
        if not isinstance(self.templates_db, TransitionTemplatesDatabase):
            self.templates_db = TransitionTemplatesDatabase()
        if not isinstance(self.energy_transitions_db, EnergyTransitionsDatabase):
            self.energy_transitions_db = EnergyTransitionsDatabase()
        if not isinstance(self.anchor_patterns_db, AnchorPatternsDatabase):
            self.anchor_patterns_db = AnchorPatternsDatabase()
        if not isinstance(self.modality_bridges_db, ModalityBridgesDatabase):
            self.modality_bridges_db = ModalityBridgesDatabase()
        if not isinstance(self.flow_optimization_db, FlowOptimizationDatabase):
            self.flow_optimization_db = FlowOptimizationDatabase()


__all__ = [
    "TransitionTemplatesDatabase",
    "EnergyTransitionsDatabase",
    "AnchorPatternsDatabase",
    "ModalityBridgesDatabase",
    "FlowOptimizationDatabase",
    "PatternTransitionCraftsmanDependencies"
]
