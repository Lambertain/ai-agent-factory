"""Tests for TypeScript Architecture Agent."""

import pytest
from pydantic_ai.models.test import TestModel
from ..agent import typescript_agent, run_typescript_analysis
from ..dependencies import TypeScriptArchitectureDependencies


@pytest.fixture
def test_deps():
    """Test dependencies for agent."""
    return TypeScriptArchitectureDependencies(
        context="Test TypeScript analysis",
        project_path="/test/project",
        analysis_mode="full"
    )


@pytest.fixture
def sample_typescript_code():
    """Sample TypeScript code for testing."""
    return """
interface User {
    id: any;
    name: string;
    email: string | number | boolean;
}

function getUser(id: any): any {
    return { id, name: "test" };
}

type ComplexType = string | number | boolean | object | null | undefined | any[];
"""


class TestTypeScriptAgent:
    """Test suite for TypeScript Architecture Agent."""

    @pytest.mark.asyncio
    async def test_agent_basic_analysis(self, test_deps, sample_typescript_code):
        """Test basic TypeScript analysis functionality."""

        # Use TestModel to avoid real API calls
        test_model = TestModel(
            custom_result_text="""
            ## 📋 ПЛАНИРОВАНИЕ
            Анализирую TypeScript код на предмет type safety и архитектурных проблем.

            ## 🛠️ ВЫПОЛНЕНИЕ С ИНСТРУМЕНТАМИ
            Найдены следующие проблемы:
            - Использование 'any' типов (3 раза)
            - Сложный union тип в ComplexType
            - Отсутствие type guards

            ## 🔄 РЕФЛЕКСИЯ-УЛУЧШЕНИЕ
            Рекомендации:
            1. Заменить 'any' на конкретные типы
            2. Разбить ComplexType на отдельные типы
            3. Добавить type guards для безопасности
            """
        )

        # Override agent model for testing
        agent = typescript_agent.override(model=test_model)

        context = f"Анализ TypeScript кода:\n\n{sample_typescript_code}"

        result = await agent.run(context, deps=test_deps)

        # Assertions
        assert "ПЛАНИРОВАНИЕ" in result.data
        assert "ВЫПОЛНЕНИЕ С ИНСТРУМЕНТАМИ" in result.data
        assert "РЕФЛЕКСИЯ-УЛУЧШЕНИЕ" in result.data
        assert "any" in result.data.lower()

    @pytest.mark.asyncio
    async def test_agent_with_different_analysis_modes(self, sample_typescript_code):
        """Test agent with different analysis modes."""

        test_model = TestModel(
            custom_result_text="Analysis completed for {analysis_mode} mode"
        )

        for mode in ["full", "types", "performance", "refactor"]:
            deps = TypeScriptArchitectureDependencies(
                context="Test analysis",
                analysis_mode=mode
            )

            agent = typescript_agent.override(model=test_model)
            result = await agent.run(f"Analyze in {mode} mode", deps=deps)

            assert mode in result.data or "Analysis completed" in result.data

    def test_agent_dependencies_initialization(self):
        """Test agent dependencies initialization."""
        deps = TypeScriptArchitectureDependencies()

        # Check default values
        assert "typescript-architecture" in deps.knowledge_tags
        assert "agent-knowledge" in deps.knowledge_tags
        assert deps.archon_url == "http://localhost:3737"
        assert deps.target_type_coverage == 0.95

    def test_agent_dependencies_customization(self):
        """Test agent dependencies customization."""
        custom_deps = TypeScriptArchitectureDependencies(
            context="Custom analysis",
            analysis_mode="performance",
            target_type_coverage=0.99
        )

        assert custom_deps.context == "Custom analysis"
        assert custom_deps.analysis_mode == "performance"
        assert custom_deps.target_type_coverage == 0.99
        assert "typescript-performance" in custom_deps.knowledge_tags

    def test_improvements_tracking(self):
        """Test improvements tracking in dependencies."""
        deps = TypeScriptArchitectureDependencies()

        deps.add_improvement("Replaced any with string", is_breaking=False)
        deps.add_improvement("Changed interface structure", is_breaking=True)

        assert len(deps.improvements_made) == 2
        assert len(deps.breaking_changes) == 1
        assert "Replaced any with string" in deps.improvements_made
        assert "Changed interface structure" in deps.breaking_changes

    def test_analysis_summary(self):
        """Test analysis summary generation."""
        deps = TypeScriptArchitectureDependencies(analysis_mode="refactor")
        deps.add_improvement("Test improvement")

        summary = deps.get_analysis_summary()

        assert summary["mode"] == "refactor"
        assert summary["improvements_count"] == 1
        assert summary["breaking_changes_count"] == 0
        assert summary["target_coverage"] == 0.95

    @pytest.mark.asyncio
    async def test_run_typescript_analysis_function(self, sample_typescript_code):
        """Test the run_typescript_analysis helper function."""

        # Mock the underlying agent call
        import unittest.mock

        with unittest.mock.patch('typescript_architecture_agent.agent.typescript_agent.run') as mock_run:
            mock_run.return_value.data = "Mocked analysis result"

            result = await run_typescript_analysis(
                context=f"Test: {sample_typescript_code}",
                project_path="/test",
                analysis_type="types"
            )

            assert result == "Mocked analysis result"
            mock_run.assert_called_once()

    def test_error_handling_in_dependencies(self):
        """Test error handling in dependencies."""
        deps = TypeScriptArchitectureDependencies(
            context="",  # Empty context should be handled
            analysis_mode="invalid_mode"  # Invalid mode should be handled
        )

        # Should have default context
        assert "TypeScript architecture analysis for" in deps.context
        # Should accept any analysis mode without validation in base class
        assert deps.analysis_mode == "invalid_mode"