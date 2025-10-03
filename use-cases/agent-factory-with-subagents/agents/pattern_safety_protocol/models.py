"""
Модели данных для Pattern Safety Protocol Agent
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class RiskLevel(str, Enum):
    """Уровни риска для пользователя."""
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(str, Enum):
    """Категории рисков."""
    SUICIDAL = "suicidal"
    SELF_HARM = "self_harm"
    CRISIS = "crisis"
    TRAUMA_TRIGGER = "trauma_trigger"
    PSYCHOSIS = "psychosis"
    SUBSTANCE_ABUSE = "substance_abuse"
    MEDICAL_CONTRAINDICATION = "medical_contraindication"
    EMOTIONAL_OVERLOAD = "emotional_overload"


class ContraindicationType(str, Enum):
    """Типы противопоказаний."""
    ABSOLUTE = "absolute"  # Абсолютное противопоказание - запрет техники
    RELATIVE = "relative"  # Относительное - адаптация необходима
    TEMPORARY = "temporary"  # Временное - ждать стабилизации


class EscalationAction(str, Enum):
    """Действия эскалации при обнаружении риска."""
    IMMEDIATE_REFERRAL = "immediate_referral"  # Немедленное направление к специалисту
    CRISIS_RESOURCES = "crisis_resources"  # Предоставление кризисных ресурсов
    PAUSE_PROGRAM = "pause_program"  # Приостановка программы
    ADAPT_TECHNIQUE = "adapt_technique"  # Адаптация техники
    MONITOR_CLOSELY = "monitor_closely"  # Усиленный мониторинг
    EMERGENCY_PROTOCOL = "emergency_protocol"  # Экстренный протокол


class RiskAssessment(BaseModel):
    """Оценка риска для пользователя."""

    assessment_id: str = Field(..., description="ID оценки риска")
    user_id: Optional[str] = Field(None, description="ID пользователя")
    timestamp: datetime = Field(default_factory=datetime.now, description="Время оценки")

    # Оценка уровня риска
    overall_risk_level: RiskLevel = Field(..., description="Общий уровень риска")
    risk_categories: List[RiskCategory] = Field(default_factory=list, description="Выявленные категории рисков")
    risk_indicators: Dict[str, Any] = Field(default_factory=dict, description="Конкретные индикаторы риска")

    # Источники данных для оценки
    data_sources: List[str] = Field(default_factory=list, description="Источники данных (feedback, behavior, responses)")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Уверенность в оценке (0-1)")

    # Рекомендации
    recommended_actions: List[EscalationAction] = Field(default_factory=list, description="Рекомендуемые действия")
    requires_immediate_action: bool = Field(default=False, description="Требуется немедленное действие")
    explanation: str = Field(..., description="Объяснение оценки риска")


class Contraindication(BaseModel):
    """Противопоказание для психологической техники."""

    contraindication_id: str = Field(..., description="ID противопоказания")
    technique_name: str = Field(..., description="Название техники")
    contraindication_type: ContraindicationType = Field(..., description="Тип противопоказания")

    # Описание противопоказания
    condition: str = Field(..., description="Медицинское/психологическое состояние")
    risk_description: str = Field(..., description="Описание возможного вреда")
    alternative_approach: Optional[str] = Field(None, description="Альтернативный подход")

    # Детали адаптации
    can_be_adapted: bool = Field(default=False, description="Можно ли адаптировать технику")
    adaptation_instructions: Optional[str] = Field(None, description="Инструкции по адаптации")
    required_supervision: bool = Field(default=False, description="Требуется ли наблюдение специалиста")


class PharmacologicalInteraction(BaseModel):
    """Взаимодействие психотехник с медикаментами."""

    interaction_id: str = Field(..., description="ID взаимодействия")
    medication_class: str = Field(..., description="Класс медикаментов")
    medication_examples: List[str] = Field(default_factory=list, description="Примеры препаратов")

    # Взаимодействие
    affected_techniques: List[str] = Field(default_factory=list, description="Затрагиваемые техники")
    interaction_type: str = Field(..., description="Тип взаимодействия (усиление/ослабление/побочный эффект)")
    severity: RiskLevel = Field(..., description="Серьезность взаимодействия")

    # Рекомендации
    recommendation: str = Field(..., description="Рекомендация по управлению взаимодействием")
    requires_medical_consultation: bool = Field(default=False, description="Требуется консультация врача")


class CrisisIndicator(BaseModel):
    """Индикатор кризисного состояния."""

    indicator_id: str = Field(..., description="ID индикатора")
    indicator_type: RiskCategory = Field(..., description="Тип индикатора")
    detection_pattern: str = Field(..., description="Паттерн для детекции")

    # Критичность
    severity: RiskLevel = Field(..., description="Уровень серьезности")
    requires_immediate_action: bool = Field(default=False, description="Требуется немедленное действие")

    # Ответные действия
    escalation_actions: List[EscalationAction] = Field(default_factory=list, description="Действия эскалации")
    response_script: str = Field(..., description="Скрипт ответа пользователю")
    crisis_resources: List[str] = Field(default_factory=list, description="Кризисные ресурсы помощи")


class SafetyProtocol(BaseModel):
    """Протокол безопасности для конкретной ситуации."""

    protocol_id: str = Field(..., description="ID протокола")
    protocol_name: str = Field(..., description="Название протокола")
    trigger_conditions: List[str] = Field(default_factory=list, description="Условия активации")

    # Шаги протокола
    immediate_actions: List[str] = Field(default_factory=list, description="Немедленные действия")
    communication_script: str = Field(..., description="Скрипт коммуникации с пользователем")
    resource_links: List[Dict[str, str]] = Field(default_factory=list, description="Ссылки на ресурсы помощи")

    # Follow-up
    follow_up_required: bool = Field(default=False, description="Требуется ли последующее наблюдение")
    follow_up_timeline: Optional[str] = Field(None, description="Временные рамки follow-up")
    escalation_path: List[str] = Field(default_factory=list, description="Путь эскалации помощи")


class VulnerableGroupProfile(BaseModel):
    """Профиль уязвимой группы пользователей."""

    group_id: str = Field(..., description="ID группы")
    group_name: str = Field(..., description="Название группы")
    vulnerability_factors: List[str] = Field(default_factory=list, description="Факторы уязвимости")

    # Адаптации
    required_modifications: List[str] = Field(default_factory=list, description="Необходимые модификации программы")
    contraindicated_techniques: List[str] = Field(default_factory=list, description="Противопоказанные техники")
    recommended_alternatives: List[str] = Field(default_factory=list, description="Рекомендуемые альтернативы")

    # Мониторинг
    monitoring_frequency: str = Field(..., description="Частота мониторинга")
    red_flags: List[str] = Field(default_factory=list, description="Красные флаги для данной группы")


class SafetyCheckResult(BaseModel):
    """Результат проверки безопасности."""

    check_id: str = Field(..., description="ID проверки")
    timestamp: datetime = Field(default_factory=datetime.now, description="Время проверки")

    # Результаты
    is_safe: bool = Field(..., description="Безопасно ли продолжать")
    risk_assessment: RiskAssessment = Field(..., description="Оценка риска")
    detected_contraindications: List[Contraindication] = Field(default_factory=list, description="Обнаруженные противопоказания")

    # Действия
    required_actions: List[EscalationAction] = Field(default_factory=list, description="Требуемые действия")
    safety_message: str = Field(..., description="Сообщение о безопасности для пользователя")
    allow_continuation: bool = Field(default=True, description="Разрешить продолжение программы")


__all__ = [
    "RiskLevel",
    "RiskCategory",
    "ContraindicationType",
    "EscalationAction",
    "RiskAssessment",
    "Contraindication",
    "PharmacologicalInteraction",
    "CrisisIndicator",
    "SafetyProtocol",
    "VulnerableGroupProfile",
    "SafetyCheckResult"
]
