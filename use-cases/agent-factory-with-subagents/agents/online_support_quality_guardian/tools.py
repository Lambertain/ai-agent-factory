"""
Инструменты для Psychology Quality Guardian Agent

Набор специализированных инструментов для контроля качества,
этической валидации и научной оценки психологического контента.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic_ai import RunContext
import json
import re
from datetime import datetime

try:
    from mcp__archon__rag_search_knowledge_base import mcp__archon__rag_search_knowledge_base
    ARCHON_AVAILABLE = True
except ImportError:
    ARCHON_AVAILABLE = False

from .dependencies import QualityGuardianDependencies


async def search_quality_guardian_knowledge(
    ctx: RunContext[QualityGuardianDependencies],
    query: str,
    focus_area: str = "general",
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний Psychology Quality Guardian по контролю качества.

    Args:
        query: Поисковый запрос
        focus_area: Область фокуса (ethical, scientific, safety, cultural)
        match_count: Количество результатов

    Returns:
        Найденная информация по контролю качества
    """
    enhanced_query = f"{query} psychology quality {focus_area} validation"

    if ARCHON_AVAILABLE:
        try:
            result = await mcp__archon__rag_search_knowledge_base(
                query=enhanced_query,
                match_count=match_count
            )

            if result.get("success") and result.get("results"):
                knowledge = "\n".join([
                    f"**{r['metadata']['title']}:**\n{r['content']}"
                    for r in result["results"]
                ])
                return f"📚 База знаний Quality Guardian:\n{knowledge}"
            else:
                return f"⚠️ Поиск в базе знаний: результаты не найдены для '{query}' в области '{focus_area}'"

        except Exception as e:
            return f"❌ Ошибка поиска в базе знаний: {e}"
    else:
        return f"📖 Локальные знания по '{query}' в области '{focus_area}': используйте стандарты APA, ITC, и этические принципы психологии"


async def evaluate_ethical_compliance(
    ctx: RunContext[QualityGuardianDependencies],
    content_data: Dict[str, Any],
    ethical_standards: List[str] = None,
    target_population: str = "adults"
) -> str:
    """
    Оценка этического соответствия психологического контента.

    Args:
        content_data: Данные контента для оценки
        ethical_standards: Стандарты для проверки (APA, BPS, ITC и т.д.)
        target_population: Целевая популяция

    Returns:
        Детальная оценка этического соответствия
    """
    if ethical_standards is None:
        ethical_standards = ["APA", "informed_consent", "beneficence", "justice", "respect"]

    ethical_analysis = {
        "compliance_score": 0,
        "ethical_issues": [],
        "recommendations": [],
        "risk_level": "low"
    }

    # Анализ информированного согласия
    if "informed_consent" in ethical_standards:
        consent_issues = _check_informed_consent(content_data, target_population)
        ethical_analysis["ethical_issues"].extend(consent_issues)

    # Анализ принципа благополучия
    if "beneficence" in ethical_standards:
        beneficence_issues = _check_beneficence_principle(content_data)
        ethical_analysis["ethical_issues"].extend(beneficence_issues)

    # Анализ справедливости и равенства
    if "justice" in ethical_standards:
        justice_issues = _check_justice_principle(content_data, target_population)
        ethical_analysis["ethical_issues"].extend(justice_issues)

    # Анализ уважения к человеческому достоинству
    if "respect" in ethical_standards:
        respect_issues = _check_respect_principle(content_data)
        ethical_analysis["ethical_issues"].extend(respect_issues)

    # Расчет общего балла соответствия
    total_checks = len(ethical_standards) * 10  # Максимум 10 баллов за каждый стандарт
    issues_penalty = len(ethical_analysis["ethical_issues"]) * 2
    ethical_analysis["compliance_score"] = max(0, total_checks - issues_penalty)

    # Определение уровня риска
    if len(ethical_analysis["ethical_issues"]) == 0:
        ethical_analysis["risk_level"] = "low"
    elif len(ethical_analysis["ethical_issues"]) <= 3:
        ethical_analysis["risk_level"] = "medium"
    else:
        ethical_analysis["risk_level"] = "high"

    # Генерация рекомендаций
    ethical_analysis["recommendations"] = _generate_ethical_recommendations(
        ethical_analysis["ethical_issues"]
    )

    return f"""
🔍 **Оценка этического соответствия:**

**Общий балл соответствия:** {ethical_analysis['compliance_score']}/{total_checks}
**Уровень этического риска:** {ethical_analysis['risk_level'].upper()}
**Проверенные стандарты:** {', '.join(ethical_standards)}

**📋 Выявленные этические проблемы ({len(ethical_analysis['ethical_issues'])}):**
{_format_issues_list(ethical_analysis['ethical_issues'])}

**💡 Рекомендации по улучшению:**
{_format_recommendations_list(ethical_analysis['recommendations'])}

**🎯 Следующие шаги:**
1. Устранить критические этические проблемы
2. Внедрить рекомендации по приоритету
3. Провести повторную этическую оценку
4. Получить одобрение этического комитета (при необходимости)
"""


