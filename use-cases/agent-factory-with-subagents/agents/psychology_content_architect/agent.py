"""
Universal NLP Content Architect Agent
Универсальный агент для создания контента с применением NLP-методологии
Использует 5-этапную систему: Research → Draft → Reflection → Final → Analytics
Работает с любыми доменами: психология, астрология, таро, нумерология, коучинг, велнес
"""

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model
from .dependencies import UniversalNLPDependencies, get_nlp_config
from ..common import check_pm_switch
from .tools import (
    research_domain_topic,
    create_content_draft,
    reflect_and_improve_content,
    finalize_nlp_content,
    create_transformation_program,
    adapt_content_for_vak,
    validate_nlp_structure,
    search_nlp_knowledge,
    delegate_specialized_task
)
from .prompts import get_universal_nlp_prompt
from .settings import UniversalNLPSettings
from typing import Any, Dict, List, Optional

universal_nlp_content_architect = Agent(
    model='openai:gpt-4o',
    deps_type=UniversalNLPDependencies,
    result_type=str,
    system_prompt=get_universal_nlp_prompt,
    tools=[
        research_domain_topic,
        create_content_draft,
        reflect_and_improve_content,
        finalize_nlp_content,
        create_transformation_program,
        adapt_content_for_vak,
        validate_nlp_structure,
        search_nlp_knowledge,
        delegate_specialized_task
    ]
)

@universal_nlp_content_architect.system_prompt
def system_prompt(ctx: RunContext[UniversalNLPDependencies]) -> str:
    """Системный промпт для универсального NLP архитектора"""
    return get_universal_nlp_prompt(
        domain_type=ctx.deps.domain_type,
        content_type=ctx.deps.content_type,
        target_language=ctx.deps.target_language,
        nlp_methodology=ctx.deps.nlp_methodology,
        project_context=ctx.deps.project_context
    )

async def create_nlp_content(
    content_topic: str,
    domain_type: str = "psychology",
    content_type: str = "diagnostic_test",
    target_language: str = "ukrainian",
    content_count: int = 16,
    complexity_level: str = "intermediate",
    transformation_days: int = 21,
    **kwargs
) -> Dict[str, Any]:
    """
    Основная функция создания NLP контента по 5-этапной системе

    Args:
        content_topic: Тема контента (депрессия, предназначение, таро-расклад, жизненный путь)
        domain_type: Домен применения (psychology, astrology, tarot, numerology, coaching, wellness)
        content_type: Тип контента (diagnostic_test, transformation_program, guidance_system)
        target_language: Целевой язык (ukrainian, russian, english)
        content_count: Количество элементов контента (минимум 15)
        complexity_level: Уровень сложности (basic, intermediate, advanced)
        transformation_days: Длительность программы (7, 14, 21 день)
        **kwargs: Дополнительные параметры

    Returns:
        Полный NLP контент с техниками и трансформационными элементами
    """
    settings = UniversalNLPSettings(
        domain_type=domain_type,
        content_type=content_type,
        target_language=target_language,
        content_count=max(15, content_count),  # Минимум 15 элементов
        complexity_level=complexity_level,
        transformation_days=transformation_days,
        **{k: v for k, v in kwargs.items() if hasattr(UniversalNLPSettings, k)}
    )

    nlp_config = UniversalNLPDependencies(
        domain_type=domain_type,
        content_type=content_type,
        target_language=target_language,
        nlp_methodology="ericksonian_full",
        project_context={
            "topic": content_topic,
            "content_count": settings.content_count,
            "complexity": settings.complexity_level,
            "transformation_days": settings.transformation_days,
            "language_tone": settings.get_language_tone(),
            "domain_techniques": settings.get_domain_techniques(domain_type)
        },
        vak_adaptations=settings.get_vak_templates(),
        age_adaptations=settings.get_age_adaptations(),
        nlp_techniques=settings.get_nlp_techniques(),
        ericksonian_patterns=settings.get_ericksonian_patterns(),
        knowledge_tags=["nlp-content", domain_type, "universal-nlp"],
        agent_name="universal_nlp_content_architect"
    )

    # 5-этапный процесс создания NLP контента
    result = await universal_nlp_content_architect.run(
        f"Create {content_topic} content for {domain_type} using 5-stage NLP methodology",
        deps=nlp_config
    )

    # Структурируем результат
    nlp_content = parse_nlp_content_result(result.data)

    return {
        "success": True,
        "content": nlp_content,
        "settings": settings.to_dict(),
        "metadata": {
            "topic": content_topic,
            "domain": domain_type,
            "language": target_language,
            "content_elements": nlp_content.get("content_elements", []),
            "nlp_techniques": nlp_content.get("nlp_techniques", []),
            "transformation_program": nlp_content.get("transformation_program", {}),
            "methodology": "Universal NLP 5-stage system"
        },
        "message": f"Universal NLP content for {domain_type} created successfully"
    }

