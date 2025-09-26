#!/usr/bin/env python3
"""
Инструменты для Archon Blueprint Architect Agent.

Набор специализированных инструментов для архитектурного проектирования и дизайна систем.
"""

import json
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import BlueprintArchitectDependencies


class ArchitecturalDesign(BaseModel):
    """Модель архитектурного дизайна."""
    name: str = Field(description="Название архитектурного решения")
    pattern: str = Field(description="Архитектурный паттерн")
    components: List[str] = Field(description="Список компонентов системы")
    interfaces: List[Dict[str, str]] = Field(description="Интерфейсы между компонентами")
    data_flow: List[Dict[str, str]] = Field(description="Потоки данных")
    scalability_considerations: List[str] = Field(description="Соображения масштабируемости")
    security_layers: List[str] = Field(description="Слои безопасности")
    technology_stack: List[str] = Field(description="Технологический стек")


class SystemBlueprint(BaseModel):
    """Модель системного чертежа."""
    project_name: str = Field(description="Название проекта")
    architecture: ArchitecturalDesign = Field(description="Архитектурный дизайн")
    deployment_strategy: str = Field(description="Стратегия развертывания")
    monitoring_approach: str = Field(description="Подход к мониторингу")
    testing_strategy: str = Field(description="Стратегия тестирования")
    documentation_requirements: List[str] = Field(description="Требования к документации")


async def design_architecture(
    ctx: RunContext[BlueprintArchitectDependencies],
    requirements: str,
    scalability_target: str = "medium",
    technology_preferences: Optional[List[str]] = None
) -> ArchitecturalDesign:
    """
    Спроектировать архитектуру системы на основе требований.

    Args:
        ctx: Контекст выполнения с зависимостями
        requirements: Требования к системе
        scalability_target: Цель масштабируемости (small/medium/large/enterprise)
        technology_preferences: Предпочтительные технологии

    Returns:
        Архитектурный дизайн системы
    """
    deps = ctx.deps

    # Получаем конфигурацию архитектуры
    config = deps.get_architecture_config()
    constraints = deps.get_design_constraints()

    # Определяем технологический стек
    tech_stack = technology_preferences or deps.preferred_technologies

    # Анализируем требования для определения компонентов
    components = _analyze_components_from_requirements(requirements)

    # Проектируем интерфейсы
    interfaces = _design_component_interfaces(components)

    # Определяем потоки данных
    data_flow = _design_data_flows(components)

    # Добавляем соображения масштабируемости
    scalability_considerations = _get_scalability_considerations(
        scalability_target,
        config["pattern"]
    )

    # Проектируем слои безопасности
    security_layers = []
    if config["security_patterns"]:
        security_layers = _design_security_layers(components)

    return ArchitecturalDesign(
        name=f"Архитектура системы ({config['pattern']})",
        pattern=config["pattern"],
        components=components,
        interfaces=interfaces,
        data_flow=data_flow,
        scalability_considerations=scalability_considerations,
        security_layers=security_layers,
        technology_stack=tech_stack
    )


async def create_system_blueprint(
    ctx: RunContext[BlueprintArchitectDependencies],
    architecture_design: ArchitecturalDesign,
    project_name: str,
    deployment_environment: str = "cloud"
) -> SystemBlueprint:
    """
    Создать системный чертеж на основе архитектурного дизайна.

    Args:
        ctx: Контекст выполнения с зависимостями
        architecture_design: Архитектурный дизайн
        project_name: Название проекта
        deployment_environment: Среда развертывания

    Returns:
        Системный чертеж
    """
    deps = ctx.deps
    config = deps.get_architecture_config()

    # Определяем стратегию развертывания
    deployment_strategy = _determine_deployment_strategy(
        architecture_design.pattern,
        deployment_environment
    )

    # Подход к мониторингу
    monitoring_approach = "Комплексный мониторинг"
    if config["monitoring_patterns"]:
        monitoring_approach = _design_monitoring_approach(architecture_design.components)

    # Стратегия тестирования
    testing_strategy = _design_testing_strategy(architecture_design.pattern)

    # Требования к документации
    documentation_requirements = _define_documentation_requirements(architecture_design)

    return SystemBlueprint(
        project_name=project_name,
        architecture=architecture_design,
        deployment_strategy=deployment_strategy,
        monitoring_approach=monitoring_approach,
        testing_strategy=testing_strategy,
        documentation_requirements=documentation_requirements
    )