async def assess_scientific_validity(
    ctx: RunContext[QualityGuardianDependencies],
    content_data: Dict[str, Any],
    validation_criteria: List[str] = None,
    evidence_level: str = "standard"
) -> str:
    """
    Оценка научной валидности и психометрических свойств.

    Args:
        content_data: Данные контента для анализа
        validation_criteria: Критерии валидности для проверки
        evidence_level: Уровень требуемых доказательств

    Returns:
        Анализ научной валидности с оценками
    """
    if validation_criteria is None:
        validation_criteria = ["content_validity", "construct_validity", "reliability", "theoretical_basis"]

    validity_analysis = {
        "overall_validity": "pending",
        "validity_scores": {},
        "scientific_issues": [],
        "evidence_gaps": [],
        "recommendations": []
    }

    # Оценка содержательной валидности
    if "content_validity" in validation_criteria:
        content_validity_score = _assess_content_validity(content_data)
        validity_analysis["validity_scores"]["content_validity"] = content_validity_score

    # Оценка конструктной валидности
    if "construct_validity" in validation_criteria:
        construct_validity_score = _assess_construct_validity(content_data)
        validity_analysis["validity_scores"]["construct_validity"] = construct_validity_score

    # Оценка надежности
    if "reliability" in validation_criteria:
        reliability_score = _assess_reliability(content_data)
        validity_analysis["validity_scores"]["reliability"] = reliability_score

    # Оценка теоретического обоснования
    if "theoretical_basis" in validation_criteria:
        theoretical_score = _assess_theoretical_basis(content_data)
        validity_analysis["validity_scores"]["theoretical_basis"] = theoretical_score

    # Анализ эмпирической поддержки
    empirical_support = _analyze_empirical_support(content_data, evidence_level)
    validity_analysis["evidence_gaps"] = empirical_support["gaps"]

    # Общая оценка валидности
    avg_score = sum(validity_analysis["validity_scores"].values()) / len(validity_analysis["validity_scores"])
    if avg_score >= 80:
        validity_analysis["overall_validity"] = "high"
    elif avg_score >= 60:
        validity_analysis["overall_validity"] = "adequate"
    else:
        validity_analysis["overall_validity"] = "insufficient"

    return f"""
🔬 **Оценка научной валидности:**

**Общая валидность:** {validity_analysis['overall_validity'].upper()}
**Уровень доказательств:** {evidence_level}

**📊 Оценки по критериям валидности:**
{_format_validity_scores(validity_analysis['validity_scores'])}

**⚠️ Выявленные научные проблемы:**
{_format_issues_list(validity_analysis['scientific_issues'])}

**📈 Пробелы в доказательной базе:**
{_format_evidence_gaps(validity_analysis['evidence_gaps'])}

**🔧 Рекомендации по улучшению валидности:**
1. Провести дополнительные валидационные исследования
2. Усилить теоретическое обоснование
3. Улучшить психометрические характеристики
4. Расширить эмпирическую поддержку

**📋 Следующие научные шаги:**
- Планирование валидационных исследований
- Сбор дополнительных данных
- Peer review научных материалов
- Публикация результатов валидации
"""


