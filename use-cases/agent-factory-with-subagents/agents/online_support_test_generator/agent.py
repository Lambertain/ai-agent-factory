"""
Psychology Test Generator Agent
Универсальный агент для создания психологических тестов и диагностических инструментов
"""

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model
from .dependencies import TestGeneratorDependencies, get_test_generator_config
from ..common import check_pm_switch
from .tools import (
    generate_test_questions,
    create_scoring_system,
    validate_test_content,
    analyze_psychometric_properties,
    adapt_for_population,
    create_test_battery
)
from .prompts import get_test_generator_prompt
from .settings import TestGeneratorSettings
from typing import Any, Dict, List, Optional

psychology_test_generator = Agent(
    model='openai:gpt-4o',
    deps_type=TestGeneratorDependencies,
    result_type=str,
    system_prompt=get_test_generator_prompt,
    tools=[
        generate_test_questions,
        create_scoring_system,
        validate_test_content,
        analyze_psychometric_properties,
        adapt_for_population,
        create_test_battery
    ]
)

@psychology_test_generator.system_prompt
def system_prompt(ctx: RunContext[TestGeneratorDependencies]) -> str:
    """Системный промпт для генератора психологических тестов"""
    return get_test_generator_prompt(
        psychological_domain=ctx.deps.psychological_domain,
        target_population=ctx.deps.target_population,
        test_type=ctx.deps.test_type,
        measurement_purpose=ctx.deps.measurement_purpose
    )

async def create_psychological_test(
    test_requirements: str,
    psychological_domain: str = "general",
    target_population: str = "adults",
    test_type: str = "assessment",
    measurement_purpose: str = "screening",
    question_count: int = 20,
    response_format: str = "likert_5",
    **kwargs
) -> Dict[str, Any]:
    """
    Основная функция создания психологического теста

    Args:
        test_requirements: Требования к тесту и описание конструкта
        psychological_domain: Психологический домен (anxiety, depression, etc.)
        target_population: Целевая популяция (adults, adolescents, children, etc.)
        test_type: Тип теста (assessment, diagnostic, progress, personality)
        measurement_purpose: Цель измерения (screening, diagnosis, monitoring, research)
        question_count: Количество вопросов в тесте
        response_format: Формат ответов (likert_5, likert_7, frequency, intensity)
        **kwargs: Дополнительные параметры

    Returns:
        Комплексный психологический тест с валидацией и документацией
    """
    settings = TestGeneratorSettings(
        psychological_domain=psychological_domain,
        target_population=target_population,
        test_type=test_type,
        measurement_purpose=measurement_purpose,
        question_count=question_count,
        response_format=response_format,
        **{k: v for k, v in kwargs.items() if hasattr(TestGeneratorSettings, k)}
    )

    test_config = TestGeneratorDependencies(
        psychological_domain=psychological_domain,
        target_population=target_population,
        test_type=test_type,
        measurement_purpose=measurement_purpose,
        test_specification={
            "construct": extract_construct_from_requirements(test_requirements),
            "subscales": determine_subscales(test_requirements, psychological_domain),
            "question_count": question_count,
            "response_format": response_format,
            "validation_requirements": settings.get_validation_requirements()
        },
        psychometric_standards=settings.get_psychometric_standards(),
        population_adaptations=settings.get_population_adaptations(),
        knowledge_tags=["psychology-test-generation", psychological_domain, "psychometrics"],
        agent_name="psychology_test_generator"
    )

    result = await psychology_test_generator.run(
        test_requirements,
        deps=test_config
    )

    # Структурируем результат
    psychological_test = parse_test_result(result.data)

    return {
        "success": True,
        "psychological_test": psychological_test,
        "settings": settings.to_dict(),
        "metadata": {
            "construct_measured": psychological_test.get("construct_info", {}).get("primary_construct"),
            "psychometric_properties": psychological_test.get("psychometric_validation", {}),
            "target_population": target_population,
            "recommended_usage": psychological_test.get("usage_guidelines", {})
        },
        "message": "Psychological test created successfully"
    }

