"""
Тесты для системы примеров Pattern VAK Adaptation Specialist Agent.

Проверяет корректность работы примеров конфигураций,
адаптации техник и интеграции с различными контекстами.
"""

import pytest
from typing import Dict, Any, List

from ..examples import (
    get_example_for_module_type,
    get_all_available_examples,
    get_recommended_config_for_context,
    create_multi_modal_example_set,
    NLP_TECHNIQUES_EXAMPLES,
    MEDITATION_EXAMPLES,
    VISUALIZATION_EXAMPLES,
    MOVEMENT_EXAMPLES,
    NLP_THERAPY_CONFIG,
    NLP_COACHING_CONFIG,
    NLP_EDUCATION_CONFIG,
    MEDITATION_THERAPY_CONFIG,
    MEDITATION_WELLNESS_CONFIG,
    MEDITATION_CORPORATE_CONFIG
)
from ..examples.nlp_techniques_config import (
    get_nlp_adaptation_example,
    create_custom_nlp_config
)
from ..examples.meditation_config import (
    get_meditation_adaptation_example,
    create_meditation_program_config
)
from ..examples.visualization_movement_config import (
    get_visualization_example,
    get_movement_example
)
from ..dependencies import (
    VAKModalityType,
    PatternShiftModuleType,
    AdaptationDepth
)


class TestNLPTechniquesExamples:
    """Тесты для примеров НЛП техник."""

    def test_nlp_techniques_structure(self):
        """Проверить структуру примеров НЛП техник."""
        assert isinstance(NLP_TECHNIQUES_EXAMPLES, dict)
        assert len(NLP_TECHNIQUES_EXAMPLES) > 0

        # Проверяем основные техники
        expected_techniques = ["anchoring", "reframing", "six_step_reframe"]
        for technique in expected_techniques:
            assert technique in NLP_TECHNIQUES_EXAMPLES

    def test_anchoring_examples(self):
        """Проверить примеры техники якорения."""
        anchoring = NLP_TECHNIQUES_EXAMPLES["anchoring"]

        # Должны быть примеры для всех модальностей
        for modality in VAKModalityType:
            assert modality.value in anchoring
            example = anchoring[modality.value]

            assert "title" in example
            assert "content" in example
            assert "key_elements" in example
            assert "pace" in example
            assert "structure" in example

            # Проверяем специфичность для модальности
            content_lower = example["content"].lower()
            if modality == VAKModalityType.VISUAL:
                visual_words = ["представьте", "видеть", "образ", "яркий", "цвет"]
                assert any(word in content_lower for word in visual_words)
            elif modality == VAKModalityType.AUDITORY:
                auditory_words = ["слышать", "звук", "голос", "ритм", "тон"]
                assert any(word in content_lower for word in auditory_words)
            elif modality == VAKModalityType.KINESTHETIC:
                kinesthetic_words = ["чувствовать", "ощущение", "тело", "движение"]
                assert any(word in content_lower for word in kinesthetic_words)

    def test_reframing_examples(self):
        """Проверить примеры техники рефрейминга."""
        reframing = NLP_TECHNIQUES_EXAMPLES["reframing"]

        for modality in VAKModalityType:
            example = reframing[modality.value]

            # Рефрейминг должен содержать элементы изменения перспективы
            content_lower = example["content"].lower()
            reframing_elements = [
                "перспектива", "угол", "взгляд", "изменить", "по-разному",
                "другой", "новый", "иначе"
            ]

            has_reframing = any(element in content_lower for element in reframing_elements)
            assert has_reframing, f"Рефрейминг для {modality.value} должен содержать элементы изменения перспективы"

    def test_get_nlp_adaptation_example(self):
        """Проверить получение примера адаптации НЛП техники."""
        # Тестируем существующую технику
        example = get_nlp_adaptation_example(
            technique="anchoring",
            modality=VAKModalityType.VISUAL,
            include_coaching_notes=True
        )

        assert "title" in example
        assert "content" in example
        assert "coaching_notes" in example
        assert isinstance(example["coaching_notes"], list)
        assert len(example["coaching_notes"]) > 0

        # Тестируем без заметок коуча
        example_no_notes = get_nlp_adaptation_example(
            technique="anchoring",
            modality=VAKModalityType.VISUAL,
            include_coaching_notes=False
        )

        assert "coaching_notes" not in example_no_notes or len(example_no_notes["coaching_notes"]) == 0

    def test_get_nlp_adaptation_nonexistent(self):
        """Проверить обработку несуществующей техники."""
        example = get_nlp_adaptation_example(
            technique="nonexistent_technique",
            modality=VAKModalityType.VISUAL
        )

        assert "error" in example
        assert "не найдена" in example["error"]

    def test_create_custom_nlp_config(self):
        """Проверить создание кастомной НЛП конфигурации."""
        config = create_custom_nlp_config(
            api_key="test-api-key",
            preferred_techniques=["anchoring", "reframing"],
            adaptation_style="visual-focused"
        )

        assert "dependencies" in config
        assert "technique_preferences" in config
        assert "adaptation_weights" in config
        assert "available_examples" in config

        # Проверяем веса для visual-focused стиля
        weights = config["adaptation_weights"]
        assert weights["visual_weight"] > weights["auditory_weight"]
        assert weights["visual_weight"] > weights["kinesthetic_weight"]

    def test_nlp_therapy_config(self):
        """Проверить конфигурацию НЛП для терапии."""
        assert NLP_THERAPY_CONFIG["name"] == "НЛП в терапии"
        assert NLP_THERAPY_CONFIG["adaptation_depth"] == AdaptationDepth.DEEP
        assert NLP_THERAPY_CONFIG["safety_priority"] == "high"
        assert "special_considerations" in NLP_THERAPY_CONFIG
        assert len(NLP_THERAPY_CONFIG["special_considerations"]) > 0


