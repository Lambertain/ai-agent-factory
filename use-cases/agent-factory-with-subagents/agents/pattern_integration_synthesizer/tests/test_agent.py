"""
Тесты для основной структуры Pattern Integration Synthesizer Agent.
"""

import pytest
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel
from ..agent import (
    agent,
    run_pattern_integration_synthesizer,
    analyze_program_synergy,
    optimize_emotional_curve,
    create_module_sequence
)
from ..dependencies import PatternIntegrationSynthesizerDependencies


def test_agent_structure():
    """Тест базовой структуры агента."""
    assert isinstance(agent, Agent)
    assert agent._deps_type == PatternIntegrationSynthesizerDependencies


def test_agent_has_tools():
    """Тест наличия зарегистрированных инструментов."""
    # Агент должен иметь зарегистрированные инструменты
    tools = agent._function_tools
    assert len(tools) == 6  # 6 основных инструментов

    tool_names = {tool.name for tool in tools.values()}
    expected_tools = {
        "orchestrate_module_sequence",
        "manage_emotional_curve",
        "identify_resistance_points",
        "ensure_module_synergy",
        "analyze_program_coherence",
        "search_agent_knowledge"
    }

    assert expected_tools.issubset(tool_names)


def test_agent_system_prompt():
    """Тест наличия системного промпта."""
    # Системный промпт должен быть установлен
    assert agent._system_prompt is not None
    assert len(str(agent._system_prompt)) > 0


@pytest.mark.asyncio
async def test_run_pattern_integration_synthesizer_with_test_model():
    """Тест запуска агента с TestModel."""
    # Используем TestModel для тестирования без реальных API вызовов
    test_agent = Agent(
        model=TestModel(),
        deps_type=PatternIntegrationSynthesizerDependencies
    )

    deps = PatternIntegrationSynthesizerDependencies(
        api_key="test_key",
        patternshift_project_path="/test/path"
    )

    result = await test_agent.run(
        "Test message",
        deps=deps
    )

    assert result.data is not None


@pytest.mark.asyncio
async def test_analyze_program_synergy_structure():
    """Тест структуры функции analyze_program_synergy."""
    # Этот тест проверяет что функция имеет правильную сигнатуру
    import inspect
    sig = inspect.signature(analyze_program_synergy)

    assert "program_structure" in sig.parameters
    assert "api_key" in sig.parameters
    assert "patternshift_project_path" in sig.parameters


@pytest.mark.asyncio
async def test_optimize_emotional_curve_structure():
    """Тест структуры функции optimize_emotional_curve."""
    import inspect
    sig = inspect.signature(optimize_emotional_curve)

    assert "program_duration_days" in sig.parameters
    assert "target_conditions" in sig.parameters
    assert "api_key" in sig.parameters
    assert "program_intensity" in sig.parameters


@pytest.mark.asyncio
async def test_create_module_sequence_structure():
    """Тест структуры функции create_module_sequence."""
    import inspect
    sig = inspect.signature(create_module_sequence)

    assert "module_ids" in sig.parameters
    assert "phase_type" in sig.parameters
    assert "target_goals" in sig.parameters
    assert "api_key" in sig.parameters
