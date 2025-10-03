"""
Инструменты для Pattern Scientific Validator Agent.
"""

from pydantic_ai import RunContext
from typing import Dict, Any, List
import json

from .dependencies import PatternScientificValidatorDependencies
from .models import (
    TechniqueValidation,
    SafetyCheck,
    EthicalReview,
    ValidationReport,
    EvidenceLevel,
    SafetyRating,
    ValidationStatus,
    ResearchStudy,
    EffectivenessMetrics,
    AdaptationValidation,
    LimitationsDisclosure
)


async def validate_technique_efficacy(
    ctx: RunContext[PatternScientificValidatorDependencies],
    technique_name: str,
    technique_description: str,
    target_conditions: List[str]
) -> TechniqueValidation:
    """
    Валидирует эффективность психологической техники на основе научных данных.

    Args:
        ctx: Контекст выполнения с зависимостями
        technique_name: Название техники
        technique_description: Описание техники
        target_conditions: Список целевых состояний (depression, anxiety, etc.)

    Returns:
        TechniqueValidation с оценкой доказательности и рекомендациями
    """
    deps = ctx.deps
    research_db = deps.research_database

    # Анализ техники и поиск в базе исследований
    validation_status = ValidationStatus.PENDING_REVIEW
    evidence_level = EvidenceLevel.NOT_VALIDATED
    supporting_research = []
    theoretical_foundation = ""
    safety_rating = SafetyRating.SAFE
    contraindications = []
    limitations = []
    adaptation_notes = ""

    # Проверка CBT техник
    if any(keyword in technique_name.lower() for keyword in ["cognitive", "restructuring", "reframing", "thought"]):
        # CBT техники
        cbt_data = research_db.cbt_research
        meta_analysis = cbt_data["meta_analyses"][0]  # Hofmann et al., 2012

        supporting_research.append(ResearchStudy(
            title=meta_analysis["title"],
            authors=meta_analysis["authors"],
            year=meta_analysis["year"],
            journal=meta_analysis["journal"],
            evidence_level=EvidenceLevel.META_ANALYSIS,
            sample_size=meta_analysis["sample_size"],
            effect_size=meta_analysis["effect_size"],
            findings_summary=meta_analysis["findings"],
            limitations=["Effect size ниже в самопомощи"],
            relevance_to_technique="Прямая релевантность - CBT техника"
        ))

        evidence_level = EvidenceLevel.META_ANALYSIS
        validation_status = ValidationStatus.VALIDATED
        theoretical_foundation = "Cognitive Behavioral Therapy - хорошо валидирован (мета-анализы)"
        adaptation_notes = f"Эффективность в самопомощи: d={meta_analysis.get('self_help_efficacy', 0.60)}"

    # Проверка Mindfulness техник
    elif any(keyword in technique_name.lower() for keyword in ["mindfulness", "meditation", "body scan", "awareness"]):
        mindfulness_data = research_db.mindfulness_research
        meta_analysis = mindfulness_data["meta_analyses"][0]  # Khoury et al., 2013

        supporting_research.append(ResearchStudy(
            title=meta_analysis["title"],
            authors=meta_analysis["authors"],
            year=meta_analysis["year"],
            journal=meta_analysis["journal"],
            evidence_level=EvidenceLevel.META_ANALYSIS,
            sample_size=meta_analysis["sample_size"],
            effect_size=meta_analysis["effect_size"],
            findings_summary=meta_analysis["findings"],
            limitations=["Medium effect size"],
            relevance_to_technique="Mindfulness-based техника"
        ))

        evidence_level = EvidenceLevel.META_ANALYSIS
        validation_status = ValidationStatus.VALIDATED
        theoretical_foundation = "Mindfulness-Based Interventions - мета-анализ поддерживает"
        adaptation_notes = "Хорошо адаптируется для самопомощи"

        # Contraindications для mindfulness
        if "intensive" in technique_description.lower() or "deep" in technique_description.lower():
            contraindications.append("Активный психоз")
            contraindications.append("Severe dissociation")
            safety_rating = SafetyRating.CAUTION

    # Проверка NLP техник
    elif any(keyword in technique_name.lower() for keyword in ["nlp", "anchoring", "submodalities", "reframing"]):
        nlp_data = research_db.nlp_research

        if "reframing" in technique_name.lower():
            # Reframing похож на cognitive restructuring из CBT
            evidence_level = EvidenceLevel.EXPERT_OPINION
            validation_status = ValidationStatus.VALIDATED
            theoretical_foundation = "Overlap с CBT cognitive restructuring (валидирован)"
            supporting_research.append(ResearchStudy(
                title="NLP Reframing as Cognitive Restructuring",
                authors=["Theoretical Framework"],
                year=2020,
                journal="Theoretical Analysis",
                evidence_level=EvidenceLevel.EXPERT_OPINION,
                findings_summary="Механизм похож на CBT техники",
                limitations=["Прямых RCT нет", "Основано на теоретическом overlap"],
                relevance_to_technique="Теоретическая связь с валидированными CBT техниками"
            ))
            adaptation_notes = "Безопасен, но эффективность не доказана на уровне RCT"
        else:
            # Другие NLP техники
            evidence_level = EvidenceLevel.NOT_VALIDATED
            validation_status = ValidationStatus.NEEDS_REVISION
            theoretical_foundation = "Ограниченная эмпирическая поддержка"
            limitations.extend(nlp_data["concerns"])
            adaptation_notes = "Требуется четкое раскрытие ограничений доказательной базы"

    # Проверка ACT техник
    elif any(keyword in technique_name.lower() for keyword in ["acceptance", "commitment", "values", "defusion"]):
        act_data = research_db.act_research
        meta_analysis = act_data["meta_analyses"][0]  # A-Tjak et al., 2015

        supporting_research.append(ResearchStudy(
            title=meta_analysis["title"],
            authors=meta_analysis["authors"],
            year=meta_analysis["year"],
            journal=meta_analysis["journal"],
            evidence_level=EvidenceLevel.META_ANALYSIS,
            sample_size=meta_analysis["sample_size"],
            effect_size=meta_analysis["effect_size"],
            findings_summary=meta_analysis["findings"],
            limitations=["Medium effect size"],
            relevance_to_technique="ACT техника"
        ))

        evidence_level = EvidenceLevel.META_ANALYSIS
        validation_status = ValidationStatus.VALIDATED
        theoretical_foundation = "Acceptance and Commitment Therapy - мета-анализ"
        adaptation_notes = "Хорошая теоретическая база и empirical support"

    # Общие ограничения для самопомощи
    limitations.append("Эффективность в самопомощи обычно ниже чем с терапевтом")
    limitations.append("Требует мотивации и самодисциплины")

    return TechniqueValidation(
        technique_name=technique_name,
        technique_description=technique_description,
        validation_status=validation_status,
        evidence_level=evidence_level,
        supporting_research=supporting_research,
        theoretical_foundation=theoretical_foundation,
        safety_rating=safety_rating,
        contraindications=contraindications,
        target_conditions=target_conditions,
        limitations=limitations,
        adaptation_notes=adaptation_notes
    )