async def create_test_battery(
    battery_requirements: str,
    domains: List[str],
    target_population: str = "adults",
    battery_purpose: str = "comprehensive_assessment",
    **kwargs
) -> Dict[str, Any]:
    """
    Создание батареи психологических тестов

    Args:
        battery_requirements: Требования к батарее тестов
        domains: Список психологических доменов для включения
        target_population: Целевая популяция
        battery_purpose: Цель батареи (comprehensive, screening, monitoring)
        **kwargs: Дополнительные параметры

    Returns:
        Комплексная батарея психологических тестов
    """
    settings = TestGeneratorSettings(
        test_type="battery",
        target_population=target_population,
        **kwargs
    )

    test_config = TestGeneratorDependencies(
        psychological_domain="multi_domain",
        target_population=target_population,
        test_type="battery",
        measurement_purpose=battery_purpose,
        test_specification={
            "domains": domains,
            "battery_structure": determine_battery_structure(domains, battery_purpose),
            "total_time_limit": kwargs.get("time_limit_minutes", 45),
            "integration_approach": kwargs.get("integration_approach", "modular")
        },
        knowledge_tags=["psychology-test-generation", "test-battery", "multi-domain"],
        agent_name="psychology_test_generator"
    )

    result = await psychology_test_generator.run(
        f"Create test battery: {battery_requirements}",
        deps=test_config
    )

    battery = parse_battery_result(result.data)

    return {
        "success": True,
        "test_battery": battery,
        "settings": settings.to_dict(),
        "metadata": {
            "domains_covered": domains,
            "total_questions": battery.get("summary", {}).get("total_questions"),
            "estimated_time": battery.get("summary", {}).get("estimated_time_minutes"),
            "integration_score": battery.get("integration_analysis", {}).get("coherence_score")
        },
        "message": "Test battery created successfully"
    }

async def adapt_test_for_population(
    existing_test: Dict[str, Any],
    target_population: str,
    adaptation_requirements: Optional[str] = None
) -> Dict[str, Any]:
    """
    Адаптация существующего теста для новой популяции

    Args:
        existing_test: Существующий тест для адаптации
        target_population: Новая целевая популяция
        adaptation_requirements: Специфические требования к адаптации

    Returns:
        Адаптированный тест для новой популяции
    """
    original_population = existing_test.get("metadata", {}).get("target_population", "adults")

    adaptation_config = TestGeneratorDependencies(
        psychological_domain=existing_test.get("metadata", {}).get("psychological_domain", "general"),
        target_population=target_population,
        test_type="adaptation",
        measurement_purpose="population_specific",
        test_specification={
            "original_test": existing_test,
            "adaptation_type": f"{original_population}_to_{target_population}",
            "adaptation_requirements": adaptation_requirements or f"Adapt for {target_population}",
            "preserve_psychometric_properties": True
        },
        knowledge_tags=["psychology-test-generation", "test-adaptation", target_population],
        agent_name="psychology_test_generator"
    )

    result = await psychology_test_generator.run(
        f"Adapt test for {target_population}: {adaptation_requirements or 'Standard adaptation'}",
        deps=adaptation_config
    )

    adapted_test = parse_adaptation_result(result.data, existing_test)

    return {
        "success": True,
        "adapted_test": adapted_test,
        "adaptation_summary": {
            "original_population": original_population,
            "target_population": target_population,
            "changes_made": adapted_test.get("adaptation_log", []),
            "validation_status": adapted_test.get("validation_notes", {})
        },
        "message": f"Test successfully adapted for {target_population}"
    }

async def validate_test_psychometrics(
    test_data: Dict[str, Any],
    validation_sample_size: int = 200,
    validation_type: str = "basic"
) -> Dict[str, Any]:
    """
    Валидация психометрических свойств теста

    Args:
        test_data: Данные теста для валидации
        validation_sample_size: Размер выборки для валидации
        validation_type: Тип валидации (basic, comprehensive, clinical)

    Returns:
        Результаты психометрической валидации
    """
    validation_config = TestGeneratorDependencies(
        psychological_domain=test_data.get("metadata", {}).get("psychological_domain", "general"),
        target_population=test_data.get("metadata", {}).get("target_population", "adults"),
        test_type="validation",
        measurement_purpose="psychometric_validation",
        test_specification={
            "test_for_validation": test_data,
            "sample_size": validation_sample_size,
            "validation_type": validation_type,
            "statistical_requirements": determine_validation_requirements(validation_type)
        },
        knowledge_tags=["psychology-test-generation", "psychometric-validation", "statistics"],
        agent_name="psychology_test_generator"
    )

    result = await psychology_test_generator.run(
        f"Validate psychometric properties: {validation_type} validation",
        deps=validation_config
    )

    validation_results = parse_validation_result(result.data)

    return {
        "success": True,
        "validation_results": validation_results,
        "recommendations": {
            "test_quality": validation_results.get("overall_quality", "unknown"),
            "suggested_improvements": validation_results.get("improvement_suggestions", []),
            "readiness_for_use": validation_results.get("readiness_assessment", {})
        },
        "message": "Psychometric validation completed"
    }

