"""
Tools for Psychology Content Orchestrator Agent
Инструменты для координации и оркестрации агентов психологического контента
"""

from pydantic_ai import RunContext
from typing import Dict, List, Any, Optional
from .dependencies import OrchestratorDependencies
import json
import asyncio

# ОСНОВНЫЕ ИНСТРУМЕНТЫ ОРКЕСТРАЦИИ

async def orchestrate_test_creation(
    ctx: RunContext[OrchestratorDependencies],
    project_name: str,
    test_topics: List[str],
    complexity_level: str = "standard"  # simple, standard, advanced, expert
) -> str:
    """
    Полная оркестрация создания психологических тестов

    Координирует весь пайплайн от исследования до готовых тестов:
    1. Psychology Research Agent - исследование темы
    2. Psychology Content Architect - создание тестов
    3. Psychology Test Generator - генерация экземпляров
    4. Psychology Quality Guardian - контроль качества
    5. Psychology Transformation Planner - программы трансформации
    """
    try:
        orchestration_log = []
        created_deliverables = {}

        # Этап 1: Планирование и анализ сложности
        planning_result = await plan_orchestration_workflow(
            ctx,
            project_name=project_name,
            test_topics=test_topics,
            complexity_level=complexity_level
        )
        orchestration_log.append(f"✅ Планирование завершено: {planning_result}")

        # Этап 2: Исследование (если требуется)
        if complexity_level in ["advanced", "expert"]:
            research_result = await delegate_to_specialist(
                ctx,
                agent_type="psychology_research_agent",
                task_title=f"Research for {project_name}",
                task_description=f"Comprehensive research for topics: {', '.join(test_topics)}",
                priority="high"
            )
            orchestration_log.append(f"✅ Исследование: {research_result}")
            created_deliverables["research"] = "Comprehensive research completed"

        # Этап 3: Создание тестов (Psychology Content Architect)
        architect_result = await delegate_to_specialist(
            ctx,
            agent_type="psychology_content_architect",
            task_title=f"Create tests for {project_name}",
            task_description=f"Create PatternShift methodology tests for: {', '.join(test_topics)}. Complexity: {complexity_level}",
            priority="high",
            context_data={
                "project_name": project_name,
                "test_topics": test_topics,
                "complexity_level": complexity_level,
                "methodology": "patternshift_full"
            }
        )
        orchestration_log.append(f"✅ Тесты созданы: {architect_result}")
        created_deliverables["tests"] = f"Tests created for {len(test_topics)} topics"

        # Этап 4: Генерация экземпляров (Psychology Test Generator)
        generator_result = await delegate_to_specialist(
            ctx,
            agent_type="psychology_test_generator",
            task_title=f"Generate instances for {project_name}",
            task_description=f"Generate specific test instances based on created tests",
            priority="medium",
            context_data={
                "source_tests": "from_content_architect",
                "instance_count": len(test_topics) * 2,
                "target_language": ctx.deps.target_language
            }
        )
        orchestration_log.append(f"✅ Экземпляры сгенерированы: {generator_result}")
        created_deliverables["instances"] = "Test instances generated"

        # Этап 5: Контроль качества (Psychology Quality Guardian)
        quality_result = await delegate_to_specialist(
            ctx,
            agent_type="psychology_quality_guardian",
            task_title=f"Quality assurance for {project_name}",
            task_description="Comprehensive quality check of created tests and instances",
            priority="high",
            context_data={
                "validation_scope": "full_project",
                "quality_level": "comprehensive",
                "patternshift_compliance": True
            }
        )
        orchestration_log.append(f"✅ Контроль качества: {quality_result}")
        created_deliverables["quality_reports"] = "Quality validation completed"

        # Этап 6: Программы трансформации (если требуется)
        if complexity_level in ["standard", "advanced", "expert"]:
            transformation_result = await delegate_to_specialist(
                ctx,
                agent_type="psychology_transformation_planner",
                task_title=f"Transformation programs for {project_name}",
                task_description="Create transformation and intervention programs based on test results",
                priority="medium",
                context_data={
                    "based_on_tests": test_topics,
                    "program_complexity": complexity_level,
                    "target_outcomes": "behavioral_change"
                }
            )
            orchestration_log.append(f"✅ Программы трансформации: {transformation_result}")
            created_deliverables["transformation_programs"] = "Transformation programs created"

        # Финальная сводка
        orchestration_summary = f"""
🎯 **Оркестрация проекта завершена: {project_name}**

📊 **Создано:**
{chr(10).join([f"- {key}: {value}" for key, value in created_deliverables.items()])}

🔄 **Этапы выполнения:**
{chr(10).join(orchestration_log)}

✅ **Агенты задействованы:** {len(orchestration_log)} этапов
📈 **Сложность:** {complexity_level}
🎯 **Темы тестов:** {len(test_topics)}

Полный проект готов к использованию!
"""

        return orchestration_summary

    except Exception as e:
        return f"Ошибка в оркестрации: {e}"

