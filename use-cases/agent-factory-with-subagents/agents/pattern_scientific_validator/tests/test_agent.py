"""
Тесты основного агента Pattern Scientific Validator.
"""

import pytest
from pydantic_ai.models.test import TestModel
from ..agent import agent, run_pattern_scientific_validator
from ..dependencies import PatternScientificValidatorDependencies
from ..models import ValidationReport


@pytest.mark.asyncio
async def test_agent_structure():
    """
    Тест структуры агента - проверка базовой конфигурации.
    """
    assert agent is not None
    assert agent.deps_type == PatternScientificValidatorDependencies
    assert len(agent._function_tools) == 6  # Должно быть 6 инструментов


@pytest.mark.asyncio
async def test_agent_tools_registered():
    """
    Тест регистрации всех инструментов агента.
    """
    tool_names = [tool.name for tool in agent._function_tools.values()]

    expected_tools = [
        "validate_technique_efficacy",
        "check_safety",
        "review_ethics",
        "validate_adaptation",
        "assess_effectiveness",
        "search_agent_knowledge"
    ]

    for expected_tool in expected_tools:
        assert expected_tool in tool_names, f"Инструмент {expected_tool} не зарегистрирован"


@pytest.mark.asyncio
async def test_agent_with_test_model(mock_api_key, mock_project_path):
    """
    Тест агента с TestModel для проверки логики без API вызовов.
    """
    # Используем TestModel для быстрого тестирования
    test_agent = agent.override(model=TestModel())

    deps = PatternScientificValidatorDependencies(
        api_key=mock_api_key,
        patternshift_project_path=mock_project_path
    )

    result = await test_agent.run(
        "Провалидируй технику Mindfulness Meditation",
        deps=deps
    )

    assert result is not None
    assert isinstance(result.data, str)


@pytest.mark.asyncio
async def test_run_pattern_scientific_validator_basic(sample_module_data, mock_api_key):
    """
    Тест базового запуска валидации модуля - ожидаемое использование.
    """
    # Используем TestModel для избежания реальных API вызовов
    test_agent = agent.override(model=TestModel())

    # Временно подменяем глобального агента
    import sys
    original_agent = sys.modules['pattern_scientific_validator.agent'].agent
    sys.modules['pattern_scientific_validator.agent'].agent = test_agent

    try:
        result = await run_pattern_scientific_validator(
            module_data=sample_module_data,
            api_key=mock_api_key,
            verbose=False
        )

        assert isinstance(result, ValidationReport)
        assert result.module_id == sample_module_data["module_id"]
        assert result.module_name == sample_module_data["module_name"]

    finally:
        # Восстанавливаем оригинального агента
        sys.modules['pattern_scientific_validator.agent'].agent = original_agent


@pytest.mark.asyncio
async def test_run_pattern_scientific_validator_empty_module(mock_api_key):
    """
    Тест валидации пустого модуля - edge case.
    """
    empty_module = {
        "module_id": "",
        "module_name": "",
        "techniques": [],
        "content": "",
        "target_conditions": []
    }

    test_agent = agent.override(model=TestModel())
    import sys
    original_agent = sys.modules['pattern_scientific_validator.agent'].agent
    sys.modules['pattern_scientific_validator.agent'].agent = test_agent

    try:
        result = await run_pattern_scientific_validator(
            module_data=empty_module,
            api_key=mock_api_key,
            verbose=False
        )

        assert isinstance(result, ValidationReport)
        # Должен обработать пустой модуль корректно

    finally:
        sys.modules['pattern_scientific_validator.agent'].agent = original_agent


@pytest.mark.asyncio
async def test_run_pattern_scientific_validator_missing_api_key():
    """
    Тест валидации без API ключа - failure case.
    """
    module_data = {
        "module_id": "test_001",
        "module_name": "Test Module",
        "techniques": ["test_technique"],
        "content": "Test content",
        "target_conditions": ["test"]
    }

    with pytest.raises((ValueError, Exception)):
        await run_pattern_scientific_validator(
            module_data=module_data,
            api_key="",  # Пустой API ключ
            verbose=False
        )


@pytest.mark.asyncio
async def test_agent_system_prompt_exists():
    """
    Тест наличия системного промпта у агента.
    """
    assert agent._system_prompt is not None
    assert len(str(agent._system_prompt)) > 100  # Промпт должен быть содержательным
    assert "научн" in str(agent._system_prompt).lower() or "evidence" in str(agent._system_prompt).lower()