async def analyze_content_safety(
    ctx: RunContext[QualityGuardianDependencies],
    content_data: Dict[str, Any],
    risk_categories: List[str] = None,
    sensitivity_level: str = "standard"
) -> str:
    """
    Анализ безопасности контента для психического здоровья участников.

    Args:
        content_data: Контент для анализа безопасности
        risk_categories: Категории рисков для проверки
        sensitivity_level: Уровень чувствительности анализа

    Returns:
        Оценка безопасности с выявленными рисками
    """
    if risk_categories is None:
        risk_categories = ["psychological_harm", "privacy_risk", "vulnerable_groups", "crisis_triggers"]

    safety_analysis = {
        "overall_safety": "safe",
        "risk_scores": {},
        "safety_issues": [],
        "protection_measures": [],
        "crisis_protocols": []
    }

    # Анализ психологических рисков
    if "psychological_harm" in risk_categories:
        psych_risks = _analyze_psychological_risks(content_data, sensitivity_level)
        safety_analysis["risk_scores"]["psychological_harm"] = psych_risks["score"]
        safety_analysis["safety_issues"].extend(psych_risks["issues"])

    # Анализ рисков конфиденциальности
    if "privacy_risk" in risk_categories:
        privacy_risks = _analyze_privacy_risks(content_data)
        safety_analysis["risk_scores"]["privacy_risk"] = privacy_risks["score"]
        safety_analysis["safety_issues"].extend(privacy_risks["issues"])

    # Анализ рисков для уязвимых групп
    if "vulnerable_groups" in risk_categories:
        vulnerability_risks = _analyze_vulnerability_risks(content_data)
        safety_analysis["risk_scores"]["vulnerable_groups"] = vulnerability_risks["score"]
        safety_analysis["safety_issues"].extend(vulnerability_risks["issues"])

    # Анализ триггеров кризисных состояний
    if "crisis_triggers" in risk_categories:
        crisis_risks = _analyze_crisis_triggers(content_data)
        safety_analysis["risk_scores"]["crisis_triggers"] = crisis_risks["score"]
        safety_analysis["safety_issues"].extend(crisis_risks["issues"])

    # Общая оценка безопасности
    max_risk_score = max(safety_analysis["risk_scores"].values()) if safety_analysis["risk_scores"] else 0
    if max_risk_score >= 80:
        safety_analysis["overall_safety"] = "high_risk"
    elif max_risk_score >= 50:
        safety_analysis["overall_safety"] = "moderate_risk"
    else:
        safety_analysis["overall_safety"] = "safe"

    # Рекомендации по защитным мерам
    safety_analysis["protection_measures"] = _generate_protection_measures(safety_analysis["safety_issues"])

    return f"""
🛡️ **Анализ безопасности контента:**

**Общий уровень безопасности:** {safety_analysis['overall_safety'].upper()}
**Уровень чувствительности:** {sensitivity_level}

**⚠️ Оценки рисков по категориям:**
{_format_risk_scores(safety_analysis['risk_scores'])}

**🚨 Выявленные проблемы безопасности:**
{_format_issues_list(safety_analysis['safety_issues'])}

**🛡️ Рекомендуемые защитные меры:**
{_format_protection_measures(safety_analysis['protection_measures'])}

**🆘 Протоколы кризисного реагирования:**
1. Мониторинг эмоционального состояния участников
2. Триггерные предупреждения для чувствительного контента
3. Доступ к кризисной психологической поддержке
4. Процедуры эскалации при выявлении риска
5. Контактная информация служб экстренной помощи

**📞 Контакты экстренной помощи:**
- Телефон доверия: 8-800-2000-122
- Кризисная психологическая помощь: 051
- Служба экстренного реагирования: 112
"""