async def analyze_architectural_patterns(
    ctx: RunContext[BlueprintArchitectDependencies],
    domain: str,
    requirements: List[str]
) -> Dict[str, Any]:
    """
    Анализировать архитектурные паттерны для конкретного домена.

    Args:
        ctx: Контекст выполнения с зависимостями
        domain: Предметная область
        requirements: Список требований

    Returns:
        Анализ архитектурных паттернов
    """
    deps = ctx.deps

    # Анализируем подходящие паттерны
    suitable_patterns = []

    patterns_analysis = {
        "microservices": {
            "pros": ["Масштабируемость", "Независимое развертывание", "Технологическое разнообразие"],
            "cons": ["Сложность управления", "Сетевые задержки", "Консистентность данных"],
            "suitable_for": ["Большие команды", "Высокие нагрузки", "Быстрое развитие"]
        },
        "monolith": {
            "pros": ["Простота разработки", "Простое развертывание", "Производительность"],
            "cons": ["Сложность масштабирования", "Технологическая привязка", "Риски отказа"],
            "suitable_for": ["Малые команды", "Простые приложения", "Быстрый старт"]
        },
        "layered": {
            "pros": ["Четкое разделение", "Переиспользование", "Тестируемость"],
            "cons": ["Производительность", "Жесткая структура", "Сложность изменений"],
            "suitable_for": ["Корпоративные приложения", "Стандартные решения"]
        }
    }

    # Рекомендуем паттерны на основе требований
    recommended_pattern = _recommend_pattern_for_requirements(requirements)

    return {
        "domain": domain,
        "patterns_analysis": patterns_analysis,
        "recommended_pattern": recommended_pattern,
        "requirements_analysis": _analyze_requirements_complexity(requirements)
    }


async def validate_architecture(
    ctx: RunContext[BlueprintArchitectDependencies],
    blueprint: SystemBlueprint
) -> Dict[str, Any]:
    """
    Валидировать архитектурный дизайн.

    Args:
        ctx: Контекст выполнения с зависимостями
        blueprint: Системный чертеж

    Returns:
        Результаты валидации
    """
    deps = ctx.deps
    constraints = deps.get_design_constraints()

    validation_results = {
        "is_valid": True,
        "warnings": [],
        "errors": [],
        "recommendations": []
    }

    # Проверяем соответствие ограничениям
    if len(blueprint.architecture.components) > constraints.get("max_services", 50):
        validation_results["errors"].append(
            f"Превышено максимальное количество сервисов: {len(blueprint.architecture.components)} > {constraints['max_services']}"
        )
        validation_results["is_valid"] = False

    # Проверяем консистентность компонентов и интерфейсов
    component_names = blueprint.architecture.components
    interface_components = []
    for interface in blueprint.architecture.interfaces:
        interface_components.extend([interface.get("from", ""), interface.get("to", "")])

    missing_interfaces = set(component_names) - set(interface_components)
    if missing_interfaces:
        validation_results["warnings"].append(
            f"Компоненты без интерфейсов: {list(missing_interfaces)}"
        )

    # Проверяем безопасность
    if deps.include_security_patterns and not blueprint.architecture.security_layers:
        validation_results["warnings"].append(
            "Отсутствуют слои безопасности при включенной настройке безопасности"
        )

    # Рекомендации по улучшению
    validation_results["recommendations"] = _generate_architecture_recommendations(blueprint.architecture)

    return validation_results


async def search_architecture_knowledge(
    ctx: RunContext[BlueprintArchitectDependencies],
    query: str,
    knowledge_type: str = "patterns"
) -> Dict[str, Any]:
    """
    Поиск знаний об архитектуре в базе знаний.

    Args:
        ctx: Контекст выполнения с зависимостями
        query: Поисковый запрос
        knowledge_type: Тип знаний (patterns, examples, best-practices)

    Returns:
        Результаты поиска архитектурных знаний
    """
    deps = ctx.deps

    # Формируем расширенный запрос с тегами знаний
    enhanced_query = f"{query} {' '.join(deps.knowledge_tags)}"

    # Симуляция поиска в базе знаний
    # В реальной реализации здесь будет вызов RAG системы
    search_results = {
        "query": query,
        "knowledge_type": knowledge_type,
        "results": [
            {
                "title": f"Архитектурные паттерны для {query}",
                "content": f"Рекомендации по использованию паттернов в контексте {query}",
                "relevance": 0.95,
                "source": "architecture_knowledge_base"
            }
        ],
        "total_results": 1,
        "search_time_ms": 150
    }

    return search_results


def _analyze_components_from_requirements(requirements: str) -> List[str]:
    """Анализировать компоненты из требований."""
    # Базовые компоненты для большинства систем
    base_components = ["API Gateway", "Authentication Service", "Database"]

    # Добавляем компоненты на основе ключевых слов
    if "пользователь" in requirements.lower():
        base_components.append("User Management Service")
    if "уведомлен" in requirements.lower():
        base_components.append("Notification Service")
    if "платеж" in requirements.lower() or "оплат" in requirements.lower():
        base_components.append("Payment Service")
    if "файл" in requirements.lower() or "загрузк" in requirements.lower():
        base_components.append("File Storage Service")

    return base_components


