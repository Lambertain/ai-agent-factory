"""
Тесты для инструментов Pattern VAK Adaptation Specialist Agent.

Проверяет корректность работы всех инструментов VAK адаптации,
включая анализ модальностей, адаптацию контента и валидацию безопасности.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List

from ..tools import (
    analyze_content_vak_modalities,
    adapt_content_to_vak_modality,
    validate_vak_adaptation,
    create_multimodal_variants,
    search_vak_knowledge_base,
    generate_vak_adaptation_report,
    extract_vak_predicates,
    calculate_modality_scores,
    validate_safety_requirements,
    preserve_therapeutic_core
)
from ..dependencies import (
    PatternVAKAdaptationDependencies,
    VAKModalityType,
    AdaptationDepth,
    PatternShiftModuleType
)


class TestAnalyzeContentVAKModalities:
    """Тесты для анализа VAK модальностей в контенте."""

    @pytest.mark.asyncio
    async def test_analyze_basic_content(self, basic_dependencies, sample_content):
        """Проверить базовый анализ VAK модальностей."""
        result = await analyze_content_vak_modalities(
            dependencies=basic_dependencies,
            content=sample_content,
            include_recommendations=True
        )

        # Проверяем структуру результата
        assert "dominant_modality" in result
        assert "modality_scores" in result
        assert "predicates_found" in result
        assert "recommendations" in result

        # Проверяем типы данных
        assert isinstance(result["dominant_modality"], str)
        assert isinstance(result["modality_scores"], dict)
        assert isinstance(result["predicates_found"], dict)
        assert isinstance(result["recommendations"], list)

        # Проверяем наличие всех модальностей в scores
        modality_values = [modality.value for modality in VAKModalityType]
        for modality in modality_values:
            assert modality in result["modality_scores"]
            assert 0 <= result["modality_scores"][modality] <= 1

    @pytest.mark.asyncio
    async def test_analyze_content_without_recommendations(self, basic_dependencies, sample_content):
        """Проверить анализ без рекомендаций."""
        result = await analyze_content_vak_modalities(
            dependencies=basic_dependencies,
            content=sample_content,
            include_recommendations=False
        )

        assert "dominant_modality" in result
        assert "modality_scores" in result
        assert "predicates_found" in result
        assert "recommendations" not in result or len(result["recommendations"]) == 0

    @pytest.mark.asyncio
    async def test_analyze_empty_content(self, basic_dependencies):
        """Проверить анализ пустого контента."""
        empty_content = {"title": "", "content": "", "module_type": PatternShiftModuleType.TECHNIQUE}

        result = await analyze_content_vak_modalities(
            dependencies=basic_dependencies,
            content=empty_content
        )

        # Для пустого контента должны быть равные scores
        scores = result["modality_scores"]
        score_values = list(scores.values())
        assert all(score == score_values[0] for score in score_values), \
            "Для пустого контента все scores должны быть равными"

    @pytest.mark.asyncio
    async def test_analyze_visual_heavy_content(self, basic_dependencies):
        """Проверить анализ контента с визуальной доминантой."""
        visual_content = {
            "title": "Визуализация успеха",
            "content": """
            Представьте яркую картину своего успеха. Посмотрите на детали этой сцены.
            Увидьте цвета, формы, освещение. Сфокусируйте взгляд на ключевых элементах.
            Наблюдайте, как образ становится более четким и ярким.
            """,
            "module_type": PatternShiftModuleType.VISUALIZATION
        }

        result = await analyze_content_vak_modalities(
            dependencies=basic_dependencies,
            content=visual_content
        )

        # Визуальная модальность должна доминировать
        assert result["dominant_modality"] == VAKModalityType.VISUAL.value
        assert result["modality_scores"]["visual"] > 0.4

        # Должны быть найдены визуальные предикаты
        visual_predicates = result["predicates_found"]["visual"]
        assert len(visual_predicates) > 0


class TestAdaptContentToVAKModality:
    """Тесты для адаптации контента под VAK модальности."""

    @pytest.mark.asyncio
    async def test_adapt_to_visual_modality(self, basic_dependencies, sample_content):
        """Проверить адаптацию под визуальную модальность."""
        result = await adapt_content_to_vak_modality(
            dependencies=basic_dependencies,
            content=sample_content,
            target_modality=VAKModalityType.VISUAL,
            preserve_core_message=True
        )

        # Проверяем структуру адаптированного контента
        assert "title" in result
        assert "content" in result
        assert "key_elements" in result
        assert "pace" in result
        assert "structure" in result
        assert "modality" in result

        # Проверяем, что модальность корректная
        assert result["modality"] == VAKModalityType.VISUAL.value

        # Проверяем наличие визуальных элементов
        visual_keywords = ["видеть", "представить", "образ", "картина", "яркий", "цвет"]
        content_lower = result["content"].lower()
        visual_found = any(keyword in content_lower for keyword in visual_keywords)
        assert visual_found, "Адаптированный контент должен содержать визуальные предикаты"

    @pytest.mark.asyncio
    async def test_adapt_to_auditory_modality(self, basic_dependencies, sample_content):
        """Проверить адаптацию под аудиальную модальность."""
        result = await adapt_content_to_vak_modality(
            dependencies=basic_dependencies,
            content=sample_content,
            target_modality=VAKModalityType.AUDITORY,
            preserve_core_message=True
        )

        assert result["modality"] == VAKModalityType.AUDITORY.value

        # Проверяем наличие аудиальных элементов
        auditory_keywords = ["слышать", "звук", "говорить", "голос", "ритм", "тон"]
        content_lower = result["content"].lower()
        auditory_found = any(keyword in content_lower for keyword in auditory_keywords)
        assert auditory_found, "Адаптированный контент должен содержать аудиальные предикаты"

    @pytest.mark.asyncio
    async def test_adapt_to_kinesthetic_modality(self, basic_dependencies, sample_content):
        """Проверить адаптацию под кинестетическую модальность."""
        result = await adapt_content_to_vak_modality(
            dependencies=basic_dependencies,
            content=sample_content,
            target_modality=VAKModalityType.KINESTHETIC,
            preserve_core_message=True
        )

        assert result["modality"] == VAKModalityType.KINESTHETIC.value

        # Проверяем наличие кинестетических элементов
        kinesthetic_keywords = ["чувствовать", "ощущение", "прикосновение", "движение", "тело"]
        content_lower = result["content"].lower()
        kinesthetic_found = any(keyword in content_lower for keyword in kinesthetic_keywords)
        assert kinesthetic_found, "Адаптированный контент должен содержать кинестетические предикаты"

    @pytest.mark.asyncio
    async def test_adapt_with_therapy_context(self, therapy_dependencies, sample_content):
        """Проверить адаптацию в терапевтическом контексте."""
        result = await adapt_content_to_vak_modality(
            dependencies=therapy_dependencies,
            content=sample_content,
            target_modality=VAKModalityType.KINESTHETIC,
            preserve_core_message=True
        )

        # В терапевтическом контексте должны быть элементы безопасности
        content_lower = result["content"].lower()
        safety_indicators = [
            "комфортно", "безопасно", "в своем темпе", "при желании",
            "остановиться", "границы", "выбор"
        ]

        has_safety = any(indicator in content_lower for indicator in safety_indicators)
        assert has_safety, "Терапевтическая адаптация должна содержать элементы безопасности"

    @pytest.mark.asyncio
    async def test_adapt_preserve_core_message(self, basic_dependencies, sample_content):
        """Проверить сохранение ключевого сообщения при адаптации."""
        # Адаптируем для всех модальностей
        visual_result = await adapt_content_to_vak_modality(
            dependencies=basic_dependencies,
            content=sample_content,
            target_modality=VAKModalityType.VISUAL,
            preserve_core_message=True
        )

        auditory_result = await adapt_content_to_vak_modality(
            dependencies=basic_dependencies,
            content=sample_content,
            target_modality=VAKModalityType.AUDITORY,
            preserve_core_message=True
        )

        kinesthetic_result = await adapt_content_to_vak_modality(
            dependencies=basic_dependencies,
            content=sample_content,
            target_modality=VAKModalityType.KINESTHETIC,
            preserve_core_message=True
        )

        # Все адаптации должны сохранять ключевые слова из оригинала
        original_keywords = set(sample_content["content"].lower().split())

        for result in [visual_result, auditory_result, kinesthetic_result]:
            adapted_keywords = set(result["content"].lower().split())
            overlap = len(original_keywords & adapted_keywords)
            overlap_ratio = overlap / len(original_keywords) if original_keywords else 0

            # Должно быть сохранено минимум 30% ключевых слов
            assert overlap_ratio >= 0.3, f"Недостаточное сохранение ключевых слов: {overlap_ratio:.2%}"


class TestValidateVAKAdaptation:
    """Тесты для валидации VAK адаптации."""

    @pytest.mark.asyncio
    async def test_validate_correct_adaptation(self, basic_dependencies, sample_content):
        """Проверить валидацию корректной адаптации."""
        # Сначала создаем адаптацию
        adapted_content = await adapt_content_to_vak_modality(
            dependencies=basic_dependencies,
            content=sample_content,
            target_modality=VAKModalityType.VISUAL,
            preserve_core_message=True
        )

        # Затем валидируем
        validation_result = await validate_vak_adaptation(
            dependencies=basic_dependencies,
            original_content=sample_content,
            adapted_content=adapted_content,
            target_modality=VAKModalityType.VISUAL
        )

        assert validation_result["is_valid"] is True
        assert validation_result["confidence_score"] > 0.6
        assert len(validation_result["validation_errors"]) == 0

    @pytest.mark.asyncio
    async def test_validate_incorrect_adaptation(self, basic_dependencies, sample_content):
        """Проверить валидацию некорректной адаптации."""
        # Создаем некорректную адаптацию (с неподходящими предикатами)
        incorrect_adaptation = {
            "title": "Неправильная адаптация",
            "content": "Просто обычный текст без VAK предикатов",
            "modality": VAKModalityType.VISUAL.value,
            "key_elements": [],
            "pace": "medium",
            "structure": "standard"
        }

        validation_result = await validate_vak_adaptation(
            dependencies=basic_dependencies,
            original_content=sample_content,
            adapted_content=incorrect_adaptation,
            target_modality=VAKModalityType.VISUAL
        )

        assert validation_result["is_valid"] is False
        assert validation_result["confidence_score"] < 0.5
        assert len(validation_result["validation_errors"]) > 0

    @pytest.mark.asyncio
    async def test_validate_safety_compliance(self, therapy_dependencies, sample_content):
        """Проверить валидацию соответствия требованиям безопасности."""
        # Создаем адаптацию с элементами безопасности
        safe_adaptation = {
            "title": "Безопасная техника якорения",
            "content": """
            При желании, медленно и комфортно погрузитесь в воспоминание.
            Если в любой момент станет некомфортно, остановитесь.
            Вы всегда можете выбрать свой темп и границы.
            Ощутите чувство безопасности и поддержки.
            """,
            "modality": VAKModalityType.KINESTHETIC.value,
            "key_elements": ["безопасность", "выбор", "границы"],
            "pace": "медленный",
            "structure": "поддерживающая"
        }

        validation_result = await validate_vak_adaptation(
            dependencies=therapy_dependencies,
            original_content=sample_content,
            adapted_content=safe_adaptation,
            target_modality=VAKModalityType.KINESTHETIC
        )

        assert validation_result["is_valid"] is True
        assert "safety_score" in validation_result
        assert validation_result["safety_score"] > 0.7


class TestCreateMultimodalVariants:
    """Тесты для создания мультимодальных вариантов."""

    @pytest.mark.asyncio
    async def test_create_all_modalities(self, basic_dependencies, sample_content):
        """Проверить создание вариантов для всех модальностей."""
        variants = await create_multimodal_variants(
            dependencies=basic_dependencies,
            content=sample_content,
            include_original=True
        )

        # Проверяем наличие всех модальностей
        expected_modalities = [modality.value for modality in VAKModalityType]
        for modality in expected_modalities:
            assert modality in variants
            assert "title" in variants[modality]
            assert "content" in variants[modality]
            assert "modality" in variants[modality]

        # Если включен оригинал, должен быть ключ "original"
        assert "original" in variants

    @pytest.mark.asyncio
    async def test_create_specific_modalities(self, basic_dependencies, sample_content):
        """Проверить создание вариантов для определенных модальностей."""
        target_modalities = [VAKModalityType.VISUAL, VAKModalityType.KINESTHETIC]

        variants = await create_multimodal_variants(
            dependencies=basic_dependencies,
            content=sample_content,
            target_modalities=target_modalities,
            include_original=False
        )

        # Должны быть только запрошенные модальности
        assert len(variants) == 2
        assert "visual" in variants
        assert "kinesthetic" in variants
        assert "auditory" not in variants
        assert "original" not in variants

    @pytest.mark.asyncio
    async def test_variants_quality(self, basic_dependencies, sample_content):
        """Проверить качество созданных вариантов."""
        variants = await create_multimodal_variants(
            dependencies=basic_dependencies,
            content=sample_content,
            include_validation=True
        )

        # Каждый вариант должен содержать validation_score
        for modality, variant in variants.items():
            if modality != "original":
                assert "validation_score" in variant
                assert variant["validation_score"] > 0.5


class TestSearchVAKKnowledgeBase:
    """Тесты для поиска в базе знаний VAK."""

    @pytest.mark.asyncio
    async def test_search_vak_techniques(self, basic_dependencies):
        """Проверить поиск VAK техник."""
        result = await search_vak_knowledge_base(
            dependencies=basic_dependencies,
            query="якорение визуальная модальность",
            search_type="techniques"
        )

        assert "results" in result
        assert "total_found" in result
        assert isinstance(result["results"], list)
        assert isinstance(result["total_found"], int)

    @pytest.mark.asyncio
    async def test_search_adaptation_examples(self, basic_dependencies):
        """Проверить поиск примеров адаптации."""
        result = await search_vak_knowledge_base(
            dependencies=basic_dependencies,
            query="кинестетическая адаптация медитация",
            search_type="examples"
        )

        assert "results" in result
        assert "total_found" in result

    @pytest.mark.asyncio
    async def test_search_with_modality_filter(self, basic_dependencies):
        """Проверить поиск с фильтром по модальности."""
        result = await search_vak_knowledge_base(
            dependencies=basic_dependencies,
            query="техника расслабления",
            search_type="all",
            modality_filter=VAKModalityType.AUDITORY
        )

        # Результаты должны быть релевантны аудиальной модальности
        assert "results" in result
        if result["results"]:
            # Проверяем, что есть упоминания аудиальных предикатов
            all_text = " ".join([r.get("content", "") for r in result["results"]]).lower()
            auditory_keywords = ["слышать", "звук", "голос", "ритм"]
            has_auditory = any(keyword in all_text for keyword in auditory_keywords)
            assert has_auditory, "Результаты должны содержать аудиальные элементы"


class TestUtilityFunctions:
    """Тесты для вспомогательных функций."""

    def test_extract_vak_predicates(self, sample_content):
        """Проверить извлечение VAK предикатов."""
        predicates = extract_vak_predicates(sample_content["content"])

        assert "visual" in predicates
        assert "auditory" in predicates
        assert "kinesthetic" in predicates

        # Каждая категория должна быть списком
        for modality_predicates in predicates.values():
            assert isinstance(modality_predicates, list)

    def test_calculate_modality_scores(self, sample_content):
        """Проверить расчет scores модальностей."""
        predicates = extract_vak_predicates(sample_content["content"])
        scores = calculate_modality_scores(predicates, sample_content["content"])

        # Проверяем структуру scores
        assert "visual" in scores
        assert "auditory" in scores
        assert "kinesthetic" in scores

        # Все scores должны быть в диапазоне [0, 1]
        for score in scores.values():
            assert 0 <= score <= 1

        # Сумма scores должна быть примерно 1.0 (с погрешностью)
        total_score = sum(scores.values())
        assert 0.9 <= total_score <= 1.1

    @pytest.mark.asyncio
    async def test_validate_safety_requirements(self, therapy_dependencies):
        """Проверить валидацию требований безопасности."""
        safe_content = {
            "content": "Выполняйте упражнение в комфортном темпе, при желании можете остановиться."
        }

        unsafe_content = {
            "content": "Игнорируйте любой дискомфорт и продолжайте упражнение несмотря ни на что."
        }

        safe_result = await validate_safety_requirements(therapy_dependencies, safe_content)
        unsafe_result = await validate_safety_requirements(therapy_dependencies, unsafe_content)

        assert safe_result["is_safe"] is True
        assert safe_result["safety_score"] > 0.7

        assert unsafe_result["is_safe"] is False
        assert unsafe_result["safety_score"] < 0.5
        assert len(unsafe_result["safety_violations"]) > 0

    @pytest.mark.asyncio
    async def test_preserve_therapeutic_core(self, therapy_dependencies, sample_content):
        """Проверить сохранение терапевтической основы."""
        adapted_content = {
            "title": "Адаптированная техника",
            "content": "Модифицированное содержание с сохранением ключевых элементов.",
            "modality": "visual"
        }

        result = await preserve_therapeutic_core(
            dependencies=therapy_dependencies,
            original_content=sample_content,
            adapted_content=adapted_content
        )

        assert "core_preserved" in result
        assert "preservation_score" in result
        assert "missing_elements" in result

        # В терапевтическом контексте preservation_score должен быть высоким
        assert result["preservation_score"] > 0.6


class TestErrorHandling:
    """Тесты для обработки ошибок."""

    @pytest.mark.asyncio
    async def test_analyze_with_invalid_content(self, basic_dependencies):
        """Проверить обработку некорректного контента."""
        invalid_content = "просто строка вместо словаря"

        with pytest.raises((TypeError, ValueError)):
            await analyze_content_vak_modalities(
                dependencies=basic_dependencies,
                content=invalid_content
            )

    @pytest.mark.asyncio
    async def test_adapt_with_missing_fields(self, basic_dependencies):
        """Проверить обработку контента с отсутствующими полями."""
        incomplete_content = {"title": "Только заголовок"}  # нет content

        with pytest.raises((KeyError, ValueError)):
            await adapt_content_to_vak_modality(
                dependencies=basic_dependencies,
                content=incomplete_content,
                target_modality=VAKModalityType.VISUAL
            )

    @pytest.mark.asyncio
    async def test_validate_with_mismatched_types(self, basic_dependencies, sample_content):
        """Проверить валидацию с несоответствующими типами."""
        # Адаптируем для визуальной, но валидируем для аудиальной
        adapted_content = await adapt_content_to_vak_modality(
            dependencies=basic_dependencies,
            content=sample_content,
            target_modality=VAKModalityType.VISUAL
        )

        validation_result = await validate_vak_adaptation(
            dependencies=basic_dependencies,
            original_content=sample_content,
            adapted_content=adapted_content,
            target_modality=VAKModalityType.AUDITORY  # Неправильная модальность
        )

        # Валидация должна выявить несоответствие
        assert validation_result["is_valid"] is False
        assert "modality_mismatch" in validation_result["validation_errors"][0].lower()