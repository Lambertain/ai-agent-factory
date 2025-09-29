"""
Тесты для системы зависимостей Pattern VAK Adaptation Specialist Agent.

Проверяет корректность создания и настройки зависимостей,
типов VAK модальностей и PatternShift интеграции.
"""

import pytest
from dataclasses import fields

from ..dependencies import (
    PatternVAKAdaptationDependencies,
    VAKModalityType,
    AdaptationDepth,
    PatternShiftModuleType,
    create_vak_adaptation_dependencies,
    VISUAL_PREDICATES,
    AUDITORY_PREDICATES,
    KINESTHETIC_PREDICATES
)


class TestVAKModalityType:
    """Тесты для enum VAK модальностей."""

    def test_modality_types_exist(self):
        """Проверить наличие всех типов модальностей."""
        expected_modalities = ["visual", "auditory", "kinesthetic"]
        actual_modalities = [modality.value for modality in VAKModalityType]

        assert len(actual_modalities) == 3
        for modality in expected_modalities:
            assert modality in actual_modalities

    def test_modality_from_string(self):
        """Проверить создание модальности из строки."""
        assert VAKModalityType("visual") == VAKModalityType.VISUAL
        assert VAKModalityType("auditory") == VAKModalityType.AUDITORY
        assert VAKModalityType("kinesthetic") == VAKModalityType.KINESTHETIC

    def test_modality_invalid_string(self):
        """Проверить обработку некорректной строки."""
        with pytest.raises(ValueError):
            VAKModalityType("invalid")


class TestAdaptationDepth:
    """Тесты для enum глубины адаптации."""

    def test_adaptation_depths_exist(self):
        """Проверить наличие всех уровней глубины."""
        expected_depths = ["surface", "moderate", "deep"]
        actual_depths = [depth.value for depth in AdaptationDepth]

        assert len(actual_depths) == 3
        for depth in expected_depths:
            assert depth in actual_depths

    def test_depth_ordering(self):
        """Проверить корректный порядок глубины адаптации."""
        assert AdaptationDepth.SURFACE.value == "surface"
        assert AdaptationDepth.MODERATE.value == "moderate"
        assert AdaptationDepth.DEEP.value == "deep"


class TestPatternShiftModuleType:
    """Тесты для enum типов модулей PatternShift."""

    def test_all_module_types_exist(self):
        """Проверить наличие всех типов модулей."""
        expected_types = [
            "technique", "meditation", "visualization", "movement",
            "audio_session", "exercise", "assessment", "reflection"
        ]
        actual_types = [module_type.value for module_type in PatternShiftModuleType]

        assert len(actual_types) == len(expected_types)
        for module_type in expected_types:
            assert module_type in actual_types

    def test_module_type_from_string(self):
        """Проверить создание типа модуля из строки."""
        assert PatternShiftModuleType("technique") == PatternShiftModuleType.TECHNIQUE
        assert PatternShiftModuleType("meditation") == PatternShiftModuleType.MEDITATION
        assert PatternShiftModuleType("visualization") == PatternShiftModuleType.VISUALIZATION