class TestMeditationExamples:
    """Тесты для примеров медитативных практик."""

    def test_meditation_examples_structure(self):
        """Проверить структуру примеров медитации."""
        assert isinstance(MEDITATION_EXAMPLES, dict)
        assert len(MEDITATION_EXAMPLES) > 0

        # Проверяем основные практики
        expected_practices = ["breath_awareness", "body_scan", "loving_kindness"]
        for practice in expected_practices:
            assert practice in MEDITATION_EXAMPLES

    def test_breath_awareness_examples(self):
        """Проверить примеры практики осознанности дыхания."""
        breath_awareness = MEDITATION_EXAMPLES["breath_awareness"]

        for modality in VAKModalityType:
            example = breath_awareness[modality.value]

            assert "title" in example
            assert "content" in example
            assert "duration" in example
            assert "difficulty" in example

            # Все примеры должны содержать элементы дыхания
            content_lower = example["content"].lower()
            breath_elements = ["дыхание", "вдох", "выдох", "воздух"]
            has_breath = any(element in content_lower for element in breath_elements)
            assert has_breath, f"Практика дыхания для {modality.value} должна содержать элементы дыхания"

    def test_get_meditation_adaptation_example(self):
        """Проверить получение примера адаптации медитации."""
        example = get_meditation_adaptation_example(
            practice="breath_awareness",
            modality=VAKModalityType.KINESTHETIC
        )

        assert "title" in example
        assert "content" in example
        assert "duration" in example

        # Кинестетическая адаптация дыхания должна содержать телесные ощущения
        content_lower = example["content"].lower()
        kinesthetic_elements = ["ощущение", "чувствовать", "тело", "грудь", "живот"]
        has_kinesthetic = any(element in content_lower for element in kinesthetic_elements)
        assert has_kinesthetic, "Кинестетическая адаптация должна содержать телесные элементы"

    def test_create_meditation_program_config(self):
        """Проверить создание конфигурации медитативной программы."""
        config = create_meditation_program_config(
            api_key="test-api-key",
            program_type="stress_reduction",
            duration_weeks=8,
            session_length_minutes=20
        )

        assert "dependencies" in config
        assert "program_structure" in config
        assert "weekly_practices" in config
        assert config["program_type"] == "stress_reduction"

    def test_meditation_corporate_config(self):
        """Проверить корпоративную конфигурацию медитации."""
        assert MEDITATION_CORPORATE_CONFIG["recommended_focus"] == "stress_reduction"
        assert MEDITATION_CORPORATE_CONFIG["time_constraints"] == "short_sessions"