async def check_safety(
    ctx: RunContext[PatternScientificValidatorDependencies],
    module_id: str,
    module_content: str,
    techniques_used: List[str]
) -> SafetyCheck:
    """
    Проверяет безопасность модуля для самостоятельного использования.

    Args:
        ctx: Контекст выполнения
        module_id: ID модуля
        module_content: Содержание модуля
        techniques_used: Список используемых техник

    Returns:
        SafetyCheck с оценкой рисков и рекомендациями
    """
    deps = ctx.deps
    safety_db = deps.safety_protocols

    potential_risks = []
    risk_mitigation = []
    contraindications = []
    warning_signs = safety_db.warning_signs.copy()
    emergency_protocol = "При усилении симптомов - прекратить упражнения и обратиться к профессионалу"
    safety_rating = SafetyRating.SAFE

    # Анализ техник на риски
    for technique in techniques_used:
        technique_lower = technique.lower()

        # Проверка на intensive emotional work
        if any(keyword in technique_lower for keyword in ["deep", "intensive", "trauma", "regression"]):
            potential_risks.append("Интенсивная эмоциональная работа без надзора")
            contraindications.extend(safety_db.contraindications["severe_trauma"]["techniques_contraindicated"])
            safety_rating = SafetyRating.REQUIRES_PROFESSIONAL

        # Проверка на mindfulness risks
        if "mindfulness" in technique_lower or "meditation" in technique_lower:
            if "intensive" in technique_lower:
                potential_risks.append("Intensive mindfulness может вызвать диссоциацию")
                contraindications.extend(safety_db.contraindications["active_psychosis"]["techniques_contraindicated"])
                safety_rating = SafetyRating.CAUTION

    # Общие риски для самопомощи
    if not potential_risks:
        potential_risks.append("Минимальные риски при следовании инструкциям")

    # Mitigation strategies
    risk_mitigation.extend([
        "Четкие инструкции когда остановиться",
        "Информирование о пределах самопомощи",
        "Ресурсы профессиональной помощи",
        "Monitoring прогресса и ухудшений"
    ])

    # Общие contraindications
    if safety_rating == SafetyRating.SAFE:
        contraindications.extend([
            "Активные суицидальные мысли (требуется немедленная профессиональная помощь)",
            "Активный психоз",
            "Severe trauma без профессиональной поддержки"
        ])

    return SafetyCheck(
        module_id=module_id,
        safety_rating=safety_rating,
        potential_risks=potential_risks,
        risk_mitigation=risk_mitigation,
        contraindications=contraindications,
        warning_signs=warning_signs,
        emergency_protocol=emergency_protocol
    )