class TestVAKPredicates:
    """Тесты для констант VAK предикатов."""

    def test_visual_predicates_not_empty(self):
        """Проверить наличие визуальных предикатов."""
        assert len(VISUAL_PREDICATES) > 0
        assert "видеть" in VISUAL_PREDICATES
        assert "представить" in VISUAL_PREDICATES
        assert "показать" in VISUAL_PREDICATES

    def test_auditory_predicates_not_empty(self):
        """Проверить наличие аудиальных предикатов."""
        assert len(AUDITORY_PREDICATES) > 0
        assert "слышать" in AUDITORY_PREDICATES
        assert "говорить" in AUDITORY_PREDICATES
        assert "звучать" in AUDITORY_PREDICATES

    def test_kinesthetic_predicates_not_empty(self):
        """Проверить наличие кинестетических предикатов."""
        assert len(KINESTHETIC_PREDICATES) > 0
        assert "чувствовать" in KINESTHETIC_PREDICATES
        assert "ощущать" in KINESTHETIC_PREDICATES
        assert "прикоснуться" in KINESTHETIC_PREDICATES

    def test_predicates_no_overlap(self):
        """Проверить отсутствие пересечений между предикатами."""
        visual_set = set(VISUAL_PREDICATES)
        auditory_set = set(AUDITORY_PREDICATES)
        kinesthetic_set = set(KINESTHETIC_PREDICATES)

        # Пересечения должны быть минимальными
        visual_auditory_overlap = visual_set & auditory_set
        visual_kinesthetic_overlap = visual_set & kinesthetic_set
        auditory_kinesthetic_overlap = auditory_set & kinesthetic_set

        # Допускаем небольшие пересечения, но не более 10%
        assert len(visual_auditory_overlap) < len(visual_set) * 0.1
        assert len(visual_kinesthetic_overlap) < len(visual_set) * 0.1
        assert len(auditory_kinesthetic_overlap) < len(auditory_set) * 0.1


class TestPatternVAKAdaptationDependencies:
    """Тесты для класса зависимостей VAK адаптации."""

    def test_dependencies_creation(self, test_api_key):
        """Проверить создание зависимостей с базовыми параметрами."""
        deps = PatternVAKAdaptationDependencies(
            api_key=test_api_key,
            pattern_shift_base_path="/test/path"
        )

        assert deps.api_key == test_api_key
        assert deps.pattern_shift_base_path == "/test/path"
        assert deps.adaptation_depth == AdaptationDepth.MODERATE  # по умолчанию
        assert deps.enable_multimodal is True  # по умолчанию
        assert deps.enable_safety_validation is True  # по умолчанию

    def test_dependencies_all_fields(self, test_api_key):
        """Проверить создание зависимостей со всеми параметрами."""
        deps = PatternVAKAdaptationDependencies(
            api_key=test_api_key,
            pattern_shift_base_path="/custom/path",
            adaptation_depth=AdaptationDepth.DEEP,
            enable_multimodal=False,
            enable_safety_validation=True,
            trauma_informed_adaptations=True,
            preserve_therapeutic_integrity=True,
            max_adaptation_time_seconds=60.0,
            batch_adaptation_size=10,
            knowledge_tags=["test", "vak"],
            safety_keywords=["безопасно", "комфортно"],
            therapeutic_frameworks=["cbt", "nlp"]
        )

        assert deps.adaptation_depth == AdaptationDepth.DEEP
        assert deps.enable_multimodal is False
        assert deps.trauma_informed_adaptations is True
        assert deps.preserve_therapeutic_integrity is True
        assert deps.max_adaptation_time_seconds == 60.0
        assert deps.batch_adaptation_size == 10
        assert "test" in deps.knowledge_tags
        assert "vak" in deps.knowledge_tags
        assert "безопасно" in deps.safety_keywords
        assert "cbt" in deps.therapeutic_frameworks

    def test_dependencies_validation(self, test_api_key):
        """Проверить валидацию параметров зависимостей."""
        # Проверяем валидацию max_adaptation_time_seconds
        with pytest.raises(ValueError):
            PatternVAKAdaptationDependencies(
                api_key=test_api_key,
                max_adaptation_time_seconds=-10.0  # отрицательное значение
            )

        # Проверяем валидацию batch_adaptation_size
        with pytest.raises(ValueError):
            PatternVAKAdaptationDependencies(
                api_key=test_api_key,
                batch_adaptation_size=0  # нулевое значение
            )

    def test_dependencies_required_fields(self):
        """Проверить обязательные поля зависимостей."""
        # api_key обязателен
        with pytest.raises(TypeError):
            PatternVAKAdaptationDependencies(
                pattern_shift_base_path="/test/path"
                # api_key отсутствует
            )

    def test_dependencies_defaults(self, test_api_key):
        """Проверить значения по умолчанию."""
        deps = PatternVAKAdaptationDependencies(api_key=test_api_key)

        # Проверяем значения по умолчанию
        assert deps.pattern_shift_base_path == ""
        assert deps.adaptation_depth == AdaptationDepth.MODERATE
        assert deps.enable_multimodal is True
        assert deps.enable_safety_validation is True
        assert deps.trauma_informed_adaptations is False
        assert deps.preserve_therapeutic_integrity is False
        assert deps.max_adaptation_time_seconds == 30.0
        assert deps.batch_adaptation_size == 5
        assert deps.knowledge_tags == []
        assert deps.safety_keywords == []
        assert deps.therapeutic_frameworks == []