def _design_component_interfaces(components: List[str]) -> List[Dict[str, str]]:
    """Спроектировать интерфейсы между компонентами."""
    interfaces = []

    # Базовые интерфейсы
    if "API Gateway" in components:
        for component in components:
            if component != "API Gateway" and "Service" in component:
                interfaces.append({
                    "from": "API Gateway",
                    "to": component,
                    "protocol": "HTTP/REST",
                    "description": f"API маршрутизация к {component}"
                })

    return interfaces


def _design_data_flows(components: List[str]) -> List[Dict[str, str]]:
    """Спроектировать потоки данных."""
    data_flows = []

    if "Database" in components:
        for component in components:
            if "Service" in component:
                data_flows.append({
                    "from": component,
                    "to": "Database",
                    "type": "data_persistence",
                    "description": f"Сохранение данных из {component}"
                })

    return data_flows


def _get_scalability_considerations(scalability_target: str, pattern: str) -> List[str]:
    """Получить соображения масштабируемости."""
    considerations = []

    if scalability_target == "enterprise":
        considerations.extend([
            "Горизонтальное масштабирование",
            "Кэширование на множественных уровнях",
            "Балансировка нагрузки",
            "Асинхронная обработка"
        ])

    if pattern == "microservices":
        considerations.extend([
            "Независимое масштабирование сервисов",
            "Service mesh для управления трафиком"
        ])

    return considerations


def _design_security_layers(components: List[str]) -> List[str]:
    """Спроектировать слои безопасности."""
    security_layers = [
        "API Authentication & Authorization",
        "Input Validation & Sanitization",
        "Data Encryption at Rest and in Transit",
        "Network Security & Firewalls"
    ]

    if "Database" in components:
        security_layers.append("Database Access Control")

    return security_layers


def _determine_deployment_strategy(pattern: str, environment: str) -> str:
    """Определить стратегию развертывания."""
    if pattern == "microservices":
        return "Контейнерное развертывание с оркестрацией (Kubernetes)"
    elif environment == "cloud":
        return "Облачное развертывание с автомасштабированием"
    else:
        return "Традиционное развертывание на серверах"


def _design_monitoring_approach(components: List[str]) -> str:
    """Спроектировать подход к мониторингу."""
    if len(components) > 5:
        return "Распределенный мониторинг с агрегацией метрик и трейсингом"
    else:
        return "Централизованный мониторинг с алертингом"


def _design_testing_strategy(pattern: str) -> str:
    """Спроектировать стратегию тестирования."""
    if pattern == "microservices":
        return "Пирамида тестирования: Unit -> Integration -> Contract -> E2E"
    else:
        return "Традиционная пирамида тестирования: Unit -> Integration -> E2E"


def _define_documentation_requirements(architecture: ArchitecturalDesign) -> List[str]:
    """Определить требования к документации."""
    docs = [
        "Архитектурная диаграмма системы",
        "API документация",
        "Руководство по развертыванию"
    ]

    if len(architecture.components) > 3:
        docs.append("Диаграмма взаимодействия компонентов")

    if architecture.security_layers:
        docs.append("Документация по безопасности")

    return docs


def _recommend_pattern_for_requirements(requirements: List[str]) -> str:
    """Рекомендовать паттерн на основе требований."""
    if any("масштабируем" in req.lower() for req in requirements):
        return "microservices"
    elif any("простот" in req.lower() for req in requirements):
        return "monolith"
    else:
        return "layered"


def _analyze_requirements_complexity(requirements: List[str]) -> Dict[str, Any]:
    """Анализировать сложность требований."""
    return {
        "complexity_level": "medium",
        "total_requirements": len(requirements),
        "functional_requirements": len([r for r in requirements if "должен" in r.lower()]),
        "non_functional_requirements": len([r for r in requirements if any(word in r.lower() for word in ["производительность", "безопасность", "масштабируемость"])])
    }


def _generate_architecture_recommendations(architecture: ArchitecturalDesign) -> List[str]:
    """Генерировать рекомендации по архитектуре."""
    recommendations = []

    if len(architecture.components) > 10:
        recommendations.append("Рассмотрите группировку компонентов в домены")

    if not architecture.security_layers:
        recommendations.append("Добавьте слои безопасности")

    if len(architecture.interfaces) < len(architecture.components) - 1:
        recommendations.append("Определите все необходимые интерфейсы между компонентами")

    return recommendations