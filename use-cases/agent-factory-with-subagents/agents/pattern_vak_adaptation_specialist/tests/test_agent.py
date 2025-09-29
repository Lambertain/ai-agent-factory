"""
Тесты для основного агента Pattern VAK Adaptation Specialist.

Проверяет корректность работы агента, обработку запросов
и интеграцию с PatternShift системой.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List

from ..agent import (
    PatternVAKAdaptationAgent,
    VAKAdaptationRequest,
    VAKAdaptationResponse,
    BatchVAKAdaptationRequest,
    BatchVAKAdaptationResponse
)
from ..dependencies import (
    PatternVAKAdaptationDependencies,
    VAKModalityType,
    AdaptationDepth,
    PatternShiftModuleType,
    create_vak_adaptation_dependencies
)


class TestVAKAdaptationRequest:
    """Тесты для модели запроса VAK адаптации."""

    def test_basic_request_creation(self, sample_content):
        """Проверить создание базового запроса."""
        request = VAKAdaptationRequest(
            content=sample_content,
            target_modality=VAKModalityType.VISUAL,
            adaptation_depth=AdaptationDepth.MODERATE
        )

        assert request.content == sample_content
        assert request.target_modality == VAKModalityType.VISUAL
        assert request.adaptation_depth == AdaptationDepth.MODERATE
        assert request.preserve_core_message is True  # значение по умолчанию
        assert request.include_safety_validation is True  # значение по умолчанию

    def test_request_with_all_parameters(self, sample_content):
        """Проверить создание запроса со всеми параметрами."""
        request = VAKAdaptationRequest(
            content=sample_content,
            target_modality=VAKModalityType.KINESTHETIC,
            adaptation_depth=AdaptationDepth.DEEP,
            preserve_core_message=False,
            include_safety_validation=True,
            context_metadata={"session_id": "test-123", "user_profile": "therapist"}
        )

        assert request.preserve_core_message is False
        assert request.include_safety_validation is True
        assert request.context_metadata["session_id"] == "test-123"
        assert request.context_metadata["user_profile"] == "therapist"

    def test_request_validation(self):
        """Проверить валидацию запроса."""
        # Пустой контент должен вызывать ошибку
        with pytest.raises(ValueError):
            VAKAdaptationRequest(
                content={},  # пустой контент
                target_modality=VAKModalityType.VISUAL
            )

        # Контент без обязательных полей
        with pytest.raises(ValueError):
            VAKAdaptationRequest(
                content={"title": "Только заголовок"},  # нет content и module_type
                target_modality=VAKModalityType.VISUAL
            )


class TestVAKAdaptationResponse:
    """Тесты для модели ответа VAK адаптации."""

    def test_response_creation(self):
        """Проверить создание ответа."""
        adapted_content = {
            "title": "Адаптированная техника",
            "content": "Визуализированный контент",
            "modality": "visual",
            "key_elements": ["образы", "цвета"],
            "pace": "быстрый"
        }

        response = VAKAdaptationResponse(
            adapted_content=adapted_content,
            original_modality=VAKModalityType.KINESTHETIC,
            target_modality=VAKModalityType.VISUAL,
            adaptation_quality_score=0.85,
            adaptation_metadata={"processing_time": 2.5}
        )

        assert response.adapted_content == adapted_content
        assert response.original_modality == VAKModalityType.KINESTHETIC
        assert response.target_modality == VAKModalityType.VISUAL
        assert response.adaptation_quality_score == 0.85
        assert response.success is True  # по умолчанию
        assert response.adaptation_metadata["processing_time"] == 2.5

    def test_response_with_errors(self):
        """Проверить создание ответа с ошибками."""
        response = VAKAdaptationResponse(
            adapted_content={},
            target_modality=VAKModalityType.VISUAL,
            adaptation_quality_score=0.3,
            success=False,
            error_message="Низкое качество адаптации",
            validation_errors=["Отсутствуют визуальные предикаты"]
        )

        assert response.success is False
        assert response.error_message == "Низкое качество адаптации"
        assert len(response.validation_errors) == 1
        assert "визуальные предикаты" in response.validation_errors[0]


class TestBatchVAKAdaptationRequest:
    """Тесты для модели батчевого запроса."""

    def test_batch_request_creation(self, sample_content, sample_meditation_content):
        """Проверить создание батчевого запроса."""
        content_list = [sample_content, sample_meditation_content]
        target_modalities = [VAKModalityType.VISUAL, VAKModalityType.AUDITORY]

        batch_request = BatchVAKAdaptationRequest(
            content_list=content_list,
            target_modalities=target_modalities,
            adaptation_depth=AdaptationDepth.MODERATE
        )

        assert len(batch_request.content_list) == 2
        assert len(batch_request.target_modalities) == 2
        assert batch_request.adaptation_depth == AdaptationDepth.MODERATE

    def test_batch_request_validation(self, sample_content):
        """Проверить валидацию батчевого запроса."""
        # Пустой список контента
        with pytest.raises(ValueError):
            BatchVAKAdaptationRequest(
                content_list=[],
                target_modalities=[VAKModalityType.VISUAL]
            )

        # Несоответствие количества контента и модальностей
        with pytest.raises(ValueError):
            BatchVAKAdaptationRequest(
                content_list=[sample_content],
                target_modalities=[VAKModalityType.VISUAL, VAKModalityType.AUDITORY]  # больше модальностей
            )


class TestPatternVAKAdaptationAgent:
    """Тесты для основного агента VAK адаптации."""

    @pytest.fixture
    def agent(self, basic_dependencies):
        """Создать экземпляр агента для тестирования."""
        return PatternVAKAdaptationAgent(dependencies=basic_dependencies)

    @pytest.mark.asyncio
    async def test_agent_initialization(self, basic_dependencies):
        """Проверить инициализацию агента."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        assert agent.dependencies == basic_dependencies
        assert hasattr(agent, 'agent')  # Pydantic AI agent
        assert hasattr(agent, 'adapt_content')
        assert hasattr(agent, 'analyze_content')
        assert hasattr(agent, 'create_multimodal_variants')

    @pytest.mark.asyncio
    async def test_adapt_content_single(self, agent, sample_content):
        """Проверить адаптацию одного контента."""
        request = VAKAdaptationRequest(
            content=sample_content,
            target_modality=VAKModalityType.VISUAL,
            adaptation_depth=AdaptationDepth.MODERATE
        )

        response = await agent.adapt_content(request)

        assert isinstance(response, VAKAdaptationResponse)
        assert response.success is True
        assert response.target_modality == VAKModalityType.VISUAL
        assert response.adaptation_quality_score > 0.5
        assert "title" in response.adapted_content
        assert "content" in response.adapted_content
        assert response.adapted_content["modality"] == "visual"

    @pytest.mark.asyncio
    async def test_adapt_content_with_safety_validation(self, agent, sample_content):
        """Проверить адаптацию с валидацией безопасности."""
        # Используем therapy context dependencies для более строгой валидации
        therapy_deps = create_vak_adaptation_dependencies(
            api_key="test-key",
            adaptation_depth=AdaptationDepth.DEEP,
            trauma_informed_adaptations=True,
            preserve_therapeutic_integrity=True
        )
        therapy_agent = PatternVAKAdaptationAgent(dependencies=therapy_deps)

        request = VAKAdaptationRequest(
            content=sample_content,
            target_modality=VAKModalityType.KINESTHETIC,
            include_safety_validation=True
        )

        response = await therapy_agent.adapt_content(request)

        assert response.success is True
        # Должны быть метаданные о безопасности
        assert "safety_score" in response.adaptation_metadata
        assert response.adaptation_metadata["safety_score"] > 0.6

    @pytest.mark.asyncio
    async def test_analyze_content_modalities(self, agent, sample_content):
        """Проверить анализ модальностей контента."""
        analysis = await agent.analyze_content(
            content=sample_content,
            include_recommendations=True
        )

        assert "dominant_modality" in analysis
        assert "modality_scores" in analysis
        assert "predicates_found" in analysis
        assert "recommendations" in analysis

        # Проверяем валидность scores
        scores = analysis["modality_scores"]
        for modality in VAKModalityType:
            assert modality.value in scores
            assert 0 <= scores[modality.value] <= 1

    @pytest.mark.asyncio
    async def test_create_multimodal_variants(self, agent, sample_content):
        """Проверить создание мультимодальных вариантов."""
        variants = await agent.create_multimodal_variants(
            content=sample_content,
            include_original=True,
            include_validation=True
        )

        # Должны быть варианты для всех модальностей + оригинал
        expected_keys = ["visual", "auditory", "kinesthetic", "original"]
        for key in expected_keys:
            assert key in variants

        # Каждый вариант должен иметь корректную структуру
        for modality in ["visual", "auditory", "kinesthetic"]:
            variant = variants[modality]
            assert "title" in variant
            assert "content" in variant
            assert "modality" in variant
            assert variant["modality"] == modality

            # При включенной валидации должен быть validation_score
            assert "validation_score" in variant
            assert variant["validation_score"] > 0.5

    @pytest.mark.asyncio
    async def test_batch_adaptation(self, agent, sample_content, sample_meditation_content):
        """Проверить батчевую адаптацию."""
        batch_request = BatchVAKAdaptationRequest(
            content_list=[sample_content, sample_meditation_content],
            target_modalities=[VAKModalityType.VISUAL, VAKModalityType.AUDITORY],
            adaptation_depth=AdaptationDepth.MODERATE
        )

        batch_response = await agent.adapt_content_batch(batch_request)

        assert isinstance(batch_response, BatchVAKAdaptationResponse)
        assert batch_response.overall_success is True
        assert len(batch_response.responses) == 2
        assert batch_response.successful_adaptations == 2
        assert batch_response.failed_adaptations == 0

        # Проверяем каждый ответ в батче
        for i, response in enumerate(batch_response.responses):
            assert isinstance(response, VAKAdaptationResponse)
            assert response.success is True
            expected_modality = batch_request.target_modalities[i]
            assert response.target_modality == expected_modality

    @pytest.mark.asyncio
    async def test_agent_with_nlp_content(self, agent, sample_nlp_content):
        """Проверить работу агента с НЛП контентом."""
        request = VAKAdaptationRequest(
            content=sample_nlp_content,
            target_modality=VAKModalityType.AUDITORY,
            adaptation_depth=AdaptationDepth.DEEP
        )

        response = await agent.adapt_content(request)

        assert response.success is True
        assert response.target_modality == VAKModalityType.AUDITORY

        # НЛП контент должен быть адаптирован с сохранением техники
        adapted_content = response.adapted_content
        assert "рефрейминг" in adapted_content["title"].lower() or \
               "рефрейминг" in adapted_content["content"].lower()

        # Должны присутствовать аудиальные элементы
        content_lower = adapted_content["content"].lower()
        auditory_keywords = ["слышать", "звук", "говорить", "голос", "диалог"]
        has_auditory = any(keyword in content_lower for keyword in auditory_keywords)
        assert has_auditory, "НЛП адаптация должна содержать аудиальные предикаты"

    @pytest.mark.asyncio
    async def test_agent_error_handling(self, agent):
        """Проверить обработку ошибок агентом."""
        # Некорректный запрос
        invalid_request = VAKAdaptationRequest(
            content={"title": "", "content": ""},  # пустой контент
            target_modality=VAKModalityType.VISUAL
        )

        response = await agent.adapt_content(invalid_request)

        assert response.success is False
        assert response.error_message is not None
        assert len(response.error_message) > 0

    @pytest.mark.asyncio
    async def test_agent_performance_tracking(self, agent, sample_content):
        """Проверить отслеживание производительности агента."""
        request = VAKAdaptationRequest(
            content=sample_content,
            target_modality=VAKModalityType.KINESTHETIC
        )

        response = await agent.adapt_content(request)

        # Метаданные должны содержать информацию о производительности
        assert "processing_time" in response.adaptation_metadata
        assert response.adaptation_metadata["processing_time"] > 0

        # Может содержать другие метрики
        possible_metrics = [
            "token_count", "analysis_time", "adaptation_time",
            "validation_time", "predicates_count"
        ]

        # Хотя бы одна дополнительная метрика должна присутствовать
        has_additional_metrics = any(
            metric in response.adaptation_metadata
            for metric in possible_metrics
        )
        assert has_additional_metrics, "Должны быть дополнительные метрики производительности"

    @pytest.mark.asyncio
    async def test_agent_context_preservation(self, agent, sample_content):
        """Проверить сохранение контекста при адаптации."""
        # Добавляем контекстные метаданные
        request = VAKAdaptationRequest(
            content=sample_content,
            target_modality=VAKModalityType.VISUAL,
            context_metadata={
                "session_id": "test-session-123",
                "user_preference": "detailed_instructions",
                "therapeutic_context": "anxiety_management"
            }
        )

        response = await agent.adapt_content(request)

        # Контекст должен влиять на адаптацию
        assert response.success is True

        # Метаданные контекста должны быть сохранены или использованы
        if "context_used" in response.adaptation_metadata:
            context_used = response.adaptation_metadata["context_used"]
            assert "session_id" in context_used or "therapeutic_context" in context_used