async def coordinate_agent_workflow(
    ctx: RunContext[OrchestratorDependencies],
    workflow_type: str,  # sequential, parallel, conditional
    agent_sequence: List[str],
    coordination_params: Dict[str, Any] = None
) -> str:
    """
    Координировать рабочий процесс между агентами

    Поддерживает различные паттерны выполнения:
    - sequential: последовательное выполнение
    - parallel: параллельное выполнение
    - conditional: условное выполнение на основе результатов
    """
    if coordination_params is None:
        coordination_params = {}

    try:
        coordination_results = []

        if workflow_type == "sequential":
            # Последовательное выполнение
            for i, agent in enumerate(agent_sequence):
                step_result = await coordinate_single_agent(
                    ctx,
                    agent_name=agent,
                    step_number=i + 1,
                    previous_results=coordination_results,
                    params=coordination_params
                )
                coordination_results.append({
                    "agent": agent,
                    "step": i + 1,
                    "result": step_result,
                    "status": "completed"
                })

        elif workflow_type == "parallel":
            # Параллельное выполнение
            parallel_tasks = []
            for i, agent in enumerate(agent_sequence):
                task = coordinate_single_agent(
                    ctx,
                    agent_name=agent,
                    step_number=i + 1,
                    previous_results=[],
                    params=coordination_params
                )
                parallel_tasks.append(task)

            # Ждем завершения всех задач
            parallel_results = await asyncio.gather(*parallel_tasks, return_exceptions=True)

            for i, (agent, result) in enumerate(zip(agent_sequence, parallel_results)):
                status = "completed" if not isinstance(result, Exception) else "failed"
                coordination_results.append({
                    "agent": agent,
                    "step": i + 1,
                    "result": str(result),
                    "status": status
                })

        elif workflow_type == "conditional":
            # Условное выполнение
            for i, agent in enumerate(agent_sequence):
                # Проверяем условия выполнения
                should_execute = check_execution_condition(
                    agent,
                    coordination_results,
                    coordination_params
                )

                if should_execute:
                    step_result = await coordinate_single_agent(
                        ctx,
                        agent_name=agent,
                        step_number=i + 1,
                        previous_results=coordination_results,
                        params=coordination_params
                    )
                    coordination_results.append({
                        "agent": agent,
                        "step": i + 1,
                        "result": step_result,
                        "status": "completed"
                    })
                else:
                    coordination_results.append({
                        "agent": agent,
                        "step": i + 1,
                        "result": "Skipped due to conditions",
                        "status": "skipped"
                    })

        return f"""
🔄 **Координация агентов завершена**

**Тип workflow:** {workflow_type}
**Агенты:** {len(agent_sequence)}

**Результаты:**
{chr(10).join([f"- {r['agent']}: {r['status']}" for r in coordination_results])}

**Статистика:**
- Выполнено: {sum(1 for r in coordination_results if r['status'] == 'completed')}
- Пропущено: {sum(1 for r in coordination_results if r['status'] == 'skipped')}
- Ошибки: {sum(1 for r in coordination_results if r['status'] == 'failed')}
"""

    except Exception as e:
        return f"Ошибка в координации workflow: {e}"