async def validate_psychometric_properties(
    ctx: RunContext[QualityGuardianDependencies],
    test_data: Dict[str, Any],
    psychometric_standards: Dict[str, float] = None
) -> str:
    """
    Валидация психометрических свойств теста или оценочного инструмента.

    Args:
        test_data: Данные теста для анализа
        psychometric_standards: Стандарты психометрических показателей

    Returns:
        Детальный анализ психометрических характеристик
    """
    if psychometric_standards is None:
        psychometric_standards = {
            "reliability_threshold": 0.80,
            "validity_threshold": 0.70,
            "factor_loading_min": 0.30,
            "item_total_correlation_min": 0.30
        }

    psychometric_analysis = {
        "reliability": {},
        "validity": {},
        "factor_structure": {},
        "item_analysis": {},
        "overall_quality": "pending",
        "recommendations": []
    }

    # Анализ надежности
    reliability_data = _analyze_reliability_indicators(test_data, psychometric_standards)
    psychometric_analysis["reliability"] = reliability_data

    # Анализ валидности
    validity_data = _analyze_validity_indicators(test_data, psychometric_standards)
    psychometric_analysis["validity"] = validity_data

    # Анализ факторной структуры
    if "factor_structure" in test_data:
        factor_data = _analyze_factor_structure(test_data["factor_structure"], psychometric_standards)
        psychometric_analysis["factor_structure"] = factor_data

    # Анализ характеристик заданий
    if "items" in test_data or "questions" in test_data:
        items = test_data.get("items", test_data.get("questions", []))
        item_data = _analyze_item_characteristics(items, psychometric_standards)
        psychometric_analysis["item_analysis"] = item_data

    # Общая оценка качества
    psychometric_analysis["overall_quality"] = _calculate_overall_psychometric_quality(psychometric_analysis)

    return f"""
📊 **Валидация психометрических свойств:**

**Общее качество инструмента:** {psychometric_analysis['overall_quality'].upper()}

**🔄 Анализ надежности:**
{_format_reliability_analysis(psychometric_analysis['reliability'])}

**✅ Анализ валидности:**
{_format_validity_analysis(psychometric_analysis['validity'])}

**🧩 Факторная структура:**
{_format_factor_analysis(psychometric_analysis['factor_structure'])}

**📝 Анализ заданий:**
{_format_item_analysis(psychometric_analysis['item_analysis'])}

**🎯 Психометрические рекомендации:**
1. Улучшить задания с низкими характеристиками
2. Провести дополнительную валидацию
3. Расширить нормативную выборку
4. Оптимизировать факторную структуру

**📋 Следующие шаги валидации:**
- Сбор дополнительных данных
- Подтверждающий факторный анализ
- Кросс-валидация результатов
- Разработка норм и интерпретационных guidelines
"""


async def check_cultural_sensitivity(
    ctx: RunContext[QualityGuardianDependencies],
    content_data: Dict[str, Any],
    target_cultures: List[str] = None,
    sensitivity_areas: List[str] = None
) -> str:
    """
    Проверка культурной чувствительности и инклюзивности контента.

    Args:
        content_data: Контент для проверки
        target_cultures: Целевые культурные группы
        sensitivity_areas: Области чувствительности для анализа

    Returns:
        Анализ культурной адекватности с рекомендациями
    """
    if target_cultures is None:
        target_cultures = ["multiethnic", "multicultural", "global"]

    if sensitivity_areas is None:
        sensitivity_areas = ["language", "examples", "values", "accessibility", "representation"]

    cultural_analysis = {
        "overall_sensitivity": "adequate",
        "sensitivity_scores": {},
        "cultural_issues": [],
        "inclusion_gaps": [],
        "adaptation_recommendations": []
    }

    # Анализ языковой инклюзивности
    if "language" in sensitivity_areas:
        language_analysis = _analyze_language_inclusivity(content_data)
        cultural_analysis["sensitivity_scores"]["language"] = language_analysis["score"]
        cultural_analysis["cultural_issues"].extend(language_analysis["issues"])

    # Анализ примеров и кейсов
    if "examples" in sensitivity_areas:
        examples_analysis = _analyze_cultural_examples(content_data, target_cultures)
        cultural_analysis["sensitivity_scores"]["examples"] = examples_analysis["score"]
        cultural_analysis["cultural_issues"].extend(examples_analysis["issues"])

    # Анализ культурных ценностей
    if "values" in sensitivity_areas:
        values_analysis = _analyze_cultural_values(content_data)
        cultural_analysis["sensitivity_scores"]["values"] = values_analysis["score"]
        cultural_analysis["cultural_issues"].extend(values_analysis["issues"])

    # Анализ доступности
    if "accessibility" in sensitivity_areas:
        accessibility_analysis = _analyze_accessibility_features(content_data)
        cultural_analysis["sensitivity_scores"]["accessibility"] = accessibility_analysis["score"]
        cultural_analysis["cultural_issues"].extend(accessibility_analysis["issues"])

    # Анализ представленности групп
    if "representation" in sensitivity_areas:
        representation_analysis = _analyze_group_representation(content_data)
        cultural_analysis["sensitivity_scores"]["representation"] = representation_analysis["score"]
        cultural_analysis["cultural_issues"].extend(representation_analysis["issues"])

    # Общая оценка культурной чувствительности
    avg_sensitivity = sum(cultural_analysis["sensitivity_scores"].values()) / len(cultural_analysis["sensitivity_scores"])
    if avg_sensitivity >= 80:
        cultural_analysis["overall_sensitivity"] = "excellent"
    elif avg_sensitivity >= 60:
        cultural_analysis["overall_sensitivity"] = "adequate"
    else:
        cultural_analysis["overall_sensitivity"] = "needs_improvement"

    return f"""
🌍 **Анализ культурной чувствительности:**

**Общая культурная адекватность:** {cultural_analysis['overall_sensitivity'].upper()}
**Целевые группы:** {', '.join(target_cultures)}

**📊 Оценки по областям чувствительности:**
{_format_sensitivity_scores(cultural_analysis['sensitivity_scores'])}

**⚠️ Выявленные культурные проблемы:**
{_format_issues_list(cultural_analysis['cultural_issues'])}

**🎯 Рекомендации по культурной адаптации:**
1. Использовать инклюзивный язык
2. Разнообразить примеры и кейсы
3. Учесть различия в культурных ценностях
4. Обеспечить доступность для разных групп
5. Сбалансировать представленность

**🔄 Процесс культурной адаптации:**
- Привлечение представителей целевых культур
- Культурная валидация содержания
- Тестирование на фокус-группах
- Итеративное улучшение контента
"""


