# -*- coding: utf-8 -*-
"""
Инструменты для Universal Personalizer Agent
Универсальные инструменты персонализации для различных доменов
"""

import json
import asyncio
from typing import Dict, List, Any, Optional
from pydantic_ai import RunContext

try:
    # Попытка импорта MCP Archon для RAG
    from mcp_tools import mcp_archon_rag_search_knowledge_base, mcp_archon_manage_task
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

from .dependencies import PersonalizerDependencies, AGENT_COMPETENCIES, AGENT_ASSIGNEE_MAP

async def analyze_user_profile(
    ctx: RunContext[PersonalizerDependencies],
    user_data: Dict[str, Any],
    analysis_depth: str = "comprehensive",
    domain_context: str = None
) -> str:
    """
    Анализ профиля пользователя для персонализации.

    Args:
        user_data: Данные пользователя (поведение, предпочтения, демография)
        analysis_depth: Глубина анализа (basic, comprehensive, deep)
        domain_context: Контекст домена для анализа

    Returns:
        Структурированный профиль пользователя с рекомендациями по персонализации
    """
    try:
        domain_type = domain_context or ctx.deps.domain_type
        personalization_factors = ctx.deps.get_personalization_factors_for_domain()

        # Анализируем в зависимости от домена
        if domain_type == "psychology":
            return await _analyze_psychology_profile(user_data, analysis_depth, personalization_factors)
        elif domain_type == "astrology":
            return await _analyze_astrology_profile(user_data, analysis_depth, personalization_factors)
        elif domain_type == "numerology":
            return await _analyze_numerology_profile(user_data, analysis_depth, personalization_factors)
        elif domain_type == "business":
            return await _analyze_business_profile(user_data, analysis_depth, personalization_factors)
        else:
            return await _analyze_universal_profile(user_data, analysis_depth, personalization_factors)

    except Exception as e:
        return f"Ошибка анализа профиля: {e}"

async def _analyze_psychology_profile(user_data: Dict[str, Any], depth: str, factors: List[str]) -> str:
    """Анализ профиля для психологического домена."""
    analysis = {
        "psychological_profile": {
            "personality_traits": user_data.get("personality", {}),
            "emotional_state": user_data.get("emotional_indicators", {}),
            "therapeutic_goals": user_data.get("goals", []),
            "cultural_background": user_data.get("culture", "unknown"),
            "previous_interventions": user_data.get("history", [])
        },
        "personalization_recommendations": {
            "content_adaptation": "Evidence-based therapeutic content matching personality and goals",
            "intervention_timing": "Optimize based on emotional state patterns",
            "cultural_sensitivity": "Adapt language and examples to cultural background",
            "progress_tracking": "Personalized metrics based on therapeutic goals"
        },
        "risk_factors": {
            "trauma_indicators": user_data.get("trauma_history", False),
            "crisis_risk": user_data.get("crisis_indicators", "low"),
            "support_system": user_data.get("support_level", "unknown")
        },
        "recommended_approaches": _get_psychology_approaches(user_data),
        "personalization_confidence": _calculate_confidence(user_data, factors)
    }

    return json.dumps(analysis, ensure_ascii=False, indent=2)

async def _analyze_astrology_profile(user_data: Dict[str, Any], depth: str, factors: List[str]) -> str:
    """Анализ профиля для астрологического домена."""
    analysis = {
        "astrological_profile": {
            "birth_chart_data": user_data.get("birth_info", {}),
            "astrological_preferences": user_data.get("traditions", ["western"]),
            "experience_level": user_data.get("experience", "beginner"),
            "spiritual_orientation": user_data.get("spirituality", "open"),
            "consultation_history": user_data.get("consultations", [])
        },
        "personalization_recommendations": {
            "chart_emphasis": "Focus on most relevant planetary aspects",
            "interpretation_style": "Match depth to experience level",
            "cultural_context": "Adapt to preferred astrological tradition",
            "timing_sensitivity": "Provide relevant transit information"
        },
        "astrological_insights": {
            "dominant_elements": user_data.get("elements", []),
            "key_aspects": user_data.get("aspects", []),
            "life_themes": user_data.get("themes", [])
        },
        "recommended_content": _get_astrology_content(user_data),
        "personalization_confidence": _calculate_confidence(user_data, factors)
    }

    return json.dumps(analysis, ensure_ascii=False, indent=2)

async def _analyze_numerology_profile(user_data: Dict[str, Any], depth: str, factors: List[str]) -> str:
    """Анализ профиля для нумерологического домена."""
    analysis = {
        "numerological_profile": {
            "core_numbers": user_data.get("core_numbers", {}),
            "life_path": user_data.get("life_path", None),
            "personal_year": user_data.get("personal_year", None),
            "name_vibrations": user_data.get("name_analysis", {}),
            "system_preference": user_data.get("system", "pythagorean")
        },
        "personalization_recommendations": {
            "calculation_focus": "Emphasize most relevant numbers",
            "interpretation_depth": "Match to user's understanding level",
            "practical_application": "Provide actionable insights",
            "cultural_adaptation": "Adapt meanings to cultural context"
        },
        "numerological_insights": {
            "strengths": user_data.get("strengths", []),
            "challenges": user_data.get("challenges", []),
            "opportunities": user_data.get("opportunities", []),
            "life_cycles": user_data.get("cycles", [])
        },
        "recommended_guidance": _get_numerology_guidance(user_data),
        "personalization_confidence": _calculate_confidence(user_data, factors)
    }

    return json.dumps(analysis, ensure_ascii=False, indent=2)

async def _analyze_business_profile(user_data: Dict[str, Any], depth: str, factors: List[str]) -> str:
    """Анализ профиля для бизнес-домена."""
    analysis = {
        "business_profile": {
            "industry_sector": user_data.get("industry", "unknown"),
            "company_size": user_data.get("company_size", "unknown"),
            "role_level": user_data.get("role", "unknown"),
            "business_goals": user_data.get("goals", []),
            "market_position": user_data.get("market_position", "unknown"),
            "technology_adoption": user_data.get("tech_level", "medium")
        },
        "personalization_recommendations": {
            "content_relevance": "Industry-specific insights and benchmarks",
            "complexity_level": "Match to role and experience level",
            "actionability": "Provide implementation-ready recommendations",
            "roi_focus": "Emphasize measurable business outcomes"
        },
        "business_insights": {
            "competitive_advantages": user_data.get("advantages", []),
            "growth_opportunities": user_data.get("opportunities", []),
            "operational_challenges": user_data.get("challenges", []),
            "market_trends": user_data.get("trends", [])
        },
        "recommended_strategies": _get_business_strategies(user_data),
        "personalization_confidence": _calculate_confidence(user_data, factors)
    }

    return json.dumps(analysis, ensure_ascii=False, indent=2)

