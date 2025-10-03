"""
Интеграционные тесты для Pattern VAK Adaptation Specialist Agent.

Проверяет полную интеграцию с PatternShift системой,
взаимодействие компонентов и сценарии реального использования.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List

from ..agent import PatternVAKAdaptationAgent
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
    create_multimodal_variants
)
from ..examples import (
    get_example_for_module_type,
    get_all_available_examples,
    get_recommended_config_for_context,
    create_multi_modal_example_set
)


class TestPatternShiftIntegration:
    """Тесты интеграции с PatternShift системой."""

    @pytest.mark.asyncio
    async def test_pattern_shift_module_adaptation(self, basic_dependencies):
        """Проверить адаптацию для всех типов модулей PatternShift."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        # Тестируем все типы модулей
        module_types = [
            PatternShiftModuleType.TECHNIQUE,
            PatternShiftModuleType.MEDITATION,
            PatternShiftModuleType.VISUALIZATION,
            PatternShiftModuleType.MOVEMENT,
            PatternShiftModuleType.AUDIO_SESSION,
            PatternShiftModuleType.EXERCISE,
            PatternShiftModuleType.ASSESSMENT,
            PatternShiftModuleType.REFLECTION
        ]

        for module_type in module_types:
            # Получаем пример для типа модуля
            example = get_example_for_module_type(
                module_type=module_type,
                modality=VAKModalityType.VISUAL,
                specific_technique="test_technique"
            )

            if "error" not in example:
                # Создаем контент для тестирования
                test_content = {
                    "title": example.get("title", f"Тест {module_type.value}"),
                    "content": example.get("content", "Тестовый контент для адаптации"),
                    "module_type": module_type
                }

                # Адаптируем для всех модальностей
                for modality in VAKModalityType:
                    adapted = await adapt_content_to_vak_modality(
                        dependencies=basic_dependencies,
                        content=test_content,
                        target_modality=modality,
                        preserve_core_message=True
                    )

                    assert adapted["modality"] == modality.value
                    assert len(adapted["content"]) > 0
                    assert len(adapted["key_elements"]) > 0

    @pytest.mark.asyncio
    async def test_therapeutic_context_integration(self, therapy_dependencies):
        """Проверить интеграцию в терапевтическом контексте."""
        agent = PatternVAKAdaptationAgent(dependencies=therapy_dependencies)

        # Получаем рекомендуемую конфигурацию для терапии
        therapy_config = get_recommended_config_for_context(
            context="therapy",
            api_key=therapy_dependencies.api_key
        )

        assert "nlp" in therapy_config
        assert "meditation" in therapy_config
        assert therapy_config["nlp"]["name"] == "НЛП в терапии"

        # Тестируем адаптацию с терапевтическими требованиями
        therapy_content = {
            "title": "Работа с тревогой",
            "content": """
            Сосредоточьтесь на своих ощущениях. Если появляется тревога,
            просто заметьте её без осуждения. Дышите спокойно и глубоко.
            """,
            "module_type": PatternShiftModuleType.TECHNIQUE
        }

        # Адаптируем с учетом травма-информированного подхода
        adapted = await adapt_content_to_vak_modality(
            dependencies=therapy_dependencies,
            content=therapy_content,
            target_modality=VAKModalityType.KINESTHETIC,
            preserve_core_message=True
        )

        # Проверяем наличие элементов безопасности
        content_lower = adapted["content"].lower()
        safety_elements = [
            "в своем темпе", "при желании", "комфортно", "безопасно",
            "остановиться", "границы", "выбор"
        ]

        safety_found = any(element in content_lower for element in safety_elements)
        assert safety_found, "Терапевтическая адаптация должна содержать элементы безопасности"

    @pytest.mark.asyncio
    async def test_coaching_context_integration(self, coaching_dependencies):
        """Проверить интеграцию в коучинговом контексте."""
        agent = PatternVAKAdaptationAgent(dependencies=coaching_dependencies)

        # Получаем рекомендуемую конфигурацию для коучинга
        coaching_config = get_recommended_config_for_context(
            context="coaching",
            api_key=coaching_dependencies.api_key
        )

        assert "nlp" in coaching_config
        assert coaching_config["nlp"]["name"] == "НЛП в коучинге"
        assert coaching_config["recommended_focus"] == "goal_achievement"

        # Тестируем коучинговый контент
        coaching_content = {
            "title": "Достижение целей",
            "content": """
            Определите свою ключевую цель. Визуализируйте её достижение.
            Разработайте пошаговый план действий. Отслеживайте прогресс.
            """,
            "module_type": PatternShiftModuleType.EXERCISE
        }

        adapted = await adapt_content_to_vak_modality(
            dependencies=coaching_dependencies,
            content=coaching_content,
            target_modality=VAKModalityType.AUDITORY,
            preserve_core_message=True
        )

        # Коучинговая адаптация должна содержать элементы мотивации и действий
        content_lower = adapted["content"].lower()
        coaching_elements = [
            "достижение", "цель", "план", "действие", "прогресс",
            "результат", "успех", "развитие"
        ]

        coaching_found = any(element in content_lower for element in coaching_elements)
        assert coaching_found, "Коучинговая адаптация должна содержать мотивационные элементы"