async def generate_quality_report(
    ctx: RunContext[QualityGuardianDependencies],
    evaluation_results: Dict[str, Any],
    report_type: str = "comprehensive"
) -> str:
    """
    Генерация комплексного отчета о качестве контента.

    Args:
        evaluation_results: Результаты всех проведенных оценок
        report_type: Тип отчета (summary, detailed, comprehensive)

    Returns:
        Структурированный отчет о качестве
    """
    report_sections = []

    # Исполнительное резюме
    executive_summary = _generate_executive_summary(evaluation_results)
    report_sections.append(f"## 📋 Исполнительное резюме\n{executive_summary}")

    # Сводка оценок
    if report_type in ["detailed", "comprehensive"]:
        assessment_summary = _generate_assessment_summary(evaluation_results)
        report_sections.append(f"## 📊 Сводка оценок\n{assessment_summary}")

    # Детальные результаты
    if report_type == "comprehensive":
        detailed_results = _generate_detailed_results(evaluation_results)
        report_sections.append(f"## 🔍 Детальные результаты\n{detailed_results}")

    # Приоритетные рекомендации
    priority_recommendations = _generate_priority_recommendations(evaluation_results)
    report_sections.append(f"## 🎯 Приоритетные рекомендации\n{priority_recommendations}")

    # План действий
    action_plan = _generate_action_plan(evaluation_results)
    report_sections.append(f"## 📋 План действий\n{action_plan}")

    # Метаданные отчета
    report_metadata = _generate_report_metadata(ctx.deps, evaluation_results)
    report_sections.append(f"## 📄 Метаданные отчета\n{report_metadata}")

    return "\n\n".join(report_sections)


