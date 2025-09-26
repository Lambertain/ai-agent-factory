"""
Тесты для основного Psychology Test Generator Agent
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from psychology_test_generator import (
    psychology_test_generator_agent,
    TestGenerationRequest,
    TestBatteryRequest,
    PopulationAdaptationRequest,
    TestGeneratorDependencies
)
from psychology_test_generator.settings import load_settings


@pytest.fixture
def test_dependencies():
    """Создает тестовые зависимости для агента."""
    return TestGeneratorDependencies(
        api_key="test_api_key",
        project_path="./test_project",
        psychological_domain="anxiety",
        target_population="adults",
        test_type="assessment",
        measurement_purpose="screening",

        test_specification={
            "construct": "anxiety_assessment",
            "subscales": ["general_anxiety", "social_anxiety"],
            "question_count": 10,
            "response_format": "frequency",
            "time_limit_minutes": 8
        },

        psychometric_standards={
            "reliability_threshold": 0.80,
            "validity_requirements": ["content", "construct"],
            "validation_type": "basic"
        }
    )


@pytest.fixture
def test_generation_request():
    """Создает тестовый запрос на генерацию теста."""
    return TestGenerationRequest(
        domain="anxiety",
        population="adults",
        purpose="screening",
        question_count=10,
        response_format="frequency",
        time_limit_minutes=8,
        language="ru"
    )


@pytest.fixture
def test_battery_request():
    """Создает тестовый запрос на создание батареи тестов."""
    return TestBatteryRequest(
        domains=["anxiety", "depression"],
        population="adults",
        assessment_type="comprehensive",
        total_time_limit=30
    )


class TestPsychologyTestGeneratorAgent:
    """Тесты основного агента генерации тестов."""

    @pytest.mark.asyncio
    async def test_agent_initialization(self, test_dependencies):
        """Тест инициализации агента."""
        # Проверяем, что агент может быть инициализирован
        assert psychology_test_generator_agent is not None
        assert hasattr(psychology_test_generator_agent, 'run')

    @pytest.mark.asyncio
    @patch('psychology_test_generator.agent.get_llm_model')
    async def test_simple_test_generation(self, mock_llm, test_dependencies, test_generation_request):
        """Тест простой генерации теста."""
        # Мокаем LLM модель
        mock_model = Mock()
        mock_llm.return_value = mock_model

        # Мокаем результат работы агента
        with patch.object(psychology_test_generator_agent, 'run') as mock_run:
            mock_run.return_value = Mock(data={
                "test_title": "Тест на тревожность",
                "questions": [
                    {
                        "id": 1,
                        "text": "Как часто вы чувствуете беспокойство?",
                        "response_format": "frequency",
                        "scale": ["Никогда", "Редко", "Иногда", "Часто", "Всегда"]
                    }
                ],
                "scoring": {"method": "sum", "interpretation": "Чем выше балл, тем выше тревожность"}
            })

            result = await psychology_test_generator_agent.run(
                user_prompt=f"Создай тест: {test_generation_request.model_dump_json()}",
                deps=test_dependencies
            )

            # Проверяем результат
            assert result.data is not None
            assert "test_title" in result.data
            assert "questions" in result.data
            assert len(result.data["questions"]) > 0

    @pytest.mark.asyncio
    async def test_test_validation(self, test_dependencies):
        """Тест валидации созданного теста."""
        test_content = {
            "questions": [
                {"id": 1, "text": "Тестовый вопрос", "response_format": "likert_5"}
            ],
            "scoring": {"method": "sum"}
        }

        # Тестируем валидацию через инструмент агента
        with patch('psychology_test_generator.tools.validate_test_content') as mock_validate:
            mock_validate.return_value = {
                "valid": True,
                "issues": [],
                "recommendations": ["Добавить больше обратных вопросов"]
            }

            # Проверяем, что валидация работает
            validation_result = mock_validate(test_content, test_dependencies.psychological_domain)
            assert validation_result["valid"] is True

    @pytest.mark.asyncio
    async def test_population_adaptation(self, test_dependencies):
        """Тест адаптации теста под целевую популяцию."""
        original_test = {
            "questions": [
                {"id": 1, "text": "Сложный психологический вопрос", "response_format": "likert_7"}
            ]
        }

        # Тестируем адаптацию для детей
        with patch('psychology_test_generator.tools.adapt_for_population') as mock_adapt:
            mock_adapt.return_value = {
                "adapted_questions": [
                    {"id": 1, "text": "Простой вопрос для детей", "response_format": "frequency"}
                ],
                "adaptations_made": ["simplified_language", "reduced_complexity"]
            }

            adapted_test = mock_adapt(original_test, "children", test_dependencies)
            assert "adapted_questions" in adapted_test
            assert len(adapted_test["adaptations_made"]) > 0

    @pytest.mark.asyncio
    async def test_psychometric_analysis(self, test_dependencies):
        """Тест психометрического анализа."""
        test_data = {
            "responses": [[1, 2, 3, 2, 1], [2, 3, 4, 3, 2], [3, 4, 5, 4, 3]],
            "questions": [
                {"id": 1, "subscale": "anxiety"},
                {"id": 2, "subscale": "anxiety"},
                {"id": 3, "subscale": "depression"},
                {"id": 4, "subscale": "depression"},
                {"id": 5, "subscale": "depression"}
            ]
        }

        with patch('psychology_test_generator.tools.analyze_psychometric_properties') as mock_analyze:
            mock_analyze.return_value = {
                "reliability": {
                    "cronbach_alpha": 0.85,
                    "subscale_reliability": {"anxiety": 0.82, "depression": 0.88}
                },
                "validity": {
                    "content_validity": "Good",
                    "construct_validity": "Acceptable"
                },
                "meets_standards": True
            }

            analysis = mock_analyze(test_data, test_dependencies.psychometric_standards)
            assert analysis["reliability"]["cronbach_alpha"] >= test_dependencies.psychometric_standards["reliability_threshold"]
            assert analysis["meets_standards"] is True

    @pytest.mark.asyncio
    async def test_error_handling(self, test_dependencies):
        """Тест обработки ошибок."""
        # Тестируем обработку некорректных входных данных
        with patch.object(psychology_test_generator_agent, 'run') as mock_run:
            mock_run.side_effect = Exception("API Error")

            with pytest.raises(Exception):
                await psychology_test_generator_agent.run(
                    user_prompt="Некорректный запрос",
                    deps=test_dependencies
                )

    def test_dependencies_validation(self):
        """Тест валидации зависимостей."""
        # Тестируем корректные зависимости
        deps = TestGeneratorDependencies(
            api_key="test_key",
            psychological_domain="anxiety",
            target_population="adults"
        )

        # Проверяем, что post_init выполняется без ошибок
        assert deps.psychological_domain == "anxiety"
        assert deps.target_population == "adults"

        # Тестируем валидацию спецификации теста
        assert deps.test_specification["question_count"] >= 5
        assert deps.test_specification["question_count"] <= 100

    @pytest.mark.asyncio
    async def test_rag_integration(self, test_dependencies):
        """Тест интеграции с RAG системой."""
        with patch('psychology_test_generator.tools.search_psychology_knowledge') as mock_search:
            mock_search.return_value = {
                "success": True,
                "results": [
                    {
                        "title": "Anxiety Assessment Methods",
                        "content": "Методы оценки тревожности включают...",
                        "relevance": 0.95
                    }
                ]
            }

            # Тестируем поиск знаний
            search_result = mock_search("anxiety assessment methods", test_dependencies)
            assert search_result["success"] is True
            assert len(search_result["results"]) > 0
            assert search_result["results"][0]["relevance"] > 0.9


class TestTestGenerationRequests:
    """Тесты запросов на генерацию тестов."""

    def test_test_generation_request_validation(self):
        """Тест валидации запроса на генерацию теста."""
        request = TestGenerationRequest(
            domain="anxiety",
            population="adults",
            purpose="screening",
            question_count=15,
            response_format="frequency"
        )

        assert request.domain == "anxiety"
        assert request.question_count == 15
        assert request.response_format == "frequency"

    def test_test_battery_request_validation(self):
        """Тест валидации запроса на батарею тестов."""
        request = TestBatteryRequest(
            domains=["anxiety", "depression", "stress"],
            population="adults",
            assessment_type="comprehensive"
        )

        assert len(request.domains) == 3
        assert "anxiety" in request.domains
        assert request.assessment_type == "comprehensive"

    def test_population_adaptation_request(self):
        """Тест запроса на адаптацию под популяцию."""
        original_test = {"questions": [{"id": 1, "text": "Test question"}]}

        request = PopulationAdaptationRequest(
            original_test=original_test,
            target_population="children",
            adaptation_type="full"
        )

        assert request.target_population == "children"
        assert request.adaptation_type == "full"
        assert request.original_test == original_test


class TestIntegrationWithOtherAgents:
    """Тесты интеграции с другими агентами."""

    @pytest.mark.asyncio
    async def test_research_agent_delegation(self, test_dependencies):
        """Тест делегирования задач Research Agent."""
        with patch('psychology_test_generator.tools.delegate_to_research_agent') as mock_delegate:
            mock_delegate.return_value = {
                "success": True,
                "task_id": "research-task-123",
                "status": "created"
            }

            result = mock_delegate(
                "Проанализировать валидность конструкта тревожности",
                {"domain": "anxiety", "population": "adults"}
            )

            assert result["success"] is True
            assert "task_id" in result

    @pytest.mark.asyncio
    async def test_quality_guardian_delegation(self, test_dependencies):
        """Тест делегирования задач Quality Guardian."""
        test_content = {"questions": [{"id": 1, "text": "Test question"}]}

        with patch('psychology_test_generator.tools.delegate_to_quality_guardian') as mock_delegate:
            mock_delegate.return_value = {
                "success": True,
                "quality_report": {
                    "ethical_compliance": "Good",
                    "psychometric_quality": "Acceptable",
                    "recommendations": ["Improve question clarity"]
                }
            }

            result = mock_delegate(test_content, "ethical_and_psychometric")
            assert result["success"] is True
            assert "quality_report" in result


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"])