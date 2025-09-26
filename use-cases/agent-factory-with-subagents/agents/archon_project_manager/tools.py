#!/usr/bin/env python3
"""
Инструменты для Archon Project Manager Agent.

Набор специализированных инструментов для управления проектами и координации команды.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import ProjectManagerDependencies, ProjectPhase, TaskPriority


class ProjectPlan(BaseModel):
    """Модель плана проекта."""
    project_name: str = Field(description="Название проекта")
    phases: List[Dict[str, Any]] = Field(description="Фазы проекта")
    milestones: List[Dict[str, Any]] = Field(description="Ключевые вехи")
    team_allocation: Dict[str, Any] = Field(description="Распределение команды")
    timeline: Dict[str, Any] = Field(description="Временные рамки")
    risks: List[str] = Field(description="Идентифицированные риски")
    dependencies: List[Dict[str, str]] = Field(description="Зависимости между задачами")


class TaskSchedule(BaseModel):
    """Модель расписания задач."""
    tasks: List[Dict[str, Any]] = Field(description="Список задач")
    assignments: Dict[str, str] = Field(description="Назначения исполнителей")
    timeline: Dict[str, str] = Field(description="Временные рамки задач")
    dependencies: List[Dict[str, str]] = Field(description="Зависимости между задачами")
    conflicts: List[str] = Field(description="Обнаруженные конфликты")


class StatusReport(BaseModel):
    """Модель отчета о статусе."""
    project_name: str = Field(description="Название проекта")
    current_phase: str = Field(description="Текущая фаза")
    overall_progress: float = Field(description="Общий прогресс (0-100)")
    completed_tasks: int = Field(description="Выполненные задачи")
    total_tasks: int = Field(description="Общее количество задач")
    team_status: Dict[str, Any] = Field(description="Статус команды")
    risks: List[Dict[str, str]] = Field(description="Текущие риски")
    blockers: List[str] = Field(description="Блокеры")
    next_steps: List[str] = Field(description="Следующие шаги")
    recommendations: List[str] = Field(description="Рекомендации")


class RiskAssessment(BaseModel):
    """Модель оценки рисков."""
    identified_risks: List[Dict[str, Any]] = Field(description="Идентифицированные риски")
    risk_matrix: Dict[str, Any] = Field(description="Матрица рисков")
    mitigation_plans: List[Dict[str, str]] = Field(description="Планы митигации")
    monitoring_schedule: Dict[str, str] = Field(description="График мониторинга")


async def create_project_plan(
    ctx: RunContext[ProjectManagerDependencies],
    project_description: str,
    requirements: List[str],
    timeline_weeks: int = 8
) -> ProjectPlan:
    """
    Создать план проекта на основе описания и требований.

    Args:
        ctx: Контекст выполнения с зависимостями
        project_description: Описание проекта
        requirements: Список требований
        timeline_weeks: Временные рамки в неделях

    Returns:
        План проекта с фазами, вехами и распределением ресурсов
    """
    deps = ctx.deps
    management_config = deps.get_management_config()
    team_strategy = deps.get_team_allocation_strategy()

    # Определяем фазы проекта
    phases = _generate_project_phases(project_description, requirements, management_config)

    # Создаем ключевые вехи
    milestones = _generate_project_milestones(phases, deps)

    # Распределяем команду
    team_allocation = _allocate_team_resources(requirements, deps)

    # Создаем временные рамки
    timeline = _create_project_timeline(phases, timeline_weeks, deps)

    # Идентифицируем риски
    risks = _identify_project_risks(project_description, requirements, deps)

    # Определяем зависимости
    dependencies = _identify_task_dependencies(phases)

    return ProjectPlan(
        project_name=_extract_project_name(project_description),
        phases=phases,
        milestones=milestones,
        team_allocation=team_allocation,
        timeline=timeline,
        risks=risks,
        dependencies=dependencies
    )


async def manage_task_priorities(
    ctx: RunContext[ProjectManagerDependencies],
    tasks: List[Dict[str, Any]],
    constraints: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Управлять приоритетами задач с учетом ограничений.

    Args:
        ctx: Контекст выполнения с зависимостями
        tasks: Список задач для приоритизации
        constraints: Ограничения (дедлайны, ресурсы, зависимости)

    Returns:
        Результат приоритизации с обновленными задачами
    """
    deps = ctx.deps
    priority_matrix = deps.get_priority_matrix()

    # Анализируем задачи и их характеристики
    prioritized_tasks = []
    
    for task in tasks:
        priority_score = _calculate_priority_score(
            task,
            constraints or {},
            priority_matrix
        )
        
        task_copy = task.copy()
        task_copy['priority_score'] = priority_score
        task_copy['recommended_priority'] = _map_score_to_priority(priority_score)
        
        prioritized_tasks.append(task_copy)

    # Сортируем по приоритету
    prioritized_tasks.sort(key=lambda x: x['priority_score'], reverse=True)

    # Проверяем ресурсные ограничения
    resource_conflicts = _check_resource_conflicts(prioritized_tasks, deps)

    # Рекомендации по балансировке нагрузки
    balancing_recommendations = _generate_balancing_recommendations(
        prioritized_tasks, deps
    )

    return {
        'prioritized_tasks': prioritized_tasks,
        'priority_changes': _track_priority_changes(tasks, prioritized_tasks),
        'resource_conflicts': resource_conflicts,
        'recommendations': balancing_recommendations,
        'next_review_date': (datetime.now() + timedelta(days=7)).isoformat()
    }


