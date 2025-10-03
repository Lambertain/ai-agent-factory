"""
Pydantic модели для Pattern Scientific Validator Agent.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import uuid


class EvidenceLevel(str, Enum):
    """Уровни доказательности (evidence-based)."""
    META_ANALYSIS = "meta_analysis"  # Мета-анализы и систематические обзоры
    RCT = "rct"  # Randomized Controlled Trials
    COHORT_STUDY = "cohort_study"  # Когортные исследования
    CASE_CONTROL = "case_control"  # Исследования случай-контроль
    EXPERT_OPINION = "expert_opinion"  # Экспертное мнение
    NOT_VALIDATED = "not_validated"  # Не валидировано


class SafetyRating(str, Enum):
    """Оценка безопасности."""
    SAFE = "safe"  # Безопасно для самостоятельного применения
    CAUTION = "caution"  # Требует осторожности
    CONTRAINDICATED = "contraindicated"  # Противопоказано для определенных групп
    REQUIRES_PROFESSIONAL = "requires_professional"  # Требует профессионального надзора


class ValidationStatus(str, Enum):
    """Статус валидации."""
    VALIDATED = "validated"  # Валидирован и одобрен
    NEEDS_REVISION = "needs_revision"  # Требует доработки
    REJECTED = "rejected"  # Отклонен
    PENDING_REVIEW = "pending_review"  # Ожидает проверки


class ResearchStudy(BaseModel):
    """Научное исследование."""
    study_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    authors: List[str]
    year: int
    journal: str
    doi: Optional[str] = None
    evidence_level: EvidenceLevel
    sample_size: Optional[int] = None
    effect_size: Optional[float] = None  # Cohen's d или другая метрика
    findings_summary: str
    limitations: List[str]
    relevance_to_technique: str


class TechniqueValidation(BaseModel):
    """Валидация техники."""
    validation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    technique_name: str
    technique_description: str
    validation_status: ValidationStatus
    evidence_level: EvidenceLevel
    supporting_research: List[ResearchStudy]
    theoretical_foundation: str
    efficacy_rate: Optional[float] = None  # 0-1, если известно
    safety_rating: SafetyRating
    contraindications: List[str]
    target_conditions: List[str]  # Для каких состояний эффективна
    limitations: List[str]
    adaptation_notes: str  # Как адаптирована для самопомощи


class SafetyCheck(BaseModel):
    """Проверка безопасности."""
    check_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    module_id: str
    safety_rating: SafetyRating
    potential_risks: List[str]
    risk_mitigation: List[str]  # Как риски минимизированы
    contraindications: List[str]
    warning_signs: List[str]  # Признаки что нужна профессиональная помощь
    emergency_protocol: str


class EthicalReview(BaseModel):
    """Этическая проверка."""
    review_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    module_id: str
    ethical_concerns: List[str]
    informed_consent_adequacy: bool
    autonomy_respected: bool  # Уважение автономии пользователя
    beneficence: bool  # Принцип благодеяния
    non_maleficence: bool  # Принцип не навреди
    justice: bool  # Принцип справедливости
    ethical_approval: bool
    notes: str


class EffectivenessMetrics(BaseModel):
    """Метрики эффективности."""
    metrics_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    technique_name: str
    primary_outcome: str
    measurement_method: str
    expected_effect_size: str  # small, medium, large
    time_to_effect: str  # Когда ожидать результаты
    success_indicators: List[str]
    failure_indicators: List[str]


class AdaptationValidation(BaseModel):
    """Валидация адаптации для самопомощи."""
    adaptation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_protocol: str
    adapted_protocol: str
    adaptation_rationale: str
    fidelity_maintained: bool  # Сохранена ли суть техники
    key_elements_preserved: List[str]
    modifications_made: List[str]
    expected_efficacy_change: str  # Как изменится эффективность


class ValidationReport(BaseModel):
    """Полный отчет о валидации модуля."""
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    module_id: str
    module_name: str
    validation_date: datetime = Field(default_factory=datetime.now)
    validator_name: str = "Pattern Scientific Validator"

    technique_validations: List[TechniqueValidation]
    safety_check: SafetyCheck
    ethical_review: EthicalReview
    effectiveness_metrics: List[EffectivenessMetrics]
    adaptation_validations: List[AdaptationValidation]

    overall_validation_status: ValidationStatus
    overall_evidence_level: EvidenceLevel
    overall_safety_rating: SafetyRating

    recommendations: List[str]
    required_changes: List[str]
    approval_notes: str


class LimitationsDisclosure(BaseModel):
    """Раскрытие ограничений подхода."""
    disclosure_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    technique_name: str
    known_limitations: List[str]
    conditions_where_less_effective: List[str]
    populations_excluded_from_research: List[str]
    generalizability_concerns: List[str]
    confidence_level: str  # high, moderate, low
    disclosure_text: str  # Что сообщать пользователю


__all__ = [
    "EvidenceLevel",
    "SafetyRating",
    "ValidationStatus",
    "ResearchStudy",
    "TechniqueValidation",
    "SafetyCheck",
    "EthicalReview",
    "EffectivenessMetrics",
    "AdaptationValidation",
    "ValidationReport",
    "LimitationsDisclosure"
]
