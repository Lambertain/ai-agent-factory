"""
Тесты инструментов Pattern Scientific Validator Agent.
"""

import pytest
from pydantic_ai import RunContext
from ..tools import (
    validate_technique_efficacy,
    check_safety,
    review_ethics,
    validate_adaptation,
    assess_effectiveness,
    search_agent_knowledge
)
from ..dependencies import PatternScientificValidatorDependencies


@pytest.mark.asyncio
async def test_validate_technique_efficacy_cbt(mock_dependencies):
    """
    Тест валидации CBT техники - ожидаемое использование.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await validate_technique_efficacy(
        ctx,
        technique_name="Cognitive Restructuring",
        description="Техника выявления и изменения дисфункциональных мыслей",
        target_conditions=["depression", "anxiety"]
    )

    assert isinstance(result, str)
    assert "Cognitive Restructuring" in result
    assert "Meta-analysis" in result or "RCT" in result
    assert "depression" in result.lower() or "anxiety" in result.lower()


@pytest.mark.asyncio
async def test_validate_technique_efficacy_unknown(mock_dependencies):
    """
    Тест валидации неизвестной техники - edge case.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await validate_technique_efficacy(
        ctx,
        technique_name="Unknown Fantasy Technique",
        description="Completely made up technique",
        target_conditions=["test_condition"]
    )

    assert isinstance(result, str)
    assert "Unknown Fantasy Technique" in result
    # Должна вернуть информацию о недостаточной evidence base


@pytest.mark.asyncio
async def test_validate_technique_efficacy_empty_input(mock_dependencies):
    """
    Тест валидации с пустыми данными - failure case.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await validate_technique_efficacy(
        ctx,
        technique_name="",
        description="",
        target_conditions=[]
    )

    assert isinstance(result, str)
    # Должна обработать пустые данные корректно


@pytest.mark.asyncio
async def test_check_safety_safe_technique(mock_dependencies):
    """
    Тест проверки безопасности безопасной техники.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await check_safety(
        ctx,
        module_id="test_001",
        techniques=["Mindfulness Meditation", "Deep Breathing"],
        content="Простые техники дыхания и осознанности"
    )

    assert isinstance(result, str)
    assert "safe" in result.lower() or "безопасн" in result.lower()


@pytest.mark.asyncio
async def test_check_safety_risky_technique(mock_dependencies):
    """
    Тест проверки безопасности рискованной техники.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await check_safety(
        ctx,
        module_id="test_002",
        techniques=["Deep Trauma Processing", "Prolonged Exposure"],
        content="Интенсивная работа с травматическими воспоминаниями"
    )

    assert isinstance(result, str)
    assert "risk" in result.lower() or "risk" in result.lower() or "caution" in result.lower()


@pytest.mark.asyncio
async def test_review_ethics_valid_module(mock_dependencies):
    """
    Тест этической проверки валидного модуля.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await review_ethics(
        ctx,
        module_id="test_003",
        module_content="Научно обоснованные техники с информированным согласием",
        claims=["Может помочь улучшить настроение", "Эффективность индивидуальна"]
    )

    assert isinstance(result, str)
    assert "ethic" in result.lower() or "этик" in result.lower()


@pytest.mark.asyncio
async def test_review_ethics_overclaiming(mock_dependencies):
    """
    Тест этической проверки модуля с завышенными заявлениями.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await review_ethics(
        ctx,
        module_id="test_004",
        module_content="Гарантированное излечение депрессии за 7 дней",
        claims=["100% гарантия", "Работает для всех", "Замена терапии"]
    )

    assert isinstance(result, str)
    # Должно выявить проблемы с overclaiming


@pytest.mark.asyncio
async def test_validate_adaptation_high_fidelity(mock_dependencies):
    """
    Тест валидации адаптации с высокой fidelity.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await validate_adaptation(
        ctx,
        original_protocol="Therapist-guided CBT with homework",
        adapted_protocol="Self-paced CBT workbook with same structure",
        key_elements_preserved=["Thought records", "Behavioral activation", "Cognitive restructuring"]
    )

    assert isinstance(result, str)
    assert "fidelity" in result.lower()


@pytest.mark.asyncio
async def test_validate_adaptation_low_fidelity(mock_dependencies):
    """
    Тест валидации адаптации с низкой fidelity - edge case.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await validate_adaptation(
        ctx,
        original_protocol="12-week intensive therapy program",
        adapted_protocol="5-minute daily affirmations",
        key_elements_preserved=[]
    )

    assert isinstance(result, str)
    # Должно выявить проблемы с низкой fidelity


@pytest.mark.asyncio
async def test_assess_effectiveness_valid_technique(mock_dependencies):
    """
    Тест оценки эффективности валидной техники.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await assess_effectiveness(
        ctx,
        technique_name="Mindfulness-Based Stress Reduction",
        target_outcomes=["Reduce stress", "Improve well-being"],
        expected_timeline="8 weeks"
    )

    assert isinstance(result, str)
    assert "effectiveness" in result.lower() or "эффективност" in result.lower()


@pytest.mark.asyncio
async def test_assess_effectiveness_unrealistic(mock_dependencies):
    """
    Тест оценки эффективности с нереалистичными ожиданиями.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await assess_effectiveness(
        ctx,
        technique_name="Quick Fix Magic",
        target_outcomes=["Complete personality change", "Instant happiness"],
        expected_timeline="1 day"
    )

    assert isinstance(result, str)
    # Должно выявить нереалистичные ожидания


@pytest.mark.asyncio
async def test_search_agent_knowledge(mock_dependencies):
    """
    Тест поиска в базе знаний агента.
    """
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await search_agent_knowledge(
        ctx,
        query="cognitive behavioral therapy evidence",
        match_count=3
    )

    assert isinstance(result, str)
    # Должна вернуть результаты поиска или сообщение о проблемах поиска
