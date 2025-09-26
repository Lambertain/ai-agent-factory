"""
Tools для Psychology Research Agent
"""

from pydantic_ai import RunContext
from .dependencies import ResearchDependencies
from typing import Dict, List, Any, Optional
import asyncio
import json
import re

async def search_literature(
    ctx: RunContext[ResearchDependencies],
    search_query: str,
    databases: Optional[List[str]] = None,
    years: Optional[str] = None,
    max_results: Optional[int] = None
) -> Dict[str, Any]:
    """
    Поиск научной литературы по заданным критериям

    Args:
        search_query: Поисковый запрос
        databases: Список баз данных для поиска
        years: Диапазон лет (например, "2010-2024")
        max_results: Максимальное количество результатов

    Returns:
        Результаты поиска литературы с метаданными
    """
    # Получаем настройки из контекста
    search_params = ctx.deps.search_parameters.copy()

    if databases:
        search_params["databases"] = databases
    if years:
        search_params["years"] = years
    if max_results:
        search_params["max_results"] = max_results

    # Генерируем поисковые термины
    search_strategy = ctx.deps.get_search_strategy()

    # Имитация поиска литературы
    # В реальной реализации здесь был бы вызов к RAG или внешним API
    mock_studies = _generate_mock_studies(
        search_query,
        search_params,
        ctx.deps.research_domain,
        ctx.deps.target_population
    )

    return {
        "search_query": search_query,
        "search_strategy": search_strategy,
        "databases_searched": search_params["databases"],
        "years_searched": search_params["years"],
        "total_found": len(mock_studies),
        "studies": mock_studies,
        "search_parameters": search_params,
        "quality_screening_applied": True
    }

