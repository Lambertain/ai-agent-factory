"""
Тесты для основного агента Pattern Cultural Adaptation Expert.
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Добавляем путь к родительской директории для импорта агента
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import agent, CulturalAdaptationDependencies
from dependencies import CultureType


class TestPatternCulturalAdaptationAgent:
    """Тесты для основного агента культурной адаптации."""

    def test_agent_initialization(self):
        """Тест инициализации агента с зависимостями."""
        deps = CulturalAdaptationDependencies(
            api_key="test_key",
            target_culture=CultureType.UKRAINIAN,
            domain_type="therapy",
            project_type="clinical"
        )

        assert deps.api_key == "test_key"
        assert deps.target_culture == CultureType.UKRAINIAN
        assert deps.domain_type == "therapy"
        assert deps.project_type == "clinical"

    @pytest.mark.asyncio
    async def test_agent_basic_functionality(self):
        """Тест базовой функциональности агента."""
        deps = CulturalAdaptationDependencies(
            api_key="test_key",
            target_culture=CultureType.UKRAINIAN,
            domain_type="therapy"
        )

        # Мокаем ответ агента
        with patch.object(agent, 'run') as mock_run:
            mock_run.return_value = Mock(data="Адаптированный контент для украинской культуры")

            result = await agent.run(
                "Адаптируй технику управления тревогой для украинской культуры",
                deps=deps
            )

            assert mock_run.called
            assert "украинской культуры" in str(result.data)

    @pytest.mark.asyncio
    async def test_cultural_sensitivity_adaptation(self):
        """Тест адаптации с учетом культурной чувствительности."""
        deps = CulturalAdaptationDependencies(
            api_key="test_key",
            target_culture=CultureType.POLISH,
            domain_type="therapy",
            sensitivity_level="high",
            religious_accommodation=True
        )

        with patch.object(agent, 'run') as mock_run:
            mock_run.return_value = Mock(data="Техника с учетом католических ценностей")

            result = await agent.run(
                "Адаптируй семейную терапию для польской культуры",
                deps=deps
            )

            assert mock_run.called

    @pytest.mark.asyncio
    async def test_domain_specific_adaptation(self):
        """Тест адаптации для разных доменов."""
        # Тест для образовательного домена
        education_deps = CulturalAdaptationDependencies(
            api_key="test_key",
            target_culture=CultureType.ENGLISH,
            domain_type="education",
            project_type="e_learning"
        )

        with patch.object(agent, 'run') as mock_run:
            mock_run.return_value = Mock(data="Образовательный контент для англоязычной аудитории")

            result = await agent.run(
                "Адаптируй курс по психологии стресса",
                deps=education_deps
            )

            assert mock_run.called

    def test_agent_dependencies_validation(self):
        """Тест валидации зависимостей агента."""
        # Тест с минимальными требованиями
        minimal_deps = CulturalAdaptationDependencies(
            api_key="test_key"
        )

        assert minimal_deps.api_key == "test_key"
        assert minimal_deps.target_culture == CultureType.UNIVERSAL
        assert minimal_deps.domain_type == "general"

        # Тест с полными настройками
        full_deps = CulturalAdaptationDependencies(
            api_key="test_key",
            target_culture=CultureType.UKRAINIAN,
            domain_type="therapy",
            project_type="clinical",
            adaptation_depth="deep",
            sensitivity_level="high",
            cultural_validation_required=True,
            religious_accommodation=True,
            trauma_informed=True,
            professional_context=True
        )

        assert full_deps.adaptation_depth == "deep"
        assert full_deps.sensitivity_level == "high"
        assert full_deps.cultural_validation_required is True
        assert full_deps.religious_accommodation is True
        assert full_deps.trauma_informed is True
        assert full_deps.professional_context is True

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Тест обработки ошибок агента."""
        deps = CulturalAdaptationDependencies(
            api_key="invalid_key",
            target_culture=CultureType.UKRAINIAN
        )

        with patch.object(agent, 'run') as mock_run:
            mock_run.side_effect = Exception("API Error")

            with pytest.raises(Exception):
                await agent.run("Тестовый запрос", deps=deps)