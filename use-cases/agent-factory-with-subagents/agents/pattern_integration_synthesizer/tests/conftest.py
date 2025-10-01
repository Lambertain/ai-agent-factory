"""
Pytest конфигурация и фикстуры для Pattern Integration Synthesizer Agent.
"""

import pytest
from ..dependencies import (
    PatternIntegrationSynthesizerDependencies,
    OrchestrationPatternsDatabase,
    EmotionalCurveDatabase,
    ModuleLoadDatabase,
    TransitionPatternsDatabase
)


@pytest.fixture
def mock_api_key():
    """Mock API key для тестирования."""
    return "test_api_key_12345"


@pytest.fixture
def mock_project_path():
    """Mock путь к проекту PatternShift."""
    return "/path/to/patternshift"


@pytest.fixture
def mock_dependencies(mock_api_key, mock_project_path):
    """Mock зависимости для тестирования."""
    return PatternIntegrationSynthesizerDependencies(
        api_key=mock_api_key,
        patternshift_project_path=mock_project_path,
        agent_name="pattern_integration_synthesizer",
        knowledge_tags=[
            "pattern-integration-synthesizer",
            "orchestration",
            "synergy"
        ],
        archon_project_id="test_project_id"
    )


@pytest.fixture
def sample_program_structure():
    """Пример структуры программы для тестирования."""
    return {
        "program_id": "test_prog_001",
        "program_name": "Test Anxiety Program",
        "total_days": 21,
        "target_conditions": ["anxiety", "stress"],
        "overall_goals": ["reduce anxiety", "build coping skills"],
        "phases": [
            {
                "phase_type": "beginning",
                "phase_name": "Foundation",
                "duration_days": 7,
                "phase_goals": ["build awareness", "psychoeducation"],
                "days": [
                    {
                        "day_number": 1,
                        "phase": "beginning",
                        "daily_theme": "Welcome and Orientation",
                        "emotional_stage": "excitement",
                        "sessions": [
                            {
                                "session_id": "s1_d1",
                                "day_number": 1,
                                "slot": "morning",
                                "theme": "Introduction",
                                "total_duration_minutes": 15,
                                "activities": []
                            }
                        ]
                    }
                ]
            }
        ]
    }


@pytest.fixture
def sample_module_list():
    """Пример списка модулей для оркестрации."""
    return [
        "psychoeducation_anxiety",
        "breathing_basics",
        "thought_awareness",
        "cognitive_restructuring",
        "behavioral_activation",
        "exposure_gentle"
    ]


@pytest.fixture
def orchestration_patterns_db():
    """Фикстура базы данных паттернов оркестрации."""
    return OrchestrationPatternsDatabase()


@pytest.fixture
def emotional_curve_db():
    """Фикстура базы данных эмоциональной кривой."""
    return EmotionalCurveDatabase()


@pytest.fixture
def module_load_db():
    """Фикстура базы данных нагрузки модулей."""
    return ModuleLoadDatabase()


@pytest.fixture
def transition_patterns_db():
    """Фикстура базы данных паттернов переходов."""
    return TransitionPatternsDatabase()
