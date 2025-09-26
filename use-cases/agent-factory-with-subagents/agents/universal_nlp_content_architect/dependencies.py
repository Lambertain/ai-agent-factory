"""
Dependencies for Universal NLP Content Architect Agent
Зависимости для универсального агента создания NLP контента
Поддерживает все домены: психология, астрология, таро, нумерология, коучинг, велнес
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Literal
import os
from dotenv import load_dotenv

load_dotenv()

# Типы доменов для универсального применения
DomainType = Literal[
    "psychology",      # Психология
    "astrology",       # Астрология
    "tarot",          # Таро
    "numerology",     # Нумерология
    "coaching",       # Коучинг
    "wellness",       # Велнес/медитация
    "spirituality",   # Духовность
    "self_development" # Саморазвитие
]

# Типы контента
ContentType = Literal[
    "diagnostic_test",        # Диагностический тест
    "transformation_program", # Программа трансформации
    "guidance_system",        # Система наставничества
    "assessment_tool",        # Инструмент оценки
    "meditation_program",     # Программа медитации
    "coaching_framework",     # Коучинговая рамка
    "divination_system",      # Система предсказания
    "analysis_framework"      # Аналитическая рамка
]

# NLP методологии
NLPMethodology = Literal[
    "ericksonian_full",    # Полные Эриксоновские техники
    "basic_nlp",           # Базовые NLP техники
    "advanced_nlp",        # Продвинутые NLP техники
    "metaphorical",        # Метафорический подход
    "conversational",      # Разговорный гипноз
    "adaptation_mode",     # Режим адаптации
    "validation_mode"      # Режим валидации
]

@dataclass
class UniversalNLPDependencies:
    """
    Зависимости для Universal NLP Content Architect Agent
    Универсальная система для всех доменов применения NLP
    """

    # Основные параметры домена
    domain_type: DomainType = "psychology"
    content_type: ContentType = "diagnostic_test"
    target_language: str = "ukrainian"  # ukrainian, russian, english
    nlp_methodology: NLPMethodology = "ericksonian_full"

    # Контекст проекта
    project_context: Dict[str, Any] = field(default_factory=dict)

    # NLP техники по доменам
    nlp_techniques: Dict[str, List[str]] = field(default_factory=lambda: {
        "psychology": [
            "reframing", "anchoring", "rapport_building", "meta_programs",
            "submodalities", "timeline_work", "parts_integration", "belief_change"
        ],
        "astrology": [
            "metaphorical_modeling", "temporal_anchoring", "archetype_integration",
            "energy_reframing", "cosmic_timeline", "planetary_rapport"
        ],
        "tarot": [
            "symbolic_anchoring", "intuitive_reframing", "archetypal_integration",
            "metaphorical_guidance", "insight_amplification", "wisdom_accessing"
        ],
        "numerology": [
            "pattern_recognition", "numeric_anchoring", "analytical_reframing",
            "systematic_integration", "logical_flow", "calculated_insights"
        ],
        "coaching": [
            "outcome_setting", "resource_anchoring", "strategy_modeling",
            "belief_alignment", "future_pacing", "ecological_checking"
        ],
        "wellness": [
            "state_management", "relaxation_anchoring", "mindful_reframing",
            "body_awareness", "breath_synchronization", "natural_pacing"
        ]
    })

    # Эриксоновские паттерны по доменам
    ericksonian_patterns: Dict[str, List[str]] = field(default_factory=lambda: {
        "psychology": [
            "therapeutic_metaphors", "embedded_commands", "truisms", "presuppositions",
            "utilization_principle", "confusion_technique", "double_binds", "indirect_suggestions"
        ],
        "astrology": [
            "cosmic_metaphors", "planetary_commands", "celestial_truisms", "karmic_presuppositions",
            "energy_utilization", "cycle_confusion", "choice_binds", "destiny_suggestions"
        ],
        "tarot": [
            "symbolic_metaphors", "archetypal_commands", "wisdom_truisms", "intuitive_presuppositions",
            "card_utilization", "mystery_technique", "path_binds", "guidance_suggestions"
        ],
        "numerology": [
            "numeric_metaphors", "calculated_commands", "mathematical_truisms", "pattern_presuppositions",
            "number_utilization", "formula_technique", "logic_binds", "systematic_suggestions"
        ],
        "coaching": [
            "success_metaphors", "achievement_commands", "growth_truisms", "potential_presuppositions",
            "resource_utilization", "challenge_technique", "progress_binds", "empowerment_suggestions"
        ],
        "wellness": [
            "healing_metaphors", "relaxation_commands", "nature_truisms", "balance_presuppositions",
            "body_utilization", "flow_technique", "harmony_binds", "wellness_suggestions"
        ]
    })

    # VAK адаптации с учетом доменов
    vak_adaptations: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "visual": {
            "general_words": ["видишь", "ясно", "ярко", "представь", "образ", "картина", "перспектiva"],
            "psychology_metaphors": ["свет понимания", "ясность мыслей", "яркие решения"],
            "astrology_metaphors": ["звездная карта", "космические образы", "планетарные цвета"],
            "tarot_metaphors": ["символические картины", "визуальные архетипы", "образы карт"],
            "numerology_metaphors": ["числовые паттерны", "математические образы", "графики судьбы"],
            "coaching_metaphors": ["визуализация целей", "четкие планы", "яркое будущее"],
            "wellness_metaphors": ["внутренний свет", "образы природы", "визуальный покой"]
        },
        "auditory": {
            "general_words": ["слышишь", "звучит", "мелодия", "ритм", "голос", "эхо", "тишина"],
            "psychology_metaphors": ["внутренний голос", "гармония мыслей", "резонанс души"],
            "astrology_metaphors": ["музыка сфер", "планетарные вибрации", "космическая гармония"],
            "tarot_metaphors": ["голос интуиции", "шепот карт", "звуки мудрости"],
            "numerology_metaphors": ["ритм чисел", "математическая мелодия", "звуки расчетов"],
            "coaching_metaphors": ["призыв к действию", "мотивационные ритмы", "эхо успеха"],
            "wellness_metaphors": ["звуки природы", "внутренняя тишина", "дыхательные ритмы"]
        },
        "kinesthetic": {
            "general_words": ["чувствуешь", "касаешься", "тепло", "легко", "тяжело", "движение", "поток"],
            "psychology_metaphors": ["эмоциональное тепло", "легкость бытия", "поток осознания"],
            "astrology_metaphors": ["энергетические потоки", "планетарные влияния", "космические вибрации"],
            "tarot_metaphors": ["энергия карт", "тактильная связь", "чувство истины"],
            "numerology_metaphors": ["вес чисел", "давление фактов", "поток расчетов"],
            "coaching_metaphors": ["движение к цели", "сила мотивации", "импульс роста"],
            "wellness_metaphors": ["телесные ощущения", "энергетический баланс", "физический покой"]
        }
    })

    # Возрастные адаптации
    age_adaptations: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "youth": {  # 18-25
            "tone": "informal_friendly",
            "slang": {
                "ukrainian": ["йо", "челлендж", "топово", "кайф", "зайти", "жесть"],
                "russian": ["го", "вайб", "крута", "огонь", "зацени", "ваще"],
                "english": ["cool", "awesome", "like", "literally", "vibe", "slay"]
            },
            "references": ["social_media", "gaming", "trends", "memes", "streaming", "apps"],
            "nlp_style": "energetic_modern"
        },
        "friendly": {  # 26-35
            "tone": "conversational",
            "slang": {
                "ukrainian": ["круто", "давай розберемося", "супер", "класно"],
                "russian": ["классно", "давай разберемся", "здорово", "отлично"],
                "english": ["great", "let's figure out", "awesome", "perfect"]
            },
            "references": ["work_life", "relationships", "goals", "balance", "growth"],
            "nlp_style": "practical_supportive"
        },
        "professional": {  # 36+
            "tone": "respectful",
            "slang": {
                "ukrainian": ["цікаво", "варто зауважити", "справді", "безумовно"],
                "russian": ["интересно", "стоит отметить", "действительно", "безусловно"],
                "english": ["interesting", "worth noting", "indeed", "certainly"]
            },
            "references": ["experience", "wisdom", "stability", "mastery", "legacy"],
            "nlp_style": "wise_respectful"
        }
    })

    # Трансформационные программы по сложности
    transformation_complexity: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "crisis": {  # 21 день - глубокие изменения
            "duration": 21,
            "phases": [
                {"name": "destabilization", "days": 7, "focus": "breaking_old_patterns"},
                {"name": "transformation", "days": 7, "focus": "installing_new_patterns"},
                {"name": "integration", "days": 7, "focus": "stabilizing_changes"}
            ],
            "nlp_intensity": "high",
            "daily_exercises": 3,
            "ericksonian_density": "maximum"
        },
        "stabilization": {  # 21 день - укрепление
            "duration": 21,
            "phases": [
                {"name": "assessment", "days": 5, "focus": "current_state_analysis"},
                {"name": "gradual_change", "days": 11, "focus": "step_by_step_improvement"},
                {"name": "maintenance", "days": 5, "focus": "habit_formation"}
            ],
            "nlp_intensity": "moderate",
            "daily_exercises": 2,
            "ericksonian_density": "optimal"
        },
        "development": {  # 14 дней - развитие
            "duration": 14,
            "phases": [
                {"name": "skill_building", "days": 7, "focus": "learning_techniques"},
                {"name": "mastery", "days": 7, "focus": "advanced_application"}
            ],
            "nlp_intensity": "moderate",
            "daily_exercises": 2,
            "ericksonian_density": "selective"
        }
    })

    # Культурные адаптации
    cultural_adaptations: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "slavic": {
            "values": ["family", "tradition", "spirituality", "community"],
            "metaphors": ["природа", "времена года", "народные мудрости"],
            "communication": "direct_emotional",
            "avoid": ["excessive_individualism", "superficial_positivity"]
        },
        "western": {
            "values": ["individual_achievement", "efficiency", "innovation", "self_reliance"],
            "metaphors": ["sports", "technology", "business", "science"],
            "communication": "structured_rational",
            "avoid": ["fatalism", "passive_acceptance"]
        },
        "eastern": {
            "values": ["harmony", "balance", "wisdom", "patience"],
            "metaphors": ["природные циклы", "инь-ян", "поток", "путь"],
            "communication": "indirect_philosophical",
            "avoid": ["aggressive_change", "disruption_of_harmony"]
        }
    })

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "universal-nlp",
        "ericksonian-hypnosis",
        "content-architecture"
    ])
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"  # AI Agent Factory

    # Имя агента для RAG
    agent_name: str = "universal_nlp_content_architect"

    # Межагентное взаимодействие
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"

    def __post_init__(self):
        """Инициализация дополнительных параметров"""
        # Добавляем теги на основе домена
        if self.domain_type and self.domain_type not in self.knowledge_tags:
            self.knowledge_tags.append(self.domain_type)

        # Устанавливаем domain для RAG
        if not self.knowledge_domain:
            self.knowledge_domain = f"{self.domain_type}.universal-nlp.ai"

    def get_nlp_techniques(self, domain: Optional[str] = None) -> List[str]:
        """Получить NLP техники для конкретного домена"""
        target_domain = domain or self.domain_type
        return self.nlp_techniques.get(target_domain, self.nlp_techniques["psychology"])

    def get_ericksonian_patterns(self, domain: Optional[str] = None) -> List[str]:
        """Получить Эриксоновские паттерны для конкретного домена"""
        target_domain = domain or self.domain_type
        return self.ericksonian_patterns.get(target_domain, self.ericksonian_patterns["psychology"])

    def get_vak_adaptation(self, vak_type: str, domain: Optional[str] = None) -> Dict[str, Any]:
        """Получить VAK адаптацию для конкретного типа и домена"""
        target_domain = domain or self.domain_type
        vak_data = self.vak_adaptations.get(vak_type, self.vak_adaptations["visual"])

        # Добавляем домен-специфичные метафоры
        domain_key = f"{target_domain}_metaphors"
        if domain_key in vak_data:
            vak_data["domain_metaphors"] = vak_data[domain_key]

        return vak_data

    def get_age_adaptation(self, age: int) -> Dict[str, Any]:
        """Получить адаптацию по возрасту"""
        if age <= 25:
            return self.age_adaptations["youth"]
        elif age <= 35:
            return self.age_adaptations["friendly"]
        else:
            return self.age_adaptations["professional"]

    def get_transformation_config(self, complexity: str) -> Dict[str, Any]:
        """Получить конфигурацию трансформационной программы"""
        return self.transformation_complexity.get(complexity, self.transformation_complexity["stabilization"])

    def get_cultural_adaptation(self, culture: str) -> Dict[str, Any]:
        """Получить культурную адаптацию"""
        return self.cultural_adaptations.get(culture, self.cultural_adaptations["slavic"])

    def should_delegate(self, task_keywords: List[str]) -> Optional[str]:
        """
        Определить нужно ли делегировать задачу и кому
        """
        # Матрица компетенций для делегирования
        delegation_map = {
            "transformation_plan": "nlp_transformation_planner_agent",
            "content_generation": "nlp_content_generator_agent",
            "quality_check": "nlp_quality_guardian_agent",
            "orchestration": "nlp_content_orchestrator_agent",
            "research": "nlp_research_agent",
            "testing": "nlp_test_generator_agent"
        }

        for keyword_group, agent in delegation_map.items():
            if any(kw in keyword_group for kw in task_keywords):
                return agent

        return None

    def get_domain_specific_config(self) -> Dict[str, Any]:
        """Получить домен-специфичную конфигурацию"""
        domain_configs = {
            "psychology": {
                "scientific_approach": True,
                "clinical_safety": True,
                "evidence_based": True,
                "ethical_guidelines": "apa_standards"
            },
            "astrology": {
                "symbolic_approach": True,
                "tradition_respect": True,
                "empowerment_focus": True,
                "disclaimer_required": True
            },
            "tarot": {
                "intuitive_approach": True,
                "archetypal_focus": True,
                "empowerment_emphasis": True,
                "personal_responsibility": True
            },
            "numerology": {
                "analytical_approach": True,
                "mathematical_accuracy": True,
                "pattern_focus": True,
                "transparency_required": True
            },
            "coaching": {
                "goal_oriented": True,
                "action_focused": True,
                "client_autonomy": True,
                "professional_boundaries": True
            },
            "wellness": {
                "holistic_approach": True,
                "safety_first": True,
                "gradual_progress": True,
                "individual_adaptation": True
            }
        }

        return domain_configs.get(self.domain_type, domain_configs["psychology"])

def get_nlp_config() -> UniversalNLPDependencies:
    """
    Получить конфигурацию зависимостей из переменных окружения
    """
    return UniversalNLPDependencies(
        domain_type=os.getenv("DOMAIN_TYPE", "psychology"),
        content_type=os.getenv("CONTENT_TYPE", "diagnostic_test"),
        target_language=os.getenv("TARGET_LANGUAGE", "ukrainian"),
        nlp_methodology=os.getenv("NLP_METHODOLOGY", "ericksonian_full"),
        archon_project_id=os.getenv("ARCHON_PROJECT_ID", "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a")
    )

# Константы для валидации
SUPPORTED_DOMAINS = [
    "psychology", "astrology", "tarot", "numerology",
    "coaching", "wellness", "spirituality", "self_development"
]

SUPPORTED_CONTENT_TYPES = [
    "diagnostic_test", "transformation_program", "guidance_system",
    "assessment_tool", "meditation_program", "coaching_framework",
    "divination_system", "analysis_framework"
]

SUPPORTED_LANGUAGES = ["ukrainian", "russian", "english"]

NLP_TECHNIQUE_CATEGORIES = [
    "reframing", "anchoring", "rapport", "meta_programs", "submodalities",
    "timeline", "parts", "beliefs", "modeling", "strategies"
]

ERICKSONIAN_PATTERN_TYPES = [
    "metaphors", "embedded_commands", "truisms", "presuppositions",
    "utilization", "confusion", "double_binds", "indirect_suggestions"
]