class TestVisualizationMovementExamples:
    """Тесты для примеров визуализации и движения."""

    def test_visualization_examples_structure(self):
        """Проверить структуру примеров визуализации."""
        assert isinstance(VISUALIZATION_EXAMPLES, dict)
        assert len(VISUALIZATION_EXAMPLES) > 0

    def test_movement_examples_structure(self):
        """Проверить структуру примеров движения."""
        assert isinstance(MOVEMENT_EXAMPLES, dict)
        assert len(MOVEMENT_EXAMPLES) > 0

    def test_get_visualization_example(self):
        """Проверить получение примера визуализации."""
        example = get_visualization_example(
            technique="safe_place",
            modality=VAKModalityType.VISUAL
        )

        assert "title" in example
        assert "content" in example
        assert "key_elements" in example

        # Визуализация безопасного места должна содержать элементы безопасности
        content_lower = example["content"].lower()
        safety_elements = ["безопасн", "спокойн", "комфорт", "защищен"]
        has_safety = any(element in content_lower for element in safety_elements)
        assert has_safety, "Визуализация безопасного места должна содержать элементы безопасности"

    def test_get_movement_example(self):
        """Проверить получение примера движения."""
        example = get_movement_example(
            practice="grounding",
            modality=VAKModalityType.KINESTHETIC
        )

        assert "title" in example
        assert "content" in example
        assert "instructions" in example

        # Заземляющие практики должны содержать элементы связи с землей/телом
        content_lower = example["content"].lower()
        grounding_elements = ["земля", "стопы", "ноги", "устойчив", "опора", "заземл"]
        has_grounding = any(element in content_lower for element in grounding_elements)
        assert has_grounding, "Заземляющая практика должна содержать элементы заземления"


class TestModuleTypeExamples:
    """Тесты для примеров по типам модулей."""

    def test_get_example_for_all_module_types(self):
        """Проверить получение примеров для всех типов модулей."""
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
            for modality in VAKModalityType:
                example = get_example_for_module_type(
                    module_type=module_type,
                    modality=modality
                )

                # Некоторые модули могут не иметь примеров, но не должно быть критических ошибок
                assert isinstance(example, dict)

                if "error" not in example:
                    assert "title" in example
                    assert "content" in example

    def test_assessment_adaptation(self):
        """Проверить адаптацию оценочных инструментов."""
        for modality in VAKModalityType:
            example = get_example_for_module_type(
                module_type=PatternShiftModuleType.ASSESSMENT,
                modality=modality
            )

            if "error" not in example:
                assert "key_elements" in example
                assert "special_notes" in example
                assert "валидность" in example["special_notes"]

    def test_audio_session_adaptation(self):
        """Проверить адаптацию аудио сессий."""
        example = get_example_for_module_type(
            module_type=PatternShiftModuleType.AUDIO_SESSION,
            modality=VAKModalityType.AUDITORY
        )

        # Аудио сессии должны быть хорошо адаптированы для аудиальной модальности
        if "error" not in example:
            content_lower = example["content"].lower()
            audio_elements = ["слушать", "звук", "голос", "аудио", "слышать"]
            has_audio = any(element in content_lower for element in audio_elements)
            assert has_audio, "Аудио сессия должна содержать аудиальные элементы"


class TestContextualConfigurations:
    """Тесты для контекстуальных конфигураций."""

    def test_get_all_available_examples(self):
        """Проверить получение всех доступных примеров."""
        examples = get_all_available_examples()

        expected_categories = [
            "nlp_techniques", "meditation_practices",
            "visualization_techniques", "movement_practices"
        ]

        for category in expected_categories:
            assert category in examples
            assert isinstance(examples[category], list)
            assert len(examples[category]) > 0

    def test_get_recommended_config_therapy(self):
        """Проверить рекомендуемую конфигурацию для терапии."""
        config = get_recommended_config_for_context(
            context="therapy",
            api_key="test-api-key"
        )

        assert "nlp" in config
        assert "meditation" in config
        assert "visualization" in config
        assert "movement" in config
        assert "dependencies" in config

        # Терапевтические конфигурации должны иметь высокий приоритет безопасности
        nlp_config = config["nlp"]
        assert nlp_config["safety_priority"] == "high"

    def test_get_recommended_config_coaching(self):
        """Проверить рекомендуемую конфигурацию для коучинга."""
        config = get_recommended_config_for_context(
            context="coaching",
            api_key="test-api-key"
        )

        assert "nlp" in config
        assert "meditation" in config
        assert "recommended_focus" in config
        assert config["recommended_focus"] == "goal_achievement"

    def test_get_recommended_config_education(self):
        """Проверить рекомендуемую конфигурацию для образования."""
        config = get_recommended_config_for_context(
            context="education",
            api_key="test-api-key"
        )

        assert "nlp" in config
        assert "meditation" in config
        assert "recommended_focus" in config
        assert config["recommended_focus"] == "learning_enhancement"

    def test_get_recommended_config_corporate(self):
        """Проверить рекомендуемую конфигурацию для корпораций."""
        config = get_recommended_config_for_context(
            context="corporate",
            api_key="test-api-key"
        )

        assert "meditation" in config
        assert "recommended_focus" in config
        assert "time_constraints" in config
        assert config["time_constraints"] == "short_sessions"

    def test_get_recommended_config_wellness(self):
        """Проверить рекомендуемую конфигурацию для велнеса."""
        config = get_recommended_config_for_context(
            context="wellness",
            api_key="test-api-key"
        )

        assert "meditation" in config
        assert "visualization" in config
        assert "recommended_focus" in config
        assert config["recommended_focus"] == "general_wellbeing"

    def test_get_recommended_config_invalid_context(self):
        """Проверить обработку некорректного контекста."""
        config = get_recommended_config_for_context(
            context="invalid_context",
            api_key="test-api-key"
        )

        assert "error" in config
        assert "available_contexts" in config
        assert isinstance(config["available_contexts"], list)