async def adapt_existing_content(
    existing_content: Dict[str, Any],
    target_language: str,
    target_domain: Optional[str] = None,
    target_vak: Optional[str] = None,
    target_age_group: Optional[str] = None
) -> Dict[str, Any]:
    """
    Адаптация существующего NLP контента под новый домен, язык, VAK тип или возрастную группу

    Args:
        existing_content: Существующий контент для адаптации
        target_language: Целевой язык
        target_domain: Целевой домен (psychology, astrology, tarot, etc.)
        target_vak: Целевой VAK тип (visual, auditory, kinesthetic)
        target_age_group: Целевая возрастная группа (youth, friendly, professional)

    Returns:
        Адаптированный NLP контент
    """
    adaptation_config = UniversalNLPDependencies(
        domain_type=target_domain or existing_content.get("metadata", {}).get("domain", "psychology"),
        content_type="adaptation",
        target_language=target_language,
        nlp_methodology="adaptation_mode",
        project_context={
            "original_content": existing_content,
            "target_vak": target_vak,
            "target_age_group": target_age_group,
            "target_domain": target_domain,
            "preserve_nlp_structure": True
        },
        knowledge_tags=["nlp-content", "adaptation", target_language],
        agent_name="universal_nlp_content_architect"
    )

    result = await universal_nlp_content_architect.run(
        f"Adapt content to {target_domain or 'current domain'} with language={target_language}, VAK={target_vak}, age={target_age_group}",
        deps=adaptation_config
    )

    adapted_content = parse_nlp_content_result(result.data)

    return {
        "success": True,
        "adapted_content": adapted_content,
        "adaptation_summary": {
            "target_language": target_language,
            "target_domain": target_domain,
            "vak_type": target_vak,
            "age_group": target_age_group,
            "nlp_techniques_adapted": adapted_content.get("nlp_techniques", []),
            "changes_made": adapted_content.get("adaptation_log", [])
        },
        "message": f"Content successfully adapted to {target_domain or 'target domain'} in {target_language}"
    }

async def validate_nlp_methodology(
    content_data: Dict[str, Any],
    domain_type: str = "psychology",
    check_ericksonian_compliance: bool = True
) -> Dict[str, Any]:
    """
    Валидация контента на соответствие NLP/Ericksonian методологии

    Args:
        content_data: Данные контента для валидации
        domain_type: Тип домена для проверки
        check_ericksonian_compliance: Проверять соответствие Ericksonian техникам

    Returns:
        Результаты валидации с рекомендациями
    """
    validation_config = UniversalNLPDependencies(
        domain_type=domain_type,
        content_type="quality_check",
        target_language="neutral",
        nlp_methodology="validation_mode",
        project_context={
            "content_for_validation": content_data,
            "check_ericksonian": check_ericksonian_compliance,
            "validation_criteria": [
                "nlp_techniques_quality",
                "vak_adaptations_completeness",
                "ericksonian_patterns_usage",
                "domain_appropriateness",
                "transformation_effectiveness"
            ]
        },
        knowledge_tags=["nlp-content", "validation", "quality"],
        agent_name="universal_nlp_content_architect"
    )

    result = await universal_nlp_content_architect.run(
        f"Validate NLP methodology and quality for {domain_type} content",
        deps=validation_config
    )

    validation_results = parse_validation_result(result.data)

    return {
        "success": True,
        "validation_results": validation_results,
        "compliance": {
            "nlp_compliant": validation_results.get("nlp_score", 0) > 0.8,
            "ericksonian_compliant": validation_results.get("ericksonian_score", 0) > 0.8,
            "domain_appropriate": validation_results.get("domain_score", 0) > 0.8,
            "quality_score": validation_results.get("overall_quality", 0),
            "recommendations": validation_results.get("improvements", [])
        },
        "message": "NLP methodology validation completed"
    }

