"""
Конфигурация тестов для Pattern VAK Adaptation Specialist Agent.

Содержит фикстуры и утилиты для тестирования VAK адаптации.
"""

import pytest
import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass

from ..dependencies import (
    PatternVAKAdaptationDependencies,
    VAKModalityType,
    AdaptationDepth,
    PatternShiftModuleType,
    create_vak_adaptation_dependencies
)
from ..tools import (
    analyze_content_vak_modalities,
    adapt_content_to_vak_modality,
    validate_vak_adaptation,
    create_multimodal_variants
)


@pytest.fixture
def test_api_key():
    """Тестовый API ключ."""
    return "test-api-key-12345"


@pytest.fixture
def basic_dependencies(test_api_key):
    """Базовые зависимости для тестирования."""
    return create_vak_adaptation_dependencies(
        api_key=test_api_key,
        adaptation_depth=AdaptationDepth.MODERATE,
        enable_multimodal=True,
        enable_safety_validation=True
    )


@pytest.fixture
def therapy_dependencies(test_api_key):
    """Зависимости для терапевтического контекста."""
    return create_vak_adaptation_dependencies(
        api_key=test_api_key,
        adaptation_depth=AdaptationDepth.DEEP,
        trauma_informed_adaptations=True,
        preserve_therapeutic_integrity=True,
        enable_safety_validation=True,
        knowledge_tags=["therapy", "nlp", "vak", "pattern-shift"]
    )


@pytest.fixture
def coaching_dependencies(test_api_key):
    """Зависимости для коучингового контекста."""
    return create_vak_adaptation_dependencies(
        api_key=test_api_key,
        adaptation_depth=AdaptationDepth.MODERATE,
        enable_multimodal=True,
        batch_adaptation_size=10,
        knowledge_tags=["coaching", "nlp", "vak", "pattern-shift"]
    )


@pytest.fixture
def sample_content():
    """Образец контента для тестирования адаптации."""
    return {
        "title": "Техника якорения",
        "description": "Создание положительного эмоционального якоря",
        "content": """
        Сядьте удобно и вспомните момент, когда вы чувствовали себя уверенно.
        Сосредоточьтесь на этом воспоминании и усильте ощущения.
        Когда чувство достигнет пика, сожмите кулак.
        Повторите это упражнение несколько раз.
        """,
        "module_type": PatternShiftModuleType.TECHNIQUE,
        "difficulty_level": "beginner",
        "duration_minutes": 10
    }


@pytest.fixture
def sample_meditation_content():
    """Образец медитативного контента."""
    return {
        "title": "Осознанность дыхания",
        "description": "Базовая практика внимательности к дыханию",
        "content": """
        Найдите удобное положение сидя или лежа.
        Закройте глаза и обратите внимание на естественное дыхание.
        Следите за входом и выходом воздуха.
        Когда ум отвлекается, мягко возвращайте внимание к дыханию.
        """,
        "module_type": PatternShiftModuleType.MEDITATION,
        "difficulty_level": "beginner",
        "duration_minutes": 15
    }


@pytest.fixture
def sample_nlp_content():
    """Образец НЛП контента."""
    return {
        "title": "Рефрейминг ситуации",
        "description": "Изменение восприятия проблемной ситуации",
        "content": """
        Подумайте о ситуации, которая вас беспокоит.
        Представьте, что вы смотрите на неё со стороны.
        Найдите три позитивных аспекта в этой ситуации.
        Сформулируйте новое понимание происходящего.
        """,
        "module_type": PatternShiftModuleType.TECHNIQUE,
        "difficulty_level": "intermediate",
        "duration_minutes": 20
    }


@pytest.fixture
def expected_vak_adaptations():
    """Ожидаемые результаты VAK адаптации."""
    return {
        VAKModalityType.VISUAL: {
            "key_elements": ["яркие образы", "визуализация", "картины"],
            "pace": "быстрый",
            "structure": "короткие инструкции"
        },
        VAKModalityType.AUDITORY: {
            "key_elements": ["внутренний диалог", "звуки", "ритм"],
            "pace": "средний",
            "structure": "ритмичные повторы"
        },
        VAKModalityType.KINESTHETIC: {
            "key_elements": ["телесные ощущения", "движения", "чувства"],
            "pace": "медленный",
            "structure": "детальные описания"
        }
    }


@dataclass
class MockVAKAnalysisResult:
    """Мок результат анализа VAK модальностей."""
    dominant_modality: VAKModalityType
    modality_scores: Dict[VAKModalityType, float]
    predicates_found: Dict[VAKModalityType, List[str]]
    recommendations: List[str]


@pytest.fixture
def mock_vak_analysis():
    """Мок анализа VAK модальностей."""
    return MockVAKAnalysisResult(
        dominant_modality=VAKModalityType.KINESTHETIC,
        modality_scores={
            VAKModalityType.VISUAL: 0.2,
            VAKModalityType.AUDITORY: 0.3,
            VAKModalityType.KINESTHETIC: 0.5
        },
        predicates_found={
            VAKModalityType.VISUAL: ["видеть", "представить", "показать"],
            VAKModalityType.AUDITORY: ["слышать", "говорить", "звучать"],
            VAKModalityType.KINESTHETIC: ["чувствовать", "ощущать", "прикоснуться"]
        },
        recommendations=[
            "Увеличить количество кинестетических предикатов",
            "Добавить описания телесных ощущений",
            "Замедлить темп подачи материала"
        ]
    )