class TestMultiModalExampleSets:
    """Тесты для мультимодальных наборов примеров."""

    def test_create_multi_modal_example_set(self):
        """Проверить создание мультимодального набора примеров."""
        example_set = create_multi_modal_example_set(
            technique_name="anchoring",
            module_type=PatternShiftModuleType.TECHNIQUE
        )

        assert example_set["technique_name"] == "anchoring"
        assert example_set["module_type"] == PatternShiftModuleType.TECHNIQUE.value
        assert "modalities" in example_set

        modalities = example_set["modalities"]

        # Должны быть примеры для всех модальностей
        for modality in VAKModalityType:
            assert modality.value in modalities
            modality_example = modalities[modality.value]

            if "error" not in modality_example:
                assert "title" in modality_example
                assert "content" in modality_example

    def test_multi_modal_consistency(self):
        """Проверить консистентность мультимодальных примеров."""
        example_set = create_multi_modal_example_set(
            technique_name="reframing",
            module_type=PatternShiftModuleType.TECHNIQUE
        )

        modalities = example_set["modalities"]

        # Все модальности должны содержать ключевые элементы рефрейминга
        reframing_keywords = ["ситуация", "перспектива", "взгляд", "изменить"]

        for modality, example in modalities.items():
            if "error" not in example and "content" in example:
                content_lower = example["content"].lower()
                has_reframing = any(keyword in content_lower for keyword in reframing_keywords)
                assert has_reframing, f"Пример для {modality} должен содержать элементы рефрейминга"

    def test_multi_modal_modality_specificity(self):
        """Проверить специфичность примеров для модальностей."""
        example_set = create_multi_modal_example_set(
            technique_name="anchoring",
            module_type=PatternShiftModuleType.TECHNIQUE
        )

        modalities = example_set["modalities"]

        if "visual" in modalities and "error" not in modalities["visual"]:
            visual_content = modalities["visual"]["content"].lower()
            visual_words = ["видеть", "представить", "образ", "яркий"]
            has_visual = any(word in visual_content for word in visual_words)
            assert has_visual, "Визуальный пример должен содержать визуальные предикаты"

        if "auditory" in modalities and "error" not in modalities["auditory"]:
            auditory_content = modalities["auditory"]["content"].lower()
            auditory_words = ["слышать", "звук", "говорить", "голос"]
            has_auditory = any(word in auditory_content for word in auditory_words)
            assert has_auditory, "Аудиальный пример должен содержать аудиальные предикаты"

        if "kinesthetic" in modalities and "error" not in modalities["kinesthetic"]:
            kinesthetic_content = modalities["kinesthetic"]["content"].lower()
            kinesthetic_words = ["чувствовать", "ощущение", "тело", "прикосновение"]
            has_kinesthetic = any(word in kinesthetic_content for word in kinesthetic_words)
            assert has_kinesthetic, "Кинестетический пример должен содержать кинестетические предикаты"