async def create_improvement_recommendations(
    ctx: RunContext[QualityGuardianDependencies],
    quality_issues: List[Dict[str, Any]],
    priority_level: str = "high"
) -> str:
    """
    Создание приоритизированных рекомендаций по улучшению качества.

    Args:
        quality_issues: Список выявленных проблем качества
        priority_level: Уровень приоритета для фокуса

    Returns:
        Структурированные рекомендации с планом внедрения
    """
    recommendations = {
        "immediate_actions": [],
        "short_term_improvements": [],
        "long_term_enhancements": [],
        "resource_requirements": {},
        "success_metrics": {}
    }

    # Анализ и приоритизация проблем
    prioritized_issues = _prioritize_quality_issues(quality_issues, priority_level)

    # Генерация немедленных действий
    recommendations["immediate_actions"] = _generate_immediate_actions(prioritized_issues["critical"])

    # Краткосрочные улучшения
    recommendations["short_term_improvements"] = _generate_short_term_improvements(prioritized_issues["high"])

    # Долгосрочные усовершенствования
    recommendations["long_term_enhancements"] = _generate_long_term_enhancements(prioritized_issues["medium"])

    # Требования к ресурсам
    recommendations["resource_requirements"] = _estimate_resource_requirements(recommendations)

    # Метрики успеха
    recommendations["success_metrics"] = _define_success_metrics(recommendations)

    return f"""
🚀 **Рекомендации по улучшению качества:**

**Приоритет фокуса:** {priority_level.upper()}
**Всего проблем проанализировано:** {len(quality_issues)}

## ⚡ Немедленные действия (Критические):
{_format_action_list(recommendations['immediate_actions'])}

## 📅 Краткосрочные улучшения (1-3 месяца):
{_format_improvement_list(recommendations['short_term_improvements'])}

## 🎯 Долгосрочные усовершенствования (3-12 месяцев):
{_format_enhancement_list(recommendations['long_term_enhancements'])}

## 💰 Требования к ресурсам:
{_format_resource_requirements(recommendations['resource_requirements'])}

## 📈 Метрики успеха:
{_format_success_metrics(recommendations['success_metrics'])}

## 🔄 Процесс внедрения:
1. **Неделя 1-2:** Реализация немедленных действий
2. **Месяц 1:** Планирование краткосрочных улучшений
3. **Месяц 2-3:** Внедрение краткосрочных решений
4. **Месяц 4-12:** Реализация долгосрочных усовершенствований
5. **Непрерывно:** Мониторинг метрик и корректировка плана
"""


# Вспомогательные функции для анализа

def _check_informed_consent(content_data: Dict, target_population: str) -> List[str]:
    """Проверка наличия и адекватности информированного согласия."""
    issues = []

    # Проверка наличия формы согласия
    if "informed_consent" not in content_data and "consent_form" not in content_data:
        issues.append("Отсутствует форма информированного согласия")

    # Проверка адекватности для целевой популяции
    if target_population in ["children", "adolescents"] and "parental_consent" not in str(content_data):
        issues.append("Требуется согласие родителей для несовершеннолетних")

    # Проверка права на отказ
    consent_text = str(content_data).lower()
    if "право на отказ" not in consent_text and "right to withdraw" not in consent_text:
        issues.append("Не указано право на отказ от участия")

    return issues


def _check_beneficence_principle(content_data: Dict) -> List[str]:
    """Проверка соблюдения принципа благополучия."""
    issues = []

    # Поиск потенциально вредного контента
    harmful_patterns = ["суицид", "самоповреждение", "насилие", "травма"]
    content_text = str(content_data).lower()

    for pattern in harmful_patterns:
        if pattern in content_text and "предупреждение" not in content_text:
            issues.append(f"Чувствительная тема '{pattern}' без предупреждения")

    # Проверка наличия поддержки
    if "поддержка" not in content_text and "support" not in content_text:
        issues.append("Отсутствует информация о доступной поддержке")

    return issues


def _check_justice_principle(content_data: Dict, target_population: str) -> List[str]:
    """Проверка соблюдения принципа справедливости."""
    issues = []

    content_text = str(content_data).lower()

    # Проверка инклюзивности языка
    exclusive_terms = ["нормальный", "обычный", "типичный"]
    for term in exclusive_terms:
        if term in content_text:
            issues.append(f"Потенциально исключающий термин: '{term}'")

    # Проверка культурной чувствительности
    if target_population == "multicultural" and "культурные различия" not in content_text:
        issues.append("Недостаточный учет культурных различий")

    return issues


def _check_respect_principle(content_data: Dict) -> List[str]:
    """Проверка соблюдения принципа уважения."""
    issues = []

    content_text = str(content_data).lower()

    # Проверка уважительного языка
    disrespectful_patterns = ["дефект", "ненормальн", "отклонен"]
    for pattern in disrespectful_patterns:
        if pattern in content_text:
            issues.append(f"Неуважительная формулировка: содержит '{pattern}'")

    # Проверка конфиденциальности
    if "конфиденциальность" not in content_text and "privacy" not in content_text:
        issues.append("Отсутствует информация о конфиденциальности")

    return issues