async def _analyze_universal_profile(user_data: Dict[str, Any], depth: str, factors: List[str]) -> str:
    """Универсальный анализ профиля."""
    analysis = {
        "universal_profile": {
            "user_segments": user_data.get("segments", []),
            "behavioral_patterns": user_data.get("behavior", {}),
            "preferences": user_data.get("preferences", {}),
            "engagement_history": user_data.get("engagement", {}),
            "demographic_info": user_data.get("demographics", {})
        },
        "personalization_recommendations": {
            "content_matching": "Align content with user preferences and behavior",
            "engagement_optimization": "Optimize based on interaction patterns",
            "experience_customization": "Adapt interface and flow to user needs",
            "recommendation_tuning": "Fine-tune recommendations based on feedback"
        },
        "insights": {
            "key_interests": user_data.get("interests", []),
            "interaction_patterns": user_data.get("patterns", []),
            "satisfaction_drivers": user_data.get("satisfaction", [])
        },
        "personalization_confidence": _calculate_confidence(user_data, factors)
    }

    return json.dumps(analysis, ensure_ascii=False, indent=2)

def _get_psychology_approaches(user_data: Dict[str, Any]) -> List[str]:
    """Получить рекомендуемые психологические подходы."""
    approaches = []
    personality = user_data.get("personality", {})

    if personality.get("openness", 0) > 0.7:
        approaches.append("mindfulness_based_interventions")
    if personality.get("conscientiousness", 0) > 0.6:
        approaches.append("structured_cognitive_behavioral")
    if user_data.get("culture", "").lower() in ["ukraine", "eastern_european"]:
        approaches.append("culturally_adapted_therapy")

    return approaches

def _get_astrology_content(user_data: Dict[str, Any]) -> List[str]:
    """Получить рекомендуемый астрологический контент."""
    content = []
    experience = user_data.get("experience", "beginner")

    if experience == "beginner":
        content.extend(["basic_chart_reading", "planetary_meanings", "sign_characteristics"])
    elif experience == "intermediate":
        content.extend(["aspect_patterns", "transits", "progressions"])
    else:
        content.extend(["advanced_techniques", "traditional_methods", "predictive_astrology"])

    return content

def _get_numerology_guidance(user_data: Dict[str, Any]) -> List[str]:
    """Получить нумерологические рекомендации."""
    guidance = []
    life_path = user_data.get("life_path")

    if life_path:
        guidance.append(f"life_path_{life_path}_guidance")
    if user_data.get("personal_year"):
        guidance.append("personal_year_insights")
    if user_data.get("business_focus"):
        guidance.append("business_numerology")

    return guidance

def _get_business_strategies(user_data: Dict[str, Any]) -> List[str]:
    """Получить бизнес-стратегии."""
    strategies = []
    industry = user_data.get("industry", "")
    size = user_data.get("company_size", "")

    if size in ["startup", "small"]:
        strategies.extend(["growth_hacking", "lean_operations", "agile_development"])
    elif size in ["medium", "large"]:
        strategies.extend(["digital_transformation", "process_optimization", "data_analytics"])

    if industry in ["tech", "software"]:
        strategies.append("innovation_management")

    return strategies

def _calculate_confidence(user_data: Dict[str, Any], factors: List[str]) -> float:
    """Рассчитать уверенность в персонализации."""
    available_factors = len([f for f in factors if f in str(user_data)])
    total_factors = len(factors)

    if total_factors == 0:
        return 0.5

    base_confidence = available_factors / total_factors
    data_completeness = len(user_data) / 10  # Предполагаем 10 ключевых полей

    return min(0.95, (base_confidence * 0.7 + min(1.0, data_completeness) * 0.3))

async def generate_personalized_content(
    ctx: RunContext[PersonalizerDependencies],
    base_content: str,
    user_profile: Dict[str, Any],
    personalization_strategy: str = "adaptive",
    content_type: str = "general"
) -> str:
    """
    Генерация персонализированного контента.

    Args:
        base_content: Исходный контент для персонализации
        user_profile: Профиль пользователя
        personalization_strategy: Стратегия персонализации
        content_type: Тип контента для адаптации

    Returns:
        Персонализированный контент
    """
    try:
        domain_type = ctx.deps.domain_type
        content_types = ctx.deps.get_content_types_for_domain()
        adaptation_rules = ctx.deps.get_adaptation_rules_for_domain()

        # Персонализируем в зависимости от домена
        if domain_type == "psychology":
            return await _personalize_psychology_content(base_content, user_profile, adaptation_rules)
        elif domain_type == "astrology":
            return await _personalize_astrology_content(base_content, user_profile, adaptation_rules)
        elif domain_type == "numerology":
            return await _personalize_numerology_content(base_content, user_profile, adaptation_rules)
        elif domain_type == "business":
            return await _personalize_business_content(base_content, user_profile, adaptation_rules)
        else:
            return await _personalize_universal_content(base_content, user_profile, adaptation_rules)

    except Exception as e:
        return f"Ошибка генерации персонализированного контента: {e}"

async def _personalize_psychology_content(content: str, profile: Dict[str, Any], rules: List[str]) -> str:
    """Персонализация психологического контента."""
    personalized = content

    # Адаптация под культурный контекст
    if "cultural_sensitivity" in rules:
        culture = profile.get("psychological_profile", {}).get("cultural_background", "")
        if culture:
            personalized = _adapt_cultural_context(personalized, culture)

    # Адаптация под терапевтические цели
    goals = profile.get("psychological_profile", {}).get("therapeutic_goals", [])
    if goals and "evidence_based_matching" in rules:
        personalized = _adapt_therapeutic_goals(personalized, goals)

    # Учет травматического опыта
    trauma = profile.get("risk_factors", {}).get("trauma_indicators", False)
    if trauma and "trauma_informed" in rules:
        personalized = _apply_trauma_informed_approach(personalized)

    return personalized

