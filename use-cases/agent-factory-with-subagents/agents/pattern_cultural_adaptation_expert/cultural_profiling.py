"""
Система культурного профилирования пользователя для PatternShift.

Определяет культурную и религиозную принадлежность пользователя
независимо от его географического местоположения.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

from .dependencies import (
    PatternShiftCulture,
    PatternShiftReligion,
    PatternShiftCulturalProfile,
    PatternShiftPhase,
    ModuleType
)


class CulturalQuestionType(Enum):
    """Типы вопросов для культурного профилирования."""
    DIRECT_CULTURE = "direct_culture"
    LANGUAGE_PREFERENCE = "language_preference"
    RELIGIOUS_AFFILIATION = "religious_affiliation"
    CULTURAL_VALUES = "cultural_values"
    FAMILY_TRADITIONS = "family_traditions"
    HISTORICAL_REFERENCES = "historical_references"
    METAPHOR_PREFERENCES = "metaphor_preferences"
    COMMUNICATION_STYLE = "communication_style"


@dataclass
class CulturalQuestion:
    """Вопрос для определения культурной принадлежности."""
    id: str
    question_type: CulturalQuestionType
    question_text_ru: str
    question_text_en: str
    answer_options: List[Dict[str, Any]]
    weight: int  # вес при определении культуры (1-10)
    helps_determine: List[PatternShiftCulture]  # какие культуры помогает определить


@dataclass
class UserCulturalResponse:
    """Ответ пользователя на культурный вопрос."""
    question_id: str
    selected_option_id: str
    confidence_level: int = 5  # 1-10, насколько уверен пользователь


@dataclass
class CulturalProfilingResult:
    """Результат культурного профилирования."""
    primary_culture: PatternShiftCulture
    primary_religion: PatternShiftReligion
    confidence_score: float  # 0.0-1.0
    alternative_cultures: List[Tuple[PatternShiftCulture, float]]  # альтернативы с весами
    cultural_profile: PatternShiftCulturalProfile
    profiling_notes: str


class PatternShiftCulturalProfiler:
    """Система культурного профилирования для PatternShift."""

    def __init__(self):
        self.questions = self._initialize_cultural_questions()
        self.culture_scoring_matrix = self._create_culture_scoring_matrix()

    def _initialize_cultural_questions(self) -> List[CulturalQuestion]:
        """Создать набор вопросов для культурного профилирования."""

        questions = [
            # Прямой вопрос о культурной принадлежности
            CulturalQuestion(
                id="direct_culture",
                question_type=CulturalQuestionType.DIRECT_CULTURE,
                question_text_ru="С какой культурой вы себя больше всего отождествляете?",
                question_text_en="Which culture do you most identify with?",
                answer_options=[
                    {"id": "ukrainian", "text_ru": "Украинская", "text_en": "Ukrainian", "culture": PatternShiftCulture.UKRAINIAN},
                    {"id": "polish", "text_ru": "Польская", "text_en": "Polish", "culture": PatternShiftCulture.POLISH},
                    {"id": "english", "text_ru": "Английская/Американская", "text_en": "English/American", "culture": PatternShiftCulture.ENGLISH},
                    {"id": "german", "text_ru": "Немецкая", "text_en": "German", "culture": PatternShiftCulture.GERMAN},
                    {"id": "french", "text_ru": "Французская", "text_en": "French", "culture": PatternShiftCulture.FRENCH},
                    {"id": "italian", "text_ru": "Итальянская", "text_en": "Italian", "culture": PatternShiftCulture.ITALIAN},
                    {"id": "spanish", "text_ru": "Испанская", "text_en": "Spanish", "culture": PatternShiftCulture.SPANISH},
                    {"id": "russian", "text_ru": "Русская", "text_en": "Russian", "culture": PatternShiftCulture.RUSSIAN},
                    {"id": "other", "text_ru": "Другая/Смешанная", "text_en": "Other/Mixed", "culture": None}
                ],
                weight=10,
                helps_determine=list(PatternShiftCulture)
            ),

            # Религиозная принадлежность
            CulturalQuestion(
                id="religious_affiliation",
                question_type=CulturalQuestionType.RELIGIOUS_AFFILIATION,
                question_text_ru="Какая религиозная традиция вам ближе?",
                question_text_en="Which religious tradition is closest to you?",
                answer_options=[
                    {"id": "orthodox", "text_ru": "Православие", "text_en": "Orthodox Christianity", "religion": PatternShiftReligion.ORTHODOX},
                    {"id": "catholic", "text_ru": "Католицизм", "text_en": "Catholicism", "religion": PatternShiftReligion.CATHOLIC},
                    {"id": "protestant", "text_ru": "Протестантизм", "text_en": "Protestantism", "religion": PatternShiftReligion.PROTESTANT},
                    {"id": "secular", "text_ru": "Светские взгляды", "text_en": "Secular views", "religion": PatternShiftReligion.SECULAR},
                    {"id": "mixed", "text_ru": "Смешанные традиции", "text_en": "Mixed traditions", "religion": PatternShiftReligion.MIXED}
                ],
                weight=8,
                helps_determine=[PatternShiftCulture.UKRAINIAN, PatternShiftCulture.POLISH, PatternShiftCulture.GERMAN]
            ),

            # Языковые предпочтения
            CulturalQuestion(
                id="language_preference",
                question_type=CulturalQuestionType.LANGUAGE_PREFERENCE,
                question_text_ru="На каком языке вы предпочитаете получать психологические материалы?",
                question_text_en="In which language do you prefer to receive psychological materials?",
                answer_options=[
                    {"id": "ukrainian", "text_ru": "Украинский", "text_en": "Ukrainian", "cultures": [PatternShiftCulture.UKRAINIAN]},
                    {"id": "polish", "text_ru": "Польский", "text_en": "Polish", "cultures": [PatternShiftCulture.POLISH]},
                    {"id": "english", "text_ru": "Английский", "text_en": "English", "cultures": [PatternShiftCulture.ENGLISH]},
                    {"id": "german", "text_ru": "Немецкий", "text_en": "German", "cultures": [PatternShiftCulture.GERMAN]},
                    {"id": "french", "text_ru": "Французский", "text_en": "French", "cultures": [PatternShiftCulture.FRENCH]},
                    {"id": "russian", "text_ru": "Русский", "text_en": "Russian", "cultures": [PatternShiftCulture.RUSSIAN]}
                ],
                weight=7,
                helps_determine=list(PatternShiftCulture)
            ),

            # Семейные традиции
            CulturalQuestion(
                id="family_traditions",
                question_type=CulturalQuestionType.FAMILY_TRADITIONS,
                question_text_ru="Какие семейные традиции для вас наиболее значимы?",
                question_text_en="Which family traditions are most meaningful to you?",
                answer_options=[
                    {"id": "orthodox_holidays", "text_ru": "Православные праздники и традиции", "text_en": "Orthodox holidays and traditions",
                     "cultures": [PatternShiftCulture.UKRAINIAN, PatternShiftCulture.RUSSIAN, PatternShiftCulture.SERBIAN]},
                    {"id": "catholic_traditions", "text_ru": "Католические традиции и обряды", "text_en": "Catholic traditions and rituals",
                     "cultures": [PatternShiftCulture.POLISH, PatternShiftCulture.ITALIAN, PatternShiftCulture.FRENCH]},
                    {"id": "secular_family", "text_ru": "Светские семейные ценности", "text_en": "Secular family values",
                     "cultures": [PatternShiftCulture.ENGLISH, PatternShiftCulture.GERMAN]},
                    {"id": "mixed_traditions", "text_ru": "Смешанные культурные традиции", "text_en": "Mixed cultural traditions",
                     "cultures": list(PatternShiftCulture)}
                ],
                weight=6,
                helps_determine=list(PatternShiftCulture)
            ),

            # Стиль коммуникации
            CulturalQuestion(
                id="communication_style",
                question_type=CulturalQuestionType.COMMUNICATION_STYLE,
                question_text_ru="Какой стиль общения вам более комфортен?",
                question_text_en="Which communication style is more comfortable for you?",
                answer_options=[
                    {"id": "high_context", "text_ru": "Эмоциональный, с подтекстом и историями", "text_en": "Emotional, with subtext and stories",
                     "cultures": [PatternShiftCulture.UKRAINIAN, PatternShiftCulture.RUSSIAN, PatternShiftCulture.ITALIAN]},
                    {"id": "medium_context", "text_ru": "Традиционный, с уважением к авторитету", "text_en": "Traditional, with respect for authority",
                     "cultures": [PatternShiftCulture.POLISH, PatternShiftCulture.GERMAN]},
                    {"id": "low_context", "text_ru": "Прямой, конкретный и практичный", "text_en": "Direct, specific and practical",
                     "cultures": [PatternShiftCulture.ENGLISH]},
                    {"id": "flexible", "text_ru": "Адаптивный в зависимости от ситуации", "text_en": "Adaptive depending on situation",
                     "cultures": list(PatternShiftCulture)}
                ],
                weight=5,
                helps_determine=list(PatternShiftCulture)
            ),

            # Предпочтения метафор
            CulturalQuestion(
                id="metaphor_preferences",
                question_type=CulturalQuestionType.METAPHOR_PREFERENCES,
                question_text_ru="Какие образы и метафоры лучше всего помогают вам понять новые идеи?",
                question_text_en="Which images and metaphors best help you understand new ideas?",
                answer_options=[
                    {"id": "nature_home", "text_ru": "Природа, дом, семейный очаг", "text_en": "Nature, home, family hearth",
                     "cultures": [PatternShiftCulture.UKRAINIAN, PatternShiftCulture.RUSSIAN]},
                    {"id": "tradition_church", "text_ru": "Традиции, церковь, семейные ценности", "text_en": "Traditions, church, family values",
                     "cultures": [PatternShiftCulture.POLISH, PatternShiftCulture.ITALIAN]},
                    {"id": "business_tech", "text_ru": "Бизнес, технологии, достижения", "text_en": "Business, technology, achievements",
                     "cultures": [PatternShiftCulture.ENGLISH, PatternShiftCulture.GERMAN]},
                    {"id": "culture_art", "text_ru": "Культура, искусство, философия", "text_en": "Culture, art, philosophy",
                     "cultures": [PatternShiftCulture.FRENCH, PatternShiftCulture.ITALIAN]}
                ],
                weight=4,
                helps_determine=list(PatternShiftCulture)
            ),

            # Культурные ценности
            CulturalQuestion(
                id="cultural_values",
                question_type=CulturalQuestionType.CULTURAL_VALUES,
                question_text_ru="Какие ценности для вас наиболее важны?",
                question_text_en="Which values are most important to you?",
                answer_options=[
                    {"id": "community_family", "text_ru": "Община, семья, взаимопомощь", "text_en": "Community, family, mutual aid",
                     "cultures": [PatternShiftCulture.UKRAINIAN, PatternShiftCulture.POLISH, PatternShiftCulture.RUSSIAN]},
                    {"id": "individual_freedom", "text_ru": "Индивидуальная свобода, самореализация", "text_en": "Individual freedom, self-realization",
                     "cultures": [PatternShiftCulture.ENGLISH, PatternShiftCulture.FRENCH]},
                    {"id": "order_discipline", "text_ru": "Порядок, дисциплина, качество", "text_en": "Order, discipline, quality",
                     "cultures": [PatternShiftCulture.GERMAN]},
                    {"id": "balance_harmony", "text_ru": "Баланс между традициями и современностью", "text_en": "Balance between tradition and modernity",
                     "cultures": list(PatternShiftCulture)}
                ],
                weight=6,
                helps_determine=list(PatternShiftCulture)
            )
        ]

        return questions

    def _create_culture_scoring_matrix(self) -> Dict[str, Dict[PatternShiftCulture, int]]:
        """Создать матрицу подсчета баллов для определения культуры."""

        # Базовая матрица - каждый ответ получает баллы для соответствующих культур
        matrix = {}

        for question in self.questions:
            matrix[question.id] = {}
            for option in question.answer_options:
                # Прямое указание культуры
                if 'culture' in option and option['culture']:
                    culture = option['culture']
                    if culture not in matrix[question.id]:
                        matrix[question.id][culture] = {}
                    matrix[question.id][culture][option['id']] = question.weight

                # Список культур
                if 'cultures' in option:
                    for culture in option['cultures']:
                        if culture not in matrix[question.id]:
                            matrix[question.id][culture] = {}
                        matrix[question.id][culture][option['id']] = question.weight // len(option['cultures'])

        return matrix

    def get_cultural_questions(self, language: str = "ru") -> List[Dict[str, Any]]:
        """Получить вопросы для культурного профилирования."""

        questions_data = []
        for question in self.questions:
            question_text = question.question_text_ru if language == "ru" else question.question_text_en

            options = []
            for option in question.answer_options:
                option_text = option.get(f'text_{language}', option['text_ru'])
                options.append({
                    'id': option['id'],
                    'text': option_text
                })

            questions_data.append({
                'id': question.id,
                'question': question_text,
                'type': question.question_type.value,
                'options': options,
                'weight': question.weight
            })

        return questions_data

    def analyze_cultural_profile(self, responses: List[UserCulturalResponse]) -> CulturalProfilingResult:
        """Проанализировать ответы пользователя и определить культурный профиль."""

        # Подсчет баллов по культурам
        culture_scores = {culture: 0 for culture in PatternShiftCulture}
        religion_scores = {religion: 0 for religion in PatternShiftReligion}

        total_weight = 0

        for response in responses:
            question = next((q for q in self.questions if q.id == response.question_id), None)
            if not question:
                continue

            selected_option = next((opt for opt in question.answer_options
                                  if opt['id'] == response.selected_option_id), None)
            if not selected_option:
                continue

            # Увеличиваем вес ответа согласно уверенности пользователя
            confidence_multiplier = response.confidence_level / 10.0
            effective_weight = question.weight * confidence_multiplier
            total_weight += effective_weight

            # Подсчет баллов для культур
            if 'culture' in selected_option and selected_option['culture']:
                culture_scores[selected_option['culture']] += effective_weight

            if 'cultures' in selected_option:
                score_per_culture = effective_weight / len(selected_option['cultures'])
                for culture in selected_option['cultures']:
                    culture_scores[culture] += score_per_culture

            # Подсчет баллов для религий
            if 'religion' in selected_option and selected_option['religion']:
                religion_scores[selected_option['religion']] += effective_weight

        # Определение основной культуры
        primary_culture = max(culture_scores.items(), key=lambda x: x[1])
        primary_religion = max(religion_scores.items(), key=lambda x: x[1])

        # Расчет уверенности
        confidence_score = primary_culture[1] / max(total_weight, 1)

        # Альтернативные культуры
        sorted_cultures = sorted(culture_scores.items(), key=lambda x: x[1], reverse=True)
        alternative_cultures = [(culture, score/max(total_weight, 1))
                               for culture, score in sorted_cultures[1:4] if score > 0]

        # Создание культурного профиля
        from .dependencies import PATTERNSHIFT_CULTURAL_PROFILES
        cultural_profile = PATTERNSHIFT_CULTURAL_PROFILES.get(
            primary_culture[0],
            PATTERNSHIFT_CULTURAL_PROFILES[PatternShiftCulture.ENGLISH]  # fallback
        )

        # Обновление профиля согласно определенной религии
        if primary_religion[0]:
            cultural_profile.religion = primary_religion[0]

        # Заметки о профилировании
        profiling_notes = self._generate_profiling_notes(
            responses, primary_culture[0], primary_religion[0], confidence_score
        )

        return CulturalProfilingResult(
            primary_culture=primary_culture[0],
            primary_religion=primary_religion[0],
            confidence_score=confidence_score,
            alternative_cultures=alternative_cultures,
            cultural_profile=cultural_profile,
            profiling_notes=profiling_notes
        )

    def _generate_profiling_notes(self, responses: List[UserCulturalResponse],
                                 culture: PatternShiftCulture, religion: PatternShiftReligion,
                                 confidence: float) -> str:
        """Генерировать заметки о процессе профилирования."""

        notes = f"Культурное профилирование завершено:\n"
        notes += f"- Определенная культура: {culture.value} (уверенность: {confidence:.1%})\n"
        notes += f"- Религиозный контекст: {religion.value}\n"
        notes += f"- Количество ответов: {len(responses)}\n"

        if confidence < 0.6:
            notes += f"- ВНИМАНИЕ: Низкая уверенность профилирования. Рекомендуется дополнительное уточнение.\n"
        elif confidence > 0.8:
            notes += f"- Высокая уверенность профилирования. Рекомендации будут точными.\n"

        # Анализ согласованности ответов
        direct_culture_response = next((r for r in responses if r.question_id == "direct_culture"), None)
        if direct_culture_response:
            notes += f"- Прямое указание культуры учтено в профилировании\n"

        return notes

    def suggest_follow_up_questions(self, current_result: CulturalProfilingResult) -> List[Dict[str, Any]]:
        """Предложить дополнительные вопросы для уточнения профиля."""

        follow_up_questions = []

        # Если низкая уверенность, добавляем уточняющие вопросы
        if current_result.confidence_score < 0.6:
            follow_up_questions.extend([
                {
                    "question": "В какой стране вы провели большую часть своего детства?",
                    "type": "geographic_background",
                    "purpose": "уточнение_культурного_контекста"
                },
                {
                    "question": "Какой язык был основным в вашей семье?",
                    "type": "family_language",
                    "purpose": "уточнение_языкового_контекста"
                }
            ])

        # Специальные вопросы для смешанных культур
        if current_result.primary_culture in [PatternShiftCulture.GERMAN] and len(current_result.alternative_cultures) > 1:
            follow_up_questions.append({
                "question": "Вы выросли в моно- или мультикультурной среде?",
                "type": "cultural_environment",
                "purpose": "определение_адаптации_программы"
            })

        return follow_up_questions


# Convenience функции

def create_cultural_profiler() -> PatternShiftCulturalProfiler:
    """Создать экземпляр культурного профайлера."""
    return PatternShiftCulturalProfiler()


def get_registration_questions(language: str = "ru") -> List[Dict[str, Any]]:
    """Получить вопросы для этапа регистрации пользователя."""
    profiler = create_cultural_profiler()
    return profiler.get_cultural_questions(language)


def analyze_user_culture(responses: List[Dict[str, Any]]) -> CulturalProfilingResult:
    """Проанализировать ответы пользователя и определить его культурный профиль."""

    profiler = create_cultural_profiler()

    # Конвертация ответов в правильный формат
    cultural_responses = []
    for response in responses:
        cultural_responses.append(UserCulturalResponse(
            question_id=response.get('question_id', ''),
            selected_option_id=response.get('selected_option_id', ''),
            confidence_level=response.get('confidence_level', 5)
        ))

    return profiler.analyze_cultural_profile(cultural_responses)