def _generate_ethical_recommendations(issues: List[str]) -> List[str]:
    """Генерация рекомендаций по этическим проблемам."""
    recommendations = []

    for issue in issues:
        if "согласие" in issue:
            recommendations.append("Добавить детальную форму информированного согласия")
        elif "предупреждение" in issue:
            recommendations.append("Включить предупреждения о чувствительном контенте")
        elif "поддержка" in issue:
            recommendations.append("Предоставить информацию о службах поддержки")
        elif "язык" in issue or "формулировка" in issue:
            recommendations.append("Использовать более уважительные формулировки")
        else:
            recommendations.append("Провести дополнительную этическую экспертизу")

    return list(set(recommendations))  # Убираем дубликаты


def _assess_content_validity(content_data: Dict) -> float:
    """Оценка содержательной валидности."""
    score = 70.0  # Базовый балл

    # Проверка теоретического обоснования
    if "theoretical_basis" in content_data or "theory" in str(content_data):
        score += 10

    # Проверка покрытия конструкта
    if "subscales" in content_data or "dimensions" in content_data:
        score += 10

    # Проверка экспертной оценки
    if "expert_review" in content_data or "validation" in str(content_data):
        score += 10

    return min(score, 100.0)


def _assess_construct_validity(content_data: Dict) -> float:
    """Оценка конструктной валидности."""
    score = 60.0

    # Проверка факторной структуры
    if "factor_structure" in content_data:
        score += 15

    # Проверка конвергентной валидности
    if "convergent_validity" in content_data:
        score += 10

    # Проверка дискриминантной валидности
    if "discriminant_validity" in content_data:
        score += 15

    return min(score, 100.0)


def _assess_reliability(content_data: Dict) -> float:
    """Оценка надежности."""
    score = 60.0

    # Проверка внутренней согласованности
    if "cronbach_alpha" in content_data:
        alpha = content_data.get("cronbach_alpha", 0.0)
        if alpha >= 0.90:
            score += 20
        elif alpha >= 0.80:
            score += 15
        elif alpha >= 0.70:
            score += 10

    # Проверка ретестовой надежности
    if "test_retest" in content_data:
        score += 10

    return min(score, 100.0)


def _assess_theoretical_basis(content_data: Dict) -> float:
    """Оценка теоретического обоснования."""
    score = 50.0

    content_text = str(content_data).lower()

    # Проверка ссылок на теории
    if "теория" in content_text or "theory" in content_text:
        score += 20

    # Проверка литературного обзора
    if "literature" in content_text or "исследования" in content_text:
        score += 15

    # Проверка современности источников
    if any(year in content_text for year in ["2020", "2021", "2022", "2023", "2024"]):
        score += 15

    return min(score, 100.0)


def _analyze_empirical_support(content_data: Dict, evidence_level: str) -> Dict:
    """Анализ эмпирической поддержки."""
    gaps = []

    # Требования по уровню доказательств
    if evidence_level == "comprehensive":
        required_studies = ["RCT", "meta_analysis", "longitudinal"]
        for study_type in required_studies:
            if study_type not in str(content_data):
                gaps.append(f"Отсутствуют {study_type} исследования")

    elif evidence_level == "standard":
        if "research" not in str(content_data).lower():
            gaps.append("Недостаточно исследовательских данных")

    return {"gaps": gaps}


def _analyze_psychological_risks(content_data: Dict, sensitivity_level: str) -> Dict:
    """Анализ психологических рисков."""
    risks = {
        "score": 0,
        "issues": []
    }

    content_text = str(content_data).lower()

    # Высокорискованные темы
    high_risk_topics = ["суицид", "самоповреждение", "насилие", "trauma", "abuse"]
    for topic in high_risk_topics:
        if topic in content_text:
            risks["score"] += 30
            risks["issues"].append(f"Высокорискованная тема: {topic}")

    # Проверка предупреждений
    if risks["score"] > 0 and "предупреждение" not in content_text:
        risks["score"] += 20
        risks["issues"].append("Отсутствуют предупреждения о рисках")

    return risks