async def coordinate_team_work(
    ctx: RunContext[ProjectManagerDependencies],
    current_tasks: List[Dict[str, Any]],
    team_status: Dict[str, str]
) -> Dict[str, Any]:
    """
    Координировать работу команды и распределение задач.

    Args:
        ctx: Контекст выполнения с зависимостями
        current_tasks: Текущие задачи
        team_status: Статус членов команды

    Returns:
        Результат координации с назначениями и рекомендациями
    """
    deps = ctx.deps
    communication_config = deps.get_communication_config()

    # Анализируем загрузку команды
    workload_analysis = _analyze_team_workload(current_tasks, team_status)

    # Предлагаем перераспределение задач
    rebalancing_suggestions = _suggest_task_rebalancing(
        current_tasks, workload_analysis, deps
    )

    # Определяем потребности в коммуникации
    communication_needs = _identify_communication_needs(
        current_tasks, team_status, deps
    )

    # Планируем встречи и синхронизации
    meeting_schedule = _plan_team_meetings(communication_config)

    # Выявляем блокеры и зависимости
    blockers = _identify_blockers(current_tasks, team_status)

    return {
        'workload_analysis': workload_analysis,
        'rebalancing_suggestions': rebalancing_suggestions,
        'communication_plan': communication_needs,
        'meeting_schedule': meeting_schedule,
        'blockers': blockers,
        'coordination_actions': _generate_coordination_actions(current_tasks, deps)
    }


async def generate_status_report(
    ctx: RunContext[ProjectManagerDependencies],
    project_data: Dict[str, Any]
) -> StatusReport:
    """
    Генерировать отчет о статусе проекта.

    Args:
        ctx: Контекст выполнения с зависимостями
        project_data: Данные о проекте

    Returns:
        Подробный отчет о статусе проекта
    """
    deps = ctx.deps
    reporting_config = deps.get_reporting_config()

    # Рассчитываем общий прогресс
    overall_progress = _calculate_overall_progress(project_data)

    # Анализируем статус команды
    team_status = _analyze_team_performance(project_data, deps)

    # Выявляем текущие риски
    current_risks = _assess_current_risks(project_data, deps)

    # Идентифицируем блокеры
    blockers = _identify_current_blockers(project_data)

    # Планируем следующие шаги
    next_steps = _plan_next_steps(project_data, deps)

    # Генерируем рекомендации
    recommendations = _generate_management_recommendations(project_data, deps)

    return StatusReport(
        project_name=project_data.get('name', 'Unnamed Project'),
        current_phase=project_data.get('current_phase', 'unknown'),
        overall_progress=overall_progress,
        completed_tasks=project_data.get('completed_tasks', 0),
        total_tasks=project_data.get('total_tasks', 0),
        team_status=team_status,
        risks=current_risks,
        blockers=blockers,
        next_steps=next_steps,
        recommendations=recommendations
    )


