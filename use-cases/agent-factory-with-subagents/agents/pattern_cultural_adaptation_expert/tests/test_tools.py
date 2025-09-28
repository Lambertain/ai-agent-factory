"""
Тесты для инструментов Pattern Cultural Adaptation Expert Agent.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import sys
import os

# Добавляем путь к родительской директории для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import (
    analyze_cultural_context,
    adapt_content_culturally,
    generate_cultural_metaphors,
    validate_cultural_appropriateness,
    search_cultural_knowledge
)
from dependencies import CulturalAdaptationDependencies, CultureType


class TestCulturalAdaptationTools:
    """Тесты для инструментов культурной адаптации."""

    def setup_method(self):
        """Настройка для каждого теста."""
        self.deps = CulturalAdaptationDependencies(
            api_key="test_key",
            target_culture=CultureType.UKRAINIAN,
            domain_type="therapy",
            project_type="clinical"
        )
        self.mock_ctx = Mock()
        self.mock_ctx.deps = self.deps

    @pytest.mark.asyncio
    async def test_analyze_cultural_context(self):
        """Тест анализа культурного контекста."""
        result = await analyze_cultural_context(
            self.mock_ctx,
            culture="ukrainian",
            domain="therapy",
            specific_aspects=["family_values", "collective_trauma"]
        )

        assert isinstance(result, str)
        assert "ukrainian" in result.lower()
        assert "family" in result.lower() or "семья" in result.lower()

    @pytest.mark.asyncio
    async def test_adapt_content_culturally(self):
        """Тест культурной адаптации контента."""
        original_content = "Когнитивно-поведенческая терапия для управления тревогой"
        target_culture = "ukrainian"

        result = await adapt_content_culturally(
            self.mock_ctx,
            original_content=original_content,
            target_culture=target_culture,
            adaptation_type="therapeutic",
            sensitivity_level="high"
        )

        assert isinstance(result, str)
        assert len(result) > len(original_content)
        assert "украин" in result.lower() or "ukrainian" in result.lower()

    @pytest.mark.asyncio
    async def test_generate_cultural_metaphors(self):
        """Тест генерации культурных метафор."""
        concept = "psychological_resilience"
        target_culture = "ukrainian"

        result = await generate_cultural_metaphors(
            self.mock_ctx,
            concept=concept,
            target_culture=target_culture,
            metaphor_count=3,
            domain_context="therapy"
        )

        assert isinstance(result, str)
        assert "метафор" in result.lower() or "metaphor" in result.lower()

    @pytest.mark.asyncio
    async def test_validate_cultural_appropriateness(self):
        """Тест валидации культурной приемлемости."""
        content = "Техника медитации осознанности для снижения стресса"
        target_culture = "polish"

        result = await validate_cultural_appropriateness(
            self.mock_ctx,
            content=content,
            target_culture=target_culture,
            validation_criteria=["religious_sensitivity", "cultural_values"],
            domain="therapy"
        )

        assert isinstance(result, str)
        assert "валидация" in result.lower() or "validation" in result.lower()

    @pytest.mark.asyncio
    async def test_search_cultural_knowledge(self):
        """Тест поиска культурных знаний."""
        with patch('tools.mcp__archon__rag_search_knowledge_base') as mock_rag:
            mock_rag.return_value = {
                "success": True,
                "results": [
                    {
                        "content": "Украинская культура характеризуется...",
                        "metadata": {"title": "Украинская психология"}
                    }
                ]
            }

            result = await search_cultural_knowledge(
                self.mock_ctx,
                query="ukrainian culture therapy",
                culture_filter="ukrainian",
                domain_filter="therapy"
            )

            assert isinstance(result, str)
            assert mock_rag.called

    @pytest.mark.asyncio
    async def test_tools_with_different_cultures(self):
        """Тест инструментов с разными культурами."""
        cultures = ["ukrainian", "polish", "english"]

        for culture in cultures:
            result = await analyze_cultural_context(
                self.mock_ctx,
                culture=culture,
                domain="education"
            )

            assert isinstance(result, str)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_tools_error_handling(self):
        """Тест обработки ошибок в инструментах."""
        # Тест с некорректными параметрами
        try:
            await analyze_cultural_context(
                self.mock_ctx,
                culture="",  # Пустая культура
                domain="invalid_domain"
            )
        except Exception as e:
            # Ожидаем, что инструмент обработает ошибку gracefully
            pass

    @pytest.mark.asyncio
    async def test_adaptation_depth_levels(self):
        """Тест разных уровней глубины адаптации."""
        content = "Стратегии управления стрессом"

        depths = ["shallow", "moderate", "deep"]

        for depth in depths:
            # Обновляем зависимости для теста
            self.deps.adaptation_depth = depth

            result = await adapt_content_culturally(
                self.mock_ctx,
                original_content=content,
                target_culture="ukrainian",
                adaptation_type="educational"
            )

            assert isinstance(result, str)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_domain_specific_adaptation(self):
        """Тест адаптации для разных доменов."""
        domains = ["therapy", "education", "corporate"]
        content = "Техники эмоциональной регуляции"

        for domain in domains:
            self.deps.domain_type = domain

            result = await adapt_content_culturally(
                self.mock_ctx,
                original_content=content,
                target_culture="ukrainian",
                adaptation_type=domain
            )

            assert isinstance(result, str)
            assert len(result) > 0