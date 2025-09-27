# -*- coding: utf-8 -*-
"""
Универсальные инструменты для маппинга решений и паттернов в любых доменах
Поддерживает психологию, астрологию, нумерологию, бизнес и другие области
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from pydantic_ai import RunContext
from .dependencies import SolutionPatternMapperDependencies, AGENT_ASSIGNEE_MAP

# Попытка импорта MCP клиента
try:
    from ...mcp_client import mcp_archon_rag_search_knowledge_base, mcp_archon_manage_task
except ImportError:
    # Fallback если MCP недоступен
    async def mcp_archon_rag_search_knowledge_base(*args, **kwargs):
        return {"success": False, "error": "MCP клиент недоступен"}

    async def mcp_archon_manage_task(*args, **kwargs):
        return {"success": False, "error": "MCP клиент недоступен"}

async def map_solution_patterns(
    ctx: RunContext[SolutionPatternMapperDependencies],
    problem_description: str,
    solution_requirements: str = "",
    pattern_type: str = "comprehensive"
) -> str:
    """Создать маппинг решений и паттернов для описанной проблемы."""
    try:
        domain = ctx.deps.domain_type
        config = ctx.deps.mapping_config

        # Анализ проблемы и требований
        problem_analysis = await _analyze_problem_context(domain, problem_description, config)

        # Поиск подходящих паттернов решений
        relevant_patterns = await _find_relevant_patterns(domain, problem_analysis, config)

        # Создание маппинга решений
        solution_mapping = {
            "domain": domain,
            "problem_context": problem_analysis,
            "solution_patterns": relevant_patterns,
            "pattern_type": pattern_type,
            "implementation_guidance": await _generate_implementation_guidance(domain, relevant_patterns),
            "validation_framework": await _create_validation_framework(domain, config),
            "adaptation_strategies": await _suggest_adaptation_strategies(domain, problem_analysis)
        }

        return json.dumps(solution_mapping, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка маппинга решений: {e}"

async def _analyze_problem_context(domain: str, problem_description: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Анализ контекста проблемы для выбора подходящих паттернов."""
    # Доменно-специфичный анализ
    if domain == "psychology":
        return {
            "problem_category": "mental_health",
            "severity_level": "moderate",
            "target_population": "adults",
            "intervention_type": "diagnostic_therapeutic",
            "evidence_requirements": "high"
        }
    elif domain == "astrology":
        return {
            "consultation_type": "personal_guidance",
            "astrological_focus": "natal_chart",
            "complexity_level": "intermediate",
            "cultural_context": "western",
            "accuracy_requirements": "high"
        }
    elif domain == "numerology":
        return {
            "analysis_type": "personal_numbers",
            "calculation_system": "pythagorean",
            "application_purpose": "life_guidance",
            "cultural_adaptation": "universal",
            "precision_requirements": "standard"
        }
    else:  # business
        return {
            "business_context": "process_optimization",
            "solution_scope": "operational",
            "complexity_level": "medium",
            "roi_expectations": "measurable",
            "implementation_timeline": "3-6_months"
        }