async def manage_project_risks(
    ctx: RunContext[ProjectManagerDependencies],
    project_context: Dict[str, Any]
) -> RiskAssessment:
    """
    Управлять рисками проекта.

    Args:
        ctx: Контекст выполнения с зависимостями
        project_context: Контекст проекта

    Returns:
        Оценка рисков с планами митигации
    """
    deps = ctx.deps
    risk_config = deps.get_risk_management_config()

    if not risk_config.get('enabled', False):
        return RiskAssessment(
            identified_risks=[],
            risk_matrix={},
            mitigation_plans=[],
            monitoring_schedule={}
        )

    # Идентифицируем риски
    identified_risks = _identify_all_risks(project_context, risk_config)

    # Создаем матрицу рисков
    risk_matrix = _create_risk_matrix(identified_risks)

    # Разрабатываем планы митигации
    mitigation_plans = _create_mitigation_plans(identified_risks, deps)

    # Создаем график мониторинга
    monitoring_schedule = _create_risk_monitoring_schedule(identified_risks, risk_config)

    return RiskAssessment(
        identified_risks=identified_risks,
        risk_matrix=risk_matrix,
        mitigation_plans=mitigation_plans,
        monitoring_schedule=monitoring_schedule
    )


async def schedule_tasks(
    ctx: RunContext[ProjectManagerDependencies],
    tasks: List[Dict[str, Any]],
    constraints: Dict[str, Any]
) -> TaskSchedule:
    """
    Планировать выполнение задач с учетом ограничений.

    Args:
        ctx: Контекст выполнения с зависимостями
        tasks: Список задач для планирования
        constraints: Ограничения планирования

    Returns:
        Расписание задач с назначениями
    """
    deps = ctx.deps
    scheduling_rules = deps.get_scheduling_rules()

    # Анализируем зависимости между задачами
    dependencies = _analyze_task_dependencies(tasks)

    # Создаем оптимальное расписание
    optimized_schedule = _optimize_task_schedule(
        tasks, dependencies, constraints, scheduling_rules
    )

    # Назначаем исполнителей
    assignments = _assign_tasks_to_team(
        optimized_schedule, deps.available_roles, deps
    )

    # Проверяем конфликты
    conflicts = _detect_scheduling_conflicts(optimized_schedule, assignments)

    # Создаем временные рамки
    timeline = _create_task_timeline(optimized_schedule, deps)

    return TaskSchedule(
        tasks=optimized_schedule,
        assignments=assignments,
        timeline=timeline,
        dependencies=dependencies,
        conflicts=conflicts
    )


async def track_progress(
    ctx: RunContext[ProjectManagerDependencies],
    project_id: str
) -> Dict[str, Any]:
    """
    Отслеживать прогресс выполнения проекта.

    Args:
        ctx: Контекст выполнения с зависимостями
        project_id: Идентификатор проекта

    Returns:
        Данные о прогрессе проекта
    """
    deps = ctx.deps
    
    # Симуляция получения данных из Archon
    project_data = {
        'completed_tasks': 15,
        'total_tasks': 25,
        'current_velocity': 3.2,
        'planned_velocity': 3.0,
        'team_utilization': 85.0
    }

    # Рассчитываем метрики прогресса
    progress_metrics = _calculate_progress_metrics(project_data)

    # Анализируем тренды
    trends = _analyze_progress_trends(project_data)

    # Прогнозируем завершение
    completion_forecast = _forecast_project_completion(project_data, deps)

    # Генерируем рекомендации
    progress_recommendations = _generate_progress_recommendations(
        progress_metrics, trends, deps
    )

    return {
        'project_id': project_id,
        'progress_metrics': progress_metrics,
        'trends': trends,
        'completion_forecast': completion_forecast,
        'recommendations': progress_recommendations,
        'last_updated': datetime.now().isoformat()
    }