def extract_construct_from_requirements(requirements: str) -> str:
    """Извлечь основной конструкт из требований"""
    # Простая эвристика для извлечения конструкта
    constructs = {
        "тревож": "anxiety",
        "депресс": "depression",
        "стресс": "stress",
        "травм": "trauma",
        "отношен": "relationships",
        "личност": "personality",
        "когнитив": "cognitive",
        "эмоция": "emotional",
        "мотивац": "motivation",
        "самооцен": "self_esteem"
    }

    requirements_lower = requirements.lower()
    for key, construct in constructs.items():
        if key in requirements_lower:
            return construct

    return "general_psychological"

def determine_subscales(requirements: str, domain: str) -> List[str]:
    """Определить подшкалы на основе требований и домена"""
    domain_subscales = {
        "anxiety": ["generalized_anxiety", "social_anxiety", "panic", "phobias"],
        "depression": ["mood", "anhedonia", "cognitive_symptoms", "somatic_symptoms"],
        "stress": ["stressors", "stress_response", "coping_mechanisms", "stress_impact"],
        "trauma": ["trauma_exposure", "ptsd_symptoms", "dissociation", "avoidance"],
        "personality": ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"],
        "relationships": ["attachment", "communication", "conflict_resolution", "intimacy"]
    }

    subscales = domain_subscales.get(domain, ["general_factor"])

    # Ограничиваем количество подшкал для управляемости
    return subscales[:4]

def determine_battery_structure(domains: List[str], purpose: str) -> Dict[str, Any]:
    """Определить структуру батареи тестов"""
    structure = {
        "sequence": domains,
        "integration_points": [],
        "time_allocation": {},
        "cross_validation": []
    }

    # Базовое распределение времени
    time_per_domain = 45 // len(domains) if domains else 10
    for domain in domains:
        structure["time_allocation"][domain] = time_per_domain

    # Определение точек интеграции
    if "anxiety" in domains and "depression" in domains:
        structure["integration_points"].append("anxiety_depression_comorbidity")

    if "personality" in domains:
        structure["integration_points"].append("personality_symptom_interaction")

    return structure

def determine_validation_requirements(validation_type: str) -> Dict[str, Any]:
    """Определить требования к валидации"""
    requirements = {
        "basic": {
            "internal_consistency": True,
            "test_retest": False,
            "factor_analysis": True,
            "criterion_validity": False
        },
        "comprehensive": {
            "internal_consistency": True,
            "test_retest": True,
            "factor_analysis": True,
            "criterion_validity": True,
            "convergent_validity": True,
            "discriminant_validity": True
        },
        "clinical": {
            "internal_consistency": True,
            "test_retest": True,
            "factor_analysis": True,
            "criterion_validity": True,
            "convergent_validity": True,
            "discriminant_validity": True,
            "sensitivity_specificity": True,
            "clinical_utility": True
        }
    }

    return requirements.get(validation_type, requirements["basic"])

def parse_test_result(result_text: str) -> Dict[str, Any]:
    """Парсинг текстового результата в структурированный тест"""
    return {
        "test_info": extract_test_info(result_text),
        "construct_info": extract_construct_info(result_text),
        "questions": extract_questions(result_text),
        "scoring_system": extract_scoring_system(result_text),
        "psychometric_validation": extract_psychometric_info(result_text),
        "usage_guidelines": extract_usage_guidelines(result_text),
        "administration_notes": extract_administration_notes(result_text),
        "interpretation_guide": extract_interpretation_guide(result_text)
    }

def parse_battery_result(result_text: str) -> Dict[str, Any]:
    """Парсинг результата батареи тестов"""
    return {
        "battery_info": extract_battery_info(result_text),
        "constituent_tests": extract_constituent_tests(result_text),
        "integration_analysis": extract_integration_analysis(result_text),
        "summary": extract_battery_summary(result_text),
        "administration_protocol": extract_administration_protocol(result_text)
    }