class TestAgentIntegration:
    """Интеграционные тесты агента."""

    @pytest.mark.asyncio
    async def test_full_adaptation_workflow(self, basic_dependencies, sample_content):
        """Проверить полный рабочий процесс адаптации."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        # 1. Анализируем оригинальный контент
        analysis = await agent.analyze_content(sample_content)
        original_modality = analysis["dominant_modality"]

        # 2. Создаем адаптацию для противоположной модальности
        target_modality = VAKModalityType.VISUAL if original_modality != "visual" else VAKModalityType.AUDITORY

        request = VAKAdaptationRequest(
            content=sample_content,
            target_modality=target_modality,
            preserve_core_message=True
        )

        response = await agent.adapt_content(request)

        # 3. Проверяем качество адаптации
        assert response.success is True
        assert response.target_modality == target_modality
        assert response.adaptation_quality_score > 0.6

        # 4. Создаем мультимодальные варианты
        variants = await agent.create_multimodal_variants(
            content=sample_content,
            include_validation=True
        )

        # Все варианты должны иметь высокое качество
        for modality, variant in variants.items():
            if modality != "original":
                assert variant["validation_score"] > 0.5

    @pytest.mark.asyncio
    async def test_therapy_context_workflow(self, therapy_dependencies, sample_content):
        """Проверить рабочий процесс в терапевтическом контексте."""
        agent = PatternVAKAdaptationAgent(dependencies=therapy_dependencies)

        # Адаптация с максимальными требованиями безопасности
        request = VAKAdaptationRequest(
            content=sample_content,
            target_modality=VAKModalityType.KINESTHETIC,
            adaptation_depth=AdaptationDepth.DEEP,
            include_safety_validation=True,
            preserve_core_message=True
        )

        response = await agent.adapt_content(request)

        assert response.success is True
        assert "safety_score" in response.adaptation_metadata
        assert response.adaptation_metadata["safety_score"] > 0.7

        # Адаптированный контент должен содержать элементы безопасности
        content_lower = response.adapted_content["content"].lower()
        safety_indicators = [
            "комфортно", "безопасно", "в своем темпе", "границы", "выбор"
        ]
        has_safety = any(indicator in content_lower for indicator in safety_indicators)
        assert has_safety, "Терапевтическая адаптация должна содержать элементы безопасности"

    @pytest.mark.asyncio
    async def test_pattern_shift_module_types(self, basic_dependencies):
        """Проверить работу с разными типами модулей PatternShift."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        module_contents = {
            PatternShiftModuleType.TECHNIQUE: {
                "title": "Техника якорения",
                "content": "НЛП техника для создания положительных состояний",
                "module_type": PatternShiftModuleType.TECHNIQUE
            },
            PatternShiftModuleType.MEDITATION: {
                "title": "Медитация осознанности",
                "content": "Практика внимательного наблюдения за дыханием",
                "module_type": PatternShiftModuleType.MEDITATION
            },
            PatternShiftModuleType.VISUALIZATION: {
                "title": "Визуализация цели",
                "content": "Мысленное представление достижения цели",
                "module_type": PatternShiftModuleType.VISUALIZATION
            }
        }

        for module_type, content in module_contents.items():
            request = VAKAdaptationRequest(
                content=content,
                target_modality=VAKModalityType.KINESTHETIC
            )

            response = await agent.adapt_content(request)

            assert response.success is True, f"Ошибка адаптации для {module_type}"
            assert response.target_modality == VAKModalityType.KINESTHETIC

            # Адаптация должна учитывать тип модуля
            adapted_content = response.adapted_content["content"].lower()

            if module_type == PatternShiftModuleType.MEDITATION:
                # Медитации должны содержать кинестетические элементы дыхания и тела
                kinesthetic_elements = ["дыхание", "тело", "ощущения", "чувствовать"]
                has_elements = any(element in adapted_content for element in kinesthetic_elements)
                assert has_elements, "Медитативная адаптация должна содержать телесные элементы"

    @pytest.mark.asyncio
    async def test_agent_consistency(self, basic_dependencies, sample_content):
        """Проверить консистентность результатов агента."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        # Выполняем одинаковую адаптацию несколько раз
        request = VAKAdaptationRequest(
            content=sample_content,
            target_modality=VAKModalityType.VISUAL,
            adaptation_depth=AdaptationDepth.MODERATE
        )

        responses = []
        for _ in range(3):
            response = await agent.adapt_content(request)
            responses.append(response)

        # Все ответы должны быть успешными
        for response in responses:
            assert response.success is True
            assert response.target_modality == VAKModalityType.VISUAL

        # Качество адаптации должно быть стабильным (разброс < 0.2)
        quality_scores = [r.adaptation_quality_score for r in responses]
        score_range = max(quality_scores) - min(quality_scores)
        assert score_range < 0.2, f"Слишком большой разброс в качестве: {score_range}"