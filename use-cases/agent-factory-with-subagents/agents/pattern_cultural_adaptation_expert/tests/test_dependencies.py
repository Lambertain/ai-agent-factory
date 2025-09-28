"""
Тесты для зависимостей Pattern Cultural Adaptation Expert Agent.
"""

import pytest
import sys
import os

# Добавляем путь к родительской директории для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dependencies import (
    CultureType,
    CulturalAdaptationDependencies,
    create_cultural_adaptation_dependencies
)


class TestCultureType:
    """Тесты для типов культур."""

    def test_culture_type_enum(self):
        """Тест перечисления типов культур."""
        assert CultureType.UKRAINIAN == "ukrainian"
        assert CultureType.POLISH == "polish"
        assert CultureType.ENGLISH == "english"
        assert CultureType.GERMAN == "german"
        assert CultureType.UNIVERSAL == "universal"

    def test_culture_type_values(self):
        """Тест значений типов культур."""
        all_cultures = [
            CultureType.UKRAINIAN,
            CultureType.POLISH,
            CultureType.ENGLISH,
            CultureType.GERMAN,
            CultureType.UNIVERSAL
        ]

        for culture in all_cultures:
            assert isinstance(culture, str)
            assert len(culture) > 0


class TestCulturalAdaptationDependencies:
    """Тесты для зависимостей культурной адаптации."""

    def test_minimal_dependencies(self):
        """Тест минимальных зависимостей."""
        deps = CulturalAdaptationDependencies(api_key="test_key")

        assert deps.api_key == "test_key"
        assert deps.target_culture == CultureType.UNIVERSAL
        assert deps.domain_type == "general"
        assert deps.project_type == "generic"
        assert deps.adaptation_depth == "moderate"
        assert deps.sensitivity_level == "medium"

    def test_full_dependencies(self):
        """Тест полных зависимостей."""
        deps = CulturalAdaptationDependencies(
            api_key="test_key",
            target_culture=CultureType.UKRAINIAN,
            domain_type="therapy",
            project_type="clinical",
            adaptation_depth="deep",
            sensitivity_level="high",
            cultural_validation_required=True,
            religious_accommodation=True,
            trauma_informed=True,
            professional_context=True,
            inclusive_content=True,
            academic_context=False,
            age_appropriate=True,
            business_appropriate=False,
            performance_focused=False
        )

        assert deps.api_key == "test_key"
        assert deps.target_culture == CultureType.UKRAINIAN
        assert deps.domain_type == "therapy"
        assert deps.project_type == "clinical"
        assert deps.adaptation_depth == "deep"
        assert deps.sensitivity_level == "high"
        assert deps.cultural_validation_required is True
        assert deps.religious_accommodation is True
        assert deps.trauma_informed is True
        assert deps.professional_context is True
        assert deps.inclusive_content is True
        assert deps.academic_context is False
        assert deps.age_appropriate is True
        assert deps.business_appropriate is False
        assert deps.performance_focused is False

    def test_therapy_specific_dependencies(self):
        """Тест зависимостей для терапевтического домена."""
        deps = CulturalAdaptationDependencies(
            api_key="test_key",
            target_culture=CultureType.POLISH,
            domain_type="therapy",
            project_type="clinical",
            religious_accommodation=True,
            trauma_informed=True,
            professional_context=True
        )

        assert deps.domain_type == "therapy"
        assert deps.religious_accommodation is True
        assert deps.trauma_informed is True
        assert deps.professional_context is True

    def test_education_specific_dependencies(self):
        """Тест зависимостей для образовательного домена."""
        deps = CulturalAdaptationDependencies(
            api_key="test_key",
            target_culture=CultureType.ENGLISH,
            domain_type="education",
            project_type="e_learning",
            inclusive_content=True,
            academic_context=True,
            age_appropriate=True
        )

        assert deps.domain_type == "education"
        assert deps.inclusive_content is True
        assert deps.academic_context is True
        assert deps.age_appropriate is True

    def test_corporate_specific_dependencies(self):
        """Тест зависимостей для корпоративного домена."""
        deps = CulturalAdaptationDependencies(
            api_key="test_key",
            target_culture=CultureType.GERMAN,
            domain_type="corporate",
            project_type="training",
            professional_context=True,
            business_appropriate=True,
            performance_focused=True
        )

        assert deps.domain_type == "corporate"
        assert deps.professional_context is True
        assert deps.business_appropriate is True
        assert deps.performance_focused is True

    def test_archon_integration_fields(self):
        """Тест полей интеграции с Archon."""
        deps = CulturalAdaptationDependencies(
            api_key="test_key",
            archon_project_id="test_project_id",
            knowledge_tags=["culture", "adaptation", "psychology"],
            knowledge_domain="psychology.example.com"
        )

        assert deps.archon_project_id == "test_project_id"
        assert "culture" in deps.knowledge_tags
        assert "adaptation" in deps.knowledge_tags
        assert "psychology" in deps.knowledge_tags
        assert deps.knowledge_domain == "psychology.example.com"

    def test_dependencies_validation(self):
        """Тест валидации зависимостей."""
        # Тест отсутствия API ключа
        with pytest.raises((ValueError, TypeError)):
            CulturalAdaptationDependencies()

        # Тест корректных значений
        valid_deps = CulturalAdaptationDependencies(
            api_key="valid_key",
            target_culture=CultureType.UKRAINIAN,
            adaptation_depth="deep",
            sensitivity_level="high"
        )

        assert valid_deps.api_key == "valid_key"

    def test_default_values(self):
        """Тест значений по умолчанию."""
        deps = CulturalAdaptationDependencies(api_key="test_key")

        # Проверяем значения по умолчанию
        assert deps.target_culture == CultureType.UNIVERSAL
        assert deps.domain_type == "general"
        assert deps.project_type == "generic"
        assert deps.adaptation_depth == "moderate"
        assert deps.sensitivity_level == "medium"
        assert deps.cultural_validation_required is False
        assert deps.religious_accommodation is False
        assert deps.trauma_informed is False
        assert deps.professional_context is False


