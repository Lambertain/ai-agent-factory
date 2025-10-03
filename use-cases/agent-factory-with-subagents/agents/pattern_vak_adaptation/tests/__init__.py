"""
Тесты для Pattern VAK Adaptation Specialist Agent.

Модуль содержит полный набор тестов для проверки корректности работы
агента VAK адаптации в рамках PatternShift системы.

Структура тестов:
- test_dependencies.py: Тесты системы зависимостей и типов
- test_tools.py: Тесты инструментов VAK адаптации
- test_agent.py: Тесты основного агента
- test_integration.py: Интеграционные тесты с PatternShift
- test_examples.py: Тесты системы примеров и конфигураций
- conftest.py: Общие фикстуры и утилиты для тестирования

Использование:
    # Запуск всех тестов
    pytest tests/

    # Запуск конкретного модуля
    pytest tests/test_agent.py

    # Запуск с покрытием
    pytest tests/ --cov=pattern_vak_adaptation_specialist

    # Запуск только быстрых тестов
    pytest tests/ -m "not slow"
"""

# Импорты для удобства использования в тестах
from .conftest import (
    assert_vak_adaptation_quality,
    assert_safety_compliance,
    assert_therapeutic_integrity,
    create_test_module_types,
    create_test_vak_modalities
)

__all__ = [
    'assert_vak_adaptation_quality',
    'assert_safety_compliance',
    'assert_therapeutic_integrity',
    'create_test_module_types',
    'create_test_vak_modalities'
]