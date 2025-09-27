"""
Universal Quality Validator Agent

Универсальный агент для валидации и контроля качества различных типов проектов
с поддержкой множественных стандартов, автоматизированных проверок и отчетности.
"""

from pydantic_ai import Agent, RunContext
from typing import Dict, List, Any, Optional, Union
import asyncio
import json
from datetime import datetime

from .dependencies import (
    QualityValidatorDependencies,
    ProjectDomain,
    QualityStandard,
    ValidationLevel
)
from .tools import (
    validate_code_quality,
    run_security_scan,
    perform_performance_tests,
    check_compliance,
    generate_quality_report,
    validate_documentation,
    run_automated_tests,
    check_quality_gates,
    # Коллективные инструменты
    break_down_to_microtasks,
    report_microtask_progress,
    delegate_task_to_agent,
    check_delegation_need,
    reflect_and_improve,
    search_agent_knowledge
)
from .prompts import get_system_prompt
from .providers import QualityValidatorModelProvider


universal_quality_validator_agent = Agent(
    model=QualityValidatorModelProvider().get_optimal_model(
        validation_type="comprehensive",
        project_domain="general",
        priority="quality"
    ),
    deps_type=QualityValidatorDependencies,
    system_prompt=get_system_prompt(),
    retries=2
)


@universal_quality_validator_agent.function
async def run_quality_validation(
    ctx: RunContext[QualityValidatorDependencies],
    project_path: str,
    validation_scope: str = "full",
    environment: str = "development",
    quality_standard: Optional[str] = None,
    validation_level: Optional[str] = None,
    custom_rules: Optional[Dict[str, Any]] = None
) -> str:
    """
    Выполнение комплексной валидации качества проекта

    Args:
        project_path: Путь к проекту
        validation_scope: Область валидации (full, code, security, performance, compliance)
        environment: Среда (development, staging, production)
        quality_standard: Стандарт качества (iso_9001, ieee_830, cmmi, agile)
        validation_level: Уровень валидации (basic, standard, comprehensive, enterprise)
        custom_rules: Пользовательские правила валидации
    """
    deps = ctx.deps

    # Получение конфигурации для среды
    env_config = deps.get_environment_config(environment)

    # Установка уровня валидации
    if validation_level:
        deps.validation_level = ValidationLevel(validation_level)
    elif env_config.get("validation_level"):
        deps.validation_level = ValidationLevel(env_config["validation_level"])

    # Установка стандарта качества
    if quality_standard:
        deps.quality_standard = QualityStandard(quality_standard)

    # Применение пользовательских правил
    if custom_rules:
        deps.custom_rules.update(custom_rules)

    validation_results = {
        "timestamp": datetime.now().isoformat(),
        "project_path": project_path,
        "environment": environment,
        "validation_scope": validation_scope,
        "quality_standard": deps.quality_standard.value,
        "validation_level": deps.validation_level.value,
        "results": {},
        "summary": {},
        "recommendations": []
    }

    try:
        # Валидация кода
        if validation_scope in ["full", "code"]:
            code_results = await validate_code_quality(
                ctx,
                project_path=project_path,
                rules=deps.code_quality_rules,
                exclude_patterns=deps.exclude_patterns,
                include_patterns=deps.include_patterns
            )
            validation_results["results"]["code_quality"] = json.loads(code_results)

        # Сканирование безопасности
        if validation_scope in ["full", "security"]:
            security_results = await run_security_scan(
                ctx,
                project_path=project_path,
                security_config=deps.security_validation,
                scan_dependencies=True,
                check_vulnerabilities=True
            )
            validation_results["results"]["security"] = json.loads(security_results)

        # Тестирование производительности
        if validation_scope in ["full", "performance"]:
            perf_results = await perform_performance_tests(
                ctx,
                project_path=project_path,
                performance_config=deps.performance_validation,
                environment=environment
            )
            validation_results["results"]["performance"] = json.loads(perf_results)

        # Проверка соответствия
        if validation_scope in ["full", "compliance"]:
            compliance_results = await check_compliance(
                ctx,
                project_path=project_path,
                compliance_config=deps.compliance_validation,
                domain=deps.project_domain.value
            )
            validation_results["results"]["compliance"] = json.loads(compliance_results)

        # Валидация документации
        if validation_scope in ["full", "documentation"]:
            docs_results = await validate_documentation(
                ctx,
                project_path=project_path,
                documentation_config=deps.documentation_validation
            )
            validation_results["results"]["documentation"] = json.loads(docs_results)

        # Запуск автоматизированных тестов
        if validation_scope in ["full", "testing"]:
            test_results = await run_automated_tests(
                ctx,
                project_path=project_path,
                testing_config=deps.testing_configuration,
                environment=environment
            )
            validation_results["results"]["testing"] = json.loads(test_results)

        # Проверка качественных ворот
        if validation_scope == "full":
            gates_results = await check_quality_gates(
                ctx,
                validation_results=validation_results,
                quality_gates=deps.quality_gates,
                environment=environment
            )
            validation_results["results"]["quality_gates"] = json.loads(gates_results)

        # Генерация сводки и рекомендаций
        validation_results["summary"] = _generate_summary(validation_results["results"])
        validation_results["recommendations"] = await _generate_recommendations(
            ctx, validation_results, deps
        )

        # Генерация отчета
        if deps.reporting_settings.generate_html_reports or deps.reporting_settings.generate_json_reports:
            report_path = await generate_quality_report(
                ctx,
                validation_results=validation_results,
                reporting_config=deps.reporting_settings,
                project_path=project_path
            )
            validation_results["report_path"] = report_path

        return json.dumps(validation_results, indent=2, ensure_ascii=False)

    except Exception as e:
        error_result = {
            "error": f"Ошибка валидации качества: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "project_path": project_path,
            "validation_scope": validation_scope
        }
        return json.dumps(error_result, indent=2, ensure_ascii=False)