class TestCreateCulturalAdaptationDependencies:
    """Тесты для функции создания зависимостей."""

    def test_create_basic_dependencies(self):
        """Тест создания базовых зависимостей."""
        deps = create_cultural_adaptation_dependencies(
            api_key="test_key",
            target_culture=CultureType.UKRAINIAN
        )

        assert isinstance(deps, CulturalAdaptationDependencies)
        assert deps.api_key == "test_key"
        assert deps.target_culture == CultureType.UKRAINIAN

    def test_create_therapy_dependencies(self):
        """Тест создания зависимостей для терапии."""
        deps = create_cultural_adaptation_dependencies(
            api_key="test_key",
            target_culture=CultureType.POLISH,
            domain_type="therapy",
            project_type="clinical",
            adaptation_depth="deep",
            sensitivity_level="high",
            religious_accommodation=True,
            trauma_informed=True
        )

        assert deps.domain_type == "therapy"
        assert deps.project_type == "clinical"
        assert deps.adaptation_depth == "deep"
        assert deps.sensitivity_level == "high"
        assert deps.religious_accommodation is True
        assert deps.trauma_informed is True

    def test_create_education_dependencies(self):
        """Тест создания зависимостей для образования."""
        deps = create_cultural_adaptation_dependencies(
            api_key="test_key",
            target_culture=CultureType.ENGLISH,
            domain_type="education",
            project_type="e_learning",
            inclusive_content=True,
            academic_context=True,
            age_appropriate=True
        )

        assert deps.domain_type == "education"
        assert deps.project_type == "e_learning"
        assert deps.inclusive_content is True
        assert deps.academic_context is True
        assert deps.age_appropriate is True

    def test_create_corporate_dependencies(self):
        """Тест создания зависимостей для корпоративной среды."""
        deps = create_cultural_adaptation_dependencies(
            api_key="test_key",
            target_culture=CultureType.GERMAN,
            domain_type="corporate",
            project_type="training",
            professional_context=True,
            business_appropriate=True,
            performance_focused=True
        )

        assert deps.domain_type == "corporate"
        assert deps.project_type == "training"
        assert deps.professional_context is True
        assert deps.business_appropriate is True
        assert deps.performance_focused is True

    def test_create_with_archon_integration(self):
        """Тест создания зависимостей с интеграцией Archon."""
        deps = create_cultural_adaptation_dependencies(
            api_key="test_key",
            target_culture=CultureType.UKRAINIAN,
            archon_project_id="archon_project_123",
            knowledge_tags=["cultural_adaptation", "psychology"],
            knowledge_domain="psychology.research.org"
        )

        assert deps.archon_project_id == "archon_project_123"
        assert "cultural_adaptation" in deps.knowledge_tags
        assert "psychology" in deps.knowledge_tags
        assert deps.knowledge_domain == "psychology.research.org"