class TestCreateVAKAdaptationDependencies:
    """Тесты для функции создания зависимостей."""

    def test_create_basic_dependencies(self, test_api_key):
        """Проверить создание базовых зависимостей."""
        deps = create_vak_adaptation_dependencies(api_key=test_api_key)

        assert isinstance(deps, PatternVAKAdaptationDependencies)
        assert deps.api_key == test_api_key
        assert deps.adaptation_depth == AdaptationDepth.MODERATE

    def test_create_therapy_dependencies(self, test_api_key):
        """Проверить создание зависимостей для терапии."""
        deps = create_vak_adaptation_dependencies(
            api_key=test_api_key,
            adaptation_depth=AdaptationDepth.DEEP,
            trauma_informed_adaptations=True,
            preserve_therapeutic_integrity=True,
            safety_keywords=["безопасно", "комфортно", "границы"],
            therapeutic_frameworks=["trauma-informed", "person-centered"]
        )

        assert deps.adaptation_depth == AdaptationDepth.DEEP
        assert deps.trauma_informed_adaptations is True
        assert deps.preserve_therapeutic_integrity is True
        assert "безопасно" in deps.safety_keywords
        assert "trauma-informed" in deps.therapeutic_frameworks

    def test_create_coaching_dependencies(self, test_api_key):
        """Проверить создание зависимостей для коучинга."""
        deps = create_vak_adaptation_dependencies(
            api_key=test_api_key,
            adaptation_depth=AdaptationDepth.MODERATE,
            enable_multimodal=True,
            batch_adaptation_size=10,
            knowledge_tags=["coaching", "nlp", "goal-setting"]
        )

        assert deps.adaptation_depth == AdaptationDepth.MODERATE
        assert deps.enable_multimodal is True
        assert deps.batch_adaptation_size == 10
        assert "coaching" in deps.knowledge_tags

    def test_create_education_dependencies(self, test_api_key):
        """Проверить создание зависимостей для образования."""
        deps = create_vak_adaptation_dependencies(
            api_key=test_api_key,
            adaptation_depth=AdaptationDepth.SURFACE,
            enable_safety_validation=True,
            max_adaptation_time_seconds=20.0,
            knowledge_tags=["education", "learning-styles", "accessibility"]
        )

        assert deps.adaptation_depth == AdaptationDepth.SURFACE
        assert deps.enable_safety_validation is True
        assert deps.max_adaptation_time_seconds == 20.0
        assert "education" in deps.knowledge_tags

    def test_create_with_custom_path(self, test_api_key):
        """Проверить создание с кастомным путем PatternShift."""
        custom_path = "/custom/pattern/shift/path"
        deps = create_vak_adaptation_dependencies(
            api_key=test_api_key,
            pattern_shift_base_path=custom_path
        )

        assert deps.pattern_shift_base_path == custom_path

    def test_create_with_all_parameters(self, test_api_key):
        """Проверить создание со всеми параметрами."""
        deps = create_vak_adaptation_dependencies(
            api_key=test_api_key,
            pattern_shift_base_path="/full/path",
            adaptation_depth=AdaptationDepth.DEEP,
            enable_multimodal=True,
            enable_safety_validation=True,
            trauma_informed_adaptations=True,
            preserve_therapeutic_integrity=True,
            max_adaptation_time_seconds=45.0,
            batch_adaptation_size=8,
            knowledge_tags=["comprehensive", "testing"],
            safety_keywords=["test-safety"],
            therapeutic_frameworks=["test-framework"]
        )

        # Проверяем все переданные параметры
        assert deps.pattern_shift_base_path == "/full/path"
        assert deps.adaptation_depth == AdaptationDepth.DEEP
        assert deps.enable_multimodal is True
        assert deps.enable_safety_validation is True
        assert deps.trauma_informed_adaptations is True
        assert deps.preserve_therapeutic_integrity is True
        assert deps.max_adaptation_time_seconds == 45.0
        assert deps.batch_adaptation_size == 8
        assert "comprehensive" in deps.knowledge_tags
        assert "test-safety" in deps.safety_keywords
        assert "test-framework" in deps.therapeutic_frameworks


