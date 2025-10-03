"""
Зависимости для Pattern Cultural Adaptation Expert Agent.

PatternShift-специфичный агент для культурной адаптации
психологических техник и программ трансформации.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class PatternShiftCulture(Enum):
    """Культуры, поддерживаемые в PatternShift."""
    UKRAINIAN = "ukrainian"
    POLISH = "polish"
    ENGLISH = "english"
    GERMAN = "german"
    FRENCH = "french"
    ITALIAN = "italian"
    SPANISH = "spanish"
    RUSSIAN = "russian"
    CZECH = "czech"
    SLOVAK = "slovak"
    HUNGARIAN = "hungarian"
    ROMANIAN = "romanian"
    BULGARIAN = "bulgarian"
    CROATIAN = "croatian"
    SERBIAN = "serbian"
    SLOVENIAN = "slovenian"
    LITHUANIAN = "lithuanian"
    LATVIAN = "latvian"
    ESTONIAN = "estonian"


class PatternShiftReligion(Enum):
    """Религиозные контексты PatternShift."""
    ORTHODOX = "orthodox"        # Православная традиция (украинская, русская, болгарская, сербская)
    CATHOLIC = "catholic"        # Католическая традиция (польская, немецкая, французская, итальянская, испанская, хорватская, словенская, словацкая, венгерская, литовская, чешская)
    PROTESTANT = "protestant"    # Протестантская традиция (германские страны, балтийские)
    SECULAR = "secular"          # Светский контекст (англоязычные, скандинавские)
    MIXED = "mixed"              # Смешанный религиозный контекст


class PatternShiftPhase(Enum):
    """Фазы программы PatternShift."""
    BEGINNING = "beginning"      # Начальная фаза (дни 1-7)
    DEVELOPMENT = "development"  # Развитие (дни 8-14)
    INTEGRATION = "integration"  # Интеграция (дни 15-21)


class ModuleType(Enum):
    """Типы модулей PatternShift."""
    TECHNIQUE = "technique"      # НЛП техники
    EXERCISE = "exercise"        # Трансформационные упражнения
    HYPNOSIS = "hypnosis"        # Эриксоновский гипноз
    FEEDBACK = "feedback"        # Системы обратной связи
    EDUCATION = "education"      # Образовательные модули
    MIXED_VALUES = "mixed_values"


@dataclass
class PatternShiftCulturalProfile:
    """Профиль культурной адаптации для PatternShift."""
    culture: PatternShiftCulture
    religion: PatternShiftReligion
    phase: PatternShiftPhase
    target_modules: List[ModuleType] = field(default_factory=list)

    # Культурно-специфичные элементы
    sensitive_topics: List[str] = field(default_factory=list)
    preferred_metaphors: List[str] = field(default_factory=list)
    cultural_heroes: List[str] = field(default_factory=list)
    historical_context: Dict[str, Any] = field(default_factory=dict)

    # PatternShift архитектура
    program_duration: int = 21  # дней
    cultural_adaptation_level: str = "deep"  # shallow, moderate, deep


@dataclass
class PatternShiftAdaptationSettings:
    """Настройки адаптации контента для PatternShift."""
    # PatternShift специфика
    patternshift_version: str = "3.0"
    content_pipeline: str = "program->phase->day->session->activity->module"

    # Основные настройки
    adaptation_depth: str = "deep"  # PatternShift использует глубокую адаптацию
    preserve_therapeutic_efficacy: bool = True
    cultural_safety_validation: bool = True

    # PatternShift компоненты
    nlp_techniques_adaptation: bool = True
    ericksonian_patterns_adaptation: bool = True
    vak_modalities_adaptation: bool = True
    microhabits_localization: bool = True
    metaphor_cultural_alignment: bool = True


@dataclass
class PatternCulturalAdaptationExpertDependencies:
    """
    Зависимости для Pattern Cultural Adaptation Expert Agent.

    PatternShift-специфичный агент для культурной адаптации
    психологических программ трансформации.
    """

    # Основные настройки
    api_key: str
    agent_name: str = "pattern_cultural_adaptation_expert"

    # PatternShift интеграция
    patternshift_architecture_files: List[str] = field(default_factory=lambda: [
        "D:\\Automation\\Development\\projects\\patternshift\\docs\\content-agents-system-prompts.md",
        "D:\\Automation\\Development\\projects\\patternshift\\docs\\final-kontent-architecture-complete.md"
    ])

    # RAG конфигурация для PatternShift
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "pattern-cultural-adaptation-expert", "agent-knowledge", "pydantic-ai", "patternshift"
    ])
    knowledge_domain: str = "patternshift-cultural-adaptation"
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # PatternShift культурная конфигурация
    target_culture: PatternShiftCulture = PatternShiftCulture.UKRAINIAN
    cultural_profile: Optional[PatternShiftCulturalProfile] = None
    adaptation_settings: PatternShiftAdaptationSettings = field(default_factory=PatternShiftAdaptationSettings)

    # PatternShift поддерживаемые культуры (расширенный список)
    supported_cultures: List[PatternShiftCulture] = field(default_factory=lambda: [
        PatternShiftCulture.UKRAINIAN,
        PatternShiftCulture.POLISH,
        PatternShiftCulture.ENGLISH,
        PatternShiftCulture.GERMAN,
        PatternShiftCulture.FRENCH,
        PatternShiftCulture.ITALIAN,
        PatternShiftCulture.SPANISH,
        PatternShiftCulture.RUSSIAN,
        PatternShiftCulture.CZECH,
        PatternShiftCulture.SLOVAK,
        PatternShiftCulture.HUNGARIAN,
        PatternShiftCulture.ROMANIAN,
        PatternShiftCulture.BULGARIAN,
        PatternShiftCulture.CROATIAN,
        PatternShiftCulture.SERBIAN,
        PatternShiftCulture.SLOVENIAN,
        PatternShiftCulture.LITHUANIAN,
        PatternShiftCulture.LATVIAN,
        PatternShiftCulture.ESTONIAN
    ])

    # Inter-agent communication
    enable_pattern_agent_delegation: bool = True
    pattern_agents_registry: Dict[str, str] = field(default_factory=lambda: {
        "nlp_technique_master": "Pattern NLP Technique Master Agent",
        "test_architect": "Pattern Test Architect Agent",
        "vak_adaptation_specialist": "Pattern VAK Adaptation Specialist Agent",
        "ericksonian_hypnosis": "Pattern Ericksonian Hypnosis Scriptwriter Agent"
    })

    # PatternShift безопасность
    cultural_safety_validation: bool = True
    therapeutic_efficacy_preservation: bool = True
    religious_sensitivity_mode: bool = True

    def __post_init__(self):
        """Инициализация зависимостей после создания."""
        # Создание культурного профиля по умолчанию если не указан
        if self.cultural_profile is None:
            self.cultural_profile = self._create_default_patternshift_profile()

        # Валидация настроек
        self._validate_patternshift_settings()

    def _create_default_patternshift_profile(self) -> PatternShiftCulturalProfile:
        """Создает профиль культуры PatternShift по умолчанию."""
        default_profiles = {
            # Славянские православные культуры
            PatternShiftCulture.UKRAINIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.UKRAINIAN,
                religion=PatternShiftReligion.ORTHODOX,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.HYPNOSIS],
                sensitive_topics=["война", "оккупация", "национальная идентичность", "травма"],
                preferred_metaphors=["поле", "дуб", "река", "домашний очаг", "мост через реку"],
                cultural_heroes=["Тарас Шевченко", "Леся Украинка", "Иван Франко"],
                historical_context={"current_conflict": True, "independence": "1991", "collective_trauma": True, "cultural_resilience": True}
            ),
            PatternShiftCulture.RUSSIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.RUSSIAN,
                religion=PatternShiftReligion.ORTHODOX,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.HYPNOSIS],
                sensitive_topics=["политика", "история СССР", "национальная идея", "духовность"],
                preferred_metaphors=["берёза", "медведь", "широкая душа", "матушка Россия", "дорога-дороженька"],
                cultural_heroes=["Пушкин", "Достоевский", "Гагарин"],
                historical_context={"imperial_heritage": True, "soviet_legacy": True, "orthodox_revival": True}
            ),
            PatternShiftCulture.BULGARIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.BULGARIAN,
                religion=PatternShiftReligion.ORTHODOX,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.HYPNOSIS],
                sensitive_topics=["османское иго", "национальное возрождение", "балканские войны"],
                preferred_metaphors=["роза", "горы", "древняя мудрость", "золотое наследие"],
                cultural_heroes=["Васил Левски", "Христо Ботев", "Кирилл и Мефодий"],
                historical_context={"ancient_heritage": True, "ottoman_period": True, "eu_membership": "2007"}
            ),
            PatternShiftCulture.SERBIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.SERBIAN,
                religion=PatternShiftReligion.ORTHODOX,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.HYPNOSIS],
                sensitive_topics=["косово", "югославские войны", "национальная гордость"],
                preferred_metaphors=["орёл", "крест", "косово поле", "славянское братство"],
                cultural_heroes=["Свети Сава", "Никола Тесла", "Милош Обилич"],
                historical_context={"kosovo_battle": True, "yugoslavia_legacy": True, "orthodox_identity": True}
            ),

            # Католические культуры
            PatternShiftCulture.POLISH: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.POLISH,
                religion=PatternShiftReligion.CATHOLIC,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.HYPNOSIS],
                sensitive_topics=["католическая мораль", "национальная гордость", "солидарность"],
                preferred_metaphors=["католические образы", "историческая гордость", "семейные традиции"],
                cultural_heroes=["Иоанн Павел II", "Лех Валенса", "Мария Склодовская-Кюри"],
                historical_context={"solidarity_movement": True, "eu_membership": "2004", "cultural_pride": True}
            ),
            PatternShiftCulture.GERMAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.GERMAN,
                religion=PatternShiftReligion.MIXED,  # Католики + Протестанты
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.EDUCATION],
                sensitive_topics=["история 20 века", "нацизм", "миграция", "национализм"],
                preferred_metaphors=["механизм", "порядок", "дисциплина", "качество", "точность"],
                cultural_heroes=["Гёте", "Бетховен", "Эйнштейн"],
                historical_context={"reunification": "1990", "eu_founder": True, "responsibility_culture": True}
            ),
            PatternShiftCulture.FRENCH: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.FRENCH,
                religion=PatternShiftReligion.CATHOLIC,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.EDUCATION],
                sensitive_topics=["революция", "секуляризм", "иммиграция", "национальная идентичность"],
                preferred_metaphors=["элегантность", "искусство", "философия", "свобода", "равенство"],
                cultural_heroes=["Наполеон", "Вольтер", "Мария Кюри"],
                historical_context={"republic_values": True, "cultural_pride": True, "secular_tradition": True}
            ),
            PatternShiftCulture.ITALIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.ITALIAN,
                religion=PatternShiftReligion.CATHOLIC,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.HYPNOSIS],
                sensitive_topics=["семья", "традиции", "региональные различия", "мафия"],
                preferred_metaphors=["семейный очаг", "римское наследие", "ренессанс", "красота", "страсть"],
                cultural_heroes=["Данте", "Леонардо да Винчи", "Микеланджело"],
                historical_context={"roman_heritage": True, "renaissance": True, "family_values": True}
            ),
            PatternShiftCulture.SPANISH: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.SPANISH,
                religion=PatternShiftReligion.CATHOLIC,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.HYPNOSIS],
                sensitive_topics=["франкизм", "региональная автономия", "католические ценности"],
                preferred_metaphors=["солнце", "фиеста", "семья", "честь", "страсть"],
                cultural_heroes=["Сервантес", "Гауди", "Пикассо"],
                historical_context={"reconquista": True, "colonial_empire": True, "democracy_transition": "1975"}
            ),
            PatternShiftCulture.CROATIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.CROATIAN,
                religion=PatternShiftReligion.CATHOLIC,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.HYPNOSIS],
                sensitive_topics=["югославские войны", "независимость", "национальная идентичность"],
                preferred_metaphors=["адриатическое море", "шахматная доска", "католический крест"],
                cultural_heroes=["Франьо Туджман", "Никола Тесла", "Мирослав Крлежа"],
                historical_context={"independence": "1991", "eu_membership": "2013", "yugoslav_legacy": True}
            ),
            PatternShiftCulture.SLOVENIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.SLOVENIAN,
                religion=PatternShiftReligion.CATHOLIC,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.EDUCATION],
                sensitive_topics=["национальная идентичность", "языковая политика", "европейская интеграция"],
                preferred_metaphors=["альпы", "пчела", "липовое дерево", "зелёная природа"],
                cultural_heroes=["Франце Прешерн", "Йоже Плечник", "Примож Трубар"],
                historical_context={"alpine_culture": True, "eu_membership": "2004", "small_nation_pride": True}
            ),
            PatternShiftCulture.SLOVAK: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.SLOVAK,
                religion=PatternShiftReligion.CATHOLIC,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.EDUCATION],
                sensitive_topics=["венгерское господство", "чехословацкий период", "национальная идентичность"],
                preferred_metaphors=["высокие татры", "народные традиции", "деревенская жизнь"],
                cultural_heroes=["Людовит Штур", "Милан Растислав Штефаник", "Александр Дубчек"],
                historical_context={"independence": "1993", "eu_membership": "2004", "slavic_heritage": True}
            ),
            PatternShiftCulture.CZECH: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.CZECH,
                religion=PatternShiftReligion.CATHOLIC,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.EDUCATION],
                sensitive_topics=["коммунизм", "бархатная революция", "атеизм", "немецкое влияние"],
                preferred_metaphors=["пивная культура", "золотые руки", "чешский юмор", "пражская красота"],
                cultural_heroes=["Вацлав Гавел", "Томаш Масарик", "Ян Гус"],
                historical_context={"velvet_revolution": "1989", "eu_membership": "2004", "secular_society": True}
            ),
            PatternShiftCulture.HUNGARIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.HUNGARIAN,
                religion=PatternShiftReligion.CATHOLIC,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.HYPNOSIS],
                sensitive_topics=["трианонский договор", "национальные меньшинства", "венгерская уникальность"],
                preferred_metaphors=["пушта", "венгерская душа", "мадьярская гордость", "дунай"],
                cultural_heroes=["Стефан I", "Лист Ференц", "Имре Надь"],
                historical_context={"unique_language": True, "trianon_trauma": True, "eu_membership": "2004"}
            ),
            PatternShiftCulture.LITHUANIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.LITHUANIAN,
                religion=PatternShiftReligion.CATHOLIC,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.EDUCATION],
                sensitive_topics=["советская оккупация", "депортации", "независимость"],
                preferred_metaphors=["дуб", "янтарь", "балтийское море", "жемайтские холмы"],
                cultural_heroes=["Витаутас Великий", "Винцас Кудирка", "Йонас Базилявичус"],
                historical_context={"grand_duchy": True, "soviet_occupation": "1940-1990", "eu_membership": "2004"}
            ),

            # Протестантские и смешанные культуры
            PatternShiftCulture.LATVIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.LATVIAN,
                religion=PatternShiftReligion.MIXED,  # Лютеране + Католики
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.EDUCATION],
                sensitive_topics=["советская оккупация", "русское меньшинство", "языковая политика"],
                preferred_metaphors=["сосна", "янтарь", "балтийские волны", "песенный праздник"],
                cultural_heroes=["Райнис", "Карлис Улманис", "Вайра Вике-Фрейберга"],
                historical_context={"singing_revolution": True, "soviet_occupation": "1940-1991", "eu_membership": "2004"}
            ),
            PatternShiftCulture.ESTONIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.ESTONIAN,
                religion=PatternShiftReligion.PROTESTANT,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.EDUCATION],
                sensitive_topics=["советская оккупация", "цифровые технологии", "финно-угорская идентичность"],
                preferred_metaphors=["цифровое общество", "лесные традиции", "балтийская независимость"],
                cultural_heroes=["Юри Лотман", "Леннарт Мери", "Константин Пятс"],
                historical_context={"digital_society": True, "finno_ugric": True, "eu_membership": "2004"}
            ),

            # Балканские смешанные культуры
            PatternShiftCulture.ROMANIAN: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.ROMANIAN,
                religion=PatternShiftReligion.ORTHODOX,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.HYPNOSIS],
                sensitive_topics=["чаушеску", "цыгане", "коррупция", "европейская интеграция"],
                preferred_metaphors=["карпаты", "дунай", "латинская душа", "православный крест"],
                cultural_heroes=["Михай Эминеску", "Георге Энеску", "Нико Костеа"],
                historical_context={"latin_heritage": True, "communist_legacy": True, "eu_membership": "2007"}
            ),

            # Светские культуры
            PatternShiftCulture.ENGLISH: PatternShiftCulturalProfile(
                culture=PatternShiftCulture.ENGLISH,
                religion=PatternShiftReligion.SECULAR,
                phase=PatternShiftPhase.BEGINNING,
                target_modules=[ModuleType.TECHNIQUE, ModuleType.EXERCISE, ModuleType.EDUCATION],
                sensitive_topics=["политика", "расовые отношения", "религия"],
                preferred_metaphors=["светские метафоры", "индивидуальный рост", "бизнес аналогии"],
                cultural_heroes=["Martin Luther King", "Shakespeare", "Einstein"],
                historical_context={"diversity": True, "globalization": True, "individualism": True}
            )
        }

        return default_profiles.get(self.target_culture, PatternShiftCulturalProfile(
            culture=self.target_culture,
            religion=PatternShiftReligion.SECULAR,
            phase=PatternShiftPhase.BEGINNING,
            target_modules=[ModuleType.MIXED_VALUES]
        ))

    def _validate_patternshift_settings(self):
        """Валидация настроек PatternShift зависимостей."""
        if self.target_culture not in self.supported_cultures:
            raise ValueError(f"PatternShift культура {self.target_culture} не поддерживается")

        if not self.patternshift_architecture_files:
            raise ValueError("Отсутствуют файлы архитектуры PatternShift")

    def get_patternshift_cultural_context(self) -> Dict[str, Any]:
        """Получить контекст PatternShift культуры для адаптации."""
        if not self.cultural_profile:
            return {}

        return {
            "culture": self.cultural_profile.culture.value,
            "religion": self.cultural_profile.religion.value,
            "phase": self.cultural_profile.phase.value,
            "target_modules": [m.value for m in self.cultural_profile.target_modules],
            "sensitive_topics": self.cultural_profile.sensitive_topics,
            "preferred_metaphors": self.cultural_profile.preferred_metaphors,
            "cultural_heroes": self.cultural_profile.cultural_heroes,
            "historical_context": self.cultural_profile.historical_context,
            "patternshift_settings": {
                "version": self.adaptation_settings.patternshift_version,
                "pipeline": self.adaptation_settings.content_pipeline,
                "depth": self.adaptation_settings.adaptation_depth,
                "preserve_efficacy": self.adaptation_settings.preserve_therapeutic_efficacy,
                "safety_validation": self.adaptation_settings.cultural_safety_validation
            }
        }

    def update_patternshift_culture(self, culture: PatternShiftCulture):
        """Обновить целевую PatternShift культуру и профиль."""
        self.target_culture = culture
        self.cultural_profile = self._create_default_patternshift_profile()

    def is_patternshift_culture_supported(self, culture: PatternShiftCulture) -> bool:
        """Проверить, поддерживается ли PatternShift культура."""
        return culture in self.supported_cultures

    def delegate_to_pattern_agent(self, agent_type: str, task_description: str) -> str:
        """Делегировать задачу другому Pattern агенту через Archon."""
        if not self.enable_pattern_agent_delegation:
            return "Делегирование Pattern агентам отключено"

        if agent_type not in self.pattern_agents_registry:
            return f"Pattern агент {agent_type} не найден в реестре"

        return f"Делегирование задачи '{task_description}' агенту {self.pattern_agents_registry[agent_type]}"


def create_pattern_cultural_adaptation_dependencies(
    api_key: str,
    target_culture: PatternShiftCulture = PatternShiftCulture.UKRAINIAN,
    **kwargs
) -> PatternCulturalAdaptationExpertDependencies:
    """
    Создать зависимости для Pattern Cultural Adaptation Expert.

    Args:
        api_key: Ключ API для LLM
        target_culture: Целевая PatternShift культура
        **kwargs: Дополнительные параметры

    Returns:
        Настроенные зависимости PatternShift агента
    """
    return PatternCulturalAdaptationExpertDependencies(
        api_key=api_key,
        target_culture=target_culture,
        **kwargs
    )


# PatternShift конфигурации для культур
PATTERNSHIFT_UKRAINIAN_CONFIG = {
    "target_culture": PatternShiftCulture.UKRAINIAN,
    "knowledge_tags": ["pattern-cultural-adaptation-expert", "ukrainian-context", "orthodox", "patternshift"]
}

PATTERNSHIFT_POLISH_CONFIG = {
    "target_culture": PatternShiftCulture.POLISH,
    "knowledge_tags": ["pattern-cultural-adaptation-expert", "polish-context", "catholic", "patternshift"]
}

PATTERNSHIFT_ENGLISH_CONFIG = {
    "target_culture": PatternShiftCulture.ENGLISH,
    "knowledge_tags": ["pattern-cultural-adaptation-expert", "english-context", "secular", "patternshift"]
}