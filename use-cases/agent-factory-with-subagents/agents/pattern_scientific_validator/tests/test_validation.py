"""
Тесты валидации моделей и данных Pattern Scientific Validator Agent.
"""

import pytest
from pydantic import ValidationError
from ..models import (
    TechniqueValidation,
    SafetyCheck,
    EthicalReview,
    ValidationReport,
    ResearchStudy,
    EffectivenessMetrics,
    AdaptationValidation,
    EvidenceLevel,
    SafetyRating,
    ValidationStatus
)


def test_technique_validation_model_valid():
    """
    Тест создания валидной модели TechniqueValidation.
    """
    validation = TechniqueValidation(
        technique_name="Cognitive Restructuring",
        evidence_level=EvidenceLevel.META_ANALYSIS,
        validation_status=ValidationStatus.VALIDATED,
        supporting_research=[
            ResearchStudy(
                authors=["Hofmann et al."],
                year=2012,
                title="Effect of CBT",
                study_type="Meta-analysis",
                sample_size=16000,
                effect_size=0.75,
                findings="Large effect for depression"
            )
        ],
        theoretical_foundation="Cognitive Behavioral Therapy",
        target_conditions=["depression", "anxiety"],
        safety_rating=SafetyRating.SAFE,
        contraindications=["active psychosis"],
        self_help_adaptation_notes="Effective with guidance"
    )

    assert validation.technique_name == "Cognitive Restructuring"
    assert validation.evidence_level == EvidenceLevel.META_ANALYSIS
    assert validation.validation_status == ValidationStatus.VALIDATED
    assert len(validation.supporting_research) == 1
    assert validation.supporting_research[0].effect_size == 0.75


def test_technique_validation_model_invalid():
    """
    Тест создания невалидной модели - failure case.
    """
    with pytest.raises(ValidationError):
        TechniqueValidation(
            technique_name="",  # Пустое имя - невалидно
            evidence_level="invalid_level",  # Невалидный уровень
            validation_status="invalid_status"
        )


def test_safety_check_model_valid():
    """
    Тест создания валидной модели SafetyCheck.
    """
    safety = SafetyCheck(
        module_id="test_001",
        safety_rating=SafetyRating.SAFE,
        potential_risks=["Minor discomfort"],
        risk_mitigation=["Start slowly", "Use grounding techniques"],
        contraindications=["Active trauma", "Severe symptoms"],
        warning_signs=["Increased distress", "Dissociation"],
        emergency_protocol="Contact crisis hotline if distressed"
    )

    assert safety.module_id == "test_001"
    assert safety.safety_rating == SafetyRating.SAFE
    assert len(safety.contraindications) == 2
    assert "Active trauma" in safety.contraindications


def test_safety_check_requires_supervision():
    """
    Тест SafetyCheck для техники требующей надзора - edge case.
    """
    safety = SafetyCheck(
        module_id="test_002",
        safety_rating=SafetyRating.REQUIRES_SUPERVISION,
        potential_risks=["Emotional overwhelm", "Re-traumatization"],
        risk_mitigation=["Professional guidance required"],
        contraindications=["PTSD", "Recent trauma"],
        warning_signs=["Flashbacks", "Panic"],
        emergency_protocol="Seek immediate professional help"
    )

    assert safety.safety_rating == SafetyRating.REQUIRES_SUPERVISION
    assert len(safety.potential_risks) > 0


def test_ethical_review_model_valid():
    """
    Тест создания валидной модели EthicalReview.
    """
    review = EthicalReview(
        module_id="test_003",
        ethical_concerns=["Minor overclaiming"],
        informed_consent_adequacy=True,
        autonomy_respected=True,
        beneficence=True,
        non_maleficence=True,
        justice=True,
        ethical_approval=True,
        notes="Generally ethical with minor improvements needed"
    )

    assert review.module_id == "test_003"
    assert review.ethical_approval is True
    assert review.autonomy_respected is True


def test_ethical_review_not_approved():
    """
    Тест EthicalReview для неодобренного модуля.
    """
    review = EthicalReview(
        module_id="test_004",
        ethical_concerns=["Overclaiming efficacy", "Inadequate informed consent"],
        informed_consent_adequacy=False,
        autonomy_respected=False,
        beneficence=False,
        non_maleficence=True,
        justice=True,
        ethical_approval=False,
        notes="Requires significant revision"
    )

    assert review.ethical_approval is False
    assert len(review.ethical_concerns) > 0