async def search_management_knowledge(
    ctx: RunContext[ProjectManagerDependencies],
    query: str,
    knowledge_type: str = "management"
) -> Dict[str, Any]:
    """
    Поиск знаний по управлению проектами в базе знаний.

    Args:
        ctx: Контекст выполнения с зависимостями
        query: Поисковый запрос
        knowledge_type: Тип знаний (management, coordination, planning)

    Returns:
        Результаты поиска знаний по управлению
    """
    deps = ctx.deps

    # Формируем расширенный запрос с тегами знаний
    enhanced_query = f"{query} {' '.join(deps.knowledge_tags)}"

    # Симуляция поиска в базе знаний
    search_results = {
        'query': query,
        'knowledge_type': knowledge_type,
        'results': [
            {
                'title': f"Методологии управления для {query}",
                'content': f"Рекомендации по управлению проектами в контексте {query}",
                'relevance': 0.92,
                'source': 'management_knowledge_base',
                'methodologies': _get_relevant_methodologies(query, deps)
            }
        ],
        'total_results': 1,
        'search_time_ms': 100
    }

    return search_results


async def delegate_task(
    ctx: RunContext[ProjectManagerDependencies],
    task_description: str,
    task_type: str,
    complexity: str = "medium",
    deadline: Optional[str] = None
) -> Dict[str, Any]:
    """
    Делегировать задачу соответствующему члену команды.

    Args:
        ctx: Контекст выполнения с зависимостями
        task_description: Описание задачи
        task_type: Тип задачи
        complexity: Сложность задачи
        deadline: Срок выполнения

    Returns:
        Результат делегирования
    """
    deps = ctx.deps

    # Определяем наиболее подходящего исполнителя
    assigned_role = deps.should_delegate_task(task_type, complexity)

    if not assigned_role:
        return {
            'delegated': False,
            'reason': 'Задача выполняется Project Manager',
            'self_execution': True
        }

    # Подготавливаем контекст делегирования
    delegation_context = {
        'task_type': task_type,
        'description': task_description,
        'complexity': complexity,
        'deadline': deadline,
        'project_context': {
            'phase': deps.current_phase.value,
            'management_style': deps.management_style.value,
            'quality_requirements': deps.get_quality_requirements()
        }
    }

    return {
        'delegated': True,
        'assigned_to': assigned_role,
        'task_context': delegation_context,
        'expected_deliverables': _define_expected_deliverables(task_type),
        'coordination_plan': _create_coordination_plan(assigned_role, deps)
    }


# Вспомогательные функции

