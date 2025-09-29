"""
Автоматическое назначение PatternShift культуры пользователю.

Анализирует ответы пользователя на анкету и автоматически определяет
оптимальную культурную адаптацию для программы трансформации.
"""

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json

from .dependencies import (
    PatternShiftCulture,
    PatternShiftReligion,
    PatternShiftCulturalProfile,
    PatternShiftPhase,
    PATTERNSHIFT_CULTURAL_PROFILES
)
from .cultural_profiling import (
    PatternShiftCulturalProfiler,
    UserCulturalResponse,
    CulturalProfilingResult
)


class AssignmentConfidenceLevel(Enum):
    """Уровни уверенности автоматического назначения."""
    VERY_HIGH = "very_high"  # 0.9+ - можно назначать автоматически
    HIGH = "high"            # 0.8-0.89 - рекомендованное назначение
    MEDIUM = "medium"        # 0.6-0.79 - требуется подтверждение пользователя
    LOW = "low"              # 0.4-0.59 - показать варианты на выбор
    VERY_LOW = "very_low"    # <0.4 - требуется дополнительное анкетирование


@dataclass
class CultureAssignmentResult:
    """Результат автоматического назначения культуры."""
    assigned_culture: PatternShiftCulture
    assigned_religion: PatternShiftReligion
    confidence_level: AssignmentConfidenceLevel
    confidence_score: float
    assignment_rationale: str
    alternative_suggestions: List[Tuple[PatternShiftCulture, float]]
    requires_confirmation: bool
    follow_up_questions: List[Dict[str, Any]]
    cultural_profile: PatternShiftCulturalProfile