class TestExampleQuality:
    """Тесты качества примеров."""

    def test_nlp_example_completeness(self):
        """Проверить полноту НЛП примеров."""
        for technique_name, technique_examples in NLP_TECHNIQUES_EXAMPLES.items():
            for modality, example in technique_examples.items():
                # Обязательные поля
                required_fields = ["title", "content", "key_elements", "pace", "structure"]
                for field in required_fields:
                    assert field in example, f"Отсутствует поле {field} в {technique_name}.{modality}"

                # Контент не должен быть пустым
                assert len(example["content"].strip()) > 50, \
                    f"Слишком короткий контент в {technique_name}.{modality}"

                # Ключевые элементы должны быть списком
                assert isinstance(example["key_elements"], list), \
                    f"key_elements должны быть списком в {technique_name}.{modality}"
                assert len(example["key_elements"]) > 0, \
                    f"Пустые key_elements в {technique_name}.{modality}"

    def test_meditation_example_completeness(self):
        """Проверить полноту примеров медитации."""
        for practice_name, practice_examples in MEDITATION_EXAMPLES.items():
            for modality, example in practice_examples.items():
                # Обязательные поля для медитации
                required_fields = ["title", "content", "duration", "difficulty"]
                for field in required_fields:
                    assert field in example, f"Отсутствует поле {field} в {practice_name}.{modality}"

                # Продолжительность должна быть разумной
                assert 1 <= example["duration"] <= 120, \
                    f"Неразумная продолжительность в {practice_name}.{modality}"

    def test_example_language_consistency(self):
        """Проверить языковую консистентность примеров."""
        # Все примеры должны быть на русском языке
        import re
        cyrillic_pattern = re.compile('[а-яё]', re.IGNORECASE)

        all_examples = []
        all_examples.extend([(name, ex) for name, technique in NLP_TECHNIQUES_EXAMPLES.items()
                           for modality, ex in technique.items()])
        all_examples.extend([(name, ex) for name, practice in MEDITATION_EXAMPLES.items()
                           for modality, ex in practice.items()])

        for example_name, example in all_examples:
            content = example.get("content", "")
            title = example.get("title", "")

            # Проверяем наличие кириллицы в контенте
            has_cyrillic_content = bool(cyrillic_pattern.search(content))
            has_cyrillic_title = bool(cyrillic_pattern.search(title))

            assert has_cyrillic_content, f"Контент должен быть на русском: {example_name}"
            assert has_cyrillic_title, f"Заголовок должен быть на русском: {example_name}"

    def test_example_safety_compliance(self):
        """Проверить соответствие примеров требованиям безопасности."""
        # Опасные фразы, которых не должно быть в примерах
        dangerous_phrases = [
            "игнорируйте дискомфорт", "подавите", "заставьте себя",
            "против воли", "принуждение", "насилие"
        ]

        all_contents = []
        for technique in NLP_TECHNIQUES_EXAMPLES.values():
            for example in technique.values():
                all_contents.append(example.get("content", ""))

        for practice in MEDITATION_EXAMPLES.values():
            for example in practice.values():
                all_contents.append(example.get("content", ""))

        for content in all_contents:
            content_lower = content.lower()
            for phrase in dangerous_phrases:
                assert phrase not in content_lower, \
                    f"Обнаружена потенциально опасная фраза: {phrase}"

    def test_example_therapeutic_appropriateness(self):
        """Проверить терапевтическую уместность примеров."""
        # Положительные элементы, которые должны присутствовать
        positive_elements = [
            "комфортно", "безопасно", "в своем темпе", "при желании",
            "выбор", "остановиться", "границы", "поддержка"
        ]

        therapy_examples = []

        # Собираем примеры из терапевтических конфигураций
        for technique in NLP_TECHNIQUES_EXAMPLES.values():
            for example in technique.values():
                therapy_examples.append(example.get("content", ""))

        # Проверяем, что хотя бы некоторые примеры содержат элементы безопасности
        examples_with_safety = 0
        for content in therapy_examples:
            content_lower = content.lower()
            has_positive = any(element in content_lower for element in positive_elements)
            if has_positive:
                examples_with_safety += 1

        # Минимум 30% примеров должны содержать элементы безопасности
        safety_ratio = examples_with_safety / len(therapy_examples) if therapy_examples else 0
        assert safety_ratio >= 0.3, \
            f"Недостаточно примеров с элементами безопасности: {safety_ratio:.1%}"