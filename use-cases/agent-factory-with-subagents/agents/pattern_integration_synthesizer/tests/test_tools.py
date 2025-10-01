"""
Тесты для инструментов Pattern Integration Synthesizer Agent.
"""

import pytest
from pydantic_ai import RunContext
from ..tools import (
    orchestrate_module_sequence,
    manage_emotional_curve,
    identify_resistance_points,
    ensure_module_synergy,
    analyze_program_coherence,
    search_agent_knowledge
)


# ===== ТЕСТЫ orchestrate_module_sequence =====

@pytest.mark.asyncio
async def test_orchestrate_module_sequence_beginning_phase(mock_dependencies, sample_module_list):
    """Тест оркестрации модулей для Beginning phase."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await orchestrate_module_sequence(
        ctx=ctx,
        module_ids=sample_module_list[:3],
        phase_type="beginning",
        target_goals=["build awareness", "psychoeducation"]
    )

    assert isinstance(result, str)
    assert "beginning" in result.lower()
    assert "progressive_intensity" in result.lower()
    assert len(sample_module_list[:3]) > 0


@pytest.mark.asyncio
async def test_orchestrate_module_sequence_development_phase(mock_dependencies, sample_module_list):
    """Тест оркестрации модулей для Development phase."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await orchestrate_module_sequence(
        ctx=ctx,
        module_ids=sample_module_list[2:5],
        phase_type="development",
        target_goals=["challenge thoughts", "increase activity"]
    )

    assert isinstance(result, str)
    assert "development" in result.lower()
    assert "technique_sandwich" in result.lower()


@pytest.mark.asyncio
async def test_orchestrate_module_sequence_integration_phase(mock_dependencies, sample_module_list):
    """Тест оркестрации модулей для Integration phase."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await orchestrate_module_sequence(
        ctx=ctx,
        module_ids=sample_module_list[3:],
        phase_type="integration",
        target_goals=["transfer to life", "maintain progress"]
    )

    assert isinstance(result, str)
    assert "integration" in result.lower()
    assert "spiral_deepening" in result.lower()


@pytest.mark.asyncio
async def test_orchestrate_module_sequence_unknown_phase(mock_dependencies, sample_module_list):
    """Тест оркестрации с неизвестным типом фазы - должен использовать default паттерн."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await orchestrate_module_sequence(
        ctx=ctx,
        module_ids=sample_module_list[:2],
        phase_type="unknown_phase",
        target_goals=["test goal"]
    )

    assert isinstance(result, str)
    assert "progressive_intensity" in result.lower()  # default pattern


# ===== ТЕСТЫ manage_emotional_curve =====

@pytest.mark.asyncio
async def test_manage_emotional_curve_21_days_medium(mock_dependencies):
    """Тест управления эмоциональной кривой для 21-дневной программы средней интенсивности."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await manage_emotional_curve(
        ctx=ctx,
        program_duration_days=21,
        program_intensity="medium"
    )

    assert isinstance(result, str)
    assert "21" in result
    assert "medium" in result.lower()
    assert "excitement" in result.lower()
    assert "resistance" in result.lower()
    assert "breakthrough" in result.lower()
    assert "integration" in result.lower()
    assert "mastery" in result.lower()


@pytest.mark.asyncio
async def test_manage_emotional_curve_intensive(mock_dependencies):
    """Тест управления эмоциональной кривой для интенсивной программы."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await manage_emotional_curve(
        ctx=ctx,
        program_duration_days=14,
        program_intensity="intensive"
    )

    assert isinstance(result, str)
    assert "intensive" in result.lower()


@pytest.mark.asyncio
async def test_manage_emotional_curve_light(mock_dependencies):
    """Тест управления эмоциональной кривой для легкой программы."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await manage_emotional_curve(
        ctx=ctx,
        program_duration_days=7,
        program_intensity="light"
    )

    assert isinstance(result, str)
    assert "light" in result.lower()


# ===== ТЕСТЫ identify_resistance_points =====

@pytest.mark.asyncio
async def test_identify_resistance_points_standard(mock_dependencies, sample_program_structure):
    """Тест идентификации стандартных точек сопротивления."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await identify_resistance_points(
        ctx=ctx,
        program=sample_program_structure
    )

    assert isinstance(result, str)
    assert "4-7" in result  # Первая критическая точка
    assert "novelty_wearoff" in result.lower()
    assert "severity" in result.lower()


