"""
Интеграционные тесты для Pattern Integration Synthesizer Agent.
"""

import pytest
from ..dependencies import PatternIntegrationSynthesizerDependencies
from ..agent import agent


@pytest.mark.asyncio
async def test_dependencies_initialization(mock_api_key, mock_project_path):
    """Тест инициализации зависимостей."""
    deps = PatternIntegrationSynthesizerDependencies(
        api_key=mock_api_key,
        patternshift_project_path=mock_project_path
    )

    assert deps.api_key == mock_api_key
    assert deps.patternshift_project_path == mock_project_path
    assert deps.orchestration_patterns_db is not None
    assert deps.emotional_curve_db is not None
    assert deps.module_load_db is not None
    assert deps.transition_patterns_db is not None


@pytest.mark.asyncio
async def test_knowledge_databases_populated(mock_dependencies):
    """Тест что базы знаний заполнены данными."""
    # Orchestration Patterns
    assert len(mock_dependencies.orchestration_patterns_db.patterns) > 0
    assert "progressive_intensity" in mock_dependencies.orchestration_patterns_db.patterns
    assert "technique_sandwich" in mock_dependencies.orchestration_patterns_db.patterns

    # Emotional Curve
    assert len(mock_dependencies.emotional_curve_db.curve_stages) > 0
    assert "days_1_3_excitement" in mock_dependencies.emotional_curve_db.curve_stages

    # Module Load
    assert mock_dependencies.module_load_db.load_guidelines is not None
    assert "daily_limits" in mock_dependencies.module_load_db.load_guidelines

    # Transition Patterns
    assert len(mock_dependencies.transition_patterns_db.transition_types) > 0
    assert "bridge" in mock_dependencies.transition_patterns_db.transition_types


@pytest.mark.asyncio
async def test_agent_full_workflow(mock_dependencies):
    """Тест полного рабочего процесса агента."""
    from pydantic_ai.models.test import TestModel

    # Создаем тестового агента с TestModel
    test_agent = agent.override(model=TestModel())

    message = "Оркеструй модули для 21-дневной программы по работе с тревогой"

    result = await test_agent.run(message, deps=mock_dependencies)

    assert result.data is not None


@pytest.mark.asyncio
async def test_orchestration_patterns_accessibility(orchestration_patterns_db):
    """Тест доступности паттернов оркестрации."""
    patterns = orchestration_patterns_db.patterns

    # Проверяем основные паттерны
    assert "progressive_intensity" in patterns
    assert "technique_sandwich" in patterns
    assert "energy_wave" in patterns
    assert "spiral_deepening" in patterns

    # Проверяем структуру паттерна
    progressive = patterns["progressive_intensity"]
    assert "description" in progressive
    assert "sequence" in progressive
    assert "rationale" in progressive
    assert "best_for" in progressive


@pytest.mark.asyncio
async def test_emotional_curve_stages(emotional_curve_db):
    """Тест этапов эмоциональной кривой."""
    stages = emotional_curve_db.curve_stages

    # Проверяем все 5 этапов
    assert "days_1_3_excitement" in stages
    assert "days_4_7_resistance" in stages
    assert "days_8_12_breakthrough" in stages
    assert "days_13_18_integration" in stages
    assert "days_19_21_mastery" in stages

    # Проверяем структуру этапа
    excitement = stages["days_1_3_excitement"]
    assert excitement["stage"] == "excitement"
    assert excitement["energy"] == "high"
    assert excitement["motivation"] == "high"


@pytest.mark.asyncio
async def test_resistance_points_defined(emotional_curve_db):
    """Тест определенных точек сопротивления."""
    resistance_points = emotional_curve_db.resistance_points

    assert len(resistance_points) > 0

    # Проверяем критическую точку 4-7 дней
    critical_point = next(
        (rp for rp in resistance_points if rp["day_range"] == "4-7"),
        None
    )

    assert critical_point is not None
    assert critical_point["type"] == "novelty_wearoff"
    assert critical_point["severity"] == "high"
    assert len(critical_point["mitigation"]) > 0


@pytest.mark.asyncio
async def test_module_load_guidelines(module_load_db):
    """Тест руководств по нагрузке модулей."""
    guidelines = module_load_db.load_guidelines

    assert "daily_limits" in guidelines
    assert "module_intensity" in guidelines
    assert "recovery_time" in guidelines

    # Проверяем дневные лимиты
    daily_limits = guidelines["daily_limits"]
    assert "total_minutes" in daily_limits
    assert "sessions_per_day" in daily_limits
    assert "intensive_modules" in daily_limits


@pytest.mark.asyncio
async def test_transition_types(transition_patterns_db):
    """Тест типов переходов."""
    transitions = transition_patterns_db.transition_types

    # Проверяем основные типы переходов
    assert "bridge" in transitions
    assert "energizer" in transitions
    assert "grounding" in transitions
    assert "reflection" in transitions

    # Проверяем структуру типа перехода
    bridge = transitions["bridge"]
    assert "purpose" in bridge
    assert "duration" in bridge
    assert "elements" in bridge
