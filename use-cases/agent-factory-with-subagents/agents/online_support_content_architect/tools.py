"""
Tools для Psychology Content Architect Agent
"""

from pydantic_ai import RunContext
from typing import Dict, List, Any, Optional
import json
from .dependencies import ArchitectDependencies, get_template

@RunContext.tool
async def analyze_program_requirements(
    ctx: RunContext[ArchitectDependencies],
    requirements_text: str,
    target_outcomes: List[str],
    constraints: Optional[Dict[str, Any]] = None
) -> str:
    """
    Анализировать требования к психологической программе.

    Args:
        requirements_text: Описание требований и целей программы
        target_outcomes: Список желаемых результатов
        constraints: Ограничения (время, ресурсы, формат)

    Returns:
        Анализ требований с рекомендациями по архитектуре
    """
    try:
        analysis = {
            "domain_analysis": analyze_psychological_domain(requirements_text),
            "population_needs": assess_population_needs(
                requirements_text,
                ctx.deps.target_population
            ),
            "outcome_mapping": map_outcomes_to_modules(target_outcomes),
            "constraint_impact": evaluate_constraints(
                constraints or ctx.deps.delivery_constraints
            ),
            "complexity_assessment": assess_program_complexity(
                requirements_text,
                target_outcomes
            ),
            "recommended_approach": recommend_therapeutic_approach(
                requirements_text,
                ctx.deps.psychological_domain
            )
        }

        return f"""
        Анализ требований программы:

        Психологический домен: {analysis['domain_analysis']}
        Потребности аудитории: {analysis['population_needs']}
        Картирование результатов: {analysis['outcome_mapping']}
        Влияние ограничений: {analysis['constraint_impact']}
        Оценка сложности: {analysis['complexity_assessment']}
        Рекомендуемый подход: {analysis['recommended_approach']}

        Ключевые архитектурные рекомендации:
        - Использовать {ctx.deps.architectural_style} структуру
        - Фокус на {ctx.deps.program_type} компонентах
        - Адаптация для {ctx.deps.target_population}
        """
    except Exception as e:
        return f"Ошибка анализа требований: {str(e)}"