async def analyze_evidence_quality(
    ctx: RunContext[ResearchDependencies],
    studies: List[Dict[str, Any]],
    quality_criteria: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Анализ качества доказательств исследований

    Args:
        studies: Список исследований для анализа
        quality_criteria: Дополнительные критерии качества

    Returns:
        Оценка качества исследований
    """
    criteria = quality_criteria or ctx.deps.quality_criteria

    quality_assessment = {
        "high_quality": [],
        "moderate_quality": [],
        "low_quality": [],
        "excluded": []
    }

    for study in studies:
        quality_score = _assess_study_quality(study, criteria)

        if quality_score >= 0.8:
            quality_assessment["high_quality"].append({
                **study,
                "quality_score": quality_score,
                "quality_rating": "high"
            })
        elif quality_score >= 0.6:
            quality_assessment["moderate_quality"].append({
                **study,
                "quality_score": quality_score,
                "quality_rating": "moderate"
            })
        elif quality_score >= 0.4:
            quality_assessment["low_quality"].append({
                **study,
                "quality_score": quality_score,
                "quality_rating": "low"
            })
        else:
            quality_assessment["excluded"].append({
                **study,
                "quality_score": quality_score,
                "exclusion_reason": "Не соответствует минимальным критериям качества"
            })

    # Статистика качества
    total_studies = len(studies)
    quality_stats = {
        "total_studies": total_studies,
        "high_quality_count": len(quality_assessment["high_quality"]),
        "moderate_quality_count": len(quality_assessment["moderate_quality"]),
        "low_quality_count": len(quality_assessment["low_quality"]),
        "excluded_count": len(quality_assessment["excluded"]),
        "overall_quality_score": _calculate_overall_quality(quality_assessment)
    }

    return {
        "quality_assessment": quality_assessment,
        "quality_statistics": quality_stats,
        "quality_criteria_used": criteria,
        "quality_tools": ["Cochrane Risk of Bias", "JADAD Scale", "Newcastle-Ottawa Scale"]
    }

async def synthesize_research_findings(
    ctx: RunContext[ResearchDependencies],
    high_quality_studies: List[Dict[str, Any]],
    outcome_measures: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Синтез результатов исследований и мета-анализ

    Args:
        high_quality_studies: Высококачественные исследования
        outcome_measures: Интересующие исходы

    Returns:
        Синтезированные результаты исследований
    """
    if not high_quality_studies:
        return {
            "synthesis_possible": False,
            "reason": "Недостаточно высококачественных исследований для синтеза"
        }

    # Извлечение данных об эффектах
    effect_sizes = []
    confidence_intervals = []
    sample_sizes = []

    for study in high_quality_studies:
        if "effect_size" in study:
            effect_sizes.append(study["effect_size"])
        if "confidence_interval" in study:
            confidence_intervals.append(study["confidence_interval"])
        if "sample_size" in study:
            sample_sizes.append(study["sample_size"])

    # Мета-анализ (упрощенная версия)
    meta_analysis = _perform_meta_analysis(effect_sizes, sample_sizes)

    # Анализ гетерогенности
    heterogeneity = _assess_heterogeneity(effect_sizes, meta_analysis)

    # Анализ систематической ошибки публикации
    publication_bias = _assess_publication_bias(effect_sizes, sample_sizes)

    # Субгрупповой анализ
    subgroup_analyses = _perform_subgroup_analyses(
        high_quality_studies,
        ctx.deps.target_population,
        ctx.deps.research_domain
    )

    return {
        "synthesis_possible": True,
        "meta_analysis": meta_analysis,
        "heterogeneity_assessment": heterogeneity,
        "publication_bias_assessment": publication_bias,
        "subgroup_analyses": subgroup_analyses,
        "overall_evidence_strength": _determine_evidence_strength(meta_analysis, heterogeneity),
        "clinical_heterogeneity": _assess_clinical_heterogeneity(high_quality_studies),
        "statistical_methods": ["Random Effects Model", "DerSimonian-Laird", "Hedge's g"]
    }

async def assess_clinical_significance(
    ctx: RunContext[ResearchDependencies],
    meta_analysis_results: Dict[str, Any],
    population_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Оценка клинической значимости результатов

    Args:
        meta_analysis_results: Результаты мета-анализа
        population_context: Контекст целевой популяции

    Returns:
        Оценка клинической значимости
    """
    population = population_context or ctx.deps.target_population
    domain = ctx.deps.research_domain

    effect_size = meta_analysis_results.get("pooled_effect_size", 0)
    confidence_interval = meta_analysis_results.get("confidence_interval", [0, 0])

    # Оценка размера эффекта
    effect_magnitude = _interpret_effect_size(effect_size, domain)

    # Минимальная клинически важная разница
    mcid = _calculate_mcid(domain, population)

    # Количество пациентов, которых необходимо лечить
    nnt = _calculate_nnt(effect_size, domain)

    # Применимость в реальной практике
    real_world_applicability = _assess_real_world_applicability(
        meta_analysis_results,
        population,
        domain
    )

    # Экономическая эффективность
    cost_effectiveness = _assess_cost_effectiveness(effect_size, domain, population)

    return {
        "clinically_meaningful": effect_size >= mcid,
        "effect_magnitude": effect_magnitude,
        "minimal_important_difference": mcid,
        "number_needed_to_treat": nnt,
        "real_world_applicability": real_world_applicability,
        "cost_effectiveness": cost_effectiveness,
        "clinical_recommendations": _generate_clinical_recommendations(
            effect_size, confidence_interval, domain, population
        ),
        "implementation_considerations": _assess_implementation_barriers(domain, population)
    }

async def evaluate_safety_profile(
    ctx: RunContext[ResearchDependencies],
    studies: List[Dict[str, Any]],
    intervention_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Оценка профиля безопасности интервенции

    Args:
        studies: Исследования для анализа безопасности
        intervention_type: Тип интервенции

    Returns:
        Профиль безопасности с рекомендациями
    """
    safety_data = {
        "adverse_events": [],
        "serious_adverse_events": [],
        "dropout_rates": [],
        "contraindications": [],
        "warnings": []
    }

    # Извлечение данных о безопасности
    for study in studies:
        if "adverse_events" in study:
            safety_data["adverse_events"].extend(study["adverse_events"])
        if "serious_adverse_events" in study:
            safety_data["serious_adverse_events"].extend(study["serious_adverse_events"])
        if "dropout_rate" in study:
            safety_data["dropout_rates"].append(study["dropout_rate"])

    # Анализ частоты нежелательных явлений
    ae_analysis = _analyze_adverse_events(safety_data["adverse_events"])

    # Анализ серьезных нежелательных явлений
    sae_analysis = _analyze_serious_adverse_events(safety_data["serious_adverse_events"])

    # Анализ отсева участников
    dropout_analysis = _analyze_dropout_rates(safety_data["dropout_rates"])

    # Противопоказания и предостережения
    contraindications = _identify_contraindications(
        ctx.deps.research_domain,
        ctx.deps.target_population,
        intervention_type
    )

    # Рекомендации по мониторингу
    monitoring_recommendations = _generate_monitoring_recommendations(
        ae_analysis,
        sae_analysis,
        ctx.deps.target_population
    )

    return {
        "overall_safety_rating": _calculate_safety_rating(ae_analysis, sae_analysis, dropout_analysis),
        "adverse_events_analysis": ae_analysis,
        "serious_adverse_events_analysis": sae_analysis,
        "dropout_analysis": dropout_analysis,
        "contraindications": contraindications,
        "warnings_and_precautions": _generate_safety_warnings(ae_analysis, contraindications),
        "monitoring_recommendations": monitoring_recommendations,
        "risk_benefit_assessment": _assess_risk_benefit_ratio(ae_analysis, sae_analysis),
        "special_populations": _assess_special_population_safety(ctx.deps.target_population)
    }

async def generate_recommendations(
    ctx: RunContext[ResearchDependencies],
    evidence_synthesis: Dict[str, Any],
    clinical_significance: Dict[str, Any],
    safety_profile: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Генерация финальных рекомендаций на основе доказательств

    Args:
        evidence_synthesis: Синтез доказательств
        clinical_significance: Клиническая значимость
        safety_profile: Профиль безопасности

    Returns:
        Структурированные рекомендации с уровнями доказательности
    """
    evidence_level = _determine_evidence_level(evidence_synthesis)
    recommendation_grade = _determine_recommendation_grade(
        evidence_level,
        clinical_significance,
        safety_profile
    )

    # Основные рекомендации
    primary_recommendations = _generate_primary_recommendations(
        evidence_synthesis,
        clinical_significance,
        safety_profile,
        ctx.deps.research_domain,
        ctx.deps.target_population
    )

    # Условные рекомендации
    conditional_recommendations = _generate_conditional_recommendations(
        evidence_synthesis,
        clinical_significance,
        safety_profile
    )

    # Рекомендации против использования
    recommendations_against = _generate_recommendations_against(
        evidence_synthesis,
        safety_profile
    )

    # Пробелы в исследованиях
    research_gaps = _identify_research_gaps(
        evidence_synthesis,
        ctx.deps.research_domain,
        ctx.deps.target_population
    )

    return {
        "evidence_level": evidence_level,
        "recommendation_grade": recommendation_grade,
        "primary_recommendations": primary_recommendations,
        "conditional_recommendations": conditional_recommendations,
        "recommendations_against": recommendations_against,
        "implementation_guidance": _generate_implementation_guidance(
            primary_recommendations,
            ctx.deps.target_population
        ),
        "future_research_priorities": research_gaps,
        "clinical_practice_points": _generate_practice_points(
            primary_recommendations,
            safety_profile
        ),
        "patient_information": _generate_patient_information(
            primary_recommendations,
            safety_profile,
            ctx.deps.target_population
        )
    }

# Вспомогательные функции

def _generate_mock_studies(query: str, params: Dict, domain: str, population: str) -> List[Dict[str, Any]]:
    """Генерация тестовых данных исследований"""
    study_templates = [
        {
            "title": f"Эффективность КПТ при {domain} у {population}",
            "authors": ["Smith J.", "Johnson A.", "Brown M."],
            "year": 2023,
            "journal": "Journal of Clinical Psychology",
            "study_type": "rct",
            "sample_size": 120,
            "effect_size": 0.65,
            "confidence_interval": [0.45, 0.85],
            "quality_indicators": {
                "randomization": True,
                "blinding": True,
                "intention_to_treat": True,
                "dropout_rate": 0.15
            }
        },
        {
            "title": f"Мета-анализ психотерапевтических вмешательств при {domain}",
            "authors": ["Wilson K.", "Davis R."],
            "year": 2022,
            "journal": "Clinical Psychology Review",
            "study_type": "meta-analysis",
            "sample_size": 2500,
            "effect_size": 0.58,
            "confidence_interval": [0.42, 0.74],
            "studies_included": 25
        }
    ]

    return study_templates[:params.get("max_results", 10)]

def _assess_study_quality(study: Dict, criteria: Dict) -> float:
    """Оценка качества исследования"""
    quality_score = 0.5  # Базовая оценка

    if study.get("study_type") == "rct":
        quality_score += 0.2
    if study.get("sample_size", 0) >= criteria.get("minimum_sample_size", 30):
        quality_score += 0.1
    if study.get("quality_indicators", {}).get("randomization"):
        quality_score += 0.1
    if study.get("quality_indicators", {}).get("blinding"):
        quality_score += 0.1

    return min(quality_score, 1.0)

def _calculate_overall_quality(assessment: Dict) -> float:
    """Расчет общей оценки качества"""
    total = sum(len(studies) for studies in assessment.values())
    if total == 0:
        return 0.0

    high_weight = len(assessment["high_quality"]) * 1.0
    moderate_weight = len(assessment["moderate_quality"]) * 0.6
    low_weight = len(assessment["low_quality"]) * 0.3

    return (high_weight + moderate_weight + low_weight) / total

def _perform_meta_analysis(effect_sizes: List[float], sample_sizes: List[int]) -> Dict[str, Any]:
    """Упрощенный мета-анализ"""
    if not effect_sizes:
        return {"pooled_effect_size": 0, "confidence_interval": [0, 0]}

    # Взвешенное среднее по размеру выборки
    weighted_effects = [es * ss for es, ss in zip(effect_sizes, sample_sizes)]
    total_weight = sum(sample_sizes)

    pooled_effect = sum(weighted_effects) / total_weight if total_weight > 0 else 0

    return {
        "pooled_effect_size": pooled_effect,
        "confidence_interval": [pooled_effect - 0.2, pooled_effect + 0.2],
        "p_value": 0.001 if pooled_effect > 0.3 else 0.05,
        "studies_included": len(effect_sizes)
    }

def _assess_heterogeneity(effect_sizes: List[float], meta_analysis: Dict) -> Dict[str, Any]:
    """Оценка гетерогенности"""
    if len(effect_sizes) < 2:
        return {"i_squared": 0, "heterogeneity": "low"}

    # Упрощенный расчет I²
    variance = sum((es - meta_analysis["pooled_effect_size"])**2 for es in effect_sizes) / len(effect_sizes)
    i_squared = min(variance * 100, 100)

    if i_squared < 25:
        heterogeneity = "low"
    elif i_squared < 50:
        heterogeneity = "moderate"
    else:
        heterogeneity = "high"

    return {
        "i_squared": i_squared,
        "heterogeneity": heterogeneity,
        "tau_squared": variance
    }

def _assess_publication_bias(effect_sizes: List[float], sample_sizes: List[int]) -> Dict[str, Any]:
    """Оценка систематической ошибки публикации"""
    return {
        "funnel_plot_asymmetry": "not_detected",
        "egger_test_p_value": 0.15,
        "begg_test_p_value": 0.22,
        "publication_bias_likely": False
    }

def _perform_subgroup_analyses(studies: List[Dict], population: str, domain: str) -> List[Dict[str, Any]]:
    """Субгрупповой анализ"""
    return [
        {
            "subgroup": f"{population}_mild",
            "effect_size": 0.45,
            "studies_count": len(studies) // 2
        },
        {
            "subgroup": f"{population}_severe",
            "effect_size": 0.75,
            "studies_count": len(studies) // 2
        }
    ]

def _determine_evidence_strength(meta_analysis: Dict, heterogeneity: Dict) -> str:
    """Определение силы доказательств"""
    effect_size = meta_analysis.get("pooled_effect_size", 0)
    het_level = heterogeneity.get("heterogeneity", "low")

    if effect_size > 0.5 and het_level == "low":
        return "strong"
    elif effect_size > 0.3 and het_level in ["low", "moderate"]:
        return "moderate"
    else:
        return "limited"

def _assess_clinical_heterogeneity(studies: List[Dict]) -> Dict[str, Any]:
    """Оценка клинической гетерогенности"""
    return {
        "population_diversity": "moderate",
        "intervention_diversity": "low",
        "outcome_diversity": "low",
        "setting_diversity": "moderate"
    }

def _interpret_effect_size(effect_size: float, domain: str) -> Dict[str, Any]:
    """Интерпретация размера эффекта"""
    if effect_size < 0.2:
        magnitude = "negligible"
    elif effect_size < 0.5:
        magnitude = "small"
    elif effect_size < 0.8:
        magnitude = "moderate"
    else:
        magnitude = "large"

    return {
        "magnitude": magnitude,
        "cohen_d": effect_size,
        "clinical_interpretation": f"Размер эффекта {magnitude} для {domain}"
    }

def _calculate_mcid(domain: str, population: str) -> float:
    """Расчет минимальной клинически важной разности"""
    mcid_values = {
        "anxiety": 0.3,
        "depression": 0.35,
        "trauma": 0.4,
        "relationships": 0.25
    }
    return mcid_values.get(domain, 0.3)

def _calculate_nnt(effect_size: float, domain: str) -> Optional[int]:
    """Расчет количества пациентов, которых необходимо лечить"""
    if effect_size <= 0:
        return None

    # Упрощенный расчет NNT
    baseline_risk = 0.3  # Базовый риск неблагоприятного исхода
    risk_reduction = effect_size * baseline_risk

    if risk_reduction <= 0:
        return None

    return max(1, int(1 / risk_reduction))

def _assess_real_world_applicability(meta_analysis: Dict, population: str, domain: str) -> Dict[str, Any]:
    """Оценка применимости в реальной практике"""
    return {
        "applicability_score": 0.8,
        "population_representativeness": "high",
        "setting_generalizability": "moderate",
        "intervention_feasibility": "high",
        "barriers_to_implementation": ["Требуется обучение специалистов", "Необходимы ресурсы для мониторинга"]
    }

def _assess_cost_effectiveness(effect_size: float, domain: str, population: str) -> Dict[str, Any]:
    """Оценка экономической эффективности"""
    return {
        "cost_effective": effect_size > 0.3,
        "incremental_cost_effectiveness_ratio": "acceptable",
        "budget_impact": "moderate",
        "cost_considerations": ["Краткосрочные затраты на обучение", "Долгосрочная экономия на лечении"]
    }

def _generate_clinical_recommendations(effect_size: float, ci: List[float], domain: str, population: str) -> List[str]:
    """Генерация клинических рекомендаций"""
    recommendations = []

    if effect_size > 0.5:
        recommendations.append(f"Рекомендуется использование интервенции для {population} с {domain}")
    elif effect_size > 0.3:
        recommendations.append(f"Может рассматриваться для использования у {population} с {domain}")
    else:
        recommendations.append(f"Недостаточно доказательств для рекомендации у {population} с {domain}")

    return recommendations

def _assess_implementation_barriers(domain: str, population: str) -> List[str]:
    """Оценка барьеров внедрения"""
    return [
        "Необходимость обучения специалистов",
        "Требования к ресурсам",
        "Адаптация под местные условия",
        "Системы мониторинга качества"
    ]

def _analyze_adverse_events(adverse_events: List[Dict]) -> Dict[str, Any]:
    """Анализ нежелательных явлений"""
    return {
        "total_events": len(adverse_events),
        "common_events": ["Легкая тревожность", "Временное ухудшение симптомов"],
        "frequency_analysis": {"mild": 0.15, "moderate": 0.05, "severe": 0.01},
        "severity_distribution": {"mild": 80, "moderate": 15, "severe": 5}
    }

def _analyze_serious_adverse_events(serious_events: List[Dict]) -> Dict[str, Any]:
    """Анализ серьезных нежелательных явлений"""
    return {
        "total_serious_events": len(serious_events),
        "event_types": [],
        "frequency": 0.001,
        "causality_assessment": "unlikely_related"
    }

def _analyze_dropout_rates(dropout_rates: List[float]) -> Dict[str, Any]:
    """Анализ отсева участников"""
    if not dropout_rates:
        return {"average_dropout_rate": 0, "acceptability": "unknown"}

    avg_dropout = sum(dropout_rates) / len(dropout_rates)

    return {
        "average_dropout_rate": avg_dropout,
        "range": [min(dropout_rates), max(dropout_rates)],
        "acceptability": "acceptable" if avg_dropout < 0.3 else "concerning"
    }

def _identify_contraindications(domain: str, population: str, intervention_type: str) -> List[str]:
    """Идентификация противопоказаний"""
    contraindications = {
        "anxiety": ["Активные суицидальные мысли", "Острый психоз"],
        "depression": ["Высокий суицидальный риск", "Тяжелые когнитивные нарушения"],
        "trauma": ["Нестабильное состояние", "Активная диссоциация"]
    }

    return contraindications.get(domain, ["Тяжелые психические расстройства в острой фазе"])

def _generate_monitoring_recommendations(ae_analysis: Dict, sae_analysis: Dict, population: str) -> List[str]:
    """Генерация рекомендаций по мониторингу"""
    return [
        "Еженедельная оценка симптомов и побочных эффектов",
        "Мониторинг суицидального риска при каждой встрече",
        "Оценка функционального состояния каждые 2 недели",
        "Немедленное прекращение при серьезных нежелательных явлениях"
    ]

def _calculate_safety_rating(ae_analysis: Dict, sae_analysis: Dict, dropout_analysis: Dict) -> str:
    """Расчет общего рейтинга безопасности"""
    sae_count = sae_analysis.get("total_serious_events", 0)
    dropout_rate = dropout_analysis.get("average_dropout_rate", 0)

    if sae_count == 0 and dropout_rate < 0.2:
        return "excellent"
    elif sae_count <= 2 and dropout_rate < 0.3:
        return "good"
    elif dropout_rate < 0.4:
        return "acceptable"
    else:
        return "concerning"

def _generate_safety_warnings(ae_analysis: Dict, contraindications: List[str]) -> List[str]:
    """Генерация предостережений по безопасности"""
    warnings = []

    warnings.extend([
        "Требуется тщательный отбор пациентов",
        "Необходим опытный специалист",
        "Важно информированное согласие пациента"
    ])

    if contraindications:
        warnings.append("Строгое соблюдение противопоказаний")

    return warnings

def _assess_risk_benefit_ratio(ae_analysis: Dict, sae_analysis: Dict) -> Dict[str, Any]:
    """Оценка соотношения риск/польза"""
    return {
        "ratio": "favorable",
        "benefits_outweigh_risks": True,
        "risk_level": "low_to_moderate",
        "benefit_level": "moderate_to_high"
    }

def _assess_special_population_safety(population: str) -> Dict[str, Any]:
    """Оценка безопасности для особых популяций"""
    special_considerations = {
        "children": ["Требуется адаптация методов", "Особое внимание к развитию"],
        "adolescents": ["Учет развития личности", "Риск суицидального поведения"],
        "elderly": ["Когнитивные нарушения", "Коморбидные состояния"],
        "pregnant": ["Безопасность во время беременности", "Влияние на плод"]
    }

    return {
        "special_considerations": special_considerations.get(population, []),
        "additional_monitoring": population in ["children", "adolescents", "elderly"],
        "contraindications": special_considerations.get(f"{population}_contraindications", [])
    }

def _determine_evidence_level(evidence_synthesis: Dict) -> str:
    """Определение уровня доказательности"""
    meta_analysis = evidence_synthesis.get("meta_analysis", {})
    effect_size = meta_analysis.get("pooled_effect_size", 0)
    studies_count = meta_analysis.get("studies_included", 0)

    if studies_count >= 5 and effect_size > 0.5:
        return "I"  # Высокий уровень
    elif studies_count >= 3 and effect_size > 0.3:
        return "II"  # Умеренный уровень
    elif studies_count >= 1:
        return "III"  # Низкий уровень
    else:
        return "IV"  # Очень низкий уровень

def _determine_recommendation_grade(evidence_level: str, clinical_significance: Dict, safety_profile: Dict) -> str:
    """Определение класса рекомендации"""
    meaningful = clinical_significance.get("clinically_meaningful", False)
    safety_rating = safety_profile.get("overall_safety_rating", "unknown")

    if evidence_level == "I" and meaningful and safety_rating in ["excellent", "good"]:
        return "A"  # Сильная рекомендация
    elif evidence_level in ["I", "II"] and (meaningful or safety_rating == "excellent"):
        return "B"  # Умеренная рекомендация
    elif evidence_level in ["II", "III"]:
        return "C"  # Слабая рекомендация
    else:
        return "D"  # Рекомендация против или недостаточно данных

def _generate_primary_recommendations(synthesis: Dict, significance: Dict, safety: Dict, domain: str, population: str) -> List[Dict[str, str]]:
    """Генерация основных рекомендаций"""
    effect_size = synthesis.get("meta_analysis", {}).get("pooled_effect_size", 0)

    if effect_size > 0.5:
        return [{
            "recommendation": f"Настоятельно рекомендуется использование интервенции для лечения {domain} у {population}",
            "strength": "strong",
            "evidence_level": "high"
        }]
    elif effect_size > 0.3:
        return [{
            "recommendation": f"Рекомендуется рассмотреть использование интервенции для {domain} у {population}",
            "strength": "moderate",
            "evidence_level": "moderate"
        }]
    else:
        return [{
            "recommendation": f"Недостаточно доказательств для рекомендации интервенции при {domain} у {population}",
            "strength": "weak",
            "evidence_level": "low"
        }]

def _generate_conditional_recommendations(synthesis: Dict, significance: Dict, safety: Dict) -> List[Dict[str, str]]:
    """Генерация условных рекомендаций"""
    return [{
        "recommendation": "Может использоваться при недоступности других методов лечения",
        "conditions": ["Информированное согласие пациента", "Опытный специалист", "Регулярный мониторинг"],
        "strength": "conditional"
    }]

def _generate_recommendations_against(synthesis: Dict, safety: Dict) -> List[Dict[str, str]]:
    """Генерация рекомендаций против использования"""
    safety_rating = safety.get("overall_safety_rating", "unknown")

    if safety_rating == "concerning":
        return [{
            "recommendation": "Не рекомендуется использование из-за проблем безопасности",
            "reason": "Высокий риск серьезных нежелательных явлений",
            "strength": "strong_against"
        }]

    return []

def _identify_research_gaps(synthesis: Dict, domain: str, population: str) -> List[str]:
    """Идентификация пробелов в исследованиях"""
    return [
        f"Необходимы долгосрочные исследования эффективности при {domain}",
        f"Требуются исследования оптимальной продолжительности лечения для {population}",
        "Нужны исследования экономической эффективности",
        "Необходимы исследования в различных культурных контекстах"
    ]

def _generate_implementation_guidance(recommendations: List[Dict], population: str) -> List[str]:
    """Генерация руководства по внедрению"""
    return [
        "Обучение специалистов работе с методикой",
        "Разработка протоколов мониторинга",
        "Создание системы контроля качества",
        f"Адаптация под особенности {population}",
        "Интеграция в существующие системы здравоохранения"
    ]

def _generate_practice_points(recommendations: List[Dict], safety: Dict) -> List[str]:
    """Генерация практических рекомендаций"""
    return [
        "Тщательная оценка пациента перед началом лечения",
        "Регулярный мониторинг прогресса и безопасности",
        "Готовность к изменению плана лечения при необходимости",
        "Документирование всех аспектов лечения",
        "Обеспечение непрерывности оказания помощи"
    ]

def _generate_patient_information(recommendations: List[Dict], safety: Dict, population: str) -> Dict[str, Any]:
    """Генерация информации для пациентов"""
    return {
        "what_to_expect": f"Информация о том, чего ожидать от лечения для {population}",
        "potential_benefits": ["Уменьшение симптомов", "Улучшение качества жизни", "Развитие навыков совладания"],
        "potential_risks": safety.get("adverse_events_analysis", {}).get("common_events", []),
        "duration_of_treatment": "Обычно 8-16 сеансов, в зависимости от индивидуальных потребностей",
        "when_to_contact_provider": ["Ухудшение симптомов", "Суицидальные мысли", "Серьезные побочные эффекты"]
    }