def _generate_project_phases(description: str, requirements: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Генерировать фазы проекта."""
    if config['style'] == 'agile':
        return [
            {'name': 'Inception', 'duration_weeks': 1, 'activities': ['Vision', 'Team setup']},
            {'name': 'Elaboration', 'duration_weeks': 2, 'activities': ['Architecture', 'Risk analysis']},
            {'name': 'Construction', 'duration_weeks': 4, 'activities': ['Implementation', 'Testing']},
            {'name': 'Transition', 'duration_weeks': 1, 'activities': ['Deployment', 'Training']}
        ]
    else:
        return [
            {'name': 'Planning', 'duration_weeks': 2, 'activities': ['Requirements', 'Planning']},
            {'name': 'Design', 'duration_weeks': 2, 'activities': ['Architecture', 'Design']},
            {'name': 'Implementation', 'duration_weeks': 3, 'activities': ['Coding', 'Integration']},
            {'name': 'Testing', 'duration_weeks': 1, 'activities': ['Testing', 'QA']}
        ]

def _generate_project_milestones(phases: List[Dict[str, Any]], deps) -> List[Dict[str, Any]]:
    """Генерировать ключевые вехи."""
    milestones = []
    for phase in phases:
        milestones.append({
            'name': f"{phase['name']} Complete",
            'phase': phase['name'],
            'deliverables': phase.get('activities', []),
            'criteria': f"All {phase['name'].lower()} activities completed"
        })
    return milestones

def _allocate_team_resources(requirements: List[str], deps) -> Dict[str, Any]:
    """Распределить ресурсы команды."""
    return {
        'team_size': deps.team_size,
        'roles': deps.available_roles,
        'allocation_strategy': deps.get_team_allocation_strategy()['approach'],
        'specializations': {
            'Analysis Lead': 'Requirements analysis, research',
            'Blueprint Architect': 'System design, architecture',
            'Implementation Engineer': 'Coding, implementation',
            'Quality Guardian': 'Testing, quality assurance'
        }
    }

def _create_project_timeline(phases: List[Dict[str, Any]], total_weeks: int, deps) -> Dict[str, Any]:
    """Создать временные рамки проекта."""
    start_date = datetime.now()
    end_date = start_date + timedelta(weeks=total_weeks)
    
    return {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'total_weeks': total_weeks,
        'phases_timeline': [
            {
                'phase': phase['name'],
                'start_week': sum(p['duration_weeks'] for p in phases[:i]),
                'duration_weeks': phase['duration_weeks']
            }
            for i, phase in enumerate(phases)
        ]
    }

def _identify_project_risks(description: str, requirements: List[str], deps) -> List[str]:
    """Идентифицировать риски проекта."""
    common_risks = [
        "Неточные требования",
        "Технические сложности",
        "Ресурсные ограничения",
        "Изменение приоритетов"
    ]
    
    # Добавляем специфичные риски на основе требований
    if any('интеграция' in req.lower() for req in requirements):
        common_risks.append("Сложности интеграции")
    if any('производительность' in req.lower() for req in requirements):
        common_risks.append("Проблемы производительности")
        
    return common_risks

def _identify_task_dependencies(phases: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Идентифицировать зависимости между задачами."""
    dependencies = []
    for i in range(len(phases) - 1):
        dependencies.append({
            'from': phases[i]['name'],
            'to': phases[i + 1]['name'],
            'type': 'finish_to_start'
        })
    return dependencies

def _extract_project_name(description: str) -> str:
    """Извлечь название проекта из описания."""
    words = description.split()[:3]
    return ' '.join(words).title()

def _calculate_priority_score(task: Dict[str, Any], constraints: Dict[str, Any], matrix: Dict[str, int]) -> float:
    """Рассчитать балл приоритета задачи."""
    base_score = matrix.get(task.get('priority', 'medium'), 3)
    
    # Учитываем дедлайны
    if 'deadline' in task:
        days_until_deadline = (datetime.fromisoformat(task['deadline']) - datetime.now()).days
        if days_until_deadline < 7:
            base_score *= 1.5
    
    # Учитываем зависимости
    if task.get('blocks_other_tasks', False):
        base_score *= 1.3
        
    return base_score

def _map_score_to_priority(score: float) -> str:
    """Сопоставить балл с приоритетом."""
    if score >= 4.0:
        return 'critical'
    elif score >= 3.0:
        return 'high'
    elif score >= 2.0:
        return 'medium'
    else:
        return 'low'

def _track_priority_changes(original: List[Dict[str, Any]], updated: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Отследить изменения приоритетов."""
    changes = []
    original_dict = {task.get('id', i): task for i, task in enumerate(original)}
    
    for updated_task in updated:
        task_id = updated_task.get('id', 0)
        if task_id in original_dict:
            old_priority = original_dict[task_id].get('priority', 'medium')
            new_priority = updated_task.get('recommended_priority', 'medium')
            if old_priority != new_priority:
                changes.append({
                    'task_id': str(task_id),
                    'old_priority': old_priority,
                    'new_priority': new_priority,
                    'reason': 'Automated prioritization'
                })
    
    return changes

def _check_resource_conflicts(tasks: List[Dict[str, Any]], deps) -> List[str]:
    """Проверить конфликты ресурсов."""
    conflicts = []
    
    # Проверяем превышение максимального количества параллельных задач
    high_priority_tasks = [t for t in tasks if t.get('recommended_priority') in ['critical', 'high']]
    if len(high_priority_tasks) > deps.max_parallel_tasks:
        conflicts.append(f"Слишком много высокоприоритетных задач: {len(high_priority_tasks)} > {deps.max_parallel_tasks}")
    
    return conflicts

def _generate_balancing_recommendations(tasks: List[Dict[str, Any]], deps) -> List[str]:
    """Генерировать рекомендации по балансировке."""
    recommendations = []
    
    critical_tasks = [t for t in tasks if t.get('recommended_priority') == 'critical']
    if len(critical_tasks) > 3:
        recommendations.append("Рассмотрите возможность снижения критичности некоторых задач")
    
    return recommendations

def _analyze_team_workload(tasks: List[Dict[str, Any]], team_status: Dict[str, str]) -> Dict[str, Any]:
    """Анализировать загрузку команды."""
    return {
        'total_active_tasks': len([t for t in tasks if t.get('status') == 'in_progress']),
        'team_utilization': 75.0,
        'overloaded_members': [],
        'available_capacity': 25.0
    }

def _suggest_task_rebalancing(tasks: List[Dict[str, Any]], workload: Dict[str, Any], deps) -> List[str]:
    """Предложить перераспределение задач."""
    return [
        "Перераспределить задачи между Analysis Lead и Implementation Engineer",
        "Привлечь Quality Guardian к раннему тестированию"
    ]

def _identify_communication_needs(tasks: List[Dict[str, Any]], team_status: Dict[str, str], deps) -> List[str]:
    """Идентифицировать потребности в коммуникации."""
    return [
        "Синхронизация между Blueprint Architect и Implementation Engineer",
        "Еженедельный статус-колл с командой"
    ]

def _plan_team_meetings(config: Dict[str, Any]) -> Dict[str, str]:
    """Планировать встречи команды."""
    meetings = {}
    
    if config.get('daily_standup'):
        meetings['daily_standup'] = 'Ежедневно в 10:00'
    if config.get('weekly_reports'):
        meetings['weekly_status'] = 'Пятница в 15:00'
        
    return meetings

def _identify_blockers(tasks: List[Dict[str, Any]], team_status: Dict[str, str]) -> List[str]:
    """Идентифицировать блокеры."""
    return [
        "Ожидание внешней зависимости",
        "Требуется согласование архитектуры"
    ]

def _generate_coordination_actions(tasks: List[Dict[str, Any]], deps) -> List[str]:
    """Генерировать действия по координации."""
    return [
        "Создать задачу для Analysis Lead по детализации требований",
        "Назначить встречу Blueprint Architect и Implementation Engineer"
    ]

def _calculate_overall_progress(project_data: Dict[str, Any]) -> float:
    """Рассчитать общий прогресс проекта."""
    completed = project_data.get('completed_tasks', 0)
    total = project_data.get('total_tasks', 1)
    return (completed / total) * 100 if total > 0 else 0.0

def _analyze_team_performance(project_data: Dict[str, Any], deps) -> Dict[str, Any]:
    """Анализировать производительность команды."""
    return {
        'velocity': project_data.get('current_velocity', 0.0),
        'utilization': project_data.get('team_utilization', 0.0),
        'satisfaction': 85.0,
        'collaboration_score': 90.0
    }

def _assess_current_risks(project_data: Dict[str, Any], deps) -> List[Dict[str, str]]:
    """Оценить текущие риски."""
    return [
        {
            'risk': 'Задержка интеграции',
            'probability': 'medium',
            'impact': 'high',
            'status': 'monitoring'
        }
    ]

def _identify_current_blockers(project_data: Dict[str, Any]) -> List[str]:
    """Идентифицировать текущие блокеры."""
    return [
        "Ожидание code review от Quality Guardian",
        "Необходимо согласование API с внешней системой"
    ]

def _plan_next_steps(project_data: Dict[str, Any], deps) -> List[str]:
    """Планировать следующие шаги."""
    return [
        "Завершить текущий спринт к пятнице",
        "Начать планирование следующей итерации",
        "Провести ретроспективу команды"
    ]

def _generate_management_recommendations(project_data: Dict[str, Any], deps) -> List[str]:
    """Генерировать рекомендации по управлению."""
    return [
        "Увеличить частоту синхронизации между архитектором и разработчиками",
        "Рассмотреть возможность параллельного выполнения некоторых задач",
        "Усилить фокус на автоматизированном тестировании"
    ]

def _identify_all_risks(context: Dict[str, Any], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Идентифицировать все риски проекта."""
    return [
        {
            'name': 'Технический риск',
            'category': 'technical_risk',
            'probability': 'medium',
            'impact': 'high',
            'description': 'Сложности с интеграцией компонентов'
        },
        {
            'name': 'Ресурсный риск',
            'category': 'resource_risk',
            'probability': 'low',
            'impact': 'medium',
            'description': 'Недостаток экспертизы в конкретной области'
        }
    ]

def _create_risk_matrix(risks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Создать матрицу рисков."""
    return {
        'high_probability_high_impact': 1,
        'medium_probability_high_impact': 1,
        'low_probability_medium_impact': 1,
        'total_risks': len(risks)
    }

def _create_mitigation_plans(risks: List[Dict[str, Any]], deps) -> List[Dict[str, str]]:
    """Создать планы митигации рисков."""
    plans = []
    for risk in risks:
        plans.append({
            'risk_name': risk['name'],
            'mitigation_strategy': f"Митигация для {risk['name']}",
            'responsible': 'Project Manager',
            'timeline': '2 weeks'
        })
    return plans

def _create_risk_monitoring_schedule(risks: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, str]:
    """Создать график мониторинга рисков."""
    return {
        'review_frequency': config.get('risk_assessment_frequency', 'weekly'),
        'next_review': (datetime.now() + timedelta(days=7)).isoformat(),
        'escalation_criteria': 'Увеличение вероятности или воздействия'
    }

def _analyze_task_dependencies(tasks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Анализировать зависимости задач."""
    return [
        {
            'from_task': 'Architecture Design',
            'to_task': 'Implementation',
            'dependency_type': 'finish_to_start'
        }
    ]

def _optimize_task_schedule(tasks: List[Dict[str, Any]], dependencies: List[Dict[str, str]], constraints: Dict[str, Any], rules: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Оптимизировать расписание задач."""
    # Простая оптимизация - сортируем по приоритету и зависимостям
    optimized = sorted(tasks, key=lambda x: x.get('priority_score', 0), reverse=True)
    
    for i, task in enumerate(optimized):
        task['scheduled_order'] = i + 1
        task['estimated_start'] = (datetime.now() + timedelta(days=i*2)).isoformat()
        
    return optimized

def _assign_tasks_to_team(tasks: List[Dict[str, Any]], roles: List[str], deps) -> Dict[str, str]:
    """Назначить задачи членам команды."""
    assignments = {}
    role_cycle = 0
    
    for task in tasks:
        task_type = task.get('type', 'general')
        assigned_role = deps.should_delegate_task(task_type, task.get('complexity', 'medium'))
        
        if not assigned_role:
            assigned_role = roles[role_cycle % len(roles)]
            role_cycle += 1
            
        assignments[task.get('id', f"task_{len(assignments)}")] = assigned_role
        
    return assignments

def _detect_scheduling_conflicts(tasks: List[Dict[str, Any]], assignments: Dict[str, str]) -> List[str]:
    """Обнаружить конфликты планирования."""
    conflicts = []
    
    # Проверяем перегрузку ролей
    role_counts = {}
    for role in assignments.values():
        role_counts[role] = role_counts.get(role, 0) + 1
        
    for role, count in role_counts.items():
        if count > 3:  # Слишком много задач на одну роль
            conflicts.append(f"Перегрузка роли {role}: {count} задач")
            
    return conflicts

def _create_task_timeline(tasks: List[Dict[str, Any]], deps) -> Dict[str, str]:
    """Создать временные рамки задач."""
    if not tasks:
        return {}
        
    earliest_start = min(task.get('estimated_start', datetime.now().isoformat()) for task in tasks)
    latest_end = max(
        (datetime.fromisoformat(task.get('estimated_start', datetime.now().isoformat())) + 
         timedelta(days=task.get('estimated_days', 3))).isoformat() 
        for task in tasks
    )
    
    return {
        'start_date': earliest_start,
        'end_date': latest_end,
        'total_duration_days': (datetime.fromisoformat(latest_end) - datetime.fromisoformat(earliest_start)).days
    }

def _calculate_progress_metrics(project_data: Dict[str, Any]) -> Dict[str, float]:
    """Рассчитать метрики прогресса."""
    return {
        'completion_percentage': (project_data.get('completed_tasks', 0) / project_data.get('total_tasks', 1)) * 100,
        'velocity': project_data.get('current_velocity', 0.0),
        'velocity_variance': abs(project_data.get('current_velocity', 0.0) - project_data.get('planned_velocity', 0.0)),
        'team_utilization': project_data.get('team_utilization', 0.0)
    }

def _analyze_progress_trends(project_data: Dict[str, Any]) -> Dict[str, str]:
    """Анализировать тренды прогресса."""
    return {
        'velocity_trend': 'increasing' if project_data.get('current_velocity', 0) > project_data.get('planned_velocity', 0) else 'stable',
        'quality_trend': 'stable',
        'team_satisfaction_trend': 'improving'
    }

def _forecast_project_completion(project_data: Dict[str, Any], deps) -> Dict[str, str]:
    """Прогнозировать завершение проекта."""
    remaining_tasks = project_data.get('total_tasks', 0) - project_data.get('completed_tasks', 0)
    current_velocity = project_data.get('current_velocity', 1.0)
    
    estimated_weeks = remaining_tasks / current_velocity if current_velocity > 0 else float('inf')
    completion_date = datetime.now() + timedelta(weeks=estimated_weeks)
    
    return {
        'estimated_completion': completion_date.isoformat(),
        'confidence_level': 'medium',
        'remaining_tasks': remaining_tasks,
        'estimated_weeks': round(estimated_weeks, 1)
    }

def _generate_progress_recommendations(metrics: Dict[str, float], trends: Dict[str, str], deps) -> List[str]:
    """Генерировать рекомендации по прогрессу."""
    recommendations = []
    
    if metrics.get('velocity_variance', 0) > 0.5:
        recommendations.append("Стабилизировать скорость выполнения задач")
    
    if metrics.get('team_utilization', 0) > 90:
        recommendations.append("Рассмотреть снижение нагрузки на команду")
    elif metrics.get('team_utilization', 0) < 70:
        recommendations.append("Увеличить загрузку команды дополнительными задачами")
        
    return recommendations

def _get_relevant_methodologies(query: str, deps) -> List[str]:
    """Получить релевантные методологии."""
    if 'agile' in query.lower():
        return ['Scrum', 'Kanban', 'SAFe']
    elif 'waterfall' in query.lower():
        return ['Traditional PM', 'PRINCE2']
    else:
        return ['Agile', 'Lean', 'Hybrid']

def _define_expected_deliverables(task_type: str) -> List[str]:
    """Определить ожидаемые результаты для типа задачи."""
    deliverables_map = {
        'analysis': ['Технические требования', 'Аналитический отчет'],
        'architecture': ['Архитектурная диаграмма', 'Техническая спецификация'],
        'implementation': ['Рабочий код', 'Unit тесты', 'Документация API'],
        'testing': ['План тестирования', 'Отчет о тестировании', 'Bug report']
    }
    
    return deliverables_map.get(task_type, ['Выполненная задача', 'Отчет о выполнении'])

def _create_coordination_plan(assigned_role: str, deps) -> Dict[str, Any]:
    """Создать план координации с назначенной ролью."""
    return {
        'assigned_role': assigned_role,
        'check_in_frequency': 'daily' if deps.daily_standup_enabled else 'weekly',
        'escalation_path': 'Project Manager',
        'collaboration_tools': ['Archon', 'Daily standups', 'Status reports']
    }