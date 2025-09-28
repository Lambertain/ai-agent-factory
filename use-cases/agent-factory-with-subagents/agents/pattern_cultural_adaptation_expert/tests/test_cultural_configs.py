"""
Тесты для конфигураций культурных доменов.
"""

import pytest
import sys
import os

# Добавляем путь к родительской директории для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.therapy_config import (
    create_therapy_config,
    THERAPY_UKRAINIAN_CONFIG,
    THERAPY_POLISH_CONFIG,
    THERAPY_ENGLISH_CONFIG,
    get_therapy_examples
)
from examples.education_config import (
    create_education_config,
    EDUCATION_UKRAINIAN_CONFIG,
    EDUCATION_POLISH_CONFIG,
    EDUCATION_ENGLISH_CONFIG,
    get_education_examples
)
from examples.corporate_config import (
    create_corporate_config,
    CORPORATE_UKRAINIAN_CONFIG,
    CORPORATE_POLISH_CONFIG,
    CORPORATE_ENGLISH_CONFIG,
    get_corporate_examples
)
from dependencies import CultureType


class TestTherapyConfigurations:
    """Тесты для конфигураций терапевтического домена."""

    def test_therapy_config_creation(self):
        """Тест создания конфигурации терапии."""
        config = create_therapy_config("test_key", "ukrainian")

        assert hasattr(config, 'api_key')
        assert hasattr(config, 'target_culture')
        assert hasattr(config, 'domain_type')

    def test_therapy_ukrainian_config(self):
        """Тест украинской конфигурации терапии."""
        config = THERAPY_UKRAINIAN_CONFIG

        assert config["target_culture"] == CultureType.UKRAINIAN
        assert config["domain_type"] == "therapy"
        assert config["project_type"] == "clinical"
        assert config["adaptation_depth"] == "deep"
        assert config["sensitivity_level"] == "high"
        assert "family_systems" in config["cultural_focus"]
        assert "collective_trauma" in config["cultural_focus"]
        assert config["communication_style"] == "high_context"
        assert config["religious_accommodation"] is True
        assert config["trauma_informed"] is True

    def test_therapy_polish_config(self):
        """Тест польской конфигурации терапии."""
        config = THERAPY_POLISH_CONFIG

        assert config["target_culture"] == CultureType.POLISH
        assert config["domain_type"] == "therapy"
        assert config["adaptation_depth"] == "deep"
        assert "catholic_values" in config["cultural_focus"]
        assert "family_tradition" in config["cultural_focus"]
        assert config["communication_style"] == "formal_respectful"
        assert config["religious_accommodation"] is True

    def test_therapy_english_config(self):
        """Тест английской конфигурации терапии."""
        config = THERAPY_ENGLISH_CONFIG

        assert config["target_culture"] == CultureType.ENGLISH
        assert config["domain_type"] == "therapy"
        assert config["adaptation_depth"] == "moderate"
        assert "individual_autonomy" in config["cultural_focus"]
        assert "evidence_based" in config["cultural_focus"]
        assert config["communication_style"] == "direct_professional"
        assert config["secular_approach"] is True

    def test_therapy_examples(self):
        """Тест примеров терапевтических техник."""
        examples = get_therapy_examples()

        assert "anxiety_treatment" in examples
        assert "trauma_therapy" in examples
        assert "family_therapy" in examples

        # Проверяем наличие переводов для всех культур
        for technique in examples.values():
            assert "ukrainian" in technique
            assert "polish" in technique
            assert "english" in technique


class TestEducationConfigurations:
    """Тесты для конфигураций образовательного домена."""

    def test_education_config_creation(self):
        """Тест создания образовательной конфигурации."""
        config = create_education_config("test_key", "universal")

        assert hasattr(config, 'api_key')
        assert hasattr(config, 'target_culture')
        assert hasattr(config, 'domain_type')

    def test_education_ukrainian_config(self):
        """Тест украинской образовательной конфигурации."""
        config = EDUCATION_UKRAINIAN_CONFIG

        assert config["target_culture"] == CultureType.UKRAINIAN
        assert config["domain_type"] == "education"
        assert config["project_type"] == "e_learning"
        assert "practical_application" in config["cultural_focus"]
        assert "community_learning" in config["cultural_focus"]
        assert config["communication_style"] == "engaging_storytelling"
        assert config["learning_style"] == "visual_narrative"
        assert config["cultural_examples"] is True

    def test_education_polish_config(self):
        """Тест польской образовательной конфигурации."""
        config = EDUCATION_POLISH_CONFIG

        assert config["target_culture"] == CultureType.POLISH
        assert "structured_learning" in config["cultural_focus"]
        assert "traditional_values" in config["cultural_focus"]
        assert config["communication_style"] == "formal_academic"
        assert config["learning_style"] == "systematic_approach"
        assert config["ethical_framework"] is True

    def test_education_english_config(self):
        """Тест английской образовательной конфигурации."""
        config = EDUCATION_ENGLISH_CONFIG

        assert config["target_culture"] == CultureType.ENGLISH
        assert "evidence_based" in config["cultural_focus"]
        assert "critical_thinking" in config["cultural_focus"]
        assert config["communication_style"] == "interactive_engaging"
        assert config["learning_style"] == "self_directed"
        assert config["research_based"] is True

    def test_education_examples(self):
        """Тест примеров образовательных программ."""
        examples = get_education_examples()

        assert "psychology_course" in examples
        assert "stress_management" in examples
        assert "emotional_intelligence" in examples

        # Проверяем культурную адаптацию
        for program in examples.values():
            assert "ukrainian" in program
            assert "polish" in program
            assert "english" in program