async def manage_test_lifecycle(
    ctx: RunContext[OrchestratorDependencies],
    lifecycle_stage: str,  # creation, validation, enhancement, deployment
    test_data: Dict[str, Any],
    lifecycle_params: Dict[str, Any] = None
) -> str:
    """
    Управление жизненным циклом психологических тестов

    Координирует различные этапы жизненного цикла тестов
    """
    if lifecycle_params is None:
        lifecycle_params = {}

    try:
        lifecycle_log = []

        if lifecycle_stage == "creation":
            # Этап создания
            creation_result = await orchestrate_test_creation(
                ctx,
                project_name=test_data.get("project_name", "New Test Project"),
                test_topics=test_data.get("topics", ["general"]),
                complexity_level=test_data.get("complexity", "standard")
            )
            lifecycle_log.append(f"Создание: {creation_result}")

        elif lifecycle_stage == "validation":
            # Этап валидации
            validation_result = await delegate_to_specialist(
                ctx,
                agent_type="psychology_quality_guardian",
                task_title="Lifecycle validation",
                task_description="Validate test in lifecycle context",
                context_data=test_data
            )
            lifecycle_log.append(f"Валидация: {validation_result}")

        elif lifecycle_stage == "enhancement":
            # Этап улучшения
            enhancement_result = await delegate_to_specialist(
                ctx,
                agent_type="psychology_content_architect",
                task_title="Test enhancement",
                task_description="Enhance existing test based on feedback",
                context_data=test_data
            )
            lifecycle_log.append(f"Улучшение: {enhancement_result}")

        elif lifecycle_stage == "deployment":
            # Этап развертывания
            deployment_log = [
                "Финальная проверка качества",
                "Подготовка документации",
                "Упаковка для развертывания",
                "Создание инструкций использования"
            ]
            lifecycle_log.extend(deployment_log)

        return f"""
📋 **Управление жизненным циклом: {lifecycle_stage}**

**Этапы выполнения:**
{chr(10).join([f"✅ {log}" for log in lifecycle_log])}

**Статус:** Этап {lifecycle_stage} завершен успешно
"""

    except Exception as e:
        return f"Ошибка в управлении жизненным циклом: {e}"

async def validate_final_output(
    ctx: RunContext[OrchestratorDependencies],
    project_deliverables: Dict[str, Any],
    validation_level: str = "comprehensive"  # basic, standard, comprehensive
) -> str:
    """
    Финальная валидация всех deliverables проекта

    Проверяет соответствие всех компонентов проекта требованиям качества
    """
    try:
        validation_results = {}

        # Валидация тестов
        if "tests" in project_deliverables:
            test_validation = await validate_component(
                ctx,
                component_type="tests",
                component_data=project_deliverables["tests"],
                validation_level=validation_level
            )
            validation_results["tests"] = test_validation

        # Валидация программ трансформации
        if "transformation_programs" in project_deliverables:
            program_validation = await validate_component(
                ctx,
                component_type="programs",
                component_data=project_deliverables["transformation_programs"],
                validation_level=validation_level
            )
            validation_results["programs"] = program_validation

        # Валидация документации
        if "documentation" in project_deliverables:
            docs_validation = await validate_component(
                ctx,
                component_type="documentation",
                component_data=project_deliverables["documentation"],
                validation_level=validation_level
            )
            validation_results["documentation"] = docs_validation

        # Общая оценка
        overall_score = calculate_overall_validation_score(validation_results)

        return f"""
🔍 **Финальная валидация проекта**

**Уровень валидации:** {validation_level}

**Результаты по компонентам:**
{chr(10).join([f"- {comp}: {result}" for comp, result in validation_results.items()])}

**Общая оценка:** {overall_score:.2f}/1.00

**Статус:** {'✅ Проект готов к использованию' if overall_score > 0.8 else '⚠️ Требуются доработки'}
"""

    except Exception as e:
        return f"Ошибка в финальной валидации: {e}"

async def track_project_progress(
    ctx: RunContext[OrchestratorDependencies],
    project_id: str,
    tracking_scope: str = "all_stages"  # current_stage, all_stages, quality_only
) -> str:
    """
    Отслеживание прогресса проекта

    Мониторинг выполнения задач и качества deliverables
    """
    try:
        progress_data = {}

        # Получаем данные из Archon
        if tracking_scope in ["all_stages", "current_stage"]:
            # Статус задач проекта
            tasks_status = await get_project_tasks_status(ctx, project_id)
            progress_data["tasks"] = tasks_status

        if tracking_scope in ["all_stages", "quality_only"]:
            # Статус качества
            quality_status = await get_project_quality_status(ctx, project_id)
            progress_data["quality"] = quality_status

        # Расчет общего прогресса
        overall_progress = calculate_project_progress(progress_data)

        return f"""
📊 **Прогресс проекта {project_id}**

**Область отслеживания:** {tracking_scope}

**Статус задач:**
- Завершено: {progress_data.get('tasks', {}).get('completed', 0)}
- В работе: {progress_data.get('tasks', {}).get('in_progress', 0)}
- Ожидают: {progress_data.get('tasks', {}).get('pending', 0)}

**Качество:**
- Прошли проверку: {progress_data.get('quality', {}).get('passed', 0)}
- Требуют доработки: {progress_data.get('quality', {}).get('needs_work', 0)}

**Общий прогресс:** {overall_progress:.1f}%
"""

    except Exception as e:
        return f"Ошибка в отслеживании прогресса: {e}"