@pytest.mark.asyncio
async def test_identify_resistance_points_with_user_profile(mock_dependencies, sample_program_structure):
    """Тест идентификации точек сопротивления с профилем пользователя."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    user_profile = {
        "previous_dropout": True,
        "low_motivation": True
    }

    result = await identify_resistance_points(
        ctx=ctx,
        program=sample_program_structure,
        user_profile=user_profile
    )

    assert isinstance(result, str)
    assert "dropout" in result.lower()
    assert "motivation" in result.lower()


# ===== ТЕСТЫ ensure_module_synergy =====

@pytest.mark.asyncio
async def test_ensure_module_synergy_high_synergy_pair(mock_dependencies):
    """Тест проверки синергии между известными высокосинергичными модулями."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await ensure_module_synergy(
        ctx=ctx,
        module_a_id="cognitive_restructuring",
        module_b_id="behavioral_activation",
        gap_days=1
    )

    assert isinstance(result, str)
    assert "synergy" in result.lower()


@pytest.mark.asyncio
async def test_ensure_module_synergy_zero_gap(mock_dependencies):
    """Тест проверки синергии модулей с нулевым промежутком (один день)."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await ensure_module_synergy(
        ctx=ctx,
        module_a_id="mindfulness",
        module_b_id="cognitive_defusion",
        gap_days=0
    )

    assert isinstance(result, str)
    assert "0 days" in result.lower() or "zero" in result.lower() or "same day" in result.lower()


@pytest.mark.asyncio
async def test_ensure_module_synergy_large_gap(mock_dependencies):
    """Тест проверки синергии модулей с большим промежутком."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await ensure_module_synergy(
        ctx=ctx,
        module_a_id="values_clarification",
        module_b_id="committed_action",
        gap_days=5
    )

    assert isinstance(result, str)
    assert "5 days" in result or "large" in result.lower() or "big" in result.lower()


# ===== ТЕСТЫ analyze_program_coherence =====

@pytest.mark.asyncio
async def test_analyze_program_coherence_standard(mock_dependencies, sample_program_structure):
    """Тест анализа целостности стандартной программы."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await analyze_program_coherence(
        ctx=ctx,
        program_structure=sample_program_structure
    )

    assert isinstance(result, str)
    assert "coherence" in result.lower()
    assert "phases" in result.lower()


@pytest.mark.asyncio
async def test_analyze_program_coherence_optimal_structure(mock_dependencies):
    """Тест анализа целостности оптимальной 3-фазовой структуры."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    optimal_program = {
        "program_name": "Optimal Program",
        "total_days": 21,
        "phases": [
            {"phase_type": "beginning", "days": []},
            {"phase_type": "development", "days": []},
            {"phase_type": "integration", "days": []}
        ]
    }

    result = await analyze_program_coherence(
        ctx=ctx,
        program_structure=optimal_program
    )

    assert isinstance(result, str)
    assert "3" in result  # Optimal 3 phases


# ===== ТЕСТЫ search_agent_knowledge =====

@pytest.mark.asyncio
async def test_search_agent_knowledge_orchestration(mock_dependencies):
    """Тест поиска знаний по оркестрации."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await search_agent_knowledge(
        ctx=ctx,
        query="orchestration patterns",
        match_count=3
    )

    assert isinstance(result, str)
    assert "orchestration" in result.lower() or "pattern" in result.lower()


@pytest.mark.asyncio
async def test_search_agent_knowledge_emotional_curve(mock_dependencies):
    """Тест поиска знаний об эмоциональной кривой."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await search_agent_knowledge(
        ctx=ctx,
        query="emotional curve stages",
        match_count=5
    )

    assert isinstance(result, str)
    assert "emotional" in result.lower() or "curve" in result.lower() or "stage" in result.lower()


@pytest.mark.asyncio
async def test_search_agent_knowledge_load_management(mock_dependencies):
    """Тест поиска знаний об управлении нагрузкой."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await search_agent_knowledge(
        ctx=ctx,
        query="module load intensity",
        match_count=3
    )

    assert isinstance(result, str)
    assert "load" in result.lower() or "intensity" in result.lower()


@pytest.mark.asyncio
async def test_search_agent_knowledge_transitions(mock_dependencies):
    """Тест поиска знаний о переходах."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await search_agent_knowledge(
        ctx=ctx,
        query="transition types",
        match_count=4
    )

    assert isinstance(result, str)
    assert "transition" in result.lower()


@pytest.mark.asyncio
async def test_search_agent_knowledge_unknown_topic(mock_dependencies):
    """Тест поиска знаний по неизвестной теме."""
    ctx = RunContext(deps=mock_dependencies, retry=0)

    result = await search_agent_knowledge(
        ctx=ctx,
        query="completely unknown topic xyz",
        match_count=2
    )

    assert isinstance(result, str)
    # Должен вернуть подсказку о ключевых словах