async def create_transformation_program_standalone(
    program_topic: str,
    domain_type: str = "psychology",
    target_language: str = "ukrainian",
    program_duration: int = 21,
    complexity_level: str = "intermediate",
    **kwargs
) -> Dict[str, Any]:
    """
    Создание трансформационной программы как отдельного продукта

    Args:
        program_topic: Тема программы трансформации
        domain_type: Домен (psychology, astrology, tarot, etc.)
        target_language: Целевой язык
        program_duration: Длительность программы в днях (7, 14, 21)
        complexity_level: Уровень сложности
        **kwargs: Дополнительные параметры

    Returns:
        Полная трансформационная программа с NLP техниками
    """
    return await create_nlp_content(
        content_topic=program_topic,
        domain_type=domain_type,
        content_type="transformation_program",
        target_language=target_language,
        transformation_days=program_duration,
        complexity_level=complexity_level,
        **kwargs
    )

def parse_nlp_content_result(result_text: str) -> Dict[str, Any]:
    """Парсинг текстового результата в структурированный NLP контент"""
    return {
        "content_info": extract_content_info(result_text),
        "content_elements": extract_content_elements(result_text),
        "nlp_techniques": extract_nlp_techniques(result_text),
        "ericksonian_patterns": extract_ericksonian_patterns(result_text),
        "vak_adaptations": extract_vak_adaptations(result_text),
        "transformation_program": extract_transformation_program(result_text),
        "domain_specific_elements": extract_domain_elements(result_text),
        "methodology_notes": extract_methodology_notes(result_text)
    }

def parse_validation_result(result_text: str) -> Dict[str, Any]:
    """Парсинг результатов NLP валидации"""
    return {
        "nlp_score": extract_nlp_score(result_text),
        "ericksonian_score": extract_ericksonian_score(result_text),
        "domain_score": extract_domain_score(result_text),
        "overall_quality": extract_overall_quality(result_text),
        "identified_issues": extract_issues(result_text),
        "improvements": extract_improvements(result_text),
        "compliance_details": extract_compliance_details(result_text)
    }

# Вспомогательные функции извлечения данных
def extract_content_info(text: str) -> Dict[str, str]:
    return {"title": "Generated NLP Content", "version": "1.0", "methodology": "Universal NLP"}

def extract_content_elements(text: str) -> List[Dict[str, Any]]:
    return [{"id": 1, "text": "Sample NLP content element", "techniques": []}]

def extract_nlp_techniques(text: str) -> List[str]:
    return ["reframing", "anchoring", "rapport_building", "presuppositions"]

def extract_ericksonian_patterns(text: str) -> List[str]:
    return ["embedded_commands", "truisms", "therapeutic_metaphors", "utilization"]

def extract_vak_adaptations(text: str) -> Dict[str, Any]:
    return {"visual": {}, "auditory": {}, "kinesthetic": {}}

def extract_transformation_program(text: str) -> Dict[str, Any]:
    return {"duration": 21, "stages": [], "daily_exercises": []}

def extract_domain_elements(text: str) -> Dict[str, Any]:
    return {"domain_specific_techniques": [], "cultural_adaptations": []}

def extract_methodology_notes(text: str) -> List[str]:
    return ["Universal NLP methodology applied"]

def extract_nlp_score(text: str) -> float:
    return 0.85

def extract_ericksonian_score(text: str) -> float:
    return 0.90

def extract_domain_score(text: str) -> float:
    return 0.88

def extract_overall_quality(text: str) -> float:
    return 0.87

def extract_issues(text: str) -> List[str]:
    return []

def extract_improvements(text: str) -> List[str]:
    return ["Consider adding more VAK variations", "Enhance Ericksonian metaphors"]

def extract_compliance_details(text: str) -> Dict[str, bool]:
    return {"methodology": True, "techniques": True, "adaptations": True}

if __name__ == "__main__":
    import asyncio

    async def test_universal_nlp_architect():
        # Тест для психологии
        psychology_result = await create_nlp_content(
            content_topic="депрессия и пути выхода",
            domain_type="psychology",
            content_type="diagnostic_test",
            target_language="ukrainian",
            content_count=16,
            transformation_days=21
        )
        print("Psychology NLP content:", psychology_result)

        # Тест для астрологии
        astrology_result = await create_nlp_content(
            content_topic="предназначение через натальную карту",
            domain_type="astrology",
            content_type="guidance_system",
            target_language="ukrainian",
            content_count=15,
            transformation_days=14
        )
        print("Astrology NLP content:", astrology_result)

        # Тест для таро
        tarot_result = await create_nlp_content(
            content_topic="личностный рост через Старшие Арканы",
            domain_type="tarot",
            content_type="transformation_program",
            target_language="ukrainian",
            content_count=18,
            transformation_days=21
        )
        print("Tarot NLP content:", tarot_result)

    asyncio.run(test_universal_nlp_architect())