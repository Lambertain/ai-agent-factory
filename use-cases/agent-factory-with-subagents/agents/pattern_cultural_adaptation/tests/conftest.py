"""
Конфигурация тестов для Pattern Cultural Adaptation Expert Agent.

Содержит фикстуры и общие настройки для всех тестов.
"""

import pytest
import sys
import os
from unittest.mock import Mock, AsyncMock

# Добавляем путь к родительской директории для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dependencies import CulturalAdaptationDependencies, CultureType


@pytest.fixture
def sample_ukrainian_deps():
    """Фикстура с примером украинских зависимостей."""
    return CulturalAdaptationDependencies(
        api_key="test_key_ukrainian",
        target_culture=CultureType.UKRAINIAN,
        domain_type="therapy",
        project_type="clinical",
        adaptation_depth="deep",
        sensitivity_level="high",
        cultural_validation_required=True,
        religious_accommodation=True,
        trauma_informed=True,
        professional_context=True
    )


@pytest.fixture
def sample_polish_deps():
    """Фикстура с примером польских зависимостей."""
    return CulturalAdaptationDependencies(
        api_key="test_key_polish",
        target_culture=CultureType.POLISH,
        domain_type="therapy",
        project_type="clinical",
        adaptation_depth="deep",
        sensitivity_level="high",
        cultural_validation_required=True,
        religious_accommodation=True,
        professional_context=True
    )


@pytest.fixture
def sample_english_deps():
    """Фикстура с примером английских зависимостей."""
    return CulturalAdaptationDependencies(
        api_key="test_key_english",
        target_culture=CultureType.ENGLISH,
        domain_type="therapy",
        project_type="clinical",
        adaptation_depth="moderate",
        sensitivity_level="high",
        cultural_validation_required=True,
        professional_context=True,
        inclusive_content=True
    )


@pytest.fixture
def sample_education_deps():
    """Фикстура с примером образовательных зависимостей."""
    return CulturalAdaptationDependencies(
        api_key="test_key_education",
        target_culture=CultureType.UNIVERSAL,
        domain_type="education",
        project_type="e_learning",
        adaptation_depth="moderate",
        sensitivity_level="medium",
        cultural_validation_required=True,
        inclusive_content=True,
        academic_context=True,
        age_appropriate=True
    )


@pytest.fixture
def sample_corporate_deps():
    """Фикстура с примером корпоративных зависимостей."""
    return CulturalAdaptationDependencies(
        api_key="test_key_corporate",
        target_culture=CultureType.ENGLISH,
        domain_type="corporate",
        project_type="training",
        adaptation_depth="moderate",
        sensitivity_level="medium",
        cultural_validation_required=True,
        professional_context=True,
        business_appropriate=True,
        performance_focused=True
    )


@pytest.fixture
def mock_context():
    """Фикстура с моком контекста агента."""
    context = Mock()
    context.deps = CulturalAdaptationDependencies(
        api_key="test_key",
        target_culture=CultureType.UKRAINIAN,
        domain_type="therapy"
    )
    return context


@pytest.fixture
def mock_rag_response():
    """Фикстура с моком ответа RAG системы."""
    return {
        "success": True,
        "results": [
            {
                "content": "Украинская культура характеризуется коллективными ценностями...",
                "metadata": {
                    "title": "Украинская психология",
                    "source": "cultural_psychology_knowledge.md"
                }
            },
            {
                "content": "Семейные системы в украинской культуре играют ключевую роль...",
                "metadata": {
                    "title": "Семейная терапия в Украине",
                    "source": "family_therapy_ukraine.md"
                }
            }
        ],
        "reranked": True
    }


@pytest.fixture
def sample_therapy_content():
    """Фикстура с примером терапевтического контента для адаптации."""
    return """
    Когнитивно-поведенческая терапия (КПТ) является эффективным методом
    лечения тревожных расстройств. Основные техники включают:

    1. Идентификация автоматических мыслей
    2. Оценка доказательств за и против
    3. Разработка альтернативных интерпретаций
    4. Поведенческие эксперименты
    5. Техники релаксации

    Важно помнить о необходимости постепенного воздействия
    и формирования новых адаптивных паттернов мышления.
    """


@pytest.fixture
def sample_education_content():
    """Фикстура с примером образовательного контента для адаптации."""
    return """
    Курс "Основы психологии стресса" включает следующие модули:

    1. Теоретические основы стресса
    2. Физиологические механизмы стресс-реакции
    3. Когнитивные аспекты стресса
    4. Копинг-стратегии и их эффективность
    5. Профилактика и управление стрессом

    Каждый модуль содержит интерактивные упражнения
    и практические задания для закрепления материала.
    """


@pytest.fixture
def sample_corporate_content():
    """Фикстура с примером корпоративного контента для адаптации."""
    return """
    Программа "Лидерство в условиях изменений" направлена на развитие:

    1. Навыков адаптивного лидерства
    2. Умения мотивировать команду в кризисных ситуациях
    3. Техник эффективной коммуникации
    4. Стратегий управления сопротивлением изменениям
    5. Методов создания культуры инноваций

    Программа включает кейс-стади, ролевые игры
    и персональные планы развития.
    """


@pytest.fixture(params=[
    CultureType.UKRAINIAN,
    CultureType.POLISH,
    CultureType.ENGLISH,
    CultureType.GERMAN,
    CultureType.UNIVERSAL
])
def all_cultures(request):
    """Параметризованная фикстура для тестирования всех типов культур."""
    return request.param


@pytest.fixture(params=["therapy", "education", "corporate"])
def all_domains(request):
    """Параметризованная фикстура для тестирования всех доменов."""
    return request.param


@pytest.fixture(params=["shallow", "moderate", "deep"])
def all_adaptation_depths(request):
    """Параметризованная фикстура для тестирования всех уровней адаптации."""
    return request.param


@pytest.fixture(params=["low", "medium", "high"])
def all_sensitivity_levels(request):
    """Параметризованная фикстура для тестирования всех уровней чувствительности."""
    return request.param


@pytest.fixture
def async_mock():
    """Фикстура для создания асинхронных моков."""
    return AsyncMock()


# Настройки pytest
def pytest_configure(config):
    """Конфигурация pytest."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Фикстура для очистки после тестов
@pytest.fixture(autouse=True)
def cleanup():
    """Автоматическая очистка после каждого теста."""
    yield
    # Здесь можно добавить код очистки, если необходимо