async def review_ethics(
    ctx: RunContext[PatternScientificValidatorDependencies],
    module_id: str,
    module_content: str,
    informed_consent_present: bool
) -> EthicalReview:
    """
    Проводит этическую проверку модуля.

    Args:
        ctx: Контекст выполнения
        module_id: ID модуля
        module_content: Содержание модуля
        informed_consent_present: Присутствует ли informed consent

    Returns:
        EthicalReview с оценкой этических аспектов
    """
    deps = ctx.deps
    ethics_db = deps.ethical_guidelines

    ethical_concerns = []

    # Проверка informed consent
    informed_consent_adequacy = informed_consent_present
    if not informed_consent_present:
        ethical_concerns.append("Отсутствует informed consent с описанием рисков и преимуществ")

    # Проверка принципов
    autonomy_respected = True
    if "must" in module_content.lower() or "обязан" in module_content.lower():
        autonomy_respected = False
        ethical_concerns.append("Формулировки могут нарушать автономию (используется 'must' вместо 'can')")

    beneficence = True  # Предполагаем благие намерения
    non_maleficence = True  # Если safety check прошел
    justice = True  # Доступность для всех

    # Проверка на overclaiming
    if any(word in module_content.lower() for word in ["гарантия", "100%", "навсегда", "guarantee"]):
        ethical_concerns.append("Overclaiming эффективности - нарушение принципа честности")
        beneficence = False

    ethical_approval = len(ethical_concerns) == 0

    notes = ""
    if ethical_approval:
        notes = "Модуль соответствует этическим стандартам"
    else:
        notes = f"Выявлено {len(ethical_concerns)} этических проблем - требуется revision"

    return EthicalReview(
        module_id=module_id,
        ethical_concerns=ethical_concerns,
        informed_consent_adequacy=informed_consent_adequacy,
        autonomy_respected=autonomy_respected,
        beneficence=beneficence,
        non_maleficence=non_maleficence,
        justice=justice,
        ethical_approval=ethical_approval,
        notes=notes
    )


async def validate_adaptation(
    ctx: RunContext[PatternScientificValidatorDependencies],
    original_protocol: str,
    adapted_protocol: str,
    key_elements: List[str]
) -> AdaptationValidation:
    """
    Валидирует адаптацию техники для самопомощи.

    Args:
        ctx: Контекст выполнения
        original_protocol: Оригинальный протокол
        adapted_protocol: Адаптированный протокол
        key_elements: Ключевые элементы техники

    Returns:
        AdaptationValidation с оценкой адаптации
    """
    deps = ctx.deps
    adaptation_db = deps.adaptation_standards

    # Анализ сохранения ключевых элементов
    key_elements_preserved = []
    modifications_made = []

    for element in key_elements:
        if element.lower() in adapted_protocol.lower():
            key_elements_preserved.append(element)
        else:
            modifications_made.append(f"Удален элемент: {element}")

    # Проверка fidelity
    fidelity_maintained = len(key_elements_preserved) >= len(key_elements) * 0.7  # Минимум 70% элементов

    # Определение изменений
    if len(adapted_protocol) < len(original_protocol) * 0.5:
        modifications_made.append("Значительное упрощение протокола")

    if not modifications_made:
        modifications_made.append("Упрощение языка, добавление примеров")

    # Оценка ожидаемого изменения эффективности
    if fidelity_maintained:
        expected_efficacy_change = "Небольшое снижение (10-20%) - типично для самопомощи"
    else:
        expected_efficacy_change = "Значительное снижение (>30%) - критические элементы утеряны"

    adaptation_rationale = "Адаптация для самостоятельного использования с сохранением core механизмов"

    return AdaptationValidation(
        original_protocol=original_protocol,
        adapted_protocol=adapted_protocol,
        adaptation_rationale=adaptation_rationale,
        fidelity_maintained=fidelity_maintained,
        key_elements_preserved=key_elements_preserved,
        modifications_made=modifications_made,
        expected_efficacy_change=expected_efficacy_change
    )


