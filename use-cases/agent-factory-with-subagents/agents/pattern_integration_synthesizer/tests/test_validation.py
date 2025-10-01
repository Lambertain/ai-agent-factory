"""
Тесты для валидации Pydantic моделей Pattern Integration Synthesizer.
"""

import pytest
from pydantic import ValidationError
from datetime import datetime
from ..models import (
    PhaseType,
    SessionSlot,
    ActivityType,
    EmotionalCurveStage,
    SynergyLevel,
    ModuleReference,
    Activity,
    Session,
    Day,
    Phase,
    Program,
    ModuleSynergy,
    ResistancePoint,
    EmotionalCurvePoint,
    ModuleSequence,
    IntegrationPlan,
    DayAnalysis,
    PhaseAnalysis,
    ProgramAnalysis,
    IntegrationReport
)


# ===== ТЕСТЫ ENUMS =====

def test_phase_type_enum():
    """Тест PhaseType enum."""
    assert PhaseType.BEGINNING == "beginning"
    assert PhaseType.DEVELOPMENT == "development"
    assert PhaseType.INTEGRATION == "integration"


def test_session_slot_enum():
    """Тест SessionSlot enum."""
    assert SessionSlot.MORNING == "morning"
    assert SessionSlot.AFTERNOON == "afternoon"
    assert SessionSlot.EVENING == "evening"


def test_emotional_curve_stage_enum():
    """Тест EmotionalCurveStage enum."""
    assert EmotionalCurveStage.EXCITEMENT == "excitement"
    assert EmotionalCurveStage.RESISTANCE == "resistance"
    assert EmotionalCurveStage.BREAKTHROUGH == "breakthrough"
    assert EmotionalCurveStage.INTEGRATION == "integration"
    assert EmotionalCurveStage.MASTERY == "mastery"


def test_synergy_level_enum():
    """Тест SynergyLevel enum."""
    assert SynergyLevel.HIGH == "high"
    assert SynergyLevel.MEDIUM == "medium"
    assert SynergyLevel.LOW == "low"
    assert SynergyLevel.CONFLICTING == "conflicting"


# ===== ТЕСТЫ БАЗОВЫХ МОДЕЛЕЙ =====

def test_module_reference_valid():
    """Тест создания валидного ModuleReference."""
    module = ModuleReference(
        module_id="mod_001",
        module_name="Test Module",
        module_type="technique",
        version="1.0.0",
        duration_minutes=15
    )

    assert module.module_id == "mod_001"
    assert module.duration_minutes == 15


def test_activity_valid():
    """Тест создания валидной Activity."""
    module = ModuleReference(
        module_id="mod_001",
        module_name="Test Module",
        module_type="technique",
        duration_minutes=15
    )

    activity = Activity(
        activity_id="act_001",
        activity_type=ActivityType.TECHNIQUE,
        module=module,
        order=1
    )

    assert activity.activity_id == "act_001"
    assert activity.order == 1


def test_session_valid():
    """Тест создания валидной Session."""
    module = ModuleReference(
        module_id="mod_001",
        module_name="Test Module",
        module_type="technique",
        duration_minutes=15
    )

    activity = Activity(
        activity_id="act_001",
        activity_type=ActivityType.TECHNIQUE,
        module=module,
        order=1
    )

    session = Session(
        session_id="ses_001",
        day_number=1,
        slot=SessionSlot.MORNING,
        activities=[activity],
        total_duration_minutes=15,
        theme="Introduction"
    )

    assert session.session_id == "ses_001"
    assert len(session.activities) == 1


def test_day_valid():
    """Тест создания валидного Day."""
    day = Day(
        day_number=1,
        phase=PhaseType.BEGINNING,
        sessions=[],
        daily_theme="Welcome",
        emotional_stage=EmotionalCurveStage.EXCITEMENT
    )

    assert day.day_number == 1
    assert day.phase == PhaseType.BEGINNING


def test_phase_valid():
    """Тест создания валидной Phase."""
    phase = Phase(
        phase_type=PhaseType.BEGINNING,
        phase_name="Foundation",
        days=[],
        phase_goals=["build awareness"],
        duration_days=7
    )

    assert phase.phase_type == PhaseType.BEGINNING
    assert phase.duration_days == 7


def test_program_valid():
    """Тест создания валидной Program."""
    program = Program(
        program_id="prog_001",
        program_name="Test Program",
        total_days=21,
        phases=[],
        target_conditions=["anxiety"],
        overall_goals=["reduce anxiety"]
    )

    assert program.program_id == "prog_001"
    assert program.total_days == 21