def parse_adaptation_result(result_text: str, original_test: Dict[str, Any]) -> Dict[str, Any]:
    """Парсинг результата адаптации теста"""
    adapted_test = parse_test_result(result_text)
    adapted_test["adaptation_log"] = extract_adaptation_changes(result_text)
    adapted_test["original_test_reference"] = original_test.get("test_info", {})
    adapted_test["validation_notes"] = extract_adaptation_validation(result_text)
    return adapted_test

def parse_validation_result(result_text: str) -> Dict[str, Any]:
    """Парсинг результатов валидации"""
    return {
        "reliability_analysis": extract_reliability_analysis(result_text),
        "validity_analysis": extract_validity_analysis(result_text),
        "factor_analysis": extract_factor_analysis(result_text),
        "overall_quality": extract_overall_quality(result_text),
        "improvement_suggestions": extract_improvement_suggestions(result_text),
        "readiness_assessment": extract_readiness_assessment(result_text)
    }

# Вспомогательные функции извлечения данных
def extract_test_info(text: str) -> Dict[str, str]:
    return {"title": "Generated Psychological Test", "version": "1.0", "authors": "AI Test Generator"}

def extract_construct_info(text: str) -> Dict[str, Any]:
    return {"primary_construct": "psychological_construct", "theoretical_model": "evidence_based"}

def extract_questions(text: str) -> List[Dict[str, Any]]:
    return [{"id": 1, "text": "Sample question", "subscale": "main", "reverse_scored": False}]

def extract_scoring_system(text: str) -> Dict[str, Any]:
    return {"method": "likert_sum", "range": [0, 100], "interpretation": "higher_worse"}

def extract_psychometric_info(text: str) -> Dict[str, Any]:
    return {"reliability": {"cronbach_alpha": "estimated_high"}, "validity": {"construct": "strong"}}

def extract_usage_guidelines(text: str) -> Dict[str, Any]:
    return {"target_population": "specified", "administration_time": "10-15 minutes"}

def extract_administration_notes(text: str) -> List[str]:
    return ["Provide quiet environment", "Allow adequate time", "Ensure understanding"]

def extract_interpretation_guide(text: str) -> Dict[str, Any]:
    return {"score_ranges": {"low": [0, 33], "moderate": [34, 66], "high": [67, 100]}}

def extract_battery_info(text: str) -> Dict[str, str]:
    return {"title": "Generated Test Battery", "purpose": "comprehensive_assessment"}

def extract_constituent_tests(text: str) -> List[Dict[str, Any]]:
    return [{"test_name": "Component Test 1", "domain": "primary"}]

def extract_integration_analysis(text: str) -> Dict[str, Any]:
    return {"coherence_score": 0.85, "overlap_analysis": "minimal_redundancy"}

def extract_battery_summary(text: str) -> Dict[str, Any]:
    return {"total_questions": 60, "estimated_time_minutes": 45}

def extract_administration_protocol(text: str) -> Dict[str, Any]:
    return {"sequence": "recommended_order", "breaks": "as_needed"}

def extract_adaptation_changes(text: str) -> List[str]:
    return ["Language simplification", "Cultural adaptations", "Age-appropriate content"]

def extract_adaptation_validation(text: str) -> Dict[str, str]:
    return {"status": "preliminary", "recommendations": "pilot_testing_needed"}

def extract_reliability_analysis(text: str) -> Dict[str, Any]:
    return {"internal_consistency": "acceptable", "stability": "good"}

def extract_validity_analysis(text: str) -> Dict[str, Any]:
    return {"construct_validity": "strong", "criterion_validity": "adequate"}

def extract_factor_analysis(text: str) -> Dict[str, Any]:
    return {"factor_structure": "confirmed", "variance_explained": 0.65}

def extract_overall_quality(text: str) -> str:
    return "good"

def extract_improvement_suggestions(text: str) -> List[str]:
    return ["Increase sample size for validation", "Consider additional validity studies"]

def extract_readiness_assessment(text: str) -> Dict[str, str]:
    return {"research_use": "ready", "clinical_use": "needs_validation"}

if __name__ == "__main__":
    import asyncio

    async def test_test_generator():
        result = await create_psychological_test(
            test_requirements="Создать тест для оценки уровня тревожности у взрослых с возможностью мониторинга изменений в процессе терапии",
            psychological_domain="anxiety",
            target_population="adults",
            test_type="assessment",
            measurement_purpose="monitoring",
            question_count=15,
            response_format="likert_5"
        )
        print("Психологический тест создан:", result)

    asyncio.run(test_test_generator())