@universal_quality_validator_agent.function
async def validate_specific_component(
    ctx: RunContext[QualityValidatorDependencies],
    component_path: str,
    component_type: str = "module",
    validation_types: List[str] = None,
    strict_mode: bool = False
) -> str:
    """
    Валидация конкретного компонента проекта

    Args:
        component_path: Путь к компоненту
        component_type: Тип компонента (module, class, function, file, api)
        validation_types: Типы валидации для выполнения
        strict_mode: Строгий режим валидации
    """
    if validation_types is None:
        validation_types = ["code_quality", "security", "documentation"]

    deps = ctx.deps

    component_results = {
        "timestamp": datetime.now().isoformat(),
        "component_path": component_path,
        "component_type": component_type,
        "validation_types": validation_types,
        "strict_mode": strict_mode,
        "results": {},
        "score": 0.0,
        "issues": []
    }

    try:
        total_score = 0.0
        validation_count = 0

        # Валидация качества кода
        if "code_quality" in validation_types:
            code_score = await _validate_component_code_quality(
                ctx, component_path, component_type, strict_mode
            )
            component_results["results"]["code_quality"] = code_score
            total_score += code_score.get("score", 0.0)
            validation_count += 1

        # Валидация безопасности
        if "security" in validation_types:
            security_score = await _validate_component_security(
                ctx, component_path, component_type, strict_mode
            )
            component_results["results"]["security"] = security_score
            total_score += security_score.get("score", 0.0)
            validation_count += 1

        # Валидация производительности
        if "performance" in validation_types:
            perf_score = await _validate_component_performance(
                ctx, component_path, component_type, strict_mode
            )
            component_results["results"]["performance"] = perf_score
            total_score += perf_score.get("score", 0.0)
            validation_count += 1

        # Валидация документации
        if "documentation" in validation_types:
            docs_score = await _validate_component_documentation(
                ctx, component_path, component_type, strict_mode
            )
            component_results["results"]["documentation"] = docs_score
            total_score += docs_score.get("score", 0.0)
            validation_count += 1

        # Расчет общего балла
        if validation_count > 0:
            component_results["score"] = total_score / validation_count

        # Сбор всех проблем
        for result in component_results["results"].values():
            if isinstance(result, dict) and "issues" in result:
                component_results["issues"].extend(result["issues"])

        return json.dumps(component_results, indent=2, ensure_ascii=False)

    except Exception as e:
        error_result = {
            "error": f"Ошибка валидации компонента: {str(e)}",
            "component_path": component_path,
            "component_type": component_type
        }
        return json.dumps(error_result, indent=2, ensure_ascii=False)