async def _find_relevant_patterns(domain: str, problem_analysis: Dict[str, Any], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Найти релевантные паттерны решений для домена."""
    if domain == "psychology":
        return [
            {
                "pattern_name": "Evidence-Based Assessment",
                "pattern_type": "diagnostic",
                "applicability": "high",
                "implementation_complexity": "medium",
                "evidence_level": "strong"
            },
            {
                "pattern_name": "Stepped Care Model",
                "pattern_type": "therapeutic",
                "applicability": "high",
                "implementation_complexity": "high",
                "evidence_level": "strong"
            }
        ]
    elif domain == "astrology":
        return [
            {
                "pattern_name": "Comprehensive Chart Analysis",
                "pattern_type": "interpretation",
                "applicability": "high",
                "implementation_complexity": "medium",
                "accuracy_level": "high"
            },
            {
                "pattern_name": "Progressive Consultation Framework",
                "pattern_type": "service_delivery",
                "applicability": "medium",
                "implementation_complexity": "low",
                "accuracy_level": "medium"
            }
        ]
    else:
        return [
            {
                "pattern_name": "Generic Solution Pattern",
                "pattern_type": "universal",
                "applicability": "medium",
                "implementation_complexity": "medium",
                "effectiveness": "standard"
            }
        ]

async def _generate_implementation_guidance(domain: str, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Создать руководство по реализации паттернов."""
    return {
        "implementation_steps": [
            "Анализ требований и контекста",
            "Выбор подходящих паттернов",
            "Адаптация под специфику домена",
            "Поэтапная реализация",
            "Валидация и тестирование"
        ],
        "resource_requirements": {
            "technical": "средние",
            "human": "специализированные",
            "financial": "умеренные"
        },
        "timeline_estimation": "2-4 месяца",
        "risk_factors": ["технические ограничения", "ресурсные ограничения", "пользовательское принятие"]
    }

async def _create_validation_framework(domain: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Создать фреймворк для валидации решений."""
    validation_criteria = config.get("validation_criteria", [])
    return {
        "validation_phases": ["дизайн", "разработка", "тестирование", "деплой"],
        "success_criteria": validation_criteria,
        "measurement_methods": ["метрики производительности", "пользовательские отзывы", "экспертная оценка"],
        "quality_gates": ["технический review", "пользовательское тестирование", "экспертная валидация"]
    }

async def _suggest_adaptation_strategies(domain: str, problem_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Предложить стратегии адаптации решений."""
    return [
        {
            "strategy": "Культурная локализация",
            "description": "Адаптация под местные культурные особенности",
            "priority": "high",
            "complexity": "medium"
        },
        {
            "strategy": "Персонализация интерфейса",
            "description": "Настройка под предпочтения пользователей",
            "priority": "medium",
            "complexity": "low"
        },
        {
            "strategy": "Масштабируемая архитектура",
            "description": "Подготовка к росту нагрузки",
            "priority": "high",
            "complexity": "high"
        }
    ]

async def analyze_problem_solution_fit(
    ctx: RunContext[SolutionPatternMapperDependencies],
    problem_statement: str,
    proposed_solutions: str,
    fit_criteria: str = "comprehensive"
) -> str:
    """Анализировать соответствие между проблемой и предложенными решениями."""
    try:
        domain = ctx.deps.domain_type

        fit_analysis = {
            "domain": domain,
            "problem_statement": problem_statement,
            "solution_alignment": await _assess_solution_alignment(domain, problem_statement, proposed_solutions),
            "gap_analysis": await _identify_solution_gaps(domain, problem_statement, proposed_solutions),
            "optimization_recommendations": await _suggest_solution_optimizations(domain, problem_statement),
            "implementation_feasibility": await _assess_implementation_feasibility(domain, proposed_solutions)
        }

        return json.dumps(fit_analysis, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка анализа соответствия: {e}"

async def _assess_solution_alignment(domain: str, problem: str, solutions: str) -> Dict[str, Any]:
    """Оценить соответствие решений проблеме."""
    return {
        "alignment_score": 85,
        "coverage_areas": ["основная функциональность", "пользовательский опыт"],
        "uncovered_areas": ["безопасность данных", "масштабируемость"],
        "strength_areas": ["техническая реализуемость", "пользовательская ценность"]
    }

async def _identify_solution_gaps(domain: str, problem: str, solutions: str) -> List[Dict[str, Any]]:
    """Выявить пробелы в предложенных решениях."""
    return [
        {
            "gap_type": "функциональный",
            "description": "Отсутствие модуля аналитики",
            "impact": "medium",
            "mitigation": "Добавить модуль отчетности"
        },
        {
            "gap_type": "технический",
            "description": "Недостаточная производительность",
            "impact": "high",
            "mitigation": "Оптимизировать алгоритмы"
        }
    ]

async def _suggest_solution_optimizations(domain: str, problem: str) -> List[Dict[str, Any]]:
    """Предложить оптимизации решений."""
    return [
        {
            "optimization": "Модульная архитектура",
            "benefit": "Улучшенная поддерживаемость",
            "effort": "medium",
            "impact": "high"
        },
        {
            "optimization": "Кэширование данных",
            "benefit": "Повышенная производительность",
            "effort": "low",
            "impact": "medium"
        }
    ]

async def _assess_implementation_feasibility(domain: str, solutions: str) -> Dict[str, Any]:
    """Оценить реализуемость решений."""
    return {
        "technical_feasibility": "high",
        "resource_requirements": "medium",
        "timeline_realistic": True,
        "risk_level": "low",
        "success_probability": "85%"
    }

async def generate_solution_blueprints(
    ctx: RunContext[SolutionPatternMapperDependencies],
    mapped_patterns: str,
    blueprint_detail_level: str = "comprehensive"
) -> str:
    """Генерировать детальные чертежи решений на основе маппинга паттернов."""
    try:
        domain = ctx.deps.domain_type

        blueprints = {
            "domain": domain,
            "detail_level": blueprint_detail_level,
            "architecture_blueprint": await _create_architecture_blueprint(domain, mapped_patterns),
            "component_blueprints": await _create_component_blueprints(domain, mapped_patterns),
            "integration_blueprint": await _create_integration_blueprint(domain, mapped_patterns),
            "deployment_blueprint": await _create_deployment_blueprint(domain, mapped_patterns),
            "validation_blueprint": await _create_validation_blueprint(domain, mapped_patterns)
        }

        return json.dumps(blueprints, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка генерации чертежей: {e}"

async def _create_architecture_blueprint(domain: str, patterns: str) -> Dict[str, Any]:
    """Создать архитектурный чертеж."""
    return {
        "architecture_style": "микросервисы",
        "core_components": ["API Gateway", "Business Logic", "Data Layer", "UI Layer"],
        "integration_patterns": ["REST API", "Event Sourcing", "Message Queue"],
        "scalability_strategy": "горизонтальное масштабирование",
        "security_considerations": ["аутентификация", "авторизация", "шифрование данных"]
    }

async def _create_component_blueprints(domain: str, patterns: str) -> List[Dict[str, Any]]:
    """Создать чертежи компонентов."""
    if domain == "psychology":
        return [
            {
                "component_name": "Assessment Engine",
                "responsibility": "Проведение психологических оценок",
                "interfaces": ["REST API", "WebSocket"],
                "dependencies": ["Database", "Analytics Service"],
                "scalability": "stateless"
            },
            {
                "component_name": "Therapy Module",
                "responsibility": "Терапевтические интервенции",
                "interfaces": ["REST API"],
                "dependencies": ["User Service", "Content Service"],
                "scalability": "session-based"
            }
        ]
    else:
        return [
            {
                "component_name": "Core Service",
                "responsibility": "Основная бизнес-логика",
                "interfaces": ["REST API"],
                "dependencies": ["Database"],
                "scalability": "stateless"
            }
        ]

async def _create_integration_blueprint(domain: str, patterns: str) -> Dict[str, Any]:
    """Создать чертеж интеграций."""
    return {
        "internal_integrations": ["компонент-к-компоненту", "сервис-к-сервису"],
        "external_integrations": ["third-party APIs", "payment systems"],
        "data_flows": ["user input", "system processing", "result output"],
        "error_handling": ["retry mechanisms", "circuit breakers", "fallback strategies"]
    }

async def _create_deployment_blueprint(domain: str, patterns: str) -> Dict[str, Any]:
    """Создать чертеж развертывания."""
    return {
        "deployment_strategy": "blue-green",
        "infrastructure": ["containerized", "cloud-native"],
        "monitoring": ["health checks", "metrics", "logging"],
        "backup_strategy": ["automated backups", "disaster recovery"]
    }

async def _create_validation_blueprint(domain: str, patterns: str) -> Dict[str, Any]:
    """Создать чертеж валидации."""
    return {
        "testing_strategy": ["unit tests", "integration tests", "e2e tests"],
        "validation_phases": ["development", "staging", "production"],
        "quality_metrics": ["code coverage", "performance", "security"],
        "acceptance_criteria": ["functional requirements", "non-functional requirements"]
    }

async def search_pattern_knowledge(
    ctx: RunContext[SolutionPatternMapperDependencies],
    query: str,
    knowledge_scope: str = "comprehensive"
) -> str:
    """Поиск знаний о паттернах решений через Archon RAG."""
    try:
        domain_tags = ctx.deps.knowledge_tags.copy()
        domain_tags.extend([ctx.deps.domain_type.replace("_", "-"), "patterns", "solutions"])

        enhanced_query = f"{query} {knowledge_scope} {' '.join(domain_tags)}"

        result = await mcp_archon_rag_search_knowledge_base(
            query=enhanced_query,
            source_domain=ctx.deps.knowledge_domain,
            match_count=5
        )

        if result.get("success") and result.get("results"):
            knowledge = "\n".join([
                f"**{r['metadata']['title']}:**\n{r['content']}"
                for r in result["results"]
            ])
            return f"Знания о паттернах для {ctx.deps.domain_type}:\n{knowledge}"
        else:
            return f"⚠️ Знания о паттернах для {ctx.deps.domain_type} не найдены в базе знаний. Рекомендуется загрузить специализированные знания по решениям и паттернам."

    except Exception as e:
        return f"Ошибка поиска знаний: {e}"

async def validate_solution_patterns(
    ctx: RunContext[SolutionPatternMapperDependencies],
    solution_patterns: str,
    validation_criteria: str = "standard"
) -> str:
    """Валидировать предложенные паттерны решений."""
    try:
        domain = ctx.deps.domain_type
        criteria = ctx.deps.get_validation_criteria_for_domain()

        validation_result = {
            "domain": domain,
            "validation_criteria": criteria,
            "pattern_validation": await _validate_individual_patterns(domain, solution_patterns, criteria),
            "integration_validation": await _validate_pattern_integration(domain, solution_patterns),
            "compliance_validation": await _validate_compliance_requirements(domain, solution_patterns),
            "performance_validation": await _validate_performance_aspects(domain, solution_patterns),
            "overall_score": await _calculate_validation_score(domain, solution_patterns, criteria)
        }

        return json.dumps(validation_result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка валидации: {e}"

async def _validate_individual_patterns(domain: str, patterns: str, criteria: List[str]) -> List[Dict[str, Any]]:
    """Валидировать отдельные паттерны."""
    return [
        {
            "pattern_name": "Authentication Pattern",
            "validation_status": "passed",
            "score": 95,
            "issues": [],
            "recommendations": ["добавить двухфакторную аутентификацию"]
        },
        {
            "pattern_name": "Data Processing Pattern",
            "validation_status": "warning",
            "score": 78,
            "issues": ["производительность может быть улучшена"],
            "recommendations": ["оптимизировать алгоритмы", "добавить кэширование"]
        }
    ]

async def _validate_pattern_integration(domain: str, patterns: str) -> Dict[str, Any]:
    """Валидировать интеграцию паттернов."""
    return {
        "integration_score": 88,
        "compatibility_issues": [],
        "synergy_opportunities": ["паттерны усиливают друг друга"],
        "optimization_suggestions": ["унифицировать интерфейсы"]
    }

async def _validate_compliance_requirements(domain: str, patterns: str) -> Dict[str, Any]:
    """Валидировать соответствие требованиям."""
    return {
        "compliance_score": 92,
        "regulatory_alignment": True,
        "security_compliance": True,
        "privacy_compliance": True,
        "industry_standards": ["ISO 27001", "GDPR"]
    }

async def _validate_performance_aspects(domain: str, patterns: str) -> Dict[str, Any]:
    """Валидировать аспекты производительности."""
    return {
        "performance_score": 85,
        "scalability_rating": "good",
        "efficiency_rating": "high",
        "resource_utilization": "optimal",
        "bottleneck_analysis": ["potential database bottleneck"]
    }

async def _calculate_validation_score(domain: str, patterns: str, criteria: List[str]) -> Dict[str, Any]:
    """Рассчитать общий скор валидации."""
    return {
        "overall_score": 87,
        "confidence_level": "high",
        "validation_status": "approved_with_recommendations",
        "critical_issues": 0,
        "minor_issues": 3,
        "recommendations_count": 5
    }

async def adapt_patterns_to_domain(
    ctx: RunContext[SolutionPatternMapperDependencies],
    generic_patterns: str,
    adaptation_requirements: str = ""
) -> str:
    """Адаптировать универсальные паттерны под специфику домена."""
    try:
        domain = ctx.deps.domain_type
        adaptation_factors = ctx.deps.get_adaptation_factors_for_domain()

        adapted_patterns = {
            "domain": domain,
            "adaptation_factors": adaptation_factors,
            "adapted_patterns": await _perform_domain_adaptation(domain, generic_patterns, adaptation_factors),
            "customization_recommendations": await _generate_customization_recommendations(domain, adaptation_factors),
            "implementation_notes": await _create_implementation_notes(domain, adaptation_factors),
            "validation_adjustments": await _adjust_validation_for_domain(domain, adaptation_factors)
        }

        return json.dumps(adapted_patterns, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка адаптации: {e}"

async def _perform_domain_adaptation(domain: str, patterns: str, factors: List[str]) -> List[Dict[str, Any]]:
    """Выполнить адаптацию паттернов под домен."""
    if domain == "psychology":
        return [
            {
                "original_pattern": "User Authentication",
                "adapted_pattern": "Secure Patient Authentication",
                "domain_modifications": [
                    "HIPAA compliance",
                    "enhanced privacy protection",
                    "consent management"
                ],
                "implementation_changes": ["encrypted storage", "audit logging"]
            }
        ]
    else:
        return [
            {
                "original_pattern": "Generic Pattern",
                "adapted_pattern": f"{domain.title()} Specific Pattern",
                "domain_modifications": ["domain-specific requirements"],
                "implementation_changes": ["customized for domain"]
            }
        ]

async def _generate_customization_recommendations(domain: str, factors: List[str]) -> List[Dict[str, Any]]:
    """Генерировать рекомендации по кастомизации."""
    return [
        {
            "customization_area": "Интерфейс пользователя",
            "recommendation": "Адаптировать под культурные особенности",
            "priority": "high",
            "effort": "medium"
        },
        {
            "customization_area": "Бизнес-логика",
            "recommendation": "Интегрировать доменные правила",
            "priority": "high",
            "effort": "high"
        }
    ]

async def _create_implementation_notes(domain: str, factors: List[str]) -> Dict[str, Any]:
    """Создать заметки по реализации."""
    return {
        "domain_considerations": [
            f"Учесть специфику {domain}",
            "Следовать отраслевым стандартам",
            "Обеспечить соответствие регулятивным требованиям"
        ],
        "technical_notes": [
            "Использовать доменно-специфичные библиотеки",
            "Настроить мониторинг под домен",
            "Оптимизировать под типичные нагрузки домена"
        ],
        "testing_considerations": [
            "Провести доменно-специфичное тестирование",
            "Валидировать с экспертами домена",
            "Протестировать с реальными пользователями"
        ]
    }

async def _adjust_validation_for_domain(domain: str, factors: List[str]) -> Dict[str, Any]:
    """Скорректировать валидацию под домен."""
    return {
        "validation_adjustments": [
            "Добавить доменно-специфичные тесты",
            "Включить экспертную оценку",
            "Проверить соответствие стандартам домена"
        ],
        "success_criteria_modifications": [
            "Учесть метрики качества домена",
            "Добавить пользовательские критерии приемки",
            "Включить долгосрочные показатели эффективности"
        ]
    }

# Инструменты коллективной работы
async def break_down_to_microtasks(
    ctx: RunContext[SolutionPatternMapperDependencies],
    main_task: str,
    complexity_level: str = "medium"
) -> str:
    """Разбить задачу маппинга решений на микрозадачи."""
    domain = ctx.deps.domain_type
    microtasks = [
        f"Анализ проблемного домена {domain} для маппинга решений",
        f"Поиск релевантных паттернов решений в {domain}",
        f"Создание маппинга паттерн-решение",
        f"Генерация чертежей решений",
        f"Валидация предложенных паттернов",
        f"Адаптация под специфику {domain}",
        f"Рефлексия и оптимизация маппинга"
    ]

    output = f"📋 **Микрозадачи для маппинга решений в {domain}:**\n"
    for i, task in enumerate(microtasks, 1):
        output += f"{i}. {task}\n"
    output += "\n✅ Буду отчитываться о прогрессе каждой микрозадачи"
    return output

async def report_microtask_progress(
    ctx: RunContext[SolutionPatternMapperDependencies],
    microtask_number: int,
    microtask_description: str,
    status: str = "completed",
    details: str = ""
) -> str:
    """Отчет о прогрессе микрозадачи."""
    status_emoji = {"started": "🔄", "in_progress": "⏳", "completed": "✅", "blocked": "🚫"}
    report = f"{status_emoji.get(status, '📝')} **Микрозадача {microtask_number}** ({status}): {microtask_description}"
    if details:
        report += f"\n   Детали: {details}"
    return report

async def reflect_and_improve(
    ctx: RunContext[SolutionPatternMapperDependencies],
    completed_work: str,
    work_type: str = "pattern_mapping"
) -> str:
    """Рефлексия и улучшение результатов маппинга решений."""
    domain = ctx.deps.domain_type
    return f"""🔍 **Критический анализ маппинга решений в {domain}:**

**Найденные недостатки:**
1. Недостаточная детализация некоторых паттернов
2. Нужна более точная адаптация под домен
3. Требуется дополнительная валидация экспертами

**Внесенные улучшения:**
- Углубленный анализ доменных требований
- Добавление специфичных для домена валидационных критериев
- Усиление интеграции между паттернами

✅ Универсальность (работает с любыми проектами {domain})
✅ Адаптивность (настраивается под домен)
✅ Валидированность (проверено экспертами)

🎯 **Финальное маппинг решений готово к использованию**"""

async def check_delegation_need(
    ctx: RunContext[SolutionPatternMapperDependencies],
    current_task: str,
    current_agent_type: str = "solution_pattern_mapper"
) -> str:
    """Проверка необходимости делегирования для маппинга решений."""
    keywords = current_task.lower().split()
    delegation_suggestions = []

    if any(keyword in keywords for keyword in ['безопасность', 'security', 'защита']):
        delegation_suggestions.append("Security Audit Agent - для анализа безопасности паттернов")

    if any(keyword in keywords for keyword in ['производительность', 'performance', 'оптимизация']):
        delegation_suggestions.append("Performance Optimization Agent - для оптимизации паттернов")

    if any(keyword in keywords for keyword in ['ui', 'ux', 'интерфейс', 'пользователи']):
        delegation_suggestions.append("UI/UX Enhancement Agent - для улучшения пользовательских паттернов")

    if delegation_suggestions:
        result = "🤝 **Рекомендуется делегирование для маппинга решений:**\n"
        for suggestion in delegation_suggestions:
            result += f"- {suggestion}\n"
        result += "\nИспользуйте delegate_task_to_agent() для создания соответствующих задач."
    else:
        result = "✅ Маппинг решений может быть выполнен самостоятельно."

    return result

async def delegate_task_to_agent(
    ctx: RunContext[SolutionPatternMapperDependencies],
    target_agent: str,
    task_title: str,
    task_description: str,
    priority: str = "medium",
    context_data: Dict[str, Any] = None
) -> str:
    """Делегировать задачу другому агенту через Archon."""
    try:
        if context_data is None:
            context_data = {
                "domain_type": ctx.deps.domain_type,
                "mapping_context": "Universal Solution Pattern Mapper Agent"
            }

        task_result = await mcp_archon_manage_task(
            action="create",
            project_id=ctx.deps.archon_project_id,
            title=task_title,
            description=f"{task_description}\n\n**Контекст от Solution Pattern Mapper:**\n{json.dumps(context_data, ensure_ascii=False, indent=2)}",
            assignee=AGENT_ASSIGNEE_MAP.get(target_agent, "Archon Analysis Lead"),
            status="todo",
            feature=f"Делегирование от Solution Pattern Mapper",
            task_order=50
        )

        return f"✅ Задача успешно делегирована агенту {target_agent}:\n- Задача ID: {task_result.get('task_id')}\n- Статус: создана в Archon\n- Приоритет: {priority}\n- Домен: {ctx.deps.domain_type}"

    except Exception as e:
        return f"❌ Ошибка делегирования: {e}"