class TestExamplesIntegration:
    """Тесты интеграции с системой примеров."""

    def test_all_available_examples(self):
        """Проверить получение всех доступных примеров."""
        examples = get_all_available_examples()

        # Проверяем структуру
        assert "nlp_techniques" in examples
        assert "meditation_practices" in examples
        assert "visualization_techniques" in examples
        assert "movement_practices" in examples

        # Проверяем, что примеры не пустые
        for category, techniques in examples.items():
            assert isinstance(techniques, list)
            assert len(techniques) > 0

    def test_multi_modal_example_set(self):
        """Проверить создание мультимодального набора примеров."""
        example_set = create_multi_modal_example_set(
            technique_name="anchoring",
            module_type=PatternShiftModuleType.TECHNIQUE
        )

        assert example_set["technique_name"] == "anchoring"
        assert example_set["module_type"] == PatternShiftModuleType.TECHNIQUE.value
        assert "modalities" in example_set

        # Проверяем наличие всех модальностей
        modalities = example_set["modalities"]
        for modality in VAKModalityType:
            assert modality.value in modalities
            modality_example = modalities[modality.value]

            if "error" not in modality_example:
                assert "title" in modality_example
                assert "content" in modality_example

    def test_context_specific_examples(self):
        """Проверить примеры для специфических контекстов."""
        contexts = ["therapy", "coaching", "education", "corporate", "wellness"]

        for context in contexts:
            config = get_recommended_config_for_context(
                context=context,
                api_key="test-api-key"
            )

            if "error" not in config:
                assert "dependencies" in config
                assert config["dependencies"] is not None

                # Проверяем специфичные для контекста поля
                if context == "therapy":
                    assert "nlp" in config
                    assert config["nlp"]["safety_priority"] == "high"
                elif context == "coaching":
                    assert "recommended_focus" in config
                elif context == "corporate":
                    assert "time_constraints" in config