# ===== ТЕСТЫ АНАЛИЗ МОДЕЛЕЙ =====

def test_module_synergy_valid():
    """Тест создания валидного ModuleSynergy."""
    synergy = ModuleSynergy(
        module_a_id="mod_a",
        module_b_id="mod_b",
        synergy_level=SynergyLevel.HIGH,
        synergy_description="High synergy between modules",
        recommended_sequence="A then B",
        recommended_gap=1
    )

    assert synergy.synergy_level == SynergyLevel.HIGH
    assert synergy.recommended_gap == 1


def test_resistance_point_valid():
    """Тест создания валидного ResistancePoint."""
    resistance = ResistancePoint(
        day_number=5,
        session_slot=SessionSlot.MORNING,
        resistance_type="novelty_wearoff",
        severity="high",
        description="First dropout point",
        mitigation_strategies=["quick wins", "support"],
        support_modules=["motivational_content"]
    )

    assert resistance.day_number == 5
    assert resistance.severity == "high"


def test_emotional_curve_point_valid():
    """Тест создания валидного EmotionalCurvePoint."""
    curve_point = EmotionalCurvePoint(
        day_number=1,
        emotional_stage=EmotionalCurveStage.EXCITEMENT,
        energy_level=9,
        motivation_level=10,
        recommended_intensity="light",
        notes="High energy start"
    )

    assert curve_point.energy_level == 9
    assert curve_point.motivation_level == 10


def test_module_sequence_valid():
    """Тест создания валидного ModuleSequence."""
    sequence = ModuleSequence(
        sequence=["mod_1", "mod_2", "mod_3"],
        rationale="Progressive intensity pattern",
        cumulative_effects=["builds awareness", "develops skills"],
        synergy_score=0.85
    )

    assert len(sequence.sequence) == 3
    assert 0 <= sequence.synergy_score <= 1


# ===== ТЕСТЫ ОТЧЕТОВ =====

def test_day_analysis_valid():
    """Тест создания валидного DayAnalysis."""
    analysis = DayAnalysis(
        day_number=1,
        phase=PhaseType.BEGINNING,
        emotional_stage=EmotionalCurveStage.EXCITEMENT,
        total_load_minutes=30,
        module_count=2,
        synergy_rating=0.8,
        potential_issues=["none"],
        recommendations=["maintain pace"]
    )

    assert analysis.day_number == 1
    assert 0 <= analysis.synergy_rating <= 1


def test_phase_analysis_valid():
    """Тест создания валидного PhaseAnalysis."""
    analysis = PhaseAnalysis(
        phase_type=PhaseType.BEGINNING,
        duration_days=7,
        total_modules=14,
        average_daily_load=30,
        synergy_score=0.75,
        coherence_score=0.80,
        issues=[],
        recommendations=["good structure"]
    )

    assert analysis.duration_days == 7
    assert 0 <= analysis.synergy_score <= 1


def test_program_analysis_valid():
    """Тест создания валидного ProgramAnalysis."""
    analysis = ProgramAnalysis(
        program_id="prog_001",
        program_name="Test Program",
        total_days=21,
        phase_analyses=[],
        day_analyses=[],
        overall_synergy_score=0.80,
        overall_coherence_score=0.85,
        critical_issues=[],
        optimization_opportunities=["good program"]
    )

    assert analysis.total_days == 21
    assert 0 <= analysis.overall_synergy_score <= 1


# ===== ТЕСТЫ VALIDATION ERRORS =====

def test_emotional_curve_point_invalid_energy():
    """Тест валидации некорректного уровня энергии (должен быть 1-10)."""
    # Pydantic может не иметь встроенных constraints, но можно добавить
    # Для данного примера просто проверяем что модель создается
    with pytest.raises(ValidationError):
        EmotionalCurvePoint(
            day_number=1,
            emotional_stage=EmotionalCurveStage.EXCITEMENT,
            energy_level=15,  # Некорректно: должно быть 1-10
            motivation_level=10,
            recommended_intensity="light",
            notes="Test"
        )


def test_module_sequence_invalid_synergy_score():
    """Тест валидации некорректного synergy_score (должен быть 0-1)."""
    # synergy_score должен быть float в диапазоне 0-1
    # Если нет валидатора, можно добавить в модель
    # Для примера проверяем что некорректное значение вызывает ошибку
    with pytest.raises((ValidationError, ValueError)):
        ModuleSequence(
            sequence=["mod_1"],
            rationale="Test",
            cumulative_effects=["test"],
            synergy_score=1.5  # Некорректно: должно быть 0-1
        )