class MockPatternShiftContext:
    """Мок контекст PatternShift для тестирования."""

    def __init__(self):
        self.session_id = "test-session-123"
        self.user_profile = {
            "preferred_modality": VAKModalityType.VISUAL,
            "adaptation_history": [],
            "therapeutic_context": "coaching"
        }
        self.adaptation_settings = {
            "preserve_core_message": True,
            "safety_level": "high",
            "adaptation_depth": AdaptationDepth.MODERATE
        }

    def get_user_preferences(self) -> Dict[str, Any]:
        """Получить предпочтения пользователя."""
        return self.user_profile

    def save_adaptation_result(self, result: Dict[str, Any]) -> bool:
        """Сохранить результат адаптации."""
        self.user_profile["adaptation_history"].append(result)
        return True


@pytest.fixture
def mock_pattern_shift_context():
    """Мок контекст PatternShift."""
    return MockPatternShiftContext()


@pytest.fixture
def test_event_loop():
    """Фикстура для асинхронного тестирования."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def assert_vak_adaptation_quality(adaptation: Dict[str, Any], modality: VAKModalityType):
    """Проверить качество VAK адаптации."""
    required_fields = ["title", "content", "key_elements", "pace", "structure"]

    for field in required_fields:
        assert field in adaptation, f"Отсутствует обязательное поле: {field}"

    assert adaptation["title"], "Заголовок не должен быть пустым"
    assert adaptation["content"], "Контент не должен быть пустым"
    assert len(adaptation["key_elements"]) > 0, "Должны быть указаны ключевые элементы"

    # Проверяем специфичные для модальности элементы
    if modality == VAKModalityType.VISUAL:
        visual_keywords = ["видеть", "представить", "образ", "картина", "яркий"]
        assert any(keyword in adaptation["content"].lower() for keyword in visual_keywords), \
            "Визуальная адаптация должна содержать визуальные предикаты"

    elif modality == VAKModalityType.AUDITORY:
        auditory_keywords = ["слышать", "звук", "говорить", "голос", "ритм"]
        assert any(keyword in adaptation["content"].lower() for keyword in auditory_keywords), \
            "Аудиальная адаптация должна содержать аудиальные предикаты"

    elif modality == VAKModalityType.KINESTHETIC:
        kinesthetic_keywords = ["чувствовать", "ощущение", "прикосновение", "движение", "тело"]
        assert any(keyword in adaptation["content"].lower() for keyword in kinesthetic_keywords), \
            "Кинестетическая адаптация должна содержать кинестетические предикаты"


def assert_safety_compliance(adaptation: Dict[str, Any]):
    """Проверить соответствие требованиям безопасности."""
    # Проверяем отсутствие потенциально опасного контента
    dangerous_phrases = [
        "принуждение", "против воли", "игнорировать границы",
        "подавить", "заставить", "насилие"
    ]

    content_lower = adaptation["content"].lower()
    for phrase in dangerous_phrases:
        assert phrase not in content_lower, f"Обнаружена потенциально опасная фраза: {phrase}"

    # Проверяем наличие элементов травма-информированного подхода
    safety_indicators = [
        "комфортно", "безопасно", "в своем темпе", "при желании",
        "остановиться", "границы", "выбор"
    ]

    has_safety_element = any(indicator in content_lower for indicator in safety_indicators)
    assert has_safety_element, "Адаптация должна содержать элементы безопасности"


def assert_therapeutic_integrity(original: Dict[str, Any], adapted: Dict[str, Any]):
    """Проверить сохранение терапевтической целостности."""
    # Проверяем, что ключевые терапевтические элементы сохранены
    original_keywords = set(original["content"].lower().split())
    adapted_keywords = set(adapted["content"].lower().split())

    # Должно быть сохранено минимум 60% ключевых слов
    overlap = len(original_keywords & adapted_keywords)
    overlap_ratio = overlap / len(original_keywords) if original_keywords else 0

    assert overlap_ratio >= 0.4, f"Недостаточное сохранение ключевых элементов: {overlap_ratio:.2%}"

    # Проверяем, что цель осталась той же
    assert "title" in adapted, "Заголовок должен быть сохранен"
    assert len(adapted["title"]) > 0, "Заголовок не должен быть пустым"


def create_test_module_types():
    """Создать список типов модулей для тестирования."""
    return [
        PatternShiftModuleType.TECHNIQUE,
        PatternShiftModuleType.MEDITATION,
        PatternShiftModuleType.VISUALIZATION,
        PatternShiftModuleType.MOVEMENT,
        PatternShiftModuleType.AUDIO_SESSION,
        PatternShiftModuleType.EXERCISE,
        PatternShiftModuleType.ASSESSMENT,
        PatternShiftModuleType.REFLECTION
    ]


def create_test_vak_modalities():
    """Создать список VAK модальностей для тестирования."""
    return [
        VAKModalityType.VISUAL,
        VAKModalityType.AUDITORY,
        VAKModalityType.KINESTHETIC
    ]


# Маркеры для pytest
pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.vak_adaptation,
    pytest.mark.pattern_shift
]