class TestDependenciesIntegration:
    """Интеграционные тесты для зависимостей."""

    def test_dependencies_with_different_contexts(self, test_api_key):
        """Проверить зависимости для разных контекстов использования."""
        contexts = {
            "therapy": {
                "adaptation_depth": AdaptationDepth.DEEP,
                "trauma_informed_adaptations": True,
                "preserve_therapeutic_integrity": True
            },
            "coaching": {
                "adaptation_depth": AdaptationDepth.MODERATE,
                "enable_multimodal": True,
                "batch_adaptation_size": 8
            },
            "education": {
                "adaptation_depth": AdaptationDepth.SURFACE,
                "max_adaptation_time_seconds": 15.0
            }
        }

        for context_name, params in contexts.items():
            deps = create_vak_adaptation_dependencies(
                api_key=test_api_key,
                **params
            )

            assert isinstance(deps, PatternVAKAdaptationDependencies)
            for param_name, param_value in params.items():
                assert getattr(deps, param_name) == param_value

    def test_dependencies_serialization_readiness(self, test_api_key):
        """Проверить готовность зависимостей к сериализации."""
        deps = create_vak_adaptation_dependencies(
            api_key=test_api_key,
            knowledge_tags=["test", "serialization"],
            safety_keywords=["safe", "secure"],
            therapeutic_frameworks=["framework1", "framework2"]
        )

        # Проверяем, что все поля доступны и имеют корректные типы
        assert isinstance(deps.api_key, str)
        assert isinstance(deps.pattern_shift_base_path, str)
        assert isinstance(deps.adaptation_depth, AdaptationDepth)
        assert isinstance(deps.enable_multimodal, bool)
        assert isinstance(deps.enable_safety_validation, bool)
        assert isinstance(deps.trauma_informed_adaptations, bool)
        assert isinstance(deps.preserve_therapeutic_integrity, bool)
        assert isinstance(deps.max_adaptation_time_seconds, float)
        assert isinstance(deps.batch_adaptation_size, int)
        assert isinstance(deps.knowledge_tags, list)
        assert isinstance(deps.safety_keywords, list)
        assert isinstance(deps.therapeutic_frameworks, list)

    def test_dependencies_field_completeness(self, test_api_key):
        """Проверить полноту полей в структуре зависимостей."""
        deps = create_vak_adaptation_dependencies(api_key=test_api_key)

        # Получаем все поля dataclass
        dependency_fields = {field.name for field in fields(PatternVAKAdaptationDependencies)}

        # Проверяем наличие ключевых полей
        expected_fields = {
            'api_key', 'pattern_shift_base_path', 'adaptation_depth',
            'enable_multimodal', 'enable_safety_validation',
            'trauma_informed_adaptations', 'preserve_therapeutic_integrity',
            'max_adaptation_time_seconds', 'batch_adaptation_size',
            'knowledge_tags', 'safety_keywords', 'therapeutic_frameworks'
        }

        assert expected_fields.issubset(dependency_fields), \
            f"Отсутствуют ожидаемые поля: {expected_fields - dependency_fields}"