class PatternShiftCultureAssigner:
    """Система автоматического назначения культуры PatternShift."""

    def __init__(self):
        self.profiler = PatternShiftCulturalProfiler()
        self.culture_compatibility_matrix = self._create_compatibility_matrix()
        self.assignment_rules = self._create_assignment_rules()

    def _create_compatibility_matrix(self) -> Dict[PatternShiftCulture, List[PatternShiftCulture]]:
        """Создать матрицу совместимости культур для fallback назначения."""

        return {
            PatternShiftCulture.UKRAINIAN: [
                PatternShiftCulture.RUSSIAN,   # схожие православные традиции
                PatternShiftCulture.POLISH,    # географически близко
                PatternShiftCulture.ENGLISH    # универсальная адаптация
            ],
            PatternShiftCulture.POLISH: [
                PatternShiftCulture.ITALIAN,   # католические традиции
                PatternShiftCulture.GERMAN,    # географически близко
                PatternShiftCulture.ENGLISH    # универсальная адаптация
            ],
            PatternShiftCulture.RUSSIAN: [
                PatternShiftCulture.UKRAINIAN, # схожие традиции
                PatternShiftCulture.SERBIAN,   # православные традиции
                PatternShiftCulture.ENGLISH    # универсальная адаптация
            ],
            PatternShiftCulture.GERMAN: [
                PatternShiftCulture.ENGLISH,   # светский подход
                PatternShiftCulture.FRENCH,    # западноевропейские ценности
                PatternShiftCulture.POLISH     # географически близко
            ],
            PatternShiftCulture.FRENCH: [
                PatternShiftCulture.ITALIAN,   # романские традиции
                PatternShiftCulture.ENGLISH,   # индивидуализм
                PatternShiftCulture.SPANISH    # романские традиции
            ],
            PatternShiftCulture.ITALIAN: [
                PatternShiftCulture.SPANISH,   # католические традиции
                PatternShiftCulture.FRENCH,    # романские традиции
                PatternShiftCulture.POLISH     # католические традиции
            ],
            PatternShiftCulture.ENGLISH: [
                PatternShiftCulture.GERMAN,    # практический подход
                PatternShiftCulture.FRENCH,    # индивидуализм
                PatternShiftCulture.UKRAINIAN  # как универсальный fallback
            ]
        }

    def _create_assignment_rules(self) -> Dict[str, Any]:
        """Создать правила автоматического назначения культуры."""

        return {
            # Прямые правила - если пользователь явно указал культуру
            "direct_assignment": {
                "weight": 1.0,
                "confidence_boost": 0.3,
                "auto_assign_threshold": 0.8
            },

            # Правила по языку
            "language_rules": {
                "ukrainian": {"culture": PatternShiftCulture.UKRAINIAN, "weight": 0.8},
                "polish": {"culture": PatternShiftCulture.POLISH, "weight": 0.8},
                "english": {"culture": PatternShiftCulture.ENGLISH, "weight": 0.7},
                "german": {"culture": PatternShiftCulture.GERMAN, "weight": 0.8},
                "french": {"culture": PatternShiftCulture.FRENCH, "weight": 0.8},
                "russian": {"culture": PatternShiftCulture.RUSSIAN, "weight": 0.8}
            },

            # Правила по религии
            "religion_rules": {
                PatternShiftReligion.ORTHODOX: {
                    "preferred_cultures": [
                        PatternShiftCulture.UKRAINIAN,
                        PatternShiftCulture.RUSSIAN,
                        PatternShiftCulture.SERBIAN
                    ],
                    "weight": 0.6
                },
                PatternShiftReligion.CATHOLIC: {
                    "preferred_cultures": [
                        PatternShiftCulture.POLISH,
                        PatternShiftCulture.ITALIAN,
                        PatternShiftCulture.FRENCH,
                        PatternShiftCulture.SPANISH
                    ],
                    "weight": 0.6
                },
                PatternShiftReligion.PROTESTANT: {
                    "preferred_cultures": [
                        PatternShiftCulture.GERMAN,
                        PatternShiftCulture.ENGLISH
                    ],
                    "weight": 0.5
                },
                PatternShiftReligion.SECULAR: {
                    "preferred_cultures": [
                        PatternShiftCulture.ENGLISH,
                        PatternShiftCulture.GERMAN,
                        PatternShiftCulture.FRENCH
                    ],
                    "weight": 0.5
                }
            },

            # Минимальные требования для автоназначения
            "auto_assignment_requirements": {
                "min_questions_answered": 4,
                "min_confidence_score": 0.6,
                "max_alternatives_gap": 0.3  # разрыв между первым и вторым вариантом
            }
        }

    def process_registration_responses(self, responses: List[Dict[str, Any]]) -> CultureAssignmentResult:
        """Обработать ответы регистрационной анкеты и назначить культуру."""

        # Конвертация в формат профайлера
        cultural_responses = []
        for response in responses:
            cultural_responses.append(UserCulturalResponse(
                question_id=response.get('question_id', ''),
                selected_option_id=response.get('selected_option_id', ''),
                confidence_level=response.get('confidence_level', 5)
            ))

        # Получение профилирования
        profiling_result = self.profiler.analyze_cultural_profile(cultural_responses)

        # Применение правил назначения
        assignment_result = self._apply_assignment_rules(profiling_result, responses)

        return assignment_result

    def _apply_assignment_rules(self,
                               profiling_result: CulturalProfilingResult,
                               raw_responses: List[Dict[str, Any]]) -> CultureAssignmentResult:
        """Применить правила автоматического назначения культуры."""

        base_confidence = profiling_result.confidence_score
        assigned_culture = profiling_result.primary_culture
        assigned_religion = profiling_result.primary_religion

        # Проверка прямого указания культуры
        direct_culture_response = next(
            (r for r in raw_responses if r.get('question_id') == 'direct_culture'),
            None
        )

        confidence_adjustments = []
        rationale_parts = []

        if direct_culture_response:
            confidence_adjustments.append(0.2)  # повышаем уверенность
            rationale_parts.append("Пользователь прямо указал предпочтительную культуру")

        # Проверка согласованности языка и культуры
        language_response = next(
            (r for r in raw_responses if r.get('question_id') == 'language_preference'),
            None
        )

        if language_response:
            language_id = language_response.get('selected_option_id', '')
            expected_culture = self.assignment_rules['language_rules'].get(language_id, {}).get('culture')

            if expected_culture == assigned_culture:
                confidence_adjustments.append(0.1)
                rationale_parts.append("Языковые предпочтения соответствуют культурной принадлежности")
            elif expected_culture and expected_culture != assigned_culture:
                confidence_adjustments.append(-0.1)
                rationale_parts.append("Обнаружено несоответствие между языком и культурой")

        # Проверка согласованности религии и культуры
        religion_rules = self.assignment_rules['religion_rules'].get(assigned_religion)
        if religion_rules and assigned_culture in religion_rules['preferred_cultures']:
            confidence_adjustments.append(0.1)
            rationale_parts.append("Религиозные взгляды соответствуют культурным традициям")

        # Расчет финальной уверенности
        final_confidence = base_confidence + sum(confidence_adjustments)
        final_confidence = max(0.0, min(1.0, final_confidence))  # ограничиваем 0-1

        # Определение уровня уверенности
        if final_confidence >= 0.9:
            confidence_level = AssignmentConfidenceLevel.VERY_HIGH
        elif final_confidence >= 0.8:
            confidence_level = AssignmentConfidenceLevel.HIGH
        elif final_confidence >= 0.6:
            confidence_level = AssignmentConfidenceLevel.MEDIUM
        elif final_confidence >= 0.4:
            confidence_level = AssignmentConfidenceLevel.LOW
        else:
            confidence_level = AssignmentConfidenceLevel.VERY_LOW

        # Проверка требований для автоназначения
        requires_confirmation = self._check_confirmation_requirement(
            final_confidence, profiling_result.alternative_cultures, raw_responses
        )

        # Формирование рекомендаций
        follow_up_questions = self._generate_follow_up_questions(
            confidence_level, assigned_culture, profiling_result.alternative_cultures
        )

        # Финальное обоснование
        if not rationale_parts:
            rationale_parts.append("Назначение основано на анализе культурных предпочтений")

        rationale = "; ".join(rationale_parts) + f" (уверенность: {final_confidence:.1%})"

        return CultureAssignmentResult(
            assigned_culture=assigned_culture,
            assigned_religion=assigned_religion,
            confidence_level=confidence_level,
            confidence_score=final_confidence,
            assignment_rationale=rationale,
            alternative_suggestions=profiling_result.alternative_cultures[:3],
            requires_confirmation=requires_confirmation,
            follow_up_questions=follow_up_questions,
            cultural_profile=profiling_result.cultural_profile
        )

    def _check_confirmation_requirement(self,
                                      confidence: float,
                                      alternatives: List[Tuple[PatternShiftCulture, float]],
                                      raw_responses: List[Dict[str, Any]]) -> bool:
        """Проверить, требуется ли подтверждение пользователя."""

        requirements = self.assignment_rules['auto_assignment_requirements']

        # Минимальное количество вопросов
        if len(raw_responses) < requirements['min_questions_answered']:
            return True

        # Минимальная уверенность
        if confidence < requirements['min_confidence_score']:
            return True

        # Проверка разрыва с альтернативами
        if alternatives:
            top_alternative_score = alternatives[0][1]
            gap = confidence - top_alternative_score
            if gap < requirements['max_alternatives_gap']:
                return True

        return False

    def _generate_follow_up_questions(self,
                                    confidence_level: AssignmentConfidenceLevel,
                                    assigned_culture: PatternShiftCulture,
                                    alternatives: List[Tuple[PatternShiftCulture, float]]) -> List[Dict[str, Any]]:
        """Сгенерировать дополнительные вопросы при необходимости."""

        follow_up_questions = []

        if confidence_level in [AssignmentConfidenceLevel.LOW, AssignmentConfidenceLevel.VERY_LOW]:
            follow_up_questions.extend([
                {
                    "id": "cultural_upbringing",
                    "question_ru": "В какой культурной среде вы выросли?",
                    "question_en": "What cultural environment did you grow up in?",
                    "type": "open_text",
                    "purpose": "clarify_cultural_background"
                },
                {
                    "id": "family_language",
                    "question_ru": "На каком языке говорили в вашей семье?",
                    "question_en": "What language was spoken in your family?",
                    "type": "open_text",
                    "purpose": "clarify_linguistic_background"
                }
            ])

        if confidence_level == AssignmentConfidenceLevel.MEDIUM and alternatives:
            # Предложить выбор между топ вариантами
            culture_options = [assigned_culture] + [alt[0] for alt in alternatives[:2]]

            follow_up_questions.append({
                "id": "culture_confirmation",
                "question_ru": f"Мы рекомендуем адаптацию для {assigned_culture.value} культуры. Подходит ли вам этот выбор?",
                "question_en": f"We recommend adaptation for {assigned_culture.value} culture. Is this choice suitable for you?",
                "type": "single_choice",
                "options": [
                    {"id": "confirm", "text_ru": "Да, подходит", "text_en": "Yes, suitable"},
                    {"id": "show_alternatives", "text_ru": "Покажите альтернативы", "text_en": "Show alternatives"},
                    {"id": "mixed_approach", "text_ru": "Хочу смешанный подход", "text_en": "Want mixed approach"}
                ],
                "purpose": "confirm_assignment"
            })

        return follow_up_questions

    def get_assignment_explanation(self, result: CultureAssignmentResult, language: str = "ru") -> Dict[str, Any]:
        """Получить объяснение назначения для пользователя."""

        if language == "ru":
            explanation = {
                "title": f"Выбрана {result.assigned_culture.value} культурная адаптация",
                "confidence": f"Уверенность: {result.confidence_score:.0%}",
                "rationale": result.assignment_rationale,
                "what_this_means": [
                    f"Программа будет адаптирована под {result.assigned_culture.value} культурные особенности",
                    f"Религиозный контекст: {result.assigned_religion.value}",
                    "Метафоры и примеры будут культурно релевантными",
                    "Чувствительные темы будут учтены"
                ],
                "can_change": "Вы можете изменить эти настройки в любое время в личном кабинете"
            }
        else:
            explanation = {
                "title": f"Selected {result.assigned_culture.value} cultural adaptation",
                "confidence": f"Confidence: {result.confidence_score:.0%}",
                "rationale": result.assignment_rationale,
                "what_this_means": [
                    f"Program will be adapted to {result.assigned_culture.value} cultural specifics",
                    f"Religious context: {result.assigned_religion.value}",
                    "Metaphors and examples will be culturally relevant",
                    "Sensitive topics will be considered"
                ],
                "can_change": "You can change these settings at any time in your personal account"
            }

        if result.alternative_suggestions:
            if language == "ru":
                explanation["alternatives"] = "Также рассматривались: " + ", ".join([
                    f"{alt[0].value} ({alt[1]:.0%})" for alt in result.alternative_suggestions
                ])
            else:
                explanation["alternatives"] = "Also considered: " + ", ".join([
                    f"{alt[0].value} ({alt[1]:.0%})" for alt in result.alternative_suggestions
                ])

        return explanation

    def handle_mixed_culture_assignment(self,
                                      primary: PatternShiftCulture,
                                      secondary: PatternShiftCulture,
                                      user_preferences: Dict[str, Any]) -> PatternShiftCulturalProfile:
        """Создать смешанный культурный профиль."""

        # Получаем базовые профили
        primary_profile = PATTERNSHIFT_CULTURAL_PROFILES.get(primary)
        secondary_profile = PATTERNSHIFT_CULTURAL_PROFILES.get(secondary)

        if not primary_profile or not secondary_profile:
            # Fallback на основную культуру
            return primary_profile or PATTERNSHIFT_CULTURAL_PROFILES[PatternShiftCulture.ENGLISH]

        # Создаем смешанный профиль
        mixed_profile = PatternShiftCulturalProfile(
            culture=primary,  # основная культура остается
            religion=primary_profile.religion,
            phase=primary_profile.phase,
            target_modules=primary_profile.target_modules,

            # Объединяем чувствительные темы
            sensitive_topics=list(set(
                primary_profile.sensitive_topics + secondary_profile.sensitive_topics
            )),

            # Смешиваем предпочитаемые метафоры
            preferred_metaphors=(
                primary_profile.preferred_metaphors[:3] +
                secondary_profile.preferred_metaphors[:2]
            ),

            # Объединяем культурных героев
            cultural_heroes=(
                primary_profile.cultural_heroes[:2] +
                secondary_profile.cultural_heroes[:1]
            ),

            # Смешиваем исторический контекст
            historical_context={
                **primary_profile.historical_context,
                **secondary_profile.historical_context,
                "mixed_profile": True,
                "secondary_culture": secondary.value
            }
        )

        return mixed_profile


# Convenience функции

def auto_assign_culture_from_registration(responses: List[Dict[str, Any]]) -> CultureAssignmentResult:
    """Автоматически назначить культуру на основе регистрационных данных."""
    assigner = PatternShiftCultureAssigner()
    return assigner.process_registration_responses(responses)


def get_culture_assignment_explanation(result: CultureAssignmentResult, language: str = "ru") -> Dict[str, Any]:
    """Получить объяснение назначения культуры для пользователя."""
    assigner = PatternShiftCultureAssigner()
    return assigner.get_assignment_explanation(result, language)


def create_mixed_cultural_profile(primary: PatternShiftCulture,
                                secondary: PatternShiftCulture,
                                preferences: Dict[str, Any] = None) -> PatternShiftCulturalProfile:
    """Создать смешанный культурный профиль."""
    assigner = PatternShiftCultureAssigner()
    return assigner.handle_mixed_culture_assignment(primary, secondary, preferences or {})