@RunContext.tool
async def design_modular_structure(
    ctx: RunContext[ArchitectDependencies],
    core_components: List[str],
    duration_weeks: int,
    progression_type: str = "linear"
) -> str:
    """
    Спроектировать модульную структуру программы.

    Args:
        core_components: Основные компоненты программы
        duration_weeks: Общая длительность в неделях
        progression_type: Тип прогрессии (linear, spiral, adaptive)

    Returns:
        Детальная модульная структура программы
    """
    try:
        # Проверка на существующие шаблоны
        template = None
        if ctx.deps.psychological_domain in ["anxiety", "depression", "relationships"]:
            template_name = f"{ctx.deps.program_type}_{ctx.deps.psychological_domain}"
            template = get_template(template_name)

        modules = []
        week_counter = 0

        # Фаза foundation (25% времени)
        foundation_weeks = max(2, duration_weeks // 4)
        modules.append({
            "phase": "Foundation",
            "weeks": f"{week_counter + 1}-{week_counter + foundation_weeks}",
            "modules": create_foundation_modules(
                core_components,
                ctx.deps.target_population
            ),
            "focus": "baseline_establishment"
        })
        week_counter += foundation_weeks

        # Фаза development (50% времени)
        development_weeks = duration_weeks // 2
        modules.append({
            "phase": "Development",
            "weeks": f"{week_counter + 1}-{week_counter + development_weeks}",
            "modules": create_development_modules(
                core_components,
                progression_type
            ),
            "focus": "skill_building"
        })
        week_counter += development_weeks

        # Фаза integration (25% времени)
        integration_weeks = duration_weeks - week_counter
        modules.append({
            "phase": "Integration",
            "weeks": f"{week_counter + 1}-{duration_weeks}",
            "modules": create_integration_modules(
                core_components,
                ctx.deps.program_type
            ),
            "focus": "consolidation"
        })

        structure = {
            "total_duration": f"{duration_weeks} weeks",
            "phases": modules,
            "progression_type": progression_type,
            "flexibility": ctx.deps.flexibility_requirement,
            "template_used": template.name if template else "custom"
        }

        return f"""
        Модульная структура программы:

        {json.dumps(structure, indent=2, ensure_ascii=False)}

        Адаптационные возможности:
        - Гибкость темпа: {ctx.deps.flexibility_requirement}
        - Дополнительные модули доступны при необходимости
        - Возможность повторения модулей
        """
    except Exception as e:
        return f"Ошибка проектирования структуры: {str(e)}"

@RunContext.tool
async def optimize_sequence(
    ctx: RunContext[ArchitectDependencies],
    modules: List[Dict[str, Any]],
    optimization_criteria: List[str]
) -> str:
    """
    Оптимизировать последовательность модулей программы.

    Args:
        modules: Список модулей для оптимизации
        optimization_criteria: Критерии оптимизации (engagement, effectiveness, feasibility)

    Returns:
        Оптимизированная последовательность с обоснованием
    """
    try:
        # Анализ зависимостей между модулями
        dependencies = analyze_module_dependencies(modules)

        # Оптимизация на основе критериев
        optimized_sequence = []

        for criterion in optimization_criteria:
            if criterion == "engagement":
                # Начинаем с более вовлекающих модулей
                modules = sort_by_engagement_potential(modules)
            elif criterion == "effectiveness":
                # Следуем доказательной последовательности
                modules = sort_by_clinical_effectiveness(modules)
            elif criterion == "feasibility":
                # Учитываем ресурсные ограничения
                modules = sort_by_resource_requirements(modules)

        # Учет зависимостей
        optimized_sequence = respect_dependencies(modules, dependencies)

        return f"""
        Оптимизированная последовательность модулей:

        {format_sequence(optimized_sequence)}

        Обоснование оптимизации:
        - Критерии: {', '.join(optimization_criteria)}
        - Учтены зависимости между модулями
        - Соблюден принцип прогрессивной сложности
        - Оптимизирована вовлеченность участников
        """
    except Exception as e:
        return f"Ошибка оптимизации последовательности: {str(e)}"

@RunContext.tool
async def create_adaptation_framework(
    ctx: RunContext[ArchitectDependencies],
    base_architecture: Dict[str, Any],
    user_profiles: List[str]
) -> str:
    """
    Создать фреймворк адаптации архитектуры под разные профили пользователей.

    Args:
        base_architecture: Базовая архитектура программы
        user_profiles: Профили пользователей для адаптации

    Returns:
        Правила и механизмы адаптации
    """
    try:
        adaptation_rules = []

        for profile in user_profiles:
            rules = {
                "profile": profile,
                "adaptations": generate_profile_adaptations(
                    profile,
                    ctx.deps.psychological_domain
                ),
                "entry_point": determine_entry_point(profile, base_architecture),
                "pacing": determine_pacing(profile),
                "support_level": determine_support_level(profile),
                "optional_modules": select_optional_modules(profile)
            }
            adaptation_rules.append(rules)

        framework = {
            "base_architecture": base_architecture.get("name", "Custom"),
            "adaptation_rules": adaptation_rules,
            "flexibility_level": ctx.deps.flexibility_requirement,
            "adaptation_triggers": [
                "low_engagement",
                "high_distress",
                "rapid_progress",
                "resistance"
            ],
            "monitoring_points": [
                "module_completion",
                "weekly_assessment",
                "milestone_achievement"
            ]
        }

        return f"""
        Фреймворк адаптации программы:

        {json.dumps(framework, indent=2, ensure_ascii=False)}

        Ключевые адаптационные механизмы:
        - Гибкие точки входа для разных уровней готовности
        - Адаптивная скорость прохождения
        - Персонализированный уровень поддержки
        - Динамическое добавление/исключение модулей
        """
    except Exception as e:
        return f"Ошибка создания фреймворка адаптации: {str(e)}"

@RunContext.tool
async def search_architectural_patterns(
    ctx: RunContext[ArchitectDependencies],
    query: str,
    domain_filter: Optional[str] = None
) -> str:
    """
    Поиск архитектурных паттернов в базе знаний.

    Args:
        query: Поисковый запрос
        domain_filter: Фильтр по психологическому домену

    Returns:
        Релевантные архитектурные паттерны и примеры
    """
    try:
        # Здесь должен быть вызов RAG через MCP Archon
        # Для демонстрации возвращаем примеры паттернов

        patterns = {
            "anxiety": {
                "pattern": "Graduated Exposure Architecture",
                "structure": "Assessment → Psychoeducation → Skill Building → Graduated Exposure → Generalization",
                "key_features": ["Safety first", "Hierarchical approach", "Repeated practice"],
                "evidence_base": "Strong (multiple RCTs)"
            },
            "depression": {
                "pattern": "Behavioral Activation Architecture",
                "structure": "Monitoring → Activation → Cognitive Work → Relapse Prevention",
                "key_features": ["Activity scheduling", "Mood tracking", "Value clarification"],
                "evidence_base": "Strong (equivalent to CBT)"
            },
            "trauma": {
                "pattern": "Phase-Oriented Architecture",
                "structure": "Stabilization → Trauma Processing → Integration",
                "key_features": ["Safety establishment", "Window of tolerance", "Dual awareness"],
                "evidence_base": "Strong (international guidelines)"
            }
        }

        domain = domain_filter or ctx.deps.psychological_domain
        relevant_pattern = patterns.get(domain, patterns["anxiety"])

        return f"""
        Найденные архитектурные паттерны для {query}:

        Паттерн: {relevant_pattern['pattern']}
        Структура: {relevant_pattern['structure']}
        Ключевые особенности: {', '.join(relevant_pattern['key_features'])}
        Доказательная база: {relevant_pattern['evidence_base']}

        Рекомендация: Использовать данный паттерн как основу с адаптацией под специфику программы.
        """
    except Exception as e:
        return f"Ошибка поиска паттернов: {str(e)}"

# Вспомогательные функции для инструментов

def analyze_psychological_domain(text: str) -> str:
    """Анализ психологического домена из текста"""
    domains = {
        "anxiety": ["тревога", "беспокойство", "паника", "фобия", "anxiety"],
        "depression": ["депрессия", "подавленность", "апатия", "depression"],
        "trauma": ["травма", "ПТСР", "PTSD", "trauma"],
        "relationships": ["отношения", "пара", "семья", "relationship"]
    }

    text_lower = text.lower()
    for domain, keywords in domains.items():
        if any(keyword in text_lower for keyword in keywords):
            return domain

    return "general"

def assess_population_needs(text: str, population: str) -> str:
    """Оценка потребностей целевой аудитории"""
    needs_map = {
        "adults": "Фокус на практичность, интеграция в рабочий график",
        "adolescents": "Вовлеченность, peer support, технологии",
        "children": "Игровые элементы, вовлечение родителей",
        "couples": "Диадические упражнения, коммуникация",
        "elderly": "Адаптация темпа, учет физических ограничений"
    }
    return needs_map.get(population, "Стандартные потребности взрослой аудитории")

def map_outcomes_to_modules(outcomes: List[str]) -> str:
    """Картирование желаемых результатов на модули"""
    return f"Необходимые модули для достижения {len(outcomes)} целевых результатов"

def evaluate_constraints(constraints: Dict[str, Any]) -> str:
    """Оценка влияния ограничений на архитектуру"""
    impact = []
    if constraints.get("duration", 12) < 8:
        impact.append("Требуется интенсивный формат")
    if constraints.get("format") == "online":
        impact.append("Необходима адаптация для онлайн-доставки")
    if constraints.get("resources") == "minimal":
        impact.append("Упор на self-guided компоненты")

    return "; ".join(impact) if impact else "Стандартные ограничения"

def assess_program_complexity(text: str, outcomes: List[str]) -> str:
    """Оценка сложности программы"""
    if len(outcomes) > 5:
        return "Высокая (множественные цели)"
    elif "trauma" in text.lower() or "personality" in text.lower():
        return "Высокая (сложная проблематика)"
    elif len(outcomes) < 3:
        return "Низкая (фокусированная программа)"
    else:
        return "Средняя"

def recommend_therapeutic_approach(text: str, domain: str) -> str:
    """Рекомендация терапевтического подхода"""
    approaches = {
        "anxiety": "CBT с элементами экспозиции",
        "depression": "Behavioral Activation + Cognitive Restructuring",
        "trauma": "Phase-oriented treatment",
        "relationships": "EFT или Gottman Method"
    }
    return approaches.get(domain, "Интегративный подход")

def create_foundation_modules(components: List[str], population: str) -> List[str]:
    """Создание базовых модулей"""
    base = ["Assessment", "Psychoeducation", "Motivation building"]
    if population == "adolescents":
        base.append("Engagement strategies")
    return base

def create_development_modules(components: List[str], progression: str) -> List[str]:
    """Создание развивающих модулей"""
    return ["Skill building", "Practice", "Application"] + components[:3]

def create_integration_modules(components: List[str], program_type: str) -> List[str]:
    """Создание интеграционных модулей"""
    base = ["Consolidation", "Generalization"]
    if program_type == "therapeutic":
        base.append("Relapse prevention")
    return base

def analyze_module_dependencies(modules: List[Dict]) -> Dict[str, List[str]]:
    """Анализ зависимостей между модулями"""
    # Simplified dependency analysis
    return {"prerequisites": [], "corequisites": []}

def sort_by_engagement_potential(modules: List[Dict]) -> List[Dict]:
    """Сортировка по потенциалу вовлеченности"""
    return modules  # Placeholder

def sort_by_clinical_effectiveness(modules: List[Dict]) -> List[Dict]:
    """Сортировка по клинической эффективности"""
    return modules  # Placeholder

def sort_by_resource_requirements(modules: List[Dict]) -> List[Dict]:
    """Сортировка по требованиям к ресурсам"""
    return modules  # Placeholder

def respect_dependencies(modules: List[Dict], dependencies: Dict) -> List[Dict]:
    """Учет зависимостей в последовательности"""
    return modules  # Placeholder

def format_sequence(sequence: List[Dict]) -> str:
    """Форматирование последовательности для вывода"""
    if not sequence:
        return "Последовательность оптимизирована"
    return "\n".join([f"{i+1}. {m.get('name', 'Module')}" for i, m in enumerate(sequence)])

def generate_profile_adaptations(profile: str, domain: str) -> List[str]:
    """Генерация адаптаций для профиля"""
    return ["Adapted pacing", "Modified content", "Additional support"]

def determine_entry_point(profile: str, architecture: Dict) -> str:
    """Определение точки входа в программу"""
    return "Standard entry" if profile == "typical" else "Modified entry"

def determine_pacing(profile: str) -> str:
    """Определение темпа прохождения"""
    pacing_map = {
        "high_functioning": "accelerated",
        "typical": "standard",
        "complex_needs": "gradual"
    }
    return pacing_map.get(profile, "standard")

def determine_support_level(profile: str) -> str:
    """Определение уровня поддержки"""
    support_map = {
        "autonomous": "minimal",
        "typical": "standard",
        "high_needs": "intensive"
    }
    return support_map.get(profile, "standard")

def select_optional_modules(profile: str) -> List[str]:
    """Выбор опциональных модулей для профиля"""
    return ["Additional practice", "Peer support"] if profile == "high_needs" else []