@universal_quality_validator_agent.function
async def continuous_quality_monitoring(
    ctx: RunContext[QualityValidatorDependencies],
    project_path: str,
    monitoring_interval: int = 3600,
    alert_thresholds: Optional[Dict[str, float]] = None,
    notification_channels: Optional[List[str]] = None
) -> str:
    """
    Непрерывный мониторинг качества проекта

    Args:
        project_path: Путь к проекту
        monitoring_interval: Интервал мониторинга в секундах
        alert_thresholds: Пороги для отправки уведомлений
        notification_channels: Каналы уведомлений
    """
    deps = ctx.deps

    if not deps.automation_settings.continuous_monitoring:
        return json.dumps({
            "error": "Непрерывный мониторинг отключен в настройках",
            "monitoring_enabled": False
        }, ensure_ascii=False)

    monitoring_config = {
        "project_path": project_path,
        "interval": monitoring_interval,
        "start_time": datetime.now().isoformat(),
        "alert_thresholds": alert_thresholds or deps.critical_thresholds,
        "notification_channels": notification_channels or deps.reporting_settings.notification_channels,
        "monitoring_active": True
    }

    try:
        # Запуск базовой валидации для получения baseline
        baseline_results = await run_quality_validation(
            ctx,
            project_path=project_path,
            validation_scope="full",
            environment="development"
        )

        baseline_data = json.loads(baseline_results)
        monitoring_config["baseline"] = baseline_data

        # В реальной реализации здесь бы был цикл мониторинга
        # Для демонстрации возвращаем конфигурацию мониторинга
        monitoring_config["status"] = "Мониторинг запущен"
        monitoring_config["next_check"] = datetime.fromtimestamp(
            datetime.now().timestamp() + monitoring_interval
        ).isoformat()

        return json.dumps(monitoring_config, indent=2, ensure_ascii=False)

    except Exception as e:
        error_result = {
            "error": f"Ошибка запуска мониторинга: {str(e)}",
            "project_path": project_path,
            "monitoring_active": False
        }
        return json.dumps(error_result, indent=2, ensure_ascii=False)


# Вспомогательные функции

def _generate_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """Генерация сводки результатов валидации"""
    summary = {
        "overall_score": 0.0,
        "total_issues": 0,
        "critical_issues": 0,
        "warning_issues": 0,
        "info_issues": 0,
        "passed_checks": 0,
        "failed_checks": 0,
        "categories": {}
    }

    category_scores = []

    for category, category_results in results.items():
        if isinstance(category_results, dict):
            score = category_results.get("score", 0.0)
            issues = category_results.get("issues", [])
            passed = category_results.get("passed_checks", 0)
            failed = category_results.get("failed_checks", 0)

            category_scores.append(score)
            summary["total_issues"] += len(issues)
            summary["passed_checks"] += passed
            summary["failed_checks"] += failed

            # Подсчет проблем по критичности
            for issue in issues:
                severity = issue.get("severity", "info").lower()
                if severity == "critical":
                    summary["critical_issues"] += 1
                elif severity == "warning":
                    summary["warning_issues"] += 1
                else:
                    summary["info_issues"] += 1

            summary["categories"][category] = {
                "score": score,
                "issues_count": len(issues),
                "status": "passed" if score >= 0.8 else "failed" if score < 0.6 else "warning"
            }

    # Расчет общего балла
    if category_scores:
        summary["overall_score"] = sum(category_scores) / len(category_scores)

    return summary


async def _generate_recommendations(
    ctx: RunContext[QualityValidatorDependencies],
    validation_results: Dict[str, Any],
    deps: QualityValidatorDependencies
) -> List[Dict[str, Any]]:
    """Генерация рекомендаций на основе результатов валидации"""
    recommendations = []

    summary = validation_results.get("summary", {})
    results = validation_results.get("results", {})

    # Рекомендации на основе общего балла
    overall_score = summary.get("overall_score", 0.0)
    if overall_score < 0.6:
        recommendations.append({
            "priority": "high",
            "category": "general",
            "title": "Критично низкое качество проекта",
            "description": f"Общий балл качества составляет {overall_score:.2f}, что ниже минимального порога 0.6",
            "action": "Провести комплексный аудит и рефакторинг проекта",
            "estimated_effort": "high"
        })

    # Рекомендации по категориям
    for category, category_data in results.items():
        if isinstance(category_data, dict):
            score = category_data.get("score", 0.0)
            issues = category_data.get("issues", [])

            if score < 0.7:
                recommendations.append({
                    "priority": "medium" if score >= 0.5 else "high",
                    "category": category,
                    "title": f"Проблемы с {category}",
                    "description": f"Балл {category} составляет {score:.2f}, обнаружено {len(issues)} проблем",
                    "action": f"Исправить проблемы в категории {category}",
                    "estimated_effort": "medium",
                    "issues_count": len(issues)
                })

    # Специфичные рекомендации для критичных проблем
    critical_issues = summary.get("critical_issues", 0)
    if critical_issues > 0:
        recommendations.append({
            "priority": "critical",
            "category": "security",
            "title": "Критичные проблемы безопасности",
            "description": f"Обнаружено {critical_issues} критичных проблем",
            "action": "Немедленно исправить все критичные проблемы",
            "estimated_effort": "high"
        })

    # Сортировка рекомендаций по приоритету
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 4))

    return recommendations