class TestCorporateConfigurations:
    """Тесты для конфигураций корпоративного домена."""

    def test_corporate_config_creation(self):
        """Тест создания корпоративной конфигурации."""
        config = create_corporate_config("test_key", "english")

        assert hasattr(config, 'api_key')
        assert hasattr(config, 'target_culture')
        assert hasattr(config, 'domain_type')

    def test_corporate_ukrainian_config(self):
        """Тест украинской корпоративной конфигурации."""
        config = CORPORATE_UKRAINIAN_CONFIG

        assert config["target_culture"] == CultureType.UKRAINIAN
        assert config["domain_type"] == "corporate"
        assert config["project_type"] == "training"
        assert "team_solidarity" in config["cultural_focus"]
        assert "adaptability" in config["cultural_focus"]
        assert config["communication_style"] == "collaborative_warm"
        assert config["leadership_style"] == "supportive_democratic"
        assert config["crisis_resilience"] is True

    def test_corporate_polish_config(self):
        """Тест польской корпоративной конфигурации."""
        config = CORPORATE_POLISH_CONFIG

        assert config["target_culture"] == CultureType.POLISH
        assert "quality_excellence" in config["cultural_focus"]
        assert "tradition_innovation" in config["cultural_focus"]
        assert config["communication_style"] == "formal_structured"
        assert config["leadership_style"] == "hierarchical_respectful"
        assert config["work_ethic"] is True

    def test_corporate_english_config(self):
        """Тест английской корпоративной конфигурации."""
        config = CORPORATE_ENGLISH_CONFIG

        assert config["target_culture"] == CultureType.ENGLISH
        assert "performance_metrics" in config["cultural_focus"]
        assert "innovation" in config["cultural_focus"]
        assert config["communication_style"] == "direct_efficient"
        assert config["leadership_style"] == "results_oriented"
        assert config["data_driven"] is True

    def test_corporate_examples(self):
        """Тест примеров корпоративных программ."""
        examples = get_corporate_examples()

        assert "leadership_development" in examples
        assert "stress_workplace" in examples
        assert "team_building" in examples
        assert "change_management" in examples

        # Проверяем культурную адаптацию
        for program in examples.values():
            assert "ukrainian" in program
            assert "polish" in program
            assert "english" in program


class TestUniversalConfigurationPatterns:
    """Тесты для проверки универсальности конфигураций."""

    def test_all_configs_have_required_fields(self):
        """Тест наличия обязательных полей во всех конфигурациях."""
        configs = [
            THERAPY_UKRAINIAN_CONFIG, THERAPY_POLISH_CONFIG, THERAPY_ENGLISH_CONFIG,
            EDUCATION_UKRAINIAN_CONFIG, EDUCATION_POLISH_CONFIG, EDUCATION_ENGLISH_CONFIG,
            CORPORATE_UKRAINIAN_CONFIG, CORPORATE_POLISH_CONFIG, CORPORATE_ENGLISH_CONFIG
        ]

        required_fields = [
            "target_culture", "domain_type", "project_type",
            "adaptation_depth", "sensitivity_level", "cultural_focus",
            "metaphor_themes", "communication_style"
        ]

        for config in configs:
            for field in required_fields:
                assert field in config, f"Поле {field} отсутствует в конфигурации"

    def test_cultural_focus_consistency(self):
        """Тест консистентности культурных фокусов."""
        # Каждая конфигурация должна иметь 3+ элемента в cultural_focus
        configs = [
            THERAPY_UKRAINIAN_CONFIG, THERAPY_POLISH_CONFIG, THERAPY_ENGLISH_CONFIG,
            EDUCATION_UKRAINIAN_CONFIG, EDUCATION_POLISH_CONFIG, EDUCATION_ENGLISH_CONFIG,
            CORPORATE_UKRAINIAN_CONFIG, CORPORATE_POLISH_CONFIG, CORPORATE_ENGLISH_CONFIG
        ]

        for config in configs:
            assert len(config["cultural_focus"]) >= 3
            assert isinstance(config["cultural_focus"], list)

    def test_examples_completeness(self):
        """Тест полноты примеров для всех культур."""
        all_examples = [
            get_therapy_examples(),
            get_education_examples(),
            get_corporate_examples()
        ]

        cultures = ["ukrainian", "polish", "english"]

        for examples_dict in all_examples:
            for technique_examples in examples_dict.values():
                for culture in cultures:
                    assert culture in technique_examples
                    assert isinstance(technique_examples[culture], str)
                    assert len(technique_examples[culture]) > 0