def test_effectiveness_metrics_model():
    """
    Тест создания модели EffectivenessMetrics.
    """
    metrics = EffectivenessMetrics(
        technique_name="Mindfulness",
        primary_outcome="Reduced anxiety",
        measurement_tool="GAD-7",
        expected_effect_size=0.55,
        time_to_effect="4-8 weeks",
        success_indicators=["20% reduction in GAD-7", "Improved awareness"]
    )

    assert metrics.technique_name == "Mindfulness"
    assert metrics.expected_effect_size == 0.55
    assert len(metrics.success_indicators) == 2


def test_adaptation_validation_model():
    """
    Тест создания модели AdaptationValidation.
    """
    adaptation = AdaptationValidation(
        original_protocol="Therapist-guided exposure",
        adapted_protocol="Self-paced gentle exposure",
        fidelity_maintained=True,
        key_elements_preserved=["Hierarchy", "Gradual exposure", "Repeated practice"],
        modifications_made=["Shorter duration", "Added escape option"],
        expected_efficacy_change=-0.4,
        safety_improvements=["Added stopping rules", "Removed intense exposures"],
        validation_decision=ValidationStatus.VALIDATED,
        notes="Safe for self-help with reduced efficacy"
    )

    assert adaptation.fidelity_maintained is True
    assert len(adaptation.key_elements_preserved) == 3
    assert adaptation.expected_efficacy_change == -0.4


def test_validation_report_complete():
    """
    Тест создания полного ValidationReport.
    """
    report = ValidationReport(
        module_id="test_005",
        module_name="Complete Test Module",
        technique_validations=[
            TechniqueValidation(
                technique_name="Test Technique",
                evidence_level=EvidenceLevel.RCT,
                validation_status=ValidationStatus.VALIDATED,
                supporting_research=[],
                theoretical_foundation="Test foundation",
                target_conditions=["test"],
                safety_rating=SafetyRating.SAFE,
                contraindications=[],
                self_help_adaptation_notes=""
            )
        ],
        safety_check=SafetyCheck(
            module_id="test_005",
            safety_rating=SafetyRating.SAFE,
            potential_risks=[],
            risk_mitigation=[],
            contraindications=[],
            warning_signs=[],
            emergency_protocol=""
        ),
        ethical_review=EthicalReview(
            module_id="test_005",
            ethical_concerns=[],
            informed_consent_adequacy=True,
            autonomy_respected=True,
            beneficence=True,
            non_maleficence=True,
            justice=True,
            ethical_approval=True,
            notes=""
        ),
        effectiveness_metrics=[],
        adaptation_validations=[],
        overall_validation_status=ValidationStatus.VALIDATED,
        overall_evidence_level=EvidenceLevel.RCT,
        overall_safety_rating=SafetyRating.SAFE,
        recommendations=["Continue as is"],
        required_changes=[],
        approval_notes="Approved for use"
    )

    assert report.module_id == "test_005"
    assert report.overall_validation_status == ValidationStatus.VALIDATED
    assert len(report.technique_validations) == 1


def test_research_study_model():
    """
    Тест создания модели ResearchStudy.
    """
    study = ResearchStudy(
        authors=["Smith et al."],
        year=2020,
        title="Study of effectiveness",
        study_type="RCT",
        sample_size=500,
        effect_size=0.6,
        findings="Moderate effect observed"
    )

    assert len(study.authors) == 1
    assert study.year == 2020
    assert study.sample_size == 500


def test_evidence_level_enum():
    """
    Тест enum EvidenceLevel.
    """
    assert EvidenceLevel.META_ANALYSIS.value == "meta-analysis"
    assert EvidenceLevel.RCT.value == "rct"
    assert EvidenceLevel.EXPERT_OPINION.value == "expert-opinion"


def test_safety_rating_enum():
    """
    Тест enum SafetyRating.
    """
    assert SafetyRating.SAFE.value == "safe"
    assert SafetyRating.CAUTION.value == "caution"
    assert SafetyRating.REQUIRES_SUPERVISION.value == "requires-supervision"


def test_validation_status_enum():
    """
    Тест enum ValidationStatus.
    """
    assert ValidationStatus.VALIDATED.value == "validated"
    assert ValidationStatus.NEEDS_REVISION.value == "needs-revision"
    assert ValidationStatus.NOT_VALIDATED.value == "not-validated"