def _analyze_privacy_risks(content_data: Dict) -> Dict:
    """Анализ рисков конфиденциальности."""
    risks = {
        "score": 0,
        "issues": []
    }

    # Проверка сбора персональных данных
    personal_data_patterns = ["имя", "адрес", "телефон", "email", "дата рождения"]
    content_text = str(content_data).lower()

    for pattern in personal_data_patterns:
        if pattern in content_text and "шифрование" not in content_text:
            risks["score"] += 15
            risks["issues"].append(f"Сбор {pattern} без указания защиты данных")

    return risks


def _analyze_vulnerability_risks(content_data: Dict) -> Dict:
    """Анализ рисков для уязвимых групп."""
    risks = {
        "score": 0,
        "issues": []
    }

    content_text = str(content_data).lower()

    # Проверка учета особых потребностей
    vulnerable_groups = ["дети", "пожилые", "инвалиды", "психические расстройства"]
    for group in vulnerable_groups:
        if group in content_text and "адаптация" not in content_text:
            risks["score"] += 20
            risks["issues"].append(f"Недостаточный учет потребностей группы: {group}")

    return risks


def _analyze_crisis_triggers(content_data: Dict) -> Dict:
    """Анализ триггеров кризисных состояний."""
    risks = {
        "score": 0,
        "issues": []
    }

    content_text = str(content_data).lower()

    # Поиск потенциальных триггеров
    crisis_triggers = ["смерть", "развод", "увольнение", "болезнь", "потеря"]
    for trigger in crisis_triggers:
        if trigger in content_text and "поддержка" not in content_text:
            risks["score"] += 25
            risks["issues"].append(f"Потенциальный триггер без поддержки: {trigger}")

    return risks


def _generate_protection_measures(safety_issues: List[str]) -> List[str]:
    """Генерация защитных мер."""
    measures = []

    for issue in safety_issues:
        if "предупреждение" in issue:
            measures.append("Добавить триггерные предупреждения")
        elif "поддержка" in issue:
            measures.append("Предоставить контакты служб поддержки")
        elif "данных" in issue:
            measures.append("Усилить защиту персональных данных")
        elif "адаптация" in issue:
            measures.append("Создать специальные адаптации для уязвимых групп")

    return list(set(measures))


# Дополнительные вспомогательные функции форматирования

def _format_issues_list(issues: List[str]) -> str:
    """Форматирование списка проблем."""
    if not issues:
        return "✅ Проблемы не выявлены"
    return "\n".join([f"❌ {issue}" for issue in issues])


def _format_recommendations_list(recommendations: List[str]) -> str:
    """Форматирование списка рекомендаций."""
    if not recommendations:
        return "✅ Дополнительные рекомендации не требуются"
    return "\n".join([f"💡 {rec}" for rec in recommendations])


def _format_validity_scores(scores: Dict[str, float]) -> str:
    """Форматирование оценок валидности."""
    formatted = []
    for criterion, score in scores.items():
        emoji = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
        formatted.append(f"{emoji} {criterion.replace('_', ' ').title()}: {score:.1f}/100")
    return "\n".join(formatted)


def _format_evidence_gaps(gaps: List[str]) -> str:
    """Форматирование пробелов в доказательствах."""
    if not gaps:
        return "✅ Значимые пробелы не выявлены"
    return "\n".join([f"📈 {gap}" for gap in gaps])


def _format_risk_scores(scores: Dict[str, float]) -> str:
    """Форматирование оценок рисков."""
    formatted = []
    for category, score in scores.items():
        if score >= 80:
            emoji = "🚨"
            level = "ВЫСОКИЙ"
        elif score >= 50:
            emoji = "⚠️"
            level = "СРЕДНИЙ"
        else:
            emoji = "✅"
            level = "НИЗКИЙ"
        formatted.append(f"{emoji} {category.replace('_', ' ').title()}: {score:.1f}/100 ({level})")
    return "\n".join(formatted)


def _format_protection_measures(measures: List[str]) -> str:
    """Форматирование защитных мер."""
    if not measures:
        return "✅ Дополнительные меры защиты не требуются"
    return "\n".join([f"🛡️ {measure}" for measure in measures])


# Дополнительные функции анализа будут добавлены по мере необходимости...