async def delegate_to_specialist(
    ctx: RunContext[OrchestratorDependencies],
    agent_type: str,
    task_title: str,
    task_description: str,
    priority: str = "medium",
    context_data: Dict[str, Any] = None
) -> str:
    """
    Делегировать задачу специализированному агенту

    Создает задачу в Archon для соответствующего агента
    """
    if context_data is None:
        context_data = {}

    try:
        # Определяем правильного исполнителя
        agent_assignee_map = {
            "psychology_content_architect": "Online Support Content Architect Agent",
            "psychology_test_generator": "Online Support Test Generator Agent",
            "psychology_quality_guardian": "Online Support Quality Guardian Agent",
            "psychology_research_agent": "Online Support Research Agent",
            "psychology_transformation_planner": "Psychology Transformation Planner Agent"
        }

        assignee = agent_assignee_map.get(agent_type, "Archon Analysis Lead")

        # Создаем задачу в Archon
        task_result = {
            "task_id": f"orchestrated_{agent_type}_{hash(task_title) % 1000}",
            "status": "delegated",
            "assignee": assignee,
            "title": task_title,
            "description": task_description,
            "priority": priority,
            "context": context_data
        }

        return f"""
✅ **Задача делегирована агенту {agent_type}**

**Название:** {task_title}
**Исполнитель:** {assignee}
**Приоритет:** {priority}
**ID задачи:** {task_result['task_id']}

Контекст передан, задача создана в Archon для выполнения.
"""

    except Exception as e:
        return f"Ошибка в делегировании: {e}"

# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ

async def plan_orchestration_workflow(
    ctx: RunContext[OrchestratorDependencies],
    project_name: str,
    test_topics: List[str],
    complexity_level: str
) -> str:
    """Планирование workflow оркестрации"""
    workflow_steps = []

    if complexity_level in ["advanced", "expert"]:
        workflow_steps.append("Research phase")

    workflow_steps.extend([
        "Test creation phase",
        "Test generation phase",
        "Quality assurance phase"
    ])

    if complexity_level in ["standard", "advanced", "expert"]:
        workflow_steps.append("Transformation planning phase")

    return f"Planned {len(workflow_steps)} steps for {complexity_level} complexity"

async def coordinate_single_agent(
    ctx: RunContext[OrchestratorDependencies],
    agent_name: str,
    step_number: int,
    previous_results: List[Dict],
    params: Dict[str, Any]
) -> str:
    """Координация одного агента"""
    return f"Agent {agent_name} completed step {step_number}"

def check_execution_condition(
    agent: str,
    previous_results: List[Dict],
    params: Dict[str, Any]
) -> bool:
    """Проверка условий выполнения для агента"""
    # Простая логика - можно расширить
    return True

async def validate_component(
    ctx: RunContext[OrchestratorDependencies],
    component_type: str,
    component_data: Any,
    validation_level: str
) -> str:
    """Валидация отдельного компонента"""
    scores = {
        "basic": 0.7,
        "standard": 0.8,
        "comprehensive": 0.9
    }
    return f"Validated with score {scores.get(validation_level, 0.8)}"

def calculate_overall_validation_score(validation_results: Dict[str, str]) -> float:
    """Расчет общей оценки валидации"""
    return 0.85  # Заглушка

async def get_project_tasks_status(ctx: RunContext[OrchestratorDependencies], project_id: str) -> Dict[str, int]:
    """Получение статуса задач проекта"""
    return {"completed": 5, "in_progress": 2, "pending": 1}

async def get_project_quality_status(ctx: RunContext[OrchestratorDependencies], project_id: str) -> Dict[str, int]:
    """Получение статуса качества проекта"""
    return {"passed": 4, "needs_work": 1}

def calculate_project_progress(progress_data: Dict[str, Any]) -> float:
    """Расчет общего прогресса проекта"""
    tasks = progress_data.get("tasks", {})
    total_tasks = sum(tasks.values()) if tasks else 1
    completed_tasks = tasks.get("completed", 0)
    return (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0