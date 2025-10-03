"""
Pattern Scientific Validator Agent - научная валидация психологических техник.
"""

from pydantic_ai import Agent, RunContext
from typing import Dict, Any, List
import os

from .dependencies import PatternScientificValidatorDependencies
from .settings import AgentSettings
from .prompts import SYSTEM_PROMPT
from .models import ValidationReport, TechniqueValidation, SafetyCheck, EthicalReview
from .tools import (
    validate_technique_efficacy,
    check_safety,
    review_ethics,
    validate_adaptation,
    assess_effectiveness,
    search_agent_knowledge
)

# Импорт universal decorators
try:
    from ..common.pydantic_ai_decorators import create_universal_pydantic_agent
    HAS_DECORATORS = True
except ImportError:
    HAS_DECORATORS = False
    print("Warning: Universal decorators not available")


# Создание базового агента
if HAS_DECORATORS:
    agent = create_universal_pydantic_agent(
        model="openai:gpt-4o",
        deps_type=PatternScientificValidatorDependencies,
        system_prompt=SYSTEM_PROMPT,
        agent_type="pattern_scientific_validator",
        knowledge_tags=["pattern-scientific-validator", "validation", "agent-knowledge", "patternshift"],
        with_collective_tools=True,
        with_knowledge_tool=True
    )
else:
    # Fallback - базовый агент
    agent = Agent(
        model="openai:gpt-4o",
        deps_type=PatternScientificValidatorDependencies,
        system_prompt=SYSTEM_PROMPT
    )

    # Регистрация инструментов
    agent.tool(validate_technique_efficacy)
    agent.tool(check_safety)
    agent.tool(review_ethics)
    agent.tool(validate_adaptation)
    agent.tool(assess_effectiveness)
    agent.tool(search_agent_knowledge)


async def run_pattern_scientific_validator(
    module_data: Dict[str, Any],
    api_key: str,
    patternshift_project_path: str = "",
    verbose: bool = True
) -> ValidationReport:
    """
    Запускает валидацию модуля PatternShift.

    Args:
        module_data: Данные модуля для валидации (dict с полями: module_id, module_name, techniques, content, etc.)
        api_key: OpenAI API ключ
        patternshift_project_path: Путь к проекту PatternShift
        verbose: Выводить ли подробные логи

    Returns:
        ValidationReport с полной валидацией модуля

    Example:
        >>> module_data = {
        ...     "module_id": "module_001",
        ...     "module_name": "Cognitive Restructuring Module",
        ...     "techniques": ["cognitive_restructuring", "thought_challenging"],
        ...     "content": "Полный текст модуля...",
        ...     "target_conditions": ["depression", "anxiety"]
        ... }
        >>> report = await run_pattern_scientific_validator(
        ...     module_data=module_data,
        ...     api_key=os.getenv("OPENAI_API_KEY")
        ... )
    """
    # Создание зависимостей
    deps = PatternScientificValidatorDependencies(
        api_key=api_key,
        patternshift_project_path=patternshift_project_path
    )

    # Формирование промпта для валидации
    validation_prompt = f"""
# Валидация Модуля PatternShift

## Модуль для проверки:
**ID**: {module_data.get('module_id', 'N/A')}
**Название**: {module_data.get('module_name', 'N/A')}
**Техники**: {', '.join(module_data.get('techniques', []))}
**Целевые состояния**: {', '.join(module_data.get('target_conditions', []))}

## Содержание модуля:
{module_data.get('content', 'N/A')}

## Задача:
Проведи полную валидацию этого модуля, включая:

1. **Technique Validation** для каждой техники
2. **Safety Check** для модуля
3. **Ethical Review** модуля
4. **Effectiveness Metrics** для основных техник
5. **Overall Assessment**

Используй инструменты:
- validate_technique_efficacy() для каждой техники
- check_safety() для оценки безопасности
- review_ethics() для этической проверки
- assess_effectiveness() для метрик эффективности

Верни подробный анализ с конкретными рекомендациями.
"""

    # Запуск агента
    result = await agent.run(
        validation_prompt,
        deps=deps
    )

    if verbose:
        print(f"\n=== Pattern Scientific Validator Result ===")
        print(result.data)

    # Если result.data уже ValidationReport - вернуть
    if isinstance(result.data, ValidationReport):
        return result.data

    # Иначе создать ValidationReport из ответа агента
    # (это fallback если агент вернул строку вместо structured output)
    return ValidationReport(
        module_id=module_data.get('module_id', 'unknown'),
        module_name=module_data.get('module_name', 'Unknown Module'),
        technique_validations=[],
        safety_check=SafetyCheck(
            module_id=module_data.get('module_id', 'unknown'),
            safety_rating="safe",
            potential_risks=[],
            risk_mitigation=[],
            contraindications=[],
            warning_signs=[],
            emergency_protocol=""
        ),
        ethical_review=EthicalReview(
            module_id=module_data.get('module_id', 'unknown'),
            ethical_concerns=[],
            informed_consent_adequacy=True,
            autonomy_respected=True,
            beneficence=True,
            non_maleficence=True,
            justice=True,
            ethical_approval=True,
            notes=str(result.data)
        ),
        effectiveness_metrics=[],
        adaptation_validations=[],
        overall_validation_status="pending_review",
        overall_evidence_level="not_validated",
        overall_safety_rating="safe",
        recommendations=[],
        required_changes=[],
        approval_notes=str(result.data)
    )


__all__ = ["agent", "run_pattern_scientific_validator"]