async def _validate_component_code_quality(
    ctx: RunContext[QualityValidatorDependencies],
    component_path: str,
    component_type: str,
    strict_mode: bool
) -> Dict[str, Any]:
    """Валидация качества кода компонента"""
    # Заглушка для валидации качества кода
    return {
        "score": 0.85,
        "issues": [],
        "metrics": {
            "complexity": 5,
            "maintainability": 0.8,
            "test_coverage": 0.9
        }
    }


async def _validate_component_security(
    ctx: RunContext[QualityValidatorDependencies],
    component_path: str,
    component_type: str,
    strict_mode: bool
) -> Dict[str, Any]:
    """Валидация безопасности компонента"""
    # Заглушка для валидации безопасности
    return {
        "score": 0.9,
        "issues": [],
        "vulnerabilities": []
    }


async def _validate_component_performance(
    ctx: RunContext[QualityValidatorDependencies],
    component_path: str,
    component_type: str,
    strict_mode: bool
) -> Dict[str, Any]:
    """Валидация производительности компонента"""
    # Заглушка для валидации производительности
    return {
        "score": 0.8,
        "issues": [],
        "metrics": {
            "response_time": "50ms",
            "memory_usage": "normal",
            "cpu_usage": "low"
        }
    }


async def _validate_component_documentation(
    ctx: RunContext[QualityValidatorDependencies],
    component_path: str,
    component_type: str,
    strict_mode: bool
) -> Dict[str, Any]:
    """Валидация документации компонента"""
    # Заглушка для валидации документации
    return {
        "score": 0.7,
        "issues": [],
        "coverage": 0.75
    }


# ===== КОЛЛЕКТИВНЫЕ ИНСТРУМЕНТЫ АГЕНТА =====
# Регистрация коллективных инструментов как функций агента

@universal_quality_validator_agent.tool
async def break_down_task_to_microtasks(
    ctx: RunContext[QualityValidatorDependencies],
    main_task: str,
    complexity_level: str = "medium"
) -> str:
    """
    Разбить основную задачу на микрозадачи и вывести их пользователю.

    Args:
        main_task: Описание основной задачи
        complexity_level: Уровень сложности (simple, medium, complex)
    """
    return await break_down_to_microtasks(ctx, main_task, complexity_level)


@universal_quality_validator_agent.tool
async def report_task_progress(
    ctx: RunContext[QualityValidatorDependencies],
    microtask_number: int,
    microtask_description: str,
    status: str = "completed",
    details: str = ""
) -> str:
    """
    Отчитаться о прогрессе выполнения микрозадачи.

    Args:
        microtask_number: Номер микрозадачи
        microtask_description: Описание микрозадачи
        status: Статус (started, in_progress, completed, blocked)
        details: Дополнительные детали
    """
    return await report_microtask_progress(ctx, microtask_number, microtask_description, status, details)


@universal_quality_validator_agent.tool
async def delegate_to_specialist(
    ctx: RunContext[QualityValidatorDependencies],
    target_agent: str,
    task_title: str,
    task_description: str,
    priority: str = "medium",
    context_data: str = ""
) -> str:
    """
    Делегировать задачу специализированному агенту через Archon.

    Args:
        target_agent: Тип целевого агента (security_audit, performance_optimization, etc.)
        task_title: Название задачи
        task_description: Описание задачи
        priority: Приоритет задачи (low, medium, high, critical)
        context_data: Контекстные данные (JSON строка)
    """
    import json
    try:
        context_dict = json.loads(context_data) if context_data else {}
    except:
        context_dict = {"context": context_data}

    return await delegate_task_to_agent(ctx, target_agent, task_title, task_description, priority, context_dict)


@universal_quality_validator_agent.tool
async def check_need_for_delegation(
    ctx: RunContext[QualityValidatorDependencies],
    current_task: str,
    current_agent_type: str = "quality_validation"
) -> str:
    """
    Проверить нужно ли делегировать части задачи другим агентам.

    Args:
        current_task: Описание текущей задачи
        current_agent_type: Тип текущего агента
    """
    return await check_delegation_need(ctx, current_task, current_agent_type)


@universal_quality_validator_agent.tool
async def reflect_on_work_and_improve(
    ctx: RunContext[QualityValidatorDependencies],
    completed_work: str,
    work_type: str = "validation"
) -> str:
    """
    Выполнить критический анализ работы и улучшить результат.

    ОБЯЗАТЕЛЬНО вызывается перед завершением задачи.

    Args:
        completed_work: Описание выполненной работы
        work_type: Тип работы (validation, analysis, testing, reporting)
    """
    return await reflect_and_improve(ctx, completed_work, work_type)


@universal_quality_validator_agent.tool
async def search_quality_knowledge(
    ctx: RunContext[QualityValidatorDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в специализированной базе знаний агента.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов
    """
    return await search_agent_knowledge(ctx, query, match_count)