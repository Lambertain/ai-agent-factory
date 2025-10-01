"""
Pytest конфигурация для Pattern Scientific Validator Agent.
"""

import pytest
import os
from dataclasses import dataclass


@pytest.fixture
def mock_api_key():
    """Мок API ключа для тестов."""
    return "test-api-key-12345"


@pytest.fixture
def mock_project_path(tmp_path):
    """Временная директория проекта для тестов."""
    return str(tmp_path)


@pytest.fixture
def sample_module_data():
    """Пример данных модуля для тестирования."""
    return {
        "module_id": "test_module_001",
        "module_name": "Cognitive Restructuring Test Module",
        "techniques": ["cognitive_restructuring", "thought_challenging"],
        "content": """
        Модуль когнитивной реструктуризации помогает выявлять и изменять негативные мысли.

        Техника включает:
        1. Идентификация автоматических мыслей
        2. Оценка доказательств за и против
        3. Формирование альтернативных взглядов
        """,
        "target_conditions": ["depression", "anxiety"]
    }


@pytest.fixture
def sample_technique_data():
    """Пример данных техники для валидации."""
    return {
        "technique_name": "Cognitive Restructuring",
        "description": "Техника выявления и изменения дисфункциональных мыслей",
        "target_conditions": ["depression", "anxiety"],
        "original_context": "clinical therapy",
        "adapted_context": "self-help"
    }


@pytest.fixture
def mock_dependencies():
    """Мок зависимостей агента."""
    from ..dependencies import PatternScientificValidatorDependencies

    return PatternScientificValidatorDependencies(
        api_key="test-api-key",
        patternshift_project_path="/tmp/test_project"
    )
