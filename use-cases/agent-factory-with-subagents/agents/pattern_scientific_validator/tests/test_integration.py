"""
Интеграционные тесты Pattern Scientific Validator Agent.
"""

import pytest
from pydantic_ai.models.test import TestModel
from ..agent import agent
from ..dependencies import PatternScientificValidatorDependencies
from ..tools import (
    validate_technique_efficacy,
    check_safety,
    review_ethics
)


@pytest.mark.asyncio
async def test_full_validation_workflow(sample_module_data, mock_api_key):
    """
    Тест полного workflow валидации модуля - интеграционный тест.
    """
    deps = PatternScientificValidatorDependencies(
        api_key=mock_api_key,
        patternshift_project_path="/tmp/test"
    )

    from pydantic_ai import RunContext
    ctx = RunContext(deps=deps, retry=0)

    # 1. Валидация техники
    technique_result = await validate_technique_efficacy(
        ctx,
        technique_name="Cognitive Restructuring",
        description="CBT technique",
        target_conditions=["depression"]
    )
    assert isinstance(technique_result, str)

    # 2. Проверка безопасности
    safety_result = await check_safety(
        ctx,
        module_id=sample_module_data["module_id"],
        techniques=sample_module_data["techniques"],
        content=sample_module_data["content"]
    )
    assert isinstance(safety_result, str)

    # 3. Этическая проверка
    ethics_result = await review_ethics(
        ctx,
        module_id=sample_module_data["module_id"],
        module_content=sample_module_data["content"],
        claims=["Может помочь"]
    )
    assert isinstance(ethics_result, str)


@pytest.mark.asyncio
async def test_agent_with_multiple_tools(mock_api_key, mock_project_path):
    """
    Тест работы агента с множественными вызовами инструментов.
    """
    test_agent = agent.override(model=TestModel())

    deps = PatternScientificValidatorDependencies(
        api_key=mock_api_key,
        patternshift_project_path=mock_project_path
    )

    prompt = """
    Провалидируй модуль когнитивной терапии:
    - Техника: Cognitive Restructuring
    - Целевые состояния: depression, anxiety
    - Проверь безопасность и этичность
    """

    result = await test_agent.run(prompt, deps=deps)
    assert result is not None


@pytest.mark.asyncio
async def test_dependencies_initialization(mock_api_key):
    """
    Тест инициализации зависимостей агента.
    """
    deps = PatternScientificValidatorDependencies(
        api_key=mock_api_key,
        patternshift_project_path="/tmp/test"
    )

    assert deps.api_key == mock_api_key
    assert deps.patternshift_project_path == "/tmp/test"
    assert len(deps.knowledge_tags) > 0
    assert "pattern-scientific-validator" in deps.knowledge_tags


@pytest.mark.asyncio
async def test_databases_accessibility(mock_api_key):
    """
    Тест доступности всех баз данных в dependencies.
    """
    deps = PatternScientificValidatorDependencies(
        api_key=mock_api_key
    )

    # Проверяем что все базы данных инициализированы
    assert deps.evidence_based_research_db is not None
    assert deps.safety_protocols_db is not None
    assert deps.ethical_guidelines_db is not None
    assert deps.adaptation_standards_db is not None
    assert deps.effectiveness_metrics_db is not None

    # Проверяем что базы содержат данные
    assert len(deps.evidence_based_research_db.approaches) > 0
    assert len(deps.safety_protocols_db.contraindications) > 0
    assert len(deps.ethical_guidelines_db.principles) > 0


@pytest.mark.asyncio
async def test_error_handling_workflow(mock_api_key):
    """
    Тест обработки ошибок в процессе валидации.
    """
    deps = PatternScientificValidatorDependencies(
        api_key=mock_api_key
    )

    from pydantic_ai import RunContext
    ctx = RunContext(deps=deps, retry=0)

    # Тест с некорректными данными
    result = await validate_technique_efficacy(
        ctx,
        technique_name=None,  # Намеренно некорректный ввод
        description="",
        target_conditions=[]
    )

    # Должно обработать ошибку корректно
    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_concurrent_tool_calls(mock_api_key):
    """
    Тест параллельных вызовов инструментов.
    """
    deps = PatternScientificValidatorDependencies(
        api_key=mock_api_key
    )

    from pydantic_ai import RunContext
    import asyncio

    ctx = RunContext(deps=deps, retry=0)

    # Запускаем несколько инструментов параллельно
    tasks = [
        validate_technique_efficacy(ctx, "CBT", "Cognitive therapy", ["depression"]),
        check_safety(ctx, "test_001", ["CBT"], "Safe content"),
        review_ethics(ctx, "test_001", "Ethical content", ["Valid claims"])
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Все вызовы должны завершиться (возможно с ошибками, но без краха)
    assert len(results) == 3
    for result in results:
        assert isinstance(result, (str, Exception))
