"""
Конфигурация pytest для тестов Psychology Test Generator Agent
"""

import pytest
import asyncio
import os
from unittest.mock import Mock, AsyncMock
from psychology_test_generator import TestGeneratorDependencies
from psychology_test_generator.settings import PsychologyTestGeneratorSettings


@pytest.fixture(scope="session")
def event_loop():
    """Фикстура для асинхронных тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_settings():
    """Создает тестовые настройки."""
    return PsychologyTestGeneratorSettings(
        llm_api_key="test_api_key",
        llm_model="test_model",
        llm_base_url="http://test.api.com",
        default_psychological_domain="general",
        default_target_population="adults",
        archon_project_id="test-project-id",
        enable_rag_search=False,  # Отключаем для тестов
        enable_automatic_validation=False,
        output_directory="./test_output",
        knowledge_directory="./test_knowledge"
    )


@pytest.fixture
def minimal_dependencies():
    """Создает минимальные зависимости для тестирования."""
    return TestGeneratorDependencies(
        api_key="test_api_key",
        psychological_domain="general",
        target_population="adults"
    )


@pytest.fixture
def comprehensive_dependencies():
    """Создает полные зависимости для тестирования."""
    return TestGeneratorDependencies(
        api_key="test_api_key",
        project_path="./test_project",
        psychological_domain="anxiety",
        target_population="adults",
        test_type="assessment",
        measurement_purpose="screening",

        test_specification={
            "construct": "anxiety_assessment",
            "subscales": ["general_anxiety", "social_anxiety", "panic", "worry"],
            "question_count": 21,
            "response_format": "frequency",
            "time_limit_minutes": 10,
            "difficulty_level": "moderate",
            "cultural_adaptation": True
        },

        psychometric_standards={
            "reliability_threshold": 0.85,
            "validity_requirements": ["content", "construct", "criterion"],
            "normative_sample_size": 200,
            "validation_type": "clinical",
            "statistical_power": 0.80,
            "effect_size_detection": 0.3
        },

        population_adaptations={
            "language_level": "grade_8",
            "cultural_considerations": True,
            "accessibility_features": [],
            "administration_format": "digital",
            "support_required": "none"
        }
    )


@pytest.fixture
def sample_test_content():
    """Создает образец содержимого теста для тестирования."""
    return {
        "title": "Тест на тревожность",
        "description": "Опросник для оценки уровня тревожности",
        "instructions": "Пожалуйста, ответьте на следующие вопросы...",
        "questions": [
            {
                "id": 1,
                "text": "Как часто вы чувствуете беспокойство?",
                "subscale": "general_anxiety",
                "response_format": "frequency",
                "scale": ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
                "reverse_scored": False
            },
            {
                "id": 2,
                "text": "Как часто вы чувствуете себя спокойно?",
                "subscale": "general_anxiety",
                "response_format": "frequency",
                "scale": ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
                "reverse_scored": True
            },
            {
                "id": 3,
                "text": "Как часто вы избегаете социальных ситуаций?",
                "subscale": "social_anxiety",
                "response_format": "frequency",
                "scale": ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
                "reverse_scored": False
            }
        ],
        "scoring": {
            "method": "subscale_sum",
            "subscales": {
                "general_anxiety": [1, 2],
                "social_anxiety": [3]
            },
            "interpretation": {
                "low": "0-10: Низкий уровень тревожности",
                "moderate": "11-20: Умеренный уровень тревожности",
                "high": "21-30: Высокий уровень тревожности"
            }
        },
        "metadata": {
            "domain": "anxiety",
            "population": "adults",
            "language": "ru",
            "estimated_time": 10,
            "reliability_estimate": 0.85
        }
    }


@pytest.fixture
def sample_psychometric_data():
    """Создает образец психометрических данных для тестирования."""
    return {
        "responses": [
            [4, 2, 3, 4, 1, 5, 3, 2, 4, 3],  # Респондент 1
            [3, 3, 4, 3, 2, 4, 4, 3, 3, 4],  # Респондент 2
            [5, 1, 5, 5, 1, 5, 5, 1, 5, 5],  # Респондент 3
            [2, 4, 2, 2, 3, 2, 2, 4, 2, 2],  # Респондент 4
            [1, 5, 1, 1, 4, 1, 1, 5, 1, 1],  # Респондент 5
        ],
        "questions": [
            {"id": 1, "subscale": "anxiety", "reverse_scored": False},
            {"id": 2, "subscale": "anxiety", "reverse_scored": True},
            {"id": 3, "subscale": "anxiety", "reverse_scored": False},
            {"id": 4, "subscale": "anxiety", "reverse_scored": False},
            {"id": 5, "subscale": "depression", "reverse_scored": True},
            {"id": 6, "subscale": "depression", "reverse_scored": False},
            {"id": 7, "subscale": "depression", "reverse_scored": False},
            {"id": 8, "subscale": "depression", "reverse_scored": True},
            {"id": 9, "subscale": "stress", "reverse_scored": False},
            {"id": 10, "subscale": "stress", "reverse_scored": False}
        ]
    }


@pytest.fixture
def mock_rag_response():
    """Создает мок ответа от RAG системы."""
    return {
        "success": True,
        "results": [
            {
                "title": "Anxiety Assessment Methods",
                "content": "Методы оценки тревожности включают стандартизированные опросники...",
                "metadata": {
                    "source": "psychology_test_generator_knowledge.md",
                    "relevance": 0.95
                }
            },
            {
                "title": "Psychometric Validation",
                "content": "Психометрическая валидация требует анализа надежности...",
                "metadata": {
                    "source": "psychology_test_generator_knowledge.md",
                    "relevance": 0.88
                }
            }
        ],
        "count": 2
    }


@pytest.fixture
def mock_llm_model():
    """Создает мок LLM модели для тестирования."""
    mock = Mock()
    mock.run = AsyncMock()
    return mock


@pytest.fixture
def mock_archon_response():
    """Создает мок ответа от Archon MCP."""
    return {
        "success": True,
        "task": {
            "id": "test-task-123",
            "title": "Test Task",
            "status": "created",
            "assignee": "Psychology Research Agent"
        }
    }


@pytest.fixture(autouse=True)
def setup_test_environment(tmp_path, monkeypatch):
    """Настраивает тестовое окружение."""
    # Создаем временные директории
    test_output = tmp_path / "output"
    test_knowledge = tmp_path / "knowledge"
    test_templates = tmp_path / "templates"

    test_output.mkdir()
    test_knowledge.mkdir()
    test_templates.mkdir()

    # Устанавливаем переменные окружения для тестов
    monkeypatch.setenv("LLM_API_KEY", "test_api_key")
    monkeypatch.setenv("OUTPUT_DIRECTORY", str(test_output))
    monkeypatch.setenv("KNOWLEDGE_DIRECTORY", str(test_knowledge))
    monkeypatch.setenv("TEMPLATES_DIRECTORY", str(test_templates))

    return {
        "output_dir": test_output,
        "knowledge_dir": test_knowledge,
        "templates_dir": test_templates
    }


# Полезные утилиты для тестов
class TestUtils:
    """Утилиты для тестирования."""

    @staticmethod
    def create_test_question(question_id: int, subscale: str = "general", reverse_scored: bool = False):
        """Создает тестовый вопрос."""
        return {
            "id": question_id,
            "text": f"Тестовый вопрос {question_id}",
            "subscale": subscale,
            "response_format": "frequency",
            "scale": ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
            "reverse_scored": reverse_scored
        }

    @staticmethod
    def create_test_responses(num_respondents: int, num_questions: int):
        """Создает тестовые ответы респондентов."""
        import random
        responses = []
        for _ in range(num_respondents):
            response = [random.randint(1, 5) for _ in range(num_questions)]
            responses.append(response)
        return responses

    @staticmethod
    def validate_test_structure(test_content: dict):
        """Валидирует структуру теста."""
        required_fields = ["title", "questions", "scoring"]
        for field in required_fields:
            assert field in test_content, f"Missing required field: {field}"

        assert len(test_content["questions"]) > 0, "Test must have at least one question"

        for question in test_content["questions"]:
            required_question_fields = ["id", "text", "response_format"]
            for field in required_question_fields:
                assert field in question, f"Missing required question field: {field}"


@pytest.fixture
def test_utils():
    """Предоставляет утилиты для тестирования."""
    return TestUtils


# Маркеры для pytest
pytest_plugins = []

def pytest_configure(config):
    """Конфигурация pytest."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "rag: mark test as requiring RAG system"
    )
    config.addinivalue_line(
        "markers", "llm: mark test as requiring LLM model"
    )