class TestComponentInteraction:
    """Тесты взаимодействия компонентов системы."""

    @pytest.mark.asyncio
    async def test_analysis_to_adaptation_flow(self, basic_dependencies, sample_content):
        """Проверить поток от анализа к адаптации."""
        # 1. Анализируем контент
        analysis = await analyze_content_vak_modalities(
            dependencies=basic_dependencies,
            content=sample_content,
            include_recommendations=True
        )

        dominant_modality = VAKModalityType(analysis["dominant_modality"])

        # 2. Выбираем целевую модальность (отличную от доминантной)
        target_modalities = [m for m in VAKModalityType if m != dominant_modality]
        target_modality = target_modalities[0]

        # 3. Адаптируем под целевую модальность
        adapted = await adapt_content_to_vak_modality(
            dependencies=basic_dependencies,
            content=sample_content,
            target_modality=target_modality,
            preserve_core_message=True
        )

        # 4. Проверяем результат адаптации
        assert adapted["modality"] == target_modality.value

        # 5. Повторно анализируем адаптированный контент
        adapted_content_for_analysis = {
            "title": adapted["title"],
            "content": adapted["content"],
            "module_type": sample_content["module_type"]
        }

        new_analysis = await analyze_content_vak_modalities(
            dependencies=basic_dependencies,
            content=adapted_content_for_analysis
        )

        # Новая доминантная модальность должна быть ближе к целевой
        new_dominant = VAKModalityType(new_analysis["dominant_modality"])
        target_score = new_analysis["modality_scores"][target_modality.value]

        # Целевая модальность должна иметь высокий score
        assert target_score > 0.4, f"Целевая модальность должна иметь высокий score: {target_score}"

    @pytest.mark.asyncio
    async def test_multimodal_variants_consistency(self, basic_dependencies, sample_content):
        """Проверить консистентность мультимодальных вариантов."""
        variants = await create_multimodal_variants(
            dependencies=basic_dependencies,
            content=sample_content,
            include_original=True,
            include_validation=True
        )

        # Все варианты должны сохранять ключевые элементы оригинала
        original_keywords = set(sample_content["content"].lower().split())

        for modality, variant in variants.items():
            if modality != "original":
                variant_keywords = set(variant["content"].lower().split())
                overlap = len(original_keywords & variant_keywords)
                overlap_ratio = overlap / len(original_keywords) if original_keywords else 0

                # Минимальное сохранение ключевых слов
                assert overlap_ratio >= 0.3, \
                    f"Вариант {modality} недостаточно сохраняет оригинал: {overlap_ratio:.2%}"

                # Должна быть корректная модальность
                assert variant["modality"] == modality

                # Валидационный score должен быть приемлемым
                if "validation_score" in variant:
                    assert variant["validation_score"] > 0.5

    @pytest.mark.asyncio
    async def test_batch_processing_efficiency(self, basic_dependencies):
        """Проверить эффективность батчевой обработки."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        # Создаем набор контента для батчевой обработки
        test_contents = []
        target_modalities = []

        for i in range(5):
            content = {
                "title": f"Тестовая техника {i+1}",
                "content": f"Содержание техники номер {i+1} для тестирования батчевой обработки.",
                "module_type": PatternShiftModuleType.TECHNIQUE
            }
            test_contents.append(content)
            target_modalities.append(list(VAKModalityType)[i % 3])

        # Измеряем время батчевой обработки
        import time
        start_time = time.time()

        from ..agent import BatchVAKAdaptationRequest
        batch_request = BatchVAKAdaptationRequest(
            content_list=test_contents,
            target_modalities=target_modalities,
            adaptation_depth=AdaptationDepth.MODERATE
        )

        batch_response = await agent.adapt_content_batch(batch_request)
        batch_time = time.time() - start_time

        # Проверяем успешность батчевой обработки
        assert batch_response.overall_success is True
        assert batch_response.successful_adaptations == 5
        assert batch_response.failed_adaptations == 0

        # Батчевая обработка должна быть относительно быстрой
        assert batch_time < 30.0, f"Батчевая обработка слишком медленная: {batch_time:.2f}s"

        # Измеряем время последовательной обработки для сравнения
        start_time = time.time()

        for i, content in enumerate(test_contents):
            from ..agent import VAKAdaptationRequest
            request = VAKAdaptationRequest(
                content=content,
                target_modality=target_modalities[i]
            )
            await agent.adapt_content(request)

        sequential_time = time.time() - start_time

        # Батчевая обработка не должна быть значительно медленнее последовательной
        efficiency_ratio = batch_time / sequential_time
        assert efficiency_ratio < 1.5, f"Батчевая обработка неэффективна: {efficiency_ratio:.2f}x"


class TestErrorHandlingIntegration:
    """Тесты комплексной обработки ошибок."""

    @pytest.mark.asyncio
    async def test_invalid_content_propagation(self, basic_dependencies):
        """Проверить распространение ошибок при некорректном контенте."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        # Тестируем различные типы некорректного контента
        invalid_contents = [
            {},  # пустой словарь
            {"title": ""},  # только пустой заголовок
            {"content": ""},  # только пустой контент
            {"title": "Test", "content": "Test"},  # без module_type
        ]

        for invalid_content in invalid_contents:
            try:
                from ..agent import VAKAdaptationRequest
                request = VAKAdaptationRequest(
                    content=invalid_content,
                    target_modality=VAKModalityType.VISUAL
                )
                response = await agent.adapt_content(request)

                # Если не произошло исключение, response должен указывать на ошибку
                assert response.success is False
                assert response.error_message is not None

            except (ValueError, KeyError, TypeError):
                # Ожидаемые исключения для некорректного контента
                pass

    @pytest.mark.asyncio
    async def test_partial_batch_failure_handling(self, basic_dependencies):
        """Проверить обработку частичных сбоев в батчевой обработке."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        # Смешиваем корректный и некорректный контент
        mixed_contents = [
            {  # корректный
                "title": "Правильная техника",
                "content": "Это корректный контент для адаптации.",
                "module_type": PatternShiftModuleType.TECHNIQUE
            },
            {  # некорректный - пустой контент
                "title": "",
                "content": "",
                "module_type": PatternShiftModuleType.TECHNIQUE
            },
            {  # корректный
                "title": "Еще одна техника",
                "content": "Другой корректный контент.",
                "module_type": PatternShiftModuleType.MEDITATION
            }
        ]

        target_modalities = [VAKModalityType.VISUAL, VAKModalityType.AUDITORY, VAKModalityType.KINESTHETIC]

        from ..agent import BatchVAKAdaptationRequest
        batch_request = BatchVAKAdaptationRequest(
            content_list=mixed_contents,
            target_modalities=target_modalities
        )

        batch_response = await agent.adapt_content_batch(batch_request)

        # Проверяем корректную обработку смешанного батча
        assert batch_response.successful_adaptations >= 2  # минимум 2 успешных
        assert batch_response.failed_adaptations >= 1  # минимум 1 неудачная
        assert len(batch_response.responses) == 3  # все ответы присутствуют

        # Проверяем, что успешные адаптации корректны
        successful_responses = [r for r in batch_response.responses if r.success]
        for response in successful_responses:
            assert response.adaptation_quality_score > 0.5
            assert len(response.adapted_content["content"]) > 0


class TestPerformanceIntegration:
    """Тесты производительности интегрированной системы."""

    @pytest.mark.asyncio
    async def test_concurrent_adaptations(self, basic_dependencies):
        """Проверить параллельную обработку адаптаций."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        # Создаем несколько задач адаптации
        tasks = []
        for i in range(3):
            content = {
                "title": f"Параллельная техника {i+1}",
                "content": f"Контент для параллельной обработки номер {i+1}.",
                "module_type": PatternShiftModuleType.TECHNIQUE
            }

            from ..agent import VAKAdaptationRequest
            request = VAKAdaptationRequest(
                content=content,
                target_modality=list(VAKModalityType)[i % 3]
            )

            task = agent.adapt_content(request)
            tasks.append(task)

        # Запускаем все задачи параллельно
        import time
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        parallel_time = time.time() - start_time

        # Все адаптации должны быть успешными
        for response in responses:
            assert response.success is True
            assert response.adaptation_quality_score > 0.5

        # Параллельная обработка должна быть быстрее последовательной
        assert parallel_time < 15.0, f"Параллельная обработка слишком медленная: {parallel_time:.2f}s"

    @pytest.mark.asyncio
    async def test_memory_efficiency(self, basic_dependencies):
        """Проверить эффективность использования памяти."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        # Обрабатываем множество адаптаций последовательно
        for i in range(10):
            content = {
                "title": f"Тест памяти {i+1}",
                "content": f"Содержание для тестирования памяти {i+1}. " * 50,  # длинный контент
                "module_type": PatternShiftModuleType.TECHNIQUE
            }

            from ..agent import VAKAdaptationRequest
            request = VAKAdaptationRequest(
                content=content,
                target_modality=VAKModalityType.VISUAL
            )

            response = await agent.adapt_content(request)
            assert response.success is True

            # Проверяем, что нет утечек памяти (примерная проверка)
            # В реальных условиях использовался бы профайлер памяти
            assert len(response.adapted_content["content"]) > 0

    @pytest.mark.asyncio
    async def test_large_content_handling(self, basic_dependencies):
        """Проверить обработку больших объемов контента."""
        agent = PatternVAKAdaptationAgent(dependencies=basic_dependencies)

        # Создаем большой контент
        large_content = {
            "title": "Большая техника трансформации",
            "content": """
            Это очень длинный контент для тестирования обработки больших объемов текста.
            """ * 100,  # повторяем 100 раз
            "module_type": PatternShiftModuleType.TECHNIQUE
        }

        from ..agent import VAKAdaptationRequest
        request = VAKAdaptationRequest(
            content=large_content,
            target_modality=VAKModalityType.KINESTHETIC,
            adaptation_depth=AdaptationDepth.MODERATE
        )

        response = await agent.adapt_content(request)

        # Большой контент должен быть успешно обработан
        assert response.success is True
        assert len(response.adapted_content["content"]) > 1000  # должен остаться большим
        assert response.adaptation_quality_score > 0.4  # качество может быть ниже для больших текстов