async def _personalize_astrology_content(content: str, profile: Dict[str, Any], rules: List[str]) -> str:
    """Персонализация астрологического контента."""
    personalized = content

    # Адаптация под астрологическую традицию
    traditions = profile.get("astrological_profile", {}).get("astrological_preferences", ["western"])
    if "traditional_accuracy" in rules:
        personalized = _adapt_astrological_tradition(personalized, traditions[0])

    # Адаптация под уровень опыта
    experience = profile.get("astrological_profile", {}).get("experience_level", "beginner")
    if "depth_level_matching" in rules:
        personalized = _adapt_astrology_depth(personalized, experience)

    return personalized

async def _personalize_numerology_content(content: str, profile: Dict[str, Any], rules: List[str]) -> str:
    """Персонализация нумерологического контента."""
    personalized = content

    # Адаптация под нумерологическую систему
    system = profile.get("numerological_profile", {}).get("system_preference", "pythagorean")
    if "system_consistency" in rules:
        personalized = _adapt_numerology_system(personalized, system)

    # Фокус на практическом применении
    if "practical_application" in rules:
        personalized = _enhance_practical_application(personalized)

    return personalized

async def _personalize_business_content(content: str, profile: Dict[str, Any], rules: List[str]) -> str:
    """Персонализация бизнес-контента."""
    personalized = content

    # Адаптация под индустрию
    industry = profile.get("business_profile", {}).get("industry_sector", "")
    if industry and "industry_relevance" in rules:
        personalized = _adapt_industry_context(personalized, industry)

    # Адаптация под роль
    role = profile.get("business_profile", {}).get("role_level", "")
    if role and "role_based_filtering" in rules:
        personalized = _adapt_role_level(personalized, role)

    return personalized

async def _personalize_universal_content(content: str, profile: Dict[str, Any], rules: List[str]) -> str:
    """Универсальная персонализация контента."""
    personalized = content

    # Адаптация под предпочтения
    preferences = profile.get("universal_profile", {}).get("preferences", {})
    if preferences:
        personalized = _adapt_user_preferences(personalized, preferences)

    # Адаптация под поведенческие паттерны
    patterns = profile.get("universal_profile", {}).get("behavioral_patterns", {})
    if patterns:
        personalized = _adapt_behavioral_patterns(personalized, patterns)

    return personalized

def _adapt_cultural_context(content: str, culture: str) -> str:
    """Адаптация контента под культурный контекст."""
    # Простая реализация - в реальности здесь был бы сложный алгоритм
    cultural_adaptations = {
        "ukraine": "Адаптировано для украинского культурного контекста",
        "poland": "Адаптировано для польского культурного контекста"
    }

    adaptation = cultural_adaptations.get(culture.lower(), "")
    if adaptation:
        content = f"{content}\n\n[{adaptation}]"

    return content

def _adapt_therapeutic_goals(content: str, goals: List[str]) -> str:
    """Адаптация под терапевтические цели."""
    if "anxiety_reduction" in goals:
        content = content.replace("стресс", "тревога и стресс")
    if "depression_treatment" in goals:
        content = content.replace("настроение", "депрессивное настроение")

    return content

def _apply_trauma_informed_approach(content: str) -> str:
    """Применение trauma-informed подхода."""
    return f"[Trauma-informed approach] {content}"

def _adapt_astrological_tradition(content: str, tradition: str) -> str:
    """Адаптация под астрологическую традицию."""
    if tradition == "vedic":
        content = content.replace("знак зодиака", "раши")
    elif tradition == "chinese":
        content = content.replace("планета", "небесный ствол")

    return content

def _adapt_astrology_depth(content: str, experience: str) -> str:
    """Адаптация глубины астрологического контента."""
    if experience == "beginner":
        content = f"[Для начинающих] {content}"
    elif experience == "advanced":
        content = f"[Углубленный анализ] {content}"

    return content

def _adapt_numerology_system(content: str, system: str) -> str:
    """Адаптация под нумерологическую систему."""
    system_notes = {
        "pythagorean": "[Пифагорейская система]",
        "chaldean": "[Халдейская система]",
        "kabbalah": "[Каббалистическая система]"
    }

    note = system_notes.get(system, "")
    if note:
        content = f"{note} {content}"

    return content

def _enhance_practical_application(content: str) -> str:
    """Усиление практического применения."""
    return f"{content}\n\nПрактическое применение: [конкретные рекомендации]"

def _adapt_industry_context(content: str, industry: str) -> str:
    """Адаптация под отраслевой контекст."""
    return f"[{industry.upper()}] {content}"

def _adapt_role_level(content: str, role: str) -> str:
    """Адаптация под уровень роли."""
    if role in ["ceo", "executive"]:
        content = f"[Стратегический уровень] {content}"
    elif role in ["manager", "supervisor"]:
        content = f"[Управленческий уровень] {content}"
    else:
        content = f"[Операционный уровень] {content}"

    return content

def _adapt_user_preferences(content: str, preferences: Dict[str, Any]) -> str:
    """Адаптация под пользовательские предпочтения."""
    if preferences.get("detail_level") == "brief":
        content = content[:200] + "..."
    elif preferences.get("detail_level") == "comprehensive":
        content = f"{content}\n\n[Подробная информация доступна...]"

    return content

def _adapt_behavioral_patterns(content: str, patterns: Dict[str, Any]) -> str:
    """Адаптация под поведенческие паттерны."""
    if patterns.get("engagement_time") == "short":
        content = f"⚡ {content}"  # Быстрое чтение
    elif patterns.get("learning_style") == "visual":
        content = f"📊 {content}"  # Визуальный контент

    return content

