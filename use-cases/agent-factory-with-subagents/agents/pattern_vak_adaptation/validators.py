"""
Дополнительные валидаторы для Pattern VAK Adaptation Specialist Agent.

Этот модуль содержит улучшенные валидаторы безопасности, качества и целостности
для обеспечения безопасного и эффективного функционирования агента.
"""

import re
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .dependencies import VAKModalityType, AdaptationDepth, PatternShiftModuleType


class ValidationSeverity(Enum):
    """Уровни серьезности валидационных проблем."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationResult:
    """Результат валидации."""
    is_valid: bool
    severity: ValidationSeverity
    issues: List[str]
    recommendations: List[str]
    confidence_score: float


class SafetyValidator:
    """Валидатор безопасности для терапевтического контента."""

    # Потенциально опасные фразы и паттерны
    DANGEROUS_PATTERNS = [
        # Принуждение и насилие
        r'\b(заставьте?|принудьте?|против воли|насильно)\b',
        r'\b(игнорируйте дискомфорт|подавите|не обращайте внимания на боль)\b',

        # Медицинские утверждения
        r'\b(вылечит|излечит|диагноз|лекарство|терапия заменит)\b',
        r'\b(медицинские показания|противопоказания|побочные эффекты)\b',

        # Гарантии результата
        r'\b(гарантируется|обязательно поможет|100% результат)\b',
        r'\b(навсегда избавит|полностью исключит)\b',

        # Травматичные элементы
        r'\b(травма|насилие|жестокость|боль|страдание)\b(?!\s+(в прошлом|была преодолена))',

        # Мистические утверждения
        r'\b(магия|колдовство|сверхъестественное|паранормальное)\b'
    ]

    # Позитивные элементы безопасности
    SAFETY_INDICATORS = [
        r'\b(комфортно|безопасно|в своем темпе|при желании)\b',
        r'\b(остановиться|границы|выбор|контроль)\b',
        r'\b(поддержка|забота|понимание|принятие)\b',
        r'\b(можете|имеете право|позвольте себе)\b'
    ]

    def __init__(self, adaptation_depth: AdaptationDepth):
        self.adaptation_depth = adaptation_depth
        self.min_safety_score = self._get_min_safety_score()

    def _get_min_safety_score(self) -> float:
        """Определить минимальный требуемый уровень безопасности."""
        if self.adaptation_depth == AdaptationDepth.DEEP:
            return 0.8  # Высокие требования для глубокой адаптации
        elif self.adaptation_depth == AdaptationDepth.MODERATE:
            return 0.6  # Средние требования
        else:
            return 0.4  # Базовые требования

    async def validate_content_safety(self, content: Dict[str, Any]) -> ValidationResult:
        """Валидация безопасности контента."""
        issues = []
        recommendations = []
        safety_score = 0.0

        content_text = f"{content.get('title', '')} {content.get('content', '')}".lower()

        # Проверка опасных паттернов
        dangerous_found = []
        for pattern in self.DANGEROUS_PATTERNS:
            matches = re.findall(pattern, content_text, re.IGNORECASE | re.UNICODE)
            if matches:
                dangerous_found.extend(matches)

        if dangerous_found:
            issues.append(f"Обнаружены потенциально опасные элементы: {', '.join(set(dangerous_found))}")
            recommendations.append("Удалите или переформулируйте опасные элементы")
            safety_score -= 0.3

        # Проверка позитивных индикаторов безопасности
        safety_found = []
        for pattern in self.SAFETY_INDICATORS:
            matches = re.findall(pattern, content_text, re.IGNORECASE | re.UNICODE)
            if matches:
                safety_found.extend(matches)

        safety_indicators_ratio = len(set(safety_found)) / max(len(self.SAFETY_INDICATORS), 1)
        safety_score += safety_indicators_ratio * 0.5

        # Базовый score
        safety_score += 0.5

        # Проверка длины контента (слишком короткий может быть небезопасным)
        content_length = len(content.get('content', ''))
        if content_length < 50:
            issues.append("Контент слишком короткий для надежной оценки безопасности")
            safety_score -= 0.1

        # Проверка наличия инструкций по безопасности для терапевтического контента
        module_type = content.get('module_type')
        if module_type in [PatternShiftModuleType.TECHNIQUE, PatternShiftModuleType.EXERCISE]:
            if not any(indicator in content_text for indicator in ['остановиться', 'комфортно', 'безопасно']):
                recommendations.append("Добавьте инструкции по безопасности и возможности остановки")

        # Нормализация score
        safety_score = max(0.0, min(1.0, safety_score))

        # Определение валидности
        is_valid = safety_score >= self.min_safety_score and len([i for i in issues if 'опасные' in i]) == 0

        severity = ValidationSeverity.INFO
        if safety_score < 0.3:
            severity = ValidationSeverity.CRITICAL
        elif safety_score < 0.5:
            severity = ValidationSeverity.ERROR
        elif safety_score < 0.7:
            severity = ValidationSeverity.WARNING

        return ValidationResult(
            is_valid=is_valid,
            severity=severity,
            issues=issues,
            recommendations=recommendations,
            confidence_score=safety_score
        )


class QualityValidator:
    """Валидатор качества VAK адаптации."""

    def __init__(self, target_modality: VAKModalityType):
        self.target_modality = target_modality
        self.modality_predicates = self._get_modality_predicates()

    def _get_modality_predicates(self) -> List[str]:
        """Получить предикаты для целевой модальности."""
        predicates_map = {
            VAKModalityType.VISUAL: [
                'видеть', 'смотреть', 'представить', 'показать', 'образ', 'картина',
                'яркий', 'четкий', 'цвет', 'свет', 'темный', 'блестящий', 'фокус'
            ],
            VAKModalityType.AUDITORY: [
                'слышать', 'звук', 'голос', 'говорить', 'слушать', 'тон', 'ритм',
                'громкий', 'тихий', 'мелодия', 'эхо', 'резонанс', 'диалог'
            ],
            VAKModalityType.KINESTHETIC: [
                'чувствовать', 'ощущение', 'прикосновение', 'движение', 'тело',
                'теплый', 'холодный', 'мягкий', 'твердый', 'легкий', 'тяжелый', 'текстура'
            ]
        }
        return predicates_map.get(self.target_modality, [])

    async def validate_adaptation_quality(
        self,
        original_content: Dict[str, Any],
        adapted_content: Dict[str, Any]
    ) -> ValidationResult:
        """Валидация качества адаптации."""
        issues = []
        recommendations = []
        quality_score = 0.0

        # Проверка наличия предикатов целевой модальности
        adapted_text = adapted_content.get('content', '').lower()
        predicates_found = [p for p in self.modality_predicates if p in adapted_text]
        predicates_ratio = len(predicates_found) / len(self.modality_predicates)

        if predicates_ratio < 0.2:
            issues.append(f"Недостаточно предикатов {self.target_modality.value} модальности")
            recommendations.append(f"Добавьте больше {self.target_modality.value} предикатов")

        quality_score += predicates_ratio * 0.4

        # Проверка сохранения ключевых элементов
        original_text = original_content.get('content', '').lower()
        original_words = set(original_text.split())
        adapted_words = set(adapted_text.split())

        preservation_ratio = len(original_words & adapted_words) / len(original_words) if original_words else 0
        if preservation_ratio < 0.3:
            issues.append("Слишком мало сохранено от оригинального контента")
            recommendations.append("Сохраните больше ключевых элементов оригинала")

        quality_score += preservation_ratio * 0.3

        # Проверка структурной адаптации
        structure_score = self._validate_structure_adaptation(adapted_content)
        quality_score += structure_score * 0.3

        # Нормализация
        quality_score = max(0.0, min(1.0, quality_score))

        # Определение валидности
        is_valid = quality_score >= 0.6 and len(issues) < 3

        severity = ValidationSeverity.INFO
        if quality_score < 0.4:
            severity = ValidationSeverity.ERROR
        elif quality_score < 0.6:
            severity = ValidationSeverity.WARNING

        return ValidationResult(
            is_valid=is_valid,
            severity=severity,
            issues=issues,
            recommendations=recommendations,
            confidence_score=quality_score
        )

    def _validate_structure_adaptation(self, content: Dict[str, Any]) -> float:
        """Валидация структурной адаптации."""
        structure_score = 0.5  # Базовый score

        content_text = content.get('content', '')
        if not content_text:
            return 0.0

        # Проверка соответствия структуры модальности
        if self.target_modality == VAKModalityType.VISUAL:
            # Для визуалов: короткие предложения, списки
            sentences = re.split(r'[.!?]+', content_text)
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
            if avg_sentence_length <= 15:
                structure_score += 0.3

        elif self.target_modality == VAKModalityType.AUDITORY:
            # Для аудиалов: ритмичность, повторы
            if re.search(r'\b(во-первых|во-вторых|затем|далее)\b', content_text, re.IGNORECASE):
                structure_score += 0.3

        elif self.target_modality == VAKModalityType.KINESTHETIC:
            # Для кинестетиков: последовательность, поэтапность
            if re.search(r'\b(медленно|постепенно|шаг за шагом|поэтапно)\b', content_text, re.IGNORECASE):
                structure_score += 0.3

        return min(1.0, structure_score)


class IntegrityValidator:
    """Валидатор терапевтической целостности."""

    def __init__(self, preserve_therapeutic_integrity: bool = True):
        self.preserve_therapeutic_integrity = preserve_therapeutic_integrity

    async def validate_therapeutic_integrity(
        self,
        original_content: Dict[str, Any],
        adapted_content: Dict[str, Any]
    ) -> ValidationResult:
        """Валидация сохранения терапевтической целостности."""
        if not self.preserve_therapeutic_integrity:
            return ValidationResult(
                is_valid=True,
                severity=ValidationSeverity.INFO,
                issues=[],
                recommendations=[],
                confidence_score=1.0
            )

        issues = []
        recommendations = []
        integrity_score = 0.0

        # Проверка сохранения цели
        original_title = original_content.get('title', '').lower()
        adapted_title = adapted_content.get('title', '').lower()

        if original_title and adapted_title:
            title_similarity = self._calculate_semantic_similarity(original_title, adapted_title)
            if title_similarity < 0.5:
                issues.append("Цель техники изменена слишком сильно")
                recommendations.append("Сохраните основную цель в заголовке")
            integrity_score += title_similarity * 0.3

        # Проверка сохранения ключевых инструкций
        original_content_text = original_content.get('content', '')
        adapted_content_text = adapted_content.get('content', '')

        # Извлечение ключевых терапевтических терминов
        therapeutic_terms = [
            'техника', 'упражнение', 'практика', 'метод', 'подход',
            'дыхание', 'расслабление', 'концентрация', 'внимание',
            'осознанность', 'принятие', 'работа', 'процесс'
        ]

        original_terms = [term for term in therapeutic_terms if term in original_content_text.lower()]
        adapted_terms = [term for term in therapeutic_terms if term in adapted_content_text.lower()]

        terms_preservation = len(set(original_terms) & set(adapted_terms)) / len(original_terms) if original_terms else 1.0
        if terms_preservation < 0.7:
            issues.append("Утрачены ключевые терапевтические элементы")
            recommendations.append("Сохраните больше терапевтических терминов")

        integrity_score += terms_preservation * 0.4

        # Проверка этических принципов
        ethical_score = self._validate_ethical_principles(adapted_content_text)
        integrity_score += ethical_score * 0.3

        # Нормализация
        integrity_score = max(0.0, min(1.0, integrity_score))

        # Определение валидности
        is_valid = integrity_score >= 0.7 and len(issues) < 2

        severity = ValidationSeverity.INFO
        if integrity_score < 0.5:
            severity = ValidationSeverity.ERROR
        elif integrity_score < 0.7:
            severity = ValidationSeverity.WARNING

        return ValidationResult(
            is_valid=is_valid,
            severity=severity,
            issues=issues,
            recommendations=recommendations,
            confidence_score=integrity_score
        )

    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Простой расчет семантической похожести."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def _validate_ethical_principles(self, content: str) -> float:
        """Валидация соблюдения этических принципов."""
        ethical_score = 0.5  # Базовый score

        content_lower = content.lower()

        # Позитивные этические элементы
        positive_elements = [
            'выбор', 'согласие', 'добровольно', 'желание',
            'уважение', 'достоинство', 'права', 'свобода'
        ]

        found_positive = sum(1 for element in positive_elements if element in content_lower)
        ethical_score += (found_positive / len(positive_elements)) * 0.3

        # Негативные элементы (снижают score)
        negative_elements = [
            'принуждение', 'обязательно', 'должны', 'необходимо без выбора'
        ]

        found_negative = sum(1 for element in negative_elements if element in content_lower)
        ethical_score -= (found_negative / len(negative_elements)) * 0.2

        return max(0.0, min(1.0, ethical_score))


class CompositeValidator:
    """Комплексный валидатор, объединяющий все виды проверок."""

    def __init__(
        self,
        adaptation_depth: AdaptationDepth,
        target_modality: VAKModalityType,
        preserve_therapeutic_integrity: bool = True
    ):
        self.safety_validator = SafetyValidator(adaptation_depth)
        self.quality_validator = QualityValidator(target_modality)
        self.integrity_validator = IntegrityValidator(preserve_therapeutic_integrity)

    async def validate_comprehensive(
        self,
        original_content: Dict[str, Any],
        adapted_content: Dict[str, Any]
    ) -> Dict[str, ValidationResult]:
        """Комплексная валидация всех аспектов."""
        results = {}

        # Параллельное выполнение всех валидаций
        safety_task = self.safety_validator.validate_content_safety(adapted_content)
        quality_task = self.quality_validator.validate_adaptation_quality(original_content, adapted_content)
        integrity_task = self.integrity_validator.validate_therapeutic_integrity(original_content, adapted_content)

        safety_result, quality_result, integrity_result = await asyncio.gather(
            safety_task, quality_task, integrity_task
        )

        results['safety'] = safety_result
        results['quality'] = quality_result
        results['integrity'] = integrity_result

        return results

    def get_overall_validation_summary(self, results: Dict[str, ValidationResult]) -> Dict[str, Any]:
        """Получить общую сводку валидации."""
        all_valid = all(result.is_valid for result in results.values())
        avg_confidence = sum(result.confidence_score for result in results.values()) / len(results)

        all_issues = []
        all_recommendations = []
        max_severity = ValidationSeverity.INFO

        for validation_type, result in results.items():
            all_issues.extend([f"[{validation_type}] {issue}" for issue in result.issues])
            all_recommendations.extend([f"[{validation_type}] {rec}" for rec in result.recommendations])

            if result.severity.value == 'critical':
                max_severity = ValidationSeverity.CRITICAL
            elif result.severity.value == 'error' and max_severity.value != 'critical':
                max_severity = ValidationSeverity.ERROR
            elif result.severity.value == 'warning' and max_severity.value in ['info']:
                max_severity = ValidationSeverity.WARNING

        return {
            'overall_valid': all_valid,
            'overall_confidence': round(avg_confidence, 3),
            'max_severity': max_severity.value,
            'total_issues': len(all_issues),
            'total_recommendations': len(all_recommendations),
            'all_issues': all_issues,
            'all_recommendations': all_recommendations,
            'individual_results': {
                validation_type: {
                    'valid': result.is_valid,
                    'confidence': result.confidence_score,
                    'severity': result.severity.value,
                    'issues_count': len(result.issues),
                    'recommendations_count': len(result.recommendations)
                }
                for validation_type, result in results.items()
            }
        }


# Фабричные функции для удобного создания валидаторов

def create_safety_validator(adaptation_depth: AdaptationDepth) -> SafetyValidator:
    """Создать валидатор безопасности."""
    return SafetyValidator(adaptation_depth)


def create_quality_validator(target_modality: VAKModalityType) -> QualityValidator:
    """Создать валидатор качества."""
    return QualityValidator(target_modality)


def create_integrity_validator(preserve_integrity: bool = True) -> IntegrityValidator:
    """Создать валидатор целостности."""
    return IntegrityValidator(preserve_integrity)


def create_composite_validator(
    adaptation_depth: AdaptationDepth,
    target_modality: VAKModalityType,
    preserve_therapeutic_integrity: bool = True
) -> CompositeValidator:
    """Создать комплексный валидатор."""
    return CompositeValidator(adaptation_depth, target_modality, preserve_therapeutic_integrity)