async def assess_effectiveness(
    ctx: RunContext[PatternScientificValidatorDependencies],
    technique_name: str,
    primary_outcome: str,
    expected_effect_size: str
) -> EffectivenessMetrics:
    """
    Оценивает метрики эффективности техники.

    Args:
        ctx: Контекст выполнения
        technique_name: Название техники
        primary_outcome: Основной outcome (снижение депрессии, тревожности, etc.)
        expected_effect_size: Ожидаемый размер эффекта (small, medium, large)

    Returns:
        EffectivenessMetrics с определением метрик измерения
    """
    deps = ctx.deps
    metrics_db = deps.effectiveness_metrics

    # Определение measurement method
    measurement_method = ""
    if "depression" in primary_outcome.lower() or "депресс" in primary_outcome.lower():
        measurement_method = "PHQ-9 (Patient Health Questionnaire-9) или BDI-II"
    elif "anxiety" in primary_outcome.lower() or "тревож" in primary_outcome.lower():
        measurement_method = "GAD-7 (Generalized Anxiety Disorder-7)"
    elif "wellbeing" in primary_outcome.lower() or "благополуч" in primary_outcome.lower():
        measurement_method = "WEMWBS (Warwick-Edinburgh Mental Wellbeing Scale)"
    else:
        measurement_method = "Self-report measures + behavioral indicators"

    # Определение времени до эффекта
    time_to_effect = ""
    if expected_effect_size == "large":
        time_to_effect = "2-4 недели регулярной практики"
    elif expected_effect_size == "medium":
        time_to_effect = "4-8 недель регулярной практики"
    else:
        time_to_effect = "8-12 недель регулярной практики"

    # Success indicators
    success_indicators = [
        f"Снижение {primary_outcome} на 20-30%",
        "Улучшение повседневного функционирования",
        "Положительная субъективная оценка пользователя",
        "Продолжение использования техники"
    ]

    # Failure indicators
    failure_indicators = [
        f"Отсутствие изменений в {primary_outcome} после {time_to_effect}",
        "Ухудшение симптомов",
        "Невозможность выполнять упражнения",
        "Появление негативных побочных эффектов"
    ]

    return EffectivenessMetrics(
        technique_name=technique_name,
        primary_outcome=primary_outcome,
        measurement_method=measurement_method,
        expected_effect_size=expected_effect_size,
        time_to_effect=time_to_effect,
        success_indicators=success_indicators,
        failure_indicators=failure_indicators
    )


async def search_agent_knowledge(
    ctx: RunContext[PatternScientificValidatorDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Ищет информацию в базе знаний агента через Archon RAG.

    Args:
        ctx: Контекст выполнения
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Строка с найденной информацией
    """
    deps = ctx.deps

    try:
        # Импорт MCP tools
        from agent_factory.mcp_integration.archon import search_knowledge_base

        # Поиск в knowledge base с тегами агента
        results = await search_knowledge_base(
            query=query,
            source_domain=deps.knowledge_domain,
            match_count=match_count
        )

        if results["success"] and results["results"]:
            formatted_results = []
            for result in results["results"]:
                formatted_results.append(
                    f"## {result.get('title', 'Результат')}\n{result.get('content', '')}"
                )
            return "\n\n".join(formatted_results)
        else:
            return "Информация не найдена в базе знаний"

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {str(e)}"


__all__ = [
    "validate_technique_efficacy",
    "check_safety",
    "review_ethics",
    "validate_adaptation",
    "assess_effectiveness",
    "search_agent_knowledge"
]