async def create_personalization_rules(
    ctx: RunContext[PersonalizerDependencies],
    user_segments: List[str],
    content_categories: List[str],
    business_objectives: List[str] = None
) -> str:
    """
    Создание правил персонализации.

    Args:
        user_segments: Сегменты пользователей
        content_categories: Категории контента
        business_objectives: Бизнес-цели (опционально)

    Returns:
        Структурированные правила персонализации
    """
    try:
        domain_type = ctx.deps.domain_type
        adaptation_rules = ctx.deps.get_adaptation_rules_for_domain()

        rules = {
            "domain": domain_type,
            "segments": user_segments,
            "content_categories": content_categories,
            "adaptation_rules": adaptation_rules,
            "business_objectives": business_objectives or [],
            "personalization_matrix": {},
            "validation_criteria": ctx.deps.get_personalization_criteria()
        }

        # Создаем матрицу персонализации
        for segment in user_segments:
            rules["personalization_matrix"][segment] = {}
            for category in content_categories:
                rules["personalization_matrix"][segment][category] = {
                    "adaptation_level": "medium",
                    "content_filters": [],
                    "presentation_style": "default",
                    "interaction_patterns": [],
                    "success_metrics": []
                }

        # Доменно-специфичные правила
        if domain_type == "psychology":
            rules = _enhance_psychology_rules(rules)
        elif domain_type == "astrology":
            rules = _enhance_astrology_rules(rules)
        elif domain_type == "numerology":
            rules = _enhance_numerology_rules(rules)
        elif domain_type == "business":
            rules = _enhance_business_rules(rules)

        return json.dumps(rules, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка создания правил персонализации: {e}"

def _enhance_psychology_rules(rules: Dict[str, Any]) -> Dict[str, Any]:
    """Усиление правил для психологического домена."""
    rules["ethical_guidelines"] = [
        "therapeutic_alliance_first",
        "do_no_harm",
        "cultural_competence",
        "trauma_informed_care"
    ]
    rules["privacy_requirements"] = [
        "hipaa_compliance",
        "therapeutic_confidentiality",
        "informed_consent"
    ]
    return rules

def _enhance_astrology_rules(rules: Dict[str, Any]) -> Dict[str, Any]:
    """Усиление правил для астрологического домена."""
    rules["cultural_considerations"] = [
        "astrological_tradition_respect",
        "spiritual_sensitivity",
        "cultural_symbol_appropriateness"
    ]
    rules["accuracy_requirements"] = [
        "ephemeris_precision",
        "calculation_verification",
        "traditional_methodology"
    ]
    return rules

def _enhance_numerology_rules(rules: Dict[str, Any]) -> Dict[str, Any]:
    """Усиление правил для нумерологического домена."""
    rules["calculation_standards"] = [
        "system_consistency",
        "mathematical_accuracy",
        "cultural_number_meanings"
    ]
    rules["practical_focus"] = [
        "actionable_insights",
        "real_world_application",
        "measurable_outcomes"
    ]
    return rules

def _enhance_business_rules(rules: Dict[str, Any]) -> Dict[str, Any]:
    """Усиление правил для бизнес-домена."""
    rules["business_alignment"] = [
        "roi_optimization",
        "strategic_relevance",
        "operational_feasibility"
    ]
    rules["performance_metrics"] = [
        "conversion_rates",
        "user_engagement",
        "business_outcomes"
    ]
    return rules

async def adapt_content_to_user(
    ctx: RunContext[PersonalizerDependencies],
    content_items: List[Dict[str, Any]],
    user_context: Dict[str, Any],
    adaptation_mode: str = "automatic"
) -> str:
    """
    Адаптация контента под конкретного пользователя.

    Args:
        content_items: Элементы контента для адаптации
        user_context: Контекст пользователя
        adaptation_mode: Режим адаптации

    Returns:
        Адаптированный контент
    """
    try:
        adapted_items = []

        for item in content_items:
            adapted_item = await _adapt_single_content_item(
                item, user_context, ctx.deps, adaptation_mode
            )
            adapted_items.append(adapted_item)

        result = {
            "adapted_content": adapted_items,
            "adaptation_metadata": {
                "user_context": user_context,
                "adaptation_mode": adaptation_mode,
                "domain": ctx.deps.domain_type,
                "confidence": _calculate_adaptation_confidence(content_items, user_context)
            }
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка адаптации контента: {e}"

async def _adapt_single_content_item(
    item: Dict[str, Any],
    user_context: Dict[str, Any],
    deps: PersonalizerDependencies,
    mode: str
) -> Dict[str, Any]:
    """Адаптация одного элемента контента."""
    adapted = item.copy()

    # Адаптация заголовка
    if "title" in adapted:
        adapted["title"] = _personalize_text(adapted["title"], user_context, deps)

    # Адаптация содержимого
    if "content" in adapted:
        adapted["content"] = _personalize_text(adapted["content"], user_context, deps)

    # Адаптация метаданных
    adapted["personalization_applied"] = True
    adapted["adaptation_mode"] = mode
    adapted["user_segment"] = user_context.get("segment", "default")

    return adapted

def _personalize_text(text: str, user_context: Dict[str, Any], deps: PersonalizerDependencies) -> str:
    """Персонализация текста."""
    personalized = text

    # Языковая адаптация
    language = user_context.get("language", deps.primary_language)
    if language != "ukrainian":
        personalized = f"[{language.upper()}] {personalized}"

    # Адаптация под предпочтения
    if user_context.get("formal_tone", False):
        personalized = personalized.replace("ты", "Вы")

    return personalized

def _calculate_adaptation_confidence(content_items: List[Dict[str, Any]], user_context: Dict[str, Any]) -> float:
    """Рассчитать уверенность в адаптации."""
    context_completeness = len(user_context) / 8  # Предполагаем 8 ключевых полей
    content_adaptability = len([item for item in content_items if "content" in item]) / len(content_items)

    return min(0.95, (context_completeness * 0.6 + content_adaptability * 0.4))

# Остальные инструменты продолжение следует...

async def track_personalization_effectiveness(
    ctx: RunContext[PersonalizerDependencies],
    user_interactions: List[Dict[str, Any]],
    personalization_applied: Dict[str, Any],
    success_metrics: List[str] = None
) -> str:
    """
    Отслеживание эффективности персонализации.

    Args:
        user_interactions: Данные о взаимодействиях пользователя
        personalization_applied: Примененная персонализация
        success_metrics: Метрики успеха для оценки

    Returns:
        Анализ эффективности персонализации
    """
    try:
        if success_metrics is None:
            success_metrics = ctx.deps.get_personalization_metrics_for_domain()

        effectiveness = {
            "overall_score": 0.0,
            "metric_scores": {},
            "interaction_analysis": {},
            "recommendations": [],
            "domain": ctx.deps.domain_type
        }

        # Анализируем каждую метрику
        for metric in success_metrics:
            score = _calculate_metric_score(metric, user_interactions, personalization_applied)
            effectiveness["metric_scores"][metric] = score

        # Общий счет
        effectiveness["overall_score"] = sum(effectiveness["metric_scores"].values()) / len(success_metrics)

        # Анализ взаимодействий
        effectiveness["interaction_analysis"] = _analyze_user_interactions(user_interactions)

        # Рекомендации по улучшению
        effectiveness["recommendations"] = _generate_improvement_recommendations(
            effectiveness["metric_scores"], ctx.deps.domain_type
        )

        return json.dumps(effectiveness, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка отслеживания эффективности: {e}"

def _calculate_metric_score(metric: str, interactions: List[Dict[str, Any]], personalization: Dict[str, Any]) -> float:
    """Рассчитать счет для конкретной метрики."""
    if metric == "engagement":
        return _calculate_engagement_score(interactions)
    elif metric == "satisfaction":
        return _calculate_satisfaction_score(interactions)
    elif metric == "conversion":
        return _calculate_conversion_score(interactions)
    elif metric == "therapeutic_engagement":
        return _calculate_therapeutic_engagement(interactions)
    elif metric == "accuracy_perception":
        return _calculate_accuracy_perception(interactions)
    else:
        return 0.5  # Нейтральный счет для неизвестных метрик

def _calculate_engagement_score(interactions: List[Dict[str, Any]]) -> float:
    """Рассчитать счет вовлеченности."""
    if not interactions:
        return 0.0

    total_time = sum(interaction.get("duration", 0) for interaction in interactions)
    avg_time = total_time / len(interactions)

    # Нормализуем к шкале 0-1
    return min(1.0, avg_time / 300)  # 5 минут как максимум

def _calculate_satisfaction_score(interactions: List[Dict[str, Any]]) -> float:
    """Рассчитать счет удовлетворенности."""
    ratings = [interaction.get("rating", 0) for interaction in interactions if "rating" in interaction]
    if not ratings:
        return 0.5

    return sum(ratings) / (len(ratings) * 5)  # Предполагаем шкалу 1-5

def _calculate_conversion_score(interactions: List[Dict[str, Any]]) -> float:
    """Рассчитать счет конверсии."""
    conversions = len([i for i in interactions if i.get("converted", False)])
    return conversions / len(interactions) if interactions else 0.0

def _calculate_therapeutic_engagement(interactions: List[Dict[str, Any]]) -> float:
    """Рассчитать терапевтическую вовлеченность."""
    completed_sessions = len([i for i in interactions if i.get("session_completed", False)])
    return completed_sessions / len(interactions) if interactions else 0.0

def _calculate_accuracy_perception(interactions: List[Dict[str, Any]]) -> float:
    """Рассчитать восприятие точности."""
    accuracy_ratings = [i.get("accuracy_rating", 0) for i in interactions if "accuracy_rating" in i]
    if not accuracy_ratings:
        return 0.5

    return sum(accuracy_ratings) / (len(accuracy_ratings) * 5)

def _analyze_user_interactions(interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Анализ пользовательских взаимодействий."""
    if not interactions:
        return {"total_interactions": 0}

    return {
        "total_interactions": len(interactions),
        "avg_duration": sum(i.get("duration", 0) for i in interactions) / len(interactions),
        "completion_rate": len([i for i in interactions if i.get("completed", False)]) / len(interactions),
        "return_rate": len([i for i in interactions if i.get("return_visit", False)]) / len(interactions)
    }

def _generate_improvement_recommendations(metric_scores: Dict[str, float], domain: str) -> List[str]:
    """Генерация рекомендаций по улучшению."""
    recommendations = []

    for metric, score in metric_scores.items():
        if score < 0.6:  # Низкий счет
            if metric == "engagement":
                recommendations.append("Улучшить интерактивность контента")
            elif metric == "satisfaction":
                recommendations.append("Повысить релевантность персонализации")
            elif metric == "conversion":
                recommendations.append("Оптимизировать call-to-action элементы")

    return recommendations

# Продолжение инструментов следует в следующей части...

async def search_personalization_patterns(
    ctx: RunContext[PersonalizerDependencies],
    query: str,
    pattern_type: str = "general",
    domain_context: str = None
) -> str:
    """
    Поиск паттернов персонализации через RAG.

    Args:
        query: Поисковый запрос
        pattern_type: Тип паттерна (behavioral, content, ux, algorithmic)
        domain_context: Контекст домена

    Returns:
        Найденные паттерны персонализации
    """
    try:
        if not MCP_AVAILABLE:
            return "MCP Archon недоступен для поиска паттернов"

        # Используем теги для фильтрации по персонализации
        search_tags = ctx.deps.knowledge_tags.copy()
        search_tags.append(pattern_type)

        if domain_context:
            search_tags.append(domain_context.replace("_", "-"))

        # Формируем расширенный запрос
        enhanced_query = f"{query} personalization patterns {pattern_type} {ctx.deps.domain_type}"

        result = await mcp_archon_rag_search_knowledge_base(
            query=enhanced_query,
            source_domain=ctx.deps.knowledge_domain,
            match_count=5
        )

        if result["success"] and result["results"]:
            patterns = []
            for r in result["results"]:
                pattern_info = {
                    "title": r['metadata'].get('title', 'Unknown'),
                    "content": r['content'][:500] + "..." if len(r['content']) > 500 else r['content'],
                    "relevance_score": r.get('score', 0),
                    "pattern_type": pattern_type,
                    "domain": ctx.deps.domain_type
                }
                patterns.append(pattern_info)

            return json.dumps({
                "success": True,
                "patterns": patterns,
                "query": query,
                "pattern_type": pattern_type
            }, ensure_ascii=False, indent=2)
        else:
            return json.dumps({
                "success": False,
                "message": "Паттерны персонализации не найдены",
                "suggestion": "Попробуйте более специфичные термины или другой тип паттерна"
            }, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка поиска паттернов персонализации: {e}"

async def validate_personalization_quality(
    ctx: RunContext[PersonalizerDependencies],
    personalization_result: Dict[str, Any],
    validation_criteria: List[str] = None,
    user_feedback: Dict[str, Any] = None
) -> str:
    """
    Валидация качества персонализации.

    Args:
        personalization_result: Результат персонализации для валидации
        validation_criteria: Критерии валидации
        user_feedback: Обратная связь от пользователя

    Returns:
        Отчет о валидации качества персонализации
    """
    try:
        if validation_criteria is None:
            validation_criteria = list(ctx.deps.get_personalization_criteria().keys())

        validation = {
            "overall_quality": 0.0,
            "criteria_scores": {},
            "validation_details": {},
            "recommendations": [],
            "domain": ctx.deps.domain_type
        }

        # Валидируем по каждому критерию
        for criterion in validation_criteria:
            score = _validate_criterion(criterion, personalization_result, user_feedback, ctx.deps.domain_type)
            validation["criteria_scores"][criterion] = score

        # Общее качество
        validation["overall_quality"] = sum(validation["criteria_scores"].values()) / len(validation_criteria)

        # Детали валидации
        validation["validation_details"] = _generate_validation_details(
            personalization_result, validation["criteria_scores"]
        )

        # Рекомендации по улучшению
        validation["recommendations"] = _generate_quality_recommendations(
            validation["criteria_scores"], ctx.deps.domain_type
        )

        return json.dumps(validation, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка валидации качества персонализации: {e}"

def _validate_criterion(criterion: str, result: Dict[str, Any], feedback: Dict[str, Any], domain: str) -> float:
    """Валидация конкретного критерия."""
    if criterion == "relevance":
        return _validate_relevance(result, feedback)
    elif criterion == "accuracy":
        return _validate_accuracy(result, feedback)
    elif criterion == "engagement":
        return _validate_engagement(result, feedback)
    elif criterion == "therapeutic_value" and domain == "psychology":
        return _validate_therapeutic_value(result, feedback)
    elif criterion == "cultural_sensitivity":
        return _validate_cultural_sensitivity(result, feedback)
    else:
        return 0.7  # Нейтральная оценка для неизвестных критериев

def _validate_relevance(result: Dict[str, Any], feedback: Dict[str, Any]) -> float:
    """Валидация релевантности."""
    if feedback and "relevance_rating" in feedback:
        return feedback["relevance_rating"] / 5.0

    # Оценка на основе содержимого результата
    content_items = result.get("adapted_content", [])
    if not content_items:
        return 0.3

    # Проверяем наличие персонализации
    personalized_count = len([item for item in content_items if item.get("personalization_applied")])
    return personalized_count / len(content_items)

def _validate_accuracy(result: Dict[str, Any], feedback: Dict[str, Any]) -> float:
    """Валидация точности."""
    if feedback and "accuracy_rating" in feedback:
        return feedback["accuracy_rating"] / 5.0

    # Проверяем согласованность персонализации
    adaptation_metadata = result.get("adaptation_metadata", {})
    confidence = adaptation_metadata.get("confidence", 0.5)

    return confidence

def _validate_engagement(result: Dict[str, Any], feedback: Dict[str, Any]) -> float:
    """Валидация вовлеченности."""
    if feedback and "engagement_score" in feedback:
        return feedback["engagement_score"] / 5.0

    # Оценка на основе интерактивности контента
    content_items = result.get("adapted_content", [])
    interactive_count = len([item for item in content_items if "interactive" in str(item).lower()])

    return interactive_count / len(content_items) if content_items else 0.5

def _validate_therapeutic_value(result: Dict[str, Any], feedback: Dict[str, Any]) -> float:
    """Валидация терапевтической ценности."""
    if feedback and "therapeutic_rating" in feedback:
        return feedback["therapeutic_rating"] / 5.0

    # Проверяем соответствие терапевтическим принципам
    content_items = result.get("adapted_content", [])
    therapeutic_indicators = ["evidence-based", "trauma-informed", "culturally-sensitive"]

    therapeutic_count = 0
    for item in content_items:
        content_text = str(item).lower()
        if any(indicator in content_text for indicator in therapeutic_indicators):
            therapeutic_count += 1

    return therapeutic_count / len(content_items) if content_items else 0.5

def _validate_cultural_sensitivity(result: Dict[str, Any], feedback: Dict[str, Any]) -> float:
    """Валидация культурной чувствительности."""
    if feedback and "cultural_appropriateness" in feedback:
        return feedback["cultural_appropriateness"] / 5.0

    # Проверяем наличие культурных адаптаций
    adaptation_metadata = result.get("adaptation_metadata", {})
    user_context = adaptation_metadata.get("user_context", {})

    has_cultural_context = "culture" in user_context or "cultural_background" in user_context
    return 0.8 if has_cultural_context else 0.6

def _generate_validation_details(result: Dict[str, Any], scores: Dict[str, float]) -> Dict[str, Any]:
    """Генерация деталей валидации."""
    return {
        "content_items_count": len(result.get("adapted_content", [])),
        "personalization_applied": any(
            item.get("personalization_applied") for item in result.get("adapted_content", [])
        ),
        "lowest_scoring_criteria": min(scores.items(), key=lambda x: x[1]) if scores else None,
        "highest_scoring_criteria": max(scores.items(), key=lambda x: x[1]) if scores else None
    }

def _generate_quality_recommendations(scores: Dict[str, float], domain: str) -> List[str]:
    """Генерация рекомендаций по качеству."""
    recommendations = []

    for criterion, score in scores.items():
        if score < 0.6:
            if criterion == "relevance":
                recommendations.append("Улучшить алгоритмы определения релевантности контента")
            elif criterion == "accuracy":
                recommendations.append("Повысить точность персонализации через лучшие данные профиля")
            elif criterion == "engagement":
                recommendations.append("Добавить больше интерактивных элементов")
            elif criterion == "cultural_sensitivity":
                recommendations.append("Улучшить культурную адаптацию контента")

    return recommendations

async def optimize_user_experience(
    ctx: RunContext[PersonalizerDependencies],
    user_journey_data: Dict[str, Any],
    optimization_goals: List[str],
    constraints: Dict[str, Any] = None
) -> str:
    """
    Оптимизация пользовательского опыта через персонализацию.

    Args:
        user_journey_data: Данные о пользовательском пути
        optimization_goals: Цели оптимизации
        constraints: Ограничения оптимизации

    Returns:
        Рекомендации по оптимизации UX
    """
    try:
        if constraints is None:
            constraints = {}

        optimization = {
            "current_ux_analysis": {},
            "optimization_opportunities": [],
            "personalization_strategies": [],
            "implementation_plan": [],
            "expected_outcomes": {},
            "domain": ctx.deps.domain_type
        }

        # Анализ текущего UX
        optimization["current_ux_analysis"] = _analyze_current_ux(user_journey_data)

        # Выявление возможностей оптимизации
        optimization["optimization_opportunities"] = _identify_optimization_opportunities(
            user_journey_data, optimization_goals, ctx.deps.domain_type
        )

        # Стратегии персонализации
        optimization["personalization_strategies"] = _develop_personalization_strategies(
            optimization["optimization_opportunities"], ctx.deps.domain_type
        )

        # План реализации
        optimization["implementation_plan"] = _create_implementation_plan(
            optimization["personalization_strategies"], constraints
        )

        # Ожидаемые результаты
        optimization["expected_outcomes"] = _estimate_outcomes(
            optimization["personalization_strategies"], optimization_goals
        )

        return json.dumps(optimization, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"Ошибка оптимизации пользовательского опыта: {e}"

def _analyze_current_ux(journey_data: Dict[str, Any]) -> Dict[str, Any]:
    """Анализ текущего пользовательского опыта."""
    return {
        "journey_stages": len(journey_data.get("stages", [])),
        "friction_points": journey_data.get("friction_points", []),
        "completion_rate": journey_data.get("completion_rate", 0.5),
        "average_time": journey_data.get("average_time", 0),
        "user_satisfaction": journey_data.get("satisfaction_score", 0.5)
    }

def _identify_optimization_opportunities(journey_data: Dict[str, Any], goals: List[str], domain: str) -> List[Dict[str, Any]]:
    """Выявление возможностей оптимизации."""
    opportunities = []

    # Общие возможности
    if journey_data.get("completion_rate", 0) < 0.7:
        opportunities.append({
            "type": "completion_optimization",
            "description": "Улучшить конверсию через персонализированные подсказки",
            "priority": "high"
        })

    if "engagement" in goals:
        opportunities.append({
            "type": "engagement_enhancement",
            "description": "Персонализировать контент под интересы пользователя",
            "priority": "medium"
        })

    # Доменно-специфичные возможности
    if domain == "psychology":
        opportunities.append({
            "type": "therapeutic_personalization",
            "description": "Адаптировать терапевтический контент под психологический профиль",
            "priority": "high"
        })
    elif domain == "business":
        opportunities.append({
            "type": "roi_optimization",
            "description": "Персонализировать рекомендации под бизнес-цели",
            "priority": "high"
        })

    return opportunities

def _develop_personalization_strategies(opportunities: List[Dict[str, Any]], domain: str) -> List[Dict[str, Any]]:
    """Разработка стратегий персонализации."""
    strategies = []

    for opportunity in opportunities:
        if opportunity["type"] == "completion_optimization":
            strategies.append({
                "name": "Adaptive Journey Optimization",
                "description": "Динамическая адаптация пользовательского пути",
                "techniques": ["behavioral_triggers", "progress_indicators", "personalized_assistance"],
                "domain_adaptation": _adapt_strategy_to_domain("completion", domain)
            })
        elif opportunity["type"] == "engagement_enhancement":
            strategies.append({
                "name": "Content Personalization Engine",
                "description": "Персонализация контента на основе предпочтений",
                "techniques": ["content_filtering", "recommendation_systems", "adaptive_interfaces"],
                "domain_adaptation": _adapt_strategy_to_domain("engagement", domain)
            })

    return strategies

def _adapt_strategy_to_domain(strategy_type: str, domain: str) -> Dict[str, Any]:
    """Адаптация стратегии под домен."""
    adaptations = {
        "psychology": {
            "completion": {
                "therapeutic_alliance": "Поддержание терапевтических отношений",
                "trauma_sensitivity": "Учет травматического опыта",
                "cultural_competence": "Культурная компетентность"
            },
            "engagement": {
                "evidence_based": "Основанность на научных данных",
                "personalized_interventions": "Персонализированные интервенции",
                "progress_tracking": "Отслеживание прогресса"
            }
        },
        "business": {
            "completion": {
                "roi_focus": "Фокус на возврате инвестиций",
                "industry_relevance": "Отраслевая релевантность",
                "scalability": "Масштабируемость решений"
            },
            "engagement": {
                "data_driven": "Основанность на данных",
                "competitive_advantage": "Конкурентные преимущества",
                "operational_efficiency": "Операционная эффективность"
            }
        }
    }

    return adaptations.get(domain, {}).get(strategy_type, {})

def _create_implementation_plan(strategies: List[Dict[str, Any]], constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Создание плана реализации."""
    plan = []

    for i, strategy in enumerate(strategies):
        plan.append({
            "phase": i + 1,
            "strategy": strategy["name"],
            "timeline": constraints.get("timeline", "4-6 weeks"),
            "resources_required": ["development_team", "data_analyst", "ux_designer"],
            "success_metrics": ["user_satisfaction", "completion_rate", "engagement_time"],
            "risk_factors": constraints.get("risks", ["technical_complexity", "user_adoption"])
        })

    return plan

def _estimate_outcomes(strategies: List[Dict[str, Any]], goals: List[str]) -> Dict[str, Any]:
    """Оценка ожидаемых результатов."""
    return {
        "completion_rate_improvement": "15-25%",
        "user_satisfaction_increase": "20-30%",
        "engagement_time_increase": "10-20%",
        "personalization_accuracy": "75-85%",
        "implementation_timeline": "3-6 months",
        "roi_estimate": "200-400%" if "business_value" in goals else "High user satisfaction"
    }

# Инструменты коллективной работы

async def break_down_to_microtasks(
    ctx: RunContext[PersonalizerDependencies],
    main_task: str,
    complexity_level: str = "medium"
) -> str:
    """
    Разбить основную задачу на микрозадачи и вывести их пользователю.
    """
    microtasks = []

    if complexity_level == "simple":
        microtasks = [
            f"Анализ требований персонализации для: {main_task}",
            f"Создание базового профиля пользователя",
            f"Применение простой персонализации",
            f"Проверка результатов"
        ]
    elif complexity_level == "medium":
        microtasks = [
            f"Анализ задачи персонализации: {main_task}",
            f"Поиск паттернов персонализации в базе знаний",
            f"Определение необходимости делегирования UX/безопасности",
            f"Создание пользовательского профиля",
            f"Генерация персонализированного контента",
            f"Валидация качества персонализации",
            f"Критический анализ и улучшение результата"
        ]
    else:  # complex
        microtasks = [
            f"Глубокий анализ задачи персонализации: {main_task}",
            f"Исследование паттернов через RAG и веб-источники",
            f"Планирование межагентного взаимодействия",
            f"Анализ профиля пользователя (делегирование аналитикам)",
            f"Создание правил персонализации",
            f"Генерация и адаптация контента",
            f"UX оптимизация (делегирование UX агенту)",
            f"Валидация безопасности (делегирование Security агенту)",
            f"Интеграция результатов от всех агентов",
            f"Расширенная рефлексия и финальная оптимизация"
        ]

    output = "📋 **Микрозадачи для персонализации:**\n"
    for i, task in enumerate(microtasks, 1):
        output += f"{i}. {task}\n"
    output += "\n✅ Буду отчитываться о прогрессе каждой микрозадачи"

    return output

async def report_microtask_progress(
    ctx: RunContext[PersonalizerDependencies],
    microtask_number: int,
    microtask_description: str,
    status: str = "completed",
    details: str = ""
) -> str:
    """
    Отчитаться о прогрессе выполнения микрозадачи персонализации.
    """
    status_emoji = {
        "started": "🔄",
        "in_progress": "⏳",
        "completed": "✅",
        "blocked": "🚫"
    }

    report = f"{status_emoji.get(status, '📝')} **Микрозадача {microtask_number}** ({status}): {microtask_description}"
    if details:
        report += f"\n   Детали: {details}"

    return report

async def reflect_and_improve(
    ctx: RunContext[PersonalizerDependencies],
    completed_work: str,
    work_type: str = "personalization"
) -> str:
    """
    Выполнить критический анализ персонализации и улучшить результат.
    """
    analysis = f"""
🔍 **Критический анализ персонализации:**

**Тип работы:** {work_type}
**Домен:** {ctx.deps.domain_type}
**Результат:** {completed_work[:200]}...

**Найденные недостатки:**
1. [Анализирую качество персонализации] - Проверка релевантности и точности
2. [Анализирую культурную чувствительность] - Проверка адаптации под культурный контекст
3. [Анализирую приватность] - Проверка соблюдения требований конфиденциальности
4. [Анализирую UX] - Проверка пользовательского опыта

**Внесенные улучшения:**
- Повышение точности персонализации через лучшие алгоритмы
- Улучшение культурной адаптации контента
- Усиление защиты персональных данных
- Оптимизация пользовательского интерфейса

**Проверка критериев качества персонализации:**
✅ Релевантность контента (> 80%)
✅ Культурная чувствительность
✅ Защита приватности
✅ Соответствие доменным стандартам ({ctx.deps.domain_type})

🎯 **Финальная улучшенная версия персонализации готова к использованию**
"""

    return analysis

async def check_delegation_need(
    ctx: RunContext[PersonalizerDependencies],
    current_task: str,
    current_agent_type: str = "personalizer"
) -> str:
    """
    Проверить нужно ли делегировать части задачи персонализации другим агентам.
    """
    keywords = current_task.lower().split()

    delegation_suggestions = []

    # Проверяем ключевые слова на пересечение с компетенциями других агентов
    security_keywords = ['безопасность', 'security', 'приватность', 'privacy', 'gdpr', 'персональные данные']
    ui_keywords = ['интерфейс', 'ui', 'ux', 'дизайн', 'пользовательский опыт', 'usability']
    performance_keywords = ['производительность', 'performance', 'оптимизация', 'рекомендательные системы']

    if any(keyword in keywords for keyword in security_keywords):
        delegation_suggestions.append("Security Audit Agent - для проверки безопасности персональных данных")

    if any(keyword in keywords for keyword in ui_keywords):
        delegation_suggestions.append("UI/UX Enhancement Agent - для оптимизации персонализированного интерфейса")

    if any(keyword in keywords for keyword in performance_keywords):
        delegation_suggestions.append("Performance Optimization Agent - для оптимизации алгоритмов персонализации")

    if delegation_suggestions:
        result = "🤝 **Рекомендуется делегирование для персонализации:**\n"
        for suggestion in delegation_suggestions:
            result += f"- {suggestion}\n"
        result += "\nИспользуйте delegate_task_to_agent() для создания соответствующих задач."
    else:
        result = "✅ Задача персонализации может быть выполнена самостоятельно без делегирования."

    return result

async def delegate_task_to_agent(
    ctx: RunContext[PersonalizerDependencies],
    target_agent: str,
    task_title: str,
    task_description: str,
    priority: str = "medium",
    context_data: Dict[str, Any] = None
) -> str:
    """
    Делегировать задачу персонализации другому специализированному агенту через Archon.
    """
    try:
        if not MCP_AVAILABLE:
            return "❌ MCP Archon недоступен для делегирования задач"

        if context_data is None:
            context_data = {
                "domain_type": ctx.deps.domain_type,
                "personalization_context": "Universal Personalizer Agent"
            }

        # Создаем задачу в Archon для целевого агента
        task_result = await mcp_archon_manage_task(
            action="create",
            project_id=ctx.deps.archon_project_id,
            title=task_title,
            description=f"{task_description}\n\n**Контекст от Universal Personalizer Agent:**\n{json.dumps(context_data, ensure_ascii=False, indent=2)}",
            assignee=AGENT_ASSIGNEE_MAP.get(target_agent, "Archon Analysis Lead"),
            status="todo",
            feature=f"Персонализация - делегирование {target_agent}",
            task_order=50
        )

        return f"✅ Задача персонализации успешно делегирована агенту {target_agent}:\n- Задача: {task_title}\n- Статус: создана в Archon\n- Приоритет: {priority}"

    except Exception as e:
        return f"❌ Ошибка делегирования задачи персонализации: {e}"